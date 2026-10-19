# 🏛️ QURAN VISION v6.2.2 — OFFICIAL METHODOLOGICAL LINTER AUDIT REPORT
## Resmi Metodolojik Linter Denetim Tutanağı (V1–V14 & Z-1..Z-5 Katalog Devamlılığı)

- **Denetim Motoru / Verification Engine:** [`src/gem_lint.py`](src/gem_lint.py) (`GemLinterV6` — `v6.2.2` Canonical Standard)
- **Denetlenen Külliyat / Audited Corpus:** 15 Kurucu Monografi (`QV-2026-001` – `QV-2026-015`, 15 TR + 15 EN = 30 Rapor, Katman 3, H6 Zorlu Âyet Standardı)
- **Proje Kurucusu & Başyazar / Founder & Principal Author:** **Mehmet Yarıcı** (`ORCID: 0009-0003-0356-8582`)
- **Akademik Danışman & Dış Hakem / Academic Advisor & External Peer-Reviewer:** **Mehmet Emin Koç** (`ORCID: 0000-0002-1025-5643`)
- **Kalıcı CERN / Zenodo DOI:** [`10.5281/zenodo.23410818`](https://doi.org/10.5281/zenodo.23410818) *(Concept DOI: [`10.5281/zenodo.23391192`](https://doi.org/10.5281/zenodo.23391192))*
- **Kriptografik Ana Manifesto / Master Hash Ledger:** [`SHA256SUMS.txt`](SHA256SUMS.txt) (`sha256sum -c SHA256SUMS.txt`)
- **Nihai Denetim Sonucu / Final Audit Verdict:** **🟢 30 / 30 GEÇTİ — TOPLAM KESİCİ HATA (BLOCK): `0`**

---

## 📊 1. Külliyat Katalog Devamlılığı ve Linter Doğrulama Tablosu (`QV-2026-001` .. `QV-2026-015`)

| Vaka Kodu | Sûre & Âyet (TR / EN) | Türkçe Rapor Dosyası (`docs/tr/`) | 26 Adım & `Z-1..Z-5` | İSNAD 2 Klasik | APA 7 / DOI | Bayesyen `P(S1) → P(S1\|E)` | Kelime (TR / EN) | Harici `.sha256` Özeti (İlk 16 Hane) | `BLOCK` |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- | :---: |
| **QV-2026-001** | **Tevbe 9:5** (*At-Tawbah 9:5*) | [`06-pilot-tevbe-95-v6.1.1.md`](docs/tr/06-pilot-tevbe-95-v6.1.1.md) | ✅ **26/26 + Z-1..Z-5** | 5 | 3 | `%42 → %77 (+35)` | 6,165 / 8,396 | `6752607a3bca098f…` | **0** |
| **QV-2026-002** | **Nisâ 4:34** (*An-Nisa 4:34*) | [`07-pilot-nisa-434-v6.1.1.md`](docs/tr/07-pilot-nisa-434-v6.1.1.md) | ✅ **26/26 + Z-1..Z-5** | 5 | 3 | `%36 → %71 (+35)` | 7,089 / 8,551 | `f4ebd0832f65ae1a…` | **0** |
| **QV-2026-003** | **Mâide 5:38** (*Al-Ma'idah 5:38*) | [`08-pilot-maide-538-v6.1.1.md`](docs/tr/08-pilot-maide-538-v6.1.1.md) | ✅ **26/26 + Z-1..Z-5** | 5 | 2 | `%38 → %75 (+37)` | 6,564 / 8,030 | `16396c17569043ef…` | **0** |
| **QV-2026-004** | **Bakara 2:256** (*Al-Baqarah 2:256*) | [`09-rapor-bakara-2256-v6.1.1.md`](docs/tr/09-rapor-bakara-2256-v6.1.1.md) | ✅ **26/26 + Z-1..Z-5** | 5 | 2 | `%38 → %78 (+40)` | 6,056 / 7,875 | `3c577569b84ac51e…` | **0** |
| **QV-2026-005** | **Nisâ 4:58** (*An-Nisa 4:58*) | [`10-rapor-nisa-458-v6.1.1.md`](docs/tr/10-rapor-nisa-458-v6.1.1.md) | ✅ **26/26 + Z-1..Z-5** | 5 | 2 | `%35 → %77 (+42)` | 6,094 / 8,075 | `a788a5619d231092…` | **0** |
| **QV-2026-006** | **Âl-i İmrân 3:159** (*Ali 'Imran 3:159*) | [`11-rapor-ali-imran-3159-v6.1.1.md`](docs/tr/11-rapor-ali-imran-3159-v6.1.1.md) | ✅ **26/26 + Z-1..Z-5** | 5 | 2 | `%40 → %78 (+38)` | 6,241 / 7,993 | `bd4ce3fd4c9e893c…` | **0** |
| **QV-2026-007** | **Hucurât 49:9-10** (*Al-Hujurat 49:9-10*) | [`12-rapor-hucurat-49910-v6.1.1.md`](docs/tr/12-rapor-hucurat-49910-v6.1.1.md) | ✅ **26/26 + Z-1..Z-5** | 5 | 3 | `%35 → %62 (+27)` | 6,429 / 8,101 | `4fc4c683f8d2f611…` | **0** |
| **QV-2026-008** | **İsrâ 17:36** (*Al-Isra 17:36*) | [`13-rapor-isra-1736-v6.1.1.md`](docs/tr/13-rapor-isra-1736-v6.1.1.md) | ✅ **26/26 + Z-1..Z-5** | 5 | 3 | `%30 → %65 (+35)` | 6,533 / 8,173 | `603d51246e0e3f35…` | **0** |
| **QV-2026-009** | **Haşr 59:7** (*Al-Hashr 59:7*) | [`14-rapor-hasr-597-v6.1.1.md`](docs/tr/14-rapor-hasr-597-v6.1.1.md) | ✅ **26/26 + Z-1..Z-5** | 5 | 3 | `%20 → %68 (+48)` | 6,630 / 8,269 | `6e1b6962f1ed2544…` | **0** |
| **QV-2026-010** | **Rûm 30:22** (*Ar-Rum 30:22*) | [`15-rapor-rum-3022-v6.1.1.md`](docs/tr/15-rapor-rum-3022-v6.1.1.md) | ✅ **26/26 + Z-1..Z-5** | 5 | 3 | `%25 → %72 (+47)` | 6,468 / 8,022 | `49145fc9cc34382a…` | **0** |
| **QV-2026-011** | **En'âm 6:151-152** (*Al-An'am 6:151-152*) | [`16-rapor-enam-6151152-v6.1.1.md`](docs/tr/16-rapor-enam-6151152-v6.1.1.md) | ✅ **26/26 + Z-1..Z-5** | 5 | 4 | `%22 → %75 (+53)` | 6,900 / 8,627 | `48845b16e68c9c6b…` | **0** |
| **QV-2026-012** | **Hadîd 57:25** (*Al-Hadid 57:25*) | [`17-rapor-hadid-5725-v6.1.1.md`](docs/tr/17-rapor-hadid-5725-v6.1.1.md) | ✅ **26/26 + Z-1..Z-5** | 5 | 4 | `%20 → %74 (+54)` | 7,275 / 8,385 | `ca5eddea828eb910…` | **0** |
| **QV-2026-013** | **Nahl 16:90** (*An-Nahl 16:90*) | [`18-rapor-nahl-1690-v6.1.1.md`](docs/tr/18-rapor-nahl-1690-v6.1.1.md) | ✅ **26/26 + Z-1..Z-5** | 5 | 4 | `%24 → %76 (+52)` | 7,458 / 8,501 | `da5adffcf4be7918…` | **0** |
| **QV-2026-014** | **Hucurât 49:13** (*Al-Hujurat 49:13*) | [`19-rapor-hucurat-4913-v6.1.1.md`](docs/tr/19-rapor-hucurat-4913-v6.1.1.md) | ✅ **26/26 + Z-1..Z-5** | 6 | 4 | `%28 → %81 (+53)` | 7,486 / 8,561 | `d11ea9c84399ccb9…` | **0** |
| **QV-2026-015** | **Mâide 5:32** (*Al-Ma'idah 5:32*) | [`20-rapor-maide-532-v6.1.1.md`](docs/tr/20-rapor-maide-532-v6.1.1.md) | ✅ **26/26 + Z-1..Z-5** | 6 | 4 | `%26 → %82 (+56)` | 7,686 / 8,943 | `c0fd69abdde6170a…` | **0** |
| **TOPLAM / ORTALAMA ($\mu$)** | **15 Kurucu Âyet** | **15 TR + 15 EN Monografi** | ✅ **%100 Şablon Uyumu** | **77 Nakil** | **46 Veri Seti** | **`%31 → %74 (+43 μ)`** | **101,074 / 124,502** | [`SHA256SUMS.txt`](SHA256SUMS.txt) | **0** |

---

## 🛡️ 2. Doğrulanan Metodolojik Kapılar (`V1–V14` & `L-0100..L-2303`)

1. **Bölüm ve Şablon Tamlığı (`L-0201` / `L-2003`):** 15 raporun (30 TR+EN dosyasının) tamamında **5 Makro Faz**, **26 Analiz Adımı** (`Adım 00`, `Adım 00-5`, `Adım 01` .. `Adım 20`) ve **6 Koşullu/Zorunlu Ek** (`Z-1 Aporia`, `Z-2 İhtilaf Cetveli`, `Z-3 Zayıflıklar`, `Z-4 Sınır Beyanı`, `Z-4.5 Çift Katmanlı Bibliyografya`, `Z-5 Hakem Kaydı`) eksiksiz mevcuttur; sıfır şablon kayması (`0 drift`) teyit edilmiştir.
2. **İSNAD 2 Klasik Tefsir, Nokta Atışı `page_id` ve APA 7 / DOI Doğrulaması (`V1` — `L-0101..L-0107`):** Toplam **77 birincil Arapça klasik kaynak** (müellif, hicrî/milâdî vefat yılı, eser, muhakkik, yayınevi, cilt/sayfa, 100% lafzî harekeli Arapça ibare, URN / Katalog Kodu ve `shamela.ws/book/<book_id>/<page_id>` formatında nokta atışı doğrulanmış Al-Maktaba Al-Shamela dijital kütüphane bağlantısı — `L-0107 BLOCK`) ile **46 çağdaş kurumsal veri seti** (APA 7 ve çalışan kurumsal URL/DOI) doğrulanmıştır.
3. **Adım 13 İrfânî Reform ve 3'lü Bütünlük Kapısı (`V14` — `L-2301..L-2303`):** 15 monografinin tamamında (TR ve EN) `### ADIM 13 — ENFÜSÎ-ÂFÂKÎ DİYALEKTİK VE KALP FIKHI (İRFÂNÎ / İŞÂRÎ KATMAN)` bölümü; `13.1. Enfüsî-Âfâkî Diyalektik`, `13.2. Kalp Fıkhı ve Bâtınî İlletler` ve `13.3. Nefis Mertebeleri ve İrfânî Dönüşüm (Seyr ü Sülûk)` alt başlıklarıyla ve birincil klasik irfânî/işârî kaynaklarla (Kuşeyrî, Gazzâlî, Muhâsibî, Râgıb el-İsfahânî, Mâverdî, İbn Kayyim, Sehl et-Tüsterî, İbn Acîbe, Bursevî, Âlûsî) teçhiz edilmiştir.
4. **Epistemik Ayrım ve Dil Güvenliği (`V2` & `İlke 3` — `L-0100`, `L-0301`):** Tüm raporlarda `[NAKİL]` (`[CITATION]`) ve `[YORUM]` (`[ANALYSIS]`) ayrımı ile mutlaklık/fetva dili yasağı denetlenmiştir.
5. **Sayısal Tutarlılık ve Koşullu Bayesyen Kalibrasyon (`V5`, `V6`, `V8` & `İlke 5`):** Her raporun `Adım 14` metin içi Bayesyen güncellemesi ($P(S_1) \rightarrow P(S_1|E)$), web kokpiti (`Tab 1`), sentez matrisi (`Tab 5`) ve `README.md` kataloğu birebir eşitlenmiştir. Külliyat genel ortalaması **15 Raporun Aritmetik Ortalaması ($\mu$): `%31 → %74 (+43 puan)`** olarak açıkça ayrıştırılmıştır.
6. **Harici Kriptografik Hash Disiplini (`V4` — `L-0401..L-0404`):** Kendi kendine referans paradoksu (*self-referential hash paradox*) oluşmaması için YAML üst-verisindeki `sha256_hash` alanı `0000...` yer tutucusu olarak korunmuş; gerçek kriptografik özetler harici `docs/tr/*.md.sha256`, `docs/en/*.md.sha256` ve kök dizindeki [`SHA256SUMS.txt`](SHA256SUMS.txt) manifestosuna kaydedilmiştir.
7. **İçerik Yoğunluğu ve Nedensel Döngü Derinliği (`V12` & `V13` — `L-2101..L-2207`):** Her raporda `Adım 01` lafzî tahlil derinliği (harekeli Arapça blok alıntı, bütüncül meal, $\ge 6$ transliterasyonlu kelime tahlili) ve `Adım 07` Sistem Haritası (`R1` pekiştirici döngü, `B1` dengeleyici döngü, gecikme, kaldıraç ve `N4` erken uyarı sinyali) algoritmik olarak doğrulanmıştır.

---

## 💻 3. Bağımsız Tekrarlanabilirlik ve Doğrulama Komutları (Reproducibility Protocol)

Herhangi bir dış hakem veya araştırmacı, aşağıdaki iki standart komutla külliyatın hem metodolojik iç tutarlılığını hem de kriptografik dosya bütünlüğünü kendi yerel terminalinde saniyeler içinde doğrulayabilir:

```bash
# 1. 30 kurucu raporun (15 TR + 15 EN) tamamında V1-V14 ve Z-1..Z-5 Linter denetimini çalıştır (Beklenen: BLOCK = 0)
python -X utf8 src/gem_lint.py --all

# 2. 33 PDF, 30 Markdown raporu, docs/index.html ve talimatnamelerin harici SHA-256 özetlerini doğrula
sha256sum -c SHA256SUMS.txt
```
