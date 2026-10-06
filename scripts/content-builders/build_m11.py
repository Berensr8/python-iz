"""Builds content/module-11.json and the M11 writing tasks.

Run: PYTHONIOENCODING=utf-8 python scripts/content-builders/build_m11.py
Lesson sections live in m11_sections.py, questions in m11_questions.py, writing tasks in m11_tasks.py.
"""
import json
from collections import Counter
from pathlib import Path

from m11_questions import questions
from m11_sections import sections
from m11_tasks import tasks

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

practice = (1, 3, 4, 8, 10, 11, 13, 14, 16, 18, 21, 22, 27, 31, 34)
module = {
    "id": 11,
    "slug": "oop-1",
    "title": "OOP 1",
    "description": "Sınıf ve nesne kurmayı, durumu korumayı, kalıtım ile composition arasında seçmeyi ve property, classmethod, staticmethod'u kendi kodunda ve başkasının kodunda tanımayı öğren.",
    "contentVersion": 1,
    "estimatedMinutes": 150,
    "practiceIds": [f"m11-q{n:02d}" for n in practice],
    "sections": sections,
    "questions": questions,
}
(ROOT / "module-11.json").write_text(json.dumps(module, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

for item in tasks:
    assert item["sectionId"] in section_ids, item["id"]
tasks_path = ROOT / "writing-tasks.json"
existing = [t for t in json.loads(tasks_path.read_text(encoding="utf-8")) if t["moduleId"] != 11]
ordered = sorted(existing + tasks, key=lambda item: (item["moduleId"], int(item["id"].split("-w")[1])))
tasks_path.write_text(json.dumps(ordered, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("module-11.json ve", len(tasks), "yazma görevi yazıldı:", dict(kinds))
