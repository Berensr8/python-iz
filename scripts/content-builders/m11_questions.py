"""M11 (OOP 1) questions. Imported by build_m11.py.

Order: 12 output, 6 bug, 4 fill, 4 order, 10 code, 4 traceback (ids m11-q01 ... m11-q40).
"""

from _qhelper import make_questions

questions, q = make_questions("m11")


# ------------------------------------------------------------------ output (12)
q(type="output", topic="class-nesne", sectionId="class-object", difficulty=1,
  prompt="İki nesneden birinin özniteliği değiştiriliyor. Çıktı ne olur?",
  code=r'''
class Box:
    def __init__(self, label):
        self.label = label

a = Box("x")
b = Box("y")
a.label = "z"
print(a.label, b.label)
''',
  expectedOutput="z y",
  options=["z y", "z z", "x y", "y y"],
  hints=["Her nesnenin kendi label özniteliği vardır.", "a.label ataması yalnızca a'yı değiştirir."],
  explanation="a ve b aynı sınıftan üretilmiş iki ayrı nesnedir. a.label = 'z' yalnızca a'nın verisini değiştirir; b'nin label'ı 'y' kalır.")

q(type="output", topic="self", sectionId="class-object", difficulty=2,
  prompt="Metot nesne üzerinden ve sınıf üzerinden çağrılıyor. Karşılaştırma ne verir?",
  code=r'''
class Greeter:
    def hello(self, name):
        return f"Merhaba {name}"

g = Greeter()
print(g.hello("Ada") == Greeter.hello(g, "Ada"))
''',
  expectedOutput="True",
  options=["True", "False", "TypeError verir", "None"],
  hints=["g.hello('Ada') çağrısında g, metoda otomatik geçer.", "Greeter.hello(g, 'Ada') bunu elle yapar."],
  explanation="Nesne üzerinden çağrıda Python nesneyi self olarak ilk argümana kendisi koyar; ikinci çağrı aynı şeyi elle yapar. İki çağrı da aynı metni döndürür.")

q(type="output", topic="referans", sectionId="class-object", difficulty=3,
  prompt="Sınıf listesine kayıt ve iki ad aynı nesneye bağlı. Çıktı ne olur?",
  code=r'''
class Node:
    created = []

    def __init__(self, value):
        self.value = value
        Node.created.append(value)

n1 = Node(1)
n2 = Node(2)
n3 = n2
n3.value = 9
print(Node.created, n2.value, n1 is n3)
''',
  expectedOutput="[1, 2] 9 False",
  options=["[1, 2] 9 False", "[1, 2, 9] 9 False", "[1, 2] 2 False", "[1, 2] 9 True"],
  hints=["__init__ yalnızca nesne yaratılırken çalışır; kaç kez?", "n3 = n2 yeni bir nesne üretmez."],
  explanation="Yalnızca iki Node yaratıldığı için created [1, 2]'dir; n3.value = 9 atamasından sonra __init__ yeniden çalışmaz. n3 ve n2 aynı nesnedir, bu yüzden n2.value 9 olur; n1 ise ayrı bir nesnedir.")

q(type="output", topic="str-repr", sectionId="methods-state", difficulty=2,
  prompt="__str__ ve __repr__ birlikte tanımlı. Üç satırın çıktısı nedir?",
  code=r'''
class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __repr__(self):
        return f"Point({self.x}, {self.y})"

    def __str__(self):
        return f"({self.x}, {self.y})"

p = Point(1, 2)
print(p)
print([p])
print(f"{p!r}")
''',
  expectedOutput="(1, 2)\n[Point(1, 2)]\nPoint(1, 2)",
  options=[
      "(1, 2) / [Point(1, 2)] / Point(1, 2)",
      "Point(1, 2) / [Point(1, 2)] / Point(1, 2)",
      "(1, 2) / [(1, 2)] / (1, 2)",
      "(1, 2) / [Point(1, 2)] / (1, 2)",
  ],
  hints=["print(nesne) __str__'i kullanır.", "Listenin içindeki öğeler repr ile gösterilir; !r de repr ister."],
  explanation="print(p) __str__'i çağırır. Liste öğelerini repr ile gösterir ve f-string'deki !r de repr'i seçer; ikisi de Point(1, 2) verir.")

q(type="output", topic="komut-metot", sectionId="methods-state", difficulty=1,
  prompt="add durumu değiştiren bir metot. result neyi tutar?",
  code=r'''
class Buffer:
    def __init__(self):
        self.parts = []

    def add(self, text):
        self.parts.append(text)

result = Buffer().add("a")
print(result)
''',
  expectedOutput="None",
  options=["None", "['a']", "a", "Bir Buffer nesnesi"],
  hints=["add bir return ifadesi içeriyor mu?", "return yoksa metot None döndürür."],
  explanation="add listeye ekleme yapar ama bir şey döndürmez; Python return olmayan her fonksiyondan None verir. Zincirleme çağrı istiyorsan metodun sonuna return self yazmalısın.")

q(type="output", topic="class-degiskeni", sectionId="instance-class-vars", difficulty=1,
  prompt="Sınıf değişkeni sınıf üzerinden değiştiriliyor. Çıktı ne olur?",
  code=r'''
class Shop:
    tax = 0.2

a = Shop()
b = Shop()
Shop.tax = 0.1
print(a.tax, b.tax)
''',
  expectedOutput="0.1 0.1",
  options=["0.1 0.1", "0.2 0.2", "0.1 0.2", "AttributeError verir"],
  hints=["a ve b'nin kendi tax özniteliği var mı?", "Yoksa Python sınıfa bakar."],
  explanation="a ve b'nin kendi tax özniteliği yoktur; okunurken sınıftaki değer bulunur. Shop.tax değişince ikisi de yeni değeri görür.")

q(type="output", topic="golgeleme", sectionId="instance-class-vars", difficulty=2,
  prompt="Bir nesne üzerinden atama yapılıyor, sonra sınıf değişiyor. Çıktı ne olur?",
  code=r'''
class Shop:
    tax = 0.2

a = Shop()
b = Shop()
a.tax = 0.5
Shop.tax = 0.1
print(a.tax, b.tax, Shop.tax)
''',
  expectedOutput="0.5 0.1 0.1",
  options=["0.5 0.1 0.1", "0.5 0.5 0.1", "0.1 0.1 0.1", "0.5 0.1 0.2"],
  hints=["a.tax = 0.5 sınıfı mı değiştirir, a'ya yeni bir öznitelik mi ekler?", "Okuma sırası: önce nesne, sonra sınıf."],
  explanation="a.tax = 0.5 yalnızca a'da kendi tax özniteliğini oluşturur ve sınıftakini gölgeler. Sonradan Shop.tax değişince b yeni değeri görür; a ise kendi 0.5'ini kullanmaya devam eder.")

q(type="output", topic="sayac", sectionId="instance-class-vars", difficulty=3,
  prompt="self.count += 1 ile sayaç artırılıyor. Çıktı ne olur?",
  code=r'''
class Visitor:
    count = 0

    def visit(self):
        self.count += 1

a, b = Visitor(), Visitor()
a.visit()
a.visit()
b.visit()
print(a.count, b.count, Visitor.count)
''',
  expectedOutput="2 1 0",
  options=["2 1 0", "2 1 3", "3 3 3", "0 0 3"],
  hints=["self.count += 1, self.count = self.count + 1 demektir.", "Atama nesnede mi, sınıfta mı yapılır?"],
  explanation="Sağ taraf sınıftaki (ya da nesnedeki) değeri okur, sol taraf ise nesnede yeni bir count oluşturur. Bu yüzden her nesne kendi sayacını tutar: a 2, b 1; sınıfın count'u hiç değişmez ve 0 kalır. Ortak sayaç için Visitor.count += 1 yazılır.")

q(type="output", topic="override", sectionId="inheritance-super", difficulty=2,
  prompt="Üç sınıflı kalıtım zincirinde hello çağrılıyor. Çıktı ne olur?",
  code=r'''
class A:
    def hello(self):
        return "A"

class B(A):
    def hello(self):
        return "B" + super().hello()

class C(B):
    pass

print(C().hello())
''',
  expectedOutput="BA",
  options=["BA", "B", "AB", "A"],
  hints=["C hello'yu kendi içinde tanımlamıyor; kimden devralıyor?", "B.hello, super().hello() ile A'nın sürümünü çağırır."],
  explanation="C'de hello yok, bu yüzden B'dekini devralır. B.hello önce 'B' yazar, ardından super() ile A.hello'dan 'A' alır ve birleştirir: BA.")

q(type="output", topic="super-sirasi", sectionId="inheritance-super", difficulty=3,
  prompt="Üst sınıfın __init__'i alt sınıfın geçersiz kıldığı bir metodu çağırıyor. Çıktı ne olur?",
  code=r'''
class Base:
    def __init__(self):
        print("Base")
        self.setup()

    def setup(self):
        print("Base.setup")

class Child(Base):
    def __init__(self):
        print("Child önce")
        super().__init__()
        print("Child sonra")

    def setup(self):
        print("Child.setup")

Child()
''',
  expectedOutput="Child önce\nBase\nChild.setup\nChild sonra",
  options=[
      "Child önce / Base / Child.setup / Child sonra",
      "Child önce / Base / Base.setup / Child sonra",
      "Base / Base.setup / Child önce / Child sonra",
      "Base / Child önce / Child.setup / Child sonra",
  ],
  hints=["Child() önce Child.__init__'i çalıştırır.", "self.setup() çağrısında self bir Child nesnesidir."],
  explanation="Child.__init__ 'Child önce' yazar, super().__init__() ile Base.__init__'e geçer ve 'Base' yazar. Orada self.setup() çağrılır; self bir Child olduğundan Child.setup çalışır. Sonra kontrol Child.__init__'e döner ve 'Child sonra' yazılır.")

q(type="output", topic="name-mangling", sectionId="encapsulation", difficulty=2,
  prompt="Çift alt çizgili öznitelik sınıfın dışından aranıyor. Çıktı ne olur?",
  code=r'''
class Vault:
    def __init__(self):
        self.__code = 1234

v = Vault()
print(hasattr(v, "__code"), v._Vault__code)
''',
  expectedOutput="False 1234",
  options=["False 1234", "True 1234", "AttributeError verir", "False None"],
  hints=["Sınıf içinde __code adı yeniden adlandırılır.", "Yeni ad _SınıfAdı__ad biçimindedir."],
  explanation="__code sınıf içinde _Vault__code olarak saklanır; '__code' adıyla aranınca bulunamaz (False) ama gerçek adıyla yine okunabilir. Ad bozma bir güvenlik değil, ad çakışması önlemidir.")

q(type="output", topic="property", sectionId="property", difficulty=2,
  prompt="area bir property. w değişince area ne gösterir?",
  code=r'''
class Rect:
    def __init__(self, w, h):
        self.w, self.h = w, h

    @property
    def area(self):
        return self.w * self.h

r = Rect(2, 3)
before = r.area
r.w = 10
print(before, r.area)
''',
  expectedOutput="6 30",
  options=["6 30", "6 6", "30 30", "AttributeError verir"],
  hints=["Property her okunuşta metodu yeniden çalıştırır.", "before, ilk okumanın sonucunu saklar."],
  explanation="area saklanan bir değer değil, her okunuşta hesaplanan bir sonuçtur. İlk okuma 2 x 3 = 6 verdi ve before'a bağlandı; w 10 olunca ikinci okuma 10 x 3 = 30 hesapladı.")

# ------------------------------------------------------------------ bug (6)
q(type="bug", topic="self", sectionId="class-object", difficulty=1,
  prompt="Bu kod neden TypeError verir?",
  code=r'''
class Lamp:
    def __init__(self):
        self.on = False

    def toggle():
        self.on = not self.on

lamp = Lamp()
lamp.toggle()
''',
  answer="toggle self parametresini almıyor; nesne ilk argüman olarak geçiliyor",
  options=[
      "toggle self parametresini almıyor; nesne ilk argüman olarak geçiliyor",
      "__init__ içinde on özniteliği tanımlanamaz",
      "toggle çağrısında parantez kullanılamaz",
      "self yerine this yazılmalı",
  ],
  optionFeedback={
      "__init__ içinde on özniteliği tanımlanamaz": "__init__ özniteliklerin tam olarak kurulduğu yerdir.",
      "toggle çağrısında parantez kullanılamaz": "Metot çağrısı parantezlidir; sorun tanımdadır.",
      "self yerine this yazılmalı": "Python'da this yoktur; ilk parametre geleneksel olarak self adını taşır.",
  },
  hints=["lamp.toggle() çağrısında Python metoda ne geçer?", "Tanımda hangi parametre eksik?"],
  explanation="lamp.toggle() çağrısı nesneyi ilk argüman olarak geçer ama def toggle(): hiç parametre almaz; Python 'takes 0 positional arguments but 1 was given' hatası verir. Doğrusu def toggle(self): olmalıdır.")

q(type="bug", topic="class-degiskeni", sectionId="instance-class-vars", difficulty=2,
  prompt="a'ya eklenen ürün neden b'de de görünüyor?",
  code=r'''
class Cart:
    items = []

    def add(self, name):
        self.items.append(name)

a = Cart()
b = Cart()
a.add("elma")
print(b.items)
''',
  answer="items bir class değişkeni; liste bütün nesnelerce paylaşılıyor, __init__ içinde self.items = [] kurulmalı",
  options=[
      "items bir class değişkeni; liste bütün nesnelerce paylaşılıyor, __init__ içinde self.items = [] kurulmalı",
      "Python aynı sınıftan üretilen nesneleri birbirine bağlar",
      "append bir listeyi tüm sınıflara kopyalar",
      "b.items yazımı a'nın özniteliğini okur",
  ],
  optionFeedback={
      "Python aynı sınıftan üretilen nesneleri birbirine bağlar": "Nesneler bağımsızdır; paylaşılan şey sınıftaki tek liste.",
      "append bir listeyi tüm sınıflara kopyalar": "append hiçbir kopya üretmez; listeyi yerinde büyütür.",
      "b.items yazımı a'nın özniteliğini okur": "b.items, b'de yoksa sınıfa bakar; a'ya hiç bakmaz.",
  },
  hints=["items nerede tanımlanmış: metodun içinde mi, sınıf gövdesinde mi?", "Tek bir liste nesnesi var mı, iki mi?"],
  explanation="items sınıf gövdesinde tanımlandığı için a ve b'nin ikisi de aynı listeyi görür; self.items.append bu tek listeyi büyütür. Nesneye özel liste __init__ içinde self.items = [] ile kurulmalıdır.")

q(type="bug", topic="super", sectionId="inheritance-super", difficulty=2,
  prompt="Bu kod neden AttributeError verir?",
  code=r'''
class Animal:
    def __init__(self, name):
        self.name = name

class Dog(Animal):
    def __init__(self, name, breed):
        self.breed = breed

dog = Dog("Pamuk", "Golden")
print(dog.name)
''',
  answer="Dog.__init__ üst sınıfın __init__'ini çağırmıyor; name hiç kurulmuyor",
  options=[
      "Dog.__init__ üst sınıfın __init__'ini çağırmıyor; name hiç kurulmuyor",
      "Dog, Animal'ın metotlarını devralamaz",
      "breed özniteliği name'i siler",
      "name üst sınıfta gizli olduğu için erişilemez",
  ],
  optionFeedback={
      "Dog, Animal'ın metotlarını devralamaz": "Devralma çalışır; sorun __init__'in geçersiz kılınmış olması.",
      "breed özniteliği name'i siler": "Bir öznitelik atamak ötekini silmez.",
      "name üst sınıfta gizli olduğu için erişilemez": "name herkese açık bir özniteliktir; sadece hiç atanmadı.",
  },
  hints=["Dog kendi __init__'ini yazınca Animal.__init__ otomatik çalışır mı?", "name özniteliğini kim kuruyor?"],
  explanation="Alt sınıf kendi __init__'ini tanımlayınca üst sınıfınki çalışmaz. super().__init__(name) çağrılmadığı için self.name hiç atanmaz ve okunurken AttributeError alınır.")

q(type="bug", topic="kapsulleme", sectionId="encapsulation", difficulty=2,
  prompt="Takım kuralı (aynı ad iki kez olmaz) neden bozulabiliyor?",
  code=r'''
class Team:
    def __init__(self):
        self._members = []

    def add(self, name):
        if name not in self._members:
            self._members.append(name)

    def members(self):
        return self._members

team = Team()
team.add("Ada")
team.members().append("Ada")
print(team.members())
''',
  answer="members() iç listenin kendisini döndürüyor; dışarıdan değiştirilebiliyor, kopya döndürülmeli",
  options=[
      "members() iç listenin kendisini döndürüyor; dışarıdan değiştirilebiliyor, kopya döndürülmeli",
      "_members adı Python tarafından gizlenir ve değiştirilemez",
      "add metodu aynı adı her zaman iki kez ekler",
      "name not in kontrolü listelerde çalışmaz",
  ],
  optionFeedback={
      "_members adı Python tarafından gizlenir ve değiştirilemez": "Tek alt çizgi yalnızca bir gelenektir; Python erişimi engellemez.",
      "add metodu aynı adı her zaman iki kez ekler": "add kuralı doğru uygular; bozulma add'e hiç uğramayan bir yoldan geliyor.",
      "name not in kontrolü listelerde çalışmaz": "in ve not in listelerde sorunsuz çalışır.",
  },
  hints=["team.members() tam olarak neyi döndürüyor?", "append hangi kurallı metottan geçiyor?"],
  explanation="members() iç listeyi olduğu gibi verdiği için çağıran taraf append ile add'in kuralını atlayabilir. list(self._members) ya da tuple(self._members) döndürmek iç durumu korur.")

q(type="bug", topic="property", sectionId="property", difficulty=3,
  prompt="Product(10) neden RecursionError verir?",
  code=r'''
class Product:
    def __init__(self, price):
        self.price = price

    @property
    def price(self):
        return self.price

    @price.setter
    def price(self, value):
        if value < 0:
            raise ValueError("fiyat negatif olamaz")
        self.price = value

Product(10)
''',
  answer="property kendi adını okuyup yazıyor; veri _price gibi ayrı bir özniteliğe saklanmalı",
  options=[
      "property kendi adını okuyup yazıyor; veri _price gibi ayrı bir özniteliğe saklanmalı",
      "@property ile setter aynı sınıfta kullanılamaz",
      "value < 0 koşulu tanımsızdır",
      "__init__ property'den önce tanımlanmalıdır",
  ],
  optionFeedback={
      "@property ile setter aynı sınıfta kullanılamaz": "@property ve @ad.setter birlikte yazılır.",
      "value < 0 koşulu tanımsızdır": "Koşul geçerli; sorun setter'ın içinde self.price'a tekrar atama yapılması.",
      "__init__ property'den önce tanımlanmalıdır": "Tanım sırası bu hatayla ilgili değildir.",
  },
  hints=["return self.price yazınca hangi property çalışır?", "setter içinde self.price = value yazınca ne olur?"],
  explanation="Getter'ın içindeki self.price yeniden aynı getter'ı, setter'ın içindeki self.price = value yeniden aynı setter'ı çağırır; bu sonsuz özyinelemedir. Gerçek değer self._price gibi farklı bir adda saklanmalıdır.")

q(type="bug", topic="staticmethod", sectionId="static-class-methods", difficulty=2,
  prompt="Temp.describe(20) neden çalışmaz?",
  code=r'''
class Temp:
    unit = "C"

    @staticmethod
    def describe(value):
        return f"{value}{self.unit}"

print(Temp.describe(20))
''',
  answer="staticmethod self almaz; sınıf değişkenine erişmek için classmethod ve cls gerekir",
  options=[
      "staticmethod self almaz; sınıf değişkenine erişmek için classmethod ve cls gerekir",
      "unit bir sınıf değişkeni olamaz",
      "staticmethod içinde f-string kullanılamaz",
      "describe yalnızca bir nesne üzerinden çağrılabilir",
  ],
  optionFeedback={
      "unit bir sınıf değişkeni olamaz": "Sınıf gövdesinde tanımlanan adlar sınıf değişkenidir ve geçerlidir.",
      "staticmethod içinde f-string kullanılamaz": "Statik metotlar her tür ifadeyi kullanabilir.",
      "describe yalnızca bir nesne üzerinden çağrılabilir": "Statik ve sınıf metotları sınıf üzerinden de çağrılabilir; sorun self adının tanımsız olması.",
  },
  hints=["describe'ın parametreleri arasında self var mı?", "Sınıf değişkenine erişmenin yolu hangi metot türüdür?"],
  explanation="@staticmethod hiçbir otomatik parametre geçirmez, bu yüzden self tanımsızdır (NameError). Sınıf değişkenine erişmek istiyorsan @classmethod yazıp cls.unit kullan.")

# ------------------------------------------------------------------ fill (4)
q(type="fill", topic="self", sectionId="class-object", difficulty=1,
  prompt="Nesnenin name özniteliğini kuran satırdaki boşluğu tamamla.",
  code=r'''
class Dog:
    def __init__(self, name):
        ___.name = name

print(Dog("Pamuk").name)
''',
  answer="self",
  expectedOutput="Pamuk",
  hints=["Öznitelik, metodun çalıştığı nesneye bağlanır.", "Metodun ilk parametresi bu nesnedir."],
  explanation="self.name = name, name değerini o an kurulan nesnenin özniteliğine bağlar.")

q(type="fill", topic="super", sectionId="inheritance-super", difficulty=2,
  prompt="Alt sınıf, üst sınıfın __init__'ini çağıracak. Boşluğu tamamla.",
  code=r'''
class Animal:
    def __init__(self, name):
        self.name = name

class Dog(Animal):
    def __init__(self, name, breed):
        ___().__init__(name)
        self.breed = breed

dog = Dog("Pamuk", "Golden")
print(dog.name, dog.breed)
''',
  answer="super",
  expectedOutput="Pamuk Golden",
  hints=["Üst sınıfa doğrudan adını yazmadan erişen yerleşik işlev hangisi?", "Parantezle çağrılır."],
  explanation="super() üst sınıfın metotlarına erişir; super().__init__(name) Animal'ın kurulum kodunu çalıştırıp name'i atar.")

q(type="fill", topic="property", sectionId="property", difficulty=1,
  prompt="area, parantezsiz öznitelik gibi okunsun. Decorator'ı tamamla.",
  code=r'''
class Square:
    def __init__(self, side):
        self.side = side

    @___
    def area(self):
        return self.side ** 2

print(Square(4).area)
''',
  answer="property",
  expectedOutput="16",
  hints=["Metodu öznitelik gibi okutan yerleşik decorator.", "Adı, özelliğin İngilizcesidir."],
  explanation="@property, area'yı parantezsiz okunan bir öznitelik yapar: Square(4).area metodu çalıştırıp 16 verir.")

q(type="fill", topic="classmethod", sectionId="static-class-methods", difficulty=2,
  prompt="Metot sınıfı (cls) alıp nesne kuruyor. Decorator'ı tamamla.",
  code=r'''
class Pizza:
    def __init__(self, toppings):
        self.toppings = toppings

    @___
    def margherita(cls):
        return cls(["peynir", "domates"])

print(Pizza.margherita().toppings)
''',
  answer="classmethod",
  expectedOutput="['peynir', 'domates']",
  hints=["İlk parametre self değil cls.", "Sınıfa bağlı metot decorator'ı."],
  explanation="@classmethod ilk parametre olarak sınıfı geçirir; margherita cls(...) ile Pizza nesnesi kurar ve alt sınıftan çağrılırsa o alt sınıfın nesnesini verir.")

# ------------------------------------------------------------------ order (4)
q(type="order", topic="class-nesne", sectionId="class-object", difficulty=1,
  prompt="Dog sınıfını tanımlayıp Pamuk'un konuşmasını yazdıracak sırayı kur.",
  answer_lines=[
      "class Dog:",
      "    def __init__(self, name):",
      "        self.name = name",
      "    def speak(self):",
      "        return self.name + ' havlıyor'",
      "print(Dog('Pamuk').speak())",
  ],
  perm=[5, 3, 1, 4, 0, 2],
  expectedOutput="Pamuk havlıyor",
  hints=["Sınıf başlığı önce gelir, gövde girintilidir.", "Nesne kullanılmadan önce sınıf tanımlanmalı."],
  explanation="class başlığı, ardından __init__ ve speak metotları yazılır; sınıf hazır olunca nesne oluşturulup metot çağrılır.")

q(type="order", topic="override", sectionId="inheritance-super", difficulty=2,
  prompt="Cat'in üst sınıftan farklı ses çıkardığı sırayı kur.",
  answer_lines=[
      "class Animal:",
      "    def sound(self):",
      "        return '...'",
      "class Cat(Animal):",
      "    def sound(self):",
      "        return 'miyav'",
      "print(Cat().sound())",
  ],
  perm=[4, 6, 0, 2, 5, 3, 1],
  expectedOutput="miyav",
  hints=["Üst sınıf, alt sınıftan önce tanımlanır.", "Alt sınıf aynı adlı metodu yeniden yazar."],
  explanation="Animal tanımlandıktan sonra Cat(Animal) onu genişletir ve sound'u geçersiz kılar; son satır Cat'in sürümünü çalıştırır.")

q(type="order", topic="classmethod", sectionId="static-class-methods", difficulty=2,
  prompt="Sınıf düzeyinde bilet numarası veren sayaç sırasını kur.",
  answer_lines=[
      "class Ticket:",
      "    issued = 0",
      "    @classmethod",
      "    def issue(cls):",
      "        cls.issued += 1",
      "        return cls.issued",
      "print(Ticket.issue(), Ticket.issue())",
  ],
  perm=[3, 6, 1, 5, 0, 2, 4],
  expectedOutput="1 2",
  hints=["Decorator, uyguladığı metodun hemen üstünde durur.", "Sayaç sınıf gövdesinde başlatılır."],
  explanation="issued sınıf değişkeni olarak başlar; @classmethod ile işaretlenen issue cls.issued'i artırıp döndürür. İki çağrı 1 ve 2 verir.")

q(type="order", topic="composition", sectionId="composition", difficulty=2,
  prompt="Car'ın işi Engine'e devrettiği sırayı kur.",
  answer_lines=[
      "class Engine:",
      "    def start(self):",
      "        return 'çalıştı'",
      "class Car:",
      "    def __init__(self, engine):",
      "        self.engine = engine",
      "    def start(self):",
      "        return self.engine.start()",
      "print(Car(Engine()).start())",
  ],
  perm=[7, 3, 8, 1, 5, 0, 4, 6, 2],
  expectedOutput="çalıştı",
  hints=["Car, Engine nesnesini __init__ parametresi olarak alır.", "Program nesneleri sınıflar tanımlandıktan sonra kurar."],
  explanation="Engine ve Car tanımlanır; Car engine'i saklar ve start çağrısını ona devreder. Son satır Engine'li bir Car kurup çalıştırır.")

# ------------------------------------------------------------------ code (10)
q(type="code", topic="class-nesne", sectionId="class-object", difficulty=1,
  prompt="Rectangle sınıfını tamamla: __init__ en ve boyu saklasın, area() alanı, perimeter() çevreyi döndürsün. Program iki satırdan en ve boyu okuyup 'alan çevre' yazdırır.",
  starterCode=r'''
class Rectangle:
    def __init__(self, width, height):
        # width ve height'ı nesneye kaydet
        pass

    def area(self):
        pass

    def perimeter(self):
        pass

width = int(input())
height = int(input())
rect = Rectangle(width, height)
print(rect.area(), rect.perimeter())
''',
  answer=r'''
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)

width = int(input())
height = int(input())
rect = Rectangle(width, height)
print(rect.area(), rect.perimeter())
''',
  exampleInput="3\n4",
  expectedOutput="12 14",
  tests=[
      {"label": "Normal", "stdin": "3\n4", "expectedOutput": "12 14"},
      {"label": "Kare", "stdin": "1\n1", "expectedOutput": "1 4"},
      {"label": "Sıfır kenar", "stdin": "0\n5", "expectedOutput": "0 10"},
      {"label": "Büyük", "stdin": "10\n2", "expectedOutput": "20 24"},
  ],
  hints=["Öznitelikleri self.width ve self.height olarak kaydet.", "Metotlar değeri return ile döndürmeli."],
  explanation="__init__ değerleri self'e bağlar; area ve perimeter bu özniteliklerden hesaplayıp döndürür.")

q(type="code", topic="metot-durum", sectionId="methods-state", difficulty=2,
  prompt="ShoppingCart sınıfını yaz: add(name, price) ürünü ekleyip self'i döndürsün; total() fiyatların toplamını versin; __str__ 'ad1, ad2 (toplam 55)' biçiminde (boşsa 'boş sepet (toplam 0)') metin döndürsün. Program ürün sayısını ve her satırda 'ad fiyat' okur, sepeti yazdırır; son satırda add'in self döndürdüğünü gösterir.",
  starterCode=r'''
class ShoppingCart:
    def __init__(self):
        self.items = []

    def add(self, name, price):
        # ürünü ekle ve zincirleme için self'i döndür
        pass

    def total(self):
        # fiyatların toplamı
        return 0

    def __str__(self):
        # 'ad1, ad2 (toplam 55)' ya da 'boş sepet (toplam 0)'
        return ""

cart = ShoppingCart()
for _ in range(int(input())):
    name, price = input().split()
    cart.add(name, int(price))
print(cart)
print(cart.add("kontrol", 0) is cart)
''',
  answer=r'''
class ShoppingCart:
    def __init__(self):
        self.items = []

    def add(self, name, price):
        self.items.append((name, price))
        return self

    def total(self):
        return sum(price for _, price in self.items)

    def __str__(self):
        if not self.items:
            return "boş sepet (toplam 0)"
        names = ", ".join(name for name, _ in self.items)
        return f"{names} (toplam {self.total()})"

cart = ShoppingCart()
for _ in range(int(input())):
    name, price = input().split()
    cart.add(name, int(price))
print(cart)
print(cart.add("kontrol", 0) is cart)
''',
  exampleInput="2\nEkmek 15\nSüt 40",
  expectedOutput="Ekmek, Süt (toplam 55)\nTrue",
  tests=[
      {"label": "İki ürün", "stdin": "2\nEkmek 15\nSüt 40", "expectedOutput": "Ekmek, Süt (toplam 55)\nTrue"},
      {"label": "Tek ürün", "stdin": "1\nSu 10", "expectedOutput": "Su (toplam 10)\nTrue"},
      {"label": "Boş sepet", "stdin": "0", "expectedOutput": "boş sepet (toplam 0)\nTrue"},
      {"label": "Aynı ürün iki kez", "stdin": "3\nA 1\nB 2\nA 3", "expectedOutput": "A, B, A (toplam 6)\nTrue"},
  ],
  hints=["items listesine (ad, fiyat) çiftleri ekleyebilirsin.", "add'in sonuna return self yaz; boş sepeti ayrı karşıla."],
  explanation="add çifti listeye ekleyip self döndürür; total fiyatları toplar; __str__ boş sepeti ayrı ele alır, değilse adları ', ' ile birleştirip toplamı ekler.")

q(type="code", topic="class-degiskeni", sectionId="instance-class-vars", difficulty=2,
  prompt="Ticket sınıfı, sınıf düzeyindeki issued sayacını her yeni biletle artırsın ve biletin numarasını (1'den başlayarak) number özniteliğine kaydetsin. Program bilet sahiplerinin adlarını okur, 'ad: numara' yazdırır ve son satırda 'toplam: sayı' gösterir.",
  starterCode=r'''
class Ticket:
    issued = 0

    def __init__(self, owner):
        self.owner = owner
        # sayacı sınıf üzerinden artır ve numarayı kaydet
        self.number = 0

count = int(input())
tickets = [Ticket(input()) for _ in range(count)]
for ticket in tickets:
    print(f"{ticket.owner}: {ticket.number}")
print(f"toplam: {Ticket.issued}")
''',
  answer=r'''
class Ticket:
    issued = 0

    def __init__(self, owner):
        self.owner = owner
        Ticket.issued += 1
        self.number = Ticket.issued

count = int(input())
tickets = [Ticket(input()) for _ in range(count)]
for ticket in tickets:
    print(f"{ticket.owner}: {ticket.number}")
print(f"toplam: {Ticket.issued}")
''',
  exampleInput="3\nAda\nCan\nEda",
  expectedOutput="Ada: 1\nCan: 2\nEda: 3\ntoplam: 3",
  tests=[
      {"label": "Üç bilet", "stdin": "3\nAda\nCan\nEda", "expectedOutput": "Ada: 1\nCan: 2\nEda: 3\ntoplam: 3"},
      {"label": "Tek bilet", "stdin": "1\nAda", "expectedOutput": "Ada: 1\ntoplam: 1"},
      {"label": "Hiç bilet", "stdin": "0", "expectedOutput": "toplam: 0"},
      {"label": "Aynı ad iki kez", "stdin": "2\nAda\nAda", "expectedOutput": "Ada: 1\nAda: 2\ntoplam: 2"},
  ],
  hints=["Ortak sayacı Ticket.issued ile artır; self.issued yazmak nesnede yeni bir öznitelik oluşturur.", "Sayaç artınca değerini number'a ata."],
  explanation="Ticket.issued += 1 sınıfın sayacını artırır; yeni değer biletin numarası olur. self.issued += 1 yazılsaydı her nesnede ayrı bir sayaç oluşur ve sınıfınki hep 0 kalırdı.")

q(type="code", topic="super", sectionId="inheritance-super", difficulty=2,
  prompt="Employee hazır. Manager(Employee) sınıfını yaz: __init__(name, salary, bonus) üst sınıfı super() ile kursun ve bonus'u saklasın; yearly() üst sınıfın yearly() sonucuna bonus'u eklesin. Program 'çalışan' ya da 'yönetici' ile ad ve maaşı okur (yönetici için bonus da gelir) ve 'ad: yıllık gelir' yazdırır.",
  starterCode=r'''
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def yearly(self):
        return self.salary * 12

class Manager(Employee):
    def __init__(self, name, salary, bonus):
        # üst sınıfı super() ile kur, bonus'u sakla
        pass

    def yearly(self):
        # üst sınıfın yearly() sonucuna bonus'u ekle
        return 0

kind = input()
name = input()
salary = int(input())
if kind == "yönetici":
    person = Manager(name, salary, int(input()))
else:
    person = Employee(name, salary)
print(f"{person.name}: {person.yearly()}")
''',
  answer=r'''
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def yearly(self):
        return self.salary * 12

class Manager(Employee):
    def __init__(self, name, salary, bonus):
        super().__init__(name, salary)
        self.bonus = bonus

    def yearly(self):
        return super().yearly() + self.bonus

kind = input()
name = input()
salary = int(input())
if kind == "yönetici":
    person = Manager(name, salary, int(input()))
else:
    person = Employee(name, salary)
print(f"{person.name}: {person.yearly()}")
''',
  exampleInput="yönetici\nCan\n1000\n5000",
  expectedOutput="Can: 17000",
  tests=[
      {"label": "Çalışan", "stdin": "çalışan\nAda\n1000", "expectedOutput": "Ada: 12000"},
      {"label": "Yönetici", "stdin": "yönetici\nCan\n1000\n5000", "expectedOutput": "Can: 17000"},
      {"label": "Maaşsız yönetici", "stdin": "yönetici\nEda\n0\n20000", "expectedOutput": "Eda: 20000"},
      {"label": "Maaşsız çalışan", "stdin": "çalışan\nBo\n0", "expectedOutput": "Bo: 0"},
  ],
  hints=["super().__init__(name, salary) üst sınıfın kurulumunu yapar.", "Yıllık geliri yeniden hesaplama; super().yearly() kullan."],
  explanation="Manager name ve salary'yi üst sınıfa devreder, yalnızca bonus'u kendisi saklar; yearly de üst sınıfın sonucunu yeniden kullanıp bonus'u ekler.")

q(type="code", topic="kapsulleme", sectionId="encapsulation", difficulty=2,
  prompt="Wallet sınıfını yaz. Bakiye _balance özniteliğinde dursun. deposit(amount) ve spend(amount) önce tutarın pozitif olduğunu denetlesin (değilse ValueError('tutar pozitif olmalı')); spend ayrıca bakiyeden büyük tutarı ValueError('yetersiz bakiye') ile reddetsin. balance() bakiyeyi döndürsün. Program 'yatır N' ve 'harca N' komutlarını işler, hataları 'hata: ...' diye yazar ve sonda 'bakiye: X' gösterir.",
  starterCode=r'''
class Wallet:
    def __init__(self):
        self._balance = 0

    def deposit(self, amount):
        pass

    def spend(self, amount):
        pass

    def balance(self):
        pass

wallet = Wallet()
for _ in range(int(input())):
    command, amount = input().split()
    try:
        if command == "yatır":
            wallet.deposit(int(amount))
        else:
            wallet.spend(int(amount))
    except ValueError as error:
        print("hata:", error)
print("bakiye:", wallet.balance())
''',
  answer=r'''
class Wallet:
    def __init__(self):
        self._balance = 0

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("tutar pozitif olmalı")
        self._balance += amount

    def spend(self, amount):
        if amount <= 0:
            raise ValueError("tutar pozitif olmalı")
        if amount > self._balance:
            raise ValueError("yetersiz bakiye")
        self._balance -= amount

    def balance(self):
        return self._balance

wallet = Wallet()
for _ in range(int(input())):
    command, amount = input().split()
    try:
        if command == "yatır":
            wallet.deposit(int(amount))
        else:
            wallet.spend(int(amount))
    except ValueError as error:
        print("hata:", error)
print("bakiye:", wallet.balance())
''',
  exampleInput="3\nyatır 100\nharca 30\nharca 500",
  expectedOutput="hata: yetersiz bakiye\nbakiye: 70",
  tests=[
      {"label": "Yetersiz bakiye", "stdin": "3\nyatır 100\nharca 30\nharca 500", "expectedOutput": "hata: yetersiz bakiye\nbakiye: 70"},
      {"label": "Geçersiz tutarlar", "stdin": "2\nyatır -5\nharca 0", "expectedOutput": "hata: tutar pozitif olmalı\nhata: tutar pozitif olmalı\nbakiye: 0"},
      {"label": "Komut yok", "stdin": "0", "expectedOutput": "bakiye: 0"},
      {"label": "Tam bakiyeyi harca", "stdin": "2\nyatır 40\nharca 40", "expectedOutput": "bakiye: 0"},
      {"label": "Boş cüzdandan harca", "stdin": "1\nharca 10", "expectedOutput": "hata: yetersiz bakiye\nbakiye: 0"},
  ],
  hints=["Tutar denetimi her iki metotta da ilk adımdır.", "Hata durumunda bakiyeyi değiştirme; önce denetle, sonra güncelle."],
  explanation="Her metot önce kuralları denetleyip ValueError fırlatır; durum yalnızca geçerli istekte güncellenir, bu yüzden bakiye hiçbir hata sonrası bozulmaz.")

q(type="code", topic="property", sectionId="property", difficulty=2,
  prompt="Temperature sınıfında celsius bir property olsun: setter -273.15'in altındaki değeri ValueError('mutlak sıfırın altında') ile reddetsin (kurulumda da denetlensin). fahrenheit saklanmayan, salt okunur bir property olsun (celsius * 9 / 5 + 32). Program bir ondalık sayı okur, fahrenheit'i bir ondalık basamakla yazar; hatada 'hata: ...' yazar.",
  starterCode=r'''
class Temperature:
    def __init__(self, celsius):
        self.celsius = celsius

    # celsius için property ve setter yaz
    # fahrenheit için salt okunur property yaz

try:
    temp = Temperature(float(input()))
    print(f"{temp.fahrenheit:.1f}")
except ValueError as error:
    print("hata:", error)
''',
  answer=r'''
class Temperature:
    def __init__(self, celsius):
        self.celsius = celsius

    @property
    def celsius(self):
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        if value < -273.15:
            raise ValueError("mutlak sıfırın altında")
        self._celsius = value

    @property
    def fahrenheit(self):
        return self._celsius * 9 / 5 + 32

try:
    temp = Temperature(float(input()))
    print(f"{temp.fahrenheit:.1f}")
except ValueError as error:
    print("hata:", error)
''',
  exampleInput="100",
  expectedOutput="212.0",
  tests=[
      {"label": "Kaynama", "stdin": "100", "expectedOutput": "212.0"},
      {"label": "Donma", "stdin": "0", "expectedOutput": "32.0"},
      {"label": "Eşit nokta", "stdin": "-40", "expectedOutput": "-40.0"},
      {"label": "Mutlak sıfırın altı", "stdin": "-300", "expectedOutput": "hata: mutlak sıfırın altında"},
      {"label": "Sınır değer kabul", "stdin": "-273.15", "expectedOutput": "-459.7"},
  ],
  hints=["Gerçek değeri self._celsius'ta sakla.", "__init__ self.celsius = celsius yazmalı ki setter kurulumda da çalışsın."],
  explanation="celsius için getter ve setter yazılır; setter sınırın altını reddeder, __init__ atamayı setter üzerinden yaptığı için kurulumda da denetim olur. fahrenheit saklanmaz, her okunuşta hesaplanır.")

q(type="code", topic="classmethod", sectionId="static-class-methods", difficulty=2,
  prompt="Duration'a iki yardımcı ekle: @staticmethod valid(text) 's:dd' biçimini denetlesin (tek ':', saat kısmı rakam, dakika kısmı tam iki rakam ve 0-59); @classmethod from_string(text) toplam dakikadan cls(...) kursun. Program metni okur; geçersizse 'geçersiz', geçerliyse label() sonucunu yazar.",
  starterCode=r'''
class Duration:
    def __init__(self, minutes):
        self.minutes = minutes

    def label(self):
        return f"{self.minutes} dk ({self.minutes // 60} sa {self.minutes % 60} dk)"

    # valid(text) staticmethod ve from_string(text) classmethod

text = input()
if Duration.valid(text):
    print(Duration.from_string(text).label())
else:
    print("geçersiz")
''',
  answer=r'''
class Duration:
    def __init__(self, minutes):
        self.minutes = minutes

    def label(self):
        return f"{self.minutes} dk ({self.minutes // 60} sa {self.minutes % 60} dk)"

    @staticmethod
    def valid(text):
        parts = text.split(":")
        if len(parts) != 2:
            return False
        hours, minutes = parts
        return hours.isdigit() and len(minutes) == 2 and minutes.isdigit() and int(minutes) < 60

    @classmethod
    def from_string(cls, text):
        hours, minutes = text.split(":")
        return cls(int(hours) * 60 + int(minutes))

text = input()
if Duration.valid(text):
    print(Duration.from_string(text).label())
else:
    print("geçersiz")
''',
  exampleInput="2:45",
  expectedOutput="165 dk (2 sa 45 dk)",
  tests=[
      {"label": "Normal", "stdin": "2:45", "expectedOutput": "165 dk (2 sa 45 dk)"},
      {"label": "Baştaki sıfır", "stdin": "0:05", "expectedOutput": "5 dk (0 sa 5 dk)"},
      {"label": "Dakika 59'dan büyük", "stdin": "1:75", "expectedOutput": "geçersiz"},
      {"label": "Tek haneli dakika", "stdin": "1:5", "expectedOutput": "geçersiz"},
      {"label": "Ayraç yok", "stdin": "abc", "expectedOutput": "geçersiz"},
      {"label": "Çok haneli saat", "stdin": "10:00", "expectedOutput": "600 dk (10 sa 0 dk)"},
  ],
  hints=["valid, split(':') sonucunun tam iki parça olduğunu da denetlemeli.", "from_string cls(...) döndürmeli; Duration(...) yazma."],
  explanation="valid yalnızca metni inceler ve nesne gerektirmediği için staticmethod'dur. from_string metni dakikaya çevirip cls(...) ile nesne kuran bir alternatif kurucudur.")

q(type="code", topic="composition", sectionId="composition", difficulty=3,
  prompt="İndirim kuralları hazır. Order sınıfını composition ile yaz: __init__(prices, discount) fiyat listesini ve indirim nesnesini saklasın; total() fiyatların toplamına discount.apply(...) uygulayıp döndürsün. Order bir indirim sınıfından türemesin.",
  starterCode=r'''
class NoDiscount:
    def apply(self, amount):
        return amount

class PercentDiscount:
    def __init__(self, percent):
        self.percent = percent

    def apply(self, amount):
        return amount * (100 - self.percent) // 100

class Order:
    def __init__(self, prices, discount):
        # fiyatları ve indirim nesnesini sakla
        pass

    def total(self):
        # toplam fiyata indirimi uygula
        return 0

rule = input().split()
discount = NoDiscount() if rule[0] == "yok" else PercentDiscount(int(rule[1]))
prices = [int(input()) for _ in range(int(input()))]
print(Order(prices, discount).total())
''',
  answer=r'''
class NoDiscount:
    def apply(self, amount):
        return amount

class PercentDiscount:
    def __init__(self, percent):
        self.percent = percent

    def apply(self, amount):
        return amount * (100 - self.percent) // 100

class Order:
    def __init__(self, prices, discount):
        self.prices = prices
        self.discount = discount

    def total(self):
        return self.discount.apply(sum(self.prices))

rule = input().split()
discount = NoDiscount() if rule[0] == "yok" else PercentDiscount(int(rule[1]))
prices = [int(input()) for _ in range(int(input()))]
print(Order(prices, discount).total())
''',
  exampleInput="yüzde 10\n2\n100\n200",
  expectedOutput="270",
  tests=[
      {"label": "İndirimsiz", "stdin": "yok\n2\n100\n200", "expectedOutput": "300"},
      {"label": "Yüzde 10", "stdin": "yüzde 10\n2\n100\n200", "expectedOutput": "270"},
      {"label": "Boş sipariş", "stdin": "yüzde 50\n0", "expectedOutput": "0"},
      {"label": "Tamsayı bölme", "stdin": "yüzde 33\n1\n100", "expectedOutput": "67"},
  ],
  hints=["Order iki nesneyi öznitelik olarak tutar: fiyat listesi ve indirim nesnesi.", "İndirimi kendin hesaplama; self.discount.apply(...) çağır."],
  explanation="Order indirimi kendisi hesaplamaz; indirim nesnesine devreder. Farklı bir indirim kuralı vermek Order'ı değiştirmeyi gerektirmez; bu composition'ın esnekliğidir.")

q(type="code", topic="override", sectionId="inheritance-super", difficulty=2,
  prompt="Product hazır: total() fiyatla shipping()'i toplar, shipping() 30'dur. DigitalProduct(Product) yalnızca shipping()'i geçersiz kılsın (dijital ürünün kargosu yoktur). total()'ı yeniden yazma. Program 'dijital' ya da 'fiziksel' ile fiyatı okur ve toplam tutarı yazdırır.",
  starterCode=r'''
class Product:
    def __init__(self, price):
        self.price = price

    def shipping(self):
        return 30

    def total(self):
        return self.price + self.shipping()

class DigitalProduct(Product):
    pass  # yalnızca shipping'i geçersiz kıl

kind = input()
price = int(input())
product = DigitalProduct(price) if kind == "dijital" else Product(price)
print(product.total())
''',
  answer=r'''
class Product:
    def __init__(self, price):
        self.price = price

    def shipping(self):
        return 30

    def total(self):
        return self.price + self.shipping()

class DigitalProduct(Product):
    def shipping(self):
        return 0

kind = input()
price = int(input())
product = DigitalProduct(price) if kind == "dijital" else Product(price)
print(product.total())
''',
  exampleInput="dijital\n100",
  expectedOutput="100",
  tests=[
      {"label": "Fiziksel", "stdin": "fiziksel\n100", "expectedOutput": "130"},
      {"label": "Dijital", "stdin": "dijital\n100", "expectedOutput": "100"},
      {"label": "Ücretsiz dijital", "stdin": "dijital\n0", "expectedOutput": "0"},
      {"label": "Ücretsiz fiziksel", "stdin": "fiziksel\n0", "expectedOutput": "30"},
  ],
  hints=["Yalnızca bir metodu yeniden yaz; __init__ ve total devralınır.", "Product.total, self.shipping()'i çağırıyor: self bir DigitalProduct ise hangi sürüm çalışır?"],
  explanation="DigitalProduct yalnızca shipping'i geçersiz kılar. Üst sınıfın total'ı self.shipping() çağırdığı için bir DigitalProduct üzerinde alt sınıfın sürümü çalışır ve kargo 0 olur.")

q(type="code", topic="composition", sectionId="composition", difficulty=3,
  prompt="Stack sınıfını composition ile yaz: iç listeyi _items'ta tut, list'ten türeme. push(x) ekler, pop() son öğeyi çıkarıp döndürür, peek() çıkarmadan son öğeyi verir (boşken ikisi de IndexError('yığın boş') fırlatır), size() öğe sayısını döndürür. Program 'push X', 'pop', 'peek', 'size' komutlarını işler; sonda yığında insert metodu olmadığını gösterir.",
  starterCode=r'''
class Stack:
    def __init__(self):
        pass

    def push(self, item):
        pass

    def pop(self):
        pass

    def peek(self):
        pass

    def size(self):
        pass

stack = Stack()
for _ in range(int(input())):
    parts = input().split()
    try:
        if parts[0] == "push":
            stack.push(parts[1])
        elif parts[0] == "pop":
            print(stack.pop())
        elif parts[0] == "peek":
            print(stack.peek())
        elif parts[0] == "size":
            print(stack.size())
    except IndexError as error:
        print("hata:", error)
print("insert yok:", not hasattr(stack, "insert"))
''',
  answer=r'''
class Stack:
    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.append(item)

    def pop(self):
        if not self._items:
            raise IndexError("yığın boş")
        return self._items.pop()

    def peek(self):
        if not self._items:
            raise IndexError("yığın boş")
        return self._items[-1]

    def size(self):
        return len(self._items)

stack = Stack()
for _ in range(int(input())):
    parts = input().split()
    try:
        if parts[0] == "push":
            stack.push(parts[1])
        elif parts[0] == "pop":
            print(stack.pop())
        elif parts[0] == "peek":
            print(stack.peek())
        elif parts[0] == "size":
            print(stack.size())
    except IndexError as error:
        print("hata:", error)
print("insert yok:", not hasattr(stack, "insert"))
''',
  exampleInput="5\npush a\npush b\npeek\npop\nsize",
  expectedOutput="b\nb\n1\ninsert yok: True",
  tests=[
      {"label": "Normal akış", "stdin": "5\npush a\npush b\npeek\npop\nsize", "expectedOutput": "b\nb\n1\ninsert yok: True"},
      {"label": "Boş yığında pop", "stdin": "1\npop", "expectedOutput": "hata: yığın boş\ninsert yok: True"},
      {"label": "Komut yok", "stdin": "0", "expectedOutput": "insert yok: True"},
      {"label": "Boşalan yığın", "stdin": "3\npush x\npop\npeek", "expectedOutput": "x\nhata: yığın boş\ninsert yok: True"},
      {"label": "Boş yığın boyutu", "stdin": "2\nsize\npeek", "expectedOutput": "0\nhata: yığın boş\ninsert yok: True"},
  ],
  hints=["Listeyi self._items özniteliğinde sakla; sınıf başlığına list yazma.", "pop ve peek boş listeyi kendin denetlemeli."],
  explanation="Stack bir listeye sahiptir ama onun arayüzünü devralmaz: yalnızca push, pop, peek ve size açıktır. Bu yüzden insert gibi yığın kuralını bozan metotlar yoktur.")

# ------------------------------------------------------------------ traceback (4)
q(type="traceback", topic="init", sectionId="class-object", difficulty=1,
  prompt="__init__'in beklediği argüman verilmeden nesne kuruluyor. Hangi hata oluşur?",
  code=r'''
class Dog:
    def __init__(self, name):
        self.name = name

pet = Dog()
''',
  expectedError="TypeError",
  options=["TypeError", "AttributeError", "NameError", "ValueError"],
  optionFeedback={
      "AttributeError": "Hiçbir öznitelik aranmıyor; çağrı daha nesne kurulurken başarısız oluyor.",
      "NameError": "Dog ve __init__ tanımlı; eksik olan çağrıdaki argüman.",
      "ValueError": "Değer geçersiz değil, hiç verilmedi.",
  },
  hints=["Dog() çağrısı __init__'e hangi argümanları geçiriyor?", "Eksik pozisyonel argüman hangi hatayı verir?"],
  explanation="Dog() __init__'i yalnızca self ile çağırır, name eksik kalır: TypeError: Dog.__init__() missing 1 required positional argument: 'name'.")

q(type="traceback", topic="name-mangling", sectionId="encapsulation", difficulty=2,
  prompt="Çift alt çizgili öznitelik sınıfın dışından okunuyor. Hangi hata oluşur?",
  code=r'''
class Vault:
    def __init__(self):
        self.__code = 1234

vault = Vault()
print(vault.__code)
''',
  expectedError="AttributeError",
  options=["AttributeError", "NameError", "KeyError", "PermissionError"],
  optionFeedback={
      "NameError": "vault tanımlı; hata, nesne üzerinde öznitelik arayışından geliyor.",
      "KeyError": "Sözlük araması yok; öznitelik erişimi hata veriyor.",
      "PermissionError": "Python erişimi izinle engellemez; öznitelik yalnızca farklı bir adla saklanıyor.",
  },
  hints=["Sınıf içinde __code hangi adla saklanır?", "Dışarıdan vault.__code aranınca o ad bulunur mu?"],
  explanation="Ad bozma nedeniyle öznitelik _Vault__code adıyla saklanır; sınıfın dışında vault.__code yazınca bu ad bulunamaz ve AttributeError oluşur.")

q(type="traceback", topic="property", sectionId="property", difficulty=3,
  prompt="Property kendi adını okuyor. Hangi hata oluşur?",
  code=r'''
class User:
    @property
    def name(self):
        return self.name

print(User().name)
''',
  expectedError="RecursionError",
  options=["RecursionError", "AttributeError", "TypeError", "ValueError"],
  optionFeedback={
      "AttributeError": "name özniteliği var (property olarak); sorun, okunuşunun kendini çağırması.",
      "TypeError": "Çağrı biçimi doğru; sorun sonsuz kendini çağırma.",
      "ValueError": "Hiçbir değer dönüşümü yok.",
  },
  hints=["self.name okunduğunda hangi kod çalışır?", "O kod içinde tekrar self.name okunuyor."],
  explanation="self.name okuması name property'sini çağırır, o da yine self.name okur; bu sonsuz özyineleme Python'un yığın sınırına çarpıp RecursionError verir.")

q(type="traceback", topic="super", sectionId="inheritance-super", difficulty=2,
  prompt="super().__init__'e fazladan argüman veriliyor. Hangi hata oluşur?",
  code=r'''
class Base:
    def __init__(self, name):
        self.name = name

class Child(Base):
    def __init__(self, name, age):
        super().__init__(name, age)
        self.age = age

Child("Ada", 5)
''',
  expectedError="TypeError",
  options=["TypeError", "AttributeError", "NameError", "KeyError"],
  optionFeedback={
      "AttributeError": "Hiçbir öznitelik aranmıyor; Base.__init__ çağrısı argüman sayısı yüzünden başarısız oluyor.",
      "NameError": "Base, super ve age tanımlı adlardır.",
      "KeyError": "Sözlük araması yok.",
  },
  hints=["Base.__init__ kaç parametre bekliyor?", "super().__init__(name, age) ona kaç argüman veriyor?"],
  explanation="Base.__init__ yalnızca self ve name alır; super().__init__(name, age) iki argüman verdiği için TypeError: Base.__init__() takes 2 positional arguments but 3 were given oluşur.")
