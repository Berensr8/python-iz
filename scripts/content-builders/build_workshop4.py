"""Builds Atölye 4 (after M10): a small multi-file command-line report tool.

Writes the workshop4-* tasks into content/workshop-tasks.json and the workshop4 definition into
content/milestones.json. Expected outputs come from running each reference solution; read the
printed outputs to check they match the contract in the prompt. Other workshops, their tasks and
the exams are left untouched.

The browser has no terminal, so every program here gets its "command line" as one input line and
passes it to argparse (parse_args(argv)); the input files are created from input lines first.
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2] / "content"


def run(code, stdin=""):
    with tempfile.TemporaryDirectory() as scratch:
        result = subprocess.run([sys.executable, "-X", "utf8", "-c", code], input=stdin.encode("utf-8"), capture_output=True, cwd=scratch)
    if result.returncode != 0:
        raise SystemExit(result.stderr.decode("utf-8", "replace"))
    return result.stdout.decode("utf-8").replace("\r\n", "\n").rstrip("\n")


def c(text):
    return text.strip("\n")


tasks = []


def task(id, title, level, objective, prompt, starterCode, solution, hints, tests):
    solution, starterCode = c(solution), c(starterCode)
    built = [{"label": label, "stdin": stdin, "expectedOutput": run(solution, stdin)} for label, stdin in tests]
    tasks.append({
        "id": id, "moduleId": 10, "sectionId": "sys-subprocess-argparse", "title": title, "level": level,
        "objective": objective, "prompt": prompt, "starterCode": starterCode,
        "exampleInput": built[0]["stdin"], "exampleOutput": built[0]["expectedOutput"],
        "hints": hints, "solution": solution, "tests": built,
    })
    print(f"\n== {id} ({len(built)} test)")
    for item in built:
        print(f"  [{item['label']}] girdi={item['stdin']!r}\n      çıktı={item['expectedOutput']!r}")


FILES_NOTE = "Girdinin ilk satırı dosya sayısıdır; sonraki her satır 'ad|içerik' biçimindedir ve içerikteki '/' satır sonu demektir (bu satırlar dosyaları oluşturan test düzenidir). Son satır, terminalde yazılacak komut satırı argümanlarıdır; program onu bölüp argparse'a verir."

# ---------------------------------------------------------------- İncele
READ4 = c(r'''
from pathlib import Path

Path("sayac.py").write_text("""def count_words(text, min_len=1):
    return sum(1 for word in text.split() if len(word) >= min_len)
""", encoding="utf-8")

Path("cli.py").write_text("""import argparse
from pathlib import Path
import sayac

def main(argv):
    parser = argparse.ArgumentParser(prog="say")
    parser.add_argument("files", nargs="+")
    parser.add_argument("--min", type=int, default=1)
    args = parser.parse_args(argv)
    for name in args.files:
        text = Path(name).read_text(encoding="utf-8")
        print(name, sayac.count_words(text, args.min))

if __name__ == "__main__":
    import sys
    main(sys.argv[1:])
""", encoding="utf-8")

Path("a.txt").write_text("bir iki üç dört", encoding="utf-8")
Path("b.txt").write_text("merhaba dünya", encoding="utf-8")

import cli
cli.main(["a.txt", "b.txt", "--min", "4"])
''')

# ---------------------------------------------------------------- Düzelt
FIX_SETUP = r'''
# --- test düzeni: girdideki dosyaları oluştur ve komut satırını çalıştır (dokunma)
for _ in range(int(input())):
    name, content = input().split("|", 1)
    Path(name).write_text(content.replace("/", "\n"), encoding="utf-8")
main(input().split())
'''

task(
    "workshop4-fix", "Sayım aracını onar", "Düzelt",
    "argparse seçeneklerinin türünü ve davranışını düzelt; olmayan dosyada programın çökmeden devam etmesini sağla.",
    "say aracı verilen dosyalarda satır sayar: uç boşlukları atıldıktan sonra uzunluğu --min değerinden (varsayılan 1) az olmayan satırlar sayılır, yani boş satırlar sayılmaz. --words verilirse satır yerine en az --min harfli kelimeleri sayar. Her dosya için 'ad: sayı', olmayan dosya için 'bulunamadı: ad' yazar ve devam eder; sonda bulunan dosyaların toplamını 'toplam: N' yazar. Kodda üç hata var: --words ters çalışıyor (verilmeyince kelime sayıyor), --min sayıya çevrilmiyor (verilince TypeError) ve olmayan bir dosya programı çökertiyor. " + FILES_NOTE,
    r'''
import argparse
from pathlib import Path

def build_parser():
    parser = argparse.ArgumentParser(prog="say")
    parser.add_argument("files", nargs="+")
    parser.add_argument("--words", action="store_false")
    parser.add_argument("--min", default=1)
    return parser

def count(path, words, min_len):
    text = path.read_text(encoding="utf-8")
    if words:
        return sum(1 for word in text.split() if len(word) >= min_len)
    return sum(1 for line in text.splitlines() if len(line.strip()) >= min_len)

def main(argv):
    args = build_parser().parse_args(argv)
    total = 0
    for name in args.files:
        n = count(Path(name), args.words, args.min)
        print(f"{name}: {n}")
        total += n
    print(f"toplam: {total}")
''' + FIX_SETUP,
    r'''
import argparse
from pathlib import Path

def build_parser():
    parser = argparse.ArgumentParser(prog="say")
    parser.add_argument("files", nargs="+")
    parser.add_argument("--words", action="store_true")
    parser.add_argument("--min", type=int, default=1)
    return parser

def count(path, words, min_len):
    text = path.read_text(encoding="utf-8")
    if words:
        return sum(1 for word in text.split() if len(word) >= min_len)
    return sum(1 for line in text.splitlines() if len(line.strip()) >= min_len)

def main(argv):
    args = build_parser().parse_args(argv)
    total = 0
    for name in args.files:
        path = Path(name)
        if not path.exists():
            print(f"bulunamadı: {name}")
            continue
        n = count(path, args.words, args.min)
        print(f"{name}: {n}")
        total += n
    print(f"toplam: {total}")
''' + FIX_SETUP,
    [
        "store_true ile store_false'ın varsayılanları terstir. argparse argümanları metin olarak okur; sayı istiyorsan type=int ver. Dosyayı okumadan önce var olup olmadığını denetle.",
        "--words için action=\"store_true\", --min için type=int yaz; döngüde path = Path(name) ile path.exists() yanlışsa 'bulunamadı: ad' yazıp continue kullan.",
    ],
    [
        ("Örnek: satır sayımı", "2\na.txt|bir iki/üç//dört beş altı\nb.txt|tek\na.txt b.txt"),
        ("--words", "1\na.txt|bir iki/üç\n--words a.txt"),
        ("--min", "1\na.txt|ab/abcd/abcdef\n--min 4 a.txt"),
        ("Olmayan dosya", "1\na.txt|x\na.txt yok.txt"),
        ("--words ve --min birlikte", "1\nm.txt|merhaba dünya ve evren\n--words --min 5 m.txt"),
    ],
)

# ---------------------------------------------------------------- Sıfırdan yaz
BUILD_SETUP = r'''
import argparse
from pathlib import Path

# Test düzeni: girdideki dosyaları oluşturur ve komut satırını argv'ye alır (dokunma).
for _ in range(int(input())):
    name, content = input().split("|", 1)
    Path(name).write_text(content.replace("/", "\n"), encoding="utf-8")
argv = input().split()
'''

BUILD_CHECK = r'''
print(sorted(name for name in dir(metrik) if not name.startswith("_")))
'''

task(
    "workshop4-build", "Kendi raporlama aracını yaz", "Sıfırdan yaz",
    "Hesaplamaları kendi modülüne ayır; argparse ile seçenekleri tanımla ve dosyaları pathlib ile oku.",
    "İki parçalı bir araç yaz. 1) Path('metrik.py').write_text(...) ile bir metrik.py modülü oluştur; içinde üç fonksiyon olsun: line_count(text) boş olmayan (uç boşlukları atılınca boş kalmayan) satırları sayar, word_count(text) kelimeleri sayar, longest_word(text) en uzun kelimeyi döndürür (eşitse ilk görüleni; metin boşsa '-'). 2) import metrik ile modülü içe aktar ve argparse ile şu komut satırını çözümle: bir ya da daha çok dosya adı, --metric (satır, kelime ya da en-uzun; varsayılan satır) ve --sort bayrağı. Her dosya için 'ad: değer' yaz; olmayan dosya için 'bulunamadı: ad' yazıp devam et. --sort verilirse bulunan dosyaları değere göre büyükten küçüğe sırala (en-uzun için kelimenin uzunluğuna göre), eşitlerde ada göre; olmayan dosya mesajları her durumda önce, girdi sırasıyla yazılır. Programın son satırı modülündeki adları yazdırır; test bu satırla modülü de denetler. " + FILES_NOTE,
    BUILD_SETUP + r'''
# 1) metrik.py modülünü Path("metrik.py").write_text(...) ile oluştur:
#    line_count(text), word_count(text), longest_word(text)
# 2) import metrik
# 3) argparse ile dosyaları, --metric ve --sort seçeneklerini tanımla,
#    parser.parse_args(argv) ile çözümle ve raporu yazdır.
''' + BUILD_CHECK,
    BUILD_SETUP + r'''
Path("metrik.py").write_text("""def line_count(text):
    return sum(1 for line in text.splitlines() if line.strip())

def word_count(text):
    return len(text.split())

def longest_word(text):
    return max(text.split(), key=len, default="-")
""", encoding="utf-8")

import metrik

METRICS = {"satır": metrik.line_count, "kelime": metrik.word_count, "en-uzun": metrik.longest_word}

parser = argparse.ArgumentParser(prog="rapor")
parser.add_argument("files", nargs="+")
parser.add_argument("--metric", choices=sorted(METRICS), default="satır")
parser.add_argument("--sort", action="store_true")
args = parser.parse_args(argv)

rows = []
for name in args.files:
    path = Path(name)
    if not path.exists():
        print(f"bulunamadı: {name}")
        continue
    rows.append((name, METRICS[args.metric](path.read_text(encoding="utf-8"))))

def size(value):
    return len(value) if isinstance(value, str) else value

if args.sort:
    rows.sort(key=lambda row: (-size(row[1]), row[0]))
for name, value in rows:
    print(f"{name}: {value}")
''' + BUILD_CHECK,
    [
        "Modül içeriğini üç tırnaklı bir metin olarak yaz ve Path('metrik.py').write_text(metin, encoding='utf-8') ile kaydet; ardından import metrik çalışır (M9).",
        "argparse: add_argument('files', nargs='+'), add_argument('--metric', choices=[...], default='satır'), add_argument('--sort', action='store_true'). Metrik adından fonksiyona giden bir sözlük kur; önce bulunamayanları yazdırıp sonuçları bir listede topla, --sort verildiyse sort(key=...) ile sırala.",
    ],
    [
        ("Örnek: satır", "2\na.txt|bir iki/üç//dört\nb.txt|merhaba\na.txt b.txt"),
        ("Kelime ve sıralama", "2\nkisa.txt|a b\nuzun.txt|a b c d e\n--metric kelime --sort kisa.txt uzun.txt"),
        ("En uzun kelime", "1\na.txt|kısa çokuzunkelime orta\n--metric en-uzun a.txt"),
        ("Olmayan dosya", "1\na.txt|x\na.txt yok.txt"),
        ("Boş dosyada en uzun", "1\nbos.txt|\n--metric en-uzun bos.txt"),
        ("Eşitlerde ada göre", "2\nb.txt|x\na.txt|y\n--sort b.txt a.txt"),
        ("En uzuna göre sıralama", "2\na.txt|ab\nb.txt|abcd\n--metric en-uzun --sort a.txt b.txt"),
    ],
)

# ---------------------------------------------------------------- dosyalara yaz
tasks_path = ROOT / "workshop-tasks.json"
mine = {item["id"] for item in tasks}
existing = [item for item in json.loads(tasks_path.read_text(encoding="utf-8")) if item["id"] not in mine]
tasks_path.write_text(json.dumps(existing + tasks, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

milestones_path = ROOT / "milestones.json"
data = json.loads(milestones_path.read_text(encoding="utf-8"))
data["workshops"] = [item for item in data["workshops"] if item["id"] != "workshop4"]
read4_out = run(READ4)
print("\nokuma çıktısı:", repr(read4_out))
data["workshops"].append({
    "id": "workshop4", "afterModule": 10, "title": "Atölye 4 · Komut satırı raporlayıcısı",
    "summary": "Önce iki dosyaya bölünmüş küçük bir komut satırı aracının ne yazdırdığını izle, sonra argparse seçenekleri bozuk bir sayım aracını onar. Son adımda hesaplamaları kendi modülüne ayıran, argparse ve pathlib kullanan bir dosya raporlama aracını sıfırdan yaz.",
    "steps": [
        {"kind": "read", "label": "İncele", "progressKey": "workshop4-read",
         "heading": "cli.main(...) çağrısı ne yazdırır?", "code": READ4,
         "inputLabel": "Çıktı (iki satır)", "placeholder": "Örn. a.txt 2 / b.txt 1",
         "answer": read4_out, "expectedOutput": read4_out,
         "wrongHint": "cli import edildiğinde __name__ \"cli\" olur; korumalı blok çalışmaz ve yalnızca son satırdaki main çağrısı çıktı üretir. --min 4, en az dört harfli kelimeleri sayar; len('dört') kaçtır?",
         "explanation": "cli.py import edilince if __name__ == \"__main__\" bloğu atlanır (M9); çıktıyı yalnızca cli.main([...]) üretir. argparse '--min 4' değerini type=int sayesinde sayıya çevirir. a.txt'de yalnızca 'dört' dört harflidir (bir, iki, üç daha kısa), b.txt'de 'merhaba' ve 'dünya' ikisi de en az dört harflidir.",
         "nextLabel": "Düzeltme adımına geç"},
        {"kind": "write", "label": "Düzelt", "taskId": "workshop4-fix",
         "note": "Kontrol listesi: --words verilmediğinde satır sayılsın · --min sayı olarak okunsun · olmayan dosya mesaj verip atlansın, toplam yalnız bulunan dosyalardan oluşsun.",
         "nextLabel": "Kendi aracını yaz"},
        {"kind": "write", "label": "Sıfırdan yaz", "taskId": "workshop4-build",
         "note": "Sorumlulukları ayır: metrik.py yalnızca metin alıp sayı ya da kelime döndürür, dosya okumaz ve yazdırmaz. Komut satırı, dosya okuma ve yazdırma ana programdadır."},
    ],
})
data["workshops"].sort(key=lambda item: item["afterModule"])
milestones_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("\nyazıldı:", len(tasks), "görev,", len(data["workshops"]), "atölye")
