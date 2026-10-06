"""Builds Atölye 2 (after M6) and Atölye 3 (after M8).

Writes the workshop tasks into content/workshop-tasks.json and the workshop definitions into
content/milestones.json. Expected outputs are produced by running each reference solution, so a
test can never disagree with its own solution; read the printed outputs to check they also match
the contract in the prompt. Atölye 1 and the exams are left untouched.
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2] / "content"


def run(code, stdin=""):
    # A scratch folder per run: the solutions write files (satis.csv, rapor.json) into their working directory.
    with tempfile.TemporaryDirectory() as scratch:
        result = subprocess.run([sys.executable, "-X", "utf8", "-c", code], input=stdin.encode("utf-8"), capture_output=True, cwd=scratch)
    if result.returncode != 0:
        raise SystemExit(result.stderr.decode("utf-8", "replace"))
    return result.stdout.decode("utf-8").replace("\r\n", "\n").rstrip("\n")


def c(text):
    return text.strip("\n")


tasks = []


def task(id, moduleId, sectionId, title, level, objective, prompt, starterCode, solution, hints, tests):
    solution, starterCode = c(solution), c(starterCode)
    built = [{"label": label, "stdin": stdin, "expectedOutput": run(solution, stdin)} for label, stdin in tests]
    tasks.append({
        "id": id, "moduleId": moduleId, "sectionId": sectionId, "title": title, "level": level,
        "objective": objective, "prompt": prompt, "starterCode": starterCode,
        "exampleInput": built[0]["stdin"], "exampleOutput": built[0]["expectedOutput"],
        "hints": hints, "solution": solution, "tests": built,
    })
    print(f"\n== {id} ({len(built)} test)")
    for item in built:
        print(f"  [{item['label']}] girdi={item['stdin']!r}\n      çıktı={item['expectedOutput']!r}")


# ---------------------------------------------------------------- Atölye 2 (M6 sonrası)
READ2 = c(r'''
def clean_names(names, seen=[]):
    for name in names:
        cleaned = " ".join(name.split()).title()
        if cleaned not in seen:
            seen.append(cleaned)
    return seen

first = clean_names(["  ada  lovelace ", "ADA LOVELACE"])
second = clean_names(["can"])
print(first, second)
''')

task(
    "workshop2-fix", 6, "mutable-default", "AI'ın isim temizleyicisini onar", "Düzelt",
    "Paylaşılan varsayılan değeri, boş adları ve kaybolan sırayı bul ve düzelt.",
    "Girdi: ilk satır A grubundaki isim sayısı, ardından o kadar isim satırı; sonra aynı düzende B grubu. clean_names(names) bir grubu temizler: uçlardaki ve kelimeler arasındaki fazla boşluklar tek boşluğa iner, her kelimenin yalnız ilk harfi büyük olur, boş kalan adlar atılır, tekrar eden adlar yalnız ilk görüldükleri yerde kalır ve sıra korunur. Fonksiyon her çağrıda yeni bir liste döndürür. Program iki grubu ayrı satırlarda yazdırır. Başlangıç kodunda üç sorun var: çağrılar arasında veri sızıyor, boş adlar listeye giriyor ve sıra bozuluyor.",
    r'''
def clean_names(names, seen=[]):
    for name in names:
        cleaned = " ".join(name.split()).title()
        if cleaned not in seen:
            seen.append(cleaned)
    return sorted(seen)

count_a = int(input())
group_a = [input() for _ in range(count_a)]
count_b = int(input())
group_b = [input() for _ in range(count_b)]
print(clean_names(group_a))
print(clean_names(group_b))
''',
    r'''
def clean_names(names):
    result = []
    for name in names:
        cleaned = " ".join(name.split()).title()
        if cleaned and cleaned not in result:
            result.append(cleaned)
    return result

count_a = int(input())
group_a = [input() for _ in range(count_a)]
count_b = int(input())
group_b = [input() for _ in range(count_b)]
print(clean_names(group_a))
print(clean_names(group_b))
''',
    [
        "Varsayılan değer olan seen=[] fonksiyon tanımlanırken bir kez oluşturulur; bu yüzden ikinci grup birincinin adlarını da görür. Listeyi fonksiyonun içinde, her çağrıda yeniden kur.",
        "Boş kalan adı eklemeden önce kontrol et (if cleaned and ...). sorted() ilk görülme sırasını bozar; kaldır.",
    ],
    [
        ("Örnek", "3\n  ada  lovelace \nADA LOVELACE\ncan\n1\nzeynep"),
        ("Gruplar birbirine karışmaz", "1\nali\n1\nveli"),
        ("Boş adlar atılır", "3\n   \nali\n  \n1\n  "),
        ("Sıra korunur", "3\nzeynep\nali\nveli\n0"),
        ("Aynı ad iki grupta", "2\nali\nali\n2\nali\nveli"),
    ],
)

SLUG_HELPERS = r'''
TURKISH = str.maketrans("çğıöşüÇĞİÖŞÜI", "cgiosucgiosui")

def words(text):
    parts, word = [], ""
    for char in text:
        if char.isascii() and char.isalnum():
            word += char
        elif word:
            parts.append(word)
            word = ""
    if word:
        parts.append(word)
    return parts
'''

task(
    "workshop2-build", 6, "def-return", "Başlıktan bağlantı adı (slug) üret", "Sıfırdan yaz",
    "Sözleşmesi verilen bir metin temizleme fonksiyonunu eksiksiz yaz.",
    "make_slug(title) bir başlığı adres parçasına çevirir. Sözleşme: (1) Türkçe harfler ASCII karşılığına çevrilir (ç→c, ğ→g, ı→i, ö→o, ş→s, ü→u; büyük harfler dahil, İ ve I da i olur). (2) Harfler küçük yazılır. (3) ASCII harf ve rakam dışındaki her karakter ayırıcıdır; art arda gelen ayırıcılar tek \"-\" olur. (4) Baştaki ve sondaki \"-\" bulunmaz. (5) Hiç harf ya da rakam kalmazsa sonuç \"bos\" olur. Program ilk satırda başlık sayısını, sonra her satırda bir başlık okur ve her başlığın adresini ayrı satırda yazdırır. İpucu: İ harfine lower() uygulanırsa iki karakter olur; çeviriyi küçültmeden önce yap.",
    r'''
# make_slug(title) fonksiyonunu sözleşmeye göre yaz.

count = int(input())
for _ in range(count):
    print(make_slug(input()))
''',
    SLUG_HELPERS + r'''
def make_slug(title):
    return "-".join(words(title.translate(TURKISH).lower())) or "bos"

count = int(input())
for _ in range(count):
    print(make_slug(input()))
''',
    [
        "Önce Türkçe harfleri çevir (str.maketrans ile translate), sonra lower() uygula; ters sırada İ iki karakter olur.",
        "Her karakteri gez: harf/rakamsa kelimeye ekle, değilse kelimeyi bitir. Kelimeleri \"-\".join ile birleştir; boş liste \"bos\" olmalı (or ile).",
    ],
    [
        ("Örnek", "3\nMerhaba Dünya!\nÇığ Şöleni İçin Öğütler\nPython 3.12 Sürümü"),
        ("Büyük İ ve I", "2\nİstanbul Işık\nIĞDIR"),
        ("Ayırıcılar", "3\n  a -- b  \n---x---\nbir_iki+üç"),
        ("Boş sonuç", "3\n!!!\n   \nçç"),
        ("ASCII dışı karakter ve rakam", "2\nCafé 24\n2026-10-06"),
        ("Tek harf", "1\nZ"),
    ],
)

TESTS_IMPLS = SLUG_HELPERS + r'''
def slug_ok(title):
    return "-".join(words(title.translate(TURKISH).lower())) or "bos"

def slug_hata1(title):
    return "-".join(words(title.lower())) or "bos"

def slug_hata2(title):
    out = ""
    for char in title.translate(TURKISH).lower():
        if char.isascii() and char.isalnum():
            out += char
        elif not out.endswith("-"):
            out += "-"
    return out or "bos"

def slug_hata3(title):
    out = ""
    for char in title.translate(TURKISH).lower():
        out += char if char.isascii() and char.isalnum() else "-"
    return out.strip("-") or "bos"

def slug_hata4(title):
    return "-".join(words(title.translate(TURKISH).lower()))

def slug_hata5(title):
    return "-".join(words(title.lower().translate(TURKISH))) or "bos"

IMPLS = {"dogru": slug_ok, "hata1": slug_hata1, "hata2": slug_hata2, "hata3": slug_hata3, "hata4": slug_hata4, "hata5": slug_hata5}
'''

task(
    "workshop2-tests", 6, "lambda-higher-order", "Hataları yakalayan testleri kur", "Sıfırdan yaz",
    "Bir fonksiyonun doğru ve hatalı sürümlerini ayırt eden test vakaları tasarla.",
    "Yukarıdaki make_slug sözleşmesini bir de test tarafından gör. IMPLS sözlüğünde bir doğru (dogru) ve beş hatalı sürüm var; hatalar sırayla: Türkçe harfler çevrilmiyor, uçlarda tire kalıyor, art arda ayırıcılar tek tire olmuyor, boş sonuç \"bos\" olmuyor, büyük İ yanlış çevriliyor. Sen cases listesine (girdi, beklenen çıktı) çiftleri yaz ve passes(implementation) fonksiyonunu tamamla: bir sürümde tüm vakalar geçiyorsa True döndürsün. Doğru sürümde bütün vakalar geçmeli; her hatalı sürümde en az bir vaka başarısız olmalı. Program bir satırda boşlukla ayrılmış sürüm adlarını okur ve her ad için \"ad: GEÇTİ\" ya da \"ad: YAKALANDI\" yazdırır.",
    TESTS_IMPLS + r'''
cases = [
    # ("Merhaba Dünya", "merhaba-dunya"),
]

def passes(implementation):
    # her vakayı çalıştır; hepsi geçerse True döndür
    pass

for name in input().split():
    print(f"{name}: {'GEÇTİ' if passes(IMPLS[name]) else 'YAKALANDI'}")
''',
    TESTS_IMPLS + r'''
cases = [
    ("Merhaba Dünya!", "merhaba-dunya"),
    ("İstanbul", "istanbul"),
    ("Işık", "isik"),
    ("  a -- b  ", "a-b"),
    ("a -- b", "a-b"),
    ("!!!", "bos"),
]

def passes(implementation):
    return all(implementation(title) == expected for title, expected in cases)

for name in input().split():
    print(f"{name}: {'GEÇTİ' if passes(IMPLS[name]) else 'YAKALANDI'}")
''',
    [
        "cases bir liste; her öğe (girdi, beklenen) çifti. passes içinde for döngüsüyle ya da all(...) ile her vakayı implementation(girdi) == beklenen diye karşılaştır.",
        "Her hata için o hatayı tetikleyen bir girdi düşün: Türkçe harf (Dünya), büyük İ, baştaki/sondaki ayırıcı, art arda ayırıcı, hiç harf içermeyen girdi.",
    ],
    [
        ("Doğru sürüm", "dogru"),
        ("Türkçe harf hatası", "hata1"),
        ("Uçtaki tire hatası", "hata2"),
        ("Art arda ayırıcı hatası", "hata3"),
        ("Boş sonuç hatası", "hata4"),
        ("Büyük İ hatası", "hata5"),
        ("Karışık sıra", "hata3 dogru hata5 hata1"),
    ],
)

# ---------------------------------------------------------------- Atölye 3 (M8 sonrası)
READ3 = c(r'''
import csv
from pathlib import Path

Path("satis.csv").write_text('urun,adet,fiyat\nkalem,3,150\n"defter, çizgili",2,900\nsilgi,x,50\nkalem,4,150\n', encoding="utf-8")

total = 0
bad = 0
with open("satis.csv", encoding="utf-8", newline="") as f:
    for row in csv.DictReader(f):
        try:
            total += int(row["adet"]) * int(row["fiyat"])
        except ValueError:
            bad += 1
print(total, bad)
''')

task(
    "workshop3-fix", 8, "csv", "Satış özetleyicisini onar", "Düzelt",
    "Tırnaklı alanı, hatalı satırı ve boş veriyi doğru işle.",
    "Girdi: ilk satır CSV satır sayısı, ardından başlık (urun,adet,fiyat) dahil o kadar CSV satırı. Program satırları satis.csv'ye yazar ve okur. Bir veri satırı geçerlidir: tam üç alanı varsa ve adet ile fiyat (uç boşlukları atıldıktan sonra) yalnız rakamlardan oluşuyorsa. Çıktı tek satır: \"satır: <geçerli>, hatalı: <geçersiz>, toplam: <adet*fiyat toplamı>, ortalama: <toplam / geçerli satır, bir ondalık>\"; geçerli satır yoksa ortalama 0.0. Başlangıç kodunda üç sorun var: tırnak içindeki virgül alanı bölüyor, hatalı satır programı çökertiyor ve geçerli satır yokken sıfıra bölünüyor.",
    r'''
count = int(input())
lines = [input() for _ in range(count)]
with open("satis.csv", "w", encoding="utf-8", newline="") as f:
    f.write("\n".join(lines) + "\n")

valid = 0
bad = 0
total = 0
with open("satis.csv", encoding="utf-8") as f:
    next(f)
    for line in f:
        name, qty, price = line.rstrip("\n").split(",")
        total += int(qty) * int(price)
        valid += 1
print(f"satır: {valid}, hatalı: {bad}, toplam: {total}, ortalama: {total / valid:.1f}")
''',
    r'''
import csv

count = int(input())
lines = [input() for _ in range(count)]
with open("satis.csv", "w", encoding="utf-8", newline="") as f:
    f.write("\n".join(lines) + "\n")

valid = 0
bad = 0
total = 0
with open("satis.csv", encoding="utf-8", newline="") as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        if len(row) != 3 or not row[1].strip().isdigit() or not row[2].strip().isdigit():
            bad += 1
            continue
        total += int(row[1]) * int(row[2])
        valid += 1
average = total / valid if valid else 0.0
print(f"satır: {valid}, hatalı: {bad}, toplam: {total}, ortalama: {average:.1f}")
''',
    [
        "split(\",\") tırnakları tanımaz; satırları csv.reader ile oku (dosyayı newline=\"\" ile aç).",
        "Her satırı doğrula: len(row) == 3 ve adet/fiyat isdigit(). Geçersizse bad artır ve continue ile atla. Ortalamada valid sıfırsa 0.0 kullan.",
    ],
    [
        ("Örnek", '5\nurun,adet,fiyat\nkalem,3,150\n"defter, çizgili",2,900\nsilgi,x,50\nkalem,4,150'),
        ("Yalnız başlık", "1\nurun,adet,fiyat"),
        ("Hepsi hatalı", "3\nurun,adet,fiyat\nkalem,iki,150\nsilgi,3"),
        ("Tırnaklı ad ve boşluk", '3\nurun,adet,fiyat\n"kalem, mavi",2, 100 \n"defter ""A4""",1,500'),
        ("Eksik ve fazla alan", "4\nurun,adet,fiyat\nkalem,3\nkalem,3,150,ek\nsilgi,2,50"),
        ("Negatif sayı hatalıdır", "3\nurun,adet,fiyat\nkalem,-1,150\nsilgi,2,50"),
    ],
)

task(
    "workshop3-build", 8, "json", "CSV'den JSON satış raporu yaz", "Sıfırdan yaz",
    "Doğrulama, gruplama ve hata listesiyle gerçek bir CSV→JSON raporlayıcı yaz.",
    "Girdi: ilk satır CSV satır sayısı, ardından başlık (urun,adet,fiyat) dahil o kadar CSV satırı. Satırları satis.csv'ye yaz, csv modülüyle oku ve rapor.json'a json.dump ile (ensure_ascii=False, sort_keys=True) şu raporu yaz: {\"hatalar\": [...], \"toplam\": ..., \"urunler\": {...}}. Her kayıt sırayla denetlenir ve ilk bulunan neden kaydedilir: alan sayısı üç değilse \"alan eksik\", adet yalnız rakamlardan oluşmuyorsa \"adet sayı değil\", fiyat yalnız rakamlardan oluşmuyorsa \"fiyat sayı değil\" (adet ve fiyat uç boşlukları atılarak denetlenir). Hatalı kayıt {\"neden\": ..., \"satir\": <dosyadaki satır numarası; başlık 1. satırdır>} olarak hatalar listesine sırayla eklenir. Geçerli kayıtlar ürün adına (uç boşlukları atılmış) göre gruplanır: urunler[ad] = {\"adet\": toplam adet, \"tutar\": toplam adet*fiyat}; toplam tüm geçerli tutarların toplamıdır. Yalnız başlık varsa rapor boş olur. Son olarak rapor.json'u okuyup içeriğini olduğu gibi yazdır.",
    r'''
# 1) satırları satis.csv'ye yaz
# 2) csv ile oku, her kaydı doğrula ve grupla
# 3) raporu rapor.json'a yaz, sonra dosyayı okuyup yazdır
''',
    r'''
import csv
import json

count = int(input())
lines = [input() for _ in range(count)]
with open("satis.csv", "w", encoding="utf-8", newline="") as f:
    f.write("\n".join(lines) + "\n")

def is_count(text):
    return text.strip().isdigit()

report = {"hatalar": [], "toplam": 0, "urunler": {}}
with open("satis.csv", encoding="utf-8", newline="") as f:
    reader = csv.reader(f)
    next(reader)
    for number, row in enumerate(reader, start=2):
        if len(row) != 3:
            reason = "alan eksik"
        elif not is_count(row[1]):
            reason = "adet sayı değil"
        elif not is_count(row[2]):
            reason = "fiyat sayı değil"
        else:
            reason = None
        if reason:
            report["hatalar"].append({"satir": number, "neden": reason})
            continue
        quantity, amount = int(row[1]), int(row[1]) * int(row[2])
        item = report["urunler"].setdefault(row[0].strip(), {"adet": 0, "tutar": 0})
        item["adet"] += quantity
        item["tutar"] += amount
        report["toplam"] += amount

with open("rapor.json", "w", encoding="utf-8") as f:
    json.dump(report, f, ensure_ascii=False, sort_keys=True)
with open("rapor.json", encoding="utf-8") as f:
    print(f.read())
''',
    [
        "csv.reader satırları listeler; ilk satırı next(reader) ile atla. Satır numarası için enumerate(reader, start=2) kullan.",
        "Önce neden belirle (if/elif zinciri), neden varsa hatalar listesine ekleyip continue yap. Gruplamak için urunler.setdefault(ad, {\"adet\": 0, \"tutar\": 0}) işini görür.",
    ],
    [
        ("Örnek", '4\nurun,adet,fiyat\nkalem,3,150\n"defter, çizgili",2,900\nsilgi,x,50'),
        ("Yalnız başlık", "1\nurun,adet,fiyat"),
        ("Aynı ürün birleşir", "4\nurun,adet,fiyat\nkalem,3,150\n kalem ,4,150\nsilgi,2,50"),
        ("Hata nedenleri ve satırları", "6\nurun,adet,fiyat\nkalem,iki,150\nsilgi,3\ndefter,2,x\nkalem,1,150\ncetvel,,10"),
        ("Hepsi hatalı", "3\nurun,adet,fiyat\nkalem,-1,150\nsilgi,2,5.5"),
        ("İkisi de hatalıysa ilk neden: adet", "3\nurun,adet,fiyat\nkalem,x,y\nsilgi,2,z"),
        ("Tırnaklı ve boşluklu", '3\nurun,adet,fiyat\n" kalem, mavi ", 2 , 100 \n"defter ""A4""",1,500'),
    ],
)

# ---------------------------------------------------------------- dosyalara yaz
tasks_path = ROOT / "workshop-tasks.json"
mine = {item["id"] for item in tasks}
existing = [item for item in json.loads(tasks_path.read_text(encoding="utf-8")) if item["id"] not in mine]
tasks_path.write_text(json.dumps(existing + tasks, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

milestones_path = ROOT / "milestones.json"
data = json.loads(milestones_path.read_text(encoding="utf-8"))
data["workshops"] = [item for item in data["workshops"] if item["id"] not in ("workshop2", "workshop3")]
read2_out, read3_out = run(READ2), run(READ3)
print("\nokuma çıktıları:", repr(read2_out), "|", repr(read3_out))
data["workshops"] += [
    {
        "id": "workshop2", "afterModule": 6, "title": "Atölye 2 · Metin temizleyicileri",
        "summary": "Önce yapay zekânın yazdığı bir temizleme fonksiyonunun neden beklenmedik sonuç verdiğini açıkla, sonra onu onar. Ardından sözleşmesi verilen yeni bir fonksiyonu sıfırdan yaz ve son adımda fonksiyonu bozan hataları yakalayan kendi testlerini kur.",
        "steps": [
            {"kind": "read", "label": "İncele", "progressKey": "workshop2-read",
             "heading": "İki çağrıdan sonra ekrana ne yazılır?", "code": READ2,
             "inputLabel": "Çıktı (iki liste)", "placeholder": "Örn. [1] [2]",
             "answer": read2_out, "expectedOutput": read2_out,
             "wrongHint": "Varsayılan değer olan seen=[] fonksiyon her çağrıldığında yeniden oluşmaz. İkinci çağrı hangi listeye ekleme yapıyor ve first hangi listeyi gösteriyor?",
             "explanation": "seen=[] varsayılanı fonksiyon tanımlanırken bir kez üretilir ve her çağrıda aynı liste kullanılır. İkinci çağrı aynı listeye Can'ı ekler; return aynı nesneyi döndürdüğü için first ve second aynı listeyi gösterir ve ikisi de iki adlı listeyi yazdırır. Çözüm: seen=None ya da hiç parametre almamak ve listeyi fonksiyonun içinde kurmak.",
             "nextLabel": "Düzeltme adımına geç"},
            {"kind": "write", "label": "Düzelt", "taskId": "workshop2-fix",
             "note": "Kontrol listesi: her çağrı boş bir listeyle başlasın · boş adlar atılsın · ilk görülme sırası korunsun · aynı ad bir kez yer alsın.",
             "nextLabel": "Kendi fonksiyonunu yaz"},
            {"kind": "write", "label": "Sıfırdan yaz", "taskId": "workshop2-build",
             "note": "Sözleşmedeki her maddeyi ayrı bir örnekle düşün: Türkçe harf, büyük İ, art arda ayırıcı, baştaki/sondaki ayırıcı, boş sonuç.",
             "nextLabel": "Testlerini kur"},
            {"kind": "write", "label": "Testlerini kur", "taskId": "workshop2-tests"},
        ],
    },
    {
        "id": "workshop3", "afterModule": 8, "title": "Atölye 3 · Satış CSV'sini raporla",
        "summary": "Bir satış dosyasını okuyan kodun hangi satırı neden saydığını açıkla, sonra tırnaklı alan, hatalı satır ve boş dosya sorunlarını onar. Son adımda hata nedenlerini ve satır numaralarını da veren bir CSV→JSON raporlayıcıyı sıfırdan yaz.",
        "steps": [
            {"kind": "read", "label": "İncele", "progressKey": "workshop3-read",
             "heading": "Kod hangi satırları sayıyor?", "code": READ3,
             "inputLabel": "Çıktı (toplam ve hatalı sayısı)", "placeholder": "Örn. 100 2",
             "answer": read3_out, "expectedOutput": read3_out,
             "wrongHint": "csv modülü tırnak içindeki virgülü alan ayırıcı saymaz. Her satırı ayrı ayrı çarp; adedi sayı olmayan satır toplama girmez ve hatalı sayılır.",
             "explanation": "Üç geçerli satır var: kalem 3×150 = 450, tırnaklı \"defter, çizgili\" 2×900 = 1800 ve ikinci kalem 4×150 = 600; toplam 2850. Adedi x olan silgi satırında int() ValueError verir ve hatalı sayılır.",
             "nextLabel": "Düzeltme adımına geç"},
            {"kind": "write", "label": "Düzelt", "taskId": "workshop3-fix",
             "note": "Kontrol listesi: tırnaklı alan bölünmesin · hatalı satır programı durdurmasın · hiç geçerli satır yokken bölme hatası olmasın.",
             "nextLabel": "Kendi raporunu yaz"},
            {"kind": "write", "label": "Sıfırdan yaz", "taskId": "workshop3-build",
             "note": "Hata nedenlerinin denetim sırası önemli: önce alan sayısı, sonra adet, sonra fiyat. Başlık satırı numaralandırmaya dahildir (ilk veri satırı 2. satırdır)."},
        ],
    },
]
data["workshops"].sort(key=lambda item: item["afterModule"])
milestones_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("\nyazıldı:", len(tasks), "görev,", len(data["workshops"]), "atölye")
