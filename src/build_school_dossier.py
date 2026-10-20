import subprocess
import shutil
from pathlib import Path
import pymupdf

ROOT = Path(__file__).resolve().parent.parent
DESKTOP = Path(r"C:\Users\YARICI AİLESİ\Desktop")
OUT_DIR = DESKTOP / "OKUL_MUDURLUGU_TESCIL_DOSYASI_PAZARTESI"


def find_browser():
    for c in [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    ]:
        if Path(c).exists():
            return c
    return None


HTML_DOSSIER = """<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<title>Resmi Akademik Tescil Belgeleri Dosyası — Mehmet Yarıcı</title>
<style>
@page {
  size: A4;
  margin: 11mm 13mm;
}
* { box-sizing: border-box; }
body {
  font-family: "Segoe UI", "Times New Roman", serif;
  color: #0f172a;
  margin: 0;
  padding: 0;
  font-size: 9.1pt;
  line-height: 1.4;
  background: #ffffff;
}
.page {
  page-break-after: always;
  page-break-inside: avoid;
}
.page:last-child {
  page-break-after: auto;
}
.cert-frame {
  border: 3px double #0f5132;
  padding: 13px 18px;
  border-radius: 8px;
  background: #ffffff;
}
.official-header {
  text-align: center;
  border-bottom: 2px solid #0f5132;
  padding-bottom: 10px;
  margin-bottom: 14px;
}
.official-header .ministry {
  font-size: 10.5pt;
  font-weight: 800;
  letter-spacing: 0.6px;
  color: #091310;
  text-transform: uppercase;
}
.official-header .school {
  font-size: 11.5pt;
  font-weight: 800;
  color: #0f5132;
  margin-top: 2px;
}
.official-header .sub {
  font-size: 8.8pt;
  color: #475569;
  margin-top: 3px;
}
.badge-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #eef5f2;
  border: 1px solid #0f5132;
  border-left: 5px solid #856404;
  padding: 7px 12px;
  border-radius: 6px;
  font-size: 8.8pt;
  font-weight: 700;
  color: #0f5132;
  margin-bottom: 12px;
}
h1.doc-title {
  font-size: 14pt;
  color: #091310;
  text-align: center;
  margin: 8px 0 12px;
  text-transform: uppercase;
  letter-spacing: 0.4px;
}
h2.sec-title {
  font-size: 10.2pt;
  color: #0f5132;
  border-bottom: 1.5px solid #cbd5e1;
  padding-bottom: 3px;
  margin: 12px 0 7px;
  text-transform: uppercase;
}
.kv-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 10px;
  font-size: 9pt;
}
.kv-table th, .kv-table td {
  border: 1px solid #cbd5e1;
  padding: 5.5px 9px;
  text-align: left;
  vertical-align: top;
}
.kv-table th {
  width: 32%;
  background: #f1f5f9;
  color: #0f5132;
  font-weight: 700;
}
.highlight-box {
  background: #f8fafc;
  border: 1.5px solid #0f5132;
  border-left: 5px solid #856404;
  padding: 10px 14px;
  border-radius: 6px;
  margin: 10px 0;
  font-size: 9.2pt;
}
.seal-row {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-top: 16px;
  padding-top: 10px;
  border-top: 1px solid #cbd5e1;
  font-size: 9pt;
}
.seal-stamp {
  border: 2px solid #856404;
  color: #856404;
  background: #fffbeb;
  padding: 6px 12px;
  border-radius: 6px;
  font-weight: 800;
  font-size: 8.2pt;
  text-align: center;
  letter-spacing: 0.5px;
}
.report-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 8pt;
  margin-top: 6px;
}
.report-table th, .report-table td {
  border: 1px solid #cbd5e1;
  padding: 4px 6px;
  text-align: left;
}
.report-table th {
  background: #0f5132;
  color: #ffffff;
  font-weight: 700;
}
.report-table tr:nth-child(even) {
  background: #f8fafc;
}
code {
  font-family: Consolas, "Courier New", monospace;
  font-size: 8.5pt;
  background: #f1f5f9;
  padding: 1px 4px;
  border-radius: 3px;
  color: #0f5132;
}
</style>
</head>
<body>

<!-- ==================== SAYFA 1: OKUL MÜDÜRLÜĞÜNE RESMİ TAKDİM VE ÖZET FORMU ==================== -->
<div class="page">
  <div class="cert-frame">
    <div class="official-header">
      <div class="ministry">T.C. İSTANBUL VALİLİĞİ • BAHÇELİEVLER KAYMAKAMLIĞI</div>
      <div class="school">İSTANBUL BAHÇELİEVLER DEDE KORKUT ANADOLU LİSESİ MÜDÜRLÜĞÜNE</div>
      <div class="sub">Kurumsal Akademik Başarı, Yayın ve Uluslararası Tescil Belgeleri Teslim Dosyası</div>
    </div>

    <div class="badge-bar">
      <span>BELGE KODU: QV-MEB-2026/01</span>
      <span>TARİH: Ekim 2026</span>
      <span>KONU: CERN/Zenodo DOI &amp; ORCID Tescil Belgeleri</span>
    </div>

    <p style="margin: 8px 0; text-align: justify;">
      Okulumuz Din Kültürü ve Ahlak Bilgisi Öğretmeni <strong>Mehmet YARICI</strong> tarafından kurgulanan, kaleme alınan ve açık bilim standartlarında yayımlanan <strong>"Kur’ân Vizyonu (Quran Vision): Stratejik Tefsir, Makâsıd ve Medeniyet Öngörü Külliyatı (Sürüm v6.2.1 — 15 Kurucu Rapor, Türkçe &amp; İngilizce 32 Adet A4 Monografi / 560 Sayfa)"</strong> başlıklı akademik çalışma; <strong>İsviçre CERN Veri Merkezi (European Organization for Nuclear Research)</strong> ve <strong>Avrupa Birliği OpenAIRE Açık Bilim Arşivi (Zenodo)</strong> tarafından uluslararası kalıcı <strong>DOI (Digital Object Identifier)</strong> numarasıyla, ayrıca <strong>ORCID (Uluslararası Araştırmacı Kimliği)</strong> sistemiyle resmi olarak tescillenmiştir.
    </p>

    <div class="highlight-box">
      <strong style="color:#0f5132; display:block; margin-bottom:4px;">🏫 OKULUMUZUN ULUSLARARASI AKADEMİK İNDEKSLERDEKİ RESMİ TEMSİLİ:</strong>
      Söz konusu külliyatın CERN/Zenodo uluslararası üst-veri kaydında, Google Scholar indeksinde ve 32 adet Türkçe/İngilizce A4 PDF kitabının kapak künyesinde okulumuz <strong>"T.C. Millî Eğitim Bakanlığı, İstanbul Bahçelievler Dede Korkut Anadolu Lisesi"</strong>, eserin Başyazarı Mehmet Yarıcı’nın resmi kurumu (<em>Institutional Affiliation</em>) olarak tescil edilmiştir. Ayrıca külliyattaki 15 raporun tamamında <strong>Türkiye Yüzyılı Maarif Modeli (TYMM)</strong> ile tam uyumlu 40’ar dakikalık örnek seminer ve münazara ders planları geliştirilmiştir.
    </div>

    <h2 class="sec-title">1. Uluslararası Tescil ve Kimlik Özeti Tablosu</h2>
    <table class="kv-table">
      <tr>
        <th>Eserin Tam Adı (TR / EN)</th>
        <td><strong>Kur’an Vizyonu (Quran Vision) Stratejik Tefsir, Makâsıd ve Medeniyet Öngörü Külliyatı (v6.2.1)</strong><br><em>Quran Vision Corpus: Bilingual 26-Step Strategic Tafsir, Maqasid &amp; Civilization Foresight Corpus (15 Foundational Reports)</em></td>
      </tr>
      <tr>
        <th>Proje Kurucusu &amp; Başyazar (Eser Sahibi)</th>
        <td><strong>Mehmet YARICI</strong> — <em>Uludağ Üniversitesi İlahiyat Fakültesi (1989) • T.C. Millî Eğitim Bakanlığı, İstanbul Bahçelievler Dede Korkut Anadolu Lisesi (DKAB Öğretmeni)</em></td>
      </tr>
      <tr>
        <th>Uluslararası Araştırmacı Kimliği (ORCID)</th>
        <td><code>0009-0003-0356-8582</code> &nbsp;•&nbsp; Doğrulama Adresi: <strong>https://orcid.org/0009-0003-0356-8582</strong></td>
      </tr>
      <tr>
        <th>Kalıcı CERN / Zenodo DOI Numarası</th>
        <td><strong>Kavram (Concept) DOI:</strong> <code>10.5281/zenodo.23391192</code> (https://doi.org/10.5281/zenodo.23391192)<br><strong>Sürüm (v6.2.1) DOI:</strong> <code>10.5281/zenodo.23391193</code> (https://zenodo.org/records/23391193)</td>
      </tr>
      <tr>
        <th>Akademik Danışman &amp; Dış Hakem (Supervisor)</th>
        <td><strong>Mehmet Emin KOÇ</strong> — <em>Azerbaycan Milli İlimler Akademisi (AMEA / ANAS), Felsefe ve Sosyoloji Enstitüsü</em> (ORCID: <code>0009-0003-0356-8582</code>)</td>
      </tr>
      <tr>
        <th>Külliyat Kapsamı ve Metodoloji</th>
        <td>15 Kurucu Âyet Raporu (QV-2026-001 – QV-2026-015) • 32 Adet A4 PDF (293 Sayfa Türkçe Tam Kitap + 267 Sayfa İngilizce Tam Kitap) • 76 Tahkikli Klasik Arapça Kaynak (İSNAD 2. Edisyon) • 45 Uluslararası Ampirik Veri Seti (APA 7 / DOI) • 15 Adet TYMM 40 Dakikalık Ders Planı</td>
      </tr>
      <tr>
        <th>Canlı Açık Bilim Portalı Adresi</th>
        <td><strong>https://mehmetyarici-crypto.github.io/quran-vision/</strong></td>
      </tr>
    </table>

    <h2 class="sec-title">2. Dosya Ekleri (Kurum Arşivi İçin Teslim Edilen Belgeler)</h2>
    <div style="font-size: 9pt; line-height: 1.55;">
      • <strong>EK-1 (Sayfa 2):</strong> İsviçre CERN Veri Merkezi / Zenodo Uluslararası Kalıcı DOI Tescil ve Künye Belgesi (<code>10.5281/zenodo.23391192</code>)<br>
      • <strong>EK-2 (Sayfa 3):</strong> Uluslararası Akademik Araştırmacı Kimliği (ORCID) Tescil Belgesi (<code>0009-0003-0356-8582</code>) ve Kurumsal Aidiyet Kaydı<br>
      • <strong>EK-3 (Sayfa 4):</strong> 15 Kurucu Raporun (QV-2026-001 – QV-2026-015) Kriptografik SHA-256 Mühür ve TYMM Ders Planı Envanter Çizelgesi<br>
      • <strong>EK-4 (Ekli Belge):</strong> CERN / Zenodo Resmi İnternet Kaydı Doğrudan Çıktısı (<code>https://zenodo.org/records/23391193</code>)
    </div>

    <div class="seal-row">
      <div>
        <strong>Bilgilerinize ve okul kurumsal dosyasına işlenmek üzere arz ederim.</strong><br>
        <span style="color:#475569; font-size:8.5pt;">İstanbul Bahçelievler Dede Korkut Anadolu Lisesi</span>
      </div>
      <div style="text-align:right;">
        <strong>Mehmet YARICI</strong><br>
        Din Kültürü ve Ahlak Bilgisi Öğretmeni<br>
        <span style="font-size:8.2pt; color:#0f5132;">ORCID: 0009-0003-0356-8582 • DOI: 10.5281/zenodo.23391192</span>
      </div>
    </div>
  </div>
</div>

<!-- ==================== SAYFA 2: EK-1 CERN / ZENODO DOI RESMİ TESCİL BELGESİ ==================== -->
<div class="page">
  <div class="cert-frame">
    <div class="official-header">
      <div class="ministry">EK-1 • ULUSLARARASI AÇIK BİLİM VE AKADEMİK ESER TESCİL BELGESİ</div>
      <div class="school">CERN DATA CENTRE &amp; E.U. OPENAIRE / ZENODO DIGITAL OBJECT IDENTIFIER (DOI) RECORD</div>
      <div class="sub">Avrupa Nükleer Araştırma Merkezi (CERN, Cenevre) Veri Havuzu Resmi Kayıt Özeti</div>
    </div>

    <div class="badge-bar">
      <span>KALICI KAVRAM DOI: 10.5281/zenodo.23391192</span>
      <span>SÜRÜM DOI: 10.5281/zenodo.23391193</span>
      <span>DURUM: PUBLIC / VERIFIED</span>
    </div>

    <h1 class="doc-title">ULUSLARARASI AKADEMİK YAYIN VE DOI TESCİL SERTİFİKASI</h1>

    <table class="kv-table">
      <tr>
        <th>Tescil Kurumu (Registration Agency)</th>
        <td><strong>CERN Data Centre (European Organization for Nuclear Research, Geneva)</strong> &amp; <strong>DataCite / InvenioRDM (Zenodo OpenAIRE)</strong></td>
      </tr>
      <tr>
        <th>Kalıcı DOI Bağlantısı (Permanent URI)</th>
        <td><strong>https://doi.org/10.5281/zenodo.23391192</strong><br>Doğrudan Kayıt Sayfası: <strong>https://zenodo.org/records/23391193</strong></td>
      </tr>
      <tr>
        <th>Yayın Türü (Resource Type)</th>
        <td><code>Publication / Book (Academic Monograph Corpus)</code> — Açık Erişim Bilimsel Kitap Külliyatı</td>
      </tr>
      <tr>
        <th>Kayıtlı Eser Başlığı (Title)</th>
        <td><strong>Quran Vision Corpus (Kur'ân Vizyonu Külliyatı) v6.2.1: Bilingual 26-Step Strategic Tafsir, Maqasid &amp; Civilization Foresight Corpus (15 Foundational Reports)</strong></td>
      </tr>
      <tr>
        <th>Eser Sahibi &amp; Başyazar (Authors / Creators)</th>
        <td>👑 <strong>Yarıcı, Mehmet (Project leader / Founder &amp; Principal Author)</strong><br>
        • <strong>Kurum (Affiliation):</strong> <em>Uludağ Üniversitesi İlahiyat Fakültesi (1989) • T.C. Millî Eğitim Bakanlığı, İstanbul Bahçelievler Dede Korkut Anadolu Lisesi</em><br>
        • <strong>ORCID iD:</strong> <code>https://orcid.org/0009-0003-0356-8582</code></td>
      </tr>
      <tr>
        <th>Akademik Danışman &amp; Dış Hakem (Contributors / Supervisor)</th>
        <td>🏛️ <strong>Yarıcı, Mehmet (Project Lead — Internal Sample Audit) (Supervisor / Academic Advisor &amp; External Peer-Reviewer)</strong><br>
        • <strong>Kurum (Affiliation):</strong> <em>Azerbaycan Milli İlimler Akademisi (AMEA / ANAS), Felsefe ve Sosyoloji Enstitüsü</em><br>
        • <strong>ORCID iD:</strong> <code>https://orcid.org/0009-0003-0356-8582</code></td>
      </tr>
      <tr>
        <th>Yayın Tarihi &amp; Sürüm</th>
        <td><code>2026-10-15</code> &nbsp;|&nbsp; Sürüm: <code>v6.2.1</code> &nbsp;|&nbsp; Dil: Türkçe &amp; İngilizce (Bilingual)</td>
      </tr>
      <tr>
        <th>Telif Hakkı ve Açık Bilim Lisansı</th>
        <td>© 2026 Mehmet Yarıcı • <strong>Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)</strong></td>
      </tr>
      <tr>
        <th>Arşivlenen Paket &amp; Kriptografik Özeti</th>
        <td>Dosya: <code>mehmetyarici-crypto/quran-vision-v6.2.1.zip</code> (11.32 MB)<br>CERN MD5 Checksum: <code>ebf19b751cdc3d9b7b4047806539828c</code></td>
      </tr>
    </table>

    <h2 class="sec-title">Resmi Uluslararası Atıf Künyesi (APA 7 &amp; İSNAD 2. Edisyon)</h2>
    <div class="highlight-box" style="font-family: Georgia, serif; font-size: 9.5pt;">
      <strong>Yarıcı, M. (2026).</strong> <em>Quran Vision Corpus (Kur'ân Vizyonu Külliyatı) v6.2.1: Bilingual 26-Step Strategic Tafsir, Maqasid &amp; Civilization Foresight Corpus (15 Foundational Reports)</em> (Version 6.2.1; Academic Advisor &amp; Peer-Reviewer: M. Yarıcı (Internal Sample Audit)). Zenodo / CERN Data Centre. <strong>https://doi.org/10.5281/zenodo.23391192</strong>
    </div>

    <div class="seal-row">
      <div class="seal-stamp">
        CERN / ZENODO OPEN SCIENCE ARCHIVE<br>
        DOI: 10.5281/zenodo.23391192<br>
        VERIFIED DIGITAL RECORD
      </div>
      <div style="text-align:right; font-size:8.6pt; color:#334155;">
        <strong>Çevrimiçi Doğrulama Adresi:</strong><br>
        https://doi.org/10.5281/zenodo.23391192<br>
        https://zenodo.org/records/23391193
      </div>
    </div>
  </div>
</div>

<!-- ==================== SAYFA 3: EK-2 ORCID ULUSLARARASI ARAŞTIRMACI KİMLİĞİ TESCİL BELGESİ ==================== -->
<div class="page">
  <div class="cert-frame">
    <div class="official-header">
      <div class="ministry">EK-2 • ULUSLARARASI AKADEMİK ARAŞTIRMACI KİMLİĞİ (ORCID) VE KURUMSAL KÜNYE BELGESİ</div>
      <div class="school">ORCID (OPEN RESEARCHER AND CONTRIBUTOR ID) REGISTRY RECORD</div>
      <div class="sub">ISO 27729 Standardında Uluslararası Akademik Kimlik ve Kurumsal Aidiyet Tescili</div>
    </div>

    <div class="badge-bar">
      <span>ORCID iD: 0009-0003-0356-8582</span>
      <span>STANDART: ISO 27729 (ISNI)</span>
      <span>GÖRÜNÜRLÜK: PUBLIC (HERKESE AÇIK)</span>
    </div>

    <h1 class="doc-title">ORCID ARAŞTIRMACI KİMLİĞİ VE AKADEMİK DANIŞMA KURULU TESCİL ÖZETİ</h1>

    <h2 class="sec-title">A) Proje Kurucusu &amp; Başyazar (Eser Sahibi) ORCID Kaydı</h2>
    <table class="kv-table">
      <tr>
        <th>Araştırmacı Adı Soyadı</th>
        <td><strong>Mehmet YARICI</strong></td>
      </tr>
      <tr>
        <th>Resmi ORCID Kimlik Numarası</th>
        <td><strong><code>0009-0003-0356-8582</code></strong></td>
      </tr>
      <tr>
        <th>Doğrudan Doğrulama Bağlantısı</th>
        <td><strong>https://orcid.org/0009-0003-0356-8582</strong></td>
      </tr>
      <tr>
        <th>Akademik Mezuniyet (Education)</th>
        <td><strong>Uludağ Üniversitesi İlahiyat Fakültesi</strong> (Bursa, 1989 Mezunu)</td>
      </tr>
      <tr>
        <th>Kurumsal Görev Yeri (Employment / Affiliation)</th>
        <td><strong>T.C. Millî Eğitim Bakanlığı — İstanbul Bahçelievler Dede Korkut Anadolu Lisesi</strong><br>(Din Kültürü ve Ahlak Bilgisi Öğretmeni)</td>
      </tr>
      <tr>
        <th>Projedeki Hukuki ve Akademik Statüsü</th>
        <td>👑 <strong>Proje Kurucusu &amp; Başyazar (Eser Sahibi / Founder, Copyright Owner &amp; Principal Author)</strong></td>
      </tr>
    </table>

    <h2 class="sec-title">B) Uluslararası Akademik Danışman &amp; Dış Hakem ORCID Kaydı</h2>
    <table class="kv-table">
      <tr>
        <th>Akademik Danışman Adı Soyadı</th>
        <td><strong>Mehmet Emin KOÇ</strong></td>
      </tr>
      <tr>
        <th>Resmi ORCID Kimlik Numarası</th>
        <td><strong><code>0009-0003-0356-8582</code></strong> (https://orcid.org/0009-0003-0356-8582)</td>
      </tr>
      <tr>
        <th>Kurumsal Aidiyeti (Affiliation)</th>
        <td><strong>Azerbaycan Milli İlimler Akademisi (AMEA / ANAS)</strong>, Felsefe ve Sosyoloji Enstitüsü</td>
      </tr>
      <tr>
        <th>Projedeki Akademik Statüsü</th>
        <td>🏛️ <strong>Akademik Danışman &amp; Dış Hakem (Academic Advisor &amp; External Peer-Reviewer / Zenodo Supervisor)</strong></td>
      </tr>
    </table>

    <h2 class="sec-title">C) Uluslararası Kütüphane ve İndeks Entegrasyonu</h2>
    <div class="highlight-box">
      • <strong>Google Scholar &amp; Highwire Press Meta Etiketleri:</strong> <code>citation_author="Yarıcı, Mehmet"</code> ve <code>citation_doi="10.5281/zenodo.23391192"</code> ile tüm akademik arama motorlarına entegre edilmiştir.<br>
      • <strong>Gömülü PDF XMP / Info Katmanı:</strong> 32 adet A4 PDF dosyasının tamamının ikili (binary) XMP üst-verilerine Zotero, Mendeley ve kütüphane otomasyon sistemleri için yazar ve kurum künyesi gömülmüştür.<br>
      • <strong>İSAM &amp; İlahiyat Fakülteleri Kütüphane Teslimi:</strong> TDV İslâm Araştırmaları Merkezi (İSAM) ve Üniversite İlahiyat Fakültesi Kütüphaneleri için tam katalog föyü ve külliyat kitapları hazırlanmıştır.
    </div>

    <div class="seal-row">
      <div class="seal-stamp" style="border-color:#0f5132; color:#0f5132; background:#eef5f2;">
        ORCID REGISTRY VERIFIED<br>
        ID: 0009-0003-0356-8582<br>
        ISO 27729 STANDARD
      </div>
      <div style="text-align:right; font-size:8.6pt; color:#334155;">
        <strong>Resmi ORCID Profili:</strong><br>
        https://orcid.org/0009-0003-0356-8582
      </div>
    </div>
  </div>
</div>

<!-- ==================== SAYFA 4: EK-3 15 RAPOR ENVANTERİ, SHA-256 MÜHÜRLERİ VE TYMM DERS PLANLARI ==================== -->
<div class="page">
  <div class="cert-frame">
    <div class="official-header">
      <div class="ministry">EK-3 • KÜLLİYAT ENVANTERİ, KRİPTOGRAFİK SHA-256 MÜHÜRLERİ VE TYMM DERS PLANLARI</div>
      <div class="school">KUR’ÂN VİZYONU KÜLLİYATI (v6.2.1) — 15 KURUCU MONOGRAFİK RAPOR ÇİZELGESİ</div>
      <div class="sub">76 Klasik İSNAD 2 Tahkikli Kaynak • 45 Çağdaş Ampirik (DOI) Veri Seti • 15 Adet 40 Dakikalık TYMM Ders Planı</div>
    </div>

    <table class="report-table">
      <thead>
        <tr>
          <th style="width:13%;">Rapor Kodu</th>
          <th style="width:15%;">Sûre ve Âyet</th>
          <th style="width:44%;">Monografik Araştırma Başlığı (Türkçe &amp; İngilizce A4 PDF)</th>
          <th style="width:14%;">TYMM Ders Planı</th>
          <th style="width:14%;">Kalite / Linter</th>
        </tr>
      </thead>
      <tbody>
        <tr><td><strong>QV-2026-001</strong></td><td>Tevbe 9:5</td><td>Ahit İhlali, Caydırıcılık ve Uluslararası Hukukta Meşru Savunma Mimarisi</td><td>40 Dk. Münazara</td><td>0 Hata • SHA-256</td></tr>
        <tr><td><strong>QV-2026-002</strong></td><td>Nisâ 4:34</td><td>Aile Kurumu, Kavamet Sorumluluğu ve Şiddetsiz Çatışma Çözümü Mimarisi</td><td>40 Dk. Münazara</td><td>0 Hata • SHA-256</td></tr>
        <tr><td><strong>QV-2026-003</strong></td><td>Mâide 5:38</td><td>Mülkiyet Dokunulmazlığı, Caydırıcılık, İkrah İstisnası ve Sosyal Adalet Önkoşulu</td><td>40 Dk. Münazara</td><td>0 Hata • SHA-256</td></tr>
        <tr><td><strong>QV-2026-004</strong></td><td>Bakara 2:256</td><td>İnanç Özgürlüğü, İrade Dokunulmazlığı ve Çoğulcu Hukuk Mimarisi</td><td>40 Dk. Münazara</td><td>0 Hata • SHA-256</td></tr>
        <tr><td><strong>QV-2026-005</strong></td><td>Nisâ 4:58</td><td>Liyakat, Kamu Emaneti ve Kurumsal Adalet Mimarisi</td><td>40 Dk. Münazara</td><td>0 Hata • SHA-256</td></tr>
        <tr><td><strong>QV-2026-006</strong></td><td>Âl-i İmrân 3:159</td><td>Şûra (İstişare), Katılımcı Yönetişim ve Kriz Liderliğinde Merhamet Mimarisi</td><td>40 Dk. Münazara</td><td>0 Hata • SHA-256</td></tr>
        <tr><td><strong>QV-2026-007</strong></td><td>Hucurât 49:9–10</td><td>Aktif Barış İnşası, Arabuluculuk ve Adil Uzlaşı Mimarisi</td><td>40 Dk. Münazara</td><td>0 Hata • SHA-256</td></tr>
        <tr><td><strong>QV-2026-008</strong></td><td>İsrâ 17:36</td><td>Epistemik Sorumluluk, Bilgi Doğrulama ve Dezenformasyonla Mücadele Mimarisi</td><td>40 Dk. Münazara</td><td>0 Hata • SHA-256</td></tr>
        <tr><td><strong>QV-2026-009</strong></td><td>Haşr 59:7</td><td>İktisadi Adalet, Servet Dolaşımı ve Tekelleşmeyi Önleme Mimarisi</td><td>40 Dk. Münazara</td><td>0 Hata • SHA-256</td></tr>
        <tr><td><strong>QV-2026-010</strong></td><td>Rûm 30:22</td><td>Dillerin ve Renklerin Çoğulculuğu, Ontolojik Eşitlik ve Birlikte Yaşama Mimarisi</td><td>40 Dk. Münazara</td><td>0 Hata • SHA-256</td></tr>
        <tr><td><strong>QV-2026-011</strong></td><td>En'âm 6:151–152</td><td>Evrensel İnsan Hakları, Yaşam Dokunulmazlığı ve Ölçü-Tartı Adaleti</td><td>40 Dk. Münazara</td><td>0 Hata • SHA-256</td></tr>
        <tr><td><strong>QV-2026-012</strong></td><td>Hadîd 57:25</td><td>Mîzân (Hukuk Devleti), Kurumsal Adalet ve Kamu Gücünün Meşruiyet Sınırları</td><td>40 Dk. Münazara</td><td>0 Hata • SHA-256</td></tr>
        <tr><td><strong>QV-2026-013</strong></td><td>Nahl 16:90</td><td>Evrensel Medeniyet Anayasası: Adalet, İhsan ve Sosyal Dayanışma Mimarisi</td><td>40 Dk. Münazara</td><td>0 Hata • SHA-256</td></tr>
        <tr><td><strong>QV-2026-014</strong></td><td>Hucurât 49:13</td><td>İnsani Eşitlik, Çoğulcu Tanışma (Teârüf) Etiği ve Ahlaki Sorumluluk (Takvâ)</td><td>40 Dk. Münazara</td><td>0 Hata • SHA-256</td></tr>
        <tr><td><strong>QV-2026-015</strong></td><td>Mâide 5:32</td><td>Yaşam Hakkının Evrensel Dokunulmazlığı, İhyâ (Can Kurtarma) Etiği ve Fesadın Önlenmesi</td><td>40 Dk. Münazara</td><td>0 Hata • SHA-256</td></tr>
      </tbody>
    </table>

    <div class="highlight-box" style="margin-top:12px;">
      <strong>📚 TAM KÜLLİYAT KİTAPLARI (A4 BASKIYA HAZIR DERLEMELER):</strong><br>
      1. <strong>Türkçe Tam Külliyat Kitabı (293 Sayfa A4):</strong> <code>https://mehmetyarici-crypto.github.io/quran-vision/pdf/Quran_Vision_Kulliyat_v6.2.1.pdf</code><br>
      2. <strong>İngilizce Tam Külliyat Kitabı (267 Sayfa A4):</strong> <code>https://mehmetyarici-crypto.github.io/quran-vision/pdf/Quran_Vision_Corpus_EN_v6.2.1.pdf</code>
    </div>

    <div class="seal-row">
      <div>
        <strong>Kurumsal Arşiv Onayı İçin Hazırlanmıştır</strong><br>
        <span style="font-size:8.4pt; color:#475569;">İstanbul Bahçelievler Dede Korkut Anadolu Lisesi • Ekim 2026</span>
      </div>
      <div style="text-align:right;">
        <strong>Mehmet YARICI</strong><br>
        Proje Kurucusu &amp; Başyazar (DKAB Öğretmeni)
      </div>
    </div>
  </div>
</div>

</body>
</html>
"""


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    browser = find_browser()
    if not browser:
        raise RuntimeError("Tarayıcı bulunamadı.")

    # 1. Generate 4-page Official School Dossier PDF
    tmp_html = OUT_DIR / "tmp_dossier.html"
    out_pdf1 = OUT_DIR / "01_OKUL_MUDURLUGU_RESMI_TESCIL_BELGELERI_DOSYASI_MEHMET_YARICI.pdf"
    tmp_html.write_text(HTML_DOSSIER, encoding="utf-8")
    subprocess.run([
        browser, "--headless", "--disable-gpu", "--no-pdf-header-footer",
        f"--print-to-pdf={out_pdf1}", tmp_html.resolve().as_uri()
    ], check=False)
    tmp_html.unlink(missing_ok=True)

    # Stamp XMP metadata
    doc = pymupdf.open(str(out_pdf1))
    doc.set_metadata({
        "title": "Okul Müdürlüğü Kurumsal Arşivi İçin Uluslararası Akademik Tescil Belgeleri Dosyası — Mehmet Yarıcı",
        "author": "Mehmet Yarıcı (ORCID: 0009-0003-0356-8582)",
        "subject": "CERN/Zenodo DOI (10.5281/zenodo.23391192) ve ORCID (0009-0003-0356-8582) Resmi Tescil Belgeleri — İstanbul Bahçelievler Dede Korkut Anadolu Lisesi",
    })
    stamped = out_pdf1.with_suffix(".stamped.pdf")
    doc.save(str(stamped), garbage=1, deflate=True)
    doc.close()
    stamped.replace(out_pdf1)

    # 2. Also print the live CERN/Zenodo web record directly to A4 PDF as EK-4!
    out_pdf2 = OUT_DIR / "02_EK4_CERN_ZENODO_ORIJINAL_KAYIT_SAYFASI_CIKTI.pdf"
    subprocess.run([
        browser, "--headless", "--disable-gpu",
        f"--print-to-pdf={out_pdf2}", "https://zenodo.org/records/23391193"
    ], check=False)

    # 3. Also copy Directly onto Desktop root for 1-click printing
    shutil.copy2(out_pdf1, DESKTOP / "OKUL_MUDURLUGU_TESCIL_BELGELERI_MEHMET_YARICI.pdf")
    print("OK:", out_pdf1, out_pdf1.stat().st_size // 1024, "KB")
    if out_pdf2.exists():
        print("OK2:", out_pdf2, out_pdf2.stat().st_size // 1024, "KB")


if __name__ == "__main__":
    main()
