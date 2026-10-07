"""Shared question helper for the part-file module builders (m11_*.py, m12_*.py, ...).

    questions, q = make_questions("m12")

q() normalises one question and appends it with the next id (m12-q01, m12-q02, ...):
- output: the answer is derived from expectedOutput (multi-line output becomes "line1 / line2"),
  so the answer key can never drift from what the code prints. `options` must contain it.
- fill: acceptedAnswers defaults to [answer]; solutionCode is the code with ___ replaced by the answer.
- order: pass answer_lines (the correct order) and perm (indices giving the shuffled display order).
- code/order: solutionCode defaults to answer.
- traceback: answer is expectedError.
- options are rotated by the question number so the right answer is not always first
  (the app also shuffles them per session).
"""


def c(text):
    return text.strip("\n")


def flat(text):
    """Multi-line output as one option line (options are single-line buttons)."""
    return " / ".join(text.split("\n"))


def make_questions(prefix):
    questions = []

    def q(**fields):
        for key in ("code", "expectedOutput", "answer", "solutionCode", "starterCode"):
            if key in fields and isinstance(fields[key], str):
                fields[key] = c(fields[key])
        kind = fields["type"]
        number = len(questions) + 1
        if "tests" in fields:
            for test in fields["tests"]:
                test["expectedOutput"] = c(test["expectedOutput"])
        if kind == "output":
            fields["answer"] = flat(fields["expectedOutput"])
        if kind == "fill":
            fields["acceptedAnswers"] = fields.get("acceptedAnswers", [fields["answer"]])
            fields["solutionCode"] = fields["code"].replace("___", fields["answer"], 1)
        if kind == "order":
            lines = fields.pop("answer_lines")
            perm = fields.pop("perm")
            fields["answer"] = "\n".join(lines)
            fields["lines"] = [lines[i] for i in perm]
            assert fields["lines"] != lines and sorted(fields["lines"]) == sorted(lines), (number, "perm")
        if kind in ("code", "order") and "solutionCode" not in fields:
            fields["solutionCode"] = fields["answer"]
        if kind == "traceback":
            fields["answer"] = fields["expectedError"]
        if fields.get("options"):
            options = list(fields["options"])
            assert fields["answer"] in options, (number, "answer not in options")
            assert len(set(options)) == len(options), (number, "duplicate options")
            shift = len(questions) % len(options)
            fields["options"] = options[-shift:] + options[:-shift] if shift else options
        if fields.get("optionFeedback"):
            wrong = {option for option in fields["options"] if option != fields["answer"]}
            assert set(fields["optionFeedback"]) == wrong, (number, "optionFeedback keys")
        questions.append({"id": f"{prefix}-q{number:02d}", **fields})

    return questions, q
