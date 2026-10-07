"""M14 (Type hints) questions. Imported by build_m14.py.

Order: 12 output, 6 bug, 4 fill, 4 order, 10 code, 4 traceback (ids m14-q01 ... m14-q40).
"""

from _qhelper import make_questions

questions, q = make_questions("m14")

ANN_FULL_NAME = "{'first': <class 'str'>, 'last': <class 'str'>, 'upper': <class 'bool'>, 'return': <class 'str'>}"
ANN_WORDS = "{'words': list[str], 'return': dict[str, int]}"
ANN_CHUNK = "{'items': list[~T], 'size': <class 'int'>, 'return': list[list[~T]]}"
KEYS_PRODUCT = "['name', 'price'] ['stock']"

# ------------------------------------------------------------------ output (12)
q(type="output", topic="denetim-yok", sectionId="annotations-basics", difficulty=1,
  prompt="int ipucu verilmiş fonksiyona iki metin veriliyor. Çıktı ne olur?",
  code=r'''
def add(a: int, b: int) -> int:
    return a + b

print(add("3", "4"))
''',
  expectedOutput="34",
  options=["34", "7", "TypeError verir", "None"],
  hints=["Python tip ipuçlarını çalışma anında denetler mi?", "İki metin + ile ne olur?"],
  explanation="Tip ipuçları çalışma anında uygulanmaz ve değer dönüştürmez. a + b iki metni birleştirir ve '34' döner; mypy ise bu çağrıyı çalıştırmadan işaretlerdi.")

q(type="output", topic="annotations", sectionId="annotations-basics", difficulty=2,
  prompt="Fonksiyonun __annotations__ sözlüğünün anahtarları nelerdir?",
  code=r'''
def f(x: int, y: str = "a") -> bool:
    return True

print(list(f.__annotations__))
''',
  expectedOutput="['x', 'y', 'return']",
  options=["['x', 'y', 'return']", "['x', 'y']", "['x', 'return']", "['return', 'x', 'y']"],
  hints=["Varsayılanlı parametrenin de ipucu var.", "Dönüş ipucu hangi anahtarla saklanır?"],
  explanation="Her ipuçlu parametre adıyla, dönüş ipucu 'return' anahtarıyla saklanır; sıra tanımdaki sıradır.")

q(type="output", topic="yalniz-anotasyon", sectionId="annotations-basics", difficulty=2,
  prompt="Değeri olmayan bir değişken anotasyonu okunuyor. Çıktı ne olur?",
  code=r'''
x: int
try:
    print(x)
except NameError:
    print("tanımsız")
''',
  expectedOutput="tanımsız",
  options=["tanımsız", "0", "None", "<class 'int'>"],
  hints=["x: int bir değer atıyor mu?", "Değer verilmeyen ad tanımlı mıdır?"],
  explanation="x: int yalnızca bir ipucudur, değer atamaz; x adı oluşmaz ve okunması NameError verir. Varsayılan bir 0 ya da None da yoktur.")

q(type="output", topic="koleksiyon", sectionId="collection-types", difficulty=1,
  prompt="Koleksiyon tipi yazdırılıyor. Çıktı ne olur?",
  code=r'''
scores: dict[str, list[int]] = {"ada": [1, 2]}
print(dict[str, list[int]], len(scores["ada"]))
''',
  expectedOutput="dict[str, list[int]] 2",
  options=["dict[str, list[int]] 2", "<class 'dict'> 2", "dict 2", "TypeError verir"],
  hints=["Parametrelenmiş tip kendi yazımıyla görünür.", "scores['ada'] kaç öğeli?"],
  explanation="dict[str, list[int]] çalışma anında bir tip nesnesidir ve yazıldığı gibi gösterilir. Değişkendeki sözlük sıradan bir dict'tir; listede iki öğe vardır.")

q(type="output", topic="iterable", sectionId="collection-types", difficulty=2,
  prompt="Iterable[int] isteyen fonksiyona farklı türler veriliyor. Çıktı ne olur?",
  code=r'''
from collections.abc import Iterable

def total(xs: Iterable[int]) -> int:
    return sum(xs)

print(total([1, 2]), total({3, 4}), total(range(4)), total(n for n in (5,)))
''',
  expectedOutput="3 7 6 5",
  options=["3 7 6 5", "3 TypeError", "3 7 10 5", "3 7 6 0"],
  hints=["Iterable, dolaşılabilen her şeyi kapsar.", "range(4) 0, 1, 2, 3 üretir."],
  explanation="Liste, küme, range ve generator dolaşılabilir oldukları için hepsi Iterable[int]'e uyar: 1 + 2, 3 + 4, 0 + 1 + 2 + 3 ve 5.")

q(type="output", topic="daraltma", sectionId="optional-union", difficulty=2,
  prompt="str | None alan fonksiyon üç farklı değerle çağrılıyor. Çıktı ne olur?",
  code=r'''
def shout(text: str | None) -> str:
    if not text:
        return "-"
    return text.upper()

print(shout(None), shout(""), shout("ok"))
''',
  expectedOutput="- - OK",
  options=["- - OK", "- OK", "None - OK", "AttributeError verir"],
  hints=["if not text hem None'ı hem boş metni yakalar.", "Yalnızca dolu metin büyütülür."],
  explanation="not text, None için de boş metin için de doğrudur; ikisi '-' döner. Bu denetimden sonra text kesinlikle dolu bir str'dir ve upper güvenle çağrılır.")

q(type="output", topic="optional-esitlik", sectionId="optional-union", difficulty=3,
  prompt="Eski ve yeni birleşim yazımları karşılaştırılıyor. Çıktı ne olur?",
  code=r'''
from typing import Optional, Union

print(Optional[int] == Union[int, None], (int | None) == Optional[int])
''',
  expectedOutput="True True",
  options=["True True", "True False", "False True", "False False"],
  hints=["Optional[X], Union[X, None]'ın kısaltmasıdır.", "X | None, Python 3.10'dan beri aynı tipin yeni yazımıdır."],
  explanation="Optional[int] tanım gereği Union[int, None]'dır ve int | None ile aynı tipi gösterir; üç yazım birbirine eşittir.")

q(type="output", topic="typeddict-dict", sectionId="typeddict", difficulty=2,
  prompt="TypedDict ile kurulan nesnelerin çalışma anındaki türü nedir?",
  code=r'''
from typing import TypedDict

class Point(TypedDict):
    x: int
    y: int

p: Point = {"x": 1, "y": 2}
q = Point(x=3, y=4)
print(type(q).__name__, q["x"] + p["y"], isinstance(p, dict))
''',
  expectedOutput="dict 5 True",
  options=["dict 5 True", "Point 5 True", "Point 5 False", "dict 4 True"],
  hints=["TypedDict çalışma anında yeni bir tür üretir mi?", "q['x'] 3, p['y'] 2'dir."],
  explanation="TypedDict yalnızca statik bir şekil tanımıdır; Point(...) çağrısı da sıradan bir dict döndürür. 3 + 2 = 5 ve p bir dict'tir.")

q(type="output", topic="runtime-checkable", sectionId="protocol", difficulty=3,
  prompt="runtime_checkable bir Protocol ile isinstance denetleniyor. Çıktı ne olur?",
  code=r'''
from typing import Protocol, runtime_checkable

@runtime_checkable
class Closer(Protocol):
    def close(self) -> None: ...

class File:
    def close(self) -> None:
        print("kapandı")

class Door:
    close = "kapı"

print(isinstance(File(), Closer), isinstance(Door(), Closer), isinstance("x", Closer))
''',
  expectedOutput="True True False",
  options=["True True False", "True False False", "True False True", "False False False"],
  hints=["runtime_checkable isinstance neye bakar?", "Door'da close adlı bir şey var mı? Çağrılabilir olması denetlenir mi?"],
  explanation="runtime_checkable isinstance yalnızca close adının var olup olmadığına bakar. File da Door da bu adı taşır (Door'unki bir metin bile olsa); str'de close yoktur. İmza ve tür denetimi mypy'nin işidir.")

q(type="output", topic="typevar", sectionId="generics", difficulty=2,
  prompt="TypeVar ile tiplenmiş fonksiyon farklı türlerle çağrılıyor. Çıktı ne olur?",
  code=r'''
from typing import TypeVar

T = TypeVar("T")

def last(items: list[T]) -> T:
    return items[-1]

print(last([1, 2, 3]), last("abc"), T.__name__)
''',
  expectedOutput="3 c T",
  options=["3 c T", "3 abc T", "TypeError verir", "3 c ~T"],
  hints=["Çalışma anında list[T] ipucu bir metni reddeder mi?", "'abc'[-1] nedir?"],
  explanation="TypeVar çalışma anında hiçbir şeyi denetlemez; last bir metinle de çalışır ve son karakteri döndürür. Tip değişkeninin adı 'T'dir (annotation'larda ~T olarak görünür).")

q(type="output", topic="callable", sectionId="callable", difficulty=2,
  prompt="Callable[[int], int] alan fonksiyon iki kez uyguluyor. Çıktı ne olur?",
  code=r'''
from collections.abc import Callable

def apply(f: Callable[[int], int], x: int) -> int:
    return f(f(x))

print(apply(lambda n: n * 3, 2), apply(abs, -4))
''',
  expectedOutput="18 4",
  options=["18 4", "6 4", "18 -4", "12 16"],
  hints=["f(f(x)): önce içteki çağrı.", "Yerleşik abc de bir çağrılabilirdir."],
  explanation="İlk çağrı 2 → 6 → 18 verir. abs(-4) 4, abs(4) yine 4'tür. Lambda ve yerleşik fonksiyon, imzaya uyan çağrılabilirlerdir.")

q(type="output", topic="cast", sectionId="mypy-runtime", difficulty=3,
  prompt="typing.cast ile bir değer int diye işaretleniyor. Çıktı ne olur?",
  code=r'''
from typing import Any, cast

value: Any = "42"
number = cast(int, value)
print(number, type(number).__name__)
''',
  expectedOutput="42 str",
  options=["42 str", "42 int", "TypeError verir", "ValueError verir"],
  hints=["cast değeri dönüştürür mü?", "cast yalnızca kime bir şey söyler?"],
  explanation="cast yalnızca denetleyiciye 'bu değeri int say' der; çalışma anında değeri olduğu gibi döndürür. number hâlâ '42' metnidir. Dönüştürmek için int(value) gerekir.")

# ------------------------------------------------------------------ bug (6)
q(type="bug", topic="denetim-yok", sectionId="annotations-basics", difficulty=1,
  prompt="Kullanıcı 5 yazdığında neden 'ses: 5555555555' çıkıyor?",
  code=r'''
def set_volume(level: int) -> None:
    print("ses:", level * 10)

set_volume(input())
''',
  answer="Tip ipucu çalışma anında dönüştürme ya da denetim yapmaz; input() str döndürür, int(...) ile çevrilmeli",
  options=[
      "Tip ipucu çalışma anında dönüştürme ya da denetim yapmaz; input() str döndürür, int(...) ile çevrilmeli",
      "level: int yazımı değeri on kez tekrarlamaya zorlar",
      "-> None dönüş ipucu sonucu bozar",
      "print iki değeri birleştirirken sayıyı metne çevirir",
  ],
  optionFeedback={
      "level: int yazımı değeri on kez tekrarlamaya zorlar": "İpucu davranışı değiştirmez; tekrarı metin * 10 işlemi yapar.",
      "-> None dönüş ipucu sonucu bozar": "Fonksiyon zaten bir şey döndürmüyor; sorun parametrenin türünde.",
      "print iki değeri birleştirirken sayıyı metne çevirir": "print değeri olduğu gibi gösterir; değer zaten '5555555555' metnidir.",
  },
  hints=["input() hangi türde değer döndürür?", "Metin * 10 ne yapar?"],
  explanation="input() '5' metnini döndürür; level: int ipucu bunu sayıya çevirmez. '5' * 10 metni on kez tekrarlar. Çağrı set_volume(int(input())) olmalı; mypy bu hatayı çalıştırmadan gösterirdi.")

q(type="bug", topic="dict-tipi", sectionId="collection-types", difficulty=2,
  prompt="Kod çalışıyor ama tip denetleyici dönüş tipini geçersiz buluyor. Sorun ne?",
  code=r'''
def count_words(words: list[str]) -> dict[str: int]:
    counts = {}
    for word in words:
        counts[word] = counts.get(word, 0) + 1
    return counts

print(count_words(["a", "b", "a"]))
''',
  answer="Sözlük tipinde anahtar ve değer türü virgülle ayrılır: dict[str, int]; iki nokta bir dilim üretir",
  options=[
      "Sözlük tipinde anahtar ve değer türü virgülle ayrılır: dict[str, int]; iki nokta bir dilim üretir",
      "list[str] parametre olarak kullanılamaz",
      "Dönüş tipi yalnızca dict olabilir, içi yazılamaz",
      "counts.get tip ipucu olan fonksiyonlarda çalışmaz",
  ],
  optionFeedback={
      "list[str] parametre olarak kullanılamaz": "list[str] geçerli bir parametre tipidir.",
      "Dönüş tipi yalnızca dict olabilir, içi yazılamaz": "dict[str, int] gibi içi yazılmış tipler geçerlidir ve tercih edilir.",
      "counts.get tip ipucu olan fonksiyonlarda çalışmaz": "get her yerde çalışır; kod da doğru çıktı veriyor.",
  },
  hints=["Kod doğru sonucu yazdırıyor; sorun yalnızca ipucunda.", "dict tipinin iki parametresi neyle ayrılır?"],
  explanation="dict[str: int] Python'da dilim nesnesiyle parametrelenmiş anlamsız bir tip üretir; çalışma anında hata vermez ama denetleyici geçersiz sayar. Doğrusu dict[str, int].")

q(type="bug", topic="eksik-donus", sectionId="optional-union", difficulty=2,
  prompt="Can için neden TypeError oluşuyor? (mypy bu fonksiyon için 'Missing return statement' uyarısı verir.)",
  code=r'''
def find_age(people: dict[str, int], name: str) -> int:
    if name in people:
        return people[name]

age = find_age({"Ada": 30}, "Can")
print(age + 1)
''',
  answer="Ad yoksa fonksiyon None döndürüyor; dönüş tipi int | None olmalı ve çağıran None'ı denetlemeli",
  options=[
      "Ad yoksa fonksiyon None döndürüyor; dönüş tipi int | None olmalı ve çağıran None'ı denetlemeli",
      "dict[str, int] tipinde anahtarlar aranamaz",
      "-> int ipucu çalışma anında None'ı 0'a çevirir",
      "age + 1 işleminde int ile int toplanamaz",
  ],
  optionFeedback={
      "dict[str, int] tipinde anahtarlar aranamaz": "in ile anahtar aramak sorunsuzdur.",
      "-> int ipucu çalışma anında None'ı 0'a çevirir": "İpuçları hiçbir değeri dönüştürmez; None olduğu gibi döner.",
      "age + 1 işleminde int ile int toplanamaz": "Sorun age'in int değil None olması.",
  },
  hints=["Can sözlükte yok; fonksiyon hangi satırla bitiyor?", "return yazılmayan yol ne döndürür?"],
  explanation="Ad bulunamazsa fonksiyon return'süz biter ve None döner; None + 1 TypeError verir. Dönüş tipini int | None yapıp çağırırken if age is None denetle ya da bulunamadığında bir varsayılan döndür.")

q(type="bug", topic="typeddict-dogrulama", sectionId="typeddict", difficulty=2,
  prompt="User bir TypedDict olduğu hâlde neden TypeError oluşuyor?",
  code=r'''
import json
from typing import TypedDict

class User(TypedDict):
    name: str
    age: int

user: User = json.loads('{"name": "Ada", "age": "otuz"}')
print(user["age"] + 1)
''',
  answer="TypedDict yalnızca statik bir şekildir; JSON'dan gelen veriyi doğrulamaz, age burada bir metin",
  options=[
      "TypedDict yalnızca statik bir şekildir; JSON'dan gelen veriyi doğrulamaz, age burada bir metin",
      "json.loads TypedDict'leri okuyamaz",
      "TypedDict'te int alanı tanımlanamaz",
      "user['age'] yerine user.age yazılmalı",
  ],
  optionFeedback={
      "json.loads TypedDict'leri okuyamaz": "json.loads sıradan bir dict döndürür; TypedDict'ten habersizdir.",
      "TypedDict'te int alanı tanımlanamaz": "Her türde alan tanımlanabilir.",
      "user['age'] yerine user.age yazılmalı": "TypedDict nesnesi bir dict'tir; anahtarla erişilir.",
  },
  hints=["Çalışma anında user'ın türü nedir?", "JSON'daki age değerinin türü ne?"],
  explanation="user: User işaretlemesi veriyi kontrol etmez; json.loads'tan gelen dict'te age metindir ve '... + 1' TypeError verir. Dış veri isinstance denetimleriyle ya da bir doğrulama kütüphanesiyle doğrulanmalıdır.")

q(type="bug", topic="protocol-uyum", sectionId="protocol", difficulty=2,
  prompt="notify(Sms()) neden AttributeError verir?",
  code=r'''
from typing import Protocol

class Sender(Protocol):
    def send(self, text: str) -> None: ...

class Sms:
    def send_text(self, text: str) -> None:
        print("sms:", text)

def notify(sender: Sender) -> None:
    sender.send("selam")

notify(Sms())
''',
  answer="Sms, Protocol'ün istediği send metodunu sunmuyor (send_text); türemek gerekmez ama metot adı ve imzası uymalı",
  options=[
      "Sms, Protocol'ün istediği send metodunu sunmuyor (send_text); türemek gerekmez ama metot adı ve imzası uymalı",
      "Sms, Sender'dan türemediği için Protocol'e hiçbir zaman uyamaz",
      "Protocol sınıfları fonksiyon parametresi tipi olamaz",
      "print Protocol metotlarının içinde kullanılamaz",
  ],
  optionFeedback={
      "Sms, Sender'dan türemediği için Protocol'e hiçbir zaman uyamaz": "Protocol yapısaldır; send metodu olsaydı Sms türemeden uyardı.",
      "Protocol sınıfları fonksiyon parametresi tipi olamaz": "Protocol'lerin asıl kullanım yeri parametre tipleridir.",
      "print Protocol metotlarının içinde kullanılamaz": "Sorun print değil; çağrılan send metodu yok.",
  },
  hints=["notify hangi metodu çağırıyor?", "Sms'te o adla bir metot var mı?"],
  explanation="notify sender.send(...) çağırır ama Sms'in metodu send_text adındadır; çalışma anında AttributeError gelir. mypy aynı sorunu notify(Sms()) satırında, çalıştırmadan bildirirdi.")

q(type="bug", topic="callable-imza", sectionId="callable", difficulty=2,
  prompt="run(greet) neden TypeError verir?",
  code=r'''
from collections.abc import Callable

def run(callback: Callable[[], str]) -> str:
    return callback()

def greet(name: str) -> str:
    return "selam " + name

print(run(greet))
''',
  answer="run argümansız bir fonksiyon bekliyor (Callable[[], str]); greet ise bir argüman istiyor",
  options=[
      "run argümansız bir fonksiyon bekliyor (Callable[[], str]); greet ise bir argüman istiyor",
      "Callable tipi fonksiyonlara uygulanamaz, yalnızca sınıflara uygulanır",
      "greet'in dönüş tipi str olduğu için çağrılamaz",
      "callback() yerine callback yazılmalı",
  ],
  optionFeedback={
      "Callable tipi fonksiyonlara uygulanamaz, yalnızca sınıflara uygulanır": "Callable her çağrılabilir şeyi kapsar; fonksiyonlar başta gelir.",
      "greet'in dönüş tipi str olduğu için çağrılamaz": "Dönüş tipi doğru; sorun parametre sayısı.",
      "callback() yerine callback yazılmalı": "O zaman fonksiyon çağrılmaz, nesnesi döndürülür; asıl sorun eksik argüman.",
  },
  hints=["Callable[[], str] içindeki boş liste neyi söyler?", "run, callback'i kaç argümanla çağırıyor?"],
  explanation="run callback'i argümansız çağırır ama greet name bekler: 'missing 1 required positional argument'. Uygun bir sarmalayıcı verilmeli: run(lambda: greet('Ada')). mypy imza uyumsuzluğunu çalıştırmadan gösterirdi.")

# ------------------------------------------------------------------ fill (4)
q(type="fill", topic="union", sectionId="optional-union", difficulty=1,
  prompt="Dönüş değerinin int ya da None olabileceğini yazan işareti tamamla.",
  code=r'''
def parse(text: str) -> int ___ None:
    return int(text) if text.isdigit() else None

print(parse("12"), parse("x"))
''',
  answer="|",
  expectedOutput="12 None",
  hints=["Python 3.10'dan beri iki türü birleştiren işaret.", "Bit düzeyinde 'veya' işlecidir."],
  explanation="int | None, değerin int ya da None olabileceğini söyler; eski yazımı Optional[int]'tir.")

q(type="fill", topic="typeddict", sectionId="typeddict", difficulty=1,
  prompt="Sözlüğün şeklini tanımlayan taban sınıfı yaz.",
  code=r'''
from typing import TypedDict

class Book(___):
    title: str
    pages: int

b: Book = {"title": "Dune", "pages": 412}
print(b["pages"])
''',
  answer="TypedDict",
  expectedOutput="412",
  hints=["typing'den içe aktarılan ad.", "Adı 'tiplenmiş sözlük' demektir."],
  explanation="class Book(TypedDict) anahtarları ve türlerini tanımlar; b çalışma anında sıradan bir dict'tir.")

q(type="fill", topic="protocol", sectionId="protocol", difficulty=2,
  prompt="Yapısal bir arayüz tanımlayan taban sınıfı yaz.",
  code=r'''
from typing import Protocol

class Greeter(___):
    def greet(self) -> str: ...

class Tr:
    def greet(self) -> str:
        return "merhaba"

def hello(g: Greeter) -> str:
    return g.greet()

print(hello(Tr()))
''',
  answer="Protocol",
  expectedOutput="merhaba",
  hints=["typing'den içe aktarılan ad.", "Tr bu sınıftan türemediği hâlde ona uyar."],
  explanation="Greeter bir Protocol'dür; greet metodu olan her sınıf (Tr gibi) türemeden ona uyar.")

q(type="fill", topic="typevar", sectionId="generics", difficulty=2,
  prompt="Tip değişkeni tanımlayan yardımcıyı yaz.",
  code=r'''
from typing import TypeVar

T = ___("T")

def first(items: list[T]) -> T:
    return items[0]

print(first(["x", "y"]))
''',
  answer="TypeVar",
  expectedOutput="x",
  hints=["typing'den içe aktarılan ad.", "Adı 'tip değişkeni' demektir."],
  explanation="T = TypeVar('T') bir tip değişkenidir; first'ün girdi listesindeki türle aynı türde değer döndürdüğünü anlatır.")

# ------------------------------------------------------------------ order (4)
q(type="order", topic="annotations", sectionId="annotations-basics", difficulty=1,
  prompt="Tip ipuçlu bir fonksiyon tanımlayıp sonucunu yazdıran sırayı kur.",
  answer_lines=[
      "def area(width: float, height: float) -> float:",
      "    return width * height",
      "result: float = area(2.5, 4)",
      "print(result)",
  ],
  perm=[2, 0, 3, 1],
  expectedOutput="10.0",
  hints=["Fonksiyon kullanılmadan önce tanımlanır.", "Dönüş ipucu def satırındadır."],
  explanation="area tanımlanır, sonucu ipuçlu result değişkenine atanır ve yazdırılır: 2.5 x 4 = 10.0.")

q(type="order", topic="iterable", sectionId="collection-types", difficulty=2,
  prompt="Iterable[str] alan ve en uzun kelimeyi bulan sırayı kur.",
  answer_lines=[
      "from collections.abc import Iterable",
      "def longest(words: Iterable[str]) -> str:",
      '    best = ""',
      "    for word in words:",
      "        if len(word) > len(best):",
      "            best = word",
      "    return best",
      'print(longest(["py", "python", "pip"]))',
  ],
  perm=[3, 7, 1, 5, 0, 6, 2, 4],
  expectedOutput="python",
  hints=["İçe aktarma en üstte olmalı.", "return döngünün dışında, fonksiyon gövdesi hizasında durur."],
  explanation="longest, dolaşılabilen her metin kaynağını kabul eder ve en uzun kelimeyi döndürür.")

q(type="order", topic="generic-sinif", sectionId="generics", difficulty=2,
  prompt="Genel bir Stack sınıfı tanımlayıp kullanan sırayı kur.",
  answer_lines=[
      "from typing import Generic, TypeVar",
      'T = TypeVar("T")',
      "class Stack(Generic[T]):",
      "    def __init__(self) -> None:",
      "        self.items: list[T] = []",
      "    def push(self, item: T) -> None:",
      "        self.items.append(item)",
      "s: Stack[int] = Stack()",
      "s.push(3)",
      "print(s.items)",
  ],
  perm=[7, 2, 9, 0, 5, 8, 3, 1, 6, 4],
  expectedOutput="[3]",
  hints=["T, sınıfta kullanılmadan önce tanımlanmalı.", "Nesne, sınıf tanımından sonra kurulur."],
  explanation="TypeVar tanımlanır, Stack Generic[T] ile genel yapılır; Stack[int] ipucuyla kurulan nesneye 3 eklenir.")

q(type="order", topic="callable", sectionId="callable", difficulty=2,
  prompt="Bir fonksiyonu iki kez uygulayan sırayı kur.",
  answer_lines=[
      "from collections.abc import Callable",
      "def twice(f: Callable[[int], int], x: int) -> int:",
      "    return f(f(x))",
      "def inc(n: int) -> int:",
      "    return n + 1",
      "print(twice(inc, 5))",
  ],
  perm=[3, 5, 1, 4, 0, 2],
  expectedOutput="7",
  hints=["Callable içe aktarılmadan ipucunda kullanılamaz.", "inc, twice'a argüman olarak verilir; çağrıdan önce tanımlanmalı."],
  explanation="twice, int alıp int döndüren bir fonksiyonu iki kez uygular: 5 → 6 → 7.")

# ------------------------------------------------------------------ code (10)
q(type="code", topic="annotations", sectionId="annotations-basics", difficulty=1,
  prompt="full_name fonksiyonuna tip ipuçları ekle: first ve last metin, upper bool (varsayılan False), dönüş metin. Program adı, soyadı ve 'evet'/'hayır' okur; sonucu ve fonksiyonun ipuçlarını yazar.",
  starterCode=r'''
def full_name(first, last, upper=False):
    # parametrelere ve dönüşe tip ipucu ekle
    name = f"{first} {last}"
    return name.upper() if upper else name

first = input()
last = input()
upper = input() == "evet"
print(full_name(first, last, upper))
print(full_name.__annotations__)
''',
  answer=r'''
def full_name(first: str, last: str, upper: bool = False) -> str:
    name = f"{first} {last}"
    return name.upper() if upper else name

first = input()
last = input()
upper = input() == "evet"
print(full_name(first, last, upper))
print(full_name.__annotations__)
''',
  exampleInput="ada\nlovelace\nhayır",
  expectedOutput="ada lovelace\n" + ANN_FULL_NAME,
  tests=[
      {"label": "Büyütmeden", "stdin": "ada\nlovelace\nhayır", "expectedOutput": "ada lovelace\n" + ANN_FULL_NAME},
      {"label": "Büyük harf", "stdin": "Can\nYıldız\nevet", "expectedOutput": "CAN YILDIZ\n" + ANN_FULL_NAME},
      {"label": "Kısa adlar", "stdin": "a\nb\nevet", "expectedOutput": "A B\n" + ANN_FULL_NAME},
  ],
  hints=["Parametre ipucu adın hemen ardından gelir: first: str.", "Varsayılanlı parametrede önce ipucu sonra varsayılan: upper: bool = False; dönüş için -> str."],
  explanation="İpuçları davranışı değiştirmez ama __annotations__'ta saklanır; program bu sözlüğü yazdırarak her ipucunun yerinde olduğunu gösterir.")

q(type="code", topic="koleksiyon", sectionId="collection-types", difficulty=2,
  prompt="word_lengths(words) fonksiyonunu yaz: her kelimeden uzunluğuna giden bir sözlük döndürsün. İpuçlarını yerleşik yazımla ver: parametre list[str], dönüş dict[str, int]. Program sözlüğü sıralı yazar ve ipuçlarını gösterir.",
  starterCode=r'''
def word_lengths(words):
    # her kelimeden uzunluğuna giden sözlüğü döndür; ipuçlarını ekle
    return {}

words = input().split()
lengths = word_lengths(words)
print(sorted(lengths.items()))
print(word_lengths.__annotations__)
''',
  answer=r'''
def word_lengths(words: list[str]) -> dict[str, int]:
    return {word: len(word) for word in words}

words = input().split()
lengths = word_lengths(words)
print(sorted(lengths.items()))
print(word_lengths.__annotations__)
''',
  exampleInput="elma armut kivi",
  expectedOutput="[('armut', 5), ('elma', 4), ('kivi', 4)]\n" + ANN_WORDS,
  tests=[
      {"label": "Üç kelime", "stdin": "elma armut kivi", "expectedOutput": "[('armut', 5), ('elma', 4), ('kivi', 4)]\n" + ANN_WORDS},
      {"label": "Tekrar eden kelime", "stdin": "a a", "expectedOutput": "[('a', 1)]\n" + ANN_WORDS},
      {"label": "Tek kelime", "stdin": "python", "expectedOutput": "[('python', 6)]\n" + ANN_WORDS},
  ],
  hints=["Sözlük kurucu: {word: len(word) for word in words}.", "İpuçları: words: list[str] ve -> dict[str, int] (typing.List değil, yerleşik list)."],
  explanation="Koleksiyon tiplerinin içindeki türler köşeli parantezle yazılır; dict'te anahtar ve değer türü virgülle ayrılır.")

q(type="code", topic="optional", sectionId="optional-union", difficulty=2,
  prompt="find_user(users: dict[str, int], name: str) -> int | None adı yoksa None, varsa yaşı döndürsün. describe(age: int | None) -> str, None için 'bilinmiyor', değilse 'N yaşında' döndürsün (0 da geçerli bir yaştır). Program kayıtları ve bir adı okur; sonucu ve iki ipucunu yazar.",
  starterCode=r'''
def find_user(users, name):
    # ipuçlarını ekle; ad yoksa None döndür
    return None

def describe(age):
    # ipuçlarını ekle; None için "bilinmiyor"
    return ""

users = {}
for _ in range(int(input())):
    name, age = input().split()
    users[name] = int(age)
print(describe(find_user(users, input())))
print(find_user.__annotations__["return"], describe.__annotations__["age"])
''',
  answer=r'''
def find_user(users: dict[str, int], name: str) -> int | None:
    return users.get(name)

def describe(age: int | None) -> str:
    if age is None:
        return "bilinmiyor"
    return f"{age} yaşında"

users = {}
for _ in range(int(input())):
    name, age = input().split()
    users[name] = int(age)
print(describe(find_user(users, input())))
print(find_user.__annotations__["return"], describe.__annotations__["age"])
''',
  exampleInput="2\nAda 30\nCan 25\nCan",
  expectedOutput="25 yaşında\nint | None int | None",
  tests=[
      {"label": "Bulunan", "stdin": "2\nAda 30\nCan 25\nCan", "expectedOutput": "25 yaşında\nint | None int | None"},
      {"label": "Bulunmayan", "stdin": "1\nAda 30\nEda", "expectedOutput": "bilinmiyor\nint | None int | None"},
      {"label": "Kayıt yok", "stdin": "0\nAda", "expectedOutput": "bilinmiyor\nint | None int | None"},
      {"label": "Sıfır yaş", "stdin": "1\nBebek 0\nBebek", "expectedOutput": "0 yaşında\nint | None int | None"},
  ],
  hints=["users.get(name) bulunamazsa None döndürür.", "describe'da if not age değil if age is None kullan; 0 yaşı da geçerli."],
  explanation="int | None, sonucun bulunamayabileceğini açıkça söyler. None denetimi is None ile yapılmalı; if not age 0 yaşını da 'bilinmiyor' sayardı.")

q(type="code", topic="typeddict", sectionId="typeddict", difficulty=2,
  prompt="Product adında bir TypedDict yaz: name (str), price (int) zorunlu, stock (int) NotRequired. restock_needed(products: list[Product]) -> list[str], stoğu hiç yazılmamış ya da 5'ten az olan ürünlerin adlarını sıralı döndürsün. Program ürünleri okur, sonucu ve anahtar bilgisini yazar.",
  starterCode=r'''
from typing import TypedDict, NotRequired

# Product TypedDict'ini ve restock_needed fonksiyonunu yaz

products = []
for _ in range(int(input())):
    parts = input().split()
    item = Product(name=parts[0], price=int(parts[1]))
    if len(parts) == 3:
        item["stock"] = int(parts[2])
    products.append(item)
print(restock_needed(products))
print(sorted(Product.__required_keys__), sorted(Product.__optional_keys__))
''',
  answer=r'''
from typing import TypedDict, NotRequired

class Product(TypedDict):
    name: str
    price: int
    stock: NotRequired[int]

def restock_needed(products: list[Product]) -> list[str]:
    return sorted(product["name"] for product in products if product.get("stock", 0) < 5)

products = []
for _ in range(int(input())):
    parts = input().split()
    item = Product(name=parts[0], price=int(parts[1]))
    if len(parts) == 3:
        item["stock"] = int(parts[2])
    products.append(item)
print(restock_needed(products))
print(sorted(Product.__required_keys__), sorted(Product.__optional_keys__))
''',
  exampleInput="3\nkalem 15 10\nsilgi 5 2\ndefter 40",
  expectedOutput="['defter', 'silgi']\n" + KEYS_PRODUCT,
  tests=[
      {"label": "Karışık", "stdin": "3\nkalem 15 10\nsilgi 5 2\ndefter 40", "expectedOutput": "['defter', 'silgi']\n" + KEYS_PRODUCT},
      {"label": "Sınır 5", "stdin": "1\na 1 5", "expectedOutput": "[]\n" + KEYS_PRODUCT},
      {"label": "Ürün yok", "stdin": "0", "expectedOutput": "[]\n" + KEYS_PRODUCT},
      {"label": "Sıralı çıktı", "stdin": "2\nb 1 4\na 1", "expectedOutput": "['a', 'b']\n" + KEYS_PRODUCT},
  ],
  hints=["İsteğe bağlı anahtar için stock: NotRequired[int].", "product.get('stock', 0) eksik stoğu 0 sayar; sonuçları sorted ile döndür."],
  explanation="TypedDict anahtarların şeklini anlatır; isteğe bağlı stock'a get ile güvenle erişilir. Çalışma anında ürünler sıradan sözlüklerdir.")

q(type="code", topic="protocol", sectionId="protocol", difficulty=3,
  prompt="runtime_checkable bir Discount Protocol'ü yaz: apply(self, price: int) -> int. Percent(percent) price * (100 - percent) // 100, Fixed(amount) price - amount döndürsün; ikisi de Discount'tan türemesin. checkout(prices: list[int], discount: Discount) -> int toplam fiyata indirimi uygulasın ve sonucu 0'ın altına düşürmesin.",
  starterCode=r'''
from typing import Protocol, runtime_checkable

# Discount Protocol'ünü (runtime_checkable) yaz
# Percent ve Fixed sınıflarını Discount'tan TÜRETMEDEN yaz
# checkout(prices, discount) fonksiyonunu yaz

kind, value = input().split()
prices = [int(p) for p in input().split()]
discount = Percent(int(value)) if kind == "yüzde" else Fixed(int(value))
print(checkout(prices, discount))
print(isinstance(discount, Discount), Discount in type(discount).__mro__)
''',
  answer=r'''
from typing import Protocol, runtime_checkable

@runtime_checkable
class Discount(Protocol):
    def apply(self, price: int) -> int: ...

class Percent:
    def __init__(self, percent: int) -> None:
        self.percent = percent

    def apply(self, price: int) -> int:
        return price * (100 - self.percent) // 100

class Fixed:
    def __init__(self, amount: int) -> None:
        self.amount = amount

    def apply(self, price: int) -> int:
        return price - self.amount

def checkout(prices: list[int], discount: Discount) -> int:
    return max(0, discount.apply(sum(prices)))

kind, value = input().split()
prices = [int(p) for p in input().split()]
discount = Percent(int(value)) if kind == "yüzde" else Fixed(int(value))
print(checkout(prices, discount))
print(isinstance(discount, Discount), Discount in type(discount).__mro__)
''',
  exampleInput="yüzde 10\n100 200",
  expectedOutput="270\nTrue False",
  tests=[
      {"label": "Yüzde", "stdin": "yüzde 10\n100 200", "expectedOutput": "270\nTrue False"},
      {"label": "Sıfırın altına düşmez", "stdin": "sabit 50\n30 10", "expectedOutput": "0\nTrue False"},
      {"label": "Sabit", "stdin": "sabit 5\n10", "expectedOutput": "5\nTrue False"},
      {"label": "Sıfır yüzde", "stdin": "yüzde 0\n7 8", "expectedOutput": "15\nTrue False"},
  ],
  hints=["Protocol gövdesinde metot imzası ve ... yeterlidir; isinstance için @runtime_checkable gerekir.", "Percent ve Fixed'in başlığına Discount yazma; yalnızca apply metotları olsun."],
  explanation="Percent ve Fixed, Discount'tan türemeden apply metotları sayesinde ona uyar. isinstance True verir ama Discount MRO'da yoktur: uyum yapısaldır.")

q(type="code", topic="typevar", sectionId="generics", difficulty=2,
  prompt="chunk(items: list[T], size: int) -> list[list[T]] genel fonksiyonunu yaz (T bir TypeVar): listeyi size uzunluğunda parçalara bölsün, son parça kısa olabilir. Program sayılarla ve metinlerle çağırır, ipuçlarını yazar.",
  starterCode=r'''
from typing import TypeVar

T = TypeVar("T")

def chunk(items, size):
    # ipuçlarını ekle: list[T], int -> list[list[T]]
    return []

numbers = [int(x) for x in input().split()]
size = int(input())
print(chunk(numbers, size))
print(chunk(input().split(), size))
print(chunk.__annotations__)
''',
  answer=r'''
from typing import TypeVar

T = TypeVar("T")

def chunk(items: list[T], size: int) -> list[list[T]]:
    return [items[start:start + size] for start in range(0, len(items), size)]

numbers = [int(x) for x in input().split()]
size = int(input())
print(chunk(numbers, size))
print(chunk(input().split(), size))
print(chunk.__annotations__)
''',
  exampleInput="1 2 3 4 5\n2\na b c",
  expectedOutput="[[1, 2], [3, 4], [5]]\n[['a', 'b'], ['c']]\n" + ANN_CHUNK,
  tests=[
      {"label": "Sayılar ve metinler", "stdin": "1 2 3 4 5\n2\na b c", "expectedOutput": "[[1, 2], [3, 4], [5]]\n[['a', 'b'], ['c']]\n" + ANN_CHUNK},
      {"label": "Boyut büyük", "stdin": "7\n3\nx", "expectedOutput": "[[7]]\n[['x']]\n" + ANN_CHUNK},
      {"label": "Boyut 1", "stdin": "1 2\n1\np q", "expectedOutput": "[[1], [2]]\n[['p'], ['q']]\n" + ANN_CHUNK},
  ],
  hints=["range(0, len(items), size) parçaların başlangıçlarını verir.", "İpuçlarında T'yi kullan; annotations çıktısında ~T olarak görünecek."],
  explanation="Aynı fonksiyon int ve str listeleriyle çalışır; T, denetleyiciye dönen parçaların girdiyle aynı türde öğe taşıdığını anlatır.")

q(type="code", topic="generic-sinif", sectionId="generics", difficulty=3,
  prompt="Stack(Generic[T]) sınıfını yaz: push(item: T) -> None, pop() -> T (boşsa IndexError('yığın boş')), peek() -> T | None (boşsa None), size() -> int. Program komutları ('push x', 'pop', 'peek', 'size') işler ve sonda sınıfın tip parametrelerini ve peek'in dönüş ipucunu yazar.",
  starterCode=r'''
from typing import Generic, TypeVar

T = TypeVar("T")

class Stack(Generic[T]):
    # push, pop, peek ve size metotlarını ipuçlarıyla yaz
    pass

stack: Stack[str] = Stack()
for _ in range(int(input())):
    parts = input().split()
    if parts[0] == "push":
        stack.push(parts[1])
    elif parts[0] == "pop":
        try:
            print(stack.pop())
        except IndexError as error:
            print("hata:", error)
    elif parts[0] == "peek":
        top = stack.peek()
        print("boş" if top is None else top)
    else:
        print(stack.size())
print(Stack.__parameters__, Stack.peek.__annotations__["return"])
''',
  answer=r'''
from typing import Generic, TypeVar

T = TypeVar("T")

class Stack(Generic[T]):
    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        if not self._items:
            raise IndexError("yığın boş")
        return self._items.pop()

    def peek(self) -> T | None:
        return self._items[-1] if self._items else None

    def size(self) -> int:
        return len(self._items)

stack: Stack[str] = Stack()
for _ in range(int(input())):
    parts = input().split()
    if parts[0] == "push":
        stack.push(parts[1])
    elif parts[0] == "pop":
        try:
            print(stack.pop())
        except IndexError as error:
            print("hata:", error)
    elif parts[0] == "peek":
        top = stack.peek()
        print("boş" if top is None else top)
    else:
        print(stack.size())
print(Stack.__parameters__, Stack.peek.__annotations__["return"])
''',
  exampleInput="4\npush a\npush b\npop\npeek",
  expectedOutput="b\na\n(~T,) typing.Optional[~T]",
  tests=[
      {"label": "Normal akış", "stdin": "4\npush a\npush b\npop\npeek", "expectedOutput": "b\na\n(~T,) typing.Optional[~T]"},
      {"label": "Boş yığın", "stdin": "3\npeek\npop\nsize", "expectedOutput": "boş\nhata: yığın boş\n0\n(~T,) typing.Optional[~T]"},
      {"label": "Boyut", "stdin": "3\npush x\npush y\nsize", "expectedOutput": "2\n(~T,) typing.Optional[~T]"},
  ],
  hints=["Listeyi __init__ içinde self._items: list[T] = [] ile kur.", "peek'in dönüş ipucu T | None; çalışma anında typing.Optional[~T] olarak görünür."],
  explanation="Stack[str] ipucu denetleyiciye yığının metin tuttuğunu söyler; pop'un dönüşü bu yüzden str bilinir. peek boş yığında None döndürebildiği için T | None'dır.")

q(type="code", topic="callable", sectionId="callable", difficulty=2,
  prompt="make_multiplier(factor: int) -> Callable[[int], int] bir çarpan fonksiyonu döndürsün; apply_all(funcs: list[Callable[[int], int]], value: int) -> list[int] her fonksiyonu değere uygulasın. Callable'ı collections.abc'den kullan. Program çarpanları ve değeri okur; sonucu ve iki ipucunu yazar.",
  starterCode=r'''
from collections.abc import Callable

def make_multiplier(factor):
    # ipuçlarını ekle; factor ile çarpan bir fonksiyon döndür
    pass

def apply_all(funcs, value):
    # ipuçlarını ekle; her fonksiyonu value'ya uygula
    return []

factors = [int(x) for x in input().split()]
value = int(input())
print(apply_all([make_multiplier(f) for f in factors], value))
print(make_multiplier.__annotations__["return"])
print(apply_all.__annotations__["funcs"])
''',
  answer=r'''
from collections.abc import Callable

def make_multiplier(factor: int) -> Callable[[int], int]:
    def multiply(x: int) -> int:
        return x * factor
    return multiply

def apply_all(funcs: list[Callable[[int], int]], value: int) -> list[int]:
    return [func(value) for func in funcs]

factors = [int(x) for x in input().split()]
value = int(input())
print(apply_all([make_multiplier(f) for f in factors], value))
print(make_multiplier.__annotations__["return"])
print(apply_all.__annotations__["funcs"])
''',
  exampleInput="2 3\n5",
  expectedOutput="[10, 15]\ncollections.abc.Callable[[int], int]\nlist[collections.abc.Callable[[int], int]]",
  tests=[
      {"label": "İki çarpan", "stdin": "2 3\n5", "expectedOutput": "[10, 15]\ncollections.abc.Callable[[int], int]\nlist[collections.abc.Callable[[int], int]]"},
      {"label": "Sıfır değer", "stdin": "1\n0", "expectedOutput": "[0]\ncollections.abc.Callable[[int], int]\nlist[collections.abc.Callable[[int], int]]"},
      {"label": "Negatif çarpan", "stdin": "-1 10\n4", "expectedOutput": "[-4, 40]\ncollections.abc.Callable[[int], int]\nlist[collections.abc.Callable[[int], int]]"},
  ],
  hints=["make_multiplier içinde x * factor döndüren bir iç fonksiyon tanımla ve onu döndür (closure, M6).", "Callable'ın parametre türleri listede olmalı: Callable[[int], int]."],
  explanation="Fonksiyon döndüren ve fonksiyon listesi alan kodun ipuçları Callable ile yazılır; köşeli parantezdeki ilk liste parametre türleri, ikinci öğe dönüş türüdür.")

q(type="code", topic="calisma-zamani", sectionId="mypy-runtime", difficulty=2,
  prompt="validate_age(value: object) -> int yaz: değer int değilse (bool da int sayılmaz) TypeError(f'yaş tam sayı olmalı: {tür adı}'), 0-150 aralığı dışındaysa ValueError(f'yaş aralık dışında: {değer}') fırlatsın, geçerliyse değeri döndürsün. Program JSON değerleri okur ve sonucu ya da hatayı yazar.",
  starterCode=r'''
import json

def validate_age(value: object) -> int:
    # isinstance ile türü, sonra aralığı denetle
    return value

for _ in range(int(input())):
    raw = json.loads(input())
    try:
        print("geçerli:", validate_age(raw))
    except (TypeError, ValueError) as error:
        print(type(error).__name__, error)
''',
  answer=r'''
import json

def validate_age(value: object) -> int:
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(f"yaş tam sayı olmalı: {type(value).__name__}")
    if not 0 <= value <= 150:
        raise ValueError(f"yaş aralık dışında: {value}")
    return value

for _ in range(int(input())):
    raw = json.loads(input())
    try:
        print("geçerli:", validate_age(raw))
    except (TypeError, ValueError) as error:
        print(type(error).__name__, error)
''',
  exampleInput='5\n30\n"otuz"\n-1\ntrue\n12.5',
  expectedOutput="geçerli: 30\nTypeError yaş tam sayı olmalı: str\nValueError yaş aralık dışında: -1\nTypeError yaş tam sayı olmalı: bool\nTypeError yaş tam sayı olmalı: float",
  tests=[
      {"label": "Karışık", "stdin": '5\n30\n"otuz"\n-1\ntrue\n12.5', "expectedOutput": "geçerli: 30\nTypeError yaş tam sayı olmalı: str\nValueError yaş aralık dışında: -1\nTypeError yaş tam sayı olmalı: bool\nTypeError yaş tam sayı olmalı: float"},
      {"label": "Üst sınır", "stdin": "2\n150\n151", "expectedOutput": "geçerli: 150\nValueError yaş aralık dışında: 151"},
      {"label": "null", "stdin": "1\nnull", "expectedOutput": "TypeError yaş tam sayı olmalı: NoneType"},
      {"label": "Sıfır", "stdin": "1\n0", "expectedOutput": "geçerli: 0"},
  ],
  hints=["bool, int'in alt sınıfıdır: isinstance(True, int) True verir; ayrıca denetle.", "Önce tür, sonra aralık: 0 <= value <= 150."],
  explanation="value: object ipucu, fonksiyonun her türlü girdiyle çağrılabileceğini dürüstçe söyler; doğrulama çalışma anında isinstance ve aralık denetimiyle yapılır.")

q(type="code", topic="get-type-hints", sectionId="mypy-runtime", difficulty=3,
  prompt="validate(data: dict, schema: type) -> list[str] yaz: get_type_hints(schema) ile alan türlerini al; eksik anahtar için 'eksik: anahtar', türü tam eşleşmeyen (type(değer) is beklenen değilse) anahtar için 'tür: anahtar', şemada olmayan anahtar için 'fazla: anahtar' ekle ve listeyi sıralı döndür. Program User şemasıyla bir JSON nesnesini doğrular.",
  starterCode=r'''
import json
from typing import TypedDict, get_type_hints

class User(TypedDict):
    name: str
    age: int
    active: bool

def validate(data: dict, schema: type) -> list[str]:
    # get_type_hints(schema) ile beklenen türleri al ve hataları topla
    return []

errors = validate(json.loads(input()), User)
print("geçerli" if not errors else "\n".join(errors))
''',
  answer=r'''
import json
from typing import TypedDict, get_type_hints

class User(TypedDict):
    name: str
    age: int
    active: bool

def validate(data: dict, schema: type) -> list[str]:
    hints = get_type_hints(schema)
    errors = []
    for key, expected in hints.items():
        if key not in data:
            errors.append(f"eksik: {key}")
        elif type(data[key]) is not expected:
            errors.append(f"tür: {key}")
    for key in data:
        if key not in hints:
            errors.append(f"fazla: {key}")
    return sorted(errors)

errors = validate(json.loads(input()), User)
print("geçerli" if not errors else "\n".join(errors))
''',
  exampleInput='{"name": "Ada", "age": 30, "active": true}',
  expectedOutput="geçerli",
  tests=[
      {"label": "Geçerli", "stdin": '{"name": "Ada", "age": 30, "active": true}', "expectedOutput": "geçerli"},
      {"label": "Eksik ve yanlış tür", "stdin": '{"name": "Ada", "age": "30"}', "expectedOutput": "eksik: active\ntür: age"},
      {"label": "bool int sayılmaz, fazla anahtar", "stdin": '{"name": 1, "age": true, "active": false, "x": 0}', "expectedOutput": "fazla: x\ntür: age\ntür: name"},
      {"label": "Boş nesne", "stdin": "{}", "expectedOutput": "eksik: active\neksik: age\neksik: name"},
  ],
  hints=["get_type_hints(User) {'name': str, 'age': int, 'active': bool} sözlüğünü verir.", "type(değer) is beklenen tam eşleşme ister; bu yüzden True bir int sayılmaz. Hataları bir listede toplayıp sorted ile döndür."],
  explanation="TypedDict tek başına hiçbir şeyi doğrulamaz, ama ipuçları çalışma anında okunabilir. pydantic gibi kütüphaneler bu fikri çok daha kapsamlı uygular.")

# ------------------------------------------------------------------ traceback (4)
q(type="traceback", topic="isinstance-generic", sectionId="mypy-runtime", difficulty=2,
  prompt="isinstance'a parametreli bir tip veriliyor. Hangi hata oluşur?",
  code=r'''
values = [1, 2, 3]
print(isinstance(values, list[int]))
''',
  expectedError="TypeError",
  options=["TypeError", "ValueError", "NameError", "AttributeError"],
  optionFeedback={
      "ValueError": "Değer geçersiz değil; isinstance'ın ikinci argümanı bu türde olamaz.",
      "NameError": "list ve int tanımlı adlardır.",
      "AttributeError": "Hiçbir öznitelik aranmıyor.",
  },
  hints=["isinstance öğelerin türünü denetleyebilir mi?", "list[int] çalışma anında nasıl bir nesnedir?"],
  explanation="isinstance parametreli tiplerle kullanılamaz: TypeError: isinstance() argument 2 cannot be a parameterized generic. Önce isinstance(values, list), sonra öğeleri tek tek denetle.")

q(type="traceback", topic="typeddict-eksik", sectionId="typeddict", difficulty=1,
  prompt="TypedDict'te zorunlu bir anahtar eksik. Okunurken hangi hata oluşur?",
  code=r'''
from typing import TypedDict

class Config(TypedDict):
    host: str
    port: int

cfg: Config = {"host": "localhost"}
print(cfg["port"])
''',
  expectedError="KeyError",
  options=["KeyError", "TypeError", "AttributeError", "ValueError"],
  optionFeedback={
      "TypeError": "Nesne bir dict ve anahtarla erişim geçerli; anahtar yok.",
      "AttributeError": "Öznitelik değil sözlük anahtarı aranıyor.",
      "ValueError": "Bir değer dönüştürülmüyor.",
  },
  hints=["cfg çalışma anında sıradan bir dict.", "Olmayan anahtarı köşeli parantezle okumak hangi hatayı verir?"],
  explanation="TypedDict eksik anahtar için varsayılan eklemez; cfg sıradan bir dict olduğundan cfg['port'] KeyError verir. mypy eksik anahtarı atama satırında, çalıştırmadan bildirirdi.")

q(type="traceback", topic="protocol-ornek", sectionId="protocol", difficulty=2,
  prompt="Bir Protocol sınıfından doğrudan nesne üretiliyor. Hangi hata oluşur?",
  code=r'''
from typing import Protocol

class Shape(Protocol):
    def area(self) -> float: ...

shape = Shape()
''',
  expectedError="TypeError",
  options=["TypeError", "NotImplementedError", "AttributeError", "NameError"],
  optionFeedback={
      "NotImplementedError": "Hata gövdeden değil, nesne kurulurken Protocol kuralından gelir.",
      "AttributeError": "Öznitelik aranmıyor; örnekleme engelleniyor.",
      "NameError": "Shape tanımlı bir sınıftır.",
  },
  hints=["Protocol bir arayüz tanımıdır; kendisi bir uygulama mıdır?", "Hata nesne kurulurken mi çıkıyor?"],
  explanation="Protocol sınıfları örneklenemez: TypeError: Protocols cannot be instantiated. Protocol'e uyan somut bir sınıf yazılıp onun nesnesi kullanılır.")

q(type="traceback", topic="none-kullanimi", sectionId="optional-union", difficulty=2,
  prompt="str | None döndüren fonksiyonun sonucu denetlenmeden kullanılıyor. Hangi hata oluşur?",
  code=r'''
def find(names: list[str], prefix: str) -> str | None:
    for name in names:
        if name.startswith(prefix):
            return name
    return None

print(find(["ada"], "c").upper())
''',
  expectedError="AttributeError",
  options=["AttributeError", "TypeError", "ValueError", "NameError"],
  optionFeedback={
      "TypeError": "Bir işlem değil, None üzerinde olmayan bir metot aranıyor.",
      "ValueError": "Değer dönüştürülmüyor.",
      "NameError": "find ve upper tanımlı; sorun None'da upper olmaması.",
  },
  hints=["'c' ile başlayan bir ad var mı?", "None nesnesinin upper metodu var mı?"],
  explanation="Eşleşme olmadığı için find None döndürür ve None.upper() AttributeError: 'NoneType' object has no attribute 'upper' verir. Önce if result is None denetimi yapılmalı; mypy bu satırı çalıştırmadan işaretlerdi.")
