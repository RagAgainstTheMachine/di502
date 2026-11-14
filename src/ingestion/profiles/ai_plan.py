"""Optional layout profile for the 44-page Turkish AI action plan only."""

import re

TITLE = "Türkiye Yapay Zekâ Eylem Planı 2026-2030"
ACTION_HEADING = re.compile(r"^Eylem\s+(\d{1,2})\s*[-–—.:]\s*", re.IGNORECASE)
SECTION_MARKER = re.compile(r"(?=\bHedefimiz\s*[,;:]|\bAna sorumlu\s*:)", re.IGNORECASE)
AXES = {1: "Fark Et", 2: "İstifade Et", 3: "Üret", 4: "Yönet"}


def axis_for(action: int) -> str:
    return AXES[(action - 1) // 4 + 1]



def action_blocks(blocks: list[dict], page_widths: dict[int, float]) -> list[dict]:
    selected = []
    for block in blocks:
        if not 21 <= block["page"] <= 35:
            continue
        text = block["text"]
        if text.isdigit():
            continue
        if block["page"] == 21 and block["bbox"][2] < page_widths[21] * 0.34:
            continue  # Decorative chapter sidebar, not action content.
        if block["page"] == 21 and text in {"FARK ET.", "İSTİFADE ET.", "ÜRET.", "YÖNET."}:
            continue
        selected.append(block)
    # Repair the two-column reading order before detecting semantic boundaries.
    ordered = sorted(selected, key=lambda b: (b["page"], 0 if b["page"] == 21 else int(b["bbox"][0] > page_widths[b["page"]] * 0.5), b["bbox"][1], b.get("table_row", 0)))
    result, between_axes = [], True
    for block in ordered:
        if block["text"].startswith("EKSEN "):
            between_axes = True
            continue
        if ACTION_HEADING.match(block["text"]):
            between_axes = False
        if not between_axes:
            result.append(block)
    return result



def segment_actions(blocks: list[dict], document_id: str) -> list[dict]:
    parents, current = [], None
    section = "Açıklama"
    for block in blocks:
        text = block["text"]
        match = ACTION_HEADING.match(text)
        if match:
            action = int(match.group(1))
            if action != len(parents) + 1:
                raise ValueError(f"Eylem okuma sırası hatalı: {action}; beklenen {len(parents)+1}.")
            current = {"parent_id": f"{document_id}:action_{action:02d}", "document_id": document_id, "action_id": action, "axis": axis_for(action), "title": text, "kind": "action", "blocks": []}
            parents.append(current)
            section = "Açıklama"
        if current is None:
            continue
        for part in SECTION_MARKER.split(text):
            if not part.strip():
                continue
            if re.match(r"Hedefimiz\s*[,;:]", part, re.IGNORECASE):
                section = "Hedefler"
            elif re.match(r"Ana sorumlu\s*:", part, re.IGNORECASE):
                section = "Sorumlular"
            current["blocks"].append({**block, "text": part.strip(), "section": section})
    if len(parents) != 16:
        raise ValueError(f"16 eylem bekleniyor; {len(parents)} bulundu.")
    for parent in parents:
        sections = {b["section"] for b in parent["blocks"]}
        if sections != {"Açıklama", "Hedefler", "Sorumlular"}:
            raise ValueError(f"Eylem {parent['action_id']}: hedef/sorumlu bölümü eksik: {sections}.")
    return parents



def segment_glossary(blocks: list[dict], page_widths: dict[int, float], document_id: str) -> list[dict]:
    parents = []
    for page in range(36, 40):
        on_page = [b for b in blocks if b["page"] == page and not b["text"].isdigit()]
        # Glossary is laid out as term/definition rows, not two reading columns.
        table_rows = [b for b in on_page if "table_row" in b and " | " in b["text"]]
        if table_rows:
            pairs = [(b["text"].split(" | ", 1)[0], b["text"].split(" | ", 1)[1], b) for b in table_rows]
        else:
            boundary = page_widths[page] * (0.51 if page == 36 else 0.31)
            left = sorted((b for b in on_page if b["bbox"][2] < boundary), key=lambda b: b["bbox"][1])
            right = sorted((b for b in on_page if b["bbox"][0] >= boundary - 4), key=lambda b: b["bbox"][1])
            terms, pending = [], []
            for block in left:
                if page == 36 and block["bbox"][0] < page_widths[page] * 0.25:
                    continue
                pending.append(block)
                if block["text"].endswith(":"):
                    terms.append((" ".join(b["text"] for b in pending), pending[0]))
                    pending = []
            if pending:
                raise ValueError(f"Sözlük s.{page}: tanımsız kavram satırı.")
            pairs = []
            for i, (term, block) in enumerate(terms):
                top = block["bbox"][1] - 4
                bottom = terms[i+1][1]["bbox"][1] - 4 if i+1 < len(terms) else float("inf")
                definitions = [b["text"] for b in right if top <= b["bbox"][1] < bottom]
                if not definitions:
                    raise ValueError(f"Sözlük tanımı bulunamadı: {term}")
                pairs.append((term, " ".join(definitions), block))
        for term, definition, block in pairs:
            term = term.rstrip(": ")
            # TableFormer serializes line breaks as spaces. In these glossary
            # rows, lowercase '- ' joins are verified line-wrapped words.
            definition = re.sub(r"(?<=[a-zçğıöşü])-\s+(?=[a-zçğıöşü])", "", definition)
            parent_id = f"{document_id}:term_{len(parents)+1:02d}"
            parents.append({"parent_id": parent_id, "document_id": document_id, "action_id": None, "axis": None, "title": term, "kind": "glossary", "blocks": [{**block, "text": f"{term}: {definition}", "section": "Terimler Sözlüğü"}]})
    if len(parents) != 38:
        raise ValueError(f"Sözlükte 38 kavram bekleniyor; {len(parents)} bulundu.")
    return parents



def segment_other(blocks: list[dict], document_id: str) -> list[dict]:
    major_by_page = {3: "Künye", 5: "Takdim", 7: "Sunuş", 9: "İçindekiler", 10: "Yönetici Özeti", 11: "Yönetici Özeti", 12: "Vizyon ve Stratejik Yaklaşım", 13: "Vizyon ve Stratejik Yaklaşım", 14: "Planın Mimarisi", 15: "Uygulama İlkeleri", 16: "Dört Eksen", 17: "Dört Eksen", 18: "Uygulama, Yönetişim ve İzleme", 19: "Uygulama, Yönetişim ve İzleme", 20: "Uygulama, Yönetişim ve İzleme", 36: "Terimler Sözlüğü - Giriş", 40: "İzleme ve Raporlama", 41: "Mevcut Durum ve Hedefler", 42: "İletişim"}
    parents, current, current_major = [], None, None
    for block in blocks:
        glossary_intro = block["page"] == 36 and block["text"].startswith("Bu sözlükte")
        if (21 <= block["page"] <= 39 and not glossary_intro) or block["text"].isdigit():
            continue
        is_heading = block["label"] in {"section_header", "title"}
        major = major_by_page.get(block["page"], f"PDF sayfa {block['page']}")
        if current is None or is_heading or major != current_major:
            title = f"{major} / {block['text']}" if is_heading else major
            current = {"parent_id": f"{document_id}:section_{len(parents)+1:03d}", "document_id": document_id, "action_id": None, "axis": None, "title": title, "kind": "section", "blocks": []}
            parents.append(current)
            current_major = major
        current["blocks"].append({**block, "section": current["title"]})
    return parents


def build_parents(document, blocks: list[dict], document_id: str) -> list[dict]:
    if len(document.pages) != 44:
        raise ValueError("ai-plan profili yalnızca 44 sayfalık Türkiye Yapay Zekâ Eylem Planı içindir.")
    widths = {n: page.size.width for n, page in document.pages.items()}
    return (segment_other(blocks, document_id)
            + segment_actions(action_blocks(blocks, widths), document_id)
            + segment_glossary(blocks, widths, document_id))
