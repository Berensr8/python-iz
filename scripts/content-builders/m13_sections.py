"""M13 (İleri yapılar) lesson sections. Imported by build_m13.py."""

TUTORIAL = "https://docs.python.org/3.12/tutorial/classes.html"


def c(text):
    return text.strip("\n")


sections = []


def section(**fields):
    for key in ("code", "expectedOutput", "realCode", "realOutput"):
        fields[key] = c(fields[key])
    fields["runtime"] = "browser"
    sections.append(fields)


section(
    id="iterator-protocol",
    title="Iterable, iterator ve for'un arkası",
    eyebrow="for döngüsü aslında ne yapıyor?",
    objectives=[
        "iterable (iter() ile iterator veren) ile iterator (next() ile sıradaki değeri veren) arasındaki farkı açıklar ve for döngüsünün iter/next/StopIteration ile nasıl çalıştığını gösterir.",
        "Iterator'ın tek yönlü ve tek kullanımlık olduğunu, map, zip, enumerate ve dosyaların iterator döndürdüğünü bilir; next(it, varsayılan) kullanır.",
    ],
    prerequisites=["m3:for-range", "m3:enumerate-zip", "m12:dunder-basics"],
    summary="Liste gibi yinelenebilir (iterable) bir nesneden iter() ile bir iterator alınır; next() her çağrıda sıradaki değeri verir, değer kalmayınca StopIteration fırlatır. for döngüsü bunu senin yerine yapar. Iterator tükenince yeniden başlamaz.",
    explanation=(
        "for x in nesne: yazınca Python önce iter(nesne) ile bir iterator alır, sonra her turda next(iterator) çağırır ve StopIteration gelince döngüyü sessizce bitirir. İki kavram var: iterable, iter() verilebilen her şeydir (list, str, dict, set, range, dosya); iterator ise next() ile sıradaki değeri veren nesnedir ve iter(iterator) kendisini döndürür. "
        "Liste bir iterable'dır, iterator değildir: her for döngüsü listeden yeni bir iterator alır, bu yüzden liste tekrar tekrar dolaşılabilir. Iterator ise tek yönlü ve tek kullanımlıktır: ilerledikçe tükenir, geri sarılmaz. next ile ilk değeri aldıktan sonra kalanını for ile gezebilir ya da list() ile toplayabilirsin; bir kez tükenen iterator ikinci list() çağrısında boş liste verir. "
        "map, filter, zip, enumerate, reversed ve açık dosya nesneleri iterator döndürür; sonucu iki kez kullanmak istiyorsan list() ile bir kez listeye çevir. Bir başlık satırını atlamak için next(satırlar) kullanmak yaygındır; iterator boş olabilecekse next(it, varsayılan) StopIteration yerine varsayılanı döndürür. "
        "Bunun yararı tembelliktir: iterator değerleri ancak istendiğinde üretir. Milyonlarca satırlık bir dosyayı satır satır dolaşmak belleğe tamamını almayı gerektirmez. Kendi iterable sınıflarını ve generator'ları sonraki bölümlerde bu protokol üzerine kuracaksın."
    ),
    code=r'''
numbers = [10, 20, 30]
it = iter(numbers)
print(type(it).__name__)
print(next(it), next(it))
for value in it:
    print("döngüde:", value)
print(list(it))
try:
    next(it)
except StopIteration:
    print("StopIteration")

words = iter(["a", "b"])
print(list(words), list(words))
print(iter(numbers) is iter(numbers), iter(it) is it)
''',
    expectedOutput=r'''
list_iterator
10 20
döngüde: 30
[]
StopIteration
['a', 'b'] []
False True
''',
    why="İki next çağrısı ilk iki değeri tüketti; for döngüsü aynı iterator'dan yalnızca kalan 30'u aldı ve sonra iterator boştu. Liste tükenmez: iter(numbers) her çağrıda yeni bir iterator üretir (False). Iterator'dan yeniden iterator istemek ise aynı nesneyi verir (True); bu yüzden iterator ikinci kez baştan başlamaz.",
    alternatives=[
        "Değerleri birden çok kez kullanacaksan iterator'ı bir kez list() ile listeye çevir.",
        "Yalnızca ilk öğeye ihtiyacın varsa next(iter(nesne), varsayılan) ile bütün diziyi dolaşmadan al.",
    ],
    traps=[
        "map, zip ya da filter sonucunu iki kez dolaşmaya çalışmak: ikinci dolaşma boş gelir.",
        "Boş olabilecek bir iterator'da varsayılansız next çağırmak (StopIteration).",
        "Listeyi iterator sanıp next(liste) yazmak (TypeError: 'list' object is not an iterator).",
        "Bir iterator'ı for ile dolaşırken aynı iterator'dan next ile de değer çekip öğe atlamak.",
    ],
    realCode=r'''
lines = iter(["ad,puan", "Ada,90", "Can,75"])
header = next(lines).split(",")
rows = [dict(zip(header, line.split(","))) for line in lines]
print(header, rows)
pairs = zip([1, 2, 3], "ab")
print(list(pairs), list(pairs))
print(next(iter([]), "boş"))
''',
    realOutput=r'''
['ad', 'puan'] [{'ad': 'Ada', 'puan': '90'}, {'ad': 'Can', 'puan': '75'}]
[(1, 'a'), (2, 'b')] []
boş
''',
    lineByLine=[
        "next(lines) başlık satırını alır; liste kurucu aynı iterator'dan yalnızca kalan satırları gezer.",
        "zip başlıkla değerleri eşleyip her satırı sözlüğe çevirir.",
        "zip bir iterator döndürür ve en kısa girdide durur; ikinci list() boş gelir.",
        "Boş bir iterator'da next'in ikinci argümanı StopIteration yerine varsayılan değeri döndürür.",
    ],
    sources=[
        {"title": "Python 3.12 · Iterator'lar", "url": TUTORIAL + "#iterators"},
        {"title": "Python sözlüğü · iterator", "url": "https://docs.python.org/3.12/glossary.html#term-iterator"},
    ],
)

section(
    id="custom-iterator",
    title="Kendi iterable sınıfın",
    eyebrow="for döngüsüyle dolaşılabilen nesneler kur",
    objectives=[
        "__iter__ ve __next__ ile kendi iterator sınıfını yazar ve değer bitince StopIteration fırlatır.",
        "Kendisi iterator olan (tek kullanımlık) bir sınıf ile her __iter__ çağrısında yeni bir iterator veren (tekrar kullanılabilir) iterable'ı ayırır; __iter__'i generator olarak yazar.",
    ],
    prerequisites=["iterator-protocol", "m12:dunder-basics"],
    summary="Bir sınıfa __iter__ yazarsan nesnesi for, list, sum ve in ile kullanılabilir. __iter__ self döndürüp __next__ yazan sınıf tek kullanımlıktır; her çağrıda yeni bir iterator (ya da generator) döndüren __iter__ ise tekrar tekrar dolaşılabilir.",
    explanation=(
        "Kendi sınıfını yinelenebilir yapmak için __iter__ yazarsın; Python for döngüsünde onu çağırır. İki yol var. Birincisi sınıfın kendisinin iterator olmasıdır: __iter__ self döndürür, __next__ her çağrıda sıradaki değeri verir ve değer kalmayınca raise StopIteration yazar. Bu nesne tek kullanımlıktır: durumu (self.current) nesnenin içinde ilerlediği için ikinci for döngüsünde hiçbir şey vermez. "
        "İkincisi iterable ile iterator'ı ayırmaktır: __iter__ her çağrıldığında yeni bir iterator nesnesi döndürür. Listenin davranışı budur; aynı nesne istendiği kadar dolaşılabilir. Çoğu sınıf için doğru seçim budur. "
        "En kısa yol __iter__'i bir generator olarak yazmaktır: gövdesinde yield olan __iter__ her çağrıldığında yeni bir generator döner, sen ayrıca __next__ ve StopIteration yazmazsın (generator'ları sonraki bölümde ayrıntılı göreceksin). "
        "__iter__'i olan bir nesne in işleci için de dolaşılır (ayrı bir __contains__ yoksa), sum, max, sorted, list ve tuple da onu kabul eder. M12'de gördüğün __getitem__ tabanlı eski yol hâlâ çalışır ama yeni kodda __iter__ yaz. __next__ değer bitince None döndürmek gibi bir yolla bitmeye çalışırsa döngü sonsuza kadar sürer: yineleme yalnızca StopIteration ile biter."
    ),
    code=r'''
class Countdown:
    """Kendisi iterator: tek kullanımlık."""

    def __init__(self, start):
        self.current = start

    def __iter__(self):
        return self

    def __next__(self):
        if self.current <= 0:
            raise StopIteration
        self.current -= 1
        return self.current + 1

class Range3:
    """Iterable: her for için yeni bir iterator verir."""

    def __init__(self, stop):
        self.stop = stop

    def __iter__(self):
        return Countdown(self.stop)

down = Countdown(3)
print(list(down), list(down))
r = Range3(2)
print(list(r), list(r))
print(sum(Countdown(4)), 2 in Range3(3), max(Range3(5)))
''',
    expectedOutput=r'''
[3, 2, 1] []
[2, 1] [2, 1]
10 True 5
''',
    why="Countdown kendi durumunu taşıdığı için ilk list() onu tüketti, ikincisi boş kaldı. Range3 her __iter__ çağrısında yeni bir Countdown ürettiği için iki kez dolaşıldı. sum, in ve max aynı protokolü kullandı: 2 in Range3(3) önce 3'ü, sonra 2'yi üretip True verdi.",
    alternatives=[
        "__iter__'i gövdesinde yield olan bir metot olarak yaz; ayrı iterator sınıfına gerek kalmaz.",
        "Veriyi zaten bir listede tutuyorsan __iter__ içinde return iter(self._items) yazmak yeterlidir.",
    ],
    traps=[
        "Tekrar dolaşılması gereken bir sınıfta __iter__'den self döndürmek: ikinci dolaşma boş gelir.",
        "__next__'in sonunda StopIteration yerine None döndürmek: döngü hiç bitmez.",
        "__iter__'in bir iterator yerine liste ya da None döndürmesi (TypeError: iter() returned non-iterator).",
        "Dolaşma sırasında nesnenin içindeki listeyi değiştirmek; atlanan ya da tekrar gelen öğeler olur.",
    ],
    realCode=r'''
class Pages:
    def __init__(self, items, size):
        self.items, self.size = items, size

    def __iter__(self):
        for start in range(0, len(self.items), self.size):
            yield self.items[start:start + self.size]

pages = Pages(list("abcdefg"), 3)
for number, page in enumerate(pages, start=1):
    print(number, page)
print(len(list(pages)))
''',
    realOutput=r'''
1 ['a', 'b', 'c']
2 ['d', 'e', 'f']
3 ['g']
3
''',
    lineByLine=[
        "Pages, bir listeyi sabit boyutlu sayfalara bölen bir iterable'dır (API'lerin sayfalı sonuçları gibi).",
        "__iter__ gövdesinde yield olduğu için her çağrıda yeni bir generator döner; __next__ yazılmadı.",
        "enumerate sayfaları 1'den numaralar; son sayfa daha kısadır.",
        "Aynı nesne ikinci kez dolaşıldığında yine üç sayfa çıkar: Pages tek kullanımlık değildir.",
    ],
    sources=[
        {"title": "Python 3.12 · Iterator'lar (kendi sınıfın)", "url": TUTORIAL + "#iterators"},
        {"title": "Python 3.12 · Iterator türleri", "url": "https://docs.python.org/3.12/library/stdtypes.html#iterator-types"},
    ],
)

section(
    id="generators",
    title="Generator fonksiyonları ve yield",
    eyebrow="Değerleri istendikçe üret",
    objectives=[
        "Gövdesinde yield olan fonksiyonun çağrılınca çalışmadığını, bir generator nesnesi döndürdüğünü ve her next'te bir sonraki yield'e kadar ilerleyip orada duraklayıp sürdüğünü izler.",
        "Generator'ın tükendiğini, return'ün yinelemeyi bitirdiğini (değeri StopIteration.value'da) ve return ile yield arasındaki farkı açıklar.",
    ],
    prerequisites=["iterator-protocol", "m6:def-return"],
    summary="Gövdesinde yield bulunan fonksiyon bir generator fonksiyonudur: çağrısı gövdeyi çalıştırmaz, bir generator (iterator) döndürür. Her next(), gövdeyi bir sonraki yield'e kadar çalıştırır, değeri verir ve yerel değişkenleriyle birlikte orada bekler.",
    explanation=(
        "Normal bir fonksiyon return ile tek bir değer döndürür ve biter. Gövdesinde yield olan fonksiyon ise farklı çalışır: countdown(3) çağrısı tek satır bile çalıştırmaz, bir generator nesnesi döndürür. Generator bir iterator'dır; next() çağrıldığında gövde kaldığı yerden bir sonraki yield'e kadar çalışır, yield'in değerini verir ve yerel değişkenleri, döngü konumu dahil, olduğu gibi bekletir. "
        "Gövdenin sonuna gelinince (ya da return çalışınca) generator StopIteration fırlatır ve tükenir; for döngüsü bunu sessizce bitiş olarak yorumlar. Generator'da return değer de taşıyabilir: return 5, StopIteration.value'da 5 olarak görünür ama for ve list bu değeri görmez. "
        "Tükenen generator yeniden başlamaz: aynı değerleri tekrar istiyorsan fonksiyonu yeniden çağır. Gövdede yield'den sonra gelen print gibi satırlar, ancak bir sonraki next istendiğinde çalışır; çıktıların sırası bu yüzden şaşırtıcı görünebilir. "
        "Neden kullanılır? Bir listeyi baştan kurup döndürmek yerine değerleri birer birer üretmek bellek kazandırır, sonsuz akışları mümkün kılar ve okuma/süzme/dönüştürme adımlarını küçük fonksiyonlara böler. Değeri birden çok kez kullanacaksan ya da uzunluğunu (len) bilmen gerekiyorsa sonucu list() ile topla."
    ),
    code=r'''
def countdown(n):
    print("başladı")
    while n > 0:
        yield n
        n -= 1
    print("bitti")

gen = countdown(3)
print(type(gen).__name__)
print(next(gen))
print(next(gen))
print(list(gen))
print(list(gen))

def numbered(items):
    for index, item in enumerate(items, 1):
        yield f"{index}. {item}"
    return len(items)

print(list(numbered(["süt", "ekmek"])))
try:
    next(numbered([]))
except StopIteration as stop:
    print("dönüş değeri:", stop.value)
''',
    expectedOutput=r'''
generator
başladı
3
2
bitti
[1]
[]
['1. süt', '2. ekmek']
dönüş değeri: 0
''',
    why="countdown(3) çağrısı 'başladı' yazmadı; gövde ilk next ile çalıştı. Her next bir yield'de durdu. list(gen) kalan tek değeri (1) aldı, döngü bitince 'bitti' yazıldı ve generator tükendi; ikinci list boş geldi. numbered'ın return değeri list()'e girmedi, yalnızca StopIteration.value'da göründü.",
    alternatives=[
        "Az sayıda değeri birden çok kez kullanacaksan doğrudan liste döndüren normal bir fonksiyon daha basittir.",
        "Tek satırlık dönüşümler için generator ifadesi (n * n for n in sayılar) yeterlidir; sonraki bölümde.",
    ],
    traps=[
        "Generator fonksiyonunu çağırınca gövdenin çalıştığını sanmak; hiçbir şey next istenene kadar çalışmaz.",
        "Generator'ı iki kez dolaşmak: ikincisi boş gelir.",
        "Generator'da her değeri üretmek isterken return yazmak: ilk return yinelemeyi bitirir.",
        "len(generator) ya da generator[0] denemek: generator'ın uzunluğu ve indeksi yoktur (TypeError).",
    ],
    realCode=r'''
def read_records(lines):
    for number, line in enumerate(lines, start=1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        name, score = line.split(":")
        yield number, name, int(score)

data = ["# notlar", "Ada:90", "", "Can:75"]
for number, name, score in read_records(data):
    print(number, name, score)
best = max(read_records(data), key=lambda record: record[2])
print("en yüksek:", best[1])
''',
    realOutput=r'''
2 Ada 90
4 Can 75
en yüksek: Ada
''',
    lineByLine=[
        "read_records boş satırları ve yorumları atlar, geçerli satırları satır numarasıyla birlikte üretir.",
        "Satır numarası, girdideki gerçek konumdur (2 ve 4); hata mesajı yazarken işe yarar.",
        "max ikinci bir dolaşma ister; read_records yeniden çağrılarak yeni bir generator alınır.",
        "Fonksiyon bütün kayıtları listede toplamadığı için büyük dosyalarda da az bellek kullanır.",
    ],
    sources=[
        {"title": "Python 3.12 · Generator'lar", "url": TUTORIAL + "#generators"},
        {"title": "Python 3.12 · yield ifadeleri", "url": "https://docs.python.org/3.12/reference/expressions.html#yield-expressions"},
    ],
)

section(
    id="generator-pipelines",
    title="Generator ifadeleri ve boru hatları",
    eyebrow="Tembel adımları birbirine bağla",
    objectives=[
        "Generator ifadesi (x for x in ...) ile liste kurucuyu ayırır ve generator'ları birbirine bağlayarak tembel bir veri boru hattı kurar.",
        "yield from ile alt generator'ın değerlerini aktarır; sonsuz generator'ları itertools.islice ile sınırlar ve generator'ı yalnızca bir kez tüketebileceğini hesaba katar.",
    ],
    prerequisites=["generators", "m5:list-comprehension", "m10:itertools-functools"],
    summary="Köşeli yerine yuvarlak parantezle yazılan kurucu, liste değil generator üretir: (n * n for n in sayılar). Generator'lar birbirini besleyerek tembel bir boru hattı kurar; her değer ancak en sondaki tüketici istediğinde üretilir.",
    explanation=(
        "[n * n for n in sayılar] bütün sonuçları bir listede toplar. (n * n for n in sayılar) ise bir generator ifadesidir: değerleri ancak istendiğinde üretir. Tek argümanlı çağrılarda ek parantez gerekmez: sum(n * n for n in sayılar). "
        "Generator'lar boru hattı gibi birbirine bağlanabilir: satırları okuyan, onları ayrıştıran, süzen ve dönüştüren her adım bir öncekinin çıktısını tüketir. Hiçbir ara liste kurulmaz; en sondaki tüketici (for, sum, list, max) bir değer istediğinde zincirin her halkası tam bir adım çalışır. Bu yüzden sonsuz bir kaynak bile kullanılabilir: naturals() hiç bitmeyen bir generator'dır, itertools.islice ilk birkaç değeri alıp gerisini hiç üretmez (M10). "
        "yield from alt_generator, alt generator'ın bütün değerlerini sırayla dışarı verir; for x in alt: yield x yazmanın kısa ve doğru yoludur. İç içe yapıları düzleştirmek ya da bir generator'ı küçük parçalara bölmek için kullanılır. "
        "Dikkat edilecek tek şey tüketmedir: generator bir kez dolaşılır. 2 in gen gibi bir sorgu bile aradığı değere kadar olanları tüketir ve kalanlar ilerideki kullanıma kalır. Aynı sonuçları birden çok yerde kullanacaksan listeye çevir; büyük veride ise boru hattını iki kez kurmak (fonksiyonu yeniden çağırmak) daha az bellek tüketir."
    ),
    code=r'''
from itertools import islice, count

def naturals():
    n = 1
    while True:
        yield n
        n += 1

squares = (n * n for n in naturals())
evens = (n for n in squares if n % 2 == 0)
print(list(islice(evens, 4)))
print(sum(n * n for n in range(1, 4)))

def flatten(groups):
    for group in groups:
        yield from group

print(list(flatten([[1, 2], (3,), "ab"])))
gen = (x for x in [1, 2, 3])
print(2 in gen, list(gen))
print(list(islice(count(10, 5), 3)))
''',
    expectedOutput=r'''
[4, 16, 36, 64]
14
[1, 2, 3, 'a', 'b']
True [3]
[10, 15, 20]
''',
    why="naturals sonsuzdur ama islice yalnızca dört çift kare istediği için zincir sekizinci doğal sayıda durdu. sum'a verilen generator ifadesi ara liste kurmadı. flatten, yield from ile her grubun öğelerini sırayla verdi; bir str de iterable'dır. 2 in gen, 1 ve 2'yi tüketti; list(gen) yalnızca kalan 3'ü aldı.",
    alternatives=[
        "Sonucu birden çok kez kullanacaksan ya da indeksle erişeceksen liste kurucu yaz.",
        "Hazır yapı taşları için itertools'a bak (chain, islice, takewhile, groupby; M10).",
    ],
    traps=[
        "Generator ifadesini iki kez kullanmak; ikinci kullanım boş gelir.",
        "Sonsuz bir generator'ı list() ile toplamak: program hiç bitmez.",
        "in ya da next ile yapılan bir sorgunun generator'dan değer tükettiğini unutmak.",
        "yield from yerine yield alt_generator yazmak: değerler yerine generator nesnesinin kendisi üretilir.",
    ],
    realCode=r'''
logs = [
    "INFO başladı",
    "ERROR disk dolu",
    "INFO devam",
    "ERROR ağ yok",
    "ERROR disk dolu",
]

def parse(lines):
    for line in lines:
        level, message = line.split(" ", 1)
        yield level, message

def only(level, records):
    return (message for lvl, message in records if lvl == level)

seen = set()
for message in only("ERROR", parse(logs)):
    if message not in seen:
        seen.add(message)
        print(message)
''',
    realOutput=r'''
disk dolu
ağ yok
''',
    lineByLine=[
        "parse her satırı (düzey, mesaj) çiftine ayırır; only bu akıştan yalnızca bir düzeyi süzer.",
        "only bir generator ifadesi döndürür; iki adım da tembeldir, ara liste kurulmaz.",
        "Döngü değerleri tek tek çeker; tekrar eden hata mesajları bir küme ile atlanır.",
        "Aynı yapı, logs yerine gigabaytlık bir dosya nesnesi verildiğinde de az bellekle çalışır.",
    ],
    sources=[
        {"title": "Python 3.12 · Generator ifadeleri", "url": TUTORIAL + "#generator-expressions"},
        {"title": "Python 3.12 · itertools", "url": "https://docs.python.org/3.12/library/itertools.html"},
    ],
)

section(
    id="decorators",
    title="Decorator temelleri",
    eyebrow="Bir fonksiyonu değiştirmeden sarmala",
    objectives=[
        "Decorator'ın fonksiyon alıp fonksiyon döndüren bir fonksiyon olduğunu ve @dec yazımının f = dec(f) atamasıyla aynı olduğunu gösterir; decorator'ın tanım anında bir kez çalıştığını bilir.",
        "Sarmalayıcıyı *args/**kwargs ile yazar, sonucu döndürür ve functools.wraps ile asıl fonksiyonun adını ve belgesini korur.",
    ],
    prerequisites=["m6:closure", "m6:args-kwargs", "m10:itertools-functools"],
    summary="Decorator, bir fonksiyonu alıp yerine başka bir fonksiyon (genellikle onu çağıran bir sarmalayıcı) döndüren fonksiyondur. def'in üstündeki @shout, greet = shout(greet) demektir. Sarmalayıcı *args, **kwargs ile her argümanı geçirmeli, sonucu döndürmeli ve @wraps(func) ile işaretlenmelidir.",
    explanation=(
        "Python'da fonksiyonlar değerdir: bir değişkene atanır, başka bir fonksiyona verilir, bir fonksiyondan döndürülür (M6). Decorator bunun üzerine kurulur: shout(func) içinde wrapper adında yeni bir fonksiyon tanımlar, wrapper func'ı çağırıp sonucunu değiştirir ve shout wrapper'ı döndürür. wrapper, func'ı bir closure olarak hatırlar. "
        "@shout satırı def greet'in hemen üstüne yazılır ve greet = shout(greet) ile birebir aynıdır. Bu atama fonksiyon tanımlanırken bir kez yapılır; decorator'ın gövdesindeki kod (wrapper'ın dışındaki satırlar) modül yüklenirken çalışır, sarmalayıcının gövdesi ise her çağrıda çalışır. "
        "Sarmalayıcıyı genel yaz: def wrapper(*args, **kwargs): return func(*args, **kwargs). Argüman almayan bir wrapper, argümanlı bir fonksiyonu sarınca TypeError verir; return yazmayı unutan wrapper ise her zaman None döndürür. "
        "Sarmalayıcı yeni bir fonksiyon olduğu için asıl fonksiyonun adı (__name__), belgesi (__doc__) ve imzası kaybolur; hata ayıklama, belgeler ve testler yanlış ad görür. functools.wraps(func) bu bilgileri wrapper'a kopyalar ve asıl fonksiyonu __wrapped__ olarak saklar; her decorator'da kullan. "
        "Gördüğün yerler: @property ve @classmethod (M11), @functools.lru_cache (M10), @dataclass (M12), web çatılarında @app.get(...) gibi rota kayıtları; günlükleme, süre ölçme, önbellekleme, yetki denetimi ve yeniden deneme yaygın kullanımlardır."
    ),
    code=r'''
from functools import wraps

def shout(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return result.upper() + "!"
    return wrapper

@shout
def greet(name, polite=False):
    """Selam verir."""
    return f"{'merhaba' if polite else 'selam'} {name}"

print(greet("ada"))
print(greet("can", polite=True))
print(greet.__name__, greet.__doc__)

def plain(name):
    return name

same = shout(plain)
print(same("x"), same.__wrapped__("x"))

def no_wraps(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@no_wraps
def report():
    """Rapor üretir."""

print(report.__name__, report.__doc__)
''',
    expectedOutput=r'''
SELAM ADA!
MERHABA CAN!
greet Selam verir.
X! x
wrapper None
''',
    why="@shout, greet'i sarmalayıcıyla değiştirdi; konumsal ve isimli argümanlar *args/**kwargs ile asıl fonksiyona geçti, sonuç büyük harfe çevrildi. wraps sayesinde greet adını ve belgesini korudu. shout(plain) aynı işin @ olmadan yazılışıdır ve __wrapped__ asıl fonksiyona ulaştırır. wraps kullanmayan decorator'da ad 'wrapper', belge None oldu.",
    alternatives=[
        "Davranış yalnızca bir yerde gerekiyorsa decorator yazmak yerine fonksiyonun içine eklemek daha açıktır.",
        "Önbellek gibi hazır ihtiyaçlar için kendi decorator'ını yazmadan önce functools'a bak (lru_cache, cache).",
    ],
    traps=[
        "wrapper içinde return'ü unutmak: dekore edilen fonksiyon her zaman None döndürür.",
        "wrapper'ı argümansız yazmak (def wrapper():): argümanlı fonksiyonda TypeError verir.",
        "decorator'dan wrapper yerine wrapper() döndürmek ya da hiçbir şey döndürmemek: ad None'a bağlanır.",
        "@wraps(func) eklememek: ad, belge ve testlerde görünen bilgi kaybolur.",
    ],
    realCode=r'''
from functools import wraps

def count_calls(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.calls += 1
        return func(*args, **kwargs)
    wrapper.calls = 0
    return wrapper

@count_calls
def add(a, b):
    return a + b

add(1, 2)
add(3, 4)
print(add(5, 6), add.calls, add.__name__)
''',
    realOutput=r'''
11 3 add
''',
    lineByLine=[
        "count_calls, sarmalayıcı fonksiyonun kendisine bir calls özniteliği ekler; fonksiyonlar da nesnedir.",
        "Her çağrıda sayaç artar ve asıl fonksiyon aynı argümanlarla çağrılır.",
        "Üç çağrıdan sonra sayaç 3'tür; print argümanları soldan sağa değerlendirildiği için add(5, 6) sayaçtan önce çalışır.",
        "wraps sayesinde add.__name__ hâlâ 'add'dir.",
    ],
    sources=[
        {"title": "Python sözlüğü · decorator", "url": "https://docs.python.org/3.12/glossary.html#term-decorator"},
        {"title": "Python 3.12 · functools.wraps", "url": "https://docs.python.org/3.12/library/functools.html#functools.wraps"},
    ],
)

section(
    id="decorator-params",
    title="Parametreli ve yığılmış decorator'lar",
    eyebrow="@retry(3) nasıl çalışır?",
    objectives=[
        "Parametreli decorator'ın üç katmanını (parametreyi alan fonksiyon → decorator → sarmalayıcı) okur ve yazar; @dec(…) ile @dec farkını açıklar.",
        "Birden çok decorator yığıldığında ifadelerin yukarıdan aşağı değerlendirildiğini, sarmalamanın ise aşağıdan yukarı uygulandığını ve çağrıda dıştan içe çalıştığını izler.",
    ],
    prerequisites=["decorators"],
    summary="@repeat(2) önce repeat(2)'yi çağırır; bu çağrı asıl decorator'ı döndürür ve o da fonksiyona uygulanır. Bu yüzden parametreli decorator üç iç içe fonksiyondur. Yığılmış decorator'larda def'e en yakın olan önce uygulanır, çağrıda ise en üstteki en dıştadır.",
    explanation=(
        "@ işaretinden sonra herhangi bir ifade gelebilir. @repeat(2) yazınca Python önce repeat(2) ifadesini değerlendirir; bunun sonucu asıl decorator olmalıdır. Bu yüzden parametreli decorator üç katmanlıdır: dıştaki fonksiyon parametreyi (times) alır ve decorator'ı döndürür, decorator fonksiyonu alıp sarmalayıcıyı döndürür, sarmalayıcı her çağrıda çalışır. İçteki katmanlar dıştakilerin parametrelerini closure olarak görür. "
        "Karışıklık genelde parantezlerde olur: parametresiz bir decorator'ı @log() diye çağırırsan log fonksiyon yerine hiç argüman almadan çağrılır ve TypeError verir; parametreli bir decorator'ı parantezsiz @repeat yazarsan repeat, fonksiyonu times parametresi sanır ve fonksiyonun yerine yanlış bir nesne konur. "
        "Birden çok decorator üst üste yazılabilir. @tag('b') @tag('i') def word() ifadesi word = tag('b')(tag('i')(word)) demektir: def'e en yakın decorator önce uygulanır, en üstteki en dışa sarılır. Çağrıldığında dıştaki sarmalayıcı önce başlar ve içtekini çağırır; sonuç <b><i>…</i></b> olur. Decorator ifadeleri (tag('b'), tag('i')) ise uygulanmadan önce yukarıdan aşağı değerlendirilir. "
        "Sıra önemlidir: önbellek ile yetki denetimini ters sırada yığmak, yetkisiz bir kullanıcıya önbellekteki sonucu gösterebilir. Yeniden deneme (retry), zaman aşımı, oran sınırı ve rota kaydı gibi gerçek kod örneklerinde parametreli decorator'lar çok yaygındır; yazmaktan çok okumayı bilmen yeterli."
    ),
    code=r'''
from functools import wraps

def repeat(times):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return [func(*args, **kwargs) for _ in range(times)]
        return wrapper
    return decorator

def tag(name):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return f"<{name}>{func(*args, **kwargs)}</{name}>"
        return wrapper
    return decorator

@repeat(2)
def hello(who):
    return f"merhaba {who}"

print(hello("Ada"))

@tag("b")
@tag("i")
def word():
    return "kalın"

print(word())

def trace(label):
    print("decorator kuruluyor:", label)
    def decorator(func):
        print("uygulanıyor:", label)
        return func
    return decorator

@trace("dış")
@trace("iç")
def task():
    return "iş"

print(task())
''',
    expectedOutput=r'''
['merhaba Ada', 'merhaba Ada']
<b><i>kalın</i></b>
decorator kuruluyor: dış
decorator kuruluyor: iç
uygulanıyor: iç
uygulanıyor: dış
iş
''',
    why="repeat(2) bir decorator döndürdü ve hello'yu iki kez çağıran sarmalayıcıyla değiştirdi. tag('i') word'e önce uygulandı, tag('b') onun dışına sarıldı. trace çıktısı sırayı açıkça gösterir: ifadeler yukarıdan aşağı değerlendirildi (dış, iç), uygulama ise aşağıdan yukarı yapıldı (iç, dış).",
    alternatives=[
        "Yalnızca birkaç sabit seçenek varsa ayrı parametresiz decorator'lar (retry_three, retry_five) daha basit olabilir.",
        "Yeniden deneme gibi işler için olgun kütüphaneler (tenacity gibi) vardır; kendi sürümünü yazmadan önce bak.",
    ],
    traps=[
        "Parametresiz decorator'ı @log() diye çağırmak (TypeError) ya da parametreliyi @repeat diye parantezsiz yazmak.",
        "Yığma sırasını ters düşünmek: def'e en yakın decorator önce uygulanır.",
        "Üç katmandan birinde return'ü unutmak; ad None'a bağlanır ya da sonuç kaybolur.",
        "Parametreyi sarmalayıcı içinde değiştirmek (times -= 1): closure değişkenine atama nonlocal ister ve paylaşılan durum yaratır.",
    ],
    realCode=r'''
from functools import wraps

def retry(times, exceptions=(ValueError,)):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as error:
                    print(f"deneme {attempt} başarısız: {error}")
            raise RuntimeError(f"{func.__name__} {times} denemede başarısız")
        return wrapper
    return decorator

answers = iter(["", "", "42"])

@retry(3)
def read_number():
    text = next(answers)
    if not text:
        raise ValueError("boş yanıt")
    return int(text)

print(read_number())
''',
    realOutput=r'''
deneme 1 başarısız: boş yanıt
deneme 2 başarısız: boş yanıt
42
''',
    lineByLine=[
        "retry(times, exceptions) parametreleri alır ve asıl decorator'ı döndürür.",
        "Sarmalayıcı yalnızca belirtilen hata türlerinde yeniden dener; başka hatalar olduğu gibi yükselir.",
        "answers ağ ya da kullanıcı gibi güvenilmez bir kaynağı taklit eder: ilk iki yanıt boştur.",
        "Üçüncü denemede değer geldiği için 42 döner; bütün denemeler başarısız olsaydı RuntimeError fırlatılacaktı.",
    ],
    sources=[
        {"title": "Python 3.12 · Fonksiyon tanımları ve decorator'lar", "url": "https://docs.python.org/3.12/reference/compound_stmts.html#function-definitions"},
    ],
)

section(
    id="context-manager-class",
    title="Context manager: __enter__ ve __exit__",
    eyebrow="with bloğunun girişini ve çıkışını yönet",
    objectives=[
        "with ifadesinin __enter__ ve __exit__ çağrılarını, as ile bağlanan değeri ve bloktan hata ile çıkılsa bile __exit__'in çalıştığını açıklar ve kendi context manager sınıfını yazar.",
        "__exit__'in hata bilgisini (tür, değer, traceback) aldığını ve True döndürürse hatayı yuttuğunu bilir; hatayı yalnızca bilinçli olarak yutar.",
    ],
    prerequisites=["m8:with-lifecycle", "m7:else-finally", "m12:dunder-basics"],
    summary="with X() as y: bloğu önce X().__enter__()'i çağırır ve dönüşü y'ye bağlar; blok nasıl biterse bitsin (normal, return, hata) __exit__ çağrılır. __exit__ hata bilgisini alır; False (ya da None) döndürürse hata yükselmeye devam eder, True döndürürse yutulur.",
    explanation=(
        "M8'de with open(...) as f: kalıbını kullandın; dosya, blok nasıl biterse bitsin kapanıyordu. Bu davranış iki dunder metotla tanımlanır. with ifadesi önce nesnenin __enter__ metodunu çağırır; dönen değer as'ten sonraki ada bağlanır (çoğu zaman self, ama başka bir şey de olabilir). Blok bitince __exit__(exc_type, exc, tb) çağrılır. "
        "Blok hatasız biterse üç argüman da None'dır. Blok içinde bir hata olursa __exit__ yine çağrılır ve hatanın türünü, nesnesini ve traceback'ini alır; temizlik (kapatma, kilidi bırakma, geri alma) bu yüzden kesin olarak yapılır. try/finally'nin yeniden kullanılabilir bir paketidir. "
        "__exit__'in dönüş değeri önemlidir: False ya da None (return yazmamak) hatanın with'in dışına yükselmesine izin verir; True hatayı yutar ve program with'ten sonraki satırdan devam eder. Her hatayı yutmak hataları gizler; yalnızca belirli ve beklenen türleri yut, gerisini yükselt. "
        "Context manager'lar kaynakların ömrünü yönetir: dosya ve ağ bağlantıları, kilitler (threading.Lock, M15), veritabanı işlemleri (commit/rollback, M18), geçici ayar değişiklikleri, süre ölçümü. Bir sınıf yazmak, durum tutman ya da birden çok metot sunman gerektiğinde uygundur; kısa senaryolar için sonraki bölümdeki contextlib daha az kod ister."
    ),
    code=r'''
class Tag:
    def __init__(self, name):
        self.name = name

    def __enter__(self):
        print(f"<{self.name}>")
        return self

    def __exit__(self, exc_type, exc, tb):
        print(f"</{self.name}>")
        return False

with Tag("p") as tag:
    print("içerik:", tag.name)

class Ignore:
    def __init__(self, *errors):
        self.errors = errors

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        if exc_type is not None and issubclass(exc_type, self.errors):
            print("yutuldu:", exc_type.__name__)
            return True
        return False

with Ignore(KeyError):
    {}["x"]
print("devam")
try:
    with Tag("div"):
        raise ValueError("bozuk")
except ValueError as error:
    print("dışarıda yakalandı:", error)
''',
    expectedOutput=r'''
<p>
içerik: p
</p>
yutuldu: KeyError
devam
<div>
</div>
dışarıda yakalandı: bozuk
''',
    why="Tag'in __enter__'i açılış etiketini yazıp nesneyi as tag'e bağladı; blok bitince __exit__ kapanış etiketini yazdı. Ignore, KeyError'u True döndürerek yuttu ve program devam etti. Tag ise False döndürdüğü için ValueError dışarı yükseldi, ama önce </div> yazıldı: temizlik hata durumunda da yapıldı.",
    alternatives=[
        "Basit giriş/çıkış işleri için contextlib.contextmanager ile bir generator fonksiyonu yaz (sonraki bölüm).",
        "Yalnızca belirli bir hatayı görmezden gelmek için hazır contextlib.suppress(KeyError) kullan.",
    ],
    traps=[
        "__exit__'ten koşulsuz True döndürüp bütün hataları sessizce yutmak.",
        "__enter__'den bir şey döndürmeyi unutup as değişkeninin None olması.",
        "Temizliği __exit__ yerine with bloğunun sonuna yazmak: hata olunca atlanır.",
        "__enter__ ya da __exit__ olmayan bir nesneyi with ile kullanmak (TypeError).",
    ],
    realCode=r'''
class Transaction:
    def __init__(self, account):
        self.account = account

    def __enter__(self):
        self.snapshot = dict(self.account)
        return self.account

    def __exit__(self, exc_type, exc, tb):
        if exc_type is not None:
            self.account.clear()
            self.account.update(self.snapshot)
            print("geri alındı:", exc)
        return False

account = {"bakiye": 100}
with Transaction(account) as acc:
    acc["bakiye"] -= 30
print(account)
try:
    with Transaction(account) as acc:
        acc["bakiye"] -= 500
        if acc["bakiye"] < 0:
            raise ValueError("bakiye eksiye düştü")
except ValueError as error:
    print("hata:", error)
print(account)
''',
    realOutput=r'''
{'bakiye': 70}
geri alındı: bakiye eksiye düştü
hata: bakiye eksiye düştü
{'bakiye': 70}
''',
    lineByLine=[
        "__enter__ hesabın bir kopyasını alır ve hesabın kendisini as acc'ye verir.",
        "İlk blok hatasız biter; değişiklik kalır ve bakiye 70 olur.",
        "İkinci blokta hata olunca __exit__ hesabı kopyadan geri yükler ve False döndürerek hatayı dışarı bırakır.",
        "Çağıran hatayı görür ve yakalar; hesap tutarlı hâlde (70) kalır. Veritabanı işlemlerinin rollback mantığı budur.",
    ],
    sources=[
        {"title": "Python 3.12 · with ifadesi bağlam yöneticileri", "url": "https://docs.python.org/3.12/reference/datamodel.html#with-statement-context-managers"},
        {"title": "Python 3.12 · with ifadesi", "url": "https://docs.python.org/3.12/reference/compound_stmts.html#the-with-statement"},
    ],
)

section(
    id="contextlib",
    title="contextlib ile context manager",
    eyebrow="Bir generator ile with yaz",
    objectives=[
        "@contextmanager ile generator tabanlı context manager yazar; yield öncesini giriş, sonrasını çıkış olarak kullanır ve temizliği try/finally ile garanti eder.",
        "contextlib.suppress ve ExitStack'i tanır; birden çok kaynağın ters sırayla kapandığını bilir.",
    ],
    prerequisites=["context-manager-class", "generators"],
    summary="@contextmanager, tek bir yield içeren generator fonksiyonunu context manager'a çevirir: yield'den öncesi __enter__, sonrası __exit__ gibi çalışır, yield'in değeri as'e bağlanır. Hata durumunda da temizliğin çalışması için yield try/finally içine yazılır.",
    explanation=(
        "Her context manager için sınıf yazmak uzundur. contextlib.contextmanager decorator'ı, içinde tek bir yield olan generator fonksiyonunu context manager'a çevirir: yield'e kadar olan kod with bloğuna girerken çalışır, yield'in değeri as'ten sonraki ada bağlanır, blok bittiğinde yield'den sonraki kod çalışır. "
        "Kritik ayrıntı: with bloğunda bir hata olursa bu hata generator'ın içinde, yield satırında yükselir. yield try/finally içinde değilse yield'den sonraki temizlik satırları atlanır. Bu yüzden kalıp şudur: hazırla; try: yield kaynak; finally: temizle. Hatayı yakalayıp yutmak istersen yield'i try/except ile sarabilirsin, ama yutmadığın sürece hata dışarı çıkar. "
        "contextlib'de hazır araçlar vardır: suppress(HataTürü) yalnızca o hatayı yutar (bilinçli olarak yok saymak için), ExitStack ise sayısı çalışma anında belli olan kaynakları (ör. bir dizi dosya) tek with içinde açar ve hepsini ters sırayla kapatır. redirect_stdout, chdir (3.11+) ve closing da sık görülür. "
        "Hangi yolu seçmeli? Durum tutman, birden çok metot sunman ya da yeniden kullanılabilir bir nesne gerekiyorsa sınıf; kısa bir giriş/çıkış işi için @contextmanager. İkisi de with açısından aynı davranır."
    ),
    code=r'''
from contextlib import contextmanager, suppress, ExitStack

@contextmanager
def tag(name):
    print(f"<{name}>")
    try:
        yield name.upper()
    finally:
        print(f"</{name}>")

with tag("ul") as upper:
    print("içerik", upper)

try:
    with tag("li"):
        raise ValueError("bozuk")
except ValueError:
    print("hata yine dışarı çıktı")

with suppress(FileNotFoundError):
    open("yok.txt", encoding="utf-8")
print("suppress sonrası")

with ExitStack() as stack:
    names = [stack.enter_context(tag(n)) for n in ("a", "b")]
    print(names)
''',
    expectedOutput=r'''
<ul>
içerik UL
</ul>
<li>
</li>
hata yine dışarı çıktı
suppress sonrası
<a>
<b>
['A', 'B']
</b>
</a>
''',
    why="tag'in yield öncesi giriş, finally bloğu çıkış işini yaptı; yield'in değeri as upper'a bağlandı. li bloğundaki hata yield satırında yükseldi, finally yine kapanış etiketini yazdı ve hata dışarı çıktı. suppress yalnızca FileNotFoundError'ı yuttu. ExitStack iki tag'i sırayla açtı ve ters sırayla kapattı.",
    alternatives=[
        "Durum tutan ya da başka metotlar da sunan bir kaynak için __enter__/__exit__ sınıfı yaz.",
        "Tek bir hatayı yok saymak için try/except: pass yerine suppress niyeti daha açık gösterir; ama hatayı gerçekten yok saymak istediğinden emin ol.",
    ],
    traps=[
        "yield'i try/finally içine almamak: with bloğunda hata olunca temizlik atlanır.",
        "Generator'ın ikinci bir yield'e ulaşması ya da hiç yield'e ulaşmaması (RuntimeError: generator didn't stop / didn't yield).",
        "suppress ile geniş hata türlerini (Exception) yutup gerçek hataları gizlemek.",
        "@contextmanager ile dekore edilen fonksiyonu with olmadan çağırıp kodun çalıştığını sanmak.",
    ],
    realCode=r'''
from contextlib import contextmanager

settings = {"debug": False}

@contextmanager
def temporarily(key, value):
    old = settings[key]
    settings[key] = value
    try:
        yield
    finally:
        settings[key] = old

with temporarily("debug", True):
    print("içeride:", settings["debug"])
print("dışarıda:", settings["debug"])
try:
    with temporarily("debug", True):
        raise RuntimeError("test")
except RuntimeError:
    pass
print("hatadan sonra:", settings["debug"])
''',
    realOutput=r'''
içeride: True
dışarıda: False
hatadan sonra: False
''',
    lineByLine=[
        "temporarily bir ayarı geçici olarak değiştirir; eski değer yield'den önce saklanır.",
        "with bloğunda ayar True'dur; blok bitince finally eski değeri geri koyar.",
        "Blokta hata olsa bile finally çalıştığı için ayar False'a döner; hata ise dışarıda yakalanır.",
        "Testlerde ortam değişkeni ya da ayar değiştirmenin güvenli yolu budur (pytest'in monkeypatch'i de aynı fikri kullanır, M16).",
    ],
    sources=[
        {"title": "Python 3.12 · contextlib", "url": "https://docs.python.org/3.12/library/contextlib.html"},
    ],
)
