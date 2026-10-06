import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { loadPyodide } from "pyodide";
import { defaultProgress, parseProgress, markStudy, recordWriting, studyDay, exportProgress, importProgress } from "../lib/progress-repository.ts";
import { isAnswerCorrect, wrongOptionFeedback } from "../lib/answer-check.ts";
import { createQuiz, answerQuiz, nextQuizQuestion, finishQuiz, expireQuiz, saveQuizDraft } from "../lib/quiz-engine.ts";
import "../public/python-runtime.js";

let checks = 0;
function check(name, fn) { fn(); checks++; console.log(`✓ ${name}`); }
const py = await loadPyodide();
const runtime = globalThis.pythonRuntime;
const tasks = JSON.parse(await readFile(new URL("../content/writing-tasks.json", import.meta.url), "utf8"));
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
console.log(`\n${checks} regresyon kontrolü geçti; ${tasks.reduce((sum, task) => sum + task.tests.length, 0)} atölye referans vakası doğrulandı.`);
