"""M12 (OOP 2) lesson sections. Imported by build_m12.py."""

TUTORIAL = "https://docs.python.org/3.12/tutorial/classes.html"
DATAMODEL = "https://docs.python.org/3.12/reference/datamodel.html"


def c(text):
    return text.strip("\n")


sections = []


def section(**fields):
    for key in ("code", "expectedOutput", "realCode", "realOutput"):
        fields[key] = c(fields[key])
    fields["runtime"] = "browser"
    sections.append(fields)


section(
    id="polymorphism",
    title="Polimorfizm ve duck typing",
    eyebrow="Aynı çağrı, farklı nesne",
    objectives=[
        "Aynı metot adını farklı sınıflarda uygulayıp ortak kodun hepsiyle çalıştığını gösterir.",
        "Kalıtımla polimorfizmi (override) ve ortak üst sınıf gerektirmeyen duck typing'i ayırır; isinstance zincirleri yerine polimorfizmi seçer.",
    ],
    prerequisites=["m11:inheritance-super", "m11:composition"],
    summary="Polimorfizm, aynı çağrının (shape.area()) nesnenin sınıfına göre farklı iş yapmasıdır. Python'da çağıran kod yalnızca nesnenin ilgili metoda sahip olup olmadığına bakar; ortak bir üst sınıf şart değildir (duck typing).",
    explanation=(
        "Polimorfizm 'çok biçimlilik' demektir: çağıran kod nesnenin hangi sınıftan olduğunu bilmeden aynı metodu çağırır ve her nesne kendi işini yapar. M11'de bunun bir biçimini gördün: üst sınıftaki self.role() çağrısı alt sınıfın sürümünü çalıştırıyordu. "
        "Python'da bunun için ortak üst sınıf gerekmez. for shape in shapes: shape.area() satırı, area metodu olan her nesneyle çalışır; buna duck typing denir ('ördek gibi yürüyor ve ötüyorsa ördektir'). len() de böyledir: list, str ve dict'in ortak bir sınıfı yoktur ama hepsi len ile çalışır. "
        "Alternatif, çağıran tarafta tür sormaktır: if isinstance(shape, Square): ... elif isinstance(shape, Rectangle): .... Bu zincir her yeni tür eklendiğinde bütün çağıran yerlerin değişmesini ister. Polimorfizmde yeni bir sınıf yazarsın ve mevcut çağıran kodun hiçbir satırı değişmez. "
        "Bedeli: arayüz dilde yazılı olmadığı için eksik bir metot ancak çalışma anında AttributeError olarak ortaya çıkar. Arayüzü açıkça belirtip hatayı erkene çekmek için sonraki bölümdeki abc (ve M14'teki Protocol) kullanılır. Python'da önce çalıştırmayı deneyip hatayı yakalama tarzına (EAFP) uygun olarak, tür sormak yerine metodu çağırmak çoğu zaman en sade çözümdür."
    ),
    code=r'''
class Square:
    def __init__(self, side):
        self.side = side

    def area(self):
        return self.side ** 2

class Rectangle:
    def __init__(self, width, height):
        self.width, self.height = width, height

    def area(self):
        return self.width * self.height

class Triangle:
    def __init__(self, base, height):
        self.base, self.height = base, height

    def area(self):
        return self.base * self.height / 2

shapes = [Square(3), Rectangle(2, 5), Triangle(4, 5)]
for shape in shapes:
    print(type(shape).__name__, shape.area())
print(sum(shape.area() for shape in shapes))
print(len("abc"), len([1, 2]), len({"a": 1}))

class Robot:
    pass

try:
    Robot().area()
except AttributeError:
    print("Robot'ta area yok")
''',
    expectedOutput=r'''
Square 9
Rectangle 10
Triangle 10.0
29.0
3 2 1
Robot'ta area yok
''',
    why="Üç sınıfın ortak bir üst sınıfı yok; hepsi area metodunu sunduğu için aynı döngüde kullanıldı. sum de aynı arayüzden yararlandı. Robot area sunmadığı için çağrı çalışma anında AttributeError verdi: duck typing arayüzü denetlemez, yalnızca kullanır.",
    alternatives=[
        "Ortak davranışı ve zorunlu metotları belirtmek istiyorsan ortak bir soyut üst sınıf yaz (sonraki bölüm).",
        "Tür bazlı farklı davranışı bir sözlükle (tür → işlev) ya da metot olarak sınıfa koymak, isinstance zincirinden daha kolay genişler.",
    ],
    traps=[
        "Her yeni türde isinstance zincirine yeni bir elif eklemek; polimorfizm bu zinciri gereksiz kılar.",
        "Arayüzü yarım uygulayan bir sınıfı listeye koymak: hata ancak o nesneye sıra geldiğinde, çalışma anında çıkar.",
        "Metot adını farklı yazmak (area / surface): duck typing adlara bakar, anlama değil.",
        "Polimorfizm için kalıtımın şart olduğunu sanmak; Python'da gerekmez.",
    ],
    realCode=r'''
import json

class JsonExporter:
    def export(self, rows):
        return json.dumps(rows, ensure_ascii=False)

class CsvExporter:
    def export(self, rows):
        header = ",".join(rows[0])
        lines = [",".join(str(value) for value in row.values()) for row in rows]
        return "\n".join([header, *lines])

def save(exporter, rows):
    return exporter.export(rows)

rows = [{"ad": "Ada", "puan": 90}, {"ad": "Can", "puan": 75}]
for exporter in (JsonExporter(), CsvExporter()):
    print(save(exporter, rows))
''',
    realOutput=r'''
[{"ad": "Ada", "puan": 90}, {"ad": "Can", "puan": 75}]
ad,puan
Ada,90
Can,75
''',
    lineByLine=[
        "İki dışa aktarıcı sınıf aynı export metodunu sunar; ortak üst sınıfları yoktur.",
        "save fonksiyonu hangi dışa aktarıcıyı aldığını bilmez, yalnızca export çağırır.",
        "Yeni bir biçim (XML gibi) eklemek yalnızca yeni bir sınıf yazmaktır; save değişmez.",
        "Döngü aynı rows verisini iki farklı biçimde yazdırır.",
    ],
    sources=[
        {"title": "Python 3.12 · Sınıflar (duck typing ve çok biçimlilik)", "url": TUTORIAL},
        {"title": "Python sözlüğü · duck-typing", "url": "https://docs.python.org/3.12/glossary.html#term-duck-typing"},
    ],
)

section(
    id="abc",
    title="Soyut sınıflar (abc)",
    eyebrow="Alt sınıflara sözleşme dayat",
    objectives=[
        "ABC ve @abstractmethod ile alt sınıfların uygulaması gereken metotları belirler.",
        "Soyut sınıfın ve soyut metodu eksik bırakan alt sınıfın örneklenemediğini (TypeError) gösterir; soyut sınıfta somut ortak metotla soyut metodu birlikte kullanır.",
    ],
    prerequisites=["polymorphism", "m11:inheritance-super"],
    summary="class Report(ABC) içindeki @abstractmethod ile işaretlenen metotlar alt sınıflarda yazılmak zorundadır. Eksik bırakan alt sınıf, nesne kurulurken TypeError verir; hata çalışma anının ortasına kadar beklemez.",
    explanation=(
        "abc modülü (Abstract Base Classes) arayüzü açıkça yazmanı sağlar. class Report(ABC): ile soyut bir sınıf tanımlar, uygulanması şart metotları @abstractmethod ile işaretlersin. Soyut metotları olan sınıftan doğrudan nesne üretilemez, soyut metodunu yazmayan alt sınıftan da üretilemez: Report() ve BrokenReport() çağrıları TypeError verir. "
        "Duck typing'in geç gelen AttributeError'ına karşı bu hata erkendir: nesne kurulurken, yani eksik metoda hiç sıra gelmeden. Hangi metotların eksik olduğunu SınıfAdı.__abstractmethods__ gösterir. "
        "Soyut sınıf yalnızca zorunluluk koymaz, ortak davranışı da taşır: somut render() metodu soyut rows()'u çağırır, alt sınıf yalnızca rows()'u yazar. Bu şablon metot (template method) kalıbıdır. "
        "abc yalnızca metodun adının var olduğunu denetler; imzayı, dönüş türünü ya da doğru çalıştığını denetlemez. Her arayüz için abc şart değildir: küçük, tek dosyalık kodda duck typing yeter. Eklenti sistemleri, çok sayıda alt sınıfı olan çerçeveler ve kütüphane sınıfları için sözleşmeyi açık yazmak değerlidir. Tip ipuçlarıyla yapısal arayüz tanımlamak (Protocol) M14'te gelecek."
    ),
    code=r'''
from abc import ABC, abstractmethod

class Report(ABC):
    @abstractmethod
    def rows(self):
        ...

    def render(self):
        lines = [f"- {row}" for row in self.rows()]
        return "\n".join(lines) or "(boş)"

class SalesReport(Report):
    def rows(self):
        return ["elma: 5", "armut: 3"]

class BrokenReport(Report):
    pass

print(SalesReport().render())
for cls in (Report, BrokenReport):
    try:
        cls()
    except TypeError:
        print(cls.__name__, "örneklenemez")
print(isinstance(SalesReport(), Report), issubclass(BrokenReport, Report))
print(sorted(Report.__abstractmethods__))
''',
    expectedOutput=r'''
- elma: 5
- armut: 3
Report örneklenemez
BrokenReport örneklenemez
True True
['rows']
''',
    why="SalesReport soyut rows metodunu yazdığı için nesnesi kurulabildi ve ortak render metodunu kullandı. Report soyut olduğu, BrokenReport ise rows'u yazmadığı için ikisi de kurulurken TypeError verdi. BrokenReport yine de Report'un alt sınıfıdır (True); örneklenemez olması soyut kalmasından gelir.",
    alternatives=[
        "Sözleşme küçük ve tek yerdeyse duck typing ile başla; yanlış kullanım görüldükçe soyut sınıfa geç.",
        "Yalnızca davranış paylaşımı istiyorsan ve zorunluluk gerekmiyorsa soyut metotsuz normal bir üst sınıf yeterlidir.",
    ],
    traps=[
        "Soyut metodu alt sınıfta başka bir adla yazmak (send / send_message): sınıf soyut kalır ve örneklenemez.",
        "ABC'den türetmeyi unutup yalnızca @abstractmethod kullanmak: denetim çalışmaz.",
        "abc'nin imzayı ya da dönüş değerini denetlediğini sanmak; yalnızca adın varlığına bakar.",
        "Her küçük sınıf için soyut üst sınıf yazıp kodu gereksiz karmaşıklaştırmak.",
    ],
    realCode=r'''
from abc import ABC, abstractmethod

class Validator(ABC):
    @abstractmethod
    def check(self, value):
        ...

    def validate(self, values):
        return [value for value in values if not self.check(value)]

class Positive(Validator):
    def check(self, value):
        return value > 0

class Even(Validator):
    def check(self, value):
        return value % 2 == 0

for validator in (Positive(), Even()):
    print(type(validator).__name__, validator.validate([-2, 3, 4]))
''',
    realOutput=r'''
Positive [-2]
Even [3]
''',
    lineByLine=[
        "Validator sözleşmeyi koyar: her doğrulayıcı check yazmak zorundadır.",
        "validate ortak somut metottur; check'i çağırıp kuralı geçemeyen değerleri toplar.",
        "Positive ve Even yalnızca check'i yazar; liste süzme kodu bir kez yazılmıştır.",
        "Aynı validate çağrısı, doğrulayıcıya göre farklı sonuç verir (polimorfizm).",
    ],
    sources=[
        {"title": "Python 3.12 · abc modülü", "url": "https://docs.python.org/3.12/library/abc.html"},
    ],
)

section(
    id="dunder-basics",
    title="Dunder metotlar ve veri modeli",
    eyebrow="Python yerleşik işlevleri nesnene bağlar",
    objectives=[
        "len(), bool(), in, [] ve () gibi işlevlerin ve sözdiziminin arkasında özel metotlar (__len__, __bool__, __contains__, __getitem__, __call__) olduğunu açıklar ve kendi sınıfında uygular.",
        "__eq__ tanımlanınca __hash__'in None olduğunu bilir; desteklenmeyen türde NotImplemented döndürmenin amacını açıklar.",
    ],
    prerequisites=["m11:methods-state"],
    summary="Adı iki alt çizgiyle başlayıp biten (dunder) metotları sen çağırmazsın; Python çağırır. len(x) x.__len__()'i, x[i] x.__getitem__(i)'yi, a == b a.__eq__(b)'yi çalıştırır. Bunları yazarak nesneni yerleşik türler gibi kullanılır yaparsın.",
    explanation=(
        "Dunder ('double underscore') metotlar Python'un veri modelidir: dil, belirli sözdizimini ve yerleşik işlevleri nesnenin özel metotlarına bağlar. __init__, __repr__ ve __str__'i M11'de gördün. Bu bölümde: len(x) için __len__, x[i] için __getitem__, 'a' in x için __contains__, x(...) için __call__, bool(x) ve if x: için __bool__ ve a == b için __eq__. "
        "Bu metotları doğrudan çağırma (x.__len__() yerine len(x) yaz); onlar Python'un çağırması içindir. Kendi dunder adını da uydurma: çift alt çizgili adlar dile ayrılmıştır. "
        "Doğruluk değeri sırası: __bool__ varsa o, yoksa __len__ (0 ise yanlış), ikisi de yoksa nesne her zaman doğrudur. Bu yüzden len'i olan bir sınıfta boş nesne if nesne: koşulunda yanlış sayılır. "
        "__getitem__ yazarsan sınıf indekslemeyi ve eski bir kural gereği for döngüsü ile list() dönüşümünü de kazanır (IndexError gelene kadar 0, 1, 2... dener); iterator protokolünün doğru yolunu M13'te göreceksin. "
        "Varsayılan == nesnenin kimliğine bakar. __eq__ yazarak değere göre eşitlik tanımlarsın. Dikkat: __eq__ tanımlı ve __hash__ yazılmamış bir sınıfta Python __hash__'i None yapar; nesne artık set öğesi ya da sözlük anahtarı olamaz (eşit nesneler aynı hash'i vermeli, değiştirilebilir nesne için güvenli hash yazmak zordur). Tanımadığı türle karşılaşan __eq__ ve işleç metotları NotImplemented döndürmelidir: Python bunun üzerine karşı tarafı dener, ikisi de reddederse == için kimlik karşılaştırmasına düşer, aritmetik işleçlerde TypeError verir."
    ),
    code=r'''
class Playlist:
    def __init__(self, name, songs):
        self.name = name
        self._songs = list(songs)

    def __len__(self):
        return len(self._songs)

    def __getitem__(self, index):
        return self._songs[index]

    def __contains__(self, song):
        return song.lower() in (s.lower() for s in self._songs)

    def __call__(self, index):
        return f"{self.name}: {self._songs[index]}"

    def __eq__(self, other):
        if not isinstance(other, Playlist):
            return NotImplemented
        return self.name == other.name and self._songs == other._songs

mix = Playlist("Yol", ["Ezgi", "Rüzgar", "Deniz"])
print(len(mix), mix[0], mix[-1])
print("rüzgar" in mix, "Dağ" in mix)
print(list(mix))
print(mix(1))
print(bool(Playlist("Boş", [])), bool(mix))
print(mix == Playlist("Yol", ["Ezgi", "Rüzgar", "Deniz"]), mix == "Yol")
print(Playlist.__hash__)
''',
    expectedOutput=r'''
3 Ezgi Deniz
True False
['Ezgi', 'Rüzgar', 'Deniz']
Yol: Rüzgar
False True
True False
None
''',
    why="Tek tek dunder'lar tek tek yerleşik davranışa bağlandı: len, indeks, in, çağırma, doğruluk (boş çalma listesi __len__ 0 olduğu için False) ve ==. __getitem__ sayesinde list(mix) de çalıştı. mix == 'Yol' karşılaştırmasında __eq__ NotImplemented döndürdü, str de reddetti ve sonuç False oldu. Son satır, __eq__ yazıldığı için __hash__'in None olduğunu gösterir.",
    alternatives=[
        "Yalnızca listeye benzeyen bir kap yazıyorsan listeden türemek yerine list'i içeride tutup bu dunder'ları yazmak (composition) arayüzü senin elinde bırakır.",
        "Bir kapsayıcıyı tam bir koleksiyon yapmak istiyorsan collections.abc sınıfları (Sequence, Mapping) eksik dunder'ları tamamlar.",
    ],
    traps=[
        "__eq__ yazıp nesneyi set ya da sözlük anahtarı olarak kullanmaya çalışmak (TypeError: unhashable type).",
        "Dunder metotları doğrudan çağırmak (x.__len__()) ya da kendi çift alt çizgili adını uydurmak.",
        "__eq__ içinde other'ın türünü denetlemeyip başka türle karşılaştırınca AttributeError almak; NotImplemented döndür.",
        "__len__ yazıp boş nesnenin if koşulunda yanlış sayıldığını unutmak.",
    ],
    realCode=r'''
class Settings:
    def __init__(self, **values):
        self._values = values

    def __getitem__(self, key):
        return self._values[key]

    def __contains__(self, key):
        return key in self._values

    def __len__(self):
        return len(self._values)

settings = Settings(debug=True, port=8000)
print(settings["port"], "debug" in settings, "host" in settings, len(settings))
try:
    settings["host"]
except KeyError as error:
    print("KeyError:", error)
''',
    realOutput=r'''
8000 True False 2
KeyError: 'host'
''',
    lineByLine=[
        "Settings, sözlüğü içeride saklar ve yalnızca gereken dunder'ları dışarı açar.",
        "settings['port'] __getitem__'e, 'debug' in settings __contains__'e, len(settings) __len__'e gider.",
        "Olmayan anahtarda iç sözlüğün KeyError'ı olduğu gibi yükselir; çağıran bunu sözlükteki gibi yakalayabilir.",
        "Sınıf sözlükten türemediği için update ya da pop gibi istenmeyen metotlar açılmaz.",
    ],
    sources=[
        {"title": "Python 3.12 · Veri modeli: özel metot adları", "url": DATAMODEL + "#special-method-names"},
    ],
)

section(
    id="operator-overloading",
    title="Operatör aşırı yükleme",
    eyebrow="+, == ve < kendi nesnelerinle çalışsın",
    objectives=[
        "__add__, __mul__, __eq__ ve __lt__ ile işleçleri kendi sınıfı için tanımlar; toplama gibi işleçlerin yeni nesne döndürmesi gerektiğini bilir.",
        "Yansıyan __radd__ ile sum() kullanımını açıklar, functools.total_ordering ile karşılaştırma işleçlerini tamamlar ve desteklenmeyen türde NotImplemented döndürür.",
    ],
    prerequisites=["dunder-basics", "m10:itertools-functools"],
    summary="a + b, Python'da type(a).__add__(a, b) çağrısıdır. Metot NotImplemented döndürürse Python b.__radd__(a)'yı dener; ikisi de reddederse TypeError çıkar. İşleç metotları operandları değiştirmez, yeni nesne döndürür.",
    explanation=(
        "İşleçler dunder metotlarla tanımlanır: + için __add__, - için __sub__, * için __mul__, == için __eq__, < için __lt__. Amaç, doğal bir anlamı olan türlerde (para, vektör, sürüm numarası) kodu okunur kılmaktır; Person + Person gibi anlamsız bir işleç tanımlama. "
        "a + b yazınca önce a.__add__(b) denenir. Tanımadığı bir tür görürse metot NotImplemented döndürmelidir (hata fırlatma, return NotImplemented): Python bunun üzerine sağ operandın yansıyan metodunu, yani b.__radd__(a)'yı dener. Hiçbiri çözemezse TypeError: unsupported operand çıkar. "
        "Bu yüzden sum() kendi türünde çalışır: sum başlangıç değeri olarak 0 kullanır, yani ilk adım 0 + nesne'dir. int, nesneyi tanımaz; Python nesne.__radd__(0)'ı çağırır. __radd__ içinde other == 0 ise self döndürmek sum([...]) çağrısını mümkün kılar. "
        "İşleç metotları yeni nesne döndürmeli, operandları değiştirmemeli: c = a + b yazınca a'nın değişmesi şaşırtıcıdır. += için ayrı bir __iadd__ yazılmazsa Python a = a + b yapar. "
        "Karşılaştırmada Python gerekirse yansıyanı kullanır: yalnızca __lt__ varsa a > b, b < a'ya çevrilir; ama <= ve >= için tanımlı bir yol yoktur (TypeError). Dört karşılaştırmayı elle yazmamak için __eq__ ve bir sıralama metodu yaz, sınıfa @functools.total_ordering ekle (M10'daki functools). __eq__ yazdığında __hash__'in None olacağını unutma."
    ),
    code=r'''
from functools import total_ordering

@total_ordering
class Money:
    def __init__(self, cents):
        self.cents = cents

    def __add__(self, other):
        if not isinstance(other, Money):
            return NotImplemented
        return Money(self.cents + other.cents)

    def __radd__(self, other):
        if other == 0:
            return self
        return NotImplemented

    def __mul__(self, factor):
        if not isinstance(factor, int):
            return NotImplemented
        return Money(self.cents * factor)

    def __eq__(self, other):
        if not isinstance(other, Money):
            return NotImplemented
        return self.cents == other.cents

    def __lt__(self, other):
        if not isinstance(other, Money):
            return NotImplemented
        return self.cents < other.cents

    def __repr__(self):
        return f"Money({self.cents // 100},{self.cents % 100:02d})"

a, b = Money(250), Money(175)
print(a + b, a * 3)
print(sum([a, b, Money(5)]))
print(a > b, a <= b, a == Money(250))
print(sorted([a, b, Money(5)]))
try:
    a + 10
except TypeError:
    print("TypeError")
''',
    expectedOutput=r'''
Money(4,25) Money(7,50)
Money(4,30)
True False True
[Money(0,05), Money(1,75), Money(2,50)]
TypeError
''',
    why="a + b ve a * 3 yeni Money nesneleri döndürdü; a ve b değişmedi. sum 0 + Money adımını __radd__ ile çözdü. total_ordering, __eq__ ve __lt__'dan >, <= ve >='yi türetti; sorted yalnızca __lt__ kullandı. a + 10'da __add__ NotImplemented verdi, int de reddetti ve TypeError çıktı.",
    alternatives=[
        "Para gibi değerleri tam sayı kuruş ya da decimal.Decimal ile tut; float ile hesap yuvarlama hatası getirir (M1).",
        "Yalnızca sıralama anahtarı lazımsa işleç yazmak yerine sorted(..., key=...) kullan.",
    ],
    traps=[
        "__add__ içinde self'i değiştirip döndürmek: a + b operandı bozar.",
        "Tanımadığı türde TypeError fırlatmak: return NotImplemented ile Python'a diğer tarafı denetme şansı ver.",
        "sum() kullanacağın sınıfta __radd__ yazmamak (0 + nesne TypeError verir).",
        "Yalnız __lt__ yazıp <= beklemek: total_ordering ya da elle tanımlama gerekir.",
    ],
    realCode=r'''
class Vector:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __mul__(self, k):
        return Vector(self.x * k, self.y * k)

    __rmul__ = __mul__

    def __abs__(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

v = Vector(3, 4)
print(v + Vector(1, 1), v * 2, 2 * v, abs(v))
''',
    realOutput=r'''
Vector(4, 5) Vector(6, 8) Vector(6, 8) 5.0
''',
    lineByLine=[
        "__add__ ve __mul__ yeni Vector döndürür; v değişmez.",
        "__rmul__ = __mul__ atamasıyla 2 * v ifadesi de çalışır: int, Vector'u tanımadığı için Python v.__rmul__(2)'yi dener.",
        "__abs__ abs(v) çağrısına bağlıdır; 3-4-5 üçgeninden 5.0 döner.",
        "__repr__ sonucu okunur gösterir; yazdırılan her değer yeni bir Vector'dur.",
    ],
    sources=[
        {"title": "Python 3.12 · Veri modeli: sayısal tür emülasyonu", "url": DATAMODEL + "#emulating-numeric-types"},
        {"title": "Python 3.12 · functools.total_ordering", "url": "https://docs.python.org/3.12/library/functools.html#functools.total_ordering"},
    ],
)

section(
    id="mro",
    title="Çoklu kalıtım ve MRO",
    eyebrow="Hangi metot önce bulunur?",
    objectives=[
        "class D(B, C) ile çoklu kalıtımı kurar ve metot arama sırasını (__mro__) okur.",
        "super()'in 'üst sınıf' değil MRO'daki bir sonraki sınıf olduğunu, elmas yapıda her sınıfın bir kez çalıştığını ve mixin'in ne işe yaradığını açıklar.",
    ],
    prerequisites=["m11:inheritance-super", "polymorphism"],
    summary="Python metodu sınıfın MRO'sundaki (Method Resolution Order) sırayla arar: sınıfın kendisi, sonra tutarlı bir sırayla üst sınıfları. super(), MRO'da bir sonraki sınıfı çağırır; elmas yapıda ortak üst sınıf bir kez çalışır.",
    explanation=(
        "class D(B, C): bir sınıfın birden çok üst sınıfı olabilir. Bir ad aranırken Python D.__mro__ listesini soldan sağa gezer ve ilk bulduğunu kullanır. Sıra C3 doğrusallaştırması ile hesaplanır; temel kurallar: bir sınıf kendi üst sınıflarından önce gelir ve sınıf başlığında yazdığın sıra korunur. D(B, C) için sonuç D, B, C, A, object olur (B ve C'nin ortak üst sınıfı A en sona gider). "
        "super() 'üst sınıf' demek değildir: 'bu nesnenin MRO'sunda, bu sınıftan sonra gelen sınıf' demektir. D'deki super().hello() B'ye gider, B'deki super().hello() ise A'ya değil C'ye gider; çünkü D nesnesinin MRO'sunda B'den sonra C vardır. Elmas yapıda her sınıf yalnızca bir kez çalışır, ortak üst sınıf (A) bir kez kurulur. Bunun işlemesi için zincirdeki her sınıf super()'i çağırmalıdır (işbirlikçi kalıtım); biri çağırmazsa zincir orada kopar ve sonrasındaki sınıflar hiç çalışmaz. "
        "Çelişen bir sıra istersen (class Bad(A, B) iken B zaten A'dan türüyorsa) sınıf tanımı TypeError verir: tutarlı bir MRO kurulamaz. "
        "Çoklu kalıtımın yaygın ve güvenli kullanımı mixin'dir: tek bir işe odaklı, kendi başına örneklenmesi beklenmeyen küçük sınıf (JsonMixin.to_json gibi) bir ya da birkaç sınıfa eklenir. Karmaşık çoklu kalıtım hiyerarşilerinden kaçın: çoğu zaman composition daha okunurdur. Bu bölümün amacı yazmaktan çok, başkasının kodunda gördüğünde sırayı doğru okumandır."
    ),
    code=r'''
import json

class A:
    def hello(self):
        return ["A"]

class B(A):
    def hello(self):
        return ["B"] + super().hello()

class C(A):
    def hello(self):
        return ["C"] + super().hello()

class D(B, C):
    def hello(self):
        return ["D"] + super().hello()

print([cls.__name__ for cls in D.__mro__])
print(D().hello())
print([cls.__name__ for cls in B.__mro__])

class JsonMixin:
    def to_json(self):
        return json.dumps(vars(self), sort_keys=True)

class Pet(JsonMixin):
    def __init__(self, name, age):
        self.name, self.age = name, age

print(Pet("Pamuk", 3).to_json())

try:
    class Bad(A, B):
        pass
except TypeError:
    print("tutarsız MRO")
''',
    expectedOutput=r'''
['D', 'B', 'C', 'A', 'object']
['D', 'B', 'C', 'A']
['B', 'A', 'object']
{"age": 3, "name": "Pamuk"}
tutarsız MRO
''',
    why="D'nin MRO'su B'yi C'den önce, A'yı ikisinden sonra sıralar. D().hello() zinciri bu sırayı izledi: B'deki super() A'ya değil C'ye gitti, A yalnızca bir kez göründü. B tek başına incelenince MRO'su B, A, object'tir; yani aynı sınıfta super()'in kime gittiği nesnenin gerçek sınıfına bağlıdır. JsonMixin tek işli bir yardımcıdır. Bad(A, B) tanımı A'yı B'den önce istediği için tutarsızdır.",
    alternatives=[
        "Çoklu kalıtım yerine composition ve açık işlev çağrıları çoğu zaman daha anlaşılır olur.",
        "Mixin kullanacaksan durumsuz (öznitelik tanımlamayan) ve tek işli tut; adını Mixin ile bitir.",
    ],
    traps=[
        "super()'i 'tek üst sınıf' sanmak: çoklu kalıtımda sıradaki sınıf sana bilinmeyen bir kardeş olabilir.",
        "Zincirdeki bir sınıfta super().__init__()'i çağırmayı unutmak; MRO'daki sonraki sınıflar kurulmaz.",
        "Sınıf başlığındaki sırayı önemsiz saymak: class D(B, C) ile class D(C, B) farklı davranır.",
        "Aynı adlı metotları çok sayıda üst sınıfa dağıtıp hangisinin çalıştığını izleyemez hâle gelmek.",
    ],
    realCode=r'''
class Base:
    def __init__(self, **kwargs):
        print("Base")

class Timestamped(Base):
    def __init__(self, **kwargs):
        print("Timestamped")
        super().__init__(**kwargs)

class Named(Base):
    def __init__(self, name, **kwargs):
        print("Named", name)
        super().__init__(**kwargs)

class Record(Timestamped, Named):
    def __init__(self, **kwargs):
        print("Record")
        super().__init__(**kwargs)

Record(name="Ada")
''',
    realOutput=r'''
Record
Timestamped
Named Ada
Base
''',
    lineByLine=[
        "Record'un MRO'su Record, Timestamped, Named, Base, object'tir.",
        "Her __init__ kendi işini yapıp **kwargs ile geri kalanı super()'e iletir (işbirlikçi kalıtım).",
        "Timestamped, name'i tanımaz ama kwargs içinde Named'e iletir; Named bu argümanı alır.",
        "Base her kurulum zincirinde yalnızca bir kez, en sonda çalışır.",
    ],
    sources=[
        {"title": "Python 3.12 · Çoklu kalıtım", "url": TUTORIAL + "#multiple-inheritance"},
        {"title": "Python 3.12 · Python 2.3 Method Resolution Order (C3)", "url": "https://docs.python.org/3.12/howto/mro.html"},
    ],
)

section(
    id="dataclass",
    title="dataclass",
    eyebrow="Veri sınıfını birkaç satırda kur",
    objectives=[
        "@dataclass ile __init__, __repr__ ve __eq__'in alan tanımlarından üretildiğini gösterir; varsayılan değer, field(default_factory=...) ve değiştirilebilir varsayılan hatasını açıklar.",
        "frozen=True, order=True ve __post_init__ ile değiştirilemez, sıralanabilir ve doğrulamalı veri sınıfı kurar; anotasyonun çalışma anında tür denetlemediğini bilir.",
    ],
    prerequisites=["m11:class-object", "m6:mutable-default"],
    summary="@dataclass, sınıf gövdesindeki alan anotasyonlarından __init__, __repr__ ve __eq__ üretir. field(default_factory=list), order=True, frozen=True ve __post_init__ ile veri sınıfı ihtiyaca göre ayarlanır. Anotasyonlar alanları belirler, değerleri denetlemez.",
    explanation=(
        "Yalnızca veri taşıyan sınıfta __init__, __repr__ ve __eq__ yazmak sıkıcı ve hataya açıktır. from dataclasses import dataclass ile sınıfa @dataclass eklersen ad: tür biçimindeki her anotasyon bir alan olur ve Python bu üç metodu senin yerine yazar: Task(2, 'rapor') kurulur, print Task(priority=2, title='rapor', ...) gösterir, == alan alan karşılaştırır (yalnızca aynı sınıfın nesneleri eşit olabilir). "
        "Anotasyondaki tür yalnızca belgedir: Task('x', 5) hata vermez; türleri denetlemek için ayrı araçlar gerekir (M14). Varsayılan değer yazılır (done: bool = False); varsayılanlı alan varsayılansızdan sonra gelmelidir. "
        "Liste, sözlük, küme gibi değiştirilebilir varsayılan değer yasaktır: tags: list = [] sınıf tanımı sırasında ValueError verir, çünkü bütün nesneler aynı listeyi paylaşırdı (M6'daki varsayılan argüman tuzağı). Çözüm field(default_factory=list): her nesne için yeni bir liste kurulur. field(compare=False) bir alanı karşılaştırmadan çıkarır, field(init=False) onu __init__'in dışında tutar. "
        "@dataclass(order=True) alanların tanım sırasıyla <, <=, >, >= üretir (sorted çalışır). @dataclass(frozen=True) alanlara atamayı yasaklar (FrozenInstanceError) ve __hash__ üretir; değiştirilemez nesne sözlük anahtarı olabilir. frozen olmayan, eq'su açık dataclass'ta __hash__ None olur. "
        "__post_init__, __init__ alanları atadıktan sonra çalışır: doğrulama ve türetilmiş değerler için kullanılır. dataclasses.replace(nesne, alan=yeni) değiştirilmiş bir kopya üretir (frozen nesnelerde değişim yolu), asdict sözlüğe çevirir. Davranışı çok, kuralı sıkı sınıflarda normal sınıf, değişmez demet gibi kullanılacak küçük kayıtlarda namedtuple (M10) da seçenektir."
    ),
    code=r'''
from dataclasses import dataclass, field, replace, asdict

@dataclass(order=True)
class Task:
    priority: int
    title: str
    tags: list = field(default_factory=list, compare=False)
    done: bool = field(default=False, compare=False)

    def __post_init__(self):
        if self.priority < 1:
            raise ValueError("öncelik 1 veya daha büyük olmalı")

t1 = Task(2, "rapor")
t2 = Task(1, "test", ["acil"])
print(t1)
print(t1 == Task(2, "rapor"), t1 == Task(2, "rapor", ["x"]))
print(sorted([t1, t2])[0].title)
t1.tags.append("haftalık")
print(Task(3, "yeni").tags, t1.tags)
print(asdict(replace(t2, done=True)))
try:
    Task(0, "hatalı")
except ValueError as error:
    print(error)
''',
    expectedOutput=r'''
Task(priority=2, title='rapor', tags=[], done=False)
True True
test
[] ['haftalık']
{'priority': 1, 'title': 'test', 'tags': ['acil'], 'done': True}
öncelik 1 veya daha büyük olmalı
''',
    why="Tek dekoratör __init__, __repr__, __eq__ ve sıralama metotlarını üretti. tags ve done compare=False olduğu için karşılaştırmaya ve sıralamaya girmedi (üçüncü satırda tags farklı olsa da eşit çıktı). default_factory her nesneye ayrı bir liste verdi: t1.tags değişince yeni Task'ın listesi etkilenmedi. replace değiştirilmiş bir kopya üretti ve __post_init__ hatalı önceliği reddetti.",
    alternatives=[
        "Değişmez, demet gibi küçük kayıtlar için collections.namedtuple (M10) ya da typing.NamedTuple de olur.",
        "Kuralları sıkı, davranışı çok olan bir sınıfı dataclass yapmak yerine normal sınıf ve property ile yaz (M11).",
    ],
    traps=[
        "tags: list = [] yazmak: ValueError verir; field(default_factory=list) gerekir.",
        "Anotasyonun türü denetlediğini sanmak: Task('x', 'y') hata vermeden kurulur.",
        "Varsayılanlı alanı varsayılansızdan önce yazmak (TypeError).",
        "frozen=True nesnenin içindeki listenin de değişmez olduğunu sanmak; yalnızca alana atama engellenir.",
    ],
    realCode=r'''
from dataclasses import dataclass, FrozenInstanceError

@dataclass(frozen=True)
class Point:
    x: int
    y: int

p = Point(1, 2)
try:
    p.x = 5
except FrozenInstanceError:
    print("değiştirilemez")
print({p: "başlangıç"}[Point(1, 2)], hash(p) == hash(Point(1, 2)))
print(Point(1, 2) == (1, 2))
''',
    realOutput=r'''
değiştirilemez
başlangıç True
False
''',
    lineByLine=[
        "frozen=True alanlara atamayı engeller; p.x = 5 FrozenInstanceError verir.",
        "Dondurulmuş dataclass hash üretir, bu yüzden Point sözlük anahtarı olabilir; eşit iki Point aynı hash'e sahiptir.",
        "Point(1, 2) == (1, 2) yanlıştır: dataclass'ın eşitliği yalnızca aynı sınıfın nesnelerini karşılaştırır.",
        "Alan değeri değiştirmek gerekirse dataclasses.replace ile yeni nesne üretilir.",
    ],
    sources=[
        {"title": "Python 3.12 · dataclasses", "url": "https://docs.python.org/3.12/library/dataclasses.html"},
    ],
)

section(
    id="slots",
    title="__slots__ ve slots=True",
    eyebrow="Bellek ve öznitelik denetimi",
    objectives=[
        "__slots__ ile örnek sözlüğünün (__dict__) yerine sabit öznitelik listesi kurar ve slotlu nesneye yeni öznitelik eklenemediğini (AttributeError) gösterir.",
        "@dataclass(slots=True) kullanır ve kalıtımda __slots__'un alt sınıfta tekrarlanmazsa __dict__'in geri geldiğini bilir; bellek kazancını varsaymak yerine ölçmek gerektiğini açıklar.",
    ],
    prerequisites=["dataclass", "m11:instance-class-vars"],
    summary="Normalde her nesne özniteliklerini kendi __dict__ sözlüğünde tutar. __slots__ = ('x', 'y') yalnızca bu adlara yer ayırır ve sözlüğü kaldırır: milyonlarca küçük nesnede bellek azalır, yazım hatasıyla yeni öznitelik eklemek ise hata verir.",
    explanation=(
        "Sıradan bir nesnenin öznitelikleri __dict__ adlı sözlükte durur; bu esnektir (p.z = 3 yeni öznitelik ekler) ama her nesne için bir sözlük demektir. Sınıfa __slots__ = ('x', 'y') yazarsan Python yalnızca bu iki öznitelik için yer ayırır, nesnenin __dict__'i olmaz. Sonuçlar: bellek kullanımı genelde azalır (özellikle çok sayıda küçük nesnede), nesne yalnızca tanımlı öznitelikleri alır ve p.spead = 5 gibi yazım hataları AttributeError ile hemen yakalanır. "
        "Kalıtımda dikkat: alt sınıf kendi __slots__'unu yazmazsa __dict__ geri gelir ve kazanç kaybolur. Slotlu sınıflarda vars(nesne) çalışmaz (nesnede __dict__ yok), zayıf referans için __weakref__ ayrıca eklenmelidir ve varsayılan değerli sınıf düzeyi öznitelikle aynı adlı slot çakışır. "
        "dataclass bunu kolaylaştırır: @dataclass(slots=True) (Python 3.10+) alanlardan slotları üretir ve varsayılan değerlerle de sorunsuz çalışır. "
        "Bellek kazancını tahmin etme, ölç: tracemalloc ya da sys.getsizeof ile gerçek veride karşılaştır. Bayt değerleri Python sürümüne ve platforma bağlı olduğu için bu sitede kesin bayt sayısı göstermiyoruz. Çoğu sınıfta fark küçüktür; asıl yarar çok nesne üretilen yerlerde ve öznitelik kümesini sabitlemek istediğinde ortaya çıkar."
    ),
    code=r'''
from dataclasses import dataclass

class Plain:
    def __init__(self, x, y):
        self.x, self.y = x, y

class Slotted:
    __slots__ = ("x", "y")

    def __init__(self, x, y):
        self.x, self.y = x, y

@dataclass(slots=True)
class Compact:
    x: int
    y: int = 0

p, s, c = Plain(1, 2), Slotted(1, 2), Compact(1)
print(hasattr(p, "__dict__"), hasattr(s, "__dict__"), hasattr(c, "__dict__"))
p.z = 3
print(p.z)
for obj in (s, c):
    try:
        obj.z = 3
    except AttributeError:
        print(type(obj).__name__, "yeni öznitelik eklenemez")
print(c, Compact.__slots__)

class Child(Slotted):
    pass

print(hasattr(Child(1, 2), "__dict__"))
''',
    expectedOutput=r'''
True False False
3
Slotted yeni öznitelik eklenemez
Compact yeni öznitelik eklenemez
Compact(x=1, y=0) ('x', 'y')
True
''',
    why="Plain nesnesinin __dict__'i olduğu için p.z = 3 çalıştı; Slotted ve Compact nesnelerinde __dict__ yoktur ve yeni öznitelik AttributeError verdi. dataclass(slots=True) slotları alanlardan üretti, varsayılan değer de çalıştı. Child kendi __slots__'unu yazmadığı için __dict__ geri geldi: kazanç kalıtımda tekrar tanımlama ister.",
    alternatives=[
        "Bellek sorunu yoksa __slots__ yazma; okunabilirlik ve esneklik çoğu zaman daha değerlidir.",
        "Çok sayıda kayıt tutacaksan tuple, namedtuple ya da kolonlu yapılar (NumPy gibi) daha da az yer kaplayabilir.",
    ],
    traps=[
        "Alt sınıfta __slots__ yazmayıp __dict__'in geri geldiğini fark etmemek.",
        "Slotlu nesnede vars() ya da keyfi öznitelik atamayı denemek.",
        "Kazancı ölçmeden varsaymak; küçük veride fark ihmal edilebilir.",
        "Elle yazılmış __slots__ ile aynı adlı varsayılan değerli sınıf özniteliğini birlikte kullanmak (ValueError); dataclass(slots=True) bunu çözer.",
    ],
    realCode=r'''
class Particle:
    __slots__ = ("x", "y", "speed")

    def __init__(self, x, y, speed=1):
        self.x, self.y, self.speed = x, y, speed

    def move(self):
        self.x += self.speed

dot = Particle(0, 0, 2)
dot.move()
print(dot.x, dot.speed)
try:
    dot.spead = 5
except AttributeError:
    print("yazım hatası yakalandı")
''',
    realOutput=r'''
2 2
yazım hatası yakalandı
''',
    lineByLine=[
        "__slots__ nesnenin taşıyabileceği üç özniteliği sabitler; nesne başına sözlük yoktur.",
        "move tanımlı özniteliği değiştirir; hareket sonrası x iki olur.",
        "dot.spead yazımı tanımlı bir slot olmadığı için AttributeError verir.",
        "Aynı hata sıradan bir sınıfta sessizce yeni bir öznitelik yaratırdı ve hata daha geç ortaya çıkardı.",
    ],
    sources=[
        {"title": "Python 3.12 · __slots__", "url": DATAMODEL + "#slots"},
        {"title": "Python 3.12 · dataclass(slots=True)", "url": "https://docs.python.org/3.12/library/dataclasses.html#dataclasses.dataclass"},
    ],
)

section(
    id="descriptor-metaclass",
    title="Descriptor ve metaclass (tanıma)",
    eyebrow="Sihrin arkasındaki mekanizmaları tanı",
    objectives=[
        "property, classmethod ve fonksiyon metotlarının descriptor protokolünü (__get__ / __set__) kullandığını söyler ve kısa bir descriptor sınıfını okuyup ne yaptığını açıklar.",
        "Her sınıfın bir metaclass'ı olduğunu (varsayılan type), __init_subclass__'in çoğu metaclass ihtiyacını karşıladığını ve bu araçların ne zaman kaçınılması gerektiğini tanır.",
    ],
    prerequisites=["m11:property", "dunder-basics"],
    summary="Descriptor, __get__/__set__ metotları olan ve sınıf özniteliği olarak duran bir nesnedir; öznitelik erişimini yakalar (property de budur). Metaclass sınıfı yaratan sınıftır; varsayılanı type'tır. İkisini de çerçeve kodunda tanımak yeterlidir, günlük kodda gerekmez.",
    explanation=(
        "Bu bölüm tanıma düzeyindedir: yazmak yerine gördüğünde ne olduğunu anlamak hedeflenir. "
        "Descriptor: bir sınıfın gövdesinde, __get__, __set__ ya da __delete__ metotları olan bir nesneyi sınıf özniteliği olarak tutarsan, o ada her erişimde (nesne.ad, nesne.ad = değer) Python bu metodu çağırır. M11'deki property aslında yerleşik bir descriptor'dır; classmethod, staticmethod ve sıradan fonksiyonlar da (nesneye bağlı metot oluşturmak için) descriptor protokolünü kullanır. Kendi descriptor'ünü, aynı doğrulama kuralını birçok alanda tekrar etmek istediğinde yazarsın: Positive() ile hem price hem qty doğrulanır. "
        "__set_name__(self, owner, name) sınıf kurulurken descriptor'a hangi adla bağlandığını söyler. Önemli ayrıntı: descriptor nesnesi sınıfta tek durur, bu yüzden nesneye özel değeri descriptor'ün içinde değil, nesnenin kendisinde (_price gibi başka bir adda) saklamalıdır; aksi hâlde tüm nesneler aynı değeri paylaşır. __set__ tanımlı descriptor'a veri descriptor'ü denir ve nesnenin kendi __dict__'inden önceliklidir. "
        "Metaclass: Python'da sınıfların kendisi de nesnedir ve bir sınıftan üretilirler; bu sınıfa metaclass denir, varsayılanı type'tır (type(Item) type verir). class Base(metaclass=Registry): ile sınıf yaratılışını özelleştirebilirsin; Django modelleri, ORM'ler, enum ve abc bu mekanizmayı kullanır. type('Dog', (), {...}) ile çalışma anında sınıf da yaratılabilir. "
        "Günlük kodda bunlara gerek yok: alt sınıf kaydı gibi işlerin çoğunu __init_subclass__ (bir sınıf türetildiğinde çağrılır) ya da sınıf dekoratörü çok daha sade yapar. Karşılaştığında tanı, anla, ama kendi kodunda yalnızca gerçekten bu kadar gerekli olduğunda kullan."
    ),
    code=r'''
class Positive:
    def __set_name__(self, owner, name):
        self.name = "_" + name

    def __get__(self, obj, owner=None):
        if obj is None:
            return self
        return getattr(obj, self.name)

    def __set__(self, obj, value):
        if value <= 0:
            raise ValueError(f"{self.name[1:]} pozitif olmalı")
        setattr(obj, self.name, value)

class Item:
    price = Positive()
    qty = Positive()

    def __init__(self, price, qty):
        self.price = price
        self.qty = qty

item = Item(10, 3)
print(item.price * item.qty, vars(item))
try:
    item.qty = 0
except ValueError as error:
    print(error)
print(type(Item.price).__name__, type(item).__name__, type(Item).__name__)
''',
    expectedOutput=r'''
30 {'_price': 10, '_qty': 3}
qty pozitif olmalı
Positive Item type
''',
    why="price ve qty aynı Positive descriptor sınıfının iki örneğidir. self.price = price satırı Positive.__set__'e gitti, doğruladı ve değeri nesnenin _price özniteliğinde sakladı (vars bunu gösterir). item.price okuması __get__'e gitti. Sınıf özniteliği Item.price bir Positive nesnesidir; Item'ın kendisinin türü ise type'tır, yani metaclass'ı varsayılandır.",
    alternatives=[
        "Tek bir alan için doğrulama gerekiyorsa descriptor yerine property yeterlidir (M11).",
        "Birçok alanda aynı doğrulama gerekiyorsa descriptor yerine dataclass'ta __post_init__ ya da pydantic gibi bir doğrulama kütüphanesi düşünülebilir (M18'de tanıyacaksın).",
    ],
    traps=[
        "Descriptor içinde nesneye özel değeri self.value gibi descriptor'ün kendisinde saklamak: bütün nesneler aynı değeri görür.",
        "Descriptor'ü __init__ içinde self.x = Positive() ile oluşturmak: descriptor yalnızca sınıf özniteliği olarak çalışır.",
        "Metaclass yazmak için acele etmek: önce __init_subclass__ ya da sınıf dekoratörü yeter mi diye bak.",
        "type(x) ile x.__class__ ya da metaclass kavramlarını karıştırmak; her sınıfın bir metaclass'ı vardır, çoğunlukla type.",
    ],
    realCode=r'''
class Registry(type):
    names = []

    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)
        Registry.names.append(name)
        return cls

class Base(metaclass=Registry):
    pass

class Plugin(Base):
    pass

class Easy:
    names = []

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        Easy.names.append(cls.__name__)

class First(Easy):
    pass

class Second(Easy):
    pass

Dog = type("Dog", (), {"sound": lambda self: "hav"})
print(Registry.names, Easy.names)
print(Dog().sound(), type(Dog).__name__)
''',
    realOutput=r'''
['Base', 'Plugin'] ['First', 'Second']
hav type
''',
    lineByLine=[
        "Registry metaclass'ı her sınıf yaratıldığında adını listeye ekler; Base ve Plugin kaydolur.",
        "Easy aynı işi __init_subclass__ ile yapar: yalnızca alt sınıflar (First, Second) kaydolur, çok daha az kodla.",
        "type('Dog', (), {...}) çalışma anında sınıf yaratır: yazılmış bir class bloğunun yaptığı iş budur.",
        "Dog sınıfının türü type'tır; yani Dog, type'ın bir örneğidir.",
    ],
    sources=[
        {"title": "Python 3.12 · Descriptor nasıl kullanılır", "url": "https://docs.python.org/3.12/howto/descriptor.html"},
        {"title": "Python 3.12 · Veri modeli: metaclass'lar", "url": DATAMODEL + "#metaclasses"},
    ],
)
