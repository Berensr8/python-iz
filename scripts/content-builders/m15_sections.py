"""M15 (Eşzamanlılık) lesson sections. Imported by build_m15.py.

Threads and processes cannot start in the browser (Pyodide), so those sections are "mixed": the editor
example runs in the browser and `localExample` holds the real thread/process code, verified with
CPython by `npm run verify:local`. asyncio runs in the browser through the site's own loop
(public/python-runtime.js), which skips idle waits but keeps loop.time() as in real Python.
"""

DOCS = "https://docs.python.org/3.12/library/"


def c(text):
    return text.strip("\n")


sections = []

ASYNC_NOTE = "Tarayıcıda çalışır · Python 3.12. Site boşta beklemeyi atlar: asyncio.sleep hemen biter ama loop.time() gerçek Python'daki gibi ilerler, çıktı yerel Python'la aynıdır."


def section(**fields):
    for key in ("code", "expectedOutput", "realCode", "realOutput"):
        fields[key] = c(fields[key])
    if "localExample" in fields:
        example = fields["localExample"]
        example["code"] = c(example["code"])
        example["output"] = c(example["output"])
    fields.setdefault("runtime", "browser")
    sections.append(fields)


section(
    id="io-cpu",
    title="Bekleyen iş, hesaplayan iş",
    eyebrow="Eşzamanlılık neden gerekir?",
    objectives=[
        "Bir işin I/O bağımlı (ağ, disk, kullanıcı beklemek) mı yoksa CPU bağımlı (hesaplama) mı olduğunu ayırt eder.",
        "Eşzamanlılık (concurrency) ile paralelliği (parallelism) ayırır ve sırayla, örtüşerek ve paralel çalışmanın toplam süresini kabaca tahmin eder.",
    ],
    prerequisites=["m10:datetime", "m6:def-return"],
    summary="Programlar zamanlarının çoğunu ya bir şey beklerken (ağ yanıtı, disk, veritabanı) ya da hesaplarken geçirir. Bekleyen işleri örtüştürmek (eşzamanlılık) toplam süreyi en uzun beklemeye indirir; hesaplamayı hızlandırmak ise birden çok çekirdekte gerçekten aynı anda çalışmayı (paralellik) gerektirir.",
    explanation=(
        "Bir program iki tür işte zaman harcar. I/O bağımlı işte (input/output) işlemci çoğunlukla boştadır: bir web sayfasının yanıtını, diskten okunan dosyayı ya da veritabanı sorgusunu bekler. CPU bağımlı işte ise işlemci sürekli çalışır: büyük bir listeyi sıralamak, görüntü küçültmek, asal sayı aramak gibi. Hangisiyle uğraştığını bilmeden doğru aracı seçemezsin; emin değilsen önce ölç (time.perf_counter, M10). "
        "Eşzamanlılık (concurrency), birden çok işin aynı zaman aralığında ilerlemesidir; işler sırayla ama iç içe ilerleyebilir. Bir aşçı makarna suyu kaynarken salata doğrar: tek kişi, ama beklemeyi boşa harcamaz. Paralellik (parallelism) ise işlerin gerçekten aynı anda, farklı çekirdeklerde çalışmasıdır: iki aşçı. "
        "Üç dosyayı sırayla indirmek 0,8 + 0,3 + 0,6 = 1,7 saniye sürer; beklemeler örtüşürse toplam süre en uzun beklemeye, 0,8 saniyeye iner. Bunun için tek çekirdek yeter, çünkü beklerken hesaplanacak bir şey yoktur. Hesaplama işlerinde ise örtüştürmek işe yaramaz: tek çekirdekte üç adet 0,5 saniyelik hesap yine 1,5 saniye sürer. Hızlanma için ikinci, üçüncü çekirdeğin de çalışması gerekir. "
        "Python'da üç araç var: threading (iş parçacıkları; I/O için), multiprocessing (ayrı süreçler; CPU için) ve asyncio (tek iş parçacığında, await noktalarında sırayı değiştiren görevler; çok sayıda I/O için). Bu modül hepsini okuyup ne zaman hangisinin seçildiğini anlayacak kadar tanıtır. Eşzamanlılık karmaşıklık da getirir: hatalar zamanlamaya bağlı olur ve her çalıştırmada görünmeyebilir. İş zaten hızlıysa sıralı kod en iyi seçimdir."
    ),
    code=r'''
downloads = [0.8, 0.3, 0.6]   # saniye: çoğunlukla ağdan yanıt bekleniyor (I/O)
hashes = [0.5, 0.5, 0.5]      # saniye: işlemci sürekli hesaplıyor (CPU)

print("I/O sırayla:", round(sum(downloads), 1))
print("I/O örtüşerek:", max(downloads))
print("CPU tek çekirdek:", round(sum(hashes), 1))
print("CPU üç çekirdek:", max(hashes))
''',
    expectedOutput=r'''
I/O sırayla: 1.7
I/O örtüşerek: 0.8
CPU tek çekirdek: 1.5
CPU üç çekirdek: 0.5
''',
    why="Beklemeler örtüşebildiği için I/O işlerinde toplam süre en uzun beklemeye iner ve bunun için tek çekirdek yeter. Hesaplama işleri tek çekirdekte örtüştürülse de toplam yine aynı kalır; süre ancak işler farklı çekirdeklere dağıtılınca düşer.",
    alternatives=[
        "Gerçek süreyi tahmin etmek yerine ölç: start = time.perf_counter() ... print(time.perf_counter() - start).",
        "İş zaten kısa sürüyorsa eşzamanlılık ekleme; sıralı kod daha kolay okunur ve test edilir.",
    ],
    traps=[
        "Eşzamanlılığın her işi hızlandırdığını sanmak; hesaplama işinde tek çekirdekte kazanç yoktur.",
        "Eşzamanlılık ile paralelliği aynı şey sanmak: biri işlerin iç içe ilerlemesi, diğeri gerçekten aynı anda çalışmasıdır.",
        "Ölçmeden 'yavaş olan ağ' ya da 'yavaş olan hesap' diye tahmin edip yanlış aracı seçmek.",
    ],
    realCode=r'''
def choose_tool(kind: str, count: int) -> str:
    if count == 1:
        return "sırayla çalıştır"
    if kind == "io":
        return "asyncio ya da thread havuzu"
    if kind == "cpu":
        return "süreç havuzu (multiprocessing)"
    return "önce ölç (time.perf_counter)"

jobs = [("100 sayfa indir", "io", 100), ("tek dosya oku", "io", 1), ("40 görüntü küçült", "cpu", 40), ("rapor üret", "?", 5)]
for name, kind, count in jobs:
    print(f"{name}: {choose_tool(kind, count)}")
''',
    realOutput=r'''
100 sayfa indir: asyncio ya da thread havuzu
tek dosya oku: sırayla çalıştır
40 görüntü küçült: süreç havuzu (multiprocessing)
rapor üret: önce ölç (time.perf_counter)
''',
    lineByLine=[
        "Tek bir iş için eşzamanlılık bir şey kazandırmaz; sıralı kod yeterlidir.",
        "Çok sayıda bekleme (ağ, disk) varsa beklemeleri örtüştüren asyncio ya da thread havuzu seçilir.",
        "Çok sayıda hesaplama varsa işler ayrı süreçlere, yani ayrı çekirdeklere dağıtılır.",
        "İşin türü bilinmiyorsa karar vermeden önce süre ölçülür.",
    ],
    sources=[
        {"title": "Python 3.12 · Eşzamanlı çalıştırma", "url": DOCS + "concurrency.html"},
        {"title": "Python 3.12 · time.perf_counter", "url": DOCS + "time.html#time.perf_counter"},
    ],
)

section(
    id="threads",
    title="threading ve thread havuzu",
    eyebrow="Beklemeleri iş parçacıklarıyla örtüştür",
    depth="okuma",
    objectives=[
        "threading.Thread(target=..., args=...), start() ve join() ile çalışan kodu okur; join'in neden gerektiğini açıklar.",
        "concurrent.futures.ThreadPoolExecutor ile submit, map ve Future.result() kullanımını okur; bir thread'deki hatanın result() çağrısında yeniden fırlatıldığını bilir.",
    ],
    prerequisites=["io-cpu", "m6:parameters", "m7:try-except"],
    summary="Thread (iş parçacığı), aynı program içinde aynı belleği paylaşarak çalışan ayrı bir yürütme yoludur. Bir thread ağ yanıtı beklerken diğerleri çalışır; bu yüzden thread'ler I/O işlerini hızlandırır. Gündelik kodda thread'leri elle yönetmek yerine ThreadPoolExecutor kullanılır.",
    explanation=(
        "threading.Thread(target=fetch, args=(3,)) bir iş parçacığı nesnesi oluşturur ama çalıştırmaz. start() onu başlatır ve hemen döner; ana program kendi işine devam eder. join() ise o thread bitene kadar bekler. join çağrılmazsa program, sonuçlar daha hazır değilken onları okumaya çalışabilir. args bir demettir: tek argümanda bile virgül gerekir, (3,). "
        "Thread'ler aynı süreçte çalıştığı için aynı değişkenleri, listeleri ve nesneleri görür. Bu kolaylıktır ama tehlikelidir: iki thread aynı veriyi aynı anda değiştirirse sonuç bozulabilir (bu modülün son bölümü). Sonuçları ortak bir listeye yazmak yerine her işin bir değer döndürmesi daha güvenlidir. "
        "concurrent.futures.ThreadPoolExecutor bir thread havuzu kurar ve işleri ona dağıtır. executor.submit(fetch, 3) hemen bir Future (ileride hazır olacak sonuç) döndürür; future.result() sonuç hazır olana kadar bekler ve iş hata verdiyse aynı hatayı orada yeniden fırlatır. executor.map(fetch, pages) her öğe için işi başlatır ve sonuçları girdi sırasıyla verir. with bloğu sonunda havuz bütün işlerin bitmesini bekler. as_completed(futures) ise işleri bitme sırasıyla dolaşır. "
        "Bu sitede kod tarayıcıda çalışır ve tarayıcıdaki Python thread başlatamaz (RuntimeError: can't start new thread). Bu yüzden editördeki örnek thread nesnelerini kurar ama işi sırayla yapar; gerçek thread'li sürüm aşağıda yerel Python içindir. Gerçek kodda ise aynı Executor arayüzünü sırayla çalıştıran küçük bir sınıfla değiştirmek, thread kullanan kodu test etmenin yaygın bir yoludur."
    ),
    code=r'''
import threading

results = {}

def fetch(page: int) -> None:
    # gerçekte burada ağ yanıtı beklenir
    results[page] = f"sayfa-{page}"

workers = [threading.Thread(target=fetch, args=(n,), name=f"indirici-{n}") for n in range(1, 4)]
print([worker.name for worker in workers])
print(threading.current_thread().name, workers[0].is_alive())
for n in range(1, 4):   # tarayıcıda thread başlatılamaz; aynı işi sırayla yapıyoruz
    fetch(n)
print(results)
''',
    expectedOutput=r'''
['indirici-1', 'indirici-2', 'indirici-3']
MainThread False
{1: 'sayfa-1', 2: 'sayfa-2', 3: 'sayfa-3'}
''',
    why="Thread nesneleri kuruldu ama start() çağrılmadığı için hiçbiri çalışmıyor (is_alive False); kod ana iş parçacığında (MainThread) yürüyor. Yerel örnekte aynı fetch dört thread'de çalışınca her biri 0,5 saniye beklediği hâlde toplam süre 2 değil 0,5 saniye olur, çünkü beklemeler örtüşür.",
    alternatives=[
        "Thread'leri elle başlatıp join etmek yerine ThreadPoolExecutor kullan; sonuçları ve hataları Future'lar taşır.",
        "Çok sayıda ağ isteğinde asyncio daha az kaynakla daha çok bağlantıyı yönetir (sonraki bölümler).",
    ],
    traps=[
        "start() yerine run() çağırmak: run işi yeni thread'de değil, çağıran thread'de sırayla çalıştırır.",
        "join() etmeden sonuçları okumak; işler henüz bitmemiş olabilir.",
        "args=(3) yazmak: bu bir demet değil, 3 sayısıdır; doğrusu args=(3,).",
        "Thread'de oluşan hatanın kaybolduğunu sanmak: havuzda hata Future'da saklanır ve result() çağrılınca fırlar.",
    ],
    localExample={
        "note": "Tarayıcıdaki Python thread başlatamaz. Bu kodu kendi bilgisayarında python yerel.py ile çalıştır; süreler küçük farklarla değişebilir.",
        "code": r'''
import threading
import time
from concurrent.futures import ThreadPoolExecutor

def fetch(page: int) -> str:
    time.sleep(0.5)          # ağ yanıtını bekliyormuş gibi
    return f"sayfa-{page}"

start = time.perf_counter()
workers = [threading.Thread(target=fetch, args=(n,)) for n in range(1, 5)]
for worker in workers:
    worker.start()
for worker in workers:
    worker.join()
print(f"4 thread: {time.perf_counter() - start:.1f} sn")

start = time.perf_counter()
with ThreadPoolExecutor(max_workers=4) as pool:
    pages = list(pool.map(fetch, range(1, 5)))
print(pages, f"{time.perf_counter() - start:.1f} sn")

start = time.perf_counter()
pages = [fetch(n) for n in range(1, 5)]
print(f"sırayla: {time.perf_counter() - start:.1f} sn")
''',
        "output": r'''
4 thread: 0.5 sn
['sayfa-1', 'sayfa-2', 'sayfa-3', 'sayfa-4'] 0.5 sn
sırayla: 2.0 sn
''',
    },
    realCode=r'''
from concurrent.futures import Executor, Future

class InlineExecutor(Executor):
    """ThreadPoolExecutor ile aynı arayüz; işleri sırayla yapar (testler ve tarayıcı için)."""
    def submit(self, fn, /, *args, **kwargs):
        future = Future()
        try:
            future.set_result(fn(*args, **kwargs))
        except Exception as error:
            future.set_exception(error)
        return future

def fetch(page: int) -> str:
    if page < 1:
        raise ValueError(f"geçersiz sayfa: {page}")
    return f"sayfa-{page}"

def download(executor: Executor, pages: list[int]) -> None:
    with executor:
        futures = {page: executor.submit(fetch, page) for page in pages}
    for page, future in futures.items():
        try:
            print(page, future.result())
        except ValueError as error:
            print(page, "hata:", error)

download(InlineExecutor(), [2, 0, 5])
''',
    realOutput=r'''
2 sayfa-2
0 hata: geçersiz sayfa: 0
5 sayfa-5
''',
    lineByLine=[
        "download hangi executor'la çalışacağını bilmez; yalnızca submit ve with arayüzünü kullanır.",
        "Yerel Python'da download(ThreadPoolExecutor(max_workers=4), [2, 0, 5]) aynı çıktıyı verir ama işler aynı anda yürür.",
        "Her submit bir Future döndürür; işte oluşan ValueError Future'da saklanır.",
        "future.result() sonucu verir ya da saklanan hatayı burada yeniden fırlatır; hata bu yüzden ana kodda yakalanabilir.",
    ],
    sources=[
        {"title": "Python 3.12 · threading", "url": DOCS + "threading.html"},
        {"title": "Python 3.12 · concurrent.futures", "url": DOCS + "concurrent.futures.html"},
    ],
    runtime="mixed",
    runtimeNote="Editör örneği tarayıcıda çalışır ama thread başlatmaz; tarayıcıdaki Python'da thread yoktur. Gerçek thread'li sürüm 'Yerel Python'da çalıştır' bölümünde, yerel Python içindir.",
)

section(
    id="gil-processes",
    title="GIL ve multiprocessing",
    eyebrow="Hesaplamayı çekirdeklere dağıt",
    depth="okuma",
    objectives=[
        "GIL'in (Global Interpreter Lock) ne olduğunu, thread'lerin neden I/O'yu hızlandırıp saf Python hesaplamasını hızlandırmadığını ve bunun sürüme/derlemeye bağlı olduğunu açıklar.",
        "ProcessPoolExecutor ile işi süreçlere dağıtan kodu okur; if __name__ == '__main__' korumasını, modül düzeyinde fonksiyon ve pickle gerekliliğini tanır.",
    ],
    prerequisites=["threads", "m9:main-guard", "m10:collections"],
    summary="Standart CPython'da GIL, aynı anda yalnızca bir thread'in Python kodu çalıştırmasına izin verir; bekleyen thread kilidi bırakır. Bu yüzden hesaplama işini hızlandırmak için ayrı süreçler kullanılır: her sürecin kendi yorumlayıcısı ve kendi GIL'i vardır, işler gerçekten farklı çekirdeklerde çalışır.",
    explanation=(
        "GIL (Global Interpreter Lock), CPython yorumlayıcısının iç verisini korumak için kullandığı tek bir kilittir: bir süreçte aynı anda yalnızca bir thread Python bayt kodu çalıştırabilir. Bir thread ağdan yanıt, diskten veri ya da time.sleep beklerken GIL'i bırakır ve diğerleri çalışır; bu yüzden thread'ler I/O işinde gerçekten kazandırır. Saf Python hesaplamasında ise dört thread, işi sırayla yapmaktan hızlı değildir ve geçişlerin yüzünden biraz daha yavaş bile olabilir. NumPy gibi C ile yazılmış kütüphaneler hesap sırasında GIL'i bırakabildiği için onlarda durum farklıdır. "
        "GIL bir dil kuralı değil, bir uygulama ayrıntısıdır ve değişmektedir. Python 3.13 ile GIL'siz, ayrı bir 'free-threaded' derleme (python3.13t) deneysel olarak geldi (PEP 703); 3.14'te bu derleme resmî olarak destekleniyor ama isteğe bağlı. python.org'dan indirilen varsayılan yorumlayıcı hâlâ GIL'lidir. 3.13 ve sonrasında sys._is_gil_enabled() hangisinde çalıştığını söyler. Bu sitedeki Python 3.12'dir ve tek iş parçacığıyla çalışır. "
        "Hesaplamayı hızlandırmanın standart yolu süreçlerdir. concurrent.futures.ProcessPoolExecutor, multiprocessing modülünün üstünde thread havuzuyla aynı arayüzü sunar: pool.map(count_primes, chunks) parçaları ayrı süreçlerde hesaplar. Her sürecin kendi belleği olduğundan argümanlar ve sonuçlar pickle ile kopyalanarak taşınır: fonksiyon modül düzeyinde tanımlanmalıdır (lambda ya da iç fonksiyon olmaz), veriler küçük tutulmalıdır ve bir süreçte bir listeyi değiştirmek diğerlerini etkilemez. "
        "Windows ve macOS'ta (Python 3.14'ten beri Linux'ta da varsayılan olarak) yeni süreç programı baştan içe aktarır. Süreç başlatan kod if __name__ == '__main__': altında değilse her alt süreç yeniden süreç başlatmaya çalışır ve program hata verir (M9); korumayı her zaman yaz. Süreç başlatmak thread'den pahalıdır; işi birkaç büyük parçaya bölmek, binlerce küçük iş göndermekten iyidir. Bu sitedeki tarayıcı Python'u süreç de başlatamaz; gerçek örnek yerel Python içindir."
    ),
    code=r'''
def count_primes(bounds: tuple[int, int]) -> int:
    low, high = bounds
    return sum(1 for n in range(max(low, 2), high)
               if all(n % d for d in range(2, int(n ** 0.5) + 1)))

chunks = [(0, 2500), (2500, 5000), (5000, 7500), (7500, 10000)]
counts = list(map(count_primes, chunks))   # yerelde: pool.map(count_primes, chunks)
print(counts)
print("toplam:", sum(counts))
''',
    expectedOutput=r'''
[367, 302, 281, 279]
toplam: 1229
''',
    why="İş, birbirinden bağımsız dört parçaya bölündü; her parça yalnızca kendi aralığını hesaplıyor ve ortak bir değişkene dokunmuyor. Bu yüzden map'i ProcessPoolExecutor'ın map'iyle değiştirmek sonucu değiştirmez, yalnızca parçaları farklı çekirdeklere dağıtır.",
    alternatives=[
        "Sayısal hesaplamada önce NumPy gibi vektörleştirilmiş kütüphanelere bak; çoğu zaman süreç havuzundan daha basit ve hızlıdır.",
        "I/O işlerinde süreç değil thread ya da asyncio kullan; süreç başlatmanın bedeli kazancı yer.",
    ],
    traps=[
        "CPU bağımlı saf Python işini thread'lerle hızlandırmaya çalışmak; standart CPython'da GIL buna izin vermez.",
        "Süreç başlatan kodu if __name__ == '__main__': koruması olmadan yazmak (Windows ve macOS'ta hata).",
        "pool.map'e lambda ya da iç fonksiyon vermek; pickle edilemedikleri için süreçlere gönderilemezler.",
        "Alt süreçte değiştirilen bir global listenin ana süreçte de değiştiğini sanmak; her sürecin belleği ayrıdır.",
    ],
    localExample={
        "note": "Tarayıcıdaki Python süreç başlatamaz. Kendi bilgisayarında python yerel.py ile çalıştır; dosya olarak çalıştırmak gerekir, çünkü alt süreçler bu dosyayı yeniden içe aktarır.",
        "code": r'''
from concurrent.futures import ProcessPoolExecutor

def count_primes(bounds: tuple[int, int]) -> int:
    low, high = bounds
    return sum(1 for n in range(max(low, 2), high)
               if all(n % d for d in range(2, int(n ** 0.5) + 1)))

if __name__ == "__main__":
    chunks = [(0, 2500), (2500, 5000), (5000, 7500), (7500, 10000)]
    with ProcessPoolExecutor(max_workers=4) as pool:
        counts = list(pool.map(count_primes, chunks))
    print(counts)
    print("toplam:", sum(counts))
''',
        "output": r'''
[367, 302, 281, 279]
toplam: 1229
''',
    },
    realCode=r'''
from collections import Counter

def count_words(lines: list[str]) -> Counter[str]:
    return Counter(word for line in lines for word in line.lower().split())

def split(items: list[str], parts: int) -> list[list[str]]:
    size = -(-len(items) // parts)   # yukarı yuvarlanmış bölme
    return [items[i:i + size] for i in range(0, len(items), size)]

lines = ["Ada kod yazar", "Can kod okur", "Ada test yazar", "Eda kod"]
parts = split(lines, 2)
partials = list(map(count_words, parts))   # yerelde: pool.map(count_words, parts)
total = sum(partials, Counter())
print(len(parts), total.most_common(2))
''',
    realOutput=r'''
2 [('kod', 3), ('ada', 2)]
''',
    lineByLine=[
        "count_words yalnızca kendisine verilen satırlara bakar; paylaşılan bir duruma dokunmadığı için ayrı süreçte güvenle çalışır.",
        "split işi çekirdek sayısı kadar büyük parçaya böler; çok sayıda küçük iş göndermek, kopyalama bedeli yüzünden yavaştır.",
        "map yerine ProcessPoolExecutor().map kullanıldığında her parça ayrı süreçte sayılır ve Counter sonuçları pickle ile geri döner.",
        "Ara sonuçlar ana süreçte birleştirilir: Counter'lar toplanabilir, sum'a başlangıç olarak boş bir Counter verilir.",
    ],
    sources=[
        {"title": "Python 3.12 · multiprocessing", "url": DOCS + "multiprocessing.html"},
        {"title": "Python · Free-threaded CPython", "url": "https://docs.python.org/3/howto/free-threading-python.html"},
        {"title": "PEP 703 · GIL'i isteğe bağlı yapmak", "url": "https://peps.python.org/pep-0703/"},
    ],
    runtime="mixed",
    runtimeNote="Editör örneği tarayıcıda çalışır ama süreç başlatmaz; tarayıcıdaki Python'da süreç yoktur. ProcessPoolExecutor'lı sürüm 'Yerel Python'da çalıştır' bölümünde, yerel Python içindir.",
)

section(
    id="coroutines",
    title="async def, await ve asyncio.run",
    eyebrow="Duraklayıp devam eden fonksiyonlar",
    depth="okuma",
    objectives=[
        "async def ile tanımlanan fonksiyonun çağrılınca çalışmadığını, bir coroutine nesnesi döndürdüğünü ve await ya da asyncio.run ile çalıştırıldığını açıklar.",
        "Event loop'un tek iş parçacığında görevleri await noktalarında değiştirdiğini ve art arda await'lerin süreleri topladığını okur.",
    ],
    prerequisites=["io-cpu", "m13:generators", "m14:annotations-basics"],
    summary="async def bir coroutine fonksiyonu tanımlar; çağırmak yalnızca bir coroutine nesnesi üretir. asyncio.run(main()) bir event loop başlatır ve coroutine'i çalıştırır. await, beklenen iş bitene kadar bu coroutine'i duraklatır ve o sırada event loop başka işleri sürdürebilir.",
    explanation=(
        "async def ile tanımlanan bir fonksiyon (coroutine fonksiyonu) çağrıldığında gövdesi çalışmaz; M13'teki generator'lar gibi duraklatılabilen bir nesne, coroutine döner. Onu çalıştırmanın iki yolu vardır: başka bir coroutine içinden await ile ya da programın en üstünde asyncio.run(main()) ile. asyncio.run bir event loop (olay döngüsü) kurar, verilen coroutine'i bitene kadar çalıştırır, dönüş değerini verir ve döngüyü kapatır. Bir programda genellikle tek bir asyncio.run çağrısı olur. "
        "await yalnızca async def içinde yazılabilir ve 'beklenebilir' (awaitable) bir nesne bekler: coroutine, Task ya da Future. await asyncio.sleep(0.1), bu coroutine'i 0,1 saniye duraklatır ve kontrolü event loop'a geri verir. Event loop tek bir iş parçacığında çalışır; her an yalnızca bir coroutine yürür, ama biri beklerken loop hazır olan başka birine geçer. Geçiş yalnızca await noktalarında olur; iki await arasındaki kod kesintisiz çalışır. "
        "Art arda yazılan await'ler sırayla çalışır: first = await greet('Can') bitmeden ikinci satıra geçilmez, bu yüzden iki 0,1 saniyelik bekleme toplam 0,2 saniye sürer. async yazmak tek başına hiçbir şeyi hızlandırmaz; işleri aynı anda yürütmek için onları görev olarak başlatmak gerekir (sonraki bölüm). "
        "Süre ölçerken loop.time() kullan: asyncio.get_running_loop() çalışan döngüyü verir ve loop.time() döngünün saatini okur. Gerçek kodda await, ağ istemcilerinde (aiohttp, httpx), veritabanı sürücülerinde ve web çatılarında (FastAPI) görülür; hepsinin ortak fikri beklerken başkasına yer açmaktır."
    ),
    code=r'''
import asyncio

async def greet(name: str) -> str:
    await asyncio.sleep(0.1)
    return f"merhaba {name}"

coro = greet("Ada")
print(type(coro).__name__)
print(asyncio.run(coro))

async def main() -> None:
    loop = asyncio.get_running_loop()
    start = loop.time()
    first = await greet("Can")
    second = await greet("Eda")
    print(first, "|", second)
    print(f"süre: {loop.time() - start:.1f} sn")

asyncio.run(main())
''',
    expectedOutput=r'''
coroutine
merhaba Ada
merhaba Can | merhaba Eda
süre: 0.2 sn
''',
    why="greet('Ada') çağrısı gövdeyi çalıştırmadı, bir coroutine nesnesi döndürdü; asyncio.run onu çalıştırıp dönüş değerini verdi. main içindeki iki await sırayla bekledi; ikinci selam birincisi bitmeden başlamadığı için süre 0,1 + 0,1 = 0,2 saniye oldu.",
    alternatives=[
        "İki işin aynı anda beklemesi için asyncio.gather ya da asyncio.create_task kullan (sonraki bölüm).",
        "Async kütüphanesi olmayan bir işi (eski bir istemci, dosya okuma) await ile beklemek için asyncio.to_thread kullanılır (beşinci bölüm).",
    ],
    traps=[
        "await'i unutmak: greet('Can') bir coroutine nesnesidir, metin değil; Python 'coroutine ... was never awaited' uyarısı verir.",
        "await'i async def dışında yazmak (SyntaxError).",
        "Zaten çalışan bir event loop içinden asyncio.run çağırmak (RuntimeError); async kod içinde await kullanılır.",
        "async def yazmanın tek başına kodu hızlandıracağını sanmak; art arda await'ler sırayla bekler.",
    ],
    realCode=r'''
import asyncio

async def fetch_user(user_id: int) -> dict[str, object]:
    await asyncio.sleep(0.05)   # gerçekte: await client.get(f"/users/{user_id}")
    return {"id": user_id, "name": f"kullanıcı{user_id}"}

async def main() -> None:
    user = await fetch_user(7)
    print(user["name"])

if __name__ == "__main__":
    asyncio.run(main())
''',
    realOutput=r'''
kullanıcı7
''',
    lineByLine=[
        "fetch_user bir ağ isteğini temsil eder; gerçek bir async HTTP istemcisinde bekleme satırı await client.get(...) olurdu.",
        "main, programın async giriş noktasıdır; diğer coroutine'leri await ile çağırır.",
        "asyncio.run yalnızca en üstte, bir kez çağrılır ve event loop'u kurup kapatır.",
        "__main__ koruması, dosya içe aktarıldığında programın kendiliğinden başlamasını engeller (M9).",
    ],
    sources=[
        {"title": "Python 3.12 · Coroutine'ler ve görevler", "url": DOCS + "asyncio-task.html"},
        {"title": "Python 3.12 · asyncio.run", "url": DOCS + "asyncio-runner.html"},
    ],
    runtimeNote=ASYNC_NOTE,
)

section(
    id="tasks-gather",
    title="Görevler: create_task, gather ve TaskGroup",
    eyebrow="Beklemeleri aynı anda yürüt",
    depth="okuma",
    objectives=[
        "asyncio.gather ve asyncio.create_task ile coroutine'leri aynı anda yürüten kodu okur; toplam sürenin en uzun beklemeye indiğini gösterir.",
        "gather'ın sonuçları verilen sırayla döndürdüğünü, create_task'in görevi hemen değil ilk beklemede başlattığını ve TaskGroup'un hata durumunda diğer görevleri iptal ettiğini bilir.",
    ],
    prerequisites=["coroutines"],
    summary="asyncio.gather(a(), b(), c()) üç coroutine'i görev olarak aynı anda başlatır ve hepsi bitince sonuçlarını verilen sırayla bir liste olarak döndürür; toplam süre en uzun işin süresi olur. create_task tek bir görevi arka planda başlatır, TaskGroup ise bir grup görevi birlikte yönetir.",
    explanation=(
        "Bir coroutine'i Task (görev) olarak sarmak, onu event loop'a 'fırsat bulunca bunu da yürüt' diye teslim etmektir. asyncio.create_task(fetch('d')) görevi planlar ve hemen döner; görev, çağıran kod bir await'te duraklayınca çalışmaya başlar. Sonucu almak için görev await edilir: result = await task. Oluşturulan görevlere bir referans tutulmalıdır; aksi hâlde görev bitmeden çöp toplayıcı tarafından silinebilir. "
        "asyncio.gather(*coroutineler) verilen coroutine'leri görev olarak başlatır, hepsinin bitmesini bekler ve sonuçları verilen sırayla döndürür; bitiş sırası farklı olsa bile. Üç bekleme 0,3, 0,1 ve 0,2 saniye sürüyorsa toplam süre 0,6 değil 0,3 saniyedir. Görevlerden biri hata verirse gather o hatayı fırlatır ama diğer görevler çalışmaya devam eder; return_exceptions=True verilirse hatalar da listede sonuç olarak döner. "
        "Python 3.11'den beri asyncio.TaskGroup daha güvenli bir yol sunar: async with asyncio.TaskGroup() as group: bloğunda group.create_task(...) ile başlatılan bütün görevler blok sonunda beklenir. Görevlerden biri hata verirse diğerleri iptal edilir ve hatalar bir ExceptionGroup içinde fırlatılır; böylece hiçbir görev sahipsiz kalmaz. Sonuçlar görev nesnelerinden task.result() ile okunur. "
        "Çıktının sırasına dikkat: önce bütün görevler 'başladı' yazar (her biri ilk await'te duraklar), sonra bitenler bitiş sırasıyla yazar. Bu düzen zamanlamaya bağlıdır; gerçek ağ isteklerinde bitiş sırası her çalıştırmada değişebilir, bu yüzden sonuçları bitiş sırasına değil gather'ın döndürdüğü listeye göre kullan."
    ),
    code=r'''
import asyncio

async def fetch(name: str, delay: float) -> str:
    print("başladı", name)
    await asyncio.sleep(delay)
    print("bitti", name)
    return name.upper()

async def main() -> None:
    loop = asyncio.get_running_loop()
    start = loop.time()
    results = await asyncio.gather(fetch("a", 0.3), fetch("b", 0.1), fetch("c", 0.2))
    print(results, f"{loop.time() - start:.1f} sn")
    task = asyncio.create_task(fetch("d", 0.1))
    print("görev oluşturuldu")
    print(await task)

asyncio.run(main())
''',
    expectedOutput=r'''
başladı a
başladı b
başladı c
bitti b
bitti c
bitti a
['A', 'B', 'C'] 0.3 sn
görev oluşturuldu
başladı d
bitti d
D
''',
    why="gather üç görevi birlikte başlattı; her biri ilk await'te duraklayınca sıradaki başladı. Bitiş sırası bekleme sürelerine göre (b, c, a) oldu ama sonuç listesi verilen sırayla ['A', 'B', 'C'] döndü ve toplam süre en uzun bekleme kadar, 0,3 saniye sürdü. create_task görevi planladı ama main await'e gelene kadar görev başlamadı; bu yüzden önce 'görev oluşturuldu' yazıldı.",
    alternatives=[
        "Yeni kodda görev gruplarını asyncio.TaskGroup ile yönet; bir görev hata verirse diğerlerini iptal eder.",
        "Sonuçları bitiş sırasıyla işlemek için asyncio.as_completed kullan.",
    ],
    traps=[
        "Coroutine'leri listeye koyup await etmeden bırakmak; görev olmayan coroutine hiç çalışmaz.",
        "Sonuç listesinin bitiş sırasıyla geldiğini sanmak; gather verilen sırayı korur.",
        "create_task ile başlatılan görevin referansını tutmamak; görev bitmeden kaybolabilir.",
        "gather'da bir görev hata verince diğerlerinin durduğunu sanmak; durmazlar (TaskGroup durdurur).",
    ],
    realCode=r'''
import asyncio

PRICES = {"USD": 32.5, "EUR": 35.25}

async def fetch_price(code: str) -> float:
    await asyncio.sleep(0.1)   # gerçekte: kur servisine istek
    return PRICES[code]

async def main() -> None:
    async with asyncio.TaskGroup() as group:
        tasks = {code: group.create_task(fetch_price(code)) for code in ("USD", "EUR")}
    for code, task in tasks.items():
        print(code, task.result())

asyncio.run(main())
''',
    realOutput=r'''
USD 32.5
EUR 35.25
''',
    lineByLine=[
        "fetch_price bir kur servisine yapılan isteği temsil eder.",
        "TaskGroup bloğunda iki görev aynı anda başlatılır; blok, ikisi de bitmeden kapanmaz.",
        "Görevlerden biri hata verseydi diğeri iptal edilir ve hata bloğun sonunda fırlatılırdı.",
        "Blok bittikten sonra her görevin sonucu task.result() ile güvenle okunur.",
    ],
    sources=[
        {"title": "Python 3.12 · gather ve create_task", "url": DOCS + "asyncio-task.html#running-tasks-concurrently"},
        {"title": "Python 3.12 · TaskGroup", "url": DOCS + "asyncio-task.html#task-groups"},
    ],
    runtimeNote=ASYNC_NOTE,
)

section(
    id="blocking-loop",
    title="Event loop'u bloklamak",
    eyebrow="time.sleep ile asyncio.sleep aynı şey değil",
    depth="okuma",
    objectives=[
        "Bir coroutine içindeki bloklayan çağrının (time.sleep, uzun hesap, async olmayan kütüphane) bütün event loop'u durdurduğunu çıktıdan ve süreden gösterir.",
        "Bloklayan işi asyncio.to_thread ile bir thread'e aktarmayı ve uzun hesaplamada ara ara await asyncio.sleep(0) ile döngüye sıra vermeyi okur.",
    ],
    prerequisites=["tasks-gather", "threads"],
    summary="Event loop tek iş parçacığında çalıştığı için, bir coroutine await etmeden uzun süre çalışırsa diğer bütün görevler bekler. time.sleep, döngüye haber vermeden bütün programı durdurur; asyncio.sleep ise yalnızca o görevi duraklatır. Async olmayan bloklayan çağrılar asyncio.to_thread ile bir thread'e aktarılır.",
    explanation=(
        "Event loop yalnızca await noktalarında görev değiştirebilir. Bir coroutine içinde time.sleep(0.2) çağırmak, döngüye 'başkası çalışsın' demeden bütün iş parçacığını 0,2 saniye durdurur: o sırada hiçbir görev ilerlemez. Üç görev aynı anda başlatılsa bile her biri sırayla 0,2 saniye bloklayınca toplam süre 0,6 saniye olur. await asyncio.sleep(0.2) ise yalnızca o görevi duraklatır; üç görev 0,2 saniyede biter. "
        "Aynı sorun her bloklayan çağrıda vardır: async olmayan bir HTTP kütüphanesiyle (requests) istek atmak, büyük bir dosyayı open ile okumak, uzun bir döngüde hesap yapmak. Async kodda bunlar web sunucusunun bütün kullanıcılara yanıt vermeyi kesmesi gibi görünür. Kural: async kodda bekleyen her şey await edilmelidir; await edilemeyen bekleme ya da hesap döngünün dışına taşınmalıdır. "
        "asyncio.to_thread(func, *args) bloklayan bir fonksiyonu ayrı bir thread'de çalıştırır ve onu await edilebilir yapar; event loop bu sırada diğer görevleri sürdürür. Hesaplama işlerinde (GIL yüzünden) thread yerine loop.run_in_executor ile bir ProcessPoolExecutor kullanılır. Kısa süren ama uzun döngülü hesaplarda bir ara yol, döngüde ara ara await asyncio.sleep(0) yazarak diğer görevlere sıra vermektir. "
        "Tarayıcıdaki Python thread başlatamadığı için asyncio.to_thread burada çalışmaz; örneği aşağıda yerel Python için. asyncio'nun hata ayıklama modu (asyncio.run(main(), debug=True)) 0,1 saniyeden uzun bloklayan adımları uyarı olarak yazar ve bu tür sorunları bulmanın kolay yoludur."
    ),
    code=r'''
import asyncio
import time

async def blocking(name: str) -> None:
    time.sleep(0.2)            # bütün döngüyü durdurur
    print("bitti", name)

async def polite(name: str) -> None:
    await asyncio.sleep(0.2)   # yalnızca bu görevi duraklatır
    print("bitti", name)

async def measure(job) -> None:
    loop = asyncio.get_running_loop()
    start = loop.time()
    await asyncio.gather(job("a"), job("b"), job("c"))
    print(job.__name__, f"{loop.time() - start:.1f} sn")

asyncio.run(measure(blocking))
asyncio.run(measure(polite))
''',
    expectedOutput=r'''
bitti a
bitti b
bitti c
blocking 0.6 sn
bitti a
bitti b
bitti c
polite 0.2 sn
''',
    why="Çıktı satırları iki durumda da aynı sırada; fark süredir. blocking içindeki time.sleep döngüye kontrolü vermediği için görevler birbirini bekledi ve süreler toplandı (0,6 sn). polite'te üç bekleme örtüştü ve toplam süre tek bir beklemeye (0,2 sn) indi.",
    alternatives=[
        "Bloklayan bir kütüphane çağrısını await asyncio.to_thread(func, ...) ile thread'e aktar (yerel örnek).",
        "Async sürümü olan kütüphaneyi seç: requests yerine httpx.AsyncClient ya da aiohttp gibi.",
    ],
    traps=[
        "async def içinde time.sleep kullanmak; kod çalışır ama eşzamanlılık kaybolur.",
        "Bloklama hatasının hata mesajı vermediğini unutmak: program yalnızca yavaşlar, bu yüzden süre ölçülmeden fark edilmez.",
        "Hesaplama ağırlıklı işi asyncio.to_thread ile hızlandırmayı beklemek; GIL yüzünden döngüyü serbest bırakır ama hesabı hızlandırmaz.",
    ],
    localExample={
        "note": "asyncio.to_thread bir thread kullandığı için tarayıcıda çalışmaz. Kendi bilgisayarında python yerel.py ile çalıştır.",
        "code": r'''
import asyncio
import time

def blocking_read(name: str) -> str:
    time.sleep(0.3)      # async olmayan eski bir kütüphane çağrısı gibi
    return name.upper()

async def main() -> None:
    loop = asyncio.get_running_loop()
    start = loop.time()
    results = await asyncio.gather(*(asyncio.to_thread(blocking_read, n) for n in ("a", "b", "c")))
    print(results, f"{loop.time() - start:.1f} sn")

asyncio.run(main())
''',
        "output": r'''
['A', 'B', 'C'] 0.3 sn
''',
    },
    realCode=r'''
import asyncio

async def heartbeat(stop: asyncio.Event, beats: list[int]) -> None:
    while not stop.is_set():
        beats.append(1)
        await asyncio.sleep(0)

async def crunch(n: int, stop: asyncio.Event) -> int:
    total = 0
    for i in range(n):
        total += i * i
        if i % 1000 == 999:
            await asyncio.sleep(0)   # uzun hesapta ara ara döngüye sıra ver
    stop.set()
    return total

async def main() -> None:
    stop = asyncio.Event()
    beats: list[int] = []
    _, total = await asyncio.gather(heartbeat(stop, beats), crunch(3000, stop))
    print("sonuç:", total, "nabız:", len(beats))

asyncio.run(main())
''',
    realOutput=r'''
sonuç: 8995500500 nabız: 4
''',
    lineByLine=[
        "heartbeat, bir web sunucusunun öbür kullanıcılara yanıt vermesi gibi sürekli sıra bekleyen bir görevi temsil eder.",
        "crunch uzun bir hesap yapar ama her 1000 adımda await asyncio.sleep(0) ile döngüye sıra verir.",
        "Bu sayede heartbeat hesap sürerken de çalışır; await olmasaydı hesap bitene kadar yalnızca bir kez çalışabilirdi.",
        "Hesap bitince Event kurulur ve heartbeat döngüden çıkar; gather iki sonucu birlikte döndürür.",
    ],
    sources=[
        {"title": "Python 3.12 · asyncio ile geliştirme (bloklayan kod)", "url": DOCS + "asyncio-dev.html#running-blocking-code"},
        {"title": "Python 3.12 · asyncio.to_thread", "url": DOCS + "asyncio-task.html#running-in-threads"},
    ],
    runtime="mixed",
    runtimeNote="Editör örnekleri tarayıcıda çalışır (site boşta beklemeyi atlar, time.sleep ise gerçekten bekler). asyncio.to_thread thread kullandığı için onun örneği yerel Python içindir.",
)

section(
    id="cancellation-timeout",
    title="İptal ve zaman aşımı",
    eyebrow="Sonsuza dek bekleme",
    depth="okuma",
    objectives=[
        "asyncio.wait_for ve async with asyncio.timeout(...) ile bir beklemeye süre sınırı koyar; aşımda TimeoutError yakalar.",
        "task.cancel()'ın görevde CancelledError fırlattığını, finally ile kaynakların kapatıldığını ve CancelledError'ın yakalanıp yutulmaması gerektiğini açıklar.",
    ],
    prerequisites=["tasks-gather", "m7:else-finally"],
    summary="Ağ çağrıları takılabilir; her beklemeye bir üst süre koymak gerekir. wait_for ve asyncio.timeout süre dolunca işi iptal edip TimeoutError fırlatır. İptal, görevin içinde bir CancelledError olarak görünür; finally blokları kaynakları kapatır ve hata yeniden fırlatılarak iptal tamamlanır.",
    explanation=(
        "Bir görev iptal edildiğinde (task.cancel()), görevin beklediği await noktasında asyncio.CancelledError fırlatılır. Bu hata görevin içinden yukarı doğru yayılır: try/finally blokları çalışır, bağlantılar ve dosyalar kapatılır, görev 'iptal edildi' durumunda biter. Görevi await eden kod da CancelledError alır; task.cancelled() True döner. "
        "CancelledError, Exception'dan değil BaseException'dan türer; bu yüzden except Exception onu yanlışlıkla yutmaz. İptali yakalayıp temizlik yapmak meşrudur ama sonunda raise ile yeniden fırlatılmalıdır; yutulursa görev iptal edilmemiş gibi devam eder ve iptal isteyen kod (zaman aşımı, TaskGroup) bozulur. Temizlik için çoğu zaman finally yeterlidir. "
        "Zaman aşımı, iptalin otomatik hâlidir. asyncio.wait_for(coro, timeout=0.5) işi başlatır; 0,5 saniyede bitmezse işi iptal eder, iptalin bitmesini bekler ve TimeoutError fırlatır. Python 3.11'den beri async with asyncio.timeout(0.5): bloğu aynı işi birden çok satır için yapar. Python 3.11'den beri asyncio.TimeoutError yerleşik TimeoutError ile aynıdır. "
        "Gerçek kodda zaman aşımı çoğu zaman yeniden denemeyle birlikte kullanılır: birkaç deneme, her denemede bir süre sınırı, sonunda vazgeçip None ya da açık bir hata döndürmek. Hiç süre sınırı olmayan bir ağ çağrısı, karşı taraf yanıt vermediğinde programı sonsuza dek bekletebilir."
    ),
    code=r'''
import asyncio

async def download(name: str, seconds: float) -> str:
    try:
        await asyncio.sleep(seconds)
        return f"{name} indi"
    except asyncio.CancelledError:
        print(name, "iptal edildi, temizleniyor")
        raise
    finally:
        print(name, "bağlantı kapandı")

async def main() -> None:
    try:
        print(await asyncio.wait_for(download("küçük", 0.1), timeout=1))
        print(await asyncio.wait_for(download("büyük", 5), timeout=0.5))
    except TimeoutError:
        print("zaman aşımı")
    task = asyncio.create_task(download("yedek", 5))
    await asyncio.sleep(0.1)
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        print("iptal edildi mi?", task.cancelled())

asyncio.run(main())
''',
    expectedOutput=r'''
küçük bağlantı kapandı
küçük indi
büyük iptal edildi, temizleniyor
büyük bağlantı kapandı
zaman aşımı
yedek iptal edildi, temizleniyor
yedek bağlantı kapandı
iptal edildi mi? True
''',
    why="Küçük indirme süre sınırından önce bitti; finally yine de çalıştı. Büyük indirme 0,5 saniyede bitmeyince wait_for onu iptal etti: görevde CancelledError oluştu, temizlik yapıldı, hata yeniden fırlatıldı ve main'e TimeoutError olarak ulaştı. Yedek görevi elle iptal edildi; await eden kod CancelledError aldı ve görev 'iptal edildi' durumunda bitti.",
    alternatives=[
        "Birden çok satırı aynı süre sınırına almak için async with asyncio.timeout(0.5): kullan (Python 3.11+).",
        "Ağ kütüphanelerinin kendi timeout parametrelerini de ayarla (httpx.AsyncClient(timeout=5) gibi).",
    ],
    traps=[
        "except asyncio.CancelledError: içinde raise yazmayıp iptali yutmak.",
        "Ağ çağrılarını hiç süre sınırı koymadan beklemek.",
        "TimeoutError yakalandığında işin arka planda sürdüğünü sanmak; wait_for işi iptal etmiştir.",
        "Temizliği yalnızca başarılı yolda yapmak; iptal ve hata yollarında da çalışması için finally kullan.",
    ],
    realCode=r'''
import asyncio

class FlakyService:
    def __init__(self) -> None:
        self.calls = 0

    async def call(self) -> str:
        self.calls += 1
        await asyncio.sleep(2 if self.calls < 3 else 0.1)   # ilk iki çağrı takılıyor
        return "yanıt"

async def call_with_retry(service: FlakyService, retries: int, limit: float) -> str | None:
    for attempt in range(1, retries + 1):
        try:
            async with asyncio.timeout(limit):
                return await service.call()
        except TimeoutError:
            print(f"deneme {attempt}: zaman aşımı")
    return None

print(asyncio.run(call_with_retry(FlakyService(), 3, 0.5)))
''',
    realOutput=r'''
deneme 1: zaman aşımı
deneme 2: zaman aşımı
yanıt
''',
    lineByLine=[
        "FlakyService, bazen yanıt vermeyen bir dış servisi temsil eder.",
        "Her denemede async with asyncio.timeout(limit) bloğu bekleme süresini sınırlar; süre dolunca çağrı iptal edilir ve TimeoutError fırlar.",
        "Zaman aşımı yakalanıp yazdırılır ve döngü sonraki denemeye geçer; üçüncü deneme zamanında yanıt alır.",
        "Bütün denemeler tükenirse fonksiyon None döndürür; dönüş tipi str | None bunu belgeler.",
    ],
    sources=[
        {"title": "Python 3.12 · Zaman aşımları", "url": DOCS + "asyncio-task.html#timeouts"},
        {"title": "Python 3.12 · Görev iptali", "url": DOCS + "asyncio-task.html#task-cancellation"},
    ],
    runtimeNote=ASYNC_NOTE,
)

section(
    id="shared-state",
    title="Paylaşılan veri: yarış durumu ve kilit",
    eyebrow="Oku, bekle, yaz: arada ne oldu?",
    depth="okuma",
    objectives=[
        "Oku-bekle-yaz adımları arasında başka bir görevin veriyi değiştirmesiyle oluşan yarış durumunu (race condition) çıktıdan bulur.",
        "asyncio.Lock ve threading.Lock ile kritik bölgeyi tek parça yapar; paylaşılan veri yerine Queue ile iş dağıtmayı okur.",
    ],
    prerequisites=["tasks-gather", "threads", "m11:methods-state"],
    summary="İki görev aynı veriyi okuyup bir süre bekledikten sonra eski değere göre yazarsa, birinin güncellemesi kaybolur: buna yarış durumu denir. Kilit (Lock), oku-denetle-yaz adımlarını tek parça yapar; asyncio.Queue ise veriyi paylaşmak yerine işleri sırayla dağıtır.",
    explanation=(
        "Yarış durumu (race condition), sonucun işlerin hangi sırayla ilerlediğine bağlı olmasıdır. Tipik desen oku-bekle-yaz'dır: bir görev bakiyeyi okur, bir ağ çağrısını bekler, sonra okuduğu eski değere göre yeni bakiyeyi yazar. Beklerken başka bir görev aynı bakiyeyi okuyup değiştirirse, iki görev de 'yeterli para var' sonucuna varır ve birinin yazdığı değer diğerininkini ezer. "
        "asyncio'da görev değişimi yalnızca await noktalarında olur, bu yüzden iki await arasındaki kod güvendedir ve yarışlar await'in olduğu yerde aranır. Thread'lerde ise geçiş hemen her bayt kodu arasında olabilir: count += 1 bile oku, topla, yaz adımlarından oluşur ve iki thread arasında kesilebilir. Bu hatalar zamanlamaya bağlıdır; kodu yüz kez çalıştırıp hiç görmeyebilir, üretimde bir gün karşılaşabilirsin. "
        "Çözüm, kritik bölgeyi (oku-denetle-yaz) bir kilitle korumaktır. asyncio.Lock async with lock: ile, threading.Lock ise with lock: ile kullanılır (M13'teki context manager'lar); kilidi aynı anda yalnızca bir görev tutar, diğerleri bekler. Kilidi gereğinden geniş tutmak eşzamanlılığı yok eder, kilitleri farklı sıralarla almak ise iki görevin birbirini sonsuza dek beklemesine (deadlock) yol açar. "
        "Çoğu zaman en iyi kilit, hiç paylaşmamaktır: her görev kendi sonucunu döndürür ve sonuçlar sonunda birleştirilir (gather, pool.map), ya da işler bir kuyruktan (asyncio.Queue, queue.Queue) alınır. Kuyruk, birden çok üreticinin ve tüketicinin veriyi kilitsiz ve sırayla paylaşmasını sağlar; queue.join() bütün işlerin task_done ile bitirilmesini bekler."
    ),
    code=r'''
import asyncio

class Account:
    def __init__(self, balance: int) -> None:
        self.balance = balance
        self.lock = asyncio.Lock()

    async def withdraw_unsafe(self, amount: int) -> None:
        current = self.balance              # oku
        await asyncio.sleep(0.1)            # bu arada öbür görev çalışır
        if current >= amount:
            self.balance = current - amount  # eski değere göre yaz
            print("çekildi", amount)

    async def withdraw(self, amount: int) -> None:
        async with self.lock:               # oku-denetle-yaz tek parça
            if self.balance >= amount:
                await asyncio.sleep(0.1)
                self.balance -= amount
                print("çekildi", amount)
            else:
                print("yetersiz", amount)

async def main() -> None:
    first = Account(100)
    await asyncio.gather(first.withdraw_unsafe(80), first.withdraw_unsafe(70))
    print("kilitsiz bakiye:", first.balance)
    second = Account(100)
    await asyncio.gather(second.withdraw(80), second.withdraw(70))
    print("kilitli bakiye:", second.balance)

asyncio.run(main())
''',
    expectedOutput=r'''
çekildi 80
çekildi 70
kilitsiz bakiye: 30
çekildi 80
yetersiz 70
kilitli bakiye: 20
''',
    why="Kilitsiz sürümde iki görev de bakiyeyi 100 olarak okudu, ikisi de beklerken öbürü değişmedi sandı ve ikisi de para çekti; son yazan (100 - 70) kazandı ve 80 liralık çekiş kayboldu. Kilitli sürümde ikinci görev, birincisi işini bitirene kadar bekledi ve güncel bakiyeyi (20) görerek çekişi reddetti.",
    alternatives=[
        "Paylaşılan durumu hiç kullanma: her görev kendi sonucunu döndürsün, sonuçlar en sonda birleştirilsin.",
        "Üretici-tüketici işlerinde asyncio.Queue ya da thread'ler için queue.Queue kullan.",
    ],
    traps=[
        "Bir kez doğru çalıştı diye eşzamanlı kodun güvenli olduğunu sanmak; yarış hataları zamanlamaya bağlıdır.",
        "Kilidi yalnızca yazma satırına koyup okumayı dışarıda bırakmak; denetim ile yazma arasında yine yarış olur.",
        "İki kilidi farklı yerlerde farklı sırayla almak (deadlock).",
        "asyncio kodunda threading.Lock kullanmak; await sırasında tutulan thread kilidi bütün döngüyü kilitleyebilir.",
    ],
    localExample={
        "note": "Tarayıcıdaki Python thread başlatamaz. Kendi bilgisayarında python yerel.py ile çalıştır. Kilidi kaldırırsan sonuç bazı çalıştırmalarda 400000'den az çıkabilir; güncel CPython'da bu kısa döngüde nadiren görülür ama nadir olması güvenli olduğu anlamına gelmez.",
        "code": r'''
import threading

count = 0
lock = threading.Lock()

def add_many(n: int) -> None:
    global count
    for _ in range(n):
        with lock:          # count += 1 oku-topla-yaz adımlarından oluşur
            count += 1

threads = [threading.Thread(target=add_many, args=(100_000,)) for _ in range(4)]
for thread in threads:
    thread.start()
for thread in threads:
    thread.join()
print(count)
''',
        "output": r'''
400000
''',
    },
    realCode=r'''
import asyncio

async def worker(wid: int, queue: asyncio.Queue[str], done: list[str]) -> None:
    while True:
        job = await queue.get()
        await asyncio.sleep(0.1 * len(job))   # işin süresi adının uzunluğu kadar
        done.append(f"{job}@{wid}")
        queue.task_done()

async def main() -> None:
    queue: asyncio.Queue[str] = asyncio.Queue()
    for job in ["ab", "c", "def", "g"]:
        queue.put_nowait(job)
    done: list[str] = []
    workers = [asyncio.create_task(worker(wid, queue, done)) for wid in (1, 2)]
    await queue.join()
    for task in workers:
        task.cancel()
    print(done)

asyncio.run(main())
''',
    realOutput=r'''
['c@2', 'ab@1', 'g@1', 'def@2']
''',
    lineByLine=[
        "İşler kuyruğa konur; iki çalışan görev işleri kuyruktan sırayla alır ve aynı işi iki kez almaz.",
        "Çalışan 2 kısa 'c' işini önce bitirip 'def'i alır; çalışan 1 'ab'yi bitirince 'g'yi alır.",
        "queue.join(), konan her iş için task_done çağrılana kadar bekler.",
        "Çalışanlar sonsuz döngüdedir; işler bitince iptal edilerek kapatılırlar.",
    ],
    sources=[
        {"title": "Python 3.12 · asyncio senkronizasyon (Lock)", "url": DOCS + "asyncio-sync.html"},
        {"title": "Python 3.12 · asyncio.Queue", "url": DOCS + "asyncio-queue.html"},
        {"title": "Python 3.12 · threading.Lock", "url": DOCS + "threading.html#lock-objects"},
    ],
    runtime="mixed",
    runtimeNote="Editör örnekleri tarayıcıda çalışır (site boşta beklemeyi atlar). threading.Lock'lu thread örneği thread başlattığı için yerel Python içindir.",
)
