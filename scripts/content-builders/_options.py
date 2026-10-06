"""Shared by build_m8.py and build_m9.py: gives every output question its answer options.

Output questions are answered by picking an option, so a question without options and an
answer cannot be answered in the app. The options live in output-options.json.
"""
import json
from pathlib import Path


def apply_output_options(questions):
    data = json.loads((Path(__file__).parent / "output-options.json").read_text(encoding="utf-8"))
    for question in questions:
        entry = data.get(question["id"])
        if entry:
            question["options"] = entry["options"]
            question["answer"] = entry["answer"]
    missing = [q["id"] for q in questions if q["type"] == "output" and not q.get("options")]
    assert not missing, f"Seçeneksiz çıktı sorusu: {missing}"
    for question in questions:
        if question.get("options"):
            assert question["answer"] in question["options"], question["id"]
            assert len(set(question["options"])) == len(question["options"]), f"{question['id']}: yinelenen seçenek"
