[English](METHOD.md) | **Türkçe**

# Quran Vision — 26 Adımlı Analiz Yöntemi ve 5 Makro Faz

> **Not:** Bu belge yöntemin genel mimarisini ve adım dizinini özetler. Ayrıntılı metodolojik kurallar, epistemik sınır şartları ve V1–V12 doğrulama modülleri için güncel kanonik şartname belgesine bakınız:  
> 🔗 **[Quran Vision v6.2.1 Kanonik Şartname Belgesi (Markdown)](QURAN_VISION_v6.2.1_SPECIFICATION.md)** | **[Tam Talimatname Metni (.txt)](docs/QURAN_VISION_v6.2.1_TAM_TALIMAT.txt)**

---

## Makro Fazlar ve Analiz Adımları (Katman 3)

Quran Vision mimarisi, 26 analiz adımını bilişsel bütünlüğü korumak amacıyla **5 Makro Faz** altında düzenler:

### Faz I — Kimlik, Metin ve Bağlam
- **Adım 00 — Künye ve Giriş Bilgileri:** Vaka kodu, âyet, konu, tarih, katman, H6, güven düzeyi.
- **Adım 00-5 — Dil ve Semantik Matrisi (H6 Zorunlu):** Kök anlam (*İbn Fâris* / *Râgıb*), Kur'an semantiği, nahiv/belâğat (*Zemahşerî*) ve klasik lisan (*İbn Manzûr*). `[NAKİL]` ve `[YORUM]` ayrımı zorunludur.
- **Adım 01 — Lafzî Tahlil:** Arapça metin, gramer ve mealler.
- **Adım 02 — Mantıksal Semantik ve Karşıt İlke:** Önerme yapısı, maslahat tartımı ve sınır tayini.
- **Adım 03 — Üçlü Çerçeve (Ethos / Logos / Pathos) ve Olgu-Değer Köprüsü:** Hume Giyotini denetimi.
- **Adım 04 — Makasıd Analizi:** Zarûriyyât, hâciyyât, tahsîniyyât (Şâtıbî ve İbn Âşûr çerçevesi).
- **Adım 04b — Yorumcu Konumu (Gadamer Hermenötiği):** Usûl tercihi, önkabuller ve alternatif ekollerin muhtemel sonuçları.
- **Adım 05 — Siyak-Sibak Analizi (S1–S7):** S1 (Önceki âyet), S2 (Sonraki âyet), S3 (Pasaj konumu), S4 (Sûre bütünlüğü), S5 (Nüzul teması), S6 (Tarihsel bağlam), S7 (Kırpma riski emniyeti).
- **Adım 06 — Çapraz Âyet Analizi:** Metin içi tahsis, takyid ve paralellikler.

### Faz II — Sistem ve Gelecek Modellemesi
- **Adım 07 — Sistem Haritası (CLD):** Causal Loop Diagramı, pekiştirici (R) ve dengeleyici (B) döngüler, gecikmeler.
- **Adım 08 — Dört Senaryo:** Koruyucu, Yozlaşma, Denge/Çözülme ve İhya/Dönüşüm senaryoları.
- **Adım 09 — Zaman Ufku Bandı:** H1 (0–3 yıl), H2 (3–10 yıl), H3 (10–30 yıl), H4 (30+ yıl medeniyet ufku).
- **Adım 10 — Morfolojik Gözlem:** Dilbilimsel/morfolojik frekans özellikleri (Ebced ve numeroloji yasaktır).
- **Adım 10b — Belirsizlik ve Karar Stratejisi:** Knightian belirsizlik, robust ve koruyucu stratejiler.

### Faz III — Sınama, Karşı Okuma ve Ahlakî Değerlendirme
- **Adım 11 — Sekiz İç Denetim Testi:** Algoritmik iç tutarlılık denetimleri.
- **Adım 12 — Red Team ve Sınanabilirlik Protokolü:** Karşıt okumalar ve Popperci ampirik politika testi ($P(E|H)$).
- **Adım 13 — Enfüs-Âfâk ve Kalp Fıkhı:** İçsel-ahlakî yöneliş (enfüs) ile dış şartlar (âfâk) ilişkisi; niyet ve vicdan muhasebesi; fıkhî hükümle karıştırılmayan işârî derinlik.

### Faz IV — Bayes, Karar ve Etik Denetim
- **Adım 14 — Erken Uyarı Sinyalleri ve Bayes Güncellemesi:** `EU-01..EU-n` sinyalleri, doğrulanmış/öznel prior ayrımı ve likelihood hesaplaması.
- **Adım 15 — Karar Kolları ve Kaldıraç Bağlantısı:** CLD döngülerine bağlı politika araçları, Meadows kaldıraç noktaları ve trade-off analizi.
- **Adım 16 — Önyargı ve Taraflılık Denetimi:** Doğrulama yanlılığı, anakronizm ve apologetik savunma filtreleri.

### Faz V — Güven, Sorumluluk ve İzleme Kaydı
- **Adım 17 — Güven Düzeyi:** A / B / C nitel güven derecelendirmesi.
- **Adım 17b — Aktör Haritası:** Güç odakları, karar vericiler, etkilenenler ve gelecek nesiller.
- **Adım 18 — Bilgi Tabanı ve Zayıflıklar:** İddia statüleri ve yöntemin sınırları.
- **Adım 18.1 — Dil Güvenliği:** Kesinlik ve sahte-onay iddialarından arındırma.
- **Adım 19 — İzleme ve Geriye Dönük Sınama (Retrodiction):** Tarihsel vaka doğrulama ve KPI takibi.
- **Adım 20 — Açık Sorular ve Varsayımlar:** Çözülmemiş sorular listesi.

---

## Koşullu Ekler (Z-1 — Z-5)

- **Z-1 — Özgün Problematik (Aporia):** Âyetin analitik şablona sığmayan derin teolojik ve felsefî açmazı.
- **Z-2 — Görüş İhtilafı Cetveli:** En az 3 farklı klasik mezhep ve çağdaş ekolün karşılaştırmalı matrisi.
- **Z-3 — Zayıflık ve Geliştirme Önerileri:** Analizin açıkça ilan edilen eksiklikleri.
- **Z-4 — Standart Sınır Beyanı:** Raporun fetva veya ilahî muradın tek tefsiri olmadığını bildiren zorunlu şerh.
- **Z-4.5 — Akademik Kaynakça (İSNAD 2 ve APA / DOI Bibliyografyası):** Klasik İslami kaynakların İSNAD 2. Edisyon kurallarıyla (vefat yılı `ö. H/M`, muhakkik, neşir yeri/yılı), çağdaş ampirik kaynakların ise APA 7 / DOI standardıyla alfabetik listelendiği ve metin içi dipnotların (`[^1]`, `[^2]`) çözümlendiği kaynakça bölümü.
- **Z-5 — Hakem ve Akran Değerlendirme Kaydı:** Dış bağımsız akademik değerlendirme kütüğü (`DRAFT`, `PRE-RELEASE`, `EXTERNALLY-REVIEWED`).
