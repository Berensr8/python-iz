"""M12 (OOP 2) questions. Imported by build_m12.py.

Order: 12 output, 6 bug, 4 fill, 4 order, 10 code, 4 traceback (ids m12-q01 ... m12-q40).
"""

from _qhelper import make_questions

questions, q = make_questions("m12")

# ------------------------------------------------------------------ output (12)
q(type="output", topic="duck-typing", sectionId="polymorphism", difficulty=1,
  prompt="İki ilgisiz sınıfın nesneleri aynı ifadede kullanılıyor. Çıktı ne olur?",
  code=r'''
class Cat:
    def speak(self):
        return "miyav"

class Robot:
    def speak(self):
        return "bip"

print(" ".join(thing.speak() for thing in (Cat(), Robot())))
''',
  expectedOutput="miyav bip",
  options=["miyav bip", "bip miyav", "miyav miyav", "AttributeError verir"],
  hints=["Cat ve Robot'un ortak üst sınıfı var mı? Gerekli mi?", "Her nesne kendi speak metodunu çalıştırır."],
  explanation="Çağıran kod yalnızca speak metodunun var olmasına bakar (duck typing). Cat 'miyav', Robot 'bip' döndürür ve join bunları sırayla birleştirir.")

q(type="output", topic="override", sectionId="polymorphism", difficulty=2,
  prompt="Üst sınıftaki show, alt sınıfın geçersiz kıldığı name'i çağırıyor. Çıktı ne olur?",
  code=r'''
class Base:
    def name(self):
        return "base"

    def show(self):
        return "Ben " + self.name()

class Child(Base):
    def name(self):
        return "child"

print(Base().show(), Child().show(), sep=" | ")
''',
  expectedOutput="Ben base | Ben child",
  options=["Ben base | Ben child", "Ben base | Ben base", "Ben child | Ben child", "Ben base | child"],
  hints=["show Child'da yazılmadı; kimden devralınıyor?", "show içindeki self, Child nesnesi olunca self.name() hangi sürümü çağırır?"],
  explanation="Child, show'u Base'ten devralır ama self bir Child nesnesidir; bu yüzden self.name() Child'ın sürümünü çalıştırır. Aynı metot nesnenin sınıfına göre farklı sonuç verir.")

q(type="output", topic="abc", sectionId="abc", difficulty=2,
  prompt="Soyut sınıf ve somut alt sınıf örneklenmeye çalışılıyor. shapes listesi ne olur?",
  code=r'''
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        ...

class Sq(Shape):
    def __init__(self, side):
        self.side = side

    def area(self):
        return self.side ** 2

shapes = []
for cls, args in ((Shape, ()), (Sq, (3,))):
    try:
        shapes.append(cls(*args).area())
    except TypeError:
        shapes.append("hata")
print(shapes)
''',
  expectedOutput="['hata', 9]",
  options=["['hata', 9]", "[None, 9]", "[9]", "TypeError ile program durur"],
  hints=["Shape() soyut sınıfı doğrudan kurar; ne olur?", "TypeError except bloğunda yakalanıyor."],
  explanation="Shape soyut metodu olduğu için örneklenemez ve TypeError verir; except bunu yakalayıp 'hata' ekler. Sq soyut metodu yazdığı için kurulur ve 3 ** 2 = 9 döner.")

q(type="output", topic="len-bool", sectionId="dunder-basics", difficulty=1,
  prompt="Yalnızca __len__ tanımlı bir sınıfta doğruluk değeri nedir?",
  code=r'''
class Bag:
    def __init__(self, items):
        self.items = items

    def __len__(self):
        return len(self.items)

print(bool(Bag([])), bool(Bag([0])), len(Bag("abc")))
''',
  expectedOutput="False True 3",
  options=["False True 3", "True True 3", "False False 3", "TypeError verir"],
  hints=["__bool__ yoksa Python doğruluk için __len__'e bakar.", "Bag([0]) listesinde bir öğe var (değeri 0 olsa da)."],
  explanation="__bool__ tanımlı değilse __len__ kullanılır: 0 yanlış, diğerleri doğrudur. Bag([]) uzunluğu 0 olduğu için False, Bag([0]) uzunluğu 1 olduğu için True'dur.")

q(type="output", topic="eq-hash", sectionId="dunder-basics", difficulty=3,
  prompt="__eq__ tanımlı, __hash__ yazılmamış bir sınıf set içinde kullanılıyor. Çıktı ne olur?",
  code=r'''
class Tag:
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return self.name == other.name

a, b = Tag("x"), Tag("x")
print(a == b, a != b)
try:
    print(len({a, b}))
except TypeError:
    print("unhashable")
''',
  expectedOutput="True False\nunhashable",
  options=["True False / unhashable", "True False / 1", "True False / 2", "False True / unhashable"],
  hints=["!= varsayılan olarak == sonucunu tersler.", "__eq__ yazılınca __hash__'e ne olur?"],
  explanation="a == b True, a != b False'tır. __eq__ tanımlı ve __hash__ yazılmamış olduğu için Python __hash__'i None yapar; set kurulurken nesneleri hashlemeye çalışınca TypeError (unhashable) oluşur.")

q(type="output", topic="radd", sectionId="operator-overloading", difficulty=2,
  prompt="__add__ ve __radd__ ile sum() birlikte kullanılıyor. Çıktı ne olur?",
  code=r'''
class N:
    def __init__(self, v):
        self.v = v

    def __add__(self, other):
        return N(self.v + (other.v if isinstance(other, N) else other))

    def __radd__(self, other):
        return self + other

    def __repr__(self):
        return f"N({self.v})"

print(N(1) + 2, 3 + N(4), sum([N(1), N(2)]))
''',
  expectedOutput="N(3) N(7) N(3)",
  options=["N(3) N(7) N(3)", "N(3) 7 N(3)", "N(3) N(7) N(2)", "TypeError verir"],
  hints=["3 + N(4) önce int'in __add__'ini dener; sonra ne olur?", "sum(...) 0 + N(1) ile başlar."],
  explanation="N(1) + 2 doğrudan __add__ ile N(3) verir. 3 + N(4)'te int tanımadığı için N(4).__radd__(3) çalışır ve N(7) olur. sum, 0 + N(1)'i __radd__ ile N(1)'e, sonra N(1) + N(2)'yi N(3)'e çevirir.")

q(type="output", topic="karsilastirma", sectionId="operator-overloading", difficulty=3,
  prompt="Yalnızca __lt__ tanımlı bir sınıf sıralanıp karşılaştırılıyor. Çıktı ne olur?",
  code=r'''
class V:
    def __init__(self, n):
        self.n = n

    def __lt__(self, other):
        return self.n < other.n

    def __repr__(self):
        return f"V{self.n}"

items = [V(3), V(1), V(2)]
print(sorted(items), max(items), V(2) > V(1))
try:
    print(V(1) <= V(2))
except TypeError:
    print("TypeError")
''',
  expectedOutput="[V1, V2, V3] V3 True\nTypeError",
  options=[
      "[V1, V2, V3] V3 True / TypeError",
      "[V3, V2, V1] V3 True / TypeError",
      "[V1, V2, V3] V3 True / True",
      "TypeError / TypeError",
  ],
  hints=["V(2) > V(1) için V.__gt__ yoksa Python karşı tarafı dener: V(1) < V(2).", "<= için ne __le__ ne de yansıyan bir karşılığı var."],
  explanation="sorted yalnızca < kullanır. a > b, b < a'ya çevrilebildiği için V(2) > V(1) True verir ve max çalışır. <= ise ne __le__ ne de yansıyan __ge__ olduğu için TypeError üretir.")

q(type="output", topic="mro", sectionId="mro", difficulty=2,
  prompt="Elmas biçimli çoklu kalıtımda MRO listesi nedir?",
  code=r'''
class A:
    pass

class B(A):
    pass

class C(A):
    pass

class D(B, C):
    pass

print([cls.__name__ for cls in D.__mro__])
''',
  expectedOutput="['D', 'B', 'C', 'A', 'object']",
  options=["['D', 'B', 'C', 'A', 'object']", "['D', 'B', 'A', 'C', 'object']", "['D', 'C', 'B', 'A', 'object']", "['D', 'A', 'B', 'C', 'object']"],
  hints=["Sınıf başlığındaki sıra (B, C) korunur.", "Ortak üst sınıf A, hem B'den hem C'den sonra gelmeli."],
  explanation="C3 doğrusallaştırması önce D'yi, sonra başlıktaki sırayla B ve C'yi, ortak üst sınıf A'yı ikisinden sonra ve en sona object'i koyar.")

q(type="output", topic="super-mro", sectionId="mro", difficulty=3,
  prompt="Her sınıf super()'i çağırıyor. D().go() çıktısı nedir?",
  code=r'''
class A:
    def go(self):
        print("A")

class B(A):
    def go(self):
        print("B")
        super().go()

class C(A):
    def go(self):
        print("C")
        super().go()

class D(B, C):
    def go(self):
        print("D")
        super().go()

D().go()
''',
  expectedOutput="D\nB\nC\nA",
  options=["D / B / C / A", "D / B / A", "D / B / A / C", "D / C / B / A"],
  hints=["super(), MRO'da bir sonraki sınıfa gider; üst sınıfa değil.", "D nesnesinin MRO'su: D, B, C, A."],
  explanation="D nesnesinin MRO'su D, B, C, A, object'tir. B'deki super() A'ya değil MRO'daki sonraki sınıf olan C'ye gider; A en sonda bir kez çalışır.")

q(type="output", topic="dataclass-repr", sectionId="dataclass", difficulty=1,
  prompt="Varsayılan değerli bir dataclass yazdırılıyor ve karşılaştırılıyor. Çıktı ne olur?",
  code=r'''
from dataclasses import dataclass

@dataclass
class P:
    x: int
    y: int = 0

print(P(1), P(1) == P(1, 0))
''',
  expectedOutput="P(x=1, y=0) True",
  options=["P(x=1, y=0) True", "P(1, 0) True", "P(x=1, y=0) False", "P(x=1) True"],
  hints=["dataclass __repr__'i alan adlarıyla üretir.", "__eq__ alan alan karşılaştırır."],
  explanation="@dataclass, alan adlarını gösteren bir __repr__ ve alanlara bakan bir __eq__ üretir. P(1)'in y'si varsayılan 0 olduğu için P(1, 0)'a eşittir.")

q(type="output", topic="frozen-replace", sectionId="dataclass", difficulty=2,
  prompt="Dondurulmuş dataclass'tan replace ile kopya üretiliyor. Çıktı ne olur?",
  code=r'''
from dataclasses import dataclass, replace

@dataclass(frozen=True)
class P:
    x: int

q = P(1)
r = replace(q, x=5)
print(q.x, r.x, q == r)
''',
  expectedOutput="1 5 False",
  options=["1 5 False", "5 5 True", "1 5 True", "FrozenInstanceError verir"],
  hints=["replace yeni bir nesne üretir; mevcut nesneyi değiştirmez.", "Alan değerleri farklı olan nesneler eşit değildir."],
  explanation="replace, q'ya dokunmadan x=5 ile yeni bir P üretir. q.x 1 kalır, r.x 5 olur ve alanlar farklı olduğu için q == r False'tır.")

q(type="output", topic="slots", sectionId="slots", difficulty=2,
  prompt="__slots__ tanımlı bir nesnede öznitelik denetleniyor. Çıktı ne olur?",
  code=r'''
class S:
    __slots__ = ("a",)

s = S()
s.a = 1
print(hasattr(s, "__dict__"), hasattr(s, "a"), hasattr(s, "b"))
''',
  expectedOutput="False True False",
  options=["False True False", "True True False", "False True True", "False False False"],
  hints=["__slots__ nesne başına __dict__'i kaldırır.", "b adlı bir slot yok ve hiç atanmadı."],
  explanation="Slotlu nesnenin __dict__'i olmaz (False). a slotuna 1 atandığı için hasattr(s, 'a') True'dur. b hiç tanımlanmadığı için False döner.")

# ------------------------------------------------------------------ bug (6)
q(type="bug", topic="duck-typing", sectionId="polymorphism", difficulty=1,
  prompt="Bu döngü neden ikinci nesnede hata verir?",
  code=r'''
class Circle:
    def area(self):
        return 3

class Square:
    def surface(self):
        return 4

for shape in [Circle(), Square()]:
    print(shape.area())
''',
  answer="Square aynı arayüzü uygulamıyor: area yerine surface tanımlı",
  options=[
      "Square aynı arayüzü uygulamıyor: area yerine surface tanımlı",
      "Listede farklı sınıflar bulunamaz",
      "area yalnızca Circle gibi ortak üst sınıfı olan nesnelerde çağrılabilir",
      "for döngüsü nesnelerin metotlarını çağıramaz",
  ],
  optionFeedback={
      "Listede farklı sınıflar bulunamaz": "Python listeleri her türden nesne taşıyabilir.",
      "area yalnızca Circle gibi ortak üst sınıfı olan nesnelerde çağrılabilir": "Duck typing ortak üst sınıf gerektirmez; metodun adı yeter.",
      "for döngüsü nesnelerin metotlarını çağıramaz": "Döngü içinde metot çağırmak sorunsuzdur; ilk nesne çalışıyor.",
  },
  hints=["İlk nesne için çıktı geliyor mu?", "Square'de hangi adlı metot var?"],
  explanation="Duck typing metot adına bakar. Square, area yerine surface tanımladığı için shape.area() çalışma anında AttributeError verir. Doğru ad area olmalı ya da arayüz soyut bir sınıfla zorunlu kılınmalıdır.")

q(type="bug", topic="abstractmethod", sectionId="abc", difficulty=2,
  prompt="Email().send_message('selam') neden TypeError verir?",
  code=r'''
from abc import ABC, abstractmethod

class Notifier(ABC):
    @abstractmethod
    def send(self, message):
        ...

class Email(Notifier):
    def send_message(self, message):
        print("gönder:", message)

Email().send_message("selam")
''',
  answer="Email soyut send metodunu uygulamıyor (adı send_message); nesne kurulamıyor",
  options=[
      "Email soyut send metodunu uygulamıyor (adı send_message); nesne kurulamıyor",
      "send_message adında alt çizgi kullanılamaz",
      "Soyut sınıfın alt sınıfı kendi yeni metotlarını tanımlayamaz",
      "print soyut sınıf içinde çalışmaz",
  ],
  optionFeedback={
      "send_message adında alt çizgi kullanılamaz": "Alt çizgili metot adları geçerlidir.",
      "Soyut sınıfın alt sınıfı kendi yeni metotlarını tanımlayamaz": "Alt sınıf ek metot tanımlayabilir; asıl sorun zorunlu send'in eksik olması.",
      "print soyut sınıf içinde çalışmaz": "print normal çalışır; hata nesne kurulurken, print'ten önce oluşur.",
  },
  hints=["Hata satırı hangisi: Email() mi, send_message mı?", "Notifier'ın zorunlu kıldığı metot hangi ad?"],
  explanation="Notifier send'i soyut kıldığı halde Email onu yazmadı, bu yüzden Email soyut kalır ve Email() TypeError verir. Metot send adıyla yazılmalıdır.")

q(type="bug", topic="eq-hash", sectionId="dunder-basics", difficulty=2,
  prompt="Bu kod neden TypeError verir?",
  code=r'''
class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)

visited = {Point(1, 2)}
''',
  answer="__eq__ tanımlanınca __hash__ None olur; nesne set öğesi olamaz",
  options=[
      "__eq__ tanımlanınca __hash__ None olur; nesne set öğesi olamaz",
      "Set içine yalnızca sayılar konabilir",
      "__init__ içinde iki öznitelik atanamaz",
      "Küme parantezi yalnızca sözlük oluşturur",
  ],
  optionFeedback={
      "Set içine yalnızca sayılar konabilir": "Set, hashlenebilir her türü (str, tuple, uygun nesneler) alır.",
      "__init__ içinde iki öznitelik atanamaz": "Çoklu atama geçerlidir; bu satırda hata yok.",
      "Küme parantezi yalnızca sözlük oluşturur": "Boş küme parantezi sözlüktür; içinde öğe varsa küme oluşur.",
  },
  hints=["Hata hangi satırda ortaya çıkıyor?", "__eq__ yazınca __hash__'e ne olur?"],
  explanation="Eşit nesnelerin aynı hash'i vermesi gerektiği için Python, __eq__ yazılıp __hash__ yazılmamış sınıflarda __hash__'i None yapar. Nesne set öğesi ya da sözlük anahtarı olamaz; değişmez bir sınıf için __hash__ yazılabilir (örneğin dataclass(frozen=True)).")

q(type="bug", topic="islec-mutasyon", sectionId="operator-overloading", difficulty=2,
  prompt="a + b neden a'yı da değiştiriyor?",
  code=r'''
class Money:
    def __init__(self, cents):
        self.cents = cents

    def __add__(self, other):
        self.cents += other.cents
        return self

a = Money(100)
b = Money(50)
total = a + b
print(a.cents, total.cents)
''',
  answer="__add__ yeni nesne döndürmek yerine self'i değiştirip döndürüyor; toplama operandları bozmamalı",
  options=[
      "__add__ yeni nesne döndürmek yerine self'i değiştirip döndürüyor; toplama operandları bozmamalı",
      "Python + işleciyle her zaman soldaki nesneyi günceller",
      "cents özniteliği başka bir sınıfla paylaşılıyor",
      "other.cents okunurken b değiştirilir",
  ],
  optionFeedback={
      "Python + işleciyle her zaman soldaki nesneyi günceller": "Bu davranış __add__ içindeki += satırından gelir, işlecin kendisinden değil.",
      "cents özniteliği başka bir sınıfla paylaşılıyor": "cents nesneye özgü bir özniteliktir; paylaşım yok.",
      "other.cents okunurken b değiştirilir": "Okumak değiştirmez; asıl değişiklik self.cents += ... satırında.",
  },
  hints=["a.cents çıktıda kaç yazıyor?", "__add__ içinde self'e ne yapılıyor?"],
  explanation="self.cents += other.cents soldaki operandı değiştirir ve self döndürülür; total ile a aynı nesnedir (ikisi de 150). Doğrusu return Money(self.cents + other.cents) olmalı.")

q(type="bug", topic="mixin-super", sectionId="mro", difficulty=3,
  prompt="s.ready neden AttributeError verir?",
  code=r'''
class Base:
    def __init__(self):
        self.ready = True

class LogMixin:
    def __init__(self):
        self.logs = []

class Service(LogMixin, Base):
    pass

s = Service()
print(s.ready)
''',
  answer="LogMixin.__init__ super().__init__() çağırmıyor; MRO'daki Base kurulumu hiç çalışmıyor",
  options=[
      "LogMixin.__init__ super().__init__() çağırmıyor; MRO'daki Base kurulumu hiç çalışmıyor",
      "Service iki üst sınıftan türeyemez",
      "ready özniteliği yalnızca sınıf düzeyinde tanımlanabilir",
      "Base, MRO'da Service'ten önce gelir",
  ],
  optionFeedback={
      "Service iki üst sınıftan türeyemez": "Python çoklu kalıtımı destekler; sorun zincirin kopması.",
      "ready özniteliği yalnızca sınıf düzeyinde tanımlanabilir": "ready bir instance özniteliği; __init__ içinde atanabilir.",
      "Base, MRO'da Service'ten önce gelir": "MRO'da önce Service, sonra LogMixin, sonra Base gelir.",
  },
  hints=["Service'in MRO'su: Service, LogMixin, Base. Service.__init__ yok; hangisi çalışıyor?", "LogMixin.__init__ zincirin devamını çağırıyor mu?"],
  explanation="Service() ilk bulunan __init__'i, yani LogMixin'inkini çalıştırır. O super().__init__() çağırmadığı için zincir kopar ve Base.__init__ hiç çalışmaz; ready kurulmaz. İşbirlikçi kalıtımda zincirdeki her sınıf super()'i çağırmalıdır.")

q(type="bug", topic="dataclass-default", sectionId="dataclass", difficulty=2,
  prompt="Bu sınıf tanımı neden ValueError verir?",
  code=r'''
from dataclasses import dataclass

@dataclass
class Playlist:
    name: str
    songs: list = []
''',
  answer="dataclass değiştirilebilir varsayılan değere izin vermez; field(default_factory=list) kullanılmalı",
  options=[
      "dataclass değiştirilebilir varsayılan değere izin vermez; field(default_factory=list) kullanılmalı",
      "list bir tür olarak anotasyonda kullanılamaz",
      "name alanından sonra başka alan gelemez",
      "dataclass yalnızca int ve str alanlarını destekler",
  ],
  optionFeedback={
      "list bir tür olarak anotasyonda kullanılamaz": "Anotasyonlarda list kullanılabilir; sorun varsayılan değer.",
      "name alanından sonra başka alan gelemez": "İstenen kadar alan tanımlanabilir.",
      "dataclass yalnızca int ve str alanlarını destekler": "Her türde alan tanımlanabilir.",
  },
  hints=["Hata sınıf tanımı sırasında, nesne kurulmadan çıkıyor.", "songs: list = [] tüm nesnelerde aynı listeyi paylaştırırdı."],
  explanation="Liste gibi değiştirilebilir bir varsayılan, bütün nesnelerce paylaşılan tek bir nesne olurdu; dataclass bunu sınıf tanımı sırasında ValueError ile reddeder. Çözüm: songs: list = field(default_factory=list).")

# ------------------------------------------------------------------ fill (4)
q(type="fill", topic="abstractmethod", sectionId="abc", difficulty=1,
  prompt="Alt sınıfların yazması zorunlu olan metodu işaretleyen decorator'ı tamamla.",
  code=r'''
from abc import ABC, abstractmethod

class Shape(ABC):
    @___
    def area(self):
        ...

class Sq(Shape):
    def area(self):
        return 4

print(Sq().area())
''',
  answer="abstractmethod",
  expectedOutput="4",
  hints=["abc modülünden içe aktarılan ikinci ad.", "İngilizce 'soyut metot' demektir."],
  explanation="@abstractmethod, alt sınıfların bu metodu yazmasını zorunlu kılar. Sq area'yı yazdığı için nesnesi kurulabilir.")

q(type="fill", topic="eq", sectionId="dunder-basics", difficulty=2,
  prompt="== işleciyle çağrılan özel metodun adını yaz.",
  code=r'''
class P:
    def __init__(self, x):
        self.x = x

    def ___(self, other):
        return self.x == other.x

print(P(1) == P(1))
''',
  answer="__eq__",
  expectedOutput="True",
  hints=["Eşitlik, 'equal' sözcüğünün kısaltmasıdır.", "Adı iki alt çizgiyle başlayıp biter."],
  explanation="a == b ifadesi a.__eq__(b)'yi çağırır. Varsayılan sürüm kimliğe bakar; kendi __eq__'in değere göre eşitlik tanımlar.")

q(type="fill", topic="dataclass-field", sectionId="dataclass", difficulty=2,
  prompt="Her nesne için yeni bir liste kuran alan tanımını tamamla.",
  code=r'''
from dataclasses import dataclass, field

@dataclass
class Box:
    tags: list = ___(default_factory=list)

print(Box().tags, Box().tags is Box().tags)
''',
  answer="field",
  expectedOutput="[] False",
  hints=["dataclasses modülünden içe aktarılan ikinci ad.", "default_factory bu işlevin bir parametresidir."],
  explanation="field(default_factory=list) her nesne için yeni bir liste üretir; bu yüzden iki Box aynı listeyi paylaşmaz (is False).")

q(type="fill", topic="descriptor", sectionId="descriptor-metaclass", difficulty=3,
  prompt="Descriptor'ün öznitelik okunurken çağrılan metodunun adını yaz.",
  code=r'''
class Upper:
    def ___(self, obj, owner=None):
        return "HAV"

class Dog:
    sound = Upper()

print(Dog().sound)
''',
  answer="__get__",
  expectedOutput="HAV",
  hints=["Descriptor protokolünün okuma metodu.", "Adı 'get' sözcüğünü içerir."],
  explanation="Sınıf özniteliği olan nesne __get__ tanımlıyorsa Dog().sound okunurken Python bu metodu çağırır ve dönen değeri verir; property'nin çalışma biçimi de budur.")

# ------------------------------------------------------------------ order (4)
q(type="order", topic="duck-typing", sectionId="polymorphism", difficulty=1,
  prompt="İki ilgisiz sınıfı aynı döngüde konuşturacak sırayı kur.",
  answer_lines=[
      "class Dog:",
      "    def speak(self):",
      "        return 'hav'",
      "class Cat:",
      "    def speak(self):",
      "        return 'miyav'",
      "for pet in (Dog(), Cat()):",
      "    print(pet.speak())",
  ],
  perm=[6, 3, 1, 7, 0, 4, 2, 5],
  expectedOutput="hav\nmiyav",
  hints=["Sınıflar döngüden önce tanımlanır.", "Her metot gövdesi tanım başlığının altında girintilidir."],
  explanation="Dog ve Cat aynı adlı speak metodunu sunar; döngü hangisi olduğunu sormadan çağırır (duck typing).")

q(type="order", topic="abstractmethod", sectionId="abc", difficulty=2,
  prompt="Soyut sınıfı ve onu uygulayan alt sınıfı kullanacak sırayı kur.",
  answer_lines=[
      "from abc import ABC, abstractmethod",
      "class Base(ABC):",
      "    @abstractmethod",
      "    def run(self):",
      "        ...",
      "class Job(Base):",
      "    def run(self):",
      "        return 'bitti'",
      "print(Job().run())",
  ],
  perm=[6, 2, 8, 0, 4, 7, 1, 5, 3],
  expectedOutput="bitti",
  hints=["İçe aktarma en üstte olmalı.", "Decorator, uyguladığı metodun hemen üstünde durur."],
  explanation="abc içe aktarılır, soyut Base tanımlanır, Job soyut metodu yazar ve nesne en sonda kurulup çağrılır.")

q(type="order", topic="dataclass", sectionId="dataclass", difficulty=2,
  prompt="Bir dataclass tanımlayıp yazdıracak sırayı kur.",
  answer_lines=[
      "from dataclasses import dataclass",
      "@dataclass",
      "class Point:",
      "    x: int",
      "    y: int",
      "print(Point(1, 2))",
  ],
  perm=[4, 1, 5, 0, 3, 2],
  expectedOutput="Point(x=1, y=2)",
  hints=["Decorator, class satırının hemen üstündedir.", "Alanlar sınıf başlığından sonra gelir."],
  explanation="Önce dataclass içe aktarılır, sonra @dataclass ile işaretlenen sınıf iki alanla tanımlanır; nesne yazdırılınca üretilen __repr__ alan adlarını gösterir.")

q(type="order", topic="mixin", sectionId="mro", difficulty=3,
  prompt="Mixin'in super() ile Animal'a ulaştığı sırayı kur.",
  answer_lines=[
      "class Animal:",
      "    def speak(self):",
      "        return 'hav'",
      "class Loud:",
      "    def speak(self):",
      "        return super().speak().upper()",
      "class Dog(Loud, Animal):",
      "    pass",
      "print(Dog().speak())",
  ],
  perm=[8, 3, 6, 1, 0, 5, 7, 2, 4],
  expectedOutput="HAV",
  hints=["Dog'un MRO'su: Dog, Loud, Animal.", "Loud içindeki super() Animal'a gider; Animal ve Loud, Dog'dan önce tanımlanmalı."],
  explanation="Dog(Loud, Animal) için MRO Dog, Loud, Animal'dır. Loud.speak, super() ile Animal.speak'i çağırır ve sonucu büyük harfe çevirir.")

# ------------------------------------------------------------------ code (10)
q(type="code", topic="duck-typing", sectionId="polymorphism", difficulty=1,
  prompt="Square hazır. Rectangle (genişlik, yükseklik) ve Triangle (taban, yükseklik) sınıflarının area() metotlarını yaz; ikisinin de ortak üst sınıfı olması gerekmez. Program şekilleri okuyup her birinin alanını ve toplamı yazdırır.",
  starterCode=r'''
class Square:
    def __init__(self, side):
        self.side = side

    def area(self):
        return self.side ** 2

class Rectangle:
    def __init__(self, width, height):
        self.width, self.height = width, height

    def area(self):
        pass

class Triangle:
    def __init__(self, base, height):
        self.base, self.height = base, height

    def area(self):
        pass

shapes = []
for _ in range(int(input())):
    kind, *numbers = input().split()
    numbers = [int(n) for n in numbers]
    if kind == "kare":
        shapes.append(Square(*numbers))
    elif kind == "dikdörtgen":
        shapes.append(Rectangle(*numbers))
    else:
        shapes.append(Triangle(*numbers))
for shape in shapes:
    print(f"{type(shape).__name__}: {shape.area():.1f}")
print(f"toplam: {sum(shape.area() for shape in shapes):.1f}")
''',
  answer=r'''
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

shapes = []
for _ in range(int(input())):
    kind, *numbers = input().split()
    numbers = [int(n) for n in numbers]
    if kind == "kare":
        shapes.append(Square(*numbers))
    elif kind == "dikdörtgen":
        shapes.append(Rectangle(*numbers))
    else:
        shapes.append(Triangle(*numbers))
for shape in shapes:
    print(f"{type(shape).__name__}: {shape.area():.1f}")
print(f"toplam: {sum(shape.area() for shape in shapes):.1f}")
''',
  exampleInput="3\nkare 3\ndikdörtgen 2 5\nüçgen 4 5",
  expectedOutput="Square: 9.0\nRectangle: 10.0\nTriangle: 10.0\ntoplam: 29.0",
  tests=[
      {"label": "Üç şekil", "stdin": "3\nkare 3\ndikdörtgen 2 5\nüçgen 4 5", "expectedOutput": "Square: 9.0\nRectangle: 10.0\nTriangle: 10.0\ntoplam: 29.0"},
      {"label": "Şekil yok", "stdin": "0", "expectedOutput": "toplam: 0.0"},
      {"label": "Yalnız üçgen", "stdin": "1\nüçgen 3 3", "expectedOutput": "Triangle: 4.5\ntoplam: 4.5"},
      {"label": "Aynı tür tekrar", "stdin": "2\nkare 1\nkare 2", "expectedOutput": "Square: 1.0\nSquare: 4.0\ntoplam: 5.0"},
  ],
  hints=["Dikdörtgenin alanı genişlik çarpı yükseklik, üçgeninki taban çarpı yükseklik bölü iki.", "Metotlar değeri return ile döndürmeli; ortak üst sınıf yazma."],
  explanation="Her sınıf aynı area adını sunduğu için döngü ve sum nesnenin türünü bilmeden çalışır (duck typing).")

q(type="code", topic="abc", sectionId="abc", difficulty=2,
  prompt="PriceRule soyut sınıfı hazır: apply(price) soyuttur, final(price) ise apply sonucunu 0'ın altına düşürmez. Percent(yüzde) ve Fixed(tutar) alt sınıflarını yaz: Percent price * (100 - yüzde) // 100, Fixed price - tutar hesaplar. Program 'yüzde N' ya da 'sabit N' kuralını ve fiyatı okur.",
  starterCode=r'''
from abc import ABC, abstractmethod

class PriceRule(ABC):
    @abstractmethod
    def apply(self, price):
        ...

    def final(self, price):
        return max(0, self.apply(price))

class Percent(PriceRule):
    pass

class Fixed(PriceRule):
    pass

kind, value = input().split()
price = int(input())
rule = Percent(int(value)) if kind == "yüzde" else Fixed(int(value))
print(rule.final(price))
try:
    PriceRule()
except TypeError:
    print("soyut: True")
''',
  answer=r'''
from abc import ABC, abstractmethod

class PriceRule(ABC):
    @abstractmethod
    def apply(self, price):
        ...

    def final(self, price):
        return max(0, self.apply(price))

class Percent(PriceRule):
    def __init__(self, percent):
        self.percent = percent

    def apply(self, price):
        return price * (100 - self.percent) // 100

class Fixed(PriceRule):
    def __init__(self, amount):
        self.amount = amount

    def apply(self, price):
        return price - self.amount

kind, value = input().split()
price = int(input())
rule = Percent(int(value)) if kind == "yüzde" else Fixed(int(value))
print(rule.final(price))
try:
    PriceRule()
except TypeError:
    print("soyut: True")
''',
  exampleInput="yüzde 10\n200",
  expectedOutput="180\nsoyut: True",
  tests=[
      {"label": "Yüzde", "stdin": "yüzde 10\n200", "expectedOutput": "180\nsoyut: True"},
      {"label": "Sabit", "stdin": "sabit 50\n200", "expectedOutput": "150\nsoyut: True"},
      {"label": "Negatif sonuç sıfırlanır", "stdin": "sabit 500\n200", "expectedOutput": "0\nsoyut: True"},
      {"label": "Yüzde yüz", "stdin": "yüzde 100\n80", "expectedOutput": "0\nsoyut: True"},
  ],
  hints=["Her alt sınıfın __init__'i indirim değerini saklamalı.", "final'ı yeniden yazma; yalnızca apply'ı yaz."],
  explanation="Alt sınıflar yalnızca soyut apply'ı yazar; ortak final metodu hepsinde aynı kuralı (0'ın altına düşme) uygular.")

q(type="code", topic="dunder", sectionId="dunder-basics", difficulty=2,
  prompt="Library sınıfına __len__, __getitem__ ve __contains__ ekle (contains büyük/küçük harfe bakmasın). Program kitapları ve bir sorgu adını okur; kitaplık boşsa 'boş kitaplık', değilse sayıyı, ilk ve son kitabı yazar; ardından sorgu kitaplıkta varsa 'var' yoksa 'yok' der.",
  starterCode=r'''
class Library:
    def __init__(self, titles):
        self._titles = list(titles)

    # __len__, __getitem__ ve __contains__ yaz

titles = [input() for _ in range(int(input()))]
query = input()
library = Library(titles)
if not library:
    print("boş kitaplık")
else:
    print(len(library), library[0], library[-1])
print("var" if query in library else "yok")
''',
  answer=r'''
class Library:
    def __init__(self, titles):
        self._titles = list(titles)

    def __len__(self):
        return len(self._titles)

    def __getitem__(self, index):
        return self._titles[index]

    def __contains__(self, title):
        return title.lower() in (t.lower() for t in self._titles)

titles = [input() for _ in range(int(input()))]
query = input()
library = Library(titles)
if not library:
    print("boş kitaplık")
else:
    print(len(library), library[0], library[-1])
print("var" if query in library else "yok")
''',
  exampleInput="3\nDune\nEmma\nUlysses\nemma",
  expectedOutput="3 Dune Ulysses\nvar",
  tests=[
      {"label": "Büyük/küçük harf", "stdin": "3\nDune\nEmma\nUlysses\nemma", "expectedOutput": "3 Dune Ulysses\nvar"},
      {"label": "Olmayan kitap", "stdin": "2\nA\nB\nC", "expectedOutput": "2 A B\nyok"},
      {"label": "Boş kitaplık", "stdin": "0\nX", "expectedOutput": "boş kitaplık\nyok"},
      {"label": "Tek kitap", "stdin": "1\nDune\nDUNE", "expectedOutput": "1 Dune Dune\nvar"},
  ],
  hints=["if not library koşulu __len__'e dayanır; ayrıca __bool__ yazmana gerek yok.", "__contains__ içinde her iki tarafı da lower() ile karşılaştır."],
  explanation="__len__ hem len()'i hem boşluk denetimini (if not library) sağlar; __getitem__ indekslemeyi, __contains__ in işlecini tanımlar.")

q(type="code", topic="islec", sectionId="operator-overloading", difficulty=2,
  prompt="Vec sınıfına __add__, __sub__, __mul__ (sayıyla çarpma) ve __eq__ ekle; işleçler yeni Vec döndürsün. __repr__ hazır. Program iki vektörü ve bir sayıyı okur; toplam, fark, ilk vektörün sayıyla çarpımı ve eşitlik sonucunu yazdırır.",
  starterCode=r'''
class Vec:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __repr__(self):
        return f"Vec({self.x}, {self.y})"

    # __add__, __sub__, __mul__ ve __eq__ yaz

x1, y1 = map(int, input().split())
x2, y2 = map(int, input().split())
k = int(input())
a, b = Vec(x1, y1), Vec(x2, y2)
print(a + b)
print(a - b)
print(a * k)
print(a == b)
''',
  answer=r'''
class Vec:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __repr__(self):
        return f"Vec({self.x}, {self.y})"

    def __add__(self, other):
        return Vec(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vec(self.x - other.x, self.y - other.y)

    def __mul__(self, k):
        return Vec(self.x * k, self.y * k)

    def __eq__(self, other):
        if not isinstance(other, Vec):
            return NotImplemented
        return (self.x, self.y) == (other.x, other.y)

x1, y1 = map(int, input().split())
x2, y2 = map(int, input().split())
k = int(input())
a, b = Vec(x1, y1), Vec(x2, y2)
print(a + b)
print(a - b)
print(a * k)
print(a == b)
''',
  exampleInput="3 4\n1 1\n2",
  expectedOutput="Vec(4, 5)\nVec(2, 3)\nVec(6, 8)\nFalse",
  tests=[
      {"label": "Normal", "stdin": "3 4\n1 1\n2", "expectedOutput": "Vec(4, 5)\nVec(2, 3)\nVec(6, 8)\nFalse"},
      {"label": "Eşit vektörler", "stdin": "2 2\n2 2\n3", "expectedOutput": "Vec(4, 4)\nVec(0, 0)\nVec(6, 6)\nTrue"},
      {"label": "Negatif", "stdin": "-1 5\n4 -2\n-1", "expectedOutput": "Vec(3, 3)\nVec(-5, 7)\nVec(1, -5)\nFalse"},
      {"label": "Sıfırla çarpma", "stdin": "7 8\n0 0\n0", "expectedOutput": "Vec(7, 8)\nVec(7, 8)\nVec(0, 0)\nFalse"},
  ],
  hints=["Her işleç yeni bir Vec döndürmeli; self'i değiştirme.", "__eq__ için koordinat çiftlerini karşılaştır."],
  explanation="İşleç metotları operandları değiştirmeden yeni nesne üretir; __eq__ değere göre eşitlik tanımlar.")

q(type="code", topic="total-ordering", sectionId="operator-overloading", difficulty=3,
  prompt="Version sınıfı sürüm metnini ('1.10.2') tam sayı demetine çevirir. total_ordering ile sıralanabilmesi için __eq__ ve __lt__ yaz (demetleri karşılaştır). __str__ hazır. Program sürümleri okuyup sıralar, en yenisini yazar ve <=, >= denemesinin sonucunu gösterir.",
  starterCode=r'''
from functools import total_ordering

@total_ordering
class Version:
    def __init__(self, text):
        self.text = text
        self.parts = tuple(int(part) for part in text.split("."))

    def __str__(self):
        return self.text

    # __eq__ ve __lt__ yaz

versions = [Version(input()) for _ in range(int(input()))]
print(" < ".join(str(v) for v in sorted(versions)))
print("en yeni:", max(versions))
print(Version("1.0") <= Version("1.0"), Version("1.0") >= Version("2.0"))
''',
  answer=r'''
from functools import total_ordering

@total_ordering
class Version:
    def __init__(self, text):
        self.text = text
        self.parts = tuple(int(part) for part in text.split("."))

    def __str__(self):
        return self.text

    def __eq__(self, other):
        if not isinstance(other, Version):
            return NotImplemented
        return self.parts == other.parts

    def __lt__(self, other):
        if not isinstance(other, Version):
            return NotImplemented
        return self.parts < other.parts

versions = [Version(input()) for _ in range(int(input()))]
print(" < ".join(str(v) for v in sorted(versions)))
print("en yeni:", max(versions))
print(Version("1.0") <= Version("1.0"), Version("1.0") >= Version("2.0"))
''',
  exampleInput="3\n1.2.0\n1.10.0\n1.9.5",
  expectedOutput="1.2.0 < 1.9.5 < 1.10.0\nen yeni: 1.10.0\nTrue False",
  tests=[
      {"label": "Sayısal sıralama", "stdin": "3\n1.2.0\n1.10.0\n1.9.5", "expectedOutput": "1.2.0 < 1.9.5 < 1.10.0\nen yeni: 1.10.0\nTrue False"},
      {"label": "Tek sürüm", "stdin": "1\n3.1", "expectedOutput": "3.1\nen yeni: 3.1\nTrue False"},
      {"label": "Farklı uzunluk", "stdin": "2\n2.0.0\n2.0", "expectedOutput": "2.0 < 2.0.0\nen yeni: 2.0.0\nTrue False"},
      {"label": "Ters girdi", "stdin": "3\n10.0\n9.9\n9.10", "expectedOutput": "9.9 < 9.10 < 10.0\nen yeni: 10.0\nTrue False"},
  ],
  hints=["Metin yerine self.parts demetlerini karşılaştır: '1.10' metin olarak '1.9'dan küçüktür, sayı olarak büyüktür.", "total_ordering, yalnızca __eq__ ve bir sıralama metodundan diğerlerini türetir."],
  explanation="Sürümleri metin olarak karşılaştırmak '1.10' < '1.9' sonucunu verirdi. Tam sayı demetleri doğru sıralar; total_ordering eksik karşılaştırma işleçlerini tamamlar.")

q(type="code", topic="mixin", sectionId="mro", difficulty=2,
  prompt="JsonMixin'e to_json() (vars(self)'i anahtarlara göre sıralı ve ensure_ascii=False ile JSON'a çevirir) ve from_json(text) classmethod'unu (JSON'u çözüp cls(**veri) kurar) yaz. User ve Product mixin'i kullanır. Program bir nesne kurar, JSON'a çevirir, geri kurar ve eşitliği gösterir.",
  starterCode=r'''
import json

class JsonMixin:
    def to_json(self):
        # vars(self)'i anahtarları sıralı, ensure_ascii=False ile JSON'a çevir
        return ""

    @classmethod
    def from_json(cls, text):
        # JSON'u çöz ve cls(**veri) ile nesne kur
        return None

class User(JsonMixin):
    def __init__(self, name, age):
        self.name, self.age = name, age

class Product(JsonMixin):
    def __init__(self, title, price):
        self.title, self.price = title, price

kind = input()
first = input()
second = int(input())
model = User if kind == "user" else Product
obj = model(first, second)
text = obj.to_json()
print(text)
copy = model.from_json(text)
print(type(copy).__name__, vars(copy) == vars(obj))
''',
  answer=r'''
import json

class JsonMixin:
    def to_json(self):
        return json.dumps(vars(self), sort_keys=True, ensure_ascii=False)

    @classmethod
    def from_json(cls, text):
        return cls(**json.loads(text))

class User(JsonMixin):
    def __init__(self, name, age):
        self.name, self.age = name, age

class Product(JsonMixin):
    def __init__(self, title, price):
        self.title, self.price = title, price

kind = input()
first = input()
second = int(input())
model = User if kind == "user" else Product
obj = model(first, second)
text = obj.to_json()
print(text)
copy = model.from_json(text)
print(type(copy).__name__, vars(copy) == vars(obj))
''',
  exampleInput="user\nAda\n30",
  expectedOutput='{"age": 30, "name": "Ada"}\nUser True',
  tests=[
      {"label": "Kullanıcı", "stdin": "user\nAda\n30", "expectedOutput": '{"age": 30, "name": "Ada"}\nUser True'},
      {"label": "Ürün", "stdin": "product\nKalem\n12", "expectedOutput": '{"price": 12, "title": "Kalem"}\nProduct True'},
      {"label": "Türkçe karakter", "stdin": "user\nÇağrı\n5", "expectedOutput": '{"age": 5, "name": "Çağrı"}\nUser True'},
      {"label": "Sıfır fiyat", "stdin": "product\nDefter\n0", "expectedOutput": '{"price": 0, "title": "Defter"}\nProduct True'},
  ],
  hints=["json.dumps için sort_keys=True ve ensure_ascii=False ver.", "from_json'da cls(**json.loads(text)) yaz; sınıf adını sabit yazma."],
  explanation="Mixin, kendi başına örneklenmeyen ama her sınıfa aynı davranışı ekleyen küçük bir sınıftır. from_json'daki cls sayesinde User.from_json User, Product.from_json Product üretir.")

q(type="code", topic="dataclass", sectionId="dataclass", difficulty=2,
  prompt="Student adında bir dataclass yaz: name (str) ve grades (liste; her nesne için ayrı, varsayılan boş). average() notların ortalamasını, not yoksa 0.0 döndürsün. Program öğrencileri okur, ortalamaları yazar ve iki öğrencinin not listesini paylaşmadığını gösterir.",
  starterCode=r'''
from dataclasses import dataclass, field

# Student dataclass'ını yaz

for _ in range(int(input())):
    name, *grades = input().split()
    student = Student(name, [int(g) for g in grades])
    print(f"{student.name}: {student.average():.1f}")
print("liste paylaşılmıyor:", Student("a").grades is not Student("b").grades)
''',
  answer=r'''
from dataclasses import dataclass, field

@dataclass
class Student:
    name: str
    grades: list = field(default_factory=list)

    def average(self):
        return sum(self.grades) / len(self.grades) if self.grades else 0.0

for _ in range(int(input())):
    name, *grades = input().split()
    student = Student(name, [int(g) for g in grades])
    print(f"{student.name}: {student.average():.1f}")
print("liste paylaşılmıyor:", Student("a").grades is not Student("b").grades)
''',
  exampleInput="2\nAda 90 80\nCan 70",
  expectedOutput="Ada: 85.0\nCan: 70.0\nliste paylaşılmıyor: True",
  tests=[
      {"label": "İki öğrenci", "stdin": "2\nAda 90 80\nCan 70", "expectedOutput": "Ada: 85.0\nCan: 70.0\nliste paylaşılmıyor: True"},
      {"label": "Notu olmayan", "stdin": "1\nEda", "expectedOutput": "Eda: 0.0\nliste paylaşılmıyor: True"},
      {"label": "Öğrenci yok", "stdin": "0", "expectedOutput": "liste paylaşılmıyor: True"},
      {"label": "Ondalık ortalama", "stdin": "1\nBo 1 2", "expectedOutput": "Bo: 1.5\nliste paylaşılmıyor: True"},
  ],
  hints=["grades için field(default_factory=list) kullan.", "average içinde boş listeyi ayrı karşıla."],
  explanation="@dataclass __init__ ve __repr__'i üretir; default_factory her öğrenciye ayrı bir liste verir. Boş listede ortalama 0.0 olarak ayrıca ele alınır.")

q(type="code", topic="frozen-order", sectionId="dataclass", difficulty=3,
  prompt="Task'ı sıralanabilir (order=True) ve değiştirilemez (frozen=True) bir dataclass yap: priority (int) ve title (str). priority 1'den küçükse __post_init__ ValueError('öncelik 1 veya daha büyük olmalı') fırlatsın. Program görevleri okur, geçersizleri 'hata: ...' ile bildirir, geçerlileri sıralı yazar ve ilk görevi değiştirmeyi dener.",
  starterCode=r'''
from dataclasses import dataclass, FrozenInstanceError

@dataclass
class Task:
    priority: int
    title: str

tasks = []
for _ in range(int(input())):
    priority, title = input().split(maxsplit=1)
    try:
        tasks.append(Task(int(priority), title))
    except ValueError as error:
        print("hata:", error)
for task in sorted(tasks):
    print(f"{task.priority}: {task.title}")
if tasks:
    try:
        tasks[0].priority = 99
    except FrozenInstanceError:
        print("değiştirilemez")
''',
  answer=r'''
from dataclasses import dataclass, FrozenInstanceError

@dataclass(order=True, frozen=True)
class Task:
    priority: int
    title: str

    def __post_init__(self):
        if self.priority < 1:
            raise ValueError("öncelik 1 veya daha büyük olmalı")

tasks = []
for _ in range(int(input())):
    priority, title = input().split(maxsplit=1)
    try:
        tasks.append(Task(int(priority), title))
    except ValueError as error:
        print("hata:", error)
for task in sorted(tasks):
    print(f"{task.priority}: {task.title}")
if tasks:
    try:
        tasks[0].priority = 99
    except FrozenInstanceError:
        print("değiştirilemez")
''',
  exampleInput="3\n2 rapor\n1 test\n3 yayın",
  expectedOutput="1: test\n2: rapor\n3: yayın\ndeğiştirilemez",
  tests=[
      {"label": "Sıralama", "stdin": "3\n2 rapor\n1 test\n3 yayın", "expectedOutput": "1: test\n2: rapor\n3: yayın\ndeğiştirilemez"},
      {"label": "Geçersiz öncelik", "stdin": "2\n0 hatalı\n1 iyi", "expectedOutput": "hata: öncelik 1 veya daha büyük olmalı\n1: iyi\ndeğiştirilemez"},
      {"label": "Tek görev", "stdin": "1\n5 tek", "expectedOutput": "5: tek\ndeğiştirilemez"},
      {"label": "Aynı öncelik başlığa göre", "stdin": "2\n1 b\n1 a", "expectedOutput": "1: a\n1: b\ndeğiştirilemez"},
  ],
  hints=["@dataclass(order=True, frozen=True) yaz.", "Doğrulama __post_init__ içinde; frozen sınıfta bile alan atamadan yalnızca denetleyebilirsin."],
  explanation="order=True alanların sırasıyla karşılaştırma üretir, frozen=True alan atamayı yasaklar. __post_init__ nesne kurulurken doğrulama yapar.")

q(type="code", topic="slots", sectionId="slots", difficulty=2,
  prompt="Particle sınıfına __slots__ ekle (x, y, vx, vy) ve move() metodunu yaz: x vx kadar, y vy kadar artsın. Program başlangıç konumunu, hızı ve adım sayısını okur, parçacığı hareket ettirir ve olmayan bir öznitelik atamanın hata verdiğini gösterir.",
  starterCode=r'''
class Particle:
    # __slots__ ekle

    def __init__(self, x, y, vx, vy):
        self.x, self.y, self.vx, self.vy = x, y, vx, vy

    def move(self):
        # x ve y'yi hız kadar artır
        pass

x, y, vx, vy, steps = (int(input()) for _ in range(5))
particle = Particle(x, y, vx, vy)
for _ in range(steps):
    particle.move()
print(particle.x, particle.y)
try:
    particle.z = 1
except AttributeError:
    print("yeni öznitelik eklenemez")
''',
  answer=r'''
class Particle:
    __slots__ = ("x", "y", "vx", "vy")

    def __init__(self, x, y, vx, vy):
        self.x, self.y, self.vx, self.vy = x, y, vx, vy

    def move(self):
        self.x += self.vx
        self.y += self.vy

x, y, vx, vy, steps = (int(input()) for _ in range(5))
particle = Particle(x, y, vx, vy)
for _ in range(steps):
    particle.move()
print(particle.x, particle.y)
try:
    particle.z = 1
except AttributeError:
    print("yeni öznitelik eklenemez")
''',
  exampleInput="0\n0\n1\n2\n3",
  expectedOutput="3 6\nyeni öznitelik eklenemez",
  tests=[
      {"label": "Üç adım", "stdin": "0\n0\n1\n2\n3", "expectedOutput": "3 6\nyeni öznitelik eklenemez"},
      {"label": "Negatif hız", "stdin": "5\n5\n-1\n0\n5", "expectedOutput": "0 5\nyeni öznitelik eklenemez"},
      {"label": "Hiç adım yok", "stdin": "2\n3\n9\n9\n0", "expectedOutput": "2 3\nyeni öznitelik eklenemez"},
      {"label": "Çok adım", "stdin": "1\n1\n2\n-3\n10", "expectedOutput": "21 -29\nyeni öznitelik eklenemez"},
  ],
  hints=["__slots__ bir demet olmalı: dört adı yaz.", "move içinde self.x += self.vx ve self.y += self.vy kullan."],
  explanation="__slots__ nesnenin taşıyabileceği öznitelikleri sabitler; tanımsız bir adı atamak AttributeError verir ve yazım hatalarını erkenden yakalar.")

q(type="code", topic="descriptor", sectionId="descriptor-metaclass", difficulty=3,
  prompt="Bounded(alt, üst) adında bir descriptor yaz: __set_name__ ile alan adını ve saklama adını (_ad) öğrensin, __get__ değeri nesneden okusun, __set__ değer [alt, üst] aralığı dışındaysa ValueError(f'{ad} {alt} ile {üst} arasında olmalı') fırlatsın. Player sınıfı bunu iki alanda kullanıyor.",
  starterCode=r'''
class Bounded:
    pass

class Player:
    health = Bounded(0, 100)
    level = Bounded(1, 50)

    def __init__(self, health, level):
        self.health = health
        self.level = level

try:
    player = Player(int(input()), int(input()))
    print(player.health, player.level)
except ValueError as error:
    print("hata:", error)
''',
  answer=r'''
class Bounded:
    def __init__(self, low, high):
        self.low, self.high = low, high

    def __set_name__(self, owner, name):
        self.name = name
        self.storage = "_" + name

    def __get__(self, obj, owner=None):
        if obj is None:
            return self
        return getattr(obj, self.storage)

    def __set__(self, obj, value):
        if not self.low <= value <= self.high:
            raise ValueError(f"{self.name} {self.low} ile {self.high} arasında olmalı")
        setattr(obj, self.storage, value)

class Player:
    health = Bounded(0, 100)
    level = Bounded(1, 50)

    def __init__(self, health, level):
        self.health = health
        self.level = level

try:
    player = Player(int(input()), int(input()))
    print(player.health, player.level)
except ValueError as error:
    print("hata:", error)
''',
  exampleInput="80\n5",
  expectedOutput="80 5",
  tests=[
      {"label": "Geçerli", "stdin": "80\n5", "expectedOutput": "80 5"},
      {"label": "Can aralık dışı", "stdin": "120\n5", "expectedOutput": "hata: health 0 ile 100 arasında olmalı"},
      {"label": "Seviye aralık dışı", "stdin": "50\n0", "expectedOutput": "hata: level 1 ile 50 arasında olmalı"},
      {"label": "Sınır değerler", "stdin": "0\n50", "expectedOutput": "0 50"},
  ],
  hints=["Nesneye özel değeri descriptor'de değil, nesnede (_health gibi) sakla.", "Alan adını __set_name__ içinde öğren; mesajda ve saklama adında kullan."],
  explanation="Aynı Bounded sınıfı iki alanda farklı sınırlarla kullanıldı. Değer descriptor'ün içinde değil nesnenin _health ve _level özniteliklerinde saklandığı için nesneler birbirinden bağımsızdır.")

# ------------------------------------------------------------------ traceback (4)
q(type="traceback", topic="abstractmethod", sectionId="abc", difficulty=1,
  prompt="Soyut metodu olan bir sınıf doğrudan kuruluyor. Hangi hata oluşur?",
  code=r'''
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        ...

shape = Shape()
''',
  expectedError="TypeError",
  options=["TypeError", "NotImplementedError", "AttributeError", "ValueError"],
  optionFeedback={
      "NotImplementedError": "abc, metot gövdesinin içinde hata fırlatmaz; nesne kurulmadan önce TypeError ile engeller.",
      "AttributeError": "Hiçbir öznitelik aranmıyor; hata nesne kurulurken çıkıyor.",
      "ValueError": "Argüman değeri geçersiz değil; sınıfın kendisi soyut.",
  },
  hints=["Hata hangi satırda, nesne kurulurken mi, metot çağrılırken mi?", "Soyut sınıftan nesne üretmek hangi hatayı verir?"],
  explanation="Soyut metodu olan sınıf örneklenemez: Can't instantiate abstract class Shape ... TypeError ile bildirilir.")

q(type="traceback", topic="slots", sectionId="slots", difficulty=2,
  prompt="Slotlu bir nesneye tanımsız öznitelik atanıyor. Hangi hata oluşur?",
  code=r'''
class Point:
    __slots__ = ("x", "y")

    def __init__(self, x, y):
        self.x, self.y = x, y

p = Point(1, 2)
p.z = 3
''',
  expectedError="AttributeError",
  options=["AttributeError", "TypeError", "KeyError", "NameError"],
  optionFeedback={
      "TypeError": "Atama biçimi geçerli; sorun, z adında bir slot olmaması.",
      "KeyError": "Sözlük araması yok; nesnenin __dict__'i bile yok.",
      "NameError": "p tanımlı; hata, nesne üzerindeki öznitelik atamasından geliyor.",
  },
  hints=["Point'in __dict__'i var mı?", "z, __slots__ listesinde mi?"],
  explanation="__slots__ yalnızca x ve y için yer ayırır, nesnenin __dict__'i yoktur. z için slot bulunmadığından atama AttributeError verir.")

q(type="traceback", topic="frozen", sectionId="dataclass", difficulty=2,
  prompt="Dondurulmuş bir dataclass'ın alanına atama yapılıyor. Hangi hata oluşur?",
  code=r'''
from dataclasses import dataclass

@dataclass(frozen=True)
class Point:
    x: int
    y: int

p = Point(1, 2)
p.x = 5
''',
  expectedError="FrozenInstanceError",
  options=["FrozenInstanceError", "AttributeError", "TypeError", "ValueError"],
  optionFeedback={
      "AttributeError": "FrozenInstanceError, AttributeError'ın alt sınıfıdır; ama tracebackte görünen ve doğru olan özel ad FrozenInstanceError'dır.",
      "TypeError": "Atama türü ile ilgili bir sorun yok; alan donmuş.",
      "ValueError": "Değer geçerli; yasak olan atamanın kendisi.",
  },
  hints=["frozen=True neyi yasaklar?", "dataclasses modülünün özel bir hata sınıfı var."],
  explanation="frozen=True alan atamasını engeller ve dataclasses.FrozenInstanceError fırlatır (AttributeError'ın alt sınıfı). Değiştirilmiş kopya için dataclasses.replace kullanılır.")

q(type="traceback", topic="mro", sectionId="mro", difficulty=3,
  prompt="Sınıf başlığındaki sıra MRO ile çelişiyor. Hangi hata oluşur?",
  code=r'''
class A:
    pass

class B(A):
    pass

class Bad(A, B):
    pass
''',
  expectedError="TypeError",
  options=["TypeError", "NameError", "RecursionError", "AttributeError"],
  optionFeedback={
      "NameError": "A ve B tanımlı; hata sınıf başlığındaki sıradan geliyor.",
      "RecursionError": "Sonsuz özyineleme yok; MRO hesaplanırken tutarsızlık bulunuyor.",
      "AttributeError": "Hiçbir öznitelik aranmıyor; sorun sınıfın tanımında.",
  },
  hints=["Bad(A, B) A'nın B'den önce gelmesini istiyor.", "Ama B zaten A'dan türüyor; MRO'da B, A'dan önce gelmek zorunda."],
  explanation="Bad(A, B) hem A'nın B'den önce gelmesini hem de B'nin A'nın alt sınıfı olduğu için A'dan önce gelmesini ister. Tutarlı bir MRO kurulamaz: TypeError: Cannot create a consistent method resolution order.")
