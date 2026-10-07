"""One-off fix (7 Ekim 2026): early modules must not show constructs the learner has not met yet.

Learner feedback: seeing type(x).__name__ in the first lessons was confusing. A scan of M1–M5 found
__name__ (M1, M2, M4), import in M1, and def in 17 "gerçek kod" examples of M3–M5 although functions
are taught in M6. This script rewrites those spots in place (content/module-01..05.json); every
replacement must match exactly once. Kept on purpose: import copy in M5 deep-copy (the topic itself)
and key=lambda in M4 sorting-key (introduced there with a pointer to M6).
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2] / "content"


def c(text):
    return text.strip("\n")


def load(n):
    return json.loads((ROOT / f"module-{n:02d}.json").read_text(encoding="utf-8"))


def save(n, module):
    module["contentVersion"] += 1
    (ROOT / f"module-{n:02d}.json").write_text(json.dumps(module, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def section(module, sid):
    return next(s for s in module["sections"] if s["id"] == sid)


def question(module, qid):
    return next(q for q in module["questions"] if q["id"] == qid)


def sub(obj, key, old, new):
    value = obj[key]
    assert value.count(old) == 1, (key, value.count(old), old[:60])
    obj[key] = value.replace(old, new)


def item(obj, key, old, new):
    """Replace one list element that equals old."""
    assert obj[key].count(old) == 1, (key, old[:60])
    obj[key][obj[key].index(old)] = new


def real(sec, code, output, lines):
    sec["realCode"], sec["realOutput"], sec["lineByLine"] = c(code), c(output), lines


# ------------------------------------------------------------------ M1
m = load(1)
s = section(m, "variables-types")
sub(s, "code", "print(type(user_count).__name__)", "print(type(user_count))")
sub(s, "expectedOutput", "int\nTrue", "<class 'int'>\nTrue")
sub(s, "explanation", "type(value) tip bilgisi verir; örnekteki .__name__ bu tipin yalnız adını gösterir, şimdilik bir tanılama kalıbı olarak oku.",
    "type(value) değerin tipini gösterir: çıktıdaki <class 'int'> 'bu değer int tipinde' demektir; class kelimesini şimdilik 'tip' diye oku (sınıfları M11'de göreceksin).")
sub(s, "why", "12 bir int nesnesidir.", "12 bir int nesnesidir; type() bunu <class 'int'> olarak gösterir.")

s = section(m, "conversion-input")
sub(s, "code", "print(type(next_age).__name__)", "print(type(next_age))")
sub(s, "expectedOutput", "22\nint", "22\n<class 'int'>")
sub(s, "realCode", "print(type(raw_limit).__name__)\nprint(type(limit).__name__)", "print(type(raw_limit))\nprint(type(limit))")
sub(s, "realOutput", "25\nstr\nint", "25\n<class 'str'>\n<class 'int'>")
item(s, "lineByLine", "İki tipin str ve int olduğu gösterilir.", "type() ham değerin str, dönüştürülmüş değerin int olduğunu gösterir.")

s = section(m, "float-precision")
s["code"] = c('''
result = 0.1 + 0.2
print(result)
print(result == 0.3)
print(abs(result - 0.3) < 0.000001)
print(round(result, 2))
''')
s["expectedOutput"] = "0.30000000000000004\nFalse\nTrue\n0.3"
s["explanation"] = (
    "float sayıları sınırlı sayıda ikilik basamakla temsil eder; bazı ondalık değerler bu sistemde ancak yaklaşık saklanabilir. 0.1 + 0.2 bu nedenle 0.30000000000000004 görünür ve 0.3 ile == karşılaştırması False verir. "
    "Bu her float karşılaştırmasının yanlış olduğu anlamına gelmez; örneğin tam temsil edilen 0.5 güvenlidir. Ancak hesaplanmış yaklaşık değerlerde eşitlik yerine farkın yeterince küçük olup olmadığını sor: abs(a - b) < 0.000001. abs() bir sayının mutlak değerini (işaretsiz büyüklüğünü) veren hazır bir fonksiyondur. "
    "round veya .2f gösterimi yalnızca sonucu yuvarlayarak gösterir; önceki hesap hatasını yok etmez. Para gibi kesin olması gereken tutarlarda en basit güvenli yol, tutarı kuruş cinsinden tam sayı olarak tutmaktır: tam sayılarda yuvarlama hatası olmaz. "
    "İleride hazır araçlarla tanışacaksın: math.isclose toleranslı karşılaştırmayı, decimal.Decimal ise kesin ondalık hesabı yapar (modülleri içe aktarmayı M9'da, standart kütüphaneyi M10'da göreceksin)."
)
s["why"] = "İlk satır yaklaşık temsil farkını, ikincisi bu yüzden == karşılaştırmasının False olduğunu gösterir. Fark çok küçük olduğu için toleranslı karşılaştırma True verir. round yalnızca gösterimi yuvarlar; result'ın kendisi değişmez."
s["alternatives"] = [
    "Ölçüm ve bilimsel hesaplarda ileride math.isclose kullanacaksın; aynı toleranslı karşılaştırmayı hazır sunar.",
    "Para ve kesin ondalık kuralları için kuruşla tam sayı hesap yap; ileride decimal.Decimal da bir seçenek olacak.",
]
s["traps"] = [
    "round() kullanımını her hassasiyet sorununa kalıcı çözüm sanmak.",
    "Hesaplanmış yaklaşık sonuçlarda tolerans gereksinimini unutmak.",
    "Para tutarlarını float olarak toplayıp karşılaştırmak; kuruş cinsinden tam sayı tut.",
]
s["objectives"] = [
    "Float değerlerinin yaklaşık saklandığını açıklar.",
    "Float değerleri toleransla karşılaştırır; kesin tutarları kuruş cinsinden tam sayıyla hesaplar.",
]
real(s, '''
price_kurus = 10
fee_kurus = 20
total_kurus = price_kurus + fee_kurus
print(total_kurus)
print(total_kurus == 30)
print(total_kurus / 100, "TL")
''', '''
30
True
0.3 TL
''', [
    "Tutarlar kuruş cinsinden tam sayı olarak tutulur: 0,10 TL yerine 10 kuruş.",
    "Tam sayı toplamında yuvarlama hatası olmaz; sonuç tam olarak 30'dur.",
    "Eşitlik karşılaştırması bu yüzden güvenle True verir.",
    "Lira değeri yalnızca gösterirken 100'e bölünerek üretilir.",
])
save(1, m)

# ------------------------------------------------------------------ M2
m = load(2)
s = section(m, "indexing")
sub(s, "code", "print(type(language[1]).__name__)", "print(type(language[1]))")
sub(s, "expectedOutput", "P\nn\nstr", "P\nn\n<class 'str'>")
s = section(m, "bytes-vs-str")
sub(s, "code", "print(type(data).__name__)", "print(type(data))")
sub(s, "expectedOutput", "65\nABC\nbytes", "65\nABC\n<class 'bytes'>")
save(2, m)

# ------------------------------------------------------------------ M3
m = load(3)
real(section(m, "if-elif-else"), '''
age = 15
if age < 0:
    status = "geçersiz"
elif age < 18:
    status = "reşit değil"
else:
    status = "yetişkin"
print(status)
''', "reşit değil", [
    "Yaş bir isme bağlanır; gerçek programda input() ile gelir.",
    "Önce geçersiz değer elenir; koşullar yukarıdan aşağı sırayla denenir.",
    "İlk doğru koşulun bloğu çalışır, kalanlar atlanır: 15 < 18 olduğu için 'reşit değil' seçilir.",
    "Sonuç tek bir değişkende toplanıp bir kez yazdırılır.",
])
real(section(m, "match-case"), '''
point = (0, 5)
match point:
    case (0, 0):
        label = "başlangıç"
    case (0, y):
        label = f"y ekseni, y={y}"
    case (x, y):
        label = f"nokta ({x}, {y})"
print(label)
''', "y ekseni, y=5", [
    "point iki elemanlı bir demettir (tuple; ayrıntısı M4'te).",
    "(0, 0) deseni yalnızca tam başlangıç noktasıyla eşleşir.",
    "(0, y) ilk eleman 0 ise eşleşir ve ikinci elemanı y adına bağlar.",
    "(0, 5) ikinci desenle eşleşir; y=5 metne yerleşir ve sonuç yazdırılır.",
])
real(section(m, "while"), '''
max_attempts = 3
attempt = 1
delay = 1
while attempt <= max_attempts:
    print(f"Deneme {attempt}: {delay} sn bekle")
    delay *= 2
    attempt += 1
''', '''
Deneme 1: 1 sn bekle
Deneme 2: 2 sn bekle
Deneme 3: 4 sn bekle
''', [
    "En çok deneme sayısı, sayaç ve ilk bekleme süresi hazırlanır.",
    "Koşul, deneme sayısı sınırı aşılana kadar doğru kalır.",
    "Her turda bekleme süresi ikiye katlanır (üstel geri çekilme).",
    "attempt += 1 olmasaydı döngü hiç bitmezdi.",
])
real(section(m, "for-range"), '''
text = "Python Programı"
count = 0
for char in text.lower():
    if char in "aeıioöuü":
        count += 1
print(count)
''', "4", [
    "Sayaç döngüden önce sıfırlanır.",
    "lower() büyük harfleri de saymak için metni küçültür; for her karakteri sırayla verir.",
    "in, karakterin ünlü harfler metninde olup olmadığını sınar.",
    "Döngü bitince toplam yazdırılır: o, o, a, ı.",
])
real(section(m, "break-continue-pass"), '''
lines = ["", "INFO başladı", "ERROR disk dolu", "ERROR ağ"]
first_error = None
for line in lines:
    if not line.strip():
        continue
    if line.startswith("ERROR"):
        first_error = line
        break
print(first_error)
''', "ERROR disk dolu", [
    "Satırlar köşeli parantezli bir listede durur (ayrıntısı M4'te); sonuç başlangıçta None'dır.",
    "Boş satırlar continue ile atlanır.",
    "ERROR ile başlayan ilk satır kaydedilir ve break döngüyü bitirir; sonraki hata satırına bakılmaz.",
    "Hiç hata satırı olmasaydı first_error None kalırdı.",
])
s = section(m, "loop-else")
real(s, '''
n = 15
if n < 2:
    print(n, "asal değil")
else:
    for divisor in range(2, n):
        if n % divisor == 0:
            print(n, "asal değil:", divisor, "ile bölünür")
            break
    else:
        print(n, "asal")
''', "15 asal değil: 3 ile bölünür", [
    "2'den küçük sayılar asal değildir; bu durum döngüden önce ayrılır.",
    "2'den n - 1'e kadar her bölen denenir.",
    "15'i 3 böldüğü için mesaj yazılır ve break döngüyü keser; döngünün else bloğu atlanır.",
    "n = 13 olsaydı hiç bölen bulunmaz, döngü normal biter ve else '13 asal' yazardı.",
])
item(s, "alternatives", "Ekibin çoğu bu yapıyı tanımıyorsa fonksiyon içinden erken return daha okunur olabilir.",
     "Ekibin çoğu bu yapıyı tanımıyorsa bayrak değişkeni daha okunur olabilir; fonksiyonları öğrenince (M6) erken return da bir seçenek olacak.")
item(s, "traps", "Döngüden return ile çıkıldığında da else'in çalışmadığını unutmak.",
     "break ile çıkıldığında else'in çalışmadığını unutmak (ileride fonksiyon içinden return ile çıkmak da aynı etkiyi yapar).")
real(section(m, "enumerate-zip"), '''
headers = ["ad", "şehir"]
values = ["Ada", "İzmir"]
for position, (header, value) in enumerate(zip(headers, values), start=1):
    print(f"{position}. {header} = {value}")
''', '''
1. ad = Ada
2. şehir = İzmir
''', [
    "Başlıklar ve değerler iki ayrı listede durur.",
    "zip her başlığı kendi değeriyle eşleştirir.",
    "enumerate bu ikililere 1'den başlayan sıra numarası ekler; (header, value) ikiliyi açar.",
    "Her satır numara, başlık ve değerle yazdırılır.",
])
real(section(m, "nested-loops"), '''
numbers = [3, 8, 5, 2]
target = 7
pair = None
for i in range(len(numbers)):
    for j in range(i + 1, len(numbers)):
        if pair is None and numbers[i] + numbers[j] == target:
            pair = (i, j)
print(pair)
''', "(2, 3)", [
    "Dış döngü her indeksi sırayla seçer.",
    "İç döngü i'den sonraki indekslerden başlar; aynı çift iki kez denenmez.",
    "Toplamı hedefe eşit ilk çift kaydedilir: 5 + 2 = 7. break yalnızca iç döngüyü bitireceği için ilk çift pair is None denetimiyle korunur.",
    "Hiç çift olmasaydı pair None kalırdı; bu yöntem yaklaşık n² karşılaştırma yapar.",
])
save(3, m)

# ------------------------------------------------------------------ M4
m = load(4)
real(section(m, "lists"), '''
events = ["giriş", "arama", "sepet", "ödeme"]
count = 2
latest = events[-count:] if count > 0 else []
print(latest)
print(events)
''', '''
['sepet', 'ödeme']
['giriş', 'arama', 'sepet', 'ödeme']
''', [
    "Olay listesi ve istenen öğe sayısı hazırlanır.",
    "count 0 olsaydı events[-0:] bütün listeyi verirdi; bu yüzden koşullu ifadeyle ayrıca ele alınır.",
    "Negatif başlangıçlı dilim son count öğeyi alır.",
    "Orijinal liste değişmez; dilim yeni bir liste üretir.",
])
real(section(m, "list-methods"), '''
line = "4 15 8"
numbers = []
for part in line.split():
    numbers.append(int(part))
print(numbers)
''', "[4, 15, 8]", [
    "Boş bir liste biriktirici olarak başlatılır.",
    "split metni boşluklardan parçalara ayırır.",
    "Her parça int'e çevrilip append ile sona eklenir.",
    "Bu kalıbın kısa yazımı list comprehension'dır; M5'te göreceksin.",
])
s = section(m, "tuples")
sub(s, "code", "print(type(single).__name__, type(not_tuple).__name__)", "print(type(single), type(not_tuple))")
sub(s, "expectedOutput", "7\ntuple int", "7\n<class 'tuple'> <class 'int'>")
sub(s, "explanation", "return a, b yazan bir fonksiyon aslında tek bir tuple döndürür; x, y = point ile parçalar isimlere açılır (unpacking; ayrıntısı M5'te).",
    "x, y = point ile parçalar isimlere açılır (unpacking; ayrıntısı M5'te). İleride (M6) bir fonksiyondan birden çok değer döndürürken de aslında tek bir tuple döndürülür.")
real(s, '''
values = [7, 2, 9, 4]
low = values[0]
high = values[0]
for value in values:
    if value < low:
        low = value
    if value > high:
        high = value
result = (low, high)
smallest, largest = result
print(smallest, largest)
''', "2 9", [
    "İlk eleman hem en küçük hem en büyük aday olarak alınır.",
    "Her değer iki adayla ayrı ayrı karşılaştırılır.",
    "İki sonuç tek bir tuple içinde paketlenir.",
    "Tuple iki isme açılır (unpacking); fonksiyonlar birden çok değeri de böyle döndürür (M6).",
])
real(section(m, "sets"), '''
log_lines = ["ada /home", "can /cart", "ada /pay"]
seen = set()
for line in log_lines:
    user = line.split()[0]
    seen.add(user)
print(len(seen))
''', "2", [
    "Boş küme set() ile oluşturulur.",
    "Her log satırının ilk kelimesi kullanıcı adıdır.",
    "add, aynı kullanıcı ikinci kez geldiğinde hiçbir şey eklemez.",
    "Kümenin boyu farklı ziyaretçi sayısını verir.",
])
real(section(m, "dicts"), '''
DEFAULTS = {"theme": "light", "page_size": 20}
user_settings = {"theme": "dark"}
settings = DEFAULTS.copy()
settings.update(user_settings)
print(settings)
print(DEFAULTS)
''', '''
{'theme': 'dark', 'page_size': 20}
{'theme': 'light', 'page_size': 20}
''', [
    "Varsayılan ayarlar büyük harfli sabit bir sözlükte tutulur.",
    "copy() varsayılanlar değişmesin diye ayrı bir sözlük üretir.",
    "update, kullanıcının verdiği anahtarları üzerine yazar; vermediği page_size varsayılanda kalır.",
    "DEFAULTS değişmeden kalır; copy() olmasaydı update onu da değiştirirdi.",
])
real(section(m, "dict-iteration"), '''
orders = {"A1": "kargoda", "A2": "hazır", "A3": "kargoda"}
groups = {}
for order_id, status in orders.items():
    groups.setdefault(status, []).append(order_id)
print(groups)
''', "{'kargoda': ['A1', 'A3'], 'hazır': ['A2']}", [
    "Sipariş kimliğinden duruma giden bir sözlük hazırlanır.",
    "items() her siparişin kimliğini ve durumunu birlikte verir.",
    "setdefault, durum ilk kez görülüyorsa boş liste ekler ve o listeyi döndürür; append kimliği ekler.",
    "Sonuç, durumdan sipariş listesine bir gruplamadır.",
])
q = question(m, "m4-q06")
sub(q, "code", "print(type(x).__name__, len(y))", "print(type(x), len(y))")
q["expectedOutput"] = "<class 'int'> 1"
q["options"] = ["<class 'int'> 1", "<class 'tuple'> 1", "<class 'int'> 7", "<class 'tuple'> 7"]
q["answer"] = "<class 'int'> 1"
save(4, m)

# ------------------------------------------------------------------ M5
m = load(5)
real(section(m, "identity-equality"), '''
config = {"debug": None, "port": 8000}
MISSING = object()
for key in ("debug", "port", "host"):
    value = config.get(key, MISSING)
    if value is MISSING:
        print(key, "eksik")
    else:
        print(key, "=", value)
''', '''
debug = None
port = 8000
host eksik
''', [
    "object() benzersiz bir işaretçi nesne üretir; None geçerli bir ayar değeri olabileceği için eksikliği None ile anlatamayız.",
    "get, anahtar yoksa ikinci argümanı, yani işaretçinin kendisini döndürür.",
    "is değeri değil o tek nesneyi arar; debug'ın değeri None olsa bile eksik sayılmaz.",
    "Yalnızca gerçekten bulunmayan host eksik olarak raporlanır.",
])
s = section(m, "mutable-immutable")
real(s, '''
cart = [10.0, 25.0]
prices = cart
for i in range(len(prices)):
    prices[i] = round(prices[i] * 1.2, 2)
print(cart)
''', "[12.0, 30.0]", [
    "prices = cart yeni bir liste üretmez; aynı listeye ikinci bir ad bağlar.",
    "Her indeksteki öğe yerinde güncellenir.",
    "Değişiklik prices üzerinden yapıldı ama liste tek olduğu için cart da değişti.",
    "Yan etki istenmiyorsa önce kopya alınmalı: prices = cart.copy(). M6'da bir fonksiyona liste verdiğinde de aynı durum oluşacak.",
])
sub(s, "explanation", "Fonksiyona bir liste verdiğinde fonksiyon aynı nesneyi alır: içeride append yapılırsa çağıran taraf da değişikliği görür, ama parametreye yeni bir liste atanırsa dışarısı etkilenmez.",
    "Aynı durum M6'da fonksiyonlarda da karşına çıkacak: bir fonksiyona liste verdiğinde fonksiyon kopyayı değil listenin kendisini alır.")
item(s, "objectives", "Fonksiyona verilen bir listenin fonksiyon içinde değiştirilebildiğini açıklar.",
     "Aynı listeye bağlı iki addan birinde yapılan yerinde değişikliğin ötekinde de göründüğünü açıklar.")
s = section(m, "deep-copy")
sub(s, "explanation", "import copy ile gelen deepcopy,",
    "import copy satırı Python'la gelen hazır copy aracını kullanıma açar (içe aktarmayı M9'da ayrıntılı göreceksin); bu araçtaki deepcopy,")
real(s, '''
import copy

DEFAULT_STATE = {"level": 1, "inventory": ["kılıç"]}
player1 = copy.deepcopy(DEFAULT_STATE)
player2 = copy.deepcopy(DEFAULT_STATE)
player1["inventory"].append("kalkan")
print(player1["inventory"], player2["inventory"], DEFAULT_STATE["inventory"])
''', "['kılıç', 'kalkan'] ['kılıç'] ['kılıç']", [
    "Başlangıç durumu iç içe bir sözlükte tutulur.",
    "Her oyuncu deepcopy ile bağımsız bir durum alır; iç liste de kopyalanır.",
    "Birinci oyuncunun envanterine ekleme yalnızca onun listesini değiştirir.",
    "İkinci oyuncu ve varsayılan durum etkilenmez; copy() kullanılsaydı envanter listesi ortak olurdu.",
])
q = question(m, "m5-q18")
q["prompt"] = "Yazar new_cart'a eklemenin my_cart'ı değiştirmeyeceğini düşündü ama ['ekmek', 'süt'] yazdırıldı. Neden?"
q["code"] = c('''
my_cart = ["ekmek"]
new_cart = my_cart
new_cart.append("süt")
print(my_cart)
''')
q["options"] = [
    "new_cart = my_cart yeni liste üretmez; iki ad aynı listeye bağlı ve append onu yerinde değiştirir",
    "append her zaman programdaki bütün listeleri değiştirir",
    "print yanlış listeyi gösterir",
    "Atama listeyi kopyalar ama append kopyayı orijinale geri yazar",
]
q["answer"] = q["options"][0]
q["optionFeedback"] = {
    "append her zaman programdaki bütün listeleri değiştirir": "append yalnızca çağrıldığı listeyi değiştirir; burada o liste my_cart'ın kendisi.",
    "print yanlış listeyi gösterir": "print doğru listeyi gösteriyor; liste gerçekten değişti.",
    "Atama listeyi kopyalar ama append kopyayı orijinale geri yazar": "Atama hiç kopya üretmez; tek bir liste var.",
}
q["hints"] = ["new_cart = my_cart satırı kaç liste oluşturur?", "Bağımsız bir liste için new_cart = my_cart.copy() ya da my_cart + ['süt'] kullan."]
q["explanation"] = "Atama listeyi kopyalamaz; new_cart ve my_cart aynı listeye bağlı iki addır. append bu tek listeyi değiştirir. Bağımsız sonuç için new_cart = my_cart.copy() ya da new_cart = my_cart + ['süt'] yazılmalıydı. M6'da bir fonksiyona liste verdiğinde de aynı şey olur."
save(5, m)
print("M1–M5 düzeltildi")
