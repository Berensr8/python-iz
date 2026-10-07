"""Builds Ara Sınav 3 (after M12) into content/milestones.json.

Each module gets a list of question types (older modules fewer, M9–M12 the most). For each slot the
question is picked from that module's pool, skipping questions used in earlier exams and practice
questions (the learner has just seen those), avoiding a second question from the same lesson section
where possible and preferring harder questions. The choice is deterministic, so rerunning gives the
same exam. Only midterm-3 is replaced; the other exams and the workshops are left untouched.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2] / "content"

PLAN = {
    1: ["output"],
    2: ["fill"],
    3: ["code"],
    4: ["bug"],
    5: ["output", "code"],
    6: ["bug", "code"],
    7: ["traceback", "order"],
    8: ["code", "bug"],
    9: ["output", "bug", "code", "traceback"],
    10: ["output", "bug", "code", "traceback"],
    11: ["output", "code", "traceback", "code"],
    12: ["output", "code", "bug", "code"],
}

data = json.loads((ROOT / "milestones.json").read_text(encoding="utf-8"))
used = {qid for exam in data["exams"] if exam["id"] != "midterm-3" for qid in exam["questionIds"]}

chosen = []
for module_id, slots in PLAN.items():
    module = json.loads((ROOT / f"module-{module_id:02d}.json").read_text(encoding="utf-8"))
    practice = set(module["practiceIds"])
    taken_sections = set()
    for kind in slots:
        pool = [q for q in module["questions"] if q["type"] == kind and q["id"] not in used and q["id"] not in chosen]
        assert pool, (module_id, kind)
        # Fresh section first, then not a practice question, then harder, then later in the module (later ids lean harder).
        pool.sort(key=lambda q: (q["sectionId"] in taken_sections, q["id"] in practice, -q["difficulty"], -int(q["id"].split("-q")[1])))
        pick = pool[0]
        chosen.append(pick["id"])
        taken_sections.add(pick["sectionId"])
        print(f"{pick['id']:>8} {kind:9} z{pick['difficulty']} {pick['sectionId']:22} {'(pratik)' if pick['id'] in practice else ''} {pick['prompt'][:70]}")

exam = {
    "id": "midterm-3",
    "afterModule": 12,
    "title": "Ara Sınav 3",
    "scope": "M1–M12",
    "minutes": 45,
    "description": "On iki modülü birlikte tekrar eder. En çok soru son öğrendiklerinden (M9–M12: modüller, standart kütüphane ve iki OOP modülü) gelir; önceki modüllerden de en az birer soru var. On soru kod yazmayı, on soru hata bulma ve traceback okumayı ölçer. Önceki ara sınavların ve modül pratiklerinin soruları kullanılmaz. İpuçları kapalı, çözüm açıklamaları sonda.",
    "questionIds": chosen,
}
data["exams"] = [item for item in data["exams"] if item["id"] != "midterm-3"] + [exam]
data["exams"].sort(key=lambda item: item["afterModule"])
(ROOT / "milestones.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(len(chosen), "soru yazıldı")
