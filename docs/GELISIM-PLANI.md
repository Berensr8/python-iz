# Python İz gelişim ve tamamlama planı

Tarih: 5 Ekim 2026
Durum (6 Ekim 2026): Aşama 1 uygulanıyor. İlk yazma paketi hazır; aşağıdaki açık maddeler tamamlanmış sayılmıyor.

## Hedef ve kapsam

Öğrenci hem kendisinin hem AI'ın yazdığı Python kodunu okuyabilmeli; gereksinimden yola çıkarak sıfırdan program yazabilmeli; veri ve kontrol akışını tasarlayabilmeli; hataları bulup testlerle düzeltebilmelidir. Kod okuma ve kod yazma eşit temel hedeflerdir. AI bir yardımcıdır; çözümü kopyalamak bağımsız üretim başarısı sayılmaz. Mezuniyet için küçük ama tamamlanmış, çok dosyalı bir uygulamayı tasarlama, yazma, test etme ve açıklama gerekir.

İlk istekteki 18 modülün bütün alt başlıkları kapsamda kalır. Bitwise, walrus, MRO, descriptor ve metaclass gibi kavramlar silinmez; önkoşulları ve gerekli öğrenme derinlikleri işaretlenir. Descriptor/metaclass tanıma düzeyindedir. Framework konuları Python çekirdeğiyle aynı derinlikte öğretilmez.

Önceki değerlendirmedeki yüzde ve 10 üzerinden puanlar ölçülmüş öğrenme sonuçları değildir. Bu planda tamamlanma, doğrulanmış kazanımlar ve kabul ölçütleriyle izlenir. Modül sayısı tek başına öğrenme düzeyini göstermez.

## Başlangıç durumu

- İçeriği bulunan modüller: M1 Temeller, M2 String'ler; toplam 16 ders bölümü ve 80 soru.
- 18 modül adı bulunuyor; M3–M18 içeriği henüz yok ve gezinme ilk iki modülle sınırlı.
- Son doğrulama 109 çalıştırılabilir örnek/çözümü kontrol etti. Bu sayı 109 bağımsız alıştırma anlamına gelmez; açıklamaların pedagojik doğruluğunu tek başına kanıtlamaz.
- Kod çalıştırıcı, altı soru tipi, kademeli ipuçları, modül testi, yerel ilerleme, tema ve ses kontrolleri mevcut.
- Gerçek adım adım yürütme görselleştiricisi, ara/genel sınavlar ve proje inceleme atölyeleri mevcut değil.
- Kod soruları tek beklenen çıktıyla değerlendiriliyor. Süre dolumunda sınav sonucu kaydı, zayıf konuların doğrudan bölüm bağlantıları ve günlük seri hesabı geliştirilmeli.
- Doğrulayıcı yalnızca ilk iki içerik dosyasını listeliyor; tüm görünür kodları ve cevap anahtarlarını kapsayan kontrol eklenmeli.

## Her modül için ortak teslim standardı

- [ ] İlk istekteki her alt başlık için kazanım, önkoşul, öğrenme düzeyi ve kaynak eşlemesi.
- [ ] Her kavramda sade açıklama, çalıştırılabilir örnek, çıktı, neden-sonuç açıklaması, alternatifler, tuzaklar ve satır satır gerçek kod incelemesi.
- [ ] Basitten karmaşığa ilerleme; henüz öğretilmemiş sözdizimi kullanıldığında kısa açıklama ve ilgili derse bağlantı.
- [ ] En az 40 özgün soru; 15 soruluk pratik; 18 soruluk bitiriş testi; geçme eşiği %70.
- [ ] Yeni modüllerde başlangıç dağılımı: 12 çıktı, 6 hata bulma, 4 boşluk doldurma, 4 sıralama, 10 kod yazma, 4 traceback. Mevcut M1–M2 havuzları kademeli dönüştürülecek; sayı artışı kalite yerine geçmez.
- [ ] Her modülde en az üç yazma görevi: iskelet tamamlama → hata düzeltme/değiştirme → boş editörden çözüm. Sonraki modüllerde yardım azalır, bağımsız yazma payı artar.
- [ ] Kod testlerinde normal, sınır ve uygun olduğunda hatalı girdiler; çoklu doğru çözüm kabulü. Kod okuma ve yazma başarıları, yardımlı ve ipucusuz tamamlama ayrı izlenir.
- [ ] Bitiriş testinde en az üç kod yazma sorusu; teste geçiş için modülün yazma görevleri de tamamlanır.
- [ ] Pratikte iki ipucu ve çözüm; yanlış seçeneğe uygun neden açıklaması. Testte ipuçları ve cevap anahtarı sonuç ekranına kadar kapalı.
- [ ] M2 ve sonrasında 18 test sorusunun 4'ü önceki açık modüllerden gelir; ilk modülde önceki konu kotası yoktur.
- [ ] Sorular alt konu ve zorluk düzeyiyle etiketlenir; test kazanım kapsamını koruyarak rastgele seçilir.
- [ ] Her görünür çalıştırılabilir örnek ve referans çözüm gerçek Python 3.12+ ile doğrulanır. Kasıtlı hatalar beklenen hata ve neden açısından kontrol edilir.
- [ ] Kesin çıktısı olmayan örneklerde sıra, nesne adresi, zamanlama ve rastlantısallık uygun beklenti kurallarıyla ele alınır.
- [ ] Kaynaklardan özgün Türkçe açıklamalar üretilir; lisans şartları korunur. Doğru çıktı, doğru açıklama ve öğretim sırası ayrı ayrı gözden geçirilir.

## Aşama 1 — Ölçme sistemi ve içerik temelini düzelt

Yeni modüllerden önce uygulanır.

- [x] A1.1: 18 modülün bütün alt başlıklarını ders/soru/test kimliklerine bağlayan kapsam matrisi oluştur. Durumlar: planlandı, yazıldı, doğrulandı, yayınlandı. (`content/coverage.json`, `npm run coverage`. M3–M18 alt başlıkları bu plandaki modül tanımlarından alındı; ilk istekteki listeyle karşılaştırılmalı.)
- [ ] A1.2: İçerik şemasına kazanım, önkoşul, zorluk, kaynak, bölüm bağlantısı, çalışma ortamı, test vakaları ve içerik sürümü ekle. Mevcut kimlikleri koru. (Yapıldı: kazanım, önkoşul, zorluk, bölüm bağlantısı, içerik sürümü. Açık: kaynak ve çalışma ortamı etiketi.)
- [x] A1.3: Modül kaydını ve doğrulayıcıyı tüm içerik dosyalarını keşfedecek şekilde geliştir. Sabit iki-modül sınırlarını yayınlanmış içerik/ilerleme verisinden türet.
- [x] A1.4: Her değerlendirmeyi temiz Python ad alanında çalıştır; paralel istekleri sırala; eski sonuçların yeni koda uygulanmasını engelle. İlk çalışma ortamı yüklenmesi ile kod çalışma süresini ayrı yönet.
- [ ] A1.5: Kısa kod sorularına birden çok girdi, sınır durumları ve hata senaryolarıyla test ekle. Fonksiyon sorularında dönüş değerini, çıktı sorularında çıktıyı doğrula. Farklı doğru çözümleri kabul et.
- [ ] A1.6: Test vakalarını çözümden önce arayüzde göstermeme özelliği ekle. Tarayıcıdaki testleri güvenli/gizli sınav altyapısı olarak sunma; öğrenme aracı olduklarını esas al.
- [ ] A1.7: Gerçek traceback metni ve satır seçimi ekle. Boşluk doldurmada birden çok geçerli cevap desteğini, hata bulmada neden açıklamalarını tanımla. (Yapıldı: çoklu cevap, bug/traceback yanlış seçenek gerekçeleri. Açık: traceback satır seçimi.)
- [x] A1.8: Sınav oturumunun soru listesini sabitle; yanıt geldikçe yeniden sıralanmasını engelle. Süre dolması ve normal bitirme aynı kayıt yolunu kullansın. Yenilemede süre uzamasın, ödül/sonuç iki kez yazılmasın.
- [x] A1.9: Yanlışların bağlantısı ilgili modülün ilgili ders bölümünü açsın. Zayıf konu testi sadece son modülden değil tüm açık konulardan seçim yapsın. Çözülmemiş konu ile yanlış öğrenilmiş konuyu ayır.
- [x] A1.10: İlerleme sürüm geçişi, bozuk veri durumları, dışa/içe aktarma ve depolama hatası geri bildirimi ekle. Eski XP, tema ve tamamlanmalar korunsun.
- [x] A1.11: Günlük çalışma serisini İstanbul tarihine göre hesapla; aynı gün tekrarı, ara verilen gün ve gün değişimini doğrula.
- [ ] A1.12: M1–M2 anlatımlarını yeniden denetle. Kurulum/REPL gerçek kullanım yönergelerini tamamla; input() için giriş alanı sağla. Taban bölmede negatif sayılar ve bool dışındaki and/or sonuçları gibi aşırı genellemeleri düzelt.

Kapanış: Yanlış bir algoritma tek örneği geçerek doğru sayılmıyor; doğru alternatif çözümler kabul ediliyor; sınav süre bitiminde bir kez kaydediliyor; eski ilerleme okunuyor; tüm mevcut içerik doğrulanıyor. Bu davranışları hedefleyen regresyon testleri ve kısa tarayıcı kontrolü geçiyor.

## Aşama 2 — Akış ve veri: M3–M5

- [x] M3: if/elif/else, match-case, for/while, break/continue/pass, döngü else, range/enumerate/zip. Pattern matching ile basit eşitlik kontrolü ayrımı. (6 Ekim 2026: 8 bölüm, 40 soru — 12 çıktı, 6 hata bulma, 4 boşluk, 4 sıralama, 10 kod, 4 traceback —, 15 pratik, 3 yazma görevi; tümü Python 3.12.7 ile doğrulandı.)
- [x] M4: list/tuple/set/dict, metotlar, iç içe veriler, sorted/min/max ve key; alias ve mutasyon konularına hazırlık. (6 Ekim 2026: 8 bölüm, 40 soru, 15 pratik, 3 yazma görevi; Python 3.12.7 ile doğrulandı.)
- [x] M5: Referanslar, id, is/==, mutable/immutable, shallow/deep copy, unpacking ve comprehension'lar. (6 Ekim 2026: 8 bölüm, 40 soru, 15 pratik, 3 yazma görevi; Python 3.12.7 ile doğrulandı.)
- [ ] Görselleştirme 1: Döngüde aktif satır ve değişken tablosu; aynı listeye bağlı iki isim ve sığ/derin kopya için adım ileri/geri kontrolleri.
- [ ] Atölye 1 (M4 sonrası): Sipariş/harcama analiz kodunu incele ve düzelt; ardından gereksinimden kendi filtreleme ve özetleme programını yaz, boş veriyle test et.
- [ ] Ara sınav 1 (M4 sonrası): M1–M4 kapsamı.

Kapanış: Öğrenci iç içe yapıdaki verinin hangi döngüyle işlendiğini ve bir liste değişikliğinin hangi isimleri etkilediğini açıklayabiliyor. M3, M4, M5 sırasıyla eklenir; grup sonunda tüm içerik doğrulanır ve raporlanır.

## Aşama 3 — Fonksiyon, hata ve dosya: M6–M8

- [x] M6: return, parametre türleri, *args/**kwargs, mutable default, LEGB/global/nonlocal, lambda/map/filter/reduce, recursion, closure, docstring. Positional-only ve keyword-only parametreleri ekle. (6 Ekim 2026: 8 bölüm, 40 soru, 15 pratik, 3 yazma görevi; Python 3.12.7 ile doğrulandı.)
- [x] M7: Ayrıntılı traceback, yaygın hatalar, try/except/else/finally, raise, özel exception, raise from ve assert. Girdi doğrulaması ile assert farkını işle. (6 Ekim 2026: 8 bölüm, 40 soru, 15 pratik, 3 yazma görevi; Python 3.12.7 ile doğrulandı.)
- [x] M8: open ve modlar, with, pathlib/os/shutil, CSV/JSON, encoding ve dosya yaşam döngüsü.
- [ ] M8 arayüzü: tarayıcıdaki sanal dosyalar için yükleme/indirme ve hazır örnek dosyalar. (Şimdilik örnekler dosyalarını kod içinde kendileri oluşturuyor.)
- [ ] Görselleştirme 2: Fonksiyon çağrısı, yerel/global kapsam, recursion ve dönüş değerleri için call stack.
- [ ] Atölye 2 (M6 sonrası): AI'ın yazdığı metin temizleme fonksiyonunu düzelt; ardından sözleşmesi verilen yeni temizleme fonksiyonunu sıfırdan yaz ve parametrik testlerini kur.
- [ ] Atölye 3 (M8 sonrası): CSV raporlama projesini incele; kendi CSV→JSON raporlayıcını yaz, hatalı kayıt ve boş dosya senaryolarını test et.
- [ ] Ara sınav 2 (M8 sonrası): M1–M8; son öğrenilen konulara ağırlık ve önceki kazanımlara tekrar.

Kapanış: Öğrenci traceback'ten kendi kodundaki ilgili satıra ulaşabiliyor; bir fonksiyonun girdisini, çıktısını ve yan etkisini ayırabiliyor; dosya işleme hatasını testle gösterebiliyor.

## Aşama 4 — Proje düzeni ve nesneler: M9–M11

- [x] M9: import, kendi modülü, __main__, relative import, pip/venv, requirements.txt/pyproject.toml, uv/poetry, ortam değişkenleri ve .env. Araçlar tek önerilen başlangıç akışı üzerinden tanıtılır; alternatiflerin rolü açıklanır.
- [x] M10: math/random, datetime/time/timezone, collections, itertools, functools, enum, heapq, bisect, re, sys/subprocess/argparse; ilk istekteki alt türler dâhil. subprocess yerel ortamda okuma düzeyinde; diğerleri tarayıcı alıştırmalarıyla.
- [ ] M11: class/object, __init__/self, instance/class değişkenleri, inheritance/super, kapsülleme, property/staticmethod/classmethod. Composition alternatifini ekle.
- [ ] Yerel geliştirme rehberi: Python, editör, terminal, sanal ortam, bağımlılık yükleme ve örnek projeyi çalıştırma adımları.
- [ ] Ortam etiketleri: Tarayıcıda çalışır / yerel Python gerekir / kaydedilmiş veriyle incelenir. Desteklenmeyen komutlar başarılı çalışmış gibi gösterilmez.
- [ ] Atölye 4 (M10 sonrası): Çok dosyalı bir CLI uygulamasını incele; ardından argparse, pathlib ve kendi modüllerinle dosya raporlama aracı oluştur.

Kapanış: Öğrenci yeni bir Python deposunda hangi dosyanın başladığını ve import zincirini bulabiliyor; bağımlılık sorununu kod hatasından ayırabiliyor; sınıf ve nesne durumunu açıklayabiliyor.

## Aşama 5 — İleri kodu okuma ve üretme: M12–M14

- [ ] M12: Polimorfizm, abc, dunder metotlar, operator overloading, multiple inheritance/MRO, dataclass ve slots; descriptor/metaclass tanıma düzeyi.
- [ ] M13: Iterator protokolü, generator/yield, decorator ve parametreli decorator, sınıf/contextlib ile context manager.
- [ ] M14: Temel type hints, koleksiyon tipleri, Optional/Union/|, TypedDict, Protocol, generics, Callable ve mypy mantığı. Annotation ile çalışma zamanı doğrulamasını ayır.
- [ ] Görselleştirme 3: Generator'ın duraklama/devam etmesi, decorator sarma sırası ve context manager giriş/çıkışı.
- [ ] Atölye 5 (M12 sonrası): Envanter projesindeki model hatalarını incele; kendi dataclass tabanlı envanter modelini ve davranış testlerini yaz.
- [ ] Ara sınav 3 (M12 sonrası): M1–M12.

Kapanış: Öğrenci @ işaretlerinin, yield'in ve tip anotasyonlarının gerçek davranıştaki rolünü açıklayabiliyor; decorator ve generator içeren bir kodun çalışma sırasını izleyebiliyor.

## Aşama 6 — Eşzamanlılık, kalite ve performans: M15–M17

- [ ] M15: threading/multiprocessing, GIL, asyncio/async-await, event loop, I/O/CPU farkı ve seçim gerekçesi. Cancellation, timeout ve paylaşılan veri hatalarını ekle; GIL anlatımını Python sürümü/derlemesi bağlamında sınırla.
- [ ] M16: breakpoint/pdb, logging, unittest/pytest, ruff/black/mypy ve proje yapısı. Fixture, parametrik test, mock ve regresyon testi okuma.
- [ ] M17: Big-O, temel arama/sıralama, iç içe döngü maliyeti, uygun veri yapısı seçimi ve ölçümle darboğaz bulma.
- [ ] Görselleştirme 4: Event loop'ta hazır/bekleyen görevler; aynı işin sıralı ve async akışı. Modelin gerçek çalışma garantilerini ve sınırlarını belirt.
- [ ] Atölye 6 (M16 sonrası): Hatalı async toplayıcıyı teşhis et; fixture servislerle kendi toplayıcını, timeout/hata yönetimini ve testlerini yaz.
- [ ] Ara sınav 4 (M16 sonrası): M1–M16.

Kapanış: Öğrenci bir testin neyi kanıtladığını açıklayabiliyor; doğru görünen AI düzeltmesine karşı örnek bulabiliyor; yavaşlığın algoritmadan mı beklemeden mi kaynaklandığını ayırabiliyor.

## Aşama 7 — Ekosistem ve bitirme: M18

- [ ] M18: requests, FastAPI, SQLite/SQLAlchemy, NumPy/Pandas ve LLM API çağrısı içeren kısa kod okumaları. Amaç kütüphaneleri derinlemesine öğretmek değil, kod içindeki rollerini tanımak.
- [ ] Modern kod ekleri: HTTP status/timeout/retry, SQL parametreleri, veri doğrulama modelleri, API anahtarını ortamdan okuma ve bağımlılık sürümleri. Her ek konu kapsam matrisinde ilk istekten ayrı işaretlenip raporlanır.
- [ ] Ağ/API örnekleri varsayılan olarak fixture ve sahte servislerle tekrarlanabilir çalışır; ücretli hesap veya gerçek anahtar zorunlu değildir. Gerçek sunucu/subprocess/multiprocessing alıştırmaları yerel ortam yönergesiyle sağlanır.
- [ ] Bitirme atölyesi: Gereksinimleri verilen küçük bir CLI/raporlama uygulamasını sıfırdan tasarla ve yaz. README, birkaç Python modülü, fixture verisi, hata yönetimi ve testler üret. Sonra başka bir çözümü inceleyip kendi tasarımınla karşılaştır. AI yardımı kullanılan kısımları belirt; çözümü açıklayabil ve yeni bir gereksinime kendin uyarlayabil.
- [ ] Genel sınav: 50 soru, bütün modüllerden temsil, ipucusuz, %70 baraj; konu bazında sonuç ve eksik kazanımlara bağlantı. Kod okuma, hata bulma ve traceback başarısı ayrı gösterilir.
- [ ] Bitirme değerlendirmesi: Açık rubrik: gereksinim doğruluğu %40, testler/sınır durumları %25, kod düzeni/okunabilirlik %20, açıklama ve yeni gereksinime uyarlama %15. Okuma ve bağımsız yazma için ayrı sonuç. Otomatik testlerin değerlendiremediği açıklamalarda referans analiz/öz değerlendirme kullan; otomatik pedagojik puan varmış gibi sunma.

Kapanış: 18 modül tamamlanmış; altı atölye ve bitirme incelemesi kullanılabilir; tüm modüller genel sınavda temsil ediliyor. Tamamlama belgesi profesyonel yeterlilik veya işe hazır olma garantisi olarak sunulmuyor.

## Aşama 8 — Kalıcılık, görseller ve bütün ürün denetimi

Temel erişilebilirlik ve işlev kontrolleri her yayında yapılır. Bu aşama tüm deneyimin son birleştirme denetimidir; görselleştiriciler ilgili modülleri bekletmeden yukarıdaki aşamalarda geliştirilir.

- [ ] 1/3/7/14 gün önerili tekrar kuyruğu; sonuç ve ipucu kullanımına göre ayarlama. Çözülmemiş konuyu öğrenilmiş sayma.
- [ ] İlk deneme başarısı, ipucusuz başarı, son tekrar ve alt konu bazlı ilerleme raporu.
- [ ] Modül/test/atölye rozetleri, anlamlı XP kuralları, yol haritası görünümü, seviye atlama sesi ve tamamlanma animasyonları.
- [ ] Görselleştirme altyapısı: Python yürütmesinden satır, kapsam, nesne kimliği ve call stack anlık görüntüleri üret; dersteki beklenen durumlarla doğrula. Başlangıçta sınırlı destekli örnekler kullan, desteklenmeyen kod için açık geri bildirim ver.
- [ ] İleri/geri, sıfırla ve hız kontrolleri; animasyonun yanında metin/tablo karşılığı; azaltılmış hareket tercihine uyum.
- [ ] Klavye ve ekran okuyucu kullanımı, mobil editör/Parsons kontrolleri, uzun Türkçe metinler, açık/koyu tema kontrolü.
- [ ] Pyodide geç yüklenmesi, ağ hatası, sonsuz döngüden toparlanma, örnekler arası durum sızması ve çalışma alanı yaşam döngüsü kontrolü.
- [ ] İlerleme yedeği geri yükleme ve sürüm geçişi denemesi. Bulut senkronizasyonu ayrı bir gelecek geliştirmesidir; bu planın tamamlanmasını engellemez.

Kapanış: Temsilî mobil/masaüstü akışlarında engelleyici hata yok; her kazanımın dersi ve değerlendirmesi var; tüm kod doğrulamaları geçiyor; ilerleme güncellemelerde korunuyor.

## Teslim ve takip yöntemi

1. İşler sırayla yürütülür: Aşama 1 → M3–M5 → M6–M8 → M9–M11 → M12–M14 → M15–M17 → M18 → son bütünlük denetimi.
2. Her modül ayrı tamamlanır; değişen içerik hemen doğrulanır. Her üç yeni modülde tüm müfredat doğrulanıp toplu rapor verilir. M18 sonrasında ayrıca tam kontrol yapılır.
3. Ara sınavlar M4, M8, M12, M16 sonrasında öğrenci akışına bağlanır; geliştirme paketinin üç modüllük olması bu sıralamayı değiştirmez.
4. Her yayında teslim edilen maddeler, doğrulanan içerik/soru sayıları, açık eksikler ve kaynak commit kaydedilir. İşaretler yalnızca kanıtla kapanır.
5. Aşama durumları: bekliyor → uygulanıyor → doğrulandı → yayınlandı. Uygulama Aşama 1'den başladı; tamamlanmayan maddeler açık tutulur.
6. Site değişikliklerinde mevcut erişim ayarı korunur. Salt bu plan belgesinin oluşturulması site yayını başlatmaz.

## Referans kaynaklar

Önceki karşılaştırmada incelenen kaynaklar, kapsam ve öğretim yaklaşımı için referanstır. Yeni içerik yazılırken ilgili resmî konu sayfaları ve kullanılan Python/kütüphane sürümleri yeniden kontrol edilir.

- Python resmî öğreticisi: https://docs.python.org/3/tutorial/index.html
- CS50P ders ve problem setleri: https://cs50.harvard.edu/python/
- Helsinki Python MOOC, incelenen 2025 sürümü: https://programming-25.mooc.fi/
- Exercism Python: https://exercism.org/tracks/python/
- Automate the Boring Stuff, 3. baskı: https://automatetheboringstuff.com/3e/
- Python Tutor: https://pythontutor.com/

## Nihai kabul listesi

- [ ] İlk istekteki bütün alt başlıklar kazanım matrisinde doğrulanmış içerik ve değerlendirmeye bağlı.
- [ ] 18 modül, en az 720 özgün soru ve 270 modül pratiği seçimi mevcut; pratik ve testlerin aynı havuzdan seçim olduğu açık.
- [ ] 18 bitiriş testi, 4 ara sınav, 1 genel sınav çalışıyor; ara/genel sınavlarda kapsam dengeli. Ara sınavlar 24–30 soru ve %70 eşiği kullanıyor.
- [ ] Altı okuma+yazma proje atölyesi ve sıfırdan uygulama üretmeyi gerektiren bir bitirme projesi hazır; hata teşhisi ve test kanıtı içeriyor.
- [ ] Akış, referans/kopya, scope/call stack, generator ve event loop görselleri ilgili derslere bağlı.
- [ ] Beklenen çıktılar, hatalar, soru cevap anahtarları, test vakaları ve referans çözümler birlikte doğrulanmış.
- [ ] Açıklamalar ve öğretim sırası ayrıca denetlenmiş; otomatik çalıştırma başarısı öğrenme başarısıyla karıştırılmıyor.
- [ ] Kullanıcı kayıtları korunuyor; ortam kısıtları anlaşılır; ana öğrenme akışı mobilde ve klavyeyle kullanılabiliyor.

## 6 Ekim 2026 — İlk yazma paketi

- [x] Hedef okuma + bağımsız yazma olarak güncellendi; altı proje atölyesi ve bitirme projesi yeniden tanımlandı.
- [x] M1–M2 için 6 yazma görevi, 24 test vakası: tamamla → düzelt → sıfırdan yaz.
- [x] Mevcut 6 kod sorusu gerçek input() ve toplam 24 test vakasıyla değerlendiriliyor; farklı doğru çözümler kabul ediliyor.
- [x] Testlerde en az 3 kod yazma sorusu; modül testine girişte yazma görevlerinin tamamlanması kontrol ediliyor.
- [x] A1.4'ün temiz ad alanı, sıralı istek, eski sonuç engeli ve ayrı yükleme/çalışma süre sınırları uygulandı. Ad alanı ayrılığı bir güvenlik sandbox'ı değildir; modül/dosya sistemi izolasyonu sağlamaz.
- [x] A1.6 yazma atölyesinde uygulandı; kontrol detayları gönderim sonrası gösterilir ve istemci tarafı sınırları açıklanır.
- [x] Taslak saklama, yardımlı/ipucusuz sonuç ayrımı ve tekrarda XP vermeme eklendi.
- [x] v1→v2 ilerleme geçişi ve bozuk/depolanamayan kayıt uyarısı; eski kayıt korunur. Dışa/içe aktarma henüz yok.
- [x] A1.11 İstanbul tarihine göre günlük seri ve sınır testleri.
- [x] Zayıf tekrar havuzu oturum içinde sabit; açık modüllerde yanlış cevaplanan soruları kullanır. Doğrudan ders bölümü bağlantıları henüz yok.
- [x] İpuçsuz testte açıklamalar soru anında değil sonuç ekranında açılır.

Doğrulama: 25 regresyon kontrolü; 24 atölye referans vakası; mevcut müfredatta 133 çalıştırılabilir kontrol. TypeScript kontrolü geçti. Bu rakamlar öğrenme başarısı ölçümü değildir.

## 6 Ekim 2026 — Aşama 1 ikinci paket

Ayrıntılı uygulama planı: `docs/superpowers/plans/2026-10-06-asama1-tamamlama.md`.

- [x] Yarım kalan A1.8/A1.10 işi kararlı: TypeScript hatası giderildi, v3 geçiş testi düzeltildi.
- [x] A1.8 regresyon testleri: sabit soru listesi, süre bitiminde tek kayıt, geç yanıt reddi, çift ödül engeli, ipucu/XP kuralı.
- [x] A1.10 testi: yedek dışa/içe aktarma gidiş-dönüş; yabancı ve bozuk dosya reddi.
- [x] A1.2/A1.3: 80 soru `sectionId` ve `difficulty` ile ders bölümüne bağlandı; 16 bölüme kazanım ve önkoşul eklendi; modüller `import.meta.glob` ile keşfediliyor. Doğrulayıcı bölüm, önkoşul, seçenek, gerekçe ve kabul edilen cevap tutarlılığını zorunlu kılıyor; yazma görevlerinin referans çözümlerini de çalıştırıyor.
- [x] A1.7 kısmi: boşluk doldurmada çoklu cevap (`acceptedAnswers`, operatör çevresindeki boşluk yok sayılır); 18 bug/traceback sorusunda her yanlış seçeneğe gerekçe. Her kabul edilen cevap boşluğa yerleştirilip gerçek Python ile çalıştırılıyor.
- [x] A1.9: Pratik geri bildiriminde ve sonuç incelemesinde "Dersi aç" bağlantısı; istatistikler ders bölümü bazında, her satır derse bağlı; yanlış öğrenilmiş ve hiç denenmemiş sorular ayrı sayılıyor.
- [x] A1.1: Kapsam matrisi ve raporu (109 alt başlık; 17'si doğrulanmış içerikle kapsanıyor).
- [x] A1.12 kısmi: m1-q02 açıklaması, and/or dönüş değerleri, kurulum/REPL/dosya çalıştırma yönergesi, M2 yüzde biçimi (`70%`), m2-q10 yuvarlama açıklaması (2.675 tuzağıyla tutarlı), `in` tanımı düzeltildi.

Doğrulama: 38 regresyon kontrolü; mevcut müfredatta 169 çalıştırılabilir kontrol (Python 3.12.7); TypeScript temiz; üretim derlemesi başarılı; tarayıcıda bölüm bağlantısı, seçenek gerekçesi ve oturumun korunması elle denendi.

## 6 Ekim 2026 — M3 Akış kontrolü

Kullanıcı kararıyla Aşama 1'in kalan maddeleri beklerken M3'e geçildi.

- [x] `content/module-03.json`: if/elif/else, match-case, while, for ve range, break/continue/pass, döngü else, enumerate ve zip, iç içe döngüler. Her bölümde kazanım, önkoşul, gerçek kod ve satır satır inceleme.
- [x] 40 soru yeni modül dağılımında; her bug/traceback yanlış seçeneğine gerekçe. Kod sorularında sınır girdileri (0, 1, eşik değerleri, negatif sayı, boş çıktı).
- [x] Yazma görevleri: not ortalaması (tamamla), şifre denemesi break/else (düzelt), tahmin oyunu while True (sıfırdan yaz).
- [x] Kapsam matrisinde M3'ün 6 alt başlığı doğrulandı (toplam 23/109).
- [x] Yeni regresyon kontrolü: her yazma görevinin başlangıç kodu testleri tek başına geçemez.
- Not: Listeler M4'te anlatılacağı için M3'teki birkaç örnek basit liste kullanır ve bunu ilk geçtiği yerde belirtir.

Doğrulama: 277 çalıştırılabilir içerik kontrolü; 53 regresyon kontrolü; 36 atölye referans vakası; TypeScript ve üretim derlemesi temiz; tarayıcıda M3 kilidi, ders gezinmesi, match-case örneğinin Pyodide çalıştırması ve yazma atölyesi denendi.

## 6 Ekim 2026 — M4 Veri yapıları

- [x] `content/module-04.json`: listeler, liste metotları, tuple, küme, sözlük, sözlükte gezinme ve sayma, iç içe veri, sorted/min/max ve key. Takma ad (b = a) M5'e hazırlık olarak tanıtıldı.
- [x] 40 soru (12 çıktı, 6 hata bulma, 4 boşluk, 4 sıralama, 10 kod, 4 traceback). Kod soruları sözlük listesi kurma, frekans sayma, eşitlikte kararlı seçim ve harf duyarsız sıralama içeriyor.
- [x] Yazma görevleri: kelime sayacı (tamamla), fiyat sıralaması — str fiyat ve yön hatası (düzelt), etiket karşılaştırması küme işlemleriyle (sıfırdan yaz).
- [x] Küme çıktıları her yerde sorted() ile sabitlendi; içerik doğrulaması iki kez çalıştırılarak sıra bağımlılığı denendi.
- [x] Kapsam: 29/109 alt başlık doğrulanmış içerikle kapsanıyor.

Doğrulama: 388 çalıştırılabilir içerik kontrolü; 62 regresyon kontrolü; 48 atölye referans vakası; TypeScript ve üretim derlemesi temiz; tarayıcıda M4 kilidi ve küme örneğinin Pyodide çalıştırması denendi.

## 6 Ekim 2026 — M5 Referans ve kopyalama

- [x] `content/module-05.json`: isimler ve referanslar, is/==, mutable/immutable, sığ kopya, derin kopya ve liste çarpımı tuzağı, unpacking, list comprehension, sözlük/küme comprehension.
- [x] Belirsiz çıktılar dışarıda tutuldu: id() değerleri yalnızca karşılaştırma olarak yazdırılıyor; küçük sayı/metin önbelleğine bağlı is sonuçları soru olarak kullanılmadı, yalnızca tuzak olarak anlatıldı.
- [x] 40 soru (12 çıktı, 6 hata bulma, 4 boşluk, 4 sıralama, 10 kod, 4 traceback). Öne çıkanlar: y = y + [2] ile y += [2] farkı, str ve liste += karşılaştırması, sığ kopyada ortak iç liste, [[...] * 3] * 3 ızgara tuzağı, filtre if'inin konumu, fonksiyona geçen listenin yan etkisi.
- [x] Yazma görevleri: temiz sayı listesi comprehension (tamamla), [template] * n haftalık plan (düzelt), not raporu sözlük/liste comprehension (sıfırdan yaz).
- [x] Kapsam: 35/109 alt başlık doğrulanmış içerikle kapsanıyor; Aşama 2'nin üç modülü (M3–M5) tamamlandı.

Doğrulama: 496 çalıştırılabilir içerik kontrolü; 71 regresyon kontrolü; 60 atölye referans vakası; TypeScript ve üretim derlemesi temiz; tarayıcıda M5 kilidi ve copy modülü içeren örneğin Pyodide çalıştırması denendi.

Aşama 2'de açık kalanlar: Görselleştirme 1 (döngüde aktif satır/değişken tablosu; aynı listeye bağlı iki isim; sığ/derin kopya adımları), Atölye 1 ve Ara sınav 1 (M1–M4). Bu üçü yeni arayüz bileşeni gerektirir.

## 6 Ekim 2026 — M6 Fonksiyonlar

- [x] `content/module-06.json`: def/return/docstring, parametreler (/ ve *), *args/**kwargs, mutable varsayılan, LEGB/global/nonlocal, lambda/map/filter/reduce, recursion, closure. Docstring kapsam alt başlığı def/return bölümüne bağlandı.
- [x] A1.5'in fonksiyon kısmı içerik tasarımıyla karşılandı: kod sorularında öğrenci yalnızca fonksiyonu yazar, çağrı ve print başlangıç kodunda hazırdır. Fonksiyon return yerine print kullanırsa çıktıya fazladan None girer ve test kalır.
- [x] 40 soru (12 çıktı, 6 hata bulma, 4 boşluk, 4 sıralama, 10 kod, 4 traceback). Öne çıkanlar: print/return farkı, tükenen filter iterator'ı, paylaşılan varsayılan liste, UnboundLocalError, return'süz özyineleme, döngüde lambda geç bağlaması.
- [x] Yazma görevleri: sıcaklık dönüştürücü (tamamla), sepet fonksiyonu — UnboundLocalError ve mutable default (düzelt), ızgara yolları özyinelemesi (sıfırdan yaz).
- [x] Ek doğrulama: Düzelt görevinde yalnızca ilk hatayı düzeltmek testleri geçmiyor; yanlış sıralanmış özyineleme Pyodide'de temiz RecursionError veriyor ve çalışma ortamı sonraki çalıştırmada sağlam kalıyor.
- [x] Kapsam: 44/109 alt başlık doğrulanmış içerikle kapsanıyor.

Doğrulama: 607 çalıştırılabilir içerik kontrolü; 80 regresyon kontrolü; 73 atölye referans vakası; TypeScript ve üretim derlemesi temiz; tarayıcıda M6 kilidi ve closure örneğinin Pyodide çalıştırması denendi.

## 6 Ekim 2026 — M7 Hata yönetimi

- [x] `content/module-07.json`: traceback okuma, yaygın hata türleri ve hiyerarşi, try/except, else/finally, raise ve yeniden fırlatma, özel exception aileleri, raise from ve __cause__, assert ile girdi doğrulaması farkı.
- [x] Ders örnekleri hatasız çalışmak zorunda olduğu için traceback bölümü hatayı yakalayıp traceback.extract_tb ile çerçeveleri (fonksiyon adı, satır numarası) yazdırıyor; çıktı Node doğrulayıcısında ve tarayıcıda aynı.
- [x] 40 soru (12 çıktı, 6 hata bulma, 4 boşluk, 4 sıralama, 10 kod, 4 traceback). Öne çıkanlar: genel except'in özel olanı gölgelemesi, return'lü try'da finally sırası, KeyError mesajındaki tırnaklar, except sonrası atanmamış değişken, alt sınıf except sırası, parantezli assert, from None ile kaybolan neden.
- [x] Yazma görevleri: güvenli bölme (tamamla), kayıt doğrulayıcı — print yerine raise, genel except, kayık satır numarası (düzelt), para transferi hata ailesi ve from ile çeviri (sıfırdan yaz; başarısız transfer durumu bozmamalı).
- [x] Kapsam: 50/109 alt başlık doğrulanmış içerikle kapsanıyor.

Doğrulama: 715 çalıştırılabilir içerik kontrolü; 89 regresyon kontrolü; 85 atölye referans vakası; TypeScript ve üretim derlemesi temiz; tarayıcıda M7 kilidi ve traceback çerçeve örneğinin Pyodide çıktısı denendi.

Sıradaki teslim: Atölye 1 (sipariş/harcama analizi: incele + düzelt + kendi programını yaz) ve Ara sınav 1 (M1–M4). Bu ikisi için yeni arayüz bileşenleri gerekir. Ardından M5. Aşama 1'den açık kalanlar: A1.7 traceback satır seçimi; A1.2 kaynak/çalışma ortamı etiketi; A1.12 tam anlatım denetimi (M1–M2 metinlerinin baştan sona okunması); A1.5 fonksiyon dönüş değeri testleri. Bunlar kapanınca M3–M5 grubuna geçilir.

## 6 Ekim 2026 — M8 Dosyalar

- [x] Çalışma zamanı: her çalıştırma boş bir geçici klasörde başlar ve sonunda klasör silinir (`public/python-runtime.js`). Böylece dosya örnekleri her çalıştırmada aynı sonucu verir; bir çalıştırmanın dosyaları sonrakine sızmaz. Regresyon testi eklendi.
- [x] Doğrulayıcı, modül önekli hata adlarını da tanır (`json.decoder.JSONDecodeError` → JSONDecodeError).
- [x] `content/module-08.json`: open ve modlar (r/w/a/x, eksik dosya), with ve tampon/kapanma, satır satır okuma, pathlib, os/shutil (okuma düzeyi), encoding (UTF-8 bayt sayısı, mojibake, UnicodeDecodeError, errors="replace"), CSV (tırnaklı alan, newline="", DictReader), JSON (tür dönüşümleri, ensure_ascii, JSONDecodeError).
- [x] Belirlenimcilik kuralları: dosya örnekleri okuyacakları dosyayı kendileri oluşturur; listdir/iterdir/glob sonuçları sorted ile yazdırılır; yollar as_posix() ile gösterilir; OSError mesajındaki errno (Pyodide'de 44, Windows/Linux'ta 2) yazdırılmaz, yerine hata türü ve error.filename kullanılır; her open'da encoding açıkça verilir.
- [x] 40 soru (12 çıktı, 6 hata bulma, 4 boşluk, 4 sıralama, 10 kod, 4 traceback). Öne çıkanlar: kapatılmamış dosyanın tamponda kalan verisi, iki kez read(), print(line) ile çift satır aralığı, csv.reader ile split farkı, JSON'da int anahtar/tuple kaybı, başlık satırında int dönüşümü.
- [x] Yazma görevleri: yapılacaklar listesi okuyucu (tamamla), not defteri — "w" yerine "a", eksik satır sonu, not yokken çökme (düzelt), CSV'den JSON rapor; tırnaklı ad, eksik alan ve geçersiz maaş testleriyle (sıfırdan yaz; Atölye 3'ün ön hazırlığı).
- [x] Taşınabilirlik: modüldeki 84 çalıştırılabilir vaka yerel Windows CPython 3.11'de de aynı çıktıyı verdi.
- [x] Kapsam: 55/109 alt başlık doğrulanmış içerikle kapsanıyor; M1–M8 içerikleri tamam.

Doğrulama: 817 çalıştırılabilir içerik kontrolü; 99 regresyon kontrolü; 98 atölye referans vakası; Düzelt ve Sıfırdan yaz görevlerinde yarım düzeltmelerin testlerde yakalandığı denendi.

Sıradaki teslim: Aşama 3'ün içerik kısmı tamamlandı. Açık kalanlar arayüz işleri: Görselleştirme 1, Atölye 1–3, Ara sınav 1 (M1–M4) ve Ara sınav 2 (M1–M8), M8 dosya yükleme/indirme. Ardından M9 (Modüller ve ekosistem).

## 6 Ekim 2026 — M9 Modüller ve ekosistem

- [x] Çalışma zamanı: bir çalıştırmanın yazıp import ettiği modüller (çalışma klasöründen yüklenenler) sys.modules'ten silinir; sys.path ve os.environ çalıştırma sonunda eski hâline döner; her çalıştırma başında importlib.invalidate_caches çağrılır. Böylece aynı modül adı farklı içerikle sonraki çalıştırmalarda doğru yüklenir. Regresyon testi eklendi.
- [x] `content/module-09.json`: import biçimleri, kendi modülün (ilk importta çalışma, sys.modules, sys.path ve gölgeleme, from import ile kopyalanan değer), __name__ == "__main__" (runpy.run_path ile terminal çalıştırması taklidi), paketler ve relative import (runpy.run_module ile python -m taklidi), pip ve venv (find_spec ile kurulum denetimi), requirements.txt ve pyproject.toml (sürüm belirteçleri, tomllib), uv ve poetry (kilit dosyasından aracı tanıma, [tool.poetry] ile [project] farkı), ortam değişkenleri ve .env.
- [x] Önerilen başlangıç akışı pip + venv (python -m venv .venv, python -m pip install); uv ve poetry aynı adımları otomatikleştiren araçlar olarak tanıtıldı; ekip projesinde deponun aracına uyma kuralı verildi.
- [x] Pyodide'de pip/venv/terminal olmadığından ilgili hata senaryoları (yanlış yorumlayıcıya kurulum, tek = belirteci, python app/cli.py ile relative import, random.py gölgelemesi) çalıştırılmayan hata bulma sorularında; çalıştırılabilir kısımlar find_spec, tomllib ve runpy ile.
- [x] 40 soru (12 çıktı, 6 hata bulma, 4 boşluk, 4 sıralama, 10 kod, 4 traceback). Öne çıkanlar: from import sonrası modülde değişen değer, ortam değişkeni varsayılanında str/int karışması, bool("false"), ~= uyumlu sürüm denetimi (sürümleri tuple olarak karşılaştırma), dosya yolundan python -m modül adı.
- [x] Yazma görevleri: ayarları ortamdan okuma (tamamla), bağımlılık denetleyicisi — yorum satırı, pip ad normalleştirme, == çevresindeki boşluk (düzelt), relative importlu metin paketi (sıfırdan yaz; paket yapısı dir() satırıyla sınanıyor, ancak çıktı tabanlı test bu satırın sabit yazılmasını engelleyemez).
- [x] Taşınabilirlik: 92 çalıştırılabilir vaka ve 4 traceback sorusu yerel Windows CPython 3.11'de aynı sonucu verdi.
- [x] Kapsam: 62/109 alt başlık doğrulanmış içerikle kapsanıyor.

Doğrulama: 929 çalıştırılabilir içerik kontrolü; 109 regresyon kontrolü; 112 atölye referans vakası; yarım düzeltmeler testlerde yakalanıyor (Düzelt görevine boşluklu sabitleme testi bu denemeden sonra eklendi).

M9 sonundaki sıradaki teslim M10 idi; aşağıdaki teslimle tamamlandı.

### 6 Ekim 2026 — M10 Standart kütüphane

- Sekiz ders bölümü, 40 soru (10 doğrudan kod yazma sorusu dâhil), 15 soruluk pratik ve üç yazma görevi eklendi.
- Yazma görevleri: Counter sıklık raporu (Tamamla), saat dilimleri arasında toplam süre (Düzelt), argparse/re/Counter günlük analiz aracı (Sıfırdan yaz). Toplam 14 test vakası; eşitlik, boş girdi, negatif süre, farklı saat dilimleri ve tam satır doğrulaması ele alındı.
- Düzelt görevinde yalnız bir hatayı gidermenin yeterli olmadığını doğrulayan iki regresyon testi eklendi.
- M10 derslerine Python 3.12 resmî kaynak bağlantıları ve tarayıcı/yerel ortam ayrımı eklendi. subprocess tarayıcıda çalıştırılabilir gibi sunulmaz. Önceki modüller için A1.2 henüz tamamlanmadı.
- Deterministik sabit tarihler, yerel Random örnekleri ve açık argparse listeleri kullanıldı; gerçek saat, bekleme ve işletim sistemi süreçleri testlere katılmadı.
- Kontroller: 1.037 çalıştırılabilir içerik, 120 regresyon kontrolü, 126 yazma referans vakası; TypeScript ve üretim derlemesi başarılı. Derlemede büyük paket uyarısı var; performans optimizasyonu ayrı iş.
- Durum: 10 modül / 400 soru / 30 yazma görevi; kapsam 70/109 (%64). Bu oran öğrenme başarısı değil, kapsam haritasındaki doğrulanmış içerik oranıdır.

Sıradaki içerik: M11 OOP 1. Atölye 1–4, Ara sınav 1–2, Görselleştirme 1–2 ve M8 dosya arayüzü açık kalır. Çıktı temelli testler kullanılan yöntemi veya bütün girdiler için doğruluğu kanıtlamaz.
