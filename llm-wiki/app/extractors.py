from __future__ import annotations

from pathlib import Path
import re


def extract_pdf(file_path: Path) -> str:
    from pypdf import PdfReader

    reader = PdfReader(str(file_path))
    pages_text = []
    for idx, page in enumerate(reader.pages, 1):
        text = page.extract_text() or ""
        text = text.strip()
        if text:
            pages_text.append(f"<!-- Seite {idx} -->\n{text}")
    return "\n\n".join(pages_text)


def extract_docx(file_path: Path) -> str:
    import docx

    doc = docx.Document(str(file_path))
    content_blocks = []

    # 1. Absaetze & Ueberschriften
    for p in doc.paragraphs:
        text = p.text.strip()
        if not text:
            continue
        style_name = p.style.name.lower() if p.style else ""
        if "heading 1" in style_name:
            content_blocks.append(f"# {text}")
        elif "heading 2" in style_name:
            content_blocks.append(f"## {text}")
        elif "heading 3" in style_name:
            content_blocks.append(f"### {text}")
        else:
            content_blocks.append(text)

    # 2. Tabellen in sauberes Markdown-Format umwandeln
    for table in doc.tables:
        rows_data = []
        for row in table.rows:
            row_cells = [cell.text.strip().replace("\n", " ") for cell in row.cells]
            if any(row_cells):
                rows_data.append(row_cells)
        if rows_data:
            header = rows_data[0]
            col_count = max(len(header), max((len(r) for r in rows_data), default=1))
            padded_header = header + [""] * (col_count - len(header))
            md_table = [
                "| " + " | ".join(padded_header) + " |",
                "| " + " | ".join(["---"] * col_count) + " |",
            ]
            for row in rows_data[1:]:
                padded_row = row + [""] * (col_count - len(row))
                md_table.append("| " + " | ".join(padded_row[:col_count]) + " |")
            content_blocks.append("\n".join(md_table))

    return "\n\n".join(content_blocks)


def extract_xlsx(file_path: Path) -> str:
    import openpyxl

    wb = openpyxl.load_workbook(str(file_path), data_only=True, read_only=True)
    sheets_output = []

    for sheet_name in wb.sheetnames:
        ws = wb[sheet_name]
        rows = list(ws.iter_rows(values_only=True))
        # Leere Zeilen filtern
        non_empty_rows = [
            r for r in rows if any(cell is not None and str(cell).strip() != "" for cell in r)
        ]
        if not non_empty_rows:
            continue

        sheet_md = [f"## Tabellenblatt: {sheet_name}\n"]
        max_cols = max(len(r) for r in non_empty_rows)

        # Erste nicht-leere Zeile als Header
        header = [str(c) if c is not None else "" for c in non_empty_rows[0]]
        header += [""] * (max_cols - len(header))
        sheet_md.append("| " + " | ".join(header) + " |")
        sheet_md.append("| " + " | ".join(["---"] * max_cols) + " |")

        for r in non_empty_rows[1:]:
            row_vals = [str(c).replace("\n", " ").strip() if c is not None else "" for c in r]
            row_vals += [""] * (max_cols - len(row_vals))
            sheet_md.append("| " + " | ".join(row_vals[:max_cols]) + " |")

        sheets_output.append("\n".join(sheet_md))

    wb.close()
    return "\n\n".join(sheets_output)


def extract_text_file(file_path: Path) -> str:
    try:
        return file_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return file_path.read_text(encoding="latin-1", errors="replace")


def extract_text_from_file(file_path: Path, filename: str) -> str:
    """Extrahiert Volltext aus einer hochgeladenen Datei je nach Dateiendung."""
    ext = Path(filename).suffix.lower()

    if ext == ".pdf":
        return extract_pdf(file_path)
    elif ext in (".docx", ".doc"):
        return extract_docx(file_path)
    elif ext in (".xlsx", ".xls"):
        return extract_xlsx(file_path)
    elif ext in (".md", ".markdown", ".txt"):
        return extract_text_file(file_path)
    else:
        # Fallback: Versuche als Textdatei einzulesen
        return extract_text_file(file_path)
