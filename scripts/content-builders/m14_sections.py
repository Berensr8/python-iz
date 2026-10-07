"""M14 (Type hints) lesson sections. Imported by build_m14.py."""

TYPING = "https://docs.python.org/3.12/library/typing.html"


def c(text):
    return text.strip("\n")


sections = []


def section(**fields):
    for key in ("code", "expectedOutput", "realCode", "realOutput"):
        fields[key] = c(fields[key])
    fields.setdefault("runtime", "browser")
    sections.append(fields)


section(
    id="annotations-basics",
    title="Tip ipuçlarının temeli",
    eyebrow="Kodun ne beklediğini yaz",
    objectives=[
        "Parametrelere, dönüş değerine ve değişkenlere tip ipucu (annotation) yazar ve fonksiyonun __annotations__ sözlüğünde saklandığını gösterir.",
        "Tip ipuçlarının çalışma anında denetlenmediğini ve değer dönüştürmediğini açıklar; ne işe yaradıklarını (okunurluk, editör, statik denetleyici) bilir.",
    ],
    prerequisites=["m6:def-return", "m1:variables-types"],
    summary="def greet(name: str) -> str: name'in metin, dönüşün metin olması beklendiğini söyler. Python bu bilgiyi saklar ama çalışma anında denetlemez: greet(5) yine çalışır. Tip ipuçları okuyan insanlar, editörler ve mypy gibi araçlar içindir.",
    explanation=(
        "Tip ipucu (type hint, annotation), bir adın hangi türde değer taşımasının beklendiğini yazmanın yoludur. Parametreden sonra iki nokta ve tür (name: str), varsayılanla birlikte (excited: bool = False), dönüş türü için -> (-> str) yazılır. Değişkenlere de yazılabilir: count: int = 3. Yalnızca anotasyon yazıp değer vermek (count: int) değişken oluşturmaz. "
        "Python bu bilgiyi fonksiyonun __annotations__ sözlüğünde saklar ama çalışma anında hiçbir şeyi denetlemez ve dönüştürmez: double(n: int) fonksiyonuna 'ab' verirsen 'abab' döner, total: int = 'on' hata vermez. Tip ipucu bir sözleşmedir, bir kural motoru değildir. "
        "O hâlde ne işe yarar? Kodu okuyan kişi fonksiyonun neyi beklediğini hemen görür; editör otomatik tamamlama ve uyarı verir; mypy ya da pyright gibi statik denetleyiciler programı çalıştırmadan uyumsuzlukları bulur (bu modülün son bölümü). Yapay zekânın ürettiği kodu incelerken tip ipuçları niyeti okumanın en hızlı yoludur. "
        "Tip ipuçları isteğe bağlıdır ve kademeli eklenebilir: önce genel fonksiyonların imzalarından başla. Yerel değişkenlerin çoğuna yazmaya gerek yoktur; denetleyici sağdaki değerden türü çıkarır."
    ),
    code=r'''
def greet(name: str, excited: bool = False) -> str:
    return f"Merhaba {name}" + ("!" if excited else ".")

def double(n: int) -> int:
    return n * 2

print(greet("Ada"))
print(greet.__annotations__)
print(double(4), double("ab"))
total: int = "on"
print(total, type(total))
''',
    expectedOutput=r'''
Merhaba Ada.
{'name': <class 'str'>, 'excited': <class 'bool'>, 'return': <class 'str'>}
8 abab
on <class 'str'>
''',
    why="İpuçları __annotations__ sözlüğünde saklandı ama hiçbiri çalışma anında uygulanmadı: double'a metin verildiğinde * tekrar etme işlemi yaptı ve 'abab' döndü; int olarak işaretlenen total bir str'ye bağlandı. Bu hataları yakalamak statik denetleyicinin işidir.",
    alternatives=[
        "Uyumsuzlukları çalıştırmadan bulmak için mypy ya da editörün yerleşik denetleyicisini (Pylance/pyright) kullan.",
        "Dışarıdan gelen veriyi (kullanıcı girdisi, JSON) gerçekten doğrulamak için isinstance denetimi ya da doğrulama kütüphanesi gerekir (bu modülün son bölümü).",
    ],
    traps=[
        "Tip ipucunun değeri dönüştürdüğünü sanmak: age: int yazmak input()'tan gelen metni sayıya çevirmez.",
        "Tip ipucunun yanlış türde çağrıyı engellediğini sanmak; Python çalıştırır, hata sonra ve başka bir yerde çıkar.",
        "count: int yazınca count'un 0 olarak tanımlandığını sanmak (değer verilmedikçe ad yoktur).",
        "Varsayılanlı parametrede sırayı karıştırmak: excited: bool = False doğru, excited = False: bool sözdizimi hatasıdır.",
    ],
    realCode=r'''
def average(scores: list[int]) -> float:
    if not scores:
        return 0.0
    return sum(scores) / len(scores)

def describe(name: str, scores: list[int]) -> str:
    return f"{name}: {average(scores):.1f}"

print(describe("Ada", [90, 85, 77]))
print(describe("Can", []))
''',
    realOutput=r'''
Ada: 84.0
Can: 0.0
''',
    lineByLine=[
        "average bir tam sayı listesi alır ve float döndürür; imza bunu belgeler.",
        "Boş liste için 0.0 döndürmek, dönüş türünün her yolda float olmasını sağlar.",
        "describe'ın imzası, iki parametreyi ve metin döndüreceğini tek satırda anlatır.",
        "İpuçları çalışmayı değiştirmez; çıktı ipuçsuz sürümle aynıdır.",
    ],
    sources=[
        {"title": "Python 3.12 · typing (giriş)", "url": TYPING},
        {"title": "Python 3.12 · Fonksiyon anotasyonları", "url": "https://docs.python.org/3.12/tutorial/controlflow.html#function-annotations"},
    ],
)

section(
    id="collection-types",
    title="Koleksiyon tipleri",
    eyebrow="list[int], dict[str, float] ve geniş parametre tipleri",
    objectives=[
        "list[int], dict[str, list[int]], set[str], tuple[int, int] ve tuple[int, ...] yazımlarını okur ve yazar.",
        "Parametrelerde geniş (Iterable, Sequence, Mapping), dönüşte kesin (list, dict) tip kullanmanın nedenini açıklar.",
    ],
    prerequisites=["annotations-basics", "m4:dicts", "m13:iterator-protocol"],
    summary="Kap türlerinin içindeki öğe türü köşeli parantezle yazılır: list[int], dict[str, float], tuple[int, str]. Değişken uzunluklu tuple tuple[int, ...] olur. Parametre için collections.abc.Iterable gibi geniş türler, fonksiyonu daha çok çağırana açık tutar.",
    explanation=(
        "Python 3.9'dan beri yerleşik türler köşeli parantezle parametrelenir: list[int] tam sayılar listesi, dict[str, list[int]] metinden tam sayı listesine sözlük, set[str] metin kümesi demektir. tuple biraz farklıdır: tuple[int, str] tam iki öğeli (int, str) demettir; tuple[int, ...] ise her uzunlukta tam sayı demetidir. Eski kodlarda typing modülünden List[int], Dict[str, int] yazımını görürsün; anlamı aynıdır, yeni kodda yerleşik yazımı kullan. "
        "Bu yazımlar da yalnızca bilgidir: list[int] çalışma anında bir 'tip nesnesidir', listedeki öğeleri denetlemez. "
        "Parametrelerde gerektiğinden dar tip istemek fonksiyonun kullanımını kısıtlar. Fonksiyon yalnızca öğeleri dolaşıyorsa collections.abc.Iterable[float] iste: liste, demet, küme, range ve generator (M13) hepsi kabul edilir. İndeks ve len gerekiyorsa Sequence, sözlük gibi okuma yapıyorsan Mapping iste. Dönüş tipinde ise kesin ol (list[str], dict[str, int]): çağıran, eline geçen nesneyle neler yapabileceğini bilsin. "
        "Karmaşık tipleri okunur tutmak için takma ad (alias) tanımlayabilirsin: Scores = dict[str, list[int]]. Python 3.12 bunun için type Scores = dict[str, list[int]] yazımını da getirdi."
    ),
    code=r'''
from collections.abc import Iterable, Mapping

def total(prices: Iterable[float]) -> float:
    return sum(prices)

def lookup(stock: Mapping[str, int], name: str) -> int:
    return stock.get(name, 0)

point: tuple[int, int] = (3, 4)
scores: dict[str, list[int]] = {"Ada": [90, 85]}
tags: set[str] = {"python", "tip"}
print(total([1.5, 2.5]), total((10, 20)), total(x / 2 for x in range(3)))
print(lookup({"kalem": 3}, "silgi"))
print(list[int], dict[str, list[int]], tuple[int, ...])
print(sorted(tags), point, scores["Ada"])
''',
    expectedOutput=r'''
4.0 30 1.5
0
list[int] dict[str, list[int]] tuple[int, ...]
['python', 'tip'] (3, 4) [90, 85]
''',
    why="Iterable[float] isteyen total; listeyi, demeti ve bir generator'ı aynı şekilde kabul etti. Mapping isteyen lookup sözlükle çalıştı. Koleksiyon tipleri yazdırıldığında kendi gösterimleriyle görünür: bunlar çalışma anında değer denetlemeyen tip nesneleridir.",
    alternatives=[
        "Uzun bir tipi tekrar tekrar yazmak yerine bir ad ver: Scores = dict[str, list[int]].",
        "Sabit alanlı kayıtlar için dict[str, object] yerine TypedDict ya da dataclass kullan (sonraki bölümler, M12).",
    ],
    traps=[
        "Sözlük tipini dict[str: int] diye yazmak; doğru yazım dict[str, int] (iki nokta dilim üretir).",
        "Yalnızca dolaşan bir fonksiyonda list[float] isteyip demet ya da generator verenleri gereksiz yere uyumsuz saymak.",
        "tuple[int] ile tuple[int, ...]'ı karıştırmak: ilki tam bir öğeli demettir.",
        "Yeni kodda typing.List, typing.Dict kullanmak; Python 3.9+ yerleşik list, dict yazımını destekler.",
    ],
    realCode=r'''
def group_by_city(people: list[tuple[str, str]]) -> dict[str, list[str]]:
    groups: dict[str, list[str]] = {}
    for name, city in people:
        groups.setdefault(city, []).append(name)
    return groups

print(group_by_city([("Ada", "İzmir"), ("Can", "Ankara"), ("Eda", "İzmir")]))
''',
    realOutput=r'''
{'İzmir': ['Ada', 'Eda'], 'Ankara': ['Can']}
''',
    lineByLine=[
        "Parametre (ad, şehir) demetlerinden oluşan bir listedir.",
        "Dönüş türü, şehirden ad listesine giden bir sözlüktür.",
        "Boş sözlüğe tip ipucu yazmak, denetleyicinin içine ne konacağını bilmesini sağlar.",
        "İmza okununca gövdeye bakmadan ne girip ne çıktığı anlaşılır.",
    ],
    sources=[
        {"title": "Python 3.12 · Genel (generic) yerleşik tipler", "url": "https://docs.python.org/3.12/library/stdtypes.html#types-genericalias"},
        {"title": "Python 3.12 · collections.abc", "url": "https://docs.python.org/3.12/library/collections.abc.html"},
    ],
)

section(
    id="optional-union",
    title="Optional, Union ve |",
    eyebrow="Değer olmayabilir ya da birden çok türde olabilir",
    objectives=[
        "int | None (Optional[int]) ve int | str (Union[int, str]) yazımlarını okur, birbirine eşit olduklarını bilir.",
        "None olabilecek bir değeri kullanmadan önce denetler (daraltma) ve None döndürebilen fonksiyonun dönüş tipini doğru yazar.",
    ],
    prerequisites=["annotations-basics", "m5:identity-equality"],
    summary="int | None, değerin ya int ya da None olabileceğini söyler; eski yazımı Optional[int]'tir. int | float gibi birleşimler Union'dır. None olabilecek bir değeri kullanmadan önce if value is None ile denetlemek gerekir; denetleyici bu kontrolden sonra türü daraltır.",
    explanation=(
        "Bir fonksiyon bazen sonuç bulamaz: find_index aranan öğe yoksa None döndürür. Dönüş türü bu yüzden int değil int | None'dır. Python 3.10'dan beri | işareti kullanılır; eski kodda Optional[int] (yani Union[int, None]) ve Union[int, str] görürsün. Hepsi aynı anlamdadır ve birbirine eşittir. "
        "Optional adı yanıltıcıdır: parametrenin isteğe bağlı olduğunu değil, None olabileceğini söyler. Varsayılanı None olan parametre için doğru yazım port: int | None = None'dır. "
        "None olabilecek bir değeri doğrudan kullanmak (sonuc.upper(), index + 1) çalışma anında AttributeError ya da TypeError verir. Bunu önlemek için önce denetle: if index is None: return 'yok'. Bu kontrolden sonra mypy, index'in artık int olduğunu bilir; buna tip daraltma (narrowing) denir. isinstance(value, str) de daraltır. "
        "Birleşimleri gerektiğinde kullan ama çok geniş birleşimler (int | str | list | None) kullanımı zorlaştırır; çoğu zaman tek bir türe dönüştürmek ya da ayrı fonksiyonlar yazmak daha temizdir. Eksik bulgu için None döndürmek yerine hata fırlatmak da bir tasarım seçeneğidir (M7)."
    ),
    code=r'''
from typing import Optional, Union

def find_index(items: list[str], target: str) -> int | None:
    for index, item in enumerate(items):
        if item == target:
            return index
    return None

def parse_amount(text: str) -> int | float:
    return float(text) if "." in text else int(text)

def label(index: int | None) -> str:
    if index is None:
        return "yok"
    return f"#{index + 1}"

names = ["ada", "can"]
print(find_index(names, "can"), find_index(names, "eda"))
print(label(find_index(names, "can")), label(find_index(names, "eda")))
print(parse_amount("3"), parse_amount("2.5"))
print(Optional[int] == (int | None), Union[int, str] == (int | str))
''',
    expectedOutput=r'''
1 None
#2 yok
3 2.5
True True
''',
    why="find_index bulamadığında None döndürdü; dönüş tipi bunu açıkça söylüyor. label önce None'ı ayırdı, sonra index'i sayı olarak kullandı. parse_amount girdiye göre int ya da float döndürdü. Son satır eski ve yeni yazımların aynı tipi gösterdiğini doğrular.",
    alternatives=[
        "Bulunamama gerçekten bir hataysa None yerine özel bir hata fırlat (M7); çağıranlar None denetimini unutamaz.",
        "Varsayılan bir değer anlamlıysa dict.get(anahtar, varsayılan) gibi None yerine o değeri döndür.",
    ],
    traps=[
        "None döndürebilen fonksiyonun dönüş tipini yalnızca int yazmak; mypy 'Missing return statement' ya da uyumsuzluk uyarısı verir.",
        "None olabilecek değeri denetlemeden kullanmak (AttributeError: 'NoneType' object has no attribute ...).",
        "Optional[int]'i 'parametre isteğe bağlı' diye okumak; isteğe bağlılığı varsayılan değer sağlar.",
        "if not value: ile None denetlemek; 0 ve boş metin de yanlış sayılır, kesin denetim için is None kullan.",
    ],
    realCode=r'''
def get_port(settings: dict[str, str], default: int | None = None) -> int | None:
    raw = settings.get("port")
    if raw is None:
        return default
    return int(raw)

print(get_port({"port": "8080"}), get_port({}), get_port({}, 80))
''',
    realOutput=r'''
8080 None 80
''',
    lineByLine=[
        "Ayar sözlüğü metin değerler taşır; port ayarı olmayabilir.",
        "settings.get bulunamazsa None döndürür; bu durum ayrıca ele alınır.",
        "Varsayılan da None olabildiği için dönüş tipi int | None'dır.",
        "Ayar varsa metin int'e çevrilir; tip ipucu bunu otomatik yapmaz.",
    ],
    sources=[
        {"title": "Python 3.12 · Union tipi (X | Y)", "url": "https://docs.python.org/3.12/library/stdtypes.html#types-union"},
        {"title": "Python 3.12 · typing.Optional", "url": TYPING + "#typing.Optional"},
    ],
)

section(
    id="typeddict",
    title="TypedDict",
    eyebrow="Sözlüğün şeklini tanımla",
    objectives=[
        "TypedDict ile anahtarları ve değer türleri belli bir sözlük şekli tanımlar; NotRequired ile isteğe bağlı anahtar belirtir.",
        "TypedDict'in çalışma anında sıradan bir dict olduğunu ve gelen veriyi doğrulamadığını açıklar; dataclass ile farkını bilir.",
    ],
    prerequisites=["collection-types", "m8:json", "m12:dataclass"],
    summary="JSON'dan gelen veri gibi sabit anahtarlı sözlükler için class Movie(TypedDict): title: str; year: int yazılır. Denetleyici yanlış anahtar ya da tür kullanımını bulur; çalışma anında ise nesne sıradan bir dict'tir ve hiçbir şey denetlenmez.",
    explanation=(
        "dict[str, object] bir sözlüğün hangi anahtarları taşıdığını anlatmaz. TypedDict bunu yapar: class Movie(TypedDict): gövdesine anahtarları ve türlerini yazarsın. Bir değişkene m: Movie = {...} dediğinde mypy eksik anahtarı, fazladan anahtarı ya da yanlış türü yakalar; editör de anahtar adlarını tamamlar. "
        "Varsayılan olarak bütün anahtarlar zorunludur. İsteğe bağlı bir anahtar için NotRequired[float] yaz (ya da sınıfa total=False ver ve zorunluları Required ile işaretle). Bu bilgi Movie.__required_keys__ ve __optional_keys__'te görünür. "
        "Önemli: TypedDict yalnızca statik bir tanımdır. Movie(...) ya da {...} ile oluşturulan nesne sıradan bir dict'tir; type() dict der, yanlış türde değer çalışma anında kabul edilir, eksik anahtar KeyError verir. json.loads ile gelen veriyi : Movie diye işaretlemek onu doğrulamaz; doğrulama ayrıca yapılmalıdır (bu modülün son bölümü, M18'de pydantic). "
        "Ne zaman hangisi? Veri zaten sözlük olarak geliyor ve sözlük olarak kalacaksa (JSON, API yanıtları) TypedDict; davranışı ve kuralları olan bir nesne istiyorsan dataclass (M12) ya da normal sınıf."
    ),
    code=r'''
from typing import TypedDict, NotRequired

class Movie(TypedDict):
    title: str
    year: int
    rating: NotRequired[float]

m: Movie = {"title": "Dune", "year": 2021}
print(m, type(m).__name__)
print(sorted(Movie.__required_keys__), sorted(Movie.__optional_keys__))
bad: Movie = {"title": "X", "year": "iki bin"}
print(bad["year"])
print(m.get("rating", "puan yok"))
''',
    expectedOutput=r'''
{'title': 'Dune', 'year': 2021} dict
['title', 'year'] ['rating']
iki bin
puan yok
''',
    why="m bir Movie olarak işaretlendi ama çalışma anında sıradan bir dict'tir. Sınıf, hangi anahtarların zorunlu hangisinin isteğe bağlı olduğunu saklar. year'ı metin olan bad sorunsuz oluştu; bu uyumsuzluğu yalnızca mypy yakalar. İsteğe bağlı rating için get ile varsayılan kullanıldı.",
    alternatives=[
        "Davranışı ve doğrulaması olan bir kayıt istiyorsan @dataclass kullan (M12).",
        "Dışarıdan gelen veriyi gerçekten doğrulamak için alanları elle denetle ya da pydantic gibi bir kütüphane kullan (M18).",
    ],
    traps=[
        "TypedDict'in JSON verisini doğruladığını sanmak; yanlış tür sessizce içeri girer.",
        "TypedDict'ten nesne kurup öznitelik erişimi beklemek (m.title); erişim sözlük gibi m['title'] ile yapılır.",
        "İsteğe bağlı anahtarı m['rating'] ile okuyup KeyError almak; get ya da in denetimi kullan.",
        "isinstance(x, Movie) denemek; TypedDict ile isinstance kullanılamaz (TypeError).",
    ],
    realCode=r'''
import json
from typing import TypedDict

class User(TypedDict):
    id: int
    name: str
    email: str

def parse_users(text: str) -> list[User]:
    return json.loads(text)

users = parse_users('[{"id": 1, "name": "Ada", "email": "ada@ornek.com"}]')
for user in users:
    print(user["id"], user["name"])
print(type(users[0]).__name__)
''',
    realOutput=r'''
1 Ada
dict
''',
    lineByLine=[
        "User, bir API'nin döndürdüğü kullanıcı kaydının şeklini tanımlar.",
        "parse_users'ın dönüş tipi, çağıranın hangi anahtarları kullanabileceğini söyler; editör user['na...] yazarken tamamlar.",
        "json.loads gerçek denetim yapmaz; veri şekle uymasa bile aynı list[dict] döner.",
        "Çalışma anında her kayıt sıradan bir dict'tir.",
    ],
    sources=[
        {"title": "Python 3.12 · typing.TypedDict", "url": TYPING + "#typing.TypedDict"},
    ],
)

section(
    id="protocol",
    title="Protocol: yapısal tipler",
    eyebrow="Duck typing'in tip denetleyiciye anlatılmış hâli",
    objectives=[
        "Protocol ile 'bu metotlara sahip olan her nesne' türünü tanımlar; sınıfların Protocol'den türemeden ona uyabildiğini gösterir.",
        "runtime_checkable ile isinstance denetiminin yalnızca adların varlığına baktığını, imza ve türleri denetlemediğini bilir; abc ile farkını açıklar.",
    ],
    prerequisites=["annotations-basics", "m12:polymorphism", "m12:abc"],
    summary="class Shape(Protocol): def area(self) -> float: ... yazınca, area metodu olan her sınıf bir Shape sayılır; türemeye gerek yoktur. Bu, M12'deki duck typing'in tip denetleyicinin anlayacağı biçimidir. abc kalıtım ister, Protocol ise yalnızca yapıya bakar.",
    explanation=(
        "M12'de duck typing'i gördün: area metodu olan her nesne aynı döngüde kullanılabiliyordu, ama bu arayüz hiçbir yerde yazılı değildi. abc arayüzü yazdırıyordu ama alt sınıfların ondan türemesini istiyordu. Protocol ikisinin ortasıdır: arayüzü yazarsın, sınıflar ondan türemek zorunda kalmaz. "
        "class Shape(Protocol): gövdesine beklenen metotların imzalarını yazarsın (gövde ... olur). Artık total_area(shapes: list[Shape]) imzası, area metodu uygun olan her sınıfın nesnesini kabul eder; Square, Shape'i hiç bilmese de uyar. Uymayan bir nesne verirsen mypy bunu çalıştırmadan söyler. Buna yapısal tipleme (structural typing) denir; abc'deki kalıtıma dayalı yaklaşım ise nominal tiplemedir. "
        "Protocol'ler çalışma anında da var olur ama varsayılan olarak isinstance ile kullanılamaz. @runtime_checkable eklersen isinstance çalışır; ancak bu denetim yalnızca adın var olup olmadığına bakar, imzayı, dönüş türünü hatta adın çağrılabilir olup olmadığını denetlemez. Protocol sınıfının kendisinden nesne üretilemez (TypeError). "
        "Ne zaman? Bir fonksiyonun yalnızca birkaç davranışa ihtiyacı varsa (yazılabilir bir şey, kapatılabilir bir kaynak, alanı hesaplanabilen bir şekil) Protocol iste; testlerde sahte nesneler vermek de kolaylaşır. Ortak kod paylaşacak ve alt sınıfları zorlayacaksan abc kullan."
    ),
    code=r'''
from typing import Protocol, runtime_checkable

@runtime_checkable
class Shape(Protocol):
    def area(self) -> float: ...

class Square:
    def __init__(self, side: int) -> None:
        self.side = side

    def area(self) -> float:
        return self.side ** 2

class Rectangle:
    def __init__(self, width: int, height: int) -> None:
        self.width, self.height = width, height

    def area(self) -> float:
        return self.width * self.height

class Robot:
    def walk(self) -> str:
        return "yürüyor"

def total_area(shapes: list[Shape]) -> float:
    return sum(shape.area() for shape in shapes)

print(total_area([Square(2), Rectangle(2, 3)]))
print(isinstance(Square(1), Shape), isinstance(Robot(), Shape))
print(issubclass(Square, Shape), Shape in Square.__mro__)
''',
    expectedOutput=r'''
10
True False
True False
''',
    why="Square ve Rectangle Shape'ten türemedi ama area metotları olduğu için Shape sayıldı; total_area ikisini de kabul etti. Robot'ta area olmadığı için isinstance False verdi. Son satır, uyumun kalıtımdan değil yapıdan geldiğini gösterir: Shape, Square'in MRO'sunda yoktur.",
    alternatives=[
        "Ortak davranış paylaşacak ve uygulamayı zorlayacaksan abc ile soyut sınıf yaz (M12).",
        "Arayüz tek bir çağrıdan ibaretse Callable (bu modülde) daha kısa olabilir.",
    ],
    traps=[
        "runtime_checkable isinstance denetiminin imzayı ya da türleri doğruladığını sanmak; yalnızca adın varlığına bakar.",
        "Protocol'den nesne üretmeye çalışmak (TypeError: Protocols cannot be instantiated).",
        "Protocol'ü kullanmak için sınıfların ondan türemesi gerektiğini sanmak.",
        "Metot adını ya da parametrelerini Protocol'dekinden farklı yazmak; mypy uyumsuzluk bildirir, çalışma anında ise AttributeError gelir.",
    ],
    realCode=r'''
from typing import Protocol

class Writer(Protocol):
    def write(self, text: str) -> None: ...

class Console:
    def write(self, text: str) -> None:
        print(text)

class Memory:
    def __init__(self) -> None:
        self.lines: list[str] = []

    def write(self, text: str) -> None:
        self.lines.append(text)

def report(writer: Writer, total: int) -> None:
    writer.write(f"toplam: {total}")

report(Console(), 42)
memory = Memory()
report(memory, 7)
print(memory.lines)
''',
    realOutput=r'''
toplam: 42
['toplam: 7']
''',
    lineByLine=[
        "Writer, report'un ihtiyaç duyduğu tek davranışı (write) tanımlar.",
        "Console ve Memory Writer'dan türemez; write metotları olduğu için uyarlar.",
        "Gerçek programda Console, testte Memory verilir: report'u değiştirmeden çıktı yakalanır.",
        "Memory'nin lines listesi, testin neyin yazıldığını denetlemesini sağlar.",
    ],
    sources=[
        {"title": "Python 3.12 · typing.Protocol", "url": TYPING + "#typing.Protocol"},
    ],
)

section(
    id="generics",
    title="Generics ve TypeVar",
    eyebrow="Türü sonradan belli olan kod",
    objectives=[
        "TypeVar ile 'girdi hangi türdeyse çıktı da o tür' ilişkisini kuran genel (generic) fonksiyon yazar.",
        "Generic[T] ile genel sınıf tanımlar, Box[int] gibi kullanır; bound ile tip değişkenini sınırlamayı ve Python 3.12'nin yeni yazımını tanır.",
    ],
    prerequisites=["collection-types", "m11:class-object"],
    summary="T = TypeVar('T') bir tip değişkenidir: def first(items: list[T]) -> T, int listesi verilirse int, str listesi verilirse str döndüğünü söyler. Sınıflar Generic[T] ile genel yapılır: Box[int] tam sayı tutan kutudur. Çalışma anında T hiçbir şeyi denetlemez.",
    explanation=(
        "Bazı fonksiyonlar türden bağımsız çalışır ama girdiyle çıktı arasında bir ilişki vardır: first, liste ne tutuyorsa onun bir öğesini döndürür. list[object] -> object yazsaydın bu ilişki kaybolurdu ve first([1, 2]) + 1 satırını denetleyici reddederdi. Tip değişkeni bu ilişkiyi yazar: T = TypeVar('T'), def first(items: list[T]) -> T. Denetleyici her çağrıda T'nin yerine geçen türü çıkarır. "
        "Sınıflar da genel olabilir: class Box(Generic[T]) içindeki T, nesne kurulurken belirlenir. box: Box[int] = Box(5) yazınca box.get() int döndürür. Yerleşik list[int], dict[str, int] de böyle genel sınıflardır. Birden çok tip değişkeni olabilir: Registry(Generic[K, V]). "
        "Tip değişkeni sınırlanabilir: TypeVar('N', int, float) yalnızca bu türlerden birini, TypeVar('T', bound=HasId) ise HasId'ye (ör. bir Protocol) uyan türleri kabul eder. "
        "Python 3.12 daha kısa bir yazım getirdi: def first[T](items: list[T]) -> T ve class Box[T]: (TypeVar tanımlamaya gerek kalmaz). Bu sitedeki Python 3.12 bunu çalıştırır ama 3.11 ve öncesinde sözdizimi hatasıdır; ikisini de okuyabilmen gerekir. Fonksiyonun __annotations__'ında tip değişkeni ~T olarak görünür."
    ),
    code=r'''
from typing import Generic, TypeVar

T = TypeVar("T")
Num = TypeVar("Num", int, float)

def first(items: list[T]) -> T:
    return items[0]

def pairwise(items: list[T]) -> list[tuple[T, T]]:
    return list(zip(items, items[1:]))

def biggest(a: Num, b: Num) -> Num:
    return a if a >= b else b

class Box(Generic[T]):
    def __init__(self, value: T) -> None:
        self.value = value

    def get(self) -> T:
        return self.value

print(first([3, 1, 2]), first(["a", "b"]))
print(pairwise([1, 2, 3]))
print(biggest(2, 7), biggest(1.5, 0.5))
box: Box[int] = Box(5)
print(box.get(), type(box).__name__, first.__annotations__)
''',
    expectedOutput=r'''
3 a
[(1, 2), (2, 3)]
7 1.5
5 Box {'items': list[~T], 'return': ~T}
''',
    why="first ve pairwise her türde listeyle çalıştı; ipuçları girdi ile çıktı arasındaki tür ilişkisini anlatır. biggest yalnızca int ya da float için tanımlandı. Box[int] ile kurulan kutu sıradan bir Box nesnesidir; T çalışma anında hiçbir şeyi denetlemez. Annotation sözlüğünde tip değişkeni ~T olarak görünür.",
    alternatives=[
        "Python 3.12+ projelerde def first[T](items: list[T]) -> T yazımı daha kısadır.",
        "Tür ilişkisi gerekmiyorsa (yalnızca dolaşılıyor ve sonuç başka türdeyse) Iterable[object] gibi düz bir tip yeterlidir.",
    ],
    traps=[
        "TypeVar'ı yalnızca bir yerde kullanmak (def f(x: T) -> None): ilişki kurmuyorsa object yeterlidir.",
        "Box[int] yazmanın değerlerin int olmasını çalışma anında zorladığını sanmak.",
        "TypeVar adını değişkenden farklı vermek (T = TypeVar('U')); denetleyiciler uyarır.",
        "3.12 yazımını (def f[T]) eski Python sürümlerinde kullanmak: SyntaxError.",
    ],
    realCode=r'''
from typing import Generic, TypeVar

K = TypeVar("K")
V = TypeVar("V")

class Registry(Generic[K, V]):
    def __init__(self) -> None:
        self._items: dict[K, V] = {}

    def add(self, key: K, value: V) -> None:
        self._items[key] = value

    def get(self, key: K, default: V) -> V:
        return self._items.get(key, default)

ports: Registry[str, int] = Registry()
ports.add("web", 8080)
print(ports.get("web", 0), ports.get("db", 5432))
''',
    realOutput=r'''
8080 5432
''',
    lineByLine=[
        "Registry iki tip değişkeniyle tanımlanır: anahtar türü K ve değer türü V.",
        "Registry[str, int] yazımı, bu kaydın metin anahtar ve tam sayı değer tuttuğunu söyler.",
        "get'in dönüş türü V olduğu için denetleyici ports.get(...) sonucunun int olduğunu bilir.",
        "Çalışma anında sıradan bir sözlük sarmalayıcısıdır; tipler davranışı değiştirmez.",
    ],
    sources=[
        {"title": "Python 3.12 · Generics", "url": TYPING + "#generics"},
        {"title": "Python 3.12 · Tip parametre listeleri (PEP 695)", "url": "https://docs.python.org/3.12/reference/compound_stmts.html#type-params"},
    ],
)

section(
    id="callable",
    title="Callable ve tip takma adları",
    eyebrow="Fonksiyon alan ve döndüren kodun tipi",
    objectives=[
        "Callable[[int], str] yazımıyla fonksiyon parametrelerini ve fonksiyon döndüren fonksiyonları tiplendirir.",
        "Tip takma adlarıyla (Number = int | float) uzun tipleri okunur kılar ve decorator imzalarında ParamSpec kalıbını tanır.",
    ],
    prerequisites=["generics", "m6:lambda-higher-order", "m13:decorators"],
    summary="Callable[[int, int], str] iki int alıp str döndüren her çağrılabilir şeyi anlatır: fonksiyon, lambda, metot ya da __call__'lu nesne. Fonksiyon alan (callback) ve fonksiyon döndüren kodda kullanılır. Uzun tiplere ad vermek (Transform = Callable[[Number], Number]) imzaları kısaltır.",
    explanation=(
        "M6'da fonksiyonları değer gibi kullandın (map, sorted'ın key'i, closure), M13'te decorator'lar fonksiyon alıp fonksiyon döndürdü. Bu kodun tipi collections.abc.Callable ile yazılır: köşeli parantez içinde önce parametre türlerinin listesi, sonra dönüş türü gelir. Callable[[int], int] tek int alıp int döndürür, Callable[[], str] hiç argüman almayıp str döndürür. Argümanları önemsizse Callable[..., str] yazılır. "
        "Parametre olarak: def apply(f: Callable[[int], int], x: int) -> int. Dönüş değeri olarak: def make_multiplier(factor: int) -> Callable[[int], int]. Denetleyici, verilen fonksiyonun imzasının uyup uymadığını kontrol eder; argüman sayısı tutmayan bir fonksiyon verirsen çalıştırmadan uyarır (çalışma anında ise TypeError ancak çağrıda gelir). "
        "Tipler uzadıkça okunurluk düşer. Takma ad bir atamadır: Number = int | float, Transform = Callable[[Number], Number]. Python 3.12'de type Transform = ... yazımı da vardır. "
        "Decorator'ların doğru tiplenmesi için ParamSpec kullanılır: P = ParamSpec('P'), R = TypeVar('R') ve def logged(func: Callable[P, R]) -> Callable[P, R]. Bu kalıp sarmalanan fonksiyonun parametre imzasının korunduğunu denetleyiciye anlatır; gerçek kodda sık görürsün, okuyabilmen yeterli."
    ),
    code=r'''
from collections.abc import Callable

Number = int | float
Transform = Callable[[Number], Number]

def apply_all(values: list[Number], steps: list[Transform]) -> list[Number]:
    result = values
    for step in steps:
        result = [step(value) for value in result]
    return result

def double(x: Number) -> Number:
    return x * 2

def make_adder(amount: int) -> Callable[[int], int]:
    def add(x: int) -> int:
        return x + amount
    return add

print(apply_all([1, 2, 3], [double, lambda x: x + 1]))
add_ten = make_adder(10)
print(add_ten(5), make_adder.__annotations__["return"])
print(Transform)
''',
    expectedOutput=r'''
[3, 5, 7]
15 collections.abc.Callable[[int], int]
collections.abc.Callable[[int | float], int | float]
''',
    why="apply_all, Transform imzasına uyan her çağrılabilir şeyi (adlı fonksiyon ve lambda) sırayla uyguladı. make_adder bir fonksiyon döndürdü; dönüş tipi bunu Callable ile anlatıyor. Takma ad Transform, açıldığında uzun tipin kendisidir.",
    alternatives=[
        "Çağrılabilir nesnenin ek metotları ya da isimli parametreleri de önemliyse __call__ içeren bir Protocol yaz.",
        "Python 3.12+ projelerde takma adlar için type Transform = Callable[[Number], Number] yazımını kullanabilirsin.",
    ],
    traps=[
        "Callable[int, int] yazmak; parametre türleri her zaman bir liste içinde olmalı: Callable[[int], int].",
        "Argümansız fonksiyon bekleyen bir yere (Callable[[], str]) argüman isteyen fonksiyon vermek; çağrıda TypeError gelir.",
        "Callable'ı typing'den ya da collections.abc'den karıştırarak içe aktarmak; ikisi de çalışır ama yeni kodda collections.abc önerilir.",
        "Decorator'ları Callable[..., Any] ile tiplendirip parametre bilgisini kaybetmek; ParamSpec bunu korur.",
    ],
    realCode=r'''
from collections.abc import Callable
from functools import wraps
from typing import ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")

def logged(func: Callable[P, R]) -> Callable[P, R]:
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        print("çağrı:", func.__name__)
        return func(*args, **kwargs)
    return wrapper

@logged
def add(a: int, b: int) -> int:
    return a + b

print(add(2, 3))
''',
    realOutput=r'''
çağrı: add
5
''',
    lineByLine=[
        "P, sarmalanan fonksiyonun bütün parametre imzasını; R, dönüş türünü temsil eder.",
        "logged'un imzası 'aynı parametreleri alıp aynı türü döndüren bir fonksiyon döner' der.",
        "wrapper'ın *args ve **kwargs'ı P.args ve P.kwargs ile işaretlenir; denetleyici add('x', 2) çağrısını yine yakalar.",
        "Çalışma anında sıradan bir decorator'dır (M13); tipler yalnızca denetleyici içindir.",
    ],
    sources=[
        {"title": "Python 3.12 · Callable", "url": TYPING + "#annotating-callable-objects"},
        {"title": "Python 3.12 · typing.ParamSpec", "url": TYPING + "#typing.ParamSpec"},
    ],
)

section(
    id="mypy-runtime",
    title="mypy mantığı ve çalışma zamanı doğrulaması",
    eyebrow="Tipleri kim denetler, veriyi kim doğrular?",
    objectives=[
        "mypy'nin kodu çalıştırmadan tip ipuçlarına göre denetlediğini, çıktı biçimini (dosya:satır: error: ... [kod]) ve Any ile # type: ignore'un etkisini okur.",
        "Tip ipucu ile çalışma zamanı doğrulamasını ayırır; dışarıdan gelen veriyi isinstance ve değer denetimleriyle kendisi doğrular, cast'in hiçbir şey yapmadığını bilir.",
    ],
    prerequisites=["annotations-basics", "optional-union", "m7:raising"],
    summary="mypy (ya da pyright) programı çalıştırmadan tip ipuçlarını okur ve uyumsuzlukları raporlar. Çalışma anında ise Python ipuçlarını uygulamaz: kullanıcıdan, dosyadan ya da ağdan gelen veriyi kendin doğrulamalısın. İkisi farklı sorunları çözer ve birbirinin yerini tutmaz.",
    explanation=(
        "mypy statik bir denetleyicidir: kendi bilgisayarında pip install mypy ile kurulur, mypy uygulama.py ile çalıştırılır ve kodu çalıştırmadan okur. Bulduğu her sorunu dosya:satır: error: açıklama [hata-kodu] biçiminde yazar, örneğin app.py:12: error: Argument 1 to \"greet\" has incompatible type \"int\"; expected \"str\"  [arg-type]. reveal_type(x) satırı, mypy'nin x için çıkardığı türü raporlatır. Editörlerdeki Pylance/pyright aynı işi yazarken yapar. Bu araçlar tarayıcıdaki editörde çalışmaz; bu bölümdeki mypy örnekleri yerel Python içindir. "
        "Denetim kademelidir: ipucu olmayan fonksiyonların gövdesi varsayılan olarak denetlenmez; Any türü 'her şey olabilir' der ve o değerle ilgili denetimi kapatır; # type: ignore[arg-type] yorumu tek bir satırdaki uyarıyı susturur. Bunları ancak nedenini bilerek kullan; --strict seçeneği eksik ipuçlarını da hata sayar. "
        "Çalışma anında ise durum farklıdır: input(), json.loads, dosyadan okunan satırlar ve API yanıtları ipuçlarını hiç görmez. Bu veriyi isinstance, değer aralığı ve anahtar denetimleriyle doğrula ve uygun hatayı fırlat (M7). bool, int'in alt sınıfı olduğu için isinstance(True, int) True verir; gerekiyorsa ayrıca denetle. isinstance, list[int] gibi parametreli tiplerle kullanılamaz (TypeError); listeyi ve öğelerini ayrı ayrı denetlemen gerekir. "
        "typing.cast(int, değer) yalnızca denetleyiciye 'bana güven, bu int' der; çalışma anında değeri değiştirmez, denetlemez. typing.get_type_hints(fonksiyon) ipuçlarını çalışma anında okur; kendi küçük doğrulayıcını yazarken ya da pydantic gibi kütüphanelerin (M18) nasıl çalıştığını anlamak için kullanılır."
    ),
    code=r'''
from typing import get_type_hints

def set_age(age: int) -> str:
    return f"yaş: {age}"

def checked_set_age(age: int) -> str:
    if not isinstance(age, int) or isinstance(age, bool):
        raise TypeError(f"age int olmalı, {type(age).__name__} geldi")
    if age < 0:
        raise ValueError("age negatif olamaz")
    return f"yaş: {age}"

print(set_age("on"))
print(get_type_hints(set_age))
for value in (30, "otuz", -1):
    try:
        print(checked_set_age(value))
    except (TypeError, ValueError) as error:
        print(type(error).__name__, error)
''',
    expectedOutput=r'''
yaş: on
{'age': <class 'int'>, 'return': <class 'str'>}
yaş: 30
TypeError age int olmalı, str geldi
ValueError age negatif olamaz
''',
    why="set_age ipucuna rağmen metni kabul etti; mypy bu çağrıyı işaretlerdi ama Python çalıştırdı. get_type_hints ipuçlarını çalışma anında okuyabildiğimizi gösterir. checked_set_age ise gerçekten doğruladı: yanlış türü TypeError, geçersiz değeri ValueError ile reddetti.",
    alternatives=[
        "Çok alanlı dış veriyi doğrulamak için elle yazılmış denetimler yerine pydantic gibi bir doğrulama kütüphanesi kullanılabilir (M18).",
        "Projede kademeli ilerle: önce genel fonksiyonların imzalarına ipucu ekle, mypy'yi CI'da çalıştır, sonra --strict'e doğru sıkılaştır (M16).",
    ],
    traps=[
        "mypy hatasız geçti diye dış verinin doğru olduğunu sanmak; mypy çalışma anındaki veriyi görmez.",
        "cast'in değeri dönüştürdüğünü ya da denetlediğini sanmak.",
        "Uyarıları Any ya da # type: ignore ile sessizce kapatıp gerçek hatayı gizlemek.",
        "isinstance(x, list[int]) yazmak (TypeError); önce isinstance(x, list), sonra öğeleri denetle.",
    ],
    realCode=r'''
def total_price(prices: list[int]) -> int:
    return sum(prices)

user_input = "100"
prices: list[int] = [50, int(user_input)]
print(total_price(prices))
# Son satır yorumdan çıkarılırsa mypy, programı çalıştırmadan her öğe için şunu söyler:
# app.py:9: error: List item 0 has incompatible type "str"; expected "int"  [list-item]
# total_price(["50", "100"])
''',
    realOutput=r'''
150
''',
    lineByLine=[
        "total_price yalnızca tam sayı listesi beklediğini imzasıyla söyler.",
        "Kullanıcıdan gelen metin, listeye girmeden önce int() ile dönüştürülür; ipucu bunu kendisi yapmaz.",
        "Yorumdaki çağrı çalıştırılsaydı sum metinleri toplayamayıp TypeError verirdi; mypy ise sorunu çalıştırmadan, satır numarası ve hata koduyla bildirir.",
        "mypy'yi yerelde mypy app.py ile çalıştırırsın; editördeki denetleyici aynı uyarıyı yazarken gösterir.",
    ],
    sources=[
        {"title": "mypy · Belgeler", "url": "https://mypy.readthedocs.io/en/stable/"},
        {"title": "Python 3.12 · typing.cast ve get_type_hints", "url": TYPING + "#typing.get_type_hints"},
    ],
    runtime="mixed",
    runtimeNote="Editör örnekleri tarayıcıda çalışır. mypy ve pyright bu sitede çalışmaz; mypy komutları ve çıktıları yerel Python içindir.",
)
