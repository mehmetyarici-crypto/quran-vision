---
gem_version: "6.1.1"
case_id: "GEM-RAPOR-TEST-001"
surah: "Fâtiha"
verse: "1:1"
topic: "Test Raporu"
date: "2026-10-15"
layer: 3
h6: true
confidence_grade: "B"
status: "PRE-RELEASE"
sha256_hash: "0000000000000000000000000000000000000000000000000000000000000000"

classical_sources:
  - id: "src-zemahseri"
    author: "Zemahşerî, Mahmûd b. Ömer"
    death_year: "ö. 538/1144"
    work: "el-Keşşâf"
    volume: "1"
    pages: "10-15"
    verification_link: "https://archive.org/test"

modern_sources:
  - id: "mod-wb"
    institution: "World Bank"
    title: "Worldwide Governance Indicators"
    publication_year: 2025
    url: "https://databank.worldbank.org"

thresholds:
  - id: "th-01"
    name: "Örnek Eşik"
    value: "<= %15"
    derivation_basis: "[TAHMİNÎ EŞİK] Test modelleme hipotezi"
    is_empirical: false

scenarios:
  - id: "S1"
    title: "Baz Senaryo"
    score_justification: "Gerekçelendirilmiş metodolojik simülasyon puanı."

peer_review:
  status: "PENDING_EXTERNAL_REVIEW"
  review_notes: "Ön sürüm inceleme kaydı."
---

# GEM TEST RAPORU

## ADIM 00 — KÜNYE
- **Vaka Kodu:** GEM-RAPOR-TEST-001
- **Güven Düzeyi:** B

## ADIM 00-5 — DİL MATRİSİ
1. İbn Fâris:
   - `[NAKİL]`: el-Müfredât ve Makâyîs ibaresi.
   - `[YORUM]`: Kök anlam analizi.
2. Zemahşerî:
   - `[NAKİL]`: Keşşâf ibaresi.
   - `[YORUM]`: Belâğat nüktesi.
3. İbn Manzûr:
   - `[NAKİL]`: Lisânü'l-Arab ibaresi.
   - `[YORUM]`: Lisan tahlili.

## ADIM 01 — LAFZÎ TAHLİL
- Metin çözümlemesi.
- `[NAKİL]`: Zemahşerî tefsir aktarımı.
- `[YORUM]`: Anlamsal çıkarım.

## ADIM 02 — MANTIKSAL SEMANTİK VE KARŞIT İLKE
- Karşıt ilke dengesi.

## ADIM 03 — ETHOS, LOGOS, PATHOS VE OLGU-DEĞER
- Hume giyotini ve is-ought köprüsü denetimi.

## ADIM 04 — MAKASID ANALİZİ
- Zarûriyyât koruması.

## ADIM 04b — YORUMCU KONUMU
- Çoğulcu usûl yaklaşımı.

## ADIM 05 — SİYAK-SİBAK VE S7
- S1, S2 bağlamı ve S7 kırpma riski denetimi.

## ADIM 06 — ÇAPRAZ ÂYET VE N4
- N4 hitap ilişkisi ve EU-01 erken uyarı sinyali.

## ADIM 07 — SİSTEM HARİTASI VE CLD
- Tipping point ve döngüler.

## ADIM 08 — DÖRT SENARYO
- Koruyucu ve çözülme senaryoları.

## ADIM 09 — ZAMAN UFKU
- H1 ve H4 zaman aralığı ve yıllık pencere.

## ADIM 10 — MORFOLOJİK GÖZLEM
- Dilbilimsel gözlem.

## ADIM 10b — BELİRSİZLİK VE KARAR STRATEJİSİ
- Minimax stratejisi.

## ADIM 11 — SEKİZ İÇ DENETİM TESTİ
- Algoritmik iç tutarlılık testleri.

## ADIM 12 — RED TEAM VE FALSIFIABILITE
- Falsifiabilite protokolü.
- Endeks ve veri kaynağı: Dünya Bankası veritabanı. Sayısal eşik değeri belirlenmiştir.

### ADIM 13 — ENFÜSÎ-ÂFÂKÎ DİYALEKTİK VE KALP FIKHI (İRFÂNÎ / İŞÂRÎ KATMAN)

#### 13.1. Enfüsî-Âfâkî Diyalektik (Varlık ve Algı Düzeyi)
- **[YORUM]** Âyetin dışsal ve kurumsal boyutu (âfâk) ile bireyin içsel vicdan ve niyet muhasebesi (enfüs) arasındaki ontolojik ayna ilişkisi (Fussilet 41:53) ve Adım 15 karar kollarına kurduğu ahlâkî köprü.

#### 13.2. Kalp Fıkhı ve Bâtınî İlletler (*Fıkhü'l-Bâtın*)
- **[YORUM]** Hâris el-Muhâsibî (*er-Ri'âye li-Hukûkillâh*) ve Ebû Hâmid el-Gazzâlî (*İhyâ'u 'Ulûmi'd-Dîn*) metodolojisiyle bâtınî illetlerin (kibir, riyâ, ucb, tamah, gazap, kasvet) teşhisi ve tezkiyesi.

#### 13.3. Klasik İşârî ve İrfânî Tahrîc
- **[NAKİL]** Abdülkerîm el-Kuşeyrî (*Letâ'ifü'l-İşârât*), Sehl et-Tüsterî (*Tefsîru't-Tüsterî*) veya İbn Acîbe (*el-Bahrü'l-Medîd*) kaynaklarından harekeli Arapça iktibas, tercüme ve İSNAD 2 künyesi.
- **[YORUM]** İşârî ibarenin zâhirî fıkıh hükmünü iptal etmeksizin kurduğu kalbî derinlik sentezi.
## ADIM 14 — ERKEN UYARI VE BAYES
- Prior ve posterior güncellenmiş olasılık değerleri. Bayes güncellemesi.

## ADIM 15 — KARAR VE POLİTİKA KOLLARI
- Karar kolu ve aktör sorumlulukları.

## ADIM 16 — ÖNYARGI VE DİL GÜVENLİĞİ
- Öz-denetim ve dil güvenliği filtreleri. Yasaklı kelime kullanılmamıştır.

## ADIM 17 — GÜVEN DÜZEYİ VE AKTÖR HARİTASI
- Aktör güç haritası.

## ADIM 18 — BİLGİ TABANI VE ZAYIFLIK LİSTESİ
- Zayıflık ve geliştirme önerileri listesi.

## ADIM 19 — İZLEME VE RETRODICTION
- Retrodiction tarihsel doğrulaması.

### ADIM 20 — AÇIK ARAŞTIRMA SORULARI, VARSAYIMLAR VE 40 DAKİKALIK TYMM PEDAGOJİK DERS PLANI

#### 20.1. Genel Bilgiler, TTKB 2026 Program Hizalaması ve Beceri Matrisi
- Açık araştırma soruları ve temel varsayımlar.
- Öğrenme Çıktısı: DKAB.10.1.3, Alan Becerileri: DAB1, DAB2, DAB3, Sosyal-Duygusal Beceriler: SDB1.2, SDB3.3.

#### 20.2. Beş Aşamalı 40 Dakikalık Ders Akış Raporu ve Doldurulmuş Uygulama Araçları
- Anlam Çözümleme Tablosu, Yapılandırılmış Grid, Zıt Panel, Konuşma Halkası ve Çıkış Kartı uygulamaları.

#### 20.3. Farklılaştırma Protokolü (Zenginleştirme ve Destekleme)
- Zenginleştirme ve Destekleme basamakları.

#### 20.4. Metodolojik Denetim ve 3'lü Doğrulama Filtresi
- Lafzî iktibas, pedagojik süreç ve din istismarını önleme filtreleri.

## Z-1 · ŞABLONA SIĞMAYAN ÖZGÜN PROBLEMATİK
- Âyetin analitik aporia tartışması.

## Z-2 · GÖRÜŞ İHTİLAFI CETVELİ
- Farklı fıkhî mezheplerin ihtilaf tablosu.

## Z-3 · ZAYIFLIK VE GELİŞTİRME ÖNERİLERİ
- Metodolojik sınırlılıklar.

## Z-4 · STANDART VE DÜRÜST EPİSTEMİK SINIR BEYANI
> Bu rapor iç tutarlılık denetiminden geçmiş olup bir fetva niteliği taşımaz.

## Z-4.5 · AKADEMİK KAYNAKÇA (İSNAD 2 VE APA / DOI BİBLİYOGRAFYASI)
- **Zemahşerî, Mahmûd b. Ömer (ö. 538/1144).** *el-Keşşâf*.
- **World Bank (2025).** *Worldwide Governance Indicators*. https://databank.worldbank.org

## Z-5 · HAKEM VE AKRAN DEĞERLENDİRME KAYDI
- Ön sürüm hakem kütüğü.
