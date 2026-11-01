# GEM Akademik Hakem Değerlendirme Rehberi ve İnceleme Rubriği

Bu belge; Kur'an Temelli Gelecek Vizyonu (GEM v6.2.1) mimarisi çerçevesinde hazırlanan Katman 3 raporlarını inceleyecek bağımsız ilahiyat, tefsir, fıkıh ve kamu politikası akademisyenleri için standart değerlendirme protokolünü ve puanlama rubriğini düzenler.

---

## 1. Hakemliğin Amacı ve Epistemik Sınırlar

GEM çerçevesinde kod tabanlı iç denetim (`gem_lint.py`) yalnızca biçimsel dosya yapısını, anahtar kelimeleri ve dil güvenliği filtrelerini tarar. **Linter, hiçbir tefsirî iddianın ilmî doğruluğunu, kaynakların sıhhatini veya usûlî geçerliliğini onaylayamaz.**

Bir raporun `PRE-RELEASE` (Ön Sürüm) statüsünden **`EXTERNALLY-REVIEWED` (Akademik Hakem İncelemesinden Geçmiş)** statüsüne yükseltilebilmesi için, alanında uzman bağımsız bir akademisyenin aşağıdaki 5 boyutlu rubrik üzerinden raporu inceleyip yazılı değerlendirme kaydı bırakması zorunludur.

> **Önemli İlke (Otorite Sınırı):** Hakem onayı, raporun "ilahî muradın yegâne ve mutlak doğrusu" olduğunu tescillemez; raporun akademik usûle, filolojik tahkike ve bilim felsefesine uygun meşru bir araştırma modellemesi olduğunu teyit eder.

---

## 2. Beş Boyutlu Akademik Değerlendirme Rubriği

Hakemler, raporu aşağıdaki 5 ana boyut ve alt kriterler üzerinden değerlendirir:

### Boyut 1: Filolojik Tahkik ve Kaynak Sıhhati (V1 & V2)
- [ ] **Kaynak Künyesi:** Kullanılan klasik eserlerin neşir yılı, tahkik edeni, yayınevi ve cilt/sayfa numaraları matbu nüshalarla uyuşuyor mu?
- [ ] **Arapça İbare Doğruluğu:** Metne alınan Arapça ibareler tahrifatsız, bağlamından koparılmadan asıl kaynaktan mı aktarılmış?
- [ ] **[NAKİL] / [YORUM] Ayrımı:** Klasik müfessirin kendi lafızları `[NAKİL]` altında korunmuş mu? Modern analistin kavramsal çıkarımları `[YORUM]` altında dürüstçe ayrıştırılmış mı? Müfessire modern sosyolojik kavramlar söyletilerek anakronizm yapılmış mı?

### Boyut 2: Hermenevtik Çoğulculuk ve Mezhepler Matrisi (V3 & Z-2)
- [ ] **İhtilaf Temsili:** Z-2 cetvelinde en az 3 farklı klasik mezhep (Hanefî, Şâfiî, Mâlikî/Hanbelî) ile çağdaş ekollerin görüşleri tarafsızca özetlenmiş mi?
- [ ] **Tekelcilik Yasağı:** Analist kendi benimsediği yaklaşımı nassın tek zorunlu neticesi gibi sunmaktan kaçınmış mı?

### Boyut 3: Bilim Felsefesi ve Hume Giyotini (V8)
- [ ] **Olgu-Değer Ayrımı:** Âyetin normatif hükmü ile ondan türetilen dünyevî kamu politikası hipotezi ayrılmış mı?
- [ ] **Sınırlandırılmış Yanlışlanabilirlik:** Popperci yanlışlanabilirlik ($P(E|H)$) âyetin kendisine değil, yalnızca 5 yıllık izleme penceresindeki ampirik politika kollarına uygulanmış mı?

### Boyut 4: Aporia ve Problematik Derinliği (V9 & Z-1)
- [ ] **Şablona Sığmayan Gerilim:** Âyete özgü teolojik kriz (nesh tartışmaları, lafzî gerilimler, ahlaki aporialar) şablon içinde buharlaştırılmadan Z-1 bölümünde dürüstçe itiraf edilmiş mi?
- [ ] **Enfüs-Âfâk / Kalp Fıkhı (Adım 13):** İçsel vicdani muhasebe ile dış toplumsal şartlar arasındaki bağ fıkhî hükümle karıştırılmadan ele alınmış mı?

### Boyut 5: Sistem Dinamiği ve Politika Kolları (Adım 07 & Adım 15)
- [ ] **Kaldıraç Köprüsü:** Adım 07'deki Causal Loop döngüleri ile Adım 15'teki Karar Kolları mantıksal bir nedensellik bağıyla birleştirilmiş mi?
- [ ] **Eşikler:** Ampirik olmayan politika eşikleri açıkça `[TAHMİNÎ EŞİK]` olarak etiketlenmiş mi?

---

## 3. Hakem Karar Türleri

| Karar Kodu | Karar | Anlamı ve İşlem |
|---|---|---|
| **ACC-01** | **Kabul (Accept)** | Rapor akademik standartlara uygundur; hiçbir düzeltme gerekmeksizin `EXTERNALLY-REVIEWED` statüsüne yükseltilir. |
| **REV-02** | **Düzeltme (Revise & Resubmit)** | Kaynak tahkiki, tercüme veya usûlî dengede eksiklikler vardır; belirtilen maddeler düzeltildikten sonra yeniden incelenir. |
| **REJ-03** | **Red (Reject)** | Ağır anakronizm, metin tahrifatı, mezhep taassubu veya Hume Giyotini ihlali tespit edilmiştir; bu formatla yayımlanamaz. |

---

## 4. Rapor Z-5 Hakem Değerlendirme Formu Şablonu

İncelemeyi tamamlayan hakem, raporun sonundaki `Z-5` bölümüne aşağıdaki resmi değerlendirme kaydını işler:

```markdown
## Z-5 · HAKEM VE AKRAN DEĞERLENDİRME KAYDI [V11 ZORUNLU]

- **Hakem Adı / Soyadı:** Prof. Dr. / Doç. Dr. [İsim Soyisim]
- **Akademik Ünvanı ve Kurumu:** [Üniversite / Fakülte / Anabilim Dalı]
- **ORCID No:** 0000-000X-XXXX-XXXX
- **Değerlendirme Tarihi:** YYYY-MM-DD
- **İncelenen Rapor Sürümü ve SHA-256 Hash'i:** [64 Haneli Hash]
- **Hakem Kararı:** `KABUL (ACCEPT - EXTERNALLY-REVIEWED)`
- **Hakem Değerlendirme Raporu Özeti:**
  > "Bu çalışma; GEM v6.2.1 metodolojisi çerçevesinde incelenmiş olup, klasik tefsir nakillerinin tahkiki matbu nüshalarla karşılaştırılmıştır. [NAKİL] ve [YORUM] ayrımı titizlikle korunmuş; Z-2 Görüş İhtilafı Cetveli'nde klasik ve çağdaş ekoller dengeli biçimde temsil edilmiştir. Âyetin normatif ilkesi ile ampirik politika hipotezleri Hume Giyotini kuralına uygun olarak ayrılmıştır. Rapor, bağımsız akademik usûl standartlarını karşılamaktadır."
- **Kriptografik İmza (İsteğe Bağlı):** GPG Key Fingerprint / Git Signed Commit
```

---

## 5. GEM Akademik Atıf ve Kaynakça Standardı (İSNAD 2 + Veri Bilimi Hibriti)

GEM raporlarının hem geleneksel ilahiyat fakültelerinde (İSNAD Atıf Sistemi) hem de uluslararası hakemli indekslerde (Scopus / WoS / Chicago) en üst düzey meşruiyet kazanması için aşağıdaki iki katmanlı kaynakça mimarisi uygulanır:

### 5.1. Klasik İslami Kaynaklar (İSNAD 2 Standardı)
Klasik tefsir, hadis, fıkıh ve lügat kaynakları için müellifin vefat tarihi (hicrî ve miladî olarak `ö. H/M`), muhakkiki, matbu neşir künyesi, cilt/sayfa numarası ve orijinal Arapça nakil (`[NAKİL]`) zorunludur:
- **Format:** Müellif Soyadı, Adı (ö. Vefat Yılı). *Eser Adı*. thk. Muhakkik Adı. Basım Yeri: Yayınevi, Basım Yılı, Cilt/Sayfa.
- *Örnek (İSNAD):* Zemahşerî, Mahmûd b. Ömer (ö. 538/1144). *el-Keşşâf 'an Hakâ'ikı Gavâmizi't-Tenzîl*. thk. Âdil Ahmed Abdülmevcûd - Ali Muhammed Muavvaz. Riyad: Mektebetü'l-Ubeykân, 1998, 2/488-494.

### 5.2. Çağdaş Literatür ve Ampirik Veri Kaynakları (DOI / URL Standartlı)
Metinde atıf yapılan uluslararası endeksler, iktisat ve sosyoloji raporları ile bilimsel yayınlar müstakil bir modern kaynak kimliğiyle kaydedilir:
- **Format:** Yazar/Kurum Adı. *Rapor/Eser Başlığı*. Yayıncı/Organizasyon, Yayın Yılı, URL / DOI.
- *Örnek:* World Justice Project (WJP). *Rule of Law Index 2025-2026*. Washington, D.C.: WJP Publications, 2025, https://worldjusticeproject.org.

### 5.3. Metin İçi Dipnotlama ve Rapor Sonu Kaynakçası
1. **Metin İçi Dipnotlar (`[^1]`, `[^2]`):** Kritik nassî nakiller ve ampirik veri iddiaları standart Markdown dipnotlarıyla metne işlenir.
2. **Akademik Kaynakça Bölümü:** Her raporun Z-4 Sınır Beyanı sonrasında, kaynakların tam bibliyografik künyelerini içeren alfabetik "Akademik Kaynakça / Bibliography" tablosu yer alır.

