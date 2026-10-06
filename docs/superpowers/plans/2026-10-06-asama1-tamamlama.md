# Aşama 1 tamamlama — uygulama planı

> Ajan çalışanlar için: superpowers:executing-plans ile görev görev uygulanır. Adımlar `- [ ]` ile izlenir.

**Hedef:** GELISIM-PLANI.md'deki Aşama 1'in açık maddelerini (A1.1, A1.2, A1.3, A1.7 kısmi, A1.8 testleri, A1.9, A1.10 düzeltmesi, A1.12) kapatıp M3'e geçilebilir bir temel bırakmak.

**Mimari:** İçerik JSON dosyalarında kalır; şema `lib/learning-types.ts` içinde genişletilir, doğrulama `scripts/verify-content.mjs` içinde zorunlu hâle gelir. Saf mantık (`lib/quiz-engine.ts`, `lib/answer-check.ts`) Node ile doğrudan test edilir; arayüz `components/learning-app.tsx` içinde güncellenir.

**Teknoloji:** Next/vinext (Vite), React 19, Zod, Pyodide 0.27 (Python 3.12), Node 24 (`.ts` dosyalarını doğrudan çalıştırır).

**Doğrulama komutları (her görev sonunda):**
- `npm run test:learning` → tüm `✓` satırları, çıkış kodu 0
- `npm run verify:content` → "tüm çıktılar doğru"
- `npx tsc --noEmit -p .` → çıktı yok

---

## Başlangıç durumu (6 Ekim 2026 incelemesi)

- Commit'lenmemiş yarım iş: `lib/quiz-engine.ts` (A1.8), `components/progress-backup.tsx` (A1.10), ilerleme şeması v3.
- `npm run test:learning` kırık: test v2 bekliyor, şema v3.
- `tsc` hatası: `progress-backup.tsx:12` — `document.body.append` Workers tipleriyle çakışıyor.
- `quiz-engine.ts` için hiç regresyon testi yok.
- İçerik hataları: m1-q02 açıklaması bozuk; `or` anlatımı eksik; M2 f-string örneği `%70%` üretiyor; "Kurulum" bölümünde kurulum yok; "tam eşleşme için in" yanlış.

## Görev 0 — Yarım işi kararlı hâle getir (A1.8, A1.10)

**Dosyalar:** `components/progress-backup.tsx`, `scripts/test-learning.mjs`

- [ ] `document.body.append(link)` → `document.body.appendChild(link)`; tsc temiz.
- [ ] Test: v1 kaydı v3'e taşınır (beklenen sürüm 3).
- [ ] Testler (quiz-engine): test oturumunda tüm sorular yanıtlanmadan `finishQuiz(...,"submitted")` sonucu değiştirmez; süre dolunca `expireQuiz` bir kez kayıt ekler, ikinci çağrı yeni kayıt/XP eklemez; tamamlanmış oturumda `answerQuiz` etkisizdir; soru listesi `structuredClone` ile sabittir (kaynak dizi değişse de oturum değişmez); başarılı test `unlockedModule` değerini artırır.
- [ ] Testler (yedek): `exportProgress` → `importProgress` gidiş-dönüşü aynı ilerlemeyi verir; yanlış `app` alanı reddedilir.

## Görev 1 — İçerik düzeltmeleri (A1.12)

**Dosyalar:** `content/module-01.json`, `content/module-02.json`

- [ ] m1-q02 açıklaması: "7'nin içinde 3 tane tam 2 vardır; kalan 1 atılır, sonuç 3'tür."
- [ ] `comparison-logic` açıklaması: `or` truthy yoksa son değeri döndürür; `"" or "misafir"` örneği.
- [ ] `repl-syntax` açıklaması: python.org kurulumu, `python --version` (Windows'ta `py --version`), REPL'i açma/kapama (`exit()`), dosyayı `python dosya.py` ile çalıştırma; sitedeki editörün tarayıcıda Python 3.12 çalıştırdığı.
- [ ] m2 `formatting.realCode`: başta fazladan `%` kaldırılır → çıktı `  7/10  · 70%`; satır açıklaması güncellenir.
- [ ] m2 `methods.alternatives`: "Alt metin var mı diye bakmak için in…".
- [ ] `npm run verify:content` geçer.

## Görev 2 — Şema ve kayıt genişletme (A1.2, A1.3)

**Dosyalar:** `lib/learning-types.ts`, `lib/content.ts`, `content/*.json`, `scripts/verify-content.mjs`, `scripts/annotate-content.mjs` (tek seferlik)

- [ ] Tipler: `Question` → `sectionId: string`, `difficulty: 1|2|3`, `acceptedAnswers?: string[]`, `optionFeedback?: Record<string,string>`. `LessonSection` → `objectives: string[]`, `prerequisites: string[]`. `LearningModule` → `contentVersion: number`.
- [ ] 80 sorunun her biri bir ders bölümüne (`sectionId`) ve zorluğa bağlanır (konu→bölüm eşlemesi; kod ve traceback soruları zorluk 2-3).
- [ ] `content.ts`: `import.meta.glob("../content/module-*.json", { eager: true })` ile keşif; modüller `id` ile sıralanır. "İlk iki modül hazır" metni sayıdan türetilir.
- [ ] Doğrulayıcı: her sorunun `sectionId` değeri modülde var; `difficulty` 1–3; `optionFeedback` anahtarları seçeneklerde var ve doğru cevabı içermiyor; `acceptedAnswers` cevabı içeriyor; fill için `solutionCode` her kabul edilen cevapla da çalışıyor; yazma görevlerinin `sectionId` değerleri geçerli; modül kimlikleri 1..n ardışık.

## Görev 3 — Yanlıştan derse bağlantı (A1.9)

**Dosyalar:** `components/learning-app.tsx`, `lib/learning-types.ts`

- [ ] `LessonView` dışarıdan `sectionId` alabilir (`python-iz-open` olayına isteğe bağlı `sectionId`).
- [ ] Pratik geri bildiriminde yanlış cevapta ve sonuç incelemesinde "Dersi aç: <bölüm başlığı>" düğmesi.
- [ ] İstatistiklerde zayıf konu satırları ilgili bölüme bağlanır.
- [ ] Zayıf tekrar: hiç denenmemiş (çözülmemiş) ve yanlış öğrenilmiş sorular ayrı sayılır; kart metni bunu söyler.

## Görev 4 — Çoklu cevap ve seçenek gerekçesi (A1.7 kısmi)

**Dosyalar:** `lib/answer-check.ts` (yeni), `components/learning-app.tsx`, `content/*.json`, `scripts/test-learning.mjs`

- [ ] `isAnswerCorrect(question, value)`: fill için boşluk normalize edilmiş, `acceptedAnswers` dahil karşılaştırma.
- [ ] Bug ve traceback sorularına yanlış seçenek başına gerekçe (`optionFeedback`); pratikte seçilen yanlış seçeneğin gerekçesi gösterilir, testte sonuç ekranında.
- [ ] Testler: `isAnswerCorrect` kabul/ret vakaları.
- [ ] Açık kalan: gerçek traceback metninden satır seçme soru tipi (ayrı görev; M3 öncesi).

## Görev 5 — Kapsam matrisi (A1.1)

**Dosyalar:** `content/coverage.json` (yeni), `scripts/coverage-report.mjs` (yeni), `package.json`

- [ ] 18 modülün alt başlıkları; her biri `status: planlandı|yazıldı|doğrulandı|yayınlandı`, `sections: [...]`.
- [ ] Rapor: modül başına alt başlık / bağlı bölüm / soru / yazma görevi sayısı; bağlanmamış bölüm veya bilinmeyen kimlik varsa çıkış kodu 1.
- [ ] `npm run coverage`.

## Görev 6 — Belgeleri güncelle

- [ ] GELISIM-PLANI.md: kapanan maddeler `[x]`, kalanlar ve doğrulama sayıları.

## Bu planın dışında kalanlar (sıradaki)

A1.7 traceback satır seçimi, A1.12 kalan anlatım denetimi (tam metin okuması), ardından Aşama 2 (M3–M5).
