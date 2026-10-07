"""Runs every lesson's localExample with this machine's CPython and compares the output.

localExample holds code the browser cannot run (threads, processes), so verify-content.mjs
(Pyodide) skips it. Run: npm run verify:local  (needs Python 3.11+ on PATH).
Each example runs as a real file (yerel.py) in its own empty folder, the way a learner would run
it; multiprocessing needs that on Windows and macOS, where child processes re-import the file.
"""
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "content"
sys.stdout.reconfigure(encoding="utf-8")

if sys.version_info < (3, 11):
    sys.exit(f"Python 3.11+ gerekli; bu {sys.version.split()[0]}.")

failures = []
checked = 0
for path in sorted(ROOT.glob("module-*.json")):
    module = json.loads(path.read_text(encoding="utf-8"))
    for section in module["sections"]:
        example = section.get("localExample")
        if not example:
            continue
        label = f"M{module['id']} {section['id']}"
        with tempfile.TemporaryDirectory(prefix="iz-yerel-") as folder:
            Path(folder, "yerel.py").write_text(example["code"], encoding="utf-8")
            env = {**os.environ, "PYTHONIOENCODING": "utf-8", "PYTHONUTF8": "1"}
            try:
                result = subprocess.run([sys.executable, "yerel.py"], cwd=folder, capture_output=True, text=True, encoding="utf-8", timeout=60, env=env)
            except subprocess.TimeoutExpired:
                failures.append(f"{label}: 60 saniyede bitmedi.")
                continue
        checked += 1
        output = result.stdout.rstrip("\n")
        if result.returncode != 0:
            failures.append(f"{label}: hata verdi:\n{result.stderr.strip()}")
        elif output != example["output"]:
            failures.append(f"{label}: çıktı {example['output']!r} olmalı, {output!r} alındı.")

if failures:
    print(f"{len(failures)} yerel örnek hatası:", *failures, sep="\n- ")
    sys.exit(1)
print(f"Python {sys.version.split()[0]} ile {checked} yerel örnek doğrulandı.")
