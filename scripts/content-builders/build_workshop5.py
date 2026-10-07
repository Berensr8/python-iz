"""Builds Atölye 5 (after M12): an inventory model with dataclasses.

Writes the workshop5-* tasks into content/workshop-tasks.json and the workshop5 definition into
content/milestones.json. As in build_workshops.py, expected outputs come from running each reference
solution; read the printed outputs to check they match the contract in the prompt. Other workshops,
their tasks and the exams are left untouched.
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2] / "content"


def run(code, stdin=""):
    with tempfile.TemporaryDirectory() as scratch:
        result = subprocess.run([sys.executable, "-X", "utf8", "-c", code], input=stdin.encode("utf-8"), capture_output=True, cwd=scratch)
    if result.returncode != 0:
        raise SystemExit(result.stderr.decode("utf-8", "replace"))
    return result.stdout.decode("utf-8").replace("\r\n", "\n").rstrip("\n")


def c(text):
    return text.strip("\n")


tasks = []


def task(id, sectionId, title, level, objective, prompt, starterCode, solution, hints, tests):
    solution, starterCode = c(solution), c(starterCode)
    built = [{"label": label, "stdin": stdin, "expectedOutput": run(solution, stdin)} for label, stdin in tests]
    tasks.append({
        "id": id, "moduleId": 12, "sectionId": sectionId, "title": title, "level": level,
        "objective": objective, "prompt": prompt, "starterCode": starterCode,
        "exampleInput": built[0]["stdin"], "exampleOutput": built[0]["expectedOutput"],
        "hints": hints, "solution": solution, "tests": built,
    })
    print(f"\n== {id} ({len(built)} test)")
    for item in built:
        print(f"  [{item['label']}] girdi={item['stdin']!r}\n      çıktı={item['expectedOutput']!r}")


# ---------------------------------------------------------------- İncele
READ5 = c(r'''
from dataclasses import dataclass

@dataclass
class Item:
    sku: str
    qty: int = 0

class Inventory:
    items = {}

    def add(self, sku, qty):
        item = self.items.setdefault(sku, Item(sku))
        item.qty += qty

a = Inventory()
b = Inventory()
a.add("kalem", 5)
b.add("kalem", 2)
print(a.items["kalem"].qty, len(b.items))
''')

# ---------------------------------------------------------------- Düzelt
FIX_PROGRAM = r'''
warehouses = {"A": Warehouse("A"), "B": Warehouse("B")}
for _ in range(int(input())):
    parts = input().split()
    try:
        if parts[1] == "ekle":
            warehouses[parts[0]].add(parts[2], int(parts[3]))
        elif parts[1] == "çıkar":
            warehouses[parts[0]].remove(parts[2], int(parts[3]))
        elif parts[1] == "rapor":
            print(f"[{parts[0]}]", ", ".join(warehouses[parts[0]].report()) or "boş")
    except ValueError as error:
        print("hata:", error)
'''

task(
    "workshop5-fix", "dataclass", "Depo modelini onar", "Düzelt",
    "Paylaşılan sınıf sözlüğünü, yanlış sıralama alanını ve eksiye düşen stoğu bul ve düzelt.",
    "İki depo (A ve B) var. Komutlar: 'DEPO ekle ÜRÜN ADET', 'DEPO çıkar ÜRÜN ADET' ve 'DEPO rapor'. Sözleşme: her deponun stoğu ayrıdır; çıkarılacak adet stoktan fazlaysa ValueError(f'yetersiz stok: {ürün}') fırlatılır ve stok değişmez; bilinmeyen ürün ValueError(f'bilinmeyen ürün: {ürün}') verir; rapor ürünleri ada göre sıralı 'ürün: adet' biçiminde virgülle yazar, depo boşsa 'boş' yazar. Başlangıç kodunda üç sorun var: depolar birbirinin stoğunu görüyor, rapor ada göre değil adede göre sıralanıyor ve stok eksiye düşebiliyor.",
    r'''
from dataclasses import dataclass

@dataclass(order=True)
class StockItem:
    qty: int
    sku: str

class Warehouse:
    items = {}

    def __init__(self, name):
        self.name = name

    def add(self, sku, qty):
        item = self.items.setdefault(sku, StockItem(qty=0, sku=sku))
        item.qty += qty

    def remove(self, sku, qty):
        if sku not in self.items:
            raise ValueError(f"bilinmeyen ürün: {sku}")
        self.items[sku].qty -= qty

    def report(self):
        return [f"{item.sku}: {item.qty}" for item in sorted(self.items.values())]
''' + FIX_PROGRAM,
    r'''
from dataclasses import dataclass

@dataclass
class StockItem:
    sku: str
    qty: int = 0

class Warehouse:
    def __init__(self, name):
        self.name = name
        self.items = {}

    def add(self, sku, qty):
        item = self.items.setdefault(sku, StockItem(qty=0, sku=sku))
        item.qty += qty

    def remove(self, sku, qty):
        if sku not in self.items:
            raise ValueError(f"bilinmeyen ürün: {sku}")
        item = self.items[sku]
        if qty > item.qty:
            raise ValueError(f"yetersiz stok: {sku}")
        item.qty -= qty

    def report(self):
        return [f"{item.sku}: {item.qty}" for item in sorted(self.items.values(), key=lambda item: item.sku)]
''' + FIX_PROGRAM,
    [
        "İncele adımındaki hatayı hatırla: items nerede tanımlanmış? order=True alanları hangi sırayla karşılaştırır?",
        "items'ı __init__ içinde self.items = {} ile kur; sıralamayı key=lambda item: item.sku ile ya da alan sırasını değiştirerek ada göre yap; remove'da qty > item.qty ise ValueError fırlat.",
    ],
    [
        ("Örnek", "6\nA ekle kalem 5\nA ekle defter 2\nB ekle silgi 4\nA çıkar kalem 3\nA rapor\nB rapor"),
        ("Depolar ayrı", "3\nA ekle kalem 1\nA rapor\nB rapor"),
        ("Yetersiz stok", "3\nA ekle kalem 2\nA çıkar kalem 5\nA rapor"),
        ("Ada göre sıralama", "3\nA ekle zımba 1\nA ekle ataş 9\nA rapor"),
        ("Bilinmeyen ürün", "2\nB çıkar kalem 1\nB rapor"),
    ],
)

# ---------------------------------------------------------------- Sıfırdan yaz
BUILD_PROGRAM = r'''
inventory = Inventory()
for _ in range(int(input())):
    parts = input().split()
    try:
        if parts[0] == "kaydet":
            inventory.register(Product(parts[1], parts[2], int(parts[3])))
        elif parts[0] == "giriş":
            inventory.receive(parts[1], int(parts[2]))
        elif parts[0] == "çıkış":
            inventory.ship(parts[1], int(parts[2]))
        elif parts[0] == "değer":
            print("değer:", inventory.value)
        elif parts[0] == "az":
            print("az:", ", ".join(inventory.low_stock(int(parts[1]))) or "yok")
    except ValueError as error:
        print("hata:", error)
print("ürün:", len(inventory), "| kalem kayıtlı:", "kalem" in inventory, "| dondurulmuş:", Product.__dataclass_params__.frozen)
'''

task(
    "workshop5-build", "dataclass", "Kendi envanter modelini yaz", "Sıfırdan yaz",
    "Dondurulmuş dataclass, doğrulama, property ve dunder metotlarla katalog + stok modeli tasarla.",
    "Product ve Inventory sınıflarını yaz. Product dondurulmuş bir dataclass'tır: sku, name (str), price (int, kuruş); price < 0 ise ValueError(f'geçersiz fiyat: {sku}'). Inventory ürün kataloğunu (sku → Product) ve stok adetlerini (sku → adet) tutar. register(product): aynı sku ikinci kez gelirse ValueError(f'zaten kayıtlı: {sku}'); yeni ürünün stoğu 0'dır. receive(sku, qty) ve ship(sku, qty): kayıtsız ürün ValueError(f'bilinmeyen ürün: {sku}'), qty 1'den küçükse ValueError('adet pozitif olmalı'); ship stoktan fazlasını isterse ValueError(f'yetersiz stok: {sku}'). Hatalı istek durumu değiştirmez. value property'si stoktaki ürünlerin fiyat x adet toplamıdır. low_stock(limit) stoğu limit'ten küçük (eşit değil) ürünlerin sku'larını sıralı liste olarak döndürür. len(inventory) kayıtlı ürün sayısını, 'sku' in inventory kayıtlı olup olmadığını verir. Programın komut okuma kısmı hazır; sınıfları üstüne yaz.",
    r'''
from dataclasses import dataclass

# Product ve Inventory sınıflarını buraya yaz.

''' + BUILD_PROGRAM,
    r'''
from dataclasses import dataclass

@dataclass(frozen=True)
class Product:
    sku: str
    name: str
    price: int

    def __post_init__(self):
        if self.price < 0:
            raise ValueError(f"geçersiz fiyat: {self.sku}")

class Inventory:
    def __init__(self):
        self._catalog = {}
        self._stock = {}

    def register(self, product):
        if product.sku in self._catalog:
            raise ValueError(f"zaten kayıtlı: {product.sku}")
        self._catalog[product.sku] = product
        self._stock[product.sku] = 0

    def _check(self, sku, qty):
        if sku not in self._catalog:
            raise ValueError(f"bilinmeyen ürün: {sku}")
        if qty < 1:
            raise ValueError("adet pozitif olmalı")

    def receive(self, sku, qty):
        self._check(sku, qty)
        self._stock[sku] += qty

    def ship(self, sku, qty):
        self._check(sku, qty)
        if qty > self._stock[sku]:
            raise ValueError(f"yetersiz stok: {sku}")
        self._stock[sku] -= qty

    @property
    def value(self):
        return sum(self._catalog[sku].price * qty for sku, qty in self._stock.items())

    def low_stock(self, limit):
        return sorted(sku for sku, qty in self._stock.items() if qty < limit)

    def __len__(self):
        return len(self._catalog)

    def __contains__(self, sku):
        return sku in self._catalog

''' + BUILD_PROGRAM,
    [
        "Product için @dataclass(frozen=True) ve __post_init__; Inventory'de iki sözlük (katalog ve stok) __init__ içinde kurulsun.",
        "Ortak denetimleri (kayıtlı mı, adet pozitif mi) küçük bir yardımcı metoda topla; ship'te önce bu denetimi, sonra stok yeterliliğini kontrol et. value için @property kullan.",
    ],
    [
        ("Örnek", "7\nkaydet kalem Kalem 150\nkaydet defter Defter 900\ngiriş kalem 10\ngiriş defter 2\nçıkış kalem 4\ndeğer\naz 5"),
        ("Hatalar durum değiştirmez", "8\nkaydet kalem Kalem 150\nkaydet kalem Mavi 200\ngiriş silgi 3\ngiriş kalem 0\ngiriş kalem 2\nçıkış kalem 5\nkaydet cetvel Cetvel -1\ndeğer"),
        ("Sınır: limit dahil değil", "5\nkaydet a A 1\nkaydet b B 1\ngiriş a 3\ngiriş b 2\naz 3"),
        ("Boş envanter", "2\ndeğer\naz 1"),
        ("Stok sıfırlanınca da kayıtlı", "5\nkaydet kalem Kalem 100\ngiriş kalem 1\nçıkış kalem 1\naz 1\ndeğer"),
    ],
)

# ---------------------------------------------------------------- Testlerini kur
TESTS_IMPLS = r'''
class Stock:
    shared = {}

    def __init__(self, bugs=()):
        self.bugs = set(bugs)
        self.counts = Stock.shared if "paylasim" in self.bugs else {}

    def receive(self, sku, qty):
        if qty < 1 and "sifir" not in self.bugs:
            raise ValueError("adet pozitif olmalı")
        self.counts[sku] = self.counts.get(sku, 0) + qty

    def ship(self, sku, qty):
        have = self.counts.get(sku, 0)
        if qty > have and "eksi" not in self.bugs:
            raise ValueError(f"yetersiz stok: {sku}")
        self.counts[sku] = have - qty

    def low_stock(self, limit):
        if "sinir" in self.bugs:
            return sorted(sku for sku, qty in self.counts.items() if qty <= limit)
        return sorted(sku for sku, qty in self.counts.items() if qty < limit)

IMPLS = {"dogru": (), "hata1": ("eksi",), "hata2": ("paylasim",), "hata3": ("sifir",), "hata4": ("sinir",)}

def raises(action):
    try:
        action()
    except ValueError:
        return True
    return False
'''

TESTS_LOOP = r'''
for name in input().split():
    make = lambda: Stock(IMPLS[name])
    print(f"{name}: {'GEÇTİ' if passes(make) else 'YAKALANDI'}")
'''

task(
    "workshop5-tests", "dataclass", "Davranış testlerini kur", "Sıfırdan yaz",
    "Bir stok sınıfının doğru ve hatalı sürümlerini yalnızca davranışına bakarak ayırt eden senaryolar tasarla.",
    "Stock sınıfının bir doğru (dogru) ve dört hatalı sürümü var: hata1 stoğun eksiye düşmesine izin veriyor, hata2 bütün nesnelerde aynı sayaçları paylaşıyor, hata3 0 adetlik girişi kabul ediyor, hata4 low_stock'ta sınırı dahil ediyor (limit'e eşit stok da az sayılıyor). passes(make) fonksiyonunu yaz: make() her çağrıldığında yeni, boş bir Stock verir. Senaryolarını yalnızca genel metotlarla (receive, ship, low_stock) kur, iç sözlüğe (counts) bakma; raises(action) yardımcısı, bir işlemin ValueError fırlatıp fırlatmadığını söyler. Doğru sürümde passes True, her hatalı sürümde False dönmeli. Program sürüm adlarını okur ve her biri için 'ad: GEÇTİ' ya da 'ad: YAKALANDI' yazar.",
    TESTS_IMPLS + r'''
def passes(make):
    # make() ile nesneler kur, davranışları dene; hepsi beklendiği gibiyse True döndür
    pass
''' + TESTS_LOOP,
    TESTS_IMPLS + r'''
def passes(make):
    a, b = make(), make()
    a.receive("kalem", 3)
    checks = [
        raises(lambda: a.ship("kalem", 5)),
        raises(lambda: b.ship("kalem", 1)),
        raises(lambda: a.receive("silgi", 0)),
        a.low_stock(3) == [],
        a.low_stock(4) == ["kalem"],
    ]
    return all(checks)
''' + TESTS_LOOP,
    [
        "Her hata için onu ortaya çıkaran bir davranış düşün: stoktan fazla çıkış, ikinci bir nesnenin boş olması, 0 adetlik giriş, stoğu tam limit kadar olan ürün.",
        "İki nesne kur (a, b = make(), make()), a'ya 3 kalem gir. Sonra: a'dan 5 çıkış hata vermeli, b'den 1 çıkış hata vermeli (b boş), 0 adet giriş hata vermeli, a.low_stock(3) boş ve a.low_stock(4) ['kalem'] olmalı. Sonuçları bir listeye topla ve all(...) döndür.",
    ],
    [
        ("Doğru sürüm", "dogru"),
        ("Eksi stok hatası", "hata1"),
        ("Paylaşılan sayaç hatası", "hata2"),
        ("Sıfır adet hatası", "hata3"),
        ("Sınır hatası", "hata4"),
        ("Karışık sıra", "hata4 dogru hata2 hata1 hata3"),
    ],
)

# ---------------------------------------------------------------- dosyalara yaz
tasks_path = ROOT / "workshop-tasks.json"
mine = {item["id"] for item in tasks}
existing = [item for item in json.loads(tasks_path.read_text(encoding="utf-8")) if item["id"] not in mine]
tasks_path.write_text(json.dumps(existing + tasks, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

milestones_path = ROOT / "milestones.json"
data = json.loads(milestones_path.read_text(encoding="utf-8"))
data["workshops"] = [item for item in data["workshops"] if item["id"] != "workshop5"]
read5_out = run(READ5)
print("\nokuma çıktısı:", repr(read5_out))
data["workshops"].append({
    "id": "workshop5", "afterModule": 12, "title": "Atölye 5 · Envanter modeli",
    "summary": "Önce iki deponun neden aynı stoğu gördüğünü açıkla, sonra bozuk depo modelini onar. Ardından dataclass, property ve dunder metotlarla kendi envanter modelini sıfırdan yaz ve son adımda stok sınıfının hatalı sürümlerini yakalayan davranış testlerini kur.",
    "steps": [
        {"kind": "read", "label": "İncele", "progressKey": "workshop5-read",
         "heading": "İki ayrı envanter nesnesinden sonra ekrana ne yazılır?", "code": READ5,
         "inputLabel": "Çıktı (adet ve ürün sayısı)", "placeholder": "Örn. 5 1",
         "answer": read5_out, "expectedOutput": read5_out,
         "wrongHint": "items sınıfın gövdesinde tanımlanmış; a.items ile b.items aynı sözlük mü, ayrı mı? Item bir dataclass olduğu için kendi qty'si var ama sözlük paylaşılıyor.",
         "explanation": "items bir class değişkenidir (M11): a ve b aynı sözlüğü görür. a.add kalem'i 5 ile ekler, b.add aynı Item nesnesini bulup 2 ekler; sonuç 7'dir ve b'nin sözlüğünde de bir ürün vardır. Çözüm: sözlüğü __init__ içinde self.items = {} ile her depo için ayrı kurmak.",
         "nextLabel": "Düzeltme adımına geç"},
        {"kind": "write", "label": "Düzelt", "taskId": "workshop5-fix",
         "note": "Kontrol listesi: her deponun kendi sözlüğü olsun · rapor ada göre sıralansın · yetersiz stokta hata verilsin ve stok değişmesin.",
         "nextLabel": "Kendi modelini yaz"},
        {"kind": "write", "label": "Sıfırdan yaz", "taskId": "workshop5-build",
         "note": "Önce sınıfların sorumluluklarını ayır: Product değişmeyen katalog bilgisi, Inventory değişen stok durumu. Her hatalı isteğin durumu değiştirmediğinden emin ol.",
         "nextLabel": "Testlerini kur"},
        {"kind": "write", "label": "Testlerini kur", "taskId": "workshop5-tests"},
    ],
})
data["workshops"].sort(key=lambda item: item["afterModule"])
milestones_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("\nyazıldı:", len(tasks), "görev,", len(data["workshops"]), "atölye")
