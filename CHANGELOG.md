# Değişiklik Geçmişi (Changelog)

Bu belgede GEM (Kur'an Temelli Gelecek Vizyonu / Quran Vision) çerçevesinin sürüm değişiklikleri belgelenmektedir.

---

## [v6.2.2] — 2026-10-20 (İrfânî/İşârî Hermenötik Reformu, Lafzî Şâmile `page_id` Mimarisi ve 33. Rehber Belgesi)

> **Official Release Note:** `v6.2.2: Complete Irfani/Sufi Hermeneutics Reform across 15 monographs (Step 13), 100% verbatim classical Arabic quotes with exact page_id Shamela links, comprehensive Hadith/Ayat/Ulama tahrij in body text, addition of 33rd document (ISNAD-2 Classical Arabic Databases Guide authored by Mehmet Yarıcı), and compiled master corpus books.`

### Eklenen ve Güncellenen Hususlar
- **Adım 13 İrfânî / İşârî Hermenötik Reformu (15/15 TR & EN Monografi):** Külliyattaki 15 Türkçe ve 15 İngilizce monografinin tamamında (`QV-2026-001` – `QV-2026-015`) `ADIM 13` / `STEP 13` bölümü `13.1 (Enfüsî-Âfâkî Diyalektik)`, `13.2 (Kalp Fıkhı ve Bâtınî İlletler — Muhâsibî, Gazzâlî, Râgıb)` ve `13.3 (Klasik İşârî ve İrfânî Tahrîc — Kuşeyrî, Sehl et-Tüsterî, İbn Acîbe harekeli Arapça iktibas ve İSNAD 2 künyesi)` alt başlıklarıyla birleşik olarak yeniden yapılandırıldı.
- **%100 Lafzî Arapça İktibas ve Nokta Atışı Şâmile `page_id` Bağlantıları:** 77 klasik Arapça kaynak alıntısının tamamı el-Mektebetü'ş-Şâmile'deki orijinal ibareyle harfi harfine (`nakl bi'l-lafz`) eşitlendi ve tüm `verification_link` bağlantıları `https://shamela.ws/book/<book_id>/<page_id>` standardına yükseltildi.
- **`TALIMATNAME.md` ve `src/gem_lint.py` Zırhlandırması (Kontrol A & Kontrol B):** Gelecek âyet monografileri (`QV-2026-016+`) için 4 bağlayıcı kural `TALIMATNAME.md` anayasasına işlendi; `src/gem_lint.py` içine sayfa ID'siz genel Şâmile kapak linklerini reddeden **Kontrol A (`L-0107 BLOCK`)** ve Adım 13 üçlü irfânî yapıyı denetleyen **Kontrol B (`L-2301..L-2303 BLOCK`)** eklendi.
- **33. Belge (`ISNAD_2_Klasik_Arapca_Veritabanlari_Rehberi.pdf`) ve Tam Külliyat Kitapları (`v6.2.2`):** Mehmet Yarıcı tarafından kaleme alınan *İSNAD-2 Klasik Arapça Dijital Veri Tabanları ve Tahkik Rehberi* (CC-BY-4.0) 33. A4 PDF olarak derlendi ve web portalının Kaynakça sekmesine entegre edildi; `Quran_Vision_Kulliyat_v6.2.2.pdf` ve `Quran_Vision_Corpus_EN_v6.2.2.pdf` tek cilt külliyat kitapları üretildi.

---

## [v6.2.1] — 2026-10-15 (Akademik Atıf & İSNAD 2 Hibrit Bibliyografya / Academic Citations)

### Eklenen ve Güncellenen Hususlar
- **İnteraktif Dijital Külliyat ve Karar Destek Kokpiti (`docs/index.html` & `src/build_portal.py`):** 15 raporun tamamını, Bayesyen olasılık sıçramalarını, Z-1 Aporia kutularını, İSNAD 2 harekeli Arapça ibare kartlarını ve 26 adımlı tam metinleri tek tıkla tarayıcıda (ve GitHub Pages üzerinde) çalıştıran modern web portalı inşa edildi.
- **12., 13., 14. ve 15. Stratejik Analiz Raporları (Hadîd 57:25, Nahl 16:90, Hucurât 49:13 & Mâide 5:32):** Külliyat 15 kurucu monografiye tamamlandı.
- **GEM Akademik Atıf ve Kaynakça Standardı (İSNAD 2 + Veri Bilimi Hibriti):** 15 stratejik analiz raporunun tamamı çift katmanlı akademik kaynakça ve metin içi dipnot mimarisine kavuşturuldu.
- **Kriptografik Güvenlik ve Linter Uyumu:** 15 raporun tamamında `gem_lint.py --katman 3 --h6` ile **0 KESİCİ HATA (BLOCK: 0)** teyit edildi; harici `.sha256` manifestoları ve test paketi (9/9) tam senkronize edildi.

---

## [v6.2.0] — 2026-10-15 (Stratejik Külliyat / Corpus Release)

### Eklenen ve Güncellenen Hususlar
- **11 Raporluk Tam Stratejik Külliyat (Corpus Expansion):** GEM v6.1.1 standardına tam uyumlu, 26 adımlı, Katman 3 ve H6 Zorlu Âyet denetimlerinden 0 KESİCİ (BLOCK) hata ile geçmiş 11 resmi rapor yayımlandı.
- **Akademik Hakem Rehberi ve Değerlendirme Rubriği:** 5 boyutlu, her biri 20 puanlık resmi değerlendirme kılavuzu (`docs/tr/akademik-hakem-rehberi.md`) sisteme eklendi.

---

## [v6.1.1] — 2026-10-15 (Taslak / Standard Draft)

### Eklenen ve Güncellenen Hususlar
- **Adım 13 (Enfüs-Âfâk ve Kalp Fıkhı):** İçsel-ahlakî yöneliş (enfüs) ile toplumsal/kurumsal şartlar (âfâk) analitik mercekle ayrıştırıldı.
- **Beş Makro Faz & Manifest Mimarisi:** 5 Makro Faz (Faz I–V) ve harici `.sha256` manifest yapısı tanımlandı.

---

## [v6.0.0] — 2026-10-14 (Mimari Reform)

- **V1–V11 Doğrulama Modülleri, Filolojik Tahkik (`[NAKİL]` / `[YORUM]`), Hermenevtik Çoğulculuk (Z-2), Aporia (Z-1) ve Hume Giyotini (V8)** sisteme eklendi.
