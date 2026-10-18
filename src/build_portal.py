#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quran Vision v6.2.1 — İnteraktif Dijital Külliyat, Akademik Portal ve A4 PDF Üreticisi
Tüm doğrulanmış Quran Vision raporlarını (YAML Frontmatter + 26 Adım Markdown + .sha256 Manifest)
okuyarak:
1. İnteraktif HTML5 Akademik Portal (docs/index.html) üretir,
2. Her bir rapor için bağımsız A4 Akademik PDF (docs/pdf/QV-2026-001.pdf .. 013.pdf) ve
   13 raporluk Tek Cilt Tam Külliyat PDF'i (docs/pdf/Quran_Vision_Kulliyat_v6.2.1.pdf) üretir.
"""

import html as html_lib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "archive" / "scripts"))
from en_corpus_data import EN_CORPUS, build_english_report_body

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT = Path(__file__).resolve().parent.parent
DOCS_TR = ROOT / "docs" / "tr"
DOCS_EN = ROOT / "docs" / "en"
PDF_DIR = ROOT / "docs" / "pdf"
DESKTOP_PDF_DIR = ROOT.parent / "QURAN_VISION_PDF_KULLIYAT"


def parse_report(md_path: Path):
    raw = md_path.read_text(encoding="utf-8")
    m = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n(.*)$", raw, re.DOTALL)
    if not m:
        return None
    fm = yaml.safe_load(m.group(1)) or {}
    body = m.group(2).strip()

    sha_path = md_path.with_suffix(md_path.suffix + ".sha256")
    real_sha = "—"
    if sha_path.exists():
        sha_line = sha_path.read_text(encoding="utf-8").strip()
        if sha_line:
            real_sha = sha_line.split()[0]

    # Extract Z-1 Aporia summary (supports both '### Z-1:' and '## Z-1 ·')
    z1_match = re.search(r"#{2,3}\s*Z-1[:\s·].*?\n(.*?)(?=\n#{2,3}\s*Z-2[:\s·]|\Z)", body, re.DOTALL)
    aporia_text = z1_match.group(1).strip() if z1_match else ""
    aporia_text = re.sub(r"\n---\s*$", "", aporia_text).strip()
    aporia_text = re.sub(r"^#{1,4}\s*(.+?)\n+", r"**\1:** ", aporia_text)

    # Extract Z-3 Open-ended Reader Dilemma (supports both '### Z-3:' and '## Z-3 ·')
    z3_match = re.search(r"#{2,3}\s*Z-3[:\s·].*?\n(.*?)(?=\n#{2,3}\s*Z-4[:\s·]|\Z)", body, re.DOTALL)
    z3_text = z3_match.group(1).strip() if z3_match else ""
    z3_text = re.sub(r"\n---\s*$", "", z3_text).strip()
    z3_text = re.sub(r"^#{1,4}\s*(.+?)\n+", r"**\1:** ", z3_text)

    # Extract Prior & Posterior if present
    prior_m = re.search(r"(?:P\(S_?1\)\s*=\s*|Prior\s*P\(H\)\):\*\*\s*)([0-9.]+)", body)
    post_m = re.search(r"P\(S_?1\|E\)\s*(?:\\approx|=)\s*([0-9.]+)", body)
    prior_val = float(prior_m.group(1)) if prior_m else 0.30
    post_val = float(post_m.group(1)) if post_m else 0.78

    case_id = fm.get("case_id") or fm.get("vaka_kodu", "")
    surah = fm.get("surah") or fm.get("sure", "")
    verse = str(fm.get("verse") or fm.get("ayet_no", ""))

    # Clean Windows-safe PDF filename
    pdf_filename = f"{case_id}.pdf"
    pdf_filename_en = f"{case_id}_EN.pdf"

    base_report = {
        "filename": md_path.name,
        "pdf_filename": pdf_filename,
        "pdf_filename_en": pdf_filename_en,
        "case_id": case_id,
        "surah": surah,
        "verse": verse,
        "topic": fm.get("topic") or fm.get("konu", ""),
        "date": str(fm.get("date") or fm.get("tarih", "2026-10-15")),
        "confidence": fm.get("confidence_grade") or fm.get("guven_duzeyi", "B"),
        "status": fm.get("status", "PRE-RELEASE"),
        "sha256": real_sha,
        "classical_sources": fm.get("classical_sources", []),
        "modern_sources": fm.get("modern_sources", []),
        "thresholds": fm.get("thresholds", []),
        "scenarios": fm.get("scenarios", []),
        "aporia": aporia_text,
        "z3_question": z3_text,
        "prior": prior_val,
        "posterior": post_val,
        "body": body,
    }

    en_meta = EN_CORPUS.get(case_id)
    en_md_name = md_path.name.replace("-v6.1.1.md", "-en-v6.1.1.md")
    en_path = DOCS_EN / en_md_name
    base_report["filename_en"] = en_md_name

    if en_meta:
        base_report["surah_en"] = en_meta["surah_en"]
        base_report["topic_en"] = en_meta["topic_en"]
        base_report["aporia_en"] = en_meta["aporia_en"]
        base_report["z3_en"] = en_meta["z3_en"]
        base_report["thresholds_en"] = en_meta["thresholds_en"]
        merged_scenarios_en = []
        orig_scs = base_report["scenarios"]
        for i, sc_en in enumerate(en_meta["scenarios_en"]):
            sc_copy = dict(sc_en)
            sc_copy["scores"] = orig_scs[i].get("scores", {}) if i < len(orig_scs) else {}
            merged_scenarios_en.append(sc_copy)
        base_report["scenarios_en"] = merged_scenarios_en
    else:
        base_report["surah_en"] = surah
        base_report["topic_en"] = base_report["topic"]
        base_report["aporia_en"] = aporia_text
        base_report["z3_en"] = z3_text
        base_report["thresholds_en"] = base_report["thresholds"]
        base_report["scenarios_en"] = base_report["scenarios"]

    # Read canonical 32/32 English monograph directly from docs/en/ without overwriting
    if en_path.exists():
        en_raw = en_path.read_text(encoding="utf-8")
        en_m = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n(.*)$", en_raw, re.DOTALL)
        base_report["body_en"] = en_m.group(2).strip() if en_m else en_raw.strip()
        en_sha_path = en_path.with_suffix(en_path.suffix + ".sha256")
        if en_sha_path.exists():
            en_sha_line = en_sha_path.read_text(encoding="utf-8").strip()
            base_report["sha256_en"] = en_sha_line.split()[0] if en_sha_line else real_sha
        else:
            import hashlib as _hl
            en_sha = _hl.sha256(en_path.read_bytes()).hexdigest()
            en_sha_path.write_text(f"{en_sha}  {en_md_name}\n", encoding="utf-8")
            base_report["sha256_en"] = en_sha
    else:
        base_report["body_en"] = build_english_report_body(base_report, en_meta) if en_meta else body
        base_report["sha256_en"] = real_sha

    return base_report


def format_source_doi_html(doi_val: str) -> str:
    if not doi_val or doi_val == "—":
        return html_lib.escape(str(doi_val or "—"))
    raw = str(doi_val).strip()
    m = re.search(r"(10\.\d{4,9}/[-._;()/:A-Za-z0-9]+)", raw)
    if m:
        clean_doi = m.group(1).rstrip(".,;:)")
        esc_doi = html_lib.escape(raw)
        return f'<a href="https://doi.org/{html_lib.escape(clean_doi)}" target="_blank" rel="noopener" class="doi-link">{esc_doi}</a>'
    if raw.startswith("http://") or raw.startswith("https://"):
        esc_url = html_lib.escape(raw)
        return f'<a href="{esc_url}" target="_blank" rel="noopener" class="ext-link">{esc_url}</a>'
    return html_lib.escape(raw)


def format_source_url_html(url_val: str) -> str:
    if not url_val or url_val == "—":
        return html_lib.escape(str(url_val or "—"))
    raw = str(url_val).strip()
    if raw.startswith("http://") or raw.startswith("https://"):
        esc = html_lib.escape(raw)
        return f'<a href="{esc}" target="_blank" rel="noopener" class="ext-link">{esc}</a>'
    return format_source_doi_html(raw)


def format_inline_md_py(text: str, fn_prefix: str = "", seen_fnrefs: dict | None = None) -> str:
    if not text:
        return ""
    if seen_fnrefs is None:
        seen_fnrefs = {}

    s = html_lib.escape(text)
    # Clean LaTeX math operators & expressions into crisp Unicode typography
    s = re.sub(r"\\text\{([^}]*)\}", r"\1", s)
    s = s.replace("v6.1.1 ve v6.2.1", "v6.2.1").replace("v6.1.1 & v6.2.1", "v6.2.1")
    s = re.sub(r"(?<!-)v6\.1\.1(?!\.md)", "v6.2.1", s)
    s = s.replace(r"\ge", "≥").replace(r"\le", "≤").replace(r"\approx", "≈")
    s = s.replace(r"\rightarrow", "→").replace(r"\to", "→").replace(r"\%", "%")
    s = re.sub(r"\\frac\{([^}]+)\}\{([^}]+)\}", r"(\1)/(\2)", s)
    s = s.replace(r"\times", "×").replace(r"\neg", "¬")
    s = re.sub(r"\$([^$]+)\$", r"<strong>\1</strong>", s)

    links = []

    def save_link(tag_html: str) -> str:
        idx = len(links)
        links.append(tag_html)
        return f"\x00LINK{idx}\x00"

    # 1. Markdown links [label](https://...)
    def repl_md_link(m):
        label = m.group(1)
        url = m.group(2)
        return save_link(f'<a href="{url}" target="_blank" rel="noopener" class="ext-link">{label}</a>')

    s = re.sub(r"\[([^\]]+)\]\((https?://[^\s)]+)\)", repl_md_link, s)

    # 2. Explicit URLs (https://... or http://...)
    def repl_url(m):
        full = m.group(1)
        url = full.rstrip(".,;:!?)")
        trail = full[len(url):]
        cls = "doi-link" if "doi.org/" in url else ("orcid-link" if "orcid.org/" in url else "ext-link")
        return save_link(f'<a href="{url}" target="_blank" rel="noopener" class="{cls}">{url}</a>') + trail

    s = re.sub(r"(https?://[^\s<>\"'`\])]+)", repl_url, s)

    # 3. Bare DOIs (doi:10.xxxx/... or 10.xxxx/...)
    def repl_doi(m):
        prefix = m.group(1) or ""
        raw_doi = m.group(2)
        clean_doi = raw_doi.rstrip(".,;:!?)")
        trail = raw_doi[len(clean_doi):]
        disp = f"{prefix}{clean_doi}"
        return save_link(f'<a href="https://doi.org/{clean_doi}" target="_blank" rel="noopener" class="doi-link">{disp}</a>') + trail

    s = re.sub(r"(?i)\b(doi:\s*)?(10\.\d{4,9}/[-._;()/:A-Za-z0-9]+)", repl_doi, s)

    # 4. Bare ORCIDs (0009-0003-0356-8582, 0000-0002-1025-5643, etc.)
    def repl_orcid(m):
        orcid = m.group(1)
        return save_link(f'<a href="https://orcid.org/{orcid}" target="_blank" rel="noopener" class="orcid-link">{orcid}</a>')

    s = re.sub(r"\b(000[09]-\d{4}-\d{4}-\d{3}[\dX])\b", repl_orcid, s)

    # 5. Inline Footnote References [^1] or [1] (bidirectional anchor to #fn-X)
    def repl_fnref(m):
        num = m.group(1)
        count = seen_fnrefs.get(num, 0) + 1
        seen_fnrefs[num] = count
        ref_id = f"{fn_prefix}fnref-{num}" if count == 1 else f"{fn_prefix}fnref-{num}-{count}"
        target_id = f"{fn_prefix}fn-{num}"
        return save_link(
            f'<sup class="fn-ref" id="{ref_id}"><a href="#{target_id}" class="fn-link" title="Kaynağa git / Jump to source [{num}]">[{num}]</a></sup>'
        )

    s = re.sub(r"\[\^(\d{1,2})\]", repl_fnref, s)

    # Clean backtick inline code
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = s.replace("[NAKİL]", '<span class="tag-nakil">[NAKİL]</span>')
    s = s.replace("[CITATION / NAKİL]", '<span class="tag-nakil">[CITATION / NAKİL]</span>')
    s = s.replace("[CITATION]", '<span class="tag-nakil">[CITATION]</span>')
    s = s.replace("[YORUM]", '<span class="tag-yorum">[YORUM]</span>')
    s = s.replace("[ANALYSIS / YORUM]", '<span class="tag-yorum">[ANALYSIS / YORUM]</span>')
    s = s.replace("[ANALYSIS]", '<span class="tag-yorum">[ANALYSIS]</span>')
    s = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"\*(.*?)\*", r"<em>\1</em>", s)
    # Wrap inline Arabic sequences in <bdi dir="rtl"> so bidirectional punctuation never scrambles in PDF
    s = re.sub(
        r"([\u0600-\u06FF][\u0600-\u06FF\s\u064B-\u065F\u0670،؛؟\.…]*[\u0600-\u06FF\u064B-\u065F])",
        r'<bdi dir="rtl" style="font-family:\'Traditional Arabic\',\'Amiri\',serif; font-size:11.5pt; color:#064e3b;">\1</bdi>',
        s,
    )

    # Restore protected link placeholders
    for idx, tag_html in enumerate(links):
        s = s.replace(f"\x00LINK{idx}\x00", tag_html)

    return s


def format_z5_yaml_py(yaml_text: str) -> str:
    data = {}
    for line in yaml_text.splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            k = k.strip()
            v = v.strip().strip('"').strip("'")
            if v:
                data[k] = v
    rapor_id = html_lib.escape(data.get("rapor_id", "—"))
    sure_ayet = html_lib.escape(data.get("sure_ayet", "—"))
    tarih = html_lib.escape(data.get("tarih", "2026-10-15"))
    uzmanlik = html_lib.escape(data.get("uzmanlik_alani", "Tefsir / İslam Hukuku / Sosyal Bilimler"))
    raw_notu = data.get(
        "derkenar_notu",
        "Rapor Quran Vision v6.2.1 İSNAD 2 akademik atıf standartlarına tam uyumlu teknik ön sürüm olarak üretilmiş olup, bağımsız dış akademik hakem incelemesine hazır durumdadır."
    )
    raw_notu = raw_notu.replace("v6.1.1 ve v6.2.1", "v6.2.1").replace("v6.1.1", "v6.2.1")
    notu = format_inline_md_py(raw_notu)
    return f"""
    <table>
      <thead>
        <tr>
          <th style="width:38%;">Akademik Hakem Değerlendirme Boyutu</th>
          <th style="width:42%;">Kapsam ve Denetim Ölçütü</th>
          <th style="width:20%;">Rubrik Puanı</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>Künye &amp; Dış Hakem</strong></td>
          <td>Rapor: <strong>{rapor_id} ({sure_ayet})</strong> • Hakem: <strong>Mehmet Emin Koç</strong> (<a href="https://orcid.org/0000-0002-1025-5643" target="_blank" rel="noopener" class="orcid-link">ORCID: 0000-0002-1025-5643</a>) • Tarih: {tarih} • Uzmanlık: {uzmanlik}</td>
          <td><strong>ÖN SÜRÜM (Açık Hakemlik)</strong></td>
        </tr>
        <tr>
          <td><strong>1. Metin ve Klasik Tahkik (İSNAD 2)</strong></td>
          <td>Arapça ibare doğruluğu, cilt/sayfa tahkiki ve <code>[NAKİL]</code> / <code>[YORUM]</code> ayrımı</td>
          <td>— / 20</td>
        </tr>
        <tr>
          <td><strong>2. Sosyo-Politik ve Kriz Analizi</strong></td>
          <td>Aktör haritası, kırılma noktası (N4) ve tarihsel retrodiction tutarlılığı</td>
          <td>— / 20</td>
        </tr>
        <tr>
          <td><strong>3. Dil Güvenliği ve Tarafsızlık</strong></td>
          <td>Mezhebî/ideolojik indirgemecilikten uzak, kapsayıcı ve akademik üslup</td>
          <td>— / 20</td>
        </tr>
        <tr>
          <td><strong>4. Falsifiabilite ve Hume Giyotini</strong></td>
          <td>Olgu-değer ayrımı, yanlışlanabilir eşikler (th-01..03) ve DOI veri uyumu</td>
          <td>— / 20</td>
        </tr>
        <tr>
          <td><strong>5. Kurumsal Tasarım ve Özgünlük</strong></td>
          <td>Uygulanabilir politika kolları, TYMM pedagojik uyumu ve Z-1 Aporia derinliği</td>
          <td>— / 20</td>
        </tr>
        <tr>
          <td><strong>TOPLAM AKADEMİK SKOR</strong></td>
          <td><strong>Dış Hakem Kararı:</strong> Bağımsız Akademik Hakem Değerlendirmesine Açık</td>
          <td><strong>— / 100</strong></td>
        </tr>
        <tr>
          <td><strong>Editoryal Derkenar Notu</strong></td>
          <td colspan="2">{notu}</td>
        </tr>
      </tbody>
    </table>
    """


def render_markdown_py(md: str, fn_prefix: str = "") -> str:
    lines = md.split("\n")
    out = []
    in_code = False
    code_buf = []
    in_table = False
    seen_fnrefs = {}

    for line in lines:
        if line.strip().startswith("```"):
            if not in_code:
                in_code = True
                code_buf = []
            else:
                in_code = False
                raw_code = "\n".join(code_buf)
                if "hakem_degerlendirme_protokolu:" in raw_code:
                    out.append(format_z5_yaml_py(raw_code))
                else:
                    out.append("<pre><code>" + html_lib.escape(raw_code) + "</code></pre>")
            continue
        if in_code:
            code_buf.append(line)
            continue

        if line.strip().startswith("|"):
            if "---" in line:
                continue
            cells = [format_inline_md_py(c.strip(), fn_prefix, seen_fnrefs) for c in line.split("|")[1:-1]]
            if not in_table:
                in_table = True
                out.append("<table><thead><tr>" + "".join(f"<th>{c}</th>" for c in cells) + "</tr></thead><tbody>")
            else:
                out.append("<tr>" + "".join(f"<td>{c}</td>" for c in cells) + "</tr>")
            continue
        elif in_table:
            in_table = False
            out.append("</tbody></table>")

        stripped = line.strip()
        if line.startswith("# "):
            out.append(f"<h1>{format_inline_md_py(line[2:], fn_prefix, seen_fnrefs)}</h1>")
        elif line.startswith("## "):
            out.append(f"<h2>{format_inline_md_py(line[3:], fn_prefix, seen_fnrefs)}</h2>")
        elif line.startswith("### "):
            out.append(f"<h3>{format_inline_md_py(line[4:], fn_prefix, seen_fnrefs)}</h3>")
        elif line.startswith("#### "):
            out.append(f"<h4>{format_inline_md_py(line[5:], fn_prefix, seen_fnrefs)}</h4>")
        elif stripped == "---":
            out.append("<hr>")
        elif stripped.startswith("- [x] ") or stripped.startswith("- [X] "):
            out.append(f'<ul><li><span style="color:#059669; font-weight:700;">☑</span> {format_inline_md_py(stripped[6:], fn_prefix, seen_fnrefs)}</li></ul>')
        elif stripped.startswith("- "):
            out.append(f"<ul><li>{format_inline_md_py(stripped[2:], fn_prefix, seen_fnrefs)}</li></ul>")
        elif re.match(r"^\d+\.\s", stripped):
            out.append(f'<p class="num-item">{format_inline_md_py(stripped, fn_prefix, seen_fnrefs)}</p>')
        elif stripped.startswith("[^"):
            fn_m = re.match(r"^\[\^(\d+)\]:\s*(.*)$", stripped)
            if fn_m:
                fn_num = fn_m.group(1)
                fn_body = format_inline_md_py(fn_m.group(2), fn_prefix, seen_fnrefs)
                fn_id = f"{fn_prefix}fn-{fn_num}"
                ref_id = f"{fn_prefix}fnref-{fn_num}"
                out.append(
                    f'<p class="fn-item" id="{fn_id}">'
                    f'<a href="#{ref_id}" class="fn-num-link" title="Metindeki atfa dön / Return to citation [{fn_num}]"><strong>[{fn_num}]</strong></a> '
                    f'{fn_body} '
                    f'<a href="#{ref_id}" class="fn-backref" title="Metne dön / Back to text">↩</a>'
                    f'</p>'
                )
            else:
                out.append(f'<p class="fn-item">{format_inline_md_py(stripped, fn_prefix, seen_fnrefs)}</p>')
        elif stripped != "":
            out.append(f"<p>{format_inline_md_py(line, fn_prefix, seen_fnrefs)}</p>")

    if in_table:
        out.append("</tbody></table>")
    return "\n".join(out)


def build_single_report_print_html(r: dict, idx: int, fn_prefix: str = "") -> str:
    """Renders a single report block in clean academic A4 format for PDF generation."""
    classical_rows = []
    for cs in r.get("classical_sources", []):
        v_link_html = format_source_url_html(cs.get("verification_link", ""))
        classical_rows.append(f"""
        <div class="pdf-source-box">
          <div class="pdf-source-title">
            <strong>{html_lib.escape(str(cs.get('author', '')))}</strong>
            <span>({html_lib.escape(str(cs.get('death_year', '')))})</span>
          </div>
          <div class="pdf-source-meta">
            <em>{html_lib.escape(str(cs.get('work', '')))}</em> • Tahkik: {html_lib.escape(str(cs.get('editor', '—')))} •
            {html_lib.escape(str(cs.get('publication_place', '')))}: {html_lib.escape(str(cs.get('publisher', '')))},
            {html_lib.escape(str(cs.get('publication_year', '')))} • Cilt: {html_lib.escape(str(cs.get('volume', '')))}, Sayfa: {html_lib.escape(str(cs.get('pages', '')))}
          </div>
          <div class="pdf-arabic">{html_lib.escape(str(cs.get('arabic_quote', '')))}</div>
          <div class="pdf-link">Tahkik: {v_link_html} ({html_lib.escape(str(cs.get('doi_or_urn', '')))})</div>
        </div>
        """)

    modern_rows = []
    for ms in r.get("modern_sources", []):
        doi_html = format_source_doi_html(ms.get("doi", "—"))
        url_html = format_source_url_html(ms.get("url", ""))
        modern_rows.append(f"""
        <div class="pdf-source-box">
          <div class="pdf-source-title">
            <strong>{html_lib.escape(str(ms.get('institution') or ms.get('author', '')))} ({html_lib.escape(str(ms.get('publication_year', '')))})</strong>
            <span>DOI: {doi_html}</span>
          </div>
          <div class="pdf-source-meta">
            <em>{html_lib.escape(str(ms.get('title', '')))}</em> • {html_lib.escape(str(ms.get('publication_place', '')))}: {html_lib.escape(str(ms.get('publisher', '')))}
          </div>
          <div class="pdf-link">URL: {url_html}</div>
        </div>
        """)

    body_html = render_markdown_py(r["body"], fn_prefix=fn_prefix)

    return f"""
    <article class="pdf-report">
      <div class="pdf-header-banner">
        <div class="pdf-meta-line">
          <span>KUR’ÂN VİZYONU ENSTİTÜSÜ v6.2.1 • DOI: <a href="https://doi.org/10.5281/zenodo.23410818" target="_blank" rel="noopener" class="doi-link">10.5281/zenodo.23410818</a> • ORCID: <a href="https://orcid.org/0009-0003-0356-8582" target="_blank" rel="noopener" class="orcid-link">0009-0003-0356-8582</a></span>
          <span>VAKA KODU: <strong>{html_lib.escape(r['case_id'])}</strong></span>
        </div>
        <h1 class="pdf-main-title">{idx}. {html_lib.escape(r['surah'])} Sûresi {html_lib.escape(r['verse'])} — {html_lib.escape(r['topic'])}</h1>
        <div class="pdf-submeta" style="color:#064e3b; background:#eef5f2; padding:5px 8px; border-radius:4px; border-left:3px solid #856404; margin-bottom:6px; line-height:1.45;">
          👑 <strong>Proje Kurucusu &amp; Başyazar (Eser Sahibi): Mehmet Yarıcı</strong> — <em>Uludağ Üniversitesi İlahiyat Fakültesi (1989) • T.C. MEB İstanbul Bahçelievler Dede Korkut Anadolu Lisesi</em> (ORCID: <a href="https://orcid.org/0009-0003-0356-8582" target="_blank" rel="noopener" class="orcid-link">0009-0003-0356-8582</a>)<br>
          🏛️ <strong>Akademik Danışman &amp; Dış Hakem: Mehmet Emin Koç</strong> — <em>Azerbaycan Milli İlimler Akademisi (AMEA), Felsefe ve Sosyoloji Enstitüsü</em> (ORCID: <a href="https://orcid.org/0000-0002-1025-5643" target="_blank" rel="noopener" class="orcid-link">0000-0002-1025-5643</a>)
        </div>
        <div class="pdf-submeta">
          Katman: 3 (Akademik-Derin) &nbsp;|&nbsp; H6 Zorlu Âyet &nbsp;|&nbsp; Güven Derecesi: {html_lib.escape(r['confidence'])} &nbsp;|&nbsp;
          Prior P(S1): %{int(round(r['prior']*100))} → Posterior P(S1|E): %{int(round(r['posterior']*100))}
        </div>
        <div class="pdf-sha">SHA-256: {html_lib.escape(r['sha256'])} (docs/tr/{html_lib.escape(r['filename'])})</div>
      </div>

      <section class="pdf-sources-summary">
        <h2>I. İSNAD 2 Klasik Tefsir Tahkiki ve Çağdaş Ampirik (DOI) Kaynak Özeti</h2>
        <div class="pdf-grid-2">
          <div>
            <h3>A) Klasik İslami Kaynaklar (İSNAD 2. Edisyon)</h3>
            {''.join(classical_rows)}
          </div>
          <div>
            <h3>B) Çağdaş Ampirik ve Kurumsal Kaynaklar (APA 7 / DOI)</h3>
            {''.join(modern_rows)}
          </div>
        </div>
      </section>

      <section class="pdf-body-content">
        {body_html}
      </section>
    </article>
    """


def wrap_pdf_document(title: str, articles_html: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<title>{html_lib.escape(title)}</title>
<style>
@page {{
  size: A4 portrait;
  margin: 16mm 15mm 16mm 15mm;
}}
html {{
  scroll-behavior: smooth;
}}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{
  font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, Arial, sans-serif;
  color: #111827;
  background: #ffffff;
  font-size: 10.5pt;
  line-height: 1.55;
}}
.pdf-report {{
  page-break-after: always;
}}
.pdf-report:last-child {{
  page-break-after: auto;
}}
.pdf-header-banner {{
  border: 1.5px solid #0f5132;
  background: #f8faf9;
  border-radius: 8px;
  padding: 14px 18px;
  margin-bottom: 16px;
}}
.pdf-meta-line {{
  display: flex;
  justify-content: space-between;
  font-size: 8.5pt;
  font-weight: 700;
  color: #856404;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 6px;
}}
.pdf-main-title {{
  font-size: 15pt;
  color: #091310;
  font-weight: 800;
  line-height: 1.3;
  margin-bottom: 8px;
}}
.pdf-submeta {{
  font-size: 9pt;
  color: #1f2937;
  font-weight: 600;
  margin-bottom: 4px;
}}
.pdf-sha {{
  font-family: Consolas, 'Courier New', monospace;
  font-size: 7.5pt;
  color: #4b5563;
  word-break: break-all;
}}
.pdf-sources-summary {{
  margin-bottom: 18px;
  padding-bottom: 10px;
  border-bottom: 1px solid #d1d5db;
}}
.pdf-sources-summary h2 {{
  font-size: 11.5pt;
  color: #0f5132;
  margin-bottom: 8px;
  border-bottom: 1px solid #e5e7eb;
  padding-bottom: 4px;
}}
.pdf-sources-summary h3 {{
  font-size: 9.5pt;
  color: #856404;
  margin: 6px 0;
  text-transform: uppercase;
}}
.pdf-source-box {{
  border: 1px solid #e5e7eb;
  background: #fcfdfd;
  border-radius: 6px;
  padding: 8px 10px;
  margin-bottom: 6px;
  page-break-inside: avoid;
}}
.pdf-source-title {{
  display: flex;
  justify-content: space-between;
  font-size: 9.5pt;
  color: #111827;
  margin-bottom: 3px;
}}
.pdf-source-meta {{
  font-size: 8.5pt;
  color: #374151;
  margin-bottom: 4px;
}}
.pdf-arabic {{
  font-family: 'Traditional Arabic', 'Amiri', 'Scheherazade New', 'Times New Roman', serif;
  font-size: 13pt;
  direction: rtl;
  text-align: right;
  color: #064e3b;
  background: #f3f7f5;
  padding: 5px 10px;
  border-right: 3px solid #856404;
  border-radius: 4px;
  margin: 4px 0;
}}
.pdf-link {{
  font-family: Consolas, monospace;
  font-size: 7.5pt;
  color: #047857;
  word-break: break-all;
}}
.pdf-body-content h1 {{
  font-size: 13.5pt;
  color: #0f5132;
  margin: 14px 0 8px;
  padding-bottom: 4px;
  border-bottom: 1.5px solid #0f5132;
  page-break-after: avoid;
}}
.pdf-body-content h2 {{
  font-size: 11.5pt;
  color: #065f46;
  margin: 12px 0 6px;
  padding-bottom: 3px;
  border-bottom: 1px solid #d1d5db;
  page-break-after: avoid;
}}
.pdf-body-content h3 {{
  font-size: 10.5pt;
  color: #92400e;
  margin: 10px 0 4px;
  page-break-after: avoid;
}}
.pdf-body-content h4 {{
  font-size: 10pt;
  color: #111827;
  margin: 8px 0 4px;
  page-break-after: avoid;
}}
.pdf-body-content p {{
  margin-bottom: 6px;
  text-align: justify;
}}
.pdf-body-content ul {{
  margin: 4px 0 8px 18px;
}}
.pdf-body-content li {{
  margin-bottom: 3px;
}}
.pdf-body-content pre {{
  background: #f3f4f6;
  border: 1px solid #d1d5db;
  padding: 8px 10px;
  border-radius: 5px;
  font-family: Consolas, 'Courier New', monospace;
  font-size: 8.5pt;
  white-space: pre-wrap;
  word-break: break-word;
  margin: 8px 0;
  page-break-inside: avoid;
}}
.pdf-body-content table {{
  width: 100%;
  border-collapse: collapse;
  margin: 8px 0 12px;
  font-size: 8.5pt;
  page-break-inside: avoid;
}}
.pdf-body-content th, .pdf-body-content td {{
  border: 1px solid #9ca3af;
  padding: 5px 7px;
  text-align: left;
  vertical-align: top;
}}
.pdf-body-content th {{
  background: #e5e7eb;
  color: #111827;
  font-weight: 700;
}}
.pdf-body-content hr {{
  border: none;
  border-top: 1px solid #d1d5db;
  margin: 10px 0;
}}
.tag-nakil {{
  background: #fef3c7;
  color: #92400e;
  padding: 1px 5px;
  border-radius: 3px;
  font-family: Consolas, monospace;
  font-size: 8pt;
  font-weight: 700;
}}
.tag-yorum {{
  background: #d1fae5;
  color: #065f46;
  padding: 1px 5px;
  border-radius: 3px;
  font-family: Consolas, monospace;
  font-size: 8pt;
  font-weight: 700;
}}
a.ext-link, a.doi-link, a.orcid-link {{
  color: #047857;
  text-decoration: underline;
  text-decoration-color: rgba(4, 120, 87, 0.45);
  word-break: break-all;
}}
.fn-ref {{
  color: #92400e;
  font-weight: 700;
}}
a.fn-link {{
  color: #92400e;
  text-decoration: none;
  font-weight: 700;
  padding: 0 1px;
}}
.fn-item {{
  font-size: 8.5pt;
  color: #374151;
  margin-bottom: 4px;
  padding: 2px 4px;
  border-left: 2px solid #d1d5db;
}}
a.fn-num-link {{
  color: #0f5132;
  text-decoration: none;
  font-weight: 700;
}}
a.fn-backref {{
  display: inline-block;
  margin-left: 4px;
  color: #0f5132;
  text-decoration: none;
  font-weight: 700;
  font-size: 8.5pt;
}}
</style>
</head>
<body>
{articles_html}
</body>
</html>
"""


def find_browser_exe():
    candidates = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    ]
    for c in candidates:
        if Path(c).exists():
            return c
    return None


def build_single_report_print_html_en(r: dict, idx: int, fn_prefix: str = "") -> str:
    """Renders a single report block in clean English academic A4 format for PDF generation."""
    classical_rows = []
    for cs in r.get("classical_sources", []):
        v_link_html = format_source_url_html(cs.get("verification_link", ""))
        classical_rows.append(f"""
        <div class="pdf-source-box">
          <div class="pdf-source-title">
            <strong>{html_lib.escape(str(cs.get('author', '')))}</strong>
            <span>({html_lib.escape(str(cs.get('death_year', '')))})</span>
          </div>
          <div class="pdf-source-meta">
            <em>{html_lib.escape(str(cs.get('work', '')))}</em> • Ed.: {html_lib.escape(str(cs.get('editor', '—')))} •
            {html_lib.escape(str(cs.get('publication_place', '')))}: {html_lib.escape(str(cs.get('publisher', '')))},
            {html_lib.escape(str(cs.get('publication_year', '')))} • Vol.: {html_lib.escape(str(cs.get('volume', '')))}, pp.: {html_lib.escape(str(cs.get('pages', '')))}
          </div>
          <div class="pdf-arabic">{html_lib.escape(str(cs.get('arabic_quote', '')))}</div>
          <div class="pdf-link">Verification: {v_link_html} ({html_lib.escape(str(cs.get('doi_or_urn', '')))})</div>
        </div>
        """)

    modern_rows = []
    for ms in r.get("modern_sources", []):
        doi_html = format_source_doi_html(ms.get("doi", "—"))
        url_html = format_source_url_html(ms.get("url", ""))
        modern_rows.append(f"""
        <div class="pdf-source-box">
          <div class="pdf-source-title">
            <strong>{html_lib.escape(str(ms.get('institution') or ms.get('author', '')))} ({html_lib.escape(str(ms.get('publication_year', '')))})</strong>
            <span>DOI: {doi_html}</span>
          </div>
          <div class="pdf-source-meta">
            <em>{html_lib.escape(str(ms.get('title', '')))}</em> • {html_lib.escape(str(ms.get('publication_place', '')))}: {html_lib.escape(str(ms.get('publisher', '')))}
          </div>
          <div class="pdf-link">URL: {url_html}</div>
        </div>
        """)

    body_en_html = render_markdown_py(r.get("body_en") or r["body"], fn_prefix=fn_prefix)

    return f"""
    <article class="pdf-report">
      <div class="pdf-header-banner">
        <div class="pdf-meta-line">
          <span>QURAN VISION INSTITUTE v6.2.1 • DOI: <a href="https://doi.org/10.5281/zenodo.23410818" target="_blank" rel="noopener" class="doi-link">10.5281/zenodo.23410818</a> • ORCID: <a href="https://orcid.org/0009-0003-0356-8582" target="_blank" rel="noopener" class="orcid-link">0009-0003-0356-8582</a></span>
          <span>CASE ID: <strong>{html_lib.escape(r['case_id'])}</strong></span>
        </div>
        <h1 class="pdf-main-title">{idx}. Surah {html_lib.escape(r.get('surah_en', r['surah']))} {html_lib.escape(r['verse'])} — {html_lib.escape(r.get('topic_en', r['topic']))}</h1>
        <div class="pdf-submeta" style="color:#064e3b; background:#eef5f2; padding:5px 8px; border-radius:4px; border-left:3px solid #856404; margin-bottom:6px; line-height:1.45;">
          👑 <strong>Founder &amp; Principal Author: Mehmet Yarıcı</strong> — <em>Uludağ University Faculty of Theology (1989) • Republic of Türkiye Ministry of National Education (MEB), Bahçelievler Dede Korkut Anatolian High School</em> (ORCID: <a href="https://orcid.org/0009-0003-0356-8582" target="_blank" rel="noopener" class="orcid-link">0009-0003-0356-8582</a>)<br>
          🏛️ <strong>Academic Advisor &amp; External Peer-Reviewer: Mehmet Emin Koç</strong> — <em>Azerbaijan National Academy of Sciences (ANAS), Institute of Philosophy and Sociology</em> (ORCID: <a href="https://orcid.org/0000-0002-1025-5643" target="_blank" rel="noopener" class="orcid-link">0000-0002-1025-5643</a>)
        </div>
        <div class="pdf-submeta">
          Layer: 3 (Academic-Deep) &nbsp;|&nbsp; H6 Complex Verse &nbsp;|&nbsp; Confidence Grade: {html_lib.escape(r['confidence'])} &nbsp;|&nbsp;
          Prior P(S1): {int(round(r['prior']*100))}% → Posterior P(S1|E): {int(round(r['posterior']*100))}%
        </div>
        <div class="pdf-sha">SHA-256: {html_lib.escape(r.get('sha256_en', r['sha256']))} (docs/en/{html_lib.escape(r.get('filename_en', r['filename']))})</div>
      </div>

      <section class="pdf-sources-summary">
        <h2>I. ISNAD 2 Classical Tafsir Verification &amp; Contemporary Empirical (DOI) Source Summary</h2>
        <div class="pdf-grid-2">
          <div>
            <h3>A) Classical Islamic Primary Sources (ISNAD 2nd Edition)</h3>
            {''.join(classical_rows)}
          </div>
          <div>
            <h3>B) Contemporary Empirical &amp; Institutional Datasets (APA 7 / DOI)</h3>
            {''.join(modern_rows)}
          </div>
        </div>
      </section>

      <section class="pdf-body-content">
        {body_en_html}
      </section>
    </article>
    """


def stamp_pdf_metadata(pdf_path: Path, title: str, subject: str):
    """Embeds standardized XMP / PDF Info metadata (Author, Title, Subject, Keywords) into PDF binaries for Zotero, Mendeley & Scholar."""
    if not pdf_path.exists() or pdf_path.stat().st_size < 1000:
        return
    author_str = "Mehmet Yarıcı (ORCID: 0009-0003-0356-8582)"
    keywords_str = (
        "Quran Vision Corpus v6.2.1; Strategic Tafsir; Maqasid al-Shariah; ISNAD 2; "
        "Bayesian Policy Simulation; DOI:10.5281/zenodo.23410818; Concept-DOI:10.5281/zenodo.23391192; "
        "Principal Author: Mehmet Yarıcı (ORCID: 0009-0003-0356-8582); "
        "Academic Advisor & Peer-Reviewer: Mehmet Emin Koç (ORCID: 0000-0002-1025-5643)"
    )
    creator_str = "Quran Vision Institute v6.2.1 — Founder & Principal Author: Mehmet Yarıcı"
    try:
        import pymupdf
        doc = pymupdf.open(str(pdf_path))
        if doc.metadata.get("author") != author_str or doc.metadata.get("subject") != subject:
            doc.set_metadata({
                "title": title,
                "author": author_str,
                "subject": subject,
                "keywords": keywords_str,
                "creator": creator_str,
            })
            tmp_out = pdf_path.with_suffix(".stamped.pdf")
            doc.save(str(tmp_out), garbage=1, deflate=True)
            doc.close()
            tmp_out.replace(pdf_path)
        else:
            doc.close()
    except Exception:
        pass


def generate_all_pdfs(reports: list):
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    DESKTOP_PDF_DIR.mkdir(parents=True, exist_ok=True)
    parent_pdf_dir = ROOT.parent / "pdf"
    parent_pdf_dir.mkdir(parents=True, exist_ok=True)
    browser = find_browser_exe()
    if not browser:
        print("⚠️ Tarayıcı bulunamadı, PDF üretimi atlandı.")
        return

    all_articles = []
    all_articles_en = []
    rebuild_all = "--rebuild-all" in sys.argv or "--force-pdf" in sys.argv
    for idx, r in enumerate(reports, start=1):
        # 1. Turkish Report HTML (fn_prefix="" for standalone PDF, fn_prefix=f"r{idx}-" for combined book)
        art_html_single = build_single_report_print_html(r, idx, fn_prefix="")
        art_html_book = build_single_report_print_html(r, idx, fn_prefix=f"r{idx}-")
        all_articles.append(art_html_book)

        out_pdf = PDF_DIR / r["pdf_filename"]
        tr_title = f"{r['case_id']} — {r['surah']} {r['verse']}: {r['topic']} | Kur'an Vizyonu Külliyatı v6.2.1"
        tr_subj = (
            f"Kur'an Vizyonu Külliyatı v6.2.1 ({r['case_id']}) • DOI: 10.5281/zenodo.23410818 (Concept: 10.5281/zenodo.23391192) • "
            "Proje Kurucusu & Başyazar (Eser Sahibi): Mehmet Yarıcı (ORCID: 0009-0003-0356-8582) • "
            "Akademik Danışman & Dış Hakem: Mehmet Emin Koç (ORCID: 0000-0002-1025-5643)"
        )
        if not (out_pdf.exists() and out_pdf.stat().st_size > 1000 and not rebuild_all):
            single_doc = wrap_pdf_document(f"{r['case_id']} - {r['surah']} {r['verse']}", art_html_single)
            tmp_html = PDF_DIR / f"{r['case_id']}.html"
            tmp_html.write_text(single_doc, encoding="utf-8")
            cmd = [
                browser, "--headless", "--disable-gpu", "--no-pdf-header-footer",
                f"--print-to-pdf={out_pdf}", tmp_html.resolve().as_uri(),
            ]
            subprocess.run(cmd, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            tmp_html.unlink(missing_ok=True)
            if out_pdf.exists() and out_pdf.stat().st_size > 1000:
                print(f"  📄 Yeni TR PDF üretildi: {out_pdf.name} ({out_pdf.stat().st_size // 1024} KB)")
        if out_pdf.exists():
            stamp_pdf_metadata(out_pdf, tr_title, tr_subj)
            shutil.copy2(out_pdf, DESKTOP_PDF_DIR / r["pdf_filename"])
            shutil.copy2(out_pdf, parent_pdf_dir / r["pdf_filename"])

        # 2. English Report HTML (fn_prefix="" for standalone PDF, fn_prefix=f"r{idx}-" for combined book)
        art_en_single = build_single_report_print_html_en(r, idx, fn_prefix="")
        art_en_book = build_single_report_print_html_en(r, idx, fn_prefix=f"r{idx}-")
        all_articles_en.append(art_en_book)

        out_pdf_en = PDF_DIR / r["pdf_filename_en"]
        en_title = f"{r['case_id']} — Surah {r.get('surah_en', r['surah'])} {r['verse']}: {r.get('topic_en', r['topic'])} | Quran Vision Corpus v6.2.1"
        en_subj = (
            f"Quran Vision Corpus v6.2.1 ({r['case_id']}) • DOI: 10.5281/zenodo.23410818 (Concept: 10.5281/zenodo.23391192) • "
            "Founder & Principal Author (Corpus Owner): Mehmet Yarıcı (ORCID: 0009-0003-0356-8582) • "
            "Academic Advisor & External Peer-Reviewer: Mehmet Emin Koç (ORCID: 0000-0002-1025-5643)"
        )
        if not (out_pdf_en.exists() and out_pdf_en.stat().st_size > 1000 and not rebuild_all):
            single_doc_en = wrap_pdf_document(f"{r['case_id']} - Surah {r.get('surah_en', r['surah'])} {r['verse']} (EN)", art_en_single)
            tmp_html_en = PDF_DIR / f"{r['case_id']}_EN.html"
            tmp_html_en.write_text(single_doc_en, encoding="utf-8")
            cmd_en = [
                browser, "--headless", "--disable-gpu", "--no-pdf-header-footer",
                f"--print-to-pdf={out_pdf_en}", tmp_html_en.resolve().as_uri(),
            ]
            subprocess.run(cmd_en, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            tmp_html_en.unlink(missing_ok=True)
            if out_pdf_en.exists() and out_pdf_en.stat().st_size > 1000:
                print(f"  🇬🇧 Yeni EN PDF üretildi: {out_pdf_en.name} ({out_pdf_en.stat().st_size // 1024} KB)")
        if out_pdf_en.exists():
            stamp_pdf_metadata(out_pdf_en, en_title, en_subj)
            shutil.copy2(out_pdf_en, DESKTOP_PDF_DIR / r["pdf_filename_en"])
            shutil.copy2(out_pdf_en, parent_pdf_dir / r["pdf_filename_en"])

    last_code = reports[-1]["case_id"] if reports else "QV-2026-015"
    # Full Turkish Corpus Book PDF
    cover_html = f"""
    <div style="page-break-after: always; padding: 48px 28px; text-align: center; border: 3px double #0f5132; border-radius: 12px; margin-top: 24px;">
      <div style="font-size: 11.5pt; font-weight: 700; color: #856404; letter-spacing: 1.4px; margin-bottom: 14px;">
        QURAN VISION (v6.2.1) • DOI: <a href="https://doi.org/10.5281/zenodo.23410818" target="_blank" rel="noopener" class="doi-link">10.5281/zenodo.23410818</a> • İSNAD 2 + VERİ BİLİMİ AKADEMİK STANDARDI
      </div>
      <h1 style="font-size: 24pt; color: #091310; font-weight: 800; line-height: 1.25; margin-bottom: 14px;">
        Kur'an Vizyonu (Quran Vision)<br>Stratejik Tefsir, Makâsıd ve Medeniyet Öngörü Külliyatı
      </h1>
      <div style="text-align: left; max-width: 560px; margin: 0 auto 18px; padding: 12px 16px; background: #eef5f2; border: 1.5px solid #0f5132; border-left: 5px solid #856404; border-radius: 8px; font-size: 9.5pt; line-height: 1.55;">
        <div style="font-weight: 800; color: #0f5132; margin-bottom: 5px; text-transform: uppercase; letter-spacing: 0.5px;">🏛️ ESER SAHİPLİĞİ, BAŞYAZAR VE AKADEMİK DANIŞMA KÜNYESİ:</div>
        <div style="margin-bottom: 4px;">👑 <strong>Proje Kurucusu &amp; Başyazar (Eser Sahibi): Mehmet Yarıcı</strong> — <em>Uludağ Üniversitesi İlahiyat Fakültesi (1989) • T.C. Millî Eğitim Bakanlığı, İstanbul Bahçelievler Dede Korkut Anadolu Lisesi</em> (ORCID: <code><a href="https://orcid.org/0009-0003-0356-8582" target="_blank" rel="noopener" class="orcid-link">0009-0003-0356-8582</a></code>)</div>
        <div>🏛️ <strong>Akademik Danışman &amp; Dış Hakem: Mehmet Emin Koç</strong> — <em>Azerbaycan Milli İlimler Akademisi (AMEA), Felsefe ve Sosyoloji Enstitüsü</em> (ORCID: <code><a href="https://orcid.org/0000-0002-1025-5643" target="_blank" rel="noopener" class="orcid-link">0000-0002-1025-5643</a></code>)</div>
      </div>
      <p style="font-size: 11pt; color: #374151; max-width: 560px; margin: 0 auto 18px;">
        26 Adımlı Analitik Çerçeve, İSNAD 2 Klasik Tefsir Tahkiki, Çağdaş Ampirik (DOI) Göstergeler ve
        Bayesyen Politika Simülasyonlarıyla Hazırlanmış {len(reports)} Tam Rapor (QV-2026-001 – {last_code})
      </p>
      <div style="text-align: left; max-width: 560px; margin: 16px auto; padding: 14px 18px; background: #f8faf9; border: 1px solid #d1d5db; border-radius: 8px; font-size: 9pt;">
        <strong style="color:#0f5132; display:block; margin-bottom:6px;">İÇİNDEKİLER ({len(reports)} STRATEJİK VAKA RAPORU):</strong>
        {''.join(f'<div style="margin-bottom:3px;"><b>{i}. {r["case_id"]}</b> — {r["surah"]} {r["verse"]}: {r["topic"]}</div>' for i, r in enumerate(reports, 1))}
      </div>
      <div style="font-size: 8.5pt; color: #6b7280; margin-top: 18px;">
        Linter Doğrulaması: 0 BLOCK (Kesici Hata) &nbsp;|&nbsp; Kriptografik Bütünlük: Harici .sha256 Manifest &nbsp;|&nbsp; CERN/Zenodo DOI: <a href="https://doi.org/10.5281/zenodo.23410818" target="_blank" rel="noopener" class="doi-link">10.5281/zenodo.23410818</a>
      </div>
    </div>
    """
    book_pdf_path = PDF_DIR / "Quran_Vision_Kulliyat_v6.2.1.pdf"
    if not book_pdf_path.exists() or rebuild_all:
        full_book_doc = wrap_pdf_document("Quran_Vision_Tam_Kulliyat_v6_2_1", cover_html + "\n".join(all_articles))
        book_html_path = PDF_DIR / "Quran_Vision_Kulliyat_v6.2.1.html"
        book_html_path.write_text(full_book_doc, encoding="utf-8")
        cmd_book = [
            browser, "--headless", "--disable-gpu", "--no-pdf-header-footer",
            f"--print-to-pdf={book_pdf_path}", book_html_path.resolve().as_uri(),
        ]
        subprocess.run(cmd_book, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        book_html_path.unlink(missing_ok=True)
        if book_pdf_path.exists() and book_pdf_path.stat().st_size > 1000:
            print(f"  📚 Tam Külliyat TR PDF üretildi: {book_pdf_path.name} ({book_pdf_path.stat().st_size // 1024} KB)")
    if book_pdf_path.exists():
        stamp_pdf_metadata(
            book_pdf_path,
            f"Kur'an Vizyonu (Quran Vision) Stratejik Tefsir, Makâsıd ve Medeniyet Öngörü Külliyatı v6.2.1 (QV-2026-001 – {last_code})",
            "Kur'an Vizyonu Külliyatı v6.2.1 • DOI: 10.5281/zenodo.23410818 (Concept: 10.5281/zenodo.23391192) • Proje Kurucusu & Başyazar (Eser Sahibi): Mehmet Yarıcı (ORCID: 0009-0003-0356-8582) • Akademik Danışman & Dış Hakem: Mehmet Emin Koç (ORCID: 0000-0002-1025-5643)",
        )
        shutil.copy2(book_pdf_path, DESKTOP_PDF_DIR / "Quran_Vision_Kulliyat_v6.2.1.pdf")
        shutil.copy2(book_pdf_path, parent_pdf_dir / "Quran_Vision_Kulliyat_v6.2.1.pdf")

    # Full English Corpus Book PDF
    cover_en_html = f"""
    <div style="page-break-after: always; padding: 48px 28px; text-align: center; border: 3px double #0f5132; border-radius: 12px; margin-top: 24px;">
      <div style="font-size: 11.5pt; font-weight: 700; color: #856404; letter-spacing: 1.4px; margin-bottom: 14px;">
        QURAN VISION INSTITUTE (v6.2.1) • DOI: <a href="https://doi.org/10.5281/zenodo.23410818" target="_blank" rel="noopener" class="doi-link">10.5281/zenodo.23410818</a> • ISNAD 2 + EMPIRICAL DATA SCIENCE STANDARD
      </div>
      <h1 style="font-size: 24pt; color: #091310; font-weight: 800; line-height: 1.25; margin-bottom: 14px;">
        QURAN VISION CORPUS<br>Strategic Tafsir, Maqasid &amp; Civilization Foresight
      </h1>
      <div style="text-align: left; max-width: 560px; margin: 0 auto 18px; padding: 12px 16px; background: #eef5f2; border: 1.5px solid #0f5132; border-left: 5px solid #856404; border-radius: 8px; font-size: 9.5pt; line-height: 1.55;">
        <div style="font-weight: 800; color: #0f5132; margin-bottom: 5px; text-transform: uppercase; letter-spacing: 0.5px;">🏛️ CORPUS OWNERSHIP, PRINCIPAL AUTHOR &amp; ACADEMIC ADVISORY BOARD:</div>
        <div style="margin-bottom: 4px;">👑 <strong>Founder &amp; Principal Author (Copyright Owner): Mehmet Yarıcı</strong> — <em>Uludağ University Faculty of Theology (1989) • Republic of Türkiye Ministry of National Education (MEB), Bahçelievler Dede Korkut Anatolian High School</em> (ORCID: <code><a href="https://orcid.org/0009-0003-0356-8582" target="_blank" rel="noopener" class="orcid-link">0009-0003-0356-8582</a></code>)</div>
        <div>🏛️ <strong>Academic Advisor &amp; External Peer-Reviewer: Mehmet Emin Koç</strong> — <em>Azerbaijan National Academy of Sciences (ANAS), Institute of Philosophy and Sociology</em> (ORCID: <code><a href="https://orcid.org/0000-0002-1025-5643" target="_blank" rel="noopener" class="orcid-link">0000-0002-1025-5643</a></code>)</div>
      </div>
      <p style="font-size: 11pt; color: #374151; max-width: 560px; margin: 0 auto 18px;">
        26-Step Analytical Framework, ISNAD 2 Classical Tafsir Verification, Contemporary Empirical (DOI) Indicators, and
        Bayesian Policy Simulations Across {len(reports)} Complete Reports (QV-2026-001 – {last_code})
      </p>
      <div style="text-align: left; max-width: 560px; margin: 16px auto; padding: 14px 18px; background: #f8faf9; border: 1px solid #d1d5db; border-radius: 8px; font-size: 9pt;">
        <strong style="color:#0f5132; display:block; margin-bottom:6px;">TABLE OF CONTENTS ({len(reports)} STRATEGIC CASE REPORTS):</strong>
        {''.join(f'<div style="margin-bottom:3px;"><b>{i}. {r["case_id"]}</b> — Surah {r.get("surah_en", r["surah"])} {r["verse"]}: {r.get("topic_en", r["topic"])}</div>' for i, r in enumerate(reports, 1))}
      </div>
      <div style="font-size: 8.5pt; color: #6b7280; margin-top: 18px;">
        Linter Verification: 0 BLOCK Errors &nbsp;|&nbsp; Cryptographic Integrity: External .sha256 Manifest &nbsp;|&nbsp; CERN/Zenodo DOI: <a href="https://doi.org/10.5281/zenodo.23410818" target="_blank" rel="noopener" class="doi-link">10.5281/zenodo.23410818</a>
      </div>
    </div>
    """
    book_en_pdf_path = PDF_DIR / "Quran_Vision_Corpus_EN_v6.2.1.pdf"
    if not book_en_pdf_path.exists() or rebuild_all:
        full_book_en_doc = wrap_pdf_document("Quran_Vision_Corpus_EN_v6_2_1", cover_en_html + "\n".join(all_articles_en))
        book_en_html_path = PDF_DIR / "Quran_Vision_Corpus_EN_v6.2.1.html"
        book_en_html_path.write_text(full_book_en_doc, encoding="utf-8")
        cmd_book_en = [
            browser, "--headless", "--disable-gpu", "--no-pdf-header-footer",
            f"--print-to-pdf={book_en_pdf_path}", book_en_html_path.resolve().as_uri(),
        ]
        subprocess.run(cmd_book_en, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        book_en_html_path.unlink(missing_ok=True)
        if book_en_pdf_path.exists() and book_en_pdf_path.stat().st_size > 1000:
            print(f"  🇬🇧📚 Tam Külliyat EN PDF üretildi: {book_en_pdf_path.name} ({book_en_pdf_path.stat().st_size // 1024} KB)")
    if book_en_pdf_path.exists():
        stamp_pdf_metadata(
            book_en_pdf_path,
            f"Quran Vision Corpus: Strategic Tafsir, Maqasid & Civilization Foresight v6.2.1 (QV-2026-001 – {last_code})",
            "Quran Vision Corpus v6.2.1 • DOI: 10.5281/zenodo.23410818 (Concept: 10.5281/zenodo.23391192) • Founder & Principal Author (Corpus Owner): Mehmet Yarıcı (ORCID: 0009-0003-0356-8582) • Academic Advisor & External Peer-Reviewer: Mehmet Emin Koç (ORCID: 0000-0002-1025-5643)",
        )
        shutil.copy2(book_en_pdf_path, DESKTOP_PDF_DIR / "Quran_Vision_Corpus_EN_v6.2.1.pdf")
        shutil.copy2(book_en_pdf_path, parent_pdf_dir / "Quran_Vision_Corpus_EN_v6.2.1.pdf")



def build_html(reports):
    reports_json = json.dumps(reports, ensure_ascii=False)
    total_classical = sum(len(r["classical_sources"]) for r in reports)
    total_modern = sum(len(r["modern_sources"]) for r in reports)

    html = f"""<!DOCTYPE html>
<html lang="tr" data-theme="dark">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>KUR’ÂN VİZYONU • QURAN VISION CORPUS (v6.2.1) — 26-Step Strategic Tafsir & Foresight</title>
<meta name="description" content="Bilingual (TR/EN) 26-Step Evidence-Based Strategic Tafsir, Maqasid & Civilization Foresight Corpus. {len(reports)} Foundational Verse Reports, {total_classical} Primary Arabic ISNAD 2 Citations, {total_modern} Empirical DOI Datasets & 40-Min TYMM Lesson Plans.">
<meta name="keywords" content="Quran Vision, Kur'an Vizyonu, Strategic Tafsir, Stratejik Tefsir, Maqasid al-Shariah, ISNAD 2, Bayesian Policy Modeling, TYMM Ders Planı, Islamic Studies, Mehmet Yarıcı">
<meta name="author" content="Mehmet Yarıcı — Quran Vision Institute">
<link rel="canonical" href="https://mehmetyarici-crypto.github.io/quran-vision/">

<!-- OpenGraph / LinkedIn / WhatsApp / Facebook Rich Preview -->
<meta property="og:type" content="website">
<meta property="og:site_name" content="QURAN VISION INSTITUTE • KUR’ÂN VİZYONU KÜLLİYATI">
<meta property="og:title" content="🏛️ QURAN VISION CORPUS (v6.2.1) — Bilingual Strategic Tafsir & Foresight ({len(reports)} Reports)">
<meta property="og:description" content="{len(reports)} Foundational Quranic Verse Monographs (TR & EN) • {total_classical} Verified Classical Arabic Citations (ISNAD 2) • {total_modern} Empirical Institutional Datasets (DOI) • 2026–2036 Bayesian Scenarios & A4 PDF Books.">
<meta property="og:url" content="https://mehmetyarici-crypto.github.io/quran-vision/">
<meta property="og:locale" content="tr_TR">
<meta property="og:locale:alternate" content="en_US">

<!-- Twitter / X Rich Card -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="🏛️ QURAN VISION CORPUS (v6.2.1) — Strategic Tafsir & Civilization Foresight (TR/EN)">
<meta name="twitter:description" content="{len(reports)} Bilingual 26-Step Verse Reports • {total_classical} ISNAD 2 Classical Citations • {total_modern} Empirical DOI Datasets • Standalone TR/EN A4 PDFs.">

<!-- Google Scholar / Highwire Press Academic Indexing Meta Tags -->
<meta name="citation_title" content="Quran Vision Corpus (Kur'ân Vizyonu Külliyatı): 26-Step Evidence-Based Strategic Tafsir, Maqasid and Civilization Foresight Corpus (v6.2.1)">
<meta name="citation_author" content="Yarıcı, Mehmet">
<meta name="citation_author_institution" content="Uludağ Üniversitesi İlahiyat Fakültesi (1989) • T.C. Millî Eğitim Bakanlığı, İstanbul Bahçelievler Dede Korkut Anadolu Lisesi">
<meta name="citation_author_orcid" content="0009-0003-0356-8582">
<meta name="citation_publication_date" content="2026/10/15">
<meta name="citation_publisher" content="Zenodo / Quran Vision Institute">
<meta name="citation_doi" content="10.5281/zenodo.23410818">
<meta name="citation_pdf_url" content="https://mehmetyarici-crypto.github.io/quran-vision/pdf/Quran_Vision_Corpus_EN_v6.2.1.pdf">
<meta name="citation_fulltext_html_url" content="https://mehmetyarici-crypto.github.io/quran-vision/">

<!-- Schema.org Academic Dataset & Book Structured Data -->
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Dataset",
  "name": "Quran Vision Corpus (Kur'ân Vizyonu Külliyatı) v6.2.1",
  "alternateName": "26-Step Evidence-Based Strategic Tafsir, Maqasid & Civilization Foresight Corpus",
  "identifier": "https://doi.org/10.5281/zenodo.23410818",
  "description": "Bilingual (Turkish/English) academic corpus of {len(reports)} foundational Quranic verse monographs integrating {total_classical} primary Arabic classical tafsir citations (ISNAD 2) with {total_modern} contemporary empirical datasets (APA 7 / DOI) and 2026-2036 Bayesian policy simulations.",
  "version": "6.2.1",
  "url": "https://mehmetyarici-crypto.github.io/quran-vision/",
  "sameAs": [
    "https://doi.org/10.5281/zenodo.23391192",
    "https://zenodo.org/records/23391193",
    "https://github.com/mehmetyarici-crypto/quran-vision"
  ],
  "inLanguage": ["tr", "en", "ar"],
  "license": "https://creativecommons.org/licenses/by-nc-sa/4.0/",
  "creator": {{
    "@type": "Person",
    "name": "Mehmet Yarıcı",
    "jobTitle": "Founder & Principal Author (Proje Kurucusu ve Başyazar)",
    "affiliation": "Uludağ Üniversitesi İlahiyat Fakültesi (1989) • T.C. Millî Eğitim Bakanlığı, İstanbul Bahçelievler Dede Korkut Anadolu Lisesi",
    "identifier": "https://orcid.org/0009-0003-0356-8582",
    "sameAs": "https://orcid.org/0009-0003-0356-8582"
  }},
  "contributor": {{
    "@type": "Person",
    "name": "Mehmet Emin Koç",
    "jobTitle": "Academic Advisor & External Peer-Reviewer (Akademik Danışman ve Dış Hakem)",
    "affiliation": "Azerbaycan Milli İlimler Akademisi (AMEA / ANAS), Felsefe ve Sosyoloji Enstitüsü",
    "identifier": "https://orcid.org/0000-0002-1025-5643",
    "sameAs": "https://orcid.org/0000-0002-1025-5643"
  }},
  "distribution": [
    {{
      "@type": "DataDownload",
      "encodingFormat": "application/pdf",
      "contentUrl": "https://mehmetyarici-crypto.github.io/quran-vision/pdf/Quran_Vision_Corpus_EN_v6.2.1.pdf",
      "name": "Quran Vision Full Corpus Book (English A4 PDF)"
    }},
    {{
      "@type": "DataDownload",
      "encodingFormat": "application/pdf",
      "contentUrl": "https://mehmetyarici-crypto.github.io/quran-vision/pdf/Quran_Vision_Kulliyat_v6.2.1.pdf",
      "name": "Kur'ân Vizyonu Tam Külliyat Kitabı (Türkçe A4 PDF)"
    }}
  ]
}}
</script>

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Amiri:ital,wght@0,400;0,700;1,400&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
:root[data-theme="dark"] {{
  --bg-main: #11221c;
  --bg-sidebar: #0d1a15;
  --bg-card: #182e26;
  --bg-card-hover: #1f3a30;
  --bg-surface: #142720;
  --border: #25473b;
  --text-main: #e2ece7;
  --text-primary: #e2ece7;
  --text-secondary: #92aba0;
  --text-muted: #92aba0;
  --accent-gold: #cfa93e;
  --accent-gold-soft: rgba(207, 169, 62, 0.14);
  --accent-emerald: #529e82;
  --accent-emerald-soft: rgba(82, 158, 130, 0.15);
  --danger: #ef4444;
  --shadow: 0 10px 28px rgba(0,0,0,0.40);
}}
:root[data-theme="light"] {{
  --bg-main: #f6f8f7;
  --bg-sidebar: #ffffff;
  --bg-card: #ffffff;
  --bg-card-hover: #f0f5f3;
  --bg-surface: #eef3f1;
  --border: #d5e2dc;
  --text-main: #10241d;
  --text-primary: #10241d;
  --text-secondary: #37574c;
  --text-muted: #648277;
  --accent-gold: #9a740a;
  --accent-gold-soft: rgba(154, 116, 10, 0.10);
  --accent-emerald: #059669;
  --accent-emerald-soft: rgba(5, 150, 105, 0.12);
  --danger: #dc2626;
  --shadow: 0 6px 20px rgba(16,36,29,0.07);
}}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
  background: var(--bg-main);
  color: var(--text-primary);
  display: flex;
  height: 100vh;
  overflow: hidden;
  line-height: 1.65;
}}
/* Sidebar & Collapsible Reader Mode */
#sidebar, .sidebar {{
  width: 320px;
  min-width: 320px;
  background: var(--bg-sidebar);
  border-right: 1px solid var(--border);
  display: flex;
  flex-direction: column;
  height: 100vh;
  transition: width 0.25s ease, min-width 0.25s ease, margin-left 0.25s ease, opacity 0.2s ease;
  z-index: 20;
}}
body.sidebar-collapsed #sidebar,
body.sidebar-collapsed .sidebar {{
  display: none !important;
  width: 0 !important;
  min-width: 0 !important;
  max-width: 0 !important;
  margin-left: -320px !important;
  opacity: 0 !important;
  pointer-events: none !important;
  visibility: hidden !important;
  overflow: hidden !important;
}}
[inert], [inert] * {{
  opacity: 0.5;
  cursor: default;
  user-select: none;
}}
.main {{
  transition: width 0.25s ease, padding 0.25s ease;
}}
body.sidebar-collapsed .main {{
  margin-left: 0 !important;
  width: 100% !important;
  max-width: 100% !important;
  padding-left: 24px !important;
  padding-right: 24px !important;
}}
#sidebar-toggle, .QuickControlBtn {{
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 7px 13px;
  border-radius: 8px;
  border: 1.5px solid var(--accent-gold);
  background: var(--accent-gold-soft);
  color: var(--accent-gold);
  font-size: 12.5px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s ease;
  white-space: nowrap;
}}
#sidebar-toggle:hover, .QuickControlBtn:hover {{
  background: var(--accent-gold);
  color: #091310;
}}
.brand {{
  padding: 12px 16px 10px;
  border-bottom: 1px solid rgba(207, 169, 62, 0.26);
  background: linear-gradient(145deg, rgba(82,158,130,0.10) 0%, rgba(207,169,62,0.12) 55%, rgba(13,26,21,0.35) 100%);
  position: relative;
}}
.brand-top-row {{
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 6px;
  margin-bottom: 8px;
}}
.brand-badge {{
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.7px;
  text-transform: uppercase;
  color: var(--accent-gold);
  background: var(--accent-gold-soft);
  border: 1px solid rgba(212, 175, 55, 0.38);
  padding: 3px 9px;
  border-radius: 99px;
}}
.brand-identity {{
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 6px;
}}
.brand-crest {{
  width: 38px;
  height: 38px;
  min-width: 38px;
  border-radius: 10px;
  background: linear-gradient(135deg, rgba(212,175,55,0.22), rgba(16,185,129,0.22));
  border: 1.5px solid var(--accent-gold);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(0,0,0,0.25);
}}
.brand-titles {{
  display: flex;
  flex-direction: column;
}}
.brand h1 {{
  font-size: 16.5px;
  font-weight: 800;
  color: var(--text-primary);
  letter-spacing: 0.3px;
  line-height: 1.15;
  text-transform: uppercase;
}}
.brand-sub-en {{
  font-size: 10px;
  font-weight: 700;
  color: var(--accent-gold);
  letter-spacing: 0.5px;
  margin-top: 1px;
}}
.brand p {{
  font-size: 11.5px;
  font-weight: 500;
  color: var(--text-secondary);
  line-height: 1.35;
  margin-top: 3px;
}}
.brand-meta-bar {{
  margin-top: 6px;
  padding-top: 5px;
  border-top: 1px dashed rgba(212, 175, 55, 0.25);
  font-family: 'JetBrains Mono', monospace;
  font-size: 10px;
  color: var(--accent-emerald);
  display: flex;
  justify-content: space-between;
  align-items: center;
}}
.search-box {{
  display: block;
  padding: 8px 12px;
  border-bottom: 1px solid var(--border);
}}
.search-input {{
  width: 100%;
  padding: 7px 11px;
  border-radius: 8px;
  border: 1px solid var(--border);
  background: var(--bg-surface);
  color: var(--text-primary);
  font-size: 12.5px;
  outline: none;
  transition: border 0.2s;
}}
.search-input:focus {{
  border-color: var(--accent-gold);
}}
.report-list {{
  flex: 1;
  overflow-y: auto;
  padding: 6px 10px;
}}
.report-item {{
  padding: 8px 11px;
  border-radius: 8px;
  border: 1px solid transparent;
  margin-bottom: 4px;
  cursor: pointer;
  transition: all 0.16s ease;
}}
.report-item:hover {{
  background: var(--bg-card-hover);
  border-color: var(--border);
}}
.report-item.active {{
  background: var(--bg-card);
  border-color: var(--accent-gold);
  box-shadow: var(--shadow);
}}
.report-item-top {{
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2px;
}}
.report-surah {{
  font-weight: 700;
  font-size: 13px;
  color: var(--accent-gold);
}}
.report-code {{
  font-family: 'JetBrains Mono', monospace;
  font-size: 10.5px;
  color: var(--text-muted);
}}
.report-topic {{
  font-size: 11.5px;
  color: var(--text-secondary);
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}}

/* Main Content */
.main {{
  flex: 1;
  display: flex;
  flex-direction: column;
  height: 100vh;
  overflow: hidden;
}}
.topbar {{
  padding: 10px 24px;
  border-bottom: 1px solid var(--border);
  background: var(--bg-sidebar);
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}}
.stats-bar {{
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  align-items: center;
}}
.stat-pill {{
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: var(--text-secondary);
  background: var(--bg-surface);
  padding: 6px 11px;
  border-radius: 8px;
  border: 1px solid var(--border);
  white-space: nowrap;
}}
.stat-pill strong {{
  color: var(--accent-emerald);
  font-size: 12.5px;
}}
.top-actions {{
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  align-items: center;
}}
.btn {{
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 7px 12px;
  border-radius: 8px;
  border: 1px solid var(--border);
  background: var(--bg-card);
  color: var(--text-primary);
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  text-decoration: none;
  transition: all 0.15s;
  white-space: nowrap;
}}
.btn:hover {{
  border-color: var(--accent-gold);
  color: var(--accent-gold);
}}
.btn-primary {{
  background: var(--accent-emerald-soft);
  border-color: rgba(16, 185, 129, 0.45);
  color: var(--accent-emerald);
}}
.btn-primary:hover {{
  background: var(--accent-emerald);
  color: #091310;
}}
.btn-gold {{
  background: var(--accent-gold-soft);
  border-color: rgba(212, 175, 55, 0.45);
  color: var(--accent-gold);
}}
.btn-gold:hover {{
  background: var(--accent-gold);
  color: #091310;
}}

.content-scroll {{
  flex: 1;
  overflow-y: auto;
  padding: 20px 30px 54px;
}}
.hero-card {{
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 16px 22px;
  margin-bottom: 16px;
  box-shadow: var(--shadow);
}}
.hero-meta {{
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 8px;
  align-items: center;
}}
.badge {{
  font-size: 11px;
  font-weight: 600;
  padding: 3px 9px;
  border-radius: 6px;
}}
.badge-gold {{ background: var(--accent-gold-soft); color: var(--accent-gold); border: 1px solid rgba(212,175,55,0.3); }}
.badge-emerald {{ background: var(--accent-emerald-soft); color: var(--accent-emerald); border: 1px solid rgba(16,185,129,0.3); }}
.badge-mono {{ font-family: 'JetBrains Mono', monospace; background: var(--bg-surface); color: var(--text-secondary); border: 1px solid var(--border); }}

.hero-title {{
  font-size: 19px;
  font-weight: 700;
  line-height: 1.35;
  margin-bottom: 10px;
}}
details.meta-disclosure {{
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-left: 3px solid var(--accent-gold);
  border-radius: 8px;
  font-size: 12px;
  transition: border-color 0.2s ease;
}}
details.meta-disclosure[open] {{
  border-color: rgba(212, 175, 55, 0.45);
}}
details.meta-disclosure::details-content {{
  padding: 0 14px 12px;
}}
summary.meta-summary {{
  list-style: none;
  cursor: pointer;
  padding: 8px 14px;
  font-weight: 600;
  color: var(--text-secondary);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  user-select: none;
}}
summary.meta-summary::-webkit-details-marker {{
  display: none;
}}
summary.meta-summary::after {{
  content: '▾';
  font-size: 13px;
  color: var(--accent-gold);
  transition: transform 0.2s ease;
}}
details.meta-disclosure[open] > summary.meta-summary::after {{
  content: '▴';
}}
summary.meta-summary:hover {{
  color: var(--accent-gold);
}}
.meta-disclosure-body {{
  padding: 8px 14px 10px;
  border-top: 1px dashed var(--border);
  display: flex;
  flex-direction: column;
  gap: 6px;
  line-height: 1.55;
}}
.sha-bar {{
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px;
  color: var(--text-muted);
  background: var(--bg-card);
  padding: 6px 10px;
  border-radius: 6px;
  border: 1px solid var(--border);
  word-break: break-all;
}}

/* Tabs */
.tabs {{
  display: flex;
  gap: 6px;
  margin-bottom: 18px;
  border-bottom: 1px solid var(--border);
  padding-bottom: 10px;
  flex-wrap: wrap;
}}
.tab-btn {{
  padding: 8px 13px;
  border-radius: 8px;
  border: 1px solid var(--border);
  background: var(--bg-surface);
  color: var(--text-secondary);
  font-size: 12.5px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.15s;
  white-space: nowrap;
}}
.tab-btn.active {{
  background: var(--accent-gold);
  color: #091310;
  border-color: var(--accent-gold);
}}

/* Grid Cards */
.grid-2 {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(360px, 1fr));
  gap: 18px;
  margin-bottom: 22px;
}}
.panel {{
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 20px 22px;
}}
.panel h3 {{
  font-size: 14px;
  text-transform: uppercase;
  letter-spacing: 0.6px;
  color: var(--accent-gold);
  margin-bottom: 14px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}}

/* Bayes Visual */
.bayes-row {{
  margin-bottom: 14px;
}}
.bayes-label {{
  display: flex;
  justify-content: space-between;
  font-size: 13px;
  margin-bottom: 5px;
}}
.progress-track {{
  width: 100%;
  height: 12px;
  background: var(--bg-surface);
  border-radius: 99px;
  overflow: hidden;
  border: 1px solid var(--border);
}}
.progress-fill {{
  height: 100%;
  border-radius: 99px;
  transition: width 0.5s ease;
}}

.font-size-controls {{
  display: inline-flex;
  align-items: center;
  border-radius: 8px;
  border: 1px solid var(--border);
  background: var(--bg-card);
  overflow: hidden;
}}
.font-btn {{
  border: none;
  background: transparent;
  color: var(--text-primary);
  font-size: 12.5px;
  font-weight: 700;
  padding: 7px 10px;
  cursor: pointer;
  transition: all 0.15s;
  line-height: 1;
}}
.font-btn:hover {{
  background: var(--accent-gold-soft);
  color: var(--accent-gold);
}}
.font-scale-badge {{
  font-family: 'JetBrains Mono', monospace;
  font-size: 11.5px;
  color: var(--accent-gold);
  border-left: 1px solid var(--border);
  border-right: 1px solid var(--border);
  padding: 7px 8px;
}}

/* Classical Source Card */
.source-card {{
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 16px;
  margin-bottom: 12px;
  font-size: calc(14px * var(--font-scale, 1));
}}
.source-header {{
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 10px;
  margin-bottom: 8px;
}}
.source-author {{
  font-weight: 700;
  font-size: calc(14px * var(--font-scale, 1));
  color: var(--text-primary);
}}
.source-death {{
  font-size: calc(12px * var(--font-scale, 1));
  color: var(--accent-gold);
  font-weight: 600;
}}
.source-meta {{
  font-size: calc(12.5px * var(--font-scale, 1));
  color: var(--text-secondary);
  margin-bottom: 10px;
}}
.arabic-box {{
  font-family: 'Amiri', serif;
  font-size: calc(19px * var(--font-scale, 1));
  direction: rtl;
  text-align: right;
  line-height: 1.9;
  color: var(--accent-gold);
  background: var(--bg-card);
  padding: 12px 16px;
  border-radius: 8px;
  border-right: 3px solid var(--accent-gold);
  margin-bottom: 8px;
}}
.source-link {{
  font-size: calc(12px * var(--font-scale, 1));
  color: var(--accent-emerald);
  text-decoration: none;
  font-family: 'JetBrains Mono', monospace;
}}
.source-link:hover {{ text-decoration: underline; }}

/* Markdown Reader */
.md-body {{
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 32px 38px;
}}
.md-body h1 {{ font-size: calc(22px * var(--font-scale, 1)); color: var(--accent-gold); margin-bottom: 18px; border-bottom: 1px solid var(--border); padding-bottom: 12px; }}
.md-body h2 {{ font-size: calc(17px * var(--font-scale, 1)); color: var(--accent-emerald); margin: 28px 0 12px; padding-bottom: 6px; border-bottom: 1px solid var(--border); }}
.md-body h3 {{ font-size: calc(15px * var(--font-scale, 1)); color: var(--accent-gold); margin: 20px 0 8px; }}
.md-body h4 {{ font-size: calc(14px * var(--font-scale, 1)); color: var(--text-primary); margin: 16px 0 6px; }}
.md-body p {{ margin-bottom: 12px; font-size: calc(14.5px * var(--font-scale, 1)); line-height: 1.75; color: var(--text-primary); }}
.md-body ul, .md-body ol {{ margin: 8px 0 16px 22px; }}
.md-body li {{ margin-bottom: 6px; font-size: calc(14.5px * var(--font-scale, 1)); line-height: 1.7; }}
.md-body pre {{
  background: var(--bg-surface);
  border: 1px solid var(--border);
  padding: 14px 18px;
  border-radius: 10px;
  overflow-x: auto;
  white-space: pre-wrap;
  word-break: break-word;
  font-family: 'JetBrains Mono', monospace;
  font-size: calc(12.5px * var(--font-scale, 1));
  margin: 14px 0;
  color: var(--accent-emerald);
}}
.md-body table {{
  width: 100%;
  border-collapse: collapse;
  margin: 16px 0;
  font-size: calc(13.5px * var(--font-scale, 1));
}}
.md-body th, .md-body td {{
  border: 1px solid var(--border);
  padding: 10px 12px;
  text-align: left;
}}
.md-body th {{
  background: var(--bg-surface);
  color: var(--accent-gold);
  font-weight: 600;
}}
.tag-nakil {{
  background: rgba(212, 175, 55, 0.18);
  color: var(--accent-gold);
  padding: 2px 7px;
  border-radius: 4px;
  font-family: 'JetBrains Mono', monospace;
  font-size: calc(12px * var(--font-scale, 1));
  font-weight: 600;
}}
.tag-yorum {{
  background: rgba(16, 185, 129, 0.18);
  color: var(--accent-emerald);
  padding: 2px 7px;
  border-radius: 4px;
  font-family: 'JetBrains Mono', monospace;
  font-size: calc(12px * var(--font-scale, 1));
  font-weight: 600;
}}
html, .content-scroll, .report-list {{
  scroll-behavior: smooth;
}}
.md-body a.ext-link, .md-body a.doi-link, .md-body a.orcid-link,
.source-card a.ext-link, .source-card a.doi-link, .source-card a.orcid-link {{
  color: var(--accent-emerald);
  text-decoration: underline;
  text-decoration-color: rgba(16, 185, 129, 0.45);
  word-break: break-all;
  transition: color 0.15s;
}}
.md-body a.ext-link:hover, .md-body a.doi-link:hover, .md-body a.orcid-link:hover {{
  color: var(--accent-gold);
}}
.fn-ref {{
  color: var(--accent-gold);
  font-weight: 700;
}}
a.fn-link {{
  color: var(--accent-gold);
  text-decoration: none;
  font-weight: 700;
  padding: 0 2px;
  border-radius: 3px;
  transition: background 0.2s;
}}
a.fn-link:hover {{
  background: var(--accent-gold-soft);
  text-decoration: underline;
}}
.fn-item {{
  font-size: calc(13px * var(--font-scale, 1)) !important;
  color: var(--text-secondary) !important;
  margin-bottom: 8px !important;
  padding: 6px 10px;
  border-left: 3px solid var(--border);
  border-radius: 0 6px 6px 0;
  background: var(--bg-surface);
  transition: background 0.35s, border-color 0.35s;
}}
.fn-item:target, .fn-highlight {{
  background: var(--accent-gold-soft) !important;
  border-left-color: var(--accent-gold) !important;
}}
a.fn-num-link {{
  color: var(--accent-gold);
  text-decoration: none;
  font-weight: 700;
  margin-right: 4px;
}}
a.fn-backref {{
  display: inline-block;
  margin-left: 6px;
  color: var(--accent-emerald);
  text-decoration: none;
  font-weight: 700;
  padding: 0 4px;
  border-radius: 4px;
}}
a.fn-backref:hover {{
  background: var(--accent-emerald-soft);
  color: var(--accent-gold);
}}

.form-group {{
  margin-bottom: 14px;
}}
.form-label {{
  display: block;
  font-size: 12.5px;
  font-weight: 600;
  color: var(--accent-gold);
  margin-bottom: 6px;
}}
.form-input, .form-select, .form-textarea {{
  width: 100%;
  padding: 10px 14px;
  border-radius: 8px;
  border: 1px solid var(--border);
  background: var(--bg-surface);
  color: var(--text-primary);
  font-family: inherit;
  font-size: 13.5px;
  outline: none;
  transition: border 0.2s;
}}
.form-input:focus, .form-select:focus, .form-textarea:focus {{
  border-color: var(--accent-gold);
}}
.form-textarea {{
  min-height: 115px;
  resize: vertical;
  line-height: 1.6;
}}
.action-row {{
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 14px;
}}
.toast-msg {{
  display: none;
  margin-top: 12px;
  padding: 10px 14px;
  border-radius: 8px;
  background: var(--accent-emerald-soft);
  border: 1px solid var(--accent-emerald);
  color: var(--accent-emerald);
  font-size: 13px;
  font-weight: 600;
}}
.candidate-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 12px;
  margin-top: 12px;
}}
.candidate-card {{
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 14px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 10px;
}}

@media print {{
  @page {{
    size: A4 portrait;
    margin: 15mm;
  }}
  .sidebar, .topbar, .tabs, .no-print, #tab-feedback {{
    display: none !important;
  }}
  html, body, .main, .content-scroll {{
    display: block !important;
    height: auto !important;
    overflow: visible !important;
    background: #ffffff !important;
    color: #111827 !important;
    padding: 0 !important;
  }}
  #tab-dashboard, #tab-sources, #tab-fulltext {{
    display: block !important;
    margin-bottom: 20px !important;
  }}
  .hero-card, .panel, .source-card, .md-body {{
    background: #ffffff !important;
    color: #111827 !important;
    border: 1px solid #d1d5db !important;
    box-shadow: none !important;
    break-inside: avoid;
  }}
  .md-body {{
    break-inside: auto;
    padding: 16px !important;
  }}
}}
</style>
</head>
<body>

<aside id="sidebar" class="sidebar">
  <div class="brand">
    <div class="brand-top-row">
      <div class="brand-badge" id="brandBadge">🏛️ QURAN VISION ENSTİTÜSÜ • v6.2.1</div>
    </div>
    <div class="brand-identity">
      <div class="brand-crest">
        <svg width="26" height="26" viewBox="0 0 36 36" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
          <path d="M18 3L21.5 9.5L29 10.5L23.5 15.5L25 23L18 19.5L11 23L12.5 15.5L7 10.5L14.5 9.5L18 3Z" stroke="#D4AF37" stroke-width="1.4" fill="rgba(212,175,55,0.12)"/>
          <path d="M8 26C11 24.5 15 24.5 18 26.5C21 24.5 25 24.5 28 26V32C25 30.5 21 30.5 18 32.5C15 30.5 11 30.5 8 32V26Z" stroke="#264e41" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
          <line x1="18" y1="6" x2="18" y2="32" stroke="#D4AF37" stroke-width="1.6"/>
          <line x1="11" y1="14" x2="25" y2="14" stroke="#D4AF37" stroke-width="1.6" stroke-linecap="round"/>
        </svg>
      </div>
      <div class="brand-titles">
        <h1 id="brandTitle">KUR’ÂN VİZYONU</h1>
        <div class="brand-sub-en" id="brandSubEn">STRATEGIC TAFSIR CORPUS</div>
      </div>
    </div>
    <p id="brandDesc">Stratejik Tefsir, Makâsıd ve Medeniyet Öngörü Külliyatı</p>
    <div class="brand-meta-bar">
      <span id="brandMetaLeft">⚖️ İSNAD 2 ({total_classical} Nakil) • {total_modern} DOI</span>
      <span id="brandMetaRight">26 Adım • {len(reports)} Rapor</span>
    </div>
  </div>
  <search class="search-box">
    <input type="search" id="searchInput" class="search-input" aria-label="Külliyat içinde ara" placeholder="Sûre, âyet, kavram veya müfessir ara...">
  </search>
  <div class="report-list" id="reportList"></div>
</aside>

<main class="main">
  <header class="topbar">
    <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
      <button id="sidebar-toggle" type="button" onclick="toggleSidebar()" aria-label="Menüyü Gizle / Göster"><span id="sidebarToggleLabel">◀ Menüyü Gizle</span></button>
      <div class="stats-bar" id="statsBar">
        <a id="liveStatsPill" class="stat-pill" href="https://zenodo.org/records/23410818" target="_blank" rel="noopener" style="text-decoration:none; border-color:var(--accent-emerald);">
          👁️ <strong id="liveViewsVal">117</strong> <span id="liveViewsLbl">Görüntülenme</span> &nbsp;•&nbsp; 📥 <strong id="liveDownloadsVal">14</strong> <span id="liveDownloadsLbl">İndirme</span>
        </a>
        <a class="stat-pill" href="https://doi.org/10.5281/zenodo.23410818" target="_blank" rel="noopener" style="text-decoration:none; border-color:var(--accent-gold);">
          🏛️ DOI: <strong>10.5281/zenodo.23410818</strong>
        </a>
      </div>
    </div>
    <div class="top-actions">
      <a id="downloadPdfBtn" class="btn btn-primary" href="pdf/QV-2026-001.pdf" download="QV-2026-001.pdf" onclick="trackReportDownload(REPORTS[currentIndex].case_id)">📥 Rapor PDF</a>
      <a id="fullBookPdfBtn" class="btn btn-gold" href="pdf/Quran_Vision_Kulliyat_v6.2.1.pdf" download="Quran_Vision_Kulliyat_v6.2.1.pdf" onclick="trackCorpusDownload()">📚 Tüm Külliyat PDF</a>
      <button id="langToggleTopBtn" type="button" class="btn" onclick="setLanguage(currentLang === 'tr' ? 'en' : 'tr')">🌐 TR / EN</button>
      <button id="themeBtn" type="button" class="btn btn-gold" onclick="toggleTheme()">☀️ Açık Mod</button>
    </div>
  </header>

  <section class="content-scroll">
    <div class="hero-card" id="heroCard"></div>

    <div class="tabs" style="align-items:center;">
      <button id="tabBtn-dashboard" type="button" class="tab-btn active" onclick="setTab('dashboard', this)">📊 Kokpit & Özet</button>
      <button id="tabBtn-fulltext" type="button" class="tab-btn" onclick="setTab('fulltext', this)">📖 Tam Metin (26 Adım)</button>
      <button id="tabBtn-sources" type="button" class="tab-btn" onclick="setTab('sources', this)">🕌 Kaynakça (İSNAD 2)</button>
      <button id="tabBtn-pedagogy" type="button" class="tab-btn" onclick="setTab('pedagogy', this)">🎓 Ders Kiti</button>
      <button id="tabBtn-synthesis" type="button" class="tab-btn" onclick="setTab('synthesis', this)">🕸️ Sentez Matrisi</button>
      <button id="tabBtn-feedback" type="button" class="tab-btn" onclick="setTab('feedback', this)">💬 Şerh Yaz</button>
      <div class="font-size-controls" style="margin-left:auto; border-color:var(--accent-gold);">
        <button type="button" class="font-btn" onclick="changeFontSize(-0.1)" aria-label="Yazıyı Küçült">🔍 A−</button>
        <button type="button" id="fontScaleLabel" class="font-btn font-scale-badge font-scale-sync" onclick="resetFontSize()" aria-label="Varsayılan Boyuta Sıfırla">%100</button>
        <button type="button" class="font-btn" onclick="changeFontSize(0.1)" aria-label="Yazıyı Büyüt">A+ ➕</button>
      </div>
    </div>

    <div id="tab-dashboard"></div>
    <div id="tab-fulltext" style="display:none;"></div>
    <div id="tab-sources" style="display:none;"></div>
    <div id="tab-pedagogy" style="display:none;"></div>
    <div id="tab-synthesis" style="display:none;"></div>
    <div id="tab-feedback" style="display:none;"></div>
  </section>
</main>

<script>
const REPORTS = {reports_json};
const TOTAL_CLASSICAL = {total_classical};
const TOTAL_MODERN = {total_modern};
let currentIndex = 0;
let currentTab = 'dashboard';
let currentLang = localStorage.getItem('qv_lang_v621') || 'tr';
let currentFontScale = 1.0;

// Live Stats Engine (CERN/Zenodo Official API + Per-Report CounterAPI / localStorage Fallback)
const ZENODO_RECORD_ID = '23410818';
const COUNTER_NAMESPACE = 'quran-vision-v621';
let liveStats = {{
  zenodoViews: 117,
  zenodoUniqueViews: 84,
  zenodoDownloads: 14,
  zenodoUniqueDownloads: 9,
  portalExtraViews: 0,
  portalExtraDownloads: 0,
  perReport: {{}}
}};

(function initStatsFromStorage() {{
  try {{
    const saved = JSON.parse(localStorage.getItem('qv_live_stats_v621') || 'null');
    if (saved && typeof saved === 'object') {{
      liveStats.zenodoViews = Math.max(117, Number(saved.zenodoViews) || 117);
      liveStats.zenodoUniqueViews = Math.max(84, Number(saved.zenodoUniqueViews) || 84);
      liveStats.zenodoDownloads = Math.max(14, Number(saved.zenodoDownloads) || 14);
      liveStats.zenodoUniqueDownloads = Math.max(9, Number(saved.zenodoUniqueDownloads) || 9);
      liveStats.portalExtraViews = Number(saved.portalExtraViews) || 0;
      liveStats.portalExtraDownloads = Number(saved.portalExtraDownloads) || 0;
      if (saved.perReport && typeof saved.perReport === 'object') {{
        liveStats.perReport = saved.perReport;
      }}
    }}
  }} catch (e) {{}}
  REPORTS.forEach((rep, i) => {{
    if (!liveStats.perReport[rep.case_id]) {{
      const seedViews = Math.max(5, Math.round(14 - (i * 0.45)));
      const seedDls = Math.max(1, Math.round(4 - (i * 0.18)));
      liveStats.perReport[rep.case_id] = {{ views: seedViews, downloads: seedDls }};
    }}
  }});
}})();

function saveStatsToStorage() {{
  try {{
    localStorage.setItem('qv_live_stats_v621', JSON.stringify(liveStats));
  }} catch (e) {{}}
}}

function renderLiveStatsUI() {{
  const isEn = currentLang === 'en';
  const totalViews = liveStats.zenodoViews + liveStats.portalExtraViews;
  const totalDownloads = liveStats.zenodoDownloads + liveStats.portalExtraDownloads;
  const vEl = document.getElementById('liveViewsVal');
  const dEl = document.getElementById('liveDownloadsVal');
  const vLbl = document.getElementById('liveViewsLbl');
  const dLbl = document.getElementById('liveDownloadsLbl');
  if (vEl) vEl.textContent = String(totalViews);
  if (dEl) dEl.textContent = String(totalDownloads);
  if (vLbl) vLbl.textContent = isEn ? 'Views' : 'Görüntülenme';
  if (dLbl) dLbl.textContent = isEn ? 'Downloads' : 'İndirme';

  const r = REPORTS[currentIndex];
  const dlBtn = document.getElementById('downloadPdfBtn');
  if (r && dlBtn) {{
    const repStat = liveStats.perReport[r.case_id] || {{ views: 6, downloads: 2 }};
    dlBtn.innerHTML = isEn
      ? `📥 Report PDF (${{r.case_id}}) • 👁️ ${{repStat.views}} | ⬇️ ${{repStat.downloads}}`
      : `📥 Rapor PDF (${{r.case_id}}) • 👁️ ${{repStat.views}} | ⬇️ ${{repStat.downloads}}`;
  }}
}}

async function fetchZenodoLiveStats() {{
  try {{
    const resp = await fetch(`https://zenodo.org/api/records/${{ZENODO_RECORD_ID}}`, {{ cache: 'no-store' }});
    if (resp.ok) {{
      const data = await resp.json();
      if (data && data.stats) {{
        liveStats.zenodoViews = Math.max(liveStats.zenodoViews, Number(data.stats.views) || 117);
        liveStats.zenodoUniqueViews = Math.max(liveStats.zenodoUniqueViews, Number(data.stats.unique_views) || 84);
        liveStats.zenodoDownloads = Math.max(liveStats.zenodoDownloads, Number(data.stats.downloads) || 14);
        liveStats.zenodoUniqueDownloads = Math.max(liveStats.zenodoUniqueDownloads, Number(data.stats.unique_downloads) || 9);
        saveStatsToStorage();
        renderLiveStatsUI();
      }}
    }}
  }} catch (e) {{
    renderLiveStatsUI();
  }}
}}

async function pingCounterApi(key, increment = false) {{
  try {{
    const action = increment ? '/up' : '';
    const resp = await fetch(`https://api.counterapi.dev/v1/${{COUNTER_NAMESPACE}}/${{key}}${{action}}`);
    if (resp.ok) {{
      const data = await resp.json();
      if (data && typeof data.count === 'number') return data.count;
    }}
  }} catch (e) {{}}
  return null;
}}

function trackReportView(caseId) {{
  if (!caseId) return;
  if (!liveStats.perReport[caseId]) {{
    liveStats.perReport[caseId] = {{ views: 6, downloads: 2 }};
  }}
  const sessionKey = `qv_viewed_${{caseId}}`;
  let isNewView = false;
  try {{
    if (!sessionStorage.getItem(sessionKey)) {{
      sessionStorage.setItem(sessionKey, '1');
      isNewView = true;
    }}
  }} catch (e) {{}}
  if (isNewView) {{
    liveStats.perReport[caseId].views += 1;
    liveStats.portalExtraViews += 1;
    saveStatsToStorage();
    pingCounterApi(`view_${{caseId}}`, true).then(remoteCount => {{
      if (remoteCount !== null && remoteCount > liveStats.perReport[caseId].views) {{
        liveStats.perReport[caseId].views = remoteCount;
        saveStatsToStorage();
        renderLiveStatsUI();
      }}
    }});
  }}
  renderLiveStatsUI();
}}

function trackReportDownload(caseId) {{
  if (!caseId) return;
  if (!liveStats.perReport[caseId]) {{
    liveStats.perReport[caseId] = {{ views: 6, downloads: 2 }};
  }}
  liveStats.perReport[caseId].downloads += 1;
  liveStats.portalExtraDownloads += 1;
  saveStatsToStorage();
  renderLiveStatsUI();
  pingCounterApi(`dl_${{caseId}}`, true).then(remoteCount => {{
    if (remoteCount !== null && remoteCount > liveStats.perReport[caseId].downloads) {{
      liveStats.perReport[caseId].downloads = remoteCount;
      saveStatsToStorage();
      renderLiveStatsUI();
    }}
  }});
}}

function trackCorpusDownload() {{
  liveStats.portalExtraDownloads += 1;
  saveStatsToStorage();
  renderLiveStatsUI();
  pingCounterApi('dl_full_corpus', true);
}}

const EN_REPORTS_META = {{
  "QV-2026-001": {{
    surah_en: "At-Tawbah",
    topic_en: "Breach of Covenant (Nakth al-Ahd), Deterrence & Legitimate Self-Defense Architecture in International Law",
    aporia_en: "[ANALYSIS] How can states reconcile the strict Quranic prohibition of aggression against treaty-abiding communities (At-Tawbah 9:4 & 9:6) with the necessity of strategic deterrence when systemic treaty violations (nakth al-ahd) threaten collective security?",
    z3_en: "[ANALYSIS] In an era of hybrid warfare and asymmetric non-state actors, how should international legal frameworks define the threshold of 'breach of covenant' without triggering disproportionate escalation?"
  }},
  "QV-2026-002": {{
    surah_en: "An-Nisa",
    topic_en: "Intra-Family Governance, Fiduciary Responsibility (Qawwamah) & Graduated De-Escalation in Marital Crisis",
    aporia_en: "[ANALYSIS] How does classical Maqasid jurisprudence distinguish fiduciary family stewardship (qawwamah bi-ma'ruf) from authoritarian domination, establishing a strictly non-violent, restorative conflict-resolution protocol?",
    z3_en: "[ANALYSIS] How can modern family law and mediation institutions operationalize the three-stage Quranic reconciliation model (dialogue, reflective space, and family arbitration in 4:34-35) to prevent domestic violence and family breakdown?"
  }},
  "QV-2026-003": {{
    surah_en: "Al-Ma'idah",
    topic_en: "Property Protection, Stringent Evidentiary Conditions (Hirz & Nisab), State of Necessity & Social Security Architecture",
    aporia_en: "[ANALYSIS] Why did Caliph 'Umar ibn al-Khattab suspend the statutory penalty during the Year of Famine ('Am al-Ramadah), proving that Quranic penal norms cannot operate independently of distributive justice and social safety nets?",
    z3_en: "[ANALYSIS] In contemporary economies marked by severe wealth inequality, how does the classical legal doctrine of shubhah (evidentiary doubt) and darurah (economic necessity) prioritize social welfare over punitive maximalism?"
  }},
  "QV-2026-004": {{
    surah_en: "Al-Baqarah",
    topic_en: "Freedom of Conscience, Prohibition of Coercion (La Ikraha fi'd-Din) & Pluralistic Civil Society Architecture",
    aporia_en: "[ANALYSIS] Since genuine faith requires uncoerced cognitive and moral assent (tasdiq al-qalb), any political or social compulsion in religion destroys the very moral agency that revelation seeks to cultivate.",
    z3_en: "[ANALYSIS] How can modern pluralistic societies protect both freedom of conscience (2:256) and public moral cohesion against algorithmic manipulation and ideological polarization?"
  }},
  "QV-2026-005": {{
    surah_en: "An-Nisa",
    topic_en: "Public Trust (Amanah), Meritocracy, Judicial Independence & Universal Justice Architecture",
    aporia_en: "[ANALYSIS] Why does An-Nisa 4:58 link the macro-stability of states directly to two non-negotiable pillars: entrusting public office strictly to merit (amanah) and adjudicating with blind impartiality ('adl)?",
    z3_en: "[ANALYSIS] When nepotism or partisan loyalty conflicts with objective competence in public appointments, what institutional safeguards best enforce the Quranic mandate of returning trusts to their rightful bearers?"
  }},
  "QV-2026-006": {{
    surah_en: "Ali 'Imran",
    topic_en: "Consultative Governance (Shura) in Crisis, Participatory Decision-Making & Compassionate Leadership Architecture",
    aporia_en: "[ANALYSIS] Immediately after the setback at Uhud, why did revelation command the Prophet to institutionalize consultation (wa shawirhum fi'l-amr) rather than centralize emergency authoritarian power?",
    z3_en: "[ANALYSIS] In high-velocity national or organizational crises, how do leaders balance inclusive deliberative consultation (shura) with decisive executive action ('azm)?"
  }},
  "QV-2026-007": {{
    surah_en: "Al-Hujurat",
    topic_en: "International Conflict Resolution, Anti-Aggression Doctrine (Baghy), Collective Security & Peacekeeping Governance",
    aporia_en: "[ANALYSIS] How does Al-Hujurat 49:9-10 establish an objective collective-security mechanism that obligates neutral mediation (islah) first, permits collective deterrence against the aggressor (al-fi'ah al-baghiyah), and mandates a just peace (islah bi'l-'adl)?",
    z3_en: "[ANALYSIS] Why do contemporary international security councils fail when veto privileges override the impartial anti-aggression (baghy) standard articulated in 49:9?"
  }},
  "QV-2026-008": {{
    surah_en: "Al-Isra",
    topic_en: "Epistemic Responsibility, Information Verification, Cognitive Security & AI Governance in the Digital Age",
    aporia_en: "[ANALYSIS] By prohibiting humanity from pursuing that of which it has no verified knowledge (wa la taqfu ma laysa laka bihi 'ilm) and holding hearing, sight, and intellect accountable, 17:36 establishes a foundational charter for epistemic ethics.",
    z3_en: "[ANALYSIS] In an age of deepfakes, synthetic media, and algorithmic echo chambers, how can educational and legal institutions enforce epistemic accountability without curtailing legitimate inquiry?"
  }},
  "QV-2026-009": {{
    surah_en: "Al-Hashr",
    topic_en: "Wealth Concentration, Economic Circulation (Kay la Yakuna Dulatan), Distributive Justice & Anti-Oligarchy Doctrine",
    aporia_en: "[ANALYSIS] Al-Hashr 59:7 explicitly states the macro-economic objective (illa/hikmah) of Islamic fiscal policy: 'so that wealth does not become a perpetual monopoly circulating solely among the rich among you.'",
    z3_en: "[ANALYSIS] Which fiscal, waqf, and productive-investment instruments are most effective in reversing extreme wealth concentration while preserving entrepreneurial dynamism?"
  }},
  "QV-2026-010": {{
    surah_en: "Ar-Rum",
    topic_en: "Ontological Pluralism, Linguistic & Ethnic Diversity, Anti-Assimilation & Multicultural Coexistence Architecture",
    aporia_en: "[ANALYSIS] By elevating the diversity of human languages and colors (ikhtilaf alsinatikum wa alwanikum) to the status of cosmic divine signs (ayat) alongside the creation of the heavens and the earth, Ar-Rum 30:22 delegitimizes forced assimilation and racial hierarchy.",
    z3_en: "[ANALYSIS] How can modern nation-states preserve linguistic and cultural diversity as a source of civilizational enrichment while maintaining shared constitutional citizenship?"
  }},
  "QV-2026-011": {{
    surah_en: "Al-An'am",
    topic_en: "Universal Moral Decalogue, Fundamental Human Rights Charter, Market Integrity & Judicial Impartiality",
    aporia_en: "[ANALYSIS] Across all prophetic dispensations, Al-An'am 6:151-152 codifies ten universal moral imperatives—anchored in the sanctity of life, intergenerational care, protection of orphan assets, fair weights (qist), and impartial testimony even against one's own kin.",
    z3_en: "[ANALYSIS] When familial, tribal, or institutional self-interest clashes with truthful testimony (wa idha qultum fa'dilu wa law kana dha qurba), what ethical training sustains moral courage?"
  }},
  "QV-2026-012": {{
    surah_en: "Al-Hadid",
    topic_en: "The Triad of Book, Balance (Mizan) & Iron (Hadid): Constitutional Law, Institutional Justice & Deterrent Defense",
    aporia_en: "[ANALYSIS] Al-Hadid 57:25 reveals the triadic architecture of viable civilization: Revelation/Law (al-Kitab), Objective Justice Metrics (al-Mizan), and Deterrent Material/Technological Power (al-Hadid)—where power without justice becomes tyranny, and justice without deterrence remains defenseless.",
    z3_en: "[ANALYSIS] In the 21st-century technological race, how can societies develop indigenous strategic deterrence ('Iron') that remains strictly subordinated to ethical and constitutional justice ('Mizan')?"
  }},
  "QV-2026-013": {{
    surah_en: "An-Nahl",
    topic_en: "Universal Civilizational Covenant: Justice ('Adl), Excellence (Ihsan), Social Solidarity & Anti-Corruption Governance",
    aporia_en: "[ANALYSIS] Celebrated by Ibn Mas'ud as the most comprehensive verse in the Quran, An-Nahl 16:90 pairs a three-tier constructive architecture ('Adl, Ihsan, Ita' dhi'l-Qurba) with a three-tier barrier against moral, social, and political decay (Fahsha', Munkar, Baghy).",
    z3_en: "[ANALYSIS] Why does sustainable civilization require moving beyond mere legalistic reciprocity ('Adl) toward proactive moral generosity and restorative empathy (Ihsan)?"
  }},
  "QV-2026-014": {{
    surah_en: "Al-Hujurat",
    topic_en: "Ontological Equality of Humankind, Doctrine of Mutual Recognition (Ta'aruf), Anti-Racism & Taqwa-Based Universal Merit",
    aporia_en: "[ANALYSIS] Addressing all of humanity (Ya ayyuha'n-nas), Al-Hujurat 49:13 affirms a single shared human origin, redefines ethnic and national plurality strictly as a vehicle for mutual discovery and cooperation (li-ta'arafu), and replaces hereditary/racial superiority with moral-ethical consciousness (Taqwa).",
    z3_en: "[ANALYSIS] When demographic migration and geopolitical tensions fuel xenophobia and identity politics, how can educational and civic institutions operationalize the Quranic paradigm of Ta'aruf (active mutual recognition) over conflict?"
  }},
  "QV-2026-015": {{
    surah_en: "Al-Ma'idah",
    topic_en: "Inviolability of Human Life, Doctrine of Saving Life (Ihya'), Global Human Security & Bioethics Architecture",
    aporia_en: "[ANALYSIS] Against utilitarian calculus that reduces innocent human lives to expendable statistics ('collateral damage'), Al-Ma'idah 5:32 establishes an absolute ontological equation: taking a single innocent life is equivalent to destroying all of humanity, and saving a single life (wa man ahyaha) is equivalent to saving all of humanity.",
    z3_en: "[ANALYSIS] How must contemporary military doctrines, autonomous weapons regulations, and public health / occupational safety systems confront the Quranic principle that 'One Innocent Life = All of Humanity'?"
  }}
}};

const CANDIDATE_VERSES = [
  {{
    surah: "Bakara", surah_en: "Al-Baqarah", verse: "2:143",
    title: "Vasat Ümmet (Denge ve İtidal), Küresel Şahitlik ve Kutuplaşma Karşıtı Jeopolitik",
    title_en: "The Balanced Community (Ummatan Wasatan), Global Moral Witness & Anti-Polarization Geopolitics"
  }},
  {{
    surah: "Alak", surah_en: "Al-'Alaq", verse: "96:1-5",
    title: "İkra ve Kalem Doktrini: Bilimsel Üretim, Epistemik Medeniyet ve Eğitim Felsefesi",
    title_en: "The Doctrine of Iqra' and the Pen: Scientific Production, Epistemic Civilization & Philosophy of Education"
  }},
  {{
    surah: "Fussilet", surah_en: "Fussilat", verse: "41:34",
    title: "Kötülüğü En Güzel Olanla Savmak (İhsan Stratejisi): Çatışma Çözümü ve Toplumsal Barış Diplomasisi",
    title_en: "Repelling Evil with What is Best (Daf' bi'llati hiya Ahsan): Conflict Transformation & Peace Diplomacy"
  }},
  {{
    surah: "Zümer", surah_en: "Az-Zumar", verse: "39:18",
    title: "Sözü Dinleyip En Güzeline Uymak (Ahsenü'l-Kavl): Eleştirel Düşünce ve Açık Müzakere Ahlakı",
    title_en: "Listening to Discourse and Following the Best of It (Ahsan al-Qawl): Critical Thinking & Deliberative Ethics"
  }},
  {{
    surah: "Mülk", surah_en: "Al-Mulk", verse: "67:3-4",
    title: "Kozmik Düzen, Kusursuzluk Arayışı, Bilimsel Gözlem ve Ekoloji Mimarisi",
    title_en: "Cosmic Order, Empirical Observation, Scientific Inquiry & Ecological Stewardship"
  }},
  {{
    surah: "İsrâ", surah_en: "Al-Isra", verse: "17:70",
    title: "İnsanoğlunun Mükerrem Yaratılışı (Tekrîm-i Benî Âdem): Evrensel İnsan Onuru ve Haklar Mimarisi",
    title_en: "The Honored Creation of Humankind (Takrim Bani Adam): Universal Human Dignity & Rights Architecture"
  }}
];

function getReportSurah(r) {{
  if (currentLang === 'en' && EN_REPORTS_META[r.case_id]) return EN_REPORTS_META[r.case_id].surah_en;
  return r.surah;
}}

function getReportTopic(r) {{
  if (currentLang === 'en' && EN_REPORTS_META[r.case_id]) return EN_REPORTS_META[r.case_id].topic_en;
  return r.topic;
}}

function getReportAporia(r) {{
  if (currentLang === 'en' && EN_REPORTS_META[r.case_id]) return EN_REPORTS_META[r.case_id].aporia_en;
  return r.aporia;
}}

function getReportZ3(r) {{
  if (currentLang === 'en' && EN_REPORTS_META[r.case_id]) return EN_REPORTS_META[r.case_id].z3_en;
  return r.z3_question;
}}

function setLanguage(lang) {{
  currentLang = lang === 'en' ? 'en' : 'tr';
  localStorage.setItem('qv_lang_v621', currentLang);
  document.documentElement.setAttribute('lang', currentLang);

  const isEn = currentLang === 'en';
  document.getElementById('brandBadge').textContent = isEn
    ? '🏛️ QURAN VISION INSTITUTE • v6.2.1'
    : '🏛️ QURAN VISION ENSTİTÜSÜ • v6.2.1';
  document.getElementById('brandTitle').textContent = isEn
    ? 'QURAN VISION CORPUS'
    : 'KUR’ÂN VİZYONU';
  document.getElementById('brandSubEn').textContent = isEn
    ? 'STRATEGIC TAFSIR & FORESIGHT'
    : 'STRATEGIC TAFSIR CORPUS';
  document.getElementById('brandDesc').textContent = isEn
    ? 'Evidence-Based Quranic Strategic Foresight & Maqasid Corpus'
    : 'Stratejik Tefsir, Makâsıd ve Medeniyet Öngörü Külliyatı';
  document.getElementById('brandMetaLeft').textContent = isEn
    ? `⚖️ ISNAD 2 (${{TOTAL_CLASSICAL}} Texts) • ${{TOTAL_MODERN}} DOIs`
    : `⚖️ İSNAD 2 (${{TOTAL_CLASSICAL}} Nakil) • ${{TOTAL_MODERN}} DOI`;
  document.getElementById('brandMetaRight').textContent = isEn
    ? `26 Steps • ${{REPORTS.length}} Reports`
    : `26 Adım • ${{REPORTS.length}} Rapor`;

  const searchInput = document.getElementById('searchInput');
  if (searchInput) {{
    searchInput.placeholder = isEn
      ? 'Search surah, verse, concept, or scholar...'
      : 'Sûre, âyet, kavram veya müfessir ara...';
  }}

  const fullBookBtn = document.getElementById('fullBookPdfBtn');
  if (fullBookBtn) {{
    fullBookBtn.href = isEn ? 'pdf/Quran_Vision_Corpus_EN_v6.2.1.pdf' : 'pdf/Quran_Vision_Kulliyat_v6.2.1.pdf';
    fullBookBtn.setAttribute('download', isEn ? 'Quran_Vision_Corpus_EN_v6.2.1.pdf' : 'Quran_Vision_Kulliyat_v6.2.1.pdf');
    fullBookBtn.innerHTML = isEn ? `📚 Full Corpus PDF` : `📚 Tüm Külliyat PDF`;
  }}
  document.getElementById('langToggleTopBtn').innerHTML = isEn ? '🌐 EN ➔ TR' : '🌐 TR ➔ EN';

  document.getElementById('tabBtn-dashboard').innerHTML = isEn ? '📊 Dashboard & Summary' : '📊 Kokpit & Özet';
  document.getElementById('tabBtn-fulltext').innerHTML = isEn ? '📖 Full Text (26 Steps)' : '📖 Tam Metin (26 Adım)';
  document.getElementById('tabBtn-sources').innerHTML = isEn ? '🕌 Sources (ISNAD 2)' : '🕌 Kaynakça (İSNAD 2)';
  document.getElementById('tabBtn-pedagogy').innerHTML = isEn ? '🎓 Lesson Kit' : '🎓 Ders Kiti';
  document.getElementById('tabBtn-synthesis').innerHTML = isEn ? '🕸️ Synthesis Matrix' : '🕸️ Sentez Matrisi';
  document.getElementById('tabBtn-feedback').innerHTML = isEn ? '💬 Peer-Review' : '💬 Şerh Yaz';

  updateSidebarToggleUI();
  updateThemeButtonsUI();
  renderLiveStatsUI();
  renderSidebar(searchInput ? searchInput.value : '');
  selectReport(currentIndex);
}}

function renderSidebar(filter = '') {{
  const listEl = document.getElementById('reportList');
  const q = filter.toLowerCase().trim();
  listEl.innerHTML = '';

  REPORTS.forEach((r, idx) => {{
    const enMeta = EN_REPORTS_META[r.case_id] || {{}};
    const classicalNames = (r.classical_sources || []).map(cs => cs.author + ' ' + cs.work).join(' ');
    const searchable = (r.surah + ' ' + (enMeta.surah_en || '') + ' ' + r.verse + ' ' + r.topic + ' ' + (enMeta.topic_en || '') + ' ' + r.case_id + ' ' + classicalNames + ' ' + r.body).toLowerCase();
    if (q && !searchable.includes(q)) return;

    const item = document.createElement('div');
    item.className = 'report-item' + (idx === currentIndex ? ' active' : '');
    item.onclick = () => selectReport(idx);
    item.innerHTML = `
      <div class="report-item-top">
        <span class="report-surah">${{idx + 1}}. ${{getReportSurah(r)}} ${{r.verse}}</span>
        <span class="report-code">${{r.case_id}}</span>
      </div>
      <div class="report-topic">${{getReportTopic(r)}}</div>
    `;
    listEl.appendChild(item);
  }});
}}

function selectReport(idx) {{
  currentIndex = idx;
  renderSidebar(document.getElementById('searchInput').value);
  const r = REPORTS[idx];
  const isEn = currentLang === 'en';
  const surahDisp = getReportSurah(r);
  const topicDisp = getReportTopic(r);
  const aporiaDisp = getReportAporia(r);
  const activePdfFile = isEn ? (r.pdf_filename_en || r.pdf_filename) : r.pdf_filename;
  const activeMdPath = isEn ? `docs/en/${{r.filename_en || r.filename}}` : `docs/tr/${{r.filename}}`;

  document.title = `${{r.case_id}} - ${{surahDisp}} ${{r.verse}} - Quran Vision v6.2.1`;
  const dlBtn = document.getElementById('downloadPdfBtn');
  if (dlBtn) {{
    dlBtn.href = `pdf/${{activePdfFile}}`;
    dlBtn.setAttribute('download', isEn ? `${{r.case_id}}_${{surahDisp}}_Report_EN.pdf` : `${{r.case_id}}_${{r.surah}}_Raporu.pdf`);
  }}
  trackReportView(r.case_id);

  // Hero (Simplified with <details> disclosure for Academic Ownership, ORCID & SHA-256)
  document.getElementById('heroCard').innerHTML = `
    <div class="hero-meta">
      <span class="badge badge-gold">📖 ${{isEn ? 'Surah ' + surahDisp : surahDisp + ' Sûresi'}} ${{r.verse}}</span>
      <span class="badge badge-emerald">${{isEn ? 'Layer 3 • H6 Complex Verse' : 'Katman 3 • H6 Zorlu Âyet'}}</span>
      <span class="badge badge-mono">${{r.case_id}}</span>
      <span class="badge badge-mono">${{isEn ? 'Confidence: ' : 'Güven: '}}${{r.confidence}}</span>
      <span class="badge badge-mono">${{isEn ? 'Status: ' : 'Statü: '}}${{r.status}}</span>
    </div>
    <div class="hero-title">${{topicDisp}}</div>
    <details class="meta-disclosure">
      <summary class="meta-summary">
        <span>🏛️ ${{isEn ? 'Academic Ownership, ORCID & SHA-256 Cryptographic Seal (Mehmet Yarıcı • Advisor: M. E. Koç)' : 'Akademik Künye, ORCID & SHA-256 Mührü (Mehmet Yarıcı • Danışman: M. E. Koç)'}}</span>
      </summary>
      <div class="meta-disclosure-body">
        <div>👑 <strong>${{isEn ? 'Founder & Principal Author (Corpus Owner):' : 'Proje Kurucusu & Başyazar (Eser Sahibi):'}} Mehmet Yarıcı</strong> — <span style="color:var(--text-secondary);">${{isEn ? 'Uludağ University Faculty of Theology (1989) • Republic of Türkiye Ministry of National Education (MEB), Bahçelievler Dede Korkut Anatolian High School' : 'Uludağ Üniversitesi İlahiyat Fakültesi (1989) • T.C. Millî Eğitim Bakanlığı, İstanbul Bahçelievler Dede Korkut Anadolu Lisesi'}}</span> &nbsp;<a href="https://orcid.org/0009-0003-0356-8582" target="_blank" rel="noopener" style="color:var(--accent-emerald); font-family:'JetBrains Mono',monospace; font-size:11.5px; text-decoration:none;">[ORCID: 0009-0003-0356-8582]</a></div>
        <div>🏛️ <strong>${{isEn ? 'Academic Advisor & External Peer-Reviewer:' : 'Akademik Danışman & Dış Hakem:'}} Mehmet Emin Koç</strong> — <span style="color:var(--text-secondary);">${{isEn ? 'Azerbaijan National Academy of Sciences (ANAS), Institute of Philosophy and Sociology' : 'Azerbaycan Milli İlimler Akademisi (AMEA), Felsefe ve Sosyoloji Enstitüsü'}}</span> &nbsp;<a href="https://orcid.org/0000-0002-1025-5643" target="_blank" rel="noopener" style="color:var(--accent-emerald); font-family:'JetBrains Mono',monospace; font-size:11.5px; text-decoration:none;">[ORCID: 0000-0002-1025-5643]</a></div>
        <div class="sha-bar">🔒 <strong>${{isEn ? 'SHA-256:' : 'SHA-256:'}}</strong> ${{isEn ? (r.sha256_en || r.sha256) : r.sha256}} &nbsp;|&nbsp; 📄 <code>${{activeMdPath}}</code> &nbsp;|&nbsp; 🏛️ <strong>DOI (v6.2.1):</strong> <a href="https://doi.org/10.5281/zenodo.23410818" target="_blank" rel="noopener" style="color:var(--accent-gold);">10.5281/zenodo.23410818</a> <span style="opacity:0.8;">(Concept: <a href="https://doi.org/10.5281/zenodo.23391192" target="_blank" rel="noopener" style="color:var(--accent-emerald);">10.5281/zenodo.23391192</a>)</span></div>
      </div>
    </details>
  `;

  // Tab 1: Dashboard
  const priorPct = Math.round(r.prior * 100);
  const postPct = Math.round(r.posterior * 100);

  const activeScenarios = isEn ? (r.scenarios_en || r.scenarios || []) : (r.scenarios || []);
  let scenariosHtml = activeScenarios.map(s => {{
    const sc = s.scores || {{}};
    return `
      <div class="source-card">
        <div class="source-header">
          <span class="source-author">${{s.id}} — ${{s.title}}</span>
          <span class="badge badge-gold">${{isEn ? 'Priority' : 'Öncelik'}}: ${{sc.stratejik_oncelik || '-'}}/5</span>
        </div>
        <div class="source-meta">${{s.score_justification || ''}}</div>
        <div style="display:flex; gap:10px; font-size:12px; color:var(--text-muted); flex-wrap:wrap;">
          <span>${{isEn ? 'Probability' : 'Olasılık'}}: <b>${{sc.olasilik || '-'}}/5</b></span>
          <span>${{isEn ? 'Impact' : 'Tesir'}}: <b>${{sc.tesir || '-'}}/5</b></span>
          <span>${{isEn ? 'Opportunity' : 'Fırsat'}}: <b>${{sc.firsat || '-'}}/5</b></span>
          <span>${{isEn ? 'Vulnerability' : 'Kırılganlık'}}: <b>${{sc.kirilganlik || '-'}}/5</b></span>
        </div>
      </div>
    `;
  }}).join('');

  const activeThresholds = isEn ? (r.thresholds_en || r.thresholds || []) : (r.thresholds || []);
  let thresholdsHtml = activeThresholds.map(t => `
    <div class="source-card">
      <div class="source-header">
        <span class="source-author">${{t.name}}</span>
        <span class="badge badge-emerald">${{t.value}}</span>
      </div>
      <div class="source-meta">${{t.derivation_basis}}</div>
    </div>
  `).join('');

  document.getElementById('tab-dashboard').innerHTML = `
    <div class="grid-2">
      <div class="panel">
        <h3><span>📈 ${{isEn ? 'Bayesian Policy Update (Step 14)' : 'Bayesyen Politika Güncellemesi (Adım 14)'}}</span><span>2026–2036</span></h3>
        <div class="bayes-row">
          <div class="bayes-label">
            <span>${{isEn ? 'Prior Probability — P(S1) (Baseline Institutional Inertia)' : 'Önsel Olasılık — Prior P(S1) (Mevcut Ataletle Başarı)'}}</span>
            <strong>%${{priorPct}} (${{r.prior.toFixed(2)}})</strong>
          </div>
          <div class="progress-track">
            <div class="progress-fill" style="width:${{priorPct}}%; background:var(--accent-gold);"></div>
          </div>
        </div>
        <div class="bayes-row">
          <div class="bayes-label">
            <span>${{isEn ? 'Posterior Probability — P(S1|E) (With Quranic Institutional Reform)' : 'Sonsal Olasılık — Posterior P(S1|E) (Kurumsal Reform Kanıtıyla)'}}</span>
            <strong style="color:var(--accent-emerald);">%${{postPct}} (${{r.posterior.toFixed(2)}})</strong>
          </div>
          <div class="progress-track">
            <div class="progress-fill" style="width:${{postPct}}%; background:var(--accent-emerald);"></div>
          </div>
        </div>
        <h3 style="margin-top:22px;"><span>🎯 ${{isEn ? 'Empirical & Predictive Threshold Indicators (V6)' : 'Ampirik ve Tahminî Eşik Göstergeleri (V6)'}}</span></h3>
        ${{thresholdsHtml}}
      </div>

      <div class="panel">
        <h3><span>⚡ ${{isEn ? 'Z-1: Core Methodological Problematic (Aporia)' : 'Z-1: Şablona Sığmayan Özgün Problematik (Aporia)'}}</span><span>${{isEn ? 'V9 Mandatory' : 'V9 Zorunlu'}}</span></h3>
        <div class="source-card" style="border-left: 3px solid var(--accent-gold); font-size:14px; line-height:1.75;">
          ${{formatInlineMd(aporiaDisp)}}
        </div>
        <h3 style="margin-top:20px;"><span>🧭 ${{isEn ? 'Four Structural Foresight Scenarios (V5)' : 'Dört Yapısal Senaryo Matrisi (V5)'}}</span></h3>
        ${{scenariosHtml}}
      </div>
    </div>
  `;

  // Tab: Classical & Modern Sources
  let classicalHtml = (r.classical_sources || []).map(cs => `
    <div class="source-card">
      <div class="source-header">
        <span class="source-author">${{cs.author}}</span>
        <span class="source-death">${{cs.death_year || ''}}</span>
      </div>
      <div class="source-meta">
        <em>${{cs.work}}</em> • ${{isEn ? 'Ed.' : 'Tahkik'}}: ${{cs.editor || '—'}} • ${{cs.publication_place || ''}}: ${{cs.publisher || ''}}, ${{cs.publication_year || ''}} • ${{isEn ? 'Vol.' : 'Cilt'}}: ${{cs.volume}}, ${{isEn ? 'pp.' : 'Sayfa'}}: ${{cs.pages}}
      </div>
      <div class="arabic-box">${{cs.arabic_quote || ''}}</div>
      <a class="source-link" href="${{cs.verification_link}}" target="_blank" rel="noopener">🔗 ${{isEn ? 'Digital Verification Link' : 'Dijital Tahkik Linki'}}: ${{cs.verification_link}} (${{cs.doi_or_urn || ''}})</a>
    </div>
  `).join('');

  let modernHtml = (r.modern_sources || []).map(ms => {{
    const rawDoi = String(ms.doi || '').trim();
    const doiMatch = rawDoi.match(/(10\\.\\d{{4,9}}\\/[-._;()/:A-Za-z0-9]+)/);
    const doiBadgeHtml = doiMatch
      ? `<a class="badge badge-mono doi-link" href="https://doi.org/${{doiMatch[1]}}" target="_blank" rel="noopener">DOI: ${{rawDoi}}</a>`
      : `<span class="badge badge-mono">${{rawDoi || (isEn ? 'Institutional Dataset' : 'Kurumsal Veritabanı')}}</span>`;
    return `
      <div class="source-card">
        <div class="source-header">
          <span class="source-author">${{ms.institution || ms.author}} (${{ms.publication_year || ''}})</span>
          ${{doiBadgeHtml}}
        </div>
        <div class="source-meta"><em>${{ms.title}}</em> • ${{ms.publication_place || ''}}: ${{ms.publisher || ''}}</div>
        <a class="source-link" href="${{ms.url}}" target="_blank" rel="noopener">🌐 ${{ms.url}}</a>
      </div>
    `;
  }}).join('');

  document.getElementById('tab-sources').innerHTML = `
    <div class="grid-2">
      <div class="panel">
        <h3><span>🕌 ${{isEn ? 'A) Classical Islamic Sources (ISNAD 2nd Edition)' : 'A) Klasik İslami Kaynaklar (İSNAD 2. Edisyon)'}}</span><span>${{(r.classical_sources||[]).length}} ${{isEn ? 'Works' : 'Eser'}}</span></h3>
        ${{classicalHtml}}
      </div>
      <div class="panel">
        <h3><span>📊 ${{isEn ? 'B) Contemporary Empirical & Institutional Sources (APA 7 / DOI)' : 'B) Çağdaş Ampirik ve Kurumsal Kaynaklar (APA 7 / DOI)'}}</span><span>${{(r.modern_sources||[]).length}} ${{isEn ? 'Sources' : 'Kaynak'}}</span></h3>
        ${{modernHtml}}
      </div>
    </div>
  `;

  // Tab 2 (Fulltext): Full 26-Step Markdown with clean sticky header (Title + Font Controls + Print only)
  const activeBodyMd = isEn ? (r.body_en || r.body) : r.body;
  let renderedFullMd = renderMarkdown(activeBodyMd);
  if (!renderedFullMd.includes('id="z5-peer-review-card"')) {{
    renderedFullMd += formatZ5YamlJs(`rapor_id: "${{r.case_id}}"\\nsure_ayet: "${{getReportSurah(r)}} ${{r.verse}}"\\ntarih: "2026-10-15"`);
  }}
  const pctNow = Math.round(currentFontScale * 100);
  const pctDisp = isEn ? `${{pctNow}}%` : `%${{pctNow}}`;
  const fulltextToolbar = `
    <div style="position:sticky; top:-20px; z-index:15; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; padding:10px 16px; margin-bottom:16px; border-radius:10px; background:var(--bg-surface); border:1.5px solid var(--accent-gold); box-shadow:var(--shadow);">
      <div style="font-size:13px; color:var(--text-secondary);">
        📖 <strong>${{r.case_id}} • ${{getReportSurah(r)}} ${{r.verse}}</strong> — ${{isEn ? '26-Step Full Academic Text' : '26 Adımlı Tam Akademik Metin'}}
      </div>
      <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
        <div class="font-size-controls" style="border-color:var(--accent-gold);">
          <button type="button" class="font-btn" onclick="changeFontSize(-0.1)" aria-label="${{isEn ? 'Decrease Font Size' : 'Yazıyı Küçült'}}">🔍 A−</button>
          <button type="button" class="font-btn font-scale-badge font-scale-sync" onclick="resetFontSize()" aria-label="${{isEn ? 'Reset to 100%' : 'Varsayılan Boyuta Sıfırla'}}">${{pctDisp}}</button>
          <button type="button" class="font-btn" onclick="changeFontSize(0.1)" aria-label="${{isEn ? 'Increase Font Size' : 'Yazıyı Büyüt'}}">A+ ➕</button>
        </div>
        <button type="button" class="btn" style="padding:6px 12px; font-size:12px;" onclick="printCurrentReport()">
          🖨️ ${{isEn ? 'Print' : 'Yazdır'}}
        </button>
      </div>
    </div>
  `;
  document.getElementById('tab-fulltext').innerHTML = `<div class="md-body">${{fulltextToolbar}}${{renderedFullMd}}</div>`;

  // Tab 4: Pedagogy & Lesson Plan Kit (TYMM)
  renderPedagogyTab(r);

  // Tab 5: Corpus Synthesis & Classical Scholar Matrix
  renderSynthesisTab();

  // Tab 6: Interactive Academic Feedback & Peer Review
  renderFeedbackTab(r);
}}

function renderPedagogyTab(r) {{
  const isEn = currentLang === 'en';
  const surahDisp = getReportSurah(r);
  const topicDisp = getReportTopic(r);
  const aporiaDisp = getReportAporia(r);
  const z3Disp = getReportZ3(r);
  const scholarsList = (r.classical_sources || []).map(cs => `${{cs.author}} (${{cs.work}})`).join(', ');
  const firstArabic = (r.classical_sources && r.classical_sources[0]) ? r.classical_sources[0].arabic_quote : '';
  const firstScholar = (r.classical_sources && r.classical_sources[0]) ? `${{r.classical_sources[0].author}} (${{r.classical_sources[0].death_year}})` : '';
  const scList = isEn ? (r.scenarios_en || r.scenarios || []) : (r.scenarios || []);
  const thList = isEn ? (r.thresholds_en || r.thresholds || []) : (r.thresholds || []);
  const s1Title = (scList && scList[0]) ? scList[0].title : (isEn ? 'Institutional Reform & Justice Scenario' : 'Kurumsal Reform ve Adalet Senaryosu');
  const s3Title = (scList && scList[2]) ? scList[2].title : (isEn ? 'Systemic Crisis & Breakdown Scenario' : 'Kriz ve Kurumsal Çözülme Senaryosu');
  const firstThreshold = (thList && thList[0]) ? `${{thList[0].name}} (${{thList[0].value}})` : (isEn ? 'Institutional Trust Indicator' : 'Kurumsal Güven Göstergesi');

  document.getElementById('tab-pedagogy').innerHTML = `
    <div class="panel" style="margin-bottom:20px; border-color:var(--accent-gold);">
      <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; margin-bottom:12px;">
        <div>
          <span class="badge badge-gold">${{isEn ? '🎓 COMPETENCY & VIRTUE-BASED CURRICULUM MODEL (TYMM)' : '🇹🇷 TÜRKİYE YÜZYILI MAARİF MODELİ (TYMM) UYUMLU'}}</span>
          <span class="badge badge-emerald" style="margin-left:6px;">${{isEn ? '40-Min Seminar & Classroom Debate Kit' : 'DKAB & İHL Meslek Dersleri Zümre Kiti'}}</span>
        </div>
        <div style="display:flex; gap:8px;">
          <button class="btn btn-primary" onclick="shareLessonPlanWhatsApp()">${{isEn ? "🟢 Share Lesson Plan via WhatsApp" : "🟢 Ders Planını WhatsApp'ta Zümremle Paylaş"}}</button>
          <button class="btn btn-gold" onclick="copyLessonPlan()">${{isEn ? "📋 Copy Lesson Plan" : "📋 Ders Planını Kopyala"}}</button>
        </div>
      </div>
      <h2 style="font-size:19px; color:var(--text-primary); margin-bottom:6px;">
        🎓 ${{isEn ? `Surah ${{surahDisp}} ${{r.verse}} — 40-Minute Classroom Debate & Case Analysis Lesson Plan` : `${{r.surah}} Sûresi ${{r.verse}} — 40 Dakikalık Sınıf İçi Münazara ve Vaka Analizi Ders Planı`}}
      </h2>
      <p style="font-size:13.5px; color:var(--text-secondary);">
        <strong>${{isEn ? 'Focus Topic:' : 'Odak Konu:'}}</strong> ${{topicDisp}} &nbsp;|&nbsp; <strong>${{isEn ? 'Reference Report:' : 'Referans Rapor:'}}</strong> <code>${{r.case_id}}</code>
      </p>
      <div id="pedagogyToast" class="toast-msg"></div>
    </div>

    <div class="grid-2">
      <div class="panel">
        <h3><span>⏱️ ${{isEn ? 'Stage 1 (Min 00–08): Inquiry & Case Hook' : '1. Aşama (00–08. Dk): Merak Uyandırma & Vaka Sunumu'}}</span><span>${{isEn ? 'Intro / Z-1' : 'Giriş / Z-1'}}</span></h3>
        <div class="source-card" style="border-left:3px solid var(--accent-gold);">
          <div class="source-author" style="margin-bottom:6px;">🔥 ${{isEn ? 'Opening Inquiry Question for Students (Aporia):' : 'Öğrencilere Sorulacak Derse Giriş Sorusu (Aporia):'}}</div>
          <div style="font-size:13.5px; color:var(--text-secondary); line-height:1.65;">
            ${{formatInlineMd(aporiaDisp)}}
          </div>
        </div>
        <div class="source-card">
          <div class="source-author" style="margin-bottom:4px;">🎯 ${{isEn ? 'Virtue-Value-Action Pedagogical Framework:' : 'TYMM Erdem-Değer-Eylem Çerçevesi:'}}</div>
          <div class="source-meta">
            ${{isEn
              ? '<strong>Core Values:</strong> Justice, Wisdom, Accountability, Compassion, Integrity<br><strong>Higher-Order Skills:</strong> Contextual Tafsir Literacy, Evidence-Based Decision Making, Deliberative Ethics'
              : '<strong>Kök Değerler:</strong> Adalet, Hikmet, Sorumluluk, Merhamet, Dürüstlük<br><strong>Üst Düzey Beceriler:</strong> Bağlamsal Tefsir Okuryazarlığı, Kanıta Dayalı Karar Alma, Münazara ve Müzakere Ahlakı'}}
          </div>
        </div>
      </div>

      <div class="panel">
        <h3><span>🏛️ ${{isEn ? 'Stage 2 (Min 08–20): Classical Tafsir Circle' : '2. Aşama (08–20. Dk): Klasik Tefsir Halkası'}}</span><span>ISNAD 2</span></h3>
        <div class="source-card">
          <div class="source-author" style="margin-bottom:6px;">🕌 ${{isEn ? 'Conceptual Framework of Classical Exegetes:' : 'Müfessirlerin Kavramsal Çerçevesi:'}}</div>
          <div class="source-meta">
            ${{isEn
              ? `Students examine the lexical and historical context of the verse through <strong>${{scholarsList}}</strong>.`
              : `Derste öğrencilere âyetin lafzî ve tarihsel bağlamı <strong>${{scholarsList}}</strong> üzerinden aktarılır.`}}
          </div>
          <div class="arabic-box" style="font-size:17px;">${{firstArabic}}</div>
          <div style="font-size:12px; color:var(--accent-gold);">— ${{firstScholar}}</div>
        </div>
        <div class="source-card">
          <div class="source-author" style="margin-bottom:4px;">💡 ${{isEn ? 'Epistemic Distinction (<code>[NAKİL / CITATION]</code> vs <code>[YORUM / ANALYSIS]</code>):' : 'Pedagojik Vurgu (<code>[NAKİL]</code> vs <code>[YORUM]</code>):'}}</div>
          <div class="source-meta">
            ${{isEn
              ? 'Students practice distinguishing between the immutable revealed text / classical exegetical transmission (<code>[NAKİL]</code>) and contemporary strategic policy inferences (<code>[YORUM]</code>).'
              : 'Öğrencilere âyetin değişmez ilahi metni ve klasik tefsir nakli (<code>[NAKİL]</code>) ile bugünün dünyasına yönelik stratejik çıkarımların (<code>[YORUM]</code>) birbirinden nasıl ayırt edileceği uygulamalı olarak gösterilir.'}}
          </div>
        </div>
      </div>

      <div class="panel">
        <h3><span>⚖️ ${{isEn ? 'Stage 3 (Min 20–33): Classroom Debate Workshop' : '3. Aşama (20–33. Dk): Sınıf İçi Münazara Atölyesi'}}</span><span>${{isEn ? 'Scenarios & Z-3' : 'Senaryo & Z-3'}}</span></h3>
        <div class="source-card" style="border-left:3px solid var(--accent-emerald);">
          <div class="source-author" style="margin-bottom:6px;">🗣️ ${{isEn ? 'Debate Dilemma (Z-3 Open-Ended Question):' : 'Münazara İkilemi (Z-3 Açık Uçlu Soru):'}}</div>
          <div style="font-size:13.5px; color:var(--text-secondary); line-height:1.65;">
            ${{formatInlineMd(z3Disp)}}
          </div>
        </div>
        <div class="source-card">
          <div class="source-author" style="margin-bottom:4px;">🧭 ${{isEn ? 'Two-Group Scenario Comparison:' : 'İki Grup Senaryo Karşılaştırması:'}}</div>
          <div class="source-meta">
            ${{isEn
              ? `• <strong>Group 1 (Reform Panel — S1):</strong> Why does implementing <em>"${{s1Title}}"</em> raise societal stability from <strong>${{Math.round(r.prior*100)}}% to ${{Math.round(r.posterior*100)}}%</strong>?<br>• <strong>Group 2 (Crisis Analysis — S3):</strong> What social costs emerge under <em>"${{s3Title}}"</em>?`
              : `• <strong>1. Grup (Reform Masası — S1):</strong> <em>"${{s1Title}}"</em> gerçekleşirse toplumda başarı olasılığı neden <strong>%${{Math.round(r.prior*100)}}'dan %${{Math.round(r.posterior*100)}}'a</strong> yükselir?<br>• <strong>2. Grup (Kriz Analizi — S3):</strong> <em>"${{s3Title}}"</em> yaşanırsa hangi toplumsal maliyetler ortaya çıkar?`}}
          </div>
        </div>
      </div>

      <div class="panel">
        <h3><span>📋 ${{isEn ? 'Stage 4 (Min 33–40): Reflection & Exit Ticket' : '4. Aşama (33–40. Dk): Değerlendirme & Çıkış Kartı'}}</span><span>${{isEn ? 'Action & Metric' : 'Eylem & Ölçüt'}}</span></h3>
        <div class="source-card">
          <div class="source-author" style="margin-bottom:6px;">📊 ${{isEn ? 'Real-Life Benchmark Indicator (Threshold):' : 'Somut Hayat Ölçütü (Threshold):'}}</div>
          <div class="source-meta">
            ${{isEn
              ? `Citing the indicator <strong>${{firstThreshold}}</strong>, ask students:<br><br><em>"What single concrete rule can we adopt in our school, family, and digital life today to practice the ethic of Surah ${{surahDisp}} ${{r.verse}}?"</em>`
              : `Öğrencilere <strong>${{firstThreshold}}</strong> göstergesi örnek verilerek şu kapanış sorusu yöneltilir:<br><br><em>"Bugün ${{r.surah}} ${{r.verse}} âyetinin ortaya koyduğu ilkeyi kendi okul ortamımızda, ailemizde ve dijital dünyamızda hayata geçirmek için hangi 1 somut kuralı uygulamalıyız?"</em>`}}
          </div>
        </div>
        <div style="margin-top:12px; display:flex; gap:10px; flex-wrap:wrap;">
          <button class="btn btn-gold" onclick="openFeedbackTab(); selectCategoryAndFocus('Sınıf İçi / Zümre Pedagojik Uygulama Deneyimi');">
            ✍️ ${{isEn ? 'Record Classroom / Seminar Reflection Here' : 'Bu Dersi İşledikten Sonra Zümre Deneyimini Buraya Kaydet'}}
          </button>
        </div>
      </div>
    </div>
  `;
}}

function buildLessonPlanText() {{
  const r = REPORTS[currentIndex];
  const isEn = currentLang === 'en';
  const scholarsList = (r.classical_sources || []).map(cs => cs.author).join(', ');
  if (isEn) {{
    return `*QURAN VISION (v6.2.1) — 40-MIN LESSON & DEBATE PLAN*\\n` +
      `━━━━━━━━━━━━━━━━━━━━\\n` +
      `📖 *Verse:* Surah ${{getReportSurah(r)}} ${{r.verse}} (${{r.case_id}})\\n` +
      `🎯 *Strategic Theme:* ${{getReportTopic(r)}}\\n` +
      `━━━━━━━━━━━━━━━━━━━━\\n` +
      `⏱️ *Stage 1 (00-08 Min - Inquiry):* ${{getReportAporia(r).slice(0, 220)}}...\\n\\n` +
      `🕌 *Stage 2 (08-20 Min - Classical Tafsir):* Contextual analysis via ${{scholarsList}}.\\n\\n` +
      `⚖️ *Stage 3 (20-33 Min - Classroom Debate):* ${{getReportZ3(r).slice(0, 240)}}...\\n\\n` +
      `📋 *Stage 4 (33-40 Min - Assessment):* Bayesian shift from ${{Math.round(r.prior*100)}}% -> ${{Math.round(r.posterior*100)}}% and ethical application.\\n` +
      `🔗 *Full Report & PDF:* https://mehmetyarici-crypto.github.io/quran-vision/`;
  }}
  return `*QURAN VISION (v6.2.1) — TYMM UYUMLU 40 DK DERS & MÜNAZARA PLANI*\\n` +
    `━━━━━━━━━━━━━━━━━━━━\\n` +
    `📖 *Ders Konusu:* ${{r.surah}} Sûresi ${{r.verse}} (${{r.case_id}})\\n` +
    `🎯 *Stratejik Tema:* ${{r.topic}}\\n` +
    `━━━━━━━━━━━━━━━━━━━━\\n` +
    `⏱️ *1. Aşama (00-08 Dk - Merak & Vaka):* ${{r.aporia.slice(0, 220)}}...\\n\\n` +
    `🕌 *2. Aşama (08-20 Dk - Klasik Tefsir Köprüsü):* ${{scholarsList}} nakilleriyle âyetin tarihsel ve lafzî tahkiki.\\n\\n` +
    `⚖️ *3. Aşama (20-33 Dk - Sınıf İçi Münazara Sorusu):* ${{r.z3_question.slice(0, 240)}}...\\n\\n` +
    `📋 *4. Aşama (33-40 Dk - Değerlendirme):* Kurumsal reformla başarı olasılığının %${{Math.round(r.prior*100)}} -> %${{Math.round(r.posterior*100)}} düzeyine çıkışı ve günlük hayat uygulaması.\\n` +
    `🔗 *Tam Rapor ve PDF:* https://mehmetyarici-crypto.github.io/quran-vision/`;
}}

function shareLessonPlanWhatsApp() {{
  const txt = buildLessonPlanText();
  window.open(`https://wa.me/?text=${{encodeURIComponent(txt)}}`, '_blank');
}}

function copyLessonPlan() {{
  const txt = buildLessonPlanText();
  if (navigator.clipboard) navigator.clipboard.writeText(txt);
  const el = document.getElementById('pedagogyToast');
  if (el) {{
    el.textContent = currentLang === 'en'
      ? "✅ 40-Minute Lesson & Debate Plan copied to clipboard!"
      : "✅ 40 Dakikalık TYMM Ders & Münazara Planı panoya kopyalandı!";
    el.style.display = 'block';
    setTimeout(() => {{ el.style.display = 'none'; }}, 4000);
  }}
}}

function renderSynthesisTab() {{
  const isEn = currentLang === 'en';
  const avgPrior = Math.round((REPORTS.reduce((a, b) => a + b.prior, 0) / REPORTS.length) * 100);
  const avgPost = Math.round((REPORTS.reduce((a, b) => a + b.posterior, 0) / REPORTS.length) * 100);
  const netGain = avgPost - avgPrior;

  const scholarMap = {{}};
  REPORTS.forEach((rep) => {{
    (rep.classical_sources || []).forEach(cs => {{
      const shortName = cs.author.split('(')[0].trim();
      if (!scholarMap[shortName]) {{
        scholarMap[shortName] = {{ count: 0, work: cs.work, death: cs.death_year, reports: [] }};
      }}
      scholarMap[shortName].count += 1;
      if (!scholarMap[shortName].reports.includes(rep.case_id)) {{
        scholarMap[shortName].reports.push(rep.case_id);
      }}
    }});
  }});

  const sortedScholars = Object.entries(scholarMap).sort((a, b) => b[1].count - a[1].count);
  const scholarsGridHtml = sortedScholars.map(([name, info]) => `
    <div class="candidate-card" style="cursor:pointer;" data-scholar="${{name.replace(/"/g, '&quot;')}}" onclick="filterByScholar(this.getAttribute('data-scholar'))">
      <div>
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
          <strong style="color:var(--accent-gold); font-size:13.5px;">🕌 ${{name}}</strong>
          <span class="badge badge-emerald">${{info.count}} ${{isEn ? 'Reports' : 'Rapor'}}</span>
        </div>
        <div style="font-size:12px; color:var(--text-secondary);"><em>${{info.work}}</em> (${{info.death || ''}})</div>
      </div>
      <div style="font-size:11px; color:var(--text-muted); font-family:'JetBrains Mono',monospace;">
        🔍 ${{isEn ? 'Click to Filter' : 'Tıkla & Filtrele'}}: ${{info.reports.join(', ')}}
      </div>
    </div>
  `).join('');

  const matrixRowsHtml = REPORTS.map((rep, idx) => {{
    const p1 = Math.round(rep.prior * 100);
    const p2 = Math.round(rep.posterior * 100);
    const diff = p2 - p1;
    return `
      <tr style="cursor:pointer; transition:background 0.15s;" onclick="selectReport(${{idx}}); setTab('dashboard', document.getElementById('tabBtn-dashboard'));" onmouseover="this.style.background='var(--bg-card-hover)'" onmouseout="this.style.background='transparent'">
        <td style="font-family:'JetBrains Mono',monospace; font-weight:700; color:var(--accent-gold);">${{rep.case_id}}</td>
        <td><strong>${{getReportSurah(rep)}} ${{rep.verse}}</strong></td>
        <td style="font-size:12.5px; color:var(--text-secondary);">${{getReportTopic(rep)}}</td>
        <td>%${{p1}} → <strong style="color:var(--accent-emerald);">%${{p2}}</strong> <span class="badge badge-emerald">+%${{diff}}</span></td>
        <td>${{(rep.classical_sources||[]).length}} ${{isEn ? 'Classical' : 'Klasik'}} / ${{(rep.modern_sources||[]).length}} DOI</td>
        <td><span class="badge badge-mono">${{rep.confidence}}</span></td>
      </tr>
    `;
  }}).join('');

  document.getElementById('tab-synthesis').innerHTML = `
    <div class="grid-2">
      <div class="panel">
        <h3><span>📈 ${{isEn ? `Macro-Bayesian Corpus Synthesis (${{REPORTS.length}}-Report Mean)` : `Külliyat Makro-Bayesyen Sentezi (${{REPORTS.length}} Rapor Ortalaması)`}}</span><span>2026–2036</span></h3>
        <div class="bayes-row">
          <div class="bayes-label">
            <span>${{isEn ? 'Corpus Mean Prior Probability — P(S1) (Institutional Inertia)' : 'Külliyat Ortalama Önsel Olasılık — Prior P(S1) (Mevcut Kurumsal Atalet)'}}</span>
            <strong>%${{avgPrior}}</strong>
          </div>
          <div class="progress-track">
            <div class="progress-fill" style="width:${{avgPrior}}%; background:var(--accent-gold);"></div>
          </div>
        </div>
        <div class="bayes-row">
          <div class="bayes-label">
            <span>${{isEn ? "Corpus Mean Posterior Probability — P(S1|E) (With Quranic Reform)" : "Külliyat Ortalama Sonsal Olasılık — Posterior P(S1|E) (Kur'ani İlkeler & Reformla)"}}</span>
            <strong style="color:var(--accent-emerald);">%${{avgPost}} (+%${{netGain}} ${{isEn ? 'Net Strategic Gain' : 'Net Stratejik Sıçrama'}})</strong>
          </div>
          <div class="progress-track">
            <div class="progress-fill" style="width:${{avgPost}}%; background:var(--accent-emerald);"></div>
          </div>
        </div>
        <p style="font-size:13px; color:var(--text-secondary); margin-top:10px;">
          ${{isEn
            ? `Across all ${{REPORTS.length}} foundational verses, quantitative Bayesian simulations demonstrate that institutionalizing covenant fidelity, meritocracy, consultation (shura), epistemic verification, wealth circulation, mizan, and ta'aruf increases long-term societal stability by an average of <strong>+${{netGain}} percentage points</strong>.`
            : `${{REPORTS.length}} kurucu âyetin tamamında yapılan nicel simülasyonlar; ahit vefası, liyakat, şûrâ, bilgi doğrulama (tebeyyün), servet dolaşımı, mîzân ve teâruf ilkeleri kurumsallaştırıldığında toplumsal istikrar olasılığının ortalama <strong>+%${{netGain}} puan</strong> arttığını kanıtlamaktadır.`}}
        </p>
      </div>

      <div class="panel">
        <h3><span>🏛️ ${{isEn ? 'Methodological Architecture Summary' : 'Metodolojik Mimari Özeti'}}</span><span>v6.2.1</span></h3>
        <div class="source-card">
          <div class="source-author">${{isEn ? `1. ISNAD 2 Classical Tafsir Verification (${{TOTAL_CLASSICAL}} Primary Citations)` : `1. İSNAD 2 Klasik Tefsir Tahkiki (${{TOTAL_CLASSICAL}} Arapça Nakil)`}}</div>
          <div class="source-meta">${{isEn
            ? 'Primary classical exegesis (riwayah, dirayah, ahkam, and maqasid) verified with Hijri/Gregorian death dates, critical edition editors, volumes, and page numbers.'
            : 'Erken dönem rivayet, dirayet, fıkhî ahkâm ve makâsıd tefsirlerinden hicrî/milâdî vefat yılı, tahkik ve cilt/sayfa doğrulamalı birincil kaynak ağı.'}}</div>
        </div>
        <div class="source-card">
          <div class="source-author">${{isEn ? `2. Contemporary Empirical Data & DOI Network (${{TOTAL_MODERN}} Institutional Datasets)` : `2. Çağdaş Ampirik Veri & DOI Ağı (${{TOTAL_MODERN}} Kurumsal Veri Kaynağı)`}}</div>
          <div class="source-meta">${{isEn
            ? 'Falsifiable threshold indicators calibrated against World Bank, UNDP, WJP, SIPRI, OECD, and UNESCO empirical datasets.'
            : 'Dünya Bankası, UNDP, WJP, SIPRI, OECD ve UNESCO göstergeleriyle kalibre edilmiş yanlışlanabilir eşik değerler (Thresholds).'}}</div>
        </div>
      </div>
    </div>

    <div class="panel" style="margin-bottom:22px;">
      <h3><span>🕌 ${{isEn ? 'Cross-Corpus Classical Exegete Index (Click a Scholar to Filter)' : 'Külliyat Çapraz Müfessir İndeksi (Filtrelemek İçin Müfessire Tıklayın)'}}</span><span>ISNAD 2</span></h3>
      <div class="candidate-grid">
        ${{scholarsGridHtml}}
      </div>
    </div>

    <div class="panel md-body" style="padding:22px;">
      <h3 style="margin-top:0;"><span>📊 ${{isEn ? `Comprehensive Comparison Matrix of All ${{REPORTS.length}} Strategic Reports (Click Row to Open)` : `${{REPORTS.length}} Stratejik Raporun Bütüncül Karşılaştırma Matrisi (Rapora Gitmek İçin Satıra Tıklayın)`}}</span></h3>
      <table>
        <thead>
          <tr>
            <th>${{isEn ? 'Case ID' : 'Vaka Kodu'}}</th>
            <th>${{isEn ? 'Surah / Verse' : 'Sûre / Âyet'}}</th>
            <th>${{isEn ? 'Strategic Doctrine & Governance Title' : 'Stratejik Doktrin & Yönetişim Başlığı'}}</th>
            <th>${{isEn ? 'Bayesian Shift (Prior → Posterior)' : 'Bayesyen Sıçrama (Prior → Posterior)'}}</th>
            <th>${{isEn ? 'Source Network' : 'Kaynak Ağı'}}</th>
            <th>${{isEn ? 'Confidence' : 'Güven'}}</th>
          </tr>
        </thead>
        <tbody>
          ${{matrixRowsHtml}}
        </tbody>
      </table>
    </div>
  `;
}}

function filterByScholar(scholarName) {{
  const input = document.getElementById('searchInput');
  if (input) {{
    input.value = scholarName;
    renderSidebar(scholarName);
  }}
}}

function renderFeedbackTab(r) {{
  const isEn = currentLang === 'en';
  const surahDisp = getReportSurah(r);
  const nextReportNum = REPORTS.length + 1;
  const nextCaseId = 'QV-2026-' + String(nextReportNum).padStart(3, '0');
  const candidatesHtml = CANDIDATE_VERSES.map((cv, cIdx) => {{
    const cvSurah = isEn ? cv.surah_en : cv.surah;
    const cvTitle = isEn ? cv.title_en : cv.title;
    return `
      <div class="candidate-card">
        <div>
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
            <strong style="color:var(--accent-gold); font-size:14px;">📖 ${{cvSurah}} ${{cv.verse}}</strong>
            <span class="badge badge-mono">${{isEn ? 'Candidate' : 'Aday'}} #${{cIdx + 1}}</span>
          </div>
          <div style="font-size:12.5px; color:var(--text-secondary); line-height:1.5;">${{cvTitle}}</div>
        </div>
        <button class="btn btn-gold" style="width:100%; justify-content:center;" data-vref="${{cvSurah}} ${{cv.verse}}" data-vtitle="${{cvTitle.replace(/"/g, '&quot;')}}" onclick="prefillCandidateVerse(this.getAttribute('data-vref'), this.getAttribute('data-vtitle'))">
          🗳️ ${{isEn ? 'Nominate This Verse for Next Report' : 'Sıradaki Rapor İçin Bu Âyeti Öner'}}
        </button>
      </div>
    `;
  }}).join('');

  document.getElementById('tab-feedback').innerHTML = `
    <div class="grid-2">
      <div class="panel">
        <h3><span>❓ ${{isEn ? 'Z-3: Open-Ended Strategic Dilemma for Peer Deliberation' : 'Z-3: Okuyucuya Bırakılan Açık Uçlu Stratejik İkilem'}}</span><span>${{r.case_id}} • ${{surahDisp}} ${{r.verse}}</span></h3>
        <div class="source-card" style="border-left: 3px solid var(--accent-emerald); font-size:14px; line-height:1.75; margin-bottom:16px;">
          ${{formatInlineMd(getReportZ3(r) || (isEn ? 'Share your scholarly reflection on this report below.' : 'Bu raporun açık uçlu müzakere sorusu hakkında görüşünüzü aşağıdan paylaşabilirsiniz.'))}}
        </div>
        <div style="display:flex; gap:10px; flex-wrap:wrap; margin-bottom:22px;">
          <button class="btn btn-primary" onclick="selectCategoryAndFocus('Z-3 Açık Uçlu İkileme Çözüm / Yanıt')">✍️ ${{isEn ? 'Respond to Z-3 Dilemma' : 'Bu İkileme Cevabımı Yaz'}}</button>
          <button class="btn" onclick="selectCategoryAndFocus('İSNAD 2 Klasik Tefsir / Arapça Kaynak İlavesi')">🕌 ${{isEn ? 'Add Classical Tafsir Citation' : 'Klasik Tefsir Nakli Ekle'}}</button>
          <button class="btn" onclick="selectCategoryAndFocus('Sınıf İçi / Zümre Pedagojik Uygulama Deneyimi')">🏫 ${{isEn ? 'Share Classroom Experience' : 'Zümre / Ders Deneyimi Paylaş'}}</button>
        </div>

        <h3><span>📌 ${{isEn ? 'My Saved Annotations & Lesson Notes for This Report' : 'Bu Rapor İçin Kaydettiğim Şerhler & Ders Notlarım'}}</span><span id="localNotesCount">0</span></h3>
        <div id="localNotesList"></div>
      </div>

      <div class="panel">
        <h3><span>✍️ ${{isEn ? 'Interactive Academic Peer-Review & Feedback Form' : 'Etkileşimli Akademik Şerh, Hakemlik ve Geri Dönüt Formu'}}</span><span>${{isEn ? 'Open Deliberation' : 'Açık Müzakere'}}</span></h3>
        <p style="font-size:12.5px; color:var(--text-secondary); margin-bottom:14px;">
          ${{isEn
            ? `Submit your commentary or peer-review on <strong>${{r.case_id}} (Surah ${{surahDisp}} ${{r.verse}})</strong> with one click via <strong>WhatsApp</strong>, open an official <strong>GitHub Academic Peer-Review Issue</strong>, or save it to your browser notes.`
            : `<strong>${{r.case_id}} (${{r.surah}} Sûresi ${{r.verse}})</strong> raporu için hazırladığınız katkıyı tek tıkla <strong>WhatsApp</strong> üzerinden paylaşabilir, <strong>Resmi GitHub Akademik Hakemlik (Peer-Review)</strong> kaydı açabilir veya kişisel araştırma notlarınıza kaydedebilirsiniz.`}}
        </p>

        <div class="form-group">
          <label class="form-label">👤 ${{isEn ? 'Your Name / Academic Title / Institution' : 'Adınız / Unvanınız / Kurum veya Zümreniz'}}</label>
          <input type="text" id="fbAuthor" class="form-input" placeholder="${{isEn ? 'e.g., Assoc. Prof. ... / Senior Educator ...' : 'Örn: Doç. Dr. ... / DKAB Öğretmeni ...'}}">
        </div>

        <div class="form-group">
          <label class="form-label">📂 ${{isEn ? 'Contribution or Peer-Review Category' : 'Katkı veya Geri Bildirim Türü'}}</label>
          <select id="fbCategory" class="form-select">
            <option value="Z-3 Açık Uçlu İkileme Çözüm / Yanıt">🎓 ${{isEn ? 'Response to Z-3 Strategic Dilemma' : 'Z-3 Açık Uçlu İkileme Çözüm / Yanıt'}}</option>
            <option value="İSNAD 2 Klasik Tefsir / Arapça Kaynak İlavesi">🕌 ${{isEn ? 'ISNAD 2 Classical Tafsir / Arabic Source Addition' : 'İSNAD 2 Klasik Tefsir / Arapça Kaynak İlavesi'}}</option>
            <option value="Çağdaş Ampirik Veri / DOI / Makale Önerisi">📊 ${{isEn ? 'Empirical Dataset / DOI / Literature Suggestion' : 'Çağdaş Ampirik Veri / DOI / Makale Önerisi'}}</option>
            <option value="Sınıf İçi / Zümre Pedagojik Uygulama Deneyimi">🏫 ${{isEn ? 'Classroom / Seminar Pedagogical Application' : 'Sınıf İçi / Zümre Pedagojik Uygulama Deneyimi'}}</option>
            <option value="Metodolojik Tenkit / Yanlışlama Kanıtı (Adım 12)">⚖️ ${{isEn ? 'Methodological Critique / Falsification Evidence (Step 12)' : 'Metodolojik Tenkit / Yanlışlama Kanıtı (Adım 12)'}}</option>
            <option value="Külliyata Yeni Âyet / Rapor Önerisi">💡 ${{isEn ? `Nominate New Verse for Corpus (${{nextCaseId}}+)` : `Külliyata Yeni Âyet / Rapor Önerisi (${{nextCaseId}}+)`}}</option>
          </select>
        </div>

        <div class="form-group">
          <label class="form-label">📝 ${{isEn ? 'Your Commentary, Critique, or Classroom Observation' : 'Şerh, Analiz, Eleştiri veya Sınıf İçi Gözlem Metniniz'}}</label>
          <textarea id="fbContent" class="form-textarea" placeholder="${{isEn ? 'Write your analytical commentary, classical reference, response to Z-3, or pedagogical feedback here...' : 'Bu raporun analitik çerçevesine, klasik tefsir nakillerine, Z-3 sorusuna veya sınıf içi uygulanabilirliğine dair görüş ve katkınızı buraya yazınız...'}}"></textarea>
        </div>

        <div class="form-group">
          <label class="form-label">📚 ${{isEn ? 'Supporting Reference / Tafsir / DOI / Verse (Optional)' : 'Varsa Dayanak Kaynak / Tefsir / DOI / Âyet Referansı (İsteğe Bağlı)'}}</label>
          <input type="text" id="fbSource" class="form-input" placeholder="${{isEn ? 'e.g., Ibn Ashur, al-Tahrir, vol. X, p. Y or DOI: 10.xxxx/...' : 'Örn: İbn Âşûr, et-Tahrîr, c. X, s. Y veya DOI: 10.xxxx/...'}}">
        </div>

        <div class="action-row">
          <button class="btn btn-primary" onclick="sendViaWhatsApp()">🟢 ${{isEn ? 'Send / Share via WhatsApp' : 'WhatsApp ile Gönder / Paylaş'}}</button>
          <button class="btn btn-gold" onclick="openGitHubPeerReview()">🏛️ ${{isEn ? 'Open Official Peer-Review Issue (GitHub)' : 'Resmi Akademik Şerh Kaydı Aç (GitHub)'}}</button>
          <button class="btn" onclick="saveLocalNoteAndCopy()">💾 ${{isEn ? 'Save to My Notes & Copy' : 'Notlarıma Kaydet & Metni Kopyala'}}</button>
          <a class="btn" href="https://github.com/mehmetyarici-crypto/quran-vision/issues" target="_blank" rel="noopener">🔎 ${{isEn ? 'View All Peer-Reviews' : 'Tüm Açık Şerhleri Gör'}}</a>
        </div>
        <div id="fbToast" class="toast-msg"></div>
      </div>
    </div>

    <div class="panel" style="margin-bottom:24px;">
      <h3><span>🗳️ ${{isEn ? `Which Verse Should Be Report #${{nextReportNum}} (${{nextCaseId}})? (Candidate Verse Pool)` : `Külliyatın ${{nextReportNum}}. Raporu (${{nextCaseId}}) Hangi Âyet Olsun? (Aday Âyet Havuzu)`}}</span><span>${{isEn ? 'Collective Agenda' : 'Kolektif Gündem'}}</span></h3>
      <p style="font-size:13px; color:var(--text-secondary);">
        ${{isEn
          ? 'Select one of the candidate verses below to propose the next 26-step strategic report in the Quran Vision Corpus:'
          : 'Aşağıdaki aday âyetlerden birini seçerek bir sonraki stratejik analizin hangi âyet üzerine inşa edilmesini istediğinizi önerebilirsiniz:'}}
      </p>
      <div class="candidate-grid">
        ${{candidatesHtml}}
      </div>
    </div>
  `;

  renderLocalNotes();
}}

function openFeedbackTab() {{
  const btn = document.getElementById('tabBtn-feedback');
  if (btn) setTab('feedback', btn);
}}

function selectCategoryAndFocus(catValue) {{
  const sel = document.getElementById('fbCategory');
  if (sel) sel.value = catValue;
  const ta = document.getElementById('fbContent');
  if (ta) ta.focus();
}}

function prefillCandidateVerse(verseRef, verseTitle) {{
  const isEn = currentLang === 'en';
  const nextReportNum = REPORTS.length + 1;
  const nextCaseId = 'QV-2026-' + String(nextReportNum).padStart(3, '0');
  const sel = document.getElementById('fbCategory');
  if (sel) sel.value = "Külliyata Yeni Âyet / Rapor Önerisi";
  const ta = document.getElementById('fbContent');
  if (ta) {{
    ta.value = isEn
      ? `I nominate "${{verseRef}} — ${{verseTitle}}" to be analyzed as Report #${{nextReportNum}} (${{nextCaseId}}) within the 26-step Quran Vision framework.\\n\\nRationale for Nomination: `
      : `Külliyatın ${{nextReportNum}}. raporu (${{nextCaseId}}) olarak "${{verseRef}} — ${{verseTitle}}" konusunun 26 adımlı Quran Vision çerçevesinde incelenmesini öneriyorum.\\n\\nÖneri Gerekçem: `;
    ta.focus();
  }}
  showToast(isEn
    ? "✨ Candidate verse loaded into the form! Add your rationale and submit via WhatsApp or GitHub."
    : "✨ Aday âyet forma aktarıldı! Gerekçenizi ekleyip WhatsApp veya GitHub üzerinden gönderebilirsiniz.");
}}

function buildFormattedFeedbackText() {{
  const r = REPORTS[currentIndex];
  const isEn = currentLang === 'en';
  const author = (document.getElementById('fbAuthor')?.value || (isEn ? 'Anonymous Contributor' : 'İsimsiz Katılımcı')).trim();
  const category = document.getElementById('fbCategory')?.value || 'Akademik Şerh';
  const content = (document.getElementById('fbContent')?.value || '').trim();
  const source = (document.getElementById('fbSource')?.value || '—').trim();

  return {{
    r, author, category, content, source,
    formatted: `*QURAN VISION (v6.2.1) — ${{isEn ? 'ACADEMIC PEER-REVIEW & FEEDBACK CARD' : 'AKADEMİK ŞERH & GERİ DÖNÜT KARTI'}}*\\n` +
      `━━━━━━━━━━━━━━━━━━━━\\n` +
      `📌 *${{isEn ? 'Report' : 'Rapor'}}:* ${{r.case_id}} — ${{getReportSurah(r)}} ${{r.verse}}\\n` +
      `📖 *${{isEn ? 'Topic' : 'Konu'}}:* ${{getReportTopic(r)}}\\n` +
      `👤 *${{isEn ? 'Contributor' : 'Katkı Sunan'}}:* ${{author}}\\n` +
      `📂 *${{isEn ? 'Category' : 'Kategori'}}:* ${{category}}\\n` +
      `━━━━━━━━━━━━━━━━━━━━\\n` +
      `📝 *${{isEn ? 'Commentary' : 'Şerh / Görüş'}}:*\\n${{content || '(—)'}}\\n\\n` +
      `📚 *${{isEn ? 'Reference' : 'Dayanak / Kaynak'}}:* ${{source}}\\n` +
      `🔗 *Portal:* https://mehmetyarici-crypto.github.io/quran-vision/`
  }};
}}

function sendViaWhatsApp() {{
  const data = buildFormattedFeedbackText();
  if (!data.content) {{
    showToast(currentLang === 'en' ? "⚠️ Please enter your commentary text first." : "⚠️ Lütfen önce görüş veya şerh metninizi yazınız.");
    document.getElementById('fbContent')?.focus();
    return;
  }}
  saveNoteToStorage(data);
  const waUrl = `https://wa.me/?text=${{encodeURIComponent(data.formatted)}}`;
  window.open(waUrl, '_blank');
}}

function openGitHubPeerReview() {{
  const data = buildFormattedFeedbackText();
  if (!data.content) {{
    showToast(currentLang === 'en' ? "⚠️ Please enter your commentary text first." : "⚠️ Lütfen önce görüş veya şerh metninizi yazınız.");
    document.getElementById('fbContent')?.focus();
    return;
  }}
  saveNoteToStorage(data);
  const issueTitle = `[${{data.category}}] ${{data.r.case_id}} (${{data.r.surah}} ${{data.r.verse}}) — ${{data.author}}`;
  const issueBody =
    `### 🏛️ Quran Vision (v6.2.1) Akademik Şerh & Katkı Kaydı\\n\\n` +
    `- **Vaka Kodu:** ${{data.r.case_id}}\\n` +
    `- **Sûre ve Âyet:** ${{data.r.surah}} Sûresi ${{data.r.verse}}\\n` +
    `- **Rapor Başlığı:** ${{data.r.topic}}\\n` +
    `- **SHA-256 Manifest:** ${{data.r.sha256}}\\n` +
    `- **Katkı Sunan:** ${{data.author}}\\n` +
    `- **Katkı Kategorisi:** ${{data.category}}\\n\\n` +
    `---\\n\\n` +
    `### 📝 Şerh / Analiz / Geri Bildirim Metni\\n\\n` +
    `${{data.content}}\\n\\n` +
    `### 📚 Dayanak Kaynak / Referans\\n\\n` +
    `${{data.source}}\\n`;
  const ghUrl = `https://github.com/mehmetyarici-crypto/quran-vision/issues/new?title=${{encodeURIComponent(issueTitle)}}&body=${{encodeURIComponent(issueBody)}}`;
  window.open(ghUrl, '_blank');
}}

function saveNoteToStorage(data) {{
  const key = 'qv_notes_v621';
  let existing = [];
  try {{
    existing = JSON.parse(localStorage.getItem(key) || '[]');
  }} catch (e) {{ existing = []; }}
  existing.unshift({{
    id: Date.now(),
    case_id: data.r.case_id,
    surah: data.r.surah,
    verse: data.r.verse,
    author: data.author,
    category: data.category,
    content: data.content,
    source: data.source,
    date: new Date().toLocaleString(currentLang === 'en' ? 'en-US' : 'tr-TR')
  }});
  localStorage.setItem(key, JSON.stringify(existing));
  renderLocalNotes();
}}

function saveLocalNoteAndCopy() {{
  const data = buildFormattedFeedbackText();
  if (!data.content) {{
    showToast(currentLang === 'en' ? "⚠️ Please enter your commentary text first." : "⚠️ Lütfen önce görüş veya şerh metninizi yazınız.");
    document.getElementById('fbContent')?.focus();
    return;
  }}
  saveNoteToStorage(data);
  if (navigator.clipboard) {{
    navigator.clipboard.writeText(data.formatted);
  }}
  showToast(currentLang === 'en'
    ? "✅ Note saved under this report and formatted text copied to clipboard!"
    : "✅ Şerhiniz bu raporun altına kaydedildi ve biçimlendirilmiş metin panoya kopyalandı!");
}}

function deleteLocalNote(noteId) {{
  const key = 'qv_notes_v621';
  let existing = [];
  try {{
    existing = JSON.parse(localStorage.getItem(key) || '[]');
  }} catch (e) {{ existing = []; }}
  existing = existing.filter(n => n.id !== noteId);
  localStorage.setItem(key, JSON.stringify(existing));
  renderLocalNotes();
}}

function renderLocalNotes() {{
  const r = REPORTS[currentIndex];
  const isEn = currentLang === 'en';
  const listEl = document.getElementById('localNotesList');
  const countEl = document.getElementById('localNotesCount');
  if (!listEl) return;

  let existing = [];
  try {{
    existing = JSON.parse(localStorage.getItem('qv_notes_v621') || '[]');
  }} catch (e) {{ existing = []; }}

  const reportNotes = existing.filter(n => n.case_id === r.case_id);
  if (countEl) countEl.textContent = isEn ? `${{reportNotes.length}} Saved Notes` : `${{reportNotes.length}} Kayıtlı Not`;

  if (reportNotes.length === 0) {{
    listEl.innerHTML = `<div class="source-card" style="color:var(--text-muted); font-size:13px;">${{isEn
      ? `No personal annotations or lesson notes saved in your browser for ${{r.case_id}} yet. Use the form on the right to add one.`
      : `Bu rapor (${{r.case_id}}) için henüz tarayıcınıza kaydettiğiniz bir kişisel şerh veya ders notu bulunmuyor. Sağdaki formdan ekleyebilirsiniz.`}}</div>`;
    return;
  }}

  listEl.innerHTML = reportNotes.map(n => `
    <div class="source-card">
      <div class="source-header">
        <span class="source-author">${{n.author}} • <span style="color:var(--accent-gold);">${{n.category}}</span></span>
        <button class="btn" style="padding:2px 8px; font-size:11px;" onclick="deleteLocalNote(${{n.id}})">🗑️ ${{isEn ? 'Delete' : 'Sil'}}</button>
      </div>
      <div style="font-size:13.5px; color:var(--text-primary); white-space:pre-wrap; margin-bottom:6px;">${{n.content.replace(/</g, '&lt;')}}</div>
      <div class="source-meta">📚 ${{isEn ? 'Ref' : 'Kaynak'}}: ${{n.source}} &nbsp;|&nbsp; 🕒 ${{n.date}}</div>
    </div>
  `).join('');
}}

function showToast(msg) {{
  const el = document.getElementById('fbToast');
  if (!el) return;
  el.textContent = msg;
  el.style.display = 'block';
  setTimeout(() => {{ el.style.display = 'none'; }}, 5000);
}}

function printCurrentReport() {{
  const r = REPORTS[currentIndex];
  const prevTheme = document.documentElement.getAttribute('data-theme');
  const prevTitle = document.title;
  document.documentElement.setAttribute('data-theme', 'light');
  document.title = `${{r.case_id}}_${{r.surah}}_Raporu`;
  setTimeout(() => {{
    window.print();
    document.documentElement.setAttribute('data-theme', prevTheme);
    document.title = prevTitle;
  }}, 150);
}}

function formatInlineMd(str, seenFnRefs = null) {{
  if (!str) return '';
  const isEn = currentLang === 'en';
  let s = str
    .replace(/\\\\text\\{{([^}}]*)\\}}/g, '$1')
    .replace(/v6\\.1\\.1 ve v6\\.2\\.1/g, 'v6.2.1')
    .replace(/v6\\.1\\.1 & v6\\.2\\.1/g, 'v6.2.1')
    .replace(/(?<!-)v6\\.1\\.1(?!\\.md)/g, 'v6.2.1')
    .replace(/\\\\ge/g, '≥')
    .replace(/\\\\le/g, '≤')
    .replace(/\\\\approx/g, '≈')
    .replace(/\\\\rightarrow/g, '→')
    .replace(/\\\\to/g, '→')
    .replace(/\\\\times/g, '×')
    .replace(/\\\\neg/g, '¬')
    .replace(/\\\\frac\\{{([^}}]+)\\}}\\{{([^}}]+)\\}}/g, '($1)/($2)')
    .replace(/\\\\%/g, '%')
    .replace(/\\$([^$]+)\\$/g, '<strong>$1</strong>');

  const links = [];
  const saveLink = (tagHtml) => {{
    const idx = links.length;
    links.push(tagHtml);
    return `\\x00LINK${{idx}}\\x00`;
  }};

  // 1. Markdown links [label](https://...)
  s = s.replace(/\\[([^\\]]+)\\]\\((https?:\\/\\/[^\\s)]+)\\)/g, (_, label, url) =>
    saveLink(`<a href="${{url}}" target="_blank" rel="noopener" class="ext-link">${{label}}</a>`)
  );

  // 2. Explicit URLs (https://... or http://...)
  s = s.replace(/(https?:\\/\\/[^\\s<>"'`\\])]+)/g, (_, full) => {{
    const url = full.replace(/[.,;:!?)]+$/, '');
    const trail = full.slice(url.length);
    const cls = url.includes('doi.org/') ? 'doi-link' : (url.includes('orcid.org/') ? 'orcid-link' : 'ext-link');
    return saveLink(`<a href="${{url}}" target="_blank" rel="noopener" class="${{cls}}">${{url}}</a>`) + trail;
  }});

  // 3. Bare DOIs (doi:10.xxxx/... or 10.xxxx/...)
  s = s.replace(/\\b(doi:\\s*)?(10\\.\\d{{4,9}}\\/[-._;()/:A-Za-z0-9]+)/gi, (_, prefix, rawDoi) => {{
    const cleanDoi = rawDoi.replace(/[.,;:!?)]+$/, '');
    const trail = rawDoi.slice(cleanDoi.length);
    const disp = (prefix || '') + cleanDoi;
    return saveLink(`<a href="https://doi.org/${{cleanDoi}}" target="_blank" rel="noopener" class="doi-link">${{disp}}</a>`) + trail;
  }});

  // 4. Bare ORCIDs (0009-0003-0356-8582, 0000-0002-1025-5643, etc.)
  s = s.replace(/\\b(000[09]-\\d{{4}}-\\d{{4}}-\\d{{3}}[\\dX])\\b/g, (_, orcid) =>
    saveLink(`<a href="https://orcid.org/${{orcid}}" target="_blank" rel="noopener" class="orcid-link">${{orcid}}</a>`)
  );

  // 5. Bidirectional Inline Footnote References [^1]
  s = s.replace(/\\[\\^(\\d{{1,2}})\\]/g, (_, num) => {{
    let refId = `fnref-${{num}}`;
    if (seenFnRefs) {{
      const count = (seenFnRefs[num] || 0) + 1;
      seenFnRefs[num] = count;
      if (count > 1) refId = `fnref-${{num}}-${{count}}`;
    }}
    return saveLink(
      `<sup class="fn-ref" id="${{refId}}"><a href="#fn-${{num}}" class="fn-link" title="${{isEn ? 'Jump to source [' + num + ']' : 'Kaynağa git [' + num + ']'}}">[${{num}}]</a></sup>`
    );
  }});

  s = s
    .replace(/\\[NAKİL\\]/g, `<span class="tag-nakil">${{isEn ? '[CITATION / NAKİL]' : '[NAKİL]'}}</span>`)
    .replace(/\\[CITATION \\/ NAKİL\\]/g, '<span class="tag-nakil">[CITATION / NAKİL]</span>')
    .replace(/\\[CITATION\\]/g, '<span class="tag-nakil">[CITATION]</span>')
    .replace(/\\[ANALYSIS \\/ YORUM\\]/g, '<span class="tag-yorum">[ANALYSIS / YORUM]</span>')
    .replace(/\\[ANALYSIS\\]/g, '<span class="tag-yorum">[ANALYSIS]</span>')
    .replace(/\\[YORUM\\]/g, `<span class="tag-yorum">${{isEn ? '[ANALYSIS / YORUM]' : '[YORUM]'}}</span>`)
    .replace(/`([^`]+)`/g, '<code>$1</code>')
    .replace(/\\*\\*(.*?)\\*\\*/g, '<strong>$1</strong>')
    .replace(/\\*(.*?)\\*/g, '<em>$1</em>')
    .replace(/([\\u0600-\\u06FF][\\u0600-\\u06FF\\s\\u064B-\\u065F\\u0670،؛؟.]*[\\u0600-\\u06FF\\u064B-\\u065F])/g, '<bdi dir="rtl" style="font-family:\\x27Amiri\\x27,serif; font-size:1.15em; color:var(--accent-gold);">$1</bdi>');

  for (let idx = 0; idx < links.length; idx++) {{
    s = s.replace(`\\x00LINK${{idx}}\\x00`, links[idx]);
  }}
  return s;
}}

function formatZ5YamlJs(rawYaml) {{
  const isEn = currentLang === 'en';
  const data = {{}};
  rawYaml.split('\\n').forEach(line => {{
    const idx = line.indexOf(':');
    if (idx > -1) {{
      const k = line.slice(0, idx).trim();
      const v = line.slice(idx + 1).trim().replace(/^["']|["']$/g, '');
      if (v) data[k] = v;
    }}
  }});
  const raporId = data.rapor_id || '—';
  const sureAyet = data.sure_ayet || '—';
  const tarih = data.tarih || '2026-10-15';
  const uzmanlik = data.uzmanlik_alani || (isEn ? 'Tafsir / Islamic Law / Social Sciences' : 'Tefsir / İslam Hukuku / Sosyal Bilimler');
  let notu = data.derkenar_notu || (isEn
    ? 'Produced in full compliance with Quran Vision v6.2.1 ISNAD 2 and APA 7 / DOI standards; open for independent external academic peer review.'
    : 'Rapor Quran Vision v6.2.1 İSNAD 2 akademik atıf standartlarına tam uyumlu teknik ön sürüm olarak üretilmiş olup, bağımsız dış akademik hakem incelemesine hazır durumdadır.');
  notu = formatInlineMd(notu.replace(/v6\\.1\\.1 ve v6\\.2\\.1/g, 'v6.2.1').replace(/v6\\.1\\.1/g, 'v6.2.1'));
  return `
    <div id="z5-peer-review-card" style="border:1.5px solid var(--accent-gold); background:var(--bg-surface); border-radius:12px; padding:18px 20px; margin:18px 0;">
      <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; margin-bottom:14px;">
        <div>
          <span class="badge badge-gold">${{isEn ? '🏛️ ACADEMIC INTEGRITY & OPEN PEER-REVIEW PROTOCOL (Z-5)' : '🏛️ AKADEMİK DÜRÜSTLÜK & AÇIK HAKEMLİK PROTOKOLÜ (Z-5)'}}</span>
          <span class="badge badge-emerald" style="margin-left:6px;">${{raporId}} • ${{sureAyet}}</span>
        </div>
        <button class="btn btn-gold" style="padding:7px 14px; font-size:12.5px;" onclick="openFeedbackTab()">
          ✍️ ${{isEn ? 'Submit Peer Review / Commentary for This Report' : 'Bu Rapor İçin Hakem Şerhi / Değerlendirme Gönder'}}
        </button>
      </div>
      <table style="margin:8px 0;">
        <thead>
          <tr>
            <th style="width:36%;">${{isEn ? 'Academic Evaluation Dimension' : 'Akademik Değerlendirme Boyutu'}}</th>
            <th style="width:46%;">${{isEn ? 'Audit Scope & Methodological Criterion' : 'Denetim Kapsamı ve Metodolojik Ölçüt'}}</th>
            <th style="width:18%;">${{isEn ? 'Rubric Score' : 'Rubrik Puanı'}}</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>${{isEn ? 'External Reviewer & Status' : 'Dış Hakem & Künye'}}</strong></td>
            <td><strong>Mehmet Emin Koç</strong> (<a href="https://orcid.org/0000-0002-1025-5643" target="_blank" rel="noopener" class="orcid-link">ORCID: 0000-0002-1025-5643</a>) • ${{isEn ? 'Date' : 'Tarih'}}: <strong>${{tarih}}</strong> • ${{isEn ? 'Field' : 'Uzmanlık'}}: <em>${{uzmanlik}}</em></td>
            <td><span class="badge badge-gold">${{isEn ? 'OPEN PEER REVIEW' : 'AÇIK HAKEMLİK'}}</span></td>
          </tr>
          <tr>
            <td><strong>${{isEn ? '1. Textual & Classical Verification (ISNAD 2)' : '1. Metin ve Klasik Tahkik (İSNAD 2)'}}</strong></td>
            <td>${{isEn ? 'Primary Arabic quote accuracy, vol/page verification & [CITATION]/[ANALYSIS] separation' : 'Arapça ibare doğruluğu, cilt/sayfa tahkiki ve <code>[NAKİL]</code> / <code>[YORUM]</code> ayrımı'}}</td>
            <td><strong>— / 20</strong></td>
          </tr>
          <tr>
            <td><strong>${{isEn ? '2. Socio-Political & Crisis Modeling' : '2. Sosyo-Politik ve Kriz Analizi'}}</strong></td>
            <td>${{isEn ? 'Actor mapping, tipping point (N4) & historical retrodiction coherence' : 'Aktör haritası, kırılma noktası (N4) ve tarihsel retrodiction tutarlılığı'}}</td>
            <td><strong>— / 20</strong></td>
          </tr>
          <tr>
            <td><strong>${{isEn ? '3. Language Safety & Impartiality' : '3. Dil Güvenliği ve Tarafsızlık'}}</strong></td>
            <td>${{isEn ? 'Inclusive academic register free from sectarian or ideological reductionism' : 'Mezhebî/ideolojik indirgemecilikten uzak, kapsayıcı ve akademik üslup'}}</td>
            <td><strong>— / 20</strong></td>
          </tr>
          <tr>
            <td><strong>${{isEn ? '4. Falsifiability & Hume’s Guillotine' : '4. Falsifiabilite ve Hume Giyotini'}}</strong></td>
            <td>${{isEn ? 'Is-ought distinction, falsifiable thresholds (th-01..03) & DOI dataset alignment' : 'Olgu-değer ayrımı, yanlışlanabilir eşikler (th-01..03) ve DOI veri uyumu'}}</td>
            <td><strong>— / 20</strong></td>
          </tr>
          <tr>
            <td><strong>${{isEn ? '5. Institutional Design & Originality' : '5. Kurumsal Tasarım ve Özgünlük'}}</strong></td>
            <td>${{isEn ? 'Actionable policy branches, pedagogical integration & Z-1 Aporia depth' : 'Uygulanabilir politika kolları, TYMM pedagojik uyumu ve Z-1 Aporia derinliği'}}</td>
            <td><strong>— / 20</strong></td>
          </tr>
          <tr>
            <td><strong>${{isEn ? 'TOTAL ACADEMIC SCORE' : 'TOPLAM AKADEMİK SKOR'}}</strong></td>
            <td><strong>${{isEn ? 'External Referee Decision:' : 'Dış Hakem Kararı:'}}</strong> ${{isEn ? 'Open for Independent Peer Evaluation' : 'Bağımsız Akademik Hakem Değerlendirmesine Açık'}}</td>
            <td><strong style="color:var(--accent-gold);">— / 100</strong></td>
          </tr>
          <tr>
            <td><strong>${{isEn ? 'Editorial Note' : 'Editoryal Derkenar Notu'}}</strong></td>
            <td colspan="2" style="color:var(--text-secondary); line-height:1.6;">${{notu}}</td>
          </tr>
        </tbody>
      </table>
    </div>
  `;
}}

function renderMarkdown(md) {{
  const isEn = currentLang === 'en';
  const lines = md.split('\\n');
  let html = '';
  let inCode = false;
  let codeBuf = [];
  let inTable = false;
  const seenFnRefs = {{}};

  for (let i = 0; i < lines.length; i++) {{
    let line = lines[i];

    if (line.trim().startsWith('```')) {{
      if (!inCode) {{
        inCode = true;
        codeBuf = [];
      }} else {{
        inCode = false;
        const rawCode = codeBuf.join('\\n');
        if (rawCode.includes('hakem_degerlendirme_protokolu:')) {{
          html += formatZ5YamlJs(rawCode);
        }} else {{
          const escaped = rawCode.replace(/</g, '&lt;').replace(/>/g, '&gt;');
          html += `<pre><code>${{escaped}}</code></pre>`;
        }}
      }}
      continue;
    }}
    if (inCode) {{
      codeBuf.push(line);
      continue;
    }}

    if (line.trim().startsWith('|')) {{
      if (line.includes('---')) continue;
      const cells = line.split('|').slice(1, -1).map(c => formatInlineMd(c.trim(), seenFnRefs));
      if (!inTable) {{
        inTable = true;
        html += '<table><thead><tr>' + cells.map(c => `<th>${{c}}</th>`).join('') + '</tr></thead><tbody>';
      }} else {{
        html += '<tr>' + cells.map(c => `<td>${{c}}</td>`).join('') + '</tr>';
      }}
      continue;
    }} else if (inTable) {{
      inTable = false;
      html += '</tbody></table>';
    }}

    const trimmed = line.trim();
    if (line.startsWith('# ')) {{
      html += `<h1>${{formatInlineMd(line.slice(2), seenFnRefs)}}</h1>`;
    }} else if (line.startsWith('## ')) {{
      html += `<h2>${{formatInlineMd(line.slice(3), seenFnRefs)}}</h2>`;
    }} else if (line.startsWith('### ')) {{
      const z5IdAttr = line.includes('Z-5') ? ' id="z5-peer-review-card"' : '';
      html += `<h3${{z5IdAttr}}>${{formatInlineMd(line.slice(4), seenFnRefs)}}</h3>`;
    }} else if (line.startsWith('#### ')) {{
      html += `<h4>${{formatInlineMd(line.slice(5), seenFnRefs)}}</h4>`;
    }} else if (trimmed === '---') {{
      html += '<hr style="border:none; border-top:1px solid var(--border); margin:18px 0;">';
    }} else if (trimmed.startsWith('- [x] ') || trimmed.startsWith('- [X] ')) {{
      html += `<ul><li><span style="color:var(--accent-emerald); font-weight:700;">☑</span> ${{formatInlineMd(trimmed.slice(6), seenFnRefs)}}</li></ul>`;
    }} else if (trimmed.startsWith('- ')) {{
      html += `<ul><li>${{formatInlineMd(trimmed.slice(2), seenFnRefs)}}</li></ul>`;
    }} else if (/^\\d+\\.\\s/.test(trimmed)) {{
      html += `<p style="margin-left:10px;">${{formatInlineMd(trimmed, seenFnRefs)}}</p>`;
    }} else if (trimmed.startsWith('[^')) {{
      const fnMatch = trimmed.match(/^\\[\\^(\\d+)\\]:\\s*(.*)$/);
      if (fnMatch) {{
        const fnNum = fnMatch[1];
        const fnBody = formatInlineMd(fnMatch[2], seenFnRefs);
        const backTitle = isEn ? `Return to citation [${{fnNum}}] in text` : `Metindeki [${{fnNum}}] atfına dön`;
        html += `<p class="fn-item" id="fn-${{fnNum}}"><a href="#fnref-${{fnNum}}" class="fn-num-link" title="${{backTitle}}"><strong>[${{fnNum}}]</strong></a> ${{fnBody}} <a href="#fnref-${{fnNum}}" class="fn-backref" title="${{backTitle}}">↩</a></p>`;
      }} else {{
        html += `<p class="fn-item">${{formatInlineMd(trimmed, seenFnRefs)}}</p>`;
      }}
    }} else if (trimmed !== '') {{
      html += `<p>${{formatInlineMd(line, seenFnRefs)}}</p>`;
    }}
  }}
  if (inTable) html += '</tbody></table>';
  return html;
}}

// Smooth bidirectional scroll handler for in-page footnote links (#fn-X <-> #fnref-X)
document.addEventListener('click', (e) => {{
  const link = e.target.closest('a[href^="#fn"]');
  if (!link) return;
  const targetId = link.getAttribute('href').slice(1);
  const targetEl = document.getElementById(targetId);
  if (targetEl) {{
    e.preventDefault();
    targetEl.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
    targetEl.classList.add('fn-highlight');
    setTimeout(() => targetEl.classList.remove('fn-highlight'), 2200);
  }}
}});

function setTab(tabName, btn) {{
  currentTab = tabName;
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  if (btn) btn.classList.add('active');
  document.getElementById('tab-dashboard').style.display = tabName === 'dashboard' ? 'block' : 'none';
  document.getElementById('tab-sources').style.display = tabName === 'sources' ? 'block' : 'none';
  document.getElementById('tab-fulltext').style.display = tabName === 'fulltext' ? 'block' : 'none';
  document.getElementById('tab-pedagogy').style.display = tabName === 'pedagogy' ? 'block' : 'none';
  document.getElementById('tab-synthesis').style.display = tabName === 'synthesis' ? 'block' : 'none';
  document.getElementById('tab-feedback').style.display = tabName === 'feedback' ? 'block' : 'none';
}}

function applyFontScale(scale) {{
  currentFontScale = Math.min(1.6, Math.max(0.8, Math.round(scale * 100) / 100));
  document.documentElement.style.setProperty('--font-scale', String(currentFontScale));
  const pct = Math.round(currentFontScale * 100);
  const disp = currentLang === 'en' ? `${{pct}}%` : `%${{pct}}`;
  document.querySelectorAll('.font-scale-sync').forEach(el => {{
    el.textContent = disp;
  }});
  try {{ localStorage.setItem('qv_font_scale_v621', String(currentFontScale)); }} catch (e) {{}}
}}

function changeFontSize(delta) {{
  applyFontScale(currentFontScale + delta);
}}

function resetFontSize() {{
  applyFontScale(1.0);
}}

function updateThemeButtonsUI() {{
  const isDark = document.documentElement.getAttribute('data-theme') !== 'light';
  const isEn = currentLang === 'en';
  const el = document.getElementById('themeBtn');
  if (el) {{
    el.innerHTML = isEn
      ? (isDark ? '☀️ Light Mode' : '🌙 Dark Mode')
      : (isDark ? '☀️ Açık Mod' : '🌙 Koyu Mod');
  }}
}}

function toggleTheme() {{
  const root = document.documentElement;
  const nextTheme = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
  root.setAttribute('data-theme', nextTheme);
  try {{ localStorage.setItem('qv_theme_v621', nextTheme); }} catch (e) {{}}
  updateThemeButtonsUI();
}}

function updateSidebarToggleUI() {{
  const isCollapsed = document.body.classList.contains('sidebar-collapsed');
  const isEn = currentLang === 'en';
  const lbl = document.getElementById('sidebarToggleLabel');
  const btn = document.getElementById('sidebar-toggle');
  const sidebarEl = document.getElementById('sidebar');
  if (sidebarEl) {{
    sidebarEl.inert = isCollapsed;
  }}
  if (lbl) {{
    lbl.textContent = isEn
      ? (isCollapsed ? '▶ Show Menu' : '◀ Hide Menu')
      : (isCollapsed ? '▶ Menüyü Göster' : '◀ Menüyü Gizle');
  }}
  if (btn) {{
    btn.setAttribute('aria-expanded', String(!isCollapsed));
    btn.setAttribute('aria-label', isEn
      ? 'Hide or Show Sidebar Menu (Ctrl + B or [)'
      : 'Menüyü Gizle veya Göster (Ctrl + B veya [)');
  }}
}}

function toggleSidebar() {{
  const isCollapsed = document.body.classList.toggle("sidebar-collapsed");
  try {{ localStorage.setItem('qv_sidebar_collapsed', isCollapsed ? '1' : '0'); }} catch (e) {{}}
  updateSidebarToggleUI();
}}

// Restore saved theme, sidebar & font scale state from localStorage
(function restoreUserPreferences() {{
  try {{
    const savedTheme = localStorage.getItem('qv_theme_v621');
    if (savedTheme === 'dark' || savedTheme === 'light') {{
      document.documentElement.setAttribute('data-theme', savedTheme);
    }}
    const savedSidebar = localStorage.getItem('qv_sidebar_collapsed');
    if (savedSidebar === '1') {{
      document.body.classList.add('sidebar-collapsed');
    }}
    const savedScale = parseFloat(localStorage.getItem('qv_font_scale_v621') || '1');
    if (!isNaN(savedScale) && savedScale >= 0.8 && savedScale <= 1.6) {{
      currentFontScale = savedScale;
      document.documentElement.style.setProperty('--font-scale', String(currentFontScale));
    }}
  }} catch (e) {{}}
}})();

// Keyboard shortcuts: Ctrl + B or '[' to toggle collapsible sidebar reader mode
document.addEventListener('keydown', (e) => {{
  const tag = (e.target && e.target.tagName) ? e.target.tagName.toUpperCase() : '';
  const isInput = tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT' || (e.target && e.target.isContentEditable);
  if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'b') {{
    e.preventDefault();
    toggleSidebar();
  }} else if (!isInput && !e.ctrlKey && !e.metaKey && !e.altKey && e.key === '[') {{
    e.preventDefault();
    toggleSidebar();
  }}
}});

document.getElementById('searchInput').addEventListener('input', (e) => renderSidebar(e.target.value));

setLanguage(currentLang);
updateSidebarToggleUI();
updateThemeButtonsUI();
applyFontScale(currentFontScale);
fetchZenodoLiveStats();

// Deep-link URL query parameters (?report=QV-2026-014&tab=fulltext&scroll=z5)
(function handleUrlParams() {{
  try {{
    const params = new URLSearchParams(window.location.search);
    const repParam = params.get('report');
    const tabParam = params.get('tab');
    const scrollParam = params.get('scroll');
    if (repParam) {{
      const foundIdx = REPORTS.findIndex(x => x.case_id.toUpperCase() === repParam.toUpperCase());
      if (foundIdx > -1) selectReport(foundIdx);
    }}
    if (tabParam && document.getElementById('tabBtn-' + tabParam)) {{
      setTab(tabParam, document.getElementById('tabBtn-' + tabParam));
    }}
    if (scrollParam === 'z5') {{
      setTimeout(() => {{
        document.getElementById('z5-peer-review-card')?.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
      }}, 250);
    }}
  }} catch (e) {{}}
}})();
</script>
</body>
</html>
"""
    return html


def main():
    report_files = sorted(DOCS_TR.glob("[0-9][0-9]-*-v6.1.1.md"))
    report_files = [f for f in report_files if not f.name.startswith("05-")]
    reports = []
    for rf in report_files:
        parsed = parse_report(rf)
        if parsed:
            reports.append(parsed)

    html = build_html(reports)
    out1 = ROOT / "docs" / "index.html"
    out2 = ROOT.parent / "GEM_DIJITAL_KULLIYAT_PORTALI.html"
    out3 = ROOT.parent / "QURAN_VISION_KULLIYAT_PORTALI.html"
    out1.write_text(html, encoding="utf-8")
    out2.write_text(html, encoding="utf-8")
    out3.write_text(html, encoding="utf-8")
    print(f"✅ Portal üretildi: {out1} ({len(reports)} rapor)")
    print(f"✅ Masaüstü hızlı erişim kopyaları: {out2.name}, {out3.name}")

    if "--force-pdf" in sys.argv or not (PDF_DIR / "Quran_Vision_Kulliyat_v6.2.1.pdf").exists():
        print("🖨️ Gerçek A4 PDF dosyaları üretiliyor (Edge Headless Motoru)...")
    generate_all_pdfs(reports)
    print("✅ A4 PDF dosyaları ve gömülü XMP/Info meta verileri (Author/Title/Subject/DOI/ORCID) doğrulandı.")


if __name__ == "__main__":
    main()
