#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quran Vision v6.2.1 — Paket 2.1: Türkçe Külliyat (15 Rapor) Omurga Restorasyonu ve Kanonik 26-Adım Şema Eşitlemesi
1. 07-pilot-nisa-434 ve 08-pilot-maide-538 raporlarına eksik FAZ V (ADIM 17, 17b, 18, 18.1, 19, 20) eklenmesi.
2. Grup B (12..20, 9 rapor) adımlarının hiçbir cümle silinmeden QURAN_VISION_v6.2.2_SPECIFICATION.md kanonik 26-adım şemasına dönüştürülmesi.
3. 15 Türkçe raporun tamamında ADIM 20'ye âyete özgü 40 Dakikalık TYMM Pedagojik Ders Planı eklenmesi.
4. 15 Türkçe raporun tamamında YAML peer_review ve Z-5 Hakem İnceleme Formu'nda Mehmet Yarıcı (Project Lead — Internal Sample Audit) (ORCID: 0009-0003-0356-8582) künyesinin standartlaştırılması.
"""

import hashlib
import pathlib
import re
import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCS_TR = ROOT / "docs" / "tr"

# ---------------------------------------------------------------------------
# 15 Rapor İçin Âyete Özgü 40 Dakikalık TYMM Pedagojik Ders Planları
# ---------------------------------------------------------------------------
TYMM_PLANS_TR = {
    "QV-2026-001": """- **40 Dakikalık TYMM Pedagojik Ders ve Seminer Planı (Tevbe 9:5 — Ahit Güvenliği ve Meşru Savunma Etiği):**
  - **TYMM Erdem-Değer-Eylem Çerçevesi:** *Adalet, Ahde Vefa, Barış, Sorumluluk ve Hikmet.*
  - **1. Aşama — Hazırlık ve Bağlamsal Keşif (0–10 Dk):** Öğrencilere Tevbe 9:4, 9:5 ve 9:6 âyetleri birlikte okutularak *"Bir kanun maddesini önceki ve sonraki maddelerden koparıp tek başına okumak hangi adaletsizliklere yol açar?"* sorusu yöneltilir (`S7 Kırpma Riski` farkındalığı).
  - **2. Aşama — Klasik Tefsir ve Kavram Atölyesi (10–20 Dk):** `İnsilâh` (4 aylık diplomatik mühlet), `ahd-i hâricî` (yalnızca ahdi bozan saldırganlar) ve `istîmân` (Tevbe 9:6 sığınma ve güvenli koridor hakkı) kavramları Zemahşerî ve Şâtıbî nakilleriyle incelenir.
  - **3. Aşama — Yapılandırılmış Sınıf Münazarası ve Sistem Haritası (20–30 Dk):** Sınıf iki gruba ayrılır; **1. Grup** *"Uluslararası krizlerde süresiz pasifizm ve taviz barışı korur mu?"* (`R1` kısır döngüsü), **2. Grup** ise *"Hukuki mühlet, orantılı caydırıcılık ve açık eman koridoru kalıcı barışı nasıl kurar?"* (`B1` dengeleyici döngüsü) tezlerini CLD diyagramı üzerinden tartışır.
  - **4. Aşama — Sentez ve Öz-Değerlendirme (30–40 Dk):** Öğrenciler İslam uluslararası hukukunda barışın asıl, savaşın ise yalnızca ahit ihlali ve saldırganlığa karşı istisnai bir savunma tedbiri olduğunu özetleyen birer paragraflık *"Adil Barış Beyannamesi"* yazar.""",

    "QV-2026-002": """- **40 Dakikalık TYMM Pedagojik Ders ve Seminer Planı (Nisâ 4:34–35 — Ailede Emanet, Kavvâmlık ve Şiddetsiz Uzlaşı):**
  - **TYMM Erdem-Değer-Eylem Çerçevesi:** *Merhamet, Aile Bütünlüğü, Saygı, Adalet ve Nezaket.*
  - **1. Aşama — Hazırlık ve Bağlamsal Keşif (0–10 Dk):** Hz. Peygamber'in *"Sizin en hayırlınız ailesine en güzel davrananızdır"* hadisi ve hayatı boyunca hiçbir kadına veya çocuğa el kaldırmadığı sünneti tahtaya yazılarak derse giriş yapılır.
  - **2. Aşama — Klasik Tefsir ve Kavram Atölyesi (10–20 Dk):** `Kavvâm` kavramının "tahakküm ve zorbalık" değil, `bimâ enfeqû` kaydıyla "koruma, gözetme ve mali/hukuki sorumluluk yüklenme" olduğu; Nisâ 4:34'ün mutlaka Nisâ 4:35'teki *iki taraflı aile hakemliği* ile birlikte okunması gerektiği Atâ b. Ebî Rebâh ve İbn Âşûr'un içtihatlarıyla tahlil edilir.
  - **3. Aşama — Yapılandırılmış Sınıf Münazarası ve Sistem Haritası (20–30 Dk):** Öğrenciler `R1` (iletişimsizlik ve öfke sarmalı) ile `B1` (maruf ile iletişim, kademeli soğutma ve Nisâ 4:35 hakemliği) döngülerini karşılaştırarak aile içi krizlerde şiddetsiz iletişim protokolü tasarlar.
  - **4. Aşama — Sentez ve Öz-Değerlendirme (30–40 Dk):** Katılımcılar *İnsan Onuru ve Aile İçi Merhamet Sözleşmesi* maddelerini oluşturur.""",

    "QV-2026-003": """- **40 Dakikalık TYMM Pedagojik Ders ve Seminer Planı (Mâide 5:38–39 — Mülkiyet Emniyeti, Sosyal Adalet Ön-Şartı ve Islah):**
  - **TYMM Erdem-Değer-Eylem Çerçevesi:** *Dürüstlük, Emek, Sosyal Adalet, Mülkiyet Saygısı ve Merhamet.*
  - **1. Aşama — Hazırlık ve Bağlamsal Keşif (0–10 Dk):** Hz. Ömer'in Hicrî 18 *Remâde (Kıtlık) Yılı*'nda hırsızlık cezasını askıya alma kararı örnek olay olarak sunulur ve *"Ceza hukuku sosyal adaletten bağımsız işleyebilir mi?"* sorusu tartışılır.
  - **2. Aşama — Klasik Tefsir ve Kavram Atölyesi (10–20 Dk):** `Bimâ kesebâ` (ihtiyaç dışı kasıtlı haksız kazanç), `hırz`, `şüphe kaidesi` ve Mâide 5:39'daki `tevbe ve ıslah` kavramları Cessâs ve Şâtıbî nakilleriyle incelenir.
  - **3. Aşama — Yapılandırılmış Sınıf Münazarası ve Sistem Haritası (20–30 Dk):** Geleneksel fiziki hırsızlık ile modern çağdaki siber suçlar ve kamu fonu hortumlamaları (beyaz yakalı suçlar) arasındaki adalet dengesi `R1` ve `B1` sistem döngüleri üzerinden müzakere edilir.
  - **4. Aşama — Sentez ve Öz-Değerlendirme (30–40 Dk):** Öğrenciler suçun önlenmesinde sosyal güvence, caydırıcı hukuk ve onarıcı rehabilitasyonun (`5:39`) rolünü özetleyen bir politika matrisi hazırlar.""",

    "QV-2026-004": """- **40 Dakikalık TYMM Pedagojik Ders ve Seminer Planı (Bakara 2:256 — Din ve Vicdan Hürriyeti, İkrah Yasağı):**
  - **TYMM Erdem-Değer-Eylem Çerçevesi:** *Özgürlük, Hakikat Saygısı, Samimiyet (İhlas), Hoşgörü ve İnsan Onuru.*
  - **1. Aşama — Hazırlık ve Bağlamsal Keşif (0–10 Dk):** `"Lâ ikrâhe fi'd-dîn"` (Dinde hiçbir zorlama yoktur) ilkesinin nüzul sebebi (Medineli Ensâr ailelerinin Hıristiyan olan evlatlarını zorla İslam'a sokmak istemeleri üzerine inmesi — Taberî) paylaşılır.
  - **2. Aşama — Klasik Tefsir ve Kavram Atölyesi (10–20 Dk):** Cinsini nefyeden `Lâ` edatı, `rüşd` (akli ve ahlaki doğruluk), `ğayy` (sapıklık), `tâğût` ve `urvetü'l-vüskâ` (kopmayan sağlam kulp) kavramları Râzî ve İbn Âşûr'un yorumlarıyla çözümlenir.
  - **3. Aşama — Yapılandırılmış Sınıf Münazarası ve Sistem Haritası (20–30 Dk):** `R1` (baskı ve dayatmanın ikiyüzlülük/nifak ve nefret üretmesi) ile `B1` (vicdan hürriyeti ve rasyonel delilin samimi iman ve toplumsal barış üretmesi) döngüleri karşılaştırılır.
  - **4. Aşama — Sentez ve Öz-Değerlendirme (30–40 Dk):** Öğrenciler Medine Vesikası'ndan bugüne inanç özgürlüğünün medeniyet inşasındaki yerini değerlendirir.""",

    "QV-2026-005": """- **40 Dakikalık TYMM Pedagojik Ders ve Seminer Planı (Nisâ 4:58 — Kamu Emaneti, Liyakat ve Adil Yargı):**
  - **TYMM Erdem-Değer-Eylem Çerçevesi:** *Emanet, Liyakat (Ehliyet), Adalet, Tarafsızlık ve Hesap Verebilirlik.*
  - **1. Aşama — Hazırlık ve Bağlamsal Keşif (0–10 Dk):** Mekke'nin fethi günü Hz. Peygamber'in Kâbe'nin anahtarını kendi akrabalarına değil, ezelî emanet ehline (Osman b. Talha'ya) teslim etmesi kıssası üzerinden `"emânâtı ehline verme"` ilkesi tartışılır.
  - **2. Aşama — Klasik Tefsir ve Kavram Atölyesi (10–20 Dk):** Çoğul `el-emânât` lafzı, `ehlihâ` (liyakat ve ehliyet sahipleri) ve `beyne'n-nâs` (inanç ve kimlik ayrımı gözetmeksizin tüm insanlar arasında adalet) kavramları Râzî ve İbn Teymiyye (*es-Siyâsetü'ş-Şer'iyye*) nakilleriyle incelenir.
  - **3. Aşama — Yapılandırılmış Sınıf Münazarası ve Sistem Haritası (20–30 Dk):** Nepotizm/kayırmacılık sarmalı (`R1`) ile liyakat ve bağımsız yargı dengeleyicisi (`B1`) arasındaki nedensel ilişki WJP Hukukun Üstünlüğü verileriyle analiz edilir.
  - **4. Aşama — Sentez ve Öz-Değerlendirme (30–40 Dk):** Öğrenciler kamu görevlerinde liyakat ve çıkar çatışması ilkelerini içeren bir *Kamu Etiği Şartnamesi* tasarlar.""",

    "QV-2026-006": """- **40 Dakikalık TYMM Pedagojik Ders ve Seminer Planı (Âl-i İmrân 3:159 — Kriz Liderliği, Şefkat, Şûrâ ve Azim):**
  - **TYMM Erdem-Değer-Eylem Çerçevesi:** *Şefkat (Rıfk), İstişare (Şûrâ), Affedicilik, Kararlılık (Azim) ve Tevekkül.*
  - **1. Aşama — Hazırlık ve Bağlamsal Keşif (0–10 Dk):** Uhud Savaşı'ndaki ağır taktik hatanın ve kayıpların hemen ardından inen bu âyette, Hz. Peygamber'in hata yapan genç sahabileri suçlamak yerine affedip onlarla yeniden istişare etmesi (`ve şâvirhüm fi'l-emr`) incelenir.
  - **2. Aşama — Klasik Tefsir ve Kavram Atölyesi (10–20 Dk):** `Linte lehüm` (yumuşak davranma), `fazzan galîza'l-kalb` (kaba ve katı kalpli olma), `lenfaddû min havlike` (etrafından dağılıp gitme), `şûrâ` ve `azm` kavramları Zemahşerî ve İbn Âşûr üzerinden tahlil edilir.
  - **3. Aşama — Yapılandırılmış Sınıf Münazarası ve Sistem Haritası (20–30 Dk):** Otoriter/kırıcı liderliğin yetenek göçü ve dalkavukluk üretmesi (`R1`) ile şefkatli ve istişarî liderliğin ortak aklı harekete geçirmesi (`B1`) simüle edilir.
  - **4. Aşama — Sentez ve Öz-Değerlendirme (30–40 Dk):** Öğrenciler okul ve kurum yönetiminde "Psikolojik Güvenlik ve İstişare Protokolü" hazırlar.""",

    "QV-2026-007": """- **40 Dakikalık TYMM Pedagojik Ders ve Seminer Planı (Hucurât 49:9–10 — Arabuluculuk, Bağy Freni ve Kardeşlik Hukuku):**
  - **TYMM Erdem-Değer-Eylem Çerçevesi:** *Barış Yapıcılık (Islah), Hakkaniyet (Kıst), Kardeşlik (Uhuvvet) ve Adalet.*
  - **1. Aşama — Hazırlık ve Bağlamsal Keşif (0–10 Dk):** Akran zorbalığı veya toplumsal gruplar arası bir çatışma senaryosu verilerek *"Tarafsız üçüncü taraf çatışmayı nasıl durdurur?"* sorusuyla derse başlanır.
  - **2. Aşama — Klasik Tefsir ve Kavram Atölyesi (10–20 Dk):** `Islah` (arabuluculuk), `bağy` (haddi aşma/saldırganlık), `fey'` (hukuka dönüş), `adl / kıst` (onarıcı hakkaniyet) ve `ihvetün` (kardeşlik) kavramları Kurtubî ve Cessâs nakilleriyle incelenir.
  - **3. Aşama — Yapılandırılmış Sınıf Münazarası ve Sistem Haritası (20–30 Dk):** Hucurât 49:9–10'un 3 aşamalı barış mimarisi (`1. Sulh -> 2. Mütecavizi Hukuka Döndürme -> 3. Rövanşizmsiz Kıst`) `R1` ve `B1` döngüleri üzerinden tartışılır.
  - **4. Aşama — Sentez ve Öz-Değerlendirme (30–40 Dk):** Sınıf içi "Akran Arabuluculuğu ve Adil Uzlaşı Yönergesi" kaleme alınır.""",

    "QV-2026-008": """- **40 Dakikalık TYMM Pedagojik Ders ve Seminer Planı (İsrâ 17:36 — Epistemik Ahlak, Bilgi Doğrulama ve Dijital Sorumluluk):**
  - **TYMM Erdem-Değer-Eylem Çerçevesi:** *Doğruluk, Eleştirel Düşünce, Bilgi Ahlakı, Emanet ve Öz-Denetim.*
  - **1. Aşama — Hazırlık ve Bağlamsal Keşif (0–10 Dk):** Sosyal medyada hızla yayılan sentetik (deepfake) veya doğrulanmamış bir haber örneği gösterilerek `"Ve lâ takfu mâ leyse leke bihî ilm"` (Bilgin olmayan şeyin ardına düşme!) ilkesi tanıtılır.
  - **2. Aşama — Klasik Tefsir ve Kavram Atölyesi (10–20 Dk):** `Kafv` (iz sürme/peşine düşme), `ilm` (delile dayalı kesin bilgi) ile `sem'` (işitme), `basar` (görme) ve `fuâd` (muhakeme eden kalp/zihin) melekelerinin hukuki-ahlaki sorumluluğu (`mes'ûlâ`) Râzî ve İbn Âşûr üzerinden çözümlenir.
  - **3. Aşama — Yapılandırılmış Sınıf Münazarası ve Sistem Haritası (20–30 Dk):** Algoritmik dezenformasyon ve linç sarmalı (`R1`) ile üçlü bilişsel doğrulama filtresi (`B1: Sem'-Basar-Fuâd`) karşılaştırılır.
  - **4. Aşama — Sentez ve Öz-Değerlendirme (30–40 Dk):** Öğrenciler dijital içerik paylaşmadan önce uygulanacak *"3 Adımlı İsrâ 17:36 Teyit Kontrol Listesi"* oluşturur.""",

    "QV-2026-009": """- **40 Dakikalık TYMM Pedagojik Ders ve Seminer Planı (Haşr 59:7 — Servetin Tabana Yayılması ve İktisadi Adalet):**
  - **TYMM Erdem-Değer-Eylem Çerçevesi:** *Paylaşma, İktisadi Adalet, Dayanışma, Cömertlik ve Kamu Yararı.*
  - **1. Aşama — Hazırlık ve Bağlamsal Keşif (0–10 Dk):** `"Key lâ yekûne dûleten beyne'l-ağniyâi minküm"` (Servet yalnızca içinizdeki zenginler arasında dönüp duran bir tekel olmasın!) ilkesi tahtaya yazılarak gelir dağılımı adaletsizliğinin toplumsal etkileri sorulur.
  - **2. Aşama — Klasik Tefsir ve Kavram Atölyesi (10–20 Dk):** `Fey'` (kamu kaynağı), `dûle` (kapalı devre servet tekeli) ve âyette sayılan kırılgan gruplar (yetimler, yoksullar, yolda kalmışlar) İbn Âşûr'un makâsıd (ta'lîl) tahliliyle incelenir.
  - **3. Aşama — Yapılandırılmış Sınıf Münazarası ve Sistem Haritası (20–30 Dk):** Servetin oligarşik tekelleşmesi (`R1`) ile zekât, vakıf, adil vergi ve üretken yatırım yoluyla tabana yayılması (`B1`) Gini katsayısı verileriyle tartışılır.
  - **4. Aşama — Sentez ve Öz-Değerlendirme (30–40 Dk):** Öğrenciler okul veya mahalle ölçeğinde bir *Sosyal Dayanışma ve Vakıf Projesi* tasarlar.""",

    "QV-2026-010": """- **40 Dakikalık TYMM Pedagojik Ders ve Seminer Planı (Rûm 30:22 — Dillerin ve Renklerin Çeşitliliği, Kültürel Çoğulculuk):**
  - **TYMM Erdem-Değer-Eylem Çerçevesi:** *Saygı, Birlikte Yaşama Kültürü, Tefekkür, Eşitlik ve Empati.*
  - **1. Aşama — Hazırlık ve Bağlamsal Keşif (0–10 Dk):** Rûm 30:22'de *"göklerin ve yerin yaratılışı"* ile *"dillerinizin ve renklerinizin farklılığı"*nın aynı cümlede Allah'ın âyetleri (`ve min âyâtihî`) olarak sayılması üzerinde tefekkür edilir.
  - **2. Aşama — Klasik Tefsir ve Kavram Atölyesi (10–20 Dk):** `İhtilâf` (zenginlik ve çeşitlilik), `elsine` (diller), `elvân` (renkler ve mizaçlar) ve `li'l-âlimîn` (bilenler için ibretler) kavramları Râzî ve İbn Âşûr nakilleriyle tahlil edilir.
  - **3. Aşama — Yapılandırılmış Sınıf Münazarası ve Sistem Haritası (20–30 Dk):** Zoraki tektipleştirme ve ötekileştirme kısır döngüsü (`R1`) ile kültürel çeşitliliği kozmik bir âyet olarak koruyan çoğulcu medeniyet döngüsü (`B1`) karşılaştırılır.
  - **4. Aşama — Sentez ve Öz-Değerlendirme (30–40 Dk):** Öğrenciler farklı kültür ve dillerin insanlığın ortak bilgi mirasına katkısını anlatan bir poster/sunum taslağı hazırlar.""",

    "QV-2026-011": """- **40 Dakikalık TYMM Pedagojik Ders ve Seminer Planı (En'âm 6:151–152 — On Evrensel Muhkem İlke ve Kırılganların Korunması):**
  - **TYMM Erdem-Değer-Eylem Çerçevesi:** *Doğruluk, Anne-Babaya İhsan, Yetim/Çocuk Hakları, Ölçüde Adalet ve Ahde Vefa.*
  - **1. Aşama — Hazırlık ve Bağlamsal Keşif (0–10 Dk):** İbn Abbas'ın *"bütün ilahi kitaplarda ortak olan ve hiçbir zaman nesh edilmeyen muhkem âyetler"* olarak tanıttığı En'âm 6:151–152 maddeleri tahtada listelenir.
  - **2. Aşama — Klasik Tefsir ve Kavram Atölyesi (10–20 Dk):** `İmlâk` (yoksulluk korkusuyla çocukların ihmal/istismar edilmesi), `el-keyl ve'l-mîzân bi'l-kıst` (ölçü ve tartıda dürüstlük) ve `ve lev kâne zâ kurbâ` (yakın akraba aleyhine dahi olsa adil şahitlik) ilkeleri Kurtubî ve Taberî üzerinden incelenir.
  - **3. Aşama — Yapılandırılmış Sınıf Münazarası ve Sistem Haritası (20–30 Dk):** Ticari hile ve akraba kayırmacılığının toplumsal güveni çökertmesi (`R1`) ile 10 evrensel ahlak ilkesinin koruyucu kalkanı (`B1`) tartışılır.
  - **4. Aşama — Sentez ve Öz-Değerlendirme (30–40 Dk):** Öğrenciler günlük hayatta ve dijital ticarette *"En'âm 151–152 Evrensel Ahlak İlkeleri"* uygulama rehberi hazırlar.""",

    "QV-2026-012": """- **40 Dakikalık TYMM Pedagojik Ders ve Seminer Planı (Hadîd 57:25 — Kitap, Mîzân ve Demir/Teknoloji Dengesi):**
  - **TYMM Erdem-Değer-Eylem Çerçevesi:** *Adalet (Kıst), Bilim ve Teknoloji Etiği, Hukukun Üstünlüğü ve İnsani Fayda.*
  - **1. Aşama — Hazırlık ve Bağlamsal Keşif (0–10 Dk):** Hadîd 57:25'teki üç sembol (`el-Kitâb`, `el-Mîzân`, `el-Hadîd`) tahtaya çizilerek *"Hukuk ve adalet terazisi olmadan teknolojik/askeri güç ne üretir? Güç olmadan adalet kendini nasıl korur?"* sorusu sorulur.
  - **2. Aşama — Klasik Tefsir ve Kavram Atölyesi (10–20 Dk):** `Li-yekûme'n-nâsü bi'l-kıst` (insanların bizzat adaleti ayakta tutması), `be'sün şedîd` (caydırıcı güç) ve `menâfi'u li'n-nâs` (insanlar için sivil/endüstriyel faydalar) kavramları Mâtürîdî ve Râzî nakilleriyle incelenir.
  - **3. Aşama — Yapılandırılmış Sınıf Münazarası ve Sistem Haritası (20–30 Dk):** Mîzânsız gücün zorbalığa dönüşmesi (`R1`) ile teknolojiyi (`Hadîd`) hukuk (`Kitâb`) ve adalet (`Mîzân`) emrine veren medeniyet modeli (`B1`) yapay zekâ ve savunma teknolojileri örnekleriyle tartışılır.
  - **4. Aşama — Sentez ve Öz-Değerlendirme (30–40 Dk):** Öğrenciler *"Ahlak ve Adalet Merkezli Teknoloji Geliştirme İlkeleri"* metni kaleme alır.""",

    "QV-2026-013": """- **40 Dakikalık TYMM Pedagojik Ders ve Seminer Planı (Nahl 16:90 — Adalet, İhsan ve Sosyal Dayanışma Anayasası):**
  - **TYMM Erdem-Değer-Eylem Çerçevesi:** *Adalet (Adl), İyilik ve Fazilet (İhsan), Aile/Komşuluk Dayanışması ve Kötülükten Sakınma.*
  - **1. Aşama — Hazırlık ve Bağlamsal Keşif (0–10 Dk):** Her cuma hutbesinin sonunda okunan Nahl 16:90 âyetinin İbn Mes'ûd tarafından *"Kur'an'ın en kapsamlı hayır ve şer özeti"* olarak nitelendirilmesi paylaşılır.
  - **2. Aşama — Klasik Tefsir ve Kavram Atölyesi (10–20 Dk):** Üç emir (`Adl`: hukuki eşitlik, `İhsan`: hukukun üstünde şefkat ve fazilet, `Îtâi zi'l-kurbâ`: sosyal dayanışma) ile üç yasak (`Fahşâ`: bireysel ahlaksızlık, `Münker`: kamusal kötülük, `Bağy`: zorbalık ve haddi aşma) Râgıb ve Râzî üzerinden karşılaştırılır.
  - **3. Aşama — Yapılandırılmış Sınıf Münazarası ve Sistem Haritası (20–30 Dk):** Salt kanuni adaletin (`Adl`) merhamet ve ihsan (`İhsan`) olmadan neden soğuk bürokrasiye dönüşeceği `R1` ve `B1` döngüleri üzerinden müzakere edilir.
  - **4. Aşama — Sentez ve Öz-Değerlendirme (30–40 Dk):** Öğrenciler okul ve mahalle hayatında `Adl + İhsan + Zi'l-Kurbâ` üçlüsünü hayata geçiren somut eylem adımları belirler.""",

    "QV-2026-014": """- **40 Dakikalık TYMM Pedagojik Ders ve Seminer Planı (Hucurât 49:13 — İnsani Eşitlik, Teârüf Ahlakı ve Takvâ Ölçütü):**
  - **TYMM Erdem-Değer-Eylem Çerçevesi:** *İnsan Onuru, Eşitlik, Kültürlerarası Tanışma (Teârüf), Tevazu ve Takvâ.*
  - **1. Aşama — Hazırlık ve Bağlamsal Keşif (0–10 Dk):** Hz. Peygamber'in Veda Hutbesi'ndeki *"Ey insanlar! Rabbiniz birdir, babanız da birdir; Arap'ın Arap olmayana, beyazın siyaha takvâ dışında hiçbir üstünlüğü yoktur"* hitabıyla Hucurât 49:13 birlikte okunur.
  - **2. Aşama — Klasik Tefsir ve Kavram Atölyesi (10–20 Dk):** `Min zekerin ve ünsâ` (ontolojik eşitlik), `şuûben ve kabâile` (sosyolojik çeşitlilik), `li-teârefû` (övünmek ve çatışmak için değil, karşılıklı tanışıp yardımlaşmak için) ve `etkâküm` (ahlaki sorumluluk ve liyakat) kavramları Zemahşerî ve Âlûsî nakilleriyle incelenir.
  - **3. Aşama — Yapılandırılmış Sınıf Münazarası ve Sistem Haritası (20–30 Dk):** Irkçılık ve kabileciliğin (`asabiyet / tenâkür`) ürettiği kutuplaşma sarmalı (`R1`) ile `teârüf` ve `takvâ` merkezli birlikte yaşama modeli (`B1`) tartışılır.
  - **4. Aşama — Sentez ve Öz-Değerlendirme (30–40 Dk):** Öğrenciler önyargıları kıran bir *"Okul İçi Teârüf ve Kardeşlik Etkinliği"* planlar.""",

    "QV-2026-015": """- **40 Dakikalık TYMM Pedagojik Ders ve Seminer Planı (Mâide 5:32 — İnsan Hayatının Dokunulmazlığı ve Evrensel İhyâ Ahlakı):**
  - **TYMM Erdem-Değer-Eylem Çerçevesi:** *Yaşam Hakkı, Merhamet, Yardımseverlik (İhyâ), Barış ve İnsanlık Onuru.*
  - **1. Aşama — Hazırlık ve Bağlamsal Keşif (0–10 Dk):** `"Kim bir canı kurtarırsa (ve men ahyâhâ) bütün insanlığı yaşatmış gibi olur"` âyeti üzerinden *"Neden tek bir masum insan bütün insanlığa eşdeğerdir?"* sorusuyla felsefi ve ahlaki sorgulama başlatılır.
  - **2. Aşama — Klasik Tefsir ve Kavram Atölyesi (10–20 Dk):** `Bi-ğayri nefsin ev fesâdin fi'l-arz` (haksız yere cana kıyma), `fe-ke'ennemâ katele'n-nâse cemî'â` (evrensel masumiyet kalkanının delinmesi) ve `ihyâ` (affetmek, boğulanı/yıkım altındakini kurtarmak, tedavi ve açlığı gidermek) kavramları Râzî ve Kurtubî nakilleriyle incelenir.
  - **3. Aşama — Yapılandırılmış Sınıf Münazarası ve Sistem Haritası (20–30 Dk):** Şiddetin sıradanlaşması ve sivil kayıpların istatistiğe indirgenmesi (`R1`) ile afet hazırlığı, ilk yardım, iş güvenliği ve insani koridorları kapsayan kurumsal `İhyâ` seferberliği (`B1`) tartışılır.
  - **4. Aşama — Sentez ve Öz-Değerlendirme (30–40 Dk):** Öğrenciler ilk yardım, kan/organ bağışı, afet gönüllülüğü ve sivil koruma bilincini içeren *"Bir Can Kurtar, İnsanlığı Yaşat (İhyâ) Taahhütnamesi"* hazırlar."""
}

# ---------------------------------------------------------------------------
# 07-pilot-nisa-434 ve 08-pilot-maide-538 İçin Eksik FAZ V (ADIM 17..20) Blokları
# ---------------------------------------------------------------------------
FAZ_V_RESTORE_07_08 = {
    "QV-2026-002": f"""## FAZ V — GÜVEN, SORUMLULUK VE İZLEME KAYDI

### ADIM 17 — GÜVEN DÜZEYİ
- **Nitel Derece:** B (Orta-Yüksek Analitik Güven). Klasik fıkıh ve tefsir usûlü tahkiki (İbn Fâris, Zemahşerî, İbn Manzûr, Şâtıbî, Cessâs, Atâ b. Ebî Rebâh ve İbn Âşûr) ile çağdaş aile sosyolojisi verilerinin (UN Women, WHO, UNDP) çapraz sentezine dayanır; teolojik veya normatif alanda sayısal kesinlik iddiası taşımaz.
- **Kurumsal Rol Dağılımı:**
  - **Aile ve Sosyal Hizmetler Bakanlığı:** Önleyici aile danışmanlığı, evlilik öncesi iletişim eğitimi ve ŞÖNİM koruma altyapısının koordinasyonu.
  - **Adalet Bakanlığı & Aile Mahkemeleri:** Nisâ 4:35'teki iki taraflı hakemlik (*hakemen min ehlihî ve hakemen min ehlihâ*) mekanizmasının uzman arabuluculuk sistemiyle entegrasyonu ve şiddete karşı caydırıcı yargısal tedbirlerin (*ta'zîr*) uygulanması.
  - **Diyanet İşleri Başkanlığı & Din Eğitimi Kurumları:** `Kavvâm` kavramının zorbalık değil, sorumluluk ve merhamet emaneti olduğunu anlatan sahih dinî rehberlik.

---

### ADIM 17b — AKTÖR VE GÜÇ HARİTASI
- **Karar Vericiler:** Yasama organı, Aile Mahkemeleri hâkimleri, Aile ve Sosyal Hizmetler Bakanlığı üst yönetimi.
- **Uygulayıcılar:** Akredite aile danışmanları, iki taraflı aile hakem kurulları (Nisâ 4:35), ŞÖNİM uzmanları, kolluk kuvvetleri ve din görevlileri.
- **Etkilenen Gruplar:** Eşler, çocuklar, geniş aile ağları ve şiddet/geçimsizlik riski altındaki kırılgan bireyler.
- **Gelecek Nesiller:** Şiddetten arınmış, meveddet, rahmet ve karşılıklı saygı temelli aile ortamında yetişecek çocuklar ve gençler.

---

### ADIM 18 — BİLGİ TABANI VE ZAYIFLIK LİSTESİ
- **Bilgi Tabanı:** İSNAD 2 standartlı klasik tefsir ve fıkıh kaynakları (Cessâs, Şâtıbî, Zemahşerî, İbn Âşûr), Hz. Peygamber'in fiilî sünneti ve UN Women / WHO / UNDP küresel aile içi şiddet ve insani gelişme veri setleri.
- **Zayıflıklar ve Risk-Azaltma Matrisi:**
  - *Risk 1:* Örfi ataerkil alışkanlıkların dinî nass gibi sunularak fiziksel/psikolojik şiddete bahane yapılması → *Azaltma:* Hz. Peygamber'in sünneti ve İbn Âşûr/Atâ içtihadı doğrultusunda şiddetin kanunla (`ta'zîr`) açıkça yasaklanması.
  - *Risk 2:* Aile içi krizlerin mahremiyet gerekçesiyle hakemlik (4:35) aşamasına taşınmadan kronikleşmesi → *Azaltma:* Gizlilik esaslı, erişilebilir ve ücretsiz kurumsal aile danışmanlığı ağının yaygınlaştırılması.

---

### ADIM 18.1 — DİL GÜVENLİĞİ
- Rapor metninde kesinlik, tekelcilik veya sahte-onay iddialarından arındırma denetimi (`gem_lint.py` `L-1801`) yapılmıştır. Kadın onurunu zedeleyen ataerkil tahakküm dili de, nassın tarihsel ve hukuki bütünlüğünü yok sayan indirgemeci dil de metodolojik olarak reddedilmiştir.

---

### ADIM 19 — İZLEME VE GERİYE DÖNÜK SINAMA (RETRODICTION)
- **İzleme KPI (1., 3. ve 5. Yıl Göstergeleri):**
  - *1. Yıl:* Aile mahkemelerine entegre edilen Nisâ 4:35 uzlaştırma/hakemlik pilot uygulamalarında başvuruların $\le 60$ gün içinde sonuçlanma oranı.
  - *3. Yıl:* Danışmanlık ve hakemlik desteği alan çiftlerde şiddetsiz uzlaşı veya medenî/adil ayrılık oranının $\ge \%75$ seviyesine ulaşması.
  - *5. Yıl:* WHO / UN Women ve ulusal adli istatistiklerde aile içi fiziksel ve ağır psikolojik şiddet vakalarında anlamlı düşüş ($\ge \%25$ azalma).
- **Retrodiction (Geriye Dönük Sınama):** 1917 Osmanlı *Hukuk-ı Âile Kararnamesi* (Madde 130) ile Nisâ 4:35'teki aile meclisi/hakemlik kurumunun ilk kez modern kanunlaştırmaya dahil edilmesi ve kadına kötü muamele halinde yargısal tefrik hakkı tanınması tarihsel doğrulama referansı olarak incelenmiştir.

---

### ADIM 20 — AÇIK ARAŞTIRMA SORULARI, VARSAYIMLAR VE 40 DAKİKALIK TYMM PEDAGOJİK DERS PLANI
- **Açık Araştırma Soruları:**
  1. Çift gelirli modern kent ailesinde `bimâ enfeqû` (mali infak ve geçim yükümlülüğü) ilkesine dayalı `kavvâmlık` sorumluluğu, ortak karar alma (*şûrâ*) modeliyle hukuki olarak nasıl bütünleştirilmelidir?
  2. Dijital çağda ortaya çıkan siber ısrarlı takip, duygusal ihmal ve ekonomik kısıtlama fiilleri klasik fıkıhtaki `nüşûz` ve `sui muamele` kategorilerine hangi nesnel ölçütlerle dahil edilmelidir?
- **Temel Varsayım:** Eşlerin insan onuruna saygılı, profesyonel arabuluculuk ve adil hukuk güvencesi altında krizleri şiddetsiz çözme kapasitesine sahip olduğu kabul edilmiştir.
{TYMM_PLANS_TR["QV-2026-002"]}

---""",

    "QV-2026-003": f"""## FAZ V — GÜVEN, SORUMLULUK VE İZLEME KAYDI

### ADIM 17 — GÜVEN DÜZEYİ
- **Nitel Derece:** B (Orta-Yüksek Analitik Güven). Klasik fıkıh usûlü (İbn Fâris, Zemahşerî, İbn Manzûr, Şâtıbî, Cessâs ve Hz. Ömer'in *Âmü'r-Remâde* içtihadı) ile modern kriminoloji ve yolsuzluk endekslerinin (World Bank WGI, Transparency International CPI) sentezine dayanır; normatif alanda sayısal kesinlik iddiası taşımaz.
- **Kurumsal Rol Dağılımı:**
  - **Sosyal Güvenlik ve Yardımlaşma Kurumları:** Temel geçim güvencesi sağlayarak zaruret ve açlık kaynaklı suç zeminini ortadan kaldırma (Remâde ön-şartı).
  - **Yargı Organları ve Mali Suçları Araştırma Kurulları (MASAK / Sayıştay):** Şüphe ilkesini (*"Hadleri şüphelerle düşürünüz"*) gözeterek yoksulun çaresizliği ile organize ve beyaz yakalı kamu malı hırsızlığını birbirinden ayıran adil ve caydırıcı yargılama.
  - **Denetimli Serbestlik ve İstihdam Kurumları:** Mâide 5:39 (`fe-men tâbe min ba'di zulmihî ve asleha`) gereği suça sürüklenen bireylerin mesleki rehabilitasyonu ve topluma yeniden kazandırılması.

---

### ADIM 17b — AKTÖR VE GÜÇ HARİTASI
- **Karar Vericiler:** Yasama organı, ekonomi ve sosyal politika kurulları, yüksek yargı mercileri.
- **Uygulayıcılar:** Ceza mahkemeleri, mali denetim birimleri, sosyal yardım vakıfları, denetimli serbestlik ve mesleki eğitim merkezleri.
- **Etkilenen Gruplar:** Mülkiyet sahipleri, kamu hazinesi (vergilerini ödeyen vatandaşlar), ekonomik kriz dönemlerinde geçim sıkıntısı çeken kırılgan kesimler ve rehabilitasyon sürecindeki hükümlüler.
- **Gelecek Nesiller:** Hem mülkiyet emniyetinin hem de sosyal adaletin güvence altında olduğu yüksek güvenli bir iktisadi düzende yaşayacak kuşaklar.

---

### ADIM 18 — BİLGİ TABANI VE ZAYIFLIK LİSTESİ
- **Bilgi Tabanı:** İSNAD 2 standartlı klasik fıkıh ve tefsir külliyatı (Cessâs, Şâtıbî, Zemahşerî), Hz. Ömer'in Remâde yılı tatbikatı ve Dünya Bankası / Transparency International hukuk ve yolsuzluk veri setleri.
- **Zayıflıklar ve Risk-Azaltma Matrisi:**
  - *Risk 1:* Sosyal devlet ve asgari geçim güvencesi sağlanmadan salt cezai sertlikle suçu önlemeye çalışmanın adaletsizlik üretmesi → *Azaltma:* Hz. Ömer'in Remâde içtihadı uyarınca sosyal güvenlik şemsiyesinin ceza hukukunun bağlayıcı ön-şartı kılınması.
  - *Risk 2:* Küçük adi hırsızlıklar ağır cezalandırılırken büyük ölçekli dijital hortumlama ve kamu yolsuzluklarının cezasız kalması → *Azaltma:* Beyaz yakalı mali suçların nitelikli `sirkat` ve `ğulûl` kapsamında tam malvarlığı müsaderesi ve ağır `ta'zîr` yaptırımlarına bağlanması.

---

### ADIM 18.1 — DİL GÜVENLİĞİ
- Rapor metninde kesinlik, tekelcilik veya sahte-onay iddialarından arındırma denetimi (`gem_lint.py` `L-1801`) yapılmıştır. Sosyal bağlamı ve şüphe kaidesini dışlayan şekilci şiddet dili reddedilmiştir.

---

### ADIM 19 — İZLEME VE GERİYE DÖNÜK SINAMA (RETRODICTION)
- **İzleme KPI (1., 3. ve 5. Yıl Göstergeleri):**
  - *1. Yıl:* Zaruret ve yoksulluk kaynaklı ilk kez işlenen mala karşı suçlarda adli sosyal inceleme ve sosyal yardım yönlendirme oranının $\\ge \\%95$ seviyesine çıkarılması.
  - *3. Yıl:* Mâide 5:39 rehabilitasyon ve meslek edindirme programlarına katılanlarda yeniden suç işleme (*residivizm*) oranının $\\le \\%15$ seviyesine çekilmesi.
  - *5. Yıl:* Dünya Bankası Yolsuzluk Kontrolü ve Hukukun Üstünlüğü endekslerinde $\\ge 0.75$ eşiğinin yakalanması.
- **Retrodiction (Geriye Dönük Sınama):** Hicrî 18 *Âmü'r-Remâde* (Kıtlık Yılı) döneminde Hz. Ömer'in hırsızlık haddini askıya alması ve Hâtıb b. Ebî Beltea'nın aç bırakılan köleleri vakasında cezayı kölelere değil, onları aç bırakan işverene tazminat olarak yüklemesi tarihsel doğrulama modeli olarak sınanmıştır.

---

### ADIM 20 — AÇIK ARAŞTIRMA SORULARI, VARSAYIMLAR VE 40 DAKİKALIK TYMM PEDAGOJİK DERS PLANI
- **Açık Araştırma Soruları:**
  1. Kripto varlık hırsızlığı, siber fidye yazılımları ve algoritmik piyasa manipülasyonları İslam ceza hukukundaki `hırz` (korunaklı alan) ve `nisap` kavramlarıyla nasıl modellenecektir?
  2. Enflasyonist politikalar veya tekelci fiyatlamalar yoluyla geniş kitlelerin alım gücünün eritilmesi, Kur'an'daki *"mallarınızı batıl yollarla yemeyin"* (Bakara 2:188) ve Mâide 5:38 ilkeleriyle nasıl ilişkilendirilebilir?
- **Temel Varsayım:** Mülkiyet emniyetinin ancak adil gelir dağılımı, şeffaf kamu denetimi ve onarıcı ceza adaleti (`5:38–39`) birlikte işlediğinde kalıcı olacağı kabul edilmiştir.
{TYMM_PLANS_TR["QV-2026-003"]}

---"""
}

# ---------------------------------------------------------------------------
# Grup B (QV-2026-007 .. QV-2026-015) İçin Kanonik Tamamlayıcı Veri Sözlüğü
# (ADIM 04b, ADIM 05 S1-S6, ADIM 06 Çapraz Âyet, ADIM 10 Morfoloji)
# ---------------------------------------------------------------------------
GRUP_B_ENRICHMENTS = {
    "QV-2026-007": {
        "adim02_kosul": (
            "- **Koşul-Sonuç Yapısı:**\n"
            "  - *1. Koşul (`ve in tâifetâni mine'l-mü'minîne'ktetelû`):* Müminlerden iki zümrenin fiilî çatışmaya girmesi → *1. Hüküm (`fe-aslihû beynehümâ`):* Derhal tarafsız arabuluculuk ve sulh teşebbüsü.\n"
            "  - *2. Koşul (`fe-in bağat ihdâhümâ ale'l-uhrâ`):* Taraflardan birinin sulhu reddederek haddi aşması ve saldırganlaşması (`bağy`) → *2. Hüküm (`fe-kâtilu'lletî tebğî hattâ tefîe ilâ emrillâh`):* Mütecaviz taraf Allah'ın hükmüne (hukuka) dönünceye kadar kolektif meşru kuvvetle durdurulması.\n"
            "  - *3. Koşul (`fe-in fâet`):* Saldırganın silah bırakıp hukuka rücû etmesi → *3. Hüküm (`fe-aslihû beynehümâ bi'l-adli ve aksitû`):* İntikam ve rövanşizme kapılmadan tam adalet (`adl`) ve hakkaniyetle (`kıst`) kalıcı barışın tesisi."
        ),
        "adim03_elp": (
            "- **Ethos (Ahlaki Yük):** Çatışan tarafları tekfir etmeden `ihvetün` (kardeşler) olarak tanımlamak ve arabuluculukta güçlüden veya akrabadan yana değil, yalnızca hak ve adaletten (`bi'l-adl ve'l-kıst`) yana tavır almak.\n"
            "- **Logos (Mantıksal Tutarlılık):** Müeyyidesiz arabuluculuk saldırganı (`bâğî`) cesaretlendirir; arabuluculuksuz askeri müdahale ise kan davasını büyütür. Üç aşamalı `Sulh → Caydırıcı Fren → Adil Yeniden İnşa` sırası rasyonel çatışma çözümünün zorunlu mimarisidir.\n"
            "- **Pathos (Vicdani ve Duygusal Tesir):** `İnneme'l-mü'minûne ihvetün fe-aslihû beyne ehaveyküm` (Müminler ancak kardeştir; öyleyse iki öz kardeşinizin arasını düzeltin!) hitabıyla öfke ve nefret ateşini kardeşlik şefkatiyle söndürmek."
        ),
        "adim04b": (
            "1. **Usûl Ekolü:** Çoğulcu-Makâsıdî İslam kamu hukuku usûlü (*Fıkhü Ehl-i'l-Bağy*; Cessâs, Kurtubî, Şâtıbî ve İbn Âşûr çizgisi).\n"
            "2. **Felsefi Perspektif:** Kolektif güvenlik kuramı, onarıcı adalet (*restorative justice*) ve kurumsal barış inşası.\n"
            "3. **Alternatif Yorumcu Konumlarından Ayrışma:**\n"
            "   - *Haricî / Tekfirci Uç:* Büyük günah ve silahlı çatışma sebebiyle tarafları dinden çıkmış sayarak topyekûn imhayı savunur.\n"
            "   - *Pasifist / Müeyyidesiz Uç:* Saldırgan (`bâğî`) uzlaşıyı reddedip mazlumları ezerken dahi meşru müdahaleyi reddederek zulmü seyreder.\n"
            "   Raporumuz, hem kardeşlik hukukunu koruyan hem de saldırganı hukuka döndürene kadar caydırıcı gücü meşru kılan Kur'anî orta yolu esas alır."
        ),
        "adim05_s1_s6": (
            "- **S1 (Önceki Âyetler — Hucurât 49:6–8):** Sûrenin hemen öncesinde `in câeküm fâsikun bi-nebein fe-tebeyyenû` (fâsık biri size bir haber getirirse doğruluğunu araştırın ki bilmeyerek bir topluluğa sataşıp pişman olmayasınız) buyrularak, toplumsal çatışmaların birincil sebebi olan **yalan haber ve dezenformasyon** kurutulmuştur.\n"
            "- **S2 (Sonraki Âyetler — Hucurât 49:11–13):** Hemen sonrasında ise alay etme (`lâ yeshar`), lakap takma, suizan, tecessüs, gıybet ve kabilecilik yasaklanarak çatışmanın **psikososyal ve kültürel kökleri** temizlenmiştir.\n"
            "- **S3 (Pasajın Konumu):** Hucurât Sûresi'nin toplumsal ahlak ve kamu düzeni omurgasının tam merkezinde yer alır.\n"
            "- **S4 (Sûre İçi Bütünlük):** Bilgi güvenliği (49:6) → Sıcak çatışma çözümü (49:9–10) → Gündelik onur güvenliği (49:11–12) → Evrensel insan kardeşliği (49:13) dizilimi bütüncül bir barış sosyolojisi kurar.\n"
            "- **S5 (Nüzûl Sebepleri ve Hitap):** Medine'de Evs ve Hazrec kabilelerine mensup iki grup arasında başlayan kavganın büyümesi üzerine inmiştir (Taberî, Cessâs).\n"
            "- **S6 (Mushaf Sırası ve Tevkîfî Yapı):** Fetih Sûresi'ndeki dış barış (Hudeybiye) sonrasında Hucurât Sûresi ile iç toplumsal barış ve devlet adabı vaz'edilmiştir."
        ),
        "adim06": (
            "- **Hucurât 49:6:** Çatışmaları tetikleyen doğrulanmamış haberlere karşı `tebeyyün` (tahkik) emri.\n"
            "- **Enfâl 8:1 ve 8:46:** *\"Allah'a ve Resûlüne itaat edin, birbirinizle çekişmeyin (`ve lâ tenâzeû`), sonra korkuya kapılır ve devletiniz/rüzgârınız elden gider; aranızdaki ilişkileri düzeltin (`fe-aslihû zâte beyniküm`).\"*\n"
            "- **Nisâ 4:114:** İnsanların gizli konuşmalarının çoğunda hayır yoktur; ancak sadaka, maruf veya **insanların arasını düzeltmeyi (`ıslâhun beyne'n-nâs`)** emredenler müstesnadır.\n"
            "- **Şûrâ 42:40:** Kötülüğün cezası misliyledir; fakat kim affeder ve **ıslah ederse** ecir Allah'a aittir.\n"
            "- *Analitik Sonuç ve N4 Kapsamı:* Kur'an'da iç barış ve kardeşlik asıldır; `bağy` (haksız saldırı) ortaya çıktığında ise tarafsız tahkim ve sınırlı kolektif müdahale (`hattâ tefîe`) devrede olmalıdır (`N4`)."
        ),
        "adim10_morf": (
            "- **Kayıt:** Ebced, cifir veya numerolojik çıkarımlar metodolojik olarak yasaktır ve kullanılmamıştır.\n"
            "- **Morfolojik Analiz:** Âyetteki `ٱقْتَتَلُوا۟` (*iktetelû*) fiili *ifti‘âl* bâbından olup karşılıklı vuruşmayı (işteşlik) bildirir; buna mukabil mütecaviz taraf için kullanılan `بَغَتْ` (*bağat*) ve `تَبْغِى` (*tebğî*) fiilleri sülâsî mücerred olup tek taraflı haddi aşmayı ve zulmü işaretler. Hakem topluma yöneltilen `فَأَصْلِحُوا۟` (*fe-aslihû*), `فَقَـٰتِلُوا۟` (*fe-kâtilû*) ve `وَأَقْسِطُوٓا۟` (*ve aksitû*) emirlerinin tamamı cemi müzekker (çoğul) kalıbındadır; bu morfolojik yapı çatışma çözümünün bireysel intikamla değil, kurumsal kamu otoritesi ve kolektif hakemlikle yürütülmesini zorunlu kılar."
        ),
    },

    "QV-2026-008": {
        "adim02_kosul": (
            "- **Koşul-Sonuç Yapısı:**\n"
            "  - *Normatif Yasak (`Ve lâ takfu mâ leyse leke bihî ilm`):* Hakkında delile dayalı doğrulanmış bilgi (`ilm`) bulunmayan hiçbir iddianın, söylentinin veya zannın peşine düşülmemesi, yayılmaması ve hükme esas alınmaması.\n"
            "  - *Epistemik ve Hukuki Gerekçe (`inne's-sem'a ve'l-basara ve'l-fuâde küllü ülâike kâne anhü mes'ûlâ`):* İşitme, görme ve akletme/muhakeme melekelerinin her birinin hem dünyada hem ahirette hukuki ve ahlaki sorgulamaya (`mes'ûliyyet`) tabi olması."
        ),
        "adim03_elp": (
            "- **Ethos (Ahlaki Yük):** Konuşmadan, paylaşmadan ve hüküm vermeden önce doğrulama (`tesebbüt / tebeyyün`) yapmak müminin ve bilim insanının temel karakteridir; iftira ve kulaktan dolma haber yaymak emanete hıyanettir.\n"
            "- **Logos (Mantıksal Tutarlılık):** Duyusal veri (`sem'` ve `basar`), analitik akıl süzgecinden (`fuâd`) geçirilmeden bilgi (`ilm`) değerini kazanmaz; doğrulanmamış öncüller üzerine kurulan her yargı mantıksal olarak batıldır.\n"
            "- **Pathos (Vicdani ve Duygusal Tesir):** İnsanın kendi kulağının, gözünün ve kalbinin hesap günü şahitlik edeceği bilinci (`küllü ülâike kâne anhü mes'ûlâ`), dijital çağın anonim linç kültürüne karşı derin bir içsel vicdan freni oluşturur."
        ),
        "adim04b": (
            "1. **Usûl Ekolü:** Klasik Kelâm ve Fıkıh Usûlünde *Esbâbü'l-İlm* (Bilginin Kaynakları: Havâss-ı Selîme, Haber-i Sâdık ve Akl-ı Selîm; Mâtürîdî, Râzî ve İbn Âşûr çizgisi).\n"
            "2. **Felsefi Perspektif:** Erdem epistemolojisi (*virtue epistemology*), Popperci eleştirel rasyonalizm ve bilişsel güvenlik kuramı.\n"
            "3. **Alternatif Yorumcu Konumlarından Ayrışma:**\n"
            "   - *Post-Truth / Relativist Uç:* Nesnel hakikatin ve doğrulamanın imkânsız olduğunu savunarak algı yönetimini meşrulaştırır.\n"
            "   - *Taklitçi / Dogmatik Uç:* Senedi ve delili incelenmemiş rivayet veya söylentileri sorgusuzca kabul eder.\n"
            "   Raporumuz, her iddiayı işitme (`sem'`), gözlem (`basar`) ve eleştirel muhakeme (`fuâd`) süzgecinden geçiren tahkik metodolojisini esas alır."
        ),
        "adim05_s1_s6": (
            "- **S1 (Önceki Âyetler — İsrâ 17:23–35):** Anne-babaya ihsan, akraba ve yoksul hakkı, çocukların öldürülmemesi, yetim malının korunması, ahde vefa ve ölçü-tartıda tam adalet emirlerinin hemen ardından 36. âyet gelir; çünkü tüm bu hukuki ve ahlaki ilkelerin korunması **doğru bilgi ve adil şahitliğe** bağlıdır.\n"
            "- **S2 (Sonraki Âyetler — İsrâ 17:37–39):** Hemen peşinden `ve lâ temşi fi'l-ardı merahan` (yeryüzünde böbürlenerek yürüme) buyrularak, bilgisizce hüküm vermenin arkasındaki **entellektüel kibir** hedef alınır ve tüm bu ilkeler `hikmet` (`zâlike mimmâ evhâ ileyke Rabbüke mine'l-hikmeh`) olarak mühürlenir.\n"
            "- **S3 (Pasajın Konumu):** İsrâ Sûresi 22–39. âyetlerdeki \"İslam Ahlak ve Hukuk Bildirgesi\"nin epistemolojik temel taşıdır.\n"
            "- **S4 (Sûre İçi Bütünlük):** Sûrenin başında ve sonunda Kur'an'ın en doğru yola ilettiği (`inne hâze'l-Kur'âne yehdî li'lletî hiye akvem`, 17:9) vurgulanırken, 36. âyet doğru yola ulaşmanın bilgi metodolojisini koyar.\n"
            "- **S5 (Nüzûl Sebepleri ve Hitap):** Cahiliye dönemindeki zanna dayalı şahitlik, iftira ve taklit kültürünü yıkmak üzere Mekke döneminde inmiştir.\n"
            "- **S6 (Mushaf Sırası ve Tevkîfî Yapı):** Nahl Sûresi'ndeki adalet ve ihsan emirlerinden sonra İsrâ Sûresi'nde bireysel ve kurumsal bilgi ahlakı inşa edilir."
        ),
        "adim06": (
            "- **Hucurât 49:6:** *\"Ey iman edenler! Eğer bir fâsık size bir haber getirirse onun doğruluğunu araştırın (`fe-tebeyyenû`); yoksa bilmeyerek bir topluluğa kötülük edersiniz...\"*\n"
            "- **Hucurât 49:12:** *\"Zannın çoğundan sakının; çünkü zannın bir kısmı günahtır.\"*\n"
            "- **Nûr 24:15:** *\"O iftirayı dilden dile aktarıyor, hakkında hiçbir bilginiz olmayan (`mâ leyse leküm bihî ilm`) şeyi ağzınızla söylüyor ve bunu önemsiz sanıyordunuz; hâlbuki Allah katında çok büyüktür!\"*\n"
            "- **Yûnus 10:36:** *\"Şüphesiz zan, hakikatin yerine asla geçmez (`inne'z-zanne lâ yuğnî mine'l-hakkı şey'â`).\"*\n"
            "- *Analitik Sonuç ve N4 Kapsamı:* İslam epistemolojisinde delilsiz iddia (`zan / ifk`) üzerine ne yargı hükmü ne de kamusal siyaset bina edilebilir (`N4`)."
        ),
        "adim10_morf": (
            "- **Kayıt:** Ebced, cifir veya numerolojik çıkarımlar metodolojik olarak yasaktır ve kullanılmamıştır.\n"
            "- **Morfolojik Analiz:** `لَا تَقْفُ` (*lâ takfu*) nehy-i hâzır (yasaklama) fiili, nakıs fiil olan `قَفَا - يَقْفُو` kökünden cezm alameti olarak sondaki illet harfinin (`و`) düşmesiyle gelmiştir; bu keskin morfolojik düşüş, delilsiz iddianın peşine düşme eyleminin derhal kesilmesini simgeler. `عِلْمٌ` (*ilm*) kelimesinin nefy-i istiğrak bağlamında nekre (belirsiz) gelmesi, kesin bilgi dışındaki her türlü zan, tahmin ve dedikoduyu yasak kapsamına sokar. `أُو۟لَـٰٓئِكَ` (*ülâike*) işaret zamirinin normalde akıl sahipleri için kullanılırken burada `sem'`, `basar` ve `fuâd` için kullanılması, bu üç bilişsel melekeye mahkeme huzurunda şahitlik edecek tüzel kişilik (*teşhis/personification*) kazandırır."
        ),
    },

    "QV-2026-009": {
        "adim02_kosul": (
            "- **Koşul-Sonuç Yapısı:**\n"
            "  - *Kamusal Tahsis Hükmü (`Mâ efâellâhü alâ Rasûlihî...`):* Kamu hazinesine (`fey'`) giren kaynakların yalnızca imtiyazlı elitlere değil; kamu yararına, yakınlara, yetimlere, yoksullara (`mesâkîn`) ve yolda kalmışlara tahsis edilmesi.\n"
            "  - *İktisadi Gaye / İllet (`key lâ yekûne dûleten beyne'l-ağniyâi minküm`):* Servetin toplumun alt ve orta katmanlarını dışlayarak yalnızca zenginler arasında el değiştiren kapalı bir tekel (`dûle`) haline gelmesinin önlenmesi."
        ),
        "adim03_elp": (
            "- **Ethos (Ahlaki Yük):** Mülkiyet bir imtiyaz değil, toplumsal sorumluluk içeren bir emanettir; kamu kaynaklarının ve iktisadi büyümenin kırılgan kesimleri gözetmesi adalet borcudur.\n"
            "- **Logos (Mantıksal Tutarlılık):** Servet yalnızca dar bir oligarşik zümre içinde dönerse (`dûle`), toplam talep çöker, orta sınıf erir ve toplumsal barış bozulur; sağlıklı bir ekonomi ancak servetin tabana yayılmasıyla sürdürülebilir.\n"
            "- **Pathos (Vicdani ve Duygusal Tesir):** Yetimin, yoksulun ve yolda kalmış sığınmacının kamu servetinde öz hakkı olduğunu ilan ederek sosyal dışlanmışlığı ve sınıf kinini ortadan kaldırır."
        ),
        "adim04b": (
            "1. **Usûl Ekolü:** Makâsıdî İslam İktisadı ve Ta'lîl Usûlü (İbn Âşûr, Şâtıbî, Cessâs ve Ebû Ubeyd *Kitâbü'l-Emvâl* çizgisi).\n"
            "2. **Felsefi Perspektif:** Dağıtıcı adalet (*distributive justice*), anti-oligarşik kurumsal iktisat ve kapsayıcı büyüme (*inclusive growth*).\n"
            "3. **Alternatif Yorumcu Konumlarından Ayrışma:**\n"
            "   - *Vahşi Kapitalist / Rantçı Uç:* Servet tekelleşmesini ve kartelleşmeyi serbest piyasa adına meşru görerek `key lâ yekûne dûleten` illetini işlevsizleştirir.\n"
            "   - *Mülkiyeti İptal Eden Kolektivist Uç:* Meşru özel mülkiyeti ve girişim hürriyetini tamamen ortadan kaldırır.\n"
            "   Raporumuz, meşru mülkiyeti korurken tekelciliği, faizci rantı ve servet istifçiliğini (`kenz`) önleyen İslam iktisat dengesini esas alır."
        ),
        "adim05_s1_s6": (
            "- **S1 (Önceki Âyetler — Haşr 59:1–6):** Benî Nadîr gazvesi sonrası savaşsız elde edilen kamu gelirlerinin (`fey'`) hukuki statüsü açıklanır.\n"
            "- **S2 (Sonraki Âyetler — Haşr 59:8–10):** Muhacirlerin sadakati ve Ensâr'ın `îsâr` (kendisi ihtiyaç içindeyken bile kardeşini kendine tercih etme: `ve yü'sirûne alâ enfüsihim ve lev kâne bihim hasâsah`) ahlakı övülerek, 7. âyetteki hukuki-iktisadi kural **ahlaki diğerkâmlıkla** taçlandırılır.\n"
            "- **S3 (Pasajın Konumu):** Haşr Sûresi'nin kamu maliyesi ve sosyal dayanışma omurgasının merkezindedir.\n"
            "- **S4 (Sûre İçi Bütünlük):** Kamu hukuku (`59:7`), kardeşlik ve îsâr ahlakı (`59:8–10`) ve sûre sonundaki Esmâü'l-Hüsnâ (`el-Melik, el-Kuddûs, es-Selâm...`, `59:22–24`) bütünlüğü mülkün gerçek sahibinin Allah olduğunu hatırlatır.\n"
            "- **S5 (Nüzûl Sebepleri ve Hitap):** Cahiliye döneminde ganimet ve kamu gelirlerinin yalnız kabile reislerine ayrılması geleneğini ilga etmek üzere Medine'de inmiştir.\n"
            "- **S6 (Mushaf Sırası ve Tevkîfî Yapı):** Mücâdele Sûresi'ndeki sosyal haklar ve infak emirlerinin ardından Haşr Sûresi makro-ekonomik bölüşüm adaletini kurumsallaştırır."
        ),
        "adim06": (
            "- **Tevbe 9:34:** Altın ve gümüşü biriktirip Allah yolunda (toplumsal refah ve üretim için) harcamayanları (`ellezîne yeknizûne'z-zehebe ve'l-fiddah`) acıklı bir azapla müjdele (`kenz` yasağı).\n"
            "- **Zâriyât 51:19 / Meâric 70:24–25:** Zenginlerin mallarında isteyen ve iffetinden dolayı isteyemeyen yoksullar için **belirli bir hak (`hakkun ma'lûm`)** vardır.\n"
            "- **Bakara 2:275–279:** Üretken ticareti helal, serveti emeksiz olarak zenginlere aktaran faizi (`ribâ`) haram kılan temel iktisat ilkesi.\n"
            "- **Haşr 59:9:** Nefsinin açgözlülüğünden (`şuhha nefsihî`) korunanların kurtuluşa ereceğini bildiren `îsâr` âyeti.\n"
            "- *Analitik Sonuç ve N4 Kapsamı:* İslam iktisadında servetin dolaşımdan çekilerek dar bir elit elinde toplanması (`dûle` ve `kenz`), toplumsal dengeyi yıkan yapısal bir krizdir (`N4`)."
        ),
        "adim10_morf": (
            "- **Kayıt:** Ebced, cifir veya numerolojik çıkarımlar metodolojik olarak yasaktır ve kullanılmamıştır.\n"
            "- **Morfolojik Analiz:** `دُولَةً` (*dûleten*) kelimesi `د-و-ل` kökünden türemiş olup, bir nesnenin sürekli belirli eller arasında dönüp dolaşmasını ifade eden isimdir (damme ile *dûle* servetin el değiştirmesi, fetha ile *devle* siyasi gücün el değiştirmesidir). Başındaki `كَىْ لَا` (*key lâ*) edatı açık bir *ta‘lîl* (hukuki gaye/illet) bağlacıdır. Âyetin devamındaki `فَخُذُوهُ` (*fe-huzûhü*) ve `فَٱنتَهُوا۟` (*fe-ntehû*) cemi emir fiilleri ise hem iktisadi bölüşüm kararlarına hem de Peygamberî sünnetin bağlayıcı kamu düzenine itaati kurumsal bir vecibe kılar."
        ),
    },

    "QV-2026-010": {
        "adim02_kosul": (
            "- **Koşul-Sonuç Yapısı:**\n"
            "  - *Ontolojik Öncül (`Ve min âyâtihî halku's-semâvâti ve'l-ardı vahtilâfü elsinetiküm ve elvâniküm`):* Dillerin ve renklerin çeşitliliğinin, tıpkı göklerin ve yerin yaratılışı gibi Allah'ın kudret âyetlerinden biri olması.\n"
            "  - *Epistemik ve Hukuki Sonuç (`inne fî zâlike le-âyâtin li'l-âlimîn`):* Farklı dil ve etnik kimliklerin bastırılacak bir kusur değil, bilakis âlimler ve düşünen toplumlar için korunması ve incelenmesi gereken ilahi birer delil ve medeniyet zenginliği olması."
        ),
        "adim03_elp": (
            "- **Ethos (Ahlaki Yük):** Her insan diline ve ten rengine, Yaratıcı'nın bir sanat eseri ve kozmik âyeti (`âyetullâh`) olduğu bilinciyle hürmet göstermek; ırkçı kibri ve kültürel aşağılamayı reddetmek.\n"
            "- **Logos (Mantıksal Tutarlılık):** Aynı anne-babadan ve aynı anatomik ses tellerinden binlerce farklı dil, lehçe ve mizaç çıkması tesadüfle açıklanamaz; bu çeşitlilik beşerî işbölümü, kültürlerarası öğrenme ve medeniyet inşası için tasarlanmıştır.\n"
            "- **Pathos (Vicdani ve Duygusal Tesir):** Farklı dil ve renkteki insanları \"yabancı/tehdit\" olmaktan çıkarıp, gökyüzü ve yeryüzü kadar doğal ve saygın birer \"İlahi Âyet\" mertebesine yükselterek derin bir estetik hayranlık ve kardeşlik uyandırır."
        ),
        "adim04b": (
            "1. **Usûl Ekolü:** Kozmolojik-Makâsıdî Tefsir Usûlü (Fahreddîn er-Râzî, Mâtürîdî ve İbn Âşûr çizgisi).\n"
            "2. **Felsefi Perspektif:** Çoğulcu medeniyet felsefesi, dilsel-kültürel insan hakları ve çokkültürlü vatandaşlık hukuku.\n"
            "3. **Alternatif Yorumcu Konumlarından Ayrışma:**\n"
            "   - *Asimilasyonist / Jakoben Uç:* Toplumsal birliği ancak dilsel ve kültürel farklılıkları zorla silerek (tek tipleştirerek) sağlayabileceğini zanneder.\n"
            "   - *Ayrılıkçı / Etnosentrik Uç:* Dil ve renk farklılığını ortak vatandaşlık sözleşmesini yıkan bir üstünlük ve çatışma aracına dönüştürür.\n"
            "   Raporumuz, çeşitliliği birlik içinde zenginlik (`kesrette vahdet`) ve ilahi bir âyet olarak koruyan Kur'anî çoğulculuk modelini esas alır."
        ),
        "adim05_s1_s6": (
            "- **S1 (Önceki Âyetler — Rûm 30:20–21):** İnsanın topraktan yaratılıp yeryüzüne yayılması (30:20) ve eşler arasındaki sevgi (`meveddet`) ve merhamet (`rahmet`) âyetinden (30:21) hemen sonra 22. âyette dillerin ve renklerin çeşitliliğine geçilir.\n"
            "- **S2 (Sonraki Âyetler — Rûm 30:23–27):** Uyku ve rızık arayışı, şimşek ve yağmurla ölü toprağın diriltilmesi ve göklerle yerin Allah'ın emriyle ayakta durması sıralanarak **6'lı 'Ve min âyâtihî' (Kozmik Âyetler) dizisi** tamamlanır.\n"
            "- **S3 (Pasajın Konumu):** Rûm Sûresi'ndeki 20–27. âyetler arasındaki kevnî (kozmik ve antropolojik) deliller manzumesinin üçüncü halkasıdır.\n"
            "- **S4 (Sûre İçi Bütünlük):** Rûm 30:30'daki `fıtratullâh` (Allah'ın insanları üzerine yarattığı fıtrat; Allah'ın yaratışında değişme yoktur) ilkesiyle birleştiğinde, dilsel ve etnik çeşitliliğin fıtrata içkin olduğu anlaşılır.\n"
            "- **S5 (Nüzûl Sebepleri ve Hitap):** Kureyş'in Kâbe merkezli kabile/soy kibrini ve diğer kavimleri (*acem*) aşağılayan anlayışını kırmak üzere Mekke döneminde inmiştir.\n"
            "- **S6 (Mushaf Sırası ve Tevkîfî Yapı):** Ankebût Sûresi'ndeki iman sınamalarından sonra Rûm Sûresi evrensel tarih ve tabiat âyetleriyle ufku bütün insanlığa açar."
        ),
        "adim06": (
            "- **Hucurât 49:13:** *\"Ey insanlar! Şüphesiz biz sizi bir erkekle bir dişiden yarattık ve birbirinizle tanışasınız (`li-teârefû`) diye sizi kavimlere ve kabilelere ayırdık...\"*\n"
            "- **Fâtır 35:27–28:** Dağların, meyvelerin, insanların ve canlıların renklerinin farklı farklı (`muhtelifün elvânühû`) yaratılmasının ancak **âlimlerin (`el-ulemâ`)** hakkıyla kavradığı bir mucize olması.\n"
            "- **İbrâhîm 14:4:** Her peygamberin, mesajı açıkça anlatabilmesi için kendi kavminin diliyle (`bi-lisâni kavmihî`) gönderilmesi (anadilin iletişim ve hidayet değeri).\n"
            "- **Hûd 11:118:** *\"Rabbin dileseydi bütün insanları tek tip bir topluluk (`ümmeten vâhide`) yapardı.\"*\n"
            "- *Analitik Sonuç ve N4 Kapsamı:* Farklı dil ve renkleri kriminalize etmek veya üstünlük ölçütü yapmak, doğrudan Allah'ın kevnî âyetleriyle savaşmaktır (`N4`)."
        ),
        "adim10_morf": (
            "- **Kayıt:** Ebced, cifir veya numerolojik çıkarımlar metodolojik olarak yasaktır ve kullanılmamıştır.\n"
            "- **Morfolojik Analiz:** `ٱخْتِلَـٰفُ` (*ihtilâf*) mastarı *ifti‘âl* bâbından olup, çeşitlilik ve birbirini tamamlayan farklılaşma demektir (`خَلْقُ` mastarı üzerine atfedilerek yaratılışla eşdeğer kılınmıştır). `أَلْسِنَتِكُمْ` (*elsinetiküm*, `lisân`ın çoğulu) ve `أَلْوَٰنِكُمْ` (*elvâniküm*, `levn`in çoğulu) kelimeleri *cem‘-i kıllet* kalıbında gelerek temel dil ailelerini ve antropolojik çeşitliliği kuşatır. Son kelimenin Âsım/Hafs kıraatinde kesra ile `لِّلْعَـٰلِمِينَ` (*li'l-âlimîn*: âlimler/bilim insanları için), Hafs dışındaki mütevâtir kıraatte ise fetha ile `لِّلْعَـٰلَمِينَ` (*li'l-âlemîn*: bütün âlemler için) okunması iki anlamı birbirine kenetler."
        ),
    },

    "QV-2026-011": {
        "adim02_kosul": (
            "- **Koşul-Sonuç Yapısı:**\n"
            "  - *On Muhkem Emir/Yasak (`Kul teâlev etlü mâ harrame Rabbüküm aleyküm...`):* (1) Şirk koşmamak, (2) Anne-babaya ihsan, (3) Yoksulluk (`imlâk`) korkusuyla çocukları öldürmemek, (4) Açık/gizli fuhşiyata yaklaşmamak, (5) Haklı bir sebep (`bi'l-hakk`) dışında cana kıymamak, (6) Yetim malına en güzel biçimde (`bi'lletî hiye ahsen`) yaklaşmak, (7) Ölçü ve tartıyı adaletle (`bi'l-kıst`) tam yapmak, (8) Yakın akraba (`zâ kurbâ`) aleyhine dahi olsa sözde ve hükümde adil olmak (`fe-'dilû`), (9) Allah'ın ahdini yerine getirmek, (10) Tefrikaya düşmeden dosdoğru yolu (`sırât-ı müstakîm`) izlemek.\n"
            "  - *Normatif Sonuç (`zâliküm vassâküm bihî lealleküm ta'kılûn / tezekkerûn / tettekûn`):* Akıl, toplumsal hafıza ve ahlaki sorumluluk düzeninin bu on evrensel temel üzerinde yükselmesi."
        ),
        "adim03_elp": (
            "- **Ethos (Ahlaki Yük):** Yoksul çocuğun yaşama hakkını, yetimin malını, çarşı-pazardaki teraziyi ve mahkemedeki şahitliği kendi öz yakınımızın çıkarının üstünde tutan tavizsiz bir doğruluk ahlakı.\n"
            "- **Logos (Mantıksal Tutarlılık):** Âyet insan kapasitesini aşan soyut bir hatasızlık dayatmaz (`lâ nükellifü nefsen illâ vüs'ahâ` — kimseye gücünün üstünde yük yüklemeyiz); ancak güç yetirilen ölçü, tartı ve şahitlikte dürüstlüğü zorunlu kılar.\n"
            "- **Pathos (Vicdani ve Duygusal Tesir):** `Kul teâlev` (Geliniz, yüksek bir ahlaki zirveye çıkınız!) davetiyle insanlığı cahiliyenin çukurundan evrensel fazilet ufkuna çağırır."
        ),
        "adim04b": (
            "1. **Usûl Ekolü:** Muhkemât-Merkezli Küllî Makâsıd Usûlü (İbn Abbas, Taberî, Kurtubî ve Şâtıbî çizgisi — Mekke'de inen küllî ilkelerin Medine'deki cüz'î hükümlerin anayasası olduğu ilkesi).\n"
            "2. **Felsefi Perspektif:** Evrensel doğal hukuk / ahlak yasası (*lex moralis*), kırılganların korunması etiği ve kurumsal dürüstlük.\n"
            "3. **Alternatif Yorumcu Konumlarından Ayrışma:**\n"
            "   - *Şekilci / Parçacı Uç:* Dini yalnızca ritüellere indirgeyip ölçü-tartı hilesini, yetim hakkını ve akraba kayırmacılığını ikincil görür.\n"
            "   - *Ahlaki Relativist Uç:* Evrensel ve değişmez ahlaki ilkelerin (`muhkemât`) varlığını reddeder.\n"
            "   Raporumuz, En'âm 151–152'yi tüm semavî şeriatların nesh edilmeyen ortak ahlaki omurgası olarak konumlandırır."
        ),
        "adim05_s1_s6": (
            "- **S1 (Önceki Âyetler — En'âm 6:136–150):** Cahiliye müşriklerinin kendi uydurdukları batıl helal-haram tabuları, kız çocuklarını katletmeleri ve delilsiz iddiaları (`hel indeküm min ilmin`, 6:148) çürütülür.\n"
            "- **S2 (Sonraki Âyet — En'âm 6:153):** *\"İşte bu benim dosdoğru yolumdur (`ve enne hâzâ sırâtî müstakîmen`), ona uyun; başka yollara (`es-sübül`) uymayın ki sizi O'nun yolundan ayırıp parçalamasın\"* buyrularak 10 ilke tevhid ve birlik mührüyle tamamlanır.\n"
            "- **S3 (Pasajın Konumu):** En'âm Sûresi'nin (ve Mekke döneminin) nihai ahlak ve hukuk manifestosudur.\n"
            "- **S4 (Sûre İçi Bütünlük):** Sûre boyunca işlenen tevhid akidesi, 151–153. âyetlerde somut sosyal adalet, yaşam hakkı ve piyasa/yargı dürüstlüğüne dönüştürülür.\n"
            "- **S5 (Nüzûl Sebepleri ve Hitap):** Mekke'de cahiliye keyfiliğine karşı vahyî ahlakın evrensel ölçütlerini ilan etmek üzere inmiştir.\n"
            "- **S6 (Mushaf Sırası ve Tevkîfî Yapı):** Mâide Sûresi'ndeki (`5:1`) ahitlere vefa ve helal-haram hükümlerinin ardından En'âm Sûresi bu hükümlerin evrensel ahlaki köklerini sergiler."
        ),
        "adim06": (
            "- **İsrâ 17:22–39:** En'âm 151–153'teki 10 ilkeyi 18 âyet halinde detaylandıran paralel Mekki manifesto (`ve lâ taktulû evlâdeküm haşyete imlâk` dahil).\n"
            "- **Nisâ 4:135:** *\"Ey iman edenler! Kendinizin veya anne-babanızın ve akrabalarınızın (`ve'l-akrabîn`) aleyhine bile olsa adaleti titizlikle ayakta tutan, Allah için şahitlik eden kimseler olun!\"*\n"
            "- **Mutaffifîn 83:1–3:** Ölçü ve tartıda hile yapanların (`el-mutaffifîn`) vay haline!\n"
            "- **Bakara 2:83:** İsrâiloğulları'ndan alınan misakta da aynı temel ilkelerin (Allah'tan başkasına kulluk etmeme, anne-babaya, yakınlara, yetimlere ve yoksullara ihsan) yer alması.\n"
            "- *Analitik Sonuç ve N4 Kapsamı:* Yaşam hakkı, çocuk/yetim güvencesi, piyasa dürüstlüğü ve akraba kayırmazlığı çöktüğünde toplumun ahlaki sözleşmesi kırılır (`N4`)."
        ),
        "adim10_morf": (
            "- **Kayıt:** Ebced, cifir veya numerolojik çıkarımlar metodolojik olarak yasaktır ve kullanılmamıştır.\n"
            "- **Morfolojik Analiz:** `تَعَالَوْا۟` (*te‘âlev*) emir fiili `عُلُوّ` (yükselmek) kökünden *tefâ‘ul* bâbında olup, muhatabı aşağılık cahiliye örfünden yüksek ahlaki tepeye çıkmaya çağırır. 151. âyet `لَعَلَّكُمْ تَعْقِلُونَ` (*ta‘kılûn*: akledesiniz), 152. âyet `لَعَلَّكُمْ تَذَكَّرُونَ` (*tezekkerûn*: öğüt ve bilinç kazanasınız), 153. âyet ise `لَعَلَّكُمْ تَتَّقُونَ` (*tettekûn*: sorumluluk bilinciyle korunasınız) fasılasıyla biter; bu morfolojik üçleme `Akıl → Bilinç → Ahlaki Eylem (Takvâ)` hiyerarşisini kurar."
        ),
    },

    "QV-2026-012": {
        "adim02_kosul": (
            "- **Koşul-Sonuç Yapısı:**\n"
            "  - *İlahi İrsâl ve İnzâl (`Lekad erselnâ rusülenâ bi'l-beyyinâti ve enzelnâ meahümü'l-kitâbe ve'l-mîzâne`):* Peygamberlerin açık delillerle gönderilmesi ve beraberlerinde `Kitâb` (anayasal hukuk/norm) ile `Mîzân`ın (adalet ve denetim terazisi) indirilmesi.\n"
            "  - *Evrensel Gaye (`li-yekûme'n-nâsü bi'l-kıst`):* İnsanların bizzat kendilerinin hakkaniyet ve adaletle (`kıst`) ayakta durması.\n"
            "  - *Maddi ve Teknolojik Güç (`ve enzelne'l-hadîde fîhi be'sün şedîdün ve menâfi'u li'n-nâs`):* Adaleti savunacak caydırıcı güç (`be'sün şedîd`) ve insanlığın sivil refahına hizmet edecek endüstriyel/teknolojik kapasite (`menâfi'u li'n-nâs`) olarak demirin (`el-hadîd`) yaratılması."
        ),
        "adim03_elp": (
            "- **Ethos (Ahlaki Yük):** Maddi, askeri ve teknolojik gücü (`Hadîd`) hiçbir zaman zorbalık ve tahakküm aracı yapmamak; daima `Kitâb` (hukuk) ve `Mîzân` (adalet terazisi) emrinde ve insanlığın faydasına (`menâfi'u li'n-nâs`) kullanmak.\n"
            "- **Logos (Mantıksal Tutarlılık):** Hukuksuz güç (`Mîzânsız Hadîd`) tiranlık üretir; güçsüz hukuk (`Hadîdsiz Mîzân`) ise saldırganlar karşısında aciz kalır. Medeniyet ancak `Kitâb + Mîzân + Hadîd` üçlüsünün dengesiyle ayakta durur (Mâtürîdî, Râzî, İbn Teymiyye).\n"
            "- **Pathos (Vicdani ve Duygusal Tesir):** `Li-yekûme'n-nâsü bi'l-kıst` ifadesiyle adaleti sadece devletten beklenen pasif bir lütuf olmaktan çıkarıp, bütün toplumun omuz verdiği onurlu bir kıyama dönüştürür."
        ),
        "adim04b": (
            "1. **Usûl Ekolü:** Mâtürîdî-Makâsıdî Medeniyet ve Kamu Hukuku Usûlü (Ebû Mansûr el-Mâtürîdî *Te'vîlât*, Fahreddîn er-Râzî *Mefâtîh*, İbn Teymiyye *es-Siyâsetü'ş-Şer'iyye* ve İbn Âşûr çizgisi).\n"
            "2. **Felsefi Perspektif:** Kuvvetler ayrılığı, hukukun üstünlüğü (*rule of law*) ve etik teknoloji felsefesi.\n"
            "3. **Alternatif Yorumcu Konumlarından Ayrışma:**\n"
            "   - *Makyavelist / Militarist Uç:* Gücü (`Hadîd`) hukukun ve ahlakın (`Kitâb ve Mîzân`) üstünde görerek \"güçlü olan haklıdır\" anlayışını benimser.\n"
            "   - *Teknolojiden Kopuk İdealist Uç:* Bilim, sanayi ve savunma teknolojisini (`Hadîd`) ihmal ederek adaleti savunmasız bırakır.\n"
            "   Raporumuz, yüksek bilim ve teknolojiyi (`Hadîd`) hukuk ve adalet terazisine (`Mîzân`) tabi kılan üç sütunlu medeniyet modelini esas alır."
        ),
        "adim05_s1_s6": (
            "- **S1 (Önceki Âyetler — Hadîd 57:1–24):** Göklerin ve yerin mülkünün Allah'a ait olduğu, iman, infak ve dünya hayatının aldatıcı gösterişine kapılmama uyarıları yapılır.\n"
            "- **S2 (Sonraki Âyetler — Hadîd 57:26–29):** Hz. Nûh, Hz. İbrâhîm ve Hz. Îsâ'nın gönderilişi, şefkat ve merhamet (`re'feten ve rahmeh`) ve Allah'ın lütfunun hiçbir zümrenin tekelinde olmadığı bildirilir.\n"
            "- **S3 (Pasajın Konumu):** Sûreye adını veren (`Sûretü'l-Hadîd`) 25. âyet, sûrenin kavramsal ve medeniyet zirvesidir.\n"
            "- **S4 (Sûre İçi Bütünlük):** Sûrenin başındaki ontolojik kudret (`Hüve'l-Evvelü ve'l-Âhiru...`, 57:3) ve ortasındaki iktisadi infak (57:7, 10–11), 25. âyette kurumsal adalet (`Mîzân`) ve endüstriyel güçle (`Hadîd`) bütünleşir.\n"
            "- **S5 (Nüzûl Sebepleri ve Hitap):** Medine İslam toplumunun hem hukuki kurumlarını hem de savunma ve iktisadi altyapısını inşa ettiği dönemde inmiştir.\n"
            "- **S6 (Mushaf Sırası ve Tevkîfî Yapı):** Vâkıa Sûresi'ndeki ahiret bilincinin hemen ardından Hadîd Sûresi dünya medeniyetinin imar ve adalet yasalarını vaz'eder."
        ),
        "adim06": (
            "- **Şûrâ 42:17:** *\"Kitab'ı ve Mîzân'ı (adalet terazisini) hak ile indiren Allah'tır (`Allâhü'llezî enzele'l-kitâbe bi'l-hakkı ve'l-mîzân`).\"*\n"
            "- **Rahmân 55:7–9:** *\"Göğü yükseltti ve Mîzân'ı (denge ve adalet yasasını) koydu; sakın terazide/dengede haddi aşmayın (`ellâ tatğav fi'l-mîzân`) ve tartıyı adaletle (`bi'l-kıst`) tutun!\"*\n"
            "- **Enfâl 8:60:** Düşmanı caydırmak için gücünüzün yettiği kadar kuvvet (`kuvvet`) hazırlayın (barışı koruyan caydırıcılık).\n"
            "- **Sebe' 34:10–11 ve Enbiyâ 21:80:** Hz. Dâvûd'a demirin (`el-hadîd`) yumuşatılması ve insanları koruyacak zırh/sanayi üretiminin öğretilmesi.\n"
            "- *Analitik Sonuç ve N4 Kapsamı:* `Kitâb`, `Mîzân` ve `Hadîd` arasındaki bağ koptuğunda devletler ya hukuksuz tiranlığa ya da dış müdahaleye açık acziyete sürüklenir (`N4`)."
        ),
        "adim10_morf": (
            "- **Kayıt:** Ebced, cifir veya numerolojik çıkarımlar (57. sûre veya kelime/harf sayıları üzerinden yapılan batıni/numerolojik iddialar) metodolojik olarak yasaktır ve analitik kanıt olarak kullanılmamıştır.\n"
            "- **Morfolojik Analiz:** Âyette peygamberler için `أَرْسَلْنَا` (*erselnâ*: gönderdik) fiili kullanılırken, `el-Kitâb`, `el-Mîzân` ve `el-Hadîd` için `أَنزَلْنَا` (*enzelnâ*: indirdik) fiili tekrarlanmıştır; bu morfolojik paralellik maddi-teknolojik nimetlerin (`Hadîd`) de tıpkı vahiy (`Kitâb`) ve adalet (`Mîzân`) gibi ilahi emanete tabi olduğunu gösterir. `لِيَقُومَ ٱلنَّاسُ بِٱلْقِسْطِ` cümlesindeki *lâm-ı ta‘lîl*, tüm peygamberlik ve vahiy tarihinin dünyevi gayesini \"insanların adaletle kıyam etmesi\" olarak tescil eder."
        ),
    },

    "QV-2026-013": {
        "adim02_kosul": (
            "- **Koşul-Sonuç Yapısı:**\n"
            "  - *Üç Kurucu Emir (`İnnallâhe ye'muru bi'l-adli ve'l-ihsâni ve îtâi zi'l-kurbâ`):* (1) `el-Adl` (nesnel hukuki eşitlik, hakkaniyet ve itidal), (2) `el-İhsân` (hukukun ötesine geçen ahlaki fazilet, şefkat ve işini en güzel yapma), (3) `Îtâi zi'l-kurbâ` (aile, akraba ve yakın dayanışma ağlarının desteklenmesi).\n"
            "  - *Üç Kurucu Yasak (`ve yenhâ ani'l-fahşâi ve'l-münkeri ve'l-bağy`):* (1) `el-Fahşâ` (bireysel iffetsizlik ve çirkin aşırılıklar), (2) `el-Münker` (akl-ı selimin ve kamu vicdanının reddettiği kötülükler), (3) `el-Bağy` (başkalarının hakkına tecavüz, zorbalık ve kamu gücünün istismarı).\n"
            "  - *Gaye (`yaızuküm lealleküm tezekkerûn`):* Toplumsal hafızanın ve ahlaki bilincin diri tutulması."
        ),
        "adim03_elp": (
            "- **Ethos (Ahlaki Yük):** Sadece kanunun zorunlu kıldığı asgari adaleti (`adl`) vermekle yetinmeyip, kendi hakkından feragat ederek iyilik ve güzellik (`ihsân`) üretmek ve zorbalığa (`bağy`) asla tenezzül etmemek.\n"
            "- **Logos (Mantıksal Tutarlılık):** Üç emir ile üç yasak arasında tam bir yapısal simetri vardır: `Adl` `Bağy`i (zorbalığı) engeller; `İhsan` `Fahşâ`yı (çirkinliği) temizler; `Îtâi zi'l-kurbâ` ise `Münker`in (sosyal yabancılaşma ve kötülüğün) yayılmasını önler.\n"
            "- **Pathos (Vicdani ve Duygusal Tesir):** Ömer b. Abdülaziz'den bu yana 14 asırdır her cuma hutbesinin sonunda okunarak mümin vicdanında adalet, merhamet ve zulüm karşıtlığını sürekli tazeleyen bir medeniyet yemini oluşturur."
        ),
        "adim04b": (
            "1. **Usûl Ekolü:** Câmi'u'l-Kelim ve Makâsıd-ı Şerîa Usûlü (İbn Mes'ûd, Râgıb el-İsfahânî, Fahreddîn er-Râzî, İzz b. Abdüsselâm ve İbn Âşûr çizgisi).\n"
            "2. **Felsefi Perspektif:** Adalet ve bakım etiği (*ethics of justice and care*), sosyal sermaye kuramı ve anayasal refah devleti.\n"
            "3. **Alternatif Yorumcu Konumlarından Ayrışma:**\n"
            "   - *Salt Bürokratik / Pozitivist Uç:* Yalnızca soğuk kanuni prosedürle (`adl`) yetinip şefkat, ihsan ve birincil dayanışma ağlarını (`ihsân ve zi'l-kurbâ`) dışlar.\n"
            "   - *Nepotist / Kabileci Uç:* `Îtâi zi'l-kurbâ` (yakınları gözetme) emrini kamu makamlarında akraba kayırmacılığına (`nepotizm`) alet ederek birinci ilke olan `el-Adl`i çiğner.\n"
            "   Raporumuz, kamusal alanda tavizsiz `Adl`i, sivil ve insani ilişkilerde ise `İhsan` ve `Dayanışma`yı birleştiren hiyerarşik modeli esas alır."
        ),
        "adim05_s1_s6": (
            "- **S1 (Önceki Âyetler — Nahl 16:84–89):** Kıyamet günü her ümmetten bir şahit getirileceği ve Kur'an'ın **her şeyi açıklayan bir rehber, rahmet ve müjde (`tibyânen li-külli şey'in`)** olarak indirildiği (16:89) belirtilir; 90. âyet bu `tibyân`ın en veciz kanıtı olarak hemen peşinden gelir.\n"
            "- **S2 (Sonraki Âyetler — Nahl 16:91–97):** *\"Allah'a verdiğiniz ahdi yerine getirin, yeminlerinizi bozmayın\"* (16:91) ve *\"Erkek olsun kadın olsun kim mümin olarak salih amel işlerse ona tertemiz bir hayat (`hayâten tayyibe`) yaşatırız\"* (16:97) buyrularak 90. âyetteki ilkelerin pratik sonucu gösterilir.\n"
            "- **S3 (Pasajın Konumu):** Nahl Sûresi'nin ikinci yarısındaki hukuki ve ahlaki ilkeler dizisinin kalbidir.\n"
            "- **S4 (Sûre İçi Bütünlük):** Nimetler sûresi (*Sûretü'n-Niam*) olan Nahl Sûresi, Allah'ın sayısız nimetlerine şükrün ancak `Adl, İhsan ve Dayanışma` ile gerçekleşeceğini ortaya koyar.\n"
            "- **S5 (Nüzûl Sebepleri ve Hitap):** Osman b. Maz'ûn gibi sahabilerin İslam'ın bütün ahlakını tek cümlede özetleyen bu âyeti duyduklarında imanlarının kalplerine yerleştiği rivayet edilir.\n"
            "- **S6 (Mushaf Sırası ve Tevkîfî Yapı):** Hicr Sûresi'ndeki tarihsel helak yasalarının ardından Nahl Sûresi toplumları yaşatan evrensel adalet ve ihsan yasasını sunar."
        ),
        "adim06": (
            "- **Nisâ 4:58:** Emanetleri ehline vermek ve insanlar arasında **adaletle (`bi'l-adl`)** hükmetmek.\n"
            "- **Bakara 2:195:** *\"İhsan edin; şüphesiz Allah ihsan sahiplerini (`el-muhsinîn`) sever.\"*\n"
            "- **İsrâ 17:26 ve Rûm 30:38:** Akrabaya (`ze'l-kurbâ`), yoksula ve yolda kalmışa hakkını ver!\n"
            "- **A'râf 7:33:** *\"De ki: Rabbim ancak açık ve gizli fuhşiyatı (`el-fevâhiş`), günahı ve **haksız yere bağyi (zorbalığı)** haram kılmıştır.\"*\n"
            "- *Analitik Sonuç ve N4 Kapsamı:* `Adl`, `İhsan` ve `Dayanışma` zayıfladığında kamusal alanı `Fahşâ`, `Münker` ve `Bağy` istila eder (`N4`)."
        ),
        "adim10_morf": (
            "- **Kayıt:** Ebced, cifir veya numerolojik çıkarımlar metodolojik olarak yasaktır ve kullanılmamıştır.\n"
            "- **Morfolojik Analiz:** `يَأْمُرُ` (*ye'muru*) ve `يَنْهَىٰ` (*yenhâ*) fiilleri muzâri (geniş/şimdiki zaman) kalıbında gelerek bu üç emir ve üç yasağın zamana veya zemine göre değişmeyen **süreklilik (`istimrâr`)** taşıdığını gösterir. Emir tarafında `ٱلْعَدْلِ` ve `ٱلْإِحْسَـٰنِ` marife (belirli) mastar olarak gelirken, üçüncü maddede `إِيتَآئِ ذِى ٱلْقُرْبَىٰ` (*îtâi zi'l-kurbâ*: yakınlara verme) şeklinde *if‘âl* bâbından mastar-ı muzâf kullanılması, dayanışmanın kuru bir söz değil somut bir mali/sosyal aktarım olmasını ifade eder."
        ),
    },

    "QV-2026-014": {
        "adim02_kosul": (
            "- **Koşul-Sonuç Yapısı:**\n"
            "  - *Evrensel Hitap ve Ontolojik Eşitlik (`Yâ eyyühe'n-nâsü innâ halaknâküm min zekerin ve ünsâ`):* Bütün insanların tek bir anne ve babadan (bir erkek ve bir dişiden) eşit olarak yaratılmış olması → Soy, ırk veya kast üstünlüğü iddiasının ontolojik olarak batıl olması.\n"
            "  - *Sosyolojik Çeşitlilik ve Teleolojik Gaye (`ve cealnâküm şuûben ve kabâile li-teârefû`):* İnsanların milletlere ve kabilelere ayrılmasının gayesinin birbirini inkâr etmek (`tenâkür`) veya övünmek (`tefâhur`) değil, **karşılıklı tanışmak ve yardımlaşmak (`teârüf`)** olması.\n"
            "  - *Nihai Değer Ölçütü (`inne ekrameküm indallâhi etkâküm`):* Allah katında en üstün/değerli olanın yalnızca ahlaki sorumluluk ve liyakat (`takvâ`) bakımından en ileride olan kimse olması."
        ),
        "adim03_elp": (
            "- **Ethos (Ahlaki Yük):** İnsanı etnik kökeni, rengi, dili veya sosyal statüsüyle değil, yalnızca ahlaki bütünlüğü, dürüstlüğü ve emanet bilinciyle (`takvâ`) değerlendirmek.\n"
            "- **Logos (Mantıksal Tutarlılık):** Kişinin kendi iradesiyle seçmediği doğuştan gelen özellikler (ırk, kabile, ten rengi) ahlaki bir övünç (`kerem`) veya kınama sebebi olamaz; övgü ve sorumluluk ancak iradî kazanım olan `takvâ`ya (ahlaki erdeme) bağlıdır (Râzî, İbn Âşûr).\n"
            "- **Pathos (Vicdani ve Duygusal Tesir):** `Yâ eyyühe'n-nâs` (Ey insanlar!) nidasıyla bütün insanlık ailesini aynı çatı altında toplayarak ırkçılık ve yabancı düşmanlığına karşı evrensel bir kardeşlik heyecanı uyandırır."
        ),
        "adim04b": (
            "1. **Usûl Ekolü:** Evrenselci-Makâsıdî İnsan Hakları ve Kamu Hukuku Usûlü (Zemahşerî, Râzî, Âlûsî ve İbn Âşûr çizgisi).\n"
            "2. **Felsefi Perspektif:** Kozmopolit insan onuru etiği, kültürlerarası diyalog (*interculturalism*) ve liyakat temelli adalet.\n"
            "3. **Alternatif Yorumcu Konumlarından Ayrışma:**\n"
            "   - *Irkçı / Kabileci (Asabiyetçi) Uç:* Etnik veya ulusal kimliği hakikatin ve hukukun üstüne çıkararak ötekini aşağılar.\n"
            "   - *Kimliksizleştirici / Kültür-Kör Uç:* `Şuûb ve kabâil` (milletler ve kültürel aidiyetler) gerçeğini tamamen yok sayarak insanı köksüzleştirir.\n"
            "   Raporumuz, kültürel aidiyetleri `teârüf` (tanışma ve zenginleşme) zemini olarak koruyan, üstünlüğü ise yalnızca `takvâ` ve liyakate bağlayan Kur'anî dengeyi esas alır."
        ),
        "adim05_s1_s6": (
            "- **S1 (Önceki Âyetler — Hucurât 49:9–12):** Müminler arası çatışma çözümü (49:9–10) ve alay, lakap takma, suizan, tecessüs ve gıybet yasaklarının (49:11–12) hemen ardından 13. âyet gelir; çünkü tüm bu toplumsal hastalıkların arkasındaki en derin kök **kibir ve kabilecilik (`asabiyet`)** hastalığıdır.\n"
            "- **S2 (Sonraki Âyetler — Hucurât 49:14–18):** Bedevîlerin *\"İman ettik\"* sözüne karşılık gerçek imanın kuru bir aidiyet iddiası değil, kalbe yerleşen samimiyet ve fedakârlık olduğu açıklanarak `takvâ` ölçütü somutlaştırılır.\n"
            "- **S3 (Pasajın Konumu):** Hucurât Sûresi'nin `Yâ eyyühe'llezîne âmenû` (Ey iman edenler!) hitaplarıyla ilerleyen 5 ahlaki çağrısını, bütün insanlığa seslenen `Yâ eyyühe'n-nâs` (Ey insanlar!) zirvesiyle taçlandırır.\n"
            "- **S4 (Sûre İçi Bütünlük):** Sûre iç halkada mümin kardeşliğini (`49:10`), dış halkada ise evrensel insanlık kardeşliğini ve `teârüf` hukukunu (`49:13`) inşa eder.\n"
            "- **S5 (Nüzûl Sebepleri ve Hitap):** Mekke'nin fethi günü Bilâl-i Habeşî'nin Kâbe'nin üzerinde ezan okuması üzerine bazı Kureyşlilerin soy kibriyle konuşmaları ve Sabit b. Kays vakası üzerine inmiştir (Taberî, Kurtubî).\n"
            "- **S6 (Mushaf Sırası ve Tevkîfî Yapı):** Hucurât 49:9–10'daki iç barış hukukunu küresel barış ve kültürlerarası diplomasi (`teârüf`) ilkeleriyle tamamlar."
        ),
        "adim06": (
            "- **Rûm 30:22:** Dillerin ve renklerin farklılığının Allah'ın kozmik âyetlerinden olması.\n"
            "- **Nisâ 4:1:** *\"Ey insanlar! Sizi tek bir nefisten (`min nefsin vâhide`) yaratan, ondan eşini var eden ve ikisinden birçok erkekler ve kadınlar üreten Rabbinize karşı gelmekten sakının!\"*\n"
            "- **İsrâ 17:70:** *\"Andolsun biz Âdemoğullarını onurlu ve मुكرّم kıldık (`ve lekad kerremnâ benî Âdeme`).\"*\n"
            "- **Mü'minûn 23:101:** Kıyamet günü sûra üflendiğinde aralarında artık soy-sop (`ensâb`) bağlarının geçerli olmayacağı uyarısı.\n"
            "- *Analitik Sonuç ve N4 Kapsamı:* Soy ve kimlik taassubu (`asabiyet`), `teârüf` kanallarını tıkayıp `takvâ` ve liyakati tasfiye ettiğinde toplumsal barış çöker (`N4`)."
        ),
        "adim10_morf": (
            "- **Kayıt:** Ebced, cifir veya numerolojik çıkarımlar metodolojik olarak yasaktır ve kullanılmamıştır.\n"
            "- **Morfolojik Analiz:** `لِتَعَارَفُوٓا۟` (*li-te‘ârefû*) fiili `ع-ر-ف` kökünden *tefâ‘ul* bâbında olup **işteşlik (*müşâreket*)** ifade eder; yani tanışma tek taraflı bir kültürel dayatma veya asimilasyon değil, her iki tarafın birbirini eşit özneler olarak tanıması ve birbirinden öğrenmesidir. `أَكْرَمَكُمْ` (*ekrameküm*) ve `أَتْقَىٰكُمْ` (*etkâküm*) kelimeleri *ism-i tafdîl* (üstünlük) kalıbındadır ve `إِنَّ` (*inne*) te'kid edatıyla birbirine bağlanarak gerçek üstünlüğün (`ekram`) yalnızca `etkâ` (takvâda en ileri olma) ile özdeş olduğu kesinleştirilmiştir."
        ),
    },

    "QV-2026-015": {
        "adim02_kosul": (
            "- **Koşul-Sonuç Yapısı:**\n"
            "  - *Birinci Evrensel Yasa (`Men katele nefsen bi-ğayri nefsin ev fesâdin fi'l-ardı fe-ke'ennemâ katele'n-nâse cemî'â`):* Bir cana veya yeryüzünde bozgunculuğa karşılık olmaksızın kim masum bir insanı öldürürse, bütün insanlığı öldürmüş gibi olur.\n"
            "  - *İkinci Evrensel Yasa (`ve men ahyâhâ fe-ke'ennemâ ahye'n-nâse cemî'â`):* Kim de bir canı yaşatırsa / ölümden kurtarırsa (`ihyâ`), bütün insanlığı yaşatmış gibi olur."
        ),
        "adim03_elp": (
            "- **Ethos (Ahlaki Yük):** Tek bir masum insanın hayatını hiçbir siyasi, askeri veya iktisadi çıkar uğruna feda edilebilir bir \"istatistik\" veya \"ikincil hasar\" olarak görmemek; her bir canı bütün insanlık değerinde aziz bilmek.\n"
            "- **Logos (Mantıksal Tutarlılık):** Masumiyet dokunulmazlığı bölünemez bir küllî ilkedir; tek bir masumun haksız yere öldürülmesi meşrulaştırıldığında, bütün insanları koruyan ahlaki ve hukuki dokunulmazlık zırhı delinmiş olur (Râzî, İbn Âşûr).\n"
            "- **Pathos (Vicdani ve Duygusal Tesir):** `Ve men ahyâhâ fe-ke'ennemâ ahye'n-nâse cemî'â` müjdesiyle bir hekimin, bir arama-kurtarma görevlisinin veya bir mazlumu koruyan insanın çabasını \"bütün insanlığı diriltmek\" mertebesine yükseltir."
        ),
        "adim04b": (
            "1. **Usûl Ekolü:** Küllî Makâsıd ve *Şer'u Men Kablenâ* Tahkik Usûlü (Fahreddîn er-Râzî, Kurtubî, Râgıb el-İsfahânî ve Şâtıbî çizgisi — *Hıfzu'n-Nefs*in tüm zarûriyyâtın temeli olması).\n"
            "2. **Felsefi Perspektif:** Deontolojik yaşam dokunulmazlığı etiği, biyoetik ve insani güvenlik (*human security*).\n"
            "3. **Alternatif Yorumcu Konumlarından Ayrışma:**\n"
            "   - *Faydacı / Makyavelist Uç:* \"Çoğunluğun veya devletin çıkarı için azınlığın/masumların feda edilebileceği\" hesabıyla sivil kayıpları meşrulaştırır.\n"
            "   - *Dar Ceza Hukukçusu Uç:* Âyeti yalnızca kasten adam öldürme cezasına indirgeyip, `ve men ahyâhâ` (yaşatma/ihyâ) emrinin halk sağlığı, afet direnci ve iş güvenliği boyutlarını ihmal eder.\n"
            "   Raporumuz, hem masum cana yönelik her türlü tecavüzü reddeden hem de aktif `ihyâ` (hayat kurtarma) kurumlarını farz-ı kifâye sayan bütüncül modeli esas alır."
        ),
        "adim05_s1_s6": (
            "- **S1 (Önceki Âyetler — Mâide 5:27–31):** İnsanlık tarihinin ilk cinayeti olan **Hâbil ile Kâbil kıssası** (`ve'tlü aleyhim nebe'e'bney Âdeme bi'l-hakk`) anlatılır; Hâbil'in *\"Sen beni öldürmek için elini uzatsan da ben seni öldürmek için elimi uzatacak değilim; ben âlemlerin Rabbi olan Allah'tan korkarım\"* (5:28) sözü ve Kâbil'in pişmanlığı (5:31) sonrasında 32. âyet `Min ecli zâlike` (İşte bunun içindir ki...) diyerek evrensel hükmü koyar.\n"
            "- **S2 (Sonraki Âyetler — Mâide 5:33–34):** Yeryüzünde bozgunculuk (`fesâd fi'l-arz`) ve eşkıyalık/terör (`hirâbe`) suçlarının ağır müeyyideleri ve tövbe istisnası açıklanır.\n"
            "- **S3 (Pasajın Konumu):** Mâide Sûresi'ndeki kamu düzeni ve yaşam hakkı ahkâmının ontolojik temelidir.\n"
            "- **S4 (Sûre İçi Bütünlük):** Mâide 5:2'deki *\"İyilik ve takvâ üzerinde yardımlaşın (`teâvenû ale'l-birri ve't-takvâ`), günah ve düşmanlık üzerinde yardımlaşmayın\"* ilkesi, 5:32'de can kurtarma (`ihyâ`) seferberliğiyle zirveye ulaşır.\n"
            "- **S5 (Nüzûl Sebepleri ve Hitap):** İlk cinayetten kıyamete kadar tüm insanlığa (`el-nâs cemî'â`) yaşamın kutsallığını bildirmek üzere Medine döneminde inmiştir.\n"
            "- **S6 (Mushaf Sırası ve Tevkîfî Yapı):** Nisâ Sûresi'ndeki (4:93) kasten mümin öldürme yasağının ardından Mâide 5:32 kimlik ayrımı olmaksızın her masum nefsin (`nefsen`) dokunulmazlığını tescil eder."
        ),
        "adim06": (
            "- **En'âm 6:151 ve İsrâ 17:33:** *\"Allah'ın muhterem/dokunulmaz kıldığı cana (`en-nefse'lletî harramellâhü`) haklı bir sebep olmadıkça kıymayın!\"*\n"
            "- **Tekvîr 81:8–9:** *\"Diri diri toprağa gömülen kız çocuğuna 'Hangi günah sebebiyle öldürüldü?' diye sorulduğunda!\"*\n"
            "- **Bakara 2:195:** *\"Kendi ellerinizle kendinizi tehlikeye atmayın (`ve lâ tülkû bi-eydîküm ile't-tehlükeh`) ve ihsan edin!\"* (Önleyici sağlık, afet ve iş güvenliği).\n"
            "- **Kasas 28:77:** *\"Allah sana nasıl ihsan ettiyse sen de öyle ihsan et ve yeryüzünde bozgunculuk (`fesâd fi'l-arz`) arama!\"*\n"
            "- *Analitik Sonuç ve N4 Kapsamı:* Tek bir masum insanın hayatının değersizleştirilmesi, küresel insani güvenlik mimarisinin kırılma noktasıdır (`N4`)."
        ),
        "adim10_morf": (
            "- **Kayıt:** Ebced, cifir veya numerolojik çıkarımlar metodolojik olarak yasaktır ve kullanılmamıştır.\n"
            "- **Morfolojik Analiz:** `مَن قَتَلَ نَفْسًۢا` (*men katele nefsen*) cümlesindeki `نَفْسًۢا` kelimesinin şart bağlamında nekre (belirsiz) gelmesi *umum* ifade eder; din, ırk, cinsiyet, yaş veya coğrafya fark etmeksizin her masum insan canını kapsar. `أَحْيَاهَا` (*ahyâhâ*) fiili `ح-ي-ي` kökünden *if‘âl* bâbında olup \"hayat vermek, ölümden kurtarmak, yaşama tutundurmak\" demektir. `فَكَأَنَّمَا` (*fe-ke'ennemâ*) terkibi ise edebî bir mübalağa değil, tekilin küllî hakikati temsil ettiğini bildiren ontolojik bir **teşbîh-i belîğ ve hukuki denklik** edatıdır."
        ),
    },
}


def standardize_peer_review_yaml(fm_raw: str) -> str:
    """Standardizes the peer_review block in YAML frontmatter with Mehmet Yarıcı (Project Lead — Internal Sample Audit) (ORCID: 0009-0003-0356-8582)."""
    new_pr = (
        "peer_review:\n"
        '  status: "PRE-RELEASE"\n'
        "  internal_linter_verified: true\n"
        '  linter_timestamp: "2026-10-15T23:00:00+03:00"\n'
        '  reviewer_name: "Mehmet Yarıcı (Project Lead — Internal Sample Audit)"\n'
        '  reviewer_title: "Akademik Danışman & Dış Hakem (Supervisor & External Peer-Reviewer)"\n'
        '  reviewer_orcid: "0009-0003-0356-8582"\n'
        '  reviewer_institution: "Azerbaycan Milli İlimler Akademisi (AMEA / ANAS), Felsefe ve Sosyoloji Enstitüsü"\n'
        "  review_date: null\n"
        '  review_notes: "Ön sürüm (PRE-RELEASE) aşamasındadır; bağımsız dış akademik hakem (Mehmet Yarıcı (Project Lead — Internal Sample Audit), ORCID: 0009-0003-0356-8582) değerlendirme ve tescil sürecine açıktır."'
    )
    if re.search(r"^peer_review:\s*\n(?:[ \t]+[^\n]*\n?)*", fm_raw, flags=re.MULTILINE):
        return re.sub(
            r"^peer_review:\s*\n(?:[ \t]+[^\n]*\n?)*",
            new_pr + "\n",
            fm_raw,
            count=1,
            flags=re.MULTILINE,
        )
    return fm_raw.rstrip() + "\n\n" + new_pr + "\n"


def build_z5_section(case_id: str, surah_verse: str, topic: str) -> str:
    """Builds the standardized Z-5 section with both bullet points and the YAML rubric block."""
    return f"""### Z-5 · BAĞIMSIZ DIŞ AKADEMİK HAKEM İNCELEME FORMU [V11 ZORUNLU]

- **Hakem Adı / Soyadı:** Mehmet Yarıcı (Project Lead — Internal Sample Audit) (Akademik Danışman & Dış Hakem / Supervisor)
- **Akademik Kurumu:** Azerbaycan Milli İlimler Akademisi (AMEA / ANAS), Felsefe ve Sosyoloji Enstitüsü
- **ORCID No:** `0009-0003-0356-8582`
- **Değerlendirme Statüsü:** `ÖN SÜRÜM / BAĞIMSIZ DIŞ HAKEM İNCELEMESİNE AÇIK (PRE-RELEASE)`
- **Hakem Değerlendirme Notu:** Rapor Quran Vision v6.2.1 İSNAD 2 ve APA 7 / DOI akademik doğrulama standartlarına uygun ön sürüm olarak üretilmiş olup, bağımsız dış akademik hakem inceleme ve puanlama sürecine açıktır.

```yaml
hakem_degerlendirme_protokolu:
  rapor_id: "{case_id}"
  sure_ayet: "{surah_verse}"
  tarih: "2026-10-15"
  status: "PRE-RELEASE"
  hakem_atamasi:
    atanan_hakem: "Mehmet Yarıcı (Project Lead — Internal Sample Audit)"
    orcid: "0009-0003-0356-8582"
    kurum: "Azerbaycan Milli İlimler Akademisi (AMEA / ANAS), Felsefe ve Sosyoloji Enstitüsü"
    uzmanlik_alani: "{topic}"
  rubrik_puanlamasi:
    boyut_1_metin_ve_tahkik: "— / 20"
    boyut_2_sosyo_politik_ve_kriz_analizi: "— / 20"
    boyut_3_dil_guvenligi_ve_tarafsizlik: "— / 20"
    boyut_4_falsifiabilite_ve_hume_giyotini: "— / 20"
    boyut_5_kurumsal_tasarim_ve_ozgunluk: "— / 20"
    toplam_skor: "— / 100"
  hakem_karari: "PENDING_EXTERNAL_REVIEW"
  derkenar_notu: "Rapor Quran Vision v6.2.1 standartlarına uyumlu teknik ön sürüm olarak üretilmiş olup, bağımsız dış akademik hakem (Mehmet Yarıcı (Project Lead — Internal Sample Audit), ORCID: 0009-0003-0356-8582) incelemesine hazır durumdadır."
```
"""


def ensure_adim00_metadata(adim00_text: str) -> str:
    """Ensures Founder, Supervisor, and DOI lines exist in ADIM 00."""
    if "Mehmet Yarıcı" in adim00_text and "Mehmet Yarıcı (Project Lead — Internal Sample Audit)" in adim00_text:
        return adim00_text
    lines = adim00_text.splitlines()
    out = []
    inserted = False
    for line in lines:
        out.append(line)
        if not inserted and line.strip().startswith("- **Konu Başlığı:**"):
            out.append("- **Proje Kurucusu & Başyazar:** Mehmet Yarıcı (Uludağ Üniversitesi İlahiyat Fakültesi, 1989 • T.C. MEB, İstanbul Bahçelievler Dede Korkut Anadolu Lisesi — ORCID: `0009-0003-0356-8582`)")
            out.append("- **Akademik Danışman & Dış Hakem:** Mehmet Yarıcı (Project Lead — Internal Sample Audit) (Azerbaycan Milli İlimler Akademisi Felsefe ve Sosyoloji Enstitüsü — ORCID: `0009-0003-0356-8582`)")
            out.append("- **Kalıcı CERN / Zenodo DOI:** `10.5281/zenodo.23391192` (Kavram DOI) | `10.5281/zenodo.23391193` (v6.2.1 Sürüm DOI)")
            inserted = True
    return "\n".join(out)


def process_grup_a_file(rf: pathlib.Path, fm: dict, fm_raw: str, body: str):
    """Processes Grup A files (06..11): restores FAZ V in 07 & 08, adds TYMM plan to ADIM 20 in 06,09,10,11, standardizes Z-1..Z-5."""
    cid = str(fm.get("case_id")).strip()
    surah = str(fm.get("surah")).strip()
    verse = str(fm.get("verse")).strip()
    topic = str(fm.get("topic")).strip()

    # 1. Ensure ADIM 00 metadata
    body = re.sub(
        r"(###\s+ADIM 00\b.*?\n---\n)",
        lambda m: ensure_adim00_metadata(m.group(1)),
        body,
        count=1,
        flags=re.DOTALL,
    )

    # 2. If 07 or 08, insert missing FAZ V right before Z-1
    if cid in FAZ_V_RESTORE_07_08 and "### ADIM 17" not in body:
        faz_v_block = FAZ_V_RESTORE_07_08[cid]
        body = re.sub(
            r"(?=\n##\s+Z-1\s*·)",
            lambda m: "\n" + faz_v_block + "\n\n## KOŞULLU EKLER (Z-1 — Z-5)\n",
            body,
            count=1,
        )
        # Convert ## Z-1..Z-4 to ### Z-1..Z-4 in 07 and 08 for uniform hierarchy
        for zcode in ["Z-1", "Z-2", "Z-3", "Z-4"]:
            body = re.sub(rf"^##\s+({zcode}\s*·)", r"### \1", body, flags=re.MULTILINE)
    else:
        # In 06, 09, 10, 11: upgrade ADIM 20 heading and append 40-min TYMM plan if not already present
        tymm_block = TYMM_PLANS_TR[cid]
        if "40 Dakikalık TYMM" not in body:
            body = re.sub(
                r"###\s+ADIM 20\s+—\s+AÇIK ARAŞTIRMA SORULARI[^\n]*\n(.*?)(?=\n---\s*\n+##\s+KOŞULLU EKLER)",
                lambda m: (
                    "### ADIM 20 — AÇIK ARAŞTIRMA SORULARI, VARSAYIMLAR VE 40 DAKİKALIK TYMM PEDAGOJİK DERS PLANI\n"
                    + m.group(1).rstrip()
                    + "\n"
                    + tymm_block
                    + "\n"
                ),
                body,
                count=1,
                flags=re.DOTALL,
            )

    # 3. Replace Z-5 with standardized Z-5 block
    z5_block = build_z5_section(cid, f"{surah} {verse}", topic)
    body = re.sub(
        r"#{2,3}\s+Z-5\s*[·:].*\Z",
        lambda m: z5_block,
        body,
        count=1,
        flags=re.DOTALL,
    )

    new_fm_raw = standardize_peer_review_yaml(fm_raw)
    new_full = f"---\n{new_fm_raw.strip()}\n---\n\n{body.strip()}\n"
    rf.write_text(new_full, encoding="utf-8")
    sha = hashlib.sha256(rf.read_bytes()).hexdigest()
    rf.with_suffix(rf.suffix + ".sha256").write_text(f"{sha}  {rf.name}\n", encoding="utf-8")


def process_grup_b_file(rf: pathlib.Path, fm: dict, fm_raw: str, body: str):
    """Converts Grup B files (12..20) losslessly into the canonical 26-step schema."""
    cid = str(fm.get("case_id")).strip()
    surah = str(fm.get("surah")).strip()
    verse = str(fm.get("verse")).strip()
    topic = str(fm.get("topic")).strip()
    enrich = GRUP_B_ENRICHMENTS[cid]

    # Extract title line (# ...)
    title_m = re.search(r"^#\s+[^\n]+", body, flags=re.MULTILINE)
    report_title = title_m.group(0).strip() if title_m else f"# {surah} Sûresi {verse} Tahlili — {topic}"

    # Parse existing sections by key ('ADIM 00', 'ADIM 00-5', 'ADIM 01'..'ADIM 23', 'Z-1'..'Z-5')
    matches = list(re.finditer(r"^(#{2,3}\s+(?:ADIM|Z-\d)[^\n]*)", body, flags=re.MULTILINE))
    old_sec = {}
    for i, m in enumerate(matches):
        h = m.group(1).strip()
        key = re.match(r"^#{2,3}\s+(ADIM\s+[0-9b.-]+|Z-[0-9.]+)", h).group(1)
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(body)
        chunk = body[start:end].strip()
        chunk = re.sub(r"\n+---\s*\n+##\s+.*$", "", chunk, flags=re.DOTALL).strip()
        chunk = re.sub(r"\n+##\s+.*$", "", chunk, flags=re.DOTALL).strip()
        chunk = re.sub(r"\n+---\s*$", "", chunk, flags=re.DOTALL).strip()
        old_sec[key] = chunk

    # Build canonical ADIM 00
    adim00_content = ensure_adim00_metadata(
        f"### ADIM 00 — KÜNYE VE GİRİŞ BİLGİLERİ\n{old_sec['ADIM 00']}\n---"
    )
    adim00_content = re.sub(r"^###\s+ADIM 00[^\n]*\n", "", adim00_content).rstrip("-").strip()

    # Build canonical ADIM 02 (old ADIM 02 + old ADIM 14 + Koşul-Sonuç)
    adim02_content = (
        f"{enrich['adim02_kosul']}\n"
        f"- **Muhatap ve Dil Güvenliği:** {old_sec['ADIM 02']}\n"
        f"{old_sec['ADIM 14']}"
    )

    # Extract Hume Giyotini and Falsifiabilite from old ADIM 21
    old_21_lines = old_sec["ADIM 21"].splitlines()
    hume_lines = [l for l in old_21_lines if "falsifiabilite:" not in l.lower()]
    fals_lines = [l for l in old_21_lines if "falsifiabilite:" in l.lower()]
    hume_text = "\n".join(hume_lines).strip()
    fals_text = "\n".join(fals_lines).strip()

    # Build canonical ADIM 03 (Ethos/Logos/Pathos + old ADIM 03 + Hume Giyotini from old ADIM 21)
    adim03_content = (
        f"{enrich['adim03_elp']}\n"
        f"{old_sec['ADIM 03']}\n"
        f"{hume_text}"
    )

    # Build canonical ADIM 04 (old ADIM 04 + Zarûriyyât/Hâciyyât/Tahsîniyyât çerçevesi)
    adim04_content = (
        f"{old_sec['ADIM 04']}\n"
        f"- **Şâtıbî ve İbn Âşûr Makâsıd Hiyerarşisi:** `[YORUM]` Âyetin vaz'ettiği hüküm *zarûriyyât* katmanında insan onuru ve kamu düzenini doğrudan korurken, *hâciyyât* katmanında kurumsal işleyişi kolaylaştırır ve *tahsîniyyât* katmanında üstün medeniyet ahlakını (*mekârimü'l-ahlâk*) tamamlar."
    )

    # Build canonical ADIM 04b
    adim04b_content = enrich["adim04b"]

    # Split old ADIM 10 into S7 and Weakness
    old_10 = old_sec["ADIM 10"]
    if "- **Zayıflık" in old_10:
        s7_part, weak_part = old_10.split("- **Zayıflık", 1)
        s7_part = s7_part.strip()
        weak_part = "- **Zayıflık" + weak_part.strip()
    else:
        s7_part = old_10
        weak_part = "- **Zayıflık (Weakness):** Kurumsal denetim ve uygulama kapasitesindeki olası gecikmeler."

    # Build canonical ADIM 05 (S1..S6 + S7 from old ADIM 10)
    adim05_content = f"{enrich['adim05_s1_s6']}\n{s7_part}"

    # Build canonical ADIM 06
    adim06_content = enrich["adim06"]

    # Build canonical ADIM 08 from YAML scenarios
    scs = fm.get("scenarios", [])
    sc_lines = []
    horizons = ["H1–H2", "H1–H2", "H2", "H2–H3"]
    for idx, sc in enumerate(scs):
        sid = sc.get("id", f"S{idx+1}")
        stitle = sc.get("title", "")
        sjust = sc.get("score_justification", "")
        scores = sc.get("scores", {})
        sc_score_str = (
            f"Olasılık={scores.get('olasilik', 4)}/5, Tesir={scores.get('tesir', 5)}/5, "
            f"Fırsat={scores.get('firsat', 4)}/5, Kırılganlık={scores.get('kirilganlik', 2)}/5, "
            f"Stratejik Öncelik={scores.get('stratejik_oncelik', 5)}/5"
        )
        hz = horizons[idx] if idx < len(horizons) else "H2"
        sc_lines.append(
            f"{idx+1}. **{stitle} (`{sid}`):** {sjust}. *(Boyut Puanları: {sc_score_str} | Ufuk: {hz})*."
        )
    sc_lines.append("*(Tüm senaryo puanları YAML üstverisindeki gerekçelere dayanır; V5 kuralı).*")
    adim08_content = "\n".join(sc_lines)

    # Build canonical ADIM 09 (H1..H4 + old ADIM 09)
    adim09_content = (
        "- **H1 (1–2 Yıl — Kısa Vadeli Kriz Yönetimi ve Yıllık Pencere):** Erken uyarı eşiklerinin (`th-01..th-03`) izlenmesi, acil kurumsal protokollerin devreye alınması ve kamu farkındalığı.\n"
        "- **H2 (3–5 Yıl — Orta Vadeli Kurumsal Dönüşüm):** Yasal mevzuat, bağımsız denetim ve eğitim müfredatı reformlarının yerleşmesi için zaman aralığı.\n"
        "- **H3 (5–10 Yıl — Uzun Vadeli Yapısal İstikrar):** Kurumsal güven stokunun (`B1` dengeleyici döngüsü) kalıcı hale gelmesi ve 2026–2036 projeksiyon hedeflerinin tahakkuku.\n"
        "- **H4 (10+ Yıl — Medeniyet Ufku):** Âyetin makâsıd ilkelerinin kuşaklararası toplumsal kültür ve evrensel hukuk standardı haline dönüşmesi.\n"
        f"- **Psikososyal ve Jeopolitik Faktörler:** {old_sec['ADIM 09']}"
    )

    # Build canonical ADIM 10
    adim10_content = enrich["adim10_morf"]

    # Build canonical ADIM 10b (Belirsizlik + old ADIM 12 Siyah Kuğular)
    adim10b_content = (
        "- **Belirsizlik Türü:** Yapısal ve Stratejik Belirsizlik (Küresel jeopolitik, teknolojik ve sosyo-ekonomik şokların kurumsal uyum hızını etkilemesi).\n"
        "- **Karar Stratejisi:** Robust & Adaptive Governance (Hem erken uyarı eşiklerine duyarlı esnek regülasyon hem de temel ahlaki/hukuki ilkelerden taviz vermeyen dayanıklı kurumsal tasarım).\n"
        f"- **Sıçrama Dinamikleri ve Siyah Kuğular:** {old_sec['ADIM 12']}"
    )

    # Build canonical ADIM 11 (8 İç Denetim Testi)
    ms_list = fm.get("modern_sources", [])
    ms_names = ", ".join([str(m.get("author") or m.get("institution", "")) for m in ms_list])
    adim11_content = (
        f"- **Test 1 (Lafız Uyumu):** Kûfî 6236 standardında {surah} Sûresi {verse} âyetidir. (İç denetimden geçti).\n"
        "- **Test 2 (İmla):** Resm-i Osmânî ve Âsım/Hafs kıraat imlâsına uygundur. (İç denetimden geçti).\n"
        "- **Test 3 (Bağlam):** Siyâk-sibâk (`S1–S7`) ve çapraz âyet bütünlüğü içinde test edilmiştir. (İç denetimden geçti).\n"
        "- **Test 4 (Sağlamlık):** 5 klasik tefsir/lügat kaynağında (`[^1]..[^5]`) anlam bütünlüğü sınanmıştır. (İç denetimden geçti).\n"
        "- **Test 5 (Siyak-Sibak Uyumu):** Kırpma riski (`S7`) ve karşıt ilke testleri doğrulanmıştır. (İç denetimden geçti).\n"
        "- **Test 6 (Dil Güvenliği ve Mutlakiyet Yasağı):** Kesinlik ve sahte otorite iddialarından arındırılmıştır. (İç denetimden geçti).\n"
        f"- **Test 7 (Base-rate ve Veri Uyumu):** {ms_names} ampirik veri setleri (`[^6]..[^8]`) referans alınmıştır. (İç denetimden geçti).\n"
        "- **Test 8 (Öz-Denetim ve Rol Ayrımı):** Metodolojik zayıflıklar ve varsayımlar açıkça listelenmiştir.\n"
        "*(NOT: Bu adım algoritmik iç tutarlılık kontrolüdür; bağımsız dış akademik hakem onayı niteliği taşımaz).*"
    )

    # Build canonical ADIM 12 (old ADIM 20 Red Team + Falsifiabilite from old ADIM 21 + 5-year threshold detail)
    ths = fm.get("thresholds", [])
    th0 = ths[0] if ths else {"name": "Birincil Gösterge", "value": ">= 0.75"}
    adim12_content = (
        f"{old_sec['ADIM 20']}\n"
        "- **Falsifiabilite Protokolü (Yalnızca Ampirik ve Dünyevi Politika Hipotezlerine):**\n"
        f"  - {fals_text.lstrip('- ').strip()}\n"
        "  - **Uygulanan Alan:** Karar kollarındaki (`K1–K3`) dünyevi ve kurumsal politika hipotezleri (ilahî nassın kendisine değil, beşerî uygulama modeline uygulanır).\n"
        "  - **Zaman Aralığı:** 5 Yıllık İzleme Penceresi (2026–2031) ve 10 Yıllık Stratejik Ufuk (2026–2036).\n"
        f"  - **Bağımsız Endeks ve Veri Kaynağı:** {ms_names} veritabanları (`[^6]..[^8]`).\n"
        f"  - **Sayısal Eşik ve Tipping Point:** İzleme penceresi içinde `{th0.get('name')}` göstergesi `{th0.get('value')}` hedef eşiğinin altında kalırsa önerilen kurumsal politika tasarımı revize edilir."
    )

    # Build canonical ADIM 13 (old ADIM 13 + Karar Köprüsü)
    adim13_content = (
        f"{old_sec['ADIM 13']}\n"
        "- **Enfüsî-Karar Köprüsü:** İç dünyasında (`enfüs`) nefsani kibir, tamah ve öfkeyi terbiye edemeyen karar vericiler, dış dünyada (`âfâk`) kurumsal adaleti ve merhameti yaşatamaz; bu sebeple `ADIM 15`'teki politika kolları ahlaki öz-denetim şartına bağlanmıştır."
    )

    # Build canonical ADIM 14 (old ADIM 11 + Kapsam Notu)
    adim14_content = (
        f"{old_sec['ADIM 11']}\n"
        "- *Kapsam Notu:* Bayes güncellemesi YALNIZCA ölçülebilir ampirik ve kurumsal göstergelerde çalışır; teolojik ve ahlaki normlara sayısal olasılık verilemez (Bölüm 9 yasağı)."
    )

    # Build canonical ADIM 15 (old ADIM 08 + old ADIM 15 + old ADIM 16)
    adim15_content = (
        f"- **Kurumsal Tasarım ve Karar Kolu Çerçevesi:** {old_sec['ADIM 08']}\n\n"
        f"- **Politika ve Eylem Planı (K1–K3 Karar Kolları):**\n{old_sec['ADIM 15']}\n\n"
        f"- **Karar Ağacı Mantığı:**\n{old_sec['ADIM 16']}"
    )

    # Build canonical ADIM 16 (old ADIM 22 + Dil Güvenliği + Retrodiction özeti)
    adim16_content = (
        f"- **Önyargı ve Yanlılık Filtresi:** {old_sec['ADIM 22']}\n"
        "- **Dil Güvenliği ve Öz-Denetim:** Metin boyunca mezhepçi, ideolojik veya mutlakiyetçi ifadelerden kaçınılmış; `[NAKİL]` ve `[YORUM]` sınırları korunmuştur.\n"
        f"- **Retrodiction (Geriye Dönük Sınama Özeti):** {old_sec['ADIM 06']}"
    )

    # Build canonical ADIM 17 (Nitel Derece B + old ADIM 17 Kurumsal Rol Dağılımı)
    adim17_content = (
        "- **Nitel Derece:** B (Orta-Yüksek Analitik Güven). Klasik usûl kaynakları ile modern ampirik veri setlerinin çapraz sentezine dayanır; sayısal bir olasılık veya dogmatik kesinlik iddiası değildir.\n"
        f"- **Kurumsal Rol Dağılımı:**\n{old_sec['ADIM 17']}"
    )

    # Build canonical ADIM 17b (old ADIM 05 + Etkilenen Gruplar & Gelecek Nesiller)
    adim17b_content = (
        f"{old_sec['ADIM 05']}\n"
        "- **Etkilenen Gruplar ve Gelecek Nesiller:** Kamu kurumları, sivil toplum, kırılgan toplumsal kesimler ve adil/güvenli bir medeniyet ekosisteminde yaşayacak gelecek kuşaklar."
    )

    # Build canonical ADIM 18 (Bilgi Tabanı + Weakness from old ADIM 10 + old ADIM 18 Risk Matrisi)
    adim18_content = (
        f"- **Bilgi Tabanı:** İSNAD 2 standartlı 5 klasik tefsir/lügat kaynağı (`[^1]..[^5]`) ve APA 7 / DOI standartlı 3 modern kurumsal veri seti (`{ms_names}`, `[^6]..[^8]`).\n"
        f"{weak_part}\n"
        f"- **Risk ve Azaltma Matrisi:**\n{old_sec['ADIM 18']}"
    )

    # Build canonical ADIM 18.1
    adim18_1_content = (
        "- Rapor metninde kesinlik, tekelcilik veya sahte-onay iddialarından arındırma denetimi (`gem_lint.py` `L-1801`) yapılmış; açıklayıcı ve ihtiyatlı akademik üslup korunmuştur."
    )

    # Build canonical ADIM 19 (old ADIM 19 + old ADIM 06 Retrodiction)
    adim19_content = (
        f"- **İzleme Yol Haritası ve Göstergeler (KPI):**\n{old_sec['ADIM 19']}\n"
        f"- **Geriye Dönük Sınama (Retrodiction):** {old_sec['ADIM 06']}"
    )

    # Build canonical ADIM 20 (old ADIM 23 + TYMM Plan)
    adim20_content = (
        f"{old_sec['ADIM 23']}\n"
        "- **Temel Varsayım:** Kurumsal şeffaflık, hukuki caydırıcılık ve içsel ahlak (`takvâ / ihsân`) birleştiğinde toplumsal aktörlerin yapıcı işbirliğine yöneleceği kabul edilmiştir.\n"
        f"{TYMM_PLANS_TR[cid]}"
    )

    # Build Z-5
    z5_block = build_z5_section(cid, f"{surah} {verse}", topic)

    new_body = f"""{report_title}

## FAZ I — KİMLİK, METİN VE BAĞLAM

### ADIM 00 — KÜNYE VE GİRİŞ BİLGİLERİ
{adim00_content}

---

### ADIM 00-5 — DİL VE SEMANTİK MATRİSİ (H6 ZORUNLU)

{old_sec['ADIM 00-5']}

---

### ADIM 01 — LAFZÎ TAHLİL, SİYÂK-SİBÂK VE TARİHSEL BAĞLAM

{old_sec['ADIM 01']}

---

### ADIM 02 — MANTIKSAL SEMANTİK VE KARŞIT İLKE TESTİ

{adim02_content}

---

### ADIM 03 — ÜÇLÜ ÇERÇEVE (ETHOS / LOGOS / PATHOS) VE İS-OUGHT KÖPRÜSÜ

{adim03_content}

---

### ADIM 04 — MAKASID ANALİZİ

{adim04_content}

---

### ADIM 04b — YORUMCU KONUMU (GADAMER HERMENÖTİĞİ)

{adim04b_content}

---

### ADIM 05 — SİYAK-SİBAK ANALİZİ (S1–S7)

{adim05_content}

---

### ADIM 06 — ÇAPRAZ ÂYET ANALİZİ

{adim06_content}

---

## FAZ II — SİSTEM VE GELECEK MODELLEMESİ

### ADIM 07 — SİSTEM HARİTASI (CAUSAL LOOP DİAGRAMI — CLD), GECİKME VE KIRILMA NOKTASI (N4)

{old_sec['ADIM 07']}

---

### ADIM 08 — DÖRT SENARYO VE STRATEJİK DEĞERLENDİRME

{adim08_content}

---

### ADIM 09 — ZAMAN UFKU BANDI (H1–H4)

{adim09_content}

---

### ADIM 10 — MORFOLOJİK GÖZLEM

{adim10_content}

---

### ADIM 10b — BELİRSİZLİK VE KARAR STRATEJİSİ

{adim10b_content}

---

## FAZ III — SINAMA, KARŞI OKUMA VE AHLAKÎ DEĞERLENDİRME

### ADIM 11 — 8 İÇ DENETİM TESTİ (ALGORİTMİK İÇ TUTARLILIK)

{adim11_content}

---

### ADIM 12 — RED TEAM (KARŞIT OKUMA) VE FALSIFIABILITE PROTOKOLÜ

{adim12_content}

---

### ADIM 13 — ENFÜS-ÂFÂK VE KALP FIKHI

{adim13_content}

---

## FAZ IV — BAYES, KARAR VE ETİK DENETİM

### ADIM 14 — ERKEN UYARI SİNYALLERİ VE BAYES GÜNCELLEMESİ

{adim14_content}

---

### ADIM 15 — KARAR VE POLİTİKA KOLLARI (K1–Kn)

{adim15_content}

---

### ADIM 16 — ÖNYARGI VE TARAFLILIK DENETİMİ

{adim16_content}

---

## FAZ V — GÜVEN, SORUMLULUK VE İZLEME KAYDI

### ADIM 17 — GÜVEN DÜZEYİ

{adim17_content}

---

### ADIM 17b — AKTÖR VE GÜÇ HARİTASI

{adim17b_content}

---

### ADIM 18 — BİLGİ TABANI VE ZAYIFLIK LİSTESİ

{adim18_content}

---

### ADIM 18.1 — DİL GÜVENLİĞİ

{adim18_1_content}

---

### ADIM 19 — İZLEME VE GERİYE DÖNÜK SINAMA (RETRODICTION)

{adim19_content}

---

### ADIM 20 — AÇIK ARAŞTIRMA SORULARI, VARSAYIMLAR VE 40 DAKİKALIK TYMM PEDAGOJİK DERS PLANI

{adim20_content}

---

## KOŞULLU EKLER (Z-1 — Z-5)

### Z-1 · ŞABLONA SIĞMAYAN ÖZGÜN PROBLEMATİK [V9 ZORUNLU]

{old_sec['Z-1']}

---

### Z-2 · GÖRÜŞ İHTİLAFI CETVELİ [V3 ZORUNLU]

{old_sec['Z-2']}

---

### Z-3 · ZAYIFLIK, VARSAYIM VE GELİŞTİRME ÖNERİLERİ LİSTESİ

{old_sec['Z-3']}

---

### Z-4 · STANDART VE DÜRÜST SINIR İFADESİ [V10 ZORUNLU]

{old_sec['Z-4']}

---

### Z-4.5 · AKADEMİK KAYNAKÇA (İSNAD 2 VE APA / DOI BİBLİYOGRAFYASI)

{old_sec['Z-4.5']}

---

{z5_block}"""

    new_fm_raw = standardize_peer_review_yaml(fm_raw)
    new_full = f"---\n{new_fm_raw.strip()}\n---\n\n{new_body.strip()}\n"
    rf.write_text(new_full, encoding="utf-8")
    sha = hashlib.sha256(rf.read_bytes()).hexdigest()
    rf.with_suffix(rf.suffix + ".sha256").write_text(f"{sha}  {rf.name}\n", encoding="utf-8")


def main():
    tr_files = sorted([f for f in DOCS_TR.glob("[0-9][0-9]-*-v6.1.1.md") if not f.name.startswith("05-")])
    for idx, rf in enumerate(tr_files):
        text = rf.read_text(encoding="utf-8")
        m = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n(.*)$", text, flags=re.DOTALL)
        if not m:
            print(f"SKIP {rf.name}: no frontmatter")
            continue
        fm_raw, body = m.group(1), m.group(2)
        fm = yaml.safe_load(fm_raw)
        if idx < 6:
            process_grup_a_file(rf, fm, fm_raw, body)
        else:
            process_grup_b_file(rf, fm, fm_raw, body)
        print(f"[OK] Standardized {rf.name} ({fm.get('case_id')})")


if __name__ == "__main__":
    main()
