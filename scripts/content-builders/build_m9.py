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


SITE_NOTE = "Bu sitede kod tek bir dosyada çalıştığı için örnekler, gerçek projede ayrı dosyalarda duracak modülleri önce Path.write_text ile kendileri oluşturur; her çalıştırma boş bir klasörde başlar."

section(
    id="import-forms",
    title="import biçimleri",
    eyebrow="Başka bir dosyadaki kodu ada bağla",
    objectives=[
        "import x, from x import y ve as biçimlerinin hangi adı tanımladığını belirler.",
        "Bir modülün içindeki ada nokta ile erişir ve import satırlarını düzenli sıralar.",
    ],
    prerequisites=["m6:def-return"],
    summary="Modül, Python kodu içeren bir dosyadır. import math math modülünü yükleyip math adına bağlar; from math import sqrt yalnızca sqrt adını getirir; as ile takma ad verilir.",
    explanation="import modül_adı modülü yükler ve geçerli dosyada o adı modül nesnesine bağlar; içeriğe modül.ad ile erişilir. from modül import ad yalnızca o adı getirir; modül adı tanımlanmaz. as takma ad verir: import datetime as dt. from modül import * modüldeki her adı dosyana döker, hangi adın nereden geldiğini gizler ve aynı adlı değişkenleri ezer; kendi kodunda kullanma. İmport satırları dosyanın en üstüne yazılır ve gelenek gereği üç gruba ayrılır: standart kütüphane, sonradan kurulan paketler, projenin kendi modülleri. import da bir atamadır: aynı adlı bir değişken tanımlarsan modül adı ezilir.",
    code=r'''
import math
from statistics import mean, median
import datetime as dt

print(math.sqrt(16), math.pi > 3)
print(mean([2, 4, 9]), median([2, 4, 9]))
print(dt.date(2026, 10, 6).isoformat())
print(type(math).__name__, math.__name__)
''',
    expectedOutput=r'''
4.0 True
5 4
2026-10-06
module math
''',
    why="math modül adıyla, mean ve median doğrudan adlarıyla, datetime ise dt takma adıyla kullanıldı. Modül de bir nesnedir: türü module, gerçek adı math'tir. mean tam sayılarda sonuç tam bölünüyorsa int döndürür.",
    alternatives=[
        "Bir modülden çok ad kullanıyorsan import modül ile modül.ad yazmak, adın nereden geldiğini açık tutar.",
        "Uzun modül adlarında topluluğun yerleşik takma adlarını kullan (import numpy as np); kendi kısaltmalarını uydurma.",
    ],
    traps=[
        "from math import sqrt yazdıktan sonra math.pi kullanmaya çalışmak; math adı tanımlanmadı.",
        "from x import * ile adların nereden geldiğini kaybetmek.",
        "Modülle aynı adı taşıyan bir değişken tanımlayıp modülü ezmek (ör. math = 5).",
    ],
    realCode=r'''
import json
from pathlib import Path
from statistics import mean

def summarize(path):
    scores = json.loads(Path(path).read_text(encoding="utf-8"))
    return {name: round(mean(values), 1) for name, values in scores.items()}

Path("notlar.json").write_text('{"Ada": [90, 85], "Can": [70, 76, 79]}', encoding="utf-8")
print(summarize("notlar.json"))
''',
    realOutput=r'''
{'Ada': 87.5, 'Can': 75}
''',
    lineByLine=[
        "İmportlar en üstte: json ve pathlib standart kütüphaneden, mean statistics modülünden.",
        "summarize dosyayı Path ile okur, JSON'u çözer ve her kişinin ortalamasını hesaplar.",
        "Örnek veri dosyası oluşturulur; gerçekte başka bir programdan gelirdi.",
        "Can'ın notları tam bölündüğü için mean 75 (int) döndürür; round onu değiştirmez.",
    ],
)

section(
    id="own-module",
    title="Kendi modülün",
    eyebrow="Bir .py dosyası, bir modül",
    objectives=[
        "Kendi .py dosyasını modül olarak import eder ve modül kodunun yalnızca ilk importta çalıştığını açıklar.",
        "Python'un modülü nerede aradığını (sys.path) ve standart kütüphaneyle aynı adı taşıyan dosyanın sorununu açıklar.",
    ],
    prerequisites=["import-forms", "m8:pathlib"],
    summary="Aynı klasördeki selam.py dosyası import selam ile kullanılabilir. Modül ilk importta baştan sona çalışır; sonuç sys.modules'te saklanır ve sonraki importlar aynı modül nesnesini verir.",
    explanation="Modülün adı dosya adının .py'siz hâlidir; bu yüzden dosya adları geçerli Python adı olmalıdır (rapor-araci.py import edilemez, rapor_araci.py edilir). Python modülü sys.path listesindeki klasörlerde sırayla arar; ilk sırada çalıştırılan programın klasörü vardır, ardından standart kütüphane ve kurulu paketler gelir. Bu sıra yüzünden kendi dosyana random.py ya da csv.py adını verirsen import random standart kütüphane yerine senin dosyanı bulur. İlk import modül kodunu çalıştırır (en üst düzeydeki print'ler dahil) ve modülü sys.modules'e koyar; ikinci import kodu yeniden çalıştırmaz. from modül import sayı yazmak modüldeki değeri kendi dosyanda yeni bir ada bağlar; modül o değişkeni sonra değiştirirse senin adın eski değeri gösterir. Paylaşılan durumu modül.ad ile oku. " + SITE_NOTE,
    code=r'''
from pathlib import Path

Path("selam.py").write_text("""print("selam.py yükleniyor")
GREETING = "Merhaba"

def greet(name):
    return f"{GREETING}, {name}!"
""", encoding="utf-8")

import selam
import selam
print(selam.greet("Ada"))
print(selam.GREETING)
''',
    expectedOutput=r'''
selam.py yükleniyor
Merhaba, Ada!
Merhaba
''',
    why="Gerçek projede selam.py ayrı bir dosyadır; burada program onu önce yazıyor. İlk import modülü çalıştırdı ve yükleniyor mesajı bir kez göründü; ikinci import sys.modules'teki hazır modülü verdi. Fonksiyon ve değişken modül adıyla kullanıldı.",
    alternatives=[
        "Modül büyüdükçe ilgili modülleri bir pakette (klasörde) toplamak; bu modülün ileriki bölümünde.",
        "Değiştirdiğin modülü etkileşimli oturumda yeniden yüklemek için importlib.reload(modül) vardır; programlarda gerekmez.",
    ],
    traps=[
        "Dosyaya standart kütüphaneyle aynı ad vermek (random.py, csv.py, json.py).",
        "Modül en üst düzeyinde ağır iş ya da print bırakıp her import edenin onu çalıştırmasına yol açmak.",
        "from modül import sayac ile alınan değerin modüldeki değişiklikleri izlediğini sanmak.",
        "Dosya adında tire ya da Türkçe karakter kullanıp import ederken yazımı karıştırmak.",
    ],
    realCode=r'''
from pathlib import Path

Path("ayarlar.py").write_text("""DEBUG = False
""", encoding="utf-8")
Path("rapor.py").write_text("""import ayarlar

def header():
    return "[DEBUG] rapor" if ayarlar.DEBUG else "rapor"
""", encoding="utf-8")

import ayarlar
import rapor

print(rapor.header())
ayarlar.DEBUG = True
print(rapor.header())

import sys
print(sys.modules["ayarlar"] is ayarlar)
''',
    realOutput=r'''
rapor
[DEBUG] rapor
True
''',
    lineByLine=[
        "İki modül oluşturulur: ayarlar.py bir bayrak tutar, rapor.py onu import edip kullanır.",
        "rapor.header bayrağı her çağrıda ayarlar.DEBUG ile modül üzerinden okur.",
        "Ana program bayrağı değiştirince rapor da yeni değeri görür; ikisi aynı modül nesnesini paylaşır.",
        "sys.modules'teki kayıt, ana programın elindeki ayarlar nesnesinin ta kendisidir.",
    ],
)

section(
    id="main-guard",
    title="__name__ == \"__main__\"",
    eyebrow="Hem çalıştırılabilir hem import edilebilir dosya",
    objectives=[
        "Bir dosyanın doğrudan çalıştırıldığında ve import edildiğinde __name__ değerini belirler.",
        "Deneme ve başlatma kodunu if __name__ == \"__main__\": bloğuna alarak modülü yan etkisiz import edilebilir yapar.",
    ],
    prerequisites=["own-module"],
    summary="Python her modüle __name__ adlı bir değişken verir. Dosya doğrudan çalıştırılırsa (python araclar.py) değeri \"__main__\", import edilirse modülün adıdır. if __name__ == \"__main__\": bloğu yalnızca doğrudan çalıştırmada çalışır.",
    explanation="Bir dosya hem başka dosyalara fonksiyon sağlayıp hem de tek başına çalışabilir. Başlatma kodu (input okumak, main() çağırmak, deneme çıktıları) korumasız bırakılırsa, dosyayı import eden herkes o kodu da çalıştırır. Yaygın düzen: tüm işi fonksiyonlara koy, programı main() içinde başlat ve dosyanın sonunda if __name__ == \"__main__\": main() yaz. Böylece testler ve diğer modüller fonksiyonları yan etkisiz import edebilir. Bu sitede yazdığın kod her zaman __main__ olarak çalışır. Aşağıdaki örnek, terminalde python araclar.py çalıştırmayı runpy.run_path(\"araclar.py\", run_name=\"__main__\") ile taklit ediyor.",
    code=r'''
import runpy
from pathlib import Path

Path("araclar.py").write_text("""def double(x):
    return x * 2

print("araclar.py içinde __name__ =", __name__)

if __name__ == "__main__":
    print("doğrudan çalıştırıldı, deneme:", double(21))
""", encoding="utf-8")

import araclar
print("import sonrası:", araclar.double(5))
runpy.run_path("araclar.py", run_name="__main__")
''',
    expectedOutput=r'''
araclar.py içinde __name__ = araclar
import sonrası: 10
araclar.py içinde __name__ = __main__
doğrudan çalıştırıldı, deneme: 42
''',
    why="import edilince __name__ modülün adı olan araclar'dı ve korumalı blok atlandı; yalnızca korumasız print çalıştı. run_path dosyayı terminalden çalıştırılmış gibi __main__ adıyla yürüttü; bu kez korumalı blok da çalıştı.",
    alternatives=[
        "Paket içindeki bir modülü çalıştırmak için python -m paket.modul kullanılır; bu durumda da __name__ \"__main__\" olur.",
        "Komut satırı aracı olarak dağıtılan paketlerde başlangıç noktası pyproject.toml'daki [project.scripts] ile tanımlanır.",
    ],
    traps=[
        "Deneme print'lerini korumasız bırakıp modülü import eden her programda fazladan çıktı üretmek.",
        "\"__main__\" yazarken alt çizgi sayısını eksik yazmak; koşul hiç doğru olmaz ve program sessizce hiçbir şey yapmaz.",
        "Tüm programı fonksiyon yerine korumalı bloğun içine yazmak; o kod hiçbir yerden yeniden kullanılamaz.",
    ],
    realCode=r'''
def parse_scores(text):
    return [int(part) for part in text.split(",")]

def main():
    scores = parse_scores("70,85,90")
    print(f"{len(scores)} not, ortalama {sum(scores) / len(scores):.1f}")

if __name__ == "__main__":
    main()
''',
    realOutput=r'''
3 not, ortalama 81.7
''',
    lineByLine=[
        "İş, test edilebilir küçük bir fonksiyonda: parse_scores metni sayı listesine çevirir.",
        "main programın akışını toplar; gerçek bir programda veriyi input ya da dosyadan okurdu.",
        "Korumalı blok yalnızca dosya doğrudan çalıştırıldığında main'i çağırır.",
        "Bu sitede kod __main__ olarak çalıştığından main çalıştı; başka bir dosya parse_scores'u import etseydi hiçbir çıktı oluşmazdı.",
    ],
)

section(
    id="packages-relative",
    title="Paketler ve relative import",
    eyebrow="Modülleri klasörde topla",
    objectives=[
        "__init__.py içeren bir klasörü paket olarak import eder; noktalı modül yollarını okur.",
        "from .modul import ad biçimini okur ve paket içindeki modülün neden python -m ile çalıştırılması gerektiğini açıklar.",
    ],
    prerequisites=["main-guard"],
    summary="Paket, modülleri içeren bir klasördür; __init__.py paketin başlangıç dosyasıdır. Paket içindeki modüller birbirini from .modul import ad (relative) ya da from paket.modul import ad (absolute) ile import eder.",
    explanation="import magaza.fiyat önce magaza paketinin __init__.py dosyasını, sonra fiyat modülünü çalıştırır. __init__.py boş olabilir ya da dışarıya sunmak istediğin adları içe aktarabilir; böylece kullanıcı from magaza.fiyat import with_tax yerine magaza.with_tax yazabilir. Relative importta tek nokta aynı paketi, iki nokta üst paketi gösterir. Relative import yalnızca modül bir paketin parçası olarak yüklendiğinde çalışır. Paket içindeki bir dosyayı python app/cli.py ile doğrudan çalıştırırsan Python onu paketsiz tek bir dosya sayar ve ImportError: attempted relative import with no known parent package verir. Doğrusu proje kökünden python -m app.cli çalıştırmaktır. Küçük projelerde absolute import (from app.core import add) çoğu zaman daha açıktır. Bu sitede python -m komutu runpy.run_module ile taklit ediliyor.",
    code=r'''
from pathlib import Path

Path("magaza").mkdir()
Path("magaza/__init__.py").write_text("""from .fiyat import with_tax
""", encoding="utf-8")
Path("magaza/fiyat.py").write_text("""from .oranlar import KDV

def with_tax(price):
    return round(price * (1 + KDV), 2)
""", encoding="utf-8")
Path("magaza/oranlar.py").write_text("""KDV = 0.20
""", encoding="utf-8")

import magaza
from magaza.oranlar import KDV
print(magaza.with_tax(100), KDV)
''',
    expectedOutput=r'''
120.0 0.2
''',
    why="import magaza __init__.py'yi çalıştırdı; __init__ with_tax'ı fiyat modülünden, fiyat da KDV'yi oranlar modülünden relative import ile aldı. Kullanıcı yalnızca magaza.with_tax yazdı; iç yapıyı bilmesi gerekmedi. Alt modüle noktalı yolla da doğrudan ulaşılabilir.",
    alternatives=[
        "Relative yerine absolute import: from magaza.oranlar import KDV. Aynı işi yapar, dosya taşındığında daha kolay okunur ama paket adı değişirse güncellenmelidir.",
        "Büyük projelerde kod src/paket_adi/ altında tutulur (src düzeni); böylece testler kurulmuş paketi kullanır.",
    ],
    traps=[
        "Paket içindeki bir dosyayı python paket/modul.py ile çalıştırıp relative import hatası almak.",
        "Paket klasörüne standart kütüphaneyle aynı ad vermek.",
        "__init__.py'de ağır işler yapıp paketin her importunu yavaşlatmak.",
    ],
    realCode=r'''
import runpy
from pathlib import Path

Path("app").mkdir()
Path("app/__init__.py").write_text("", encoding="utf-8")
Path("app/core.py").write_text("""def add(a, b):
    return a + b
""", encoding="utf-8")
Path("app/cli.py").write_text("""from .core import add
print("sonuç:", add(2, 3))
""", encoding="utf-8")

try:
    runpy.run_path("app/cli.py")  # python app/cli.py
except ImportError as error:
    print("dosya olarak:", error)
runpy.run_module("app.cli", run_name="__main__")  # python -m app.cli
''',
    realOutput=r'''
dosya olarak: attempted relative import with no known parent package
sonuç: 5
''',
    lineByLine=[
        "Küçük bir uygulama paketi kurulur: core hesap yapar, cli komut satırı girişidir ve core'u relative import eder.",
        "Dosyayı yolu ile çalıştırmak (python app/cli.py) modülü paketsiz bırakır; .core çözülemez.",
        "Hata yakalanıp mesajı gösterilir; gerçek terminalde aynı mesajı traceback olarak görürsün.",
        "Modül adıyla çalıştırmak (python -m app.cli) paketi tanır ve relative import çalışır.",
    ],
)

section(
    id="pip-venv",
    title="pip ve venv",
    eyebrow="Her projeye kendi Python ortamı",
    objectives=[
        "Sanal ortam oluşturma, etkinleştirme ve içine paket kurma adımlarını sırasıyla uygular.",
        "ModuleNotFoundError'ın kod hatası mı yoksa eksik ya da yanlış ortama kurulmuş paket mi olduğunu ayırır.",
    ],
    prerequisites=["own-module"],
    summary="venv, bir projenin paketlerini sistemdeki diğer projelerden ayıran sanal ortamdır. pip paketleri PyPI'dan o ortama kurar. Paketi her zaman kodu çalıştıracak Python ile kur: python -m pip install paket.",
    explanation="Önerilen başlangıç akışı: proje klasöründe python -m venv .venv ile ortamı oluştur; Windows'ta .venv\\Scripts\\activate, macOS/Linux'ta source .venv/bin/activate ile etkinleştir (komut satırının başında (.venv) görünür); python -m pip install requests ile kur; çıkarken deactivate. Etkin ortamda python ve pip o ortamın kopyalarıdır; paketler .venv içindeki site-packages klasörüne gider. Yalnızca pip install yazmak, PATH'te önce hangi pip bulunuyorsa ona kurar ve bu, programı çalıştıran python olmayabilir; python -m pip bu karışıklığı önler. Kurduğun paket ModuleNotFoundError veriyorsa önce doğru ortamın etkin olduğunu kontrol et. Programın içinden sys.prefix != sys.base_prefix ise bir sanal ortamdasın. .venv klasörü projeyle paylaşılmaz (git'e eklenmez); bağımlılıklar bir sonraki bölümdeki dosyalarla kaydedilir ve ortam her makinede yeniden kurulur. Paketin kurulum adı ile import adı farklı olabilir: pillow → PIL, beautifulsoup4 → bs4, python-dotenv → dotenv. Bu site tarayıcıda çalışan Pyodide kullanır; pip ve venv burada yoktur. Aşağıdaki örnekler bir modülün kurulu olup olmadığını importlib.util.find_spec ile, modülü yüklemeden sınar.",
    code=r'''
import importlib.util

for name in ["json", "csv", "olmayan_paket"]:
    spec = importlib.util.find_spec(name)
    print(name, "kurulu" if spec is not None else "bulunamadı")
''',
    expectedOutput=r'''
json kurulu
csv kurulu
olmayan_paket bulunamadı
''',
    why="find_spec modülü sys.path'te arar ama çalıştırmaz. json ve csv standart kütüphanededir; olmayan_paket hiçbir yerde yoktur ve None döner. Gerçek bir projede kurulmamış bir paket de aynı şekilde None verir ve import edilince ModuleNotFoundError oluşur.",
    alternatives=[
        "Ortamı ve kurulumları hızlandıran uv gibi araçlar aynı adımları tek komutla yapar; modülün ilerleyen bölümünde.",
        "Kurulu paketleri ve sürümlerini görmek için python -m pip list, ayrıntı için python -m pip show paket.",
    ],
    traps=[
        "Paketi sistem Python'una kurup programı sanal ortamdaki Python ile çalıştırmak (ya da tersi).",
        "Kurulum adıyla import etmeye çalışmak (import beautifulsoup4).",
        ".venv klasörünü git deposuna eklemek ya da başka bir makineye kopyalamak.",
        "ModuleNotFoundError'ı kod hatası sanıp kodu değiştirmek; çoğu zaman sorun ortamdadır.",
    ],
    realCode=r'''
import importlib.util

REQUIRED = [("json", None), ("iz_grafik", "iz-grafik"), ("iz_veri", "iz-veri")]

def check(requirements):
    missing = [pip_name for module, pip_name in requirements
               if importlib.util.find_spec(module) is None]
    if missing:
        print("eksik:", ", ".join(missing))
        print("kur:", "python -m pip install", " ".join(missing))
    else:
        print("tüm bağımlılıklar hazır")

check(REQUIRED)
''',
    realOutput=r'''
eksik: iz-grafik, iz-veri
kur: python -m pip install iz-grafik iz-veri
''',
    lineByLine=[
        "Her bağımlılık (import adı, kurulum adı) çifti olarak tutulur; standart kütüphanenin kurulum adı yoktur. iz-grafik ve iz-veri örnek için uydurulmuş paketlerdir.",
        "find_spec None döndüren modüllerin kurulum adları toplanır.",
        "Eksik varsa kullanıcıya hangi paketlerin eksik olduğu ve doğru kurulum komutu gösterilir.",
        "Komut python -m pip biçimindedir: paket, programı çalıştıran Python'a kurulur.",
    ],
)

section(
    id="dependency-files",
    title="requirements.txt ve pyproject.toml",
    eyebrow="Bağımlılıkları dosyaya yaz, ortamı yeniden kur",
    objectives=[
        "requirements.txt ve pyproject.toml'daki bağımlılık satırlarını ve sürüm belirteçlerini (==, >=, <, ~=) okur.",
        "tomllib ile pyproject.toml'u okuyup proje adını, Python sürümünü ve bağımlılıkları çıkarır.",
    ],
    prerequisites=["pip-venv", "m8:reading-lines"],
    summary="requirements.txt her satırda bir paket ve isteğe bağlı sürüm kısıtı içeren düz bir listedir; python -m pip install -r requirements.txt ile kurulur. pyproject.toml projenin adını, sürümünü, Python gereksinimini ve bağımlılıklarını tanımlayan güncel standart dosyadır.",
    explanation="Sürüm belirteçleri: ==2.32.3 tam sürüm, >=2.31 en az, <3 üst sınır, !=2.30 hariç, ~=13.7 uyumlu sürüm (>=13.7 ve <14 demektir; ~=2.31.0 ise >=2.31.0 ve <2.32). Virgül kısıtları birleştirir: requests>=2.31,<3. Köşeli parantez ek özellikleri (requests[socks]), noktalı virgül koşulları belirtir (tomli; python_version < \"3.11\"). requirements.txt'de # yorumdur. python -m pip freeze > requirements.txt ortamdaki her paketi tam sürümüyle yazar; bu, ortamın aynısını kurmaya yarar ama elle yazılmış bir bağımlılık listesi değildir. pyproject.toml'da [project] tablosu name, version, requires-python ve dependencies alanlarını, [project.optional-dependencies] isteğe bağlı grupları tutar. Uygulamalarda tam sürümleri sabitleyen bir kilit dosyası (lock file) ayrıca tutulur. Python 3.11'den beri standart kütüphanedeki tomllib TOML okur; dosyayı \"rb\" (ikili) modunda ister.",
    code=r'''
import tomllib

pyproject = """
[project]
name = "not-defteri"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
    "requests>=2.31,<3",
    "rich~=13.7",
]

[project.optional-dependencies]
test = ["pytest>=8"]
"""
data = tomllib.loads(pyproject)
project = data["project"]
print(project["name"], project["version"], project["requires-python"])
print(project["dependencies"])
print(project["optional-dependencies"]["test"])
''',
    expectedOutput=r'''
not-defteri 0.1.0 >=3.12
['requests>=2.31,<3', 'rich~=13.7']
['pytest>=8']
''',
    why="tomllib.loads TOML metnini iç içe sözlüğe çevirdi: [project] bir sözlük, [project.optional-dependencies] onun içinde başka bir sözlüktür. Bağımlılıklar sürüm kısıtlarıyla birlikte düz metin olarak durur; requests için 2.31 ile 3 arası, rich için 13.7 ve sonrası ama 14'ten önce kabul edilir.",
    alternatives=[
        "Kısıtları gerçekten karşılaştırmak için packaging kütüphanesi (packaging.requirements, packaging.version) kullanılır; pip de onu kullanır.",
        "Dosyadan okumak: with open(\"pyproject.toml\", \"rb\") as f: data = tomllib.load(f).",
    ],
    traps=[
        "Tam sürüm için tek = yazmak (requests=2.32.3); doğrusu ==.",
        "tomllib.load'a metin modunda açılmış dosya vermek; TypeError alırsın.",
        "pip freeze çıktısını elle yazılmış bağımlılık listesiyle karıştırmak; dolaylı bağımlılıklar da listeye girer.",
        "Kısıtsız bağımlılıklarla bir uygulamayı yayımlamak; yarın kurulan yeni sürüm kodu bozabilir.",
    ],
    realCode=r'''
text = """# web
requests==2.32.3
Flask>=3.0  # sunucu

python-dotenv
"""

def parse_requirements(text):
    result = {}
    for line in text.splitlines():
        line = line.split("#", 1)[0].strip()
        if not line:
            continue
        for index, char in enumerate(line):
            if char in "=<>!~[; ":
                result[line[:index].lower()] = line[index:].strip()
                break
        else:
            result[line.lower()] = ""
    return result

for name, spec in parse_requirements(text).items():
    print(name, "→", spec or "(sürüm serbest)")
''',
    realOutput=r'''
requests → ==2.32.3
flask → >=3.0
python-dotenv → (sürüm serbest)
''',
    lineByLine=[
        "Yorumlar # işaretinden itibaren atılır, boş satırlar geçilir.",
        "Paket adı, ilk kısıt ya da özel karakterin görüldüğü yere kadar olan kısımdır; geri kalanı kısıttır.",
        "Döngü hiç kırılmazsa (for-else) satırda kısıt yoktur; sürüm serbest bırakılmıştır.",
        "Adlar küçük harfe çevrilir; pip paket adlarında büyük/küçük harf ayırmaz.",
    ],
)

section(
    id="uv-poetry",
    title="uv ve poetry",
    eyebrow="Aynı işi otomatikleştiren araçlar",
    objectives=[
        "Bir projenin hangi araçla yönetildiğini dosyalarına (uv.lock, poetry.lock, requirements.txt) bakarak tanır.",
        "uv ve poetry'nin venv, pip ve kilit dosyası adımlarından hangilerini üstlendiğini açıklar.",
    ],
    prerequisites=["dependency-files"],
    summary="uv ve poetry, venv + pip + bağımlılık dosyası işlerini tek araçta toplar: ortamı kendileri kurar, pyproject.toml'u günceller ve tam sürümleri bir kilit dosyasına yazar. Yeni bir depoda önce hangi aracın kullanıldığını bul ve onunla devam et.",
    explanation="Aynı iş üç araçla: (1) pip + venv: python -m venv .venv, python -m pip install requests, bağımlılığı requirements.txt ya da pyproject.toml'a elle ekle. (2) uv: uv init, uv add requests (pyproject.toml'a ekler, .venv'i ve uv.lock'u günceller), uv run app.py (ortamı hazırlayıp çalıştırır), uv sync (kilit dosyasındaki ortamı kurar). (3) poetry: poetry init, poetry add requests, poetry run python app.py, poetry install; kilit dosyası poetry.lock. Eski poetry projeleri bağımlılıkları [tool.poetry.dependencies] tablosunda ^2.31 (>=2.31,<3) biçiminde tutar; yeni sürümler standart [project] tablosunu da kullanabilir. Kilit dosyası her paketin tam sürümünü kaydeder ve uygulamalarda git'e eklenir; elle düzenlenmez. Öğrenirken temel akış pip + venv'dir, çünkü diğer araçların ne yaptığını anlamayı sağlar. Bir ekip projesinde deponun kullandığı araca uy ve aynı projede araçları karıştırma (uv.lock varken pip install ile paket eklemek kilit dosyasını güncellemez).",
    code=r'''
def detect_tool(files):
    if "uv.lock" in files:
        return "uv"
    if "poetry.lock" in files:
        return "poetry"
    if "requirements.txt" in files:
        return "pip + venv"
    if "pyproject.toml" in files:
        return "pyproject var, kilit dosyası yok"
    return "bağımlılık dosyası yok"

projects = [
    {"pyproject.toml", "uv.lock"},
    {"pyproject.toml", "poetry.lock"},
    {"requirements.txt", "app.py"},
    {"app.py"},
]
for files in projects:
    print(sorted(files), "→", detect_tool(files))
''',
    expectedOutput=r'''
['pyproject.toml', 'uv.lock'] → uv
['poetry.lock', 'pyproject.toml'] → poetry
['app.py', 'requirements.txt'] → pip + venv
['app.py'] → bağımlılık dosyası yok
''',
    why="Kilit dosyası, projeyi hangi aracın yönettiğinin en güçlü işaretidir; bu yüzden önce o aranır. requirements.txt genellikle pip + venv akışını, kilit dosyası olmayan pyproject.toml ise standart bir paket tanımını gösterir. Kümeler sırasız olduğundan yazdırılırken sıralandı.",
    alternatives=[
        "Deponun README'si ya da CONTRIBUTING dosyası genellikle kurulum komutunu açıkça yazar; önce oraya bak.",
        "conda, bilimsel hesaplamada Python dışı kütüphaneleri de yöneten ayrı bir ekosistemdir.",
    ],
    traps=[
        "uv.lock ya da poetry.lock olan projede bağımlılığı pip install ile eklemek.",
        "Kilit dosyasını elle düzenlemek.",
        "poetry'nin ^2.31 kısıtını >=2.31 ile aynı sanmak; ^ üst sınır olarak bir sonraki ana sürümü (3) koyar.",
    ],
    realCode=r'''
import tomllib

poetry_style = """
[tool.poetry]
name = "eski-proje"

[tool.poetry.dependencies]
python = "^3.11"
requests = "^2.31"
"""
uv_style = """
[project]
name = "yeni-proje"
dependencies = ["requests>=2.31"]

[dependency-groups]
dev = ["pytest>=8"]
"""
for text in [poetry_style, uv_style]:
    data = tomllib.loads(text)
    if "poetry" in data.get("tool", {}):
        deps = data["tool"]["poetry"]["dependencies"]
        print("poetry:", {name: spec for name, spec in deps.items() if name != "python"})
    else:
        print("standart [project]:", data["project"]["dependencies"], data.get("dependency-groups", {}))
''',
    realOutput=r'''
poetry: {'requests': '^2.31'}
standart [project]: ['requests>=2.31'] {'dev': ['pytest>=8']}
''',
    lineByLine=[
        "Eski poetry biçimi bağımlılıkları [tool.poetry.dependencies] tablosunda ad → kısıt sözlüğü olarak tutar; python da bu tablodadır.",
        "uv ve standart araçlar [project] tablosunu ve geliştirme araçları için [dependency-groups]'u kullanır.",
        "Kod tool.poetry tablosunun varlığına bakarak biçimi ayırt eder; get ile eksik tablo hata vermez.",
        "Python sürüm kısıtı paket değildir; bağımlılık listesinden çıkarılır.",
    ],
)

section(
    id="env-vars",
    title="Ortam değişkenleri ve .env",
    eyebrow="Ayarları ve gizli bilgileri koddan ayır",
    objectives=[
        "os.environ ve os.getenv ile ortam değişkenini okur; eksik değişkende varsayılan kullanır.",
        "Ortam değişkenlerinin her zaman str olduğunu hesaba katarak sayı ve mantıksal değere doğru çevirir; .env dosyasının rolünü açıklar.",
    ],
    prerequisites=["pip-venv", "m7:try-except"],
    summary="Ortam değişkenleri, program başlatılırken işletim sisteminin verdiği ad=değer çiftleridir. os.environ bir sözlük gibi davranır; os.getenv(\"AD\", \"varsayılan\") eksikse varsayılanı döndürür. Değerler her zaman metindir.",
    explanation="Port, veritabanı adresi, API anahtarı gibi ayarlar ortamdan okunursa aynı kod geliştirme, test ve sunucuda farklı ayarlarla çalışır ve gizli bilgi koda yazılmaz. Terminalde macOS/Linux'ta export APP_PORT=8080, Windows PowerShell'de $env:APP_PORT=\"8080\" ile verilir. os.environ[\"AD\"] eksikse KeyError verir: zorunlu ayarlar için uygundur. os.getenv(\"AD\") eksikse None, os.getenv(\"AD\", \"8000\") varsayılanı döndürür. Değerler str'dir: int(...) ile çevir; \"false\" metni boş olmadığı için bool(\"false\") True'dur, mantıksal değeri metni karşılaştırarak çöz. .env dosyası yerel geliştirmede bu değişkenleri bir dosyada tutar; python-dotenv paketi (from dotenv import load_dotenv) onu os.environ'a yükler ve varsayılan olarak zaten tanımlı değişkenleri ezmez. .env gizli bilgi içerdiği için .gitignore'a eklenir; değerleri boş bir .env.example paylaşılır. Bu sitede ortamı terminalden veremediğin için örnekler os.environ'a kendileri yazar; her çalıştırmadan sonra ortam eski hâline döner.",
    code=r'''
import os

os.environ["APP_PORT"] = "8080"
os.environ["APP_DEBUG"] = "false"

port = int(os.getenv("APP_PORT", "8000"))
host = os.getenv("APP_HOST", "localhost")
debug_text = os.environ["APP_DEBUG"]
print(port + 1, host)
print(repr(debug_text), bool(debug_text), debug_text.lower() in {"1", "true", "yes", "evet"})
''',
    expectedOutput=r'''
8081 localhost
'false' True False
''',
    why="APP_PORT metin olarak geldi ve int ile sayıya çevrildi. APP_HOST tanımlı olmadığı için varsayılan kullanıldı. \"false\" metni boş olmadığından bool True verir; doğru yorum, metni kabul edilen değerlerle karşılaştırmaktır.",
    alternatives=[
        "Çok sayıda ayar için pydantic-settings gibi kütüphaneler türleri ve zorunlu alanları otomatik doğrular.",
        "Yerel geliştirmede python-dotenv ile .env dosyasını yüklemek, her terminalde export yazmaktan kolaydır.",
    ],
    traps=[
        "bool(os.getenv(\"DEBUG\")) ile \"false\" değerini True okumak.",
        "os.getenv(\"PORT\", 8000) yazıp değişken tanımlıyken str, değilken int almak.",
        "API anahtarını koda ya da git'e eklenen .env dosyasına yazmak.",
        "Gizli değeri hata ayıklarken print ile log'a dökmek.",
    ],
    realCode=r'''
import os
from pathlib import Path

Path(".env").write_text("""# yerel ayarlar
DB_URL=sqlite:///dev.db
API_KEY="gizli-anahtar"
APP_PORT=9000
""", encoding="utf-8")

def load_dotenv(path=".env"):
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"'))

os.environ["APP_PORT"] = "8080"
load_dotenv()
print(os.environ["DB_URL"], os.environ["APP_PORT"])
print(len(os.environ["API_KEY"]))
''',
    realOutput=r'''
sqlite:///dev.db 8080
13
''',
    lineByLine=[
        "Örnek bir .env dosyası oluşturulur: yorum, tırnaklı ve tırnaksız değerler içerir.",
        "Her satır ilk = işaretinden ikiye bölünür; boş satırlar ve yorumlar atlanır, değerin çevresindeki tırnaklar temizlenir.",
        "setdefault zaten tanımlı değişkeni ezmez: terminalden gelen APP_PORT=8080, .env'deki 9000'e üstün gelir.",
        "Gizli anahtarın kendisi değil yalnızca uzunluğu yazdırılır; gizli değerler çıktıya dökülmez.",
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
    if fields["type"] in ("code", "order") and "solutionCode" not in fields:
        fields["solutionCode"] = fields["answer"]
    fields = {"id": f"m9-q{len(questions) + 1:02d}", **fields}
    questions.append(fields)


# ---- output (12)
q(type="output", topic="import", sectionId="import-forms", difficulty=1,
  prompt="Takma adla import edilen fonksiyon ne yazdırır?",
  code=r'''
from math import sqrt as kok
print(kok(25))
''',
  expectedOutput="5.0",
  hints=["as, sqrt'a kok adını verir.", "sqrt her zaman float döndürür."],
  explanation="from math import sqrt as kok, sqrt fonksiyonunu kok adına bağlar. sqrt sonucu float olduğu için 5.0 yazılır.")

q(type="output", topic="import", sectionId="import-forms", difficulty=2,
  prompt="import math as m sonrasında hangi adlar tanımlıdır?",
  code=r'''
import math as m
print(m.__name__)
print("math" in dir())
''',
  expectedOutput="math\nFalse",
  hints=["Modülün kendi adı değişmez.", "dir() geçerli dosyadaki adları listeler."],
  explanation="Takma ad yalnızca m adını tanımlar; modülün gerçek adı yine math'tir ama dosyada math diye bir ad yoktur.")

q(type="output", topic="kendi-modul", sectionId="own-module", difficulty=2,
  prompt="Modül iki kez import ediliyor. Çıktı ne olur?",
  code=r'''
from pathlib import Path

Path("sayac.py").write_text("""print("yüklendi")
TOTAL = 10
""", encoding="utf-8")

import sayac
import sayac
from sayac import TOTAL
print(TOTAL)
''',
  expectedOutput="yüklendi\n10",
  hints=["Modül kodu yalnızca ilk importta çalışır.", "Sonraki importlar sys.modules'teki modülü kullanır."],
  explanation="İlk import sayac.py'yi çalıştırır ve yüklendi yazar. Sonraki import ve from import aynı modül nesnesini kullanır; kod tekrar çalışmaz.")

q(type="output", topic="kendi-modul", sectionId="own-module", difficulty=3,
  prompt="Modüldeki sayaç fonksiyonla artırılıyor. Çıktı ne olur?",
  code=r'''
from pathlib import Path

Path("ayar.py").write_text("""count = 0

def increase():
    global count
    count += 1
""", encoding="utf-8")

from ayar import count
import ayar
ayar.increase()
ayar.increase()
print(count, ayar.count)
''',
  expectedOutput="0 2",
  hints=["from ayar import count, o anki değeri yeni bir ada bağlar.", "increase modüldeki count'u değiştirir, senin count adını değil."],
  explanation="from import sırasında count 0'dı ve ana dosyadaki count bu değere bağlandı. increase modülün içindeki count'u 2 yaptı; güncel değeri görmek için ayar.count okunmalıdır.")

q(type="output", topic="main", sectionId="main-guard", difficulty=1,
  prompt="Korumalı blok içeren modül import ediliyor. Çıktı ne olur?",
  code=r'''
from pathlib import Path

Path("hesap.py").write_text("""def square(x):
    return x * x

if __name__ == "__main__":
    print("deneme:", square(3))
""", encoding="utf-8")

import hesap
print(hesap.square(4))
''',
  expectedOutput="16",
  hints=["Import edilen modülde __name__ \"hesap\"tır.", "Korumalı blok atlanır."],
  explanation="hesap import edildiği için __name__ == \"__main__\" yanlıştır ve deneme satırı çalışmaz; yalnızca ana programın print'i görünür.")

q(type="output", topic="main", sectionId="main-guard", difficulty=2,
  prompt="Ana dosyada ve import edilen modülde __name__ ne yazar?",
  code=r'''
from pathlib import Path

Path("modul.py").write_text("""print("modül:", __name__)
""", encoding="utf-8")

import modul
print("ana dosya:", __name__)
''',
  expectedOutput="modül: modul\nana dosya: __main__",
  hints=["Import edilen modülün __name__'i dosya adıdır.", "Çalıştırılan dosyanınki her zaman __main__'dir."],
  explanation="Her modül kendi __name__ değerini taşır: import edilen modul, çalıştırılan dosya ise __main__.")

q(type="output", topic="paket", sectionId="packages-relative", difficulty=2,
  prompt="Paketin alt modülünden bir ad import ediliyor. Çıktı hangi sırayla oluşur?",
  code=r'''
from pathlib import Path

Path("paket").mkdir()
Path("paket/__init__.py").write_text("""print("paket başlatılıyor")
""", encoding="utf-8")
Path("paket/alt.py").write_text("""print("alt yükleniyor")
VALUE = 7
""", encoding="utf-8")

from paket.alt import VALUE
print(VALUE)
''',
  expectedOutput="paket başlatılıyor\nalt yükleniyor\n7",
  hints=["Alt modülden önce paketin kendisi yüklenir.", "Paketin kodu __init__.py'dedir."],
  explanation="paket.alt'a ulaşmak için önce paket yüklenir ve __init__.py çalışır, ardından alt.py çalışır.")

q(type="output", topic="venv", sectionId="pip-venv", difficulty=1,
  prompt="find_spec sonuçları ne yazdırır?",
  code=r'''
import importlib.util

print(importlib.util.find_spec("json") is None)
print(importlib.util.find_spec("olmayan_paket_xyz") is None)
''',
  expectedOutput="False\nTrue",
  hints=["json standart kütüphanededir.", "Bulunamayan modül için find_spec None döndürür."],
  explanation="json bulunduğu için spec None değildir (False). Kurulu olmayan modül için find_spec None döndürür (True).")

q(type="output", topic="bagimlilik", sectionId="dependency-files", difficulty=2,
  prompt="pyproject metninden ne okunur?",
  code=r'''
import tomllib

data = tomllib.loads("""
[project]
name = "rapor"
dependencies = ["requests>=2.31", "rich"]
""")
project = data["project"]
print(len(project["dependencies"]), project.get("requires-python", "belirtilmemiş"))
''',
  expectedOutput="2 belirtilmemiş",
  hints=["dependencies bir liste.", "requires-python alanı yazılmamış."],
  explanation="İki bağımlılık vardır. requires-python tanımlanmadığı için get varsayılanı döndürür.")

q(type="output", topic="bagimlilik", sectionId="dependency-files", difficulty=2,
  prompt="requirements satırları temizleniyor. Liste ne olur?",
  code=r'''
lines = ["requests==2.32.3", "# test araçları", "", "pytest>=8  # yalnız geliştirme"]
packages = []
for line in lines:
    line = line.split("#")[0].strip()
    if line:
        packages.append(line)
print(packages)
''',
  expectedOutput="['requests==2.32.3', 'pytest>=8']",
  hints=["# sonrası atılır.", "Yorum satırı ve boş satır temizlenince boş kalır."],
  explanation="Yorum satırı ve boş satır elenir; satır sonundaki yorum ve boşluklar silinir.")

q(type="output", topic="uv-poetry", sectionId="uv-poetry", difficulty=1,
  prompt="Projelerin aracı nasıl tespit edilir?",
  code=r'''
def detect(files):
    if "uv.lock" in files:
        return "uv"
    if "poetry.lock" in files:
        return "poetry"
    if "requirements.txt" in files:
        return "pip"
    return "bilinmiyor"

print(detect(["requirements.txt", "uv.lock"]), detect(["poetry.lock"]), detect(["app.py"]))
''',
  expectedOutput="uv poetry bilinmiyor",
  hints=["Kontroller sırayla yapılır; ilk eşleşen kazanır.", "İlk projede uv.lock var."],
  explanation="Kilit dosyası önce aranır; uv.lock bulunduğu için requirements.txt'ye bakılmaz. app.py tek başına bir araç göstermez.")

q(type="output", topic="env", sectionId="env-vars", difficulty=2,
  prompt="Ortam değişkeni ve varsayılan değerle çarpma. Çıktı ne olur?",
  code=r'''
import os

os.environ["WORKERS"] = "4"
workers = os.getenv("WORKERS", 1)
timeout = os.getenv("TIMEOUT", 30)
print(workers * 2, timeout * 2)
''',
  expectedOutput="44 60",
  hints=["Ortam değişkenleri str'dir.", "TIMEOUT tanımlı değil; varsayılan int olarak verilmiş."],
  explanation="WORKERS \"4\" metnidir ve \"4\" * 2 \"44\" olur. TIMEOUT yoktur, varsayılan int 30 döner ve 60 olur. Aynı satır ortama göre farklı tür döndürdüğü için varsayılanı da metin verip int ile çevirmek gerekir.")

# ---- bug (6)
q(type="bug", topic="kendi-modul", sectionId="own-module", difficulty=2,
  prompt="Öğrenci bu dosyayı random.py adıyla kaydetti; çalıştırınca AttributeError aldı (random modülünde randint yok). Neden?",
  code=r'''
# Dosya adı: random.py
import random

print(random.randint(1, 6))
''',
  options=[
      "Dosya adı standart kütüphanedeki random'u gölgeliyor; import random öğrencinin kendi dosyasını buluyor. Dosyanın adı değiştirilmeli",
      "randint yalnızca from random import randint ile kullanılabilir",
      "random modülü önce pip ile kurulmalı",
      "randint'e iki argüman verilemez",
  ],
  answer="Dosya adı standart kütüphanedeki random'u gölgeliyor; import random öğrencinin kendi dosyasını buluyor. Dosyanın adı değiştirilmeli",
  optionFeedback={
      "randint yalnızca from random import randint ile kullanılabilir": "random.randint biçimi doğrudur; sorun hangi random modülünün bulunduğu.",
      "random modülü önce pip ile kurulmalı": "random standart kütüphanededir ve kurulum gerektirmez.",
      "randint'e iki argüman verilemez": "randint(a, b) tam olarak iki argüman alır.",
  },
  hints=["sys.path'in ilk klasörü çalıştırılan dosyanın klasörüdür.", "Bu klasörde random.py adlı bir dosya var: öğrencinin kendisi."],
  explanation="Python önce programın klasörüne bakar ve random.py'yi orada bulur. Dosyayı zar.py gibi bir adla kaydetmek (ve oluşmuş __pycache__ klasörünü silmek) sorunu çözer.")

q(type="bug", topic="main", sectionId="main-guard", difficulty=1,
  prompt="main.py çalışınca önce beklenmeyen \"test: 120.0\" satırı da görünüyor. Neden?",
  code=r'''
# hesap.py
def kdv(price):
    return price * 1.2

print("test:", kdv(100))

# main.py
from hesap import kdv
print(kdv(50))
''',
  options=[
      "hesap.py'deki deneme print'i korumasız; import edilince de çalışıyor. if __name__ == \"__main__\": altına alınmalı",
      "from import modülü iki kez çalıştırır",
      "kdv fonksiyonu print içerdiği için çağrılınca test satırı yazılıyor",
      "main.py de kendi içinde hesap.py'yi çalıştırmaya çalışıyor",
  ],
  answer="hesap.py'deki deneme print'i korumasız; import edilince de çalışıyor. if __name__ == \"__main__\": altına alınmalı",
  optionFeedback={
      "from import modülü iki kez çalıştırır": "Modül yalnızca bir kez çalışır; bu tek çalışma bile print'i tetiklemeye yeter.",
      "kdv fonksiyonu print içerdiği için çağrılınca test satırı yazılıyor": "kdv yalnızca return eder; print fonksiyonun dışında, modülün en üst düzeyinde.",
      "main.py de kendi içinde hesap.py'yi çalıştırmaya çalışıyor": "main.py yalnızca import ediyor; import zaten modülün en üst düzey kodunu çalıştırır.",
  },
  hints=["Modülün en üst düzeyindeki her satır import sırasında çalışır.", "Deneme kodunu korumalı bloğa taşı."],
  explanation="Import, modülü baştan sona çalıştırır. Deneme kodu if __name__ == \"__main__\": altına alınınca yalnızca python hesap.py ile çalıştırıldığında görünür.")

q(type="bug", topic="paket", sectionId="packages-relative", difficulty=2,
  prompt="Terminalde aşağıdaki komut ImportError veriyor. Sorun nedir?",
  code=r'''
# app/__init__.py  (boş)
# app/core.py
def add(a, b):
    return a + b

# app/cli.py
from .core import add
print(add(2, 3))

# Terminal (proje kökünde):
# python app/cli.py
# ImportError: attempted relative import with no known parent package
''',
  options=[
      "Dosya yolu ile çalıştırılınca cli paketin parçası sayılmıyor; proje kökünden python -m app.cli ile çalıştırılmalı",
      "__init__.py boş olduğu için paket tanınmıyor",
      "Relative import Python 3'te kaldırıldı",
      "core.py'deki add fonksiyonu yanlış tanımlanmış",
  ],
  answer="Dosya yolu ile çalıştırılınca cli paketin parçası sayılmıyor; proje kökünden python -m app.cli ile çalıştırılmalı",
  optionFeedback={
      "__init__.py boş olduğu için paket tanınmıyor": "Boş __init__.py yeterlidir; sorun dosyanın nasıl başlatıldığı.",
      "Relative import Python 3'te kaldırıldı": "Python 3'te kaldırılan örtük relative importtur; noktalı biçim (from .core) geçerlidir.",
      "core.py'deki add fonksiyonu yanlış tanımlanmış": "Hata add'e ulaşılmadan, import satırında oluşuyor.",
  },
  hints=["Mesaj \"no known parent package\" diyor.", "Modülü adıyla çalıştırmak paketi tanıtır."],
  explanation="python app/cli.py, cli.py'yi bağımsız bir betik olarak çalıştırır; .core çözülemez. python -m app.cli paketi yükleyip cli'yi onun içinde çalıştırır. Alternatif olarak absolute import (from app.core import add) kullanılabilir.")

q(type="bug", topic="venv", sectionId="pip-venv", difficulty=2,
  prompt="Paket başarıyla kuruldu ama program ModuleNotFoundError veriyor. En olası neden ve düzeltme hangisi?",
  code=r'''
# Terminal:
# $ pip install requests
# Successfully installed requests-2.32.3
# $ python app.py
# ModuleNotFoundError: No module named 'requests'

# app.py
import requests
print(requests.__version__)
''',
  options=[
      "pip, programı çalıştıran python'dan farklı bir yorumlayıcıya (ya da etkin olmayan bir ortama) kurdu; doğru ortamı etkinleştirip python -m pip install requests kullanılmalı",
      "requests bir standart kütüphane modülü olduğu için kurulmamalıydı",
      "import adı Requests olmalı",
      "Kurulumdan sonra bilgisayar yeniden başlatılmalı",
  ],
  answer="pip, programı çalıştıran python'dan farklı bir yorumlayıcıya (ya da etkin olmayan bir ortama) kurdu; doğru ortamı etkinleştirip python -m pip install requests kullanılmalı",
  optionFeedback={
      "requests bir standart kütüphane modülü olduğu için kurulmamalıydı": "requests standart kütüphanede değildir; PyPI'dan kurulur.",
      "import adı Requests olmalı": "Modül adları büyük/küçük harfe duyarlıdır ve doğru ad requests'tir.",
      "Kurulumdan sonra bilgisayar yeniden başlatılmalı": "Kurulum hemen geçerlidir; sorun kurulumun gittiği yer.",
  },
  hints=["pip ve python komutları farklı kurulumlara ait olabilir.", "python -m pip, paketi tam olarak o python'a kurar."],
  explanation="Birden çok Python kurulumu ya da sanal ortam varken pip ile python farklı yerleri gösterebilir. python -m pip install requests paketi programı çalıştıracak yorumlayıcıya kurar.")

q(type="bug", topic="bagimlilik", sectionId="dependency-files", difficulty=1,
  prompt="python -m pip install -r requirements.txt ilk satırda hata veriyor. Sorun nedir?",
  code=r'''
# requirements.txt
requests=2.32.3
flask>=3.0
''',
  options=[
      "Tam sürüm için == yazılır; tek = geçerli bir sürüm belirteci değildir",
      "requirements.txt'de sürüm yazılamaz",
      "Paket adları büyük harfle başlamalı",
      "Her satır virgülle bitmeli",
  ],
  answer="Tam sürüm için == yazılır; tek = geçerli bir sürüm belirteci değildir",
  optionFeedback={
      "requirements.txt'de sürüm yazılamaz": "Sürüm kısıtı yazmak yaygın ve geçerlidir; ikinci satır bunun örneği.",
      "Paket adları büyük harfle başlamalı": "pip paket adlarında büyük/küçük harf ayırmaz.",
      "Her satır virgülle bitmeli": "Her satır ayrı bir gereksinimdir; ayırıcı satır sonudur.",
  },
  hints=["Karşılaştırma operatörlerini düşün.", "Python'da da eşitlik == ile yazılır."],
  explanation="Geçerli belirteçler ==, !=, >=, <=, >, < ve ~= biçimindedir. requests==2.32.3 yazılınca satır kurulur.")

q(type="bug", topic="env", sectionId="env-vars", difficulty=2,
  prompt="DEBUG kapalı (false) olduğu hâlde hata ayıklama mesajı yazılıyor. Neden?",
  code=r'''
import os

os.environ["DEBUG"] = "false"
DEBUG = bool(os.getenv("DEBUG"))
if DEBUG:
    print("hata ayıklama açık")
''',
  options=[
      "Ortam değişkenleri str'dir; \"false\" boş olmayan bir metin olduğu için bool True verir. Metin açıkça karşılaştırılmalı",
      "os.getenv mantıksal değerleri okuyamaz, os.environ kullanılmalı",
      "DEBUG adı Python'da ayrılmış bir sözcüktür",
      "os.environ'a yazılan değer programın içinde okunamaz",
  ],
  answer="Ortam değişkenleri str'dir; \"false\" boş olmayan bir metin olduğu için bool True verir. Metin açıkça karşılaştırılmalı",
  optionFeedback={
      "os.getenv mantıksal değerleri okuyamaz, os.environ kullanılmalı": "İkisi de aynı metni döndürür; sorun metnin bool'a çevrilme biçimi.",
      "DEBUG adı Python'da ayrılmış bir sözcüktür": "DEBUG sıradan bir değişken adıdır.",
      "os.environ'a yazılan değer programın içinde okunamaz": "Yazılan değer okundu: \"false\" metni geldi.",
  },
  hints=["bool(\"false\") ve bool(\"\") sonuçlarını karşılaştır.", "os.getenv(\"DEBUG\", \"\").lower() in {\"1\", \"true\"} gibi bir kontrol yaz."],
  explanation="bool yalnızca boş metni False sayar. Ortamdan gelen mantıksal ayarlar kabul edilen metinlerle karşılaştırılarak yorumlanmalıdır.")

# ---- fill (4)
q(type="fill", topic="import", sectionId="import-forms", difficulty=1,
  prompt="math modülünden yalnızca karekök fonksiyonunu getiren adı yaz.",
  code=r'''
from math import ___
print(sqrt(81))
''',
  answer="sqrt",
  acceptedAnswers=["sqrt"],
  solutionCode=r'''
from math import sqrt
print(sqrt(81))
''',
  expectedOutput="9.0",
  hints=["Kod sqrt adını modül öneki olmadan kullanıyor.", "square root'un kısaltması."],
  explanation="from math import sqrt, sqrt adını doğrudan kullanılabilir yapar; math adı tanımlanmaz.")

q(type="fill", topic="main", sectionId="main-guard", difficulty=1,
  prompt="Dosya doğrudan çalıştırıldığında main'i çağıran koşulu tamamla.",
  code=r'''
def main():
    print("başladı")

if __name__ == "___":
    main()
''',
  answer="__main__",
  acceptedAnswers=["__main__"],
  solutionCode=r'''
def main():
    print("başladı")

if __name__ == "__main__":
    main()
''',
  expectedOutput="başladı",
  hints=["İki alt çizgi, main, iki alt çizgi.", "Bu sitede kod her zaman doğrudan çalıştırılmış sayılır."],
  explanation="Doğrudan çalıştırılan dosyanın __name__ değeri \"__main__\"dir; koşul doğru olur ve main çağrılır.")

q(type="fill", topic="bagimlilik", sectionId="dependency-files", difficulty=2,
  prompt="TOML metnini sözlüğe çeviren tomllib fonksiyonunu yaz.",
  code=r'''
import tomllib

text = """
[project]
name = "demo"
"""
data = tomllib.___(text)
print(data["project"]["name"])
''',
  answer="loads",
  acceptedAnswers=["loads"],
  solutionCode=r'''
import tomllib

text = """
[project]
name = "demo"
"""
data = tomllib.loads(text)
print(data["project"]["name"])
''',
  expectedOutput="demo",
  hints=["Girdi bir dosya değil, metin (string).", "json'daki karşılığıyla aynı adı taşır."],
  explanation="tomllib.loads metinden, tomllib.load \"rb\" ile açılmış dosyadan okur.")

q(type="fill", topic="env", sectionId="env-vars", difficulty=1,
  prompt="Eksikse varsayılan değeri döndüren ortam değişkeni okumasını tamamla.",
  code=r'''
import os

port = os.___("PORT", "8000")
print(int(port) + 1)
''',
  answer="getenv",
  acceptedAnswers=["getenv", "environ.get"],
  solutionCode=r'''
import os

port = os.getenv("PORT", "8000")
print(int(port) + 1)
''',
  expectedOutput="8001",
  hints=["İkinci argüman varsayılan değer.", "get ve env sözcüklerinin birleşimi."],
  explanation="PORT tanımlı değil; os.getenv varsayılan \"8000\"i döndürür. os.environ.get de aynı işi yapar.")

# ---- order (4)
q(type="order", topic="kendi-modul", sectionId="own-module", difficulty=1,
  prompt="Modül dosyasını yazıp import eden ve \"merhaba\" yazdıran sırayı kur.",
  lines=[
      "print(selam.hi())",
      "from pathlib import Path",
      "import selam",
      "Path(\"selam.py\").write_text(\"def hi():\\n    return 'merhaba'\\n\", encoding=\"utf-8\")",
  ],
  answer=r'''
from pathlib import Path
Path("selam.py").write_text("def hi():\n    return 'merhaba'\n", encoding="utf-8")
import selam
print(selam.hi())
''',
  expectedOutput="merhaba",
  hints=["Modül import edilmeden önce dosyası var olmalı.", "Path kullanılmadan önce import edilir."],
  explanation="Dosya yazılmadan import edilirse ModuleNotFoundError oluşur. Sıra: Path'i getir, modülü yaz, import et, kullan.")

q(type="order", topic="paket", sectionId="packages-relative", difficulty=2,
  prompt="Küçük bir paket kurup alt modülünden değer okuyan ve 6 yazdıran sırayı kur.",
  lines=[
      "from pk.m import X",
      "Path(\"pk/m.py\").write_text(\"X = 3\\n\", encoding=\"utf-8\")",
      "print(X * 2)",
      "Path(\"pk\").mkdir()",
      "from pathlib import Path",
      "Path(\"pk/__init__.py\").write_text(\"\", encoding=\"utf-8\")",
  ],
  answer=r'''
from pathlib import Path
Path("pk").mkdir()
Path("pk/__init__.py").write_text("", encoding="utf-8")
Path("pk/m.py").write_text("X = 3\n", encoding="utf-8")
from pk.m import X
print(X * 2)
''',
  expectedOutput="6",
  hints=["Klasör, içine dosya yazılmadan önce oluşturulmalı.", "Import, paket dosyaları hazır olduktan sonra gelir."],
  explanation="Paket klasörü, __init__.py ve modül yazıldıktan sonra from pk.m import X çalışır. İki dosyanın yazılma sırası sonucu değiştirmez.")

q(type="order", topic="bagimlilik", sectionId="dependency-files", difficulty=2,
  prompt="pyproject.toml dosyasını yazıp tomllib ile okuyan ve proje adını yazdıran sırayı kur.",
  lines=[
      "    data = tomllib.load(f)",
      "import tomllib",
      "print(data[\"project\"][\"name\"])",
      "with open(\"pyproject.toml\", \"rb\") as f:",
      "    f.write('[project]\\nname = \"demo\"\\n')",
      "with open(\"pyproject.toml\", \"w\", encoding=\"utf-8\") as f:",
  ],
  answer=r'''
import tomllib
with open("pyproject.toml", "w", encoding="utf-8") as f:
    f.write('[project]\nname = "demo"\n')
with open("pyproject.toml", "rb") as f:
    data = tomllib.load(f)
print(data["project"]["name"])
''',
  expectedOutput="demo",
  hints=["Dosya önce yazılır, sonra okunur.", "tomllib.load \"rb\" ile açılmış dosya ister."],
  explanation="Metin modunda yazılan dosya ikili modda açılıp tomllib.load'a verilir; sonuç sözlüktür.")

q(type="order", topic="env", sectionId="env-vars", difficulty=1,
  prompt="Ortam değişkenini ayarlayıp okuyan ve TR yazdıran sırayı kur.",
  lines=[
      "lang = os.getenv(\"LANG_CODE\", \"en\")",
      "print(lang.upper())",
      "import os",
      "os.environ[\"LANG_CODE\"] = \"tr\"",
  ],
  answer=r'''
import os
os.environ["LANG_CODE"] = "tr"
lang = os.getenv("LANG_CODE", "en")
print(lang.upper())
''',
  expectedOutput="TR",
  hints=["Okumadan önce değer yazılmalı; yoksa varsayılan gelir.", "Varsayılan kullanılırsa çıktı EN olur."],
  explanation="Değişken okunmadan önce ayarlanırsa getenv \"tr\" döndürür. Sıra ters olursa varsayılan \"en\" kullanılır ve çıktı EN olur.")

# ---- code (10)
q(type="code", topic="kendi-modul", sectionId="own-module", difficulty=1,
  prompt="Başlangıç kodu araclar.py modülünü oluşturuyor. Modülü import et; girdideki sayıların ortalamasını (bir ondalık) ve açıklığını (en büyük - en küçük) araclar'daki fonksiyonlarla bulup \"ortalama: X, açıklık: Y\" yazdır.",
  starterCode=r'''
from pathlib import Path

Path("araclar.py").write_text("""def average(numbers):
    return sum(numbers) / len(numbers)

def spread(numbers):
    return max(numbers) - min(numbers)
""", encoding="utf-8")

numbers = [int(part) for part in input().split()]
# araclar modülünü import et ve iki fonksiyonu kullan
''',
  answer=r'''
from pathlib import Path

Path("araclar.py").write_text("""def average(numbers):
    return sum(numbers) / len(numbers)

def spread(numbers):
    return max(numbers) - min(numbers)
""", encoding="utf-8")

numbers = [int(part) for part in input().split()]
import araclar
print(f"ortalama: {araclar.average(numbers):.1f}, açıklık: {araclar.spread(numbers)}")
''',
  expectedOutput="ortalama: 2.5, açıklık: 3",
  exampleInput="1 2 3 4",
  tests=[
      {"label": "Örnek", "stdin": "1 2 3 4", "expectedOutput": "ortalama: 2.5, açıklık: 3"},
      {"label": "Tek sayı", "stdin": "5", "expectedOutput": "ortalama: 5.0, açıklık: 0"},
      {"label": "Negatif", "stdin": "-2 4", "expectedOutput": "ortalama: 1.0, açıklık: 6"},
  ],
  hints=["import araclar dosya yazıldıktan sonra gelmeli.", "Fonksiyonlara araclar.average gibi modül adıyla ulaş."],
  explanation="Modül dosyası yazıldıktan sonra import edilir; fonksiyonlar modül adıyla çağrılır. Hesaplamayı yeniden yazmak yerine modüldeki kodu kullanmak, modüllerin amacıdır.")

q(type="code", topic="import", sectionId="import-forms", difficulty=2,
  prompt="statistics modülünden median ve mode fonksiyonlarını import et. Girdideki sayıların medyanını ve en sık geçenini \"medyan: X, en sık: Y\" olarak yazdır. Birden çok en sık değer varsa mode ilk görüleni döndürür.",
  starterCode=r'''
numbers = [int(part) for part in input().split()]
# statistics'ten median ve mode'u import et
''',
  answer=r'''
from statistics import median, mode

numbers = [int(part) for part in input().split()]
print(f"medyan: {median(numbers)}, en sık: {mode(numbers)}")
''',
  expectedOutput="medyan: 2.5, en sık: 3",
  exampleInput="3 1 2 3",
  tests=[
      {"label": "Örnek", "stdin": "3 1 2 3", "expectedOutput": "medyan: 2.5, en sık: 3"},
      {"label": "Tek sayı", "stdin": "7", "expectedOutput": "medyan: 7, en sık: 7"},
      {"label": "Eşit sıklık", "stdin": "1 2 2 1", "expectedOutput": "medyan: 1.5, en sık: 1"},
      {"label": "Tek adet", "stdin": "5 9 1", "expectedOutput": "medyan: 5, en sık: 5"},
  ],
  hints=["from statistics import median, mode", "Tek sayıda öğede medyan ortadaki öğenin kendisidir; çift sayıda iki ortadakinin ortalamasıdır."],
  explanation="median listeyi kendisi sıralar. Tek sayıda öğede ortadaki değeri (int), çift sayıda iki ortadakinin ortalamasını (float) döndürür. mode eşitlikte ilk görülen değeri seçer.")

q(type="code", topic="main", sectionId="main-guard", difficulty=1,
  prompt="Girdideki kelimeleri ters sırayla yazdıran bir main() fonksiyonu yaz ve onu yalnızca dosya doğrudan çalıştırıldığında çağır.",
  starterCode=r'''
def reverse_words(text):
    return " ".join(reversed(text.split()))

# main() fonksiyonunu tanımla ve __main__ koruması ile çağır
''',
  answer=r'''
def reverse_words(text):
    return " ".join(reversed(text.split()))

def main():
    print(reverse_words(input()))

if __name__ == "__main__":
    main()
''',
  expectedOutput="dünya merhaba",
  exampleInput="merhaba dünya",
  tests=[
      {"label": "Örnek", "stdin": "merhaba dünya", "expectedOutput": "dünya merhaba"},
      {"label": "Tek kelime", "stdin": "python", "expectedOutput": "python"},
      {"label": "Fazla boşluk", "stdin": "  bir   iki  üç ", "expectedOutput": "üç iki bir"},
  ],
  hints=["main içinde input oku ve reverse_words'ün sonucunu yazdır.", "Dosyanın sonuna if __name__ == \"__main__\": main() ekle."],
  explanation="İş reverse_words'te, akış main'dedir. Koruma sayesinde başka bir dosya reverse_words'ü import ettiğinde input beklenmez.")

q(type="code", topic="venv", sectionId="pip-venv", difficulty=2,
  prompt="Girdide boşlukla ayrılmış modül adları var. importlib.util.find_spec ile her biri için \"ad: kurulu\" ya da \"ad: eksik\" yazdır. Eksik varsa son satırda \"kur: python -m pip install\" ve eksik adları yazdır.",
  starterCode=r'''
import importlib.util

names = input().split()
# her modülü find_spec ile kontrol et
''',
  answer=r'''
import importlib.util

names = input().split()
missing = []
for name in names:
    if importlib.util.find_spec(name) is None:
        missing.append(name)
        print(f"{name}: eksik")
    else:
        print(f"{name}: kurulu")
if missing:
    print("kur: python -m pip install", " ".join(missing))
''',
  expectedOutput="json: kurulu\niz_olmayan_paket: eksik\nkur: python -m pip install iz_olmayan_paket",
  exampleInput="json iz_olmayan_paket",
  tests=[
      {"label": "Örnek", "stdin": "json iz_olmayan_paket", "expectedOutput": "json: kurulu\niz_olmayan_paket: eksik\nkur: python -m pip install iz_olmayan_paket"},
      {"label": "Hepsi kurulu", "stdin": "csv math", "expectedOutput": "csv: kurulu\nmath: kurulu"},
      {"label": "Hepsi eksik", "stdin": "iz_yok_bir iz_yok_iki", "expectedOutput": "iz_yok_bir: eksik\niz_yok_iki: eksik\nkur: python -m pip install iz_yok_bir iz_yok_iki"},
  ],
  hints=["find_spec bulunamayan modülde None döndürür.", "Eksikleri bir listede topla; liste boş değilse kur satırını yazdır."],
  explanation="find_spec modülü çalıştırmadan arar. Eksikler toplanıp tek bir kurulum komutunda gösterilir; komut python -m pip biçimindedir.")

q(type="code", topic="bagimlilik", sectionId="dependency-files", difficulty=2,
  prompt="İlk satırda n, sonra n satır requirements.txt içeriği var. Yorumları (# sonrası) ve boş satırları atla. Her paket için \"ad → kısıt\" yazdır; kısıt yoksa \"ad → (sürüm serbest)\". Ad, ilk =, <, >, !, ~ ya da boşluk karakterine kadar olan kısımdır ve küçük harfe çevrilir.",
  starterCode=r'''
count = int(input())
lines = [input() for _ in range(count)]
# her satırı temizle, adı ve kısıtı ayır
''',
  answer=r'''
count = int(input())
lines = [input() for _ in range(count)]
for line in lines:
    line = line.split("#", 1)[0].strip()
    if not line:
        continue
    cut = len(line)
    for index, char in enumerate(line):
        if char in "=<>!~ ":
            cut = index
            break
    name, spec = line[:cut].lower(), line[cut:].strip()
    print(name, "→", spec or "(sürüm serbest)")
''',
  expectedOutput="requests → ==2.32.3\nflask → >=3.0",
  exampleInput="2\nrequests==2.32.3\nFlask>=3.0",
  tests=[
      {"label": "Örnek", "stdin": "2\nrequests==2.32.3\nFlask>=3.0", "expectedOutput": "requests → ==2.32.3\nflask → >=3.0"},
      {"label": "Yorum ve boş satır", "stdin": "4\n# araçlar\n\nrich  # renkli çıktı\npytest>=8,<9", "expectedOutput": "rich → (sürüm serbest)\npytest → >=8,<9"},
      {"label": "Boşluklu kısıt", "stdin": "1\nNumPy >= 2.0", "expectedOutput": "numpy → >= 2.0"},
      {"label": "Uyumlu sürüm", "stdin": "1\nrich~=13.7", "expectedOutput": "rich → ~=13.7"},
  ],
  hints=["line.split(\"#\", 1)[0] satır sonu yorumunu da atar.", "Kesme noktasını bulmak için enumerate ile karakterleri dolaş; bulunamazsa satırın tamamı addır."],
  explanation="Önce yorum ve boşluk temizlenir; boş kalan satır atlanır. Ad, ilk kısıt karakterinde kesilir ve pip'in yaptığı gibi küçük harfe çevrilir.")

q(type="code", topic="bagimlilik", sectionId="dependency-files", difficulty=3,
  prompt="~= (uyumlu sürüm) kısıtını denetle. Girdi: kısıttaki sürüm ve kurulu sürüm, ör. \"2.31 2.32.3\". ~=X.Y.Z kurulu sürümün X.Y ile başlamasını ve X.Y.Z'den küçük olmamasını ister (son parça hariç ön ek aynı kalır). Uyuyorsa \"uyumlu\", uymuyorsa \"uyumsuz\" yazdır. Sürümleri sayı tuple'ına çevirerek karşılaştır.",
  starterCode=r'''
spec_text, installed_text = input().split()
# sürümleri sayı tuple'ına çevir ve ~= kuralını uygula
''',
  answer=r'''
spec_text, installed_text = input().split()
spec = tuple(int(part) for part in spec_text.split("."))
installed = tuple(int(part) for part in installed_text.split("."))
prefix = spec[:-1]
compatible = installed[:len(prefix)] == prefix and installed >= spec
print("uyumlu" if compatible else "uyumsuz")
''',
  expectedOutput="uyumlu",
  exampleInput="2.31 2.32.3",
  tests=[
      {"label": "Örnek", "stdin": "2.31 2.32.3", "expectedOutput": "uyumlu"},
      {"label": "Yeni ana sürüm", "stdin": "2.31 3.0", "expectedOutput": "uyumsuz"},
      {"label": "Üç parçalı kısıt", "stdin": "2.31.0 2.32.0", "expectedOutput": "uyumsuz"},
      {"label": "Yama sürümü", "stdin": "1.4.2 1.4.5", "expectedOutput": "uyumlu"},
      {"label": "Eski sürüm", "stdin": "1.4 1.3.9", "expectedOutput": "uyumsuz"},
      {"label": "Metin değil sayı", "stdin": "1.9 1.10", "expectedOutput": "uyumlu"},
  ],
  hints=["~=2.31 ön ek olarak (2,) ister; ~=2.31.0 ön ek olarak (2, 31) ister.", "Tuple'lar soldan sağa sayı olarak karşılaştırılır: (1, 10) > (1, 9). Metin olarak \"1.10\" < \"1.9\" çıkardı."],
  explanation="Kısıtın son parçası atılarak sabit kalması gereken ön ek bulunur. Sürümler sayı tuple'ı olarak karşılaştırılır; metin karşılaştırması 1.10'u 1.9'dan küçük sanırdı.")

q(type="code", topic="uv-poetry", sectionId="uv-poetry", difficulty=2,
  prompt="Girdide bir projedeki dosya adları var (boşlukla ayrılmış). Kurulum komutunu yazdır: uv.lock varsa \"uv sync\", poetry.lock varsa \"poetry install\", requirements.txt varsa \"python -m pip install -r requirements.txt\", yalnızca pyproject.toml varsa \"python -m pip install .\", hiçbiri yoksa \"bağımlılık dosyası yok\". uv.lock ve poetry.lock birlikteyse \"uyarı: iki kilit dosyası var\" yazdır.",
  starterCode=r'''
files = set(input().split())
# kilit dosyalarına öncelik vererek kurulum komutunu seç
''',
  answer=r'''
files = set(input().split())
if {"uv.lock", "poetry.lock"} <= files:
    print("uyarı: iki kilit dosyası var")
elif "uv.lock" in files:
    print("uv sync")
elif "poetry.lock" in files:
    print("poetry install")
elif "requirements.txt" in files:
    print("python -m pip install -r requirements.txt")
elif "pyproject.toml" in files:
    print("python -m pip install .")
else:
    print("bağımlılık dosyası yok")
''',
  expectedOutput="uv sync",
  exampleInput="pyproject.toml uv.lock README.md",
  tests=[
      {"label": "Örnek", "stdin": "pyproject.toml uv.lock README.md", "expectedOutput": "uv sync"},
      {"label": "Poetry", "stdin": "poetry.lock pyproject.toml", "expectedOutput": "poetry install"},
      {"label": "requirements önceliği", "stdin": "pyproject.toml requirements.txt", "expectedOutput": "python -m pip install -r requirements.txt"},
      {"label": "Yalnız pyproject", "stdin": "pyproject.toml src", "expectedOutput": "python -m pip install ."},
      {"label": "Çakışma", "stdin": "uv.lock poetry.lock", "expectedOutput": "uyarı: iki kilit dosyası var"},
      {"label": "Dosya yok", "stdin": "app.py", "expectedOutput": "bağımlılık dosyası yok"},
  ],
  hints=["Çakışma kontrolünü en başa koy; yoksa uv.lock dalı önce yakalar.", "{a, b} <= files iki dosyanın da var olduğunu sınar."],
  explanation="Kontrollerin sırası önceliği belirler: önce çakışma, sonra kilit dosyaları, sonra daha genel dosyalar. Kilit dosyası en kesin kurulum bilgisini taşır.")

q(type="code", topic="env", sectionId="env-vars", difficulty=2,
  prompt="Başlangıç kodu girdideki satırları .env dosyasına yazar. load_env(path) fonksiyonunu yaz: boş satırları ve # ile başlayan satırları atlasın, her satırı ilk = işaretinden ayırsın, ad ve değerin uç boşluklarını ve değerin çevresindeki çift tırnağı temizlesin, sözlük döndürsün. Aynı ad iki kez varsa sonuncusu geçerlidir. Program anahtarları sıralı olarak \"AD=değer\" biçiminde yazdırır.",
  starterCode=r'''
count = int(input())
with open(".env", "w", encoding="utf-8") as f:
    for _ in range(count):
        f.write(input() + "\n")

def load_env(path):
    values = {}
    # satırları oku ve values'a ekle
    return values

for key, value in sorted(load_env(".env").items()):
    print(f"{key}={value}")
''',
  answer=r'''
count = int(input())
with open(".env", "w", encoding="utf-8") as f:
    for _ in range(count):
        f.write(input() + "\n")

def load_env(path):
    values = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            values[key.strip()] = value.strip().strip('"')
    return values

for key, value in sorted(load_env(".env").items()):
    print(f"{key}={value}")
''',
  expectedOutput="DEBUG=false\nPORT=8080",
  exampleInput="2\nPORT=8080\nDEBUG=false",
  tests=[
      {"label": "Örnek", "stdin": "2\nPORT=8080\nDEBUG=false", "expectedOutput": "DEBUG=false\nPORT=8080"},
      {"label": "Yorum ve tırnak", "stdin": "3\n# veritabanı\n\nDB_NAME = \"uygulama\"", "expectedOutput": "DB_NAME=uygulama"},
      {"label": "Değerde =", "stdin": "1\nURL=https://x.test/?a=1&b=2", "expectedOutput": "URL=https://x.test/?a=1&b=2"},
      {"label": "Tekrar eden ad", "stdin": "2\nMODE=dev\nMODE=prod", "expectedOutput": "MODE=prod"},
  ],
  hints=["line.split(\"=\", 1) yalnızca ilk = işaretinden böler.", "strip('\"') değerin başındaki ve sonundaki çift tırnakları atar."],
  explanation="Bölme yalnızca ilk = işaretinde yapılır; böylece değerin içindeki = korunur. Sözlüğe yazılan son değer öncekini ezer.")

q(type="code", topic="env", sectionId="env-vars", difficulty=2,
  prompt="Başlangıç kodu girdideki AD=değer satırlarını os.environ'a yazar. get_port() fonksiyonunu yaz: PORT tanımlı değilse 8000 döndürsün; tanımlıysa yalnızca rakamlardan oluşmalı ve 1–65535 aralığında olmalı, değilse ValueError(f\"geçersiz PORT: {değer}\") fırlatsın.",
  starterCode=r'''
import os

count = int(input())
for _ in range(count):
    key, value = input().split("=", 1)
    os.environ[key] = value

def get_port():
    # PORT'u oku, doğrula, int döndür
    pass

try:
    print("port:", get_port())
except ValueError as error:
    print(error)
''',
  answer=r'''
import os

count = int(input())
for _ in range(count):
    key, value = input().split("=", 1)
    os.environ[key] = value

def get_port():
    text = os.getenv("PORT", "8000")
    if not text.isdigit() or not 1 <= int(text) <= 65535:
        raise ValueError(f"geçersiz PORT: {text}")
    return int(text)

try:
    print("port:", get_port())
except ValueError as error:
    print(error)
''',
  expectedOutput="port: 8080",
  exampleInput="1\nPORT=8080",
  tests=[
      {"label": "Örnek", "stdin": "1\nPORT=8080", "expectedOutput": "port: 8080"},
      {"label": "Tanımsız", "stdin": "0", "expectedOutput": "port: 8000"},
      {"label": "Metin", "stdin": "1\nPORT=abc", "expectedOutput": "geçersiz PORT: abc"},
      {"label": "Aralık dışı", "stdin": "1\nPORT=70000", "expectedOutput": "geçersiz PORT: 70000"},
      {"label": "Sıfır", "stdin": "1\nPORT=0", "expectedOutput": "geçersiz PORT: 0"},
  ],
  hints=["Varsayılanı da metin olarak ver: os.getenv(\"PORT\", \"8000\").", "isdigit önce kontrol edilirse int dönüşümü hata vermez."],
  explanation="Ortam değeri metindir; önce biçimi, sonra aralığı denetlenir. Hata mesajı sorunlu değeri gösterir; yanlış ayar program başlarken açıkça bildirilir.")

q(type="code", topic="paket", sectionId="packages-relative", difficulty=2,
  prompt="Bir .py dosyasının proje köküne göre yolu verildiğinde, onu çalıştıracak python -m komutunu yazdır. Ör. app/cli.py → \"python -m app.cli\". __init__.py ise paketin kendisidir: app/__init__.py → \"python -m app\". Dosya .py ile bitmiyorsa \"python dosyası değil\" yazdır. Yollarda / kullanılır.",
  starterCode=r'''
path = input()
# yolu noktalı modül adına çevir
''',
  answer=r'''
path = input()
if not path.endswith(".py"):
    print("python dosyası değil")
else:
    parts = path[:-3].split("/")
    if parts[-1] == "__init__":
        parts = parts[:-1]
    print("python -m", ".".join(parts))
''',
  expectedOutput="python -m app.cli",
  exampleInput="app/cli.py",
  tests=[
      {"label": "Örnek", "stdin": "app/cli.py", "expectedOutput": "python -m app.cli"},
      {"label": "İç içe paket", "stdin": "app/rapor/pdf.py", "expectedOutput": "python -m app.rapor.pdf"},
      {"label": "Paket başlangıcı", "stdin": "app/__init__.py", "expectedOutput": "python -m app"},
      {"label": "Kökteki dosya", "stdin": "main.py", "expectedOutput": "python -m main"},
      {"label": "Python dışı", "stdin": "app/ayar.toml", "expectedOutput": "python dosyası değil"},
  ],
  hints=["path[:-3] .py uzantısını atar.", "Yol parçalarını / ile böl, . ile birleştir."],
  explanation="Modül yolu, klasör ayırıcılarının noktaya dönüştüğü dosya yoludur. __init__.py paketin kendisini temsil eder; bu yüzden son parça atılır.")

# ---- traceback (4)
q(type="traceback", topic="kendi-modul", sectionId="own-module", difficulty=1,
  prompt="Modül yardimci.py adıyla yazıldı ama import satırında ı harfi kullanıldı. Hangi hata oluşur?",
  code=r'''
from pathlib import Path

Path("yardimci.py").write_text("def topla(a, b):\n    return a + b\n", encoding="utf-8")
import yardımcı
print(yardımcı.topla(1, 2))
''',
  options=["ModuleNotFoundError", "NameError", "AttributeError", "SyntaxError"],
  answer="ModuleNotFoundError",
  expectedError="ModuleNotFoundError",
  optionFeedback={
      "NameError": "NameError tanımsız bir değişkende olur; burada Python modül dosyasını arıyor ve bulamıyor.",
      "AttributeError": "Modül hiç yüklenemediği için içindeki bir ada erişmeye sıra gelmedi.",
      "SyntaxError": "Python 3'te Türkçe harfli adlar geçerlidir; kod sözdizimsel olarak doğru.",
  },
  hints=["yardimci ile yardımcı farklı adlardır.", "import dosya adıyla birebir eşleşmelidir."],
  explanation="Python yardımcı.py adlı bir dosya arar ve bulamaz: ModuleNotFoundError: No module named 'yardımcı'. Modül ve dosya adlarında ASCII karakterler kullanmak bu karışıklığı önler.")

q(type="traceback", topic="paket", sectionId="packages-relative", difficulty=2,
  prompt="Paket içindeki modül dosya yolu ile çalıştırılıyor (python app/cli.py ile aynı). Hangi hata oluşur?",
  code=r'''
import runpy
from pathlib import Path

Path("app").mkdir()
Path("app/__init__.py").write_text("", encoding="utf-8")
Path("app/core.py").write_text("X = 1\n", encoding="utf-8")
Path("app/cli.py").write_text("from .core import X\nprint(X)\n", encoding="utf-8")
runpy.run_path("app/cli.py")
''',
  options=["ImportError", "ModuleNotFoundError", "SyntaxError", "NameError"],
  answer="ImportError",
  expectedError="ImportError",
  optionFeedback={
      "ModuleNotFoundError": "core.py mevcut; sorun modülün bulunamaması değil, relative importun bir üst paketi olmaması.",
      "SyntaxError": "from .core import X geçerli bir sözdizimidir.",
      "NameError": "Hata X kullanılmadan, import satırında oluşur.",
  },
  hints=["Mesaj: attempted relative import with no known parent package.", "Dosya paketsiz bir betik gibi çalıştırılıyor."],
  explanation="Yolla çalıştırılan dosyanın paketi yoktur; .core çözülemez ve ImportError oluşur. runpy.run_module(\"app.cli\") (python -m app.cli) aynı kodu sorunsuz çalıştırır.")

q(type="traceback", topic="bagimlilik", sectionId="dependency-files", difficulty=2,
  prompt="pyproject.toml metin modunda açılıp tomllib.load'a veriliyor. Hangi hata oluşur?",
  code=r'''
import tomllib

with open("pyproject.toml", "w", encoding="utf-8") as f:
    f.write('[project]\nname = "demo"\n')
with open("pyproject.toml", encoding="utf-8") as f:
    data = tomllib.load(f)
''',
  options=["TypeError", "UnicodeDecodeError", "FileNotFoundError", "KeyError"],
  answer="TypeError",
  expectedError="TypeError",
  optionFeedback={
      "UnicodeDecodeError": "Dosya UTF-8 ile yazılıp okundu; çözme sorunu yok. tomllib baytları kendisi çözmek istiyor.",
      "FileNotFoundError": "Dosya ilk with bloğunda oluşturuldu.",
      "KeyError": "Hiçbir anahtara erişilmiyor; hata yükleme sırasında oluşuyor.",
  },
  hints=["tomllib.load bytes okuyan bir dosya bekler.", "Mesaj: File must be opened in binary mode."],
  explanation="tomllib.load dosyanın \"rb\" ile açılmasını ister; metin modunda açılmış dosya str döndürdüğü için TypeError verir. Metin elindeyse tomllib.loads kullanılır.")

q(type="traceback", topic="env", sectionId="env-vars", difficulty=1,
  prompt="Zorunlu ortam değişkeni tanımlanmamış. Hangi hata oluşur?",
  code=r'''
import os

api_key = os.environ["API_KEY"]
print(len(api_key))
''',
  options=["KeyError", "NameError", "TypeError", "ValueError"],
  answer="KeyError",
  expectedError="KeyError",
  optionFeedback={
      "NameError": "os ve environ tanımlı; eksik olan sözlükteki anahtar.",
      "TypeError": "Türler doğru; os.environ str anahtar ister ve \"API_KEY\" str'dir.",
      "ValueError": "Değer var ama geçersiz değil; değer hiç yok.",
  },
  hints=["os.environ sözlük gibi davranır.", "os.getenv eksikse None döndürürdü."],
  explanation="os.environ[\"API_KEY\"] eksik anahtarda KeyError: 'API_KEY' verir. Zorunlu ayarlar için bu, programın erken ve açık biçimde durmasını sağlar; isteğe bağlı ayarlar için os.getenv kullanılır.")

assert len(questions) == 40, len(questions)
from collections import Counter
print(Counter(item["type"] for item in questions))

module = {
    "id": 9,
    "slug": "moduller-ve-ekosistem",
    "title": "Modüller ve ekosistem",
    "description": "Kodunu modüllere ve paketlere böl, doğru çalıştır; sanal ortam, bağımlılık dosyaları, uv/poetry ve ortam değişkenleriyle gerçek bir Python projesini kur ve oku.",
    "contentVersion": 1,
    "estimatedMinutes": 120,
    "practiceIds": [f"m9-q{n:02d}" for n in (1, 2, 3, 5, 6, 7, 8, 9, 11, 12, 13, 16, 19, 23, 27)],
    "sections": sections,
    "questions": questions,
}

# Source links and execution labels must survive regeneration.
section_metadata = {
  "import-forms": {
    "sources": [
      {
        "title": "Python 3.12 · import biçimleri",
        "url": "https://docs.python.org/3.12/tutorial/modules.html"
      }
    ],
    "runtime": "mixed",
    "runtimeNote": "Editör örnekleri tarayıcıda çalışır. Terminal, paket kurulumu, sanal ortam ve çok dosyalı proje yönergeleri yerel Python içindir; her çalıştırmada sanal dosyalar ve ortam sıfırlanır."
  },
  "own-module": {
    "sources": [
      {
        "title": "Python 3.12 · Kendi modülün",
        "url": "https://docs.python.org/3.12/tutorial/modules.html"
      }
    ],
    "runtime": "mixed",
    "runtimeNote": "Editör örnekleri tarayıcıda çalışır. Terminal, paket kurulumu, sanal ortam ve çok dosyalı proje yönergeleri yerel Python içindir; her çalıştırmada sanal dosyalar ve ortam sıfırlanır."
  },
  "main-guard": {
    "sources": [
      {
        "title": "Python 3.12 · __name__ == \"__main__\"",
        "url": "https://docs.python.org/3.12/library/__main__.html"
      }
    ],
    "runtime": "mixed",
    "runtimeNote": "Editör örnekleri tarayıcıda çalışır. Terminal, paket kurulumu, sanal ortam ve çok dosyalı proje yönergeleri yerel Python içindir; her çalıştırmada sanal dosyalar ve ortam sıfırlanır."
  },
  "packages-relative": {
    "sources": [
      {
        "title": "Python 3.12 · Paketler ve relative import",
        "url": "https://docs.python.org/3.12/tutorial/modules.html"
      }
    ],
    "runtime": "mixed",
    "runtimeNote": "Editör örnekleri tarayıcıda çalışır. Terminal, paket kurulumu, sanal ortam ve çok dosyalı proje yönergeleri yerel Python içindir; her çalıştırmada sanal dosyalar ve ortam sıfırlanır."
  },
  "pip-venv": {
    "sources": [
      {
        "title": "Python 3.12 · pip ve venv",
        "url": "https://docs.python.org/3.12/tutorial/venv.html"
      }
    ],
    "runtime": "mixed",
    "runtimeNote": "Editör örnekleri tarayıcıda çalışır. Terminal, paket kurulumu, sanal ortam ve çok dosyalı proje yönergeleri yerel Python içindir; her çalıştırmada sanal dosyalar ve ortam sıfırlanır."
  },
  "dependency-files": {
    "sources": [
      {
        "title": "Python 3.12 · requirements.txt ve pyproject.toml",
        "url": "https://docs.python.org/3.12/installing/index.html"
      }
    ],
    "runtime": "mixed",
    "runtimeNote": "Editör örnekleri tarayıcıda çalışır. Terminal, paket kurulumu, sanal ortam ve çok dosyalı proje yönergeleri yerel Python içindir; her çalıştırmada sanal dosyalar ve ortam sıfırlanır."
  },
  "uv-poetry": {
    "sources": [
      {
        "title": "uv · Resmî belgeler",
        "url": "https://docs.astral.sh/uv/"
      },
      {
        "title": "Poetry · Resmî belgeler",
        "url": "https://python-poetry.org/docs/"
      }
    ],
    "runtime": "mixed",
    "runtimeNote": "Editör örnekleri tarayıcıda çalışır. Terminal, paket kurulumu, sanal ortam ve çok dosyalı proje yönergeleri yerel Python içindir; her çalıştırmada sanal dosyalar ve ortam sıfırlanır."
  },
  "env-vars": {
    "sources": [
      {
        "title": "Python 3.12 · Ortam değişkenleri ve .env",
        "url": "https://docs.python.org/3.12/library/os.html"
      }
    ],
    "runtime": "mixed",
    "runtimeNote": "Editör örnekleri tarayıcıda çalışır. Terminal, paket kurulumu, sanal ortam ve çok dosyalı proje yönergeleri yerel Python içindir; her çalıştırmada sanal dosyalar ve ortam sıfırlanır."
  }
}
for section in module["sections"]:
    section.update(section_metadata[section["id"]])
module["contentVersion"] = 2
(ROOT / "module-09.json").write_text(json.dumps(module, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

# ---- writing tasks
tasks = []


def task(**fields):
    for key in ("starterCode", "solution", "exampleOutput"):
        fields[key] = c(fields[key])
    for test in fields["tests"]:
        test["expectedOutput"] = c(test["expectedOutput"])
    tasks.append(fields)


task(
    id="m9-w1", moduleId=9, sectionId="env-vars",
    title="Ayarları ortamdan oku", level="Tamamla",
    objective="Ortam değişkenlerini varsayılan değerlerle okuyup doğru türe çevir ve geçersiz değeri açıkça bildir.",
    prompt="Başlangıç kodu girdideki AD=değer satırlarını os.environ'a yazar. get_int(name, default) ve get_bool(name, default) fonksiyonlarını tamamla. Değişken tanımlı değilse varsayılan döner. get_int: değer (uç boşluklar atılarak) tam sayı değilse ValueError(f\"{name} geçersiz: {value}\"). get_bool: büyük/küçük harf ve uç boşluk fark etmeksizin 1, true, yes, evet, on → True; 0, false, no, hayır, off → False; başka her şey ValueError(f\"{name} geçersiz: {value}\"). Program PORT (8000), WORKERS (2) ve DEBUG (False) ayarlarını yazdırır ya da \"ayar hatası: ...\" der.",
    starterCode=r'''
import os

count = int(input())
for _ in range(count):
    key, value = input().split("=", 1)
    os.environ[key] = value

TRUE_WORDS = {"1", "true", "yes", "evet", "on"}
FALSE_WORDS = {"0", "false", "no", "hayır", "off"}

def get_int(name, default):
    # tanımlı değilse default; tam sayı değilse ValueError
    return default

def get_bool(name, default):
    # tanımlı değilse default; TRUE_WORDS/FALSE_WORDS dışında ValueError
    return default

try:
    port = get_int("PORT", 8000)
    workers = get_int("WORKERS", 2)
    debug = get_bool("DEBUG", False)
    print(f"PORT={port} WORKERS={workers} DEBUG={debug}")
except ValueError as error:
    print("ayar hatası:", error)
''',
    exampleInput="2\nPORT=9000\nDEBUG=Evet",
    exampleOutput="PORT=9000 WORKERS=2 DEBUG=True",
    hints=[
        "value = os.getenv(name) ile oku; None ise default döndür.",
        "Karşılaştırmadan önce value.strip().lower() kullan; int için int(value.strip()) dönüşümünü try/except ValueError içinde dene ve kendi mesajınla yeniden fırlat.",
    ],
    solution=r'''
import os

count = int(input())
for _ in range(count):
    key, value = input().split("=", 1)
    os.environ[key] = value

TRUE_WORDS = {"1", "true", "yes", "evet", "on"}
FALSE_WORDS = {"0", "false", "no", "hayır", "off"}

def get_int(name, default):
    value = os.getenv(name)
    if value is None:
        return default
    try:
        return int(value.strip())
    except ValueError:
        raise ValueError(f"{name} geçersiz: {value}") from None

def get_bool(name, default):
    value = os.getenv(name)
    if value is None:
        return default
    word = value.strip().lower()
    if word in TRUE_WORDS:
        return True
    if word in FALSE_WORDS:
        return False
    raise ValueError(f"{name} geçersiz: {value}")

try:
    port = get_int("PORT", 8000)
    workers = get_int("WORKERS", 2)
    debug = get_bool("DEBUG", False)
    print(f"PORT={port} WORKERS={workers} DEBUG={debug}")
except ValueError as error:
    print("ayar hatası:", error)
''',
    tests=[
        {"label": "Örnek", "stdin": "2\nPORT=9000\nDEBUG=Evet", "expectedOutput": "PORT=9000 WORKERS=2 DEBUG=True"},
        {"label": "Hiç ayar yok", "stdin": "0", "expectedOutput": "PORT=8000 WORKERS=2 DEBUG=False"},
        {"label": "false metni", "stdin": "2\nDEBUG=false\nWORKERS= 4 ", "expectedOutput": "PORT=8000 WORKERS=4 DEBUG=False"},
        {"label": "Geçersiz sayı", "stdin": "1\nPORT=sekiz", "expectedOutput": "ayar hatası: PORT geçersiz: sekiz"},
        {"label": "Geçersiz bool", "stdin": "1\nDEBUG=belki", "expectedOutput": "ayar hatası: DEBUG geçersiz: belki"},
    ],
)

task(
    id="m9-w2", moduleId=9, sectionId="dependency-files",
    title="Bağımlılık denetleyicisini onar", level="Düzelt",
    objective="requirements.txt satırlarını sağlam biçimde ayrıştır ve paket adlarını pip gibi karşılaştır.",
    prompt="İlk satırda requirements satır sayısı, ardından requirements.txt satırları (her paket ad==sürüm biçiminde sabitlenmiş); sonra kurulu paket sayısı ve \"ad sürüm\" satırları (pip list gibi) geliyor. Her gereksinim için \"ad: tamam\", \"ad: farklı (kurulu X)\" ya da \"ad: eksik\" yazdır. Adlar pip'in yaptığı gibi karşılaştırılır: büyük/küçük harf ve _ ile - farkı önemsizdir; çıktıda ad küçük harfle ve _ yerine - ile yazılır. Başlangıç kodunda üç sorun var: yorum ve boş satırlar programı çökertiyor, ad karşılaştırması pip'ten farklı ve == çevresindeki boşluklar sürümü bozuyor.",
    starterCode=r'''
def parse_requirements(lines):
    pins = {}
    for line in lines:
        name, version = line.split("==")
        pins[name] = version
    return pins

def parse_installed(lines):
    installed = {}
    for line in lines:
        name, version = line.split()
        installed[name] = version
    return installed

req_count = int(input())
requirements = parse_requirements([input() for _ in range(req_count)])
inst_count = int(input())
installed = parse_installed([input() for _ in range(inst_count)])

for name, version in requirements.items():
    if name not in installed:
        print(f"{name}: eksik")
    elif installed[name] != version:
        print(f"{name}: farklı (kurulu {installed[name]})")
    else:
        print(f"{name}: tamam")
''',
    exampleInput="4\n# web\nFlask==3.0.3\nrequests == 2.32.3\npython_dotenv==1.0.1\n2\nflask 3.0.3\nrequests 2.31.0",
    exampleOutput="flask: tamam\nrequests: farklı (kurulu 2.31.0)\npython-dotenv: eksik",
    hints=[
        "Adı normalleştiren küçük bir fonksiyon yaz: name.strip().lower().replace(\"_\", \"-\"); iki sözlükte de kullan.",
        "Her requirements satırında önce line.split(\"#\", 1)[0].strip(); boş kalırsa atla. Sürümü de strip ile temizle.",
    ],
    solution=r'''
def normalize(name):
    return name.strip().lower().replace("_", "-")

def parse_requirements(lines):
    pins = {}
    for line in lines:
        line = line.split("#", 1)[0].strip()
        if not line:
            continue
        name, version = line.split("==")
        pins[normalize(name)] = version.strip()
    return pins

def parse_installed(lines):
    installed = {}
    for line in lines:
        name, version = line.split()
        installed[normalize(name)] = version
    return installed

req_count = int(input())
requirements = parse_requirements([input() for _ in range(req_count)])
inst_count = int(input())
installed = parse_installed([input() for _ in range(inst_count)])

for name, version in requirements.items():
    if name not in installed:
        print(f"{name}: eksik")
    elif installed[name] != version:
        print(f"{name}: farklı (kurulu {installed[name]})")
    else:
        print(f"{name}: tamam")
''',
    tests=[
        {"label": "Örnek", "stdin": "4\n# web\nFlask==3.0.3\nrequests == 2.32.3\npython_dotenv==1.0.1\n2\nflask 3.0.3\nrequests 2.31.0", "expectedOutput": "flask: tamam\nrequests: farklı (kurulu 2.31.0)\npython-dotenv: eksik"},
        {"label": "Satır sonu yorumu ve boş satır", "stdin": "3\nrich==13.7.1  # renkli çıktı\n\nPyYAML==6.0.1\n2\nrich 13.7.1\npyyaml 6.0.1", "expectedOutput": "rich: tamam\npyyaml: tamam"},
        {"label": "Kurulu adda alt çizgi", "stdin": "1\ntyping-extensions==4.12.2\n1\ntyping_extensions 4.12.2", "expectedOutput": "typing-extensions: tamam"},
        {"label": "Hiç kurulu yok", "stdin": "1\nnumpy==2.1.0\n0", "expectedOutput": "numpy: eksik"},
        {"label": "Boşluklu sabitleme", "stdin": "1\nrequests == 2.32.3\n1\nrequests 2.32.3", "expectedOutput": "requests: tamam"},
    ],
)

task(
    id="m9-w3", moduleId=9, sectionId="packages-relative",
    title="Kendi paketini kur", level="Sıfırdan yaz",
    objective="Birden çok modülden oluşan bir paket tasarla; modülleri relative import ile bağla ve paketin dışa açık adlarını __init__.py'de topla.",
    prompt="Program önce metin adlı bir paket oluşturmalı (Path.write_text ile): metin/temizle.py içinde normalize(text) — metnin boşluklarını tek boşluğa indirip uçlarını atar; metin/say.py içinde word_counts(text) — normalize'ı from .temizle import normalize ile kullanır, her kelimenin uçlarındaki .,!?;: işaretlerini atar, boş kalanı saymaz ve {kelime: sayı} sözlüğü döndürür; metin/__init__.py ise normalize ve word_counts'u dışa açar. Ardından import metin ile paketi kullanarak girdideki n satırı (ilk satır n) boşlukla birleştirip en sık 3 kelimeyi \"kelime: sayı\" olarak yazdırır (çoktan aza; eşitlikte alfabetik; büyük/küçük harf ayrı sayılır). Son satır paketin yapısını gösterir: print(sorted(n for n in dir(metin) if not n.startswith(\"_\"))).",
    starterCode=r'''
from pathlib import Path

# 1) metin paketini oluştur: __init__.py, temizle.py, say.py
# 2) import metin
# 3) girdiyi oku, en sık 3 kelimeyi yazdır

# Son satır (değiştirme):
# print(sorted(n for n in dir(metin) if not n.startswith("_")))
''',
    exampleInput="2\nelma armut elma\nArmut,  elma!",
    exampleOutput="elma: 3\nArmut: 1\narmut: 1\n['normalize', 'say', 'temizle', 'word_counts']",
    hints=[
        "Önce Path(\"metin\").mkdir(), sonra üç dosyayı write_text ile yaz; ancak hepsi yazıldıktan sonra import metin.",
        "__init__.py: from .temizle import normalize ve from .say import word_counts. Sıralama için key=lambda item: (-item[1], item[0]).",
    ],
    solution=r'''
from pathlib import Path

Path("metin").mkdir()
Path("metin/temizle.py").write_text("""def normalize(text):
    return " ".join(text.split())
""", encoding="utf-8")
Path("metin/say.py").write_text("""from .temizle import normalize

def word_counts(text):
    counts = {}
    for word in normalize(text).split(" "):
        word = word.strip(".,!?;:")
        if word:
            counts[word] = counts.get(word, 0) + 1
    return counts
""", encoding="utf-8")
Path("metin/__init__.py").write_text("""from .temizle import normalize
from .say import word_counts
""", encoding="utf-8")

import metin

count = int(input())
text = " ".join(input() for _ in range(count))
ranked = sorted(metin.word_counts(text).items(), key=lambda item: (-item[1], item[0]))
for word, number in ranked[:3]:
    print(f"{word}: {number}")
print(sorted(n for n in dir(metin) if not n.startswith("_")))
''',
    tests=[
        {"label": "Örnek", "stdin": "2\nelma armut elma\nArmut,  elma!", "expectedOutput": "elma: 3\nArmut: 1\narmut: 1\n['normalize', 'say', 'temizle', 'word_counts']"},
        {"label": "Üçten az kelime", "stdin": "1\nmerhaba merhaba", "expectedOutput": "merhaba: 2\n['normalize', 'say', 'temizle', 'word_counts']"},
        {"label": "Yalnız noktalama", "stdin": "2\n... !!!\nbir, iki; bir: iki? üç", "expectedOutput": "bir: 2\niki: 2\nüç: 1\n['normalize', 'say', 'temizle', 'word_counts']"},
        {"label": "Boş girdi", "stdin": "0", "expectedOutput": "['normalize', 'say', 'temizle', 'word_counts']"},
    ],
)

tasks_path = ROOT / "writing-tasks.json"
existing = [t for t in json.loads(tasks_path.read_text(encoding="utf-8")) if t["moduleId"] != 9]
tasks_path.write_text(json.dumps(existing + tasks, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("module-09.json ve", len(tasks), "yazma görevi yazıldı")
