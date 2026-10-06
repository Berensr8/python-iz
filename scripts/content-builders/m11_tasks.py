"""M11 (OOP 1) writing tasks. Imported by build_m11.py."""

tasks = []


def c(text):
    return text.strip("\n")


def task(**fields):
    for key in ("starterCode", "solution", "exampleOutput"):
        fields[key] = c(fields[key])
    for test in fields["tests"]:
        test["expectedOutput"] = c(test["expectedOutput"])
    tasks.append(fields)


task(
    id="m11-w1", moduleId=11, sectionId="instance-class-vars",
    title="Kitap ödünç takibi", level="Tamamla",
    objective="Nesneye özel durumu (available) ile sınıfın ortak sayacını (borrow_count) birlikte yönet.",
    prompt="Book sınıfını tamamla. Her kitabın title ve available (başlangıçta True) öznitelikleri vardır. borrow() kitap rafta ise available'ı False yapar, sınıfın borrow_count sayacını artırır ve 'ödünç alındı' döndürür; kitap zaten ödünçteyse sayaca dokunmadan 'zaten ödünçte' döndürür. give_back() ödünçteyse available'ı True yapıp 'iade edildi' döndürür, raftaysa 'zaten rafta' döndürür. Program kitap adını, komut sayısını ve komutları ('al' ya da 'ver') okur; her komutun sonucunu yazar, son satırda 'ad: durum (toplam ödünç: N)' gösterir.",
    starterCode=r'''
class Book:
    borrow_count = 0

    def __init__(self, title):
        self.title = title
        self.available = True

    def borrow(self):
        # raftaysa ödünç ver: available False olsun, sınıf sayacı artsın
        return ""

    def give_back(self):
        # ödünçteyse iade al
        return ""

    def status(self):
        return "rafta" if self.available else "ödünçte"

book = Book(input())
for _ in range(int(input())):
    command = input()
    print(book.borrow() if command == "al" else book.give_back())
print(f"{book.title}: {book.status()} (toplam ödünç: {Book.borrow_count})")
''',
    exampleInput="Dune\n3\nal\nver\nal",
    exampleOutput="ödünç alındı\niade edildi\nödünç alındı\nDune: ödünçte (toplam ödünç: 2)",
    hints=[
        "Her iki metot da önce durumu denetlemeli: kitap zaten istenen durumda mı?",
        "Ortak sayaç sınıf üzerinden artırılır: Book.borrow_count += 1. self.borrow_count yazmak nesnede yeni bir öznitelik oluşturur.",
    ],
    solution=r'''
class Book:
    borrow_count = 0

    def __init__(self, title):
        self.title = title
        self.available = True

    def borrow(self):
        if not self.available:
            return "zaten ödünçte"
        self.available = False
        Book.borrow_count += 1
        return "ödünç alındı"

    def give_back(self):
        if self.available:
            return "zaten rafta"
        self.available = True
        return "iade edildi"

    def status(self):
        return "rafta" if self.available else "ödünçte"

book = Book(input())
for _ in range(int(input())):
    command = input()
    print(book.borrow() if command == "al" else book.give_back())
print(f"{book.title}: {book.status()} (toplam ödünç: {Book.borrow_count})")
''',
    tests=[
        {"label": "Örnek", "stdin": "Dune\n3\nal\nver\nal", "expectedOutput": "ödünç alındı\niade edildi\nödünç alındı\nDune: ödünçte (toplam ödünç: 2)"},
        {"label": "Zaten ödünçte", "stdin": "Dune\n2\nal\nal", "expectedOutput": "ödünç alındı\nzaten ödünçte\nDune: ödünçte (toplam ödünç: 1)"},
        {"label": "Zaten rafta", "stdin": "Dune\n1\nver", "expectedOutput": "zaten rafta\nDune: rafta (toplam ödünç: 0)"},
        {"label": "Komut yok", "stdin": "Dune\n0", "expectedOutput": "Dune: rafta (toplam ödünç: 0)"},
    ],
)

task(
    id="m11-w2", moduleId=11, sectionId="inheritance-super",
    title="Oyuncu puanlarını düzelt", level="Düzelt",
    objective="Paylaşılan class değişkeni, eksik super().__init__ çağrısı ve boş liste hatasını bul ve düzelt.",
    prompt="Girdideki her satır bir oyuncudur: 'oyuncu;ad;puanlar' ya da 'kaptan;ad;takım;puanlar' (puanlar virgülle ayrılır ve boş olabilir). Program her oyuncu için 'ad: toplam=T en iyi=E' (kaptanlar için 'ad [takım]: toplam=T en iyi=E') yazar; puanı olmayan oyuncuda ikisi de 0'dır. Kodda üç hata var: her oyuncu aynı puan listesini paylaşıyor; Captain üst sınıfı kurmuyor; puanı olmayan oyuncuda best() hata veriyor. Üçünü de düzelt.",
    starterCode=r'''
class Player:
    scores = []

    def __init__(self, name):
        self.name = name

    def add(self, points):
        self.scores.append(points)

    def total(self):
        return sum(self.scores)

    def best(self):
        return max(self.scores)

    def label(self):
        return self.name

class Captain(Player):
    def __init__(self, name, team):
        self.team = team

    def label(self):
        return f"{self.name} [{self.team}]"

for _ in range(int(input())):
    parts = input().split(";")
    if parts[0] == "oyuncu":
        player = Player(parts[1])
        scores = parts[2]
    else:
        player = Captain(parts[1], parts[2])
        scores = parts[3]
    for text in scores.split(","):
        if text:
            player.add(int(text))
    print(f"{player.label()}: toplam={player.total()} en iyi={player.best()}")
''',
    exampleInput="2\noyuncu;Ada;10,20\nkaptan;Can;Kırmızı;5,30",
    exampleOutput="Ada: toplam=30 en iyi=20\nCan [Kırmızı]: toplam=35 en iyi=30",
    hints=[
        "scores sınıf gövdesinde tanımlı: bütün oyuncular tek bir listeyi paylaşıyor. Nereye taşımalısın? Captain.__init__ da bir şeyi çağırmıyor.",
        "Player.__init__ içinde self.scores = [] kur; Captain.__init__ başında super().__init__(name) çağır; best() için max(self.scores, default=0) kullan.",
    ],
    solution=r'''
class Player:
    def __init__(self, name):
        self.name = name
        self.scores = []

    def add(self, points):
        self.scores.append(points)

    def total(self):
        return sum(self.scores)

    def best(self):
        return max(self.scores, default=0)

    def label(self):
        return self.name

class Captain(Player):
    def __init__(self, name, team):
        super().__init__(name)
        self.team = team

    def label(self):
        return f"{self.name} [{self.team}]"

for _ in range(int(input())):
    parts = input().split(";")
    if parts[0] == "oyuncu":
        player = Player(parts[1])
        scores = parts[2]
    else:
        player = Captain(parts[1], parts[2])
        scores = parts[3]
    for text in scores.split(","):
        if text:
            player.add(int(text))
    print(f"{player.label()}: toplam={player.total()} en iyi={player.best()}")
''',
    tests=[
        {"label": "Örnek", "stdin": "2\noyuncu;Ada;10,20\nkaptan;Can;Kırmızı;5,30", "expectedOutput": "Ada: toplam=30 en iyi=20\nCan [Kırmızı]: toplam=35 en iyi=30"},
        {"label": "Puanlar paylaşılmaz", "stdin": "2\noyuncu;Ada;10\noyuncu;Can;5", "expectedOutput": "Ada: toplam=10 en iyi=10\nCan: toplam=5 en iyi=5"},
        {"label": "Puansız oyuncu", "stdin": "1\noyuncu;Eda;", "expectedOutput": "Eda: toplam=0 en iyi=0"},
        {"label": "Puansız kaptan", "stdin": "1\nkaptan;Bo;Mavi;", "expectedOutput": "Bo [Mavi]: toplam=0 en iyi=0"},
        {"label": "Karışık", "stdin": "3\nkaptan;Ece;Yeşil;7,3\noyuncu;Ali;4\nkaptan;Ege;Sarı;1", "expectedOutput": "Ece [Yeşil]: toplam=10 en iyi=7\nAli: toplam=4 en iyi=4\nEge [Sarı]: toplam=1 en iyi=1"},
    ],
)

task(
    id="m11-w3", moduleId=11, sectionId="composition",
    title="Envanter sınıfları", level="Sıfırdan yaz",
    objective="Property, classmethod ve composition ile küçük bir envanter modeli tasarla.",
    prompt="Item ve Inventory sınıflarını yaz. Item(name, price, qty): value property'si price * qty döndürür; Item.from_line('ad fiyat adet') bir classmethod olarak metinden Item kurar (fiyat ve adet tam sayıdır). Inventory ürünleri ad → Item sözlüğünde tutar; dict'ten türemez (yalnızca object'ten türer, program bunu denetler). add(item): aynı adlı ürün varsa adedi artırır ve fiyatı yenisiyle günceller, yoksa ürünü ekler. remove(name, qty): ürün yoksa ValueError(f'bilinmeyen ürün: {name}'), qty stoktan büyükse ValueError(f'yetersiz stok: {name}') fırlatır; stok sıfıra inerse ürün envanterden silinir. report(): ürünleri ada göre sıralı 'ad: adet x fiyat = değer' satırları ve son satır olarak 'toplam: değer' içeren bir liste döndürür. Programın girdi okuma kısmı hazır; sınıfları üstüne yaz.",
    starterCode=r'''
# Item ve Inventory sınıflarını buraya yaz.


inventory = Inventory()
for _ in range(int(input())):
    parts = input().split()
    try:
        if parts[0] == "ekle":
            inventory.add(Item.from_line(" ".join(parts[1:])))
        elif parts[0] == "çıkar":
            inventory.remove(parts[1], int(parts[2]))
        elif parts[0] == "rapor":
            print("\n".join(inventory.report()))
    except ValueError as error:
        print("hata:", error)
print("kalıtım yok:", Inventory.__bases__ == (object,))
''',
    exampleInput="5\nekle elma 10 5\nekle armut 20 2\nekle elma 12 3\nçıkar elma 4\nrapor",
    exampleOutput="armut: 2 x 20 = 40\nelma: 4 x 12 = 48\ntoplam: 88\nkalıtım yok: True",
    hints=[
        "Item küçük bir veri sınıfıdır; Inventory ise Item'ları _items sözlüğünde tutar ve işi onlara devreder.",
        "add içinde self._items.get(item.name) ile ürünü ara; remove'da stok 0 olunca del self._items[name] yaz; report'ta sorted(self._items.values(), key=...) kullan.",
    ],
    solution=r'''
class Item:
    def __init__(self, name, price, qty):
        self.name = name
        self.price = price
        self.qty = qty

    @property
    def value(self):
        return self.price * self.qty

    @classmethod
    def from_line(cls, text):
        name, price, qty = text.split()
        return cls(name, int(price), int(qty))

class Inventory:
    def __init__(self):
        self._items = {}

    def add(self, item):
        known = self._items.get(item.name)
        if known:
            known.qty += item.qty
            known.price = item.price
        else:
            self._items[item.name] = item

    def remove(self, name, qty):
        item = self._items.get(name)
        if item is None:
            raise ValueError(f"bilinmeyen ürün: {name}")
        if qty > item.qty:
            raise ValueError(f"yetersiz stok: {name}")
        item.qty -= qty
        if item.qty == 0:
            del self._items[name]

    def report(self):
        items = sorted(self._items.values(), key=lambda item: item.name)
        lines = [f"{item.name}: {item.qty} x {item.price} = {item.value}" for item in items]
        lines.append(f"toplam: {sum(item.value for item in items)}")
        return lines

inventory = Inventory()
for _ in range(int(input())):
    parts = input().split()
    try:
        if parts[0] == "ekle":
            inventory.add(Item.from_line(" ".join(parts[1:])))
        elif parts[0] == "çıkar":
            inventory.remove(parts[1], int(parts[2]))
        elif parts[0] == "rapor":
            print("\n".join(inventory.report()))
    except ValueError as error:
        print("hata:", error)
print("kalıtım yok:", Inventory.__bases__ == (object,))
''',
    tests=[
        {"label": "Örnek", "stdin": "5\nekle elma 10 5\nekle armut 20 2\nekle elma 12 3\nçıkar elma 4\nrapor", "expectedOutput": "armut: 2 x 20 = 40\nelma: 4 x 12 = 48\ntoplam: 88\nkalıtım yok: True"},
        {"label": "Bilinmeyen ürün ve yetersiz stok", "stdin": "3\nçıkar süt 1\nekle süt 5 2\nçıkar süt 3", "expectedOutput": "hata: bilinmeyen ürün: süt\nhata: yetersiz stok: süt\nkalıtım yok: True"},
        {"label": "Stok bitince ürün silinir", "stdin": "4\nekle su 3 2\nçıkar su 2\nçıkar su 1\nrapor", "expectedOutput": "hata: bilinmeyen ürün: su\ntoplam: 0\nkalıtım yok: True"},
        {"label": "Boş envanter", "stdin": "1\nrapor", "expectedOutput": "toplam: 0\nkalıtım yok: True"},
        {"label": "Fiyat güncellenir", "stdin": "3\nekle kalem 5 10\nekle kalem 6 5\nrapor", "expectedOutput": "kalem: 15 x 6 = 90\ntoplam: 90\nkalıtım yok: True"},
    ],
)
