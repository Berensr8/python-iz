"""Builds content/module-14.json and the M14 writing tasks.

Run: PYTHONIOENCODING=utf-8 python scripts/content-builders/build_m14.py
Lesson sections live in m14_sections.py, questions in m14_questions.py, writing tasks in m14_tasks.py.
"""
import json
from collections import Counter
from pathlib import Path

from m14_questions import questions
from m14_sections import sections
from m14_tasks import tasks

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

practice = (1, 3, 4, 6, 8, 9, 10, 12, 13, 16, 19, 22, 27, 29, 35)
module = {
    "id": 14,
    "slug": "type-hints",
    "title": "Type hints",
    "description": "Fonksiyonlara, koleksiyonlara ve sınıflara tip ipucu yaz; Optional, TypedDict, Protocol, generics ve Callable'ı oku; mypy'nin neyi denetlediğini ve dış verinin neden ayrıca doğrulanması gerektiğini öğren.",
    "contentVersion": 1,
    "estimatedMinutes": 140,
    "practiceIds": [f"m14-q{n:02d}" for n in practice],
    "sections": sections,
    "questions": questions,
}
(ROOT / "module-14.json").write_text(json.dumps(module, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

for item in tasks:
    assert item["sectionId"] in section_ids, item["id"]
tasks_path = ROOT / "writing-tasks.json"
existing = [t for t in json.loads(tasks_path.read_text(encoding="utf-8")) if t["moduleId"] != 14]
ordered = sorted(existing + tasks, key=lambda item: (item["moduleId"], int(item["id"].split("-w")[1])))
tasks_path.write_text(json.dumps(ordered, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("module-14.json ve", len(tasks), "yazma görevi yazıldı:", dict(kinds))
