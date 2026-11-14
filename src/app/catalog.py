"""Document facts shown on source cards: legal status, date and official link.

Legal status comes from config/documents.yaml; the official URL, version date and
collection date come from data/manifest.csv, the project's source register.
"""
from __future__ import annotations

import csv
import re
from functools import lru_cache
from urllib.parse import urlparse

import yaml

from src.shared.common import ROOT

# Turkish label and colour category for each legal status (see the UI mockup).
LEGAL_STATUS = {
    "binding law": ("Kanun (bağlayıcı)", "law"),
    "policy/plan": ("Politika / plan", "plan"),
    "report": ("Rapor (öneri)", "report"),
    "guidance": ("Rehber", "guide"),
    "institutional policy": ("Kurum politikası", "inst"),
}
MONTHS = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos",
          "Eylül", "Ekim", "Kasım", "Aralık"]
DATE_NOTES = {"announced": "açıklanma", "official gazette": "Resmî Gazete"}


def turkish_date(value: str) -> str:
    """'2026-06-13 (announced)' -> '13.06.2026 (açıklanma)'; '2026-03' -> 'Mart 2026'."""
    value = (value or "").strip()
    m = re.match(r"(\d{4})-(\d{2})(?:-(\d{2}))?\s*(?:\((.*)\))?", value)
    if not m:
        return value
    year, month, day, note = m.groups()
    text = f"{day}.{month}.{year}" if day else f"{MONTHS[int(month) - 1]} {year}"
    note = DATE_NOTES.get((note or "").split(",")[0].strip().lower())
    return f"{text} ({note})" if note else text


def long_date(iso: str) -> str:
    """'2026-10-14' -> '14 Ekim 2026'."""
    y, m, d = iso.split("-")
    return f"{int(d)} {MONTHS[int(m) - 1]} {y}"


@lru_cache(maxsize=1)
def manifest() -> dict[str, dict]:
    with (ROOT / "data/manifest.csv").open(encoding="utf-8") as f:
        return {row["doc_id"]: row for row in csv.DictReader(f)}


@lru_cache(maxsize=1)
def documents() -> dict[str, dict]:
    raw = yaml.safe_load((ROOT / "config/documents.yaml").read_text(encoding="utf-8"))["documents"]
    out = {}
    for name, entry in raw.items():
        row = manifest().get(entry["doc_id"], {})
        label, category = LEGAL_STATUS.get(entry["legal_status"], (entry["legal_status"], "plan"))
        url = row.get("source_url", "")
        out[name] = {
            "doc_id": entry["doc_id"],
            "title": entry.get("short_title", name),
            "legal_status": label,
            "legal_category": category,
            "date": turkish_date(row.get("version_date", "")),
            "url": url,
            "domain": urlparse(url).netloc.removeprefix("www."),
        }
    return out


def document_facts(document_name: str) -> dict:
    """Facts for one document; unknown names still get a usable card."""
    return documents().get(document_name, {
        "doc_id": "", "title": document_name, "legal_status": "Belirtilmemiş",
        "legal_category": "plan", "date": "", "url": "", "domain": "",
    })


def collection_date() -> str:
    """Latest collection date in the source register, as '14 Ekim 2026'."""
    dates = [r["collection_date"] for r in manifest().values() if r.get("collection_date")]
    return long_date(max(dates)) if dates else ""
