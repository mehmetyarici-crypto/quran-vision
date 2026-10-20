#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GEM Linter v6.1.1 — Pytest Test Paketi
"""

import os
import sys
import tempfile
import subprocess
from pathlib import Path
import pytest

# src dizinini sys.path'e ekle
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR / "src"))

from gem_lint import (
    GemLinterV6,
    normalize,
    citirnak_muaf_mi,
    BLOCK,
    WARN,
    generate_manifest,
    check_cross_similarity,
)

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"


class TestGemLintNormalization:
    def test_normalize_turkish(self):
        assert normalize("İbn Fâris") == "ibn faris"
        assert normalize("Şâtıbî") == "satibi"
        assert normalize("Lisânü'l-Arab") == "lisanul-arab"

    def test_quote_exemption(self):
        # Tırnak içi muaf olmalı (18.1-B)
        line = 'Bu metinde "kesinlikle" kelimesi alıntı olarak geçmektedir.'
        assert citirnak_muaf_mi(line, "kesinlikle") is True

        # Tırnak dışı muaf olmamalı
        line2 = "Bu sonuç kesinlikle kanıtlanmıştır."
        assert citirnak_muaf_mi(line2, "kesinlikle") is False


class TestGemLinterRules:
    def test_valid_fixture(self):
        valid_file = FIXTURES_DIR / "valid_v611.md"
        assert valid_file.exists()

        linter = GemLinterV6(valid_file, katman=3, h6=True)
        code = linter.run_all()

        # Kesici hata (BLOCK) olmamalı
        block_findings = [f for f in linter.findings if f["level"] == BLOCK]
        assert len(block_findings) == 0, f"Beklenmeyen BLOCK hataları: {block_findings}"
        # Ön sürüm olduğu için çıkış kodu 1 (WARN) veya 0 (PASS) olmalı
        assert code in [0, 1]

    def test_forbidden_words_detected(self):
        invalid_file = FIXTURES_DIR / "invalid_forbidden.md"
        assert invalid_file.exists()

        linter = GemLinterV6(invalid_file, katman=3, h6=False)
        code = linter.run_all()

        assert code == 2  # Hard fail / BLOCK
        block_findings = [f for f in linter.findings if f["level"] == BLOCK]
        assert len(block_findings) > 0

        # Hem Türkçe hem İngilizce yasaklı kelimeler yakalanmalı
        messages = " ".join(f["message"] for f in block_findings)
        assert "kesinlikle" in messages
        assert "flawless" in messages
        assert "%100" in messages or "ispatlanmıştır" in messages

    def test_contextual_exception_for_absolute(self):
        # 'absolute path' ve 'mutlak nass' uyarı veya blok üretmemeli
        text = """---
gem_version: "6.1.1"
status: "PRE-RELEASE"
---
Bu koddaki absolute path ifadesi teknik bir yoldur.
Ayrıca mutlak nass çerçevesinde değerlendirilmiştir.
"""
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".md", delete=False) as f:
            f.write(text)
            temp_path = Path(f.name)

        try:
            linter = GemLinterV6(temp_path, katman=1, h6=False)
            linter.load_file()
            linter.check_language_safety()

            # Koşullu yasaklı uyarısı ISTISNA_IFADELERI nedeniyle verilmemeli
            warn_messages = [f["message"] for f in linter.findings if "absolute" in f["message"] or "mutlak" in f["message"]]
            assert len(warn_messages) == 0
        finally:
            if temp_path.exists():
                temp_path.unlink()

    def test_manifest_generation_and_verification(self):
        content = "Test içeriği SHA-256 bütünlük kontrolü için."
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".md", delete=False) as f:
            f.write(content)
            temp_path = Path(f.name)

        try:
            gen_code = generate_manifest(temp_path)
            assert gen_code == 0

            manifest_file = temp_path.with_suffix(temp_path.suffix + ".sha256")
            assert manifest_file.exists()

            # Linter manifesti doğrulayabilmeli
            linter = GemLinterV6(temp_path, manifest_path=manifest_file)
            linter.load_file()
            linter.is_v6 = True
            linter.check_v4_hash()

            block_hash_findings = [f for f in linter.findings if f["rule"] == "L-0404"]
            assert len(block_hash_findings) == 0

            # Dosya içeriği değiştirilirse manifest BLOCK üretmeli
            temp_path.write_text("Değiştirilmiş içerik!", encoding="utf-8")
            linter_tampered = GemLinterV6(temp_path, manifest_path=manifest_file)
            linter_tampered.load_file()
            linter_tampered.is_v6 = True
            linter_tampered.check_v4_hash()

            block_tampered = [f for f in linter_tampered.findings if f["rule"] == "L-0404"]
            assert len(block_tampered) == 1
        finally:
            if temp_path.exists():
                temp_path.unlink()
            m = temp_path.with_suffix(temp_path.suffix + ".sha256")
            if m.exists():
                m.unlink()

    def test_isnad2_classical_and_modern_sources(self):
        # classical_sources içinde death_year eksikse L-0106, modern_sources içinde url/doi eksikse L-0105 vermeli
        text = """---
gem_version: "6.1.1"
status: "PRE-RELEASE"
classical_sources:
  - id: "src-1"
    author: "Zemahşerî"
    work: "el-Keşşâf"
    volume: "1"
    pages: "10"
    verification_link: "https://archive.org/details/kashshaf"
modern_sources:
  - id: "mod-1"
    institution: "World Bank"
    title: "Governance Indicators"
---
Test içeriği.
"""
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".md", delete=False) as f:
            f.write(text)
            temp_path = Path(f.name)

        try:
            linter = GemLinterV6(temp_path, katman=1, h6=False)
            linter.load_file()
            linter.check_v1_sources()

            rules = [f["rule"] for f in linter.findings]
            assert "L-0106" in rules
            assert "L-0105" in rules
        finally:
            if temp_path.exists():
                temp_path.unlink()


class TestGemLintCLI:
    def test_cli_version(self):
        cmd = [sys.executable, str(ROOT_DIR / "src" / "gem_lint.py"), "--version"]
        res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
        assert res.returncode == 0
        assert "v6.1.1" in res.stdout

    def test_cli_help(self):
        cmd = [sys.executable, str(ROOT_DIR / "src" / "gem_lint.py"), "--help"]
        res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
        assert res.returncode == 0
        assert "Kullanım:" in res.stdout


class TestGemLintV16SourceRegistry:
    """V16 (L-2501..L-2506) Çoklu Sunucu Sicil, Fihrist/Cilt Eşleşmesi, Lafzî İktibas, Tazelik ve Rol Ayrımı Testleri."""

    def test_l2502_ghazali_cumulative_offset_blocked(self, tmp_path):
        """Gazzâlî C.3 s.186 (Rub'u'l-Mühlikât) yerine C.1 s.186 (Cuma Namazı: 9472/186) yazıldığında L-2502 BLOCK vermeli."""
        md_file = tmp_path / "wrong_ghazali.md"
        md_file.write_text(
            """---
gem_version: "6.2.2"
case_id: "QV-2026-999"
verse: "49:9"
status: "PRE-RELEASE"
sha256_hash: "1111111111111111111111111111111111111111111111111111111111111111"
---
### 13.2. Kalp Fıkhı ve Bâtınî İlletler
- Ebû Hâmid el-Gazzâlî, *İhyâ'u 'Ulûmi'd-Dîn* (Cilt: 3, s. 186; [https://shamela.ws/book/9472/186](https://shamela.ws/book/9472/186)).
""",
            encoding="utf-8",
        )
        linter = GemLinterV6(md_file, katman=3, h6=True)
        linter.load_file()
        linter.check_v16_source_registry()

        rules = [f["rule"] for f in linter.findings if f["level"] == BLOCK]
        assert "L-2502" in rules, "Gazzâlî 9472/186 kümülatif sayfa ofset hatası L-2502 BLOCK üretmeli!"
        assert "L-2501" in rules, "Sicilde olmayan 9472/186 bağlantısı L-2501 BLOCK üretmeli!"
        assert "L-2505" in rules, "L-2501/L-2502 BLOCK varken mühürlü raporda L-2505 BLOCK üretmeli!"

    def test_l2502_altafsir_wrong_tafsir_or_verse_blocked(self, tmp_path):
        """Altafsir.com bağlantısında Kuşeyrî için tTafsirNo=30 (Sülemî) veya yanlış sûre/âyet yazıldığında L-2502 BLOCK vermeli."""
        reg_file = tmp_path / "temp_registry.yaml"
        wrong_url = "https://www.altafsir.com/Tafasir.asp?tMadhNo=3&tTafsirNo=30&tSoraNo=9&tAyahNo=5&tDisplay=yes"
        reg_file.write_text(
            f"""schema_version: "16.2"
sources:
  - id: "ALT-WRONG"
    server: "altafsir"
    url: "{wrong_url}"
    expected_breadcrumb: "Altafsir | Kuşeyrî"
    verified_breadcrumb: "Altafsir | Kuşeyrî"
    quote_matched: true
    status: "VERIFIED"
    verified_at: "2026-10-20"
    reverify_period_days: 90
    snapshot_sha256: "abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789"
    human_sample_audit:
      sampled: true
  - id: "SHM-9472-932"
    url: "https://shamela.ws/book/9472/932"
    expected_breadcrumb: "a"
    verified_breadcrumb: "a"
    status: "VERIFIED"
    verified_at: "2026-10-20"
    snapshot_sha256: "abcdef0123456789abcdef0123456789"
    human_sample_audit: {{sampled: true}}
  - id: "SHM-23629-647"
    url: "https://shamela.ws/book/23629/647"
    expected_breadcrumb: "b"
    verified_breadcrumb: "b"
    status: "VERIFIED"
    verified_at: "2026-10-20"
    snapshot_sha256: "abcdef0123456789abcdef0123456789"
    human_sample_audit: {{sampled: true}}
  - id: "SHM-10273-3482"
    url: "https://shamela.ws/book/10273/3482"
    expected_breadcrumb: "c"
    verified_breadcrumb: "c"
    status: "VERIFIED"
    verified_at: "2026-10-20"
    snapshot_sha256: "abcdef0123456789abcdef0123456789"
    human_sample_audit: {{sampled: true}}
  - id: "SHM-23600-90"
    url: "https://shamela.ws/book/23600/90"
    expected_breadcrumb: "d"
    verified_breadcrumb: "d"
    status: "VERIFIED"
    verified_at: "2026-10-20"
    snapshot_sha256: "abcdef0123456789abcdef0123456789"
    human_sample_audit: {{sampled: true}}
""",
            encoding="utf-8",
        )
        md_file = tmp_path / "wrong_altafsir.md"
        md_file.write_text(
            f"""---
gem_version: "6.2.2"
case_id: "QV-2026-001"
verse: "2:256"
status: "PRE-RELEASE"
---
### 13.3. Klasik İşârî ve İrfânî Tahrîc
- Abdülkerîm el-Kuşeyrî, *Letâ'ifü'l-İşârât* ({wrong_url})
""",
            encoding="utf-8",
        )
        linter = GemLinterV6(md_file, katman=3, h6=True, registry_path=reg_file)
        linter.load_file()
        linter.check_v16_source_registry()

        l2502_msgs = [f["message"] for f in linter.findings if f["rule"] == "L-2502" and f["level"] == BLOCK]
        assert len(l2502_msgs) >= 2, f"Hem yanlış müfessir (tTafsirNo=30) hem yanlış âyet (9:5 vs 2:256) L-2502 BLOCK vermeli! Bulunan: {l2502_msgs}"

    def test_l2503_verbatim_quote_mismatch_blocked(self, tmp_path):
        """classical_sources içindeki arabic_quote hedef sayfa verisiyle eşleşmediğinde L-2503 BLOCK vermeli."""
        md_file = tmp_path / "wrong_quote.md"
        md_file.write_text(
            """---
gem_version: "6.2.2"
case_id: "QV-2026-001"
verse: "9:5"
status: "PRE-RELEASE"
classical_sources:
  - id: "cls-taberi"
    author: "Taberî"
    death_year: "ö. 310/923"
    work: "Câmi'u'l-Beyân"
    volume: "14"
    pages: "142"
    arabic_quote: "هذا نص مختلق تماما لا يوجد في الصفحة الأصلية مطلقا"
    verification_link: "https://shamela.ws/book/23627/946"
---
Test gövdesi.
""",
            encoding="utf-8",
        )
        linter = GemLinterV6(md_file, katman=3, h6=True)
        linter.load_file()
        linter.check_v16_source_registry()

        l2503_blocks = [f for f in linter.findings if f["rule"] == "L-2503" and f["level"] == BLOCK]
        assert len(l2503_blocks) >= 1, "Sayfada bulunmayan uydurma/telhîs Arapça metin L-2503 BLOCK üretmeli!"

    def test_l2504_stale_date_and_l2506_low_sample_ratio(self, tmp_path):
        """90 günü aşmış doğrulama tarihi L-2504 WARN, %10 altı manuel örneklem oranı L-2506 BLOCK üretmeli."""
        reg_file = tmp_path / "stale_registry.yaml"
        reg_file.write_text(
            """schema_version: "16.2"
sources:
  - id: "SHM-STALE"
    server: "shamela"
    url: "https://shamela.ws/book/7798/11532"
    expected_breadcrumb: "Câmi'u'l-Beyân"
    verified_breadcrumb: "Câmi'u'l-Beyân"
    quote_matched: true
    status: "VERIFIED"
    verified_at: "2026-01-01"
    reverify_period_days: 90
    snapshot_sha256: "abcdef0123456789abcdef0123456789"
    human_sample_audit:
      sampled: false
""",
            encoding="utf-8",
        )
        md_file = tmp_path / "stale_doc.md"
        md_file.write_text(
            """---
gem_version: "6.2.2"
case_id: "QV-2026-001"
verse: "9:5"
status: "PRE-RELEASE"
---
Bağlantı: https://shamela.ws/book/7798/11532
""",
            encoding="utf-8",
        )
        linter = GemLinterV6(md_file, katman=3, h6=True, registry_path=reg_file)
        linter.load_file()
        linter.check_v16_source_registry()

        warns = [f["rule"] for f in linter.findings if f["level"] == WARN]
        blocks = [f["rule"] for f in linter.findings if f["level"] == BLOCK]
        assert "L-2504" in warns, "90 günü aşan doğrulama tarihi L-2504 WARN üretmeli!"
        assert "L-2506" in blocks, "%10 altı manuel örneklem oranı L-2506 BLOCK üretmeli!"

    def test_all_30_founding_monographs_pass_v16_zero_block(self):
        """Külliyattaki 30 kurucu monografinin (15 TR + 15 EN) tamamı V1..V16 (L-0100..L-2506) kapılarından 0 BLOCK ile geçmeli."""
        tr_reps = [f for f in sorted((ROOT_DIR / "docs" / "tr").glob("[0-9][0-9]-*-v6.1.1.md")) if not f.name.startswith("05-")]
        en_reps = [f for f in sorted((ROOT_DIR / "docs" / "en").glob("[0-9][0-9]-*-en-v6.1.1.md")) if not f.name.startswith("05-")]
        all_reps = tr_reps + en_reps
        assert len(all_reps) == 30

        for rep in all_reps:
            linter = GemLinterV6(rep, katman=3, h6=True)
            linter.run_all()
            blocks = [f for f in linter.findings if f["level"] == BLOCK]
            assert len(blocks) == 0, f"{rep.name} içinde beklenmeyen BLOCK: {blocks}"

    def test_l2507_global_replace_corruption_blocked(self, tmp_path):
        """Global find-replace sonucu 'Akademik Danışman & Dış Hakem: Mehmet Yarıcı ... AMEA' gibi bozuk künye verildiğinde L-2507 BLOCK üretmeli."""
        md_file = tmp_path / "corrupted_identity.md"
        md_file.write_text(
            """---
gem_version: "6.2.3"
case_id: "QV-2026-001"
verse: "9:5"
status: "PRE-RELEASE"
peer_review:
  status: "PRE-RELEASE"
  reviewer_name: "Mehmet Yarıcı (Project Lead — Internal Sample Audit)"
  reviewer_title: "Akademik Danışman & Dış Hakem"
  reviewer_institution: "Azerbaycan Milli İlimler Akademisi (AMEA / ANAS), Felsefe ve Sosyoloji Enstitüsü"
  reviewer_orcid: "0009-0003-0356-8582"
---
- **Proje Yürütücüsü & Baş Araştırmacı:** Mehmet Yarıcı (ORCID: 0009-0003-0356-8582)
- **Akademik Danışman & Dış Hakem:** Mehmet Yarıcı (Project Lead — Internal Sample Audit) — Azerbaycan Milli İlimler Akademisi (AMEA), Felsefe ve Sosyoloji Enstitüsü
""",
            encoding="utf-8",
        )
        linter = GemLinterV6(md_file, katman=3, h6=True)
        linter.load_file()
        linter.check_v17_people_registry()

        l2507_blocks = [f for f in linter.findings if f["rule"] == "L-2507" and f["level"] == BLOCK]
        assert len(l2507_blocks) >= 2, f"Bozuk AMEA/Akademik Danışman künyesi L-2507 BLOCK üretmeli! Bulunan: {l2507_blocks}"

    def test_l2507_orcid_identity_mismatch_blocked(self, tmp_path):
        """Aynı ORCID'nin iki farklı isimle veya yanlış danışman/yürütücü eşleşmesiyle verildiği durumda L-2507 BLOCK üretmeli."""
        bad_people = tmp_path / "bad_people_registry.yaml"
        bad_people.write_text(
            """version: "6.2.3"
people:
  - id: "person-001"
    full_name: "Mehmet Yarıcı"
    orcid: "0009-0003-0356-8582"
    affiliation: "Bağımsız Araştırmacı / Proje Yürütücüsü (Quran Vision)"
    roles: ["project_lead", "principal_investigator", "internal_sample_audit"]
    forbidden_roles: ["academic_advisor", "independent_external_reviewer"]
    verified_at: "2026-10-20"
  - id: "person-002"
    full_name: "Mehmet Emin Koç"
    orcid: "0009-0003-0356-8582"
    affiliation: "Azerbaycan Milli İlimler Akademisi (AMEA), Felsefe ve Sosyoloji Enstitüsü"
    roles: ["academic_advisor"]
    forbidden_roles: ["project_lead", "internal_sample_audit", "independent_external_reviewer"]
    verified_at: "2026-10-20"
""",
            encoding="utf-8",
        )
        md_file = tmp_path / "orcid_mismatch.md"
        md_file.write_text(
            """---
gem_version: "6.2.3"
case_id: "QV-2026-001"
verse: "9:5"
status: "PRE-RELEASE"
---
- **Akademik Danışman:** Mehmet Emin Koç — Azerbaycan Milli İlimler Akademisi (AMEA) — ORCID: 0009-0003-0356-8582
""",
            encoding="utf-8",
        )
        linter = GemLinterV6(md_file, katman=3, h6=True, people_registry_path=bad_people)
        linter.load_file()
        linter.check_v17_people_registry()

        l2507_blocks = [f for f in linter.findings if f["rule"] == "L-2507" and f["level"] == BLOCK]
        assert len(l2507_blocks) >= 2, f"ORCID çakışması ve yanlış danışman ORCID'si L-2507 BLOCK üretmeli! Bulunan: {l2507_blocks}"


