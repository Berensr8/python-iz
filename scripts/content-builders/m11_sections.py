"""M11 (OOP 1) lesson sections. Imported by build_m11.py."""

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
    id="class-object",
    title="class, nesne, __init__ ve self",
    eyebrow="Veriyi ve davranışı tek şablonda topla",
    objectives=[
        "class ile bir şablon tanımlar, ondan nesneler (instance) üretir ve her nesnenin kendi verisini taşıdığını gösterir.",
        "__init__ ve self'in rolünü açıklar; metot çağrısında nesnenin ilk parametre olarak otomatik geçtiğini bilir.",
    ],
    prerequisites=["m6:def-return", "m5:names-references"],
    summary="class bir şablondur; Dog('Pamuk') ile ondan nesne üretilir. Nesne yaratılınca __init__ çalışır ve self üzerinden nesnenin verisini (öznitelik) kurar. Metotlar, self'i ilk parametre olarak alan fonksiyonlardır.",
    explanation=(
        "class Dog: ile yeni bir tür tanımlarsın; Dog(...) çağrısı bu türden bir nesne (instance) üretir. Sınıf adları gelenek olarak BüyükHarfle yazılır (Dog, ShoppingCart). "
        "Nesne yaratılınca Python önce boş nesneyi kurar, sonra __init__'i çağırır; __init__ nesneyi hazırlar, yeni bir değer döndürmez (nesnenin kendisini kuran özel metot __new__'dur ve günlük kodda yazılmaz). "
        "self, metodun çalıştığı nesnenin kendisidir: self.name = name o nesneye name özniteliğini bağlar. Aynı sınıftan üretilen her nesnenin kendi öznitelikleri vardır; birini değiştirmek ötekini etkilemez. "
        "pamuk.birthday() çağrısı Python'un gözünde Dog.birthday(pamuk) ile aynıdır: nesne, metoda ilk argüman olarak kendiliğinden geçer. Bu yüzden her metot tanımında self parametresi bulunmalı ve nesnenin verisine self. ile erişilmelidir; yalnızca age yazarsan bu bir yerel değişken ya da NameError olur. "
        "self adı bir gelenektir (dilin zorunluluğu değil) ama hiç ayrılma. type(nesne) türünü, isinstance(nesne, Dog) bir sınıfa ait olup olmadığını söyler. "
        "Yalnızca veri taşıyan basit kayıtlar için sınıf ağır kalabilir: dict, tuple ya da M10'daki namedtuple yeterli olabilir; sınıf, veriyle birlikte o veriyi değiştiren kuralların da aynı yerde durmasını istediğinde anlamlıdır."
    ),
    code=r'''
class Dog:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def describe(self):
        return f"{self.name} ({self.age} yaşında)"

    def birthday(self):
        self.age += 1

pamuk = Dog("Pamuk", 3)
karabas = Dog("Karabaş", 5)
pamuk.birthday()
print(pamuk.describe())
print(karabas.describe())
print(Dog.describe(karabas))
print(type(pamuk).__name__, isinstance(pamuk, Dog))
''',
    expectedOutput=r'''
Pamuk (4 yaşında)
Karabaş (5 yaşında)
Karabaş (5 yaşında)
Dog True
''',
    why="İki nesne aynı şablondan çıktı ama birbirinden bağımsız verileri var: pamuk'un yaşı artınca karabas değişmedi. Dog.describe(karabas) satırı, karabas.describe() çağrısının perde arkasını gösterir: self, nesnenin kendisidir.",
    alternatives=[
        "Yalnızca birkaç alan taşıyan kayıtlar için dict ya da namedtuple daha kısadır; dataclass'ı M12'de göreceksin.",
        "Tek bir iş yapan, durumu olmayan kod için sınıf yerine düz fonksiyon yaz.",
    ],
    traps=[
        "Metot tanımında self'i unutmak: def describe(): çağrıldığında 'takes 0 positional arguments but 1 was given' hatası verir.",
        "__init__ içinde self.age yerine age = age yazmak: yerel değişken oluşur, nesneye hiçbir şey kaydedilmez.",
        "Sınıfı çağırmayı unutmak: pamuk = Dog yazarsan pamuk bir nesne değil, sınıfın kendisidir.",
        "Nesne yaratılırken __init__'in istediği argümanları eksik vermek (Dog() → TypeError).",
    ],
    realCode=r'''
class Product:
    def __init__(self, name, price, stock=0):
        self.name = name
        self.price = price
        self.stock = stock

    def sell(self, count):
        if count > self.stock:
            raise ValueError(f"{self.name}: yetersiz stok ({self.stock})")
        self.stock -= count
        return count * self.price

book = Product("Kitap", 120, stock=5)
print(book.sell(2))
try:
    book.sell(10)
except ValueError as error:
    print(error)
print(book.stock)
''',
    realOutput=r'''
240
Kitap: yetersiz stok (3)
3
''',
    lineByLine=[
        "__init__ üç değeri alıp nesnenin üç özniteliğine bağlar; stock'un varsayılan değeri 0'dır.",
        "sell, kuralı (stoktan fazlası satılamaz) verinin yanında tutar ve geçersiz istekte ValueError fırlatır.",
        "İlk satış geçerlidir: stok 5'ten 3'e düşer ve 2 x 120 = 240 döner.",
        "Yetersiz stoklu satış hata verir ve stoğa dokunmaz; son satır hâlâ 3 yazar.",
    ],
    sources=[
        {"title": "Python 3.12 · Sınıflar (class tanımı ve nesneler)", "url": TUTORIAL},
    ],
)

section(
    id="methods-state",
    title="Metotlar, nesne durumu ve metin gösterimi",
    eyebrow="Durumu değiştir, okunur göster",
    objectives=[
        "Nesnenin durumunu değiştiren metot ile yeni bir değer hesaplayıp döndüren metot arasındaki farkı ayırır.",
        "__repr__ ve __str__ ile nesneye okunur bir metin gösterimi verir ve print ile liste içi gösterimin neden farklı olduğunu açıklar.",
    ],
    prerequisites=["class-object", "m5:mutable-immutable"],
    summary="Bir metot ya nesnenin durumunu değiştirir (çoğu zaman None döner) ya da bir değer hesaplayıp döndürür. __str__ print ve f-string için okunur metin, __repr__ ise geliştiriciye yönelik, mümkünse yeniden kurulabilir gösterim verir.",
    explanation=(
        "Metotlar iki ana iş yapar: komut (nesnenin durumunu değiştirir; list.append gibi, genellikle None döner) ve sorgu (durumu okuyup bir değer döndürür; total() gibi). Karıştırmak yaygın bir hatadır: result = basket.add('Süt') yazıp sonucun sepet olmasını beklemek, add yalnızca durumu değiştirdiği için None verir. "
        "Bir metot self'i döndürürse çağrılar zincirlenebilir (basket.add('a').add('b')); bunu bilinçli bir tercih olarak kullan. Nesneler değiştirilebilir referanslardır (M5): other = basket yeni nesne üretmez, aynı sepete ikinci bir ad bağlar; bir fonksiyona verilen nesne de fonksiyonun içinde değiştirilebilir. "
        "pamuk.describe gibi parantezsiz metot, nesneye bağlı bir metot nesnesidir; saklanıp sonra çağrılabilir ve self'i hatırlar. "
        "Bir nesneyi yazdırırken varsayılan gösterim <__main__.Basket object at 0x...> gibi anlamsızdır. __str__ print(nesne) ve f-string için okunur metni, __repr__ ise hata ayıklamada, repr(nesne)'de ve listelerin içinde görünen gösterimi belirler; yalnızca __repr__ yazarsan __str__ da onu kullanır. Genel kural: her sınıfa en azından bir __repr__ yaz; ikisini birden yazmak zorunlu değildir."
    ),
    code=r'''
class Basket:
    def __init__(self):
        self.items = []

    def add(self, name, price):
        self.items.append((name, price))
        return self

    def total(self):
        return sum(price for _, price in self.items)

    def __repr__(self):
        return f"Basket({len(self.items)} ürün, toplam={self.total()})"

    def __str__(self):
        return ", ".join(name for name, _ in self.items) or "boş sepet"

basket = Basket()
print(basket)
basket.add("Ekmek", 15).add("Süt", 40)
print(basket)
print(repr(basket))
print([basket])
other = basket
other.add("Peynir", 120)
print(basket.total(), len(basket.items))
add = basket.add
add("Su", 10)
print(basket.total())
''',
    expectedOutput=r'''
boş sepet
Ekmek, Süt
Basket(2 ürün, toplam=55)
[Basket(2 ürün, toplam=55)]
175 3
185
''',
    why="print(basket) __str__'i, repr(basket) ve liste içindeki gösterim __repr__'i kullandı. add self döndürdüğü için iki çağrı zincirlendi. other ve basket aynı nesneye bağlı olduğundan Peynir her ikisinde de görünür; add = basket.add ise self'i hatırlayan bağlı bir metottur, bu yüzden add('Su', 10) yine aynı sepete ekler.",
    alternatives=[
        "Yalnızca bir gösterim yazacaksan __repr__ yaz; __str__ yoksa print de onu kullanır.",
        "Zincirleme hoşuna gitmiyorsa metotları None döndüren komutlar olarak bırak ve çağrıları ayrı satırlara yaz; daha az sürpriz verir.",
    ],
    traps=[
        "Komut metodunun değer döndürdüğünü sanıp sonucu bir değişkene atamak (result = basket.add(...) → None).",
        "Nesneyi kopyalamak için other = basket yazmak; aynı nesneye ikinci bir ad bağlanır.",
        "__repr__ içinde yeniden hesaplanması pahalı ya da hata verebilecek işler yapmak; hata ayıklarken kendi hatan çıkar.",
        "__str__ ya da __repr__ içinde print yazıp metni döndürmeyi unutmak (TypeError: __str__ returned non-string).",
    ],
    realCode=r'''
class Task:
    def __init__(self, title, done=False):
        self.title = title
        self.done = done

    def finish(self):
        self.done = True

    def __repr__(self):
        return f"Task({self.title!r}, done={self.done})"

tasks = [Task("rapor"), Task("test")]
tasks[0].finish()
print(tasks)
pending = [task.title for task in tasks if not task.done]
print(pending)
''',
    realOutput=r'''
[Task('rapor', done=True), Task('test', done=False)]
['test']
''',
    lineByLine=[
        "finish bir komut metodudur: durumu değiştirir, değer döndürmez.",
        "__repr__ içindeki !r, başlığı tırnaklı (repr biçiminde) gösterir; liste içinde nesnenin ne olduğu hemen okunur.",
        "Listeyi yazdırmak her öğenin __repr__'ini kullanır; __repr__ olmasaydı adres içeren anlamsız metinler görünürdü.",
        "pending listesi, durumu bozmadan nesnelerin öznitelikleri üzerinden hesaplanan bir sorgu sonucudur.",
    ],
    sources=[
        {"title": "Python 3.12 · Sınıflar (metot nesneleri)", "url": TUTORIAL + "#method-objects"},
        {"title": "Python 3.12 · Veri modeli: __repr__ ve __str__", "url": "https://docs.python.org/3.12/reference/datamodel.html#object.__repr__"},
    ],
)

section(
    id="instance-class-vars",
    title="Instance ve class değişkenleri",
    eyebrow="Nesneye özel mi, sınıfta ortak mı?",
    objectives=[
        "Class değişkeni ile instance değişkeni arasındaki farkı ve Python'un özniteliği nesne, sonra sınıf sırasıyla aradığını açıklar.",
        "Nesne üzerinden atamanın class değişkenini gölgelediğini ve değiştirilebilir bir class değişkeninin bütün nesnelerce paylaşıldığını gösterir, hatayı düzeltir.",
    ],
    prerequisites=["class-object", "m6:mutable-default"],
    summary="self.x = ... nesneye özel (instance) özniteliği kurar. Sınıfın gövdesinde yazılan x = ... ise bütün nesnelerin paylaştığı class değişkenidir. Öznitelik okunurken önce nesne, bulunamazsa sınıf aranır.",
    explanation=(
        "Sınıf gövdesinde (metotların dışında) tanımlanan ad class değişkenidir ve sınıfa aittir; tüm nesneler ona erişebilir. self.ad = ... ile kurulan özniteliğe instance değişkeni denir ve her nesnenin kendi kopyası vardır. "
        "nesne.ad okunurken Python önce nesnenin kendi öznitelik sözlüğüne (vars(nesne)), orada yoksa sınıfa, sonra üst sınıflara bakar. Bu yüzden Student.school değiştirilince, kendi school özniteliği olmayan bütün nesneler yeni değeri görür. "
        "Atama farklı çalışır: can.school = 'X' sınıfı değiştirmez; yalnızca can nesnesinin kendi school özniteliğini oluşturur ve bu, sınıftakini gölgeler. del can.school gölgeyi kaldırır ve sınıfın değeri yeniden görünür. "
        "Ortak sayaç gibi sınıf düzeyinde durumu değiştirmek için sınıf adını kullan (Student.count += 1). self.count += 1 yazarsan sağ taraf sınıftaki değeri okur, sol taraf ise nesnede yeni bir count oluşturur; sınıfın sayacı hiç artmaz. "
        "En sık hata, değiştirilebilir bir değeri (liste, sözlük, küme) class düzeyinde tanımlamaktır: self.songs.append(...) sınıftaki tek listeyi büyütür ve bütün nesneler aynı veriyi görür; M6'daki değiştirilebilir varsayılan argüman tuzağının kardeşidir. Nesneye özel değiştirilebilir veriyi her zaman __init__ içinde kur. Class değişkenleri sabitler (vergi oranı, varsayılan ayar) ve gerçekten ortak sayaçlar için uygundur."
    ),
    code=r'''
class Student:
    school = "Python İz"
    count = 0

    def __init__(self, name):
        self.name = name
        Student.count += 1

ada = Student("Ada")
can = Student("Can")
print(Student.count, ada.count, can.school)
can.school = "Başka okul"
print(ada.school, can.school, Student.school)
print(vars(can))
Student.school = "Yeni ad"
print(ada.school, can.school)
del can.school
print(can.school)
''',
    expectedOutput=r'''
2 2 Python İz
Python İz Başka okul Python İz
{'name': 'Can', 'school': 'Başka okul'}
Yeni ad Başka okul
Yeni ad
''',
    why="count sınıfta tutulduğu için iki nesne de 2'yi gördü. can.school ataması yalnızca can'a özel bir öznitelik oluşturdu (vars bunu gösterir) ve sınıftakini gölgeledi. Student.school değişince ada yeni değeri gördü, can ise kendi gölgesini görmeye devam etti; del ile gölge kalkınca can da sınıfın değerine döndü.",
    alternatives=[
        "Nesneye özel her şeyi __init__ içinde self ile kur; class düzeyinde yalnızca sabit ve gerçekten paylaşılan değerler tut.",
        "Sınıfı ilgilendiren bir sayaç yerine her nesnenin kendi sayacına ihtiyacın varsa onu __init__ içinde self.count = 0 ile başlat.",
    ],
    traps=[
        "Değiştirilebilir bir class değişkenini (liste, sözlük) nesneye özel sanmak; tüm nesneler aynı listeyi paylaşır.",
        "Sınıf sayacını self.count += 1 ile artırmaya çalışmak; her nesnede ayrı bir count oluşur ve sınıfınki 0 kalır.",
        "nesne.ad = ... yazarak sınıf değişkenini değiştirdiğini sanmak; yalnızca o nesnede gölge oluşur.",
        "Class değişkenini yeniden atamadan, aynı nesne üzerinden okuyup değişmediğini sanmak (kendi gölgesi olan nesne eski değeri gösterir).",
    ],
    realCode=r'''
class SharedPlaylist:
    songs = []

    def add(self, song):
        self.songs.append(song)

class Playlist:
    def __init__(self):
        self.songs = []

    def add(self, song):
        self.songs.append(song)

a, b = SharedPlaylist(), SharedPlaylist()
a.add("Ezgi")
print(b.songs)
c, d = Playlist(), Playlist()
c.add("Ezgi")
print(d.songs)
''',
    realOutput=r'''
['Ezgi']
[]
''',
    lineByLine=[
        "SharedPlaylist.songs sınıfta tek bir listedir; self.songs.append o listeyi büyütür.",
        "Playlist, listeyi __init__ içinde kurar; her nesnenin kendi listesi olur.",
        "a'ya eklenen şarkı b'de de görünür çünkü ikisi aynı listeyi okur.",
        "c'ye eklenen şarkı d'yi etkilemez; nesneye özel veri __init__ içinde yaratıldı.",
    ],
    sources=[
        {"title": "Python 3.12 · Sınıf ve instance değişkenleri", "url": TUTORIAL + "#class-and-instance-variables"},
    ],
)

section(
    id="inheritance-super",
    title="Kalıtım ve super()",
    eyebrow="Var olan sınıfı genişlet",
    objectives=[
        "Alt sınıfın üst sınıfın metotlarını devraldığını, yeniden tanımladığını (override) ve super() ile genişlettiğini gösterir.",
        "isinstance ve issubclass ile 'bir ... dır' (is-a) ilişkisini sınar; super().__init__ çağrısı unutulduğunda neyin kurulmadığını açıklar.",
    ],
    prerequisites=["class-object", "instance-class-vars"],
    summary="class Manager(Employee): ile Manager, Employee'nin tüm öznitelik ve metotlarını devralır. Aynı adlı metot yazmak onu geçersiz kılar (override); super() üst sınıfın sürümüne erişip onu genişletmeyi sağlar.",
    explanation=(
        "class Alt(Üst): yazınca Alt nesneleri Üst'ün metotlarını kullanabilir. Bir metot çağrılınca Python önce nesnenin sınıfına, bulamazsa üst sınıfa bakar; alt sınıfta aynı adı yazmak üst sınıftaki sürümü geçersiz kılar (override). "
        "super() üst sınıfın metoduna erişir: super().__init__(name, salary) üst sınıfın kurulum kodunu çalıştırır, super().summary() üst sınıfın sonucunu alıp üstüne ekleme yapmanı sağlar. Alt sınıf kendi __init__'ini yazarsa üst sınıfınki otomatik çalışmaz; super().__init__(...) çağrılmazsa üst sınıfın öznitelikleri hiç kurulmaz ve sonradan AttributeError alırsın. "
        "Üst sınıfın bir metodu self.role() gibi başka bir metodu çağırıyorsa, nesne alt sınıfınsa alt sınıfın sürümü çalışır; bu, ortak akışı üst sınıfta, değişen adımı alt sınıfta yazmanın temelidir. "
        "isinstance(nesne, Sınıf) nesne o sınıftan ya da onun alt sınıfından üretildiyse True verir; type(nesne) is Sınıf ise tam eşleşmeyi sorar. issubclass sınıf ilişkisini sınar. Her sınıf örtük olarak object'ten türer. "
        "Kalıtımı yalnızca gerçek 'bir ... dır' ilişkisinde kullan (Yönetici bir çalışandır). Sırf kod tekrarı olmasın diye ilgisiz sınıfları türetmek kırılgan tasarım yaratır; ek bölümde composition alternatifine bakacağız. Çoklu kalıtım, abc ve polimorfizm M12'dedir."
    ),
    code=r'''
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def role(self):
        return "çalışan"

    def summary(self):
        return f"{self.name} - {self.role()} - {self.salary}"

class Manager(Employee):
    def __init__(self, name, salary, team):
        super().__init__(name, salary)
        self.team = team

    def role(self):
        return "yönetici"

    def summary(self):
        return super().summary() + f" - ekip: {len(self.team)}"

ada = Employee("Ada", 5000)
can = Manager("Can", 8000, ["Ada", "Eda"])
print(ada.summary())
print(can.summary())
print(isinstance(can, Employee), isinstance(ada, Manager))
print(issubclass(Manager, Employee), type(can).__name__)
''',
    expectedOutput=r'''
Ada - çalışan - 5000
Can - yönetici - 8000 - ekip: 2
True False
True Manager
''',
    why="Manager, name ve salary'yi kendisi kurmak yerine super().__init__ ile Employee'ye devretti. Employee.summary içindeki self.role() Manager nesnesinde Manager'ın sürümünü çalıştırdığı için 'yönetici' yazdı; Manager.summary ise üst sınıfın sonucuna ekip bilgisini ekledi. Yönetici bir çalışandır (True) ama her çalışan yönetici değildir (False).",
    alternatives=[
        "Alt sınıf yalnızca bir metodu değiştiriyorsa __init__ yazma; üst sınıfınki zaten devralınır.",
        "İlişki 'bir ... dır' değil 'sahiptir' ise kalıtım yerine composition kullan (bu modülün son bölümü).",
    ],
    traps=[
        "Alt sınıfta __init__ yazıp super().__init__(...) çağırmayı unutmak; üst sınıfın öznitelikleri kurulmaz.",
        "super().__init__'e üst sınıfın beklemediği fazla ya da eksik argüman vermek (TypeError).",
        "Kalıtımı yalnızca kod paylaşmak için kullanmak; alt sınıf, üst sınıfın bütün genel arayüzünü de devralır.",
        "Derin kalıtım zincirleri kurmak; bir metodun hangi sınıftan geldiğini bulmak zorlaşır.",
    ],
    realCode=r'''
class Notifier:
    def __init__(self, prefix):
        self.prefix = prefix

    def format(self, message):
        return f"[{self.prefix}] {message}"

    def send(self, message):
        print(self.format(message))

class UrgentNotifier(Notifier):
    def format(self, message):
        return super().format(message.upper()) + "!"

for notifier in (Notifier("bilgi"), UrgentNotifier("acil")):
    notifier.send("disk dolu")
''',
    realOutput=r'''
[bilgi] disk dolu
[acil] DISK DOLU!
''',
    lineByLine=[
        "Notifier.send akışı sabit tutar: önce format, sonra yazdır.",
        "UrgentNotifier yalnızca format'ı geçersiz kılar; __init__ ve send'i devralır.",
        "super().format(...) üst sınıfın biçimlendirmesini kullanıp üzerine büyük harf ve ünlem ekler.",
        "Aynı send çağrısı, nesnenin sınıfına göre farklı biçimlendirme yapar; ortak kod tek yerde kalır.",
    ],
    sources=[
        {"title": "Python 3.12 · Kalıtım", "url": TUTORIAL + "#inheritance"},
        {"title": "Python 3.12 · super()", "url": "https://docs.python.org/3.12/library/functions.html#super"},
    ],
)

section(
    id="encapsulation",
    title="Kapsülleme",
    eyebrow="Durumu korumak için sınır çiz",
    objectives=[
        "_ad ve __ad adlandırmasının ne sağladığını (gelenek ve ad bozma) ve ne sağlamadığını (gerçek gizlilik) açıklar.",
        "Geçersiz duruma izin vermeyen genel metotlar yazar ve iç veriyi kopyasıyla vererek dışarıdan bozulmasını önler.",
    ],
    prerequisites=["class-object", "m7:raising"],
    summary="Python'da gerçek private yoktur: _ad 'iç kullanım' demektir, __ad ise ad bozma (name mangling) uygular. Kapsüllemenin amacı gizlemek değil, nesnenin durumunu kurallarını bilen metotlar üzerinden değiştirmektir.",
    explanation=(
        "Kapsülleme, bir nesnenin verisini ve o veriyi değiştiren kuralları bir arada tutmaktır; böylece nesne her zaman geçerli durumda kalır (bakiye eksiye düşmez, ad boş olmaz). Python bunu dil kuralıyla değil gelenekle sağlar. "
        "Tek alt çizgiyle başlayan ad (self._balance) 'bu bir iç ayrıntı, dışarıdan dokunma' anlamına gelir; Python engellemez ama okuyan herkes sınırı anlar. İki alt çizgiyle başlayan ad (self.__log) sınıf içinde _SınıfAdı__log olarak yeniden adlandırılır (name mangling). Amaç alt sınıfların aynı adı yanlışlıkla ezmesini önlemektir; güvenlik değildir, nesne._Account__log ile yine okunur. "
        "Dışarıya iç yapının kendisini vermek kapsüllemeyi deler: bir metot self._members listesini olduğu gibi döndürürse çağıran taraf listeye doğrudan ekleme yapıp kuralı atlayabilir. Kopya (list(self._members)) ya da değiştirilemez bir görünüm (tuple(...)) döndür. "
        "İyi bir sınıf, geçersiz istekleri açık bir hatayla (ValueError) reddeder ve durumu bozmaz. Her özniteliği gizleme: kural gerektirmeyen basit alanlar herkese açık kalabilir (self.owner). Kuralı olan alanlar için bir sonraki bölümdeki property, aynı korumayı öznitelik sözdizimiyle sağlar."
    ),
    code=r'''
class Account:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self._balance = balance
        self.__log = []

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("tutar pozitif olmalı")
        self._balance += amount
        self.__log.append(("yatır", amount))

    def withdraw(self, amount):
        if amount > self._balance:
            raise ValueError("yetersiz bakiye")
        self._balance -= amount
        self.__log.append(("çek", amount))

    def history(self):
        return tuple(self.__log)

acc = Account("Ada", 100)
acc.deposit(50)
try:
    acc.withdraw(500)
except ValueError as error:
    print("hata:", error)
print(acc._balance)
print(acc.history())
print(hasattr(acc, "__log"), hasattr(acc, "_Account__log"))
print(sorted(name for name in vars(acc) if "log" in name))
''',
    expectedOutput=r'''
hata: yetersiz bakiye
150
(('yatır', 50),)
False True
['_Account__log']
''',
    why="withdraw ve deposit bakiyeyi kuralları denetleyerek değiştirir; geçersiz çekim hatayla reddedildi ve bakiye 150 kaldı. _balance Python tarafından engellenmedi, ama gelenek 'dokunma' der. __log, _Account__log adıyla saklandığı için __log adıyla bulunamaz. history ise listeyi değil, değiştirilemeyen bir tuple kopyasını verir.",
    alternatives=[
        "Kural gerektirmeyen alanları (owner gibi) düz öznitelik bırak; her şeye getter/setter yazmak Python'da gereksiz.",
        "Kural gerektiren bir alanı öznitelik gibi kullandırmak için property kullan (sonraki bölüm).",
    ],
    traps=[
        "__ad'ın gerçek bir gizlilik ya da güvenlik sağladığını sanmak; ad bozma yalnızca ad çakışmasını önler.",
        "İç listeyi ya da sözlüğü olduğu gibi döndürüp çağıranın kuralı atlamasına izin vermek.",
        "Nesne dışarıdan _ ile başlayan ada doğrudan yazılıp durumun bozulması; sınır geleneğe uymayı gerektirir.",
        "Her alana boş getter/setter yazıp kodu şişirmek.",
    ],
    realCode=r'''
class Roster:
    def __init__(self):
        self._names = []

    def add(self, name):
        name = name.strip()
        if not name:
            raise ValueError("ad boş olamaz")
        if name not in self._names:
            self._names.append(name)

    def names(self):
        return list(self._names)

roster = Roster()
roster.add(" Ada ")
roster.add("Can")
roster.add("Ada")
copy = roster.names()
copy.append("Sahte")
print(roster.names(), copy)
''',
    realOutput=r'''
['Ada', 'Can'] ['Ada', 'Can', 'Sahte']
''',
    lineByLine=[
        "add, adı temizler, boşu reddeder ve aynı adı ikinci kez eklemez; kural tek yerde durur.",
        "names iç listeyi değil kopyasını döndürür.",
        "copy.append('Sahte') yalnızca kopyayı değiştirir; Roster'ın iç listesi bozulmaz.",
        "Çıktıdaki ilk liste hâlâ yalnız Ada ve Can içerir.",
    ],
    sources=[
        {"title": "Python 3.12 · Özel değişkenler ve ad bozma", "url": TUTORIAL + "#private-variables"},
    ],
)

section(
    id="property",
    title="property",
    eyebrow="Öznitelik gibi görünen, kontrollü erişim",
    objectives=[
        "@property ile hesaplanan bir değeri öznitelik gibi okutur ve sakladığı değerin eskimesini önler.",
        "Setter ile atamayı doğrular, setter olmayan property'yi salt okunur kurar ve property içinde kendi adını kullanmanın sonsuz özyinelemeye yol açtığını bilir.",
    ],
    prerequisites=["encapsulation", "m7:raising"],
    summary="@property bir metodu öznitelik gibi okunur hâle getirir (nesne.alan). @ad.setter ile atamaya kural eklenir. Setter yoksa atama AttributeError verir. Veri, property adından farklı bir özniteliğe (_ad) saklanır.",
    explanation=(
        "@property, bir metodu parantezsiz öznitelik olarak okutur: circle.diameter, her okunuşta metodu çalıştırır ve güncel değeri verir. Böylece 'çap = yarıçap x 2' gibi türetilmiş değerleri ayrıca saklayıp eskitme riskin kalmaz. (@ ile başlayan satırlar decorator'dır; çalışma biçimini M13'te inceleyeceğiz, burada yalnızca kullanımı gerekir.) "
        "Atamayı denetlemek için aynı adla @ad.setter yazılır; setter değeri doğrular, geçerliyse saklar, değilse ValueError fırlatır. Gerçek veri, property adından farklı bir özniteliktedir (self._radius). Property içinde kendi adını okur ya da yazarsan (return self.radius) her erişim kendini çağırır ve RecursionError alırsın. "
        "__init__ içinde self.radius = radius yazmak, setter'ı da çalıştırır; böylece doğrulama nesne kurulurken de geçerli olur (self._radius = radius yazsaydın kurulumda denetim atlanırdı). Setter tanımlamazsan property salt okunurdur ve atama AttributeError verir. "
        "Öznitelik sözdiziminin avantajı şudur: başta düz bir öznitelik olarak yazılan sınıf, sonradan çağıran kodu değiştirmeden property'ye dönüştürülebilir; bu yüzden en baştan get_x/set_x metotları yazmana gerek yoktur. Property her erişimde çalışır; ağır iş (dosya, ağ) için uygun değildir, öyle işleri açık bir metoda koy."
    ),
    code=r'''
class Circle:
    def __init__(self, radius):
        self.radius = radius

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        if value <= 0:
            raise ValueError("yarıçap pozitif olmalı")
        self._radius = value

    @property
    def diameter(self):
        return self._radius * 2

circle = Circle(3)
print(circle.radius, circle.diameter)
circle.radius = 5
print(circle.diameter)
try:
    circle.radius = 0
except ValueError as error:
    print(error)
try:
    circle.diameter = 10
except AttributeError:
    print("diameter salt okunur")
try:
    Circle(-2)
except ValueError as error:
    print("kurulumda da:", error)
''',
    expectedOutput=r'''
3 6
10
yarıçap pozitif olmalı
diameter salt okunur
kurulumda da: yarıçap pozitif olmalı
''',
    why="radius dışarıdan düz bir öznitelik gibi okunup yazılıyor ama her atama setter'dan geçiyor. diameter hiç saklanmıyor, her okunuşta _radius'tan hesaplandığı için radius değişince hemen güncelleniyor; setter'ı olmadığı için atama AttributeError veriyor. __init__ self.radius = radius yazdığı için Circle(-2) kurulumda da reddediliyor.",
    alternatives=[
        "Kural ya da hesaplama gerekmiyorsa düz öznitelik yeterlidir.",
        "Hesaplama ağırsa property yerine açık bir metot (hesapla()) kullan; öznitelik okuma ucuz görünmeli.",
    ],
    traps=[
        "Property içinde kendi adını kullanmak: return self.price → RecursionError. Veriyi self._price'ta sakla.",
        "__init__ içinde self._radius = radius yazıp setter'ın doğrulamasını atlamak.",
        "Setter olmayan property'ye atama yapmak (AttributeError).",
        "Property içinde ağır iş, dosya ya da ağ çağrısı yapmak; her erişim bu işi tekrarlar.",
    ],
    realCode=r'''
class Temperature:
    def __init__(self, celsius):
        self.celsius = celsius

    @property
    def fahrenheit(self):
        return self.celsius * 9 / 5 + 32

t = Temperature(100)
print(t.fahrenheit)
t.celsius = 0
print(t.fahrenheit)
''',
    realOutput=r'''
212.0
32.0
''',
    lineByLine=[
        "celsius düz bir özniteliktir; kural gerektirmediği için property yapılmadı.",
        "fahrenheit saklanmaz, her okunuşta celsius'tan hesaplanır.",
        "İlk okuma 100 derece için 212.0 verir.",
        "celsius 0 yapılınca fahrenheit ayrıca güncellenmek zorunda kalmadan 32.0 olur.",
    ],
    sources=[
        {"title": "Python 3.12 · property", "url": "https://docs.python.org/3.12/library/functions.html#property"},
    ],
)

section(
    id="static-class-methods",
    title="classmethod ve staticmethod",
    eyebrow="Nesneye değil, sınıfa bağlı metotlar",
    objectives=[
        "@classmethod'u alternatif kurucu (from_string gibi) olarak yazar ve cls sayesinde alt sınıfın nesnesi üretildiğini gösterir.",
        "@staticmethod'un self ya da cls almadığını, yalnızca sınıfın ad alanında duran bir fonksiyon olduğunu açıklar ve ne zaman gerekmediğini bilir.",
    ],
    prerequisites=["class-object", "instance-class-vars", "inheritance-super"],
    summary="@classmethod ilk parametre olarak sınıfı (cls) alır; farklı biçimlerden nesne kurmak için kullanılır. @staticmethod hiçbir otomatik parametre almaz; sınıfla ilgili ama nesneye de sınıfa da ihtiyaç duymayan yardımcı işler içindir.",
    explanation=(
        "Sıradan metot nesneyi (self), classmethod sınıfı (cls) alır. En yaygın kullanımı alternatif kurucudur: __init__ tek bir biçimde nesne kurar; Date.from_string('2026-10-06') gibi bir classmethod metni ayrıştırıp cls(...) ile nesneyi üretir. "
        "Burada Date(...) yazmak yerine cls(...) yazman önemlidir: classmethod alt sınıftan çağrılınca cls alt sınıftır ve alt sınıfın nesnesi döner (EventDate.from_string(...) bir EventDate verir). Classmethod sınıf değişkenlerine de erişebilir ve onları değiştirebilir. "
        "@staticmethod'a ne nesne ne sınıf geçer; sınıfın içine konmuş sıradan bir fonksiyondur (Date.is_leap(2028)). Ad alanı düzeni için kullanılır: işlev sınıfla ilgilidir ve çağıran Date.is_leap yazarak ne olduğunu anlar. Bir statik metot self ya da cls'e ihtiyaç duyuyorsa yanlış türdedir. "
        "Her ikisi de nesne üzerinden de çağrılabilir (d.is_leap(1900)). İlgisiz bir yardımcı fonksiyonu sırf sınıfın içine koymak için staticmethod kullanma; çoğu zaman modül düzeyindeki düz fonksiyon daha sadedir."
    ),
    code=r'''
class Date:
    def __init__(self, year, month, day):
        self.year, self.month, self.day = year, month, day

    @classmethod
    def from_string(cls, text):
        year, month, day = map(int, text.split("-"))
        return cls(year, month, day)

    @staticmethod
    def is_leap(year):
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

    def __repr__(self):
        return f"{type(self).__name__}({self.year}, {self.month}, {self.day})"

class EventDate(Date):
    pass

d = Date.from_string("2026-10-06")
e = EventDate.from_string("2026-12-31")
print(d, e)
print(type(e).__name__, Date.is_leap(2028), d.is_leap(1900))
''',
    expectedOutput=r'''
Date(2026, 10, 6) EventDate(2026, 12, 31)
EventDate True False
''',
    why="from_string metni ayrıştırıp cls(...) ile nesne kurdu. EventDate.from_string çağrıldığında cls EventDate olduğundan sonuç bir EventDate nesnesidir. is_leap ise self'e de cls'e de ihtiyaç duymaz; hem sınıf hem nesne üzerinden çağrılabilir (1900 artık yıl değil).",
    alternatives=[
        "Alternatif biçimi tek bir fonksiyona sığdırabiliyorsan modül düzeyinde bir fabrika fonksiyonu da yazabilirsin; classmethod, alt sınıfların da kullanmasını istediğinde üstündür.",
        "Sınıfa bağlı olmayan yardımcı işleri modül düzeyinde düz fonksiyon olarak bırak.",
    ],
    traps=[
        "classmethod içinde sınıf adını sabit yazmak (return Date(...)); alt sınıf çağırınca yine üst sınıfın nesnesi döner. cls kullan.",
        "@staticmethod içinde self ya da cls kullanmaya çalışmak (NameError).",
        "@classmethod yazmayı unutup metodun ilk parametresine sınıfı bekleyerek çağırmak.",
        "Her yardımcı fonksiyonu sınıfa staticmethod olarak taşımak.",
    ],
    realCode=r'''
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email

    @classmethod
    def from_dict(cls, data):
        return cls(data["name"].strip().title(), data["email"].lower())

    @staticmethod
    def valid_email(text):
        return "@" in text and "." in text.split("@")[-1]

user = User.from_dict({"name": " ada lovelace ", "email": "ADA@Ornek.COM"})
print(user.name, user.email, User.valid_email(user.email))
''',
    realOutput=r'''
Ada Lovelace ada@ornek.com True
''',
    lineByLine=[
        "__init__ hazır değerleri alır; ham sözlüğü işleme sorumluluğu from_dict'te.",
        "from_dict adı temizleyip büyük harfe çevirir, e-postayı küçültür ve cls(...) ile nesneyi kurar.",
        "valid_email nesneye ihtiyaç duymaz; sınıf adıyla çağrılan bir doğrulama yardımcısıdır.",
        "Çıktı, düzeltilmiş ad ve e-postayı ve doğrulamanın True olduğunu gösterir.",
    ],
    sources=[
        {"title": "Python 3.12 · classmethod", "url": "https://docs.python.org/3.12/library/functions.html#classmethod"},
        {"title": "Python 3.12 · staticmethod", "url": "https://docs.python.org/3.12/library/functions.html#staticmethod"},
    ],
)

section(
    id="composition",
    title="Composition: sahip olma ilişkisi",
    eyebrow="Kalıtımdan önce 'bir mi, sahip mi?' diye sor",
    objectives=[
        "'Bir ... dır' (kalıtım) ile 'sahiptir / kullanır' (composition) ilişkisini ayırır.",
        "Bir nesnenin işini başka bir nesneye devrederek (delegation) çözer ve kalıtımın yanlış seçildiği tasarımı (ör. Stack(list)) tanır.",
    ],
    prerequisites=["inheritance-super", "encapsulation"],
    summary="Composition'da bir nesne, işini yaptıran başka nesneleri öznitelik olarak tutar (Car bir Engine'e sahiptir). Kalıtım alt sınıfı üst sınıfa bağlar; composition parçaları değiştirilebilir ve sınıfın genel arayüzünü senin kontrolünde bırakır.",
    explanation=(
        "Tasarımda iki soru sor: A bir B midir (Yönetici bir çalışandır → kalıtım) yoksa A, B'ye sahip mi / onu kullanıyor mu (Araba bir motora sahiptir → composition)? Composition'da sınıf, iş birliği yaptığı nesneleri öznitelikte tutar ve gerekli işi onlara devreder (delegation): car.start() içinde self.engine.start() çağrılır. "
        "Kalıtım güçlü ama sıkı bir bağdır: alt sınıf, üst sınıfın bütün genel arayüzünü de devralır. class Stack(list) yazarsan yığın kuralını bozan insert, remove, sort metotları da yığında kalır; kullanıcı yığının ortasına eleman sokabilir. Stack bir list değildir, bir list kullanır: listeyi iç öznitelikte saklayıp yalnızca push, pop gibi gerçekten istediğin metotları dışarı açmak arayüzü senin elinde tutar. "
        "Composition parçaları değiştirmeyi kolaylaştırır: Car bir Engine nesnesini dışarıdan alıyorsa farklı güçte bir motor ya da testte sahte bir motor verebilirsin; kalıtımda bu değişiklik sınıf hiyerarşisini değiştirmeyi gerektirir. Dışarıdan nesne verme (dependency injection) yeni bir araç değil, sadece nesneyi __init__'e parametre olarak geçirmektir. "
        "Kalıtım kötü değildir: gerçek bir uzmanlaşma varsa (UrgentNotifier bir Notifier'dır) ve üst sınıfın tüm arayüzünü devralmak mantıklıysa uygundur. Şüphede kaldığında yeni tasarımlarda composition'ı tercih et."
    ),
    code=r'''
class Engine:
    def __init__(self, power):
        self.power = power

    def start(self):
        return f"{self.power} beygir motor çalıştı"

class Radio:
    def __init__(self):
        self.on = False

    def toggle(self):
        self.on = not self.on
        return "radyo açık" if self.on else "radyo kapalı"

class Car:
    def __init__(self, engine, radio=None):
        self.engine = engine
        self.radio = radio

    def start(self):
        return self.engine.start()

    def toggle_radio(self):
        if self.radio is None:
            return "radyo yok"
        return self.radio.toggle()

car = Car(Engine(90), Radio())
basic = Car(Engine(60))
print(car.start())
print(car.toggle_radio(), car.toggle_radio())
print(basic.toggle_radio())
print(isinstance(car, Engine), isinstance(car.engine, Engine))
''',
    expectedOutput=r'''
90 beygir motor çalıştı
radyo açık radyo kapalı
radyo yok
False True
''',
    why="Car hiçbir sınıftan türemedi; Engine ve Radio nesnelerine sahip olup işi onlara devretti. Radyosu olmayan araba aynı sınıfla (radio=None) çalıştı. Araba bir motor değildir (False), ama motora sahiptir (car.engine bir Engine'dir).",
    alternatives=[
        "Gerçek bir 'bir ... dır' ilişkisinde ve üst sınıfın tüm arayüzü uygunsa kalıtım kullan.",
        "Parçayı hem sahiplenen hem de dışarıdan değiştirmek istiyorsan nesneyi __init__ parametresi olarak al.",
    ],
    traps=[
        "Sadece list ya da dict'in metotlarını kullanmak için onlardan türemek (class Stack(list)); istenmeyen metotlar da arayüze girer.",
        "Her ilişkiyi kalıtımla kurmak; 'bir mi, sahip mi?' sorusunu sormamak.",
        "Devredilen nesne None olabiliyorsa onu denetlemeyi unutup AttributeError almak.",
        "Delegation için gereksiz metotlar yazıp iç nesnenin bütün arayüzünü kopyalamak.",
    ],
    realCode=r'''
class Stack:
    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.append(item)

    def pop(self):
        if not self._items:
            raise IndexError("yığın boş")
        return self._items.pop()

    def size(self):
        return len(self._items)

stack = Stack()
stack.push(1)
stack.push(2)
print(stack.pop(), stack.size())
print(hasattr(stack, "insert"))
try:
    Stack().pop()
except IndexError as error:
    print(error)
''',
    realOutput=r'''
2 1
False
yığın boş
''',
    lineByLine=[
        "Stack bir listeye sahiptir ama list'ten türemez; iç liste _items özniteliğinde saklanır.",
        "Yalnızca push, pop ve size açıktır: yığının kuralı (son giren ilk çıkar) bozulamaz.",
        "hasattr(stack, 'insert') False verir; class Stack(list) olsaydı True verecekti.",
        "Boş yığında pop, açık bir hata mesajıyla reddedilir.",
    ],
    sources=[
        {"title": "Python 3.12 · Sınıflar (kalıtım ve alternatifler)", "url": TUTORIAL + "#inheritance"},
    ],
)
