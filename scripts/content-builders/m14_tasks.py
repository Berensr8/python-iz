"""M14 (Type hints) writing tasks. Imported by build_m14.py."""

tasks = []


def c(text):
    return text.strip("\n")


def task(**fields):
    for key in ("starterCode", "solution", "exampleOutput"):
        fields[key] = c(fields[key])
    for test in fields["tests"]:
        test["expectedOutput"] = c(test["expectedOutput"])
    tasks.append(fields)


W1_PROGRAM = r'''
valid = []
for _ in range(int(input())):
    result = parse_score(input())
    if result is not None:
        valid.append(result)
avg = average([score for _, score in valid])
print("geçerli:", len(valid))
print("ortalama:", "yok" if avg is None else f"{avg:.1f}")
print("ipuçları doğru:", get_type_hints(parse_score) == {"line": str, "return": tuple[str, int] | None}
      and get_type_hints(average) == {"scores": list[int], "return": float | None})
'''

task(
    id="m14-w1", moduleId=14, sectionId="optional-union",
    title="Puan satırlarını tiplendir", level="Tamamla",
    objective="None döndürebilen iki fonksiyonun ipuçlarını doğru yaz ve None'ı çağıran tarafta güvenle ele al.",
    prompt="Her girdi satırı 'ad:puan' biçiminde olmalı. parse_score(line) hazır: geçersiz satırda None, geçerlide (ad, puan) döndürür; ona ipuçlarını ekle: line: str, dönüş tuple[str, int] | None. average(scores) fonksiyonunu yaz ve ipuçlarını ekle: scores: list[int], dönüş float | None; liste boşsa None, değilse ortalamayı döndürsün. Yerleşik list/tuple ve | yazımını kullan. Program geçerli satır sayısını, ortalamayı (yoksa 'yok') ve ipuçlarının doğru olup olmadığını yazar.",
    starterCode=r'''
from typing import get_type_hints

def parse_score(line):
    # ipuçlarını ekle: str -> tuple[str, int] | None
    name, sep, score = line.partition(":")
    if not sep or not name.strip() or not score.strip().isdigit():
        return None
    return name.strip(), int(score)

def average(scores):
    # ipuçlarını ekle: list[int] -> float | None; boş listede None döndür
    pass
''' + W1_PROGRAM,
    exampleInput="4\nAda:90\nCan:x\nbozuk\nEda:70",
    exampleOutput="geçerli: 2\nortalama: 80.0\nipuçları doğru: True",
    hints=[
        "İpucu sözdizimi: def parse_score(line: str) -> tuple[str, int] | None:",
        "average içinde: if not scores: return None, sonra return sum(scores) / len(scores). İpuçları: (scores: list[int]) -> float | None.",
    ],
    solution=r'''
from typing import get_type_hints

def parse_score(line: str) -> tuple[str, int] | None:
    name, sep, score = line.partition(":")
    if not sep or not name.strip() or not score.strip().isdigit():
        return None
    return name.strip(), int(score)

def average(scores: list[int]) -> float | None:
    if not scores:
        return None
    return sum(scores) / len(scores)
''' + W1_PROGRAM,
    tests=[
        {"label": "Örnek", "stdin": "4\nAda:90\nCan:x\nbozuk\nEda:70", "expectedOutput": "geçerli: 2\nortalama: 80.0\nipuçları doğru: True"},
        {"label": "Ad boş", "stdin": "1\n:50", "expectedOutput": "geçerli: 0\nortalama: yok\nipuçları doğru: True"},
        {"label": "Boşluklu alanlar", "stdin": "2\n Bo : 7 \nAli:8", "expectedOutput": "geçerli: 2\nortalama: 7.5\nipuçları doğru: True"},
        {"label": "Satır yok", "stdin": "0", "expectedOutput": "geçerli: 0\nortalama: yok\nipuçları doğru: True"},
    ],
)

task(
    id="m14-w2", moduleId=14, sectionId="mypy-runtime",
    title="İpuçlarına güvenen kodu onar", level="Düzelt",
    objective="Tip ipuçlarının dönüştürme ve doğrulama yapmadığını hesaba katarak dört hatayı düzelt.",
    prompt="Her girdi satırı 'ürün adet'. Bilinmeyen ürün için 'bilinmeyen: ad', adet 1'den küçükse 'geçersiz adet: ad' yazılıp satır atlanır (önce ürün denetlenir); sonda 'toplam: N' ve price_of'un dönüş ipucunun doğru olup olmadığı yazılır. Kodda dört hata var: adet metin olarak kalıyor (qty: int ipucu dönüştürmez); bilinmeyen ürün None döndürüp hesabı çökertiyor; adet doğrulanmıyor; price_of'un dönüş ipucu None dönebildiğini söylemiyor (int | None olmalı). Dördünü de düzelt.",
    starterCode=r'''
from typing import get_type_hints

PRICES: dict[str, int] = {"kalem": 15, "defter": 40, "silgi": 5}

def price_of(name: str) -> int:
    if name in PRICES:
        return PRICES[name]

def line_total(name: str, qty: int) -> int:
    return price_of(name) * qty

total = 0
for _ in range(int(input())):
    name, qty = input().split()
    total += line_total(name, qty)
print("toplam:", total)
print("dönüş ipucu doğru:", get_type_hints(price_of)["return"] == (int | None))
''',
    exampleInput="3\nkalem 2\ndefter 1\nsilgi 4",
    exampleOutput="toplam: 90\ndönüş ipucu doğru: True",
    hints=[
        "input().split() metin verir; qty: int bunu değiştirmez. price_of ad bulunamazsa ne döndürüyor? Adet 0 ya da negatif olunca ne olmalı?",
        "qty = int(...) ile dönüştür; döngüde önce price_of(name) is None ise 'bilinmeyen' yazıp continue, sonra qty < 1 ise 'geçersiz adet' yazıp continue; price_of'un dönüşünü -> int | None yap.",
    ],
    solution=r'''
from typing import get_type_hints

PRICES: dict[str, int] = {"kalem": 15, "defter": 40, "silgi": 5}

def price_of(name: str) -> int | None:
    if name in PRICES:
        return PRICES[name]

def line_total(name: str, qty: int) -> int:
    return price_of(name) * qty

total = 0
for _ in range(int(input())):
    name, raw = input().split()
    qty = int(raw)
    if price_of(name) is None:
        print("bilinmeyen:", name)
        continue
    if qty < 1:
        print("geçersiz adet:", name)
        continue
    total += line_total(name, qty)
print("toplam:", total)
print("dönüş ipucu doğru:", get_type_hints(price_of)["return"] == (int | None))
''',
    tests=[
        {"label": "Örnek", "stdin": "3\nkalem 2\ndefter 1\nsilgi 4", "expectedOutput": "toplam: 90\ndönüş ipucu doğru: True"},
        {"label": "Bilinmeyen ürün", "stdin": "2\nkalem 1\ncetvel 2", "expectedOutput": "bilinmeyen: cetvel\ntoplam: 15\ndönüş ipucu doğru: True"},
        {"label": "Geçersiz adet", "stdin": "2\ndefter 0\nsilgi -2", "expectedOutput": "geçersiz adet: defter\ngeçersiz adet: silgi\ntoplam: 0\ndönüş ipucu doğru: True"},
        {"label": "Önce ürün denetlenir", "stdin": "3\nkalem 3\nxyz 0\ndefter 2", "expectedOutput": "bilinmeyen: xyz\ntoplam: 125\ndönüş ipucu doğru: True"},
    ],
)

W3_PROGRAM = r'''
@dataclass
class User:
    id: int
    name: str

@dataclass
class Product:
    id: int
    title: str
    price: int

repos = {"kullanıcı": Repository[User](), "ürün": Repository[Product]()}
for _ in range(int(input())):
    kind, command, *rest = input().split()
    repo = repos[kind]
    try:
        if command == "ekle":
            item = User(int(rest[0]), rest[1]) if kind == "kullanıcı" else Product(int(rest[0]), rest[1], int(rest[2]))
            repo.add(item)
            print("eklendi")
        elif command == "getir":
            print(repo.get(int(rest[0])) or "yok")
        elif command == "sil":
            print("silindi" if repo.remove(int(rest[0])) else "yok")
        elif command == "listele":
            print(", ".join(str(item.id) for item in repo.all()) or "boş")
    except ValueError as error:
        print("hata:", error)
print("tipler:", T.__bound__ is HasId, Repository.__parameters__ == (T,))
'''

task(
    id="m14-w3", moduleId=14, sectionId="generics",
    title="Genel depo sınıfı", level="Sıfırdan yaz",
    objective="Protocol, sınırlı TypeVar ve Generic ile her kayıt türüne uyan tek bir depo sınıfı tasarla.",
    prompt="Üç şey yaz. 1) HasId adında bir Protocol: id: int özniteliği. 2) T = TypeVar('T', bound=HasId). 3) Repository(Generic[T]) sınıfı: add(item: T) -> None (aynı id varsa ValueError(f'kimlik zaten var: {id}')), get(item_id: int) -> T | None, remove(item_id: int) -> bool (silindiyse True), all() -> list[T] (kimliğe göre sıralı). User ve Product dataclass'ları ve komut okuma kısmı hazır; aynı Repository sınıfı hem kullanıcılar hem ürünler için kullanılır. Komutlar: 'kullanıcı ekle ID AD', 'ürün ekle ID AD FİYAT', 'TÜR getir ID', 'TÜR sil ID', 'TÜR listele'. Son satır tip tanımlarının adlarını ve bağlarını denetler.",
    starterCode=r'''
from dataclasses import dataclass
from typing import Generic, Protocol, TypeVar

# HasId Protocol'ünü, T TypeVar'ını (bound=HasId) ve Repository(Generic[T]) sınıfını buraya yaz.

''' + W3_PROGRAM,
    exampleInput="5\nkullanıcı ekle 2 Can\nkullanıcı ekle 1 Ada\nkullanıcı listele\nkullanıcı getir 1\nürün getir 1",
    exampleOutput="eklendi\neklendi\n1, 2\nUser(id=1, name='Ada')\nyok\ntipler: True True",
    hints=[
        "Protocol'de öznitelik ipucu yeterlidir: class HasId(Protocol): id: int. T = TypeVar('T', bound=HasId) yazınca T yalnızca id'si olan türleri temsil eder.",
        "Repository içinde kayıtları self._items: dict[int, T] sözlüğünde tut; get için dict.get, remove için pop(item_id, None) is not None, all için sorted anahtarlar kullan.",
    ],
    solution=r'''
from dataclasses import dataclass
from typing import Generic, Protocol, TypeVar

class HasId(Protocol):
    id: int

T = TypeVar("T", bound=HasId)

class Repository(Generic[T]):
    def __init__(self) -> None:
        self._items: dict[int, T] = {}

    def add(self, item: T) -> None:
        if item.id in self._items:
            raise ValueError(f"kimlik zaten var: {item.id}")
        self._items[item.id] = item

    def get(self, item_id: int) -> T | None:
        return self._items.get(item_id)

    def remove(self, item_id: int) -> bool:
        return self._items.pop(item_id, None) is not None

    def all(self) -> list[T]:
        return [self._items[key] for key in sorted(self._items)]
''' + W3_PROGRAM,
    tests=[
        {"label": "Örnek", "stdin": "5\nkullanıcı ekle 2 Can\nkullanıcı ekle 1 Ada\nkullanıcı listele\nkullanıcı getir 1\nürün getir 1", "expectedOutput": "eklendi\neklendi\n1, 2\nUser(id=1, name='Ada')\nyok\ntipler: True True"},
        {"label": "Yinelenen kimlik", "stdin": "3\nürün ekle 7 Kalem 15\nürün ekle 7 Silgi 5\nürün getir 7", "expectedOutput": "eklendi\nhata: kimlik zaten var: 7\nProduct(id=7, title='Kalem', price=15)\ntipler: True True"},
        {"label": "Silme", "stdin": "4\nkullanıcı ekle 3 Eda\nkullanıcı sil 3\nkullanıcı sil 3\nkullanıcı listele", "expectedOutput": "eklendi\nsilindi\nyok\nboş\ntipler: True True"},
        {"label": "Depolar ayrı", "stdin": "2\nkullanıcı ekle 1 Ada\nürün listele", "expectedOutput": "eklendi\nboş\ntipler: True True"},
    ],
)
