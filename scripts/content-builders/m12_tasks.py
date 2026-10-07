"""M12 (OOP 2) writing tasks. Imported by build_m12.py."""

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
    id="m12-w1", moduleId=12, sectionId="abc",
    title="Bildirim kanalları", level="Tamamla",
    objective="Soyut bir sınıfın sözleşmesini (format) uygulayan iki alt sınıfı tamamla; ortak deliver metodunu yeniden yazma.",
    prompt="Notifier soyut sınıfı hazır: format(message) soyuttur, deliver(message) ise '-> ' + format(message) döndürür. EmailNotifier hazır. SmsNotifier.format 'SMS: ' ile başlayan metni döndürsün; mesaj 20 karakterden uzunsa yalnızca ilk 17 karakteri alıp '...' eklesin. PushNotifier.format 'PUSH: ' ve büyük harfli mesajı döndürsün. Program 'kanal;mesaj' satırlarını okur (mesajda ';' bulunabilir), bilinmeyen kanalda 'hata: bilinmeyen kanal: ad' yazar ve sonda soyut sınıfın örneklenemediğini gösterir.",
    starterCode=r'''
from abc import ABC, abstractmethod

class Notifier(ABC):
    @abstractmethod
    def format(self, message):
        ...

    def deliver(self, message):
        return f"-> {self.format(message)}"

class EmailNotifier(Notifier):
    def format(self, message):
        return f"[E-posta] {message}"

class SmsNotifier(Notifier):
    def format(self, message):
        # 20 karakterden uzunsa ilk 17 karakter + '...'; sonuç 'SMS: ...' ile başlasın
        pass

class PushNotifier(Notifier):
    # format metodunu yaz: 'PUSH: ' + büyük harfli mesaj
    pass

CHANNELS = {"email": EmailNotifier, "sms": SmsNotifier, "push": PushNotifier}

for _ in range(int(input())):
    channel, message = input().split(";", 1)
    if channel not in CHANNELS:
        print("hata: bilinmeyen kanal:", channel)
        continue
    print(CHANNELS[channel]().deliver(message))
try:
    Notifier()
except TypeError:
    print("soyut: True")
''',
    exampleInput="3\nemail;Merhaba\nsms;Selam\npush;yedek tamam",
    exampleOutput="-> [E-posta] Merhaba\n-> SMS: Selam\n-> PUSH: YEDEK TAMAM\nsoyut: True",
    hints=[
        "PushNotifier soyut format metodunu yazmadığı için örneklenemez; sınıfın içine def format yaz.",
        "SMS için: if len(message) > 20: message = message[:17] + '...' ve sonra f'SMS: {message}' döndür. Push için message.upper() kullan.",
    ],
    solution=r'''
from abc import ABC, abstractmethod

class Notifier(ABC):
    @abstractmethod
    def format(self, message):
        ...

    def deliver(self, message):
        return f"-> {self.format(message)}"

class EmailNotifier(Notifier):
    def format(self, message):
        return f"[E-posta] {message}"

class SmsNotifier(Notifier):
    def format(self, message):
        if len(message) > 20:
            message = message[:17] + "..."
        return f"SMS: {message}"

class PushNotifier(Notifier):
    def format(self, message):
        return f"PUSH: {message.upper()}"

CHANNELS = {"email": EmailNotifier, "sms": SmsNotifier, "push": PushNotifier}

for _ in range(int(input())):
    channel, message = input().split(";", 1)
    if channel not in CHANNELS:
        print("hata: bilinmeyen kanal:", channel)
        continue
    print(CHANNELS[channel]().deliver(message))
try:
    Notifier()
except TypeError:
    print("soyut: True")
''',
    tests=[
        {"label": "Örnek", "stdin": "3\nemail;Merhaba\nsms;Selam\npush;yedek tamam", "expectedOutput": "-> [E-posta] Merhaba\n-> SMS: Selam\n-> PUSH: YEDEK TAMAM\nsoyut: True"},
        {"label": "SMS kısaltma sınırı", "stdin": "3\nsms;Bugün toplantı saat üçte başlıyor\nsms;tam yirmi karakter!!\nsms;tam yirmi karakterli!", "expectedOutput": "-> SMS: Bugün toplantı sa...\n-> SMS: tam yirmi karakter!!\n-> SMS: tam yirmi karakte...\nsoyut: True"},
        {"label": "Bilinmeyen kanal", "stdin": "2\nfax;x\nemail;a", "expectedOutput": "hata: bilinmeyen kanal: fax\n-> [E-posta] a\nsoyut: True"},
        {"label": "Mesajda noktalı virgül", "stdin": "1\nemail;a;b", "expectedOutput": "-> [E-posta] a;b\nsoyut: True"},
    ],
)

task(
    id="m12-w2", moduleId=12, sectionId="operator-overloading",
    title="Para toplama işleçlerini düzelt", level="Düzelt",
    objective="Operandları değiştiren __add__, eksik __radd__ ve ters yönlü __lt__ hatalarını bul ve düzelt.",
    prompt="Money sınıfı kuruş tutar. Program kuruş değerlerini okur, sum ile toplar ve sıralar, sonra ilk nesnenin değişmediğini kontrol eder. Beklenen: toplam yeni bir Money olur, operandlar değişmez, sorted küçükten büyüğe sıralar. Kodda üç hata var: toplama soldaki nesneyi değiştiriyor; sum() çalışmıyor; sıralama ters. Üçünü de düzelt (tanımadığı türde NotImplemented döndürmeyi unutma).",
    starterCode=r'''
class Money:
    def __init__(self, cents):
        self.cents = cents

    def __add__(self, other):
        self.cents += other.cents
        return self

    def __lt__(self, other):
        return self.cents > other.cents

    def __repr__(self):
        return f"Money({self.cents // 100},{self.cents % 100:02d})"

amounts = [int(x) for x in input().split()]
wallet = [Money(a) for a in amounts]
total = sum(wallet)
print("toplam:", total)
print("sıralı:", sorted(wallet))
print("ilk değişmedi:", wallet[0].cents == amounts[0])
''',
    exampleInput="250 175 5",
    exampleOutput="toplam: Money(4,30)\nsıralı: [Money(0,05), Money(1,75), Money(2,50)]\nilk değişmedi: True",
    hints=[
        "sum() ilk adımda 0 + Money hesaplar. int bunu tanımaz; hangi yansıyan işleç metodu gerekli?",
        "__add__ içinde return Money(self.cents + other.cents) yaz; __radd__'de other == 0 ise self döndür; __lt__'de < kullan.",
    ],
    solution=r'''
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

    def __lt__(self, other):
        if not isinstance(other, Money):
            return NotImplemented
        return self.cents < other.cents

    def __repr__(self):
        return f"Money({self.cents // 100},{self.cents % 100:02d})"

amounts = [int(x) for x in input().split()]
wallet = [Money(a) for a in amounts]
total = sum(wallet)
print("toplam:", total)
print("sıralı:", sorted(wallet))
print("ilk değişmedi:", wallet[0].cents == amounts[0])
''',
    tests=[
        {"label": "Örnek", "stdin": "250 175 5", "expectedOutput": "toplam: Money(4,30)\nsıralı: [Money(0,05), Money(1,75), Money(2,50)]\nilk değişmedi: True"},
        {"label": "Tek tutar", "stdin": "100", "expectedOutput": "toplam: Money(1,00)\nsıralı: [Money(1,00)]\nilk değişmedi: True"},
        {"label": "Ters sıralı girdi", "stdin": "300 100 200", "expectedOutput": "toplam: Money(6,00)\nsıralı: [Money(1,00), Money(2,00), Money(3,00)]\nilk değişmedi: True"},
        {"label": "Eşit tutarlar", "stdin": "5 5", "expectedOutput": "toplam: Money(0,10)\nsıralı: [Money(0,05), Money(0,05)]\nilk değişmedi: True"},
    ],
)

task(
    id="m12-w3", moduleId=12, sectionId="dataclass",
    title="Sipariş modeli", level="Sıfırdan yaz",
    objective="Dondurulmuş dataclass, property, dunder metotlar ve değiştirilmiş kopya (replace) ile küçük bir sipariş modeli tasarla.",
    prompt="LineItem ve Order sınıflarını yaz. LineItem dondurulmuş (frozen) bir dataclass'tır: name (str), price (int), qty (int, varsayılan 1); price < 0 ya da qty < 1 ise ValueError(f'geçersiz kalem: {name}'). total property'si price * qty döndürür. Order bir dataclass'tır: items (LineItem listesi, her nesne için ayrı). add(item): aynı adlı kalem varsa adedi toplar ve fiyatı yenisiyle günceller (kalem dondurulmuş olduğundan dataclasses.replace ile yeni kalem üret), yoksa ekler. remove(name): kalem yoksa ValueError(f'bilinmeyen kalem: {name}'). total property'si kalemlerin toplamıdır. report(): kalemleri ada göre sıralı 'ad: adet x fiyat = toplam' satırları ve son satır 'toplam: değer' ile liste olarak döndürür. __len__ kalem sayısını, __contains__(ad) kalemin varlığını söyler. Programın okuma kısmı hazır; sınıfları üstüne yaz.",
    starterCode=r'''
from dataclasses import dataclass, field, replace

# LineItem ve Order sınıflarını buraya yaz.


order = Order()
for _ in range(int(input())):
    parts = input().split()
    try:
        if parts[0] == "ekle":
            order.add(LineItem(parts[1], int(parts[2]), int(parts[3])))
        elif parts[0] == "sil":
            order.remove(parts[1])
        elif parts[0] == "rapor":
            print("\n".join(order.report()))
    except ValueError as error:
        print("hata:", error)
print("kalem sayısı:", len(order), "| elma var:", "elma" in order)
print("dondurulmuş:", LineItem.__dataclass_params__.frozen)
''',
    exampleInput="5\nekle elma 10 5\nekle armut 20 2\nekle elma 12 3\nsil armut\nrapor",
    exampleOutput="elma: 8 x 12 = 96\ntoplam: 96\nkalem sayısı: 1 | elma var: True\ndondurulmuş: True",
    hints=[
        "LineItem için @dataclass(frozen=True) ve __post_init__; Order'daki liste için field(default_factory=list).",
        "add içinde aynı adlı kalemi bulunca self.items[index] = replace(kalem, price=yeni.price, qty=kalem.qty + yeni.qty) yaz. report'ta sorted(self.items, key=lambda item: item.name) kullan.",
    ],
    solution=r'''
from dataclasses import dataclass, field, replace

@dataclass(frozen=True)
class LineItem:
    name: str
    price: int
    qty: int = 1

    def __post_init__(self):
        if self.price < 0 or self.qty < 1:
            raise ValueError(f"geçersiz kalem: {self.name}")

    @property
    def total(self):
        return self.price * self.qty

@dataclass
class Order:
    items: list = field(default_factory=list)

    def add(self, item):
        for index, known in enumerate(self.items):
            if known.name == item.name:
                self.items[index] = replace(known, price=item.price, qty=known.qty + item.qty)
                return
        self.items.append(item)

    def remove(self, name):
        for index, known in enumerate(self.items):
            if known.name == name:
                del self.items[index]
                return
        raise ValueError(f"bilinmeyen kalem: {name}")

    @property
    def total(self):
        return sum(item.total for item in self.items)

    def report(self):
        lines = [f"{item.name}: {item.qty} x {item.price} = {item.total}" for item in sorted(self.items, key=lambda item: item.name)]
        lines.append(f"toplam: {self.total}")
        return lines

    def __len__(self):
        return len(self.items)

    def __contains__(self, name):
        return any(item.name == name for item in self.items)

order = Order()
for _ in range(int(input())):
    parts = input().split()
    try:
        if parts[0] == "ekle":
            order.add(LineItem(parts[1], int(parts[2]), int(parts[3])))
        elif parts[0] == "sil":
            order.remove(parts[1])
        elif parts[0] == "rapor":
            print("\n".join(order.report()))
    except ValueError as error:
        print("hata:", error)
print("kalem sayısı:", len(order), "| elma var:", "elma" in order)
print("dondurulmuş:", LineItem.__dataclass_params__.frozen)
''',
    tests=[
        {"label": "Örnek", "stdin": "5\nekle elma 10 5\nekle armut 20 2\nekle elma 12 3\nsil armut\nrapor", "expectedOutput": "elma: 8 x 12 = 96\ntoplam: 96\nkalem sayısı: 1 | elma var: True\ndondurulmuş: True"},
        {"label": "Hatalar", "stdin": "3\nekle kalem 5 0\nsil süt\nekle kalem -1 2", "expectedOutput": "hata: geçersiz kalem: kalem\nhata: bilinmeyen kalem: süt\nhata: geçersiz kalem: kalem\nkalem sayısı: 0 | elma var: False\ndondurulmuş: True"},
        {"label": "Boş sipariş", "stdin": "1\nrapor", "expectedOutput": "toplam: 0\nkalem sayısı: 0 | elma var: False\ndondurulmuş: True"},
        {"label": "Fiyat güncellenir ve sıralanır", "stdin": "4\nekle b 5 1\nekle a 3 2\nekle b 7 1\nrapor", "expectedOutput": "a: 2 x 3 = 6\nb: 2 x 7 = 14\ntoplam: 20\nkalem sayısı: 2 | elma var: False\ndondurulmuş: True"},
    ],
)
