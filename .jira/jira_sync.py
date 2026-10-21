#!/usr/bin/env python3
"""Sync epic markdown files (docs/backlog/*.md) to Jira Cloud.

Commands
  validate  Check every epic file and print the plan. Needs no Jira access.
  sync      Validate, then create/update issues in Jira and write issue keys
            back into the markdown files.
  doctor    Check the Jira connection, issue types, fields and team members.
  import    Write Jira issues that no markdown file has yet into epic files
            (new files for epics, "_imported-unsorted.md" for issues without an epic).

Environment
  JIRA_BASE_URL     e.g. https://your-team.atlassian.net
  JIRA_EMAIL        Jira login email of the API token owner
  JIRA_API_TOKEN    API token (https://id.atlassian.com/manage-profile/security/api-tokens)
  JIRA_PROJECT_KEY  e.g. DI
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import time
from types import SimpleNamespace
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Optional

import yaml

try:
    import requests
except ImportError:  # validate works without requests
    requests = None

# --------------------------------------------------------------------------
# Markdown parsing
# --------------------------------------------------------------------------

KEY_RE = re.compile(r"\b([A-Z][A-Z0-9_]+-\d+)\b")
PIPE_RE = re.compile(r"(?<!\\)\|")
COMMENT_RE = re.compile(r"<!--.*?-->", re.S)
SEP_RE = re.compile(r"^\|?\s*:?-+:?\s*(\|\s*:?-+:?\s*)*\|?\s*$")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
STORY_HEADING_RE = re.compile(r"^##\s+(S?\d+)\b\s*[·:\-–—.]?\s*(.*)$", re.I)
MARKER_RE = re.compile(
    r"^\s*(?:\*\*|#{3,6}\s+)\s*(acceptance criteria|sub-?tasks|tasks|details)\s*:?\s*(?:\*\*)?\s*:?\s*$",
    re.I,
)
LIST_RE = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+(.*)$")
STORY_FORMAT_RE = re.compile(r"\bas an?\b.+\bi want\b.+\bso that\b", re.I | re.S)
OTHER_TASKS_TITLES = ("other tasks", "epic tasks", "tasks")
ITEM_COLUMNS = {"task", "sub task", "subtask", "owner", "assignee", "points", "estimate", "jira", "sprint"}
ESTIMATE_RE = re.compile(r"^\d+(\.\d+)?[wdhm](\s+\d+(\.\d+)?[wdhm])*$")


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9# ]", " ", s.lower())).strip()


def plain(s: str) -> str:
    """Strip simple markdown emphasis from a cell value."""
    s = re.sub(r"(\*\*|__)(.+?)\1", r"\2", s)
    s = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"\1", s)
    return s.replace("<br>", " ").replace("<br/>", " ").strip()


def split_row(line: str) -> list[str]:
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|") and not s.endswith("\\|"):
        s = s[:-1]
    return [c.strip().replace("\\|", "|") for c in PIPE_RE.split(s)]


@dataclass
class Table:
    header_line: int
    header: list[str]
    rows: list[tuple[int, list[str]]]  # (line index, cells)

    def col(self, *names: str) -> Optional[int]:
        normed = [norm(h) for h in self.header]
        for n in names:
            if n in normed:
                return normed.index(n)
        return None


def table_at(lines: list[str], i: int) -> Optional[Table]:
    if i + 1 >= len(lines):
        return None
    if not lines[i].strip().startswith("|") or not SEP_RE.match(lines[i + 1].strip()):
        return None
    header = split_row(lines[i])
    rows = []
    j = i + 2
    while j < len(lines) and lines[j].strip().startswith("|"):
        rows.append((j, split_row(lines[j])))
        j += 1
    return Table(i, header, rows)


def first_table(lines: list[str], start: int, end: int) -> Optional[Table]:
    for i in range(start, end):
        t = table_at(lines, i)
        if t:
            return t
    return None


def cell(cells: list[str], idx: Optional[int]) -> str:
    if idx is None or idx >= len(cells):
        return ""
    return cells[idx].strip()


def key_in(s: str) -> Optional[str]:
    m = KEY_RE.search(s or "")
    return m.group(1) if m else None


def parse_points(s: str):
    s = re.sub(r"(?i)\s*(sp|pts?|points?)$", "", plain(s)).strip()
    if s in ("", "-", "—", "–"):
        return None
    try:
        v = float(s)
    except ValueError:
        return "invalid"
    return int(v) if v.is_integer() else v


@dataclass
class Item:
    kind: str  # "subtask" or "task"
    title: str
    owner: str
    estimate: str
    points: object
    key: Optional[str]
    line: int
    jira_col: Optional[int]
    sprint: str = ""


@dataclass
class Story:
    sid: str
    title: str
    description: str
    priority: str
    points: object
    notes: str
    key: Optional[str]
    line: int
    jira_col: Optional[int]
    ac: list[str] = field(default_factory=list)
    breakdown: Optional[str] = None  # "subtasks" | "tasks" | None
    both_breakdowns: bool = False
    items: list[Item] = field(default_factory=list)
    has_section: bool = False
    sprint: str = ""
    owner: str = ""
    details: list[str] = field(default_factory=list)
    section_end: int = 0
    item_table: Optional[Table] = None


@dataclass
class Epic:
    path: Path
    rel: str
    lines: list[str]
    name: str = ""
    summary: str = ""
    owner: str = ""
    designer: str = ""
    developers: str = ""
    release: str = ""
    owner_handle: str = ""
    key: Optional[str] = None
    key_line: Optional[int] = None
    key_col: int = 1
    stories: list[Story] = field(default_factory=list)
    tasks: list[Item] = field(default_factory=list)  # epic-level tasks ("## Other tasks")
    details: list[str] = field(default_factory=list)
    req_table: Optional[Table] = None
    other_start: Optional[int] = None
    other_table: Optional[Table] = None
    problems: list[tuple[str, int, str]] = field(default_factory=list)  # (level, line, msg)
    dirty: bool = False

    def err(self, line: int, msg: str):
        self.problems.append(("error", line, msg))

    def warn(self, line: int, msg: str):
        self.problems.append(("warning", line, msg))

    @property
    def errors(self):
        return [p for p in self.problems if p[0] == "error"]

    def set_cell(self, line: int, col: int, value: str):
        raw = self.lines[line]
        cr = "\r" if raw.endswith("\r") else ""
        raw = raw.rstrip("\r")
        indent = raw[: len(raw) - len(raw.lstrip())]
        s = raw.strip()
        if s.startswith("|"):
            s = s[1:]
        if s.endswith("|") and not s.endswith("\\|"):
            s = s[:-1]
        parts = PIPE_RE.split(s)
        while len(parts) <= col:
            parts.append(" ")
        parts[col] = f" {value} "
        self.lines[line] = indent + "|" + "|".join(parts) + "|" + cr
        self.dirty = True

    def save(self):
        if self.dirty:
            self.path.write_text("\n".join(self.lines), encoding="utf-8")
            self.dirty = False


def norm_id(s: str) -> str:
    s = plain(s).upper()
    return s if s.startswith("S") else "S" + s


def collect_details(clean: list[str], start: int, end: int, used_tables: set[int]) -> tuple[list[str], int]:
    """Free text after a **Details** marker, up to the next marker or `end`. Returns (lines, stop index)."""
    j = start
    while j < end and not MARKER_RE.match(clean[j]):
        if table_at(clean, j):
            used_tables.add(j)
        j += 1
    block = clean[start:j]
    while block and not block[0].strip():
        block.pop(0)
    while block and not block[-1].strip():
        block.pop()
    return block, j


def parse_epic(path: Path, rel: str) -> Epic:
    text = path.read_text(encoding="utf-8")
    lines = text.split("\n")
    clean_text = COMMENT_RE.sub(lambda m: "\n" * m.group(0).count("\n"), text)
    clean = clean_text.split("\n")
    ep = Epic(path=path, rel=rel, lines=lines)

    headings = [(i, len(m.group(1)), m.group(2)) for i, l in enumerate(clean) if (m := HEADING_RE.match(l))]
    req_i = next((i for i, lvl, t in headings if lvl == 2 and norm(t) == "requirements"), None)

    # --- header table (first table before ## Requirements) ---
    used_tables: set[int] = set()
    used_markers: set[int] = set()
    ht = first_table(clean, 0, req_i if req_i is not None else len(clean))
    if ht:
        used_tables.add(ht.header_line)
    if not ht:
        ep.err(1, "Missing the epic table (| Epic | ... |) at the top of the file.")
    else:
        kv = [(ht.header_line, ht.header)] + ht.rows
        for line, cells in kv:
            k = norm(cell(cells, 0))
            v = cell(cells, 1)
            if k == "epic":
                ep.name = plain(v)
            elif k in ("summary", "epic summary", "description"):
                ep.summary = plain(v)
            elif k == "document owner":
                ep.owner = v
            elif k == "designer":
                ep.designer = v
            elif k == "developers":
                ep.developers = v
            elif k.startswith("release target"):
                ep.release = plain(v)
            elif k == "jira":
                ep.key, ep.key_line = key_in(v), line
        if not ep.name:
            ep.err(ht.header_line + 1, "The Epic row is empty: give the epic a name.")
        if ep.key_line is None:
            ep.err(ht.header_line + 1, "The epic table needs a 'Jira' row (leave its value empty).")
    hdr_end = req_i if req_i is not None else len(clean)
    for i in range(hdr_end):
        mm = MARKER_RE.match(clean[i])
        if mm and mm.group(1).lower() == "details":
            used_markers.add(i)
            ep.details, _ = collect_details(clean, i + 1, hdr_end, used_tables)
            break

    # --- requirements table ---
    if req_i is None:
        ep.err(1, "Missing the '## Requirements' section.")
        return ep
    next_h = next((i for i, lvl, _ in headings if i > req_i and lvl <= 2), len(clean))
    rt = first_table(clean, req_i, next_h)
    if not rt:
        ep.err(req_i + 1, "The Requirements section has no table.")
        return ep
    used_tables.add(rt.header_line)
    ep.req_table = rt
    c_id = rt.col("#", "id")
    c_title = rt.col("user story title", "title")
    c_desc = rt.col("user story description", "description")
    c_prio = rt.col("priority")
    c_pts = rt.col("points", "story points")
    c_notes = rt.col("notes")
    c_jira = rt.col("jira")
    c_sprint = rt.col("sprint", "target sprint")
    c_owner = rt.col("owner", "assignee")
    for name, c in (("#", c_id), ("User story title", c_title), ("User story description", c_desc), ("Jira", c_jira)):
        if c is None:
            ep.err(rt.header_line + 1, f"The Requirements table needs a '{name}' column.")
    if c_id is None or c_title is None:
        return ep
    seen = {}
    for line, cells in rt.rows:
        if not any(plain(c) for i, c in enumerate(cells) if i != c_id):
            continue  # empty template row
        sid = norm_id(cell(cells, c_id)) if cell(cells, c_id) else ""
        if not re.fullmatch(r"S\d+", sid):
            ep.err(line + 1, f"Story id '{cell(cells, c_id)}' should look like S1, S2, ...")
            continue
        if sid in seen:
            ep.err(line + 1, f"Story id {sid} is used twice.")
            continue
        st = Story(
            sid=sid,
            title=plain(cell(cells, c_title)),
            description=plain(cell(cells, c_desc)),
            priority=plain(cell(cells, c_prio)),
            points=parse_points(cell(cells, c_pts)),
            notes=plain(cell(cells, c_notes)),
            key=key_in(cell(cells, c_jira)),
            line=line,
            jira_col=c_jira,
            sprint=plain(cell(cells, c_sprint)),
            owner=plain(cell(cells, c_owner)).lstrip("@"),
        )
        seen[sid] = st
        ep.stories.append(st)

    # --- story sections ---
    sections = [(i, m) for i, lvl, t in headings if lvl == 2 and (m := STORY_HEADING_RE.match(clean[i]))]
    for n, (start, m) in enumerate(sections):
        sid = norm_id(m.group(1))
        end = next((i for i, lvl, _ in headings if i > start and lvl <= 2), len(clean))
        st = seen.get(sid)
        if not st:
            ep.err(start + 1, f"Section '{clean[start].strip()}' has no row with id {sid} in the Requirements table.")
            continue
        if st.has_section:
            ep.err(start + 1, f"Story {sid} has two sections.")
            continue
        st.has_section = True
        st.section_end = end
        mode = None
        i = start + 1
        while i < end:
            l = clean[i]
            mm = MARKER_RE.match(l)
            if mm:
                used_markers.add(i)
                word = mm.group(1).lower().replace("-", "")
                if word == "details":
                    st.details, i = collect_details(clean, i + 1, end, used_tables)
                    mode = None
                    continue
                mode = "ac" if word.startswith("acceptance") else ("subtasks" if word == "subtasks" else "tasks")
                if mode in ("subtasks", "tasks"):
                    if st.breakdown and st.breakdown != mode:
                        st.both_breakdowns = True
                    st.breakdown = mode
                    t = first_table(clean, i + 1, end)
                    if not t:
                        ep.err(i + 1, f"{st.sid}: '{l.strip()}' has no table under it.")
                    if t:
                        used_tables.add(t.header_line)
                        st.item_table = t
                        parse_items(ep, st, t, mode)
                        i = t.rows[-1][0] + 1 if t.rows else t.header_line + 2
                        mode = None
                        continue
                i += 1
                continue
            if mode == "ac":
                lm = LIST_RE.match(l)
                if lm and lm.group(1).strip():
                    st.ac.append(lm.group(1).strip())
                elif l.strip() and st.ac and l.startswith((" ", "\t")):
                    st.ac[-1] += " " + l.strip()
            i += 1

    # --- epic-level tasks: "## Other tasks" ---
    other = [i for i, lvl, t in headings if lvl == 2 and norm(t) in OTHER_TASKS_TITLES]
    for n, start in enumerate(other):
        end = next((i for i, lvl, _ in headings if i > start and lvl <= 2), len(clean))
        if n > 0:
            ep.err(start + 1, "Only one '## Other tasks' section per epic file.")
            continue
        t = first_table(clean, start + 1, end)
        if not t:
            ep.err(start + 1, "'## Other tasks' has no table under it.")
            continue
        used_tables.add(t.header_line)
        ep.other_start, ep.other_table = start, t
        holder = SimpleNamespace(sid="Other tasks", items=ep.tasks)
        if t.col("estimate", "original estimate") is not None and t.col("points", "story points") is None:
            ep.err(t.header_line + 1, "Other tasks are Tasks, not sub-tasks: use a Points column instead of Estimate.")
        parse_items(ep, holder, t, "tasks")

    # --- nothing may be silently ignored ---
    for i, l in enumerate(clean):
        if MARKER_RE.match(l) and i not in used_markers:
            ep.err(i + 1, f"'{l.strip()}' is outside a story section, so the sync ignores it. "
                          f"Move it under a '## S<n> · title' heading, or put epic-level tasks under '## Other tasks'.")
    i = 0
    while i < len(clean):
        t = table_at(clean, i)
        if not t:
            i += 1
            continue
        if t.header_line not in used_tables:
            cols = {norm(h) for h in t.header}
            if cols & ITEM_COLUMNS:
                ep.err(i + 1, "This table is not read by the sync, so its rows would never reach Jira. "
                              "Tasks go under '**Tasks**' in a story section or under '## Other tasks'.")
            else:
                ep.warn(i + 1, "This table is not read by the sync (fine if it is only for reading).")
        i = (t.rows[-1][0] if t.rows else t.header_line + 1) + 1
    return ep


def parse_items(ep: Epic, st: Story, t: Table, mode: str):
    c_title = t.col("sub task", "subtask", "task", "title")
    c_owner = t.col("owner", "assignee")
    c_est = t.col("estimate", "original estimate")
    c_pts = t.col("points", "story points")
    c_jira = t.col("jira")
    c_sprint = t.col("sprint", "target sprint")
    if c_title is None:
        ep.err(t.header_line + 1, f"{st.sid}: the table needs a '{'Sub-task' if mode == 'subtasks' else 'Task'}' column.")
        return
    if c_jira is None:
        ep.err(t.header_line + 1, f"{st.sid}: the table needs a 'Jira' column.")
    for line, cells in t.rows:
        if not any(plain(c) for i, c in enumerate(cells) if i != c_jira):
            continue
        st.items.append(
            Item(
                kind="subtask" if mode == "subtasks" else "task",
                title=plain(cell(cells, c_title)),
                owner=plain(cell(cells, c_owner)).lstrip("@"),
                estimate=plain(cell(cells, c_est)),
                points=parse_points(cell(cells, c_pts)) if c_pts is not None else None,
                key=key_in(cell(cells, c_jira)),
                line=line,
                jira_col=c_jira,
                sprint=plain(cell(cells, c_sprint)) if mode == "tasks" else "",
            )
        )
        if mode == "subtasks" and plain(cell(cells, c_sprint)):
            ep.err(line + 1, f"{st.sid}: sub-tasks always follow their story's sprint. Remove the Sprint value or use a Tasks table.")
        if mode == "subtasks" and c_pts is not None and plain(cell(cells, c_pts)):
            ep.err(line + 1, f"{st.sid}: sub-tasks don't carry points. Put the points on the story or use a Tasks table.")


# --------------------------------------------------------------------------
# Validation
# --------------------------------------------------------------------------


def validate(ep: Epic, cfg: dict, team: dict):
    scale = set(cfg["points_scale"])
    prios = {p.lower(): p for p in cfg["priorities"]}
    keys = {}

    def check_key(k, line):
        if k:
            if k in keys:
                ep.err(line + 1, f"Jira key {k} appears twice (also on line {keys[k] + 1}).")
            keys[k] = line

    check_key(ep.key, ep.key_line or 0)
    owner = plain(ep.owner)
    if owner:
        handles = re.findall(r"@([\w.-]+)", owner)
        if len(handles) > 1 or re.search(r"[,;&]", owner):
            ep.err(1, "Document Owner: name one person; Jira has a single assignee.")
        elif not handles:
            ep.warn(1, f"Document Owner '{owner}' is not a GitHub handle (@name); the epic stays unassigned in Jira.")
        elif handles[0] not in team:
            ep.err(1, f"Document Owner @{handles[0]} is not in .jira/team.yml.")
        else:
            ep.owner_handle = handles[0]
    def check_items(sid, items):
        for it in items:
            IL = it.line + 1
            check_key(it.key, it.line)
            if not it.title:
                ep.err(IL, f"{sid}: a {it.kind} row has no title.")
            if it.owner:
                if re.search(r"[,;&]|\s", it.owner):
                    ep.err(IL, f"{sid}: '{it.title}' can have only one owner.")
                elif it.owner not in team:
                    ep.err(IL, f"{sid}: owner @{it.owner} is not in .jira/team.yml.")
            if it.kind == "subtask" and it.estimate and not ESTIMATE_RE.match(it.estimate):
                ep.err(IL, f"{sid}: estimate '{it.estimate}' should look like 4h, 1d or 1d 4h.")
            if it.kind == "task":
                if it.points is None:
                    ep.warn(IL, f"{sid}: task '{it.title}' has no points yet.")
                elif it.points == "invalid" or it.points not in scale:
                    (ep.warn if it.key and it.points != "invalid" else ep.err)(IL, f"{sid}: points '{it.points}' on '{it.title}' are not on the scale {sorted(scale)}.")

    if not ep.stories and not ep.tasks and not ep.errors:
        ep.warn(1, "No stories yet.")
    check_items("Other tasks", ep.tasks)
    for st in ep.stories:
        L = st.line + 1
        check_key(st.key, st.line)
        if not st.title:
            ep.err(L, f"{st.sid}: title is empty.")
        if not st.description:
            (ep.warn if st.key else ep.err)(L, f"{st.sid}: description is empty.")
        elif not STORY_FORMAT_RE.search(st.description):
            ep.warn(L, f"{st.sid}: description doesn't follow 'As a <role>, I want <goal>, so that <benefit>'.")
        if st.owner:
            if re.search(r"[,;&]|\s", st.owner):
                ep.err(L, f"{st.sid}: a story can have only one owner.")
            elif st.owner not in team:
                ep.err(L, f"{st.sid}: owner @{st.owner} is not in .jira/team.yml.")
        if st.priority and st.priority.lower() not in prios:
            ep.err(L, f"{st.sid}: priority '{st.priority}' is not one of {', '.join(cfg['priorities'])}.")
        elif st.priority:
            st.priority = prios[st.priority.lower()]
        if st.points == "invalid" or (st.points is not None and st.points not in scale):
            (ep.warn if st.key and st.points != "invalid" else ep.err)(L, f"{st.sid}: points '{st.points}' are not on the scale {sorted(scale)}.")
        if not st.has_section:
            ep.err(L, f"{st.sid}: add a section '## {st.sid} · {st.title}' with its acceptance criteria.")
            continue
        if not st.ac:
            ep.warn(L, f"{st.sid}: no acceptance criteria.")
        if st.both_breakdowns:
            ep.err(L, f"{st.sid}: use either a Sub-tasks table or a Tasks table, not both.")
        if st.breakdown == "tasks":
            if st.points is not None:
                ep.err(L, f"{st.sid}: this story uses Tasks, so the tasks carry the points. Leave the story's Points cell empty.")
        elif st.points is None:
            ep.warn(L, f"{st.sid}: no story points yet.")
        check_items(st.sid, st.items)


# --------------------------------------------------------------------------
# Reports
# --------------------------------------------------------------------------


def problems_md(epics: list[Epic]) -> str:
    out = []
    for ep in epics:
        for level, line, msg in sorted(ep.problems, key=lambda p: (p[0] != "error", p[1])):
            icon = "❌" if level == "error" else "⚠️"
            out.append(f"- {icon} `{ep.rel}:{line}` {msg}")
    return "\n".join(out)


def target_sprint(ep: Epic, st: Optional[Story], it: Optional[Item] = None) -> str:
    """Sprint an issue is placed in when it is created: row value, then story, then epic Release Target."""
    if it is not None and it.sprint:
        return it.sprint
    return (st.sprint if st else "") or ep.release


def plan_md(epics: list[Epic]) -> str:
    out = []
    act = lambda k: f"sync {k}" if k else "create"

    def spr(key, target):
        if key:
            return "(managed in Jira)"
        return target or "backlog"

    for ep in epics:
        if ep.errors:
            continue
        owner = f", owner @{ep.owner_handle}" if ep.owner_handle else ""
        out.append(f"\n**{ep.rel}**: epic *{ep.name}* ({act(ep.key)}{owner})\n")
        out.append("| Item | Type | Points / estimate | Owner | Sprint | Action |")
        out.append("|---|---|---|---|---|---|")
        for st in ep.stories:
            model = {"subtasks": "story + sub-tasks", "tasks": "story + tasks"}.get(st.breakdown, "story")
            pts = st.points if st.points is not None else "—"
            sown = f"@{st.owner}" if st.owner else ""
            out.append(f"| {st.sid} {st.title} | {model} | {pts} | {sown} | {spr(st.key, target_sprint(ep, st))} | {act(st.key)} |")
            for it in st.items:
                size = (it.estimate or "—") if it.kind == "subtask" else (it.points if it.points is not None else "—")
                typ = "sub-task" if it.kind == "subtask" else f"task, blocks {st.sid}"
                own = f"@{it.owner}" if it.owner else ""
                sp = "with its story" if it.kind == "subtask" else spr(it.key, target_sprint(ep, st, it))
                out.append(f"| ↳ {it.title} | {typ} | {size} | {own} | {sp} | {act(it.key)} |")
        for it in ep.tasks:
            pts = it.points if it.points is not None else "—"
            own = f"@{it.owner}" if it.owner else ""
            out.append(f"| {it.title} | task (epic level) | {pts} | {own} | {spr(it.key, target_sprint(ep, None, it))} | {act(it.key)} |")
    return "\n".join(out)


def write_report(path: Optional[str], text: str):
    print(text)
    if path:
        Path(path).write_text(text, encoding="utf-8")
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as f:
            f.write(text + "\n")


# --------------------------------------------------------------------------
# Jira client
# --------------------------------------------------------------------------


class JiraError(Exception):
    def __init__(self, method, path, status, body):
        detail = body
        try:
            j = json.loads(body)
            msgs = list(j.get("errorMessages", [])) + [f"{k}: {v}" for k, v in (j.get("errors") or {}).items()]
            if msgs:
                detail = "; ".join(msgs)
        except Exception:
            detail = (body or "")[:300]
        super().__init__(f"{method} {path} -> HTTP {status}: {detail}")
        self.status = status


class Jira:
    def __init__(self, base: str, email: str, token: str):
        if requests is None:
            sys.exit("The 'requests' package is required: pip install -r .jira/requirements.txt")
        self.base = base.rstrip("/")
        self.s = requests.Session()
        self.s.auth = (email, token)
        self.s.headers.update({"Accept": "application/json", "Content-Type": "application/json"})

    def req(self, method: str, path: str, **kw):
        for attempt in range(5):
            r = self.s.request(method, self.base + path, timeout=30, **kw)
            if (r.status_code == 429 or r.status_code >= 500) and attempt < 4:
                time.sleep(float(r.headers.get("Retry-After") or 2 ** attempt))
                continue
            break
        if r.status_code >= 400:
            raise JiraError(method, path, r.status_code, r.text)
        return r.json() if r.content else None

    def get(self, path, **kw):
        return self.req("GET", path, **kw)

    def post(self, path, **kw):
        return self.req("POST", path, **kw)

    def put(self, path, **kw):
        return self.req("PUT", path, **kw)

    def delete(self, path, **kw):
        return self.req("DELETE", path, **kw)


class Meta:
    """What the Jira project offers: issue types and the fields each one accepts."""

    def __init__(self, jira: Jira, project: str, cfg: dict):
        self.jira, self.project, self.cfg = jira, project, cfg
        self.proj = jira.get(f"/rest/api/3/project/{project}")
        types = self.proj.get("issueTypes", [])
        names = cfg["issue_types"]

        def by_name(n):
            return next((t for t in types if t["name"].lower() == n.lower() and not t.get("subtask")), None)

        self.types = {
            "epic": by_name(names["epic"]) or next((t for t in types if t.get("hierarchyLevel") == 1), None),
            "story": by_name(names["story"]),
            "task": by_name(names["task"]),
            "subtask": next((t for t in types if t.get("subtask")), None),
        }
        self.all_fields = jira.get("/rest/api/3/field")
        self._fields: dict[str, dict] = {}

    def fields(self, kind: str) -> dict:
        """fieldId -> createmeta entry for this issue type."""
        if kind in self._fields:
            return self._fields[kind]
        t = self.types.get(kind)
        out: dict = {}
        if t:
            start = 0
            while True:
                d = self.jira.get(
                    f"/rest/api/3/issue/createmeta/{self.project}/issuetypes/{t['id']}",
                    params={"startAt": start, "maxResults": 100},
                )
                fl = d.get("fields") or d.get("results") or d.get("values") or []
                for f in fl:
                    out[f.get("fieldId") or f.get("key")] = f
                start += len(fl)
                if not fl or start >= d.get("total", start):
                    break
        self._fields[kind] = out
        return out

    def field_ids(self, name_or_id: str) -> list[str]:
        if name_or_id.startswith("customfield_"):
            return [name_or_id]
        return [f["id"] for f in self.all_fields if f["name"].lower() == name_or_id.lower()]

    def find_field(self, setting: str, defaults: list[str], kind: str) -> Optional[str]:
        names = defaults if setting == "auto" else [setting]
        available = self.fields(kind)
        for n in names:
            for fid in self.field_ids(n):
                if fid in available:
                    return fid
        return None

    def points_field(self, kind: str) -> Optional[str]:
        return self.find_field(self.cfg["story_points_field"], ["Story point estimate", "Story Points"], kind)

    def ac_field(self) -> Optional[tuple[str, bool]]:
        name = str(self.cfg.get("acceptance_criteria_field") or "none")
        if name.lower() == "none":
            return None
        fid = self.find_field(name, [name], "story")
        if not fid:
            return None
        f = next((f for f in self.all_fields if f["id"] == fid), {})
        is_rich = "textarea" in (f.get("schema", {}).get("custom") or "")
        return fid, is_rich


# --------------------------------------------------------------------------
# Atlassian Document Format helpers
# --------------------------------------------------------------------------

LINK_RE = re.compile(r"\[([^\]]+)\]\((https?://[^)\s]+)\)|(https?://[^\s)]+)")


def inline(s: str, marks: Optional[list] = None) -> list[dict]:
    nodes, pos = [], 0
    for m in LINK_RE.finditer(s):
        if m.start() > pos:
            nodes.append({"type": "text", "text": s[pos : m.start()]})
        text, url = (m.group(1), m.group(2)) if m.group(1) else (m.group(3), m.group(3))
        nodes.append({"type": "text", "text": text, "marks": [{"type": "link", "attrs": {"href": url}}]})
        pos = m.end()
    if pos < len(s):
        nodes.append({"type": "text", "text": s[pos:]})
    if marks:
        for n in nodes:
            n["marks"] = n.get("marks", []) + marks
    return [n for n in nodes if n["text"]]


def para(s: str, marks=None) -> Optional[dict]:
    s = plain(s)
    return {"type": "paragraph", "content": inline(s, marks)} if s else None


def heading(s: str, level: int = 3) -> dict:
    return {"type": "heading", "attrs": {"level": level}, "content": [{"type": "text", "text": s}]}


def bullets(items: list[str]) -> Optional[dict]:
    items = [plain(i) for i in items if plain(i)]
    if not items:
        return None
    return {
        "type": "bulletList",
        "content": [{"type": "listItem", "content": [{"type": "paragraph", "content": inline(i)}]} for i in items],
    }


def adf(*blocks) -> dict:
    content = []
    for b in blocks:
        if isinstance(b, list):
            content += [x for x in b if x]
        elif b:
            content.append(b)
    return {"type": "doc", "version": 1, "content": content or [{"type": "paragraph", "content": []}]}


BULLET_RE = re.compile(r"^\s*[-*+]\s+(.*)$")
ORDERED_RE = re.compile(r"^\s*\d+[.)]\s+(.*)$")


def md_to_adf(lines: list[str]) -> list[dict]:
    """Turn the simple markdown of a **Details** block into ADF blocks."""
    out: list = []
    i, n = 0, len(lines)

    def starts_block(l):
        t = l.strip()
        return t.startswith("```") or t.startswith(">") or re.match(r"^#{1,6}\s", t) or BULLET_RE.match(l) or ORDERED_RE.match(l)

    while i < n:
        l = lines[i]
        t = l.strip()
        if not t:
            i += 1
            continue
        if t.startswith("```"):
            j, code = i + 1, []
            while j < n and not lines[j].strip().startswith("```"):
                code.append(lines[j])
                j += 1
            node = {"type": "codeBlock", "content": [{"type": "text", "text": "\n".join(code)}] if any(code) else []}
            out.append(node)
            i = j + 1
            continue
        m = re.match(r"^(#{1,6})\s+(.*)$", t)
        if m:
            if plain(m.group(2)):
                out.append(heading(plain(m.group(2)), len(m.group(1))))
            i += 1
            continue
        if BULLET_RE.match(l) or ORDERED_RE.match(l):
            ordered = not BULLET_RE.match(l)
            items: list[str] = []
            while i < n and lines[i].strip():
                mm = BULLET_RE.match(lines[i]) or ORDERED_RE.match(lines[i])
                if mm:
                    items.append(mm.group(1))
                elif items and not starts_block(lines[i]):
                    items[-1] += " " + lines[i].strip()
                else:
                    break
                i += 1
            content = [{"type": "listItem", "content": [{"type": "paragraph", "content": inline(plain(x))}]}
                       for x in items if plain(x)]
            if content:
                node = {"type": "orderedList", "attrs": {"order": 1}, "content": content} if ordered \
                    else {"type": "bulletList", "content": content}
                out.append(node)
            continue
        if t.startswith(">"):
            q = []
            while i < n and lines[i].strip().startswith(">"):
                q.append(lines[i].strip()[1:].strip())
                i += 1
            p_ = para(" ".join(q))
            if p_:
                out.append({"type": "blockquote", "content": [p_]})
            continue
        buf = []
        while i < n and lines[i].strip() and not (buf and starts_block(lines[i])):
            buf.append(lines[i].strip())
            i += 1
        out.append(para(" ".join(buf)))
    return [b for b in out if b]


# --------------------------------------------------------------------------
# Board and sprints
# --------------------------------------------------------------------------


class Sprints:
    """Finds the team's Scrum board and matches sprint names like 'Sprint 3' or 'DI Sprint 3'."""

    def __init__(self, jira: Jira, project: str, cfg: dict):
        self.jira, self.project, self.cfg = jira, project, cfg
        self.board: Optional[dict] = None
        self.sprints: Optional[list[dict]] = None
        self.error = ""
        self.note = ""

    def _all(self, path: str, params: dict) -> list[dict]:
        out, start = [], 0
        while True:
            d = self.jira.get(path, params={**params, "startAt": start, "maxResults": 50})
            vals = d.get("values", [])
            out += vals
            start += len(vals)
            if d.get("isLast", True) or not vals:
                return out

    def load(self):
        if self.sprints is not None:
            return
        self.sprints = []
        bid = str(self.cfg.get("board_id") or "auto")
        try:
            if bid.lower() == "auto":
                boards = self._all("/rest/agile/1.0/board", {"projectKeyOrId": self.project})
            else:
                boards = [self.jira.get(f"/rest/agile/1.0/board/{bid}")]
        except JiraError as e:
            self.error = f"could not read the project's boards ({e})"
            return
        if not boards:
            self.error = (f"no board found for project {self.project}; the token owner may not have access to it "
                          f"(or set board_id in .jira/config.yml)")
            return
        # Company-managed Scrum boards report type "scrum"; team-managed boards report "simple".
        order = {"scrum": 0, "simple": 1}
        candidates = sorted(boards, key=lambda b: order.get(b.get("type"), 2))
        tried = []
        for b in candidates:
            try:
                self.sprints = self._all(f"/rest/agile/1.0/board/{b['id']}/sprint", {"state": "active,future,closed"})
                self.board = b
                break
            except JiraError as e:
                reason = "sprints are turned off" if e.status == 400 else f"HTTP {e.status}"
                tried.append(f"{b.get('name')} (id {b.get('id')}, {b.get('type')}: {reason})")
        if not self.board:
            self.sprints = []
            self.error = ("no board with sprints found. Boards checked: " + "; ".join(tried) +
                          ". Turn on sprints for the board in Jira, or set board_id in .jira/config.yml")
            return
        usable = [b for b in candidates if b.get("type") in order]
        if bid.lower() == "auto" and len(usable) > 1:
            names = ", ".join(f"{b['name']} (id {b['id']})" for b in usable)
            self.note = f"Several boards found ({names}); using {self.board['name']}. Set board_id in .jira/config.yml to choose."

    def resolve(self, target: str) -> tuple[Optional[dict], str]:
        """Return (open sprint, '') or (None, reason)."""
        self.load()
        if self.error:
            return None, self.error
        t = target.strip()
        hits = [sp for sp in self.sprints if sp["name"].strip().lower() == t.lower()]
        if not hits:
            rest = re.sub(rf"^{re.escape(self.project)}\s+", "", t, flags=re.I)
            m = re.search(r"\d+", rest)
            if m:
                n = int(m.group(0))
                pat = re.compile(rf"^(?:{re.escape(self.project)}\s+)?sprint\s*0*{n}$", re.I)
                hits = [sp for sp in self.sprints if pat.match(sp["name"].strip())]
        board = self.board["name"] if self.board else "the board"
        if not hits:
            return None, f"no sprint matching '{t}' on {board} (looked for '{t}', 'Sprint N' and '{self.project} Sprint N')"
        open_ = [sp for sp in hits if sp.get("state") in ("active", "future")]
        if not open_:
            return None, f"sprint '{hits[0]['name']}' is already closed"
        return open_[0], ""


# --------------------------------------------------------------------------
# Sync
# --------------------------------------------------------------------------

PROP = "md-sync"
PROP_IMPORT = "md-sync-import"


class DeletedInJira(Exception):
    def __init__(self, key: str):
        super().__init__(
            f"{key} no longer exists in Jira (deleted, or moved to another project). "
            f"Delete its row and section from the markdown, or empty its Jira cell to create it again."
        )


class Syncer:
    def __init__(self, jira: Jira, meta: Meta, cfg: dict, team: dict, force: bool = False,
                 seed_keys: Optional[set] = None):
        self.jira, self.meta, self.cfg, self.team, self.force = jira, meta, cfg, team, force
        # Seed mode (used by import): compute fingerprints of imported rows and store them on the
        # issues, but change nothing else in Jira.
        self.seed = seed_keys is not None
        self.seed_keys = seed_keys or set()
        self.known: dict[str, str] = {}  # keys in synced files -> file
        self.parked: dict[str, str] = {}  # keys in "_" files -> file
        self._epic_names: Optional[list] = None
        self._story_names: dict[str, list] = {}
        self.log: list[tuple[str, str, str, str]] = []  # (file, item, action, detail)
        self.failures = 0
        self.users: dict[str, Optional[str]] = {}
        self.warned: set[str] = set()
        self.props: dict[str, dict] = {}
        self.deleted: list[str] = []
        self.sprints = Sprints(jira, meta.project, cfg)
        self.ac = meta.ac_field()
        server = os.environ.get("GITHUB_SERVER_URL", "https://github.com")
        repo = os.environ.get("GITHUB_REPOSITORY")
        self.blob = f"{server}/{repo}/blob/{cfg['default_branch']}/" if repo else None

    # -- helpers --
    def note(self, ep, item, action, detail=""):
        self.log.append((ep.rel, item, action, detail))

    def warn_once(self, msg):
        if msg not in self.warned:
            self.warned.add(msg)
            print(f"::warning::{msg}")

    def account(self, handle: str) -> Optional[str]:
        if handle in self.users:
            return self.users[handle]
        val = str(self.team.get(handle) or "")
        acc = None
        if "@" in val:
            res = self.jira.get("/rest/api/3/user/search", params={"query": val})
            exact = [u for u in res if (u.get("emailAddress") or "").lower() == val.lower()]
            pick = exact or (res if len(res) == 1 else [])
            acc = pick[0]["accountId"] if pick else None
            if not acc:
                self.warn_once(f"No single Jira user found for @{handle} ({val}); the issue stays unassigned.")
        elif val:
            acc = val
        self.users[handle] = acc
        return acc

    def footer(self, ep: Epic):
        src = f"{self.blob}{ep.rel}" if self.blob else ep.rel
        return para(f"Synced from {src}. Edit it there; changes made here to synced fields are overwritten.", [{"type": "em"}])

    def labels(self, ep: Epic) -> list[str]:
        labels = list(self.cfg["labels"])
        if ep.release:
            slug = re.sub(r"[^a-z0-9]+", "-", ep.release.lower()).strip("-")
            labels.append(self.cfg["release_target_label_prefix"] + slug)
        return labels

    def put_field(self, fields: dict, kind: str, fid: str, value, label: str):
        if fid in self.meta.fields(kind):
            fields[fid] = value
        else:
            self.warn_once(f"'{label}' is not available on {kind} issues in Jira; skipped. Run the doctor command for details.")

    def upsert(self, ep: Epic, kind: str, label: str, key: Optional[str], fields: dict,
               writeback: Callable[[str], None], on_update_drop: tuple = ()) -> tuple[str, bool]:
        labels = self.labels(ep)
        digest = hashlib.sha256(json.dumps([fields, labels], sort_keys=True).encode()).hexdigest()
        if self.seed:
            if key in self.seed_keys:
                self.jira.put(f"/rest/api/3/issue/{key}/properties/{PROP_IMPORT}", json={"hash": digest})
                self.note(ep, label, "seeded", key)
            return key, False
        if key is None:
            self.guard(kind, fields)
            create = {k: v for k, v in fields.items() if v is not None}
            create["labels"] = labels
            self.check_required(kind, create)
            res = self.jira.post("/rest/api/3/issue", json={"fields": create})
            key = res["key"]
            writeback(key)
            ep.save()  # save right away so a later failure can't cause duplicates
            self.set_prop(key, hash=digest, source=ep.rel)
            self.note(ep, label, "created", key)
            return key, True
        old = self.get_prop(key).get("hash")
        if old == digest and not self.force:
            self.note(ep, label, "unchanged", key)
            return key, False
        if old is None and not self.force and self.import_hash(key) == digest:
            # Imported from Jira and not edited since: keep Jira's content, only start tracking it.
            try:
                self.jira.put(f"/rest/api/3/issue/{key}", json={"update": {"labels": [{"add": l} for l in labels]}})
            except JiraError as e:
                if e.status == 404:
                    raise DeletedInJira(key) from e
                raise
            self.set_prop(key, hash=digest, source=ep.rel)
            self.note(ep, label, "adopted", key)
            return key, False
        upd = {k: v for k, v in fields.items() if k not in ("project", "issuetype") + on_update_drop}
        try:
            self.jira.put(f"/rest/api/3/issue/{key}", json={"fields": upd, "update": {"labels": [{"add": l} for l in labels]}})
        except JiraError as e:
            if e.status == 404:
                raise DeletedInJira(key) from e
            raise
        self.set_prop(key, hash=digest, source=ep.rel)
        self.note(ep, label, "updated", key)
        return key, False

    def import_hash(self, key) -> Optional[str]:
        try:
            return ((self.jira.get(f"/rest/api/3/issue/{key}/properties/{PROP_IMPORT}") or {}).get("value") or {}).get("hash")
        except JiraError as e:
            if e.status == 404:
                return None
            raise

    def guard(self, kind: str, fields: dict):
        """Refuse to create an epic or story that already exists in Jira under the same name."""
        if kind == "epic":
            if self._epic_names is None:
                t = self.meta.types["epic"]["name"]
                self._epic_names = self.search(f'project = "{self.meta.project}" AND issuetype = "{t}"')
            cands, where = self._epic_names, "Epic"
        elif kind == "story":
            parent = (fields.get("parent") or {}).get("key")
            if not parent:
                return
            if parent not in self._story_names:
                t = self.meta.types["story"]["name"]
                self._story_names[parent] = self.search(f'parent = {parent} AND issuetype = "{t}"')
            cands, where = self._story_names[parent], f"Story under {parent}"
        else:
            return
        name = fields["summary"].strip().lower()
        for i in cands:
            k = i["key"]
            if (i["fields"].get("summary") or "").strip().lower() != name:
                continue
            if k in self.known:
                raise RuntimeError(f"{where} '{fields['summary']}' already exists as {k} in {self.known[k]}. "
                                   f"If this is the same {kind}, keep it in that file only; otherwise give it a different name.")
            if k in self.parked:
                raise RuntimeError(f"{where} '{fields['summary']}' already exists as {k}, which is waiting in "
                                   f"{self.parked[k]}. Move that row here instead of writing a new one.")
            raise RuntimeError(f"{where} '{fields['summary']}' already exists in Jira as {k}, but no markdown file has it. "
                               f"Run the import (Actions → Jira sync → Run workflow → import) to bring it in, "
                               f"or give this one a different name.")

    def check_required(self, kind: str, fields: dict):
        missing = []
        for fid, f in self.meta.fields(kind).items():
            if f.get("required") and not f.get("hasDefaultValue") and fid not in fields:
                if (f.get("name") or "").lower() == "epic name" and "summary" in fields:
                    fields[fid] = fields["summary"]
                elif fid not in ("project", "issuetype", "summary", "reporter"):
                    missing.append(f.get("name") or fid)
        if missing:
            raise RuntimeError(f"Jira requires fields this sync doesn't fill on {kind} issues: {', '.join(missing)}")

    def get_prop(self, key) -> dict:
        if key not in self.props:
            try:
                self.props[key] = (self.jira.get(f"/rest/api/3/issue/{key}/properties/{PROP}") or {}).get("value") or {}
            except JiraError as e:
                if e.status != 404:
                    raise
                self.props[key] = {}
        return self.props[key]

    def set_prop(self, key, **values):
        value = {**self.props.get(key, {}), **values}
        self.jira.put(f"/rest/api/3/issue/{key}/properties/{PROP}", json=value)
        self.props[key] = value

    # -- sprints --
    def place(self, ep: Epic, label: str, key: str, target: str, created: bool):
        """Put a new issue into its target sprint once. After that, Jira owns the sprint."""
        if not target:
            return
        if not created:
            placed = self.get_prop(key).get("placed")
            if placed is not False:  # already placed, or created before sprint support: leave it to Jira
                return
            fl = self.jira.get(f"/rest/agile/1.0/issue/{key}", params={"fields": "sprint,closedSprints"}).get("fields", {})
            if fl.get("sprint") or fl.get("closedSprints"):  # someone planned it in Jira meanwhile
                self.set_prop(key, placed=True)
                return
        sprint, why = self.sprints.resolve(target)
        if not sprint:
            self.set_prop(key, placed=False)  # try again on a later sync
            self.warn_once(f"Sprint '{target}': {why}. Issues targeting it stay in the backlog; "
                           f"a later sync places them once the sprint exists, unless someone plans them in Jira first.")
            self.note(ep, label, "backlog", f"{key}: sprint '{target}' not found")
            return
        self.jira.post(f"/rest/agile/1.0/sprint/{sprint['id']}/issue", json={"issues": [key]})
        self.set_prop(key, placed=True)
        self.note(ep, label, "placed", f"{key} → {sprint['name']}")

    def base(self, kind: str, summary: str) -> dict:
        t = self.meta.types[kind]
        if not t:
            raise RuntimeError(f"The Jira project has no '{kind}' issue type.")
        return {"project": {"key": self.meta.project}, "issuetype": {"id": t["id"]}, "summary": summary[:254]}

    # -- links --
    def ensure_link(self, task: str, story: str):
        lt = str(self.cfg.get("link_type") or "none")
        if lt.lower() == "none":
            return

        def state():
            links = self.jira.get(f"/rest/api/3/issue/{story}", params={"fields": "issuelinks"})["fields"].get("issuelinks", [])
            good, bad = [], []
            for l in links:
                if l["type"]["name"].lower() != lt.lower():
                    continue
                # On the story: an inwardIssue entry reads "story <inward> task", i.e. "is blocked by".
                if (l.get("inwardIssue") or {}).get("key") == task:
                    good.append(l["id"])
                elif (l.get("outwardIssue") or {}).get("key") == task:
                    bad.append(l["id"])
            return good, bad

        good, bad = state()
        if good:
            return
        for lid in bad:
            self.jira.delete(f"/rest/api/3/issueLink/{lid}")
        body = {"type": {"name": lt}, "inwardIssue": {"key": task}, "outwardIssue": {"key": story}}
        self.jira.post("/rest/api/3/issueLink", json=body)
        good, bad = state()
        if not good and bad:  # direction was reversed on this site: swap
            for lid in bad:
                self.jira.delete(f"/rest/api/3/issueLink/{lid}")
            body["inwardIssue"], body["outwardIssue"] = body["outwardIssue"], body["inwardIssue"]
            self.jira.post("/rest/api/3/issueLink", json=body)

    # -- main --
    def sync_epic(self, ep: Epic):
        fields = self.base("epic", ep.name)
        people = [f"{k}: {v}" for k, v in (("Document owner", ep.owner), ("Designer", ep.designer), ("Developers", ep.developers)) if v]
        fields["description"] = adf(para(ep.summary), para(" · ".join(people)), md_to_adf(ep.details), self.footer(ep))
        label = f"Epic: {ep.name}"
        if self.seed and not ep.key:
            return
        try:
            if ep.owner_handle:
                acc = self.account(ep.owner_handle)
                if acc:
                    self.put_field(fields, "epic", "assignee", {"accountId": acc}, "Assignee")
            ep.key, _ = self.upsert(ep, "epic", label, ep.key, fields,
                                    lambda k: ep.set_cell(ep.key_line, ep.key_col, self.cell(k)))
        except Exception as e:
            self.fail(ep, label, e)
            return
        for st in ep.stories:
            self.sync_story(ep, st)
        for it in ep.tasks:
            try:
                self.sync_epic_task(ep, it)
            except Exception as e:
                self.fail(ep, f"Other task: {it.title}", e)

    def cell(self, key):
        return f"[{key}]({self.jira.base}/browse/{key})"

    def fail(self, ep, label, e):
        self.failures += 1
        if isinstance(e, DeletedInJira):
            self.deleted.append(f"`{ep.rel}` {label.strip()}: {e}")
            self.note(ep, label, "DELETED IN JIRA", str(e))
        else:
            self.note(ep, label, "FAILED", str(e))
        print(f"::error file={ep.rel}::{label.strip()}: {e}")

    def sync_story(self, ep: Epic, st: Story):
        label = f"{st.sid} {st.title}"
        if self.seed and not st.key:
            return
        f = self.base("story", st.title)
        f["parent"] = {"key": ep.key}
        blocks = [para(st.description)]
        if st.notes:
            blocks.append(para(f"Notes: {st.notes}"))
        if st.ac and not self.ac:
            blocks += [heading("Acceptance criteria"), bullets(st.ac)]
        blocks += md_to_adf(st.details)
        blocks.append(self.footer(ep))
        f["description"] = adf(*blocks)
        if self.ac and st.ac:
            fid, rich = self.ac
            f[fid] = adf(bullets(st.ac)) if rich else "\n".join(f"- {a}" for a in st.ac)
        if st.priority:
            self.put_field(f, "story", "priority", {"name": st.priority}, "Priority")
        if st.owner:
            acc = self.account(st.owner)
            if acc:
                self.put_field(f, "story", "assignee", {"accountId": acc}, "Assignee")
        pf = self.meta.points_field("story")
        if pf:
            f[pf] = st.points  # None clears it (Model B or not estimated)
        elif st.points is not None:
            self.warn_once("No story points field found on Story issues; points skipped. Run the doctor command.")
        try:
            st.key, created = self.upsert(ep, "story", label, st.key, f,
                                          lambda k: ep.set_cell(st.line, st.jira_col, self.cell(k)))
        except Exception as e:
            self.fail(ep, label, e)
            return
        try:
            # Before sub-tasks are created, so they land in the same sprint as their story.
            if not self.seed:
                self.place(ep, label, st.key, target_sprint(ep, st), created)
        except Exception as e:
            self.fail(ep, f"{label} (sprint)", e)
        for it in st.items:
            try:
                self.sync_item(ep, st, it)
            except Exception as e:
                self.fail(ep, f"  {it.title}", e)

    def sync_item(self, ep: Epic, st: Story, it: Item):
        kind = it.kind
        f = self.base(kind, it.title)
        blocks = []
        if kind == "subtask":
            f["parent"] = {"key": st.key}
            if it.estimate:
                if "timetracking" in self.meta.fields("subtask"):
                    f["timetracking"] = {"originalEstimate": it.estimate}
                else:
                    self.warn_once("Time tracking is not available on sub-tasks; estimates are written into the description instead.")
                    blocks.append(para(f"Estimate: {it.estimate}"))
        else:
            f["parent"] = {"key": ep.key}
            blocks.append(para(f"Part of story {st.key}: {st.title}"))
            pf = self.meta.points_field("task")
            if pf:
                f[pf] = it.points
            elif it.points is not None:
                self.warn_once("No story points field on Task issues; task points skipped. Ask a Jira admin to add it, or run the doctor command.")
        blocks.append(self.footer(ep))
        f["description"] = adf(*blocks)
        if it.owner:
            acc = self.account(it.owner)
            if acc:
                self.put_field(f, kind, "assignee", {"accountId": acc}, "Assignee")
        if self.seed and not it.key:
            return
        # Task and sub-task descriptions are only written on creation, so text added in Jira is kept.
        drop = ("parent", "description") if kind == "subtask" else ("description",)
        it.key, created = self.upsert(ep, kind, f"  {it.title}", it.key, f,
                                      lambda k: ep.set_cell(it.line, it.jira_col, self.cell(k)), on_update_drop=drop)
        if self.seed:
            return
        if kind == "task":
            self.ensure_link(it.key, st.key)
            self.place(ep, f"  {it.title}", it.key, target_sprint(ep, st, it), created)

    def sync_epic_task(self, ep: Epic, it: Item):
        label = f"Other task: {it.title}"
        f = self.base("task", it.title)
        f["parent"] = {"key": ep.key}
        pf = self.meta.points_field("task")
        if pf:
            f[pf] = it.points
        elif it.points is not None:
            self.warn_once("No story points field on Task issues; task points skipped. Ask a Jira admin to add it, or run the doctor command.")
        f["description"] = adf(para(f"Epic-level task in {ep.name}."), self.footer(ep))
        if it.owner:
            acc = self.account(it.owner)
            if acc:
                self.put_field(f, "task", "assignee", {"accountId": acc}, "Assignee")
        if self.seed and not it.key:
            return
        it.key, created = self.upsert(ep, "task", label, it.key, f,
                                      lambda k: ep.set_cell(it.line, it.jira_col, self.cell(k)),
                                      on_update_drop=("description",))
        if not self.seed:
            self.place(ep, label, it.key, target_sprint(ep, None, it), created)

    def search(self, jql: str) -> list[dict]:
        found, token = [], None
        while True:
            params = {"jql": jql, "fields": "summary,issuetype,labels,parent", "maxResults": 100}
            if token:
                params["nextPageToken"] = token
            d = self.jira.get("/rest/api/3/search/jql", params=params)
            found += d.get("issues", [])
            token = d.get("nextPageToken")
            if not token or d.get("isLast", True):
                return found

    def reconcile(self, epics: list[Epic]) -> tuple[list[str], list[str]]:
        """Return (synced issues no longer in the markdown, issues created in Jira under a synced epic)."""
        known = set()
        for ep in epics:
            known.add(ep.key)
            known.update(it.key for it in ep.tasks)
            for st in ep.stories:
                known.add(st.key)
                known.update(it.key for it in st.items)
        known |= set(self.parked)
        tag = self.cfg["labels"][0]

        def line(i):
            f = i["fields"]
            typ = (f.get("issuetype") or {}).get("name", "")
            parent = (f.get("parent") or {}).get("key")
            return f"{i['key']} ({typ}{', under ' + parent if parent else ''}): {f.get('summary', '')}"

        removed = [line(i) for i in self.search(f'project = "{self.meta.project}" AND labels = "{tag}" ORDER BY key')
                   if i["key"] not in known]
        jira_only = []
        epic_keys = [ep.key for ep in epics if ep.key]
        for n in range(0, len(epic_keys), 40):
            chunk = ", ".join(epic_keys[n:n + 40])
            for i in self.search(f"parent in ({chunk}) ORDER BY key"):
                if i["key"] not in known and tag not in (i["fields"].get("labels") or []):
                    jira_only.append(line(i))
        epic_type = (self.meta.types.get("epic") or {}).get("name", "Epic")
        try:
            loose = self.search(f'project = "{self.meta.project}" AND parent is EMPTY AND issuetype != "{epic_type}" '
                                f'AND statusCategory != Done ORDER BY key')
            jira_only += [line(i) + " (no epic)" for i in loose
                          if i["key"] not in known and tag not in (i["fields"].get("labels") or [])]
        except JiraError as e:
            self.warn_once(f"Could not list issues without an epic: {e}")
        return removed, jira_only


# --------------------------------------------------------------------------
# Import from Jira
# --------------------------------------------------------------------------

GENERATED_RE = re.compile(r"^[*_]*\s*(synced from |part of story |epic-level task in |estimate: |document owner: |designer: |developers: )", re.I)
MARKER_WORDS = {"acceptance criteria", "sub tasks", "subtasks", "tasks", "details", "requirements", "other tasks"}


def adf_inline(nodes: list, lossy: list) -> str:
    out = []
    for n in nodes or []:
        t = n.get("type")
        if t == "text":
            txt = n.get("text", "")
            for m in n.get("marks", []):
                if m.get("type") == "link":
                    href = (m.get("attrs") or {}).get("href", "")
                    txt = f"[{txt}]({href})" if href and href != txt else txt
                elif m.get("type") == "code":
                    txt = f"`{txt}`"
                elif m.get("type") == "strong":
                    txt = f"**{txt}**"
            out.append(txt)
        elif t == "hardBreak":
            out.append(" ")
        elif t in ("mention", "emoji", "status"):
            a = n.get("attrs") or {}
            out.append(a.get("text") or a.get("shortName") or "")
        elif t == "inlineCard":
            out.append((n.get("attrs") or {}).get("url", ""))
        elif t == "date":
            lossy.append("date")
            out.append((n.get("attrs") or {}).get("timestamp", ""))
        else:
            lossy.append(t or "?")
            out.append(adf_inline(n.get("content"), lossy))
    return "".join(out)


def adf_blocks(doc: Optional[dict]) -> tuple[list[tuple[str, str]], list[str]]:
    """Flatten an ADF document into (kind, markdown text) blocks. Kinds: para, heading, list, code, quote."""
    lossy: list[str] = []
    blocks: list[tuple[str, str]] = []

    def list_lines(node, depth=0):
        lines = []
        for i, item in enumerate(node.get("content", []), 1):
            prefix = "  " * depth + ("- " if node["type"] == "bulletList" else f"{i}. ")
            first = True
            for child in item.get("content", []):
                if child.get("type") in ("bulletList", "orderedList"):
                    lines += list_lines(child, depth + 1)
                else:
                    txt = adf_inline(child.get("content"), lossy) if child.get("type") == "paragraph" else text_of(child)
                    lines.append((prefix if first else "  " * (depth + 1)) + txt)
                    first = False
        return lines

    def text_of(node):
        if node.get("type") == "text":
            return node.get("text", "")
        return " ".join(text_of(c) for c in node.get("content", []) or []).strip()

    def walk(nodes):
        for n in nodes or []:
            t = n.get("type")
            if t == "paragraph":
                txt = adf_inline(n.get("content"), lossy).strip()
                if txt:
                    blocks.append(("para", txt))
            elif t == "heading":
                blocks.append(("heading", adf_inline(n.get("content"), lossy).strip()))
            elif t in ("bulletList", "orderedList"):
                blocks.append(("list", "\n".join(list_lines(n))))
            elif t == "codeBlock":
                blocks.append(("code", "```\n" + text_of(n) + "\n```"))
            elif t == "blockquote":
                inner = [adf_inline(c.get("content"), lossy) for c in n.get("content", [])]
                blocks.append(("quote", "\n".join("> " + x for x in inner if x)))
            elif t == "rule":
                continue
            elif t in ("panel", "expand", "nestedExpand", "layoutSection", "layoutColumn"):
                if t != "panel":
                    lossy.append(t)
                title = (n.get("attrs") or {}).get("title")
                if title:
                    blocks.append(("para", f"**{title}**"))
                walk(n.get("content"))
            elif t == "table":
                lossy.append("table")
                for row in n.get("content", []):
                    cells = [text_of(c) for c in row.get("content", [])]
                    blocks.append(("para", " · ".join(cells)))
            elif t in ("mediaSingle", "mediaGroup", "media"):
                lossy.append("image/attachment")
                blocks.append(("para", "[attachment in Jira]"))
            else:
                lossy.append(t or "?")
                txt = text_of(n)
                if txt:
                    blocks.append(("para", txt))

    walk((doc or {}).get("content"))
    return blocks, sorted(set(lossy))


def list_items(text: str) -> list[str]:
    return [re.sub(r"^\s*(?:[-*+]|\d+[.)])\s+", "", l).strip() for l in text.splitlines() if l.strip()]


def split_description(doc: Optional[dict]) -> dict:
    """Split a Jira description into the template's parts: description, notes, acceptance criteria, details."""
    blocks, lossy = adf_blocks(doc)
    notes, keep = "", []
    for kind, text in blocks:
        bare = text.strip().strip("*_ ")
        if kind == "para" and GENERATED_RE.match(bare):
            continue
        if kind == "para" and re.match(r"^notes:\s*", bare, re.I):
            notes = re.sub(r"^notes:\s*", "", bare, flags=re.I)
            continue
        keep.append((kind, text))
    ac: list[str] = []
    for idx, (kind, text) in enumerate(keep):
        label = re.sub(r"[*_#:]", "", text).strip().lower()
        if kind in ("heading", "para") and label in ("acceptance criteria", "acceptance criterion"):
            j = idx + 1
            while j < len(keep) and keep[j][0] == "list":
                ac += list_items(keep[j][1])
                j += 1
            if ac:
                del keep[idx:j]
            break
    desc = ""
    paras = [i for i, (k, _) in enumerate(keep) if k == "para"]
    pick = next((i for i in paras if STORY_FORMAT_RE.search(keep[i][1])), paras[0] if paras else None)
    if pick is not None:
        desc = keep.pop(pick)[1]
    details: list[str] = []
    for kind, text in keep:
        if kind == "heading":
            # Keep headings below level 3 and away from words the parser treats as section markers.
            h = text if norm(text) not in MARKER_WORDS else f"{text} (from Jira)"
            text = f"#### {h}"
        if details:
            details.append("")
        details += text.splitlines()
    return {"description": desc, "notes": notes, "ac": ac, "details": details, "lossy": lossy}


def esc(s) -> str:
    return re.sub(r"\s+", " ", str(s if s is not None else "")).replace("|", "\\|").strip()


def fmt_points(v) -> str:
    if v is None or v == "":
        return ""
    try:
        f = float(v)
    except (TypeError, ValueError):
        return ""
    return str(int(f)) if f.is_integer() else str(f)


def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:40] or "epic"


@dataclass
class ImpItem:
    key: str
    title: str
    owner: str = ""
    estimate: str = ""
    points: str = ""


@dataclass
class ImpStory:
    key: str
    title: str
    parts: dict
    priority: str = ""
    points: str = ""
    owner: str = ""
    subtasks: list[ImpItem] = field(default_factory=list)
    tasks: list[ImpItem] = field(default_factory=list)


@dataclass
class Dest:
    """A markdown file that receives imported issues: an existing epic file, or a new one."""
    path: Path
    ep: Optional[Epic] = None             # parsed existing file
    epic: Optional[dict] = None           # new file: key, name, parts, owner
    parked: bool = False
    stories: list[ImpStory] = field(default_factory=list)
    other: list[ImpItem] = field(default_factory=list)
    add_sub: dict = field(default_factory=dict)    # story sid -> [ImpItem] (existing stories)
    add_task: dict = field(default_factory=dict)

    def empty(self):
        return not (self.epic or self.stories or self.other or any(self.add_sub.values()) or any(self.add_task.values()))


PARK_NAME = "_imported-unsorted.md"


class Importer:
    def __init__(self, jira: Jira, meta: Meta, cfg: dict, team: dict, root: Path, epics: list[Epic]):
        self.jira, self.meta, self.cfg, self.team, self.root, self.epics = jira, meta, cfg, team, root, epics
        self.backlog = root / cfg["backlog_dir"]
        self.sy = Syncer(jira, meta, cfg, team)
        self.skipped: list[str] = []
        self.notes: list[str] = []
        self.lossy: list[str] = []
        self.unmapped: dict[str, list[str]] = {}
        self.imported: set[str] = set()
        self.dests: dict[Path, Dest] = {}
        self.acct: dict[str, str] = {}

    # -- helpers --
    def cell(self, key):
        return f"[{key}]({self.jira.base}/browse/{key})"

    def owner_of(self, issue) -> str:
        a = issue["fields"].get("assignee")
        if not a:
            return ""
        h = self.acct.get(a.get("accountId"))
        if h:
            return h
        self.unmapped.setdefault(a.get("displayName") or a.get("accountId"), []).append(issue["key"])
        return ""

    def kind(self, issue) -> str:
        it = issue["fields"].get("issuetype") or {}
        types = self.meta.types
        if it.get("subtask"):
            return "subtask"
        if (types["epic"] and it.get("id") == types["epic"]["id"]) or it.get("hierarchyLevel") == 1:
            return "epic"
        if types["story"] and it.get("id") == types["story"]["id"]:
            return "story"
        if types["task"] and it.get("id") == types["task"]["id"]:
            return "task"
        return "other"

    def dest_for_file(self, ep: Epic, parked=False) -> Dest:
        if ep.path not in self.dests:
            self.dests[ep.path] = Dest(path=ep.path, ep=ep, parked=parked)
        return self.dests[ep.path]

    def park(self) -> Dest:
        path = self.backlog / PARK_NAME
        if path not in self.dests:
            if path.exists():
                self.dests[path] = Dest(path=path, ep=parse_epic(path, path.relative_to(self.root).as_posix()), parked=True)
            else:
                self.dests[path] = Dest(path=path, parked=True, epic={"key": None, "name": "Unsorted Jira issues",
                                                                       "parts": {"description": "", "details": []}, "owner": ""})
        return self.dests[path]

    def new_epic_path(self, name: str) -> Path:
        nums = [int(m.group(1)) for p in self.backlog.glob("*.md") if (m := re.match(r"(?:epic|di)-(\d+)", p.name, re.I))]
        nums += [int(m.group(1)) for p in self.dests if (m := re.match(r"epic-(\d+)", p.name))]
        n = max(nums, default=0) + 1
        return self.backlog / f"epic-{n:02d}-{slug(name)}.md"

    # -- main --
    def run(self):
        for h in self.team:
            acc = self.sy.account(h)
            if acc:
                self.acct[acc] = h
        pf_story, pf_task = self.meta.points_field("story"), self.meta.points_field("task")
        fields = ["summary", "issuetype", "parent", "description", "assignee", "priority", "status",
                  "timetracking", "issuelinks"] + [f for f in {pf_story, pf_task} if f]
        issues = jql_search(self.jira, f'project = "{self.meta.project}" ORDER BY key', fields)
        by_key = {i["key"]: i for i in issues}

        # Where every already-tracked issue lives.
        tracked: dict[str, tuple] = {}
        epic_dest: dict[str, Dest] = {}
        files = [(ep, False) for ep in self.epics]
        for p in parked_files(self.root, self.cfg):
            files.append((parse_epic(p, p.relative_to(self.root).as_posix()), True))
        for ep, parked in files:
            for key, _ in ep_keys(ep):
                tracked[key] = (ep, parked)
            if ep.key and not parked:
                epic_dest[ep.key] = self.dest_for_file(ep)
        story_loc: dict[str, tuple] = {}  # story key -> (Dest, Story or ImpStory)
        for ep, parked in files:
            for st in ep.stories:
                if st.key:
                    story_loc[st.key] = (self.dest_for_file(ep, parked), st)

        new = [i for i in issues if i["key"] not in tracked]
        prio_ok = {p.lower(): p for p in self.cfg["priorities"]}

        # 1. Epics -> new files
        for i in new:
            if self.kind(i) != "epic":
                continue
            f = i["fields"]
            path = self.new_epic_path(f.get("summary") or i["key"])
            d = Dest(path=path, epic={"key": i["key"], "name": f.get("summary") or i["key"],
                                      "parts": split_description(f.get("description")), "owner": self.owner_of(i)})
            self.dests[path] = d
            epic_dest[i["key"]] = d
            self.imported.add(i["key"])
            if d.epic["parts"]["lossy"]:
                self.lossy.append(f"{i['key']} ({', '.join(d.epic['parts']['lossy'])})")

        def home(issue) -> Dest:
            parent = (issue["fields"].get("parent") or {}).get("key")
            if parent in epic_dest:
                d = epic_dest[parent]
                if d.ep is not None and d.ep.errors:
                    self.notes.append(f"{issue['key']} belongs in {d.ep.rel}, which has errors; it was put in {PARK_NAME} instead.")
                    return self.park()
                return d
            return self.park()

        # 2. Stories
        for i in new:
            if self.kind(i) != "story":
                continue
            f = i["fields"]
            prio = (f.get("priority") or {}).get("name", "")
            s = ImpStory(key=i["key"], title=f.get("summary") or i["key"], parts=split_description(f.get("description")),
                         priority=prio_ok.get(prio.lower(), ""), points=fmt_points(f.get(pf_story)) if pf_story else "",
                         owner=self.owner_of(i))
            d = home(i)
            d.stories.append(s)
            story_loc[i["key"]] = (d, s)
            self.imported.add(i["key"])
            if s.parts["lossy"]:
                self.lossy.append(f"{i['key']} ({', '.join(s.parts['lossy'])})")

        # 3. Sub-tasks (before tasks: a story with sub-tasks can't also take Tasks)
        for i in new:
            if self.kind(i) != "subtask":
                continue
            f = i["fields"]
            parent = (f.get("parent") or {}).get("key")
            item = ImpItem(key=i["key"], title=f.get("summary") or i["key"], owner=self.owner_of(i),
                           estimate=((f.get("timetracking") or {}).get("originalEstimate") or ""))
            loc = story_loc.get(parent)
            if not loc:
                ptype = self.kind(by_key[parent]) if parent in by_key else "unknown"
                self.skipped.append(f"{i['key']} {item.title}: sub-task of a {ptype} ({parent}); the template only has sub-tasks under stories.")
                continue
            d, st = loc
            if isinstance(st, ImpStory):
                st.subtasks.append(item)
            elif st.breakdown == "tasks":
                self.skipped.append(f"{i['key']} {item.title}: its story {parent} uses a Tasks table, and a story can't have both.")
                continue
            else:
                d.add_sub.setdefault(st.sid, []).append(item)
            self.imported.add(i["key"])

        # 4. Tasks
        lt = str(self.cfg.get("link_type") or "none").lower()
        for i in new:
            if self.kind(i) != "task":
                continue
            f = i["fields"]
            item = ImpItem(key=i["key"], title=f.get("summary") or i["key"], owner=self.owner_of(i),
                           points=fmt_points(f.get(pf_task)) if pf_task else "")
            d = home(i)
            blocks = [(l.get("outwardIssue") or {}).get("key") for l in f.get("issuelinks", [])
                      if l.get("type", {}).get("name", "").lower() == lt and l.get("outwardIssue")]
            target = next((story_loc[b] for b in blocks if b in story_loc and story_loc[b][0] is d), None)
            placed = False
            if target:
                _, st = target
                if isinstance(st, ImpStory):
                    if not st.points and not st.subtasks:
                        st.tasks.append(item)
                        placed = True
                elif st.points is None and st.breakdown != "subtasks" and not d.add_sub.get(st.sid):
                    d.add_task.setdefault(st.sid, []).append(item)
                    placed = True
                if not placed:
                    self.notes.append(f"{i['key']} blocks {st.key}, but that story has points or sub-tasks, "
                                      f"so the task went under Other tasks.")
            if not placed:
                d.other.append(item)
            self.imported.add(i["key"])

        for i in new:
            if self.kind(i) == "other":
                self.skipped.append(f"{i['key']} {i['fields'].get('summary', '')}: issue type "
                                    f"'{i['fields']['issuetype'].get('name')}' isn't part of the template.")

        for d in self.dests.values():
            if not d.empty():
                self.write(d)

    # -- rendering --
    def story_row(self, sid: str, s: ImpStory) -> dict:
        return {"#": sid, "title": s.title, "description": s.parts["description"], "priority": s.priority,
                "points": "" if s.tasks else s.points, "owner": f"@{s.owner}" if s.owner else "",
                "sprint": "", "notes": s.parts["notes"], "jira": self.cell(s.key)}

    def story_section(self, sid: str, s: ImpStory) -> list[str]:
        out = ["", f"## {sid} · {esc(s.title)}", "", "**Acceptance criteria**", ""]
        out += [f"- {a}" for a in s.parts["ac"]] or ["<!-- Add the acceptance criteria. -->"]
        if s.parts["details"]:
            out += ["", "**Details**", ""] + s.parts["details"]
        if s.subtasks:
            out += ["", "**Sub-tasks**", ""] + self.item_table("subtasks", s.subtasks)
        if s.tasks:
            out += ["", "**Tasks**", ""] + self.item_table("tasks", s.tasks)
        return out

    def item_row(self, mode: str, it: ImpItem, header: Optional[list[str]] = None) -> str:
        vals = {"title": it.title, "owner": f"@{it.owner}" if it.owner else "", "estimate": it.estimate,
                "points": it.points, "sprint": "", "jira": self.cell(it.key)}
        if header is None:
            header = ["Sub-task", "Owner", "Estimate", "Jira"] if mode == "subtasks" else ["Task", "Owner", "Points", "Sprint", "Jira"]
        return row_for(header, vals)

    def item_table(self, mode: str, items: list[ImpItem]) -> list[str]:
        header = ["Sub-task", "Owner", "Estimate", "Jira"] if mode == "subtasks" else ["Task", "Owner", "Points", "Sprint", "Jira"]
        return ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)] + [self.item_row(mode, it, header) for it in items]

    def write(self, d: Dest):
        if d.ep is None:
            text = self.render_new(d)
            d.path.write_text(text, encoding="utf-8")
        else:
            self.append(d)

    def render_new(self, d: Dest) -> str:
        e = d.epic
        n = re.match(r"epic-(\d+)", d.path.name)
        title = f"Epic {n.group(1)}" if n else e["name"]
        out = [f"# Story Requirements for {title}", ""]
        if d.parked:
            out += ["<!--",
                    "IMPORTED FROM JIRA, NOT YET SORTED",
                    "This file starts with \"_\", so the sync never reads it and nothing here changes Jira.",
                    "It holds issues that had no epic in Jira. Move each story (its row in the Requirements",
                    "table and its section, keys included) or task row into a real epic file. On the next",
                    "sync it moves under that epic in Jira. Delete this file once it is empty.",
                    "-->", ""]
        else:
            out += ["<!-- Imported from Jira. Empty cells are fields Jira didn't have: fill them in.",
                    "     Keep every Jira cell as it is: the keys link these rows to the existing issues. -->", ""]
        parts = e["parts"]
        out += [f"| Epic | {esc(e['name'])} |", "|---|---|",
                f"| Summary | {esc(parts['description'])} |",
                f"| Document Owner | {('@' + e['owner']) if e['owner'] else ''} |",
                "| Designer | |", "| Developers | |", "| Release Target (Sprint) | |",
                f"| Jira | {self.cell(e['key']) if e['key'] else ''} |"]
        if parts.get("details"):
            out += ["", "**Details**", ""] + parts["details"]
        out += ["", "## Requirements", "",
                "| # | User story title | User story description | Priority | Points | Owner | Sprint | Notes | Jira |",
                "|---|---|---|---|---|---|---|---|---|"]
        header = ["#", "User story title", "User story description", "Priority", "Points", "Owner", "Sprint", "Notes", "Jira"]
        sections = []
        for n_, s in enumerate(d.stories, 1):
            sid = f"S{n_}"
            out.append(row_for(header, self.story_row(sid, s)))
            sections += self.story_section(sid, s)
        out += sections
        if d.other:
            out += ["", "## Other tasks", ""] + self.item_table("tasks", d.other)
        return "\n".join(out) + "\n"

    def append(self, d: Dest):
        ep = d.ep
        ins: dict[int, list[str]] = {}

        def add(idx, lines_):
            ins.setdefault(idx, []).extend(lines_)

        def after(t: Table) -> int:
            return (t.rows[-1][0] if t.rows else t.header_line + 1) + 1

        nums = [int(st.sid[1:]) for st in ep.stories]
        nxt = max(nums, default=0) + 1
        eof = len(ep.lines) - (1 if ep.lines and ep.lines[-1] == "" else 0)
        story_at = ep.other_start if ep.other_start is not None else eof
        if d.stories:
            rows, sections = [], []
            for s in d.stories:
                sid = f"S{nxt}"
                nxt += 1
                rows.append(row_for(ep.req_table.header, self.story_row(sid, s)))
                sections += self.story_section(sid, s) + [""]
            add(after(ep.req_table), rows)
            add(story_at, sections)
        by_sid = {st.sid: st for st in ep.stories}
        for mode, adds in (("subtasks", d.add_sub), ("tasks", d.add_task)):
            for sid, items in adds.items():
                st = by_sid[sid]
                if st.item_table is not None and st.breakdown == mode:
                    add(after(st.item_table), [self.item_row(mode, it, st.item_table.header) for it in items])
                else:
                    word = "**Sub-tasks**" if mode == "subtasks" else "**Tasks**"
                    add(st.section_end, ["", word, ""] + self.item_table(mode, items) + [""])
        if d.other:
            if ep.other_table is not None:
                add(after(ep.other_table), [self.item_row("tasks", it, ep.other_table.header) for it in d.other])
            else:
                add(eof, ["", "## Other tasks", ""] + self.item_table("tasks", d.other))
        lines = list(ep.lines)
        for idx in sorted(ins, reverse=True):
            lines[idx:idx] = ins[idx]
        text = "\n".join(lines)
        if not text.endswith("\n"):
            text += "\n"
        d.path.write_text(text, encoding="utf-8")

    def summary(self) -> str:
        out = ["## Jira import", ""]
        written = [d for d in self.dests.values() if not d.empty()]
        if not written:
            return "\n".join(out + ["Nothing to import: every issue in the project is already in a markdown file."])
        out += [f"Imported **{len(self.imported)}** issue(s) into {len(written)} file(s).", "",
                "| File | | Stories | Sub-tasks | Tasks |", "|---|---|---|---|---|"]
        for d in written:
            rel = d.path.relative_to(self.root).as_posix()
            what = "new, not synced (no epic in Jira)" if d.parked and d.ep is None else \
                   ("not synced (no epic in Jira)" if d.parked else ("new epic file" if d.ep is None else "added to"))
            subs = sum(len(s.subtasks) for s in d.stories) + sum(len(v) for v in d.add_sub.values())
            tasks = sum(len(s.tasks) for s in d.stories) + sum(len(v) for v in d.add_task.values()) + len(d.other)
            out.append(f"| `{rel}` | {what} | {len(d.stories)} | {subs} | {tasks} |")
        if any(d.parked for d in written):
            out += ["", f"📥 Issues with no epic in Jira are in `{PARK_NAME}`. That file is never synced. "
                        f"Move each story (row and section, keys included) or task row into an epic file; "
                        f"the next sync then moves it under that epic in Jira."]
        if self.notes:
            out += ["", "**Notes**", ""] + [f"- {n}" for n in self.notes]
        if self.skipped:
            out += ["", "**Not imported**", ""] + [f"- {s}" for s in self.skipped]
        if self.unmapped:
            out += ["", "**Assignees not in `.jira/team.yml`** (their Owner cells are empty; add them to team.yml and "
                        "fill in the cells, or leave them empty to keep the Jira assignee):", ""]
            out += [f"- {name}: {', '.join(keys)}" for name, keys in self.unmapped.items()]
        if self.lossy:
            out += ["", "**Descriptions with formatting markdown can't hold**: these were flattened to text. "
                        "Jira keeps the original until someone edits the issue in markdown; after that, the "
                        "flattened version replaces it.", ""] + [f"- {x}" for x in self.lossy]
        out += ["", "**Before merging**: review the files, fill in what's missing (the check below lists it), "
                    "and keep every Jira cell as it is. Merging changes nothing in Jira for rows you didn't edit."]
        return "\n".join(out)


CANON = {
    "#": ("#", "id"), "title": ("user story title", "title", "sub task", "subtask", "task"),
    "description": ("user story description", "description"), "priority": ("priority",),
    "points": ("points", "story points"), "owner": ("owner", "assignee"), "sprint": ("sprint", "target sprint"),
    "notes": ("notes",), "jira": ("jira",), "estimate": ("estimate", "original estimate"),
}


def row_for(header: list[str], vals: dict) -> str:
    """Build a table row that fits an existing header, whatever its column order."""
    cells = []
    for h in header:
        n = norm(h)
        key = next((k for k, names in CANON.items() if n in names), None)
        v = vals.get(key, "") if key else ""
        cells.append(v if key == "jira" else esc(v))
    return "| " + " | ".join(cells) + " |"


def jql_search(jira: Jira, jql: str, fields: list[str]) -> list[dict]:
    found, token = [], None
    while True:
        params = {"jql": jql, "fields": ",".join(fields), "maxResults": 100}
        if token:
            params["nextPageToken"] = token
        d = jira.get("/rest/api/3/search/jql", params=params)
        found += d.get("issues", [])
        token = d.get("nextPageToken")
        if not token or d.get("isLast", True):
            return found


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------


def load(root: Path):
    cfg = yaml.safe_load((root / ".jira/config.yml").read_text(encoding="utf-8")) or {}
    defaults = {
        "backlog_dir": "docs/backlog",
        "default_branch": "main",
        "points_scale": [0, 1, 2, 3, 5, 8, 13],
        "priorities": ["Highest", "High", "Medium", "Low", "Lowest"],
        "issue_types": {"epic": "Epic", "story": "Story", "task": "Task"},
        "story_points_field": "auto",
        "acceptance_criteria_field": "none",
        "link_type": "Blocks",
        "labels": ["md-sync"],
        "release_target_label_prefix": "target-",
        "board_id": "auto",
    }
    for k, v in defaults.items():
        cfg.setdefault(k, v)
    team_file = root / ".jira/team.yml"
    team = yaml.safe_load(team_file.read_text(encoding="utf-8")) if team_file.exists() else {}
    team = {str(k).lstrip("@"): v for k, v in (team or {}).items()}
    files = sorted(p for p in (root / cfg["backlog_dir"]).glob("*.md") if not p.name.startswith("_"))
    epics = []
    for p in files:
        ep = parse_epic(p, p.relative_to(root).as_posix())
        validate(ep, cfg, team)
        epics.append(ep)
    # One issue, one file: a key in two synced files would make both fight over the same issue.
    seen: dict[str, str] = {}
    parked = parked_keys(root, cfg)
    for ep in epics:
        for key, line in ep_keys(ep):
            if key in seen and seen[key] != ep.rel:
                ep.err(line + 1, f"Jira key {key} is also used in {seen[key]}. Each issue may appear in only one file.")
            seen.setdefault(key, ep.rel)
            if key in parked:
                ep.warn(line + 1, f"{key} is also listed in {parked[key]}. Delete it there; this file is the one that syncs.")
    return cfg, team, epics


def ep_keys(ep: Epic) -> list[tuple[str, int]]:
    """Every Jira key in an epic file, with its line index."""
    out = []
    if ep.key:
        out.append((ep.key, ep.key_line or 0))
    for st in ep.stories:
        if st.key:
            out.append((st.key, st.line))
        out += [(it.key, it.line) for it in st.items if it.key]
    out += [(it.key, it.line) for it in ep.tasks if it.key]
    return out


def parked_files(root: Path, cfg: dict) -> list[Path]:
    """Files starting with "_" (never synced), except the template."""
    return sorted(p for p in (root / cfg["backlog_dir"]).glob("_*.md") if p.name.lower() != "_template.md")


def parked_keys(root: Path, cfg: dict) -> dict[str, str]:
    """Keys that sit in "_" files, e.g. issues imported from Jira and not yet moved into an epic file."""
    out = {}
    for p in parked_files(root, cfg):
        ep = parse_epic(p, p.relative_to(root).as_posix())
        for key, _ in ep_keys(ep):
            out.setdefault(key, ep.rel)
    return out


def env(name: str) -> str:
    v = os.environ.get(name, "").strip()
    if not v:
        sys.exit(f"Missing environment variable {name}. See docs/JIRA_SYNC_SETUP.md.")
    return v


def cmd_validate(root, report):
    text, n_err = validate_text(root)
    write_report(report, text)
    return 1 if n_err else 0


def validate_text(root) -> tuple[str, int]:
    cfg, team, epics = load(root)
    n_err = sum(len(e.errors) for e in epics)
    n_warn = sum(len(e.problems) for e in epics) - n_err
    head = "## Jira sync check\n\n"
    if not epics:
        head += f"No epic files found in `{cfg['backlog_dir']}/` (files starting with `_` are skipped).\n"
    elif n_err:
        head += f"❌ {n_err} error(s), {n_warn} warning(s). Fix the errors before merging; nothing is sent to Jira until then.\n"
    else:
        head += f"✅ No errors ({n_warn} warning(s)). On merge, the sync will do this:\n"
    body = problems_md(epics)
    return head + ("\n" + body + "\n" if body else "") + plan_md(epics), n_err


def cmd_import(root, report):
    cfg, team, epics = load(root)
    jira = Jira(env("JIRA_BASE_URL"), env("JIRA_EMAIL"), env("JIRA_API_TOKEN"))
    meta = Meta(jira, env("JIRA_PROJECT_KEY"), cfg)
    im = Importer(jira, meta, cfg, team, root, epics)
    im.run()
    text = im.summary()
    if im.imported:
        # Record what each imported row looks like now, so the first sync after merging
        # leaves Jira's content alone unless someone edited the row.
        cfg, team, epics = load(root)
        sy = Syncer(jira, meta, cfg, team, seed_keys=im.imported)
        for ep in epics:
            if not ep.errors:
                sy.sync_epic(ep)
        failed = [f"{i.strip()}: {d}" for _, i, a, d in sy.log if a == "FAILED"]
        if failed:
            text += ("\n\n⚠️ Could not record the starting state of some issues. On merge, they are rewritten "
                     "from the markdown even if nobody edited them:\n\n" + "\n".join(f"- {x}" for x in failed))
    vtext, _ = validate_text(root)
    text += "\n\n---\n\n" + vtext
    write_report(report, text[:60000])
    return 0


def cmd_sync(root, report, force):
    cfg, team, epics = load(root)
    if any(e.errors for e in epics):
        write_report(report, "## Jira sync\n\n❌ Validation errors; nothing was sent to Jira.\n\n" + problems_md(epics))
        return 1
    jira = Jira(env("JIRA_BASE_URL"), env("JIRA_EMAIL"), env("JIRA_API_TOKEN"))
    meta = Meta(jira, env("JIRA_PROJECT_KEY"), cfg)
    sy = Syncer(jira, meta, cfg, team, force)
    sy.known = {k: ep.rel for ep in epics for k, _ in ep_keys(ep)}
    sy.parked = parked_keys(root, cfg)
    for ep in epics:
        sy.sync_epic(ep)
        ep.save()
    lines = ["## Jira sync", "", "| File | Item | Result | Key / detail |", "|---|---|---|---|"]
    lines += [f"| {f} | {i.strip()} | {a} | {d} |" for f, i, a, d in sy.log]
    if sy.deleted:
        lines += ["", "**❌ Deleted in Jira but still in the markdown**", ""] + [f"- {d}" for d in sy.deleted]
    try:
        removed, jira_only = sy.reconcile(epics)
        if removed:
            lines += ["", "**In Jira but no longer in the markdown** (not deleted; close or delete them in Jira if intended):", ""]
            lines += [f"- {o}" for o in removed]
        if jira_only:
            lines += ["", "**Created in Jira, not in the markdown** (fine for bugs and chores; stories belong in the markdown):", ""]
            lines += [f"- {o}" for o in jira_only]
    except Exception as e:
        lines += ["", f"⚠️ Could not compare Jira with the markdown: {e}"]
    if sy.parked:
        files = sorted(set(sy.parked.values()))
        lines += ["", f"📥 {len(sy.parked)} imported issue(s) are waiting in {', '.join(files)}. "
                      f"Move their rows into an epic file to start syncing them."]
    if sy.sprints.note:
        sy.warn_once(sy.sprints.note)
    if sy.warned:
        lines += ["", "**Warnings**", ""] + [f"- {w}" for w in sorted(sy.warned)]
    write_report(report, "\n".join(lines))
    return 1 if sy.failures else 0


def cmd_doctor(root, report):
    cfg, team, epics = load(root)
    out = ["## Jira sync doctor", ""]
    ok = True
    jira = Jira(env("JIRA_BASE_URL"), env("JIRA_EMAIL"), env("JIRA_API_TOKEN"))
    try:
        me = jira.get("/rest/api/3/myself")
        out.append(f"✅ Logged in as **{me.get('displayName')}**")
    except JiraError as e:
        write_report(report, "\n".join(out + [f"❌ Login failed: {e}", "", "Check JIRA_BASE_URL, JIRA_EMAIL and JIRA_API_TOKEN."]))
        return 1
    try:
        meta = Meta(jira, env("JIRA_PROJECT_KEY"), cfg)
    except JiraError as e:
        write_report(report, "\n".join(out + [f"❌ Project {os.environ.get('JIRA_PROJECT_KEY')} not readable: {e}"]))
        return 1
    style = {"next-gen": "team-managed", "classic": "company-managed"}.get(meta.proj.get("style"), meta.proj.get("style", "?"))
    out.append(f"✅ Project **{meta.proj.get('key')} – {meta.proj.get('name')}** ({style})")
    out += ["", "| Check | Epic | Story | Task | Sub-task |", "|---|---|---|---|---|"]
    kinds = ["epic", "story", "task", "subtask"]
    row = ["Issue type"] + [("✅ " + meta.types[k]["name"]) if meta.types[k] else "❌ missing" for k in kinds]
    out.append("| " + " | ".join(row) + " |")
    if not meta.types["epic"] or not meta.types["story"]:
        ok = False
    need = {
        "Description": ("description", ["epic", "story", "task", "subtask"]),
        "Priority": ("priority", ["story"]),
        "Assignee": ("assignee", ["epic", "story", "task", "subtask"]),
        "Labels": ("labels", ["epic", "story", "task", "subtask"]),
        "Parent": ("parent", ["story", "task", "subtask"]),
        "Time tracking": ("timetracking", ["subtask"]),
    }
    for label, (fid, used) in need.items():
        cells = [label]
        for k in kinds:
            if not meta.types[k]:
                cells.append("–")
            elif k not in used:
                cells.append("")
            else:
                cells.append("✅" if fid in meta.fields(k) else "⚠️ not on screen")
        out.append("| " + " | ".join(cells) + " |")
    cells = ["Story points"]
    for k in kinds:
        if k in ("story", "task") and meta.types[k]:
            pf = meta.points_field(k)
            name = next((f["name"] for f in meta.all_fields if f["id"] == pf), pf)
            cells.append(f"✅ {name}" if pf else "❌ not found")
            if k == "story" and not pf:
                ok = False
        else:
            cells.append("")
    out.append("| " + " | ".join(cells) + " |")
    for k in kinds:
        if meta.types[k]:
            req = [f.get("name") or fid for fid, f in meta.fields(k).items()
                   if f.get("required") and not f.get("hasDefaultValue")
                   and fid not in ("project", "issuetype", "summary", "reporter", "parent")
                   and (f.get("name") or "").lower() != "epic name"]
            if req:
                out.append(f"\n❌ {k} issues require fields the sync can't fill: {', '.join(req)}")
                ok = False
    lt = str(cfg.get("link_type") or "none")
    if lt.lower() != "none":
        types = [t["name"] for t in jira.get("/rest/api/3/issueLinkType").get("issueLinkTypes", [])]
        out.append("")
        out.append(f"✅ Link type **{lt}** exists" if lt.lower() in (t.lower() for t in types)
                   else f"❌ Link type **{lt}** not found. Available: {', '.join(types)}")
    ac = cfg.get("acceptance_criteria_field")
    if ac and str(ac).lower() != "none":
        out.append(f"✅ Acceptance criteria field **{ac}** found" if meta.ac_field()
                   else f"❌ Acceptance criteria field **{ac}** not on Story issues")
    sp = Sprints(jira, meta.project, cfg)
    sp.load()
    out += ["", "**Board and sprints**", ""]
    if sp.error:
        out.append(f"⚠️ Sprint placement is off: {sp.error}. New issues go to the backlog.")
    else:
        open_ = [s["name"] + (" (active)" if s.get("state") == "active" else "") for s in sp.sprints if s.get("state") in ("active", "future")]
        kind = {"scrum": "company-managed Scrum", "simple": "team-managed"}.get(sp.board.get("type"), sp.board.get("type"))
        out.append(f"✅ Board **{sp.board['name']}** (id {sp.board['id']}, {kind}). Open sprints: {', '.join(open_) or 'none'}")
        if sp.note:
            out.append(f"⚠️ {sp.note}")
        targets = {target_sprint(ep, st, it) for ep in epics for st in ep.stories for it in [None] + st.items
                   if it is None or it.kind == "task"}
        targets |= {target_sprint(ep, None, it) for ep in epics for it in ep.tasks}
        targets = sorted(targets - {""})
        for t in targets:
            hit, why = sp.resolve(t)
            out.append(f"- ✅ '{t}' → {hit['name']}" if hit else f"- ⚠️ '{t}': {why}")
    out += ["", "**Team members** (.jira/team.yml)", ""]
    sy = Syncer(jira, meta, cfg, team)
    for h in team:
        acc = sy.account(h)
        out.append(f"- {'✅' if acc else '❌'} @{h} → {team[h]}")
    sy.warned.clear()
    out += ["", f"Epic files found: {len(epics)}"]
    write_report(report, "\n".join(out))
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command", choices=["validate", "sync", "doctor", "import"])
    ap.add_argument("--root", default=str(Path(__file__).resolve().parent.parent), help="repository root")
    ap.add_argument("--report", help="also write the report to this file")
    ap.add_argument("--force", action="store_true", help="update issues even if nothing changed")
    a = ap.parse_args()
    root = Path(a.root)
    if a.command == "validate":
        sys.exit(cmd_validate(root, a.report))
    if a.command == "sync":
        sys.exit(cmd_sync(root, a.report, a.force))
    if a.command == "import":
        sys.exit(cmd_import(root, a.report))
    sys.exit(cmd_doctor(root, a.report))


if __name__ == "__main__":
    main()
