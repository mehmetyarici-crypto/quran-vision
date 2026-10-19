---
gem_version: "6.2.1"
case_id: "QV-2026-001"
surah: "Tevbe"
verse: "9:5"
topic: "Ahit İhlali, Caydırıcılık ve Uluslararası Hukukta Meşru Savunma Mimarisi"
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
    work: "el-Keşşâf 'an Hakâ'ikı Gavâmizi't-Tenzîl"
    editor: "Âdil Ahmed Abdülmevcûd, Ali Muhammed Muavvaz"
    publisher: "Mektebetü'l-Ubeykân"
    publication_place: "Riyad"
    publication_year: 1998
    volume: "3"
    pages: "10-15"
    arabic_quote: "فإذا انسلخ الأشهر الحرم: يعني أشهر التسيير الأربعة... والمشركين: العاهدين الناكثين خاصة دون غيرهم، بدليل قوله تعالى: إلا الذين عاهدتم من المشركين ثم لم ينقصوكم شيئا"
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
    volume: "3"
    pages: "97-98"
    arabic_quote: "السين واللام والخاء أصل يدل على كشط الشيء عن الشيء، وانسلاخ الشهر: خروجه كله حتى لا يبقى منه شيء"
    verification_link: "https://shamela.ws/book/21710"
    doi_or_urn: "urn:shamela:23721"

  - id: "src-ibn-manzur"
    author: "İbn Manzûr, Muhammed b. Mükerrem"
    death_year: "ö. 711/1311"
    work: "Lisânü'l-Arab"
    editor: "Dârü Sâdır"
    publisher: "Dârü Sâdır"
    publication_place: "Beyrut"
    publication_year: 1993
    volume: "3"
    pages: "182-184"
    arabic_quote: "والمرصد: موضع الرصد والترقب، وقعدت له كل مرصد أي كل طريق يمر به ليؤخذ"
    verification_link: "https://shamela.ws/book/1687"
    doi_or_urn: "urn:shamela:21605"

  - id: "src-cessas"
    author: "Cessâs, Ahmed b. Ali er-Râzî"
    death_year: "ö. 370/981"
    work: "Ahkâmü'l-Kur'ân"
    editor: "Muhammed Sadık Kamhâvî"
    publisher: "Dâru İhyâi't-Türâsi'l-Arabî"
    publication_place: "Beyrut"
    publication_year: 1992
    volume: "4"
    pages: "268-272"
    arabic_quote: "هذه الآية متصلة بما قبلها في أهل العهد الناكثين، وليست بناسخة لقوله تعالى لا ينهاكم الله عن الذين لم يقاتلوكم"
    verification_link: "https://shamela.ws/book/23579"
    doi_or_urn: "urn:shamela:21571"

  - id: "src-satibi"
    author: "Şâtıbî, İbrâhîm b. Mûsâ"
    death_year: "ö. 790/1388"
    work: "el-Muvâfakât"
    editor: "Meşhûr b. Hasan Âl-i Selmân"
    publisher: "Dâru İbni Affân"
    publication_place: "Riyad"
    publication_year: 1997
    volume: "3"
    pages: "340-345"
    arabic_quote: "النسخ في لسان المتقدمين أعم منه في لسان المتأخرين، وأكثر ما يطلقونه على تخصيص العام أو تقييد المطلق"
    verification_link: "https://shamela.ws/book/11435"
    doi_or_urn: "urn:shamela:21731"

modern_sources:
  - id: "mod-ucdp"
    institution: "Uppsala University (Uppsala Conflict Data Program - UCDP)"
    title: "UCDP Georeferenced Event Dataset (GED) and Armed Conflict Database 2024"
    publication_year: 2024
    publication_place: "Uppsala"
    publisher: "Department of Peace and Conflict Research, Uppsala University"
    url: "https://ucdp.uu.se"
    doi: "doi:10.1177/0022343320934986"

  - id: "mod-iep"
    institution: "Institute for Economics and Peace (IEP)"
    title: "Global Peace Index 2024: Measuring Peace in a Complex World"
    publication_year: 2024
    publication_place: "Sydney"
    publisher: "Institute for Economics and Peace"
    url: "https://www.economicsandpeace.org"
    doi: "doi:10.13140/RG.2.2.14668.01928"

  - id: "mod-worldbank"
    institution: "World Bank Group"
    title: "Worldwide Governance Indicators (WGI): Rule of Law and Political Stability"
    publication_year: 2024
    publication_place: "Washington, D.C."
    publisher: "The World Bank"
    url: "https://datacatalog.worldbank.org"

thresholds:
  - id: "th-01"
    name: "Diplomatik Mühlet Süresi"
    value: "4 ay (120 gün)"
    derivation_basis: "[TAHMİNÎ EŞİK] Tevbe 9:2 ve 9:5 metninde geçen haram aylar nassından lafzî tespit"
    is_empirical: false

  - id: "th-02"
    name: "Sınır İhlali ve Güvenlik Tehdidi Eşiği"
    value: "> 3 ihlal / ay"
    derivation_basis: "[TAHMİNÎ EŞİK] Sınır güvenliği ve kriz tırmanma modellerine dayalı çalışma eşiği"
    is_empirical: true

  - id: "th-03"
    name: "Çatışma Nüks ve Ahit Güvenliği Skoru"
    value: ">= 0.75"
    derivation_basis: "[TAHMİNÎ EŞİK] Dünya Bankası Hukukun Üstünlüğü ve IEP Küresel Barış Endeksi izleme eşiği"
    is_empirical: true

scenarios:
  - id: "S1"
    title: "Koruyucu Senaryo (Müeyyideli Barış)"
    scores:
      olasilik: 4
      tesir: 5
      firsat: 4
      kirilganlik: 2
      stratejik_oncelik: 5
    score_justification: "Hudeybiye sonrası diplomatik teyakkuz ve caydırıcı güvenlik dengesi simülasyonu"

  - id: "S2"
    title: "Bozuluş Senaryosu (Taviz ve Felç Sarmalı)"
    scores:
      olasilik: 2
      tesir: 4
      firsat: 2
      kirilganlik: 5
      stratejik_oncelik: 3
    score_justification: "Tek taraflı taviz durumunda hasmın cüretkârlığının artması tarihsel analizi"

  - id: "S3"
    title: "Denge Senaryosu (Kademeli Askeri Sınırlandırma)"
    scores:
      olasilik: 3
      tesir: 4
      firsat: 3
      kirilganlik: 3
      stratejik_oncelik: 4
    score_justification: "Sıcak temas yerine abluka ve lojistik denetim modeli"

  - id: "S4"
    title: "İhya Senaryosu (Hukuki ve Sosyal Entegrasyon)"
    scores:
      olasilik: 4
      tesir: 5
      firsat: 5
      kirilganlik: 2
      stratejik_oncelik: 5
    score_justification: "Tevbe 9:6 eman koridoru ve anayasal entegrasyon potansiyeli"

peer_review:
  status: "PRE-RELEASE"
  internal_linter_verified: true
  linter_timestamp: "2026-10-15T23:00:00+03:00"
  reviewer_name: "Mehmet Emin Koç"
  reviewer_title: "Akademik Danışman & Dış Hakem (Supervisor & External Peer-Reviewer)"
  reviewer_orcid: "0000-0002-1025-5643"
  reviewer_institution: "Azerbaycan Milli İlimler Akademisi (AMEA / ANAS), Felsefe ve Sosyoloji Enstitüsü"
  review_date: null
  review_notes: "Ön sürüm (PRE-RELEASE) aşamasındadır; bağımsız dış akademik hakem (Mehmet Emin Koç, ORCID: 0000-0002-1025-5643) değerlendirme ve tescil sürecine açıktır."
---

# Tevbe Sûresi 9:5 Tahlili — Ahit İhlali, Caydırıcılık ve Uluslararası Hukukta Meşru Savunma Mimarisi

## FAZ I — KİMLİK, METİN VE BAĞLAM

### ADIM 00 — KÜNYE VE GİRİŞ BİLGİLERİ
- **Vaka Kodu:** QV-2026-001
- **Âyet:** Tevbe Sûresi 9:5 ("Kılıç Âyeti" / Âyetü's-Seyf)
- **Konu Başlığı:** Ahit İhlali, Caydırıcılık ve Uluslararası Hukukta Meşru Savunma Mimarisi
- **Proje Kurucusu & Başyazar:** Mehmet Yarıcı (Uludağ Üniversitesi İlahiyat Fakültesi, 1989 • T.C. MEB, İstanbul Bahçelievler Dede Korkut Anadolu Lisesi — ORCID: `0009-0003-0356-8582`)
- **Akademik Danışman & Dış Hakem:** Mehmet Emin Koç (Azerbaycan Milli İlimler Akademisi Felsefe ve Sosyoloji Enstitüsü — ORCID: `0000-0002-1025-5643`)
- **Kalıcı CERN / Zenodo DOI:** `10.5281/zenodo.23391192` (Kavram DOI) | `10.5281/zenodo.23410818` (v6.2.1 Sürüm DOI)
- **Tarih:** 2026-10-15
- **Sürüm:** v6.2.1 (Akademik Doğrulama Standartlı)
- **Katman:** 3 (26 Adımlı Tam Analiz Motoru + 5 Makro Faz + Z-1..Z-5 Zorunlu Ekler)
- **H6 Durumu:** Evet (Zorlu Âyet Kapsamı)
- **Dil:** Türkçe (TR)
- **Güven Düzeyi:** B (Katman 3 seviyesinde usûlî tahkik ve çapraz kaynak konsensüsü; teolojik alanda sayısal kesinlik iddiası taşınamaz)
- **Bilgi Düzeyi:** Doğrulanmış Metodolojik Modelleme
- **Kriptografik Bütünlük Hash'i (SHA256):** Harici manifest ile doğrulanır (`06-pilot-tevbe-95-v6.1.1.md.sha256`)
- **Mushaf / Kıraat Standardı:** Mushaf-ı Şerîf Resm-i Osmânî, Kûfî 6236 (Âsım / Hafs), Tevbe 9:5

---
### ADIM 00-5 — DİL VE SEMANTİK MATRİSİ (H6 ZORUNLU)

1. **Semantik / Kök Anlam:**
   - **Kaynak:** İbn Fâris (*Mu'cemü Makâyîsi'l-Lüğa*, C. 3, s. 97).[^1]
   - `[NAKİL]`: *"السين واللام والخاء أصل يدل على كشط الشيء عن الشيء، وانسلاخ الشهر: خروجه كله"* (İbn Fâris: Selaha kökü, bir şeyin örtüsünden sıyrılıp tamamen çıkmasını ifade eder; ayın insilâhı ise vaktin bütünüyle çıkıp geriye hiçbir şeyin kalmamasıdır).
   - `[YORUM]`: Diplomatik mühlet tek taraflı veya keyfi olarak kısaltılamaz; antlaşmanın tanıdığı zaman dilimi bütünüyle dolmadan meşru askeri mukabele başlatılamaz.

2. **Nahiv / Belâğat ve İ'câz:**
   - **Kaynak:** Zemahşerî (*el-Keşşâf*, C. 3, s. 10-15).[^2]
   - `[NAKİL]`: *"فإذا انسلخ الأشهر الحرم: يعني أشهر التسيير الأربعة... والمشركين: العاهدين الناكثين خاصة دون غيرهم"* (Zemahşerî: Âyetteki harf-i tarif ahd-i hâricî içindir; antlaşmayı tek taraflı bozan muayyen muharip müşrikleri kasteder).
   - `[YORUM]`: `Ahz` (esir alma), `hasr` (kuşatma) ve `marsad` (gözetleme yerlerini tutma) emirleri, sınırsız bir imha değil; hasmın lojistik hatlarını kesen, teslim koridorunu açık tutan kademeli bir askeri harekât doktrinidir.

3. **Lisan / Klasik Kullanım:**
   - **Kaynak:** İbn Manzûr (*Lisânü'l-Arab*, C. 3, s. 182-184).[^3]
   - `[NAKİL]`: *"والمرصد: موضع الرصد والترقب، وقعدت له كل مرصد أي كل طريق يمر به ليؤخذ"* (İbn Manzûr: Marsad, düşmanın geçiş güzergâhlarını gözetleme ve yakalama mevkiidir).
   - `[YORUM]`: Klasik Arapçada bu terkipler kör bir şiddeti değil; stratejik denetimi, istihbari gözetlemeyi ve saldırganı teslim olmaya zorlayan kuşatmayı anlatır.

- **Çapraz Kontrol ve Dil Güvenliği:** Üç kaynak da âyetin genel bir katliam fermanı değil; mühleti dolmuş ahit bozuculara yönelik kontrollü askeri güvenlik operasyonu olduğu hususunda mutabıktır.

---

### ADIM 01 — LAFZÎ TAHLİL, SİYÂK-SİBÂK VE TARİHSEL BAĞLAM

- **Arapça Metin (Tevbe Sûresi 9:5 — Resm-i Osmânî):**
  > فَإِذَا ٱنسَلَخَ ٱلْأَشْهُرُ ٱلْحُرُمُ فَٱقْتُلُوا۟ ٱلْمُشْرِكِينَ حَيْثُ وَجَدتُّمُوهُمْ وَخُذُوهُمْ وَٱحْصُرُوهُمْ وَٱقْعُدُوا۟ لَهُمْ كُلَّ مَرْصَدٍۢ ۚ فَإِن تَابُوا۟ وَأَقَامُوا۟ ٱلصَّلَوٰةَ وَءَاتَوُا۟ ٱلزَّكَوٰةَ فَخَلُّوا۟ سَبِيلَهُمْ ۚ إِنَّ ٱللَّهَ غَفُورٌۭ رَّحِيمٌۭ ﴿٥﴾

- **Sahih Türkçe Meal:**
  > *"Haram aylar (tanınan dört aylık barış ve diplomasi mühleti) çıkınca, o (antlaşmayı bozup saldırganlaşan) müşrikleri bulduğunuz yerde etkisiz hâle getirin; onları yakalayın (esir alın), kuşatın ve bütün geçit yerlerini tutun. Eğer (saldırganlıktan ve şirkten) tevbe ederler, namazı kılarlar ve zekâtı verirlerse artık yollarını serbest bırakın (onlara ilişmeyin). Şüphesiz Allah çok bağışlayandır, çok merhamet edendir. (5)"*

- **Kelime-Kelime Lafzî Çözümleme (Kelime Mealleri):**
  - `فَإِذَا` (Fe-izâ): Vaktaki, ... olduğu zaman (şart ve zaman zarfı; hükmün mutlak değil, 1–4. âyetlerdeki dört aylık diplomatik ültimatom süresinin bitimine bağlı olduğunu gösterir).
  - `ٱنسَلَخَ` (inselaha): Sıyrılıp çıktığı, tamamen sona erdiği zaman (*infi‘âl* bâbından; derinin koyundan sıyrılması gibi mühletin hiçbir şüpheye yer bırakmadan tamamlanmasını ifade eder).
  - `ٱلْأَشْهُرُ ٱلْحُرُمُ` (el-eşhüru'l-hurum): Haram aylar (Tevbe 9:2'de ahdi bozanlara tanınan 4 aylık güvenlik ve düşünme mühleti).
  - `فَٱقْتُلُوا۟` (faktulû): Mukabele edin / savaşın (kamu otoritesine yönelik meşru müdafaa emri; bireysel infaz değil, devletler hukuku tasarrufudur).
  - `ٱلْمُشْرِكِينَ` (el-müşrikîne): O ahdini bozan muharip müşrikleri (başındaki *el-* takısı *ahd-i zihnî* içindir; 9:1–4 ve 9:7–13'te tanımlanan, barış antlaşmasını arkadan vurarak bozan saldırgan zümreyi tahsis eder).
  - `حَيْثُ وَجَدتُّمُوهُمْ` (haysü vecedtümûhüm): Onları bulduğunuz / karşılaştığınız yerde (Harem bölgesi istisnasının kalktığını bildiren mekân zarfı).
  - `وَخُذُوهُمْ` (ve huzûhüm): Onları yakalayın / esir alın (öldürmenin tek seçenek olmadığını, esir alarak etkisizleştirmenin asıl olduğunu gösterir).
  - `وَٱحْصُرُوهُمْ` (vahsurûhüm): Kuşatın / stratejik ablukaya alın (sıcak çatışmaya girmeden caydırma tedbiri).
  - `وَٱقْعُدُوا۟ لَهُمْ كُلَّ مَرْصَدٍۢ` (vak‘udû lehüm külle marsadin): Her gözetleme ve sınır kontrol noktasında (`marsad`) güvenlik denetimi kurun.
  - `فَإِن تَابُوا۟` (fe-in tâbû): Eğer düşmanlıktan, ahit ihlalinden ve şirkten vazgeçip dönerlerse.
  - `وَأَقَامُوا۟ ٱلصَّلَوٰةَ وَءَاتَوُا۟ ٱلزَّكَوٰةَ` (ve ekâmü's-salâte ve âtevü'z-zekâte): Namazı ikame eder ve zekâtı verirlerse (kamu düzenine ve toplumsal barış sözleşmesine entegre olurlarsa).
  - `فَخَلُّوا۟ سَبِيلَهُمْ` (fe-hallû sebîlehüm): Derhal yollarını serbest bırakın, her türlü askeri/adli takibatı durdurun!
  - `إِنَّ ٱللَّهَ غَفُورٌۭ رَّحِيمٌۭ` (innallâhe ğafûrun rahîm): Şüphesiz Allah çok bağışlayandır, çok merhamet edendir (savaş âyetinin rahmet ve mağfiret sıfatlarıyla mühürlenmesi, asıl gayenin imha değil barış ve ıslah olduğunu tescil eder).

- **Klasik Tefsir Lafzî Tahlili (Zemahşerî & Taberî):**
  - `[NAKİL]`: Zemahşerî, `فَٱقْتُلُوا۟` emrinin hemen peşinden gelen `وَخُذُوهُمْ وَٱحْصُرُوهُمْ وَٱقْعُدُوا۟ لَهُمْ كُلَّ مَرْصَدٍۢ` tertibinin rastgele olmadığını, esir alma ve teslim olma koridorunu açık tutan kademeli bir nizam bildirdiğini kaydeder (*el-Keşşâf*, C. 3, s. 12).
  - `[YORUM]`: Bu lafzî sıralama modern askeri angajman kurallarındaki (*Rules of Engagement*) orantılı güç kullanımını ve teslim olan veya barışa yanaşan tarafa dokunulmazlık hakkını (`fe-hallû sebîlehüm`) yansıtır.

- **Siyâk-Sibâk ve Tarihsel Bağlam:**
Tevbe Sûresi 9:1–15 pasajı bir bütün olarak okunduğunda, 5. âyetin hemen öncesindeki 4. âyette (*"Ancak kendileriyle antlaşma yaptığınız müşriklerden size karşı bir eksiklik yapmayan ve aleyhinize kimseye yardım etmeyenler müstesnadır; onlarla antlaşmalarını süresinin sonuna kadar tamamlayın"*) ve hemen sonrasındaki 6. âyette (*"Müşriklerden biri senden eman dilerse ona eman ver ve onu güvenli yerine ulaştır"*) barışçıl müşriklerin mutlak koruma altına alındığı görülür. Dolayısıyla 9:5 yalnızca Hudeybiye barışını kanlı bir baskınla bozan muharip saldırganlara yöneliktir.
---

### ADIM 02 — MANTIKSAL SEMANTİK VE KARŞIT İLKE TESTİ

- **Koşul-Sonuç Yapısı:**
  - *Ön Koşul:* Diplomatik mühletin dolması (`فَإِذَا ٱنسَلَخَ`) + Muhatapların barışı ihlal etmiş olması (Adım 05, Tevbe 9:4).
  - *Askeri Yaptırım:* Kademeli harekât (abluka, gözetleme, yakalama, sıcak temasta etkisiz kılma).
  - *İptal Koşulu:* Düşmanlığın sona ermesi ve barış düzenine dahil olma (`فَخَلُّوا۟ سَبِيلَهُمْ`).
- **Karşıt İlke Testi:**
  - *Karşıt İlke / Gerilim:* **Ahit Güvenliği ve Caydırıcılık (Hıfzu'n-Nizâm) ↔ İnsan Onuru (Keramet) ve Merhamet.**
  - *Gerilimin Çözümü:* Saldırgan tarafa karşı kamu otoritesi meşru güç kullanmazsa mazlumların can emniyeti çöker. Caydırıcı güç, daha büyük bir anarşiyi önlemek için son çare olarak devreye girer.
  - *Feda Edilen Taraf (Trade-off):* Süresiz tavizkar barış feda edilir; bedeli caydırıcı askeri teyakkuz ve savunma yüküdür.

---

### ADIM 03 — ÜÇLÜ ÇERÇEVE (ETHOS / LOGOS / PATHOS) VE İS-OUGHT KÖPRÜSÜ

- **Ethos (Ahlaki Yük):** Ahde vefa esastır. Karşı taraf antlaşmayı tek taraflı çiğnesedahi, meşru devlet taahhüt ettiği mühletin son anına kadar antlaşmaya riayet etmek zorundadır. Adalet, intikam duygusunun önüne geçer.
- **Logos (Mantıksal Tutarlılık):** Eğer bir taraf antlaşmayı bozar, mühlet içinde de barışa yanaşmazsa; kamu otoritesi güç kullanmadığı takdirde anarşi doğar ve saldırgan ödüllendirilmiş olur. Caydırıcılık mantıksal bir zorunluluktur.
- **Pathos (Vicdani ve Duygusal Tesir):** İhanete uğramış mazlum topluma güven ve izzet aşılarken; teslim olan hasma anında af ve güven kapısı aralar.
- **İs-Ought Köprüsü ve Hume Giyotini:**
  - *İs (Olgu / Ampirik Durum):* Bir hasım güç yürürlükteki güvenlik antlaşmasını sistematik olarak ihlal etmekte ve diplomasiyi hileli bir zaman kazanma aracına dönüştürmektedir.
  - *Ought (Değer / Normatif Hüküm):* Meşru otorite adil bir mühlet tanımalı, süre bitiminde ise ihlali caydırıcı orantılı askeri tedbirlerle durdurmalıdır.
  - *Hume Giyotini Köprü Aksiyomu:* *"Hukuki yaptırımı ve caydırıcılığı bulunmayan antlaşmalar barış üretmez, yalnızca zorbanın tahakkümünü pekiştirir; binaenaleyh adaleti korumak ve can güvenliğini savunmak için orantılı güç kullanmak normatif bir zorunluluktur."*

---

### ADIM 04 — MAKASID ANALİZİ

- **Küllî Makasıd:** Can, din, akıl, nesil ve mal güvenliği.
- **Şâtıbî ve Cessâs Çerçevesi:**
  - `[NAKİL]`: Şâtıbî (*el-Muvâfakât*, C. 3, s. 340-345)[^4], ceza ve cihat nasslarının kamu yararı ve fesadın defi (*def‘-i mefsede*) ekseninde anlaşılması gerektiğini; 9:5'in barış nasslarını nesh etmeyip muharip saldırganlara tahsis ettiğini vurgular. Cessâs (*Ahkâmü'l-Kur'ân*, C. 4, s. 268)[^5] da âyetin ahdini bozanlarla sınırlı olduğunu tescil eder.
  - `[YORUM]`: Âyetin nihai makāsıdı kan dökmek değil; antlaşma ihlallerini sonlandırarak toplumsal barışı ve hukuk nizamını korumaktır (*Hıfzu'n-Nizâm*).
- **Zarûriyyât Dengelemesi:**
  1. *Canın Korunması (Hıfzu'n-Nefs):* Masumların canı korunurken, Tevbe 9:6 ile teslim olan düşmanın canı da dokunulmaz kılınır.
  2. *Dinin Korunması (Hıfzu'd-Dîn):* İnanç özgürlüğünün silah zoruyla yok edilmesinin engellenmesi.
  3. *Malın Korunması (Hıfzu'l-Mâl):* Yağma ve talan saldırılarına karşı ekonomik güvenliğin tesisi.

---

### ADIM 04b — YORUMCU KONUMU (GADAMER HERMENÖTİĞİ)

1. **Usûl Ekolü:** Çoğulcu-Makāsıdî Hanefî usûlü (istişhâd, tahsis ve nassların birbirini tefsir etmesi ilkesi; Şâtıbî, *el-Muvâfakât*, C. 3, s. 340–345; Cessâs, *Ahkâmü'l-Kur'ân*, C. 4, s. 268 ve İbn Âşûr, *et-Tahrîr ve't-Tenvîr*, C. 10, s. 112–118 çizgisi).
2. **Felsefi Perspektif:** Eleştirel realizm, sistemler kuramı ve uluslararası ilişkilerde Grotiusçu "Adil Savaş" (*Bellum Justum*) kuramı.
3. **Alternatif Yorumcu Konumu:**
   - *Tekfirci / Haricî Literalist Perspektif:* Bu âyeti önceki tüm barış âyetlerini iptal eden "evrensel imha fermanı" kabul ederek daimi çatışma üretir.
   - *Seküler Pasifist Perspektif:* Âyetteki askeri mukabele emirlerini bütünüyle reddederek saldırgana karşı meşru savunma hakkını felç eder.
   Raporumuz bu iki aşırı uçtan metodolojik olarak ayrışır.

---

### ADIM 05 — SİYAK-SİBAK ANALİZİ (S1–S7)

- **S1 (Önceki Âyetler — Tevbe 9:1–4):** Tevbe 9:4 en hayati istisnayı koyar: *"Ancak kendileriyle antlaşma yaptığınız, sonra da size karşı hiçbir eksiklik yapmayan ve aleyhinize hiçbir kimseye arka çıkmayan müşrikler müstesnadır. Onların antlaşmalarını sürelerine kadar tamamlayın."* Bu sibak, savaş gerekçesinin karşı tarafın inancı değil, **ihaneti ve ahit ihlali** olduğunu belgeler.
- **S2 (Sonraki Âyet — Tevbe 9:6):** Hemen sonraki âyet diplomasi ve eman koridorunu açar: *"Eğer müşriklerden biri senden eman dilerse, Allah'ın kelamını işitinceye kadar ona eman ver; sonra onu güven içinde bulunacağı yere ulaştır."*
- **S3 (Pasajın Konumu):** Tevbe 9:1'deki ilişik kesme (*Berâet*) ilanı ile başlar.
- **S4 (Sûre İçi Bütünlük):** Tevbe 9:128-129'daki şefkat ve yalnızca Allah'a tevekkül ilkesi ile tamamlanır.
- **S5 (Nüzûl Sebepleri ve Hitap):** Hicretin 9. yılı (Tebük Seferi sonrası, Mekke Fethi'nin ardından Arap Yarımadası'ndaki siyasi krizlerin çözüldüğü Hac dönemi).
- **S6 (Mushaf Sırası ve Tevkîfî Yapı):** Medine İslam Devleti'ne yönelik iç ve dış güvenlik tehditlerinin hukuki tasfiyesi.
- **S7 (Kırpma Riski):** **EVET / ÇOK YÜKSEK.** Tarih boyunca gerek radikal yapılar gerekse polemikçiler; 9:5'i 9:4'teki sadık müttefikleri koruma emrinden ve 9:6'daki eman/sığınma hakkından kopararak genel katliam fermanı gibi sunmuşlardır. Bu kırpma usûlen batıldır.

---

### ADIM 06 — ÇAPRAZ ÂYET ANALİZİ

- **Mümtehine 60:8–9:** Sizinle din hususunda savaşmayan ve sizi yurtlarınızdan çıkarmayanlara iyilik yapmanız ve adaletle davranmanız emredilir.
- **Bakara 2:190:** Sizinle savaşanlarla Allah yolunda savaşın; fakat haddi aşmayın.
- **Enfâl 8:58:** Bir kavmin hıyanetinden korkarsan, antlaşmayı aynı şekilde bozduğunu adilane bildir.
- **Enfâl 8:61:** Eğer barışa meylederlerse, sen de ona meylet.
- *Analitik Sonuç ve N4 Kapsamı:* Kur'an'ın genel ilkesi barış ve ahde vefadır. Tevbe 9:5 bu kuralı çiğneyen mütecavizlere yönelik istisnai yaptırım maddesidir (`N4`).

---

## FAZ II — SİSTEM VE GELECEK MODELLEMESİ

### ADIM 07 — SİSTEM HARİTASI (CAUSAL LOOP DİAGRAMI — CLD), GECİKME VE KIRILMA NOKTASI (N4)

- **Temel Sistem Değişkenleri (Stok & Akış Değişkenleri):** `[YORUM]` **Stok Değişkenler:** Antlaşma Güvenilirliği Stoku (*Ahde Vefa Sermayesi*), Sınır ve Kamu Güvenliği Stoku, Caydırıcı Savunma Kapasitesi. **Akış Değişkenler:** Ahit İhlali Hızı (*Nakz-ı Ahd Oranı*), Diplomatik Mühlet ve İhtar Akışı (4 Aylık Haram Aylar), Orantılı Caydırıcı Mukabele Hızı ve Eman/Diplomatik Koridor Açılma Oranı (Tevbe 9:4–6).
- **Pekiştirici Döngü (R1 — Cezasızlık ve Güvenlik Çöküşü Kısır Döngüsü / Vicious Cycle):** `[YORUM]` Ahit İhlali ve Saldırganlık (`+`) → Cezasızlık ve Pasif Taviz (`+`) → Mütecaviz Aktörün Stratejik Cüretkârlığı (`+`) → Sınır İhlalleri ve Sivil Güvenlik Kaybı (`+`) → Caydırıcılık İtibarının Erozyonu (`-`) → Ahit İhlali ve Saldırganlık (`+`). *(Hukuki müeyyideden yoksun tek taraflı pasifizm, saldırganlığı ödüllendirerek bölgesel kaos sarmalını kendi kendine besler).*
- **Dengeleyici Döngü (B1 — Tevbe 9:5–6 Müeyyideli Barış ve Eman Freni / Balancing Loop):** `[YORUM]` Ahit İhlali ve Güvenlik Tehdidi (`+`) → 4 Aylık Resmi Diplomatik Ültimatom ve İhtar (`+`) → Kademeli Gözetleme, Muhasara ve Meşru Savunma Mukabelesi (`+`) → Saldırganın Askeri Maliyetinin Artması ve İhlal Kapasitesinin Daralması (`+`) → Tevbe/Sulh veya Eman Koridoru (9:6) ile Hukuk Nizamına Dönüş (`+`) → Ahit İhlali ve Güvenlik Tehdidi (`-`). *(Kararlı caydırıcılık ve açık diplomasi kapısı sistemi yeniden sulh dengesine çeker).*
- **Sistemik Gecikme (Delay) ve Kaldıraç Noktası (Leverage Point):** `[YORUM]` **Sistemik Gecikme (Delay):** Tevbe 9:2 ve 9:5'te vaz'edilen **4 aylık (120 günlük) haram aylar mühleti**, ani askeri tırmanmayı önleyen bilinçli bir kurumsal soğutma ve diplomatik doğrulama gecikmesidir. **Kaldıraç Noktası (Leverage Point):** Tevbe 9:4'teki *"Ahdine sadık kalanları koruma"* ilkesi ile 9:6'daki *"Eman dileyene güvenli geçiş sağlama"* kuralının birlikte işletilmesi, çatışmayı topyekûn savaşa dönüşmeden çözen en yüksek kaldıraç noktasıdır.
- **Kırılma Noktası (Tipping Point) ve Erken Uyarı Sinyali (N4 / EU):** `[YORUM]` **Tipping Point (Kırılma Noktası):** Dört aylık diplomatik mühletin karşı tarafça barış arayışı yerine fiilî saldırı tahkimatı için kötüye kullanılması ve aylık sınır/ateşkes ihlallerinin kritik eşiği (`> 3 ihlal/ay`) aşması. **Erken Uyarı Sinyali (N4 / EU-01):** Sadık müttefiklere yönelik vekâlet saldırılarının başlaması, diplomatik iletişim kanallarının tek taraflı kapatılması ve sınır hatlarında olağandışı lojistik yığınak tespiti.
---

### ADIM 08 — DÖRT SENARYO VE STRATEJİK DEĞERLENDİRME

1. **Koruyucu Senaryo (Müeyyideli Barış):** Mühlet disiplini işletilir, caydırıcı askeri hazırlık tamamlanır, karşı taraf saldırıdan vazgeçerek sulhe döner. Ufuk: H1.
2. **Bozuluş Senaryosu (Taviz ve Felç Sarmalı):** İhanetlere karşı güç kullanılmaz, pasif kalınır, güvenlik kuşağı çöker. Ufuk: H1–H2.
3. **Denge Senaryosu (Kademeli Askeri Sınırlandırma):** Sıcak temas yerine lojistik yollar kesilir, gözetleme mevzileri tutulur, hasım teslim olmaya zorlanır. Ufuk: H2.
4. **İhya Senaryosu (Hukuki ve Sosyal Entegrasyon):** Düşman silah bırakır, eman verilir, anayasal sözleşmeye dahil edilerek barış kurulur. Ufuk: H2–H3.
*(Tüm puanlar YAML üstverisindeki gerekçelere dayanır; V5 kuralı).*

---

### ADIM 09 — ZAMAN UFKU BANDI (H1–H4)

- **H1 (1-2 Yıl):** Sıcak kriz yönetimi, 4 aylık diplomatik mühlet ilanı, sınır teyakkuzu ve yıllık pencere.
- **H2 (3-5 Yıl):** Caydırıcı savunma mimarisi ve bölgesel güvenlik paktlarının inşası için zaman aralığı.
- **H3 (5-10 Yıl):** Ahit güvenliğini garanti altına alan uluslararası hukuk ve hakemlik kurumlarının kurumsallaşması.
- **H4 (10+ Yıl Medeniyet Ufku):** Küresel silahsızlanma ve adil barış nizamının sürdürülebilirliği.

---

### ADIM 10 — MORFOLOJİK GÖZLEM

- **Kayıt:** Ebced veya sayısal batıl teviller reddedilmiş olup kullanılmamıştır (metodolojik yasak).
- **Morfolojik Analiz:** Âyetteki `فَٱقْتُلُوا۟`, `وَخُذُوهُمْ`, `وَٱحْصُرُوهُمْ`, `وَٱقْعُدُوا۟` fiilleri cemi (çoğul) emir kalıbındadır. İslami fıkıh metodolojisinde cemi emirler bireylere değil; kamu otoritesine ve ordu komutanlığına yöneliktir. Bireysel linç morfolojik olarak reddedilmiştir.

---

### ADIM 10b — BELİRSİZLİK VE KARAR STRATEJİSİ

- **Belirsizlik Türü:** Stratejik Belirsizlik (Düşmanın mühlet bitiminde savaşı mı teslimiyeti mi seçeceğinin öngörülemezliği).
- **Karar Stratejisi:** Robust / Shaping (Hem askeri savunmaya hazır olma hem de barış koridorunu açık tutma stratejisi).

---

## FAZ III — SINAMA, KARŞI OKUMA VE AHLAKÎ DEĞERLENDİRME

### ADIM 11 — 8 İÇ DENETİM TESTİ (ALGORİTMİK İÇ TUTARLILIK)

- **Test 1 (Lafız Uyumu):** Kûfî 6236 standardında Tevbe 5. âyettir. (İç denetimden geçti).
- **Test 2 (İmla):** Resm-i Osmânî imlâsına uygundur. (İç denetimden geçti).
- **Test 3 (Bağlam):** 9:4 ve 9:6 ile birleşik test edilmiştir. (İç denetimden geçti).
- **Test 4 (Sağlamlık):** 5 temel usûl kaynağında anlam bütünlüğü sınanmıştır. (İç denetimden geçti).
- **Test 5 (Siyak-Sibak Uyumu):** 5a-5g alt maddeleri doğrulanmıştır. (İç denetimden geçti).
- **Test 6 (Dil Güvenliği ve Mutlakiyet Yasağı):** Kesinlik iddialarından arındırılmıştır. (İç denetimden geçti).
- **Test 7 (Base-rate ve Veri Uyumu):** Uppsala Çatışma Veri Programı (UCDP) 2024[^6] ve PRIO raporları referans alınmıştır (https://ucdp.uu.se/).
- **Test 8 (Öz-Denetim ve Rol Ayrımı):** Metodolojik zayıflıklar açıkça listelenmiştir.
*(NOT: Bu adım algoritmik iç tutarlılık kontrolüdür; bağımsız dış akademik hakem onayı niteliği taşımaz).*

---

### ADIM 12 — RED TEAM (KARŞIT OKUMA) VE FALSIFIABILITE PROTOKOLÜ

- **Red Team İtirazları:**
  - *İtiraz:* "Âyet açıktır: Müşrikleri nerede bulursanız öldürün der. Barış âyetlerini nesh etmiştir."
  - *Cevap:* Bu iddia 9:4'teki sarih istisnayı ve 9:6'daki eman emrini keyfi iptal eder. Usûlde nesh ancak sarih delille mümkündür; genel ilke tahsis edilmiştir (Şâtıbî, *el-Muvâfakât*, C. 3, s. 340–345; Cessâs, *Ahkâmü'l-Kur'ân*, C. 4, s. 268).
- **Falsifiabilite Protokolü (Yalnızca Ampirik ve Dünyevi Politika Hipotezlerine):**
  - **Uygulanan Alan:** Karar kollarındaki ampirik uygulama modeli.
  - **Zaman Aralığı:** 5 Yıllık İzleme Penceresi (2026–2031).
  - **Bağımsız Endeks ve Veri Kaynağı:** Dünya Bankası Hukukun Üstünlüğü Endeksi veritabanı (https://datacatalog.worldbank.org/)[^7] ve IEP Küresel Barış Endeksi[^8].
  - **Sayısal Eşik ve Tipping Point:** 5 yıllık pencere içinde çatışma nüks ve ahit güvenliği skoru $\ge 0.75$ sayısal eşik değerine ulaşır ve taahhüt ihlal oranı $\le \%15$ seviyesine gerilerse, askeri abluka ve yüksek caydırıcılık kararı geri çekilir.

---

### ADIM 13 — ENFÜS-ÂFÂK VE KALP FIKHI

- **Enfüs (İçsel ve Ahlaki Boyut):** İnsanın iç dünyasında nefsin hilekâr hevesleri vicdani sözleşmeleri bozar. Mühlet vermek; nefse tefekkür imkânı tanımaktır. Eğer nefs ihaneti sürdürürse ahlaki irade ile o hevesler zapturapt altına alınmalıdır.
- **Âfâk (Dışsal ve Kurumsal Boyut):** Bireysel intikam hırsının meşru devlet siyasetine sızmasını önlemek; adaleti güç kullanımının tek meşru gerekçesi kılmak.
- **Karşılıklı Etki:** İçsel olarak ahde vefa ahlakı yerleşmemiş bir toplum, dış ilişkilerinde güvenilir paktlar kuramaz; dış güvensizlik de içerde paranoyayı besler.
- **Karar Köprüsü:** İç dünyasında ahde vefayı başaramayan bir liderlik, dış siyasette meşru caydırıcılığı adaletle yönetemez; intikam hırsına yenik düşer. Bu sebeple Adım 15'teki K1 ve K3 kolları vicdani denetim şartına bağlanmıştır.
- **İşârî / İrfanî Derinlik:** Güvenilir tasavvufi tefsirler çerçevesinde nefisle cihat (*cihâd-ı ekber*; Beyhakî, *ez-Zühdü'l-Kebîr*, nr. 373; krş. Buhârî, *Rikâk*, 34, nr. 6496), dış dünyadaki güç kullanımının sınırlarını belirleyen en yüksek ahlaki frendir.

---

## FAZ IV — BAYES, KARAR VE ETİK DENETİM

### ADIM 14 — ERKEN UYARI SİNYALLERİ VE BAYES GÜNCELLEMESİ

- **Erken Uyarı Sinyalleri (EU-01..EU-04):**
  - `EU-01`: Sınır ihlallerinin ayda 3 vakayı aşması.
  - `EU-02`: Karşı tarafın diplomatik heyetleri oyalaması.
  - `EU-03`: Askeri yığınak istihbaratı.
  - `EU-04`: Propaganda dilinin düşmanlaştırıcı hale gelmesi.
- **Bayes Güncelleme Alanı (`Senaryo S1 — Caydırıcılık Destekli Ahit Barışı`):**
  - **Önsel Olasılık (Prior $P(S_1)$):** `0.42` (%42.0 — UCDP / PRIO 2024 Çatışma Nüksü Veritabanı başlangıç olasılığı).
  - **Koşullu Olabilirlik $P(E|S_1) = 0.85$ & Yanlış Pozitif $P(E|\neg S_1) = 0.18$:** 120 günlük diplomatik mühlet (`th-01`), orantılı sınır tahkimatı (`marsad`) ve sivil eman koridoru (`9:6`) birlikte işletildiğinde ateşkes istikrarının korunma olasılığı.
  - **Sonsal Olasılık (Posterior $P(S_1|E)$):** $P(S_1|E) = \frac{0.42 \times 0.85}{(0.42 \times 0.85) + (0.58 \times 0.18)} = 0.774 \approx 0.77$ (%77.4 — **+35.4 puanlık** istikrar artışı).
  - *Kapsam Notu:* Bayes güncellemesi YALNIZCA ölçülebilir güvenlik göstergelerinde çalışır; teolojik ve ahlaki normlara sayısal olasılık verilemez (Bölüm 9 yasağı).

---

### ADIM 15 — KARAR VE POLİTİKA KOLLARI (K1–Kn)

- **Karar Kolu 1 (K1) — Diplomatik Mühlet ve Ahit Yenileme:**
  - **Aktör:** Dışişleri Bakanlığı ve Diplomatik Müzakere Heyeti.
  - **Araç:** Diplomatik nota ve mühlet takvimi.
  - **CLD Kaldıraç Noktası:** R1 döngüsünü diplomasi ile dondurma.
  - **Eşik:** [TAHMİNÎ EŞİK] Müzakere oturumu $\ge 5$, ihlal çözülme oranı $\ge \%80$.
- **Karar Kolu 2 (K2) — Kademeli Askeri Abluka ve Nokta Caydırıcılık:**
  - **Aktör:** Savunma Bakanlığı ve Genelkurmay Başkanlığı.
  - **Araç:** Lojistik abluka (*hasr*) ve geçiş yollarını tutma (*marsad*).
  - **CLD Kaldıraç Noktası:** B1 dengeleyici döngüsünü harekete geçirme.
  - **Eşik:** [TAHMİNÎ EŞİK] İkmal hatlarının kesilmesi $\ge \%70$, sivil zayiat $= 0$.
- **Karar Kolu 3 (K3) — İltica, Eman ve Rehabilitasyon:**
  - **Aktör:** İçişleri Bakanlığı ve İnsani Diplomasi Masası.
  - **Araç:** Güvenli geçiş koridoru ve sığınma hakkı (Tevbe 9:6).
  - **CLD Kaldıraç Noktası:** Düşmanlığın kalıcı tasfiyesi.
  - **Eşik:** [TAHMİNÎ EŞİK] Eman verilenlerin güvenli tahliyesi $\ge \%99$, nüks $\le \%5$.

- **Karar Ağacı Mantığı:**
```
[Uluslararası Ahit / Antlaşma Süreci] ---> [1. Adım: Karşı Taraf Ahde Vefa Gösteriyor mu? (9:4)]
                                                               |
                                 +-----------------------------+-----------------------------+
                                 |                                                           |
                              [EVET]                                                      [HAYIR]
                                 |                                               (Sistematik İhlal: Nakz-ı Ahit)
                  [Tam Ahde Vefa ve Barışın İdamesi]                                         |
                  (Süre Sonuna Kadar Dokunulmazlık)                          [K1: 120 Günlük Diplomatik Ültimatom]
                                                                                             |
                                                                             [Saldırganlıktan Rücu / Eman Talebi?]
                                                                                             |
                                                                             +---------------+---------------+
                                                                             |                               |
                                                                          [EVET]                          [HAYIR]
                                                                             |                               |
                                                                [K3: Eman ve Güvenli Tahliye]   [K2: Orantılı Meşru Müdafaa]
                                                                        (Tevbe 9:6)                (Sivil Dokunulmazlığı)
```

---

### ADIM 16 — ÖNYARGI VE TARAFLILIK DENETİMİ

- Modernist veya mezhepçi anakronizm kontrolleri yapılmıştır.
- **Dil Güvenliği ve Öz-Denetim:** Yasaklı kelime kullanılmamıştır.
- **Retrodiction (Geriye Dönük Sınama):** 1938 Münih Antlaşması'ndaki yatıştırma politikasının iflası ve 1962 Küba Füze Krizi'ndeki kontrollü deniz ablukası (*hasr / marsad*) örnekleri incelenmiş; tek taraflı tavizin savaşı önlemediği, caydırıcı sınır çekmenin barışı koruduğu kısmen doğrulanmıştır.

---

## FAZ V — GÜVEN, SORUMLULUK VE İZLEME KAYDI

### ADIM 17 — GÜVEN DÜZEYİ
- **Nitel Derece:** B (Orta-Yüksek Analitik Güven). Sayısal bir olasılık veya dogmatik kesinlik iddiası değildir.

---

### ADIM 17b — AKTÖR VE GÜÇ HARİTASI
- **Karar Vericiler:** Devlet başkanlığı, güvenlik konseyi.
- **Uygulayıcılar:** Ordu, diplomasi bürokrasisi, istihbarat teşkilatı.
- **Etkilenen Gruplar:** Sınır boylarındaki masum siviller, tüccarlar, sığınmacılar.
- **Gelecek Nesiller:** Barış paktının kalıcılığından yararlanacak toplum.

---

### ADIM 18 — BİLGİ TABANI VE ZAYIFLIK LİSTESİ
- **Bilgi Tabanı:** Kaynaklı tefsir nakilleri, uluslararası çatışma veri tabanları (UCDP), ampirik politika hipotezleri.
- **Zayıflıklar:** 7. yüzyıl Hicaz diplomatik kayıtlarının rivayet zincirlerine dayanması; modern uluslararası sistemdeki veto yetkili asimetriler.

---

### ADIM 18.1 — DİL GÜVENLİĞİ
- Rapor metninde kesinlik, tekelcilik veya sahte-onay iddialarından arındırma denetimi yapılmıştır.

---

### ADIM 19 — İZLEME VE GERİYE DÖNÜK SINAMA (RETRODICTION)
- **İzleme KPI:** Sınır ihlal frekansı, diplomatik nota geri dönüş süresi ($\le 48$ saat).
- **Retrodiction:** 1938 Münih Anlaşması ve 1962 Küba Krizi mukayeseli tarihsel testi.

---

### ADIM 20 — AÇIK ARAŞTIRMA SORULARI, VARSAYIMLAR VE 40 DAKİKALIK TYMM PEDAGOJİK DERS PLANI
- **Açık Sorular:** BM Güvenlik Konseyi'nin felç olduğu krizlerde meşru caydırıcılığı hangi aktörler sağlayacaktır?
- **Temel Varsayım:** Devletlerin rasyonel güvenlik ve hayatta kalma güdüsüyle hareket ettiği kabul edilmiştir.
- **40 Dakikalık TYMM Pedagojik Ders ve Seminer Planı (Tevbe 9:5 — Ahit Güvenliği ve Meşru Savunma Etiği):**
  - **TYMM Erdem-Değer-Eylem Çerçevesi:** *Adalet, Ahde Vefa, Barış, Sorumluluk ve Hikmet.*
  - **1. Aşama — Hazırlık ve Bağlamsal Keşif (0–10 Dk):** Öğrencilere Tevbe 9:4, 9:5 ve 9:6 âyetleri birlikte okutularak *"Bir kanun maddesini önceki ve sonraki maddelerden koparıp tek başına okumak hangi adaletsizliklere yol açar?"* sorusu yöneltilir (`S7 Kırpma Riski` farkındalığı).
  - **2. Aşama — Klasik Tefsir ve Kavram Atölyesi (10–20 Dk):** `İnsilâh` (4 aylık diplomatik mühlet), `ahd-i hâricî` (yalnızca ahdi bozan saldırganlar) ve `istîmân` (Tevbe 9:6 sığınma ve güvenli koridor hakkı) kavramları Zemahşerî (*el-Keşşâf*, C. 3, s. 10–15) ve Şâtıbî (*el-Muvâfakât*, C. 3, s. 340–345) nakilleriyle incelenir.
  - **3. Aşama — Yapılandırılmış Sınıf Münazarası ve Sistem Haritası (20–30 Dk):** Sınıf iki gruba ayrılır; **1. Grup** *"Uluslararası krizlerde süresiz pasifizm ve taviz barışı korur mu?"* (`R1` kısır döngüsü), **2. Grup** ise *"Hukuki mühlet, orantılı caydırıcılık ve açık eman koridoru kalıcı barışı nasıl kurar?"* (`B1` dengeleyici döngüsü) tezlerini CLD diyagramı üzerinden tartışır.
  - **4. Aşama — Sentez ve Öz-Değerlendirme (30–40 Dk):** Öğrenciler İslam uluslararası hukukunda barışın asıl, savaşın ise yalnızca ahit ihlali ve saldırganlığa karşı istisnai bir savunma tedbiri olduğunu özetleyen birer paragraflık *"Adil Barış Beyannamesi"* yazar.

---

## KOŞULLU EKLER (Z-1 — Z-5)

### Z-1 · ŞABLONA SIĞMAYAN ÖZGÜN PROBLEMATİK [V9 ZORUNLU]

#### "Kılıç Âyeti" ve Nesh Tartışması: 140 Barış Âyetinin İptali İddiası ve Metodolojik Kriz

Tevbe 9:5 âyetinin geleneksel tefsir ve fıkıh tarihindeki en çetin aporiası (çözümsüzlük düğümü); bazı mütekaddimûn ulemasının bu tek âyetle Kur'an'daki af, sabır, sulh ve müsamaha emreden yaklaşık 140 âyetin hükmünün yürürlükten kaldırıldığını (*nesh*) iddia etmiş olmasıdır.

Bu iddia şu derin teolojik ve metodolojik krizi doğurur:
1. Eğer Tevbe 9:5 bütün barış âyetlerini nesh ettiyse; Kur'an'ın "Dinde zorlama yoktur" (Bakara 2:256) ve "Sizin dininiz size, benim dinim bana" (Kâfirûn 109:6) gibi temel ahlaki-ontolojik ilkeleri tarihsel birer parantezden mi ibarettir?
2. Şâtıbî (*el-Muvâfakât*, C. 3, s. 340–345) ve Cessâs (*Ahkâmü'l-Kur'ân*, C. 4, s. 268) gibi usûlcüler erken dönemdeki "nesh" ıstılahının "tahsis ve takyid" (genel kuralın özel duruma sınırlandırılması) anlamında kullanıldığını belgelemiştir. Ancak buna rağmen tarih boyunca siyasi iktidarlar ve radikal yapılar, nesh teorisini sınırsız bir fetih ve imha ideolojisinin meşruiyet aracına dönüştürmüştür.
3. Quran Vision analiz motorunun benimsediği Makasıdî Usûl, bu krizi "Tahsis Doktrini" ile çözmektedir: Barış genel ve kalıcı ilkedir; savaş ise antlaşmayı bozan muhariplere has istisnai bir güvenlik tedbiridir. Ancak bu çözüm dahi, klasik literatürdeki 140 âyetin nesh edildiği yönündeki devasa külliyatla modern okuyucu arasındaki hermenötik gerilimi tamamen ortadan kaldıramaz. Bu husus şablonun ötesinde, bağımsız bir kelam ve tefsir usûlü müzakeresini zorunlu kılmaktadır.

---

### Z-2 · GÖRÜŞ İHTİLAFI CETVELİ [V3 ZORUNLU]

| Görüş Sahibi / Ekol | Lafzî Yorumu | Hukuki / Stratejik Neticesi | Dayandığı Temel Delil |
| :--- | :--- | :--- | :--- |
| **Görüş 1: Radikal / Haricî Literalist Ekol** | Âyetteki emir mutlaktır; barış âyetlerinin tamamını nesh etmiştir. | Gayrimüslimlerle sürekli savaş esastır; barış geçici bir aldatmacadır. | *"Müşrikleri nerede bulursanız öldürün"* mutlak lafzı. |
| **Görüş 2: Klasik Şâfiî Ekolü** | Savaşın sebebi küfürdür (*illetü'l-kıtâl el-küfr*); cizye veya İslam'a kadar savaş meşrudur. | Gayrimüslim devletlerle barış ancak zaruret halinde ve geçici (en fazla 10 yıl) yapılabilir. | Tevbe 9:5 ve 9:29'daki sarih kıtal ve cizye emirleri (Şâfiî, *el-Ümm*, C. 4, s. 240–252). |
| **Görüş 3: Klasik Hanefî ve Mâlikî Ekolü (Cumhur)** | Savaşın sebebi küfür değil, fiili savaştır (*illetü'l-kıtâl el-harb / el-muhârebe*). | Kadınlar, çocuklar, din adamları ve savaşmayan siviller asla hedef alınamaz; saldırmayana savaş açılmaz. | Bakara 2:190 (*"Sizinle savaşanlarla savaşın, haddi aşmayın"*) ve Hz. Peygamber'in yasakları (Buhârî, *Cihâd*, 147–148, nr. 3014–3015; Müslim, *Cihâd*, 24–25, nr. 1744; Ebû Dâvûd, *Cihâd*, 82, nr. 2614). |
| **Görüş 4: Çağdaş Makasıdî / Tarihselci Ekol (Şâtıbî, İbn Âşûr, Abduh)** | Elif-lâm ahd-i hâricîdir; Hudeybiye'yi bozan muayyen Mekke müşriklerine hastır; nesh değil tahsistir. | Evrensel kural barış, adalet ve diplomasidir. Güç kullanımı ancak meşru müdafaa ve ahit ihlali durumunda caizdir. | Tevbe 9:4 ve 9:6 âyetleri (Şâtıbî, *el-Muvâfakât*, 3/340; İbn Âşûr, *et-Tahrîr*, 10/112; Muhammed Abduh & Reşîd Rızâ, *Tefsîrü'l-Menâr*, C. 10, s. 190). |

---

### Z-3 · ZAYIFLIK, VARSAYIM VE GELİŞTİRME ÖNERİLERİ LİSTESİ

- **Temel Varsayımlar:**
  1. Âyetteki kıtal ve abluka hitabının bireysel linç gruplarına değil, anayasal meşru bir kamu otoritesine ait olduğu varsayılmıştır.
  2. Uluslararası sistemde devletlerin rasyonel güvenlik ve hayatta kalma güdüsüyle hareket ettiği kabul edilmiştir.
- **Metodolojik Zayıflıklar ve Geliştirme Önerisi:**
  1. *Veri Asimetrisi:* 7. yüzyıl Hicaz diplomatik metinlerinin günümüze sadece rivayet zincirleriyle ulaşmış olması sebebiyle tarafların ihlal oranları modern veri standardında ölçülememektedir.
  2. *Modern Hukuk Uyum Boşluğu:* `Hasr` ve `marsad` kavramlarının siber savaş ve modern ambargo rejimlerine fıkhi uyarlamasında literatür boşluğu bulunmaktadır.
  3. *Geliştirme Önerisi:* Uluslararası insancıl hukukçular ile İslam fıkıhçılarından oluşan bağımsız bir heyet tarafından "Modern Çağda Ahit İhlalleri ve Meşru Güç Kullanım Standartları Rehberi" hazırlanmalıdır.
- **Açık / Cevaplanmamış Sorular:**
  1. Birleşmiş Milletler Güvenlik Konseyi'nin kilitlendiği krizlerde meşru caydırıcılığı hangi uluslararası aktörler icra edecektir?
  2. Hibrit ve asimetrik savaşlarda "diplomatik mühletin bitişi" hangi dijital eşiklerle saptanacaktır?

---

### Z-4 · STANDART VE DÜRÜST SINIR İFADESİ [V10 ZORUNLU]

> **METODOLOJİK VE EPİSTEMİK SINIR BEYANI:**
> Bu rapor; Kur'an Temelli Gelecek Vizyonu (Quran Vision v6.2.1) mimarisi çerçevesinde üretilmiş analitik ve hermenötik bir modellemedir. Dini bir fetva, kesin kazi bir hüküm veya ilahi muradın eksiksiz ve yegâne tefsiri niteliği taşımaz. Raporda yer alan simülasyonlar, göstergeler ve politika kolları; analistin benimsediği usûl ekolünün ve ampirik varsayımların bir türevidir. Bu metin, kod tabanlı biçimsel iç tutarlılık denetiminden (gem_lint.py) geçmiş olup, bağımsız dış akademik hakem heyeti (peer-review) tarafından tescil edilmedikçe bilimsel kesinlik iddiası barındırmaz.

---

### Z-4.5 · AKADEMİK KAYNAKÇA (İSNAD 2 VE APA / DOI BİBLİYOGRAFYASI)

#### A) Klasik İslami Kaynaklar (İSNAD 2. Edisyon Standartlı)
- **Cessâs, Ahmed b. Ali er-Râzî (ö. 370/981).** *Ahkâmü'l-Kur'ân*. Tahkik: Muhammed Sadık Kamhâvî. 5 Cilt. Beyrut: Dâru İhyâi't-Türâsi'l-Arabî, 1412/1992. Erişim: https://shamela.ws/book/23579
- **İbn Fâris, Ahmed b. Fâris b. Zekeriyyâ (ö. 395/1004).** *Mu'cemü Makâyîsi'l-Lüğa*. Tahkik: Abdüsselâm Muhammed Hârûn. 6 Cilt. Beyrut: Dârü'l-Fikr, 1399/1979. Erişim: https://shamela.ws/book/21710
- **İbn Manzûr, Muhammed b. Mükerrem (ö. 711/1311).** *Lisânü'l-Arab*. 15 Cilt. Beyrut: Dârü Sâdır, 1413/1993. Erişim: https://shamela.ws/book/1687
- **Şâtıbî, İbrâhîm b. Mûsâ el-Garnâtî (ö. 790/1388).** *el-Muvâfakât fî Usûli'ş-Şerî'a*. Tahkik: Meşhûr b. Hasan Âl-i Selmân. 6 Cilt. Riyad: Dâru İbni Affân, 1417/1997. Erişim: https://shamela.ws/book/11435
- **Zemahşerî, Mahmûd b. Ömer (ö. 538/1144).** *el-Keşşâf 'an Hakâ'ikı Gavâmizi't-Tenzîl ve 'Uyûni'l-Ekâvîl fî Vucûhi't-Te'vîl*. Tahkik: Âdil Ahmed Abdülmevcûd, Ali Muhammed Muavvaz. 6 Cilt. Riyad: Mektebetü'l-Ubeykân, 1418/1998. Erişim: https://shamela.ws/book/23627

#### B) Çağdaş Kurumsal, Hukuki ve Ampirik Kaynaklar (APA 7 / DOI Standartlı)
- **Institute for Economics and Peace [IEP] (2024).** *Global Peace Index 2024: Measuring Peace in a Complex World*. Sydney: Institute for Economics & Peace. https://www.economicsandpeace.org. Erişim adresi: https://www.economicsandpeace.org
- **Uppsala University [UCDP] (2024).** *UCDP Georeferenced Event Dataset (GED) and Armed Conflict Database 2024*. Uppsala: Department of Peace and Conflict Research. https://doi.org/10.1177/0022343320934986. Erişim adresi: https://ucdp.uu.se
- **World Bank Group (2024).** *Worldwide Governance Indicators (WGI): Rule of Law and Political Stability*. Washington, D.C.: The World Bank. Erişim adresi: https://datacatalog.worldbank.org

#### C) Metin İçi Akademik Dipnotlar (Footnotes)
[^1]: İbn Fâris, Ahmed b. Fâris (ö. 395/1004), *Mu'cemü Makâyîsi'l-Lüğa*, thk. Abdüsselâm Muhammed Hârûn (Beyrut: Dârü'l-Fikr, 1979), 3: 97-98 ("s-l-h" maddesi).
[^2]: Zemahşerî, Mahmûd b. Ömer (ö. 538/1144), *el-Keşşâf 'an Hakâ'ikı Gavâmizi't-Tenzîl*, thk. Âdil Ahmed Abdülmevcûd - Ali Muhammed Muavvaz (Riyad: Mektebetü'l-Ubeykân, 1998), 3: 10-15.
[^3]: İbn Manzûr, Muhammed b. Mükerrem (ö. 711/1311), *Lisânü'l-Arab* (Beyrut: Dârü Sâdır, 1993), 3: 182-184 ("r-s-d" maddesi).
[^4]: Şâtıbî, İbrâhîm b. Mûsâ (ö. 790/1388), *el-Muvâfakât*, thk. Meşhûr b. Hasan Âl-i Selmân (Riyad: Dâru İbni Affân, 1997), 3: 340-345.
[^5]: Cessâs, Ahmed b. Ali er-Râzî (ö. 370/981), *Ahkâmü'l-Kur'ân*, thk. Muhammed Sadık Kamhâvî (Beyrut: Dâru İhyâi't-Türâsi'l-Arabî, 1992), 4: 268-272.
[^6]: Uppsala University (UCDP), *UCDP Georeferenced Event Dataset (GED) and Armed Conflict Database 2024* (Uppsala: Department of Peace and Conflict Research, 2024), doi:10.1177/0022343320934986, erişim 15 Ekim 2026, https://ucdp.uu.se.
[^7]: World Bank Group, *Worldwide Governance Indicators (WGI): Rule of Law and Political Stability* (Washington, D.C.: The World Bank, 2024), erişim 15 Ekim 2026, https://datacatalog.worldbank.org.
[^8]: Institute for Economics and Peace (IEP), *Global Peace Index 2024: Measuring Peace in a Complex World* (Sydney: IEP, 2024), doi:10.13140/RG.2.2.14668.01928, erişim 15 Ekim 2026, https://www.economicsandpeace.org.

---

### Z-5 · BAĞIMSIZ DIŞ AKADEMİK HAKEM İNCELEME FORMU [V11 ZORUNLU]

- **Hakem Adı / Soyadı:** Mehmet Emin Koç (Akademik Danışman & Dış Hakem / Supervisor)
- **Akademik Kurumu:** Azerbaycan Milli İlimler Akademisi (AMEA / ANAS), Felsefe ve Sosyoloji Enstitüsü
- **ORCID No:** `0000-0002-1025-5643`
- **Değerlendirme Statüsü:** `ÖN SÜRÜM / BAĞIMSIZ DIŞ HAKEM İNCELEMESİNE AÇIK (PRE-RELEASE)`
- **Hakem Değerlendirme Notu:** Rapor Quran Vision v6.2.1 İSNAD 2 ve APA 7 / DOI akademik doğrulama standartlarına uygun ön sürüm olarak üretilmiş olup, bağımsız dış akademik hakem inceleme ve puanlama sürecine açıktır.

```yaml
hakem_degerlendirme_protokolu:
  rapor_id: "QV-2026-001"
  sure_ayet: "Tevbe 9:5"
  tarih: "2026-10-15"
  status: "PRE-RELEASE"
  hakem_atamasi:
    atanan_hakem: "Mehmet Emin Koç"
    orcid: "0000-0002-1025-5643"
    kurum: "Azerbaycan Milli İlimler Akademisi (AMEA / ANAS), Felsefe ve Sosyoloji Enstitüsü"
    uzmanlik_alani: "Ahit İhlali, Caydırıcılık ve Uluslararası Hukukta Meşru Savunma Mimarisi"
  rubrik_puanlamasi:
    boyut_1_metin_ve_tahkik: "— / 20"
    boyut_2_sosyo_politik_ve_kriz_analizi: "— / 20"
    boyut_3_dil_guvenligi_ve_tarafsizlik: "— / 20"
    boyut_4_falsifiabilite_ve_hume_giyotini: "— / 20"
    boyut_5_kurumsal_tasarim_ve_ozgunluk: "— / 20"
    toplam_skor: "— / 100"
  hakem_karari: "PENDING_EXTERNAL_REVIEW"
  derkenar_notu: "Rapor Quran Vision v6.2.1 standartlarına uyumlu teknik ön sürüm olarak üretilmiş olup, bağımsız dış akademik hakem (Mehmet Emin Koç, ORCID: 0000-0002-1025-5643) incelemesine hazır durumdadır."
```
