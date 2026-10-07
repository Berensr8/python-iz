"""M13 (İleri yapılar) questions. Imported by build_m13.py.

Order: 12 output, 6 bug, 4 fill, 4 order, 10 code, 4 traceback (ids m13-q01 ... m13-q40).
"""

from _qhelper import make_questions

questions, q = make_questions("m13")

# ------------------------------------------------------------------ output (12)
q(type="output", topic="iterator", sectionId="iterator-protocol", difficulty=1,
  prompt="Bir iterator'dan önce next ile değer alınıyor, sonra iki kez listeye çevriliyor. Çıktı ne olur?",
  code=r'''
it = iter([1, 2, 3])
first = next(it)
print(first, list(it), list(it))
''',
  expectedOutput="1 [2, 3] []",
  options=["1 [2, 3] []", "1 [2, 3] [2, 3]", "1 [1, 2, 3] []", "1 [2, 3] [1, 2, 3]"],
  hints=["next ilk değeri tüketti.", "Tükenen iterator baştan başlar mı?"],
  explanation="next(it) 1'i aldı; ilk list() kalan 2 ve 3'ü tüketti. Iterator geri sarılmadığı için ikinci list() boş liste verir.")

q(type="output", topic="map-tukenme", sectionId="iterator-protocol", difficulty=2,
  prompt="map sonucu iki kez toplanıyor. Çıktı ne olur?",
  code=r'''
squares = map(lambda n: n * n, [1, 2, 3])
print(sum(squares), sum(squares))
''',
  expectedOutput="14 0",
  options=["14 0", "14 14", "0 14", "TypeError verir"],
  hints=["map liste değil, iterator döndürür.", "Boş bir dizinin toplamı kaçtır?"],
  explanation="map bir iterator'dır. İlk sum değerleri tüketip 1 + 4 + 9 = 14 verir; ikinci sum boş iterator'ı toplar ve 0 döner.")

q(type="output", topic="kendi-iterator", sectionId="custom-iterator", difficulty=2,
  prompt="__iter__ self döndüren bir sınıf iki kez dolaşılıyor. Çıktı ne olur?",
  code=r'''
class Two:
    def __init__(self):
        self.n = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.n == 2:
            raise StopIteration
        self.n += 1
        return self.n

t = Two()
print(list(t), list(t), list(Two()))
''',
  expectedOutput="[1, 2] [] [1, 2]",
  options=["[1, 2] [] [1, 2]", "[1, 2] [1, 2] [1, 2]", "[1, 2] [] []", "[0, 1] [] [0, 1]"],
  hints=["İlk list() sonunda t.n kaç olur?", "Two() yeni bir nesne, kendi sayacıyla."],
  explanation="t kendisinin iterator'ıdır; ilk list() sayacı 2'ye getirir, ikinci list() hemen StopIteration alır. Yeni bir Two() kendi sayacıyla baştan başlar.")

q(type="output", topic="generator-sira", sectionId="generators", difficulty=1,
  prompt="Generator fonksiyonu çağrılıyor ve bir değer isteniyor. Çıktı ne olur?",
  code=r'''
def gen():
    print("A")
    yield 1
    print("B")

g = gen()
print("C")
print(next(g))
''',
  expectedOutput="C\nA\n1",
  options=["C / A / 1", "A / C / 1", "C / A / 1 / B", "A / 1 / C"],
  hints=["gen() çağrısı gövdeyi çalıştırır mı?", "next, gövdeyi ilk yield'e kadar çalıştırır."],
  explanation="gen() yalnızca generator nesnesini kurar; gövde çalışmaz. 'C' yazıldıktan sonra next gövdeyi başlatır: 'A' yazılır ve yield 1'de durulur. 'B' ancak bir sonraki next istenirse çalışırdı.")

q(type="output", topic="generator-sira", sectionId="generators", difficulty=2,
  prompt="yield'ler arasında print var ve generator listeye çevriliyor. Çıktı ne olur?",
  code=r'''
def steps():
    yield "bir"
    print("ara")
    yield "iki"

print(list(steps()))
''',
  expectedOutput="ara\n['bir', 'iki']",
  options=["ara / ['bir', 'iki']", "['bir', 'iki'] / ara", "['bir', 'ara', 'iki']", "['bir', 'iki']"],
  hints=["print, listeye bir değer ekler mi?", "list() bütün değerleri toplamadan önce yazdırılabilir mi?"],
  explanation="list() generator'ı tüketirken ikinci değeri isterken 'ara' satırı çalışır ve hemen ekrana yazılır. Liste ancak generator bitince tamamlanır ve sonra yazdırılır; print değer üretmez.")

q(type="output", topic="generator-return", sectionId="generators", difficulty=3,
  prompt="Generator'da return'den sonra bir yield daha var. Çıktı ne olur?",
  code=r'''
def g():
    yield 1
    return 5
    yield 2

print(list(g()))
it = g()
next(it)
try:
    next(it)
except StopIteration as stop:
    print(stop.value)
''',
  expectedOutput="[1]\n5",
  options=["[1] / 5", "[1, 5] / 5", "[1, 2] / None", "[1] / None"],
  hints=["return generator'ı bitirir; sonraki yield'e ulaşılır mı?", "return'ün değeri nerede görünür?"],
  explanation="return yinelemeyi bitirir; yield 2 hiç çalışmaz ve list() yalnızca [1] toplar. return değeri listeye girmez, StopIteration.value'da 5 olarak görünür.")

q(type="output", topic="generator-ifadesi", sectionId="generator-pipelines", difficulty=2,
  prompt="Generator ifadesinde in sorgusundan sonra kalanlar listeleniyor. Çıktı ne olur?",
  code=r'''
gen = (n * 2 for n in range(5))
print(4 in gen, list(gen))
''',
  expectedOutput="True [6, 8]",
  options=["True [6, 8]", "True [0, 2, 4, 6, 8]", "True [8]", "False []"],
  hints=["gen sırayla 0, 2, 4, 6, 8 üretir.", "in, aradığını bulana kadar değer tüketir."],
  explanation="4 in gen; 0, 2 ve 4'ü tüketip True döner. list(gen) yalnızca kalan 6 ve 8'i toplar.")

q(type="output", topic="yield-from", sectionId="generator-pipelines", difficulty=2,
  prompt="yield from ile iç generator dışarı aktarılıyor. Çıktı ne olur?",
  code=r'''
def inner():
    yield 1
    yield 2

def outer():
    yield 0
    yield from inner()
    yield 3

print(list(outer()))
''',
  expectedOutput="[0, 1, 2, 3]",
  options=["[0, 1, 2, 3]", "[0, [1, 2], 3]", "[0, 3]", "[1, 2, 0, 3]"],
  hints=["yield from, alt generator'ın değerlerini tek tek verir.", "Değerler hangi sırayla gelir?"],
  explanation="outer önce 0'ı verir, yield from inner'ın 1 ve 2'sini sırayla aktarır, sonra 3 gelir. Değerler bir liste olarak değil tek tek üretilir.")

q(type="output", topic="decorator-zamani", sectionId="decorators", difficulty=2,
  prompt="Decorator'ın gövdesinde print var. Çıktı sırası nedir?",
  code=r'''
def announce(func):
    print("süsleniyor:", func.__name__)
    return func

@announce
def work():
    return "çalıştı"

print("tanımdan sonra")
print(work())
''',
  expectedOutput="süsleniyor: work\ntanımdan sonra\nçalıştı",
  options=[
      "süsleniyor: work / tanımdan sonra / çalıştı",
      "tanımdan sonra / süsleniyor: work / çalıştı",
      "tanımdan sonra / çalıştı",
      "tanımdan sonra / süsleniyor: work / çalıştı / süsleniyor: work",
  ],
  hints=["@announce satırı work = announce(work) demektir.", "Bu atama ne zaman yapılır: tanımda mı, çağrıda mı?"],
  explanation="Decorator fonksiyon tanımlanırken bir kez çalışır ve 'süsleniyor' yazar. announce asıl fonksiyonu olduğu gibi döndürdüğü için work() çağrısında decorator kodu tekrar çalışmaz.")

q(type="output", topic="wrapper-return", sectionId="decorators", difficulty=3,
  prompt="Sarmalayıcı asıl fonksiyonu çağırıyor. add(2, 3) ne verir?",
  code=r'''
def log(func):
    def wrapper(*args):
        print("çağrı", args)
        func(*args)
    return wrapper

@log
def add(a, b):
    return a + b

print(add(2, 3))
''',
  expectedOutput="çağrı (2, 3)\nNone",
  options=["çağrı (2, 3) / None", "çağrı (2, 3) / 5", "5", "çağrı 2 3 / 5"],
  hints=["*args bir demettir.", "wrapper func'ın sonucunu döndürüyor mu?"],
  explanation="args demet olarak (2, 3) yazdırılır. wrapper func(*args) sonucunu döndürmediği için add(2, 3) None verir; doğrusu return func(*args) olmalı.")

q(type="output", topic="yigma", sectionId="decorator-params", difficulty=3,
  prompt="İki parametreli decorator üst üste. base() ne döndürür?",
  code=r'''
def plus(n):
    def deco(func):
        def wrapper():
            return func() + n
        return wrapper
    return deco

def times(n):
    def deco(func):
        def wrapper():
            return func() * n
        return wrapper
    return deco

@plus(1)
@times(10)
def base():
    return 2

print(base())
''',
  expectedOutput="21",
  options=["21", "30", "12", "22"],
  hints=["def'e en yakın decorator önce uygulanır.", "base = plus(1)(times(10)(base))"],
  explanation="times(10) içte, plus(1) dışta durur. Çağrıda dıştaki sarmalayıcı içtekini çağırır: 2 * 10 = 20, sonra 20 + 1 = 21.")

q(type="output", topic="exit-true", sectionId="context-manager-class", difficulty=2,
  prompt="__exit__ True döndürüyor ve blokta bir hata oluşuyor. Çıktı ne olur?",
  code=r'''
class Quiet:
    def __enter__(self):
        return "kaynak"

    def __exit__(self, exc_type, exc, tb):
        print("kapandı", exc_type.__name__ if exc_type else None)
        return True

with Quiet() as res:
    print(res)
    1 / 0
    print("buraya gelmez")
print("program sürüyor")
''',
  expectedOutput="kaynak\nkapandı ZeroDivisionError\nprogram sürüyor",
  options=[
      "kaynak / kapandı ZeroDivisionError / program sürüyor",
      "kaynak / kapandı ZeroDivisionError / buraya gelmez / program sürüyor",
      "kaynak / kapandı None / program sürüyor",
      "kaynak / kapandı ZeroDivisionError (ardından ZeroDivisionError ile durur)",
  ],
  hints=["as res, __enter__'in döndürdüğü değeri alır.", "Hata bloğun kalanını atlar; __exit__ True döndürürse hata ne olur?"],
  explanation="__enter__ 'kaynak' döndürür. 1 / 0 bloğun kalanını atlar ve __exit__ hata türüyle çağrılır. True döndüğü için hata yutulur ve program with'ten sonra devam eder.")

# ------------------------------------------------------------------ bug (6)
q(type="bug", topic="stopiteration", sectionId="custom-iterator", difficulty=2,
  prompt="list(Countdown(3)) neden hiç bitmez?",
  code=r'''
class Countdown:
    def __init__(self, start):
        self.current = start

    def __iter__(self):
        return self

    def __next__(self):
        if self.current > 0:
            self.current -= 1
            return self.current + 1
        return None

print(list(Countdown(3)))
''',
  answer="Bitişte None döndürüyor; yineleme yalnızca StopIteration ile biter, list sonsuza kadar None ekler",
  options=[
      "Bitişte None döndürüyor; yineleme yalnızca StopIteration ile biter, list sonsuza kadar None ekler",
      "__iter__ self döndürdüğü için nesne dolaşılamaz",
      "self.current eksiltildiği için sayaç hiç sıfıra inmez",
      "list() kendi sınıflarını dolaşamaz",
  ],
  optionFeedback={
      "__iter__ self döndürdüğü için nesne dolaşılamaz": "Kendisi iterator olan sınıfın __iter__'i self döndürür; bu doğrudur.",
      "self.current eksiltildiği için sayaç hiç sıfıra inmez": "Sayaç 3, 2, 1 diye iner ve 0'a ulaşır; sorun 0'dan sonrası.",
      "list() kendi sınıflarını dolaşamaz": "__iter__/__next__ olan her nesne list() ile dolaşılabilir.",
  },
  hints=["Sayaç 0'a inince __next__ ne yapıyor?", "for ve list yinelemenin bittiğini nereden anlar?"],
  explanation="İlk üç değerden sonra __next__ None döndürmeye devam eder; None da geçerli bir değerdir. Yineleme ancak raise StopIteration ile biter, bu yüzden list sonsuza kadar None ekler.")

q(type="bug", topic="return-yield", sectionId="generators", difficulty=1,
  prompt="Bütün çift sayılar beklenirken neden yalnızca 2 yazılıyor?",
  code=r'''
def evens(numbers):
    for n in numbers:
        if n % 2 == 0:
            return n

print(evens([1, 2, 3, 4]))
''',
  answer="return ilk çift sayıda fonksiyonu bitirir; her değeri üretmek için yield kullanılmalı",
  options=[
      "return ilk çift sayıda fonksiyonu bitirir; her değeri üretmek için yield kullanılmalı",
      "% işleci çift sayıları doğru bulamaz",
      "for döngüsü listenin yalnızca ilk iki öğesini gezer",
      "print bir listeyi yazdıramaz",
  ],
  optionFeedback={
      "% işleci çift sayıları doğru bulamaz": "n % 2 == 0 çift sayıyı doğru bulur; 2 de 4 de çifttir.",
      "for döngüsü listenin yalnızca ilk iki öğesini gezer": "Döngü bütün listeyi gezerdi; return onu erken kesiyor.",
      "print bir listeyi yazdıramaz": "print listeleri yazdırır; sorun fonksiyonun tek değer döndürmesi.",
  },
  hints=["return çalışınca fonksiyona ne olur?", "Değerleri birer birer üretmenin anahtar sözcüğü hangisi?"],
  explanation="return ilk eşleşmede fonksiyonu bitirir ve yalnızca 2'yi döndürür. yield n yazılırsa fonksiyon generator olur; print(list(evens(...))) [2, 4] verir.")

q(type="bug", topic="generator-tukenme", sectionId="generator-pipelines", difficulty=2,
  prompt="ortalama satırı neden ZeroDivisionError verir?",
  code=r'''
scores = (int(s) for s in "70 80 90".split())
print("toplam:", sum(scores))
print("ortalama:", sum(scores) / len(list(scores)))
''',
  answer="Generator ifadesi ilk sum ile tükendi; sonraki kullanımlar boş görür, bir listeye çevrilmeli",
  options=[
      "Generator ifadesi ilk sum ile tükendi; sonraki kullanımlar boş görür, bir listeye çevrilmeli",
      "int() dönüşümü bu satırda yeniden yapılmadığı için değerler kayboldu",
      "split() boşluklara göre bölemediği için liste boş",
      "len() generator'larla hiç kullanılamaz, bu yüzden 0 döner",
  ],
  optionFeedback={
      "int() dönüşümü bu satırda yeniden yapılmadığı için değerler kayboldu": "Dönüşüm doğru; sorun generator'ın bir kez dolaşılabilmesi.",
      "split() boşluklara göre bölemediği için liste boş": "İlk satır 240 yazdırıyor; bölme doğru çalışıyor.",
      "len() generator'larla hiç kullanılamaz, bu yüzden 0 döner": "Burada len'e generator değil list(scores) veriliyor; liste boş olduğu için 0 çıkıyor.",
  },
  hints=["İlk satır doğru toplamı yazıyor mu?", "Generator ikinci kez dolaşılabilir mi?"],
  explanation="İlk sum generator'ı tüketir. İkinci satırda sum(scores) 0, list(scores) boş liste olur ve 0 / 0 ZeroDivisionError verir. Değerleri birden çok kez kullanmak için scores = [int(s) for s in ...] yazılmalı.")

q(type="bug", topic="wrapper-args", sectionId="decorators", difficulty=2,
  prompt="add(1, 2) neden TypeError verir?",
  code=r'''
def log(func):
    def wrapper():
        print("çağrılıyor")
        return func()
    return wrapper

@log
def add(a, b):
    return a + b

print(add(1, 2))
''',
  answer="wrapper argüman almıyor; *args, **kwargs ile alıp func'a geçirmeli",
  options=[
      "wrapper argüman almıyor; *args, **kwargs ile alıp func'a geçirmeli",
      "decorator'lar argümanlı fonksiyonlara uygulanamaz",
      "@log satırı fonksiyon tanımından sonra yazılmalı",
      "wrapper içinde print kullanıldığı için sonuç kayboluyor",
  ],
  optionFeedback={
      "decorator'lar argümanlı fonksiyonlara uygulanamaz": "Uygulanabilir; sarmalayıcının argümanları kabul edip iletmesi gerekir.",
      "@log satırı fonksiyon tanımından sonra yazılmalı": "Decorator def satırının hemen üstüne yazılır.",
      "wrapper içinde print kullanıldığı için sonuç kayboluyor": "print sonucu etkilemez; hata çağrı sırasında argüman sayısından çıkıyor.",
  },
  hints=["add artık hangi fonksiyonu gösteriyor?", "add(1, 2) çağrısı wrapper'a kaç argüman veriyor?"],
  explanation="@log sonrası add, wrapper'dır. add(1, 2) wrapper'a iki argüman verir ama wrapper hiç parametre almaz: 'takes 0 positional arguments but 2 were given'. def wrapper(*args, **kwargs): return func(*args, **kwargs) yazılmalı.")

q(type="bug", topic="parantez", sectionId="decorator-params", difficulty=2,
  prompt="Bu tanım neden daha çağrı yapılmadan TypeError verir?",
  code=r'''
def log(func):
    def wrapper(*args, **kwargs):
        print("çağrılıyor")
        return func(*args, **kwargs)
    return wrapper

@log()
def work():
    return 1
''',
  answer="log parametresiz bir decorator; @log() onu func olmadan çağırıyor, @log yazılmalı",
  options=[
      "log parametresiz bir decorator; @log() onu func olmadan çağırıyor, @log yazılmalı",
      "work hiçbir argüman almadığı için dekore edilemez",
      "wrapper'da *args ve **kwargs birlikte kullanılamaz",
      "Decorator'lar yalnızca sınıf metotlarına uygulanabilir",
  ],
  optionFeedback={
      "work hiçbir argüman almadığı için dekore edilemez": "Argümansız fonksiyonlar da dekore edilebilir.",
      "wrapper'da *args ve **kwargs birlikte kullanılamaz": "İkisi birlikte kullanılır; genel sarmalayıcının standart biçimi budur.",
      "Decorator'lar yalnızca sınıf metotlarına uygulanabilir": "Decorator'lar her fonksiyona uygulanabilir.",
  },
  hints=["@ işaretinden sonraki ifade önce değerlendirilir.", "log() çağrısı log'un hangi parametresini eksik bırakıyor?"],
  explanation="@log() önce log()'u argümansız çağırır; log func parametresini beklediği için 'missing 1 required positional argument' TypeError'ı tanım anında çıkar. Parametresiz decorator @log diye yazılır; parantez yalnızca parametreli (üç katmanlı) decorator'larda kullanılır.")

q(type="bug", topic="contextmanager-finally", sectionId="contextlib", difficulty=3,
  prompt="with bloğunda hata olunca neden 'kapat' yazılmıyor?",
  code=r'''
from contextlib import contextmanager

@contextmanager
def opened(name):
    print("aç", name)
    yield name
    print("kapat", name)

try:
    with opened("rapor.txt"):
        raise ValueError("yazma hatası")
except ValueError:
    pass
''',
  answer="yield try/finally içinde değil; hata yield satırında yükselir ve sonraki temizlik satırı atlanır",
  options=[
      "yield try/finally içinde değil; hata yield satırında yükselir ve sonraki temizlik satırı atlanır",
      "@contextmanager hata olduğunda generator'ı hiç devam ettirmez, bu yüzden temizlik yazılamaz",
      "except ValueError: pass satırı 'kapat' çıktısını da siler",
      "yield bir değer döndürdüğü için fonksiyon orada biter",
  ],
  optionFeedback={
      "@contextmanager hata olduğunda generator'ı hiç devam ettirmez, bu yüzden temizlik yazılamaz": "Hatayı generator'ın içine, yield noktasına iletir; finally bloğu bu yüzden çalışabilir.",
      "except ValueError: pass satırı 'kapat' çıktısını da siler": "except yazılmış çıktıyı silmez; 'kapat' hiç yazdırılmadı.",
      "yield bir değer döndürdüğü için fonksiyon orada biter": "yield fonksiyonu bitirmez, duraklatır; hatasız durumda 'kapat' yazılırdı.",
  },
  hints=["Hatasız bir blokta 'kapat' yazılır mıydı?", "Blokta hata olunca generator'ın içinde hangi satırda hata yükselir?"],
  explanation="with bloğundaki hata generator'ın içinde, yield satırında yeniden fırlatılır; yield'den sonraki satırlar atlanır. Temizlik kesin çalışsın diye kalıp try: yield name / finally: print('kapat', name) olmalı.")

# ------------------------------------------------------------------ fill (4)
q(type="fill", topic="next", sectionId="iterator-protocol", difficulty=1,
  prompt="Iterator'dan ilk değeri alan yerleşik fonksiyonu yaz.",
  code=r'''
it = iter(["a", "b"])
first = ___(it)
print(first, list(it))
''',
  answer="next",
  expectedOutput="a ['b']",
  hints=["Iterator'dan sıradaki değeri veren yerleşik fonksiyon.", "for döngüsü de her turda bunu çağırır."],
  explanation="next(it) iterator'dan sıradaki değeri alır; list(it) yalnızca kalanı toplar.")

q(type="fill", topic="yield", sectionId="generators", difficulty=1,
  prompt="Fonksiyonu, kareleri birer birer üreten bir generator yapan anahtar sözcüğü yaz.",
  code=r'''
def squares(limit):
    for n in range(limit):
        ___ n * n

print(list(squares(4)))
''',
  answer="yield",
  expectedOutput="[0, 1, 4, 9]",
  hints=["return bir kez döner; burada her turda bir değer gerekiyor.", "Değeri verip fonksiyonu duraklatan sözcük."],
  explanation="yield her turda bir değer üretir ve fonksiyonu duraklatır; list() bütün değerleri toplar.")

q(type="fill", topic="wraps", sectionId="decorators", difficulty=2,
  prompt="Sarmalayıcının asıl fonksiyonun adını ve belgesini korumasını sağlayan decorator'ı yaz.",
  code=r'''
from functools import wraps

def keep(func):
    @___(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@keep
def report():
    """Rapor."""

print(report.__name__, report.__doc__)
''',
  answer="wraps",
  expectedOutput="report Rapor.",
  hints=["functools'tan içe aktarılan ad.", "Asıl fonksiyonu argüman olarak alır."],
  explanation="@wraps(func), __name__, __doc__ gibi bilgileri wrapper'a kopyalar; bu yüzden report adını ve belgesini korur.")

q(type="fill", topic="exit", sectionId="context-manager-class", difficulty=2,
  prompt="with bloğundan çıkarken çağrılan özel metodun adını yaz.",
  code=r'''
class Door:
    def __enter__(self):
        print("açıldı")
        return self

    def ___(self, exc_type, exc, tb):
        print("kapandı")

with Door():
    print("içeride")
''',
  answer="__exit__",
  expectedOutput="açıldı\niçeride\nkapandı",
  hints=["Girişte __enter__ çağrılır; çıkışta?", "Üç hata parametresi alır."],
  explanation="with bloğu bitince __exit__ çağrılır; blokta hata olsaydı türü, nesnesi ve traceback'i bu parametrelere gelirdi.")

# ------------------------------------------------------------------ order (4)
q(type="order", topic="iter-generator", sectionId="custom-iterator", difficulty=2,
  prompt="__iter__'i generator olan bir sınıfla çift sayıları listeleyen sırayı kur.",
  answer_lines=[
      "class Evens:",
      "    def __init__(self, limit):",
      "        self.limit = limit",
      "    def __iter__(self):",
      "        for n in range(0, self.limit, 2):",
      "            yield n",
      "print(list(Evens(7)))",
  ],
  perm=[4, 6, 1, 5, 0, 3, 2],
  expectedOutput="[0, 2, 4, 6]",
  hints=["__iter__ içindeki for döngüsünün gövdesinde yield olmalı.", "Nesne, sınıf tanımlandıktan sonra kullanılır."],
  explanation="Evens'in __iter__'i bir generator'dır; her dolaşmada yeni bir generator döner ve 0'dan 7'ye kadar çift sayıları üretir.")

q(type="order", topic="boru-hatti", sectionId="generator-pipelines", difficulty=2,
  prompt="Yalnızca rakamlardan oluşan satırları toplayan tembel boru hattını kur.",
  answer_lines=[
      'lines = ["3", "x", "5"]',
      "digits = (line for line in lines if line.isdigit())",
      "numbers = (int(d) for d in digits)",
      "print(sum(numbers))",
  ],
  perm=[3, 1, 2, 0],
  expectedOutput="8",
  hints=["Her adım bir öncekinin generator'ını kullanır.", "En son tüketici sum'dır."],
  explanation="digits rakam olmayan satırı süzer, numbers kalanları sayıya çevirir; sum değerleri çektikçe zincir çalışır: 3 + 5 = 8.")

q(type="order", topic="parametreli", sectionId="decorator-params", difficulty=3,
  prompt="Parametreli bir decorator tanımlayıp kullanan sırayı kur.",
  answer_lines=[
      "def prefix(text):",
      "    def decorator(func):",
      "        def wrapper(name):",
      "            return text + func(name)",
      "        return wrapper",
      "    return decorator",
      '@prefix("Sn. ")',
      "def title(name):",
      "    return name.title()",
      'print(title("ada"))',
  ],
  perm=[6, 2, 9, 4, 0, 8, 3, 5, 1, 7],
  expectedOutput="Sn. Ada",
  hints=["Üç katman: parametre → decorator → wrapper.", "Her katman bir içteki fonksiyonu return eder; return satırlarının girintisine dikkat."],
  explanation="prefix('Sn. ') decorator'ı döndürür, decorator title'ı wrapper ile değiştirir; wrapper önek ekleyerek sonucu döndürür.")

q(type="order", topic="contextmanager", sectionId="contextlib", difficulty=2,
  prompt="@contextmanager ile bir bölümün başını ve sonunu yazan sırayı kur.",
  answer_lines=[
      "from contextlib import contextmanager",
      "@contextmanager",
      "def section(name):",
      '    print("başla", name)',
      "    yield",
      '    print("bitir", name)',
      'with section("rapor"):',
      '    print("yazılıyor")',
  ],
  perm=[5, 6, 0, 3, 7, 2, 4, 1],
  expectedOutput="başla rapor\nyazılıyor\nbitir rapor",
  hints=["yield, with bloğunun çalıştığı noktadır.", "Decorator, def satırının hemen üstündedir."],
  explanation="yield'den önceki satır girişte, with bloğu yield noktasında, yield'den sonraki satır çıkışta çalışır.")

# ------------------------------------------------------------------ code (10)
q(type="code", topic="next-baslik", sectionId="iterator-protocol", difficulty=1,
  prompt="İlk satır N, ardından N satır gelir; ilk satır başlıktır. Satırlardan bir iterator kur, next ile başlığı al (satır yoksa varsayılan None), kalan satırları say. Çıktı: 'başlık: X | kayıt: K'; hiç satır yoksa 'boş'.",
  starterCode=r'''
lines = iter([input() for _ in range(int(input()))])
# next ile başlığı al (satır yoksa None)
header = None
''',
  answer=r'''
lines = iter([input() for _ in range(int(input()))])
header = next(lines, None)
if header is None:
    print("boş")
else:
    print(f"başlık: {header} | kayıt: {sum(1 for _ in lines)}")
''',
  exampleInput="3\nad,puan\nAda,90\nCan,75",
  expectedOutput="başlık: ad,puan | kayıt: 2",
  tests=[
      {"label": "Normal", "stdin": "3\nad,puan\nAda,90\nCan,75", "expectedOutput": "başlık: ad,puan | kayıt: 2"},
      {"label": "Yalnız başlık", "stdin": "1\nad,puan", "expectedOutput": "başlık: ad,puan | kayıt: 0"},
      {"label": "Hiç satır yok", "stdin": "0", "expectedOutput": "boş"},
      {"label": "Tek kayıt", "stdin": "2\nx\ny", "expectedOutput": "başlık: x | kayıt: 1"},
  ],
  hints=["next(lines, None) boş iterator'da hata yerine None verir.", "Kalanları saymak için sum(1 for _ in lines) ya da len(list(lines)) kullanılabilir."],
  explanation="next başlığı tüketir; aynı iterator'ın kalanı yalnızca kayıtları içerir. Varsayılan değer boş girdide StopIteration'ı önler.")

q(type="code", topic="kendi-iterable", sectionId="custom-iterator", difficulty=2,
  prompt="Cycle(items, rounds) sınıfının __iter__'ini generator olarak yaz: öğeleri sırayla rounds tur boyunca üretsin. Nesne tekrar dolaşılabilir olmalı. Program öğeleri ve tur sayısını okur, listeyi yazar ve ikinci dolaşmanın aynı sonucu verdiğini gösterir.",
  starterCode=r'''
class Cycle:
    def __init__(self, items, rounds):
        self.items = items
        self.rounds = rounds

    def __iter__(self):
        # her tur için öğeleri sırayla yield et
        return iter([])

cycle = Cycle(input().split(), int(input()))
print(list(cycle))
print("tekrar:", list(cycle) == list(cycle))
''',
  answer=r'''
class Cycle:
    def __init__(self, items, rounds):
        self.items = items
        self.rounds = rounds

    def __iter__(self):
        for _ in range(self.rounds):
            yield from self.items

cycle = Cycle(input().split(), int(input()))
print(list(cycle))
print("tekrar:", list(cycle) == list(cycle))
''',
  exampleInput="a b\n2",
  expectedOutput="['a', 'b', 'a', 'b']\ntekrar: True",
  tests=[
      {"label": "İki tur", "stdin": "a b\n2", "expectedOutput": "['a', 'b', 'a', 'b']\ntekrar: True"},
      {"label": "Tek tur", "stdin": "x y z\n1", "expectedOutput": "['x', 'y', 'z']\ntekrar: True"},
      {"label": "Sıfır tur", "stdin": "a\n0", "expectedOutput": "[]\ntekrar: True"},
      {"label": "Tek öğe, üç tur", "stdin": "k\n3", "expectedOutput": "['k', 'k', 'k']\ntekrar: True"},
  ],
  hints=["__iter__ içinde for _ in range(self.rounds) döngüsü kur.", "Her turda öğeleri yield from self.items ile ver."],
  explanation="__iter__ gövdesinde yield olduğu için her list() çağrısı yeni bir generator alır; nesne tekrar tekrar aynı sonucu verir.")

q(type="code", topic="chunks", sectionId="generators", difficulty=2,
  prompt="chunks(items, size) generator'ını yaz: listeyi size uzunluğunda parçalar hâlinde üretsin, son parça kısa olabilir. Program öğeleri ve boyutu okur, her parçayı '|' ile birleştirip ayrı satıra yazar ve sonda 'parça: N' gösterir.",
  starterCode=r'''
def chunks(items, size):
    # size uzunluğunda parçaları yield et
    return []

items = input().split()
size = int(input())
count = 0
for part in chunks(items, size):
    print("|".join(part))
    count += 1
print("parça:", count)
''',
  answer=r'''
def chunks(items, size):
    for start in range(0, len(items), size):
        yield items[start:start + size]

items = input().split()
size = int(input())
count = 0
for part in chunks(items, size):
    print("|".join(part))
    count += 1
print("parça:", count)
''',
  exampleInput="a b c d e\n2",
  expectedOutput="a|b\nc|d\ne\nparça: 3",
  tests=[
      {"label": "Kısa son parça", "stdin": "a b c d e\n2", "expectedOutput": "a|b\nc|d\ne\nparça: 3"},
      {"label": "Tam bölünür", "stdin": "1 2 3 4\n2", "expectedOutput": "1|2\n3|4\nparça: 2"},
      {"label": "Boyut büyük", "stdin": "x y\n5", "expectedOutput": "x|y\nparça: 1"},
      {"label": "Boyut 1", "stdin": "p q r\n1", "expectedOutput": "p\nq\nr\nparça: 3"},
  ],
  hints=["range(0, len(items), size) parçaların başlangıç indekslerini verir.", "Her başlangıç için items[start:start + size] dilimini yield et."],
  explanation="Generator her parçayı istendiğinde üretir; dilimleme son parçanın kısa olmasını kendiliğinden halleder.")

q(type="code", topic="sonsuz", sectionId="generator-pipelines", difficulty=3,
  prompt="fibonacci() adında sonsuz bir generator yaz (0, 1, 1, 2, 3, 5, ...). Program n ve bir sınır okur; itertools.islice ile ilk n değeri yazar, sonra sınırdan büyük ilk Fibonacci sayısını yazar.",
  starterCode=r'''
from itertools import islice

def fibonacci():
    # 0, 1, 1, 2, 3, 5, ... sonsuza kadar yield et
    yield 0

n = int(input())
limit = int(input())
print(list(islice(fibonacci(), n)))
print("ilk büyük:", next(x for x in fibonacci() if x > limit))
''',
  answer=r'''
from itertools import islice

def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

n = int(input())
limit = int(input())
print(list(islice(fibonacci(), n)))
print("ilk büyük:", next(x for x in fibonacci() if x > limit))
''',
  exampleInput="7\n10",
  expectedOutput="[0, 1, 1, 2, 3, 5, 8]\nilk büyük: 13",
  tests=[
      {"label": "Normal", "stdin": "7\n10", "expectedOutput": "[0, 1, 1, 2, 3, 5, 8]\nilk büyük: 13"},
      {"label": "Hiç değer", "stdin": "0\n0", "expectedOutput": "[]\nilk büyük: 1"},
      {"label": "Büyük sınır", "stdin": "3\n1000", "expectedOutput": "[0, 1, 1]\nilk büyük: 1597"},
      {"label": "Sınır bir Fibonacci", "stdin": "2\n21", "expectedOutput": "[0, 1]\nilk büyük: 34"},
  ],
  hints=["İki değişkenle başla: a, b = 0, 1; while True içinde a'yı yield et.", "Sonra a, b = b, a + b ile ilerle; generator sonsuz olduğu için yalnızca islice ve next ile tüket."],
  explanation="Sonsuz generator değerleri yalnızca istendikçe üretir; islice ilk n değeri, next ise koşulu sağlayan ilk değeri alıp durur.")

q(type="code", topic="boru-hatti", sectionId="generator-pipelines", difficulty=2,
  prompt="parse(lines) generator'ı her 'DÜZEY mesaj' satırını (düzey, mesaj) çiftine ayırsın; only(level, records) yalnızca o düzeydeki mesajları üretsin. Program satırları ve aranan düzeyi okur, tekrarlananları atlayarak mesajları ilk görülme sırasıyla numaralandırır; hiç yoksa 'kayıt yok' yazar.",
  starterCode=r'''
def parse(lines):
    # her satırı (düzey, mesaj) olarak yield et
    return []

def only(level, records):
    # yalnızca istenen düzeydeki mesajları yield et
    return []

lines = [input() for _ in range(int(input()))]
level = input()
seen = []
for message in only(level, parse(lines)):
    if message not in seen:
        seen.append(message)
for number, message in enumerate(seen, start=1):
    print(f"{number}. {message}")
if not seen:
    print("kayıt yok")
''',
  answer=r'''
def parse(lines):
    for line in lines:
        level, message = line.split(" ", 1)
        yield level, message

def only(level, records):
    for record_level, message in records:
        if record_level == level:
            yield message

lines = [input() for _ in range(int(input()))]
level = input()
seen = []
for message in only(level, parse(lines)):
    if message not in seen:
        seen.append(message)
for number, message in enumerate(seen, start=1):
    print(f"{number}. {message}")
if not seen:
    print("kayıt yok")
''',
  exampleInput="4\nERROR disk dolu\nINFO başladı\nERROR ağ yok\nERROR disk dolu\nERROR",
  expectedOutput="1. disk dolu\n2. ağ yok",
  tests=[
      {"label": "Tekrar atlanır", "stdin": "4\nERROR disk dolu\nINFO başladı\nERROR ağ yok\nERROR disk dolu\nERROR", "expectedOutput": "1. disk dolu\n2. ağ yok"},
      {"label": "Başka düzey", "stdin": "3\nINFO a b\nERROR c\nINFO d\nINFO", "expectedOutput": "1. a b\n2. d"},
      {"label": "Eşleşme yok", "stdin": "1\nINFO tamam\nERROR", "expectedOutput": "kayıt yok"},
      {"label": "Satır yok", "stdin": "0\nERROR", "expectedOutput": "kayıt yok"},
  ],
  hints=["line.split(' ', 1) yalnızca ilk boşluktan böler; mesajdaki boşluklar korunur.", "only içinde for düzey, mesaj in records ile dolaş ve eşleşeni yield et."],
  explanation="İki küçük generator bir boru hattı kurar; ara liste oluşmaz. Tekrar denetimi ise sırayı korumak için bir listeyle yapılır.")

q(type="code", topic="generator-filtre", sectionId="generators", difficulty=2,
  prompt="read_numbers(lines) generator'ını yaz: boş satırları ve '#' ile başlayan yorumları atlasın, tam sayıya çevrilebilen satırları int olarak üretsin, çevrilemeyenleri sessizce atlasın. Program toplamı ve geçerli sayı adedini yazar.",
  starterCode=r'''
def read_numbers(lines):
    # boş ve yorum satırlarını atla, geçerli tam sayıları yield et
    return []

lines = [input() for _ in range(int(input()))]
values = list(read_numbers(lines))
print("toplam:", sum(values), "| adet:", len(values))
''',
  answer=r'''
def read_numbers(lines):
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        try:
            yield int(line)
        except ValueError:
            continue

lines = [input() for _ in range(int(input()))]
values = list(read_numbers(lines))
print("toplam:", sum(values), "| adet:", len(values))
''',
  exampleInput="5\n# başlık\n10\n\nabc\n-3",
  expectedOutput="toplam: 7 | adet: 2",
  tests=[
      {"label": "Karışık", "stdin": "5\n# başlık\n10\n\nabc\n-3", "expectedOutput": "toplam: 7 | adet: 2"},
      {"label": "Boşluklu sayı", "stdin": "2\n  5  \n#7", "expectedOutput": "toplam: 5 | adet: 1"},
      {"label": "Hiç geçerli yok", "stdin": "2\nx\n# y", "expectedOutput": "toplam: 0 | adet: 0"},
      {"label": "Ondalık atlanır", "stdin": "3\n1.5\n2\n3", "expectedOutput": "toplam: 5 | adet: 2"},
  ],
  hints=["Satırı strip() ile temizle; boşsa ya da '#' ile başlıyorsa continue.", "int(line)'ı try içinde yield et; ValueError'da atla."],
  explanation="Generator yalnızca geçerli değerleri üretir; temizlik ve doğrulama tek yerde durur, çağıran kod yalnızca sayılarla ilgilenir.")

q(type="code", topic="decorator", sectionId="decorators", difficulty=2,
  prompt="count_calls decorator'ını yaz: sarmalayıcı her çağrıda kendi calls özniteliğini artırsın, asıl fonksiyonun sonucunu döndürsün ve @wraps ile adını korusun. Program sayıları okuyup dekore edilmiş square'i her biri için çağırır.",
  starterCode=r'''
from functools import wraps

def count_calls(func):
    # wrapper yaz: calls'u artır, func'ın sonucunu döndür; @wraps(func) kullan
    return func

@count_calls
def square(n):
    return n * n

numbers = [int(x) for x in input().split()]
print([square(n) for n in numbers])
print("çağrı:", square.calls, "| ad:", square.__name__)
''',
  answer=r'''
from functools import wraps

def count_calls(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.calls += 1
        return func(*args, **kwargs)
    wrapper.calls = 0
    return wrapper

@count_calls
def square(n):
    return n * n

numbers = [int(x) for x in input().split()]
print([square(n) for n in numbers])
print("çağrı:", square.calls, "| ad:", square.__name__)
''',
  exampleInput="2 3 4",
  expectedOutput="[4, 9, 16]\nçağrı: 3 | ad: square",
  tests=[
      {"label": "Üç çağrı", "stdin": "2 3 4", "expectedOutput": "[4, 9, 16]\nçağrı: 3 | ad: square"},
      {"label": "Tek çağrı", "stdin": "-5", "expectedOutput": "[25]\nçağrı: 1 | ad: square"},
      {"label": "Tekrarlanan değer", "stdin": "1 1 1 1", "expectedOutput": "[1, 1, 1, 1]\nçağrı: 4 | ad: square"},
  ],
  hints=["Sayaç için wrapper.calls = 0 ataması wrapper tanımından sonra, return'den önce yapılır.", "wrapper içinde wrapper.calls += 1 ve return func(*args, **kwargs)."],
  explanation="Fonksiyonlar nesne olduğu için sarmalayıcıya öznitelik eklenebilir. wraps, adı square olarak korur; sonucu döndürmeyi unutmak listeyi None'larla doldururdu.")

q(type="code", topic="parametreli", sectionId="decorator-params", difficulty=3,
  prompt="in_range(low, high) adında parametreli bir decorator yaz: dekore edilen fonksiyonun bütün konumsal argümanları [low, high] aralığında değilse ValueError(f'{değer} aralık dışında') fırlatsın, değilse fonksiyonun sonucunu döndürsün. Program iki not okur ve ortalamayı ya da hatayı yazar.",
  starterCode=r'''
from functools import wraps

def in_range(low, high):
    # üç katman: parametreler → decorator → wrapper
    pass

@in_range(0, 100)
def average(a, b):
    return (a + b) / 2

try:
    print(average(int(input()), int(input())))
except ValueError as error:
    print("hata:", error)
''',
  answer=r'''
from functools import wraps

def in_range(low, high):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for value in args:
                if not low <= value <= high:
                    raise ValueError(f"{value} aralık dışında")
            return func(*args, **kwargs)
        return wrapper
    return decorator

@in_range(0, 100)
def average(a, b):
    return (a + b) / 2

try:
    print(average(int(input()), int(input())))
except ValueError as error:
    print("hata:", error)
''',
  exampleInput="80\n90",
  expectedOutput="85.0",
  tests=[
      {"label": "Geçerli", "stdin": "80\n90", "expectedOutput": "85.0"},
      {"label": "Üst sınır dışı", "stdin": "80\n120", "expectedOutput": "hata: 120 aralık dışında"},
      {"label": "Alt sınır dışı", "stdin": "-1\n50", "expectedOutput": "hata: -1 aralık dışında"},
      {"label": "Sınırlar dahil", "stdin": "0\n100", "expectedOutput": "50.0"},
  ],
  hints=["in_range bir decorator döndürmeli, decorator bir wrapper döndürmeli.", "wrapper içinde for value in args ile her argümanı low <= value <= high diye denetle."],
  explanation="@in_range(0, 100) önce in_range'i çağırır ve dönen decorator average'a uygulanır. wrapper argümanları denetleyip ancak geçerliyse asıl fonksiyonu çağırır.")

q(type="code", topic="context-manager", sectionId="context-manager-class", difficulty=2,
  prompt="Ledger context manager sınıfını yaz: __enter__ boş bir liste döndürsün (kayıtlar buna eklenecek); __exit__ hata yoksa 'toplam: X' yazsın, ValueError olursa 'iptal: mesaj' yazıp hatayı yutsun (True), başka hataları yutmasın. Program tutarları okur, negatif tutarda ValueError fırlatır ve sonda 'devam' yazar.",
  starterCode=r'''
class Ledger:
    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc, tb):
        pass

amounts = [int(x) for x in input().split()]
with Ledger() as entries:
    for amount in amounts:
        if amount < 0:
            raise ValueError(f"negatif tutar: {amount}")
        entries.append(amount)
print("devam")
''',
  answer=r'''
class Ledger:
    def __enter__(self):
        self.entries = []
        return self.entries

    def __exit__(self, exc_type, exc, tb):
        if exc_type is None:
            print("toplam:", sum(self.entries))
            return False
        if issubclass(exc_type, ValueError):
            print("iptal:", exc)
            return True
        return False

amounts = [int(x) for x in input().split()]
with Ledger() as entries:
    for amount in amounts:
        if amount < 0:
            raise ValueError(f"negatif tutar: {amount}")
        entries.append(amount)
print("devam")
''',
  exampleInput="10 20 30",
  expectedOutput="toplam: 60\ndevam",
  tests=[
      {"label": "Hatasız", "stdin": "10 20 30", "expectedOutput": "toplam: 60\ndevam"},
      {"label": "Negatif tutar", "stdin": "10 -5 30", "expectedOutput": "iptal: negatif tutar: -5\ndevam"},
      {"label": "Tek tutar", "stdin": "0", "expectedOutput": "toplam: 0\ndevam"},
      {"label": "İlk tutar negatif", "stdin": "-1", "expectedOutput": "iptal: negatif tutar: -1\ndevam"},
  ],
  hints=["__enter__ listeyi self'e kaydedip döndürmeli; __exit__ toplamı oradan hesaplar.", "exc_type None ise hata yoktur; issubclass(exc_type, ValueError) ise yut (True döndür)."],
  explanation="__enter__'in dönüşü as entries'e bağlanır. __exit__ her durumda çalışır; yalnızca beklenen ValueError'ı yutar, diğer hataları yükselmeye bırakır.")

q(type="code", topic="contextmanager", sectionId="contextlib", difficulty=3,
  prompt="@contextmanager ile changed(store, key, value) yaz: anahtarı geçici olarak value yapsın; blok bitince (hata olsa bile) eski değeri geri koysun, anahtar önceden yoksa silsin. Program sözlüğü ve geçici değişikliği okur, blok içinde ve sonrasında sözlüğü yazar; 'hata' girdisinde blok içinde RuntimeError fırlatılır.",
  starterCode=r'''
from contextlib import contextmanager

@contextmanager
def changed(store, key, value):
    # eski durumu sakla, değeri koy, yield et; finally ile geri yükle
    yield

store = dict(pair.split("=") for pair in input().split())
key, value = input().split("=")
mode = input()
try:
    with changed(store, key, value):
        print("içeride:", sorted(store.items()))
        if mode == "hata":
            raise RuntimeError("blok hatası")
except RuntimeError as error:
    print("yakalandı:", error)
print("sonra:", sorted(store.items()))
''',
  answer=r'''
from contextlib import contextmanager

@contextmanager
def changed(store, key, value):
    missing = key not in store
    old = store.get(key)
    store[key] = value
    try:
        yield
    finally:
        if missing:
            del store[key]
        else:
            store[key] = old

store = dict(pair.split("=") for pair in input().split())
key, value = input().split("=")
mode = input()
try:
    with changed(store, key, value):
        print("içeride:", sorted(store.items()))
        if mode == "hata":
            raise RuntimeError("blok hatası")
except RuntimeError as error:
    print("yakalandı:", error)
print("sonra:", sorted(store.items()))
''',
  exampleInput="debug=0 port=80\ndebug=1\nnormal",
  expectedOutput="içeride: [('debug', '1'), ('port', '80')]\nsonra: [('debug', '0'), ('port', '80')]",
  tests=[
      {"label": "Var olan anahtar", "stdin": "debug=0 port=80\ndebug=1\nnormal", "expectedOutput": "içeride: [('debug', '1'), ('port', '80')]\nsonra: [('debug', '0'), ('port', '80')]"},
      {"label": "Yeni anahtar silinir", "stdin": "port=80\nmode=test\nnormal", "expectedOutput": "içeride: [('mode', 'test'), ('port', '80')]\nsonra: [('port', '80')]"},
      {"label": "Hata olsa da geri alınır", "stdin": "debug=0\ndebug=1\nhata", "expectedOutput": "içeride: [('debug', '1')]\nyakalandı: blok hatası\nsonra: [('debug', '0')]"},
      {"label": "Hata ve yeni anahtar", "stdin": "a=1\nb=2\nhata", "expectedOutput": "içeride: [('a', '1'), ('b', '2')]\nyakalandı: blok hatası\nsonra: [('a', '1')]"},
  ],
  hints=["Önce anahtarın var olup olmadığını ve eski değerini sakla.", "yield'i try/finally içine al; finally'de anahtar önceden yoksa del, varsa eski değeri geri koy."],
  explanation="try/finally sayesinde blokta hata olsa da geri yükleme çalışır; hata ise yutulmadan dışarı çıkar ve çağıran onu yakalar.")

# ------------------------------------------------------------------ traceback (4)
q(type="traceback", topic="stopiteration", sectionId="iterator-protocol", difficulty=1,
  prompt="Tükenmiş bir iterator'dan bir değer daha isteniyor. Hangi hata oluşur?",
  code=r'''
it = iter([1])
next(it)
next(it)
''',
  expectedError="StopIteration",
  options=["StopIteration", "IndexError", "ValueError", "TypeError"],
  optionFeedback={
      "IndexError": "İndeksle erişim yok; iterator'ın sonuna gelindiğini StopIteration bildirir.",
      "ValueError": "Değer geçersiz değil; değer kalmadı.",
      "TypeError": "it bir iterator olduğu için next ile kullanılabilir.",
  },
  hints=["Listede kaç öğe var, kaç next çağrılıyor?", "for döngüsünün bitişi anlamak için yakaladığı hata."],
  explanation="İkinci next'te değer kalmadığı için StopIteration fırlatılır. for döngüsü bunu sessizce yakalar; elle next çağırırken sen yakalamalı ya da next(it, varsayılan) kullanmalısın.")

q(type="traceback", topic="generator-len", sectionId="generator-pipelines", difficulty=2,
  prompt="Bir generator ifadesinin uzunluğu soruluyor. Hangi hata oluşur?",
  code=r'''
squares = (n * n for n in range(5))
print(len(squares))
''',
  expectedError="TypeError",
  options=["TypeError", "AttributeError", "StopIteration", "ValueError"],
  optionFeedback={
      "AttributeError": "Bir öznitelik aranmıyor; len desteklenmeyen bir türe uygulanıyor.",
      "StopIteration": "Generator henüz hiç dolaşılmadı; hata len çağrısından geliyor.",
      "ValueError": "Değerle ilgili bir sorun yok; tür len'i desteklemiyor.",
  },
  hints=["Generator değerlerini önceden bilir mi?", "len hangi metodu arar?"],
  explanation="Generator değerleri istendikçe ürettiği için uzunluğunu bilmez ve __len__ tanımlamaz: TypeError: object of type 'generator' has no len(). Uzunluk için önce listeye çevir ya da sum(1 for _ in ...) ile say.")

q(type="traceback", topic="decorator-return", sectionId="decorators", difficulty=2,
  prompt="Decorator sarmalayıcıyı döndürmeyi unutuyor. greet() çağrısında hangi hata oluşur?",
  code=r'''
def log(func):
    def wrapper(*args, **kwargs):
        print("çağrılıyor")
        return func(*args, **kwargs)

@log
def greet():
    return "selam"

greet()
''',
  expectedError="TypeError",
  options=["TypeError", "NameError", "AttributeError", "RecursionError"],
  optionFeedback={
      "NameError": "greet adı tanımlı; ama None'a bağlı.",
      "AttributeError": "Öznitelik aranmıyor; None çağrılmaya çalışılıyor.",
      "RecursionError": "Fonksiyon kendini çağırmıyor.",
  },
  hints=["log fonksiyonu ne döndürüyor?", "@log, greet = log(greet) demektir."],
  explanation="log return wrapper yazmadığı için None döndürür ve greet None'a bağlanır. greet() çağrısı TypeError: 'NoneType' object is not callable verir.")

q(type="traceback", topic="with-protokol", sectionId="context-manager-class", difficulty=2,
  prompt="__enter__ ve __exit__ olmayan bir nesne with ile kullanılıyor. Hangi hata oluşur?",
  code=r'''
class Plain:
    pass

with Plain() as p:
    print("içeride")
''',
  expectedError="TypeError",
  options=["TypeError", "NameError", "ValueError", "StopIteration"],
  optionFeedback={
      "NameError": "Plain tanımlı; sorun nesnenin with protokolünü desteklememesi.",
      "ValueError": "Değerle ilgili bir sorun yok.",
      "StopIteration": "Yineleme yok; with farklı bir protokol kullanır.",
  },
  hints=["with hangi iki özel metodu arar?", "Python 3.11 ve sonrasında bu durum hangi hata türüyle bildirilir?"],
  explanation="with, nesnenin __enter__ ve __exit__ metotlarını arar. Python 3.11'den beri bunlar yoksa TypeError: 'Plain' object does not support the context manager protocol verilir (önceki sürümlerde AttributeError).")
