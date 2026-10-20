#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
III. Maarif Kongresi (25-27 Kasım 2026, Başvuru Kodu: MOIJUB)
1) Ek-1 Genişletilmiş Bildiri Özeti (500-750 Kelime)
2) Tam Metin Bildiri Kitapçığı (1500-2500 Kelime • docs/pdf/III_MAARIF_KONGRESI_TAM_METIN_MOIJUB.pdf)
2026 Türkiye Yüzyılı Maarif Modeli DKAB Öğretim Programları (TTKB 03.03.2026 / Sayı: 4 ve 5)
ve Quran Vision v6.2.3 (V15 Pedagojik + V16.2 Çoklu Sunucu Doğrulama + V17 Kimlik Sicili) Uyumlu Sürüm.
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
    ("Proje Yürütücüsü & Baş Araştırmacı", "Mehmet Yarıcı (Uludağ Üniv. İlahiyat Fak., 1989 • T.C. MEB İstanbul Bahçelievler Dede Korkut Anadolu Lisesi • ORCID: 0009-0003-0356-8582)"),
    ("Akademik Danışman", "Mehmet Emin Koç (Azerbaycan Milli İlimler Akademisi [AMEA], Felsefe ve Sosyoloji Enstitüsü • ORCID: 0000-0002-1025-5643)"),
    ("Başvuru Tarihi ve Sürüm", "20 Ekim 2026 • Quran Vision v6.2.3 (DOI: 10.5281/zenodo.23410818)"),
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
        "Eğitim, bir toplumun bilgi ve beceri birikimini yeni kuşaklara aktarmanın ötesinde; kültürel hafızasını, "
        "değer dünyasını ve gelecek tasavvurunu şekillendiren temel bir medeniyet unsurudur. Millî Eğitim "
        "Bakanlığı Talim ve Terbiye Kurulu Başkanlığının 2026 yılı kararlarıyla uygulamaya konulan Türkiye "
        "Yüzyılı Maarif Modeli Ortaöğretim (9–12. Sınıflar) ile İlkokul-Ortaokul (4–8. Sınıflar) Din Kültürü ve Ahlak Bilgisi "
        "Öğretim Programları; öğrenciyi bilgi, duygu ve davranış bütünlüğüne ulaştıran 'Erdem-Değer-Eylem' "
        "yaklaşımı üzerine yapılandırılmıştır. Programlarda olgusal gerçekliğin bilgisini teolojik bilgi ile bütünleştiren "
        "analitik bir öğrenme süreci öngörülmekte; bu süreç 'Temel Kaynakları Kullanma (DAB1)', 'Tetkik (DAB2)', 'Tahkik (DAB3)', "
        "'Tefekkür (DAB4)', 'Dinî Delillere Başvurma (DAB5)' ve 'Tatbik (DAB6)' alan becerileriyle desteklenmektedir. "
        "Özellikle 12. sınıfta yer alan 'Kur’an-ı Kerim’in anlaşılmasında temel ilkeleri özetleyebilme (DKAB.12.1.3)' ve "
        "'Güncel dinî meselelerin çözümünde temel ilke ve yöntemleri özetleyebilme (DKAB.12.3.1)' öğrenme çıktıları; ayetlerin "
        "Hz. Peygamber’in açıklamaları, bütüncül bakış, tarihsel bağlam, nüzul sebepleri ve zaruratıhamse (can, nesil, akıl, "
        "mal ve din emniyeti) ilkeleri ışığında anlaşılmasını esas almaktadır. Dijital çağda öğrencilerin ayetlere bağlamından "
        "koparılmış kesitler üzerinden maruz kalması, bu ilkeleri somutlaştıracak yapılandırılmış öğretim tasarımlarını zorunlu kılmaktadır.",
    ),
    (
        "ÇALIŞMANIN AMACI VE ÖNEMİ",
        None,
        "Bu çalışmanın amacı; 2026 Din Kültürü ve Ahlak Bilgisi Dersi Öğretim Programlarında yer alan 'Dinî Kavramları "
        "Bağlamına Uygun Kullanma (DAB3.2)', 'Dinî Metinleri Yorumlama (DAB3.3)', 'Dinî Metinleri Tahlil Etme (DAB3.4)' ve "
        "'Dinî Konularda Analitik Düşünme (DAB4.4)' süreç bileşenlerini sınıf ortamında hayata geçirmek üzere geliştirilen "
        "'Yirmi Altı Adımlı Stratejik Tefsir ve Öğretim Tasarımı Modeli'ni (Quran Vision v6.2.3) tanıtmak ve modelin öğrenme-öğretme "
        "yaşantılarına katkısını ortaya koymaktır. Literatürdeki mevcut çalışmalar çoğunlukla kuramsal öneri düzeyinde kalırken; bu araştırma "
        "tamamlanmış on beş kurucu ayet monografisi (34 A4 PDF külliyatı), kural tabanlı pedagojik ve çoklu sunucu kaynak doğrulama "
        "yazılımı (V1–V17), çift dilli dijital öğrenme platformu ve her ünite için doğrudan uygulanabilir kırkar dakikalık ders planları "
        "sunması bakımından özgün bir uygulama örneği teşkil etmektedir.",
    ),
    (
        "YÖNTEM",
        None,
        "Araştırmada, eğitim bilimleri ilkeleri ile öğretim materyali geliştirmeyi birleştiren tasarım tabanlı araştırma "
        "deseni ve nitel doküman analizi yöntemi kullanılmıştır. Çalışmanın veri setini, 2026 öğretim programlarındaki "
        "öğrenme çıktılarıyla doğrudan örtüşen on beş kurucu Kur’an-ı Kerim ayetinin tamamı (15/15) oluşturmaktadır: ahit ihlali, "
        "meşru müdafaa ve bağlam bütünlüğü (Tevbe 9:5; DKAB.11.4.3), aile içi merhamet ve sorumluluk (Nisâ 4:34; DKAB.12.2.1), "
        "mülkiyet emniyeti ve sosyal adalet (Mâide 5:38; DKAB.12.3.1), inanç ve vicdan özgürlüğü (Bakara 2:256; DKAB.10.1.2), "
        "emanet ve liyakat (Nisâ 4:58; DKAB.10.3.4), istişare ve katılımcı yönetişim (Âl-i İmrân 3:159; DKAB.10.3.3), toplumsal "
        "barış ve kardeşlik (Hucurât 49:9–10; DKAB.12.4.5), bilgi ve doğrulama sorumluluğu (İsrâ 17:36; DKAB.10.1.3), servetin adil "
        "dolaşımı (Haşr 59:7; DKAB.10.3.5), dil ve renk çeşitliliği (Rûm 30:22; DKAB.10.5.3), temel insan hakları ve ölçü-tartı "
        "dürüstlüğü (En'âm 6:151–152; DKAB.12.3.5), hukuk ve adalet dengesi (Hadîd 57:25; DKAB.11.4.4), adalet ve ihsan (Nahl "
        "16:90; DKAB.10.3.4), insanlığın eşitliği ve tanışma ahlakı (Hucurât 49:13; DKAB.10.5.3) ile yaşam hakkının dokunulmazlığı "
        "(Mâide 5:32; DKAB.8.3.1). Beş aşamalı öğretim tasarımı; "
        "(1) Lafzî çözümleme ve yedi boyutlu bağlam matrisi, (2) Zaruratıhamse ve seddizerai ilkeleriyle güncel gerçeklik arasında "
        "köprü kurma, (3) Din istismarını önleyici eleştirel sorgulama (DKAB.11.4.3), (4) Öz düzenleme (SDB1.2) ve sorumlu karar verme "
        "(SDB3.3) muhasebesi, (5) Kırk dakikalık öğrenme-öğretme uygulaması adımlarından oluşmaktadır.",
    ),
    (
        "BULGULAR",
        None,
        "Modelin on beş ayet üzerindeki uygulanması sonucunda üç temel bulguya ulaşılmıştır: Birincisi, Taberî, Mâtürîdî, "
        "Râzî, Kurtubî, Şâtıbî, İbn Âşûr, Kuşeyrî, Gazzâlî, Muhâsibî, Tüsterî ve İbn Acîbe gibi temel kaynaklardan tahkik edilen "
        "92 lafzî Arapça iktibas (77 klasik tefsir/fıkıh + 15 işârî tefsir nakli) ve 176 doğrulanmış kaynak sicilinin (127 Şâmile + "
        "15 Altafsir + 34 Kurumsal veri seti) eşleştirilmesi, öğrencilerde 'Bilgi Okuryazarlığı (OB1)' ve 'Gerçeği Arama (E3.4)' "
        "eğilimini güçlendirerek doğrudan kaynak nakli ile beşerî yorum arasındaki sınırı somutlaştırmıştır. İkincisi, anlam çözümleme "
        "tablosu, yapılandırılmış grid, zıt panel, konuşma halkası ve çıkış kartı araçlarıyla yapılandırılan kırk dakikalık ders "
        "modüllerinin (V15 L-2401..L-2403); ön değerlendirme, köprü kurma, öğrenme kanıtları ile zenginleştirme ve destekleme "
        "basamaklarını eksiksiz karşıladığı görülmüştür. Üçüncüsü, çoklu sunucu doğrulama ve kimlik sicili (V16–V17 L-2501..L-2507) "
        "sayesinde kümülatif cilt ofseti, parametre ve künye hatalarının sıfır kesici hatayla önlendiği tespit edilmiştir.",
    ),
    (
        "SONUÇ VE ÖNERİLER",
        None,
        "Sonuç olarak geliştirilen yirmi altı adımlı öğretim tasarımı; öğretmeni bilgiyi salt aktaran konumdan çıkararak, "
        "temel dinî kaynaklar ile çağdaş toplumsal gerçeklik arasında sahih köprüler kuran bir uzman ve rehber konumuna "
        "taşımaktadır. Araştırma bulguları doğrultusunda şu öneriler sunulmuştur: (1) Ortaöğretim ve ortaokul ders "
        "kitaplarındaki 'Kur’an’dan Mesajlar' bölümlerinde ayetin öncesi, sonrası, nüzul sebebi ve zaruratıhamse boyutunu "
        "bütünleştiren anlam çözümleme tablolarına yer verilmelidir; (2) İsrâ suresi 36. ayet (DKAB.10.1.3) kapsamında "
        "dijital bilgi doğrulama etkinlikleri okul temelli planlama saatlerinde uygulanmalıdır; (3) Geliştirilen kırk "
        "dakikalık münazara, zıt panel ve çıkış kartı e-içerikleri Eğitim Bilişim Ağı üzerinden zümre öğretmenlerinin "
        "erişimine açılmalıdır.",
    ),
]

REFERENCES = [
    "Gazzâlî, E. H. (2004). İhyâ’u ‘ulûmi’d-dîn (Cilt 1–4). Beyrut: Dârü’l-Ma‘rife.",
    "İbn Acîbe, A. (1999). el-Bahrü’l-medîd fî tefsîri’l-Kur’âni’l-mecîd (A. A. el-Kureşî, Ed.; Cilt 1–8). Kahire: Doktor Hasan Abbas Zekî Yayını.",
    "İbn Âşûr, M. T. (1984). et-Tahrîr ve’t-tenvîr (Cilt 1–30). Tunus: ed-Dârü’t-Tûnisiyye li’n-Neşr.",
    "Kurtubî, M. A. (1964). el-Câmi‘ li-ahkâmi’l-Kur’ân (A. el-Berdûnî & İ. Atfîş, Ed.; Cilt 1–20). Kahire: Dârü’l-Kütübi’l-Mısriyye.",
    "Kuşeyrî, A. (1981). Letâ’ifü’l-işârât (İ. Besyûnî, Ed.; Cilt 1–3). Kahire: el-Hey’etü’l-Mısriyyetü’l-Âmme li’l-Kitâb.",
    "Mâtürîdî, E. M. (2005). Te’vîlâtü Ehli’s-Sünne (B. Topaloğlu, Ed.; Cilt 1–17). İstanbul: Dârü’l-Mîzân.",
    "Millî Eğitim Bakanlığı [MEB]. (2024). Türkiye Yüzyılı Maarif Modeli öğretim programları ortak metni. Ankara: MEB Talim ve Terbiye Kurulu Başkanlığı.",
    "Millî Eğitim Bakanlığı [MEB]. (2026a). İlkokul-ortaokul ve imam hatip ortaokulu Din Kültürü ve Ahlak Bilgisi dersi (4–8. sınıflar) öğretim programı (TTKB 03.03.2026 tarih ve 4 sayılı kararı). Ankara: MEB Yayınları.",
    "Millî Eğitim Bakanlığı [MEB]. (2026b). Ortaöğretim Din Kültürü ve Ahlak Bilgisi dersi (9–12. sınıflar) öğretim programı (TTKB 03.03.2026 tarih ve 5 sayılı kararı). Ankara: MEB Yayınları.",
    "Muhâsibî, H. (1990). er-Ri‘âye li-hukûkillâh (A. H. Mahmûd, Ed.). Beyrut: Dârü’l-Kütübi’l-İlmiyye.",
    "Râzî, F. (1999). Mefâtîhu’l-gayb (et-Tefsîrü’l-kebîr) (Cilt 1–32). Beyrut: Dâru İhyâi’t-Türâsi’l-Arabî.",
    "Şâtıbî, İ. (1997). el-Muvâfakât fî usûli’ş-şerîa (M. H. Âl-i Selmân, Ed.; Cilt 1–6). Riyad: Dâru İbni Affân.",
    "Taberî, M. C. (2000). Câmi‘u’l-beyân fî te’vîli’l-Kur’ân (A. M. Şâkir, Ed.; Cilt 1–24). Beyrut: Müessesetü’r-Risâle.",
    "Tüsterî, S. A. (2002). Tefsîru’t-Tüsterî (M. B. Uyûnüssûd, Ed.). Beyrut: Dârü’l-Kütübi’l-İlmiyye.",
    "Yarıcı, M. (2026). Kur’ân Vizyonu (Quran Vision): 26 Adımlı Kanıta Dayalı Stratejik Tefsir, Makâsıd ve Medeniyet Öngörü Külliyatı (Sürüm v6.2.3; 15 Monografi, 34 Külliyat PDF'i + 2 III. Maarif Kongresi Bildiri PDF'i — Toplam 36 PDF). Zenodo. https://doi.org/10.5281/zenodo.23410818",
]


def count_words(text: str) -> int:
    return len(text.split())


def build_full_paper_html() -> str:
    """
    III. Maarif Kongresi (MOIJUB) Tam Metin Bildiri Kitapçığı HTML şablonunu üretir.
    Kongre yazım kılavuzundaki 1.500–2.500 kelime sınırına (hedef: ~2.150–2.300 kelime) tam uyumlu olarak:
    - Bölüm 1: Genişletilmiş Bildiri Özeti (EK-1)
    - Bölüm 2: 15/15 Kurucu Âyet ve TTKB 2026 DKAB Öğrenme Çıktıları Tam Eşleştirme Tablosu ile V14–V17 Kalite Kapıları
    - Bölüm 3: Dijital Tahkikte 3 Regresyon Vakası (Gazzâlî 9472/932 Cilt Ofseti, Altafsir tTafsirNo=31 ve v6.2.2 -> v6.2.3 L-2507 Kimlik Kilidi)
    - Bölüm 4: Örnek Uygulama Modülü — İsrâ Sûresi 17:36 (QV-2026-008 • DKAB.10.1.3) 5 Aşamalı 40 Dakikalık TYMM Ders Tasarımı, Anlam Çözümleme Tablosu, Zıt Panel, Çıkış Kartı ve Farklılaştırma Bulguları
    bölümlerini içerir.
    """
    abstract_blocks = "".join(
        f"<div class='sec-sub'>{h}</div><p>{b}</p>" for h, _, b in SECTIONS_WITHOUT_REF
    )
    refs_html = "".join(f"<p class='ref-item'>{r}</p>" for r in REFERENCES)

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
      <div><strong>Külliyat ve Açık Bilim Envanteri:</strong> 15 Kurucu Âyet Monografisi (15 TR + 15 EN = 30 Rapor) • 34 Külliyat PDF'i (30 Tekil Monografi + 2 TR/EN Tam Külliyat [v6.2.3] + 1 İSNAD-2 Klasik Arapça Veritabanları Rehberi [ISNAD_2_Klasik_Arapca_Veritabanlari_Rehberi.pdf] + 1 TYMM DKAB 15 Âyet Ders Tasarımı Rehberi [TYMM_DKAB_15_Ayet_Ders_Tasarimi_Rehberi.pdf]) + 2 III. Maarif Kongresi (MOIJUB) Bildiri PDF'i (Özet + Tam Metin) — Toplam 36 PDF • 92 Lafzî Arapça İktibas (77 Klasik Tefsir/Fıkıh + 15 İşârî Tefsir) • 176/176 Doğrulanmış Çoklu Sunucu Kaynağı (<code>127 Şâmile + 15 Altafsir + 34 Kurumsal DOI/URL</code>)</div>
    </div>
  </div>

  <h2>BÖLÜM 1 — EBA SİSTEMİ GENİŞLETİLMİŞ BİLDİRİ ÖZETİ (EK-1 ŞABLONU)</h2>
  {abstract_blocks}

  <h2>BÖLÜM 2 — QURAN VISION v6.2.3 METODOLOJİK MİMARİSİ: 15/15 KURUCU ÂYET–DKAB EŞLEŞTİRMESİ VE V14–V17 KALİTE KAPILARI</h2>
  <p>
    Türkiye Yüzyılı Maarif Modeli (TTKB 2026 Karar No: 4 ve 5) kapsamında öğrencilerin temel kaynaklara doğrudan ulaşması (<code>DAB1</code>),
    bilgiyi tetkik-tahkik etmesi (<code>DAB2–DAB3</code>) ve eleştirel sorgulama yapabilmesi (<code>DKAB.11.4.3</code>) hedeflenmektedir.
    <strong>Quran Vision v6.2.3</strong> külliyatındaki 15 kurucu âyetin tamamı (<code>QV-2026-001..015</code>), 2026 öğretim programlarındaki
    öğrenme çıktıları ve alan becerileriyle aşağıdaki tabloda birebir eşleştirilmiştir:
  </p>
  <table>
    <thead>
      <tr>
        <th>Vaka Kodu</th>
        <th>Sûre ve Âyet</th>
        <th>Stratejik ve Pedagojik Tema</th>
        <th>TTKB 2026 Öğrenme Çıktısı &amp; Beceri Kodları (<code>ADIM 20.1</code>)</th>
        <th>Klasik / İşârî Nakil</th>
      </tr>
    </thead>
    <tbody>
      <tr><td><code>QV-2026-001</code></td><td>Tevbe 9:5</td><td>Ahit İhlali, Meşru Müdafaa ve Bağlam Bütünlüğü</td><td><code>DKAB.11.4.3</code>, <code>DKAB.12.1.3</code> • <code>DAB3.2–3.4</code>, <code>SDB3.3</code></td><td>5 + 1 (6)</td></tr>
      <tr><td><code>QV-2026-002</code></td><td>Nisâ 4:34</td><td>Aile İçi Emanet Sorumluluğu ve Kademeli Sulh</td><td><code>DKAB.12.2.1</code>, <code>DKAB.12.1.3</code> • <code>DAB3.3</code>, <code>SDB2.2</code></td><td>5 + 1 (6)</td></tr>
      <tr><td><code>QV-2026-003</code></td><td>Mâide 5:38</td><td>Mülkiyet Emniyeti, İspat Şartları ve Sosyal Güvenlik</td><td><code>DKAB.12.3.1</code>, <code>DKAB.12.1.3</code> • <code>DAB3.4</code>, <code>SDB3.3</code></td><td>5 + 1 (6)</td></tr>
      <tr><td><code>QV-2026-004</code></td><td>Bakara 2:256</td><td>İnanç ve Vicdan Özgürlüğü, Zorlama Yasağı</td><td><code>DKAB.10.1.2</code>, <code>DKAB.11.4.3</code> • <code>DAB3.2</code>, <code>SDB2.3</code></td><td>5 + 1 (6)</td></tr>
      <tr><td><code>QV-2026-005</code></td><td>Nisâ 4:58</td><td>Emanetin Ehline Verilmesi (Liyakat) ve Adalet</td><td><code>DKAB.10.3.4</code>, <code>DKAB.12.1.3</code> • <code>DAB4.4</code>, <code>SDB3.3</code></td><td>5 + 1 (6)</td></tr>
      <tr><td><code>QV-2026-006</code></td><td>Âl-i İmrân 3:159</td><td>Kriz Yönetiminde İstişare (Şûrâ) ve Şefkat Dili</td><td><code>DKAB.10.3.3</code>, <code>DKAB.12.1.3</code> • <code>DAB3.3</code>, <code>SDB2.1</code></td><td>5 + 1 (6)</td></tr>
      <tr><td><code>QV-2026-007</code></td><td>Hucurât 49:9–10</td><td>Toplumsal Barış, Arabuluculuk (Islah) ve Kardeşlik</td><td><code>DKAB.12.4.5</code>, <code>DKAB.12.1.3</code> • <code>DAB4.4</code>, <code>SDB2.2</code></td><td>5 + 1 (6)</td></tr>
      <tr><td><code>QV-2026-008</code></td><td>İsrâ 17:36</td><td>Bilgi Doğrulama, Epistemik Sorumluluk ve Bilişsel Güvenlik</td><td><code>DKAB.10.1.3</code>, <code>DKAB.11.4.3</code> • <code>DAB2–DAB3</code>, <code>SDB1.2</code></td><td>5 + 1 (6)</td></tr>
      <tr><td><code>QV-2026-009</code></td><td>Haşr 59:7</td><td>Servetin Adil Dolaşımı ve Tekelleşme Yasağı</td><td><code>DKAB.10.3.5</code>, <code>DKAB.12.3.5</code> • <code>DAB4.4</code>, <code>SDB3.2</code></td><td>5 + 1 (6)</td></tr>
      <tr><td><code>QV-2026-010</code></td><td>Rûm 30:22</td><td>Dil ve Renk Çeşitliliğinin İlahî Âyet Oluşu</td><td><code>DKAB.10.5.3</code>, <code>DKAB.12.1.3</code> • <code>DAB4</code>, <code>SDB2.3</code></td><td>5 + 1 (6)</td></tr>
      <tr><td><code>QV-2026-011</code></td><td>En'âm 6:151–152</td><td>Evrensel Ahlak İlkeleri ve Ölçü-Tartı Dürüstlüğü</td><td><code>DKAB.12.3.5</code>, <code>DKAB.12.1.3</code> • <code>DAB3.4</code>, <code>SDB3.2</code></td><td>5 + 1 (6)</td></tr>
      <tr><td><code>QV-2026-012</code></td><td>Hadîd 57:25</td><td>Kitap, Mîzân ve Demir Dengesi: Hukuk ve Caydırıcılık</td><td><code>DKAB.11.4.4</code>, <code>DKAB.12.1.3</code> • <code>DAB4.4</code>, <code>SDB3.3</code></td><td>5 + 1 (6)</td></tr>
      <tr><td><code>QV-2026-013</code></td><td>Nahl 16:90</td><td>Adalet, İhsan, Akrabaya Yardım ve Azgınlık Yasağı</td><td><code>DKAB.10.3.4</code>, <code>DKAB.12.1.3</code> • <code>DAB3.3</code>, <code>SDB2.2</code></td><td>5 + 1 (6)</td></tr>
      <tr><td><code>QV-2026-014</code></td><td>Hucurât 49:13</td><td>İnsanlığın Ontolojik Eşitliği ve Teârüf Ahlakı</td><td><code>DKAB.10.5.3</code>, <code>DKAB.12.1.3</code> • <code>DAB3.4</code>, <code>SDB2.3</code></td><td>6 + 1 (7)</td></tr>
      <tr><td><code>QV-2026-015</code></td><td>Mâide 5:32</td><td>Yaşam Hakkının Dokunulmazlığı ve İhyâ Doktrini</td><td><code>DKAB.8.3.1</code>, <code>DKAB.12.3.5</code> • <code>DAB3.3</code>, <code>SDB3.2</code></td><td>6 + 1 (7)</td></tr>
      <tr><td colspan="4"><strong>TOPLAM (15/15 Kurucu Âyet Monografisi — 30 TR/EN Rapor)</strong></td><td><strong>77 + 15 = 92 İktibas</strong></td></tr>
    </tbody>
  </table>

  <p>
    Modelin metodolojik ve pedagojik tutarlılığını kural tabanlı olarak denetlemek üzere <code>src/gem_lint.py</code> üzerinde
    dört üst düzey kalite kapısı (<code>V14–V17</code>) çalıştırılmaktadır:
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
        <td><strong>0 BLOCK, 0 WARN (15/15 TR &amp; EN)</strong></td>
      </tr>
      <tr>
        <td><strong>V15 — TYMM Kurumsal Ders Tasarımı Kapısı</strong></td>
        <td><code>L-2401..L-2403</code> (BLOCK)</td>
        <td>Her monografide <code>ADIM 20.1</code> (TTKB 2026 <code>DKAB.</code>, <code>DAB1–DAB6</code>, <code>SDB1.2/3.3</code> kodları), <code>20.2</code> (40 dk 5 aşamalı akış ve 5 araç), <code>20.3</code> (Zenginleştirme/Destekleme) ve <code>20.4</code> (3'lü Doğrulama Filtresi).</td>
        <td><strong>0 BLOCK, 0 WARN (15/15 TR &amp; EN)</strong></td>
      </tr>
      <tr>
        <td><strong>V16.2 — Çoklu Sunucu Kaynak Sicili Kapısı</strong></td>
        <td><code>L-2501..L-2506</code> (BLOCK/WARN)</td>
        <td>Tek doğruluk kaynağı <code>data/sources_registry.yaml</code> üzerinde <code>176/176</code> kaynağın (<code>127 Şâmile + 15 Altafsir + 34 Kurumsal DOI/URL</code>) fihrist/cilt başlığı, lafzî Arapça eşleşme ve <code>%29.0 (51/176 &gt;= %10)</code> manuel örneklem denetimi.</td>
        <td><strong>176/176 VERIFIED • 0 BLOCK</strong></td>
      </tr>
      <tr>
        <td><strong>V17 — Kişi ve Rol Ayrımı Sicil Kapısı</strong></td>
        <td><code>L-2507</code> (BLOCK)</td>
        <td><code>data/people_registry.yaml</code> üzerinden Proje Yürütücüsü (Mehmet Yarıcı) ile Akademik Danışman (Mehmet Emin Koç — AMEA) arasındaki kurum, ORCID ve rol ayrımının korunması.</td>
        <td><strong>0 BLOCK, 0 WARN (16/16 Pytest PASS)</strong></td>
      </tr>
    </tbody>
  </table>

  <div class="callout">
    <strong>Epistemik Doğrulama Beyanı (Sıfır İlke 3) ve Rol Ayrımı Şeffaflık Notu (İlke 4 — C ve D3 Şartları):</strong><br>
    • <em>"[2026-10-20] itibarıyla incelenen [176/176] kayıt (127 Şâmile + 15 Altafsir + 34 Kurumsal DOI/URL), [Fihrist + Lafzî Eşleşme + &gt;=0.10 Manuel Örneklem (51/176 = 0.29)] yöntemi ve [SHA-256 Snapshot] özetiyle doğrulanmıştır; yeniden doğrulama periyodu: 90 gün."</em><br>
    • <strong>Türev Hiyerarşisi (D3 Şartı):</strong> Tek doğruluk kaynağı <code>data/sources_registry.yaml</code> dosyasıdır; <code>docs/source_verification_manifest.json</code> ise derleme anında otomatik üretilen salt-okunur arayüz türevidir.<br>
    • <strong>Metodolojik Not (İlke 4 — Rol Ayrımı):</strong> 51/176 (%29.0) kaynaklık manuel örneklem kontrolü (Gazzâlî C.3 s.186 -&gt; 9472/932 cilt ofseti düzeltmesi dahil) proje yürütücüsü <strong>Mehmet Yarıcı</strong> (<code>ORCID: 0009-0003-0356-8582</code>) tarafından iç denetim (<code>Internal Sample Audit</code>) olarak gerçekleştirilmiş; akademik danışmanlık süreci <strong>Mehmet Emin Koç</strong> (<em>Azerbaycan Milli İlimler Akademisi [AMEA], Felsefe ve Sosyoloji Enstitüsü</em>; <code>ORCID: 0000-0002-1025-5643</code>) tarafından yürütülmüştür.
  </div>

  <h2>BÖLÜM 3 — DİJİTAL TAHKİKTE REGRESYON VAKASI: KÜMÜLATİF CİLT OFSETİ, PARAMETRE VE KİMLİK DENETİMİ</h2>
  <p>
    Dijital İslami kaynak doğrulamasında yalnızca HTTP <code>200 OK</code> durum koduna güvenmek, çok ciltli klasik eserlerde
    ciddi "cilt ofseti" yanılgılarına yol açmaktadır. Kalite kontrol sürecinde tespit edilerek <code>L-2502</code>, <code>L-2503</code>
    ve <code>L-2507</code> kesici kurallarıyla kalıcı olarak kapatılan üç somut regresyon vakası şunlardır:
  </p>
  <p>
    <strong>1. Gazzâlî'nin <em>İhyâ'u 'Ulûmi'd-Dîn</em> (Book ID: <code>9472</code>) Kümülatif Sayfa ID Ofseti Vakası:</strong>
    Gazzâlî'nin <em>İhyâ</em> eserinde öfke ve haset (<em>Kitâbü Âfâti'l-Gadab ve'l-Hıkd ve'l-Hased</em>) bahsi matbu nüshada
    <strong>3. Cilt 186. sayfada</strong> yer almaktadır. Ancak Şâmile URL yapısı (<code>shamela.ws/book/9472/&lt;page_id&gt;</code>)
    her ciltte 1'den başlamamakta; 1. ve 2. ciltlerin toplam sayfa sayısı olan <code>+746</code> sayfalık kümülatif ofset üzerine eklenmektedir.
    Matbu sayfa numarası doğrudan URL'ye yazıldığında (<code>shamela.ws/book/9472/186</code>), 3. ciltteki <em>Rub'u'l-Mühlikât</em> yerine
    1. cilt 186. sayfadaki <em>"Bâbü Fadli Yevmi'l-Cum'a" (Cuma Gününün Faziletleri ve Âdâbı)</em> açılmaktadır.
    <code>L-2502</code> fihrist kilidi bu sapmayı yakalamış ve 10 monografideki Gazzâlî bağlantılarını kümülatif <code>page_id</code>
    karşılıklarına (<code>9472/186 -&gt; 9472/932</code>, <code>9472/110 -&gt; 9472/856</code>, <code>9472/136 -&gt; 9472/882</code>,
    <code>9472/293 -&gt; 9472/1490</code>) güncellemiştir.
  </p>
  <p>
    <strong>2. Altafsir.com İşârî Tefsir (<code>tMadhNo=3</code> &amp; <code>tTafsirNo=31</code>) Parametre Doğrulaması:</strong>
    <code>ADIM 13.3</code> altındaki 15 Kuşeyrî (<em>Letâ'ifü'l-İşârât</em>) bağlantısının tamamında <code>tMadhNo=3</code>,
    <code>tTafsirNo=31</code> ve <code>tSoraNo</code>/<code>tAyahNo</code> değerlerinin sûre ve âyetle birebir örtüştüğü <code>L-2502</code> kuralıyla tescil edilmiştir.
  </p>
  <p>
    <strong>3. Süreç İçi Kalite Kontrol ve <code>L-2507</code> Kimlik Kilidi Vakası (<code>v6.2.2 -&gt; v6.2.3</code>):</strong>
    Sürüm paketleme aşamasında bağlamsız metin değiştirme (<em>global find-replace</em>) nedeniyle Akademik Danışman künyesi (<strong>Mehmet Emin Koç</strong> — <em>AMEA</em>, <code>ORCID: 0000-0002-1025-5643</code>) ile Proje Yürütücüsü künyesinin (<strong>Mehmet Yarıcı</strong>, <code>ORCID: 0009-0003-0356-8582</code>) birleştiği tespit edilmiş; <code>data/people_registry.yaml</code> sicili ve <code>L-2507</code> (<code>BLOCK</code>) kimlik kilidi devreye alınarak <code>v6.2.3</code> düzeltme sürümüyle kalıcı olarak güvence altına alınmıştır.
  </p>

  <h2>BÖLÜM 4 — ÖRNEK UYGULAMA MODÜLÜ: İSRÂ SÛRESİ 17:36 (QV-2026-008 • DKAB.10.1.3) 40 DAKİKALIK TYMM DERS TASARIMI BULGULARI</h2>
  <p>
    Bağımsız 34. külliyat rehberinde (<code>TYMM_DKAB_15_Ayet_Ders_Tasarimi_Rehberi.pdf</code>) tam metinleri sunulan 15 ders planından
    <strong>İsrâ Sûresi 17:36 (Bilgi Doğrulama, Epistemik Sorumluluk ve Bilişsel Güvenlik — <code>DKAB.10.1.3</code>)</strong> modülünün
    beş aşamalı 40 dakikalık ders akışı ve pedagojik araçları aşağıda özetlenmiştir:
  </p>
  <table>
    <thead>
      <tr>
        <th>Ders Aşaması ve Süre</th>
        <th>Uygulanan TYMM Pedagojik Aracı (<code>ADIM 20.2</code>)</th>
        <th>Klasik Tahrîc, Zaruratıhamse Köprüsü ve Öğrenme Kanıtı</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>1. Aşama (0–5 dk)</strong><br>Ön Değerlendirme</td>
        <td><strong>Dijital Vaka Senaryosu &amp; Ön-Yoklama</strong> (<code>DAB2 Tetkik</code>)</td>
        <td>Kaynağı belirsiz bir sosyal medya paylaşımı karşısında öğrenci tepkileri yoklanır; <em>zan</em> ile <em>tahkik edilmiş bilgi ('ilm)</em> ayrımı sezdirilir.</td>
      </tr>
      <tr>
        <td><strong>2. Aşama (5–15 dk)</strong><br>Lafzî Çözümleme</td>
        <td><strong>Araç 1: Anlam Çözümleme Tablosu</strong> &amp; <strong>Araç 2: Yapılandırılmış 9'lu Grid</strong> (<code>DAB1</code>, <code>DAB3.2–3.4</code>)</td>
        <td><code>velâ takfü</code> (ardına düşme), <code>'ilm</code> ve <code>es-sem' / el-basar / el-fuâd</code> kavramları Taberî (<code>C.17, s.447</code>), Mâtürîdî (<code>C.8, s.275</code>) ve Râzî (<code>C.20, s.336</code>) nakilleriyle çözümlenir; Hucurât 49:6 (<em>tebeyyün</em>) ile bağlam kurulur.</td>
      </tr>
      <tr>
        <td><strong>3. Aşama (15–28 dk)</strong><br>Köprü Kurma</td>
        <td><strong>Araç 3: Zıt Panel Münazarası</strong> (<code>DKAB.11.4.3</code>, <code>DAB4.4</code>)</td>
        <td><em>Panel A</em> ("Hızlı paylaşım duyarlılığı artırır") ile <em>Panel B</em> ("Doğrulanmamış bilgi akıl ve onur emniyetini [<em>hıfzü'l-'akl ve'l-'ırz</em>] tahrip eder; İbn Âşûr <code>C.15, s.99</code>") karşılaştırılır; sentetik içeriklerde (<em>deepfake</em>) <em>sedd-i zerâi'</em> tartışılır.</td>
      </tr>
      <tr>
        <td><strong>4. Aşama (28–35 dk)</strong><br>İrfânî Muhasebe</td>
        <td><strong>Araç 4: Konuşma Halkası</strong> (<code>ADIM 13 Kalp Fıkhı</code> • <code>SDB1.2</code>, <code>SDB3.3</code>)</td>
        <td>Kuşeyrî'nin <em>Letâ'ifü'l-İşârât</em> (<code>C.2, s.347</code>) ve Gazzâlî'nin <em>İhyâ</em> (<code>C.3, s.110 / page_id: 856</code>) eserlerindeki <em>tecassüs</em> ve <em>dil âfetleri</em> uyarıları üzerinden niyet muhasebesi yapılır.</td>
      </tr>
      <tr>
        <td><strong>5. Aşama (35–40 dk)</strong><br>Ölçme &amp; Farklılaştırma</td>
        <td><strong>Araç 5: 3-2-1 Çıkış Kartı</strong> &amp; <strong>Farklılaştırma</strong> (<code>ADIM 20.3–20.4</code>)</td>
        <td>Öğrenciler 3 doğrulama ilkesi, 2 dijital risk ve 1 eylem kararı yazar. <em>Zenginleştirme:</em> Hadis usûlündeki <em>cerh ve ta'dîl</em> ile dijital teyit algoritmalarını karşılaştırma. <em>Destekleme:</em> 3 adımlı "Dur–Kaynağı Ara–Teyit Et" kontrol listesi.</td>
      </tr>
    </tbody>
  </table>
  <p>
    Bu modül; öğrencilerin klasik tefsir mirasını birincil kaynaklarından (<code>[NAKİL]</code>) tanımasını ve bilişsel güvenlik
    sorunları karşısında analitik-ahlaki karar alma (<code>[YORUM / TATBİK]</code>) becerisi geliştirmesini sağlamaktadır.
  </p>

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

    full_html = build_full_paper_html()
    body_no_ref_html = re.search(r"<body>(.*?)<h2>KAYNAKÇA</h2>", full_html, re.S).group(1)
    plain_no_ref = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", body_no_ref_html)).strip()
    full_body_words = count_words(plain_no_ref)
    print(f"Tam Metin Bildiri Gövde Kelime Sayısı (Kaynakça Hariç): {full_body_words} kelime")
    assert 1500 <= full_body_words <= 2500, (
        f"Tam metin gövde kelime sayısı 1500-2500 aralığında olmalıdır! Şu an: {full_body_words}"
    )

    abstract_blocks = "".join(
        f"<div class='sec-sub'>{h}</div><p>{b}</p>" for h, _, b in SECTIONS_WITHOUT_REF
    )
    refs_html = "".join(f"<p class='ref-item'>{r}</p>" for r in REFERENCES)
    ek1_html = f"""<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<title>III. Maarif Kongresi Genişletilmiş Bildiri Özeti (MOIJUB — Ek-1 Şablonu)</title>
<style>
  @page {{ size: A4; margin: 2.2cm; }}
  body {{ font-family: "Times New Roman", Times, serif; font-size: 11.5pt; line-height: 1.5; text-align: justify; color: #111827; margin: 0; }}
  .title {{ font-size: 14pt; font-weight: bold; text-align: center; text-transform: uppercase; color: #064e3b; margin-bottom: 8pt; }}
  .meta {{ font-size: 10pt; text-align: center; color: #334155; margin-bottom: 14pt; border-bottom: 1.5px solid #0f5132; padding-bottom: 8pt; }}
  .sec-sub {{ font-weight: bold; color: #0f5132; margin-top: 9pt; margin-bottom: 3pt; }}
  p {{ margin-top: 0; margin-bottom: 7pt; text-align: justify; }}
  .ref-item {{ margin-bottom: 4pt; padding-left: 1cm; text-indent: -1cm; font-size: 10.5pt; }}
</style>
</head>
<body>
  <div class="title">{TITLE}</div>
  <div class="meta">{" • ".join(f"<strong>{k}:</strong> {v}" for k, v in APPLICATION_META[:4])}</div>
  {abstract_blocks}
  <div class="sec-sub">KAYNAKÇA</div>
  {refs_html}
</body>
</html>
"""
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    tmp_html = PDF_DIR / "_tmp_maarif_full_moijub.html"
    tmp_ek1_html = PDF_DIR / "_tmp_maarif_ek1_moijub.html"
    full_pdf_repo = PDF_DIR / "III_MAARIF_KONGRESI_TAM_METIN_MOIJUB.pdf"
    ek1_pdf_repo = PDF_DIR / "III_MAARIF_KONGRESI_BILDIRI_OZETI_EK1_SABLONU.pdf"
    full_pdf_desktop = DESKTOP / "III_MAARIF_KONGRESI_TAM_METIN_MOIJUB.pdf"
    ek1_pdf_desktop = DESKTOP / "III_MAARIF_KONGRESI_BILDIRI_OZETI_EK1_SABLONU.pdf"
    tmp_html.write_text(full_html, encoding="utf-8")
    tmp_ek1_html.write_text(ek1_html, encoding="utf-8")

    edge_paths = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    ]
    edge_exe = next((p for p in edge_paths if Path(p).exists()), None)
    if edge_exe:
        for html_f, pdf_f in [(tmp_html, full_pdf_repo), (tmp_ek1_html, ek1_pdf_repo)]:
            subprocess.run(
                [
                    edge_exe,
                    "--headless",
                    "--disable-gpu",
                    "--no-pdf-header-footer",
                    f"--print-to-pdf={pdf_f}",
                    html_f.resolve().as_uri(),
                ],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        try:
            from build_portal import stamp_pdf_metadata
            stamp_pdf_metadata(
                full_pdf_repo,
                title="III. Maarif Kongresi Tam Metin Bildirisi (MOIJUB) — Quran Vision v6.2.3",
                subject="TYMM 2026 DKAB 26 Adımlı Öğretim Tasarımı ve V16.2 Çoklu Sunucu Doğrulama Sicili",
            )
            stamp_pdf_metadata(
                ek1_pdf_repo,
                title="III. Maarif Kongresi Genişletilmiş Bildiri Özeti (MOIJUB — Ek-1 Şablonu)",
                subject="TYMM 2026 DKAB 26 Adımlı Öğretim Tasarımı Özeti (500-750 Kelime)",
            )
        except Exception:
            pass
        shutil.copy2(full_pdf_repo, full_pdf_desktop)
        shutil.copy2(ek1_pdf_repo, ek1_pdf_desktop)
        print(f"1. Kongre PDF (Özet Ek-1) kaydedildi: {ek1_pdf_repo} ({ek1_pdf_repo.stat().st_size // 1024} KB)")
        print(f"2. Kongre PDF (Tam Metin) kaydedildi: {full_pdf_repo} ({full_pdf_repo.stat().st_size // 1024} KB)")
    for f in (tmp_html, tmp_ek1_html):
        if f.exists():
            f.unlink()


if __name__ == "__main__":
    main()
