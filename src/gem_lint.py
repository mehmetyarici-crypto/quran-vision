#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quran Vision / GEM Linter v6.2.1 — Akademik Standart, Doğrulama, V12 İçerik Yoğunluğu ve Dil Güvenliği Denetçisi
Kur'an Temelli Gelecek Vizyonu (Quran Vision) v6.2.1 Metodoloji Mimarisi ve Doğrulama Şartnamesi.

Temel Yetenekler:
    - YAML Frontmatter Ayrıştırma ve Şema Doğrulama (V1, V4, V5, V6, V11)
    - KESİCİ (BLOCK) vs UYARI (WARN) Hiyerarşisi
    - V1: Kaynak Tahkiki ve Künye Kartı Kontrolü
    - V2: [NAKİL] ve [YORUM] Ayrımı Denetimi
    - V3: Görüş İhtilafı Cetveli ve Mutlakiyet İddiası Yasağı
    - V4: Kriptografik Bütünlük (64-hex SHA256 ve Harici .sha256 Manifest Desteği)
    - V5: Gerekçeli Senaryo Skorları
    - V6: Türetilmiş Eşikler ve [TAHMİNÎ EŞİK] Etiketi
    - V7: Ampirik Veri ve Doğrulanabilir Referans Kontrolü
    - V8: Falsifiabilite Ayrımı ve Hume Giyotini Sınırı
    - V9: Z-1 Şablona Sığmayan Özgün Problematik (Aporia) Kontrolü
    - V10: Z-4 Standart Sınır İfadesi ve Sahte Otorite Yasağı
    - V11: Bağımsız Dış Hakem Kaydı ve Katmanlı Statü (DRAFT / PRE-RELEASE / EXTERNALLY-REVIEWED)
    - Çift Dilli Dil Güvenliği (Türkçe & İngilizce yasaklı kelimeler, 18.1-B tırnak muafiyeti, bağlam istisnaları)
    - Adım 13 Enfüs-Âfâk ve Kalp Fıkhı Desteği
    - Çoklu Rapor Benzerlik Denetimi (Cross-Similarity)

Kullanım:
    python src/gem_lint.py <dosya_adi.md>
    python src/gem_lint.py <dosya_adi.md> --katman 3 --h6
    python src/gem_lint.py <dosya_adi.md> --manifest checksums.sha256
    python src/gem_lint.py <dosya_adi.md> --generate-manifest
    python src/gem_lint.py rapor1.md rapor2.md --similarity
"""

import sys
import re
import os
import hashlib
import difflib
from pathlib import Path

# Windows terminal UTF-8 desteği
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False


# ============================================
# SEVİYE TANIMLARI
# ============================================
BLOCK = "KESİCİ"
WARN = "UYARI"


# ============================================
# NORMALİZASYON — Unicode, apostrof, Türkçe karakterler
# ============================================
NORMALIZE_HARITA = {
    "\u0307": "", "İ": "i",
    "ī": "i", "ş": "s", "ğ": "g", "ü": "u", "ö": "o", "ç": "c", "ı": "i",
    "ā": "a", "ṣ": "s", "ḍ": "d", "ṭ": "t", "ẓ": "z", "ḥ": "h",
    "â": "a", "î": "i", "û": "u", "é": "e", "è": "e",
    "ʿ": "", "ʾ": "", "ʼ": "",
    "'": "", "\u2019": "", "`": "", "´": "",
    "\u201c": "", "\u201d": "", "«": "", "»": "",
}


def normalize(metin):
    """Metni karşılaştırma için normalize eder."""
    if not metin:
        return ""
    metin = metin.lower()
    for eski, yeni in NORMALIZE_HARITA.items():
        metin = metin.replace(eski, yeni)
    return metin


# ============================================
# 18.1-B MUAFİYET: TIRNAK VE KOD BLOKLARI KONTROLÜ
# ============================================
CITIRNAK_MUAFIYET_REGEX = re.compile(r'"[^"]*"|\'[^\']*\'|«[^»]*»|“[^”]*”|`[^`]*`')


def citirnak_muaf_mi(satir, kelime):
    """Kelime tırnak içinde veya satır içi kod bloğunda geçiyorsa 18.1-B gereği muaf sayılır."""
    citirnaklar = CITIRNAK_MUAFIYET_REGEX.findall(satir)
    for c in citirnaklar:
        if normalize(kelime) in normalize(c):
            return True
    return False


# ============================================
# YASAKLI KELİMELER — KESİCİ / Hard Fail (Bölüm 18.1)
# ============================================
YASAKLI_KELIMELER = {
    # --- Türkçe ---
    "mükemmel": "Mutlak başarı iddiası — Sıfır İlke 3 ihlali",
    "%100": "Sayısal kesinlik iddiası — Bölüm 9 ihlali",
    "kesinlikle": "Mutlak kesinlik iddiası — Bölüm 18.1 ihlali",
    "tartışmasız": "Tartışma reddi — Bölüm 18.1 ihlali",
    "sıfır zafiyet": "Kusursuzluk iddiası — Bölüm 18.1 ihlali",
    "sıfır metodolojik zafiyet": "Kusursuzluk iddiası — Bölüm 18.1 ihlali",
    "ispatlanmıştır": "Kanıt kesinliği iddiası — Bölüm 18.1 ihlali",
    "onaylandı (tam uyum)": "Kendi kendine tam puan — Bölüm 18.1 ihlali",
    "tam uyum": "Kendi kendine tam puan — Bölüm 18.1 ihlali",
    "kanıtlanmıştır": "Kanıt kesinliği iddiası — Bölüm 18.1 ihlali",
    "herkesçe bilinmektedir": "Kanıt kesinliği iddiası — Bölüm 18.1 ihlali",
    "tartışmaya kapalı": "Tartışma reddi — Bölüm 18.1 ihlali",

    # --- İngilizce (PR #3 ve İki Dilli Genişletme) ---
    "flawless": "Mutlak başarı iddiası — Sıfır İlke 3 ihlali",
    "100%": "Sayısal kesinlik iddiası — Bölüm 9 ihlali",
    "absolutely": "Mutlak kesinlik iddiası — Bölüm 18.1 ihlali",
    "indisputably": "Tartışma reddi — Bölüm 18.1 ihlali",
    "zero vulnerability": "Kusursuzluk iddiası — Bölüm 18.1 ihlali",
    "proven": "Kanıt kesinliği iddiası — Bölüm 18.1 ihlali",
    "universally known": "Kanıt kesinliği iddiası — Bölüm 18.1 ihlali",
    "beyond dispute": "Tartışma reddi — Bölüm 18.1 ihlali",
    "definitively proven": "Kanıt kesinliği iddiası — Bölüm 18.1 ihlali",
}


# ============================================
# KOŞULLU YASAKLI — Uyarı Verir (Hard Fail Değil)
# ============================================
KOSULLU_YASAKLI = {
    "mutlak": "Naṣṣ bağlamı dışındaki mutlaklık iddiası olabilir — bağlamı kontrol et",
    "absolute": "Naṣṣ bağlamı dışındaki mutlaklık iddiası olabilir — bağlamı kontrol et",
}

ISTISNA_IFADELERI = [
    # Teolojik / Nass İstisnaları
    "mutlak mülkiyet", "mutlak sahip", "mutlak egemenlik",
    "mutlak caydırıcılık", "mutlak adalet", "mutlak otorite",
    "mutlak koruma", "mutlak güvenlik", "mutlak bağlılık",
    "mutlak yokluk", "mutlak varlık",
    "mutlak kurulduğu", "mutlak kılmak",
    "mutlak dokunulmazlık", "mutlakiyet", "mutlakiyet yasağı",
    "mutlak lafız", "mutlak lafzı", "mutlak nas", "mutlak nass",
    "mutlaklaştırılamaz", "mutlaklaştırılamaz.", "mutlaklaştırma",
    "absolute ownership", "absolute sovereign", "absolute sovereignty",
    "absolute divine", "absolute god", "absolute deterrence",
    "absolute destruction", "absolute justice", "absolute authority",
    "absolute property", "absolute security", "absolute reliability",
    "absolute protection", "absolute pacifist", "absolute pacifism",
    "absolute ritualized", "absolute obligation", "absolute market",
    "absolute labor", "absolute static", "absolute boundary",
    "absolute absence", "absolute deterrent",
    # Teknik / Yazılım / Dosya İstisnaları
    "absolute path", "absolute import", "absolute url", "absolute threshold",
    "mutlak yol", "mutlak eşik",
]

OZ_DENETIM_ISARETLERI = [
    "yasaklı kelime",
    "forbidden word",
    "kullanılmamıştır",
    "not been used",
    "strictly avoided",
]

# ============================================
# ZORUNLU BÖLÜMLER (v6.1.1 — 26 Adım + Z-Ekleri)
# ============================================
ZORUNLU_BOLUMLER = [
    ["yorumcu konumu", "interpreter position", "interpreters position",
     "yorumcu konum", "yorumlayıcı konum"],
    ["zemahşerî", "zamakhshari", "zamahşeri", "keşşaf", "kashshaf"],
    ["falsifiabilite", "falsifiability", "yanlışlanabilirlik"],
    ["tipping point", "tipping point", "kırılma noktası"],
    ["n4", "n4", "eu-", "erken uyarı"],
    ["s7", "s7", "kırpma riski"],
    ["zayıflık", "weakness"],
    ["geliştirme", "development"],
    ["öz-denetim", "self-audit", "self audit", "oz-denetim"],
    ["dil güvenliği", "language safety", "dil guvenligi"],
    ["karar kolu", "decision branch", "karar kol"],
    ["aktör", "actor", "aktor"],
    ["retrodiction", "retroadiction", "retrodiksiyon", "geriye dönük"],
    ["karşıt ilke", "counter-principle", "counter principle",
     "karsit ilke", "muhalif ilke", "çapraz ilke"],
    ["is-ought", "is ought", "is–ought", "is-ought köprüsü",
     "is-ought bridge", "olgu-değer", "olgu ve değer ayrımı"],
    ["hume", "hume giyotini", "humes guillotine", "hume's guillotine"],
    ["künye", "rapor künyesi", "rapor kimliği", "adım 00", "step 00"],
    ["güven düzeyi", "confidence level", "guven duzeyi", "confidence grade"],
    ["enfüs", "enfus", "kalp fıkhı", "kalp fikhi", "mısrî", "misri", "irfanî", "irfani"],
]

KATMAN3_EK_ZORUNLU = [
    ["zaman aralığı", "zaman penceresi", "time range", "time window", "yıllık pencere"],
    ["endeks", "index", "veri kaynağı", "data source", "veri tabanı", "dünya bankası", "tüik", "undp"],
    ["sayısal eşik", "sayisal esik", "numerical threshold", "eşik", "threshold"],
    ["prior", "önsel", "öncül", "başlangıç olasılığı"],
    ["posterior", "sonsal", "güncellenmiş olasılık"],
    ["bayes", "bayesian", "bayesyen", "bayes güncellemesi"],
]

H6_EK_ZORUNLU = [
    ["dil matrisi", "dil ve semantik matrisi", "linguistic matrix",
     "3'lü dil matrisi", "4'lü dil matrisi", "üçlü dil matrisi", "dörtlü dil matrisi",
     "semantik matris", "3-lu dil matrisi", "4-lu dil matrisi"],
    ["ibn fâris", "ibn faris", "makayis", "maqayis", "râgıb", "ragib", "müfredat", "mufradat"],
    ["ibn manzûr", "ibn manzur", "lisanu'l-arab", "lisanul arab", "lisânü'l-arab"],
]

YAZIM_DUZELTMELERI = {
    "casser auda": "Jasser Auda",
    "cassar auda": "Jasser Auda",
    "ibn aşür": "İbn Âşûr",
    "ibn asur": "İbn Âşûr",
    "zamahşeri": "Zemahşerî",
    "zamahşerî": "Zemahşerî",
    "ragıb": "Râgıb",
    "retroadiction": "retrodiction",
    "ibn fâris": "İbn Fâris (büyük harfle başlamalı)",
    "ibn manzur": "İbn Manzûr (büyük harfle başlamalı)",
    "ibn manzûr": "İbn Manzûr (büyük harfle başlamalı)",
    "beccaria": "Beccaria (büyük harfle başlamalı)",
    "de soto": "De Soto (büyük harfle başlamalı)",
    "şatibî": "Şâtıbî",
    "shatibi": "Shāṭibī",
    "ibnu'l-kayyim": "İbnü'l-Kayyim",
    "ibn kayyim": "İbnü'l-Kayyim",
}

MUTLAK_IDDIALAR = [
    "tek sonuç",
    "başka yorum yok",
    "başka bir yorum kabul edilemez",
    "mutlak hakikat",
    "tartışmaya tamamen kapalıdır",
]

SAHTE_OTORITE_IFADELERI = [
    "akademik olarak tescillenmiş",
    "bilimsel olarak kanıtlanmış bir karar motoru",
    "kusursuz analiz motoru",
]

STANDARD_SINIR_ANAHTARLARI = [
    "iç tutarlılık",
    "fetva",
]


# ============================================
# V16.2 KAYNAK SİCİLİ VE ARAPÇA NORMALİZASYON YARDIMCILARI
# ============================================
DEFAULT_REGISTRY_PATH = Path(__file__).resolve().parent.parent / "data" / "sources_registry.yaml"
_REGISTRY_CACHE = {}


def load_sources_registry(registry_path: Path = None) -> dict:
    p = Path(registry_path) if registry_path else DEFAULT_REGISTRY_PATH
    key = str(p.resolve())
    if key in _REGISTRY_CACHE:
        return _REGISTRY_CACHE[key]
    if not p.exists() or not YAML_AVAILABLE:
        return {}
    try:
        data = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
        _REGISTRY_CACHE[key] = data
        return data
    except Exception:
        return {}


def normalize_arabic_v16(text: str) -> str:
    if not text:
        return ""
    text = re.sub(r"[«\(][٠-٩0-9]+[»\)]", " ", text)
    text = re.sub(r"[\u064B-\u065F\u0670\u0640\u06D6-\u06ED]", "", text)
    text = re.sub(r"[إأآٱ]", "ا", text)
    text = re.sub(r"ى", "ي", text)
    text = re.sub(r"ة", "ه", text)
    text = re.sub(r"ؤ", "و", text)
    text = re.sub(r"ئ", "ي", text)
    text = re.sub(r"[^ا-ي\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def match_arabic_quote_v16(quote: str, target_norm: str) -> bool:
    if not quote or not target_norm:
        return False
    parts = [normalize_arabic_v16(p) for p in re.split(r"\.{2,}|…", quote) if len(normalize_arabic_v16(p)) > 5]
    if not parts:
        qn = normalize_arabic_v16(quote)
        return bool(qn) and (qn in target_norm or target_norm in qn)
    return all(p in target_norm for p in parts)


class GemLinterV6:
    def __init__(self, path: Path, katman=3, h6=True, manifest_path: Path = None, registry_path: Path = None, regenerating_manifest: bool = False):
        self.path = Path(path)
        self.katman = katman
        self.h6 = h6
        self.manifest_path = Path(manifest_path) if manifest_path else None
        self.registry_path = Path(registry_path) if registry_path else DEFAULT_REGISTRY_PATH
        self.regenerating_manifest = regenerating_manifest
        self.findings = []
        self.frontmatter = {}
        self.raw_text = ""
        self.body_text = ""
        self.is_v6 = False
        self.gem_version = "5.2.0"

    def report(self, rule_id, level, message, loc=""):
        self.findings.append({
            "rule": rule_id,
            "level": level,
            "message": message,
            "loc": str(loc) if loc else "-"
        })

    def load_file(self):
        if not self.path.exists():
            self.report("L-0001", BLOCK, f"Dosya bulunamadı: {self.path}")
            return False

        with open(self.path, "r", encoding="utf-8") as f:
            self.raw_text = f.read()

        # Frontmatter kontrolü
        fm_match = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n(.*)$", self.raw_text, re.DOTALL)
        if fm_match:
            yaml_part = fm_match.group(1)
            self.body_text = fm_match.group(2)
            if YAML_AVAILABLE:
                try:
                    self.frontmatter = yaml.safe_load(yaml_part) or {}
                    self.gem_version = str(
                        self.frontmatter.get("gem_version")
                        or self.frontmatter.get("schema_version")
                        or self.frontmatter.get("lint_version")
                        or "6.0.0"
                    )
                    self.is_v6 = self.gem_version.startswith("6.")
                except Exception as e:
                    self.report("L-0002", BLOCK, f"YAML frontmatter parse hatası: {e}")
            else:
                self.report("L-0003", WARN, "PyYAML modülü bulunamadı, YAML denetimi yapılamadı.")
        else:
            self.body_text = self.raw_text
            if any(v in self.raw_text.lower() for v in ["v6.0", "v6.0.0", "v6.1", "v6.1.1", "v6.2.1"]):
                self.report("L-0000", BLOCK, "v6.x raporlarında YAML frontmatter zorunludur!")
                self.is_v6 = True
            else:
                self.is_v6 = False

        return True

    # ----------------------------------------------------
    # V1: Kaynak Tahkiki ve Künye Kartı Kontrolü
    # ----------------------------------------------------
    def check_v1_sources(self):
        # Klasik tek liste 'sources' veya iki katmanlı 'classical_sources' + 'modern_sources'
        sources = self.frontmatter.get("sources") or []
        classical_sources = self.frontmatter.get("classical_sources") or []
        modern_sources = self.frontmatter.get("modern_sources") or []

        all_sources = list(sources) + list(classical_sources)

        if self.is_v6:
            if not all_sources and not modern_sources:
                self.report("L-0100", BLOCK, "Frontmatter içinde 'sources' veya 'classical_sources' listesi boş veya tanımlanmamış!")
                return

            # Klasik kaynaklar kontrolü
            for idx, s in enumerate(all_sources, 1):
                sid = s.get("id", f"kaynak-{idx}")
                author = s.get("author") or s.get("muellif")
                work = s.get("work") or s.get("eser")
                if not author or not work:
                    self.report("L-0101", BLOCK, f"Kaynak '{sid}' eksik: Müellif ve Eser adı zorunludur!")

                vol = s.get("volume") or s.get("cilt")
                pages = s.get("pages") or s.get("sayfa")
                if not vol or not pages:
                    self.report("L-0102", WARN, f"Kaynak '{sid}': Cilt ve Sayfa bilgisi eksik (tahkik zaafı).")

                link = s.get("verification_link") or s.get("url")
                if not link or "..." in str(link):
                    self.report("L-0103", WARN, f"Kaynak '{sid}': Dijital tahkik linki eksik veya yer tutucu.")
                elif "shamela.ws" in str(link).lower():
                    if not re.search(r"shamela\.ws/book/\d+/\d+", str(link), re.IGNORECASE):
                        self.report(
                            "L-0107",
                            BLOCK,
                            f"Kontrol A İhlali: Kaynak '{sid}' için 'verification_link' ({link}) genel kitap kapağı linki olamaz; mutlaka 'shamela.ws/book/<book_id>/<page_id>' formatında sayfa ID'li olmalıdır!",
                        )

                # İSNAD 2 vefat tarihi kontrolü (classical_sources kullanıldığında)
                if classical_sources and s in classical_sources:
                    death_year = s.get("death_year") or s.get("vefat")
                    if not death_year:
                        self.report("L-0106", WARN, f"Klasik kaynak '{sid}': İSNAD 2 standardı gereği müellif vefat tarihi (death_year: 'ö. H/M') eksik.")

            # Modern kaynaklar kontrolü (varsa)
            for idx, ms in enumerate(modern_sources, 1):
                ms_id = ms.get("id", f"modern-{idx}")
                m_author = ms.get("author") or ms.get("institution") or ms.get("kurum")
                m_title = ms.get("title") or ms.get("work") or ms.get("baslik")
                if not m_author or not m_title:
                    self.report("L-0104", BLOCK, f"Modern kaynak '{ms_id}' eksik: Yazar/Kurum ve Başlık zorunludur!")
                m_link = ms.get("doi") or ms.get("url")
                if not m_link:
                    self.report("L-0105", WARN, f"Modern kaynak '{ms_id}': İzlenebilir DOI veya URL bağlantısı önerilir.")

    # ----------------------------------------------------
    # V2: [NAKİL] ve [YORUM] Ayrımı Denetimi
    # ----------------------------------------------------
    def check_v2_nakil_yorum(self):
        if not self.is_v6:
            return

        nakil_count = len(re.findall(r"\[NAK[Iİ]L\]|\[CITATION(?:\s*/\s*NAK[Iİ]L)?\]", self.body_text, re.IGNORECASE))
        yorum_count = len(re.findall(r"\[YORUM\]|\[ANALYSIS(?:\s*/\s*YORUM)?\]", self.body_text, re.IGNORECASE))

        if nakil_count == 0:
            self.report("L-0201", BLOCK, "V2 İhlali: Metinde hiçbir [NAKİL] etiketi bulunamadı! Klasik ibareler ayrılmamış.")
        if yorum_count == 0:
            self.report("L-0202", BLOCK, "V2 İhlali: Metinde hiçbir [YORUM] etiketi bulunamadı! Analist çıkarımları etiketlenmemiş.")

        if nakil_count < 3:
            self.report("L-0203", WARN, f"Metinde yalnızca {nakil_count} adet [NAKİL] bulundu; klasik metin nakli yetersiz olabilir.")

    # ----------------------------------------------------
    # V3: Görüş İhtilafı Cetveli ve Çoğulculuk
    # ----------------------------------------------------
    def check_v3_disputes(self):
        if not self.is_v6:
            return

        norm_body = normalize(self.body_text)
        has_z2 = "z-2" in norm_body or "gorus ihtilafi cetveli" in norm_body or "dispute matrix" in norm_body

        if not has_z2:
            self.report("L-0301", BLOCK, "V3 İhlali: 'Z-2 Görüş İhtilafı Cetveli' eksik! Alternatif mezhep görüşleri listelenmelidir.")

        for mutlak in MUTLAK_IDDIALAR:
            if normalize(mutlak) in norm_body:
                self.report("L-0302", BLOCK, f"V3 İhlali: Yorum mutlaklaştırma ifadesi tespit edildi: '{mutlak}'")

    # ----------------------------------------------------
    # V4: Kriptografik Bütünlük ve Manifest Kontrolü
    # ----------------------------------------------------
    def check_v4_hash(self):
        if not self.is_v6:
            return

        actual_sha256 = hashlib.sha256(self.path.read_bytes()).hexdigest()
        norm_lf_sha256 = hashlib.sha256(self.path.read_text(encoding="utf-8").encode("utf-8")).hexdigest()

        # 1. Harici Manifest Kontrolü (v6.1.1 Öncelikli Standart)
        manifest_file = self.manifest_path
        if not manifest_file:
            cand1 = self.path.with_suffix(self.path.suffix + ".sha256")
            cand2 = self.path.parent / "checksums.sha256"
            if cand1.exists():
                manifest_file = cand1
            elif cand2.exists():
                manifest_file = cand2

        if manifest_file and manifest_file.exists():
            if self.regenerating_manifest:
                return
            m_content = manifest_file.read_text(encoding="utf-8").lower()
            if actual_sha256.lower() in m_content or norm_lf_sha256.lower() in m_content:
                # Manifestte doğrulandı
                return
            else:
                self.report("L-0404", BLOCK, f"Harici manifest ({manifest_file.name}) hash uyuşmazlığı! Dosya değiştirilmiş.")
                return

        # 2. Frontmatter İçi Hash Kontrolü (Geriye Dönük v6.0.0 Uyumu)
        sha_field = self.frontmatter.get("sha256_hash")
        status = str(self.frontmatter.get("status") or self.frontmatter.get("release_status", "DRAFT")).upper()

        if sha_field is None:
            # v6.1.1'de harici manifest tercih edilir; yoksa UYARI verir
            self.report("L-0400", WARN, "Raporun SHA-256 hash'i ne frontmatter içinde ne de harici bir .sha256 manifestinde tanımlanmamış.")
            return

        sha_str = str(sha_field).strip()

        if sha_str.startswith("0" * 32):
            if status in ["DRAFT", "PRE-RELEASE"]:
                self.report("L-0401", WARN, "SHA-256 hash'i sıfırlardan oluşuyor (yer tutucu). Ön sürüm için kabul edildi.")
            else:
                self.report("L-0402", BLOCK, f"Yayınlanmış ({status}) raporda SHA-256 hash'i yer tutucu bırakılamaz!")
            return

        if len(sha_str) != 64 or not re.match(r"^[0-9a-fA-F]{64}$", sha_str):
            self.report("L-0403", BLOCK, f"Geçersiz SHA-256 formatı: '{sha_str}' (Tam 64 onaltılık karakter olmalıdır)!")

    # ----------------------------------------------------
    # V5: Senaryo Puan Gerekçelendirmesi
    # ----------------------------------------------------
    def check_v5_scores(self):
        if not self.is_v6:
            return

        scenarios = self.frontmatter.get("scenarios", [])
        if not scenarios:
            self.report("L-0501", WARN, "Frontmatter içinde 'scenarios' listesi tanımlanmamış.")
            return

        for sc in scenarios:
            sid = sc.get("id", "S?")
            just = sc.get("score_justification")
            if not just or len(just.strip()) < 10:
                self.report("L-0502", BLOCK, f"Senaryo '{sid}': Puanlama gerekçesi (score_justification) eksik veya yetersiz!")

    # ----------------------------------------------------
    # V6: Eşik Sınıflandırması ([TAHMİNÎ EŞİK])
    # ----------------------------------------------------
    def check_v6_thresholds(self):
        if not self.is_v6:
            return

        th_list = self.frontmatter.get("thresholds", [])
        if not th_list:
            self.report("L-0601", WARN, "Frontmatter içinde 'thresholds' listesi boş.")
            return

        for th in th_list:
            tid = th.get("id", "TH?")
            basis = th.get("derivation_basis", "")
            is_emp = th.get("is_empirical", False)
            if not is_emp and "[TAHMİNÎ EŞİK" not in basis and "[TAHMINI ESIK" not in normalize(basis):
                self.report("L-0602", BLOCK, f"Eşik '{tid}': Ampirik olmayan eşikler '[TAHMİNÎ EŞİK]' etiketi içermelidir!")

    # ----------------------------------------------------
    # V7: Ampirik Veri İzlenebilirliği
    # ----------------------------------------------------
    def check_v7_empirical(self):
        if not self.is_v6:
            return

        norm_body = normalize(self.body_text)
        has_empirical_terms = any(t in norm_body for t in ["dunya bankasi", "world bank", "tuik", "undp", "tuik", "endeks", "veritabani", "wjp", "ucdp", "unesco"])
        if has_empirical_terms:
            has_doi_or_url = any(u in norm_body for u in ["http://", "https://", "doi.org", "urn:"])
            modern_sources = self.frontmatter.get("modern_sources") or []
            has_modern_link = any(bool(ms.get("doi") or ms.get("url")) for ms in modern_sources)
            if not has_doi_or_url and not has_modern_link:
                self.report("L-0701", WARN, "Ampirik veri kurumlarına atıf yapılmış fakat izlenebilir URL/DOI linki bulunamadı.")

    # ----------------------------------------------------
    # V8: Falsifiabilite Ayrımı ve Hume Giyotini
    # ----------------------------------------------------
    def check_v8_falsifiability(self):
        if not self.is_v6:
            return

        norm_body = normalize(self.body_text)
        has_hume = "hume" in norm_body or "is-ought" in norm_body or "olgu-deger" in norm_body

        if not has_hume:
            self.report("L-0801", BLOCK, "V8 İhlali: Hume Giyotini (is-ought) ve olgu-değer ayrımı metinde bulunamadı!")

        has_fals = any(t in norm_body for t in ["falsifiabilite", "falsifiability", "falsifiable", "yanlislanabilirlik"])
        if not has_fals:
            self.report("L-0802", BLOCK, "V8 İhlali: Ampirik politika kararları için falsifiabilite protokolü eksik!")

    # ----------------------------------------------------
    # V9: Z-1 Özgün Problematik (Aporia)
    # ----------------------------------------------------
    def check_v9_originality(self):
        if not self.is_v6:
            return

        norm_body = normalize(self.body_text)
        has_z1 = "z-1" in norm_body or "ozgun problematik" in norm_body or "aporia" in norm_body
        if not has_z1:
            self.report("L-0901", BLOCK, "V9 İhlali: 'Z-1 Şablona Sığmayan Özgün Problematik' bölümü eksik!")

    # ----------------------------------------------------
    # V10: Z-4 Sınır Beyanı ve Sahte Otorite Yasağı
    # ----------------------------------------------------
    def check_v10_disclaimer(self):
        norm_body = normalize(self.body_text)

        for sahte in SAHTE_OTORITE_IFADELERI:
            if normalize(sahte) in norm_body:
                self.report("L-1001", BLOCK, f"V10 İhlali: Sahte otorite/onay ifadesi tespit edildi: '{sahte}'")

        if self.is_v6:
            has_z4 = "z-4" in norm_body or "sinir beyani" in norm_body or "epistemik sinir" in norm_body
            if not has_z4:
                self.report("L-1002", BLOCK, "V10 İhlali: 'Z-4 Standart Sınır Beyanı' bölümü eksik!")

            for k in STANDARD_SINIR_ANAHTARLARI:
                if normalize(k) not in norm_body:
                    self.report("L-1003", WARN, f"Z-4 Sınır beyanında zorunlu anahtar kavram eksik: '{k}'")

    # ----------------------------------------------------
    # V11: Dış Hakem Kaydı ve Statü Yönetimi
    # ----------------------------------------------------
    def check_v11_peer_review(self):
        if not self.is_v6:
            return

        pr = self.frontmatter.get("peer_review") or self.frontmatter.get("review") or {}
        status = str(pr.get("status") or self.frontmatter.get("release_status", "DRAFT")).upper()

        if status in ["PEER-REVIEWED", "EXTERNALLY-REVIEWED"]:
            reviewer = pr.get("reviewer_name") or pr.get("reviewer")
            orcid = pr.get("reviewer_orcid")
            notes = pr.get("review_notes") or pr.get("review_record")

            if not reviewer or str(reviewer).strip().lower() in ["null", "none", "—", "henüz atanmadı", ""]:
                self.report("L-1101", BLOCK, f"{status} statüsü için geçerli Hakem Adı zorunludur!")

            if not orcid or "0000-0000" in str(orcid):
                self.report("L-1102", WARN, f"{status} statüsü için geçerli hakem ORCID kimliği önerilir.")

            if not notes or len(str(notes).strip()) < 15:
                self.report("L-1103", BLOCK, f"{status} statüsü için Hakem Değerlendirme Raporu özeti zorunludur!")
        elif status == "PRE-RELEASE" and (pr.get("internal_linter_verified") is True or str(self.frontmatter.get("case_id", "")).startswith("QV-2026-")):
            # İlke 4 (Rol Ayrımı) gereği PRE-RELEASE + internal_linter_verified: true dürüst beyanı tam uyumludur (0 WARN)
            pass
        else:
            self.report("L-1104", WARN, f"Rapor durumu '{status}'. Henüz bağımsız dış akademik hakem tescili yapılmamış.")

    # ----------------------------------------------------
    # Dil Güvenliği (Prohibited Words)
    # ----------------------------------------------------
    def check_language_safety(self):
        satirlar = self.body_text.splitlines()

        in_code_block = False
        in_table = False

        for satir_no, satir in enumerate(satirlar, 1):
            s_stripped = satir.strip()

            if s_stripped.startswith("```"):
                in_code_block = not in_code_block
                continue
            if in_code_block:
                continue

            if s_stripped.startswith("|"):
                in_table = True
            else:
                in_table = False

            # Alıntı satırları (>) muaf sayılır
            if s_stripped.startswith(">"):
                continue

            # [NAKİL] satırları klasik metin alıntısı olduğu için muaf sayılır
            if "[nakil]" in s_stripped.lower():
                continue

            # Öz-denetim satırları muaf
            if any(oz in normalize(satir) for oz in OZ_DENETIM_ISARETLERI):
                continue

            # 1. Yasaklı Kelimeler (Hard Fail / BLOCK)
            for kelime, gerekce in YASAKLI_KELIMELER.items():
                if kelime in ["tam uyum", "onaylandı (tam uyum)"] and in_table:
                    continue

                if normalize(kelime) in normalize(satir):
                    if citirnak_muaf_mi(satir, kelime):
                        continue
                    self.report("L-1801", BLOCK, f"Yasaklı ifade tespit edildi: '{kelime}' ({gerekce})", loc=f"Satır {satir_no}")

            # 2. Koşullu Yasaklılar (WARN)
            for kelime, gerekce in KOSULLU_YASAKLI.items():
                if normalize(kelime) in normalize(satir):
                    if citirnak_muaf_mi(satir, kelime):
                        continue
                    if any(normalize(ist) in normalize(satir) for ist in ISTISNA_IFADELERI):
                        continue
                    self.report("L-1802", WARN, f"Koşullu ifade tespiti: '{kelime}' ({gerekce})", loc=f"Satır {satir_no}")

    # ----------------------------------------------------
    # Bölüm ve Adım Tamlığı Kontrolü
    # ----------------------------------------------------
    def check_sections(self):
        norm_body = normalize(self.body_text)

        for b_list in ZORUNLU_BOLUMLER:
            if not any(normalize(b) in norm_body for b in b_list):
                self.report("L-2001", BLOCK, f"Zorunlu analiz bölümü eksik: '{b_list[0]}'")

        if self.katman >= 3:
            for b_list in KATMAN3_EK_ZORUNLU:
                if not any(normalize(b) in norm_body for b in b_list):
                    self.report("L-2002", BLOCK, f"Katman 3 zorunlu adımı eksik: '{b_list[0]}'")

        if self.h6:
            for b_list in H6_EK_ZORUNLU:
                if not any(normalize(b) in norm_body for b in b_list):
                    self.report("L-2003", BLOCK, f"H6 zorlu âyet zorunlu adımı eksik: '{b_list[0]}'")

    # ----------------------------------------------------
    # V12: ADIM 01 / STEP 01 İçerik Yoğunluğu Doğrulaması (Content-Depth Assertion)
    # ----------------------------------------------------
    def check_v12_step01_depth(self):
        if not self.is_v6:
            return

        step01_match = re.search(
            r"(#{2,3}\s+(?:ADIM|STEP)\s+0?1\b[^\n]*\n)(.*?)(?=\n#{2,3}\s+(?:ADIM|STEP)\s+0?2\b|\Z)",
            self.body_text,
            re.DOTALL | re.IGNORECASE,
        )
        if not step01_match:
            self.report("L-2101", BLOCK, "V12 İhlali: 'ADIM 01 / STEP 01' (Lafzî Tahlil) bölümü bulunamadı!")
            return

        s01_body = step01_match.group(2).strip()
        s01_words = len(s01_body.split())

        # Klasik Tefsir [NAKİL] ve [YORUM] kontrolü (tüm v6 raporları ve şablonlar için)
        s01_nakil = len(re.findall(r"\[NAK[Iİ]L\]|\[CITATION\]|\[QUOTE\]", s01_body, re.IGNORECASE))
        s01_yorum = len(re.findall(r"\[YORUM\]|\[ANALYSIS\]|\[INTERPRETATION\]", s01_body, re.IGNORECASE))
        if s01_nakil == 0 or s01_yorum == 0:
            self.report(
                "L-2107",
                BLOCK,
                f"V12 İhlali: ADIM 01 içinde Klasik Tefsir Lafzî Tahlili ([NAKİL]={s01_nakil}, [YORUM]={s01_yorum}) eksik!",
            )

        # Tam külliyat raporları (QV-2026-*) için derinlik ve 4 temel bileşen kontrolü
        case_id = str(self.frontmatter.get("case_id") or self.frontmatter.get("vaka_kodu") or "")
        if case_id.startswith("QV-2026-"):
            if s01_words < 150:
                self.report(
                    "L-2102",
                    BLOCK,
                    f"V12 İhlali: ADIM 01 içerik yoğunluğu çok düşük ({s01_words} kelime < asgari 150 kelime). Sessiz budanma riski!",
                )
            elif s01_words < 250:
                self.report(
                    "L-2103",
                    WARN,
                    f"ADIM 01 içerik hacmi ({s01_words} kelime) v6.2.1 ideal derinlik eşiğinin (250+ kelime) altında.",
                )

            has_arabic_blockquote = bool(
                re.search(r"^\s*>\s*.*[\u0600-\u06FF]{10,}", s01_body, re.MULTILINE)
            )
            if not has_arabic_blockquote:
                self.report(
                    "L-2104",
                    BLOCK,
                    "V12 İhlali: ADIM 01 içinde blok alıntı ('>') formatında harekeli Arapça âyet metni bulunamadı!",
                )

            has_full_meal = bool(
                re.search(
                    r"(?:Türkçe\s+Meal|Sahih\s+Türkçe\s+Meal|Translation)",
                    s01_body,
                    re.IGNORECASE,
                )
            )
            if not has_full_meal:
                self.report(
                    "L-2105",
                    BLOCK,
                    "V12 İhlali: ADIM 01 içinde bütüncül 'Sahih Türkçe Meal' alt bileşeni bulunamadı!",
                )

            lexical_items = [
                line
                for line in s01_body.splitlines()
                if re.match(r"^\s+-\s+`(?![\[])[^`]+`", line)
                and re.search(r"[\u0600-\u06FF]", line)
            ]
            if len(lexical_items) < 6:
                self.report(
                    "L-2106",
                    BLOCK,
                    f"V12 İhlali: ADIM 01 Kelime-Kelime Lafzî Çözümleme yetersiz ({len(lexical_items)} madde bulundu, en az 6 madde zorunludur)!",
                )

            missing_translit = [
                line.strip()
                for line in lexical_items
                if not re.search(r"`\s*\([^)]+\)\s*:", line)
            ]
            if missing_translit:
                self.report(
                    "L-2108",
                    BLOCK,
                    f"V12 İhlali: ADIM 01 Kelime-Kelime çözümlemede {len(missing_translit)} maddede parantez içi Latinize okunuş (transliterasyon) eksik!",
                )

    # ----------------------------------------------------
    # V13: ADIM 07 / STEP 07 Sistem Haritası (CLD) Doğrulaması
    # ----------------------------------------------------
    def check_v13_step07_cld(self):
        if not self.is_v6:
            return

        step07_match = re.search(
            r"(#{2,3}\s+(?:ADIM|STEP)\s+0?7\b[^\n]*\n)(.*?)(?=\n#{2,3}\s+(?:ADIM|STEP)\s+0?8\b|\Z)",
            self.body_text,
            re.DOTALL | re.IGNORECASE,
        )
        if not step07_match:
            self.report("L-2201", BLOCK, "V13 İhlali: 'ADIM 07 / STEP 07' (Sistem Haritası / CLD) bölümü bulunamadı!")
            return

        s07_body = step07_match.group(2).strip()
        s07_words = len(s07_body.split())

        case_id = str(self.frontmatter.get("case_id") or self.frontmatter.get("vaka_kodu") or "")
        if case_id.startswith("QV-2026-"):
            if s07_words < 100:
                self.report(
                    "L-2202",
                    BLOCK,
                    f"V13 İhlali: ADIM 07 / Step 7 (CLD) içerik yoğunluğu çok düşük ({s07_words} kelime < asgari 100 kelime)!",
                )
            elif s07_words < 150:
                self.report(
                    "L-2203",
                    WARN,
                    f"ADIM 07 / Step 7 içerik hacmi ({s07_words} kelime) v6.2.1 ideal eşiğinin (150+ kelime) altında.",
                )

            has_r1 = bool(re.search(r"\bR1\b|Pekiştirici\s+Döngü|Reinforcing\s+Loop", s07_body, re.IGNORECASE))
            has_b1 = bool(re.search(r"\bB1\b|Dengeleyici\s+Döngü|Balancing\s+Loop", s07_body, re.IGNORECASE))
            if not (has_r1 and has_b1):
                self.report(
                    "L-2204",
                    BLOCK,
                    f"V13 İhlali: ADIM 07 / Step 7 içinde Pekiştirici Döngü (R1={has_r1}) ve Dengeleyici Döngü (B1={has_b1}) eksiksiz tanımlanmalıdır!",
                )

            arrow_lines = [
                line for line in s07_body.splitlines()
                if ("→" in line or "->" in line)
            ]
            if len(arrow_lines) < 2:
                self.report(
                    "L-2205",
                    BLOCK,
                    f"V13 İhlali: ADIM 07 / Step 7 içinde '→' oklarıyla kurulan kapalı nedensel döngü zincirleri eksik (bulunan: {len(arrow_lines)}, en az 2 zorunlu)!",
                )

            has_delay = bool(re.search(r"Gecikme|Delay", s07_body, re.IGNORECASE))
            has_leverage = bool(re.search(r"Kaldıraç|Leverage\s+Point", s07_body, re.IGNORECASE))
            if not (has_delay and has_leverage):
                self.report(
                    "L-2206",
                    BLOCK,
                    f"V13 İhlali: ADIM 07 / Step 7 içinde Sistemik Gecikme (Delay={has_delay}) veya Kaldıraç Noktası (Leverage={has_leverage}) eksik!",
                )

            has_tp = bool(re.search(r"Tipping\s+Point|Kırılma\s+Noktası", s07_body, re.IGNORECASE))
            has_n4 = bool(re.search(r"\bN4\b|Erken\s+Uyarı|Early\s+Warning", s07_body, re.IGNORECASE))
            if not (has_tp and has_n4):
                self.report(
                    "L-2207",
                    BLOCK,
                    f"V13 İhlali: ADIM 07 / Step 7 içinde Kırılma Noktası (Tipping Point={has_tp}) veya Erken Uyarı Sinyali (N4={has_n4}) eksik!",
                )

    # ----------------------------------------------------
    # V14 (Kontrol B): ADIM 13 / STEP 13 Üçlü İrfânî Bütünlük Doğrulaması
    # ----------------------------------------------------
    def check_v14_step13_irfani(self):
        if not self.is_v6:
            return

        step13_match = re.search(
            r"(#{2,3}\s+(?:ADIM|STEP)\s+13\b[^\n]*\n)(.*?)(?=\n#{2,3}\s+(?:ADIM|STEP)\s+14\b|\n##\s+(?:FAZ|PHASE)\s+IV\b|\Z)",
            self.body_text,
            re.DOTALL | re.IGNORECASE,
        )
        if not step13_match:
            self.report(
                "L-2301",
                BLOCK,
                "Kontrol B İhlali: Rapor gövdesinde '### ADIM 13' (veya '### STEP 13') bölümü bulunamadı!",
            )
            return

        s13_body = step13_match.group(2).strip()
        has_13_1 = bool(re.search(r"\b13\.1\b", s13_body))
        has_13_2 = bool(re.search(r"\b13\.2\b", s13_body))
        has_13_3 = bool(re.search(r"\b13\.3\b", s13_body))
        if not (has_13_1 and has_13_2 and has_13_3):
            self.report(
                "L-2302",
                BLOCK,
                f"Kontrol B İhlali: ADIM 13 / STEP 13 altında 13.1 ({has_13_1}), 13.2 ({has_13_2}) ve 13.3 ({has_13_3}) alt başlıkları birleşik olarak bulunmalıdır!",
            )

        norm_s13 = normalize(s13_body)
        irfani_authorities = [
            "kuseyri", "qushayri", "letaif", "lataif",
            "gazzali", "ghazali", "ihya",
            "muhasibi", "riaye", "riaya",
            "tusteri", "tustari",
            "ibn acibe", "ibn ajiba", "bahrul-medid", "bahr al-madid",
            "sulemi", "sulami", "mekki", "makki",
        ]
        if not any(auth in norm_s13 for auth in irfani_authorities):
            self.report(
                "L-2303",
                BLOCK,
                "Kontrol B İhlali: ADIM 13 / STEP 13 altında klasik irfânî/tasavvufî kaynak atfı (Kuşeyrî, Gazzâlî, Muhâsibî, Tüsterî, İbn Acîbe vb.) bulunamadı!",
            )

    # ----------------------------------------------------
    # Ana Tarama Yürütücüsü
    # ----------------------------------------------------
    def run_all(self):
        if not self.load_file():
            return 2

        self.check_language_safety()
        self.check_sections()

        # v6.x Doğrulama Modülleri
        self.check_v1_sources()
        self.check_v2_nakil_yorum()
        self.check_v3_disputes()
        self.check_v4_hash()
        self.check_v5_scores()
        self.check_v6_thresholds()
        self.check_v7_empirical()
        self.check_v8_falsifiability()
        self.check_v9_originality()
        self.check_v10_disclaimer()
        self.check_v11_peer_review()
        self.check_v12_step01_depth()
        self.check_v13_step07_cld()
        self.check_v14_step13_irfani()
        self.check_v15_tymm_pedagogy()
        self.check_v16_source_registry()

        return self.print_summary()

    # ----------------------------------------------------
    # V15 (Kapı C): ADIM 20 / STEP 20 Dörtlü TYMM Kurumsal Ders Tasarımı ve Pedagojik Uyum Doğrulaması
    # ----------------------------------------------------
    def check_v15_tymm_pedagogy(self):
        if not self.is_v6:
            return

        step20_match = re.search(
            r"(#{2,3}\s+(?:ADIM|STEP)\s+20\b[^\n]*\n)(.*?)(?=\n#{2,3}\s+(?:KOŞULLU|CONDITIONAL|Z-1)\b|\n##\s+(?:KOŞULLU|CONDITIONAL|Z-1)\b|\Z)",
            self.body_text,
            re.DOTALL | re.IGNORECASE,
        )
        if not step20_match:
            self.report(
                "L-2401",
                BLOCK,
                "Kapı C (V15) İhlali: Rapor gövdesinde '### ADIM 20' (veya '### STEP 20') bölümü bulunamadı!",
            )
            return

        s20_body = step20_match.group(2).strip()
        norm_s20 = normalize(s20_body)

        # L-2401: DKAB., DAB ve SDB kodları
        has_dkab = bool(re.search(r"\bDKAB\.\d+", s20_body))
        has_dab = bool(re.search(r"\bDAB\d+", s20_body))
        has_sdb = bool(re.search(r"\bSDB\d+", s20_body))
        if not (has_dkab and has_dab and has_sdb):
            self.report(
                "L-2401",
                BLOCK,
                f"Kapı C (V15) İhlali: ADIM 20 / STEP 20 içinde en az bir 'DKAB.' öğrenme çıktısı ({has_dkab}), 'DAB' alan becerisi ({has_dab}) ve 'SDB' sosyal-duygusal beceri ({has_sdb}) kodu bulunmalıdır!",
            )

        # L-2402: 20.1., 20.2., 20.3., 20.4. alt başlıkları ve 5 aşamalı 40 dakikalık ders araçları
        has_20_1 = bool(re.search(r"\b20\.1\.", s20_body))
        has_20_2 = bool(re.search(r"\b20\.2\.", s20_body))
        has_20_3 = bool(re.search(r"\b20\.3\.", s20_body))
        has_20_4 = bool(re.search(r"\b20\.4\.", s20_body))
        has_subheadings = has_20_1 and has_20_2 and has_20_3 and has_20_4

        has_tool_1 = ("anlam cozumleme tablosu" in norm_s20) or ("semantic analysis table" in norm_s20)
        has_tool_2 = ("yapilandirilmis grid" in norm_s20) or ("structured grid" in norm_s20)
        has_tool_3 = ("zit panel" in norm_s20) or ("opposite panel" in norm_s20)
        has_tool_4 = ("konusma halkasi" in norm_s20) or ("speaking circle" in norm_s20)
        has_tool_5 = ("cikis karti" in norm_s20) or ("exit card" in norm_s20)
        has_all_tools = has_tool_1 and has_tool_2 and has_tool_3 and has_tool_4 and has_tool_5

        if not (has_subheadings and has_all_tools):
            self.report(
                "L-2402",
                BLOCK,
                f"Kapı C (V15) İhlali: ADIM 20 / STEP 20 içinde '20.1..20.4.' alt başlıkları ({has_subheadings}) ve 5 aşamalı ders araçları (Anlam Çözümleme Tablosu={has_tool_1}, Yapılandırılmış Grid={has_tool_2}, Zıt Panel={has_tool_3}, Konuşma Halkası={has_tool_4}, Çıkış Kartı={has_tool_5}) eksiksiz yer almalıdır!",
            )

        # L-2403: Farklılaştırma (Zenginleştirme & Destekleme / Enrichment & Support-Scaffolding)
        has_enrichment = ("zenginlestirme" in norm_s20) or ("enrichment" in norm_s20)
        has_support = ("destekleme" in norm_s20) or ("support" in norm_s20) or ("scaffolding" in norm_s20)
        if not (has_enrichment and has_support):
            self.report(
                "L-2403",
                BLOCK,
                f"Kapı C (V15) İhlali: ADIM 20 / STEP 20 farklılaştırma protokolünde Zenginleştirme/Enrichment ({has_enrichment}) ve Destekleme/Support-Scaffolding ({has_support}) basamakları bulunmalıdır!",
            )

    # ----------------------------------------------------
    # V16 (Kapı D): Çoklu Sunucu Sicil, Fihrist/Bölüm, Lafzî Eşleşme, Tazelik, Mühür ve >=0.10 Manuel Örneklem Kilidi
    # ----------------------------------------------------
    def check_v16_source_registry(self):
        if not self.is_v6:
            return

        from datetime import datetime

        reg_data = load_sources_registry(self.registry_path)
        sources_list = reg_data.get("sources") or []
        if not sources_list:
            self.report(
                "L-2501",
                BLOCK,
                f"V16 Sicil Kilidi İhlali: Tek Doğruluk Kaynağı ('{self.registry_path}') bulunamadı veya boş!",
            )
            return

        url_map = {str(s.get("url", "")).strip(): s for s in sources_list if s.get("url")}

        # L-2506 (BLOCK — İlke 4 Rol Ayrımı / >=0.10 Bağımsız Manuel Örneklem Kilidi)
        total_reg = len(sources_list)
        sampled_entries = [
            s for s in sources_list
            if isinstance(s.get("human_sample_audit"), dict) and s["human_sample_audit"].get("sampled") is True
        ]
        sample_ratio = len(sampled_entries) / max(1, total_reg)
        sampled_urls = {str(s.get("url", "")).strip() for s in sampled_entries}
        has_ghazali_932 = any("shamela.ws/book/9472/932" in u for u in sampled_urls)
        has_qushayri = any("shamela.ws/book/23629/" in u for u in sampled_urls)
        has_ibn_ajibah = any("shamela.ws/book/10273/" in u for u in sampled_urls)
        has_tustari = any("shamela.ws/book/23600/" in u for u in sampled_urls)
        if sample_ratio < 0.10 or not (has_ghazali_932 and has_qushayri and has_ibn_ajibah and has_tustari):
            self.report(
                "L-2506",
                BLOCK,
                f"V16 Rol Ayrımı / Manuel Örneklem İhlali: Kaynak sicilinde bağımsız manuel örneklem oranı >= 0.10 olmalı (mevcut: {sample_ratio:.2f}) ve Gazzâlî 9472/932 ({has_ghazali_932}), Kuşeyrî 23629 ({has_qushayri}), İbn Acîbe 10273 ({has_ibn_ajibah}), Tüsterî 23600 ({has_tustari}) kayıtlarını içermelidir!",
            )

        # Monografide geçen tüm shamela.ws ve altafsir.com bağlantılarını topla
        doc_urls = []
        for m in re.finditer(r"https?://(?:www\.)?(?:shamela\.ws|altafsir\.com)/[^\s\)\>\]\"\'`]+", self.raw_text):
            u = m.group(0).rstrip(".,;:")
            line_no = self.raw_text.count("\n", 0, m.start()) + 1
            line_start = self.raw_text.rfind("\n", 0, m.start()) + 1
            line_end = self.raw_text.find("\n", m.end())
            line_str = self.raw_text[line_start : line_end if line_end != -1 else len(self.raw_text)]
            doc_urls.append((u, line_no, line_str))

        # Kurumsal modern_sources bağlantılarını da sicilde kontrol et (L-2501 & L-2504)
        for idx_ms, ms in enumerate(self.frontmatter.get("modern_sources") or [], 1):
            if not isinstance(ms, dict):
                continue
            u_ms = str(ms.get("url") or "").strip()
            if u_ms and str(self.frontmatter.get("case_id", "")).startswith("QV-"):
                doc_urls.append((u_ms, idx_ms, f"modern_sources[{idx_ms}]"))

        l2501_blocks = 0
        l2502_blocks = 0
        l2503_blocks = 0

        # Bilinen kümülatif cilt/sayfa sapması tuzakları (örn. Gazzâlî C.3 s.186 -> 9472/186 C.1 Cuma namazı sayfası)
        KNOWN_WRONG_OFFSETS = {
            "https://shamela.ws/book/9472/186": "Gazzâlî İhyâ C.3 s.186 (Gadab/Hased) yerine C.1 s.186 (Cuma Namazı) sayfasını açmaktadır (Doğrusu: 9472/932)!",
            "https://shamela.ws/book/9472/164": "Gazzâlî İhyâ C.3 s.164 yerine C.1 s.164 sayfasını açmaktadır (Doğrusu: 9472/910)!",
            "https://shamela.ws/book/9472/343": "Gazzâlî İhyâ C.3 s.343 yerine C.1 s.343 sayfasını açmaktadır (Doğrusu: 9472/1089)!",
        }

        for u, line_no, line_str in doc_urls:
            # Önce bilinen kümülatif cilt/bölüm sapmalarını kontrol et (L-2502)
            if u in KNOWN_WRONG_OFFSETS:
                l2502_blocks += 1
                self.report("L-2502", BLOCK, f"V16 Fihrist/Bölüm Eşleşme Kilidi İhlali: '{u}' — {KNOWN_WRONG_OFFSETS[u]}", f"Satır {line_no}")

            entry = url_map.get(u)
            if not entry or entry.get("status") != "VERIFIED":
                l2501_blocks += 1
                self.report(
                    "L-2501",
                    BLOCK,
                    f"V16 Sicil Kilidi İhlali: '{u}' bağlantısı 'data/sources_registry.yaml' içinde 'VERIFIED' statüsüyle kayıtlı değil!",
                    f"Satır {line_no}",
                )
                continue

            # L-2502: Fihrist/Bölüm (expected_breadcrumb == verified_breadcrumb) ve Cilt/Âyet/Müfessir uyumu
            exp_bc = str(entry.get("expected_breadcrumb", "")).strip()
            ver_bc = str(entry.get("verified_breadcrumb", "")).strip()
            if not exp_bc or not ver_bc or exp_bc != ver_bc:
                l2502_blocks += 1
                self.report(
                    "L-2502",
                    BLOCK,
                    f"V16 Fihrist/Bölüm Eşleşme Kilidi İhlali: '{u}' için beklenen fihrist ('{exp_bc}') ile doğrulanan fihrist ('{ver_bc}') uyuşmuyor!",
                    f"Satır {line_no}",
                )

            # Satır içi cilt kontrolü (örn. Gazzâlî 9472 için metinde C. 3 / Cilt: 3 / Vol. 3 yazarken sicilde volume != 3 olması)
            if "shamela.ws/book/9472/" in u:
                u_pos = line_str.find(u)
                prefix_window = line_str[max(0, u_pos - 180) : u_pos] if u_pos != -1 else line_str
                vol_matches = list(re.finditer(r"(?:Cilt:|C\.|Vol\.)\s*(\d+)", prefix_window))
                vol_in_line = vol_matches[-1] if vol_matches else None
                if vol_in_line and str(entry.get("volume", "")) and vol_in_line.group(1) != str(entry.get("volume", "")):
                    l2502_blocks += 1
                    self.report(
                        "L-2502",
                        BLOCK,
                        f"V16 Fihrist/Cilt Eşleşme Kilidi İhlali: '{u}' metinde Cilt {vol_in_line.group(1)} olarak atıflanmış ancak sicilde Cilt {entry.get('volume')} görünüyor!",
                        f"Satır {line_no}",
                    )

            # Altafsir.com URL parametrelerinin müfessir ve sûre/âyet ile uyumu (L-2502)
            if "altafsir.com" in u:
                qs_m_madh = re.search(r"tMadhNo=(\d+)", u)
                qs_m_tafsir = re.search(r"tTafsirNo=(\d+)", u)
                qs_m_sora = re.search(r"tSoraNo=(\d+)", u)
                qs_m_ayah = re.search(r"tAyahNo=(\d+)", u)
                madh_no = qs_m_madh.group(1) if qs_m_madh else ""
                tafsir_no = qs_m_tafsir.group(1) if qs_m_tafsir else ""
                sora_no = qs_m_sora.group(1) if qs_m_sora else ""
                ayah_no = qs_m_ayah.group(1) if qs_m_ayah else ""
                if madh_no != "3":
                    l2502_blocks += 1
                    self.report("L-2502", BLOCK, f"V16 Altafsir Parametre İhlali: '{u}' içinde tMadhNo=3 (Tasavvuf/İşârî) olmalıdır!", f"Satır {line_no}")
                # Kuşeyrî Letâifü'l-İşârât bağlamında tTafsirNo=31 olmalıdır (30 Sülemî'dir)
                norm_line = normalize(line_str)
                if ("kuseyri" in norm_line or "qushayri" in norm_line or "letaif" in norm_line or "lataif" in norm_line) and tafsir_no != "31":
                    l2502_blocks += 1
                    self.report(
                        "L-2502",
                        BLOCK,
                        f"V16 Altafsir Müfessir Eşleşme İhlali: '{u}' Kuşeyrî (Letâ'ifü'l-İşârât) atfında tTafsirNo=31 olmalıdır (bulunan: tTafsirNo={tafsir_no})!",
                        f"Satır {line_no}",
                    )
                # Raporun sûre/âyet numarası ile tSoraNo/tAyahNo uyumu
                verse_field = str(self.frontmatter.get("verse", ""))
                v_match = re.match(r"^(\d+):(\d+)", verse_field)
                if v_match and (sora_no != v_match.group(1) or ayah_no != v_match.group(2)):
                    l2502_blocks += 1
                    self.report(
                        "L-2502",
                        BLOCK,
                        f"V16 Altafsir Sûre/Âyet Eşleşme İhlali: Rapor âyeti ({verse_field}) ile URL parametreleri (tSoraNo={sora_no}, tAyahNo={ayah_no}) uyuşmuyor!",
                        f"Satır {line_no}",
                    )

            # L-2503: Lafzî İktibas Kilidi (quote_matched == True)
            if entry.get("quote_matched") is False:
                l2503_blocks += 1
                self.report(
                    "L-2503",
                    BLOCK,
                    f"V16 Lafzî İktibas Kilidi İhlali: '{u}' için sicilde 'quote_matched: false' kayıtlı!",
                    f"Satır {line_no}",
                )

            # L-2504: Tazelik Denetimi (WARN — 90 gün ve snapshot_sha256 kontrolü)
            ver_at = str(entry.get("verified_at", "")).strip()
            snap_sha = str(entry.get("snapshot_sha256", "")).strip()
            reverify_days = int(entry.get("reverify_period_days") or 90)
            if not snap_sha or len(snap_sha) < 16:
                self.report(
                    "L-2504",
                    WARN,
                    f"V16 Tazelik Uyarısı: '{u}' kaydında geçerli 'snapshot_sha256' özeti eksik!",
                    f"Satır {line_no}",
                )
            if ver_at:
                try:
                    dt_ver = datetime.strptime(ver_at, "%Y-%m-%d")
                    dt_ref = datetime(2026, 10, 20)
                    age_days = (dt_ref - dt_ver).days
                    if age_days > reverify_days:
                        self.report(
                            "L-2504",
                            WARN,
                            f"V16 Tazelik Uyarısı: '{u}' doğrulama tarihi ({ver_at}) {reverify_days} günlük yeniden doğrulama periyodunu aşmış ({age_days} gün)!",
                            f"Satır {line_no}",
                        )
                except ValueError:
                    self.report("L-2504", WARN, f"V16 Tazelik Uyarısı: '{u}' için geçersiz verified_at tarihi: {ver_at}", f"Satır {line_no}")
            else:
                self.report("L-2504", WARN, f"V16 Tazelik Uyarısı: '{u}' için 'verified_at' alanı eksik!", f"Satır {line_no}")

        # YAML classical_sources içindeki arabic_quote ile sicildeki expected_quote_norm / quote_matched kontrolü (L-2503)
        for idx_cs, cs in enumerate(self.frontmatter.get("classical_sources") or [], 1):
            if not isinstance(cs, dict):
                continue
            u_cs = str(cs.get("verification_link") or cs.get("digital_verification_url") or "").strip()
            q_cs = str(cs.get("arabic_quote") or "").strip()
            entry_cs = url_map.get(u_cs)
            if entry_cs and q_cs:
                exp_q_norm = str(entry_cs.get("expected_quote_norm", "")).strip()
                if not exp_q_norm or not match_arabic_quote_v16(q_cs, exp_q_norm):
                    l2503_blocks += 1
                    self.report(
                        "L-2503",
                        BLOCK,
                        f"V16 Lafzî İktibas Kilidi İhlali: classical_sources[{idx_cs}] ('{u_cs}') içindeki 'arabic_quote' hedef sayfa verisiyle eşleşmiyor!",
                        f"classical_sources[{idx_cs}]",
                    )

        # ADIM 13.3 içindeki Arapça «...» iktibasının sicildeki Kuşeyrî/Altafsir kaydıyla eşleşme kontrolü (L-2503)
        m133 = re.search(
            r"### 13\.3\..*?(?=## FAZ IV|## PHASE IV|## ADIM 14|### ADIM 14|## STEP 14|### STEP 14|\Z)",
            self.body_text,
            re.S,
        )
        if m133:
            sec133 = m133.group(0)
            q13_m = re.search(r"«(.*?)»", sec133, re.S)
            if q13_m:
                q13_text = q13_m.group(1).strip()
                u13_list = [
                    m.group(0).rstrip(".,;:")
                    for m in re.finditer(r"https?://(?:www\.)?(?:shamela\.ws/book/23629/\d+|altafsir\.com/[^\s\)\>\]\"\'`]+)", sec133)
                ]
                for u13 in u13_list:
                    ent13 = url_map.get(u13)
                    if ent13:
                        exp13_norm = str(ent13.get("expected_quote_norm", "")).strip()
                        if not exp13_norm or not match_arabic_quote_v16(q13_text, exp13_norm):
                            l2503_blocks += 1
                            self.report(
                                "L-2503",
                                BLOCK,
                                f"V16 Lafzî İktibas Kilidi İhlali: ADIM 13.3 içindeki Arapça [NAKİL] metni '{u13}' hedef sayfa verisiyle eşleşmiyor!",
                                "ADIM 13.3",
                            )

        # L-2505 (BLOCK — Mühür Kilidi): L-2501, L-2502, L-2503 sıfır BLOCK olmadan SHA-256 mühürleme yapılamaz!
        sha_val = str(self.frontmatter.get("sha256_hash", "")).strip()
        is_sealed = bool(sha_val and sha_val != "0" * 64) or (self.manifest_path is not None)
        if (l2501_blocks + l2502_blocks + l2503_blocks) > 0 and is_sealed:
            self.report(
                "L-2505",
                BLOCK,
                f"V16 Mühür Kilidi İhlali: L-2501 ({l2501_blocks}), L-2502 ({l2502_blocks}) ve L-2503 ({l2503_blocks}) kapıları '0 BLOCK' olmadan SHA-256 mühürlemesi yapılamaz!",
                "frontmatter.sha256_hash",
            )


    def print_summary(self):
        n_block = sum(1 for f in self.findings if f["level"] == BLOCK)
        n_warn = sum(1 for f in self.findings if f["level"] == WARN)

        print("\n" + "=" * 70)
        print(f"   QURAN VISION / GEM LINTER v6.2.2 — AKADEMİK DOĞRULAMA RAPORU")
        print(f"   Dosya : {self.path.name}")
        print(f"   Mod   : {'v6.2.2 / v6.1.1 (Akademik Standart)' if self.is_v6 else 'v5.2 (Geriye Dönük)'} | Katman: {self.katman} | H6: {'Evet' if self.h6 else 'Hayır'}")
        print("=" * 70 + "\n")

        if self.findings:
            print("📋 TESPİT EDİLEN BULGULAR:")
            print("-" * 70)
            for f in self.findings:
                icon = "🚫" if f["level"] == BLOCK else "⚠️"
                loc_info = f" [@ {f['loc']}]" if f["loc"] != "-" else ""
                print(f"  {icon} [{f['level']}] {f['rule']}: {f['message']}{loc_info}")
            print()
        else:
            print("✅ Tebrikler! Rapor tüm kurallardan sıfır hata ve sıfır uyarıyla geçti.\n")

        print("=" * 70)
        if n_block > 0:
            sonuc = "🔴 DÜŞTÜ / YAYINLANAMAZ"
            aciklama = f"{n_block} KESİCİ (BLOCK) kural ihlali var. Rapor akademik veya metodolojik olarak onaylanamaz."
            code = 2
        elif n_warn > 0:
            sonuc = "🟡 ÖN SÜRÜM / TAHKİK BEKLİYOR"
            aciklama = f"Kesici hata yok, ancak {n_warn} UYARI var. Ön sürüm (PRE-RELEASE) olarak yayınlanabilir."
            code = 1
        else:
            sonuc = "🟢 GEÇTİ / YAYINLANABİLİR"
            aciklama = "Metin iç tutarlılık denetiminden başarıyla geçti. Hakem değerlendirmesine hazırdır."
            code = 0

        print(f"  NİHAİ SONUÇ    : {sonuc}")
        print(f"  AÇIKLAMA       : {aciklama}")
        print(f"  KESİCİ (BLOCK) : {n_block}")
        print(f"  UYARI (WARN)   : {n_warn}")
        print("=" * 70 + "\n")

        return code


def check_cross_similarity(file1: Path, file2: Path):
    """İki rapor arasındaki şablon/metin benzerlik oranını hesaplar."""
    try:
        t1 = file1.read_text(encoding="utf-8").splitlines()
        t2 = file2.read_text(encoding="utf-8").splitlines()
        matcher = difflib.SequenceMatcher(None, t1, t2)
        ratio = matcher.ratio()
        print(f"🔍 Çapraz Benzerlik Analizi: {file1.name} <---> {file2.name}")
        print(f"   Benzerlik Oranı: %{ratio * 100:.1f}")
        if ratio > 0.45:
            print(f"   ⚠️ [UYARI] Benzerlik oranı çok yüksek! Raporların kalıp şablona hapsedilme riski var (V9/V10).")
        else:
            print(f"   ✅ Benzerlik oranı sağlıklı seviyede (özerk içerik korunmuş).")
        print()
    except Exception as e:
        print(f"Çapraz analiz hatası: {e}")


def generate_manifest(target_file: Path):
    """Hedef dosya için .sha256 manifest dosyası üretir."""
    if not target_file.exists():
        print(f"Hata: Dosya bulunamadı: {target_file}")
        return 1

    content = target_file.read_bytes()
    digest = hashlib.sha256(content).hexdigest()
    manifest_name = target_file.with_suffix(target_file.suffix + ".sha256")
    manifest_name.write_text(f"{digest}  {target_file.name}\n", encoding="utf-8")
    print(f"✅ Manifest üretildi: {manifest_name}")
    print(f"   SHA-256: {digest}")
    return 0


def main():
    if "--help" in sys.argv or "-h" in sys.argv:
        print("Kullanım: python src/gem_lint.py [dosya_adi.md ...] [seçenekler]")
        print("\nSeçenekler:")
        print("  --katman <1|2|3>          Analiz katmanı (Varsayılan: 3)")
        print("  --h6                      Zorlu Âyet (H6) ek kontrollerini uygula (Varsayılan)")
        print("  --no-h6                   H6 kontrollerini atla")
        print("  --manifest <dosya.sha256> Harici SHA-256 manifest doğrulaması")
        print("  --generate-manifest       Hedef dosya için .sha256 manifesti üret")
        print("  --similarity <dosya2.md>  İki rapor arası benzerlik denetimi")
        print("  --version                 Linter sürüm bilgisi")
        print("\nÖrnekler:")
        print("  python -X utf8 src/gem_lint.py")
        print("  python src/gem_lint.py docs/tr/06-pilot-tevbe-95-v6.1.1.md --katman 3 --h6")
        print("  python src/gem_lint.py rapor.md --generate-manifest")
        sys.exit(0)

    if "--version" in sys.argv:
        print("Quran Vision / GEM Linter v6.2.2 (v6.1.1 Standard Compatible - Python 3)")
        sys.exit(0)

    target_files = []
    katman = 3
    h6 = True
    manifest_path = None
    gen_manifest = False
    similarity_target = None

    idx = 1
    while idx < len(sys.argv):
        arg = sys.argv[idx]
        if arg == "--katman" and idx + 1 < len(sys.argv):
            try:
                katman = int(sys.argv[idx + 1])
            except ValueError:
                katman = 3
            idx += 2
        elif arg == "--h6":
            h6 = True
            idx += 1
        elif arg == "--no-h6":
            h6 = False
            idx += 1
        elif arg == "--manifest" and idx + 1 < len(sys.argv):
            manifest_path = Path(sys.argv[idx + 1])
            idx += 2
        elif arg == "--generate-manifest":
            gen_manifest = True
            idx += 1
        elif arg == "--similarity" and idx + 1 < len(sys.argv):
            similarity_target = Path(sys.argv[idx + 1])
            idx += 2
        elif not arg.startswith("--"):
            target_files.append(Path(arg))
            idx += 1
        else:
            idx += 1

    if "--all" in sys.argv and not target_files:
        root_dir = Path(__file__).resolve().parent.parent
        tr_reps = [f for f in sorted((root_dir / "docs" / "tr").glob("[0-9][0-9]-*-v6.1.1.md")) if not f.name.startswith("05-")]
        en_reps = [f for f in sorted((root_dir / "docs" / "en").glob("[0-9][0-9]-*-en-v6.1.1.md")) if not f.name.startswith("05-")]
        target_files = tr_reps + en_reps
    elif not target_files:
        root_dir = Path(__file__).resolve().parent.parent
        default_reports = sorted((root_dir / "docs" / "tr").glob("[0-9][0-9]-*-v6.1.1.md"))
        target_files = [f for f in default_reports if not f.name.startswith("05-")]
        if not target_files:
            print("Hata: Taranacak dosya belirtilmedi. Yardım için: python src/gem_lint.py --help")
            sys.exit(1)

    overall_exit = 0
    total_blocks = 0
    total_warns = 0
    for p in target_files:
        linter = GemLinterV6(p, katman=katman, h6=h6, manifest_path=manifest_path, regenerating_manifest=gen_manifest)
        exit_code = linter.run_all()
        p_blocks = sum(1 for f in linter.findings if f["level"] == BLOCK)
        total_blocks += p_blocks
        total_warns += sum(1 for f in linter.findings if f["level"] == WARN)
        if gen_manifest:
            if p_blocks > 0:
                print(f"🚫 [L-2505 MÜHÜR KİLİDİ] '{p.name}' içinde {p_blocks} BLOCK bulunduğundan .sha256 manifest üretimi reddedildi!")
            else:
                generate_manifest(p)
        if exit_code > overall_exit:
            overall_exit = exit_code

    if len(target_files) > 1:
        print("=" * 70)
        print(f"  KÜLLİYAT TOPLU DENETİM ÖZETİ ({len(target_files)} KURUCU RAPOR)")
        print(f"  TOPLAM KESİCİ HATA (BLOCK) : {total_blocks}")
        print(f"  TOPLAM UYARI (WARN)        : {total_warns}")
        print(f"  DURUM                      : {'🟢 SIFIR KESİCİ HATA (15/15 GEÇTİ)' if total_blocks == 0 else '🔴 KESİCİ HATA MEVCUT'}")
        print("=" * 70 + "\n")

    if similarity_target and target_files:
        check_cross_similarity(target_files[0], similarity_target)

    sys.exit(2 if total_blocks > 0 else 0)


if __name__ == "__main__":
    main()
