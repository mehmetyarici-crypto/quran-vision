#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
III. Maarif Kongresi (25-27 Kasım 2026, Başvuru Kodu: MOIJUB)
1) Ek-1 Genişletilmiş Bildiri Özeti (500-750 Kelime)
2) Tam Metin Bildiri Kitapçığı (docs/pdf/III_MAARIF_KONGRESI_TAM_METIN_MOIJUB.pdf)
2026 Türkiye Yüzyılı Maarif Modeli DKAB Öğretim Programları (TTKB 03.03.2026 / Sayı: 4 ve 5)
ve Quran Vision v6.2.2 (V15 Pedagojik + V16.2 Çoklu Sunucu Doğrulama Sicili) Uyumlu Sürüm.
"""

from pathlib import Path
import re
import shutil
import subprocess
import docx
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING

ROOT = Path(__file__).resolve().parent.parent
DESKTOP = Path(r"C:\Users\YARICI AİLESİ\Desktop")
PDF_DIR = ROOT / "docs" / "pdf"

TITLE = (
    "KLASİK TEFSİR MİRASINDAN GELECEK TASAVVURUNA: DİN VE AHLAK ÖĞRETİMİNDE "
    "YİRMİ ALTI ADIMLI MODEL"
)

APPLICATION_META = [
    ("Başvuru Kodu", "MOIJUB"),
    ("Müellif", "Mehmet Yarıcı (Uludağ Üniv. İlahiyat Fak., 1989 • T.C. MEB İstanbul Bahçelievler Dede Korkut Anadolu Lisesi • ORCID: 0009-0003-0356-8582)"),
    ("Başvuru Tarihi ve Sürüm", "20 Ekim 2026 • Quran Vision v6.2.2 (DOI: 10.5281/zenodo.23410818)"),
    ("Başvurunun Teması", "Eğitim Yoluyla Kültür, Medeniyet ve Kimlik İnşasında Öğretmenin Rolü"),
    ("Başvuru Takip Adresi", "https://bildiri-maarifkongresi.eba.gov.tr/applications/MOIJUB"),
]

SECTIONS_WITHOUT_REF = [
    (
        "ANAHTAR KELİMELER",
        None,
        "Türkiye Yüzyılı Maarif Modeli, Din Kültürü ve Ahlak Bilgisi Öğretimi, "
        "Dinî Metinleri Yorumlama ve Tahlil Etme, Çoklu Sunucu Dijital Kaynak Doğrulama",
    ),
    (
        "GİRİŞ",
        None,
        "Eğitim, bir toplumun yalnızca bilgi ve beceri birikimini yeni kuşaklara aktaran bir alan değil; kültürel hafızasını, "
        "değer dünyasını, insan anlayışını ve gelecek tasavvurunu şekillendiren temel bir medeniyet unsurudur. Millî Eğitim "
        "Bakanlığı Talim ve Terbiye Kurulu Başkanlığının 2026 yılı kararlarıyla güncellenerek uygulamaya konulan Türkiye "
        "Yüzyılı Maarif Modeli Ortaöğretim (9–12. Sınıflar) ile İlkokul-Ortaokul (4–8. Sınıflar) Din Kültürü ve Ahlak Bilgisi "
        "Dersi Öğretim Programları; öğrenciyi bilgi, duygu ve davranış bütünlüğüne ulaştırmayı hedefleyen 'Erdem-Değer-Eylem' "
        "yaklaşımı üzerine yapılandırılmıştır. Programlarda olgusal gerçekliğin bilgisini teolojik bilgi ile bütünleştiren ve "
        "bunu analitik bir yöntemle çözümleyen anlamlı bir öğrenme süreci öngörülmekte; bu süreç 'Temel Kaynakları Kullanma "
        "(DAB1)', 'Tetkik (DAB2)', 'Tahkik (DAB3)', 'Tefekkür (DAB4)', 'Dinî Delillere Başvurma (DAB5)' ve 'Tatbik (DAB6)' "
        "alan becerileriyle desteklenmektedir. Özellikle 12. sınıfta yer alan 'Kur’an-ı Kerim’in anlaşılmasında temel ilkeleri "
        "özetleyebilme (DKAB.12.1.3)' ve 'Güncel dinî meselelerin çözümünde temel ilke ve yöntemleri özetleyebilme "
        "(DKAB.12.3.1)' öğrenme çıktıları; ayetlerin Hz. Peygamber’in açıklamaları, bütüncül bakış, tarihsel bağlam, "
        "nüzul sebepleri ve zaruratıhamse (can, nesil, akıl, mal ve din emniyeti) ilkeleri ışığında anlaşılmasını esas "
        "almaktadır. Dijital çağda öğrencilerin ayetlere bağlamından koparılmış kesitler üzerinden maruz kalması, programdaki "
        "bu ilkeleri somutlaştıracak yapılandırılmış öğretim tasarımlarını zorunlu kılmaktadır.",
    ),
    (
        "ÇALIŞMANIN AMACI VE ÖNEMİ",
        None,
        "Bu çalışmanın amacı; 2026 Din Kültürü ve Ahlak Bilgisi Dersi Öğretim Programlarında yer alan 'Dinî Kavramları "
        "Bağlamına Uygun Kullanma (DAB3.2)', 'Dinî Metinleri Yorumlama (DAB3.3)', 'Dinî Metinleri Tahlil Etme (DAB3.4)' ve "
        "'Dinî Konularda Analitik Düşünme (DAB4.4)' süreç bileşenlerini sınıf ortamında hayata geçirmek üzere geliştirilen "
        "'Yirmi Altı Adımlı Stratejik Tefsir ve Öğretim Tasarımı Modeli'ni (Quran Vision v6.2.2) tanıtmak ve modelin öğrenme-öğretme "
        "yaşantılarına katkısını ortaya koymaktır. Literatürdeki mevcut çalışmalar çoğunlukla kuramsal öneri düzeyinde kalırken; bu araştırma "
        "tamamlanmış on beş kurucu ayet monografisi (34 A4 PDF külliyatı), kural tabanlı pedagojik ve çoklu sunucu kaynak doğrulama "
        "yazılımı (V1–V16), çift dilli dijital öğrenme platformu ve her ünite için doğrudan uygulanabilir kırkar dakikalık ders planları "
        "sunması bakımından özgün bir uygulama örneği teşkil etmektedir.",
    ),
    (
        "YÖNTEM",
        None,
        "Araştırmada, eğitim bilimleri ilkeleri ile öğretim materyali geliştirmeyi birleştiren tasarım tabanlı araştırma "
        "deseni ve nitel doküman analizi yöntemi kullanılmıştır. Çalışmanın veri setini, 2026 öğretim programlarındaki "
        "öğrenme çıktılarıyla doğrudan örtüşen on beş kurucu Kur’an-ı Kerim ayeti oluşturmaktadır: bilgi ve doğrulama "
        "sorumluluğu (İsra 17:36; DKAB.10.1.3), emanet, liyakat, adalet ve ihsan (Nisa 4:58 ve Nahl 16:90; DKAB.10.3.4), "
        "insanlığın eşitliği ve tanışma ahlakı (Hucurat 49:13 ve Rum 30:22; DKAB.10.5.3), toplumsal barış ve kardeşlik "
        "(Hucurat 49:9–10; DKAB.12.4.5), temel insan hakları ve ölçü-tartı dürüstlüğü (Enam 6:151–152; DKAB.12.3.5), "
        "inanç özgürlüğü (Bakara 2:256), istişare (Al-i İmran 3:159), aile içi merhamet ve sorumluluk (Nisa 4:34; DKAB.12.2.1), "
        "servetin adil dolaşımı (Haşr 59:7), hukuk ve adalet dengesi (Hadid 57:25; DKAB.11.4.4) ile yaşam hakkının "
        "dokunulmazlığı (Maide 5:32; DKAB.8.3.1). Beş aşamalı öğretim tasarımı; (1) Lafzî çözümleme ve yedi boyutlu "
        "bağlam matrisi, (2) Zaruratıhamse ve seddizerai ilkeleriyle güncel gerçeklik arasında köprü kurma, (3) Din "
        "istismarını önleyici eleştirel sorgulama (DKAB.11.4.3), (4) Öz düzenleme (SDB1.2) ve sorumlu karar verme "
        "(SDB3.3) muhasebesi, (5) Kırk dakikalık öğrenme-öğretme uygulaması adımlarından oluşmaktadır.",
    ),
    (
        "BULGULAR",
        None,
        "Modelin on beş ayet üzerindeki uygulanması sonucunda üç temel bulguya ulaşılmıştır: Birincisi, Taberî, Matüridî, "
        "Râzî, Kurtubî, Şâtıbî, İbn Âşûr, Kuşeyrî ve Gazzâlî gibi temel kaynaklardan doğrulanan yüz yirmi yedi Şâmile ve on beş "
        "Altafsir işârî tefsir naklinin otuz dört tekil kurumsal veri setiyle (toplam yüz yetmiş altı doğrulanmış kaynak sicili) "
        "eşleştirilmesi, öğrencilerde 'Bilgi Okuryazarlığı (OB1)' ve 'Gerçeği Arama (E3.4)' eğilimini güçlendirerek doğrudan kaynak "
        "nakli ile beşerî yorum arasındaki sınırı somutlaştırmıştır. İkincisi, anlam çözümleme tablosu, yapılandırılmış grid, zıt panel, "
        "konuşma halkası ve çıkış kartı araçlarıyla yapılandırılan kırk dakikalık ders modüllerinin (V15 L-2401..L-2403); ön değerlendirme, "
        "köprü kurma, öğrenme kanıtları ile zenginleştirme ve destekleme basamaklarını eksiksiz karşıladığı görülmüştür. Üçüncüsü, "
        "çoklu sunucu doğrulama sicili (V16 L-2501..L-2506) sayesinde kümülatif cilt ofseti ve parametre hatalarının sıfır kesici "
        "hatayla önlendiği tespit edilmiştir.",
    ),
    (
        "SONUÇ VE ÖNERİLER",
        None,
        "Sonuç olarak geliştirilen yirmi altı adımlı öğretim tasarımı; öğretmeni bilgiyi salt aktaran konumdan çıkararak, "
        "temel dinî kaynaklar ile çağdaş toplumsal gerçeklik arasında sahih köprüler kuran bir uzman ve rehber konumuna "
        "taşımaktadır. Araştırma bulguları doğrultusunda şu öneriler sunulmuştur: (1) Ortaöğretim ve ortaokul ders "
        "kitaplarındaki 'Kur’an’dan Mesajlar' bölümlerinde ayetin öncesi, sonrası, nüzul sebebi ve zaruratıhamse boyutunu "
        "bütünleştiren anlam çözümleme tablolarına yer verilmelidir; (2) İsra suresi 36. ayet (DKAB.10.1.3) kapsamında "
        "dijital bilgi doğrulama etkinlikleri okul temelli planlama saatlerinde uygulanmalıdır; (3) Geliştirilen kırk "
        "dakikalık münazara, zıt panel ve çıkış kartı e-içerikleri Eğitim Bilişim Ağı üzerinden zümre öğretmenlerinin "
        "erişimine açılmalıdır.",
    ),
]

REFERENCES = [
    "Gazzâlî, E. H. (2004). İhyâ’u ‘ulûmi’d-dîn (Cilt 1–4). Beyrut: Dârü’l-Ma‘rife.",
    "İbn Âşûr, M. T. (1984). et-Tahrîr ve’t-tenvîr (Cilt 1–30). Tunus: ed-Dârü’t-Tûnisiyye li’n-Neşr.",
    "Kuşeyrî, A. (1981). Letâ’ifü’l-işârât (İ. Besyûnî, Ed.; Cilt 1–3). Kahire: el-Hey’etü’l-Mısriyyetü’l-Âmme li’l-Kitâb.",
    "Matüridî, E. M. (2005). Te’vîlâtü Ehli’s-Sünne (B. Topaloğlu, Ed.; Cilt 1–17). İstanbul: Dârü’l-Mîzân.",
    "Millî Eğitim Bakanlığı [MEB]. (2024). Türkiye Yüzyılı Maarif Modeli öğretim programları ortak metni. Ankara: MEB Talim ve Terbiye Kurulu Başkanlığı.",
    "Millî Eğitim Bakanlığı [MEB]. (2026a). İlkokul-ortaokul ve imam hatip ortaokulu Din Kültürü ve Ahlak Bilgisi dersi (4–8. sınıflar) öğretim programı (TTKB 03.03.2026 tarih ve 4 sayılı kararı). Ankara: MEB Yayınları.",
    "Millî Eğitim Bakanlığı [MEB]. (2026b). Ortaöğretim Din Kültürü ve Ahlak Bilgisi dersi (9–12. sınıflar) öğretim programı (TTKB 03.03.2026 tarih ve 5 sayılı kararı). Ankara: MEB Yayınları.",
    "Şâtıbî, İ. (1997). el-Muvâfakât fî usûli’ş-şerîa (M. H. Âl-i Selmân, Ed.; Cilt 1–6). Riyad: Dâru İbni Affân.",
    "Yarıcı, M. (2026). Kur’ân Vizyonu (Quran Vision): 26 Adımlı Kanıta Dayalı Stratejik Tefsir, Makâsıd ve Medeniyet Öngörü Külliyatı (Sürüm v6.2.2; 15 Monografi ve 34 A4 PDF). Zenodo. https://doi.org/10.5281/zenodo.23410818",
]


def count_words(text: str) -> int:
    return len(text.split())


def build_full_paper_html(isra_step20_md: str) -> str:
    """
    III. Maarif Kongresi (MOIJUB) Tam Metin Bildiri Kitapçığı HTML şablonunu üretir.
    V16.2 çoklu sunucu doğrulama sicili (176/176 kaynak: 127 Şâmile + 15 Altafsir + 34 Kurumsal DOI),
    Gazzâlî 9472/186 -> 932 kümülatif cilt ofseti ve Kuşeyrî Altafsir tTafsirNo=31 regresyon vakası,
    İlke 4 rol ayrımı şeffaflık notu ve İsrâ 17:36 (DKAB.10.1.3) tam ders tasarımını içerir.
    """
    abstract_blocks = "".join(
        f"<div class='sec-sub'>{h}</div><p>{b}</p>" for h, _, b in SECTIONS_WITHOUT_REF
    )
    refs_html = "".join(f"<p class='ref-item'>{r}</p>" for r in REFERENCES)

    # Convert Isra 17:36 Step 20 markdown lines to clean HTML paragraphs/tables
    step20_lines = []
    in_table = False
    for raw_line in isra_step20_md.splitlines():
        line = raw_line.strip()
        if line.startswith("|"):
            if "---" in line:
                continue
            cells = [c.strip() for c in line.split("|")[1:-1]]
            if not in_table:
                in_table = True
                step20_lines.append("<table><thead><tr>" + "".join(f"<th>{c}</th>" for c in cells) + "</tr></thead><tbody>")
            else:
                step20_lines.append("<tr>" + "".join(f"<td>{c}</td>" for c in cells) + "</tr>")
            continue
        elif in_table:
            in_table = False
            step20_lines.append("</tbody></table>")

        if line.startswith("### "):
            step20_lines.append(f"<h3>{line[4:]}</h3>")
        elif line.startswith("#### "):
            step20_lines.append(f"<h4>{line[5:]}</h4>")
        elif line.startswith("- "):
            step20_lines.append(f"<p style='margin-left:14pt;'>• {line[2:]}</p>")
        elif line:
            step20_lines.append(f"<p>{line}</p>")
    if in_table:
        step20_lines.append("</tbody></table>")
    step20_html = "\n".join(step20_lines)
    step20_html = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", step20_html)
    step20_html = re.sub(r"`([^`]+)`", r"<code>\1</code>", step20_html)

    return f"""<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<title>III. Maarif Kongresi Tam Metin Bildirisi (MOIJUB) — Mehmet Yarıcı (2026)</title>
<style>
  @page {{ size: A4; margin: 2.0cm; }}
  body {{
    font-family: "Times New Roman", Times, serif;
    font-size: 11.2pt;
    line-height: 1.48;
    text-align: justify;
    color: #111827;
    margin: 0;
  }}
  .header-banner {{
    border: 2px solid #0f5132;
    background: #f4f9f6;
    padding: 12pt 14pt;
    border-radius: 6pt;
    margin-bottom: 14pt;
  }}
  .title {{
    font-size: 14.5pt;
    font-weight: bold;
    text-align: center;
    text-transform: uppercase;
    color: #064e3b;
    margin-bottom: 8pt;
  }}
  .meta-box {{
    border: 1px solid #cbd5e1;
    background-color: #ffffff;
    padding: 8pt 10pt;
    border-radius: 4pt;
    font-size: 10pt;
    line-height: 1.4;
  }}
  h2 {{
    font-size: 12.5pt;
    font-weight: bold;
    text-transform: uppercase;
    color: #0f5132;
    border-bottom: 1.5px solid #0f5132;
    padding-bottom: 3pt;
    margin-top: 16pt;
    margin-bottom: 8pt;
  }}
  h3 {{
    font-size: 11.5pt;
    font-weight: bold;
    color: #1e293b;
    margin-top: 12pt;
    margin-bottom: 4pt;
  }}
  h4 {{
    font-size: 11pt;
    font-weight: bold;
    color: #065f46;
    margin-top: 10pt;
    margin-bottom: 4pt;
  }}
  .sec-sub {{
    font-weight: bold;
    color: #0f5132;
    margin-top: 8pt;
    margin-bottom: 2pt;
  }}
  p {{
    margin-top: 0;
    margin-bottom: 7pt;
    text-align: justify;
  }}
  table {{
    width: 100%;
    border-collapse: collapse;
    margin: 8pt 0 12pt;
    font-size: 9.5pt;
  }}
  th, td {{
    border: 1px solid #94a3b8;
    padding: 5pt 6pt;
    text-align: left;
    vertical-align: top;
  }}
  th {{
    background: #eef5f2;
    color: #064e3b;
    font-weight: bold;
  }}
  code {{
    font-family: "Courier New", monospace;
    font-size: 9.5pt;
    background: #f1f5f9;
    padding: 1pt 3pt;
    border-radius: 2pt;
  }}
  .callout {{
    border-left: 3.5pt solid #856404;
    background: #fffbeb;
    padding: 8pt 10pt;
    margin: 10pt 0;
    font-size: 10.2pt;
  }}
  .ref-item {{
    margin-bottom: 4pt;
    padding-left: 1cm;
    text-indent: -1cm;
    font-size: 10.2pt;
  }}
</style>
</head>
<body>
  <div class="header-banner">
    <div style="font-size:9.5pt; font-weight:bold; color:#856404; text-align:center; margin-bottom:4pt;">
      T.C. MİLLÎ EĞİTİM BAKANLIĞI • III. MAARİF KONGRESİ (25–27 KASIM 2026) • TAM METİN BİLDİRİ VE TEKNİK DOĞRULAMA DOSYASI
    </div>
    <div class="title">{TITLE}</div>
    <div class="meta-box">
      {"".join(f"<div><strong>{k}:</strong> {v}</div>" for k, v in APPLICATION_META)}
      <div><strong>Külliyat ve Açık Bilim Envanteri:</strong> 15 Kurucu Âyet Monografisi (15 TR + 15 EN = 30 Rapor) • 34 A4 PDF • 176/176 Doğrulanmış Çoklu Sunucu Kaynağı (<code>127 Şâmile + 15 Altafsir + 34 Kurumsal DOI/URL</code>)</div>
    </div>
  </div>

  <h2>BÖLÜM 1 — EBA SİSTEMİ GENİŞLETİLMİŞ BİLDİRİ ÖZETİ (EK-1 ŞABLONU)</h2>
  {abstract_blocks}

  <h2>BÖLÜM 2 — QURAN VISION v6.2.2 METODOLOJİK MİMARİSİ: V15 PEDAGOJİK VE V16.2 ÇOKLU SUNUCU KALİTE KAPILARI</h2>
  <p>
    Türkiye Yüzyılı Maarif Modeli (TTKB 2026 Karar No: 4 ve 5) kapsamında Din Kültürü ve Ahlak Bilgisi ile İHL Meslek Derslerinde
    öğrencilerin temel İslam bilimleri kaynaklarına doğrudan ulaşması (<code>DAB1</code>), bilgiyi tetkik ve tahkik etmesi (<code>DAB2–DAB3</code>)
    ve din istismarını önleyici eleştirel sorgulama yapabilmesi (<code>DKAB.11.4.3</code>) hedeflenmektedir. Bu hedefi kural tabanlı bir
    yazılım mimarisiyle güvence altına almak üzere <strong>Quran Vision v6.2.2</strong> projesinde iki yeni denetim motoru devreye alınmıştır:
  </p>
  <table>
    <thead>
      <tr>
        <th>Kalite Kapısı</th>
        <th>Kural Kodları</th>
        <th>Denetlenen Metodolojik ve Pedagojik Kriter</th>
        <th>Denetim Sonucu (30/30 Rapor)</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>V14 — İrfânî ve İşârî Tahrîc Kapısı</strong></td>
        <td><code>L-2301..L-2303</code> (BLOCK)</td>
        <td>Her monografide <code>ADIM 13.1</code> (Enfüsî-Âfâkî Diyalektik), <code>13.2</code> (Kalp Fıkhı: Muhâsibî ve Gazzâlî) ve <code>13.3</code> (Kuşeyrî, Tüsterî, İbn Acîbe lafzî Arapça metni ve İSNAD 2 künyesi) zorunluluğu.</td>
        <td><strong>0 BLOCK, 0 WARN (15/15 TR &amp; EN Tamamlandı)</strong></td>
      </tr>
      <tr>
        <td><strong>V15 — TYMM Kurumsal Ders Tasarımı Kapısı</strong></td>
        <td><code>L-2401..L-2403</code> (BLOCK)</td>
        <td>Her monografide <code>ADIM 20.1</code> (TTKB 2026 <code>DKAB.</code>, <code>DAB1–DAB6</code>, <code>SDB1.2/3.3</code> kodları), <code>20.2</code> (40 dk 5 aşamalı akış ve doldurulmuş 5 araç: Anlam Çözümleme Tablosu, 9'lu Grid, Zıt Panel, Konuşma Halkası, Çıkış Kartı), <code>20.3</code> (Zenginleştirme ve Destekleme) ve <code>20.4</code> (3'lü Doğrulama Filtresi).</td>
        <td><strong>0 BLOCK, 0 WARN (15/15 TR &amp; EN Tamamlandı)</strong></td>
      </tr>
      <tr>
        <td><strong>V16.2 — Çoklu Sunucu Kaynak Sicili Kapısı</strong></td>
        <td><code>L-2501..L-2506</code> (BLOCK/WARN)</td>
        <td>Tek doğruluk kaynağı <code>data/sources_registry.yaml</code> üzerinde <code>176/176</code> kaynağın (<code>127 Şâmile + 15 Altafsir + 34 Kurumsal DOI/URL</code>) fihrist/cilt başlığı (<code>verified_breadcrumb</code>), lafzî Arapça eşleşme (<code>quote_matched</code>), 90 gün tazelik ve <code>%29.0 (51/176 &gt;= %10)</code> manuel örneklem denetimi.</td>
        <td><strong>176/176 VERIFIED • 0 BLOCK, 0 WARN</strong></td>
      </tr>
    </tbody>
  </table>

  <div class="callout">
    <strong>Epistemik Doğrulama Beyanı (Sıfır İlke 3) ve Rol Ayrımı Şeffaflık Notu (İlke 4 — C ve D3 Şartları):</strong><br>
    • <em>"[2026-10-20] itibarıyla incelenen [176/176] kayıt (127 Şâmile + 15 Altafsir + 34 Kurumsal DOI/URL), [Fihrist + Lafzî Eşleşme + &gt;=0.10 Manuel Örneklem (51/176 = 0.29)] yöntemi ve [SHA-256 Snapshot] özetiyle doğrulanmıştır; yeniden doğrulama periyodu: 90 gün."</em><br>
    • <strong>Türev Hiyerarşisi (D3 Şartı):</strong> Tek doğruluk kaynağı <code>data/sources_registry.yaml</code> dosyasıdır; <code>docs/source_verification_manifest.json</code> ise derleme anında otomatik üretilen salt-okunur arayüz türevidir.<br>
    • <strong>Methodological Note (İlke 4 — C Şartı):</strong> Örneklem denetimi proje yürütücüsü (<code>Mehmet Yarıcı (Project Lead — Internal Sample Audit)</code>) tarafından gerçekleştirilmiş olup, bağımsız dış hakem değerlendirmesi III. Maarif Kongresi (<code>MOIJUB</code>) hakem süreci kapsamında yürütülmektedir.
  </div>

  <h2>BÖLÜM 3 — DİJİTAL TAHKİKTE REGRESYON VAKASI: KÜMÜLATİF CİLT OFSETİ VE PARAMETRE DENETİMİ</h2>
  <p>
    Dijital İslami kaynak doğrulamasında yalnızca HTTP <code>200 OK</code> durum koduna veya Arapça kelime varlığına güvenmek,
    çok ciltli klasik eserlerde ciddi "cilt ofseti" yanılgılarına yol açabilmektedir. Nitekim <code>v6.2.2</code> kalite kontrol sürecinde
    tespit edilerek <code>L-2502</code> ve <code>L-2503</code> kesici kurallarıyla kalıcı olarak kapatılan iki somut regresyon vakası şunlardır:
  </p>
  <p>
    <strong>1. Gazzâlî'nin <em>İhyâ'u 'Ulûmi'd-Dîn</em> (Book ID: <code>9472</code>) Kümülatif Sayfa ID Ofseti Vakası:</strong>
    Gazzâlî'nin <em>İhyâ</em> eserinde öfke ve haset (<em>Kitâbü Âfâti'l-Gadab ve'l-Hıkd ve'l-Hased</em>) bahsi matbu nüshada
    <strong>3. Cilt 186. sayfada</strong> yer almaktadır. Ancak el-Mektebetü'ş-Şâmile'nin URL yapısı (<code>shamela.ws/book/9472/&lt;page_id&gt;</code>)
    her ciltte 1'den başlamamakta; 1. ve 2. ciltlerin toplam sayfa sayısı olan <code>+746</code> sayfalık kümülatif ofset üzerine eklenmektedir.
    Matbu sayfa numarası doğrudan URL'ye yazıldığında (<code>shamela.ws/book/9472/186</code>), okuyucu 3. ciltteki <em>Rub'u'l-Mühlikât</em> yerine
    1. cilt 186. sayfadaki <em>"Bâbü Fadli Yevmi'l-Cum'a" (Cuma Gününün Faziletleri ve Âdâbı)</em> bölümüyle karşılaşmaktadır.
    <code>src/verify_all_servers.py</code> ve <code>src/gem_lint.py</code> (<code>L-2502</code> fihrist kilidi) bu sapmayı yakalamış ve 10 monografideki
    Gazzâlî bağlantılarının tamamını kümülatif <code>page_id</code> karşılıklarına (<code>9472/186 -&gt; 9472/932</code>, <code>9472/110 -&gt; 9472/856</code>,
    <code>9472/136 -&gt; 9472/882</code>, <code>9472/293 -&gt; 9472/1490</code>) güncellemiştir.
  </p>
  <p>
    <strong>2. Altafsir.com İşârî Tefsir (<code>tMadhNo=3</code> &amp; <code>tTafsirNo=31</code>) Parametre Doğrulaması:</strong>
    <code>ADIM 13.3</code> altında yer alan 15 Kuşeyrî (<em>Letâ'ifü'l-İşârât</em>) bağlantısının tamamında URL parametrelerindeki
    <code>tMadhNo=3</code> (Tasavvufî/İşârî Tefsir), <code>tTafsirNo=31</code> (el-Kuşeyrî) ve ilgili <code>tSoraNo</code>/<code>tAyahNo</code>
    değerlerinin monografinin sûre ve âyetiyle birebir örtüştüğü <code>L-2502</code> kuralıyla tescil edilmiştir.
  </p>

  <h2>BÖLÜM 4 — ÖRNEK UYGULAMA MODÜLÜ: İSRÂ SÛRESİ 17:36 (QV-2026-008) 40 DAKİKALIK TYMM DERS TASARIMI</h2>
  <p>
    Aşağıda, 15 kurucu âyet için hazırlanan ve bağımsız 34. PDF rehberinde (<code>TYMM_DKAB_15_Ayet_Ders_Tasarimi_Rehberi.pdf</code>)
    tamamı sunulan ders planlarından <strong>İsrâ Sûresi 17:36 (Bilgi Doğrulama, Epistemik Sorumluluk ve Bilişsel Güvenlik — DKAB.10.1.3)</strong>
    modülünün <code>ADIM 20.1..20.4</code> tam metni yer almaktadır:
  </p>
  {step20_html}

  <h2>KAYNAKÇA</h2>
  {refs_html}
</body>
</html>
"""


def main():
    abstract_only_parts = []
    for main_h, sub_h, body in SECTIONS_WITHOUT_REF:
        if main_h != "ANAHTAR KELİMELER":
            abstract_only_parts.append(main_h)
            if sub_h:
                abstract_only_parts.append(sub_h)
            abstract_only_parts.append(body)

    abstract_words = count_words(" ".join(abstract_only_parts))
    print(f"EBA Özet Alanı Kelime Sayısı (5 Alt Başlık + Metin): {abstract_words} kelime")
    assert 500 <= abstract_words <= 750, (
        f"Kelime sayısı 500-750 aralığında olmalıdır! Şu an: {abstract_words}"
    )

    # 1. Build Word (.docx) according to EK-1
    doc = docx.Document()
    for section in doc.sections:
        section.top_margin = Cm(2.5)
        section.bottom_margin = Cm(2.5)
        section.left_margin = Cm(2.5)
        section.right_margin = Cm(2.5)

    style = doc.styles["Normal"]
    style.font.name = "Times New Roman"
    style.font.size = Pt(12)

    def add_formatted_para(text: str, bold: bool = False, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after_pt: int = 6):
        p = doc.add_paragraph()
        p.alignment = align
        pf = p.paragraph_format
        pf.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
        pf.space_before = Pt(0)
        pf.space_after = Pt(space_after_pt)
        run = p.add_run(text)
        run.bold = bold
        run.font.name = "Times New Roman"
        run.font.size = Pt(12)
        return p

    add_formatted_para(TITLE, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after_pt=8)
    meta_line = " | ".join(f"{k}: {v}" for k, v in APPLICATION_META[:3])
    add_formatted_para(meta_line, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after_pt=12)

    for main_h, sub_h, body in SECTIONS_WITHOUT_REF:
        add_formatted_para(main_h, bold=True, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after_pt=3)
        if sub_h:
            add_formatted_para(sub_h, bold=True, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after_pt=3)
        add_formatted_para(body, bold=False, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after_pt=9)

    add_formatted_para("KAYNAKÇA", bold=True, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after_pt=3)
    for ref in REFERENCES:
        add_formatted_para(ref, bold=False, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after_pt=4)

    docx_path = DESKTOP / "III_MAARIF_KONGRESI_BILDIRI_OZETI_EK1_SABLONU.docx"
    doc.save(str(docx_path))
    print(f"DOCX kaydedildi: {docx_path}")

    # 2. Build plain TXT file
    txt_lines = [TITLE, ""]
    for k, v in APPLICATION_META:
        txt_lines.append(f"{k}: {v}")
    txt_lines.append("")
    for main_h, sub_h, body in SECTIONS_WITHOUT_REF:
        txt_lines.append(main_h)
        if sub_h:
            txt_lines.append(sub_h)
        txt_lines.append(body)
        txt_lines.append("")
    txt_lines.append("KAYNAKÇA")
    for ref in REFERENCES:
        txt_lines.append(ref)

    txt_path = DESKTOP / "III_MAARIF_KONGRESI_BILDIRI_OZETI_EK1_SABLONU.txt"
    txt_path.write_text("\n".join(txt_lines), encoding="utf-8")
    print(f"TXT kaydedildi: {txt_path}")

    # Extract Isra 17:36 Step 20 for full paper
    isra_path = ROOT / "docs" / "tr" / "13-rapor-isra-1736-v6.1.1.md"
    isra_text = isra_path.read_text(encoding="utf-8") if isra_path.exists() else ""
    m20 = re.search(r"(###\s+ADIM\s+20\b.*?)(?=\n##\s+Z-1|\Z)", isra_text, re.DOTALL | re.IGNORECASE)
    isra_step20_md = m20.group(1).strip() if m20 else ""

    full_html = build_full_paper_html(isra_step20_md)
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    tmp_html = PDF_DIR / "_tmp_maarif_full_moijub.html"
    full_pdf_repo = PDF_DIR / "III_MAARIF_KONGRESI_TAM_METIN_MOIJUB.pdf"
    full_pdf_desktop = DESKTOP / "III_MAARIF_KONGRESI_TAM_METIN_MOIJUB.pdf"
    ek1_pdf_desktop = DESKTOP / "III_MAARIF_KONGRESI_BILDIRI_OZETI_EK1_SABLONU.pdf"
    tmp_html.write_text(full_html, encoding="utf-8")

    edge_paths = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    ]
    edge_exe = next((p for p in edge_paths if Path(p).exists()), None)
    if edge_exe:
        subprocess.run(
            [
                edge_exe,
                "--headless",
                "--disable-gpu",
                "--no-pdf-header-footer",
                f"--print-to-pdf={full_pdf_repo}",
                tmp_html.resolve().as_uri(),
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        shutil.copy2(full_pdf_repo, full_pdf_desktop)
        shutil.copy2(full_pdf_repo, ek1_pdf_desktop)
        print(f"Tam Metin MOIJUB PDF kaydedildi: {full_pdf_repo} ({full_pdf_repo.stat().st_size // 1024} KB)")
        print(f"Masaüstü kopyası kaydedildi: {full_pdf_desktop}")
    if tmp_html.exists():
        tmp_html.unlink()


if __name__ == "__main__":
    main()
