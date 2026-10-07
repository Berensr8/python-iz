"""Builds content/module-13.json and the M13 writing tasks.

Run: PYTHONIOENCODING=utf-8 python scripts/content-builders/build_m13.py
Lesson sections live in m13_sections.py, questions in m13_questions.py, writing tasks in m13_tasks.py.
"""
import json
from collections import Counter
from pathlib import Path

from m13_questions import questions
from m13_sections import sections
from m13_tasks import tasks

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

practice = (1, 3, 4, 7, 9, 11, 12, 14, 16, 18, 20, 22, 26, 29, 33)
module = {
    "id": 13,
    "slug": "ileri-yapilar",
    "title": "İleri yapılar",
    "description": "for döngüsünün arkasındaki iterator protokolünü, değerleri istendikçe üreten generator'ları ve tembel boru hatlarını, fonksiyonları saran decorator'ları ve with bloğunu yöneten context manager'ları okuyup kendi kodunda yaz.",
    "contentVersion": 1,
    "estimatedMinutes": 150,
    "practiceIds": [f"m13-q{n:02d}" for n in practice],
    "sections": sections,
    "questions": questions,
}
(ROOT / "module-13.json").write_text(json.dumps(module, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

for item in tasks:
    assert item["sectionId"] in section_ids, item["id"]
tasks_path = ROOT / "writing-tasks.json"
existing = [t for t in json.loads(tasks_path.read_text(encoding="utf-8")) if t["moduleId"] != 13]
ordered = sorted(existing + tasks, key=lambda item: (item["moduleId"], int(item["id"].split("-w")[1])))
tasks_path.write_text(json.dumps(ordered, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("module-13.json ve", len(tasks), "yazma görevi yazıldı:", dict(kinds))
