"""Builds content/module-12.json and the M12 writing tasks.

Run: PYTHONIOENCODING=utf-8 python scripts/content-builders/build_m12.py
Lesson sections live in m12_sections.py, questions in m12_questions.py, writing tasks in m12_tasks.py.
"""
import json
from collections import Counter
from pathlib import Path

from m12_questions import questions
from m12_sections import sections
from m12_tasks import tasks

ROOT = Path(__file__).resolve().parents[2] / "content"

assert len(sections) == 8, len(sections)
assert len(questions) == 40, len(questions)
kinds = Counter(item["type"] for item in questions)
assert kinds == {"output": 12, "bug": 6, "fill": 4, "order": 4, "code": 10, "traceback": 4}, kinds
section_ids = [section["id"] for section in sections]
for item in questions:
    assert item["sectionId"] in section_ids, (item["id"], item["sectionId"])
covered = {item["sectionId"] for item in questions}
assert covered == set(section_ids), set(section_ids) - covered

practice = (2, 3, 5, 7, 9, 10, 12, 14, 15, 18, 22, 26, 28, 33, 36)
module = {
    "id": 12,
    "slug": "oop-2",
    "title": "OOP 2",
    "description": "Polimorfizm ve soyut sınıflarla arayüz kur, dunder metotlarla nesnelerini Python'un yerleşik davranışlarına bağla, MRO'yu oku, dataclass ve slots ile veri sınıfları yaz; descriptor ve metaclass'ı tanı.",
    "contentVersion": 1,
    "estimatedMinutes": 160,
    "practiceIds": [f"m12-q{n:02d}" for n in practice],
    "sections": sections,
    "questions": questions,
}
(ROOT / "module-12.json").write_text(json.dumps(module, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

for item in tasks:
    assert item["sectionId"] in section_ids, item["id"]
tasks_path = ROOT / "writing-tasks.json"
existing = [t for t in json.loads(tasks_path.read_text(encoding="utf-8")) if t["moduleId"] != 12]
ordered = sorted(existing + tasks, key=lambda item: (item["moduleId"], int(item["id"].split("-w")[1])))
tasks_path.write_text(json.dumps(ordered, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("module-12.json ve", len(tasks), "yazma görevi yazıldı:", dict(kinds))
