---
gem_version: "6.2.1"
case_id: "QV-2026-0XX"
surah: "{{SURE_ADI}}"
verse: "{{SURE_NO}}:{{AYET_NO}}"
topic: "{{KONU_BASLIGI}}"
date: "{{TARIH}}"
layer: 3
h6: true
confidence_grade: "B"
status: "PRE-RELEASE"
sha256_hash: "0000000000000000000000000000000000000000000000000000000000000000"

classical_sources:
  - id: "src-zemahseri"
    author: "Zemahşerî, Mahmûd b. Ömer"
    death_year: "ö. 538/1144"
    work: "el-Keşşâf 'an Hakâ'ikı Gavâmizi't-Tenzîl"
    editor: "Âdil Ahmed Abdülmevcûd, Ali Muhammed Muavvaz"
    publisher: "Mektebetü'l-Ubeykân"
    publication_place: "Riyad"
    publication_year: 1998
    volume: "1"
    pages: "1-10"
    arabic_quote: "..."
    verification_link: "https://shamela.ws/book/23627"
    doi_or_urn: "urn:shamela:23617"

  - id: "src-ibn-faris"
    author: "İbn Fâris, Ahmed b. Fâris"
    death_year: "ö. 395/1004"
    work: "Mu'cemü Makâyîsi'l-Lüğa"
    editor: "Abdüsselâm Muhammed Hârûn"
    publisher: "Dârü'l-Fikr"
    publication_place: "Beyrut"
    publication_year: 1979
    volume: "1"
    pages: "1-5"
    arabic_quote: "..."
    verification_link: "https://shamela.ws/book/21710"
    doi_or_urn: "urn:shamela:23721"

  - id: "src-ragib"
    author: "Râgıb el-İsfahânî, Hüseyin b. Muhammed"
    death_year: "ö. 502/1108"
    work: "el-Müfredât fî Garîbi'l-Kur'ân"
    editor: "Safvân Adnân Dâvûdî"
    publisher: "Dârü'l-Kalem"
    publication_place: "Dımaşk"
    publication_year: 1992
    volume: "1"
    pages: "1-10"
    arabic_quote: "..."
    verification_link: "https://shamela.ws/book/23636"
    doi_or_urn: "urn:shamela:8381"

  - id: "src-ibn-manzur"
    author: "İbn Manzûr, Muhammed b. Mükerrem"
    death_year: "ö. 711/1311"
    work: "Lisânü'l-Arab"
    editor: "Dârü Sâdır"
    publisher: "Dârü Sâdır"
    publication_place: "Beyrut"
    publication_year: 1993
    volume: "1"
    pages: "1-10"
    arabic_quote: "..."
    verification_link: "https://shamela.ws/book/1687"
    doi_or_urn: "urn:shamela:21605"

modern_sources:
  - id: "mod-wjp"
    institution: "World Justice Project (WJP)"
    title: "WJP Rule of Law Index"
    publication_year: 2025
    publication_place: "Washington, D.C."
    publisher: "World Justice Project"
    url: "https://worldjusticeproject.org"
    doi: "doi:10.34648/wjp.2025.01"

  - id: "mod-worldbank"
    institution: "World Bank Group"
    title: "Worldwide Governance Indicators (WGI)"
    publication_year: 2025
    publication_place: "Washington, D.C."
    publisher: "The World Bank"
    url: "https://databank.worldbank.org"

thresholds:
  - id: "th-01"
    name: "Örnek Politika Eşik Göstergesi"
    value: "<= %15"
    derivation_basis: "[TAHMİNÎ EŞİK] Modern mukayeseli ceza ve kamu politikası göstergelerine dayalı çalışma hipotezi"
    is_empirical: false

scenarios:
  - id: "S1"
    title: "Baz Senaryo"
    scores:
      olasilik: 3
      tesir: 4
      firsat: 3
      kirilganlik: 3
      stratejik_oncelik: 4
    score_justification: "Metodolojik simülasyon ve tarihsel içtihat dengesi analizi."

peer_review:
  status: "PENDING_EXTERNAL_REVIEW"
  internal_linter_verified: false
  linter_timestamp: null
  reviewer_name: null
  reviewer_title: null
  reviewer_orcid: null
  reviewer_institution: null
  review_date: null
  review_notes: "Ön sürüm (PRE-RELEASE); bağımsız dış akademik hakem incelemesine açıktır."
---

# {{SURE_ADI}} Sûresi {{SURE_NO}}:{{AYET_NO}} Tahlili — {{KONU_BASLIGI}}

## FAZ I — KİMLİK, METİN VE BAĞLAM

### ADIM 00 — KÜNYE VE GİRİŞ BİLGİLERİ
- **Vaka Kodu:** QV-2026-0XX
- **Âyet:** {{SURE_ADI}} {{SURE_NO}}:{{AYET_NO}}
- **Konu Başlığı:** {{KONU_BASLIGI}}
- **Tarih:** {{TARIH}}
- **Sürüm:** v6.2.1
- **Katman:** 3 (26 Adım + 5 Makro Faz + Z-1..Z-5)
- **H6 Durumu:** Evet
- **Dil:** Türkçe (TR)
- **Güven Düzeyi:** B
- **Rapor Durumu:** Ön Sürüm (`PRE-RELEASE`)
- **Kriptografik Bütünlük (SHA256):** `0000000000000000000000000000000000000000000000000000000000000000` (veya harici `.sha256` manifesti)

---

### ADIM 00-5 — DİL VE SEMANTİK MATRİSİ (H6 ZORUNLU)
1. **Kök Anlam ve İştikak (İbn Fâris — Makâyîsü'l-Lüğa):**
   - `[NAKİL]`: (Arapça ibare ve künyeli aktarım)
   - `[YORUM]`: (Kavramsal kök çıkarımı)
2. **Kur'anî Semantik (Râgıb el-İsfahânî — el-Müfredât):**
   - `[NAKİL]`: (Kur'an içi kavramsal kullanım tespiti)
   - `[YORUM]`: (Nass bağlamında kazandığı özgün anlam)
3. **Nahiv, İ'câz ve Belâğat (Zemahşerî — el-Keşşâf):**
   - `[NAKİL]`: (Arapça ibare ve sözdizimi tahlili)
   - `[YORUM]`: (Belâğî nükte ve anlamsal açılım)
4. **Klasik Lisan ve Örf (İbn Manzûr — Lisânü'l-Arab):**
   - `[NAKİL]`: (Arapça lisan şahidi ve kullanım örneği)
   - `[YORUM]`: (Tarihsel lisan tahlili)
- **Çapraz Kontrol ve Dil Güvenliği:** Dörtlü lisan matrisinin iç tutarlılığı ve mutabakat tespiti.

---

### ADIM 01 — LAFZÎ TAHLİL
- **Arapça Metin:** {{ARAPCA_METIN}}
- **Kelime Mealleri:**
- **Zemahşerî Tahlili:**
  - `[NAKİL]`: ...
  - `[YORUM]`: ...

---

### ADIM 02 — MANTIKSAL SEMANTİK VE KARŞIT İLKE TESTİ
- **Önerme Yapısı:**
- **Karşıt İlke Testi:** Nassın koruduğu asıl makasıd ile çatışan alternatif maslahatların tartılması ve sınır tayini.

---

### ADIM 03 — ÜÇLÜ ÇERÇEVE (ETHOS / LOGOS / PATHOS) VE İS-OUGHT KÖPRÜSÜ
- **Ethos (Ahlaki Yük):**
- **Logos (Mantıksal Tutarlılık):**
- **Pathos (Vicdani ve Duygusal Tesir):**
- **İs-Ought Köprüsü ve Hume Giyotini:** Olgudan (olan) değere (olması gereken) geçerken mantıksal sıçramaların engellenmesi; olgu-değer ayrımının korunması.

---

### ADIM 04 — MAKASID ANALİZİ
- **Küllî Makasıd:** Can, mal, akıl, nesil, din emniyeti.
- **Şâtıbî ve İbn Âşûr Çerçevesi:**
  - `[NAKİL]`: ...
  - `[YORUM]`: ...

---

### ADIM 04b — YORUMCU KONUMU (GADAMER HERMENÖTİĞİ)
1. **Usûl Ekolü:** (Örn. Çoğulcu-Makāsıdî Hanefî yaklaşımı)
2. **Felsefi Perspektif:** (Örn. Eleştirel realizm ve sistem kuramı)
3. **Alternatif Yorumcu Konumu:** (Örn. Zâhirî veya lafızcı bir usûlün üreteceği farklı netice)

---

### ADIM 05 — SİYAK-SİBAK ANALİZİ (S1–S7)
- **S1 (Önceki Âyet):**
- **S2 (Sonraki Âyet):**
- **S3 (Pasajın Konumu):**
- **S4 (Sûre İçi Bütünlük):**
- **S5 (Nüzûl Sebepleri ve Hitap):**
- **S6 (Tarihsel Bağlam):**
- **S7 (Kırpma Riski):** Âyetin bağlamından koparılması riski ve metin içi emniyet kilidi.

---

### ADIM 06 — ÇAPRAZ ÂYET ANALİZİ
- Nassı tahsis veya takyid eden çapraz âyetler zinciri. Hitap kapsam ilişkisi (`N4`).

---

## FAZ II — SİSTEM VE GELECEK MODELLEMESİ

### ADIM 07 — SİSTEM HARİTASI (CAUSAL LOOP DİAGRAMI)
- Geri besleme döngüleri, pekiştirici (R) ve dengeleyici (B) mekanizmalar, gecikmeler ve tipping point kırılma noktaları.

---

### ADIM 08 — DÖRT SENARYO VE STRATEJİK DEĞERLENDİRME
- **Senaryo 1 (Koruyucu / İdeal Uygulama):**
- **Senaryo 2 (Yozlaşma ve Şekilcilik):**
- **Senaryo 3 (Sosyal Çözülme / Denge Kaybı):**
- **Senaryo 4 (İhya ve Dönüştürücü Reform):**
*(Tüm puanlar YAML frontmatter altındaki gerekçelere dayanır; V5 kuralı).*

---

### ADIM 09 — ZAMAN UFKU BANDI (H1–H4)
- **H1 (0–3 Yıl):** Yakın dönem yıllık pencere.
- **H2 (3–10 Yıl):** Orta vadeli zaman aralığı.
- **H3 (10–30 Yıl):** Yapısal kurumsal dönem.
- **H4 (30+ Yıl Medeniyet Ufku):** Uzun erimli stratejik ufuk.

---

### ADIM 10 — MORFOLOJİK GÖZLEM
- Bilgisayarlı morfolojik frekans ve vezin özellikleri (Ebced ve sayısal batıl teviller yasaktır).

---

### ADIM 10b — BELİRSİZLİK VE KARAR STRATEJİSİ
- Knightian belirsizlik parametreleri, robust ve minimax stratejileri.

---

## FAZ III — SINAMA, KARŞI OKUMA VE AHLAKÎ DEĞERLENDİRME

### ADIM 11 — 8 İÇ DENETİM TESTİ (ALGORİTMİK İÇ TUTARLILIK)
- **Test 1:** Lafız ve semantik uyumu.
- **Test 2:** Siyak-sibak tutarlılığı.
- **Test 3:** Makasıd dengesi.
- **Test 4:** Karşıt ilke tutarlılığı.
- **Test 5:** S7 kırpma riski denetimi.
- **Test 6:** Dil güvenliği ve mutlakiyet yasağı.
- **Test 7:** Taban oran (Base-rate) ve veri uyumu.
- **Test 8:** Öz-denetim ve rol ayrımı.
*(ÖNEMLİ: Bu testler algoritmik iç tutarlılık denetimidir; bağımsız dış akademik hakem onayı değildir).*

---

### ADIM 12 — RED TEAM (KARŞIT OKUMA) VE FALSIFIABILITE PROTOKOLÜ
- **Red Team İtirazları:**
- **Falsifiabilite Protokolü (Yalnızca Ampirik ve Dünyevi Politika Hipotezlerine):**
  - **Uygulanan Alan:** Karar kollarındaki ampirik uygulama modeli.
  - **Zaman Aralığı:** 5 Yıllık İzleme Penceresi (2026–2031).
  - **Bağımsız Endeks / Veri Kaynağı:** Dünya Bankası Hukukun Üstünlüğü Endeksi veritabanı / BM İnsani Gelişme Raporu.
  - **Sayısal Eşik ve Tipping Point:** Eğer belirlenen sayısal eşik aşılırsa politika hipotezi yanlışlanmış kabul edilir.

---

### ADIM 13 — ENFÜS-ÂFÂK VE KALP FIKHI
- **Enfüs (İçsel ve Ahlaki Boyut):** Âyetin niyet, vicdani muhasebe ve ahlaki yönelişle ilişkisi.
- **Âfâk (Dışsal ve Kurumsal Boyut):** Bu yönelişlerin kurumsal, iktisadi ve maddi dünyadaki izdüşümü.
- **Karşılıklı Etki:** Bireyin iç dünyası ile toplumsal şartların birbirini nasıl beslediği veya bozduğu.
- **Karar Köprüsü:** İçsel muhasebenin Adım 15'teki hangi karar koluna ve kaldıraç noktasına dayanak teşkil ettiği.
- **İşârî / İrfanî Derinlik:** Güvenilir kaynak ve yönteme dayalı ahlaki açılım (fıkhî hüküm yerine ikame edilemez).

---

## FAZ IV — BAYES, KARAR VE ETİK DENETİM

### ADIM 14 — ERKEN UYARI SİNYALLERİ VE BAYES GÜNCELLEMESİ
- **Erken Uyarı Sinyalleri (EU-01..EU-04):**
- **Bayes Güncelleme Alanı:**
  - **Önsel Olasılık (Prior P(H)):** 0.35 (Ampirik gerekçeli veya öznel çalışma hipotezi).
  - **Veri / Kanıt P(E|H):**
  - **Sonsal Olasılık (Posterior P(H|E)):** Güncellenmiş olasılık.

---

### ADIM 15 — KARAR VE POLİTİKA KOLLARI (K1–Kn)
- **Karar Kolu 1 (K1):**
  - **Aktör:** ...
  - **Hedef Değişken:** ...
  - **Araç:** ...
  - **CLD Kaldıraç Noktası:** Adım 07'deki döngüye müdahale.
  - **Eşik:** [TAHMİNÎ EŞİK] ...
- **Karar Kolu 2 (K2):**
  - **Aktör:** ...
  - **Eşik:** [TAHMİNÎ EŞİK] ...
- **Karar Kolu 3 (K3):**
  - **Aktör:** ...
  - **Eşik:** [TAHMİNÎ EŞİK] ...

---

### ADIM 16 — ÖNYARGI VE TARAFLILIK DENETİMİ
- Modernist, mezhepçi veya apologetik anakronizm filtreleri.
- Dil güvenliği ve öz-denetim: Yasaklı kelime kullanılmamıştır.

---

## FAZ V — GÜVEN, SORUMLULUK VE İZLEME KAYDI

### ADIM 17 — GÜVEN DÜZEYİ
- **Nitel Derece:** B (Orta-Yüksek Analitik Güven). Sayısal bir olasılık veya kesinlik değildir.

---

### ADIM 17b — AKTÖR VE GÜÇ HARİTASI
- Karar vericiler, uygulayıcılar, etkilenen gruplar ve gelecek nesiller.

---

### ADIM 18 — BİLGİ TABANI VE ZAYIFLIK LİSTESİ
- İddia bilgi statüleri (kaynaklı nakil, analitik yorum, çalışma hipotezi).
- Yöntemin temel sınırlılıkları ve zayıflıkları.

---

### ADIM 18.1 — DİL GÜVENLİĞİ
- Rapor metninde kesinlik, tekelcilik veya sahte-onay iddialarından arındırma denetimi.

---

### ADIM 19 — İZLEME VE GERİYE DÖNÜK SINAMA (RETRODICTION)
- **İzleme KPI:**
- **Retrodiction:** Tarihsel örnek olay üzerinde modelin geriye dönük sınanması.

---

### ADIM 20 — AÇIK ARAŞTIRMA SORULARI VE VARSAYIMLAR
- Çözümlenmemiş açık sorular ve analizin dayandığı temel varsayımlar.

---

## KOŞULLU EKLER (Z-1 — Z-5)

### Z-1 · ŞABLONA SIĞMAYAN ÖZGÜN PROBLEMATİK [V9 ZORUNLU]
Bu âyetin analitik şablonun sınırlarını aşan özgün aporiası, teolojik gerilimi veya felsefi açmazı burada açıkça tartışılır. Sistemin nerede durduğu ve cevapsız kalan hususlar dürüstçe ortaya konur.

---

### Z-2 · GÖRÜŞ İHTİLAFI CETVELİ [V3 ZORUNLU]
| Görüş Sahibi / Ekol | Lafzî Yorumu | Hukuki / İtikadi Neticesi | Dayandığı Delil |
| :--- | :--- | :--- | :--- |
| **Görüş 1 (Cumhur / Klasik)** | ... | ... | ... |
| **Görüş 2 (Alternatif Mezhep)** | ... | ... | ... |
| **Görüş 3 (Tasavvufi / İrfanî)** | ... | ... | ... |
| **Görüş 4 (Çağdaş / Tarihselci)** | ... | ... | ... |

---

### Z-3 · ZAYIFLIK, VARSAYIM VE GELİŞTİRME ÖNERİLERİ LİSTESİ
- **Temel Varsayımlar:**
- **Metodolojik Zayıflıklar ve Geliştirme Önerisi:**
- **Açık / Cevaplanmamış Sorular:**

---

### Z-4 · STANDART VE DÜRÜST SINIR İFADESİ [V10 ZORUNLU]
> **METODOLOJİK VE EPİSTEMİK SINIR BEYANI:**
> Bu rapor; Kur'an Temelli Gelecek Vizyonu (Quran Vision v6.2.1) mimarisi çerçevesinde üretilmiş analitik ve hermenötik bir modellemedir. Dini bir fetva, kesin kazi bir hüküm veya ilahi muradın eksiksiz ve yegâne tefsiri niteliği taşımaz. Raporda yer alan simülasyonlar, göstergeler ve politika kolları; analistin benimsediği usûl ekolünün ve ampirik varsayımların bir türevidir. Bu metin, kod tabanlı biçimsel iç tutarlılık denetiminden (gem_lint.py) geçmiş olup, bağımsız dış akademik hakem heyeti (peer-review) tarafından tescil edilmedikçe bilimsel kesinlik iddiası barındırmaz.

---

### Z-4.5 · AKADEMİK KAYNAKÇA (İSNAD 2 VE APA / DOI BİBLİYOGRAFYASI)

#### A) Klasik İslami Kaynaklar (İSNAD 2. Edisyon Standartlı)
- **İbn Fâris, Ebü'l-Hüseyn Ahmed b. Fâris b. Zekeriyyâ (ö. 395/1004).** *Mu'cemü Makâyîsi'l-Lüğa*. Tahkik: Abdüsselâm Muhammed Hârûn. 6 Cilt. Beyrut: Dârü'l-Fikr, 1399/1979.
- **İbn Manzûr, Muhammed b. Mükerrem (ö. 711/1311).** *Lisânü'l-Arab*. 15 Cilt. Beyrut: Dârü Sâdır, 1410/1990.
- **Râgıb el-İsfahânî, Ebü'l-Kâsım Hüseyn b. Muhammed (ö. 502/1108 [?]).** *el-Müfredât fî Garîbi'l-Kur'ân*. Tahkik: Safvân Adnân Dâvûdî. Dımaşk: Dârü'l-Kalem, 1412/1992.
- **Zemahşerî, Cârullah Ebü'l-Kâsım Mahmûd b. Ömer (ö. 538/1144).** *el-Keşşâf 'an Hakâ'ikı Gavâmizi't-Tenzîl*. Tahkik: Âdil Ahmed Abdülmevcûd ve Ali Muhammed Muavvaz. 6 Cilt. Riyad: Mektebetü'l-Ubeykân, 1418/1998.

#### B) Çağdaş Kurumsal, Hukuki ve Ampirik Kaynaklar (APA 7 / DOI Standartlı)
- **World Bank Group (2025).** *Worldwide Governance Indicators (WGI)*. Washington, D.C.: The World Bank. Erişim adresi: https://databank.worldbank.org
- **World Justice Project [WJP] (2025).** *WJP Rule of Law Index*. Washington, D.C.: World Justice Project. https://worldjusticeproject.org

#### C) Metin İçi Akademik Dipnotlar (Footnotes)
[^1]: İbn Fâris, *Mu'cemü Makâyîsi'l-Lüğa*, thk. Abdüsselâm Muhammed Hârûn (Beyrut: Dârü'l-Fikr, 1979), 1: 1-5.
[^2]: Râgıb el-İsfahânî, *el-Müfredât fî Garîbi'l-Kur'ân*, thk. Safvân Adnân Dâvûdî (Dımaşk: Dârü'l-Kalem, 1992), 1-10.
[^3]: İbn Manzûr, *Lisânü'l-Arab* (Beyrut: Dârü Sâdır, 1990), 1: 1-10.
[^4]: Zemahşerî, *el-Keşşâf 'an Hakâ'ikı Gavâmizi't-Tenzîl* (Riyad: Mektebetü'l-Ubeykân, 1998), 1: 1-10.

---

### Z-5 · HAKEM VE AKRAN DEĞERLENDİRME KAYDI [V11 ZORUNLU]
- **Hakem Adı / Soyadı:** Henüz atanmadı
- **Akademik Ünvanı ve Kurumu:** —
- **ORCID No:** —
- **Değerlendirme Tarihi:** —
- **Hakem Kararı:** `HENÜZ ATANMADI (ÖN SÜRÜM / PRE-RELEASE)`
- **Hakem Değerlendirme Notu:** Rapor v6.2.1 biçimsel standartlarına göre hazırlanmış ön sürüm niteliğindedir. Bağımsız dış akademik hakem incelemesine açıktır.
