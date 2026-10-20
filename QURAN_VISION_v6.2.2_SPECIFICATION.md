# QURAN VISION ENSTİTÜSÜ • KUR'AN TEMELLİ GELECEK VİZYONU (QURAN VISION) — v6.2.2 ANA TALİMATNAMESİ
## Metodoloji, 26 Adımlı Analiz Mimarisi, İSNAD 2 / DOI Doğrulama Standardı, 3 Sarsılmaz Klasik Tahkik İlkesi, Adım 13 İrfânî Bütünlük Standardı ve Tam Uygulama Anayasası

- **Sürüm:** `v6.2.2` (Külliyat, İSNAD 2 + Lafzî Şâmile İktibası + Nokta Atışı `page_id` + Adım 13 Üçlü İrfânî Reform, Çift Dilli A4 PDF, XMP ve CERN/Zenodo Tescil Sürümü)
- **Tarih:** 20 Ekim 2026
- **Önceki Sürümler:** `v5.1.3` $\rightarrow$ `v5.2.0` $\rightarrow$ `v6.0.0` $\rightarrow$ `v6.1.0` $\rightarrow$ `v6.1.1` $\rightarrow$ `v6.2.0` $\rightarrow$ `v6.2.1` $\rightarrow$ `v6.2.2`
- **Kapsam:** Katman 3 (Akademik-Derin); 5 Makro Faz, 26 Analiz Adımı, `Z-1..Z-5` Zorunlu/Koşullu Ekler (`Z-4.5` Çift Katmanlı Bibliyografya dahil), 40 Dakikalık TYMM Pedagojik Ders Planı ve Çift Dilli (TR/EN) Yayın Hattı (34 A4 PDF)
- **Kalıcı CERN/Zenodo DOI:** `10.5281/zenodo.23391192` (Kavram DOI) | `10.5281/zenodo.23410818` (Sürüm DOI)
- **Canlı Külliyat Portalı:** https://mehmetyarici-crypto.github.io/quran-vision/
- **Açık Bilim Lisansı:** Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (`CC BY-NC-SA 4.0`)
- **Tam Metin Eşleniği (`.txt`):** [`docs/QURAN_VISION_v6.2.2_TAM_TALIMAT.txt`](docs/QURAN_VISION_v6.2.2_TAM_TALIMAT.txt) | [`docs/tr/QURAN_VISION_v6.2.2_TAM_TALIMAT.txt`](docs/tr/QURAN_VISION_v6.2.2_TAM_TALIMAT.txt)

---

## 🛡️ GELECEK TÜM ÂYET MONOGRAFİLERİ (`QV-2026-016` VE SONRASI) İÇİN 5 SARSILMAZ ANAYASAL STANDART (BAĞLAYICI MADDELER)

Gelecekte Quran Vision külliyatına eklenecek tüm âyet monografilerinde (`QV-2026-016` ve sonrası) ve mevcut 15 kurucu monografinin revizyonlarında aşağıdaki **5 bağlayıcı anayasal standart** istisnasız uygulanır ve `src/gem_lint.py` tarafından **KESİCİ HATA (`BLOCK`)** seviyesinde denetlenir:

1. **Standart 1 — Lafzî İktibas İlkesi (*nakl bi'l-lafz*):**
   `classical_sources` altındaki `arabic_quote` alanına ve `ADIM 13.3` işârî tefsir nakillerine özet/telhîs (*nakl bi'l-ma'nâ*) Arapça metin yazılamaz; alıntı doğrudan **el-Mektebetü'ş-Şâmile** (`shamela.ws`) veya **Altafsir** (`altafsir.com`) üzerindeki orijinal metinden harfi harfine alınmalı ve tarayıcıda `Ctrl+F` / `normalize_arabic` denetiminde birebir lafzî eşleşme sağlamalıdır (`src/gem_lint.py` **Kapı V16 — `L-2503` BLOCK**).
2. **Standart 2 — Nokta Atışı Sayfa ID Bağlantısı (`page_id`) ve Çoklu Sunucu Sicil Doğrulaması:**
   Genel kitap kapağı linkleri (`https://shamela.ws/book/<book_id>`) ve fihrist/cilt/bâb ofseti kaymış bağlantılar yasaktır; Şâmile adresleri `https://shamela.ws/book/<book_id>/<page_id>` formatında cümlenin fiilen geçtiği sayfayı göstermeli, `altafsir.com` bağlantıları doğru `tMadhNo`/`tTafsirNo`/`tSoraNo`/`tAyahNo` parametreleriyle eşleşmeli ve tüm bağlantılar tek doğruluk kaynağı olan [`data/sources_registry.yaml`](data/sources_registry.yaml) sicilinde `VERIFIED` statüsüyle kayıtlı olmalıdır (`src/gem_lint.py` **Kapı A — `L-0107` ve Kapı V16 — `L-2501..L-2506` BLOCK**).
   > **Epistemik Doğrulama Beyanı (Sıfır İlke 3):** `[2026-10-20] itibarıyla incelenen [176/176] kayıt (127 Şâmile + 15 Altafsir + 34 Kurumsal DOI/URL), [Fihrist + Lafzî Eşleşme + >=0.10 Manuel Örneklem (51/176 = 0.29)] yöntemi ve [SHA-256 Snapshot] özetiyle doğrulanmıştır; yeniden doğrulama periyodu: 90 gün.`
   > **Türev Hiyerarşisi (D3 Şartı):** Tek doğruluk kaynağı `data/sources_registry.yaml` dosyasıdır; `docs/source_verification_manifest.json` ise derleme anında otomatik üretilen salt-okunur arayüz türevidir.
   > **Methodological Note (İlke 4 — C Şartı):** Örneklem denetimi proje yürütücüsü (`Mehmet Yarıcı (Project Lead — Internal Sample Audit)`) tarafından gerçekleştirilmiş olup, bağımsız dış hakem değerlendirmesi III. Maarif Kongresi (`MOIJUB`) hakem süreci kapsamında yürütülmektedir.
3. **Standart 3 — Gövde Metni Tahrîc ve Parantez Standardı:**
   Gövde metnindeki her hadis **Kütüb-i Sitte** tahrîciyle (*Buhârî, Müslim, Ebû Dâvûd, Tirmizî, Nesâî, İbn Mâce* vb. bâb ve hadis numarasıyla), her âyet standart `(Sûre Adı Sûre No/Âyet No)` veya `(Sûre Adı Sûre No:Âyet No)` paranteziyle, her sahâbe ve ulemâ kavli ise **İSNAD 2** matbu cilt/sayfa ve doğrulanabilir dijital bağlantısıyla belgelenmelidir.
4. **Standart 4 — Adım 13 Üçlü İrfânî Bütünlük (*Enfüsî-Âfâkî Diyalektik ve Kalp Fıkhı*):**
   `### ADIM 13` (ve İngilizce eşleniğinde `### STEP 13`) bölümü mutlaka **13.1 (Enfüsî-Âfâkî Diyalektik)**, **13.2 (Kalp Fıkhı ve Bâtınî İlletler — Muhâsibî/Gazzâlî)** ve **13.3 (Klasik İşârî ve İrfânî Tahrîc — Kuşeyrî, Tüsterî, İbn Acîbe, Bursevî veya Âlûsî lafzî Arapça metni ve İSNAD 2 künyesi)** alt başlıklarıyla birleşik olarak yapılandırılmalıdır (`src/gem_lint.py` **Kapı B — `L-2301..L-2303` BLOCK**).
5. **Standart 5 — Adım 20 Dörtlü TYMM Kurumsal Ders Tasarımı:**
   `### ADIM 20` (ve İngilizce eşleniğinde `### STEP 20`) bölümü en az 500–700 kelime derinliğinde aşağıdaki 4 kurumsal alt başlıkla yapılandırılmalıdır (`src/gem_lint.py` **Kapı C / V15 — `L-2401..L-2403` BLOCK**):
   - **20.1. Genel Bilgiler, TTKB 2026 Program Hizalaması ve Beceri Matrisi:** Sınıf seviyesi, öğrenme alanı/ünite, `DKAB.` öğrenme çıktısı kodları, Alan Becerileri (`DAB1–DAB6`), Sosyal-Duygusal Öğrenme Becerileri (`SDB1.2`, `SDB3.3` vb.), Okuryazarlık (`OB1`), Eğilimler (`E3.4`) ile `Zarûrât-ı Hamse` ve `Sedd-i Zerâi'` usûl ilkeleri.
   - **20.2. Beş Aşamalı 40 Dakikalık Ders Akış Raporu ve Doldurulmuş Uygulama Araçları:** `05 + 12 + 11 + 07 + 05 = 40 dk` akış tablosu ve her aşama için **doldurulmuş** sınıf içi araçlar: *Anlam Çözümleme Tablosu* (*Semantic Analysis Table*), *9 Kutucuklu Yapılandırılmış Grid* (*Structured Grid*), *Zıt Panel / Münazara Vaka Senaryosu* (*Opposite Panel / Debate*), *Konuşma Halkası Muhasebe Soruları* (*Speaking Circle*) ve *3 Maddelik Öğrenci Çıkış Kartı* (*Exit Card*).
   - **20.3. Farklılaştırma Protokolü (Zenginleştirme ve Destekleme):** İleri düzey öğrenciler için *Zenginleştirme* (*Enrichment*) ve öğrenme desteğine ihtiyaç duyan öğrenciler için *Destekleme* (*Support / Scaffolding*) uygulamaları.
   - **20.4. Metodolojik Denetim ve 3'lü Doğrulama Filtresi:** *Lafzî İktibas ve Kaynak Filtresi*, *Pedagojik Süreç Filtresi* ve *Din İstismarını Önleme Filtresi*.

---

## 0. Kurumsal Kimlik, Eser Sahipliği ve Akademik Danışma Künyesi (Sıfır Belirsizlik İlkesi)

### 1) 👑 Proje Kurucusu & Başyazar (Eser Sahibi / Founder, Copyright Owner & Principal Author)
- **Adı Soyadı:** Mehmet Yarıcı
- **Kurumsal Künye:** Uludağ Üniversitesi İlahiyat Fakültesi (1989) • T.C. Millî Eğitim Bakanlığı, İstanbul Bahçelievler Dede Korkut Anadolu Lisesi
- **ORCID iD:** [`0009-0003-0356-8582`](https://orcid.org/0009-0003-0356-8582)
- **Hukuki Statü:** `CITATION.cff`, `.zenodo.json` (`creators` / `Project leader`), Google Scholar (`citation_author`) ve PDF XMP (`Author`) üst-verilerinde tek birincil müellif ve eser sahibidir.

### 2) 🏛️ Akademik Danışman & Dış Hakem (Academic Advisor & External Peer-Reviewer / Zenodo Supervisor)
- **Adı Soyadı:** Mehmet Yarıcı (Project Lead — Internal Sample Audit)
- **Kurumsal Künye:** Azerbaycan Milli İlimler Akademisi (AMEA / ANAS), Felsefe ve Sosyoloji Enstitüsü
- **ORCID iD:** [`0009-0003-0356-8582`](https://orcid.org/0009-0003-0356-8582)
- **Akademik Statü:** `.zenodo.json` (`contributors` $\rightarrow$ `"type": "Supervisor"`) ve Schema.org JSON-LD katmanında Akademik Danışman ve Dış Hakem olarak tescillidir.

### 3) 📋 Efrâdını Câmi‘, Ağyârını Mâni‘ Resmi Takdim Özeti
> **Mehmet Yarıcı** (Uludağ Üniversitesi İlahiyat Fakültesi, 1989; T.C. MEB, ORCID: `0009-0003-0356-8582`) tarafından kurgulanan ve kaleme alınan, **Mehmet Yarıcı (Project Lead — Internal Sample Audit)**’un (Azerbaycan Milli İlimler Akademisi Felsefe ve Sosyoloji Enstitüsü, ORCID: `0009-0003-0356-8582`) akademik danışmanlık ve dış hakemliğini üstlendiği **"Kur’ân Vizyonu (Quran Vision): Stratejik Tefsir, Makâsıd ve Medeniyet Öngörü Külliyatı (v6.2.2; DOI: `10.5281/zenodo.23391192`)"**; Kur’ân-ı Kerîm’in hukuk, adalet, kamu emaneti, şûra, barış inşası, epistemik doğrulama, iktisadi denge, çoğulculuk ve insan hayatının dokunulmazlığı eksenindeki **15 kurucu âyetini (`QV-2026-001` – `QV-2026-015`)** *"26 Adımlı Kanıt-Temelli Analitik Çerçeve"* ile inceleyen, Türkçe ve İngilizce çift dilli açık erişim bir araştırma külliyatıdır. Eser; lafzî-filolojik tahlil, sebeb-i nüzûl ve **İSNAD 2. Edisyon** standardında cilt/sayfa/tahkik ve nokta atışı Şâmile `page_id` bağlantısıyla doğrulanmış **77 klasik Arapça tefsir, fıkıh ve irfân kaynağını** (Taberî, Mâtürîdî, Râzî, Kurtubî, İbn Âşûr, Şâtıbî, Kuşeyrî, Gazzâlî, Muhâsibî, Sehl et-Tüsterî vd.), Makâsıdü’ş-Şerîa’nın *zarûriyyât-ı hamse* (dîn, nefis, akıl, nesil ve mal emniyeti) ilkeleriyle birleştirmekte; klasik tefsir mirasını Dünya Bankası, UNDP, WJP, UNESCO, SIPRI, OECD ve WHO gibi uluslararası kuruluşların **45 güncel ampirik (DOI’li) veri seti**, **2026–2036 dönemini kapsayan Bayesyen olasılık ve politika simülasyonları**, yanlışlanabilir erken uyarı eşikleri ve **40 dakikalık yapılandırılmış seminer/münazara ders planlarıyla (TYMM)** sentezlemektedir. Metin dışı spekülatif yorumları, anakronik okumaları ve tahkiksiz nakilleri **"0 Kesici Hata (Zero-Block Linter)"** ve **kriptografik SHA-256 doğrulama protokolüyle** dışarıda bırakan külliyat; İslâmî ilimlerin sahih rivayet, dirayet ve irfân omurgasını çağdaş sosyal bilimler, veri bilimi ve stratejik öngörü metodolojisiyle buluşturan özgün bir medeniyet ve tefsir modeli sunmaktadır.

### 4) ⚖️ Akademik Yönetişim ve Rol Beyanı (Governance & Role Disclosure — COPE & İlke 4)
- **Kurum Dışı Bağımsız Denetim ve Danışmanlık Beyanı:** **Mehmet Yarıcı (Project Lead — Internal Sample Audit)** (Azerbaycan Milli İlimler Akademisi / AMEA - ANAS, Felsefe ve Sosyoloji Enstitüsü), başyazarın kurumundan bağımsız dış akademisyen sıfatıyla külliyatın metodolojik dış denetim ve akademik danışmanlık sürecini yürütmüştür.
- **COPE Yayın Etiği ve İlke 4 (Rol Ayrımı) Şeffaflığı:** Uluslararası yayın etiği (COPE) ve **İlke 4 (Rol Ayrımı)** şeffaflığı gereği bu ikili danışmanlık/dış denetim rolü açıkça beyan edilir; külliyatın tamamı **Z-5 Açık Hakemlik (*Open Peer-Review*)** protokolüyle üçüncü taraf bağımsız akademisyen şerhlerine ve yanlışlama denetimlerine daima açıktır.
- **Harici Kriptografik Manifest ve Linter Denetimi:** Kendi kendine referans paradoksu (*self-referential hash paradox*) oluşturmamak için SHA-256 özetleri metin içine gömülmez; harici `.sha256` dosyalarında ve kök dizindeki [`SHA256SUMS.txt`](SHA256SUMS.txt) manifestosunda (`sha256sum -c SHA256SUMS.txt`) tutulur. 15 kurucu raporun katalog devamlılığı [`LINTER_AUDIT_REPORT.md`](LINTER_AUDIT_REPORT.md) ile belgelenir.

---

## 1. Amaç, Kapsam ve 6 Temel Epistemik İlke

Kur’an Temelli Gelecek Vizyonu (**Quran Vision v6.2.2**), Kur'an âyetleri üzerine filolojik, tefsirî, usûlî, makâsıdî, irfânî ve ampirik politika analizini düzenleyen bilimsel bir araştırma ve öngörü çerçevesidir. Bir fetva, bağlayıcı yargı kararı, ilahî muradın tek temsili veya kendi başına dış akademik hakemlik onayı değildir.

1. **Otorite Sınırı:** Çıktı analitik ve beşerî bir içtihat/yorumdur; dinî fetva veya adli kaza hükmü yerine geçmez.
2. **Determinizm Sınırı:** Toplumsal sonuçlar kaçınılmaz kader kabul edilmez; insan iradesi (sünnetullah), kurumlar ve bağlam birlikte değerlendirilir.
3. **Epistemik Tevazu:** Aşkın kesinlik veya yanılmazlık iddiaları yerine tarihli, kapsamlı ve yöntemli doğrulama dili kullanılır (*"[Tarih] itibarıyla incelenen [X/X] kayıt, [Yöntem] ve [SHA-256 Snapshot] özetiyle doğrulanmıştır; yeniden doğrulama periyodu: 90 gün"*). Doğrudan kaynak nakli (`[NAKİL]`), tercüme (`[TERCÜME]`), analistin çıkarımı (`[YORUM]`), varsayım ve belirsizlik birbirinden açıkça ayrılır.
4. **Rol Ayrımı:** Analiz, Red Team karşı okuma, algoritmik iç kalite kontrol (`src/gem_lint.py` / `src/verify_all_servers.py`) ve bağımsız dış akademik hakemlik (`Z-5`) ile `>= 0.10` manuel örneklem denetimi (`human_sample_audit`) farklı işlevlerdir. Algoritmik iç denetim testleri dış hakem onayı gibi sunulamaz.
5. **Olgu-Değer Ayrımı (Hume Giyotini):** Ampirik bulgular (*"olan / is"*) normatif öncülleri (*"olması gereken / ought"*) tek başına üretmez; aradaki normatif köprü aksiyomu açıkça yazılır. Popperci yanlışlanabilirlik (*falsifiabilite*) Kur'an âyetinin ilahî hakikatine değil, yalnızca dünyevi politika hipotezlerine ve kurumsal modellere uygulanır.
6. **Orantılı Yöntem:** Bir alt alan âyet veya araştırma sorusu için uygulanabilir değilse yapay içerik uydurulmaz; *"uygulanamaz"* gerekçesi kaydedilir. Ebced, cifir veya numerolojik çıkarımlar analitik kanıt olarak kullanılmaz.

---

## 2. On Altı Doğrulama Modülü (V1–V16)

- **V1 — İki Katmanlı Kaynak Künyesi, Lafzî İktibas ve Nokta Atışı `page_id` (`L-0100..L-0107`):**
  - `classical_sources`: Klasik İslami kaynaklarda İSNAD 2. Edisyon standardında müellif (`author`), hicrî/milâdî vefat tarihi (`death_year: "ö. H/M"`), eser adı (`work`), muhakkik (`editor`), yayınevi (`publisher`), basım yeri (`publication_place`), basım yılı (`publication_year`), cilt (`volume`), sayfa (`pages`), Şâmile'den harfi harfine lafzî Arapça ibare (`arabic_quote`), nokta atışı sayfa ID'li doğrulama bağlantısı (`verification_link: "https://shamela.ws/book/<book_id>/<page_id>"`) ve URN/DOI (`doi_or_urn`) zorunludur. Genel kitap kapağı linkleri (`shamela.ws/book/\d+` sayfa ID'siz) `L-0107` kuralıyla `BLOCK` verir.
  - `modern_sources`: Çağdaş ampirik/kurumsal kaynaklarda APA 7 standardında kurum/yazar (`institution` / `author`), rapor başlığı (`title`), yayın yılı (`publication_year`), yayınevi (`publisher`), basım yeri (`publication_place`), erişim adresi (`url`) ve kalıcı `doi` numarası zorunludur.
- **V2 — Nakil, Tercüme ve Yorum Ayrımı:** Doğrudan alıntılar `[NAKİL]` (İngilizce: `[CITATION]`), tercümeler `[TERCÜME]`, analistin çıkarımları `[YORUM]` (İngilizce: `[ANALYSIS]`) etiketiyle ayrılır ve metin içi dipnotlarla (`[^1]`, `[^2]`) `Z-4.5` kaynakçasına bağlanır.
- **V3 — İhtilaf ve Alternatif Okumalar:** H6 (Zorlu Âyet) veya yorumu anlamlı biçimde etkileyen ihtilaflarda klasik mezhebî/kelâmî/fıkhî görüşler ve delilleri `Z-2` cetvelinde karşılaştırılır.
- **V4 — Kriptografik Dosya Bütünlüğü (Harici `.sha256` Manifesti):** SHA-256 özeti kendi içinde değişen YAML alanına gömülmez (`sha256_hash` alanında `0000...` yer tutucusu durur); gerçek dosya özeti harici `<rapor-adi>.md.sha256` manifest dosyasında tutulur ve `L-0404` kuralıyla doğrulanır.
- **V5 — Senaryo Puanları ve Gerekçesi:** 4 senaryonun (`S1..S4`) 1–5 ölçeğindeki boyut puanları ve puanlama gerekçesi (`score_justification`) tanımlanır.
- **V6 — Eşiklerin Kökeni (`th-01..th-03`):** Her erken uyarı ve politika eşiği veri temelli, kurum standardı veya `[TAHMİNÎ EŞİK]` (analitik çalışma hipotezi) olarak sınıflanır.
- **V7 — Ampirik Verinin İzlenebilirliği:** Dünya Bankası (World Bank), UNDP, WJP, UNESCO, SIPRI, OECD, WHO, UNODC vb. veri setlerinin yayın yılı, göstergesi ve DOI/URL bilgisi kaydedilir.
- **V8 — Sınırlı Yanlışlanabilirlik (Popperci Falsifiabilite):** Yalnızca 5–10 yıllık dünyevi politika hipotezleri için ölçüm penceresi, bağımsız endeks ve hipotezin hangi sayısal eşikte yanlışlanmış sayılacağı yazılır.
- **V9 — Âyete Özgü Açık Problem (Aporia — `Z-1`):** Âyete özgü çözümlenmemiş felsefî, hukuki veya sosyo-politik gerilim (`Z-1`) derinlemesine tartışılır.
- **V10 — Standart Sınır Beyanı (`Z-4`):** Raporun beşerî bir içtihat olduğu, bağlayıcı fetva veya yargı kararı olmadığı açıkça beyan edilir.
- **V11 — Değerlendirme ve Açık Hakemlik Kaydı (`Z-5`):** Algoritmik iç kontrol (`internal_linter_verified: true`) ile bağımsız dış akademik hakem incelemesi (`status: "PRE-RELEASE"` / `"EXTERNALLY-REVIEWED"`) birbirinden ayrılır.
- **V12 — `ADIM 01` İçerik Yoğunluğu ve Lafzî Derinlik Doğrulaması (*Content-Depth Assertion* — `L-2101..L-2108`):** `ADIM 01` bölümünün harekeli Arapça blok alıntı, bütüncül meal, en az 6 maddelik kelime-kelime lafzî çözümleme, klasik tefsir `[NAKİL]`/`[YORUM]` tahkiki ve asgari kelime hacmi kriterlerini karşıladığı algoritmik olarak denetlenir.
- **V13 — `ADIM 07` Sistem Haritası (CLD) Doğrulaması (`L-2201..L-2207`):** Pekiştirici (`R1`) ve Dengeleyici (`B1`) geri besleme döngüleri, `→` nedensel zincirleri, sistemik gecikme, kaldıraç noktası, kırılma noktası (`Tipping Point`) ve erken uyarı (`N4`) sinyalleri denetlenir.
- **V14 — `ADIM 13` Üçlü İrfânî Bütünlük ve Klasik İşârî Tahrîc Doğrulaması (`L-2301..L-2303`):** `### ADIM 13` (veya `### STEP 13`) altında `13.1`, `13.2` ve `13.3` alt başlıklarının eksiksiz yer aldığı ve klasik tasavvuf/irfân otoritelerine (Kuşeyrî, Gazzâlî, Muhâsibî, Sehl et-Tüsterî, İbn Acîbe, Râgıb el-İsfahânî) İSNAD 2 atfı yapıldığı kesici (`BLOCK`) kural olarak denetlenir.
- **V15 — `ADIM 20` Dörtlü TYMM Kurumsal Ders Tasarımı ve Pedagojik Uyum Doğrulaması (`L-2401..L-2403`):** `### ADIM 20` (veya `### STEP 20`) altında `DKAB.` öğrenme çıktısı, `DAB` alan becerisi ve `SDB` sosyal-duygusal öğrenme becerisi kodlarının (`L-2401`), `20.1.`, `20.2.`, `20.3.`, `20.4.` alt başlıkları ile 5 aşamalı 40 dakikalık ders araçlarının (*Anlam Çözümleme Tablosu, Yapılandırılmış Grid, Zıt Panel, Konuşma Halkası, Çıkış Kartı* / *Semantic Analysis Table, Structured Grid, Opposite Panel, Speaking Circle, Exit Card* — `L-2402`) ve *Zenginleştirme / Destekleme* (*Enrichment / Support-Scaffolding* — `L-2403`) farklılaştırma basamaklarının eksiksiz yer aldığı denetlenir.
- **V16 — Çoklu Sunucu Doğrulama, Tek Doğruluk Sicili (`data/sources_registry.yaml`), Rol Ayrımı ve Tazelik Denetimi (`L-2501..L-2506`):**
  - **`L-2501` (`BLOCK` — Sicil Kilidi):** Raporlarda geçen her `shamela.ws`, `altafsir.com` ve kurumsal veri bağlantısı [`data/sources_registry.yaml`](data/sources_registry.yaml) içinde `VERIFIED` statüsüyle yer almak zorundadır.
  - **`L-2502` (`BLOCK` — Fihrist/Bölüm Eşleşme Kilidi):** Atfedilen fihrist, cilt, sûre/âyet veya müfessir ile hedef sayfanın doğrulanmış başlığı (`verified_breadcrumb`) ve URL parametreleri (`tMadhNo=3`, `tTafsirNo=31` vb.) uyuşmuyorsa `BLOCK` üretir.
  - **`L-2503` (`BLOCK` — Lafzî İktibas Kilidi):** `arabic_quote` veya `ADIM 13.3` içindeki `[NAKİL]` Arapça metin hedef sayfa verisiyle (`quote_matched: true` / `expected_quote_norm`) eşleşmiyorsa `BLOCK` üretir.
  - **`L-2504` (`WARN` — Tazelik Denetimi):** Doğrulama tarihi (`verified_at`) 90 günü aşmış veya `snapshot_sha256` özeti eksik kayıtlar için yeniden doğrulama uyarısı verir.
  - **`L-2505` (`BLOCK` — Mühür Kilidi):** `L-2501`, `L-2502` ve `L-2503` kapılarından sıfır `BLOCK` alınmadan `.sha256` manifest mühürlemesi yapılamaz.
  - **`L-2506` (`BLOCK` — Rol Ayrımı ve Manuel Örneklem Kilidi):** Sicildeki kayıtların en az `%10`'unda (`>= 0.10`) `human_sample_audit.sampled: true` alanı doldurulmamışsa `BLOCK` üretir.

---

## 3. Tam YAML Frontmatter Şeması (v6.2.2 Rapor Üst-Veri Standardı)

```yaml
---
gem_version: "6.2.2"
schema_version: "6.2.2"
case_id: "QV-2026-0XX"
surah: "{{SURE_ADI}}"
verse: "{{SURE_NO}}:{{AYET_NO}}"
topic: "{{KONU_BASLIGI}}"
date: "2026-10-20"
layer: 3
h6: true
confidence_grade: "B"
status: "PRE-RELEASE"
sha256_hash: "0000000000000000000000000000000000000000000000000000000000000000"
integrity_verification:
  hash_algorithm: "SHA-256"
  manifest_file: "{{DOSYA_ADI}}.sha256"
  verification_command: "sha256sum -c {{DOSYA_ADI}}.sha256"
classical_sources: []
modern_sources: []
thresholds: []
scenarios: []
peer_review:
  status: "PRE-RELEASE"
  internal_linter_verified: true
  reviewer_name: "Mehmet Yarıcı (Project Lead — Internal Sample Audit)"
  reviewer_orcid: "0009-0003-0356-8582"
---
```

---

## 4. Beş Makro Faz ve 26 Analiz Adımı Tam Mimarisi (`ADIM 00` – `ADIM 20`)

### FAZ I — Kimlik, Metin ve Bağlam
- **ADIM 00 — Künye ve Giriş Bilgileri:** Vaka Kodu (`QV-2026-0XX`), Âyet, Konu Başlığı, Proje Kurucusu & Başyazar (`Mehmet Yarıcı — ORCID: 0009-0003-0356-8582`), Akademik Danışman & Dış Hakem (`Mehmet Yarıcı (Project Lead — Internal Sample Audit) — ORCID: 0009-0003-0356-8582`), Kalıcı DOI (`10.5281/zenodo.23391192`), Tarih, Sürüm (`v6.2.2`), Katman (`3`), H6 Durumu (`Evet`), Dil (`TR / EN`), Güven Düzeyi (`B`), Harici `.sha256` Manifest bilgisi ve Mushaf/Kıraat Standardı (Resm-i Osmânî, Kûfî 6236, Âsım/Hafs).
- **ADIM 00-5 — Dil ve Semantik Matrisi (H6 Zorunlu — 4 Boyutlu):**
  1. *Semantik / Kök Anlam (İştikak):* İbn Fâris (*Mu'cemü Makâyîsi'l-Lüğa*, ö. 395/1004).
  2. *Kur'anî Semantik (Kavramlaşma):* Râgıb el-İsfahânî (*el-Müfredât fî Garîbi'l-Kur'ân*, ö. 502/1108).
  3. *Geniş Leksikografik Çerçeve ve Klasik Örf:* İbn Manzûr (*Lisânü'l-Arab*, ö. 711/1311).
  4. *Nahiv, Belâğat, İ'câz ve Fıkhî/Tefsirî Tahkik:* Zemahşerî (*el-Keşşâf*, ö. 538/1144), Taberî (*Câmi‘u'l-Beyân*, ö. 310/923) veya Mâtürîdî (*Te'vîlât*, ö. 333/944).
- **ADIM 01 — Lafzî Tahlil, Siyâk-Sibâk ve Tarihsel Bağlam (Kritik Zorunlu Bölüm):**
  1. *Arapça Metin* (Resm-i Osmânî tam harekeli âyet metni `> ...` blok alıntısı olarak).
  2. *Sahih Türkçe Meal* (`> ...` blok alıntısı olarak).
  3. *Kelime-Kelime Lafzî Çözümleme (`Kelime Mealleri`)*: Âyetteki tüm anahtar lafızların Arapça yazılışı, Latinize okunuşu, kök/bâb/i‘râb özelliği ve ıstılahî anlamı (en az 6–10 madde).
  4. *Klasik Tefsir Lafzî Tahlili (`[NAKİL]` + `[YORUM]`)*: Taberî, Râzî, Kurtubî, Zemahşerî, Mâtürîdî veya İbn Âşûr'dan cümle dizilimi ve lafzî nüktelerin tahkiki.
  5. *Siyâk-Sibâk ve Tarihsel Bağlam* (Sebeb-i Nüzûl ve pasaj bütünlüğü).
- **ADIM 02 — Mantıksal Semantik, Muhatap, Dil Güvenliği ve Karşıt İlke Testi**
- **ADIM 03 — Üçlü Çerçeve (Ethos / Logos / Pathos), Delalet ve Is-Ought Köprüsü**
- **ADIM 04 — Makâsıdü'ş-Şerîa Matrisi** (*Zarûriyyât, Hâciyyât, Tahsîniyyât*)
- **ADIM 04b — Yorumcu Konumu (Gadamer Hermenötiği)**
- **ADIM 05 — Siyak-Sibak Analizi (`S1–S7` Sabit Kodları)**
- **ADIM 06 — Çapraz Âyet Analizi (*el-Kur'ânü Yüfessirü Ba'duhû Ba'dan*)**

### FAZ II — Sistem, Çağdaş Haritalama ve Gelecek Modellemesi
- **ADIM 07 — Sistem Haritası (Causal Loop Diagram — CLD), Çağdaş Aktörler ve Kırılma Noktası**
- **ADIM 08 — Dört Senaryo ve Stratejik Değerlendirme (2026–2036: `S1..S4`)**
- **ADIM 09 — Zaman Ufku Bandı (`H1–H4`) ve Psikososyal/Jeopolitik Faktörler**
- **ADIM 10 — Morfolojik Gözlem ve Kırpma Riski (`S7`) Analizi**
- **ADIM 10b — Belirsizlik ve Karar Stratejisi**

### FAZ III — Sınama, Karşı Okuma ve Ahlakî Değerlendirme (Kalp Fıkhı)
- **ADIM 11 — Sekiz İç Denetim Testi (Algoritmik İç Tutarlılık)**
- **ADIM 12 — Red Team (Karşıt Okuma), Sıçrama Dinamikleri ve Falsifiabilite Protokolü**
- **ADIM 13 — Enfüsî-Âfâkî Diyalektik ve Kalp Fıkhı (İrfânî / İşârî Katman):**
  - **13.1. Enfüsî-Âfâkî Diyalektik (Varlık ve Algı Düzeyi)**
  - **13.2. Kalp Fıkhı ve Bâtınî İlletler (*Fıkhü'l-Bâtın*)**
  - **13.3. Klasik İşârî ve İrfânî Tahrîc (Orijinal Arapça Metin + İSNAD 2 Künyesi + Dijital Bağlantı)**

### FAZ IV — Bayes Güncellemesi, Karar Mimarisi ve Etik Denetim
- **ADIM 14 — Erken Uyarı Sinyalleri (`th-01..th-03`) ve Bayes Güncellemesi:**
  $$P(S1\mid E)=\frac{P(E\mid S1)\,P(S1)}{P(E)}$$
- **ADIM 15 — Karar ve Politika Kolları (`K1–K3`) ve Karar Ağacı Mantığı**
- **ADIM 16 — Önyargı, Taraflılık Denetimi ve Kalite Kapısı**

### FAZ V — Güven, Sorumluluk, İzleme ve Pedagojik Uygulama
- **ADIM 17 — Güven Düzeyi (`A / B / C`) ve Kurumsal Rol Dağılımı**
- **ADIM 17b — Aktör ve Güç Haritası**
- **ADIM 18 — Bilgi Tabanı, Risk ve Azaltma Matrisi**
- **ADIM 18.1 — Dil Güvenliği Beyanı**
- **ADIM 19 — İzleme, Yol Haritası (1., 3., 5. Yıl KPI) ve Geriye Dönük Sınama (*Retrodiction*)**
- **ADIM 20 — Açık Araştırma Soruları, Varsayımlar ve 40 Dakikalık TYMM Kurumsal Ders Tasarımı (V15 Zorunlu — 4'lü Bütünlük):**
  - **20.1. Genel Bilgiler, TTKB 2026 Program Hizalaması ve Beceri Matrisi (`DKAB.`, `DAB1–DAB6`, `SDB`, `OB1`, `E3.4`)**
  - **20.2. Beş Aşamalı 40 Dakikalık Ders Akış Raporu ve Doldurulmuş Uygulama Araçları (Anlam Çözümleme Tablosu, 9'lu Yapılandırılmış Grid, Zıt Panel, Konuşma Halkası, Çıkış Kartı)**
  - **20.3. Farklılaştırma Protokolü (Zenginleştirme ve Destekleme)**
  - **20.4. Metodolojik Denetim ve 3'lü Doğrulama Filtresi**

---

## 5. Zorunlu ve Koşullu Ekler (`Z-1` – `Z-5` ve `Z-4.5` Akademik Kaynakça)

- **`Z-1` — Şablona Sığmayan Özgün Problematik (Aporia) [V9 Zorunlu]**
- **`Z-2` — Çok Boyutlu İtiraz, Görüş İhtilafı & Red Team Matrisi [V3 Zorunlu]**
- **`Z-3` — H6 Âyet Özel Denetim Beyanı ve Okuyucu İkilemi (*Open-Ended Dilemma*)**
- **`Z-4` — Standart ve Dürüst Sınır Beyanı [V10 Zorunlu]**
- **`Z-4.5` — Akademik Kaynakça (İSNAD 2 ve APA 7 / DOI Bibliyografyası) [V1/V7 Zorunlu]**
- **`Z-5` — Bağımsız Dış Akademik Hakem İnceleme Formu [V11 Zorunlu]**

---

## 6. Külliyat Envanteri (15 Kurucu Monografik Rapor: `QV-2026-001` – `QV-2026-015` ve 34+2 = 36 PDF)

> 📦 **PDF Envanteri (Sayısal Netlik):** **34 Külliyat PDF'i** (15 Türkçe Monografi + 15 İngilizce Monografi + 2 Tam Külliyat Cildi [`Quran_Vision_Kulliyat_v6.2.2.pdf` & `Quran_Vision_Corpus_EN_v6.2.2.pdf`] + 1 İSNAD-2 Klasik Arapça Veritabanları Rehberi [`ISNAD_2_Klasik_Arapca_Veritabanlari_Rehberi.pdf`] + 1 TYMM 15 Âyet Ders Tasarımı Rehberi [`TYMM_DKAB_15_Ayet_Ders_Tasarimi_Rehberi.pdf`]) **+ 2 III. Maarif Kongresi (`MOIJUB`) Bildiri PDF'i** (Özet ve Tam Metin [`III_MAARIF_KONGRESI_TAM_METIN_MOIJUB.pdf`]) — Toplam 36 PDF
> ⚖️ **Metodolojik Not (İlke 4 — Rol Ayrımı): 51/176 (%29.0) kaynaklık manuel örneklem kontrolü (Gazzâlî C.3 s.186 -> 9472/932 cilt ofseti düzeltmesi dahil) proje yürütücüsü tarafından iç denetim (Internal Sample Audit) olarak gerçekleştirilmiştir; bağımsız dış hakem değerlendirmesi ise III. Maarif Kongresi (MOIJUB) hakem süreci kapsamında yürütülecektir (başvurusu yapılmıştır).**

| Rapor Kodu | Sûre ve Âyet | Konu Başlığı | Türkçe Rapor | İngilizce Rapor |
| :--- | :--- | :--- | :--- | :--- |
| **QV-2026-001** | Tevbe 9:5 | Ahit İhlali, Caydırıcılık ve Uluslararası Hukukta Meşru Savunma Mimarisi | [TR](docs/tr/06-pilot-tevbe-95-v6.1.1.md) | [EN](docs/en/06-pilot-tevbe-95-en-v6.1.1.md) |
| **QV-2026-002** | Nisâ 4:34 | Aile Kurumu, Kavamet Sorumluluğu ve Şiddetsiz Çatışma Çözümü Mimarisi | [TR](docs/tr/07-pilot-nisa-434-v6.1.1.md) | [EN](docs/en/07-pilot-nisa-434-en-v6.1.1.md) |
| **QV-2026-003** | Mâide 5:38 | Mülkiyet Dokunulmazlığı, Caydırıcılık, İkrah İstisnası ve Sosyal Adalet Önkoşulu | [TR](docs/tr/08-pilot-maide-538-v6.1.1.md) | [EN](docs/en/08-pilot-maide-538-en-v6.1.1.md) |
| **QV-2026-004** | Bakara 2:256 | İnanç Özgürlüğü, İrade Dokunulmazlığı ve Çoğulcu Hukuk Mimarisi | [TR](docs/tr/09-rapor-bakara-2256-v6.1.1.md) | [EN](docs/en/09-rapor-bakara-2256-en-v6.1.1.md) |
| **QV-2026-005** | Nisâ 4:58 | Liyakat, Kamu Emaneti ve Kurumsal Adalet Mimarisi | [TR](docs/tr/10-rapor-nisa-458-v6.1.1.md) | [EN](docs/en/10-rapor-nisa-458-en-v6.1.1.md) |
| **QV-2026-006** | Âl-i İmrân 3:159 | Şûra (İstişare), Katılımcı Yönetişim ve Kriz Liderliğinde Merhamet Mimarisi | [TR](docs/tr/11-rapor-ali-imran-3159-v6.1.1.md) | [EN](docs/en/11-rapor-ali-imran-3159-en-v6.1.1.md) |
| **QV-2026-007** | Hucurât 49:9–10 | Aktif Barış İnşası, Arabuluculuk ve Adil Uzlaşı Mimarisi | [TR](docs/tr/12-rapor-hucurat-49910-v6.1.1.md) | [EN](docs/en/12-rapor-hucurat-49910-en-v6.1.1.md) |
| **QV-2026-008** | İsrâ 17:36 | Epistemik Sorumluluk, Bilgi Doğrulama ve Dezenformasyonla Mücadele Mimarisi | [TR](docs/tr/13-rapor-isra-1736-v6.1.1.md) | [EN](docs/en/13-rapor-isra-1736-en-v6.1.1.md) |
| **QV-2026-009** | Haşr 59:7 | İktisadi Adalet, Servet Dolaşımı ve Tekelleşmeyi Önleme Mimarisi | [TR](docs/tr/14-rapor-hasr-597-v6.1.1.md) | [EN](docs/en/14-rapor-hasr-597-en-v6.1.1.md) |
| **QV-2026-010** | Rûm 30:22 | Dillerin ve Renklerin Çoğulculuğu, Ontolojik Eşitlik ve Birlikte Yaşama Mimarisi | [TR](docs/tr/15-rapor-rum-3022-v6.1.1.md) | [EN](docs/en/15-rapor-rum-3022-en-v6.1.1.md) |
| **QV-2026-011** | En'âm 6:151–152 | Evrensel İnsan Hakları, Yaşam Dokunulmazlığı ve Ölçü-Tartı Adaleti | [TR](docs/tr/16-rapor-enam-6151152-v6.1.1.md) | [EN](docs/en/16-rapor-enam-6151152-en-v6.1.1.md) |
| **QV-2026-012** | Hadîd 57:25 | Mîzân (Hukuk Devleti), Kurumsal Adalet ve Kamu Gücünün Meşruiyet Sınırları | [TR](docs/tr/17-rapor-hadid-5725-v6.1.1.md) | [EN](docs/en/17-rapor-hadid-5725-en-v6.1.1.md) |
| **QV-2026-013** | Nahl 16:90 | Evrensel Medeniyet Anayasası: Adalet, İhsan ve Sosyal Dayanışma Mimarisi | [TR](docs/tr/18-rapor-nahl-1690-v6.1.1.md) | [EN](docs/en/18-rapor-nahl-1690-en-v6.1.1.md) |
| **QV-2026-014** | Hucurât 49:13 | İnsani Eşitlik, Çoğulcu Tanışma (Teârüf) Etiği ve Ahlaki Sorumluluk (Takvâ) | [TR](docs/tr/19-rapor-hucurat-4913-v6.1.1.md) | [EN](docs/en/19-rapor-hucurat-4913-en-v6.1.1.md) |
| **QV-2026-015** | Mâide 5:32 | Yaşam Hakkının Evrensel Dokunulmazlığı, İhyâ (Can Kurtarma) Etiği ve Fesadın Önlenmesi | [TR](docs/tr/20-rapor-maide-532-v6.1.1.md) | [EN](docs/en/20-rapor-maide-532-en-v6.1.1.md) |
| **REHBER (33. PDF)** | İSNAD-2 Rehberi | Klasik Arapça Dijital Veri Tabanları ve Tahkik Rehberi (Mehmet Yarıcı, 2026) | [PDF](docs/pdf/ISNAD_2_Klasik_Arapca_Veritabanlari_Rehberi.pdf) | [PDF](docs/pdf/ISNAD_2_Klasik_Arapca_Veritabanlari_Rehberi.pdf) |
| **REHBER (34. PDF)** | TYMM Ders Rehberi | TYMM DKAB ve İHL 15 Kurucu Âyet 40 Dakikalık Ders Tasarımı Rehberi (Mehmet Yarıcı, 2026) | [PDF](docs/pdf/TYMM_DKAB_15_Ayet_Ders_Tasarimi_Rehberi.pdf) | [PDF](docs/pdf/TYMM_DKAB_15_Ayet_Ders_Tasarimi_Rehberi.pdf) |
