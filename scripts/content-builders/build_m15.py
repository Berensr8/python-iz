"""Builds content/module-15.json and the M15 writing tasks.

Run: PYTHONIOENCODING=utf-8 python scripts/content-builders/build_m15.py
Lesson sections live in m15_sections.py, questions in m15_questions.py, writing tasks in m15_tasks.py.
"""
import json
from collections import Counter
from pathlib import Path

from m15_questions import questions
from m15_sections import sections
from m15_tasks import tasks

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

practice = (1, 3, 5, 7, 9, 10, 12, 14, 17, 19, 25, 30, 33, 35, 38)
module = {
    "id": 15,
    "slug": "concurrency",
    "title": "Eşzamanlılık",
    "description": "I/O ve CPU bağımlı işi ayır; threading, thread havuzu, GIL ve multiprocessing'i oku; async/await, görevler, zaman aşımı, iptal ve paylaşılan veri hatalarını asyncio ile tarayıcıda çalıştırarak öğren.",
    "contentVersion": 1,
    "estimatedMinutes": 150,
    "practiceIds": [f"m15-q{n:02d}" for n in practice],
    "sections": sections,
    "questions": questions,
}
(ROOT / "module-15.json").write_text(json.dumps(module, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

for item in tasks:
    assert item["sectionId"] in section_ids, item["id"]
tasks_path = ROOT / "writing-tasks.json"
existing = [t for t in json.loads(tasks_path.read_text(encoding="utf-8")) if t["moduleId"] != 15]
ordered = sorted(existing + tasks, key=lambda item: (item["moduleId"], int(item["id"].split("-w")[1])))
tasks_path.write_text(json.dumps(ordered, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("module-15.json ve", len(tasks), "yazma görevi yazıldı:", dict(kinds))
