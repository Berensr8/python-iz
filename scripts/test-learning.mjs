import assert from "node:assert/strict";
import { readFile, readdir } from "node:fs/promises";
import { loadPyodide } from "pyodide";
import { defaultProgress, parseProgress, markStudy, recordWriting, studyDay, exportProgress, importProgress, mergeProgress, encodeTransfer, decodeTransfer } from "../lib/progress-repository.ts";
import { isAnswerCorrect, wrongOptionFeedback, answerKind, selectedAnswer } from "../lib/answer-check.ts";
import { pythonErrorHint } from "../lib/python-error-hint.ts";
import { completeLesson } from "../lib/progress-repository.ts";
import { examQuestions, examByModule, examPassCount, milestoneAvailable, workshopSteps, workshopComplete, attemptLabel } from "../lib/milestones.ts";
import { createQuiz, answerQuiz, nextQuizQuestion, finishQuiz, expireQuiz, saveQuizDraft, initialDraft } from "../lib/quiz-engine.ts";
import { fileURLToPath } from "node:url";
import { buildContentIndex } from "../build/content-index.mjs";
import { practiceQuestions, previousModulePool, seededTestQuestions } from "../lib/question-selection.ts";
import "../public/python-runtime.js";

let checks = 0;
function check(name, fn) { fn(); checks++; console.log(`✓ ${name}`); }
const py = await loadPyodide();
const runtime = globalThis.pythonRuntime;
const tasks = [...JSON.parse(await readFile(new URL("../content/writing-tasks.json", import.meta.url), "utf8")), ...JSON.parse(await readFile(new URL("../content/workshop-tasks.json", import.meta.url), "utf8"))];
for (const task of tasks) {
  const results = await runtime.assess(py, task.solution, task.tests);
  check(`${task.id}: referans çözüm / ${task.tests.length} girdi`, () => assert.ok(results.every(result => result.passed), JSON.stringify(results)));
  const hardcoded = await runtime.assess(py, `print(${JSON.stringify(task.exampleOutput)})`, task.tests);
  check(`${task.id}: sabit örnek çıktı reddedilir`, () => assert.ok(hardcoded.some(result => !result.passed)));
  // A task whose starter already passes teaches nothing ("Düzelt" bugs must be real).
  const starter = await runtime.assess(py, task.starterCode, task.tests);
  check(`${task.id}: başlangıç kodu tek başına geçmez`, () => assert.ok(starter.some(result => !result.passed)));
}
const durationTask = tasks.find(task => task.id === "m10-w2");
assert.ok(durationTask);
for (const [label, partial] of [
  ["Yalnız saat dilimi düzeltilirse gün/negatif süre testleri kalır", durationTask.starterCode.replaceAll(".replace(tzinfo=timezone.utc)", ".astimezone(timezone.utc)")],
  ["Yalnız toplam saniye düzeltilirse saat dilimi testi kalır", durationTask.starterCode.replace("print((end - start).seconds)", "print(int((end - start).total_seconds()))")],
]) {
  const results = await runtime.assess(py, partial, durationTask.tests);
  check(label, () => assert.ok(results.some(result => !result.passed)));
}
// M11 "Düzelt" görevinin üç hatası: her biri tek başına ya da ikili kombinasyonla düzeltilince en az bir test kalmalı.
const playerTask = tasks.find(task => task.id === "m11-w2");
assert.ok(playerTask);
const playerFixes = {
  "paylaşılan puan listesi": ["class Player:\n    scores = []\n\n    def __init__(self, name):\n        self.name = name\n", "class Player:\n    def __init__(self, name):\n        self.name = name\n        self.scores = []\n"],
  "Captain'da super().__init__": ["    def __init__(self, name, team):\n        self.team = team", "    def __init__(self, name, team):\n        super().__init__(name)\n        self.team = team"],
  "boş listede best": ["return max(self.scores)", "return max(self.scores, default=0)"],
};
const fixNames = Object.keys(playerFixes);
for (let mask = 1; mask < 7; mask++) {
  let partial = playerTask.starterCode;
  const applied = fixNames.filter((_, index) => mask & (1 << index));
  for (const name of applied) { const [from, to] = playerFixes[name]; assert.ok(partial.includes(from), name); partial = partial.replace(from, to); }
  const results = await runtime.assess(py, partial, playerTask.tests);
  check(`m11-w2: yalnız ${applied.join(" + ")} düzeltilirse testlerde kalır`, () => assert.ok(results.some(result => !result.passed)));
}
const alternate = await runtime.assess(py, "value = int(input())\nprint(60 * value)", tasks[0].tests);
check("Farklı doğru çözüm kabul edilir", () => assert.ok(alternate.every(item => item.passed)));
await runtime.execute(py, "leaked_name = 99");
const isolated = await runtime.execute(py, "print(leaked_name)");
check("Çalışmalar arasında değişken sızmaz", () => assert.ok(!isolated.ok && isolated.output.includes("NameError")));
await runtime.execute(py, 'open("kalinti.txt", "w").write("eski")\nimport os\nos.chdir("/")');
const fresh = await runtime.execute(py, 'import os\nprint(os.listdir("."))');
check("Her çalışma boş bir klasörde başlar", () => assert.equal(fresh.output, "[]"));
await runtime.execute(py, 'import os, sys\nopen("izmod.py", "w").write("V = 1")\nimport izmod\nos.environ["IZ_LEAK"] = "1"\nsys.path.insert(0, "/yok")');
const reloaded = await runtime.execute(py, 'import os, sys\nopen("izmod.py", "w").write("V = 2")\nimport izmod\nprint(izmod.V, os.environ.get("IZ_LEAK"), "/yok" in sys.path)');
check("Kendi modülün, ortam değişkeni ve sys.path sonraki çalışmaya sızmaz", () => assert.equal(reloaded.output, "2 None False"));
const input = await runtime.execute(py, "print(input())\nprint(input())", "ilk\nikinci");
check("input sırası korunur", () => assert.equal(input.output, "ilk\nikinci"));
const missing = await runtime.execute(py, "input()", "");
check("Eksik girdi EOFError üretir", () => assert.ok(!missing.ok && missing.output.includes("EOFError")));
const traceback = await runtime.execute(py, "print(1 / 0)");
check("Traceback dosya, satır ve hata içerir", () => assert.ok(!traceback.ok && traceback.output.includes('cozum.py", line 1') && traceback.output.includes("ZeroDivisionError")));
check("Traceback çıktısında <exec> geçmez", () => assert.ok(!traceback.output.includes("<exec>")));
for (const code of ["if True\n    print(1)", " print(1)", "print(unknown)", "print('x' + 2)", "def divide():\n    return 1 / 0\ndivide()", "try:\n    int('x')\nexcept ValueError as e:\n    raise RuntimeError('üst hata') from e"]) {
  const result = await runtime.execute(py, code);
  check(`Öğrenci traceback korunur: ${code.split("\n")[0]}`, () => { assert.ok(!result.ok); assert.ok(result.output.includes('cozum.py')); assert.ok(!result.output.includes('<exec>'), result.output); });
}
const syntax = await runtime.execute(py, "if True\n    print(1)");
check("SyntaxError yalnız öğrenci dosyası ve hata satırını gösterir", () => { assert.ok(!syntax.output.includes("Traceback (most recent")); assert.ok(syntax.output.includes("if True")); assert.ok(pythonErrorHint(syntax.output)?.includes("iki nokta")); });
check("Türkçe ipuçları hata türüne göre, çıktı metnine göre değil seçilir", () => {
  for (const name of ["IndentationError", "TabError", "NameError", "TypeError"]) assert.ok(pythonErrorHint(`${name}: test`));
  assert.equal(pythonErrorHint("NameError örneği\nValueError: test"), null);
  assert.equal(pythonErrorHint("Başarılı çıktı"), null);
});
check("Ders çalıştırılmadan tamamlanamaz; bölüm ve XP bir kez kaydedilir", () => {
  assert.equal(completeLesson(defaultProgress, "m1:repl-syntax"), defaultProgress);
  const ran = { ...defaultProgress, lessonRuns: { "m1:repl-syntax": true } };
  assert.equal(completeLesson(ran, "m1:variables-types"), ran);
  const done = completeLesson(ran, "m1:repl-syntax");
  assert.equal(done.xp, 20); assert.ok(done.completedSections["m1:repl-syntax"]);
  assert.equal(completeLesson(done, "m1:repl-syntax"), done);
  assert.deepEqual(parseProgress({ ...done, lessonRuns: undefined }).lessonRuns, {});
  assert.ok(parseProgress({ ...done, lessonRuns: undefined }).completedSections["m1:repl-syntax"]);
});
const empty = await runtime.execute(py, "x = 1");
check("Çıktısız geçerli program kabul edilir", () => assert.deepEqual(empty, { ok: true, output: "" }));
const large = await runtime.execute(py, 'print("x" * 21000)');
check("Aşırı çıktı sınırlandırılır", () => assert.ok(!large.ok && large.output.includes("Çıktı sınırı")));
const old = { ...defaultProgress, version: 1, xp: 170, theme: "light", completedSections: { "m1:repl-syntax": true } };
delete old.writingDrafts; delete old.writingResults; delete old.writingHelp;
const migrated = parseProgress(old);
check("v1 ilerlemesi XP, tema ve dersler korunarak v3'e taşınır", () => {
  assert.equal(migrated.version, 3); assert.equal(migrated.activeQuiz, null); assert.deepEqual(migrated.creditedQuizIds, []); assert.equal(migrated.xp, 170); assert.equal(migrated.theme, "light");
  assert.equal(migrated.completedSections["m1:repl-syntax"], true); assert.deepEqual(migrated.writingDrafts, {});
});
check("Bozuk/gelecek sürüm reddedilir", () => {
  assert.throws(() => parseProgress({ ...old, xp: "yüz" }));
  assert.throws(() => parseProgress({ ...old, version: 99 }));
});
const date = new Date("2026-10-06T21:01:00Z");
check("İstanbul gece yarısı doğru güne geçer", () => assert.equal(studyDay(date), "2026-10-07"));
check("Seri aynı gün artmaz, ertesi gün artar, arada gün varsa sıfırlanır", () => {
  const p = { ...defaultProgress, streak: 3, lastStudyDate: "2026-10-06" };
  assert.equal(markStudy(p, new Date("2026-10-06T12:00:00Z")).streak, 3);
  assert.equal(markStudy(p, date).streak, 4);
  assert.equal(markStudy(p, new Date("2026-10-09T12:00:00Z")).streak, 1);
});
const helped = recordWriting(defaultProgress, "task", true, true);
const repeated = recordWriting(helped, "task", true, true);
check("Yazma XP'si yalnız ilk başarıda verilir", () => { assert.equal(helped.xp, 30); assert.equal(repeated.xp, 30); assert.equal(repeated.writingResults.task.attempts, 2); });
check("Yardımlı ve ipucusuz başarı ayrıdır", () => {
  assert.equal(helped.writingResults.task.independent, false);
  assert.equal(recordWriting(defaultProgress, "task", true, false).writingResults.task.independent, true);
});

// Kalıcı sınav oturumu (A1.8)
const sampleQuestions = ["a", "b", "c"].map(id => ({ id, type: "output", topic: id, prompt: id, answer: "1", hints: [], explanation: "" }));
const t0 = Date.parse("2026-10-06T09:00:00Z");
const withTest = (timed) => ({ ...defaultProgress, activeQuiz: createQuiz("s1", 1, "test", sampleQuestions, timed, false, t0) });
check("Oturum soru listesi kaynaktan bağımsız sabitlenir", () => {
  const source = structuredClone(sampleQuestions);
  const session = createQuiz("s0", 1, "practice", source, false, false, t0);
  source.reverse(); source[0].prompt = "değişti";
  assert.deepEqual(session.questions.map(q => q.id), ["a", "b", "c"]);
});
check("Yinelenen soru kimliği reddedilir", () => assert.throws(() => createQuiz("x", 1, "test", [sampleQuestions[0], sampleQuestions[0]], false)));
check("Yanıtlanmamış soru varken test elle bitirilemez", () => {
  const p = answerQuiz(withTest(false), "s1", "a", true, t0 + 1000);
  assert.equal(finishQuiz(p, "s1", "submitted", t0 + 2000), p);
});
check("Süre dolmadan zaman aşımı kaydı yazılmaz", () => {
  const p = withTest(true);
  assert.equal(finishQuiz(p, "s1", "timeout", t0 + 60_000), p);
});
check("Süre bitince sonuç bir kez kaydedilir, tekrar kayıt/XP yok", () => {
  const answered = answerQuiz(withTest(true), "s1", "a", true, t0 + 1000);
  const expired = expireQuiz(answered, t0 + 26 * 60_000);
  assert.equal(expired.attempts.length, 1); assert.equal(expired.attempts[0].reason, "timeout");
  assert.equal(expired.attempts[0].score, 33); assert.equal(expired.activeQuiz.completedAt, t0 + 25 * 60_000);
  const again = expireQuiz(expired, t0 + 27 * 60_000);
  assert.equal(again.attempts.length, 1); assert.equal(again.xp, expired.xp);
});
check("Süre dolduktan sonra gelen yanıt kabul edilmez", () => {
  const late = answerQuiz(withTest(true), "s1", "a", true, t0 + 26 * 60_000);
  assert.equal(late.activeQuiz.answers.a, undefined); assert.equal(late.attempts.length, 1);
});
check("Aynı soru iki kez yanıtlanamaz; sıradaki soru yalnız yanıttan sonra açılır", () => {
  let p = withTest(false);
  assert.equal(nextQuizQuestion(p, "s1", "a", t0), p);
  p = answerQuiz(p, "s1", "a", true, t0);
  assert.equal(answerQuiz(p, "s1", "a", false, t0), p);
  p = nextQuizQuestion(p, "s1", "a", t0);
  assert.equal(p.activeQuiz.index, 1);
});
check("Tüm sorular doğruysa test geçilir, sonraki modül açılır, ödül bir kez verilir", () => {
  let p = withTest(false);
  for (const q of sampleQuestions) { p = answerQuiz(p, "s1", q.id, true, t0); p = nextQuizQuestion(p, "s1", q.id, t0); }
  assert.equal(p.activeQuiz.finishReason, "submitted"); assert.equal(p.unlockedModule, 2);
  assert.equal(p.attempts.length, 1); assert.equal(p.xp, 3 * 10 + 100);
  const replay = finishQuiz({ ...p, activeQuiz: { ...p.activeQuiz, completedAt: null, finishReason: null, index: 2 } }, "s1", "submitted", t0);
  assert.equal(replay.attempts.length, 1); assert.equal(replay.xp, p.xp);
});
check("Testte ipucu sayılmaz, pratikte XP ipucuyla azalır", () => {
  let practice = { ...defaultProgress, activeQuiz: createQuiz("p1", 1, "practice", sampleQuestions, false, false, t0) };
  practice = saveQuizDraft(practice, "p1", "a", { choice: "1", fill: "", ordered: [], code: "", hints: 2, stdin: "" }, t0);
  assert.equal(answerQuiz(practice, "p1", "a", true, t0).xp, 6);
});
check("Yedek dışa/içe aktarma ilerlemeyi korur, yabancı dosyayı reddeder", () => {
  const p = { ...defaultProgress, xp: 55, completedSections: { "m1:bitwise": true } };
  assert.deepEqual(importProgress(exportProgress(p)), p);
  assert.throws(() => importProgress(JSON.stringify({ app: "baska", formatVersion: 1, progress: p })));
  assert.throws(() => importProgress("{bozuk"));
});
// Cevap kontrolü (A1.7)
const fillQ = { id: "f", type: "fill", answer: "-3:", acceptedAnswers: ["-3:", "-3:len(text)"] };
check("Boşluk doldurmada kabul edilen tüm yazımlar ve operatör çevresindeki boşluk kabul edilir", () => {
  for (const value of ["-3:", " -3 : ", "-3:len(text)", "-3 : len( text )"]) assert.ok(isAnswerCorrect(fillQ, value), value);
  for (const value of ["3:", "-3", ""]) assert.ok(!isAnswerCorrect(fillQ, value), value);
});
check("Kelime arasındaki boşluk korunur", () => {
  const q = { id: "n", type: "fill", answer: "not in" };
  assert.ok(isAnswerCorrect(q, "not  in")); assert.ok(!isAnswerCorrect(q, "notin"));
});
check("Seçmeli soru yalnız tam seçenekle doğru; yanlış seçeneğin gerekçesi döner", () => {
  const q = { id: "c", type: "traceback", answer: "TypeError", options: ["TypeError", "ValueError"], optionFeedback: { ValueError: "neden" } };
  assert.ok(isAnswerCorrect(q, "TypeError")); assert.ok(!isAnswerCorrect(q, "typeerror"));
  assert.equal(wrongOptionFeedback(q, "ValueError"), "neden"); assert.equal(wrongOptionFeedback(q, "TypeError"), undefined);
});
const moduleFiles = (await readdir(new URL("../content/", import.meta.url))).filter(name => /^module-\d+\.json$/.test(name)).sort();
const modules = await Promise.all(moduleFiles.map(async name => JSON.parse(await readFile(new URL(`../content/${name}`, import.meta.url), "utf8"))));
check("Modül dosyaları 1'den ardışık numaralı", () => assert.deepEqual(modules.map(item => item.id), modules.map((_, index) => index + 1)));
const milestones = JSON.parse(await readFile(new URL("../content/milestones.json", import.meta.url), "utf8"));
const checkpoint = examQuestions(examByModule(milestones.exams, 4), modules);
check("Ara sınav M1–M4'ten eşit kapsam ve dört yazma sorusu içerir", () => {
  assert.equal(checkpoint.length, 20); assert.equal(new Set(checkpoint.map(q => q.id)).size, 20);
  for (let i = 1; i <= 4; i++) assert.equal(checkpoint.filter(q => q.id.startsWith(`m${i}-`)).length, 5);
  assert.equal(checkpoint.filter(q => q.type === "code").length, 4);
});
check("M10 zorluk dağılımı 16 kolay / 16 orta / 8 zor", () => {
  assert.deepEqual([1, 2, 3].map(level => modules[9].questions.filter(q => q.difficulty === level).length), [16, 16, 8]);
});
// Kod sorusunun başlangıç kodu kendi başına geçmemeli ve çıktı sorularının doğru seçeneği gerçek çıktıyla aynı olmalı.
for (const module of modules.filter(item => item.id >= 11)) {
  for (const question of module.questions.filter(item => item.type === "code")) {
    const starter = await runtime.assess(py, question.starterCode, question.tests);
    check(`${question.id}: başlangıç kodu tek başına geçmez`, () => assert.ok(starter.some(result => !result.passed)));
  }
  check(`M${module.id}: çıktı sorusunun doğru seçeneği gerçek çıktıdır ve seçenekler benzersizdir`, () => {
    for (const question of module.questions.filter(item => item.type === "output")) {
      assert.equal(question.answer, question.expectedOutput.split("\n").join(" / "), question.id);
      assert.ok(question.options.includes(question.answer) && new Set(question.options).size === question.options.length, question.id);
    }
  });
  check(`M${module.id}: her bölümü en az bir soru ölçer ve üç zorluk düzeyi de vardır`, () => {
    for (const section of module.sections) assert.ok(module.questions.some(item => item.sectionId === section.id), section.id);
    for (const level of [1, 2, 3]) assert.ok(module.questions.some(item => item.difficulty === level), `zorluk ${level}`);
  });
}
check("M1–M2 gerçek örneklerinde öğretilmemiş fonksiyon ve döngü yok", () => {
  for (const module of modules.slice(0, 2)) for (const section of module.sections) assert.ok(!/(^|\n)\s*(def |for |while |try:|if )/.test(section.realCode), section.id);
  assert.ok(!modules[0].sections[0].code.includes("if "));
});
check("Ara sınav kilidi ve eski ilerleme uyumluluğu", () => {
  assert.equal(milestoneAvailable(defaultProgress, 4), false);
  assert.equal(milestoneAvailable({ ...defaultProgress, unlockedModule: 5 }, 4), true);
  const old = { ...defaultProgress }; delete old.workshopRead; delete old.lessonRuns;
  assert.deepEqual(parseProgress(old).workshopRead, {});
});
check("Ara sınav kaydolur, yenilenir ve modül açmaz; ödül tekrarlanmaz", () => {
  let p = { ...defaultProgress, unlockedModule: 5, activeQuiz: createQuiz("mid1", 4, "midterm", checkpoint, true, false, t0) };
  p = parseProgress(JSON.parse(JSON.stringify(p)));
  for (const q of checkpoint) { p = answerQuiz(p, "mid1", q.id, true, t0); p = nextQuizQuestion(p, "mid1", q.id, t0); }
  assert.equal(p.unlockedModule, 5); assert.equal(p.attempts[0].kind, "midterm"); assert.equal(p.attempts[0].score, 100);
  assert.equal(p.completedPractice.m4, undefined); assert.equal(p.xp, 300);
  assert.equal(finishQuiz(p, "mid1", "submitted", t0), p);
  assert.equal(parseProgress(p).activeQuiz.mode, "midterm");
});
check("Süreli ara sınav boşları yanlış sayar ve bir kez kapanır", () => {
  let p = { ...defaultProgress, unlockedModule: 5, activeQuiz: createQuiz("mid2", 4, "midterm", checkpoint, true, false, t0) };
  p = expireQuiz(p, t0 + 1500001);
  assert.equal(p.attempts[0].score, 0); assert.equal(p.attempts[0].kind, "midterm"); assert.equal(p.attempts[0].reason, "timeout");
  assert.equal(expireQuiz(p, t0 + 2000000), p);
});

const workshop1 = milestones.workshops.find(item => item.id === "workshop1");
check("Ara sınav/atölye kilidi modüle göre: M4 testi geçilince ya da M5 açılınca; ara sınav denemesi sayılmaz", () => {
  const passed = { kind: "module", moduleId: 4, score: 70, date: "2026-10-01T10:00:00.000Z", weakTopics: [] };
  assert.equal(milestoneAvailable({ ...defaultProgress, attempts: [passed] }, 4), true);
  assert.equal(milestoneAvailable({ ...defaultProgress, attempts: [{ ...passed, score: 69 }] }, 4), false);
  assert.equal(milestoneAvailable({ ...defaultProgress, attempts: [{ ...passed, kind: "midterm" }] }, 4), false, "ara sınav sonucu modül testi yerine geçmez");
  assert.equal(milestoneAvailable({ ...defaultProgress, unlockedModule: 5 }, 8), false, "M8 sonrası, M9 açılana kadar kapalı");
  assert.equal(milestoneAvailable({ ...defaultProgress, unlockedModule: 9 }, 8), true);
});
check("Atölye adımları sırayla açılır; durum ilerlemeden okunur", () => {
  const key = workshop1.steps[0].progressKey, fixTask = workshop1.steps[1].taskId, buildTask = workshop1.steps[2].taskId;
  const state = progress => workshopSteps(progress, workshop1).map(item => `${item.done ? "✓" : "·"}${item.open ? "açık" : "kilitli"}`);
  assert.deepEqual(state(defaultProgress), ["·açık", "·kilitli", "·kilitli"]);
  const read = { ...defaultProgress, workshopRead: { [key]: true } };
  assert.deepEqual(state(read), ["✓açık", "·açık", "·kilitli"]);
  const fixed = { ...read, writingResults: { [fixTask]: { passed: true, independent: true, attempts: 1 } } };
  assert.deepEqual(state(fixed), ["✓açık", "✓açık", "·açık"]);
  assert.equal(workshopComplete(fixed, workshop1), false);
  assert.equal(workshopComplete({ ...fixed, writingResults: { ...fixed.writingResults, [buildTask]: { passed: true, independent: false, attempts: 2 } } }, workshop1), true);
  assert.deepEqual(state({ ...defaultProgress, writingResults: { [fixTask]: { passed: true, independent: true, attempts: 1 } } }), ["·açık", "✓kilitli", "·kilitli"], "okuma adımı atlanamaz");
});
check("Deneme etiketi ve geçme sayısı veriden gelir", () => {
  assert.equal(attemptLabel(milestones.exams, { kind: "midterm", moduleId: 4 }), "Ara Sınav 1");
  assert.equal(attemptLabel(milestones.exams, { kind: "module", moduleId: 4 }), "Modül 4");
  assert.equal(attemptLabel(milestones.exams, { kind: "midterm", moduleId: 99 }), "Ara sınav (M99 sonrası)");
  assert.equal(examPassCount(20), 14); assert.equal(examPassCount(24), 17); assert.equal(examPassCount(30), 21);
});
check("Her ara sınav kendi süresini kullanır; geçersiz süreler reddedilir", () => {
  const long = createQuiz("uzun", 4, "midterm", checkpoint, true, false, t0, 35);
  assert.equal(long.deadline - long.startedAt, 35 * 60000);
  let p = parseProgress({ ...defaultProgress, unlockedModule: 5, activeQuiz: long });
  assert.equal(expireQuiz(p, t0 + 1500001).activeQuiz.completedAt, null, "25. dakikada bitmez");
  assert.equal(expireQuiz(p, t0 + 35 * 60000 + 1).attempts[0].reason, "timeout");
  for (const minutes of [10, 24, 61, 25.5]) assert.throws(() => parseProgress({ ...defaultProgress, activeQuiz: createQuiz("x", 4, "midterm", checkpoint, true, false, t0, minutes) }), undefined, `${minutes} dk geçersiz`);
});

for (const exam of milestones.exams) {
  const questions = examQuestions(exam, modules);
  const run = correct => {
    let p = parseProgress({ ...defaultProgress, unlockedModule: exam.afterModule + 1, activeQuiz: createQuiz(`gen-${exam.id}-${correct}`, exam.afterModule, "midterm", questions, true, false, t0, exam.minutes) });
    questions.forEach((q, index) => { p = answerQuiz(p, `gen-${exam.id}-${correct}`, q.id, index < correct, t0); p = nextQuizQuestion(p, `gen-${exam.id}-${correct}`, q.id, t0); });
    return p;
  };
  check(`${exam.title}: tam puan, geçme sınırı (${examPassCount(questions.length)} doğru) ve modül kilidine dokunmama`, () => {
    const full = run(questions.length), edge = run(examPassCount(questions.length)), below = run(examPassCount(questions.length) - 1);
    assert.equal(full.attempts[0].score, 100); assert.equal(full.attempts[0].kind, "midterm"); assert.equal(full.attempts[0].moduleId, exam.afterModule);
    assert.equal(attemptLabel(milestones.exams, full.attempts[0]), exam.title);
    assert.ok(edge.attempts[0].score >= 70, `sınırda ${edge.attempts[0].score}`); assert.ok(below.attempts[0].score < 70, `sınırın altında ${below.attempts[0].score}`);
    assert.ok(edge.xp - below.xp >= 80, "geçen deneme (100 XP) kalandan (20 XP) en az 80 XP fazla kazanır");
    assert.equal(full.unlockedModule, exam.afterModule + 1);
    assert.equal(parseProgress(full).attempts.length, 1);
  });
  check(`${exam.title}: kendi süresi dolunca bir kez kapanır, öncesinde açık kalır`, () => {
    const p = parseProgress({ ...defaultProgress, activeQuiz: createQuiz(`sure-${exam.id}`, exam.afterModule, "midterm", questions, true, false, t0, exam.minutes) });
    assert.equal(expireQuiz(p, t0 + exam.minutes * 60000 - 1000), p);
    const done = expireQuiz(p, t0 + exam.minutes * 60000 + 1);
    assert.equal(done.attempts.length, 1); assert.equal(done.attempts[0].reason, "timeout"); assert.equal(done.attempts[0].score, 0);
    assert.equal(expireQuiz(done, t0 + exam.minutes * 120000), done);
  });
}

const choiceQuestions = modules.flatMap(module => module.questions).filter(q => q.options?.length);
const positionsOf = (id) => createQuiz(id, 1, "practice", choiceQuestions, false, false, t0).questions.map(q => q.options.indexOf(q.answer));
check("Seçenekler her oturumda karışır: doğru cevap hep aynı konumda değil, her seçenek korunur", () => {
  const quiz = createQuiz("oturum-a", 1, "practice", choiceQuestions, false, false, t0);
  for (const q of quiz.questions) {
    const original = choiceQuestions.find(item => item.id === q.id);
    assert.deepEqual([...q.options].sort(), [...original.options].sort(), `${q.id}: seçenekler değişmemeli`);
    assert.ok(q.options.includes(q.answer), q.id);
  }
  const first = positionsOf("oturum-a").filter(index => index === 0).length / choiceQuestions.length;
  assert.ok(first < 0.4, `doğru cevap %${Math.round(first * 100)} oranında ilk sırada`);
  const original = choiceQuestions.filter(q => q.options[0] === q.answer).length / choiceQuestions.length;
  assert.ok(original > 0.6, "içerikte doğru cevap çoğunlukla ilk sırada; karıştırma bu yüzden şart");
});
check("Karıştırma aynı oturumda kararlı (yenilemede sıra değişmez), oturumlar arasında farklı, kayıt-okuma sonrası aynı", () => {
  assert.deepEqual(positionsOf("oturum-a"), positionsOf("oturum-a"));
  assert.notDeepEqual(positionsOf("oturum-a"), positionsOf("oturum-b"));
  const quiz = createQuiz("oturum-a", 1, "practice", choiceQuestions.slice(0, 20), false, false, t0);
  assert.deepEqual(parseProgress({ ...defaultProgress, activeQuiz: quiz }).activeQuiz.questions.map(q => q.options), quiz.questions.map(q => q.options));
});
check("Her soru cevaplanabilir: seçenek, boşluk, sıralama ya da kod girişi var; seçenekli sorunun cevabı seçeneklerde", () => {
  for (const q of modules.flatMap(module => module.questions)) {
    assert.notEqual(answerKind(q), "none", `${q.id} (${q.type}): cevap verilecek bir kontrol yok`);
    if (answerKind(q) === "choice") { assert.ok(q.options.length >= 3 && q.options.includes(q.answer), q.id); assert.equal(new Set(q.options).size, q.options.length, `${q.id}: yinelenen seçenek`); }
  }
});
check("Uçtan uca: her modülün pratiği, arayüzdeki cevap yoluyla doğru cevaplanınca %100 olur", () => {
  for (const module of modules) {
    const practice = module.practiceIds.map(id => module.questions.find(q => q.id === id));
    let p = { ...defaultProgress, unlockedModule: 18, activeQuiz: createQuiz(`uc-${module.id}`, module.id, "practice", practice, false, false, t0) };
    for (const q of p.activeQuiz.questions) {
      const draft = { ...initialDraft(q), choice: answerKind(q) === "choice" ? q.answer : "", fill: answerKind(q) === "fill" ? q.answer : "", ordered: answerKind(q) === "order" ? q.answer.split("\n") : [...(q.lines ?? [])] };
      const correct = answerKind(q) === "code" ? true : isAnswerCorrect(q, selectedAnswer(q, draft));
      assert.ok(correct, `M${module.id} ${q.id} (${q.type}): arayüz cevabıyla doğru sayılmadı`);
    }
  }
});
const fix = tasks.find(task => task.id === "workshop1-fix");
for (const [label, code] of [["Yalnız sınır", fix.starterCode.replace("amount > limit", "amount >= limit")], ["Yalnız toplama", fix.starterCode.replace("total = amount", "total += amount")]]) {
  const results = await runtime.assess(py, code, fix.tests);
  check(`Atölye 1: ${label} düzeltmesi yeterli değil`, () => assert.ok(results.some(result => !result.passed)));
}
// Atölye 2 ve 3: kısmi ya da bozuk çözümler testlerde kalmalı (her gereksinim ayrı ayrı sınanır).
// [görev, açıklama, başlangıç kodu mu çözüm mü, değiştirilecek metin, yeni metin]
const mutants = [
  ["workshop2-fix", "yalnız paylaşılan varsayılan düzeltildi", "starter", "def clean_names(names, seen=[]):\n", "def clean_names(names):\n    seen = []\n"],
  ["workshop2-fix", "yalnız boş ad filtresi eklendi", "starter", "if cleaned not in seen:", "if cleaned and cleaned not in seen:"],
  ["workshop2-fix", "yalnız sorted kaldırıldı", "starter", "return sorted(seen)", "return seen"],
  ["workshop2-fix", "çözüm ama sıra sıralanıyor", "solution", "    return result\n", "    return sorted(result)\n"],
  ["workshop2-fix", "çözüm ama varsayılan liste paylaşılıyor", "solution", "def clean_names(names):\n    result = []\n", "def clean_names(names, result=[]):\n"],
  ["workshop2-fix", "çözüm ama boş ad kalıyor", "solution", "if cleaned and cleaned not in result", "if cleaned not in result"],
  ["workshop2-build", "boş sonuç \"bos\" olmuyor", "solution", ' or "bos"', ""],
  ["workshop2-build", "önce küçültüp sonra çeviriyor (İ bozulur)", "solution", "title.translate(TURKISH).lower()", "title.lower().translate(TURKISH)"],
  ["workshop2-build", "Türkçe harfler çevrilmiyor", "solution", "title.translate(TURKISH).lower()", "title.lower()"],
  ["workshop2-build", "ayırıcılar tek tire olmuyor", "solution", "elif word:", "else:"],
  ["workshop2-tests", "yalnız üç hata yakalayan vakalar", "solution", '    ("  a -- b  ", "a-b"),\n    ("a -- b", "a-b"),\n', ""],
  ["workshop2-tests", "yanlış beklenen değer (doğru sürüm kalır)", "solution", '("Işık", "isik")', '("Işık", "ışık")'],
  ["workshop2-tests", "passes her zaman True", "solution", "return all(implementation(title) == expected for title, expected in cases)", "return True"],
  ["workshop3-fix", "hatalı satır doğrulanmıyor", "solution", "if len(row) != 3 or not row[1].strip().isdigit() or not row[2].strip().isdigit():", "if False:"],
  ["workshop3-fix", "geçerli satır yokken sıfıra bölünüyor", "solution", "average = total / valid if valid else 0.0", "average = total / valid"],
  ["workshop3-fix", "alan sayısı denetlenmiyor", "solution", "len(row) != 3 or ", ""],
  ["workshop3-fix", "başlangıç kodu yalnız csv ile okunuyor", "starter", 'name, qty, price = line.rstrip("\\n").split(",")', "name, qty, price = next(__import__('csv').reader([line.rstrip('\\n')]))"],
  ["workshop3-build", "satır numarası 1'den başlıyor", "solution", "start=2", "start=1"],
  ["workshop3-build", "ürün adı kırpılmıyor", "solution", "row[0].strip()", "row[0]"],
  ["workshop3-build", "anahtarlar sıralanmıyor", "solution", "sort_keys=True", "sort_keys=False"],
  ["workshop3-build", "Türkçe karakterler kaçışlanıyor", "solution", "ensure_ascii=False, ", ""],
  ["workshop3-build", "adet yerine fiyat önce denetleniyor", "solution", 'elif not is_count(row[1]):\n            reason = "adet sayı değil"\n        elif not is_count(row[2]):\n            reason = "fiyat sayı değil"', 'elif not is_count(row[2]):\n            reason = "fiyat sayı değil"\n        elif not is_count(row[1]):\n            reason = "adet sayı değil"'],
];
for (const [id, label, from, find, replacement] of mutants) {
  const task = tasks.find(item => item.id === id);
  const source = from === "starter" ? task.starterCode : task.solution;
  assert.ok(source.includes(find), `${id} / ${label}: değiştirilecek metin bulunamadı (test boşa çalışırdı)`);
  const results = await runtime.assess(py, source.replace(find, replacement), task.tests);
  check(`${id}: ${label} — testlerde kalır`, () => assert.ok(results.some(result => !result.passed), "bozuk çözüm bütün testleri geçti"));
}

// --- Modülleri ihtiyaç olunca yükleme: dizin ve soru seçimi ---
const contentIndex = buildContentIndex(fileURLToPath(new URL("../content/", import.meta.url)));
check("Modül dizini her modülün yapısını verir, metni taşımaz", () => {
  assert.deepEqual(contentIndex.map(item => item.id), modules.map(item => item.id));
  for (const [index, module] of modules.entries()) {
    const summary = contentIndex[index];
    assert.deepEqual(summary.sections.map(item => item.id), module.sections.map(item => item.id));
    assert.deepEqual(summary.sections.map(item => item.title), module.sections.map(item => item.title));
    assert.deepEqual(summary.questions.map(item => item.id), module.questions.map(item => item.id));
    assert.deepEqual(summary.practiceIds, module.practiceIds);
    for (const [position, question] of module.questions.entries()) {
      const light = summary.questions[position];
      assert.equal(light.type, question.type); assert.equal(light.sectionId, question.sectionId); assert.equal(light.difficulty, question.difficulty);
    }
  }
  const text = JSON.stringify(contentIndex);
  for (const heavy of ["explanation", "\"prompt\"", "realCode", "hints", "solutionCode", "lineByLine"]) assert.ok(!text.includes(heavy), `dizinde ${heavy} var`);
});
check("Dizin tam içeriğin küçük bir kısmıdır (ana pakette kalan bu)", () => {
  const full = JSON.stringify(modules).length, light = JSON.stringify(contentIndex).length;
  assert.ok(light < full * 0.2, `dizin ${light} bayt, tam içerik ${full} bayt`);
});
check("Her sorunun modül kimliği kimlik önekinden ve dizinden aynı çıkar", () => {
  const owner = new Map(contentIndex.flatMap(module => module.questions.map(question => [question.id, module.id])));
  for (const [id, moduleId] of owner) assert.equal(Number(/^m(\d+)-/.exec(id)[1]), moduleId, id);
});
check("Test soruları: ilk modülde önceki konu yok; sonrakilerde dörtte biri yerine 4/18 önceki modüllerden", () => {
  const first = seededTestQuestions(modules[0], [], 7, 18);
  assert.equal(first.length, 18); assert.equal(new Set(first.map(q => q.id)).size, 18);
  assert.ok(first.every(q => q.id.startsWith("m1-")));
  assert.ok(first.filter(q => q.type === "code").length >= 3, "yazma sorusu garantisi");
  assert.deepEqual(previousModulePool(1, 7), []);
  const pool = previousModulePool(10, 7);
  const previous = pool.flatMap(id => modules[id - 1].questions);
  const mixed = seededTestQuestions(modules[9], previous, 7, 18);
  assert.equal(mixed.length, 18); assert.equal(new Set(mixed.map(q => q.id)).size, 18);
  assert.equal(mixed.filter(q => !q.id.startsWith("m10-")).length, 4);
  assert.ok(mixed.filter(q => q.id.startsWith("m10-") && q.type === "code").length >= 3);
});
check("Önceki modül havuzu: en çok 4 farklı modül, hepsi öncekilerden, aynı tohumla aynı, farklı tohumla farklı", () => {
  for (const moduleId of [2, 3, 5, 10, 18]) {
    const pool = previousModulePool(moduleId, 12345);
    assert.ok(pool.length >= 1 && pool.length <= 4, `M${moduleId}: ${pool.length}`);
    assert.equal(new Set(pool).size, pool.length); assert.ok(pool.every(id => id >= 1 && id < moduleId));
  }
  assert.deepEqual(previousModulePool(10, 99), previousModulePool(10, 99));
  const seen = new Set(Array.from({ length: 40 }, (_, seed) => previousModulePool(10, seed + 1).join(",")));
  assert.ok(seen.size > 5, "havuz her seferinde aynı çıkıyor");
  assert.ok(previousModulePool(18, 5).length <= 4, "M18 testi en çok dört önceki modül yükler");
});
check("Pratik soruları practiceIds sırasıyla gelir", () => {
  for (const module of modules) assert.deepEqual(practiceQuestions(module).map(q => q.id), module.practiceIds);
});

// --- Cihazlar arası aktarım: birleştirme ve aktarım kodu ---
const phone = parseProgress({ ...defaultProgress, xp: 300, streak: 4, lastStudyDate: "2026-10-05", unlockedModule: 3, theme: "light",
  completedSections: { "m1:a": true, "m1:b": true }, lessonRuns: { "m1:a": true }, hintUsage: { "m1-q01": 1 },
  questionResults: { "m1-q01": { correct: 2, wrong: 1 }, "m1-q02": { correct: 1, wrong: 0 } },
  attempts: [{ kind: "module", moduleId: 1, score: 80, date: "2026-10-01T10:00:00.000Z", weakTopics: [] }],
  writingResults: { "m1-w1": { passed: true, independent: false, attempts: 3 } }, writingDrafts: { "m1-w1": "telefon taslağı" },
  creditedQuizIds: ["s1"] });
const laptop = parseProgress({ ...defaultProgress, xp: 450, streak: 7, lastStudyDate: "2026-10-06", unlockedModule: 2, theme: "dark",
  completedSections: { "m1:b": true, "m2:c": true }, hintUsage: { "m1-q01": 3 },
  questionResults: { "m1-q01": { correct: 1, wrong: 4 }, "m2-q01": { correct: 1, wrong: 0 } },
  attempts: [{ kind: "module", moduleId: 1, score: 80, date: "2026-10-01T10:00:00.000Z", weakTopics: [] }, { kind: "module", moduleId: 2, score: 90, date: "2026-10-04T10:00:00.000Z", weakTopics: [] }],
  writingResults: { "m1-w1": { passed: true, independent: true, attempts: 1 }, "m2-w1": { passed: false, independent: false, attempts: 2 } },
  writingDrafts: { "m1-w1": "bilgisayar taslağı", "m2-w1": "yeni görev" }, creditedQuizIds: ["s1", "s2"] });
const merged = mergeProgress(phone, laptop);
check("Birleştirme: tamamlananlar birleşir, hiçbir şey kaybolmaz", () => {
  assert.deepEqual(Object.keys(merged.completedSections).sort(), ["m1:a", "m1:b", "m2:c"]);
  assert.equal(merged.lessonRuns["m1:a"], true);
  assert.equal(merged.unlockedModule, 3);
  assert.deepEqual([...merged.creditedQuizIds].sort(), ["s1", "s2"]);
});
check("Birleştirme: sayaçlar toplanmaz, büyüğü alınır (çift sayım yok)", () => {
  assert.equal(merged.xp, 450);
  assert.deepEqual(merged.questionResults["m1-q01"], { correct: 2, wrong: 4 });
  assert.equal(merged.hintUsage["m1-q01"], 3);
  assert.equal(merged.attempts.length, 2, "aynı test iki kez sayılmamalı");
  assert.deepEqual(merged.attempts.map(item => item.date), ["2026-10-01T10:00:00.000Z", "2026-10-04T10:00:00.000Z"]);
});
check("Birleştirme: seri en son çalışılan taraftan gelir; tema yerel kalır", () => {
  assert.equal(merged.streak, 7);
  assert.equal(merged.lastStudyDate, "2026-10-06");
  assert.equal(mergeProgress(laptop, phone).streak, 7);
  assert.equal(merged.theme, "light");
});
check("Birleştirme: yazma sonucu ve taslak — başarı ve ipucusuzluk korunur, yerel taslak ezilmez", () => {
  assert.deepEqual(merged.writingResults["m1-w1"], { passed: true, independent: true, attempts: 3 });
  assert.equal(merged.writingResults["m2-w1"].passed, false);
  assert.equal(merged.writingDrafts["m1-w1"], "telefon taslağı");
  assert.equal(merged.writingDrafts["m2-w1"], "yeni görev");
});
check("Birleştirme: kendisiyle birleşince değişmez, girdileri bozmaz", () => {
  assert.deepEqual(mergeProgress(phone, phone), phone);
  const before = structuredClone(laptop); mergeProgress(phone, laptop);
  assert.deepEqual(laptop, before);
});
const withExam = createQuiz("canli", 1, "test", modules[0].questions.slice(0, 3), true);
check("Birleştirme: yerel canlı sınav korunur, gelen sınav alınmaz", () => {
  assert.equal(mergeProgress({ ...phone, activeQuiz: withExam }, laptop).activeQuiz?.id, "canli");
  assert.equal(mergeProgress(phone, { ...laptop, activeQuiz: withExam }).activeQuiz, null);
});
const code = await encodeTransfer({ ...phone, activeQuiz: withExam });
const decoded = await decodeTransfer(code);
check("Aktarım kodu: gidiş-dönüş ilerlemeyi korur ve canlı sınavı taşımaz", () => {
  assert.ok(code.startsWith("PYIZ1.") && /^[A-Za-z0-9._-]+$/.test(code));
  assert.deepEqual(decoded, { ...phone, activeQuiz: null });
});
const wrapped = await decodeTransfer(code.replace(/(.{60})/g, "$1\n  "));
check("Aktarım kodu: mesajlaşma uygulamasının eklediği satır sonları ve boşluklar sorun olmaz", () => assert.deepEqual(wrapped, decoded));
const bigCode = await encodeTransfer(parseProgress({ ...defaultProgress, writingDrafts: Object.fromEntries(Array.from({ length: 30 }, (_, index) => [`t${index}`, "print('merhaba')\n".repeat(300)])) }));
check("Aktarım kodu: büyük bir ilerleme makul boyutta kalır", () => assert.ok(bigCode.length < 30000, `kod ${bigCode.length} karakter`));
const b64url = bytes => btoa(String.fromCharCode(...bytes)).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
const outcome = text => decodeTransfer(text).then(() => "KABUL EDİLDİ", error => error.message);
const rejected = [];
for (const [label, bad] of [["rastgele metin", "merhaba dünya"], ["yanlış önek", "PYIZ2." + code.slice(6)], ["kesilmiş", code.slice(0, code.length - 40)],
  ["bozuk karakter", "PYIZ1.***"], ["gzip değil", "PYIZ1." + b64url(new TextEncoder().encode("düz metin"))], ["boş", "PYIZ1."]]) rejected.push([label, await outcome(bad)]);
check("Aktarım kodu: bozuk, kesik ve yabancı kodlar anlaşılır hatayla reddedilir", () => {
  for (const [label, result] of rejected) assert.ok(result !== "KABUL EDİLDİ" && result.length > 5, `${label}: ${result}`);
});
const foreignResult = await outcome("PYIZ1R." + b64url(new TextEncoder().encode(JSON.stringify({ app: "baska", formatVersion: 1, progress: phone }))));
const bombStream = new CompressionStream("gzip"); const bombWriter = bombStream.writable.getWriter(); void bombWriter.write(new Uint8Array(12 * 1024 * 1024)); void bombWriter.close();
const bombResult = await outcome("PYIZ1." + b64url(new Uint8Array(await new Response(bombStream.readable).arrayBuffer())));
check("Aktarım kodu: yabancı uygulama kodu ve şişirilmiş (sıkıştırma bombası) kod reddedilir", () => {
  assert.notEqual(foreignResult, "KABUL EDİLDİ"); assert.match(bombResult, /büyük/);
});
const rawResult = await decodeTransfer("PYIZ1R." + b64url(new TextEncoder().encode(JSON.stringify({ app: "python-iz", formatVersion: 1, progress: phone }))));
check("Aktarım kodu: sıkıştırmasız yedek biçimi de açılır", () => assert.deepEqual(rawResult, phone));

console.log(`\n${checks} regresyon kontrolü geçti; ${tasks.reduce((sum, task) => sum + task.tests.length, 0)} yazma referans vakası doğrulandı.`);
