# Devir notu — Python İz

Son güncelleme: 6 Ekim 2026. Bu not, projeyi devralan kişinin ya da ajanın nereden devam edeceğini anlaması için yazıldı. Ayrıntılı yol haritası ve her teslimin günlüğü [GELISIM-PLANI.md](GELISIM-PLANI.md) dosyasındadır; bu not onun kısa giriş kapısıdır.

## 1. Proje ne?

Türkçe, tarayıcıda çalışan bir Python öğrenme sitesi. Öğrenci 18 modül boyunca ders okur, kodu tarayıcıda (Pyodide) çalıştırır, soru çözer, yazma görevleri yapar ve modül testlerini geçerek sonraki modülün kilidini açar. Hedef: hem kod okumak hem de sıfırdan kod yazmak.

- Yığın: Next 16 / vinext (Vite), React 19, Zod 3, CodeMirror, Pyodide 0.27 (Python 3.12.7) bir Web Worker'da. İlerleme localStorage'da (şema v3).
- Kullanıcı Türkçe konuşuyor; içerik ve yanıtlar Türkçe.

## 2. Şu anki durum (özet)

| | Durum |
|---|---|
| İçerik modülleri | **M1–M10 hazır** (`content/module-01.json` … `module-10.json`) |
| Soru | 400 (modül başına 40) |
| Yazma görevi | 30 (modül başına 3: Tamamla, Düzelt, Sıfırdan yaz) |
| Kapsam haritası | 109 alt başlıktan 70'i doğrulanmış (%64); `npm run coverage` |
| Doğrulama | 1082 çalıştırılabilir içerik kontrolü, 205 regresyon kontrolü, 168 yazma referans vakası, `tsc` ve `build` başarılı; büyük paket uyarısı sürüyor |
| Git/yayın | M10 öncesi değişiklikler korunmuştur. Güncel commit ve yayın durumunu git ve Sites üzerinden kontrol et; yayın kaynak kaydı oluşturur. |

## 3. Sıradaki iş

Plan sırasına göre bir sonraki içerik modülü **M11 OOP 1**'dir. Alt başlıkları `content/coverage.json` içinde `"id": 11` altında. M10 tamamlandı: kaynak ve ortam etiketleri bu modülde bulunur; subprocess yalnız yerel Python için okuma örneğidir. M10 JSON'u doğrudan düzenlenir; M8/M9 üreticileri M10'u üretmez.

Kullanıcı şimdiye kadar her seferinde arayüz işleri yerine bir sonraki içerik modülünü seçti, ama karar onundur. Bekleyen arayüz işleri:

- Görselleştirme 1 (döngü/değişken tablosu, sığ/derin kopya), Görselleştirme 2 (call stack)
- ~~Atölye 1–3~~ (yapıldı), Atölye 4 (M10 sonrası), Atölye 5 (M12), Atölye 6 (M16)
- ~~Ara sınav 1–2~~ (yapıldı), Ara sınav 3 (M1–M12), Ara sınav 4 (M1–M16). Yeni bir ara sınav ya da atölye için kod yazmaya gerek yok; `content/milestones.json`'a veri eklenir (bkz. bölüm 12).
- M8 için sanal dosya yükleme/indirme ve hazır örnek dosyalar
- Aşama 4: yerel geliştirme rehberi ve ortam etiketleri (Tarayıcıda çalışır / yerel Python gerekir)

Aşama 1'den açık kalanlar: A1.5 fonksiyon dönüş değeri testleri (kısmen: başlangıç kodunda çağrı + print verilerek print eden çözümler eleniyor); A1.6 test vakalarını çözümden önce gizleme; A1.7 traceback satır seçimi; A1.12 M1–M2 tam metin denetimi.

## 4. Komutlar

`D:\Python\python-iz` içinde:

```bash
npm run verify:content   # tüm ders/soru/görev kodlarını Pyodide'de çalıştırıp beklenen çıktıyla karşılaştırır
npm run test:learning    # regresyon testleri + yazma görevlerinin referans çözüm / başlangıç kodu kontrolleri
npm run coverage         # kapsam haritası özeti
npx tsc --noEmit -p .
npm run build
```

- Önizleme sunucusu: `D:\Python\.claude\launch.json` içindeki `python-iz` yapılandırması (port 5173). launch.json üst klasördedir, proje klasöründe değil.
- Git "dubious ownership" hatası verirse global ayarı değiştirmeden `git -c safe.directory=D:/Python/python-iz ...` kullan.
- `npm run lint` hataları önceden vardı (`module` değişken adı, effect içinde setState, purity); yeni kod yeni lint hatası eklemedi.

## 5. Mimari — bilinmesi gerekenler

- **İçerik keşfi:** `lib/content.ts`, `import.meta.glob("../content/module-*.json")` ile modülleri otomatik bulur. Yeni modül için yalnızca JSON dosyası eklemek yeter; menüde "hazır" görünür. Modül kimlikleri 1'den ardışık olmalı.
- **Şema:** `lib/learning-types.ts`. Bölüm alanları: `id, title, eyebrow, objectives, prerequisites, summary, explanation, code, expectedOutput, why, alternatives, traps, realCode, realOutput, lineByLine`. Önkoşul aynı modülde `"bolum-id"`, başka modülde `"m4:dicts"` biçimindedir. Soru alanları: `id (m<n>-qNN), type, topic, sectionId, difficulty (1–3), prompt, code, options, answer, expectedOutput, expectedError, optionFeedback, acceptedAnswers, solutionCode, lines, tests, starterCode, exampleInput, hints, explanation`.
- **Yazma görevleri:** `content/writing-tasks.json`; kimlik `m<n>-wN`.
- **Cevap denetimi:** `lib/answer-check.ts`. Boşluk doldurmada `acceptedAnswers`'tan biri kabul edilir. Sıralama soruları çalıştırılıp çıktıyla karşılaştırılır; aynı çıktıyı veren her sıralama doğrudur. Kod soruları `tests` ile değerlendirilir.
- **Python çalışma zamanı:** `public/python-runtime.js`, hem tarayıcı Worker'ı (`public/py-worker.js`) hem de Node doğrulayıcıları tarafından paylaşılır. Her çalıştırmada:
  - temiz ad alanı ve sahte `input()` (stdin satırları; satır biterse `EOFError`), 20.000 karakter çıktı sınırı;
  - boş bir geçici çalışma klasörü (M8 için eklendi) — çalıştırma sonunda silinir;
  - çalışma klasöründen import edilen modüller `sys.modules`'ten silinir, `sys.path` ve `os.environ` geri yüklenir, başta `importlib.invalidate_caches()` (M9 için eklendi).
  - Bu bir güvenlik sandbox'ı değildir.
- **Doğrulayıcı** (`scripts/verify-content.mjs`): bölüm `code`/`realCode`, çıktı soruları, fill/order/code `solutionCode`'ları, tüm `tests` ve `expectedError` kodlarını çalıştırır. Bug soruları **çalıştırılmaz** (bu yüzden terminal komutu ya da çalıştırılamayan senaryo içerebilir). Hata adı traceback'in son satırından okunur; modül önekli adlar da tanınır (`json.decoder.JSONDecodeError` → `JSONDecodeError`).

## 6. Her yeni modül için kalite standardı

Önceki modüllerin hepsi bu standarda göre yazıldı; M10 ve sonrası da öyle olmalı.

- 8 bölüm; her bölümde kazanım, önkoşul, açıklama, çalışan örnek ve çıktı, neden, alternatifler, tuzaklar, gerçek kod örneği ve satır satır açıklama.
- 40 soru, dağılım: **12 çıktı, 6 hata bulma, 4 boşluk, 4 sıralama, 10 kod, 4 traceback**. Her bölümü en az bir soru ölçmeli.
- 15 `practiceIds`.
- Bug ve traceback sorularında her yanlış seçenek için `optionFeedback`.
- Fill sorularında tam bir `___`; eşdeğer yazımlar `acceptedAnswers`'ta (doğrulayıcı her birini çalıştırır).
- Kod sorularında en az 3 test: normal, sınır ve uygun olduğunda hatalı girdi.
- 3 yazma görevi (Tamamla → Düzelt → Sıfırdan yaz). Düzelt görevinde başlangıç kodunun her hatası en az bir testte yakalanmalı. Bunu sınamak için yarım düzeltilmiş varyantları geçici bir betikle çalıştırıp her birinin en az bir testte kaldığını gör (M8–M9'da yapıldı; M9'da bu deneme eksik bir testi ortaya çıkardı).
- Bitince: `coverage.json`'da ilgili alt başlıkları `"doğrulandı"` yap ve bölümleri eşle; `GELISIM-PLANI.md`'de modülü işaretle ve tarihli bir günlük bölümü ekle; yukarıdaki beş komutu çalıştır; tarayıcıda en az bir örneği Worker üzerinden dene.

### Belirlenimcilik kuralları (çıktı her çalıştırmada ve her platformda aynı olmalı)

- Küme, `os.listdir`, `iterdir`, `glob` sonuçlarını yazdırmadan önce `sorted()`.
- `id()` değerini, nesne adreslerini, zamanı, rastgele sayıyı (tohumsuz) yazdırma.
- Küçük tam sayı / string önbelleğine bağlı `is` sonuçlarından kaçın.
- `OSError` mesajını yazdırma: errno Pyodide'de 44, Windows/Linux'ta 2'dir. Hata türünü ve `error.filename`'i kullan.
- Yolları `as_posix()` ile göster; her `open`'da `encoding` açıkça ver.
- `__file__`, `sys.path`, `sys.prefix`, tüm `os.environ` gibi ortama bağlı değerleri yazdırma.
- Standart kütüphaneyi gölgeleyen dosya (ör. `random.py`) çalıştırılabilir örnekte gösterilemez: Pyodide `random`, `re`, `math` gibi modülleri önceden yüklemiştir; bu senaryolar bug sorusu olarak verilir.
- Testte boş stdin (`""`) `EOFError` verir; stdin'in sonundaki `\n` yeni bir boş satır üretmez (`splitlines`).
- M8–M9'daki örnekler yerel Windows CPython 3.11'de de çalıştırılıp aynı çıktı alındı; bu denetimi sürdürmek iyi olur.

## 7. İçerik nasıl üretildi

- M1–M2 mevcuttu; Aşama 1'de şemaya göre işaretlenip düzeltildi.
- M3–M7 JSON olarak yazıldı.
- M8 ve M9, `scripts/content-builders/build_m8.py` ve `build_m9.py` betikleriyle üretildi. Kod blokları Python'da `r'''...'''` dizeleri olarak yazılır, betik JSON'u ve ilgili yazma görevlerini (`writing-tasks.json` içindeki o modülün kayıtlarını değiştirerek) yazar. M10 için bu iki betikten biri şablon olarak kopyalanabilir. Çalıştırma: `PYTHONIOENCODING=utf-8 python scripts/content-builders/build_m9.py` (yerel Python 3.11 yeterli; doğrulama yine Pyodide'de yapılır).
- Dikkat: Bash heredoc içinde ters bölü (`\n`) kaçışları bozuluyor; kaçış içeren betikleri dosya yazma aracıyla oluştur.

## 8. Bu çalışmada yapılanlar (kronolojik)

1. **Değerlendirme:** Site bir öğrenme kaynağı olarak incelendi; eksikler `GELISIM-PLANI.md`'ye işlendi.
2. **Aşama 1 paketi:**
   - Şemaya kazanım, önkoşul, zorluk, bölüm bağlantısı ve içerik sürümü eklendi.
   - Modüller otomatik keşfediliyor.
   - İlerleme şeması v3'e geçti.
   - Doğrulayıcı genişletildi.
   - `answer-check` eklendi: çoklu kabul edilen cevap ve yanlış seçenek gerekçesi.
   - Soru ve sonuç ekranından ilgili derse "Dersi aç" bağlantısı eklendi.
   - Bölüm bazlı istatistik ekranı eklendi.
   - Yedek dışa/içe aktarma testleri eklendi.
   - Kapsam haritası (`coverage.json`) ve `npm run coverage` eklendi.
   - M1–M2 metin hataları düzeltildi.
3. **M3 Akış kontrolü, M4 Veri yapıları, M5 Referans ve kopyalama, M6 Fonksiyonlar, M7 Hata yönetimi:** her biri yukarıdaki standartla yazıldı.
4. **M8 Dosyalar:**
   - Çalışma zamanına her çalıştırma için boş geçici klasör eklendi.
   - Doğrulayıcı, modül önekli hata adlarını da tanıyor.
5. **M9 Modüller ve ekosistem:** Çalışma zamanı artık bir çalıştırmanın modüllerini, `sys.path` değişikliklerini ve ortam değişkenlerini sonraki çalıştırmaya sızdırmıyor.

Her modülün ayrıntılı günlüğü (öne çıkan sorular, görevler, doğrulama sayıları) `GELISIM-PLANI.md`'nin sonundaki tarihli bölümlerdedir.

## 9. Bilinen sınırlar

- **Sıfırdan yaz görevleri:** Testler yalnızca çıktıya bakar. Örneğin m9-w3'te paket yapısı `dir(metin)` satırıyla sınanıyor, ama bu liste sabit yazılarak da geçilebilir.
- **Terminal komutları:** pip, venv, uv ve poetry tarayıcıda çalışmaz. M9 bunları açıklamalar, çalıştırılmayan bug soruları, `find_spec`, `tomllib` ve `runpy` üzerinden öğretir.
- **M10'da dikkat:**
  - `subprocess` ve `time.sleep` gibi konular Pyodide'de sınırlıdır.
  - `random` için `random.seed(...)` ile sabit tohum kullanılmalı; çıktının Python sürümleri arasında aynı olduğu doğrulanmalı.
  - `datetime.now()` çıktısı yazdırılmamalı.
- **Commit durumu:** M10'a kadar olan iş commit edilmiştir. Son geri bildirim paketi (traceback düzeltmesi, ders tamamlama koşulu, M1–M2 yeniden yazımı, Ara sınav 1, Atölye 1) henüz commit edilmemiş olabilir; `git status` ile kontrol et.
- **Çalıştırıcı tracebacki:** `public/python-runtime.js` hata biçimlendirirken `cozum.py` çerçevesine kadar ilerler. Çalıştırıcıyı değiştirirsen çıktıda `<exec>` geçmediğini sınayan regresyon testini koru.

## 10. GitHub Pages yayını

Site iki yerde yayınlanabilir; ikisi birbirini etkilemez.

| | Sites (mevcut) | GitHub Pages |
|---|---|---|
| Adres | python-iz.berensr01.chatgpt.site | https://berensr8.github.io/python-iz/ |
| Derleme | `npm run build` (Cloudflare Worker, `dist/`) | `npm run build:pages` (statik HTML, `dist-pages/client/`) |

- **Anahtar:** `PAGES_BUILD=1` ortam değişkeni `vite.config.ts` ve `next.config.ts`'i statik dışa aktarım moduna alır (Cloudflare/Sites eklentileri devre dışı). Değişken yoksa yapılandırmalar eskisi gibi çalışır. `scripts/build-pages.mjs` bunu ayarlar, çıktıyı `dist-pages/`'e taşır, `.nojekyll` ekler ve HTML'deki her adresin taban yolla başladığını denetler.
- **Taban yol:** `PAGES_BASE_PATH` (varsayılan `/python-iz`). Kullanıcı sitesi (`berensr8.github.io` deposu) ya da özel alan adı için boş bırak.
- **vinext sınırı:** `basePath` (Next ayarı) vinext 1.0.0-beta.5'te dışa aktarımda ana sayfayı atlıyor; bu yüzden taban yol Vite'ın `base` ayarıyla veriliyor. vinext güncellenirse yeniden dene.
- **Mutlak yol yasağı:** Worker ve favicon adresleri göreli/taban yola bağlı yazıldı (`new URL("py-worker.js", document.baseURI)`, `importScripts("python-runtime.js")`). Yeni kodda `/...` ile başlayan sabit adres kullanma; Pages'te alt dizinde bozulur.
- **Dağıtım:** `.github/workflows/pages.yml`, `main`'e her push'ta içerik doğrulaması ve regresyon testlerini çalıştırır, geçerse yayınlar. Depo ayarlarında Pages kaynağı "GitHub Actions" olmalı.
- **Dikkat:** `npm run build:pages` yerel `dist/` klasörünü siler (çıktıyı `dist-pages/`'e taşır). Sites derlemesini yeniden üretmek için `npm run build` çalıştır.
- **Yerelde deneme:** Pages çıktısı alt dizin altında sunulmalı; kök adreste sunmak yolları bozar. Windows'ta derleme sonunda `Assertion failed ... async.c` mesajı görülebilir; Node'un kapanış hatasıdır, betik çıktıya bakıp yok sayar.
- **Dış bağımlılık:** Python motoru (Pyodide) jsDelivr CDN'inden yüklenir.
- **İlerleme:** localStorage adrese bağlıdır; Sites adresindeki ilerleme Pages adresine otomatik taşınmaz (sitedeki yedek dışa/içe aktarma kullanılabilir).

## 11. İlerleme aktarımı ve yedek hatırlatması

İlerleme yalnızca tarayıcının `localStorage`'ında durur; cihaz değişince ya da tarayıcı verisi silinince kaybolur. Sunucu veya hesap kullanılmaz. Kalıcı depolama izni (`navigator.storage.persist()`) bilerek **istenmez**: Firefox gibi tarayıcılarda öğrenciye "izin ver" kutusu çıkarır.

- **Aktarım kodu:** `encodeTransfer` / `decodeTransfer` (`lib/progress-repository.ts`). Biçim `PYIZ1.` + base64url(gzip(JSON)); `CompressionStream` yoksa sıkıştırmasız `PYIZ1R.`. Canlı sınav (`activeQuiz`) taşınmaz. Çözerken boyut sınırı (5 MB, sıkıştırma bombasına karşı), önek ve JSON şeması denetlenir. Tam dolu bir ilerleme yaklaşık 45 KB, kod birkaç KB'tır.
- **Bağlantı:** `https://…/python-iz/#aktar=<kod>`. `#` sonrası sunucuya gitmez. Uygulama açılışta okur, adres çubuğundan ve geçmişten hemen siler, İstatistikler sayfasında onay kutusunu açar. Bozuk kodda anlaşılır hata gösterilir, ilerleme değişmez.
- **Birleştirme** (`mergeProgress`): tamamlananlar (bölüm, pratik, ders çalıştırma) birleşir; XP, soru sayaçları ve ipucu sayısı **toplanmaz, büyüğü alınır** (iki cihaz aynı eski çalışmayı içerebilir, toplamak çift sayar); testler tarih/oturumla tekrarsız birleşir; seri en son çalışılan taraftan gelir; yazma sonucunda başarı ve ipucusuzluk korunur; taslak ve tema yerelde kalır; canlı sınav yerelde kalır. Bilinen sınır: iki cihazda ayrı kazanılmış XP toplanmaz, büyük olan alınır.
- **Onay:** Birleştir (önerilir) / Yerine koy / Vazgeç. Uygulanmadan önce yerel kayıt `python-iz-before-import` anahtarına kurtarma kopyası olarak yazılır. Yedek dosyası içe aktarma da aynı onay kutusunu kullanır.
- **Hatırlatma:** `lastBackupAt` alanı (şema alanı, eski kayıtlarda `null`) yedek indirince ve kod üretince güncellenir. 100 XP'ten fazlası olup 14 gündür yedeği olmayan öğrenciye bir bant gösterilir; "1 hafta sonra hatırlat" `python-iz-backup-snooze` anahtarında tutulur (ilerleme dosyasının parçası değildir).
- **Testler:** `scripts/test-learning.mjs` içinde birleştirme (kayıpsızlık, çift sayım yok, kendisiyle birleşince değişmeme, girdiyi bozmama), kod gidiş-dönüşü, satır sonu/boşluk toleransı, bozuk/kesik/yabancı/şişirilmiş kod reddi. Mutasyon denemesi yapıldı: XP'yi toplayan ya da boyut sınırını kaldıran bozuk kod testlerce yakalanıyor.
- **Tarayıcıda denendi:** iki adres (`localhost` ve `127.0.0.1`) iki cihaz gibi kullanıldı; bağlantıyla ve elle yapıştırarak aktarım, bozuk kod, birleşik sonucun kaydedilen veriyle karşılaştırması.

## 12. Ara sınav ve atölye verisi; iki kalıcı kural

**Veri:** `content/milestones.json` iki liste tutar.
- `exams`: `id, afterModule, title, scope, description, minutes, questionIds`. `afterModule` sınavın hangi modülden sonra açıldığını ve oturum/deneme kayıtlarındaki `moduleId`'yi belirler (Ara Sınav 1 → 4, Ara Sınav 2 → 8). Süre 25–60 tam dakika.
- `workshops`: `id, afterModule, title, summary, steps`. Adım türleri: `read` (kodu incele, tek satır cevap; `progressKey` ilerlemede `workshopRead` altında tutulur, `answer` ve `expectedOutput` kodun gerçek çıktısıyla eşleşmeli) ve `write` (`taskId` → `content/workshop-tasks.json`). Son adım `write` olmalı; son adım dışındakilerde `nextLabel` gerekir. Adımlar sırayla açılır.
- Atölye görevleri `workshop-tasks.json`'dadır (alanlar `writing-tasks.json` ile aynı). `verify-content` bu dosyaları ve verileri denetler: soru kimlikleri, kapsam, kod soru sayısı, görevlerin atölyelerde kullanılması, okuma adımı çıktısı.
- Atölye 2 ve 3 `scripts/content-builders/build_workshops.py` ile üretilir (beklenen çıktılar referans çözümler çalıştırılarak hesaplanır). Atölye 1 ve ara sınavlar elle düzenlenmiş JSON'dur.
- Yeni ara sınav soruları seçilirken `scripts` altındaki seçme betiği yoktur; Ara Sınav 2 için ölçüt: son modüllere daha çok soru, her seçim farklı bir ders bölümünü ölçsün, önceki ara sınavın soruları tekrar edilmesin, en az üç kod yazma ve bir hata bulma sorusu olsun.

**Kural 1 — her soru cevaplanabilir olmalı.** `output`, `bug` ve `traceback` sorularında en az 3 farklı `options` ve `options` içinde `answer` zorunludur. Seçeneksiz bir çıktı sorusu arayüzde cevap kutusu çıkarmaz, pratiği ve bitiriş testini tamamlanamaz kılar ve oturum kaydını bozar. M8 ve M9 bu hatayla yayına çıkmıştı. M8/M9 üreticileri seçenekleri `scripts/content-builders/output-options.json` dosyasından uygular; yeni üreticide de seçenekleri baştan yaz. `verify-content` ve `test-learning` bunu zorlar.

**Kural 2 — doğru cevabın konumu içerikte önemsiz, çünkü oturum seçenekleri karıştırır.** `createQuiz` seçenekleri oturum ve soru kimliğine göre sabit tohumla karıştırır (yenilemede sıra değişmez). İçerikte doğru cevap çoğunlukla ilk sırada yazılıdır; bu bilinçli olarak karıştırmaya güvenilir. Seçeneklerde "yukarıdakilerin hepsi", "hiçbiri" gibi konuma bağlı ifade kullanma.

**Üreticiler:** `build_m8.py`, `build_m9.py` (modül + görev), `build_workshops.py` (atölye). Bash heredoc içinde ters bölü bozulabilir; kaçış içeren Python kodunu ham dizeyle (`r'...'`) ya da dosya yazma aracıyla oluştur.
