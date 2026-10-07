"""M13 (İleri yapılar) writing tasks. Imported by build_m13.py."""

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
lines = [input() for _ in range(int(input()))]
min_age, limit = map(int, input().split())
first = islice(adults(parse(lines), min_age), limit)
print("ilk:", ", ".join(record["ad"] for record in first) or "yok")
print("toplam:", sum(1 for _ in adults(parse(lines), min_age)))
print("tembel:", type(parse(lines)).__name__)
'''

task(
    id="m13-w1", moduleId=13, sectionId="generator-pipelines",
    title="Kayıtları tembel süz", level="Tamamla",
    objective="İki generator'ı tamamlayıp birbirine bağla; sonucu islice ile sınırla ve boru hattını gerektiğinde yeniden kur.",
    prompt="Girdide 'ad,şehir,yaş' satırları var. parse(lines) generator'ını tamamla: alanların uç boşluklarını temizlesin; alan sayısı 3 değilse ya da yaş yalnızca rakamlardan oluşmuyorsa satırı atlasın; geçerli satırlar için {'ad': ..., 'şehir': ..., 'yaş': int} sözlüğü üretsin. adults(records, min_age) yaşı min_age veya üstü olan kayıtları üretsin. İkisi de generator olmalı (program bunu denetler). Program ilk 'limit' yetişkinin adını, toplam yetişkin sayısını ve parse'ın türünü yazar.",
    starterCode=r'''
from itertools import islice

def parse(lines):
    # Alanları temizle; alan sayısı 3 değilse ya da yaş rakam değilse satırı atla.
    # Geçerli satır için {"ad": ..., "şehir": ..., "yaş": int} yield et.
    return []

def adults(records, min_age):
    # yaşı min_age veya üstü olan kayıtları yield et
    return []
''' + W1_PROGRAM,
    exampleInput="4\nAda,İzmir,30\nCan,Ankara,17\nbozuk satır\nEda,Bursa,45\n18 5",
    exampleOutput="ilk: Ada, Eda\ntoplam: 2\ntembel: generator",
    hints=[
        "parse içinde for line in lines döngüsü kur; parts = [p.strip() for p in line.split(',')] ile alanları al ve geçersizse continue yaz.",
        "Geçerli satırda yield {'ad': parts[0], 'şehir': parts[1], 'yaş': int(parts[2])}. adults için: for record in records: if record['yaş'] >= min_age: yield record.",
    ],
    solution=r'''
from itertools import islice

def parse(lines):
    for line in lines:
        parts = [part.strip() for part in line.split(",")]
        if len(parts) != 3 or not parts[2].isdigit():
            continue
        yield {"ad": parts[0], "şehir": parts[1], "yaş": int(parts[2])}

def adults(records, min_age):
    for record in records:
        if record["yaş"] >= min_age:
            yield record
''' + W1_PROGRAM,
    tests=[
        {"label": "Örnek", "stdin": "4\nAda,İzmir,30\nCan,Ankara,17\nbozuk satır\nEda,Bursa,45\n18 5", "expectedOutput": "ilk: Ada, Eda\ntoplam: 2\ntembel: generator"},
        {"label": "Sınır islice ile", "stdin": "3\nA,x,20\nB,y,21\nC,z,22\n18 2", "expectedOutput": "ilk: A, B\ntoplam: 3\ntembel: generator"},
        {"label": "Geçersiz yaş", "stdin": "2\nA,x,abc\nB,y,-5\n18 3", "expectedOutput": "ilk: yok\ntoplam: 0\ntembel: generator"},
        {"label": "Boşluklar ve sınır yaşı", "stdin": "2\n Ada , İzmir , 30 \nBo,Van,18\n18 1", "expectedOutput": "ilk: Ada\ntoplam: 2\ntembel: generator"},
    ],
)

task(
    id="m13-w2", moduleId=13, sectionId="decorators",
    title="Önbellek decorator'ını düzelt", level="Düzelt",
    objective="Her çağrıda sıfırlanan önbelleği, kaybolan dönüş değerini ve kaybolan fonksiyon adını bul ve düzelt.",
    prompt="memo decorator'ı bir fonksiyonun sonuçlarını önbelleğe almalı: aynı argümanla ikinci çağrıda fonksiyonu yeniden çalıştırmadan önceki sonucu döndürmeli ve fonksiyonun adını korumalı. Program sayıları okur, slow_square'i her biri için çağırır, sonuçları, gerçek hesaplama sayısını ve fonksiyonun adını yazar. Kodda üç hata var: önbellek her çağrıda sıfırlanıyor; sarmalayıcı sonucu döndürmüyor; fonksiyonun adı kayboluyor. Üçünü de düzelt.",
    starterCode=r'''
from functools import wraps

calls = 0

def memo(func):
    def wrapper(n):
        cache = {}
        if n not in cache:
            cache[n] = func(n)
        cache[n]
    return wrapper

@memo
def slow_square(n):
    global calls
    calls += 1
    return n * n

numbers = [int(x) for x in input().split()]
print([slow_square(n) for n in numbers])
print("hesaplama:", calls)
print("ad:", slow_square.__name__)
''',
    exampleInput="3 4 3",
    exampleOutput="[9, 16, 9]\nhesaplama: 2\nad: slow_square",
    hints=[
        "cache her çağrıda yeniden mi oluşuyor? Sarmalayıcının son satırı bir değer döndürüyor mu? wraps içe aktarılmış ama kullanılmıyor.",
        "cache = {} satırını wrapper'ın dışına (memo'nun içine) taşı; son satıra return yaz; wrapper'ın üstüne @wraps(func) ekle.",
    ],
    solution=r'''
from functools import wraps

calls = 0

def memo(func):
    cache = {}
    @wraps(func)
    def wrapper(n):
        if n not in cache:
            cache[n] = func(n)
        return cache[n]
    return wrapper

@memo
def slow_square(n):
    global calls
    calls += 1
    return n * n

numbers = [int(x) for x in input().split()]
print([slow_square(n) for n in numbers])
print("hesaplama:", calls)
print("ad:", slow_square.__name__)
''',
    tests=[
        {"label": "Örnek", "stdin": "3 4 3", "expectedOutput": "[9, 16, 9]\nhesaplama: 2\nad: slow_square"},
        {"label": "Tek sayı", "stdin": "5", "expectedOutput": "[25]\nhesaplama: 1\nad: slow_square"},
        {"label": "Hep aynı", "stdin": "2 2 2 2", "expectedOutput": "[4, 4, 4, 4]\nhesaplama: 1\nad: slow_square"},
        {"label": "İşaretleri farklı", "stdin": "7 -7", "expectedOutput": "[49, 49]\nhesaplama: 2\nad: slow_square"},
    ],
)

W3_PROGRAM = r'''
store = {}
for pair in input().split():
    key, value = pair.split("=")
    store[key] = int(value)
for _ in range(int(input())):
    batch = input().split(";")
    try:
        with transaction(store):
            for op in batch:
                apply(store, op)
        print(f"uygulandı: {len(batch)} işlem")
    except ValueError as error:
        print(f"geri alındı: {error}")
print(sorted(store.items()))
'''

task(
    id="m13-w3", moduleId=13, sectionId="contextlib",
    title="Geri alınabilir toplu güncelleme", level="Sıfırdan yaz",
    objective="Bir context manager ile 'ya hepsi ya hiçbiri' kuralı kur: toplu işlemlerden biri başarısız olursa sözlüğü önceki hâline geri döndür.",
    prompt="transaction(store) context manager'ını (sınıf ya da @contextmanager) ve apply(store, op) fonksiyonunu yaz. İlk satır başlangıç değerleri ('a=1 b=2', boş olabilir), ikinci satır toplu işlem sayısı, sonraki her satır ';' ile ayrılmış işlemlerdir. İşlemler: 'k=5' (k'yi tam sayı 5 yap), 'k+=3' (k'yi 3 artır; k yoksa ValueError(f'olmayan anahtar: {k}')), '-k' (k'yi sil; yoksa aynı hata). Değer tam sayı değilse ValueError(f'geçersiz değer: {op}'); bu biçimlerin hiçbirine uymayan işlem ValueError(f'geçersiz işlem: {op}'). transaction, bloğa girerken sözlüğün kopyasını alır; blokta hata olursa sözlüğü yerinde (aynı nesneyi) eski hâline döndürür ve hatayı yutmaz. Program her toplu işlem için 'uygulandı: N işlem' ya da 'geri alındı: mesaj', sonda sıralı sözlüğü yazar. Okuma kısmı hazır; fonksiyonları üstüne yaz.",
    starterCode=r'''
# transaction(store) context manager'ını ve apply(store, op) fonksiyonunu buraya yaz.

''' + W3_PROGRAM,
    exampleInput="a=1 b=2\n3\na=5;b+=3\nc=1;-z\n-a;b=x",
    exampleOutput="uygulandı: 2 işlem\ngeri alındı: olmayan anahtar: z\ngeri alındı: geçersiz değer: b=x\n[('a', 5), ('b', 5)]",
    hints=[
        "İşlem türünü sırayla denetle: '-' ile başlıyorsa silme, '+=' içeriyorsa artırma, '=' içeriyorsa atama, değilse geçersiz işlem. int dönüşümünü try/except ValueError ile sarıp kendi mesajınla yeniden fırlat.",
        "@contextmanager ile: snapshot = dict(store); try: yield; except Exception: store.clear(); store.update(snapshot); raise. store = snapshot yazma; program aynı sözlük nesnesini kullanıyor.",
    ],
    solution=r'''
from contextlib import contextmanager

@contextmanager
def transaction(store):
    snapshot = dict(store)
    try:
        yield store
    except Exception:
        store.clear()
        store.update(snapshot)
        raise

def to_int(text, op):
    try:
        return int(text)
    except ValueError:
        raise ValueError(f"geçersiz değer: {op}") from None

def apply(store, op):
    if op.startswith("-"):
        key = op[1:]
        if key not in store:
            raise ValueError(f"olmayan anahtar: {key}")
        del store[key]
    elif "+=" in op:
        key, value = op.split("+=", 1)
        if key not in store:
            raise ValueError(f"olmayan anahtar: {key}")
        store[key] += to_int(value, op)
    elif "=" in op:
        key, value = op.split("=", 1)
        store[key] = to_int(value, op)
    else:
        raise ValueError(f"geçersiz işlem: {op}")
''' + W3_PROGRAM,
    tests=[
        {"label": "Örnek", "stdin": "a=1 b=2\n3\na=5;b+=3\nc=1;-z\n-a;b=x", "expectedOutput": "uygulandı: 2 işlem\ngeri alındı: olmayan anahtar: z\ngeri alındı: geçersiz değer: b=x\n[('a', 5), ('b', 5)]"},
        {"label": "Boş başlangıç", "stdin": "\n1\nx=1", "expectedOutput": "uygulandı: 1 işlem\n[('x', 1)]"},
        {"label": "Artırma ve olmayan anahtar", "stdin": "n=1\n2\nn+=2;n+=3\nm+=1", "expectedOutput": "uygulandı: 2 işlem\ngeri alındı: olmayan anahtar: m\n[('n', 6)]"},
        {"label": "Sil ve yeniden kur", "stdin": "a=1\n1\n-a;a=2", "expectedOutput": "uygulandı: 2 işlem\n[('a', 2)]"},
        {"label": "Geçersiz işlemler geri alınır", "stdin": "x=1\n2\nx=9;x+=a\nx=7;?", "expectedOutput": "geri alındı: geçersiz değer: x+=a\ngeri alındı: geçersiz işlem: ?\n[('x', 1)]"},
    ],
)
