import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2] / "content"


def c(text):
    return text.strip("\n")


sections = []


def section(**fields):
    for key in ("code", "expectedOutput", "realCode", "realOutput"):
        fields[key] = c(fields[key])
    sections.append(fields)


section(
    id="open-modes",
    title="open ve dosya modları",
    eyebrow="Okumak, yazmak, eklemek, yalnızca yoksa oluşturmak",
    objectives=[
        "r, w, a ve x modlarının dosyaya ne yaptığını öngörür.",
        "Eksik dosyada FileNotFoundError, var olan dosyada x modunun FileExistsError verdiğini açıklar.",
    ],
    prerequisites=["m7:try-except", "m2:unicode-encoding"],
    summary="open(yol, mod, encoding=...) bir dosya nesnesi döndürür. Mod, dosyaya ne yapılacağını söyler: r okur, w boşaltıp yazar, a sona ekler, x yalnızca dosya yoksa oluşturur. İş bitince close() ile kapatılır.",
    explanation="Mod verilmezse \"r\" kullanılır; dosya yoksa FileNotFoundError oluşur. \"w\" dosyayı yoksa oluşturur, varsa açar açmaz içeriğini siler; yazmadan kapatmak bile dosyayı boşaltır. \"a\" mevcut içeriği korur ve her yazmayı sona ekler. \"x\" yalnızca dosya yoksa açılır, varsa FileExistsError verir; yanlışlıkla üzerine yazmayı önler. Moda eklenen \"b\" (\"rb\", \"wb\") str yerine bytes ile çalışır, \"+\" ise aynı dosyada hem okumaya hem yazmaya izin verir. Metin modunda encoding'i her zaman açıkça yaz: verilmezse işletim sisteminin varsayılanı kullanılır, Türkçe Windows'ta bu UTF-8 değildir. write() satır sonu eklemez; \"\\n\" senin sorumluluğundadır. Bu sitede her çalıştırma boş bir klasörde başlar ve sonunda silinir; bu yüzden örnekler okuyacakları dosyayı önce kendileri oluşturur. Hata mesajındaki errno numarası platforma göre değişir; programda mesaj yerine hata türüne ve error.filename'e bak.",
    code=r'''
f = open("notlar.txt", "w", encoding="utf-8")
f.write("ilk satır\n")
f.close()

f = open("notlar.txt", "a", encoding="utf-8")
f.write("eklenen satır\n")
f.close()

f = open("notlar.txt", encoding="utf-8")
print(f.read(), end="")
f.close()

f = open("notlar.txt", "w", encoding="utf-8")
f.close()
f = open("notlar.txt", encoding="utf-8")
print(repr(f.read()))
f.close()
''',
    expectedOutput=r'''
ilk satır
eklenen satır
''
''',
    why="İlk \"w\" dosyayı oluşturup bir satır yazar, \"a\" ikinci satırı sona ekler; okuma ikisini de verir. read() zaten \"\\n\" ile biten metni döndürdüğü için print'e end=\"\" verildi. Son \"w\" hiçbir şey yazmadan kapatıldı ama dosya açıldığı anda boşaltılmıştı; repr boş metni '' olarak gösterir.",
    alternatives=[
        "Dosyayı kapatmayı unutmamak için with kullanmak daha güvenlidir; bir sonraki bölümün konusu.",
        "Kısa metinler için pathlib.Path(\"notlar.txt\").write_text(...) ve read_text(...) dosyayı tek satırda açıp kapatır.",
    ],
    traps=[
        "Ekleme için \"w\" kullanmak; her açılış önceki içeriği siler.",
        "write()'ın satır sonu eklediğini sanmak.",
        "encoding vermemek; kod kendi bilgisayarında çalışıp başka bir makinede Türkçe karakterleri bozabilir.",
    ],
    realCode=r'''
def create_once(name, text):
    try:
        f = open(name, "x", encoding="utf-8")
    except FileExistsError:
        return f"{name} zaten var, dokunulmadı"
    f.write(text)
    f.close()
    return f"{name} oluşturuldu"

print(create_once("rapor.txt", "v1"))
print(create_once("rapor.txt", "v2"))
f = open("rapor.txt", encoding="utf-8")
print(f.read())
f.close()

try:
    open("eksik.txt", encoding="utf-8")
except FileNotFoundError as error:
    print("bulunamadı:", error.filename)
''',
    realOutput=r'''
rapor.txt oluşturuldu
rapor.txt zaten var, dokunulmadı
v1
bulunamadı: eksik.txt
''',
    lineByLine=[
        "\"x\" modu dosya varsa açılmaz; FileExistsError yakalanıp kullanıcıya anlaşılır bir sonuç döndürülür.",
        "İlk çağrı dosyayı oluşturup v1 yazar; ikinci çağrı mevcut raporu ezmez.",
        "Okuma dosyada hâlâ v1 olduğunu gösterir.",
        "Olmayan dosyayı okumak FileNotFoundError verir; error.filename hangi yolun bulunamadığını söyler.",
    ],
)

section(
    id="with-lifecycle",
    title="with ve dosya yaşam döngüsü",
    eyebrow="Aç, kullan, ne olursa olsun kapat",
    objectives=[
        "with bloğu bittiğinde, hata olsa bile dosyanın kapandığını açıklar.",
        "Kapanmış dosyayı kullanmanın ValueError verdiğini ve kapatılmayan yazmaların kaybolabileceğini öngörür.",
    ],
    prerequisites=["open-modes", "m7:else-finally"],
    summary="with open(...) as f: bloğu bitince dosya otomatik kapanır; blok bir hata yüzünden yarıda kalsa bile. Elle close() çağırmayı unutma riskini ortadan kaldırır.",
    explanation="with, M7'deki try/finally kalıbının hazır hâlidir: blok nasıl biterse bitsin (normal, return, hata) dosyanın close() metodu çağrılır. f değişkeni bloktan sonra da vardır ama dosya kapalıdır; f.closed True olur ve okuma/yazma ValueError: I/O operation on closed file verir. Yazılanlar önce bellekteki bir tampona gider ve dosyaya close() ya da flush() ile geçer. Bu yüzden kapatılmamış bir dosyaya yazılanlar, aynı dosyayı başka bir open ile okuyunca henüz görünmeyebilir; program çökerse hiç yazılmamış olabilir. with bu sorunların ikisini de çözer. Tek with içinde virgülle iki dosya açılabilir: with open(a) as src, open(b, \"w\") as dst:.",
    code=r'''
with open("liste.txt", "w", encoding="utf-8") as f:
    f.write("elma\n")
    print("içeride:", f.closed)
print("dışarıda:", f.closed)

try:
    with open("liste.txt", "a", encoding="utf-8") as f:
        f.write("armut\n")
        raise ValueError("yarıda kaldı")
except ValueError as error:
    print(error, f.closed)

with open("liste.txt", encoding="utf-8") as f:
    print(f.read().split())
''',
    expectedOutput=r'''
içeride: False
dışarıda: True
yarıda kaldı True
['elma', 'armut']
''',
    why="Blok içindeyken dosya açıktır, blok bitince kapanır. İkinci with içinde hata fırlatılmasına rağmen dosya kapatıldı ve kapanırken tampondaki \"armut\" satırı dosyaya yazıldı; bu yüzden son okumada iki meyve de var.",
    alternatives=[
        "try/finally içinde f.close() aynı güvenliği verir ama daha uzundur ve close'u yazmayı unutmak kolaydır.",
        "Uzun süre açık kalan bir dosyada (ör. log) verinin hemen yazılması gerekiyorsa f.flush() çağrılabilir.",
    ],
    traps=[
        "with bloğundan sonra f.read() çağırmak; dosya artık kapalıdır.",
        "Hata olunca with'in dosyayı açık bıraktığını sanmak.",
        "Kapatılmamış bir dosyaya yazılanların diskte olduğunu varsaymak.",
    ],
    realCode=r'''
def append_log(path, message):
    with open(path, "a", encoding="utf-8") as f:
        f.write(message + "\n")

def read_log(path):
    with open(path, encoding="utf-8") as f:
        return [line.rstrip("\n") for line in f]

append_log("uygulama.log", "başladı")
append_log("uygulama.log", "kullanıcı girdi")
print(read_log("uygulama.log"))
''',
    realOutput=r'''
['başladı', 'kullanıcı girdi']
''',
    lineByLine=[
        "Her log çağrısı dosyayı \"a\" ile açar, bir satır ekler ve with sayesinde hemen kapatır; yazılan veri diske geçmiş olur.",
        "\"\\n\" elle eklenir; yoksa mesajlar aynı satıra yapışırdı.",
        "read_log dosyayı satır satır dolaşır ve satır sonlarını atar.",
        "İki çağrının yazdığı satırlar sırasıyla okunur; dosya hiçbir anda açık unutulmadı.",
    ],
)

section(
    id="reading-lines",
    title="Satır satır okuma",
    eyebrow="read, readline, readlines ve döngü",
    objectives=[
        "read, readline, readlines ve for döngüsünün ne döndürdüğünü ayırır.",
        "Satır sonundaki \\n karakterini ve dosya konumunun ilerlediğini hesaba katar.",
    ],
    prerequisites=["with-lifecycle", "m3:enumerate-zip"],
    summary="read() tüm metni, readline() bir satırı, readlines() satır listesini döndürür. Dosyanın üzerinde for ile dönmek satırları tek tek, belleği şişirmeden verir. Her satır sonundaki \"\\n\" ile gelir.",
    explanation="Dosya nesnesi bir okuma konumu tutar: okunan kısım bir daha verilmez. read()'den sonra ikinci read() boş metin döndürür; readline() ile bir satır okuduktan sonra başlayan for döngüsü kalan satırlardan devam eder. Satırlar \"\\n\" ile biter, son satırda bu karakter olmayabilir. Karşılaştırmadan önce line.rstrip(\"\\n\") ya da baştaki/sondaki boşlukları da atmak istiyorsan line.strip() kullan. read().splitlines() satır sonlarını atarak liste verir ama tüm dosyayı belleğe alır; büyük dosyalarda for line in f tercih edilir. Boş satır \"\\n\" olarak gelir, strip() sonrası \"\" olur ve False sayılır. enumerate(f, start=1) satır numarası verir; hata mesajlarında satır numarası göstermek için kullanışlıdır.",
    code=r'''
with open("siir.txt", "w", encoding="utf-8") as f:
    f.write("bir\niki\n\nüç\n")

with open("siir.txt", encoding="utf-8") as f:
    print(repr(f.readline()))
    for number, line in enumerate(f, start=2):
        print(number, repr(line.rstrip("\n")))
''',
    expectedOutput=r'''
'bir\n'
2 'iki'
3 ''
4 'üç'
''',
    why="readline() ilk satırı \"\\n\" ile birlikte döndürdü ve okuma konumu ikinci satıra geçti. for döngüsü oradan devam eder; bu yüzden numaralandırma 2'den başlatıldı. Üçüncü satır boştu: yalnızca \"\\n\" içeriyordu, rstrip sonrası '' kaldı.",
    alternatives=[
        "Küçük dosyada f.read().splitlines() satır sonları olmadan hazır liste verir.",
        "Satır listesine ihtiyaç yoksa for line in f en az bellekle çalışır.",
    ],
    traps=[
        "line == \"evet\" gibi karşılaştırmalarda satır sonundaki \\n'i unutmak.",
        "Dosyayı bir kez okuduktan sonra aynı nesneyle tekrar okumaya çalışıp boş sonuç almak.",
        "print(line) ile satırları yazdırıp çift satır aralığı görmek; satırın kendi \\n'i ve print'in \\n'i üst üste biner.",
    ],
    realCode=r'''
sample = "INFO başladı\nERROR disk dolu\nINFO devam\nERROR bağlantı koptu\n"
with open("sunucu.log", "w", encoding="utf-8") as f:
    f.write(sample)

errors = []
with open("sunucu.log", encoding="utf-8") as f:
    for number, line in enumerate(f, start=1):
        level, _, message = line.rstrip("\n").partition(" ")
        if level == "ERROR":
            errors.append(f"{number}: {message}")

print(len(errors), "hata")
print("\n".join(errors))
''',
    realOutput=r'''
2 hata
2: disk dolu
4: bağlantı koptu
''',
    lineByLine=[
        "Örnek log dosyası oluşturulur; gerçekte bu dosya başka bir program tarafından yazılmış olurdu.",
        "Dosya satır satır dolaşılır, enumerate 1'den başlayan satır numarası verir.",
        "partition(\" \") satırı ilk boşluktan seviye ve mesaj olarak ikiye ayırır.",
        "Yalnızca ERROR satırları numaralarıyla birlikte toplanır ve rapor edilir.",
    ],
)

section(
    id="pathlib",
    title="pathlib ile yollar",
    eyebrow="Yolu metin değil nesne olarak kur",
    objectives=[
        "Path nesnesiyle yol birleştirir; name, stem, suffix ve parent parçalarını okur.",
        "Klasör oluşturur, dosya varlığını sınar ve dosyaları glob ile bulur.",
    ],
    prerequisites=["with-lifecycle"],
    summary="pathlib.Path yolları nesne olarak temsil eder. / operatörü yol parçalarını işletim sistemine uygun ayırıcıyla birleştirir; name, stem, suffix, parent yolu parçalara ayırır; exists, mkdir, read_text, write_text, glob dosya sistemiyle çalışır.",
    explanation="Path(\"veri\") / \"rapor.csv\" Windows'ta veri\\rapor.csv, Linux ve macOS'ta veri/rapor.csv olur; ayırıcıyı elle yazmak gerekmez. Bu derste yollar as_posix() ile yazdırılıyor ki çıktı her sistemde aynı olsun. Göreli yollar programın çalıştığı klasöre (çalışma dizinine) göredir; dosyanın bulunduğu klasöre göre değil. Path oluşturmak dosya oluşturmaz; exists() ile varlığı sınanır. mkdir(parents=True, exist_ok=True) eksik üst klasörleri de oluşturur ve klasör zaten varsa hata vermez. read_text/write_text dosyayı açıp kapatmayı kendileri yapar; encoding burada da açıkça verilmelidir. iterdir(), glob(\"*.txt\") ve rglob(\"*.txt\") sırası garanti olmayan sonuçlar üretir; tutarlı çıktı için sorted() ile sırala. suffix yalnızca son uzantıdır: \"yedek.tar.gz\" için .gz.",
    code=r'''
from pathlib import Path

report = Path("veri") / "2026" / "rapor.final.csv"
print(report.as_posix())
print(report.name, report.stem, report.suffix)
print(report.parent.as_posix(), report.exists())

report.parent.mkdir(parents=True, exist_ok=True)
report.write_text("ad,not\n", encoding="utf-8")
print(report.exists(), report.read_text(encoding="utf-8").strip())
''',
    expectedOutput=r'''
veri/2026/rapor.final.csv
rapor.final.csv rapor.final .csv
veri/2026 False
True ad,not
''',
    why="/ üç parçayı tek yolda birleştirdi. name dosya adının tamamı, stem son uzantı hariç kısmı, suffix yalnızca son uzantıdır. Yol nesnesi oluşturmak dosya oluşturmadığı için ilk exists() False döndü; klasörler mkdir ile kurulup dosya yazıldıktan sonra True oldu.",
    alternatives=[
        "Eski kodlarda aynı iş os.path.join, os.path.basename ve os.path.splitext ile yapılır; bir sonraki bölümde okunuyor.",
        "Uzun dosyalarda read_text yerine path.open(encoding=\"utf-8\") ile satır satır okumak belleği korur.",
    ],
    traps=[
        "Path(...) yazınca dosyanın oluştuğunu sanmak.",
        "Üst klasör yokken write_text çağırıp FileNotFoundError almak.",
        "glob/iterdir sonucunun alfabetik geldiğini varsaymak.",
        "Göreli yolun, kod dosyasının bulunduğu klasöre göre çözüldüğünü sanmak.",
    ],
    realCode=r'''
from pathlib import Path

for name in ["notlar/ocak.txt", "notlar/subat.txt", "notlar/foto.png", "notlar/eski/aralik.txt"]:
    path = Path(name)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(name, encoding="utf-8")

root = Path("notlar")
print(sorted(p.name for p in root.glob("*.txt")))
print(sorted(p.relative_to(root).as_posix() for p in root.rglob("*.txt")))
print(sorted(p.name for p in root.iterdir() if p.is_dir()))
''',
    realOutput=r'''
['ocak.txt', 'subat.txt']
['eski/aralik.txt', 'ocak.txt', 'subat.txt']
['eski']
''',
    lineByLine=[
        "Örnek klasör yapısı kurulur; her dosyanın üst klasörü gerekirse oluşturulur.",
        "glob(\"*.txt\") yalnızca notlar klasörünün kendisine bakar; alt klasördeki aralik.txt gelmez.",
        "rglob tüm alt klasörleri de tarar; relative_to yolu kök klasöre göre kısaltır.",
        "iterdir doğrudan içerikleri verir; is_dir ile yalnızca klasörler seçilir. Hepsi sorted ile sabit sıraya alınır.",
    ],
)

section(
    id="os-shutil",
    title="os ve shutil ile dosya işlemleri",
    eyebrow="Listele, taşı, kopyala, sil",
    objectives=[
        "os.listdir, os.path.join, os.rename ve os.remove içeren kodun ne yaptığını okur.",
        "shutil.copy, shutil.move ve shutil.rmtree'nin etkisini ve geri alınamayan silmenin riskini açıklar.",
    ],
    prerequisites=["pathlib"],
    summary="os modülü dosya ve klasörlerle temel işlemleri (listeleme, yeniden adlandırma, silme), os.path yol metinlerini işler. shutil üst düzey işleri yapar: dosya kopyalama, taşıma ve bütün bir klasör ağacını silme.",
    explanation="Yeni kodda yollar için pathlib tercih edilir ama mevcut projelerin çoğu os ve os.path kullanır; bu bölüm onları okuyabilmek içindir. os.path.join(\"proje\", \"a.txt\") platforma uygun ayırıcıyla birleştirir, os.path.exists varlığı, os.path.splitext uzantıyı ayırır. os.listdir bir klasördeki adları sırasız bir liste olarak verir. os.makedirs(..., exist_ok=True) iç içe klasör kurar. os.rename ve shutil.move taşır/yeniden adlandırır, shutil.copy içeriği kopyalar. os.remove tek dosya siler; klasörü silmez. shutil.rmtree klasörü içindekilerle birlikte siler ve geri dönüşüm kutusuna göndermez: geri alınamaz. Silme ve üzerine yazma yapan kodu çalıştırmadan önce yolun gerçekten hedeflediğin yer olduğundan emin ol.",
    code=r'''
import os
import shutil

os.makedirs("proje/yedek", exist_ok=True)
with open(os.path.join("proje", "ayar.txt"), "w", encoding="utf-8") as f:
    f.write("mod=test\n")

shutil.copy("proje/ayar.txt", "proje/yedek/ayar.txt")
os.rename("proje/ayar.txt", "proje/ayar.eski")
print(sorted(os.listdir("proje")))
print(os.path.exists("proje/yedek/ayar.txt"), os.path.splitext("ayar.eski"))

shutil.rmtree("proje")
print(os.path.exists("proje"))
''',
    expectedOutput=r'''
['ayar.eski', 'yedek']
True ('ayar', '.eski')
False
''',
    why="Kopya yedek klasörüne gitti, asıl dosya yeniden adlandırıldı; bu yüzden proje klasöründe ayar.eski ve yedek kaldı. splitext adı ve uzantıyı bir tuple olarak ayırır. rmtree bütün ağacı tek seferde sildi.",
    alternatives=[
        "pathlib karşılıkları: Path.rename, Path.unlink, Path.iterdir; kopyalama ve ağaç silme için yine shutil kullanılır.",
        "Silmek yerine bir arşiv klasörüne shutil.move ile taşımak, hata yaptığında geri dönmeyi sağlar.",
    ],
    traps=[
        "os.listdir'in alfabetik sıra verdiğini varsaymak.",
        "os.remove ile klasör silmeye çalışmak; klasör için os.rmdir (boşsa) ya da shutil.rmtree gerekir.",
        "rmtree'nin silinenleri geri dönüşüm kutusuna gönderdiğini sanmak.",
    ],
    realCode=r'''
import os
import shutil

def safe_write(path, text):
    if os.path.exists(path):
        shutil.copy(path, path + ".bak")
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

safe_write("ayar.ini", "v1")
safe_write("ayar.ini", "v2")
print(sorted(os.listdir(".")))
with open("ayar.ini.bak", encoding="utf-8") as f:
    print("yedek:", f.read())
''',
    realOutput=r'''
['ayar.ini', 'ayar.ini.bak']
yedek: v1
''',
    lineByLine=[
        "Dosya zaten varsa, üzerine yazmadan önce .bak uzantılı bir kopyası alınır.",
        "İlk çağrıda dosya yoktur; yedek alınmadan v1 yazılır.",
        "İkinci çağrıda v1 yedeğe kopyalanır, sonra dosyaya v2 yazılır.",
        "Klasörde asıl dosya ve yedeği vardır; yedek önceki sürümü taşır.",
    ],
)

section(
    id="encoding",
    title="Dosya encoding'i",
    eyebrow="Metin ve bayt arasındaki sözleşme",
    objectives=[
        "Bir metnin karakter sayısıyla UTF-8 bayt sayısının neden farklı olduğunu açıklar.",
        "Yanlış encoding ile okunan dosyada bozuk karakterleri ve UnicodeDecodeError'u tanır.",
    ],
    prerequisites=["open-modes", "m2:bytes-vs-str"],
    summary="Dosyalar bayt saklar. Metin modunda Python yazarken metni encoding ile bayta, okurken baytı yine encoding ile metne çevirir. Yazan ve okuyan aynı encoding'i kullanmazsa karakterler bozulur ya da UnicodeDecodeError oluşur.",
    explanation="UTF-8'de ASCII karakterler 1 bayt, ç ş ğ ı ö ü İ gibi karakterler 2 bayttır. cp1254 (Windows Türkçe) her karakteri 1 baytla saklar ama yalnızca sınırlı bir karakter kümesini kapsar. UTF-8 ile yazılmış bir dosya cp1254 ile okunursa her Türkçe harf iki tuhaf karaktere dönüşür (ş → ÅŸ); buna mojibake denir ve hata vermez, sessizce bozuk veri üretir. Tersi, cp1254 dosyasını UTF-8 ile okumak çoğu zaman UnicodeDecodeError verir. encoding verilmezse Python işletim sisteminin varsayılanını kullanır; aynı kod bir makinede çalışıp diğerinde bozulabilir. Kural: her open'a ve read_text/write_text'e encoding=\"utf-8\" yaz; başka bir kaynaktan gelen dosyanın encoding'ini o kaynağa sor. errors=\"replace\" okunamayan baytları � ile değiştirir; veriyi kurtarmaz, yalnızca okumaya devam etmeyi sağlar. \"rb\" ile açılan dosya bytes döndürür ve encoding almaz.",
    code=r'''
text = "Işık"
with open("utf8.txt", "w", encoding="utf-8") as f:
    f.write(text)
with open("utf8.txt", "rb") as f:
    data = f.read()
print(len(text), len(data), data)

print(data.decode("cp1254"))
with open("utf8.txt", encoding="utf-8") as f:
    print(f.read())
''',
    expectedOutput=r'''
4 6 b'I\xc5\x9f\xc4\xb1k'
IÅŸÄ±k
Işık
''',
    why="Işık 4 karakterdir; ş ve ı UTF-8'de ikişer bayt tuttuğu için dosya 6 bayttır. Aynı baytlar cp1254 ile çözülünce her bayt ayrı bir karakter sayılır ve mojibake oluşur. Yazarken kullanılan encoding ile okununca metin doğru gelir.",
    alternatives=[
        "Encoding'i bilinmeyen dosyada önce birkaç olası encoding'i deneyip sonucu kontrol etmek; tahmin eden kütüphaneler (charset-normalizer) de vardır ama kesin değildir.",
        "Excel'in açacağı CSV için \"utf-8-sig\" kullanmak dosya başına bir işaret (BOM) ekler ve Türkçe karakterlerin doğru görünmesini sağlar.",
    ],
    traps=[
        "encoding vermeden yazıp okumak; aynı makinede çalışır, başka makinede bozulur.",
        "Mojibake'nin hata vermemesi yüzünden verinin doğru okunduğunu sanmak.",
        "errors=\"ignore\" ile hatayı susturup karakterleri sessizce kaybetmek.",
    ],
    realCode=r'''
with open("eski.csv", "w", encoding="cp1254") as f:
    f.write("şehir,nüfus\nİzmir,4\n")

try:
    with open("eski.csv", encoding="utf-8") as f:
        f.read()
except UnicodeDecodeError as error:
    print("utf-8 değil:", error.reason)

with open("eski.csv", encoding="cp1254") as f:
    print(f.readline().strip())
with open("eski.csv", encoding="utf-8", errors="replace") as f:
    print(f.readline().strip())
''',
    realOutput=r'''
utf-8 değil: invalid start byte
şehir,nüfus
�ehir,n�fus
''',
    lineByLine=[
        "Eski bir sistemin ürettiği cp1254 kodlu CSV dosyası taklit edilir.",
        "UTF-8 ile okumak, ş harfinin baytı UTF-8'de geçersiz bir başlangıç olduğu için hata verir; reason nedeni kısa söyler.",
        "Doğru encoding ile okununca başlık satırı düzgün gelir.",
        "errors=\"replace\" okumayı sürdürür ama ş ve ü kaybolup � olur; bu bir çözüm değil, teşhis aracıdır.",
    ],
)

section(
    id="csv",
    title="CSV okuma ve yazma",
    eyebrow="Virgülle ayrılmış ama split ile değil",
    objectives=[
        "csv.reader, csv.DictReader ve csv.writer ile tablo verisini okur ve yazar.",
        "Tırnaklı alanlar, başlık satırı ve metin olarak gelen sayılar gibi CSV tuzaklarını ele alır.",
    ],
    prerequisites=["reading-lines", "m4:dicts"],
    summary="CSV, satırları ve virgülle ayrılmış alanları olan bir tablo biçimidir. csv modülü tırnak ve kaçış kurallarını uygular: alanın içinde virgül olsa bile doğru böler. DictReader her satırı başlık adlarıyla anahtarlanmış bir sözlük olarak verir.",
    explanation="line.split(\",\") \"Lin, Can\" gibi tırnaklı ve virgül içeren alanları böler; csv.reader bölmez. CSV dosyaları newline=\"\" ile açılır: csv modülü satır sonlarını kendisi yönetir, Python'un satır sonu çevirisi araya girerse Windows'ta fazladan boş satırlar oluşur. csv.reader her satırı str listesi olarak verir; ilk satır başlıktır ve next(reader) ile atlanabilir. DictReader başlığı otomatik okur ve satırı {\"ad\": ..., \"not\": ...} sözlüğü yapar. Bütün alanlar str gelir; sayı gerekiyorsa int/float ile çevir, boş alan \"\" olur. csv.writer(f).writerow(liste) gerekli yerlere tırnak ekler; DictWriter(f, fieldnames=[...]) önce writeheader() ile başlık yazar. Excel ve bazı Türkçe sistemler ayırıcı olarak noktalı virgül kullanır: csv.reader(f, delimiter=\";\").",
    code=r'''
import csv

rows = [["ad", "şehir"], ["Ada", "İzmir"], ["Lin, Can", "Ankara"]]
with open("kisiler.csv", "w", encoding="utf-8", newline="") as f:
    csv.writer(f).writerows(rows)

with open("kisiler.csv", encoding="utf-8", newline="") as f:
    print(repr(f.read()))

with open("kisiler.csv", encoding="utf-8", newline="") as f:
    for row in csv.reader(f):
        print(row)
''',
    expectedOutput=r'''
'ad,şehir\r\nAda,İzmir\r\n"Lin, Can",Ankara\r\n'
['ad', 'şehir']
['Ada', 'İzmir']
['Lin, Can', 'Ankara']
''',
    why="writer virgül içeren alanı otomatik tırnakladı ve CSV standardı gereği satırları \\r\\n ile bitirdi; newline=\"\" sayesinde bu satır sonları olduğu gibi yazıldı ve okundu. reader tırnaklı alanı tek parça olarak geri verdi.",
    alternatives=[
        "Büyük ve analiz amaçlı tablolar için pandas.read_csv kullanılır; sütun türlerini de tahmin eder.",
        "Sütun adlarıyla çalışmak için DictReader/DictWriter, sütun sırasına bağlı kalmaktan daha okunaklıdır.",
    ],
    traps=[
        "CSV'yi split(\",\") ile bölmek.",
        "Başlık satırını veri sanıp int(\"not\") gibi bir dönüşümde ValueError almak.",
        "DictReader'dan gelen sayıları çevirmeden toplamak; \"70\" + \"90\" metin birleştirir.",
        "newline=\"\" vermeyip Windows'ta satır aralarında boş satırlar görmek.",
    ],
    realCode=r'''
import csv

with open("notlar.csv", "w", encoding="utf-8", newline="") as f:
    f.write("ad,vize,final\nAda,70,90\nCan,55,65\nEce,80,\n")

with open("notlar.csv", encoding="utf-8", newline="") as f:
    for row in csv.DictReader(f):
        if not row["final"]:
            print(f"{row['ad']}: final eksik")
            continue
        average = int(row["vize"]) * 0.4 + int(row["final"]) * 0.6
        print(f"{row['ad']}: {average:.1f}")
''',
    realOutput=r'''
Ada: 82.0
Can: 61.0
Ece: final eksik
''',
    lineByLine=[
        "Not tablosu oluşturulur; Ece'nin final alanı boştur.",
        "DictReader ilk satırı başlık olarak okur; her satır ad, vize, final anahtarlı bir sözlüktür.",
        "Boş alan \"\" olarak gelir ve False sayılır; o satır raporlanıp atlanır.",
        "Notlar metin olduğundan int ile çevrilir, ağırlıklı ortalama bir ondalıkla yazdırılır.",
    ],
)

section(
    id="json",
    title="JSON okuma ve yazma",
    eyebrow="Sözlükleri dosyaya kaydet, geri yükle",
    objectives=[
        "json.dump/json.load ile Python verisini dosyaya kaydeder ve geri okur.",
        "JSON ile Python türleri arasındaki dönüşümleri ve bozuk JSON'da oluşan JSONDecodeError'u ele alır.",
    ],
    prerequisites=["encoding", "m4:nested-data"],
    summary="JSON, sözlük ve listelerden oluşan veriyi metin olarak saklayan yaygın biçimdir. json.dump(veri, f) dosyaya yazar, json.load(f) dosyadan okur; dumps/loads aynı işi str ile yapar.",
    explanation="Python dict → JSON nesne, list ve tuple → dizi, str, int, float, True/False → true/false, None → null olur. Geri okurken tuple liste olarak gelir; sözlük anahtarları her zaman str'dir, bu yüzden {1: \"a\"} geri okununca {\"1\": \"a\"} olur. set, datetime gibi türler doğrudan yazılamaz (TypeError); önce listeye ya da metne çevir. ensure_ascii=False Türkçe karakterleri \\u015f gibi kaçış kodları yerine olduğu gibi yazar; bu durumda dosyayı encoding=\"utf-8\" ile açmak şarttır. indent=2 okunabilir girintili çıktı, sort_keys=True anahtar sırası sabit çıktı üretir. JSON tek tırnak, sondaki fazladan virgül ve yorum kabul etmez; bozuk metin json.JSONDecodeError verir. Bu hata ValueError'ın alt sınıfıdır ve lineno/colno ile yerini söyler.",
    code=r'''
import json

settings = {"kullanıcı": "ada", "boyut": 14, "eklentiler": ["git"], "beta": False}
with open("ayarlar.json", "w", encoding="utf-8") as f:
    json.dump(settings, f, ensure_ascii=False, indent=2)

with open("ayarlar.json", encoding="utf-8") as f:
    print(f.read())
with open("ayarlar.json", encoding="utf-8") as f:
    loaded = json.load(f)
print(loaded == settings, type(loaded["boyut"]).__name__)
print(json.dumps({"x": None, "t": (1, 2), "ş": "ü"}))
''',
    expectedOutput=r'''
{
  "kullanıcı": "ada",
  "boyut": 14,
  "eklentiler": [
    "git"
  ],
  "beta": false
}
True int
{"x": null, "t": [1, 2], "\u015f": "\u00fc"}
''',
    why="indent=2 her öğeyi girintili satıra yazdı, ensure_ascii=False Türkçe harfleri korudu ve False JSON'da false oldu. Geri okunan veri ilk sözlüğe eşittir; sayılar int olarak döner. Son satırda None null'a, tuple diziye dönüştü; ensure_ascii verilmediği için ş ve ü kaçış kodlarıyla yazıldı.",
    alternatives=[
        "Satır satır büyüyen kayıtlar için her satıra bir JSON nesnesi yazan JSON Lines biçimi kullanılır.",
        "Yalnızca Python'un okuyacağı karmaşık nesneler için pickle vardır; güvenilmeyen kaynaktan pickle açmak güvensizdir, veri alışverişinde JSON tercih edilir.",
    ],
    traps=[
        "Geri okunan verinin tuple ve int anahtarları koruduğunu sanmak.",
        "JSON'u tek tırnakla ya da sondaki virgülle elle yazmak.",
        "ensure_ascii=False kullanıp dosyayı encoding vermeden açmak.",
        "dump ile dumps'ı karıştırmak: dump dosya ister, dumps metin döndürür.",
    ],
    realCode=r'''
import json

def load_settings(path, default):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return dict(default)
    except json.JSONDecodeError as error:
        print(f"bozuk ayar dosyası (satır {error.lineno}), varsayılan kullanılıyor")
        return dict(default)

default = {"tema": "açık"}
print(load_settings("ayar.json", default))
with open("ayar.json", "w", encoding="utf-8") as f:
    f.write('{"tema": "koyu",}')
print(load_settings("ayar.json", default))
with open("ayar.json", "w", encoding="utf-8") as f:
    json.dump({"tema": "koyu"}, f)
print(load_settings("ayar.json", default))
''',
    realOutput=r'''
{'tema': 'açık'}
bozuk ayar dosyası (satır 1), varsayılan kullanılıyor
{'tema': 'açık'}
{'tema': 'koyu'}
''',
    lineByLine=[
        "Ayar dosyası yoksa varsayılanın bir kopyası döner; kopya, çağıranın varsayılan sözlüğü değiştirmesini önler.",
        "Sondaki virgül JSON'da geçersizdir; JSONDecodeError yakalanır ve satır numarasıyla bildirilir.",
        "Geçerli dosya yazıldığında json.load kaydedilen sözlüğü döndürür.",
        "Eksik ve bozuk dosya iki ayrı except ile ayrıldı; her durumda program çalışmaya devam eder.",
    ],
)

questions = []


def q(**fields):
    for key in ("code", "expectedOutput", "answer", "solutionCode", "starterCode"):
        if key in fields and isinstance(fields[key], str):
            fields[key] = c(fields[key])
    if "tests" in fields:
        for test in fields["tests"]:
            test["expectedOutput"] = c(test["expectedOutput"])
    fields = {"id": f"m8-q{len(questions) + 1:02d}", **fields}
    questions.append(fields)


# ---- output (12)
q(type="output", topic="dosya-modu", sectionId="open-modes", difficulty=1,
  prompt="Dosyaya iki kez \"w\" ile yazılıyor. Çıktı ne olur?",
  code=r'''
f = open("a.txt", "w", encoding="utf-8")
f.write("bir")
f.close()
f = open("a.txt", "w", encoding="utf-8")
f.write("iki")
f.close()
f = open("a.txt", encoding="utf-8")
print(f.read())
f.close()
''',
  expectedOutput="iki",
  hints=["\"w\" dosyayı her açılışta boşaltır.", "İlk yazılan metin ikinci açılışta silindi."],
  explanation="İkinci open(\"a.txt\", \"w\") dosyayı açar açmaz boşaltır; geriye yalnızca \"iki\" kalır.")

q(type="output", topic="dosya-modu", sectionId="open-modes", difficulty=1,
  prompt="\"a\" modu iki kez kullanılıyor. Çıktı ne olur?",
  code=r'''
with open("sayilar.txt", "w", encoding="utf-8") as f:
    f.write("1\n")
for _ in range(2):
    with open("sayilar.txt", "a", encoding="utf-8") as f:
        f.write("2\n")
with open("sayilar.txt", encoding="utf-8") as f:
    print(f.read().splitlines())
''',
  expectedOutput="['1', '2', '2']",
  hints=["\"a\" mevcut içeriği korur.", "Döngü iki kez ekleme yapar."],
  explanation="\"w\" dosyayı \"1\" ile başlatır, her \"a\" açılışı sona bir \"2\" satırı ekler. splitlines satır sonlarını atarak listeyi verir.")

q(type="output", topic="with", sectionId="with-lifecycle", difficulty=1,
  prompt="with bloğunun içinde ve dışında f.closed ne gösterir?",
  code=r'''
with open("x.txt", "w", encoding="utf-8") as f:
    print(f.closed)
print(f.closed)
''',
  expectedOutput="False\nTrue",
  hints=["Blok içindeyken dosya açıktır.", "f bloktan sonra da vardır ama kapanmıştır."],
  explanation="with bloğu bitince dosya kapanır; f değişkeni silinmez, yalnızca kapalı bir dosyayı gösterir.")

q(type="output", topic="with", sectionId="with-lifecycle", difficulty=3,
  prompt="Yazan dosya kapatılmadan ikinci bir open ile okunuyor. Çıktı ne olur?",
  code=r'''
writer = open("olay.log", "w", encoding="utf-8")
writer.write("başladı")
with open("olay.log", encoding="utf-8") as reader:
    print(repr(reader.read()))
writer.close()
with open("olay.log", encoding="utf-8") as reader:
    print(repr(reader.read()))
''',
  expectedOutput="''\n'başladı'",
  hints=["write() veriyi önce bellekteki bir tampona koyar.", "Tampon close() ya da flush() ile dosyaya aktarılır."],
  explanation="\"w\" dosyayı oluşturup boşalttı; yazılan metin henüz tampondaydı, bu yüzden ilk okuma boş metin gördü. close() tamponu dosyaya aktardı ve ikinci okuma metni buldu. with kullanmak bu durumu önler.")

q(type="output", topic="okuma", sectionId="reading-lines", difficulty=2,
  prompt="Aynı dosya nesnesinde read() iki kez çağrılıyor. Çıktı ne olur?",
  code=r'''
with open("a.txt", "w", encoding="utf-8") as f:
    f.write("ab\ncd\n")
with open("a.txt", encoding="utf-8") as f:
    first = f.read()
    second = f.read()
print(len(first), repr(second))
''',
  expectedOutput="6 ''",
  hints=["\\n de bir karakterdir.", "İlk read() okuma konumunu dosyanın sonuna taşır."],
  explanation="İlk read() altı karakterin tamamını (iki harf, \\n, iki harf, \\n) okur. Konum sonda kaldığı için ikinci read() boş metin döndürür.")

q(type="output", topic="okuma", sectionId="reading-lines", difficulty=2,
  prompt="Son satırı \\n ile bitmeyen dosyada readlines() ne döndürür?",
  code=r'''
with open("a.txt", "w", encoding="utf-8") as f:
    f.write("x\ny")
with open("a.txt", encoding="utf-8") as f:
    print(f.readlines())
''',
  expectedOutput="['x\\n', 'y']",
  hints=["readlines satır sonlarını silmez.", "Dosyaya son satırdan sonra \\n yazılmadı."],
  explanation="readlines her satırı olduğu gibi verir: ilk satır \\n ile biter, son satır dosyada nasıl yazıldıysa öyle gelir.")

q(type="output", topic="okuma", sectionId="reading-lines", difficulty=2,
  prompt="Satırlar print ile yazdırılıyor. Çıktı kaç satırdan oluşur ve neye benzer?",
  code=r'''
with open("a.txt", "w", encoding="utf-8") as f:
    f.write("a\nb")
with open("a.txt", encoding="utf-8") as f:
    for line in f:
        print(line)
print("son")
''',
  expectedOutput="a\n\nb\nson",
  hints=["İlk satır \"a\\n\" olarak gelir.", "print kendi satır sonunu da ekler."],
  explanation="\"a\\n\" yazdırılırken print bir \\n daha ekler ve araya boş satır girer. \"b\" satırında \\n yoktur, boşluk oluşmaz. Önlemek için print(line.rstrip(\"\\n\")) ya da print(line, end=\"\").")

q(type="output", topic="pathlib", sectionId="pathlib", difficulty=2,
  prompt="Path nesnesinin parçaları ne yazdırır?",
  code=r'''
from pathlib import Path

p = Path("arsiv") / "2026" / "yedek.tar.gz"
print(p.name, p.stem, p.suffix)
print(p.parent.name)
''',
  expectedOutput="yedek.tar.gz yedek.tar .gz\n2026",
  hints=["suffix yalnızca son uzantıdır.", "parent bir üst klasörün yolu, onun name'i klasör adıdır."],
  explanation="stem son uzantıyı atar ve \"yedek.tar\" kalır; suffix \".gz\"dir. Tüm uzantılar için p.suffixes ['.tar', '.gz'] verir.")

q(type="output", topic="os", sectionId="os-shutil", difficulty=1,
  prompt="Dosyalar oluşturulup biri siliniyor. Çıktı ne olur?",
  code=r'''
import os

for name in ["c.txt", "a.txt", "b.txt"]:
    with open(name, "w", encoding="utf-8") as f:
        f.write(name)
os.remove("b.txt")
print(sorted(os.listdir(".")))
''',
  expectedOutput="['a.txt', 'c.txt']",
  hints=["Her çalıştırma boş klasörde başlar.", "sorted alfabetik sıraya koyar."],
  explanation="Üç dosya oluşturulur, os.remove biri siler. os.listdir sırası garanti olmadığından sorted ile sabit sıra elde edilir.")

q(type="output", topic="encoding", sectionId="encoding", difficulty=1,
  prompt="Karakter ve UTF-8 bayt sayısı ne çıkar?",
  code=r'''
text = "çay"
print(len(text), len(text.encode("utf-8")))
''',
  expectedOutput="3 4",
  hints=["ç UTF-8'de iki bayttır.", "a ve y birer bayttır."],
  explanation="Metin 3 karakterdir; UTF-8'de ç 2, a ve y 1'er bayt tuttuğu için toplam 4 bayttır. Dosya boyutu bayt sayısıdır.")

q(type="output", topic="csv", sectionId="csv", difficulty=2,
  prompt="Aynı satır csv.reader ve split ile bölünüyor. Kaç alan çıkar?",
  code=r'''
import csv

with open("a.csv", "w", encoding="utf-8", newline="") as f:
    f.write('Ada,"İzmir, Konak",90\n')
with open("a.csv", encoding="utf-8", newline="") as f:
    line = f.readline()
row = next(csv.reader([line]))
print(len(row), len(line.split(",")))
''',
  expectedOutput="3 4",
  hints=["Tırnak içindeki virgül alan ayırıcı değildir.", "split tırnakları tanımaz."],
  explanation="csv.reader tırnaklı alanı tek parça sayar: Ada, İzmir, Konak ve 90 olmak üzere 3 alan. split her virgülde böler ve 4 parça üretir; adres alanı ikiye ayrılır.")

q(type="output", topic="json", sectionId="json", difficulty=3,
  prompt="Veri JSON'a yazılıp geri okunuyor. Çıktı ne olur?",
  code=r'''
import json

data = {1: (2, 3)}
back = json.loads(json.dumps(data))
print(back, back == data)
''',
  expectedOutput="{'1': [2, 3]} False",
  hints=["JSON nesne anahtarları her zaman metindir.", "JSON'da tuple yoktur, yalnızca dizi vardır."],
  explanation="dumps int anahtarı \"1\" metnine, tuple'ı diziye çevirir. loads bunları str anahtar ve liste olarak geri verir; sonuç ilk sözlüğe eşit değildir.")

# ---- bug (6)
q(type="bug", topic="dosya-modu", sectionId="open-modes", difficulty=1,
  prompt="Her çağrı log'a bir satır eklemeli ama dosyada yalnızca son mesaj kalıyor. Sorun nedir?",
  code=r'''
def log(message):
    with open("app.log", "w", encoding="utf-8") as f:
        f.write(message + "\n")

log("başladı")
log("bitti")
with open("app.log", encoding="utf-8") as f:
    print(f.read().splitlines())
''',
  options=[
      "\"w\" modu her açılışta dosyayı boşaltıyor; ekleme için \"a\" kullanılmalı",
      "write() satır sonu eklemediği için satırlar birleşiyor",
      "with dosyayı kapattığı için ilk yazılan kayboluyor",
      "splitlines son satır dışındakileri atıyor",
  ],
  answer="\"w\" modu her açılışta dosyayı boşaltıyor; ekleme için \"a\" kullanılmalı",
  optionFeedback={
      "write() satır sonu eklemediği için satırlar birleşiyor": "Kod \"\\n\"i elle ekliyor; satırlar birleşseydi çıktıda iki mesaj yan yana görünürdü.",
      "with dosyayı kapattığı için ilk yazılan kayboluyor": "Kapatmak veriyi siler değil, diske yazar. Silme işini ikinci \"w\" açılışı yapıyor.",
      "splitlines son satır dışındakileri atıyor": "splitlines tüm satırları döndürür; dosyada zaten tek satır var.",
  },
  hints=["Çıktı ['bitti'].", "Hangi mod mevcut içeriği korur?"],
  explanation="Her log çağrısı dosyayı \"w\" ile açıp öncekini siliyor. \"a\" ile açılırsa çıktı ['başladı', 'bitti'] olur.")

q(type="bug", topic="with", sectionId="with-lifecycle", difficulty=1,
  prompt="Kod ValueError: I/O operation on closed file veriyor. Neden?",
  code=r'''
with open("x.txt", "w", encoding="utf-8") as f:
    f.write("veri")

with open("x.txt", encoding="utf-8") as f:
    pass
print(f.read())
''',
  options=[
      "f.read() with bloğunun dışında; blok bitince dosya kapanmıştı",
      "Dosya \"w\" ile yazıldığı için bir daha okunamaz",
      "f adı iki kez kullanıldığı için ilk dosya okunuyor",
      "encoding okurken verilmemeli",
  ],
  answer="f.read() with bloğunun dışında; blok bitince dosya kapanmıştı",
  optionFeedback={
      "Dosya \"w\" ile yazıldığı için bir daha okunamaz": "Kapatılmış bir dosya başka bir open ile her zaman tekrar okunabilir.",
      "f adı iki kez kullanıldığı için ilk dosya okunuyor": "İkinci with f'yi yeni dosya nesnesine bağladı; sorun onun da kapanmış olması.",
      "encoding okurken verilmemeli": "Okurken de encoding verilmelidir; hata türü kapalı dosyaya işaret ediyor.",
  },
  hints=["pass bloğu hemen bitirir.", "read çağrısını with bloğunun içine taşı."],
  explanation="with bloğu pass ile hemen bitti ve dosya kapandı. Okuma işlemi bloğun içinde yapılmalıdır.")

q(type="bug", topic="okuma", sectionId="reading-lines", difficulty=2,
  prompt="Dosyada iki \"evet\" satırı var ama çıktı 0. Neden?",
  code=r'''
with open("cevaplar.txt", "w", encoding="utf-8") as f:
    f.write("evet\nhayır\nevet\n")

count = 0
with open("cevaplar.txt", encoding="utf-8") as f:
    for line in f:
        if line == "evet":
            count += 1
print(count)
''',
  options=[
      "Satırlar sonlarındaki \\n ile geliyor; karşılaştırmadan önce rstrip(\"\\n\") ya da strip() gerekir",
      "for döngüsü dosyanın yalnızca ilk satırını okur",
      "Türkçe karakterler karşılaştırmayı bozuyor",
      "count döngü içinde sıfırlanıyor",
  ],
  answer="Satırlar sonlarındaki \\n ile geliyor; karşılaştırmadan önce rstrip(\"\\n\") ya da strip() gerekir",
  optionFeedback={
      "for döngüsü dosyanın yalnızca ilk satırını okur": "Döngü tüm satırları dolaşır; sorun satırların içeriği.",
      "Türkçe karakterler karşılaştırmayı bozuyor": "\"evet\"te Türkçe karakter yok; satırın sonunda \\n var.",
      "count döngü içinde sıfırlanıyor": "count = 0 döngüden önce bir kez çalışıyor.",
  },
  hints=["repr(line) yazdırıp bak.", "\"evet\\n\" == \"evet\" False'tur."],
  explanation="Dosyadan okunan satır \"evet\\n\"dir. line.rstrip(\"\\n\") == \"evet\" ile iki satır sayılır.")

q(type="bug", topic="pathlib", sectionId="pathlib", difficulty=2,
  prompt="Kod FileNotFoundError veriyor; oysa dosyayı okumuyor, yazıyor. Neden?",
  code=r'''
from pathlib import Path

report = Path("raporlar") / "ocak.txt"
report.write_text("toplam: 5", encoding="utf-8")
print(report.read_text(encoding="utf-8"))
''',
  options=[
      "raporlar klasörü yok; önce report.parent.mkdir(parents=True, exist_ok=True) gerekir",
      "write_text yalnızca var olan dosyaya yazabilir",
      "/ operatörü yolları birleştiremez; os.path.join gerekir",
      "Path nesnesi str'ye çevrilmeden kullanılamaz",
  ],
  answer="raporlar klasörü yok; önce report.parent.mkdir(parents=True, exist_ok=True) gerekir",
  optionFeedback={
      "write_text yalnızca var olan dosyaya yazabilir": "write_text dosya yoksa oluşturur; oluşturamadığı şey eksik klasördür.",
      "/ operatörü yolları birleştiremez; os.path.join gerekir": "Path için / tam olarak yol birleştirmedir.",
      "Path nesnesi str'ye çevrilmeden kullanılamaz": "Path metotları doğrudan çağrılabilir; open da Path kabul eder.",
  },
  hints=["Hatanın filename'i raporlar/ocak.txt.", "Dosya oluşturulabilir ama klasör otomatik oluşmaz."],
  explanation="Yazma, dosyayı oluşturabilir ama içinde bulunacağı klasörü oluşturmaz. mkdir(parents=True, exist_ok=True) sonrası kod \"toplam: 5\" yazdırır.")

q(type="bug", topic="encoding", sectionId="encoding", difficulty=2,
  prompt="Dosyaya \"çay\" yazıldı ama okununca \"Ã§ay\" görünüyor. Sorun nedir?",
  code=r'''
with open("menu.txt", "w", encoding="utf-8") as f:
    f.write("çay")
with open("menu.txt", encoding="cp1254") as f:
    print(f.read())
''',
  options=[
      "Yazarken utf-8, okurken cp1254 kullanılıyor; iki taraf aynı encoding'i kullanmalı",
      "ç harfi dosyalara yazılamaz",
      "Dosya \"rb\" ile açılmadığı için bozuluyor",
      "print Türkçe karakterleri yazdıramaz",
  ],
  answer="Yazarken utf-8, okurken cp1254 kullanılıyor; iki taraf aynı encoding'i kullanmalı",
  optionFeedback={
      "ç harfi dosyalara yazılamaz": "ç, UTF-8 ile iki bayt olarak sorunsuz yazıldı.",
      "Dosya \"rb\" ile açılmadığı için bozuluyor": "\"rb\" metin değil bytes verir; metni doğru almak için doğru encoding gerekir.",
      "print Türkçe karakterleri yazdıramaz": "print metni olduğu gibi yazdı; metin okunurken bozuldu.",
  },
  hints=["ç'nin iki UTF-8 baytı cp1254'te iki ayrı karakterdir.", "Okurken encoding=\"utf-8\" ver."],
  explanation="UTF-8'de ç iki bayttır (c3 a7). cp1254 bunları Ã ve § olarak çözer. Bu bozulma hata vermez; bu yüzden encoding her iki tarafta da açıkça ve aynı yazılmalıdır.")

q(type="bug", topic="csv", sectionId="csv", difficulty=2,
  prompt="Toplamı yazdırması gereken kod ValueError veriyor. Neden?",
  code=r'''
import csv

with open("puan.csv", "w", encoding="utf-8", newline="") as f:
    f.write("ad,puan\nAda,90\nCan,75\n")

total = 0
with open("puan.csv", encoding="utf-8", newline="") as f:
    for row in csv.reader(f):
        total += int(row[1])
print(total)
''',
  options=[
      "İlk satır başlık; int(\"puan\") çevrilemez. next(reader) ile atlanmalı ya da DictReader kullanılmalı",
      "csv.reader sayıları otomatik int yapar, int ikinci kez çağrılamaz",
      "row[1] yerine row[2] olmalı",
      "newline=\"\" okurken verilmemeli",
  ],
  answer="İlk satır başlık; int(\"puan\") çevrilemez. next(reader) ile atlanmalı ya da DictReader kullanılmalı",
  optionFeedback={
      "csv.reader sayıları otomatik int yapar, int ikinci kez çağrılamaz": "reader tüm alanları str verir; int(\"90\") geçerlidir.",
      "row[1] yerine row[2] olmalı": "Her satırda iki alan var; row[2] IndexError verirdi.",
      "newline=\"\" okurken verilmemeli": "csv dosyaları okurken de newline=\"\" ile açılır.",
  },
  hints=["Hata mesajı: invalid literal for int() with base 10: 'puan'.", "Döngüden önce başlık satırını tüket."],
  explanation="reader ilk olarak ['ad', 'puan'] satırını verir. Başlık atlanınca toplam 165 olur.")

# ---- fill (4)
q(type="fill", topic="dosya-modu", sectionId="open-modes", difficulty=1,
  prompt="Mevcut içeriği silmeden sona ekleyen modu yaz.",
  code=r'''
with open("log.txt", "w", encoding="utf-8") as f:
    f.write("1\n")
with open("log.txt", "___", encoding="utf-8") as f:
    f.write("2\n")
with open("log.txt", encoding="utf-8") as f:
    print(f.read().split())
''',
  answer="a",
  acceptedAnswers=["a"],
  solutionCode=r'''
with open("log.txt", "w", encoding="utf-8") as f:
    f.write("1\n")
with open("log.txt", "a", encoding="utf-8") as f:
    f.write("2\n")
with open("log.txt", encoding="utf-8") as f:
    print(f.read().split())
''',
  expectedOutput="['1', '2']",
  hints=["İngilizce append.", "Tek harf."],
  explanation="\"a\" modu dosyanın sonuna yazar ve önceki satırı korur.")

q(type="fill", topic="with", sectionId="with-lifecycle", difficulty=1,
  prompt="Dosyayı blok bitince otomatik kapatan anahtar sözcüğü yaz.",
  code=r'''
___ open("x.txt", "w", encoding="utf-8") as f:
    f.write("tamam")
print(f.closed)
''',
  answer="with",
  acceptedAnswers=["with"],
  solutionCode=r'''
with open("x.txt", "w", encoding="utf-8") as f:
    f.write("tamam")
print(f.closed)
''',
  expectedOutput="True",
  hints=["Satır \"as f:\" ile bitiyor.", "Bağlam yöneticisini başlatan sözcük."],
  explanation="with bloğu bitince dosya kapanır; f.closed True olur.")

q(type="fill", topic="json", sectionId="json", difficulty=1,
  prompt="Sözlüğü açık dosyaya JSON olarak yazan fonksiyonun adını yaz.",
  code=r'''
import json

with open("veri.json", "w", encoding="utf-8") as f:
    json.___({"ad": "Ada"}, f)
with open("veri.json", encoding="utf-8") as f:
    print(json.load(f)["ad"])
''',
  answer="dump",
  acceptedAnswers=["dump"],
  solutionCode=r'''
import json

with open("veri.json", "w", encoding="utf-8") as f:
    json.dump({"ad": "Ada"}, f)
with open("veri.json", encoding="utf-8") as f:
    print(json.load(f)["ad"])
''',
  expectedOutput="Ada",
  hints=["Okuma tarafı json.load.", "Sonunda s yok: s'li sürüm metin döndürür."],
  explanation="json.dump(veri, dosya) dosyaya yazar; json.dumps(veri) ise metin döndürür ve dosya almaz.")

q(type="fill", topic="csv", sectionId="csv", difficulty=2,
  prompt="Satırları başlık adlarıyla sözlük olarak veren okuyucunun adını yaz.",
  code=r'''
import csv

with open("k.csv", "w", encoding="utf-8", newline="") as f:
    f.write("ad,yas\nAda,36\nCan,20\n")
with open("k.csv", encoding="utf-8", newline="") as f:
    for row in csv.___(f):
        print(row["ad"])
''',
  answer="DictReader",
  acceptedAnswers=["DictReader"],
  solutionCode=r'''
import csv

with open("k.csv", "w", encoding="utf-8", newline="") as f:
    f.write("ad,yas\nAda,36\nCan,20\n")
with open("k.csv", encoding="utf-8", newline="") as f:
    for row in csv.DictReader(f):
        print(row["ad"])
''',
  expectedOutput="Ada\nCan",
  hints=["Satır row[\"ad\"] ile okunuyor; yani bir sözlük.", "Dict ile başlar, Reader ile biter."],
  explanation="DictReader ilk satırı başlık olarak alır ve her veri satırını {\"ad\": ..., \"yas\": ...} sözlüğü yapar.")

# ---- order (4)
q(type="order", topic="with", sectionId="with-lifecycle", difficulty=1,
  prompt="Dosyaya yazıp sonra okuyan ve \"merhaba\" yazdıran sırayı kur.",
  lines=[
      "    print(f.read())",
      "with open(\"a.txt\", encoding=\"utf-8\") as f:",
      "    f.write(\"merhaba\")",
      "with open(\"a.txt\", \"w\", encoding=\"utf-8\") as f:",
  ],
  answer=r'''
with open("a.txt", "w", encoding="utf-8") as f:
    f.write("merhaba")
with open("a.txt", encoding="utf-8") as f:
    print(f.read())
''',
  solutionCode=r'''
with open("a.txt", "w", encoding="utf-8") as f:
    f.write("merhaba")
with open("a.txt", encoding="utf-8") as f:
    print(f.read())
''',
  expectedOutput="merhaba",
  hints=["Okumadan önce dosyanın var olması gerekir.", "Her with satırının gövdesi hemen altında girintilidir."],
  explanation="Önce \"w\" ile yazılır ve blok bitince kapatılır; sonra ayrı bir with ile okunur.")

q(type="order", topic="pathlib", sectionId="pathlib", difficulty=2,
  prompt="Klasörü oluşturup içine dosya yazan ve dosyayı okuyan sırayı kur.",
  lines=[
      "path.write_text(\"tamam\", encoding=\"utf-8\")",
      "from pathlib import Path",
      "print(path.read_text(encoding=\"utf-8\"))",
      "path.parent.mkdir(exist_ok=True)",
      "path = Path(\"cikti\") / \"ozet.txt\"",
  ],
  answer=r'''
from pathlib import Path
path = Path("cikti") / "ozet.txt"
path.parent.mkdir(exist_ok=True)
path.write_text("tamam", encoding="utf-8")
print(path.read_text(encoding="utf-8"))
''',
  solutionCode=r'''
from pathlib import Path
path = Path("cikti") / "ozet.txt"
path.parent.mkdir(exist_ok=True)
path.write_text("tamam", encoding="utf-8")
print(path.read_text(encoding="utf-8"))
''',
  expectedOutput="tamam",
  hints=["Path kullanılmadan önce import edilir.", "Klasör, dosyayı yazmadan önce oluşturulmalı."],
  explanation="Yol nesnesi kurulur, üst klasör oluşturulur, sonra dosya yazılıp okunur. mkdir'den önce yazmak FileNotFoundError verir.")

q(type="order", topic="csv", sectionId="csv", difficulty=2,
  prompt="Virgül içeren bir alanı CSV'ye yazıp geri okuyan sırayı kur.",
  lines=[
      "    print(next(csv.reader(f)))",
      "import csv",
      "    csv.writer(f).writerow([\"x\", \"y, z\"])",
      "with open(\"a.csv\", encoding=\"utf-8\", newline=\"\") as f:",
      "with open(\"a.csv\", \"w\", encoding=\"utf-8\", newline=\"\") as f:",
  ],
  answer=r'''
import csv
with open("a.csv", "w", encoding="utf-8", newline="") as f:
    csv.writer(f).writerow(["x", "y, z"])
with open("a.csv", encoding="utf-8", newline="") as f:
    print(next(csv.reader(f)))
''',
  solutionCode=r'''
import csv
with open("a.csv", "w", encoding="utf-8", newline="") as f:
    csv.writer(f).writerow(["x", "y, z"])
with open("a.csv", encoding="utf-8", newline="") as f:
    print(next(csv.reader(f)))
''',
  expectedOutput="['x', 'y, z']",
  hints=["Yazma bloğu okuma bloğundan önce gelir.", "next(reader) ilk satırı verir."],
  explanation="writer \"y, z\" alanını tırnaklayarak yazar; reader onu tek alan olarak geri okur.")

q(type="order", topic="json", sectionId="json", difficulty=2,
  prompt="Sözlüğü JSON dosyasına kaydedip geri okuyan ve 2 yazdıran sırayı kur.",
  lines=[
      "    data = json.load(f)",
      "    json.dump({\"n\": 1}, f)",
      "print(data[\"n\"] + 1)",
      "with open(\"d.json\", \"w\", encoding=\"utf-8\") as f:",
      "import json",
      "with open(\"d.json\", encoding=\"utf-8\") as f:",
  ],
  answer=r'''
import json
with open("d.json", "w", encoding="utf-8") as f:
    json.dump({"n": 1}, f)
with open("d.json", encoding="utf-8") as f:
    data = json.load(f)
print(data["n"] + 1)
''',
  solutionCode=r'''
import json
with open("d.json", "w", encoding="utf-8") as f:
    json.dump({"n": 1}, f)
with open("d.json", encoding="utf-8") as f:
    data = json.load(f)
print(data["n"] + 1)
''',
  expectedOutput="2",
  hints=["dump yazma, load okuma bloğundadır.", "print dosya kapandıktan sonra da data'yı kullanabilir."],
  explanation="json.load sayıyı int olarak geri verir; 1 + 1 = 2. data bir Python sözlüğü olduğu için with bloğundan sonra da kullanılabilir.")

# ---- code (10)
q(type="code", topic="dosya-modu", sectionId="open-modes", difficulty=1,
  prompt="İlk satırda n, sonra n satır var. Satırları liste.txt dosyasına her biri ayrı satırda olacak şekilde yaz. Sonra dosyayı okuyup her satırı \"1. elma\" biçiminde numaralı yazdır.",
  starterCode=r'''
count = int(input())
items = [input() for _ in range(count)]
# items'ı liste.txt'ye yaz, sonra dosyadan okuyup numaralı yazdır
''',
  answer=r'''
count = int(input())
items = [input() for _ in range(count)]
with open("liste.txt", "w", encoding="utf-8") as f:
    for item in items:
        f.write(item + "\n")
with open("liste.txt", encoding="utf-8") as f:
    for number, line in enumerate(f, start=1):
        print(f"{number}. {line.rstrip()}")
''',
  solutionCode=r'''
count = int(input())
items = [input() for _ in range(count)]
with open("liste.txt", "w", encoding="utf-8") as f:
    for item in items:
        f.write(item + "\n")
with open("liste.txt", encoding="utf-8") as f:
    for number, line in enumerate(f, start=1):
        print(f"{number}. {line.rstrip()}")
''',
  expectedOutput="1. elma\n2. armut",
  exampleInput="2\nelma\narmut",
  tests=[
      {"label": "Örnek", "stdin": "2\nelma\narmut", "expectedOutput": "1. elma\n2. armut"},
      {"label": "Tek satır", "stdin": "1\nçay", "expectedOutput": "1. çay"},
      {"label": "Boş liste", "stdin": "0", "expectedOutput": ""},
      {"label": "Boşluklu ürün", "stdin": "3\nkuru üzüm\nsüt\nyumurta", "expectedOutput": "1. kuru üzüm\n2. süt\n3. yumurta"},
  ],
  hints=["write'a item + \"\\n\" ver.", "Okurken satır sonunu rstrip ile at, enumerate(f, start=1) ile numarala."],
  explanation="Yazma ve okuma ayrı with bloklarında yapılır; ilk blok bitince veri dosyaya geçmiş olur. Satırlar \\n ile döndüğü için yazdırmadan önce temizlenir.")

q(type="code", topic="dosya-modu", sectionId="open-modes", difficulty=2,
  prompt="add(line) fonksiyonunu yaz: günlük.txt dosyasını \"a\" ile açıp line'ı yeni bir satır olarak eklesin. Başlangıç kodu dosyayı \"başlangıç\" ile oluşturur, girdideki satırları add ile ekler ve sonunda dosyadaki satır sayısını ve son satırı yazdırır.",
  starterCode=r'''
with open("günlük.txt", "w", encoding="utf-8") as f:
    f.write("başlangıç\n")

def add(line):
    # dosyayı "a" ile açıp line'ı ekle
    pass

count = int(input())
for _ in range(count):
    add(input())

with open("günlük.txt", encoding="utf-8") as f:
    lines = f.read().splitlines()
print(len(lines), lines[-1])
''',
  answer=r'''
with open("günlük.txt", "w", encoding="utf-8") as f:
    f.write("başlangıç\n")

def add(line):
    with open("günlük.txt", "a", encoding="utf-8") as f:
        f.write(line + "\n")

count = int(input())
for _ in range(count):
    add(input())

with open("günlük.txt", encoding="utf-8") as f:
    lines = f.read().splitlines()
print(len(lines), lines[-1])
''',
  solutionCode=r'''
with open("günlük.txt", "w", encoding="utf-8") as f:
    f.write("başlangıç\n")

def add(line):
    with open("günlük.txt", "a", encoding="utf-8") as f:
        f.write(line + "\n")

count = int(input())
for _ in range(count):
    add(input())

with open("günlük.txt", encoding="utf-8") as f:
    lines = f.read().splitlines()
print(len(lines), lines[-1])
''',
  expectedOutput="3 koşu",
  exampleInput="2\nyürüyüş\nkoşu",
  tests=[
      {"label": "Örnek", "stdin": "2\nyürüyüş\nkoşu", "expectedOutput": "3 koşu"},
      {"label": "Ekleme yok", "stdin": "0", "expectedOutput": "1 başlangıç"},
      {"label": "Tek ekleme", "stdin": "1\nyoga", "expectedOutput": "2 yoga"},
  ],
  hints=["\"w\" kullanırsan başlangıç satırı silinir.", "Her eklemenin sonuna \"\\n\" koy; yoksa satırlar birleşir."],
  explanation="\"a\" modu mevcut satırları korur. Satır sonu eklenmezse \"yürüyüşkoşu\" tek satır olur ve sayım yanlış çıkar.")

q(type="code", topic="with", sectionId="with-lifecycle", difficulty=2,
  prompt="read_or_none(path) fonksiyonunu yaz: dosyayı with ile açıp içeriği döndürsün; dosya yoksa None döndürsün. Girdi bir dosya yolu. Başlangıç kodu mevcut.txt dosyasını oluşturur ve sonucu yazdırır.",
  starterCode=r'''
with open("mevcut.txt", "w", encoding="utf-8") as f:
    f.write("içerik hazır")

def read_or_none(path):
    # with ile oku; FileNotFoundError olursa None döndür
    pass

path = input()
content = read_or_none(path)
print(content if content is not None else f"dosya yok: {path}")
''',
  answer=r'''
with open("mevcut.txt", "w", encoding="utf-8") as f:
    f.write("içerik hazır")

def read_or_none(path):
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return None

path = input()
content = read_or_none(path)
print(content if content is not None else f"dosya yok: {path}")
''',
  solutionCode=r'''
with open("mevcut.txt", "w", encoding="utf-8") as f:
    f.write("içerik hazır")

def read_or_none(path):
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return None

path = input()
content = read_or_none(path)
print(content if content is not None else f"dosya yok: {path}")
''',
  expectedOutput="içerik hazır",
  exampleInput="mevcut.txt",
  tests=[
      {"label": "Örnek", "stdin": "mevcut.txt", "expectedOutput": "içerik hazır"},
      {"label": "Eksik dosya", "stdin": "eksik.txt", "expectedOutput": "dosya yok: eksik.txt"},
      {"label": "Eksik klasör", "stdin": "arsiv/mevcut.txt", "expectedOutput": "dosya yok: arsiv/mevcut.txt"},
  ],
  hints=["try içine with'i koy; return with bloğunun içinden yapılabilir.", "Yalnızca FileNotFoundError'u yakala."],
  explanation="with içinden return edilse bile dosya kapanır. Eksik dosya ve eksik klasör ikisi de FileNotFoundError verir; diğer hatalar (ör. encoding sorunu) gizlenmez.")

q(type="code", topic="okuma", sectionId="reading-lines", difficulty=2,
  prompt="Başlangıç kodu girdideki metni metin.txt'ye yazar. Dosyayı satır satır okuyup \"satır: X, dolu: Y, kelime: Z\" yazdır. Yalnızca boşluk içeren satırlar boş sayılır.",
  starterCode=r'''
count = int(input())
with open("metin.txt", "w", encoding="utf-8") as f:
    for _ in range(count):
        f.write(input() + "\n")

# metin.txt'yi satır satır okuyup say
''',
  answer=r'''
count = int(input())
with open("metin.txt", "w", encoding="utf-8") as f:
    for _ in range(count):
        f.write(input() + "\n")

lines = filled = words = 0
with open("metin.txt", encoding="utf-8") as f:
    for line in f:
        lines += 1
        if line.strip():
            filled += 1
        words += len(line.split())
print(f"satır: {lines}, dolu: {filled}, kelime: {words}")
''',
  solutionCode=r'''
count = int(input())
with open("metin.txt", "w", encoding="utf-8") as f:
    for _ in range(count):
        f.write(input() + "\n")

lines = filled = words = 0
with open("metin.txt", encoding="utf-8") as f:
    for line in f:
        lines += 1
        if line.strip():
            filled += 1
        words += len(line.split())
print(f"satır: {lines}, dolu: {filled}, kelime: {words}")
''',
  expectedOutput="satır: 3, dolu: 2, kelime: 5",
  exampleInput="3\nbir iki üç\n\ndört beş",
  tests=[
      {"label": "Örnek", "stdin": "3\nbir iki üç\n\ndört beş", "expectedOutput": "satır: 3, dolu: 2, kelime: 5"},
      {"label": "Yalnız boşluk", "stdin": "2\n   \ntek", "expectedOutput": "satır: 2, dolu: 1, kelime: 1"},
      {"label": "Boş dosya", "stdin": "0", "expectedOutput": "satır: 0, dolu: 0, kelime: 0"},
      {"label": "Çok boşluk", "stdin": "1\n  a   b  ", "expectedOutput": "satır: 1, dolu: 1, kelime: 2"},
  ],
  hints=["line.strip() boşsa satır boştur.", "split() argümansız çağrılınca ardışık boşlukları tek ayırıcı sayar."],
  explanation="Satır sonu ve boşluklar strip ile atılınca boş satır \"\" olur. split() boşluk dizilerini birleştirerek kelimeleri sayar.")

q(type="code", topic="okuma", sectionId="reading-lines", difficulty=3,
  prompt="Başlangıç kodu girdideki satırları şiir.txt'ye yazar. Dosyayı okuyup en uzun satırı \"N: satır\" biçiminde yazdır (N 1'den başlar). Eşitlikte ilk satır kazanır. Dosya boşsa \"boş dosya\" yazdır. Uzunluk, satır sonu karakteri sayılmadan ölçülür.",
  starterCode=r'''
count = int(input())
with open("şiir.txt", "w", encoding="utf-8") as f:
    for _ in range(count):
        f.write(input() + "\n")

# en uzun satırı bul
''',
  answer=r'''
count = int(input())
with open("şiir.txt", "w", encoding="utf-8") as f:
    for _ in range(count):
        f.write(input() + "\n")

best_number, best_line = 0, None
with open("şiir.txt", encoding="utf-8") as f:
    for number, line in enumerate(f, start=1):
        line = line.rstrip("\n")
        if best_line is None or len(line) > len(best_line):
            best_number, best_line = number, line
if best_line is None:
    print("boş dosya")
else:
    print(f"{best_number}: {best_line}")
''',
  solutionCode=r'''
count = int(input())
with open("şiir.txt", "w", encoding="utf-8") as f:
    for _ in range(count):
        f.write(input() + "\n")

best_number, best_line = 0, None
with open("şiir.txt", encoding="utf-8") as f:
    for number, line in enumerate(f, start=1):
        line = line.rstrip("\n")
        if best_line is None or len(line) > len(best_line):
            best_number, best_line = number, line
if best_line is None:
    print("boş dosya")
else:
    print(f"{best_number}: {best_line}")
''',
  expectedOutput="2: dalga dalga",
  exampleInput="3\ndeniz\ndalga dalga\nkum",
  tests=[
      {"label": "Örnek", "stdin": "3\ndeniz\ndalga dalga\nkum", "expectedOutput": "2: dalga dalga"},
      {"label": "Eşitlik", "stdin": "3\nab\ncd\na", "expectedOutput": "1: ab"},
      {"label": "Boş dosya", "stdin": "0", "expectedOutput": "boş dosya"},
      {"label": "Son satır", "stdin": "2\nx\nyy", "expectedOutput": "2: yy"},
  ],
  hints=["Karşılaştırma > olursa eşitlikte ilk satır kalır.", "Hiç satır yoksa başlangıç değeri değişmez; None ile ayırt et."],
  explanation="rstrip(\"\\n\") ile ölçüm satır sonunu saymaz. Kesin büyüktür karşılaştırması eşitlikte önceki satırı korur; None başlangıcı boş dosyayı ayırır.")

q(type="code", topic="pathlib", sectionId="pathlib", difficulty=2,
  prompt="Başlangıç kodu girdideki dosya adlarını klasor içinde oluşturur. klasor'deki dosyaları uzantıya göre say ve \"uzantı: sayı\" satırlarını alfabetik sırayla yazdır. Uzantılar küçük harfe çevrilir; uzantısı olmayan dosyalar \"(uzantısız)\" sayılır.",
  starterCode=r'''
from pathlib import Path

folder = Path("klasor")
folder.mkdir()
for name in input().split():
    (folder / name).write_text("x", encoding="utf-8")

# klasördeki dosyaları uzantıya göre say
''',
  answer=r'''
from pathlib import Path

folder = Path("klasor")
folder.mkdir()
for name in input().split():
    (folder / name).write_text("x", encoding="utf-8")

counts = {}
for path in folder.iterdir():
    suffix = path.suffix.lower() or "(uzantısız)"
    counts[suffix] = counts.get(suffix, 0) + 1
for suffix in sorted(counts):
    print(f"{suffix}: {counts[suffix]}")
''',
  solutionCode=r'''
from pathlib import Path

folder = Path("klasor")
folder.mkdir()
for name in input().split():
    (folder / name).write_text("x", encoding="utf-8")

counts = {}
for path in folder.iterdir():
    suffix = path.suffix.lower() or "(uzantısız)"
    counts[suffix] = counts.get(suffix, 0) + 1
for suffix in sorted(counts):
    print(f"{suffix}: {counts[suffix]}")
''',
  expectedOutput="(uzantısız): 1\n.csv: 1\n.txt: 2",
  exampleInput="a.txt b.TXT c.csv README",
  tests=[
      {"label": "Örnek", "stdin": "a.txt b.TXT c.csv README", "expectedOutput": "(uzantısız): 1\n.csv: 1\n.txt: 2"},
      {"label": "Çift uzantı", "stdin": "yedek.tar.gz veri.gz", "expectedOutput": ".gz: 2"},
      {"label": "Tek dosya", "stdin": "not.md", "expectedOutput": ".md: 1"},
  ],
  hints=["path.suffix uzantısız dosyada \"\" döndürür; or ile yedek değer ver.", "iterdir sırası belirsiz; yazdırırken sorted kullan."],
  explanation="suffix yalnızca son uzantıyı verir, bu yüzden yedek.tar.gz .gz sayılır. Sayım sözlükte toplanır, çıktı sorted ile sabit sıraya alınır.")

q(type="code", topic="encoding", sectionId="encoding", difficulty=2,
  prompt="Girdideki metni metin.txt'ye UTF-8 ile yaz. Sonra dosyayı \"rb\" ile açıp bayt sayısını bul ve \"karakter: X, bayt: Y\" yazdır.",
  starterCode=r'''
text = input()
# UTF-8 ile yaz, sonra ikili modda okuyup baytları say
''',
  answer=r'''
text = input()
with open("metin.txt", "w", encoding="utf-8") as f:
    f.write(text)
with open("metin.txt", "rb") as f:
    data = f.read()
print(f"karakter: {len(text)}, bayt: {len(data)}")
''',
  solutionCode=r'''
text = input()
with open("metin.txt", "w", encoding="utf-8") as f:
    f.write(text)
with open("metin.txt", "rb") as f:
    data = f.read()
print(f"karakter: {len(text)}, bayt: {len(data)}")
''',
  expectedOutput="karakter: 5, bayt: 7",
  exampleInput="çiçek",
  tests=[
      {"label": "Örnek", "stdin": "çiçek", "expectedOutput": "karakter: 5, bayt: 7"},
      {"label": "ASCII", "stdin": "abc", "expectedOutput": "karakter: 3, bayt: 3"},
      {"label": "Üç baytlık karakter", "stdin": "10€", "expectedOutput": "karakter: 3, bayt: 5"},
      {"label": "Büyük İ", "stdin": "İĞÜ", "expectedOutput": "karakter: 3, bayt: 6"},
  ],
  hints=["\"rb\" ile açılan dosyaya encoding verilmez; read() bytes döndürür.", "Satır sonu yazma; yoksa bayt sayısı bir fazla çıkar."],
  explanation="Türkçe harfler UTF-8'de iki bayttır; çiçek'te iki ç olduğu için 5 karakter 7 bayt eder. Dosya boyutu her zaman bayt cinsindendir.")

q(type="code", topic="csv", sectionId="csv", difficulty=2,
  prompt="Başlangıç kodu girdideki satırları başlığıyla birlikte puan.csv'ye yazar. Dosyayı csv.DictReader ile okuyup en yüksek puanlıyı \"en yüksek: ad (puan)\" ve ortalamayı \"ortalama: X\" (bir ondalık) olarak yazdır. Eşitlikte ilk kişi kazanır.",
  starterCode=r'''
count = int(input())
with open("puan.csv", "w", encoding="utf-8", newline="") as f:
    f.write("ad,puan\n")
    for _ in range(count):
        f.write(input() + "\n")

# DictReader ile oku, en yükseği ve ortalamayı bul
''',
  answer=r'''
import csv

count = int(input())
with open("puan.csv", "w", encoding="utf-8", newline="") as f:
    f.write("ad,puan\n")
    for _ in range(count):
        f.write(input() + "\n")

with open("puan.csv", encoding="utf-8", newline="") as f:
    rows = [(row["ad"], int(row["puan"])) for row in csv.DictReader(f)]
best = max(rows, key=lambda item: item[1])
average = sum(score for _, score in rows) / len(rows)
print(f"en yüksek: {best[0]} ({best[1]})")
print(f"ortalama: {average:.1f}")
''',
  solutionCode=r'''
import csv

count = int(input())
with open("puan.csv", "w", encoding="utf-8", newline="") as f:
    f.write("ad,puan\n")
    for _ in range(count):
        f.write(input() + "\n")

with open("puan.csv", encoding="utf-8", newline="") as f:
    rows = [(row["ad"], int(row["puan"])) for row in csv.DictReader(f)]
best = max(rows, key=lambda item: item[1])
average = sum(score for _, score in rows) / len(rows)
print(f"en yüksek: {best[0]} ({best[1]})")
print(f"ortalama: {average:.1f}")
''',
  expectedOutput="en yüksek: Ada (90)\nortalama: 77.5",
  exampleInput="2\nAda,90\nCan,65",
  tests=[
      {"label": "Örnek", "stdin": "2\nAda,90\nCan,65", "expectedOutput": "en yüksek: Ada (90)\nortalama: 77.5"},
      {"label": "Tırnaklı ad", "stdin": "2\n\"Lin, Can\",80\nEce,70", "expectedOutput": "en yüksek: Lin, Can (80)\nortalama: 75.0"},
      {"label": "Eşitlik", "stdin": "3\nA,50\nB,50\nC,20", "expectedOutput": "en yüksek: A (50)\nortalama: 40.0"},
  ],
  hints=["Puanlar str gelir; int ile çevir.", "max(..., key=...) eşitlikte ilk öğeyi döndürür."],
  explanation="DictReader tırnaklı adı tek alan olarak okur; split kullanılsaydı \"Lin, Can\" bölünürdü. max eşitlikte ilk gördüğünü korur.")

q(type="code", topic="os", sectionId="os-shutil", difficulty=2,
  prompt="safe_write(path, text) fonksiyonunu yaz: dosya varsa önce shutil.copy ile path + \".bak\" yedeğini alsın, sonra text'i yazsın. Girdide n ve n sürüm metni var; hepsi sırayla ayar.txt'ye yazılır. Sonunda güncel içeriği ve yedeği yazdır; yedek yoksa \"yedek yok\" yaz.",
  starterCode=r'''
import os
import shutil

def safe_write(path, text):
    # varsa yedekle, sonra yaz
    pass

count = int(input())
for _ in range(count):
    safe_write("ayar.txt", input())

with open("ayar.txt", encoding="utf-8") as f:
    print("güncel:", f.read())
if os.path.exists("ayar.txt.bak"):
    with open("ayar.txt.bak", encoding="utf-8") as f:
        print("yedek:", f.read())
else:
    print("yedek yok")
''',
  answer=r'''
import os
import shutil

def safe_write(path, text):
    if os.path.exists(path):
        shutil.copy(path, path + ".bak")
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

count = int(input())
for _ in range(count):
    safe_write("ayar.txt", input())

with open("ayar.txt", encoding="utf-8") as f:
    print("güncel:", f.read())
if os.path.exists("ayar.txt.bak"):
    with open("ayar.txt.bak", encoding="utf-8") as f:
        print("yedek:", f.read())
else:
    print("yedek yok")
''',
  solutionCode=r'''
import os
import shutil

def safe_write(path, text):
    if os.path.exists(path):
        shutil.copy(path, path + ".bak")
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

count = int(input())
for _ in range(count):
    safe_write("ayar.txt", input())

with open("ayar.txt", encoding="utf-8") as f:
    print("güncel:", f.read())
if os.path.exists("ayar.txt.bak"):
    with open("ayar.txt.bak", encoding="utf-8") as f:
        print("yedek:", f.read())
else:
    print("yedek yok")
''',
  expectedOutput="güncel: v2\nyedek: v1",
  exampleInput="2\nv1\nv2",
  tests=[
      {"label": "Örnek", "stdin": "2\nv1\nv2", "expectedOutput": "güncel: v2\nyedek: v1"},
      {"label": "İlk yazma", "stdin": "1\nv1", "expectedOutput": "güncel: v1\nyedek yok"},
      {"label": "Üç sürüm", "stdin": "3\na\nb\nc", "expectedOutput": "güncel: c\nyedek: b"},
  ],
  hints=["Yedek, yazmadan önce alınmalı; sonra alınırsa yeni içeriği kopyalar.", "Dosya yoksa kopyalanacak bir şey yoktur; os.path.exists ile sına."],
  explanation="Kopyalama \"w\" açılışından önce yapılmalıdır; \"w\" dosyayı boşalttığı anda eski içerik kaybolur. Yedek her zaman bir önceki sürümü tutar.")

q(type="code", topic="json", sectionId="json", difficulty=2,
  prompt="Başlangıç kodu girdideki metni veri.json'a yazar. Dosyayı json.load ile oku ve her anahtarı alfabetik sırayla \"anahtar: tür\" olarak yazdır (tür, type(değer).__name__). Dosya geçerli JSON değilse \"geçersiz JSON\" yazdır.",
  starterCode=r'''
import json

with open("veri.json", "w", encoding="utf-8") as f:
    f.write(input())

# json.load ile oku, anahtarları ve türleri yazdır
''',
  answer=r'''
import json

with open("veri.json", "w", encoding="utf-8") as f:
    f.write(input())

try:
    with open("veri.json", encoding="utf-8") as f:
        data = json.load(f)
except json.JSONDecodeError:
    print("geçersiz JSON")
else:
    for key in sorted(data):
        print(f"{key}: {type(data[key]).__name__}")
''',
  solutionCode=r'''
import json

with open("veri.json", "w", encoding="utf-8") as f:
    f.write(input())

try:
    with open("veri.json", encoding="utf-8") as f:
        data = json.load(f)
except json.JSONDecodeError:
    print("geçersiz JSON")
else:
    for key in sorted(data):
        print(f"{key}: {type(data[key]).__name__}")
''',
  expectedOutput="ad: str\nnotlar: list\nyas: int",
  exampleInput="{\"yas\": 36, \"ad\": \"Ada\", \"notlar\": [90, 85]}",
  tests=[
      {"label": "Örnek", "stdin": "{\"yas\": 36, \"ad\": \"Ada\", \"notlar\": [90, 85]}", "expectedOutput": "ad: str\nnotlar: list\nyas: int"},
      {"label": "null ve bool", "stdin": "{\"x\": null, \"aktif\": true, \"oran\": 0.5}", "expectedOutput": "aktif: bool\noran: float\nx: NoneType"},
      {"label": "Tek tırnak", "stdin": "{'ad': 'Ada'}", "expectedOutput": "geçersiz JSON"},
      {"label": "Sondaki virgül", "stdin": "{\"a\": 1,}", "expectedOutput": "geçersiz JSON"},
  ],
  hints=["json.JSONDecodeError'u yakala.", "null None'a, true bool'a, 0.5 float'a dönüşür."],
  explanation="json.load JSON türlerini Python türlerine çevirir. Tek tırnak ve sondaki virgül JSON'da geçersizdir ve JSONDecodeError verir; else bloğu yalnızca okuma başarılıysa çalışır.")

# ---- traceback (4)
q(type="traceback", topic="dosya-modu", sectionId="open-modes", difficulty=1,
  prompt="Okunmak istenen dosya hiç oluşturulmamış. Hangi hata oluşur?",
  code=r'''
with open("rapor.txt", encoding="utf-8") as f:
    print(f.read())
''',
  options=["FileNotFoundError", "FileExistsError", "NameError", "ValueError"],
  answer="FileNotFoundError",
  expectedError="FileNotFoundError",
  optionFeedback={
      "FileExistsError": "Bu, \"x\" modunun dosya zaten varken verdiği hatadır; burada dosya yok.",
      "NameError": "open ve f tanımlı; sorun dosya sistemiyle ilgili.",
      "ValueError": "ValueError kapalı dosya ya da geçersiz mod gibi durumlarda çıkar; eksik dosya OSError ailesindendir.",
  },
  hints=["Mod verilmediği için \"r\" kullanılır.", "\"r\" dosyayı oluşturmaz."],
  explanation="Okuma modu dosyanın var olmasını ister. Traceback'in son satırı FileNotFoundError ve bulunamayan yolu gösterir; errno numarası platforma göre değişir.")

q(type="traceback", topic="with", sectionId="with-lifecycle", difficulty=2,
  prompt="Dosya with bloğundan sonra okunuyor. Hangi hata oluşur?",
  code=r'''
with open("a.txt", "w", encoding="utf-8") as f:
    f.write("x")
with open("a.txt", encoding="utf-8") as f:
    first = f.readline()
rest = f.read()
''',
  options=["ValueError", "FileNotFoundError", "OSError", "NameError"],
  answer="ValueError",
  expectedError="ValueError",
  optionFeedback={
      "FileNotFoundError": "Dosya var; sorun dosya nesnesinin kapalı olması.",
      "OSError": "Kapalı dosya işletim sistemi hatası değil, nesnenin yanlış durumda kullanılmasıdır; ValueError verir.",
      "NameError": "f bloktan sonra da tanımlıdır; yalnızca kapalıdır.",
  },
  hints=["Son satır with bloğunun dışında.", "Mesaj: I/O operation on closed file."],
  explanation="with bitince dosya kapandı. Kapalı dosyada okuma ValueError: I/O operation on closed file verir.")

q(type="traceback", topic="encoding", sectionId="encoding", difficulty=2,
  prompt="cp1254 ile yazılmış dosya UTF-8 ile okunuyor. Hangi hata oluşur?",
  code=r'''
with open("eski.txt", "w", encoding="cp1254") as f:
    f.write("şeker")
with open("eski.txt", encoding="utf-8") as f:
    print(f.read())
''',
  options=["UnicodeDecodeError", "UnicodeEncodeError", "FileNotFoundError", "TypeError"],
  answer="UnicodeDecodeError",
  expectedError="UnicodeDecodeError",
  optionFeedback={
      "UnicodeEncodeError": "Encode metinden bayta çevirmektir ve yazarken olur; burada okunurken baytlar çözülemiyor.",
      "FileNotFoundError": "Dosya ilk with bloğunda oluşturuldu.",
      "TypeError": "Türler doğru; sorun baytların UTF-8 kurallarına uymaması.",
  },
  hints=["ş cp1254'te tek bayttır: 0xfe.", "0xfe UTF-8'de hiçbir karakterin başlangıcı olamaz."],
  explanation="Okuma, baytları metne çözmek (decode) demektir. cp1254 baytları UTF-8 olarak çözülemeyince UnicodeDecodeError oluşur; mesaj sorunlu baytı ve konumunu söyler.")

q(type="traceback", topic="json", sectionId="json", difficulty=2,
  prompt="Elle yazılmış JSON tek tırnak içeriyor. Hangi hata oluşur?",
  code=r'''
import json

with open("ayar.json", "w", encoding="utf-8") as f:
    f.write("{'tema': 'koyu'}")
with open("ayar.json", encoding="utf-8") as f:
    print(json.load(f))
''',
  options=["JSONDecodeError", "SyntaxError", "KeyError", "UnicodeDecodeError"],
  answer="JSONDecodeError",
  expectedError="JSONDecodeError",
  optionFeedback={
      "SyntaxError": "SyntaxError Python kodunun kendisi hatalıyken çıkar; buradaki bozuk metin bir veri dosyası.",
      "KeyError": "Hiçbir anahtara erişilmiyor; hata dosya çözümlenirken oluşuyor.",
      "UnicodeDecodeError": "Dosya UTF-8 ile yazılıp okundu; baytlar doğru çözüldü, JSON kuralları ihlal edildi.",
  },
  hints=["JSON'da metinler çift tırnak ister.", "Traceback'te json.decoder.JSONDecodeError görünür."],
  explanation="json.load JSON kurallarına uymayan metinde json.JSONDecodeError verir: Expecting property name enclosed in double quotes. Bu hata ValueError'ın alt sınıfıdır; except ValueError da yakalar.")

assert len(questions) == 40, len(questions)

module = {
    "id": 8,
    "slug": "dosyalar",
    "title": "Dosyalar",
    "description": "Dosyaları doğru modda aç, with ile güvenle kapat, yolları pathlib ile kur; CSV ve JSON verisini doğru encoding ile oku ve yaz.",
    "contentVersion": 1,
    "estimatedMinutes": 120,
    "practiceIds": [f"m8-q{n:02d}" for n in (1, 2, 3, 5, 6, 8, 10, 11, 12, 13, 15, 19, 23, 27, 37)],
    "sections": sections,
    "questions": questions,
}

# Source links and execution labels must survive regeneration.
section_metadata = {
  "open-modes": {
    "sources": [
      {
        "title": "Python 3.12 · open ve dosya modları",
        "url": "https://docs.python.org/3.12/tutorial/inputoutput.html"
      }
    ],
    "runtime": "browser",
    "runtimeNote": "Tarayıcıda geçici sanal dosyalarla çalışır. Dosyalar her çalıştırma sonunda silinir; bilgisayarındaki dosyalara erişilmez."
  },
  "with-lifecycle": {
    "sources": [
      {
        "title": "Python 3.12 · with ve dosya yaşam döngüsü",
        "url": "https://docs.python.org/3.12/reference/compound_stmts.html#the-with-statement"
      }
    ],
    "runtime": "browser",
    "runtimeNote": "Tarayıcıda geçici sanal dosyalarla çalışır. Dosyalar her çalıştırma sonunda silinir; bilgisayarındaki dosyalara erişilmez."
  },
  "reading-lines": {
    "sources": [
      {
        "title": "Python 3.12 · Satır satır okuma",
        "url": "https://docs.python.org/3.12/tutorial/inputoutput.html"
      }
    ],
    "runtime": "browser",
    "runtimeNote": "Tarayıcıda geçici sanal dosyalarla çalışır. Dosyalar her çalıştırma sonunda silinir; bilgisayarındaki dosyalara erişilmez."
  },
  "pathlib": {
    "sources": [
      {
        "title": "Python 3.12 · pathlib ile yollar",
        "url": "https://docs.python.org/3.12/library/pathlib.html"
      }
    ],
    "runtime": "browser",
    "runtimeNote": "Tarayıcıda geçici sanal dosyalarla çalışır. Dosyalar her çalıştırma sonunda silinir; bilgisayarındaki dosyalara erişilmez."
  },
  "os-shutil": {
    "sources": [
      {
        "title": "Python 3.12 · os ve shutil ile dosya işlemleri",
        "url": "https://docs.python.org/3.12/library/shutil.html"
      }
    ],
    "runtime": "browser",
    "runtimeNote": "Tarayıcıda geçici sanal dosyalarla çalışır. Dosyalar her çalıştırma sonunda silinir; bilgisayarındaki dosyalara erişilmez."
  },
  "encoding": {
    "sources": [
      {
        "title": "Python 3.12 · Dosya encoding'i",
        "url": "https://docs.python.org/3.12/howto/unicode.html"
      }
    ],
    "runtime": "browser",
    "runtimeNote": "Tarayıcıda geçici sanal dosyalarla çalışır. Dosyalar her çalıştırma sonunda silinir; bilgisayarındaki dosyalara erişilmez."
  },
  "csv": {
    "sources": [
      {
        "title": "Python 3.12 · CSV okuma ve yazma",
        "url": "https://docs.python.org/3.12/library/csv.html"
      }
    ],
    "runtime": "browser",
    "runtimeNote": "Tarayıcıda geçici sanal dosyalarla çalışır. Dosyalar her çalıştırma sonunda silinir; bilgisayarındaki dosyalara erişilmez."
  },
  "json": {
    "sources": [
      {
        "title": "Python 3.12 · JSON okuma ve yazma",
        "url": "https://docs.python.org/3.12/library/json.html"
      }
    ],
    "runtime": "browser",
    "runtimeNote": "Tarayıcıda geçici sanal dosyalarla çalışır. Dosyalar her çalıştırma sonunda silinir; bilgisayarındaki dosyalara erişilmez."
  }
}
for section in module["sections"]:
    section.update(section_metadata[section["id"]])
module["contentVersion"] = 2
(ROOT / "module-08.json").write_text(json.dumps(module, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

# ---- writing tasks
tasks = []


def task(**fields):
    for key in ("starterCode", "solution", "exampleOutput"):
        fields[key] = c(fields[key])
    for test in fields["tests"]:
        test["expectedOutput"] = c(test["expectedOutput"])
    tasks.append(fields)


task(
    id="m8-w1", moduleId=8, sectionId="reading-lines",
    title="Yapılacaklar listesini oku", level="Tamamla",
    objective="Bir dosyayı satır satır okuyup satırları biçimlerine göre ayır.",
    prompt="Başlangıç kodu girdideki satırları yapilacak.txt dosyasına yazar. Her satır \"[x] iş\" (tamamlanmış) ya da \"[ ] iş\" (bekleyen) biçimindedir; boş satırlar atlanır. read_tasks(path) fonksiyonunu tamamla: dosyayı with ile açıp (tamamlanan, bekleyen) listelerini döndürsün. Program \"tamamlanan: X/Y\" ve bekleyenleri virgülle ayırarak \"bekleyen: ...\" yazdırır; bekleyen yoksa \"bekleyen: yok\".",
    starterCode=r'''
count = int(input())
with open("yapilacak.txt", "w", encoding="utf-8") as f:
    for _ in range(count):
        f.write(input() + "\n")

def read_tasks(path):
    done, pending = [], []
    # dosyayı satır satır oku; "[x] " ile başlayanı done'a, "[ ] " ile başlayanı pending'e ekle
    return done, pending

done, pending = read_tasks("yapilacak.txt")
total = len(done) + len(pending)
print(f"tamamlanan: {len(done)}/{total}")
print("bekleyen:", ", ".join(pending) if pending else "yok")
''',
    exampleInput="3\n[x] süt al\n[ ] fatura öde\n[ ] spor",
    exampleOutput="tamamlanan: 1/3\nbekleyen: fatura öde, spor",
    hints=[
        "Her satırı önce strip() ile temizle; boş kaldıysa atla.",
        "line.startswith(\"[x] \") ve line[4:] ile işin adını al.",
    ],
    solution=r'''
count = int(input())
with open("yapilacak.txt", "w", encoding="utf-8") as f:
    for _ in range(count):
        f.write(input() + "\n")

def read_tasks(path):
    done, pending = [], []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith("[x] "):
                done.append(line[4:])
            elif line.startswith("[ ] "):
                pending.append(line[4:])
    return done, pending

done, pending = read_tasks("yapilacak.txt")
total = len(done) + len(pending)
print(f"tamamlanan: {len(done)}/{total}")
print("bekleyen:", ", ".join(pending) if pending else "yok")
''',
    tests=[
        {"label": "Örnek", "stdin": "3\n[x] süt al\n[ ] fatura öde\n[ ] spor", "expectedOutput": "tamamlanan: 1/3\nbekleyen: fatura öde, spor"},
        {"label": "Hepsi bitti", "stdin": "2\n[x] a\n[x] b", "expectedOutput": "tamamlanan: 2/2\nbekleyen: yok"},
        {"label": "Boş satırlar", "stdin": "4\n\n[ ] kitap oku\n   \n[x] yürü", "expectedOutput": "tamamlanan: 1/2\nbekleyen: kitap oku"},
        {"label": "Boş liste", "stdin": "0", "expectedOutput": "tamamlanan: 0/0\nbekleyen: yok"},
    ],
)

task(
    id="m8-w2", moduleId=8, sectionId="open-modes",
    title="Not defterini onar", level="Düzelt",
    objective="Dosya modu, satır sonu ve eksik dosya hatalarını bulup düzelt.",
    prompt="İlk satırda not sayısı, sonra her satırda bir not var. Her not notlar.txt dosyasına ayrı satır olarak eklenmeli; sonra dosya okunup \"N not\" ve numaralı notlar yazdırılmalı. Hiç not eklenmemişse dosya da yoktur; program yine \"0 not\" yazmalı. Başlangıç kodunda üç sorun var: notlar birbirini siliyor, satırlar birleşiyor ve not yokken program çöküyor. Dosyaların with ile kapatıldığından da emin ol.",
    starterCode=r'''
def add_note(path, note):
    f = open(path, "w", encoding="utf-8")
    f.write(note)
    f.close()

def read_notes(path):
    with open(path, encoding="utf-8") as f:
        return f.read().splitlines()

count = int(input())
for _ in range(count):
    add_note("notlar.txt", input().strip())

notes = read_notes("notlar.txt")
print(len(notes), "not")
for number, note in enumerate(notes, start=1):
    print(f"{number}. {note}")
''',
    exampleInput="2\nekmek al\nfaturayı öde",
    exampleOutput="2 not\n1. ekmek al\n2. faturayı öde",
    hints=[
        "\"w\" her açılışta dosyayı boşaltır; ekleme modu \"a\"dır. write satır sonu eklemez.",
        "read_notes içinde FileNotFoundError'u yakalayıp boş liste döndür.",
    ],
    solution=r'''
def add_note(path, note):
    with open(path, "a", encoding="utf-8") as f:
        f.write(note + "\n")

def read_notes(path):
    try:
        with open(path, encoding="utf-8") as f:
            return f.read().splitlines()
    except FileNotFoundError:
        return []

count = int(input())
for _ in range(count):
    add_note("notlar.txt", input().strip())

notes = read_notes("notlar.txt")
print(len(notes), "not")
for number, note in enumerate(notes, start=1):
    print(f"{number}. {note}")
''',
    tests=[
        {"label": "Örnek", "stdin": "2\nekmek al\nfaturayı öde", "expectedOutput": "2 not\n1. ekmek al\n2. faturayı öde"},
        {"label": "Hiç not yok", "stdin": "0", "expectedOutput": "0 not"},
        {"label": "Tek not", "stdin": "1\n  boşluklu not  ", "expectedOutput": "1 not\n1. boşluklu not"},
        {"label": "Üç not", "stdin": "3\na\nb\nc", "expectedOutput": "3 not\n1. a\n2. b\n3. c"},
    ],
)

task(
    id="m8-w3", moduleId=8, sectionId="json",
    title="CSV'den JSON rapor", level="Sıfırdan yaz",
    objective="CSV verisini dosyadan okuyup doğrula, özetle ve JSON rapor dosyası üret.",
    prompt="İlk satırda kayıt sayısı n, sonra n CSV satırı var: ad,departman,maaş. Ad tırnaklı olup virgül içerebilir. Programın şu adımları izlemeli: (1) satırları \"ad,departman,maas\" başlığıyla personel.csv dosyasına yaz; (2) dosyayı csv.DictReader ile oku; (3) departmanı boş ya da maaşı yalnızca rakamlardan oluşmayan kayıtları hatalı say ve atla; (4) {\"departmanlar\": {departman: {\"kişi\": k, \"toplam\": t}}, \"hatalı\": h} raporunu rapor.json'a json.dump ile ensure_ascii=False ve sort_keys=True kullanarak yaz; (5) rapor.json'u metin olarak okuyup yazdır. Departman ve maaştaki uç boşluklar temizlenir.",
    starterCode=r'''
import csv
import json

count = int(input())
lines = [input() for _ in range(count)]

# 1) personel.csv'ye başlıkla birlikte yaz
# 2) DictReader ile oku, hatalı kayıtları say
# 3) raporu rapor.json'a yaz, sonra dosyayı okuyup yazdır
''',
    exampleInput="3\nAda,Satış,100\n\"Lin, Can\",Satış,200\nEce,,150",
    exampleOutput='{"departmanlar": {"Satış": {"kişi": 2, "toplam": 300}}, "hatalı": 1}',
    hints=[
        "CSV dosyasını yazarken ve okurken newline=\"\" ve encoding=\"utf-8\" kullan; satırlar zaten CSV biçiminde olduğundan olduğu gibi yazılabilir.",
        "report[\"departmanlar\"].setdefault(dept, {\"kişi\": 0, \"toplam\": 0}) ile departmanı ilk görüşte oluştur; maaş için salary.isdigit().",
    ],
    solution=r'''
import csv
import json

count = int(input())
lines = [input() for _ in range(count)]

with open("personel.csv", "w", encoding="utf-8", newline="") as f:
    f.write("ad,departman,maas\n")
    for line in lines:
        f.write(line + "\n")

report = {"departmanlar": {}, "hatalı": 0}
with open("personel.csv", encoding="utf-8", newline="") as f:
    for row in csv.DictReader(f):
        dept = (row["departman"] or "").strip()
        salary = (row["maas"] or "").strip()
        if not dept or not salary.isdigit():
            report["hatalı"] += 1
            continue
        summary = report["departmanlar"].setdefault(dept, {"kişi": 0, "toplam": 0})
        summary["kişi"] += 1
        summary["toplam"] += int(salary)

with open("rapor.json", "w", encoding="utf-8") as f:
    json.dump(report, f, ensure_ascii=False, sort_keys=True)
with open("rapor.json", encoding="utf-8") as f:
    print(f.read())
''',
    tests=[
        {"label": "Örnek", "stdin": "3\nAda,Satış,100\n\"Lin, Can\",Satış,200\nEce,,150", "expectedOutput": '{"departmanlar": {"Satış": {"kişi": 2, "toplam": 300}}, "hatalı": 1}'},
        {"label": "İki departman", "stdin": "3\nBo,İK,50\nAl,Ar-Ge,70\nCe,İK,30", "expectedOutput": '{"departmanlar": {"Ar-Ge": {"kişi": 1, "toplam": 70}, "İK": {"kişi": 2, "toplam": 80}}, "hatalı": 0}'},
        {"label": "Geçersiz maaş", "stdin": "3\nDa,Satış,abc\nEl,Satış,-5\nFe, Satış , 40 ", "expectedOutput": '{"departmanlar": {"Satış": {"kişi": 1, "toplam": 40}}, "hatalı": 2}'},
        {"label": "Kayıt yok", "stdin": "0", "expectedOutput": '{"departmanlar": {}, "hatalı": 0}'},
        {"label": "Eksik alan", "stdin": "2\nGe,Satış\nHa,Satış,10", "expectedOutput": '{"departmanlar": {"Satış": {"kişi": 1, "toplam": 10}}, "hatalı": 1}'},
    ],
)

tasks_path = ROOT / "writing-tasks.json"
existing = [t for t in json.loads(tasks_path.read_text(encoding="utf-8")) if t["moduleId"] != 8]
tasks_path.write_text(json.dumps(existing + tasks, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("module-08.json ve", len(tasks), "yazma görevi yazıldı")
