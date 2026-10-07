"""M15 (Eşzamanlılık) questions. Imported by build_m15.py.

Order: 12 output, 6 bug, 4 fill, 4 order, 10 code, 4 traceback (ids m15-q01 ... m15-q40).
Everything that runs is browser-safe: no thread or process is started (bug questions are not run,
so they may show thread/process code). asyncio runs on the site's loop, which skips idle waits;
tests avoid equal deadlines so the finishing order is the same as in local Python.
"""

from _qhelper import make_questions

questions, q = make_questions("m15")

# ------------------------------------------------------------------ output (12)
q(type="output", topic="io-sure", sectionId="io-cpu", difficulty=1,
  prompt="Üç indirme sırayla ve beklemeleri örtüşerek yapılıyor. Toplam süreler ne olur?",
  code=r'''
waits = [0.4, 0.2, 0.4]
print(round(sum(waits), 1), max(waits))
''',
  expectedOutput="1.0 0.4",
  options=["1.0 0.4", "1.0 1.0", "0.4 1.0", "1.0 0.2"],
  hints=["Sırayla çalışınca süreler toplanır.", "Beklemeler örtüşünce en uzun bekleme belirleyicidir."],
  explanation="Sırayla 0,4 + 0,2 + 0,4 = 1,0 saniye sürer; beklemeler örtüşürse toplam süre en uzun beklemeye, 0,4 saniyeye iner.")

q(type="output", topic="run-start", sectionId="threads", difficulty=3,
  prompt="Thread nesnesinde start() yerine run() çağrılıyor. Çıktı ne olur?",
  code=r'''
import threading

def work():
    print("çalışan:", threading.current_thread().name)

t = threading.Thread(target=work, name="yardımcı")
t.run()
print(t.name, t.is_alive())
''',
  expectedOutput="çalışan: MainThread\nyardımcı False",
  options=["çalışan: MainThread / yardımcı False", "çalışan: yardımcı / yardımcı False", "çalışan: yardımcı / yardımcı True", "çalışan: MainThread / yardımcı True"],
  optionFeedback={
      "çalışan: yardımcı / yardımcı False": "Yeni thread'i başlatan start()'tır; run() hedefi çağıran thread'de çalıştırır.",
      "çalışan: yardımcı / yardımcı True": "Hiçbir thread başlatılmadı; iş ana thread'de yapıldı ve t hiç canlı olmadı.",
      "çalışan: MainThread / yardımcı True": "t.start() hiç çağrılmadığı için t hiç canlı olmaz.",
  },
  hints=["Yeni iş parçacığını hangi metot başlatır?", "run() yalnızca target'ı olduğu yerde çağırır."],
  explanation="run() işi yeni bir thread'de değil, onu çağıran ana thread'de (MainThread) sırayla yapar; t hiç başlatılmadığı için is_alive() False döner. Eşzamanlı çalıştırmak için start() çağrılır.")

q(type="output", topic="future-hata", sectionId="threads", difficulty=2,
  prompt="Bir Future'a hata konuyor ve sonucu isteniyor. Çıktı ne olur?",
  code=r'''
from concurrent.futures import Future

future = Future()
future.set_exception(ValueError("bozuk satır"))
print(future.done())
try:
    print(future.result())
except ValueError as error:
    print("yakalandı:", error)
''',
  expectedOutput="True\nyakalandı: bozuk satır",
  options=["True / yakalandı: bozuk satır", "False / yakalandı: bozuk satır", "True / None", "True / bozuk satır"],
  hints=["Hata da bir sonuçtur: Future hata ile tamamlanmış sayılır mı?", "result() saklanan hatayla ne yapar?"],
  explanation="Future hata ile tamamlanınca done() True döner. result() sonucu vermek yerine saklanan ValueError'ı yeniden fırlatır; bu yüzden havuzdaki bir işin hatası ana kodda yakalanabilir.")

q(type="output", topic="parcalama", sectionId="gil-processes", difficulty=2,
  prompt="İş, süreçlere dağıtmak için parçalanıyor. Parça boyutları ne olur?",
  code=r'''
def split(items, parts):
    size = -(-len(items) // parts)
    return [items[i:i + size] for i in range(0, len(items), size)]

print([len(part) for part in split(list(range(10)), 3)])
''',
  expectedOutput="[4, 4, 2]",
  options=["[4, 4, 2]", "[3, 3, 4]", "[3, 3, 3, 1]", "[4, 4, 4]"],
  hints=["-(-a // b) yukarı yuvarlanmış bölmedir: 10 / 3 → 4.", "Son parça kalan öğeleri alır."],
  explanation="Parça boyutu yukarı yuvarlanır: -(-10 // 3) = 4. Dilimler 0–4, 4–8 ve 8–10 olur: 4, 4 ve 2 öğe.")

q(type="output", topic="coroutine-nesnesi", sectionId="coroutines", difficulty=1,
  prompt="Bir async fonksiyon çağrılıyor ama hemen çalıştırılmıyor. Çıktı ne olur?",
  code=r'''
import asyncio

async def load():
    print("içeride")
    return 1

job = load()
print("dışarıda")
print(asyncio.run(job))
''',
  expectedOutput="dışarıda\niçeride\n1",
  options=["dışarıda / içeride / 1", "içeride / dışarıda / 1", "dışarıda / 1", "içeride / 1 / dışarıda"],
  optionFeedback={
      "içeride / dışarıda / 1": "load() çağrısı gövdeyi çalıştırmaz; yalnızca bir coroutine nesnesi üretir.",
      "dışarıda / 1": "asyncio.run coroutine'i çalıştırır; gövdedeki print de çalışır.",
      "içeride / 1 / dışarıda": "'dışarıda', coroutine çalıştırılmadan önce yazdırılıyor.",
  },
  hints=["async fonksiyonu çağırmak gövdeyi çalıştırır mı?", "Gövde ne zaman çalışır?"],
  explanation="load() yalnızca bir coroutine nesnesi döndürür; gövde, asyncio.run onu çalıştırınca yürür. Bu yüzden önce 'dışarıda', sonra 'içeride' ve dönüş değeri 1 yazılır.")

q(type="output", topic="ardisik-await", sectionId="coroutines", difficulty=2,
  prompt="Üç bekleme art arda await ediliyor. Ölçülen süre ne olur?",
  code=r'''
import asyncio

async def wait(seconds):
    await asyncio.sleep(seconds)

async def main():
    loop = asyncio.get_running_loop()
    start = loop.time()
    await wait(0.1)
    await wait(0.2)
    await wait(0.3)
    print(f"{loop.time() - start:.1f}")

asyncio.run(main())
''',
  expectedOutput="0.6",
  options=["0.6", "0.3", "0.1", "0.0"],
  optionFeedback={
      "0.3": "Bu, beklemeler aynı anda yürüseydi doğru olurdu; art arda await'ler birbirini bekler.",
      "0.1": "En kısa bekleme belirleyici değil; her await bir öncekinin bitmesini bekler.",
      "0.0": "asyncio.sleep görevi gerçekten duraklatır; loop.time() bu süre kadar ilerler.",
  },
  hints=["İkinci await, birincisi bitmeden başlar mı?", "Art arda beklemelerde süreler toplanır mı?"],
  explanation="Her await, beklediği iş bitene kadar main'i duraklatır; üç bekleme sırayla yapılır ve süreler toplanır: 0,1 + 0,2 + 0,3 = 0,6 saniye. Aynı anda yürütmek için gather gerekir.")

q(type="output", topic="gather-sira", sectionId="tasks-gather", difficulty=1,
  prompt="gather ile iki görev yürütülüyor. Çıktı ne olur?",
  code=r'''
import asyncio

async def job(name, delay):
    await asyncio.sleep(delay)
    print(name)
    return name

async def main():
    print(await asyncio.gather(job("x", 0.3), job("y", 0.1)))

asyncio.run(main())
''',
  expectedOutput="y\nx\n['x', 'y']",
  options=["y / x / ['x', 'y']", "x / y / ['x', 'y']", "y / x / ['y', 'x']", "x / y / ['y', 'x']"],
  optionFeedback={
      "x / y / ['x', 'y']": "Görevler aynı anda bekler; kısa bekleyen y önce biter ve önce yazar.",
      "y / x / ['y', 'x']": "Bitiş sırası y, x olsa da gather sonuçları verilen sırayla döndürür.",
      "x / y / ['y', 'x']": "Hem yazdırma sırası hem liste sırası ters.",
  },
  hints=["Hangi görev önce uyanır?", "gather sonuç listesini hangi sıraya göre kurar?"],
  explanation="İki görev birlikte bekler; 0,1 saniyelik y önce biter ve önce yazar. gather ise sonuçları bitiş sırasına değil, verilen sıraya göre döndürür: ['x', 'y'].")

q(type="output", topic="create-task-zaman", sectionId="tasks-gather", difficulty=3,
  prompt="create_task ile başlatılan görev ne zaman çalışır? Çıktı ne olur?",
  code=r'''
import asyncio

async def child():
    print("çocuk")

async def main():
    task = asyncio.create_task(child())
    print("ana 1")
    await asyncio.sleep(0)
    print("ana 2")
    await task

asyncio.run(main())
''',
  expectedOutput="ana 1\nçocuk\nana 2",
  options=["ana 1 / çocuk / ana 2", "çocuk / ana 1 / ana 2", "ana 1 / ana 2 / çocuk", "çocuk / ana 2"],
  optionFeedback={
      "çocuk / ana 1 / ana 2": "create_task görevi planlar ama hemen çalıştırmaz; main önce kendi satırına devam eder.",
      "ana 1 / ana 2 / çocuk": "await asyncio.sleep(0) main'i bir tur duraklatır ve sıradaki hazır görev, child, çalışır.",
      "çocuk / ana 2": "'ana 1' await'ten önce, hiçbir duraklama olmadan yazılır.",
  },
  hints=["create_task görevi hemen mi çalıştırır, yoksa planlar mı?", "main ilk kez nerede duraklıyor?"],
  explanation="create_task görevi event loop'a planlar ve hemen döner; main 'ana 1' yazar. await asyncio.sleep(0) main'i bir tur duraklatınca sıradaki hazır görev olan child çalışır ve 'çocuk' yazar; sonra main 'ana 2' ile devam eder.")

q(type="output", topic="bloklama-sira", sectionId="blocking-loop", difficulty=2,
  prompt="İki görevden biri time.sleep ile bekliyor. Çıktı ne olur?",
  code=r'''
import asyncio
import time

async def slow():
    time.sleep(0.1)
    print("yavaş")

async def quick():
    print("hızlı")

async def main():
    await asyncio.gather(slow(), quick())

asyncio.run(main())
''',
  expectedOutput="yavaş\nhızlı",
  options=["yavaş / hızlı", "hızlı / yavaş", "hızlı", "yavaş"],
  optionFeedback={
      "hızlı / yavaş": "Bu, slow await asyncio.sleep kullansaydı doğru olurdu; time.sleep döngüye sıra vermez.",
      "hızlı": "slow görevi de tamamlanır; yalnızca diğerlerini bekletir.",
      "yavaş": "quick görevi de çalışır; slow bittikten sonra sıra ona gelir.",
  },
  hints=["slow içinde hiç await var mı?", "time.sleep sırasında event loop başka bir görevi çalıştırabilir mi?"],
  explanation="gather önce slow'u başlatır. slow'da hiç await olmadığı için time.sleep bütün döngüyü durdurur ve slow bitene kadar quick çalışamaz. await asyncio.sleep(0.1) kullanılsaydı önce 'hızlı' yazılırdı.")

q(type="output", topic="wait-for-finally", sectionId="cancellation-timeout", difficulty=2,
  prompt="Süre sınırı aşılan bir işin finally bloğu var. Çıktı ne olur?",
  code=r'''
import asyncio

async def slow():
    try:
        await asyncio.sleep(1)
    finally:
        print("temizlik")

async def main():
    try:
        await asyncio.wait_for(slow(), timeout=0.1)
    except TimeoutError:
        print("zaman aşımı")

asyncio.run(main())
''',
  expectedOutput="temizlik\nzaman aşımı",
  options=["temizlik / zaman aşımı", "zaman aşımı / temizlik", "zaman aşımı", "temizlik"],
  optionFeedback={
      "zaman aşımı / temizlik": "wait_for, iptal edilen işin bitmesini (finally dahil) bekledikten sonra TimeoutError fırlatır.",
      "zaman aşımı": "İptal görevde CancelledError olarak görünür ve finally çalışır.",
      "temizlik": "İş süresinde bitmediği için wait_for TimeoutError fırlatır ve except çalışır.",
  },
  hints=["Süre dolunca wait_for slow'a ne yapar?", "İptal edilen görevde finally çalışır mı, ne zaman?"],
  explanation="0,1 saniye dolunca wait_for slow'u iptal eder: slow'da CancelledError oluşur ve finally 'temizlik' yazar. wait_for iptalin bitmesini bekler, sonra TimeoutError fırlatır ve main 'zaman aşımı' yazar.")

q(type="output", topic="iptal-yutma", sectionId="cancellation-timeout", difficulty=3,
  prompt="Görev iptal ediliyor ama CancelledError yakalanıp yutuluyor. Çıktı ne olur?",
  code=r'''
import asyncio

async def stubborn():
    try:
        await asyncio.sleep(1)
    except asyncio.CancelledError:
        print("yuttum")
    return "bitti"

async def main():
    task = asyncio.create_task(stubborn())
    await asyncio.sleep(0)
    task.cancel()
    print(await task, task.cancelled())

asyncio.run(main())
''',
  expectedOutput="yuttum\nbitti False",
  options=["yuttum / bitti False", "yuttum / bitti True", "CancelledError verir", "bitti False"],
  optionFeedback={
      "yuttum / bitti True": "Görev hatayı yeniden fırlatmadığı için normal biçimde değer döndürerek bitti; iptal edilmiş sayılmaz.",
      "CancelledError verir": "Hata görevin içinde yakalandı ve yeniden fırlatılmadı; await task normal sonucu alır.",
      "bitti False": "cancel() görevin beklediği yerde CancelledError fırlatır ve except bloğu çalışır.",
  },
  hints=["cancel() görevin içinde ne fırlatır?", "Hata yeniden fırlatılmazsa görev nasıl biter?"],
  explanation="cancel() görevin beklediği await'te CancelledError fırlatır; görev onu yakalayıp yutar ve 'bitti' döndürür. İptal tamamlanmadığı için cancelled() False olur. Bu yüzden CancelledError yakalanırsa sonunda raise ile yeniden fırlatılmalıdır.")

q(type="output", topic="yaris", sectionId="shared-state", difficulty=2,
  prompt="Beş görev aynı sayacı okuyup bir tur bekledikten sonra artırıyor. Çıktı ne olur?",
  code=r'''
import asyncio

counter = {"n": 0}

async def increment():
    value = counter["n"]
    await asyncio.sleep(0)
    counter["n"] = value + 1

async def main():
    await asyncio.gather(*(increment() for _ in range(5)))
    print(counter["n"])

asyncio.run(main())
''',
  expectedOutput="1",
  options=["1", "5", "0", "6"],
  optionFeedback={
      "5": "Her görev okuduktan sonra bekliyor; beşi de 0 okuduktan sonra yazma başlıyor.",
      "0": "Her görev 0 + 1 = 1 yazar; sayaç 0'da kalmaz.",
      "6": "Başlangıç 0 ve en fazla beş artış var; üstelik artışlar birbirini eziyor.",
  },
  hints=["Görevler okuma ile yazma arasında duraklıyor; o sırada diğerleri ne okur?", "Her görev hangi değere 1 ekleyip yazıyor?"],
  explanation="Beş görevin hepsi önce 0'ı okur ve await'te duraklar; sonra her biri kendi okuduğu eski değere göre 1 yazar. Dört güncelleme kaybolur ve sonuç 1 olur: klasik yarış durumu. Okuma ve yazma bir asyncio.Lock ile korunmalıdır.")

# ------------------------------------------------------------------ bug (6)
q(type="bug", topic="args-demet", sectionId="threads", difficulty=1,
  prompt="Thread başlatılınca iş hiç yapılmıyor ve thread içinde TypeError görülüyor. Hata nerede?",
  code=r'''
import threading

def report(page):
    print("sayfa", page)

worker = threading.Thread(target=report, args=(5))
worker.start()
worker.join()
''',
  answer="args bir demet olmalı: (5) yalnızca 5 sayısıdır, doğrusu args=(5,)",
  options=[
      "args bir demet olmalı: (5) yalnızca 5 sayısıdır, doğrusu args=(5,)",
      "target'a fonksiyon değil çağrısı verilmeli: target=report(5)",
      "join() start()'tan önce çağrılmalı",
      "Thread içinde print kullanılamaz",
  ],
  optionFeedback={
      "target'a fonksiyon değil çağrısı verilmeli: target=report(5)": "report(5) fonksiyonu hemen ana thread'de çalıştırır ve target'a None verir.",
      "join() start()'tan önce çağrılmalı": "Başlamamış bir thread join edilemez (RuntimeError); sıra start sonra join'dir.",
      "Thread içinde print kullanılamaz": "print thread'lerde de çalışır; sorun argümanların veriliş biçiminde.",
  },
  hints=["(5) ile (5,) arasındaki fark nedir?", "Thread, target'ı target(*args) diye çağırır."],
  explanation="Parantez tek başına demet oluşturmaz: (5) bir int'tir. Thread report(*args) çağırırken int'i açamaz ve TypeError oluşur. Tek öğeli demet virgülle yazılır: args=(5,).")

q(type="bug", topic="join-yok", sectionId="threads", difficulty=2,
  prompt="Program bazen boş liste, bazen eksik sonuç yazdırıyor. Hata nerede?",
  code=r'''
import threading
import time

results = []

def fetch(page):
    time.sleep(0.2)
    results.append(page)

for page in range(3):
    threading.Thread(target=fetch, args=(page,)).start()
print(results)
''',
  answer="Thread'ler join edilmeden sonuç okunuyor; thread'leri listede tutup print'ten önce join() çağrılmalı",
  options=[
      "Thread'ler join edilmeden sonuç okunuyor; thread'leri listede tutup print'ten önce join() çağrılmalı",
      "results listesine thread'lerden eleman eklenemez",
      "time.sleep thread'lerde çalışmaz",
      "range(3) yerine üç ayrı Thread sınıfı yazılmalı",
  ],
  optionFeedback={
      "results listesine thread'lerden eleman eklenemez": "Thread'ler aynı belleği paylaşır; append çalışır, ama print'e yetişmez.",
      "time.sleep thread'lerde çalışmaz": "time.sleep yalnızca o thread'i bekletir; sorun ana thread'in beklememesi.",
      "range(3) yerine üç ayrı Thread sınıfı yazılmalı": "Aynı sınıftan üç nesne oluşturmak doğrudur.",
  },
  hints=["start() thread bitene kadar bekler mi?", "Ana thread print'e geldiğinde fetch'ler bitmiş midir?"],
  explanation="start() hemen döner; ana thread 0,2 saniyelik beklemeler bitmeden print'e ulaşır. Thread'leri bir listeye koyup her biri için join() çağırmak, sonuçlar hazır olmadan okunmasını önler. Daha iyisi ThreadPoolExecutor ile sonuçları Future'lardan almaktır.")

q(type="bug", topic="main-korumasi", sectionId="gil-processes", difficulty=2,
  prompt="Bu kod bazı Linux kurulumlarında çalışıyor ama Windows'ta alt süreçler RuntimeError verip havuz çöküyor. Hata nerede?",
  code=r'''
from concurrent.futures import ProcessPoolExecutor

def square(n):
    return n * n

with ProcessPoolExecutor() as pool:
    print(list(pool.map(square, range(5))))
''',
  answer="Süreç başlatan kod if __name__ == '__main__': koruması altında değil; Windows'ta her alt süreç dosyayı yeniden içe aktarıp yine süreç başlatmaya çalışır",
  options=[
      "Süreç başlatan kod if __name__ == '__main__': koruması altında değil; Windows'ta her alt süreç dosyayı yeniden içe aktarıp yine süreç başlatmaya çalışır",
      "square bir lambda olmalı",
      "ProcessPoolExecutor with ile kullanılamaz",
      "pool.map yalnızca listeler kabul eder, range verilemez",
  ],
  optionFeedback={
      "square bir lambda olmalı": "Tersine: lambda pickle edilemez; süreçlere modül düzeyindeki fonksiyonlar gönderilir.",
      "ProcessPoolExecutor with ile kullanılamaz": "with doğru kullanımdır; blok sonunda havuz kapatılır.",
      "pool.map yalnızca listeler kabul eder, range verilemez": "map her dolaşılabilir nesneyi kabul eder.",
  },
  hints=["Windows'ta yeni süreç programı nasıl başlatır?", "M9'daki __main__ korumasını hatırla."],
  explanation="Windows ve macOS'ta (Python 3.14'ten beri Linux'ta da varsayılan olarak) alt süreç ana dosyayı baştan içe aktarır. Havuzu kuran kod korumasızsa her alt süreç yeniden süreç başlatmaya çalışır; multiprocessing bunu RuntimeError ile durdurur ve havuz BrokenProcessPool ile çöker. with bloğu if __name__ == '__main__': altına alınmalıdır.")

q(type="bug", topic="gil-cpu", sectionId="gil-processes", difficulty=3,
  prompt="Saf Python asal sayı hesabı 4 thread'e bölündü ama hiç hızlanmadı. Neden?",
  code=r'''
from concurrent.futures import ThreadPoolExecutor

def count_primes(bounds):
    low, high = bounds
    return sum(1 for n in range(max(low, 2), high)
               if all(n % d for d in range(2, int(n ** 0.5) + 1)))

chunks = [(0, 50_000), (50_000, 100_000), (100_000, 150_000), (150_000, 200_000)]
with ThreadPoolExecutor(max_workers=4) as pool:
    print(sum(pool.map(count_primes, chunks)))
''',
  answer="İş CPU bağımlı; standart CPython'da GIL aynı anda tek thread'in Python kodu çalıştırmasına izin verir, ProcessPoolExecutor kullanılmalı",
  options=[
      "İş CPU bağımlı; standart CPython'da GIL aynı anda tek thread'in Python kodu çalıştırmasına izin verir, ProcessPoolExecutor kullanılmalı",
      "max_workers 4 yerine 400 olmalı",
      "pool.map sonuçları sırayla verdiği için işler de sırayla çalışıyor",
      "Parçalar eşit olmadığı için hızlanma olmuyor",
  ],
  optionFeedback={
      "max_workers 4 yerine 400 olmalı": "Daha çok thread GIL'i aşmaz; geçiş maliyeti yüzünden daha da yavaşlatır.",
      "pool.map sonuçları sırayla verdiği için işler de sırayla çalışıyor": "map sonuçları sırayla verir ama işleri birlikte başlatır; engel GIL'dir.",
      "Parçalar eşit olmadığı için hızlanma olmuyor": "Parçalar aynı genişlikte; eşit olsalar da thread'lerle hızlanmazdı.",
  },
  hints=["Bu iş bekliyor mu, hesaplıyor mu?", "CPython'da aynı anda kaç thread Python bayt kodu çalıştırabilir?"],
  explanation="Thread'ler yalnızca beklerken GIL'i bırakır; saf Python hesabında dört thread sırayla ilerler. Hesabı çekirdeklere dağıtmak için ProcessPoolExecutor (ve if __name__ == '__main__' koruması) kullanılır. Free-threaded derlemelerde (3.13t, 3.14t) bu durum değişebilir.")

q(type="bug", topic="time-sleep-async", sectionId="blocking-loop", difficulty=2,
  prompt="Üç indirme gather ile 'aynı anda' başlatıldı ama toplam süre 0,5 değil 1,5 saniye. Hata nerede?",
  code=r'''
import asyncio
import time

async def download(name):
    time.sleep(0.5)
    return name

async def main():
    print(await asyncio.gather(download("a"), download("b"), download("c")))

asyncio.run(main())
''',
  answer="time.sleep event loop'u blokluyor; coroutine içinde await asyncio.sleep(0.5) kullanılmalı",
  options=[
      "time.sleep event loop'u blokluyor; coroutine içinde await asyncio.sleep(0.5) kullanılmalı",
      "gather görevleri sırayla çalıştırır; create_task kullanılmalı",
      "asyncio.run birden çok görev çalıştıramaz",
      "download async def değil def olmalı",
  ],
  optionFeedback={
      "gather görevleri sırayla çalıştırır; create_task kullanılmalı": "gather görevleri birlikte başlatır; ama hiçbiri await etmediği için birbirini bekliyorlar.",
      "asyncio.run birden çok görev çalıştıramaz": "asyncio.run tek bir giriş coroutine'i alır; onun içinde istenildiği kadar görev çalışır.",
      "download async def değil def olmalı": "Sıradan fonksiyon gather'a verilemez; doğru olan beklemeyi await edilebilir yapmaktır.",
  },
  hints=["download içinde hiç await var mı?", "time.sleep sırasında event loop başka görevi çalıştırabilir mi?"],
  explanation="time.sleep, döngüye sıra vermeden bütün iş parçacığını durdurur; görevler birbirini bekler ve süreler toplanır. await asyncio.sleep(0.5) yalnızca o görevi duraklatır ve üç bekleme örtüşür. Async olmayan gerçek bir çağrı ise asyncio.to_thread ile thread'e aktarılır.")

q(type="bug", topic="iptal-yutma", sectionId="cancellation-timeout", difficulty=3,
  prompt="Servis yanıt vermediğinde 'zaman aşımı' yazılması bekleniyor ama ekranda None görülüyor. Hata nerede?",
  code=r'''
import asyncio

async def fetch():
    try:
        await asyncio.sleep(5)
        return "veri"
    except asyncio.CancelledError:
        return None

async def main():
    try:
        print(await asyncio.wait_for(fetch(), timeout=0.5))
    except TimeoutError:
        print("zaman aşımı")

asyncio.run(main())
''',
  answer="fetch CancelledError'ı yakalayıp yutuyor; iptal tamamlanmadığı için wait_for TimeoutError fırlatamıyor, except bloğunda raise yazılmalı",
  options=[
      "fetch CancelledError'ı yakalayıp yutuyor; iptal tamamlanmadığı için wait_for TimeoutError fırlatamıyor, except bloğunda raise yazılmalı",
      "timeout 0.5 yerine 5 olmalı",
      "asyncio.CancelledError yerine TimeoutError yakalanmalı",
      "wait_for yalnızca görevlerle çalışır, coroutine verilemez",
  ],
  optionFeedback={
      "timeout 0.5 yerine 5 olmalı": "Süre sınırını büyütmek zaman aşımını gizler; sorun iptalin yutulması.",
      "asyncio.CancelledError yerine TimeoutError yakalanmalı": "Görevin içine TimeoutError değil CancelledError ulaşır; TimeoutError'ı wait_for dışarıda fırlatır.",
      "wait_for yalnızca görevlerle çalışır, coroutine verilemez": "wait_for coroutine'i kendisi göreve çevirir.",
  },
  hints=["Süre dolunca wait_for fetch'e ne gönderir?", "Görev iptali yutup değer döndürürse wait_for neyi görür?"],
  explanation="Süre dolunca wait_for görevi iptal eder; görevde CancelledError oluşur. fetch onu yakalayıp None döndürünce iptal 'başarısız' olur ve wait_for TimeoutError yerine None'ı döndürür. İptali yakalayan kod temizlikten sonra raise ile yeniden fırlatmalı ya da yalnızca finally kullanmalıdır.")

# ------------------------------------------------------------------ fill (4)
q(type="fill", topic="async-def", sectionId="coroutines", difficulty=1,
  prompt="Coroutine fonksiyonu tanımlayan anahtar kelimeyi yaz.",
  code=r'''
import asyncio

___ def greet(name):
    await asyncio.sleep(0.1)
    return f"merhaba {name}"

print(asyncio.run(greet("Ada")))
''',
  answer="async",
  expectedOutput="merhaba Ada",
  hints=["await yalnızca bu tür fonksiyonların içinde yazılabilir.", "def'in önüne gelen kelime."],
  explanation="async def bir coroutine fonksiyonu tanımlar; içinde await kullanılabilir ve asyncio.run onu çalıştırır.")

q(type="fill", topic="gather", sectionId="tasks-gather", difficulty=1,
  prompt="Coroutine'leri aynı anda yürütüp sonuçlarını sırayla toplayan fonksiyonu yaz.",
  code=r'''
import asyncio

async def square(n):
    await asyncio.sleep(0.1)
    return n * n

async def main():
    results = await asyncio.___(square(2), square(3), square(4))
    print(results)

asyncio.run(main())
''',
  answer="gather",
  expectedOutput="[4, 9, 16]",
  hints=["Adı 'toplamak' demektir.", "Sonuçları verilen sırayla bir liste olarak döndürür."],
  explanation="asyncio.gather verilen coroutine'leri görev olarak birlikte başlatır, hepsini bekler ve sonuçları verilen sırayla döndürür.")

q(type="fill", topic="timeout-hatasi", sectionId="cancellation-timeout", difficulty=2,
  prompt="wait_for süre sınırı aşılınca fırlatılan hatayı yakala.",
  code=r'''
import asyncio

async def main():
    try:
        await asyncio.wait_for(asyncio.sleep(10), timeout=0.2)
    except ___:
        print("süre doldu")

asyncio.run(main())
''',
  answer="TimeoutError",
  acceptedAnswers=["TimeoutError", "asyncio.TimeoutError"],
  expectedOutput="süre doldu",
  hints=["Yerleşik bir hata türü; adı 'zaman aşımı hatası' demektir.", "Python 3.11'den beri asyncio'daki aynı adlı hata bununla aynıdır."],
  explanation="Süre dolunca wait_for işi iptal eder ve TimeoutError fırlatır. Python 3.11'den beri asyncio.TimeoutError yerleşik TimeoutError'ın takma adıdır; ikisi de çalışır.")

q(type="fill", topic="async-with-lock", sectionId="shared-state", difficulty=2,
  prompt="asyncio kilidini async bağlam yöneticisi olarak kullanan kelimeyi yaz.",
  code=r'''
import asyncio

lock = asyncio.Lock()
log = []

async def write(line):
    async ___ lock:
        log.append(line)
        await asyncio.sleep(0.1)
        log.append(line.upper())

async def main():
    await asyncio.gather(write("a"), write("b"))
    print(log)

asyncio.run(main())
''',
  answer="with",
  expectedOutput="['a', 'A', 'b', 'B']",
  hints=["Dosyaları kapatan bloğun adı (M8).", "async ile birlikte bir bağlam yöneticisi bloğu açar."],
  explanation="async with lock: kilidi alır ve blok bitince bırakır. İkinci görev kilidi bekler; bu yüzden her görevin iki satırı bölünmeden yan yana yazılır.")

# ------------------------------------------------------------------ order (4)
q(type="order", topic="async-iskelet", sectionId="coroutines", difficulty=1,
  prompt="Bir coroutine tanımlayıp asyncio.run ile çalıştıran sırayı kur.",
  answer_lines=[
      "import asyncio",
      "async def main():",
      "    await asyncio.sleep(0.1)",
      '    print("hazır")',
      "asyncio.run(main())",
  ],
  perm=[3, 0, 4, 2, 1],
  expectedOutput="hazır",
  hints=["İçe aktarma en üstte olur.", "asyncio.run, main tanımlandıktan sonra çağrılır."],
  explanation="asyncio içe aktarılır, main coroutine'i tanımlanır, içinde await ile beklenir ve en sonda asyncio.run(main()) ile çalıştırılır.")

q(type="order", topic="taskgroup", sectionId="tasks-gather", difficulty=2,
  prompt="İki görevi TaskGroup ile çalıştırıp sonuçlarını yazdıran sırayı kur.",
  answer_lines=[
      "import asyncio",
      "async def double(n):",
      "    await asyncio.sleep(0.1)",
      "    return n * 2",
      "async def main():",
      "    async with asyncio.TaskGroup() as group:",
      "        first = group.create_task(double(3))",
      "        second = group.create_task(double(5))",
      "    print(first.result() + second.result())",
      "asyncio.run(main())",
  ],
  perm=[5, 9, 1, 7, 3, 0, 8, 2, 6, 4],
  expectedOutput="16",
  hints=["Görevler TaskGroup bloğunun içinde oluşturulur.", "Sonuçlar blok bittikten sonra okunur; print, with ile aynı hizadadır."],
  explanation="TaskGroup bloğu iki görevin de bitmesini bekler; blok kapandıktan sonra sonuçlar güvenle okunur: 6 + 10 = 16.")

q(type="order", topic="parcala-birlestir", sectionId="gil-processes", difficulty=2,
  prompt="İşi parçalara bölüp her parçayı ayrı hesaplayan ve sonuçları birleştiren sırayı kur.",
  answer_lines=[
      "def total_squares(part):",
      "    return sum(n * n for n in part)",
      "numbers = list(range(1, 7))",
      "parts = [numbers[:3], numbers[3:]]",
      "partials = list(map(total_squares, parts))",
      "print(partials, sum(partials))",
  ],
  perm=[4, 2, 0, 5, 3, 1],
  expectedOutput="[14, 77] 91",
  hints=["Fonksiyon, map'e verilmeden önce tanımlanmalı.", "Parçalar, sayılar oluşturulduktan sonra kesilir."],
  explanation="Her parça bağımsız hesaplanır: 1 + 4 + 9 = 14 ve 16 + 25 + 36 = 77; sonra ana kodda birleştirilir. Yerelde map yerine ProcessPoolExecutor().map yazmak her parçayı ayrı süreçte hesaplar.")

q(type="order", topic="kilitli-cekim", sectionId="shared-state", difficulty=3,
  prompt="Kilitle korunan bir para çekme coroutine'inin gövdesini sırala.",
  answer_lines=[
      "import asyncio",
      "balance = {'tl': 100}",
      "lock = asyncio.Lock()",
      "async def withdraw(amount):",
      "    async with lock:",
      "        if balance['tl'] >= amount:",
      "            await asyncio.sleep(0.1)",
      "            balance['tl'] -= amount",
      "async def main():",
      "    await asyncio.gather(withdraw(80), withdraw(70))",
      "    print(balance['tl'])",
      "asyncio.run(main())",
  ],
  perm=[6, 10, 3, 0, 8, 5, 11, 1, 7, 4, 9, 2],
  expectedOutput="20",
  hints=["Denetim de yazma da kilidin içinde olmalı.", "Bekleme, denetimden sonra ve düşmeden önce gelir."],
  explanation="Kilit, denetle-bekle-yaz adımlarını tek parça yapar: ilk görev 80 çeker, ikinci görev kilidi aldığında bakiye 20'dir ve 70 çekilemez.")

# ------------------------------------------------------------------ code (10)
q(type="code", topic="io-sure", sectionId="io-cpu", difficulty=1,
  prompt="İlk satırda boşlukla ayrılmış bekleme süreleri (saniye) var. Sırayla yapılınca toplam süreyi, beklemeler örtüşünce süreyi ve aradaki kazancı birer ondalıkla yaz: 'sırayla: 1.7', 'örtüşerek: 0.8', 'kazanç: 0.9'.",
  starterCode=r'''
waits = [float(part) for part in input().split()]
print(f"sırayla: {sum(waits):.1f}")
# örtüşerek ve kazanç satırlarını ekle
''',
  answer=r'''
waits = [float(part) for part in input().split()]
sequential = sum(waits)
overlapped = max(waits)
print(f"sırayla: {sequential:.1f}")
print(f"örtüşerek: {overlapped:.1f}")
print(f"kazanç: {sequential - overlapped:.1f}")
''',
  exampleInput="0.8 0.3 0.6",
  expectedOutput="sırayla: 1.7\nörtüşerek: 0.8\nkazanç: 0.9",
  tests=[
      {"label": "Örnek", "stdin": "0.8 0.3 0.6", "expectedOutput": "sırayla: 1.7\nörtüşerek: 0.8\nkazanç: 0.9"},
      {"label": "Eşit beklemeler", "stdin": "1 1 1 1", "expectedOutput": "sırayla: 4.0\nörtüşerek: 1.0\nkazanç: 3.0"},
      {"label": "Tek iş", "stdin": "0.5", "expectedOutput": "sırayla: 0.5\nörtüşerek: 0.5\nkazanç: 0.0"},
  ],
  hints=["Örtüşen beklemelerde toplam süre en uzun beklemedir: max.", "Kazanç, sıralı süre ile örtüşen süre arasındaki farktır."],
  explanation="Sırayla yapılan işlerde süreler toplanır; beklemeler örtüşünce en uzun bekleme belirleyicidir. Tek iş varken eşzamanlılık bir şey kazandırmaz.")

q(type="code", topic="executor-future", sectionId="threads", difficulty=2,
  prompt="run_all(executor, func, items) fonksiyonunu yaz: her öğe için executor.submit ile iş başlatsın, sonra Future'ların sonucunu girdi sırasıyla okuyup 'öğe -> sonuç' ya da hata olursa 'öğe -> hata: HataAdı' satırlarının listesini döndürsün. InlineExecutor (ThreadPoolExecutor ile aynı arayüz) ve program hazır; double geçersiz sayıda ValueError verir.",
  starterCode=r'''
from concurrent.futures import Executor, Future

class InlineExecutor(Executor):
    def submit(self, fn, /, *args, **kwargs):
        future = Future()
        try:
            future.set_result(fn(*args, **kwargs))
        except Exception as error:
            future.set_exception(error)
        return future

def double(text):
    return int(text) * 2

def run_all(executor, func, items):
    # submit ile işleri başlat, result() ile sonuçları topla; hataları yakala
    return [f"{item} -> {func(item)}" for item in items]

lines = run_all(InlineExecutor(), double, input().split())
print("\n".join(lines))
print("hata sayısı:", sum("hata" in line for line in lines))
''',
  answer=r'''
from concurrent.futures import Executor, Future

class InlineExecutor(Executor):
    def submit(self, fn, /, *args, **kwargs):
        future = Future()
        try:
            future.set_result(fn(*args, **kwargs))
        except Exception as error:
            future.set_exception(error)
        return future

def double(text):
    return int(text) * 2

def run_all(executor, func, items):
    with executor:
        futures = [executor.submit(func, item) for item in items]
    lines = []
    for item, future in zip(items, futures):
        try:
            lines.append(f"{item} -> {future.result()}")
        except Exception as error:
            lines.append(f"{item} -> hata: {type(error).__name__}")
    return lines

lines = run_all(InlineExecutor(), double, input().split())
print("\n".join(lines))
print("hata sayısı:", sum("hata" in line for line in lines))
''',
  exampleInput="3 x 10",
  expectedOutput="3 -> 6\nx -> hata: ValueError\n10 -> 20\nhata sayısı: 1",
  tests=[
      {"label": "Örnek", "stdin": "3 x 10", "expectedOutput": "3 -> 6\nx -> hata: ValueError\n10 -> 20\nhata sayısı: 1"},
      {"label": "Hatasız", "stdin": "7 -2", "expectedOutput": "7 -> 14\n-2 -> -4\nhata sayısı: 0"},
      {"label": "Hepsi hatalı", "stdin": "a 1.5", "expectedOutput": "a -> hata: ValueError\n1.5 -> hata: ValueError\nhata sayısı: 2"},
  ],
  hints=["futures = [executor.submit(func, item) for item in items] işleri başlatır; with executor: bloğu havuzu kapatır.", "Her future.result() çağrısını try/except Exception içine al; hata adı type(error).__name__ ile alınır."],
  explanation="submit hemen bir Future döndürür; iş hata verirse hata Future'da saklanır ve result() çağrısında yeniden fırlar. Aynı run_all, yerel Python'da ThreadPoolExecutor(max_workers=4) ile çalıştırıldığında işler aynı anda yürür ama sonuç ve hata satırları değişmez.")

q(type="code", topic="parcalama", sectionId="gil-processes", difficulty=2,
  prompt="split(items, parts) fonksiyonunu yaz: listeyi en fazla parts parçaya, parça boyutu yukarı yuvarlanmış len(items) / parts olacak şekilde sırayla böl. Program ilk satırdaki sayıları ikinci satırdaki parça sayısına böler, parça boyutlarını ve her parçanın kareler toplamının genel toplamını yazar.",
  starterCode=r'''
def split(items, parts):
    # parça boyutu: yukarı yuvarlanmış len(items) / parts
    return [items]

def total_squares(part):
    return sum(n * n for n in part)

numbers = [int(part) for part in input().split()]
parts = split(numbers, int(input()))
print("parçalar:", [len(part) for part in parts])
print("toplam:", sum(map(total_squares, parts)))
''',
  answer=r'''
def split(items, parts):
    size = -(-len(items) // parts)
    return [items[i:i + size] for i in range(0, len(items), size)]

def total_squares(part):
    return sum(n * n for n in part)

numbers = [int(part) for part in input().split()]
parts = split(numbers, int(input()))
print("parçalar:", [len(part) for part in parts])
print("toplam:", sum(map(total_squares, parts)))
''',
  exampleInput="1 2 3 4 5 6 7\n3",
  expectedOutput="parçalar: [3, 3, 1]\ntoplam: 140",
  tests=[
      {"label": "Örnek", "stdin": "1 2 3 4 5 6 7\n3", "expectedOutput": "parçalar: [3, 3, 1]\ntoplam: 140"},
      {"label": "Parçadan az öğe", "stdin": "1 2\n4", "expectedOutput": "parçalar: [1, 1]\ntoplam: 5"},
      {"label": "Tam bölünür", "stdin": "5 5 5 5\n2", "expectedOutput": "parçalar: [2, 2]\ntoplam: 100"},
  ],
  hints=["Yukarı yuvarlanmış bölme: size = -(-len(items) // parts) ya da math.ceil(len(items) / parts).", "Dilimler: [items[i:i + size] for i in range(0, len(items), size)]."],
  explanation="Bağımsız parçalar ayrı süreçlerde hesaplanabilir; sonuçlar ana süreçte birleştirilir. Yerelde map yerine ProcessPoolExecutor().map kullanmak sonucu değiştirmez, yalnızca parçaları çekirdeklere dağıtır.")

q(type="code", topic="await-unutma", sectionId="coroutines", difficulty=1,
  prompt="main içinde double coroutine'i await edilmeden çağrılıyor ve listeye coroutine nesneleri giriyor. Düzelt: her sayı için double'ın sonucunu bekleyip listeye ekle ve listeyi yazdır.",
  starterCode=r'''
import asyncio

async def double(n):
    await asyncio.sleep(0.1)
    return n * 2

async def main():
    results = []
    for n in [int(part) for part in input().split()]:
        results.append(double(n))
    print(results)

asyncio.run(main())
''',
  answer=r'''
import asyncio

async def double(n):
    await asyncio.sleep(0.1)
    return n * 2

async def main():
    results = []
    for n in [int(part) for part in input().split()]:
        results.append(await double(n))
    print(results)

asyncio.run(main())
''',
  exampleInput="1 2 3",
  expectedOutput="[2, 4, 6]",
  tests=[
      {"label": "Örnek", "stdin": "1 2 3", "expectedOutput": "[2, 4, 6]"},
      {"label": "Tek sayı", "stdin": "5", "expectedOutput": "[10]"},
      {"label": "Sıfır ve negatif", "stdin": "0 -4", "expectedOutput": "[0, -8]"},
  ],
  hints=["double(n) çağrısı ne döndürür: sayı mı, coroutine mi?", "Sonucu almak için çağrının önüne await yaz."],
  explanation="double(n) yalnızca bir coroutine nesnesi üretir; await double(n) onu çalıştırır ve dönüş değerini verir. await'siz sürüm listeye coroutine nesneleri koyar ve Python 'never awaited' uyarısı verir.")

q(type="code", topic="gather-sure", sectionId="tasks-gather", difficulty=2,
  prompt="İlk satır iş sayısı, sonraki her satır 'ad süre'. Kod işleri art arda await ediyor. Hepsini asyncio.gather ile aynı anda yürüt: sonuçları girdi sırasıyla yazdır ve toplam süreyi loop.time() ile 'toplam: 0.3 sn' biçiminde yaz.",
  starterCode=r'''
import asyncio

async def fetch(name, seconds):
    await asyncio.sleep(seconds)
    return f"{name} tamam"

async def main():
    jobs = []
    for _ in range(int(input())):
        name, seconds = input().split()
        jobs.append((name, float(seconds)))
    loop = asyncio.get_running_loop()
    start = loop.time()
    results = []
    for name, seconds in jobs:          # işleri aynı anda yürüt
        results.append(await fetch(name, seconds))
    print("\n".join(results))
    print(f"toplam: {loop.time() - start:.1f} sn")

asyncio.run(main())
''',
  answer=r'''
import asyncio

async def fetch(name, seconds):
    await asyncio.sleep(seconds)
    return f"{name} tamam"

async def main():
    jobs = []
    for _ in range(int(input())):
        name, seconds = input().split()
        jobs.append((name, float(seconds)))
    loop = asyncio.get_running_loop()
    start = loop.time()
    results = await asyncio.gather(*(fetch(name, seconds) for name, seconds in jobs))
    print("\n".join(results))
    print(f"toplam: {loop.time() - start:.1f} sn")

asyncio.run(main())
''',
  exampleInput="3\na 0.3\nb 0.1\nc 0.2",
  expectedOutput="a tamam\nb tamam\nc tamam\ntoplam: 0.3 sn",
  tests=[
      {"label": "Örnek", "stdin": "3\na 0.3\nb 0.1\nc 0.2", "expectedOutput": "a tamam\nb tamam\nc tamam\ntoplam: 0.3 sn"},
      {"label": "Eşit süreler", "stdin": "2\nx 0.5\ny 0.5", "expectedOutput": "x tamam\ny tamam\ntoplam: 0.5 sn"},
      {"label": "Tek iş", "stdin": "1\nsolo 0.4", "expectedOutput": "solo tamam\ntoplam: 0.4 sn"},
  ],
  hints=["gather'a coroutine'leri yıldızla açarak ver: asyncio.gather(*coroutineler).", "gather sonuçları verilen sırayla döndürür; toplam süre en uzun iş kadar olur."],
  explanation="gather işleri birlikte başlatır; beklemeler örtüştüğü için toplam süre en uzun iş kadardır ve sonuçlar girdi sırasıyla gelir.")

q(type="code", topic="as-completed", sectionId="tasks-gather", difficulty=3,
  prompt="İlk satır iş sayısı, sonraki her satır 'ad süre'. İşleri aynı anda yürüt ve bitiş sırasıyla '1. ad', '2. ad' ... yazdır. asyncio.as_completed kullan; fetch adını döndürüyor.",
  starterCode=r'''
import asyncio

async def fetch(name, seconds):
    await asyncio.sleep(seconds)
    return name

async def main():
    jobs = []
    for _ in range(int(input())):
        name, seconds = input().split()
        jobs.append(fetch(name, float(seconds)))
    # bitiş sırasıyla yazdır
    for number, name in enumerate(await asyncio.gather(*jobs), start=1):
        print(f"{number}. {name}")

asyncio.run(main())
''',
  answer=r'''
import asyncio

async def fetch(name, seconds):
    await asyncio.sleep(seconds)
    return name

async def main():
    jobs = []
    for _ in range(int(input())):
        name, seconds = input().split()
        jobs.append(fetch(name, float(seconds)))
    for number, next_done in enumerate(asyncio.as_completed(jobs), start=1):
        print(f"{number}. {await next_done}")

asyncio.run(main())
''',
  exampleInput="3\nyavaş 0.3\nhızlı 0.1\norta 0.2",
  expectedOutput="1. hızlı\n2. orta\n3. yavaş",
  tests=[
      {"label": "Örnek", "stdin": "3\nyavaş 0.3\nhızlı 0.1\norta 0.2", "expectedOutput": "1. hızlı\n2. orta\n3. yavaş"},
      {"label": "Zaten sıralı", "stdin": "2\na 0.1\nb 0.2", "expectedOutput": "1. a\n2. b"},
      {"label": "Ters sıra", "stdin": "4\nd 0.4\nc 0.3\nb 0.2\na 0.1", "expectedOutput": "1. a\n2. b\n3. c\n4. d"},
  ],
  hints=["gather verilen sırayı korur; bitiş sırası için as_completed gerekir.", "for next_done in asyncio.as_completed(jobs): name = await next_done."],
  explanation="as_completed işleri birlikte başlatır ve her adımda ilk biten işin sonucunu verir; await next_done o sonucu alır. gather ise sonuçları verilen sırayla döndürür.")

q(type="code", topic="bloklama", sectionId="blocking-loop", difficulty=2,
  prompt="İlk satır iş sayısı, sonraki her satır 'ad süre'. İşler gather ile başlatılıyor ama job içindeki time.sleep event loop'u blokluyor ve toplam süre işlerin toplamı kadar çıkıyor. Düzelt: toplam süre en uzun iş kadar olsun.",
  starterCode=r'''
import asyncio
import time

async def job(name, seconds):
    time.sleep(seconds)
    return name

async def main():
    jobs = []
    for _ in range(int(input())):
        name, seconds = input().split()
        jobs.append(job(name, float(seconds)))
    loop = asyncio.get_running_loop()
    start = loop.time()
    print(" ".join(await asyncio.gather(*jobs)))
    print(f"toplam: {loop.time() - start:.1f} sn")

asyncio.run(main())
''',
  answer=r'''
import asyncio

async def job(name, seconds):
    await asyncio.sleep(seconds)
    return name

async def main():
    jobs = []
    for _ in range(int(input())):
        name, seconds = input().split()
        jobs.append(job(name, float(seconds)))
    loop = asyncio.get_running_loop()
    start = loop.time()
    print(" ".join(await asyncio.gather(*jobs)))
    print(f"toplam: {loop.time() - start:.1f} sn")

asyncio.run(main())
''',
  exampleInput="3\na 0.2\nb 0.1\nc 0.2",
  expectedOutput="a b c\ntoplam: 0.2 sn",
  tests=[
      {"label": "Örnek", "stdin": "3\na 0.2\nb 0.1\nc 0.2", "expectedOutput": "a b c\ntoplam: 0.2 sn"},
      {"label": "İki iş", "stdin": "2\nx 0.1\ny 0.3", "expectedOutput": "x y\ntoplam: 0.3 sn"},
      {"label": "Tek iş", "stdin": "1\nz 0.2", "expectedOutput": "z\ntoplam: 0.2 sn"},
  ],
  hints=["job içinde hiç await var mı?", "time.sleep(seconds) yerine await asyncio.sleep(seconds) yaz."],
  explanation="time.sleep bütün iş parçacığını durdurur; görevler birbirini bekler ve süreler toplanır. await asyncio.sleep yalnızca o görevi duraklatır, beklemeler örtüşür ve toplam süre en uzun iş kadar olur.")

q(type="code", topic="wait-for", sectionId="cancellation-timeout", difficulty=2,
  prompt="İlk satır süre sınırı (saniye), ikinci satır iş sayısı, sonraki her satır 'ad süre'. Her indirmeyi sırayla asyncio.wait_for ile süre sınırı koyarak çalıştır: bitenler için 'ad: tamam', sınırı aşanlar için 'ad: zaman aşımı' yaz; sonda 'tamamlanan: 2/3' yaz.",
  starterCode=r'''
import asyncio

async def download(seconds):
    await asyncio.sleep(seconds)

async def main():
    limit = float(input())
    jobs = [input().split() for _ in range(int(input()))]
    done = 0
    for name, seconds in jobs:
        # süre sınırı koy; aşılırsa 'zaman aşımı' yaz
        await download(float(seconds))
        print(f"{name}: tamam")
        done += 1
    print(f"tamamlanan: {done}/{len(jobs)}")

asyncio.run(main())
''',
  answer=r'''
import asyncio

async def download(seconds):
    await asyncio.sleep(seconds)

async def main():
    limit = float(input())
    jobs = [input().split() for _ in range(int(input()))]
    done = 0
    for name, seconds in jobs:
        try:
            await asyncio.wait_for(download(float(seconds)), timeout=limit)
        except TimeoutError:
            print(f"{name}: zaman aşımı")
        else:
            print(f"{name}: tamam")
            done += 1
    print(f"tamamlanan: {done}/{len(jobs)}")

asyncio.run(main())
''',
  exampleInput="0.5\n3\na 0.2\nb 0.9\nc 0.4",
  expectedOutput="a: tamam\nb: zaman aşımı\nc: tamam\ntamamlanan: 2/3",
  tests=[
      {"label": "Örnek", "stdin": "0.5\n3\na 0.2\nb 0.9\nc 0.4", "expectedOutput": "a: tamam\nb: zaman aşımı\nc: tamam\ntamamlanan: 2/3"},
      {"label": "Hepsi yetişir", "stdin": "1\n2\nx 0.1\ny 0.3", "expectedOutput": "x: tamam\ny: tamam\ntamamlanan: 2/2"},
      {"label": "Hiçbiri yetişmez", "stdin": "0.1\n2\np 2\nq 5", "expectedOutput": "p: zaman aşımı\nq: zaman aşımı\ntamamlanan: 0/2"},
  ],
  hints=["await asyncio.wait_for(download(...), timeout=limit) süre sınırı koyar.", "try/except TimeoutError/else: başarı satırı ve sayaç else bloğuna gider."],
  explanation="wait_for süre dolunca işi iptal eder ve TimeoutError fırlatır; else bloğu yalnızca iş zamanında bittiğinde çalışır.")

q(type="code", topic="kilit", sectionId="shared-state", difficulty=2,
  prompt="İlk satır başlangıç bakiyesi, ikinci satır çekilecek tutarlar. Bütün çekişler gather ile aynı anda başlatılıyor; withdraw bakiyeyi denetleyip bir süre bekledikten sonra düşüyor ve bakiye eksiye inebiliyor. asyncio.Lock ile düzelt: her çekiş 'çekildi X' ya da 'yetersiz X' yazsın, sonda 'bakiye: B'.",
  starterCode=r'''
import asyncio

class Account:
    def __init__(self, balance):
        self.balance = balance

    async def withdraw(self, amount):
        if self.balance >= amount:
            await asyncio.sleep(0.1)     # banka onayı bekleniyor
            self.balance -= amount
            print("çekildi", amount)
        else:
            print("yetersiz", amount)

async def main():
    account = Account(int(input()))
    amounts = [int(part) for part in input().split()]
    await asyncio.gather(*(account.withdraw(amount) for amount in amounts))
    print("bakiye:", account.balance)

asyncio.run(main())
''',
  answer=r'''
import asyncio

class Account:
    def __init__(self, balance):
        self.balance = balance
        self.lock = asyncio.Lock()

    async def withdraw(self, amount):
        async with self.lock:
            if self.balance >= amount:
                await asyncio.sleep(0.1)     # banka onayı bekleniyor
                self.balance -= amount
                print("çekildi", amount)
            else:
                print("yetersiz", amount)

async def main():
    account = Account(int(input()))
    amounts = [int(part) for part in input().split()]
    await asyncio.gather(*(account.withdraw(amount) for amount in amounts))
    print("bakiye:", account.balance)

asyncio.run(main())
''',
  exampleInput="100\n80 70",
  expectedOutput="çekildi 80\nyetersiz 70\nbakiye: 20",
  tests=[
      {"label": "Örnek", "stdin": "100\n80 70", "expectedOutput": "çekildi 80\nyetersiz 70\nbakiye: 20"},
      {"label": "Üçüncüsü yetmez", "stdin": "50\n20 20 20", "expectedOutput": "çekildi 20\nçekildi 20\nyetersiz 20\nbakiye: 10"},
      {"label": "Hepsi yeter", "stdin": "100\n30 30 30", "expectedOutput": "çekildi 30\nçekildi 30\nçekildi 30\nbakiye: 10"},
  ],
  hints=["Kilidi __init__ içinde self.lock = asyncio.Lock() ile oluştur.", "Denetim, bekleme ve düşme async with self.lock: bloğunun içinde olmalı."],
  explanation="Kilit olmadan bütün görevler denetimi aynı eski bakiyeyle yapar. async with self.lock denetle-bekle-düş adımlarını tek parça yapar; asyncio.Lock bekleyenleri geliş sırasıyla aldığı için çekişler girdi sırasıyla işlenir.")

q(type="code", topic="kuyruk", sectionId="shared-state", difficulty=3,
  prompt="İlk satır çalışan sayısı, ikinci satır 'ad:süre' biçiminde işler. worker hazır. main'i tamamla: işleri kuyruğa koy, çalışan sayısı kadar worker görevi başlat (kimlikleri 1'den), queue.join() ile bütün işlerin bitmesini bekle, sonra worker'ları iptal et ve tamamlananları 'ad@kimlik' biçiminde, bitiş sırasıyla, virgülle ayırarak yaz.",
  starterCode=r'''
import asyncio

async def worker(wid, queue, done):
    while True:
        name, seconds = await queue.get()
        await asyncio.sleep(seconds)
        done.append(f"{name}@{wid}")
        queue.task_done()

async def main():
    count = int(input())
    queue = asyncio.Queue()
    for token in input().split():
        name, seconds = token.split(":")
        queue.put_nowait((name, float(seconds)))
    done = []
    # worker görevlerini başlat, kuyruğun boşalmasını bekle, worker'ları iptal et
    print(", ".join(done))

asyncio.run(main())
''',
  answer=r'''
import asyncio

async def worker(wid, queue, done):
    while True:
        name, seconds = await queue.get()
        await asyncio.sleep(seconds)
        done.append(f"{name}@{wid}")
        queue.task_done()

async def main():
    count = int(input())
    queue = asyncio.Queue()
    for token in input().split():
        name, seconds = token.split(":")
        queue.put_nowait((name, float(seconds)))
    done = []
    workers = [asyncio.create_task(worker(wid, queue, done)) for wid in range(1, count + 1)]
    await queue.join()
    for task in workers:
        task.cancel()
    print(", ".join(done))

asyncio.run(main())
''',
  exampleInput="2\nab:0.2 c:0.1 def:0.3 g:0.1",
  expectedOutput="c@2, ab@1, g@1, def@2",
  tests=[
      {"label": "Örnek", "stdin": "2\nab:0.2 c:0.1 def:0.3 g:0.1", "expectedOutput": "c@2, ab@1, g@1, def@2"},
      {"label": "Tek çalışan", "stdin": "1\na:0.1 b:0.1", "expectedOutput": "a@1, b@1"},
      {"label": "Üç çalışan", "stdin": "3\nx:0.3 y:0.1 z:0.2", "expectedOutput": "y@2, z@3, x@1"},
  ],
  hints=["workers = [asyncio.create_task(worker(wid, queue, done)) for wid in range(1, count + 1)].", "await queue.join() her iş için task_done çağrılana kadar bekler; sonra her görevde task.cancel()."],
  explanation="Kuyruk, işleri çalışanlar arasında kilitsiz ve sırayla paylaştırır: boşta kalan çalışan sıradaki işi alır. queue.join() bütün işler bitene kadar bekler; sonsuz döngüdeki çalışanlar ardından iptal edilerek kapatılır.")

# ------------------------------------------------------------------ traceback (4)
q(type="traceback", topic="await-disarida", sectionId="coroutines", difficulty=1,
  prompt="await sıradan bir fonksiyonun içinde kullanılıyor. Hangi hata oluşur?",
  code=r'''
import asyncio

def main():
    await asyncio.sleep(0.1)
    print("bitti")

main()
''',
  expectedError="SyntaxError",
  options=["SyntaxError", "RuntimeError", "TypeError", "NameError"],
  optionFeedback={
      "RuntimeError": "Kod hiç çalışmaz; hata, dosya derlenirken bulunur.",
      "TypeError": "Bir değerin türü değil, await'in yazıldığı yer yanlış.",
      "NameError": "asyncio içe aktarıldı ve tanımlı.",
  },
  hints=["await nerede yazılabilir?", "Hata program çalışmadan mı bulunuyor?"],
  explanation="await yalnızca async def içinde yazılabilir; Python dosyayı derlerken SyntaxError: 'await' outside async function verir. main async def ile tanımlanıp asyncio.run(main()) ile çalıştırılmalıdır.")

q(type="traceback", topic="await-unutma", sectionId="coroutines", difficulty=2,
  prompt="Coroutine await edilmeden sonucu kullanılıyor. Hangi hata oluşur?",
  code=r'''
import asyncio

async def fetch_name():
    await asyncio.sleep(0.1)
    return "ada"

async def main():
    name = fetch_name()
    print(name.upper())

asyncio.run(main())
''',
  expectedError="AttributeError",
  options=["AttributeError", "TypeError", "RuntimeError", "NameError"],
  optionFeedback={
      "TypeError": "Bir işlem değil, coroutine nesnesinde olmayan bir metot aranıyor.",
      "RuntimeError": "Event loop doğru çalışıyor; sorun name'in bir metin olmaması.",
      "NameError": "fetch_name ve name tanımlı adlardır.",
  },
  hints=["fetch_name() await'siz ne döndürür?", "Bir coroutine nesnesinin upper metodu var mı?"],
  explanation="fetch_name() await edilmeden çağrıldığı için name bir coroutine nesnesidir, metin değil: AttributeError: 'coroutine' object has no attribute 'upper'. Doğrusu name = await fetch_name().")

q(type="traceback", topic="yakalanmayan-timeout", sectionId="cancellation-timeout", difficulty=2,
  prompt="Süre sınırı aşılıyor ve hata yakalanmıyor. Hangi hata oluşur?",
  code=r'''
import asyncio

async def main():
    await asyncio.wait_for(asyncio.sleep(3), timeout=0.2)
    print("bitti")

asyncio.run(main())
''',
  expectedError="TimeoutError",
  options=["TimeoutError", "CancelledError", "RuntimeError", "ValueError"],
  optionFeedback={
      "CancelledError": "CancelledError iptal edilen iç işte oluşur; wait_for onu dışarıya TimeoutError olarak iletir.",
      "RuntimeError": "Event loop doğru çalışıyor; süre sınırı aşıldı.",
      "ValueError": "timeout geçerli bir sayı.",
  },
  hints=["sleep(3) 0,2 saniyede biter mi?", "wait_for süre dolunca hangi hatayı fırlatır?"],
  explanation="İş 0,2 saniyede bitmez; wait_for onu iptal eder ve TimeoutError fırlatır. Yakalanmadığı için program durur ve 'bitti' yazılmaz.")

q(type="traceback", topic="bos-kuyruk", sectionId="shared-state", difficulty=2,
  prompt="Boş bir asyncio kuyruğundan beklemeden öğe alınıyor. Hangi hata oluşur?",
  code=r'''
import asyncio

async def main():
    queue = asyncio.Queue()
    queue.put_nowait("ilk")
    print(queue.get_nowait())
    print(queue.get_nowait())

asyncio.run(main())
''',
  expectedError="QueueEmpty",
  options=["QueueEmpty", "IndexError", "KeyError", "TimeoutError"],
  optionFeedback={
      "IndexError": "Kuyruk bir liste değil; asyncio kendi hatasını fırlatır.",
      "KeyError": "Anahtar aranmıyor; kuyruk boş.",
      "TimeoutError": "get_nowait hiç beklemez, süre sınırı da yoktur.",
  },
  hints=["Kuyrukta kaç öğe var?", "_nowait sürümleri boş kuyrukta bekler mi?"],
  explanation="İlk get_nowait 'ilk'i alır; ikinci çağrıda kuyruk boştur ve beklemeyen sürüm asyncio.QueueEmpty fırlatır. Öğe gelene kadar beklemek için await queue.get() kullanılır.")
