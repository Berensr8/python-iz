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
// "Düzelt" görevlerinde her hata tek başına ya da kombinasyonla düzeltilince en az bir test kalmalı (tam düzeltme hariç tüm alt kümeler).
async function checkPartialFixes(taskId, fixes) {
  const target = tasks.find(task => task.id === taskId);
  assert.ok(target, taskId);
  const names = Object.keys(fixes);
  for (let mask = 1; mask < (1 << names.length) - 1; mask++) {
    let partial = target.starterCode;
    const applied = names.filter((_, index) => mask & (1 << index));
    for (const name of applied) { const [from, to] = fixes[name]; assert.ok(partial.includes(from), `${taskId}: ${name}`); partial = partial.replace(from, to); }
    const results = await runtime.assess(py, partial, target.tests);
    check(`${taskId}: yalnız ${applied.join(" + ")} düzeltilirse testlerde kalır`, () => assert.ok(results.some(result => !result.passed)));
  }
  let everything = target.starterCode;
  for (const [from, to] of Object.values(fixes)) everything = everything.replace(from, to);
  const full = await runtime.assess(py, everything, target.tests);
  check(`${taskId}: tüm hatalar düzeltilince testler geçer`, () => assert.ok(full.every(result => result.passed), JSON.stringify(full.filter(result => !result.passed))));
}
await checkPartialFixes("m11-w2", {
  "paylaşılan puan listesi": ["class Player:\n    scores = []\n\n    def __init__(self, name):\n        self.name = name\n", "class Player:\n    def __init__(self, name):\n        self.name = name\n        self.scores = []\n"],
  "Captain'da super().__init__": ["    def __init__(self, name, team):\n        self.team = team", "    def __init__(self, name, team):\n        super().__init__(name)\n        self.team = team"],
  "boş listede best": ["return max(self.scores)", "return max(self.scores, default=0)"],
});
// Order matters: "bilinmeyen ürün" and "adet denetimi" both insert before the same line; the unknown-product check must come first.
await checkPartialFixes("m14-w2", {
  "adet dönüşümü": ["    name, qty = input().split()\n", "    name, raw = input().split()\n    qty = int(raw)\n"],
  "bilinmeyen ürün": ["    total += line_total(name, qty)", "    if price_of(name) is None:\n        print(\"bilinmeyen:\", name)\n        continue\n    total += line_total(name, qty)"],
  "adet denetimi": ["    total += line_total(name, qty)", "    if qty < 1:\n        print(\"geçersiz adet:\", name)\n        continue\n    total += line_total(name, qty)"],
  "dönüş ipucu": ["def price_of(name: str) -> int:", "def price_of(name: str) -> int | None:"],
});
await checkPartialFixes("m15-w2", {
  "iptal yutuluyor": ["        except asyncio.CancelledError:\n            return None\n", "        except asyncio.CancelledError:\n            raise\n"],
  "yanlış hata yakalanıyor": ["        except asyncio.CancelledError:\n            print(", "        except TimeoutError:\n            print("],
  "son deneme eksik": ["range(1, retries)", "range(1, retries + 1)"],
  "bağlantı yalnız başarıda kapanıyor": ["        else:\n            self.open -= 1\n", "        finally:\n            self.open -= 1\n"],
});
await checkPartialFixes("workshop4-fix", {
  "--words yönü": ['action="store_false"', 'action="store_true"'],
  "--min türü": ['parser.add_argument("--min", default=1)', 'parser.add_argument("--min", type=int, default=1)'],
  "olmayan dosya": ["        n = count(Path(name), args.words, args.min)", "        path = Path(name)\n        if not path.exists():\n            print(f\"bulunamadı: {name}\")\n            continue\n        n = count(path, args.words, args.min)"],
});
await checkPartialFixes("workshop5-fix", {
  "depolar ayrı sözlük": ["class Warehouse:\n    items = {}\n\n    def __init__(self, name):\n        self.name = name\n", "class Warehouse:\n    def __init__(self, name):\n        self.name = name\n        self.items = {}\n"],
  "ada göre sıralama": ["@dataclass(order=True)\nclass StockItem:\n    qty: int\n    sku: str", "@dataclass(order=True)\nclass StockItem:\n    sku: str\n    qty: int"],
  "yetersiz stok denetimi": ["        self.items[sku].qty -= qty", "        if qty > self.items[sku].qty:\n            raise ValueError(f\"yetersiz stok: {sku}\")\n        self.items[sku].qty -= qty"],
});
await checkPartialFixes("m13-w2", {
  "önbellek dışarıda": ["    def wrapper(n):\n        cache = {}\n", "    cache = {}\n    def wrapper(n):\n"],
  "sonucu döndür": ["        cache[n]\n    return wrapper", "        return cache[n]\n    return wrapper"],
  "wraps": ["    def wrapper(n):", "    @wraps(func)\n    def wrapper(n):"],
});
await checkPartialFixes("m12-w2", {
  "toplama yeni nesne döndürür": ["        self.cents += other.cents\n        return self", "        return Money(self.cents + other.cents)"],
  "__radd__": ["    def __lt__(self, other):", "    def __radd__(self, other):\n        return self if other == 0 else NotImplemented\n\n    def __lt__(self, other):"],
  "__lt__ yönü": ["return self.cents > other.cents", "return self.cents < other.cents"],
});
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
const loopBefore = py.runPython("import asyncio\ntype(asyncio.events._get_running_loop()).__name__ + ' ' + str(asyncio.run is asyncio.runners.run) + ' ' + type(asyncio.get_event_loop_policy()).__name__");
const asyncRun = await runtime.execute(py, 'import asyncio\nasync def job(name, delay):\n    await asyncio.sleep(delay)\n    print(name)\nasync def main():\n    loop = asyncio.get_running_loop()\n    start = loop.time()\n    await asyncio.gather(job("yavaş", 2), job("hızlı", 1))\n    print(f"{loop.time() - start:.1f}")\nasyncio.run(main())');
check("asyncio.run çalışır; beklemeler atlanır ama loop.time() gerçek Python'daki gibi ilerler", () => assert.deepEqual(asyncRun, { ok: true, output: "hızlı\nyavaş\n2.0" }));
const asyncTimeout = await runtime.execute(py, 'import asyncio\nasync def main():\n    try:\n        await asyncio.wait_for(asyncio.sleep(60), timeout=0.5)\n    except TimeoutError:\n        print("zaman aşımı")\nasyncio.run(main())');
check("asyncio zaman aşımı çalışır", () => assert.deepEqual(asyncTimeout, { ok: true, output: "zaman aşımı" }));
const asyncStuck = await runtime.execute(py, 'import asyncio\nasync def main():\n    await asyncio.Event().wait()\nasyncio.run(main())');
check("Sonsuza dek bekleyen asyncio programı sayfayı dondurmaz, hata verir", () => assert.ok(!asyncStuck.ok && asyncStuck.output.includes("sonsuza dek bekleyecekti"), asyncStuck.output));
const pyodideLoop = py.runPython("import asyncio\ntype(asyncio.events._get_running_loop()).__name__ + ' ' + str(asyncio.run is asyncio.runners.run) + ' ' + type(asyncio.get_event_loop_policy()).__name__");
check("asyncio çalıştırmasından sonra Pyodide'in kendi döngüsü geri yüklenir", () => { assert.equal(pyodideLoop, loopBefore); assert.equal(loopBefore, "WebLoop False WebLoopPolicy"); });
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
check("Ara sınavlar birbirinin sorusunu tekrar etmez", () => {
  const seen = new Map();
  for (const exam of milestones.exams) for (const id of exam.questionIds) {
    assert.ok(!seen.has(id), `${id} hem ${seen.get(id)} hem ${exam.id} içinde`);
    seen.set(id, exam.id);
  }
});
check("Ara Sınav 3: M1–M12'nin hepsi var, ağırlık M9–M12'de, pratik soruları yok, 10 kod ve 10 hata bulma/traceback", () => {
  const exam = milestones.exams.find(item => item.id === "midterm-3");
  const questions = examQuestions(exam, modules);
  assert.equal(questions.length, 28);
  const owner = question => Number(/^m(\d+)-/.exec(question.id)[1]);
  for (let id = 1; id <= 12; id++) assert.ok(questions.some(question => owner(question) === id), `M${id}`);
  assert.ok(questions.filter(question => owner(question) >= 9).length >= 14, "M9–M12 ağırlığı");
  const practice = new Set(modules.flatMap(module => module.practiceIds));
  assert.deepEqual(questions.filter(question => practice.has(question.id)).map(question => question.id), []);
  assert.equal(questions.filter(question => question.type === "code").length, 10);
  assert.equal(questions.filter(question => question.type === "bug" || question.type === "traceback").length, 10);
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
// Yerel Python örnekleri tarayıcıda çalışmaz (thread, süreç); npm run verify:local ile CPython'da doğrulanır.
check("Yerel Python örnekleri yalnız 'mixed' bölümlerde ve eksiksiz", () => {
  for (const module of modules) for (const section of module.sections.filter(item => item.localExample)) {
    const { code, output, note } = section.localExample;
    assert.equal(section.runtime, "mixed", `m${module.id}:${section.id}`);
    assert.ok(code?.trim() && output?.trim() && note?.trim(), `m${module.id}:${section.id}`);
    assert.ok(section.runtimeNote?.includes("yerel"), `m${module.id}:${section.id}: runtimeNote yerel örneği anmalı`);
  }
});
check("M1–M5 ders ve sorularında henüz öğretilmemiş yapı yok", () => {
  // [ad, desen, öğretildiği modül]. Öğrenci geri bildirimi: ilk derslerde type(x).__name__ görmek kafa karıştırdı.
  const rules = [
    ["__name__", /__name__/, 9], ["def", /\bdef\b/, 6], ["class", /\bclass\b/, 11], ["import", /\bimport\b/, 9],
    ["lambda", /\blambda\b/, 6], ["try", /\btry:/, 7], ["with", /^\s*with\b/m, 8], ["yield", /\byield\b/, 13],
  ];
  // Bilinçli istisnalar: deepcopy copy modülü olmadan gösterilemez; sözlük alanına göre key, lambda ile tanıtılır (M6'ya işaret ederek).
  const allowed = new Set(["m4:sorting-key:lambda", "m4-w2:lambda", "m5:deep-copy:import", "m5-q09:import", "m5-q20:import", "m5-q24:import"]);
  const found = [];
  for (const module of modules.filter(item => item.id <= 5)) {
    const items = [
      ...module.sections.flatMap(section => [[`m${module.id}:${section.id}`, section.code], [`m${module.id}:${section.id}`, section.realCode]]),
      ...module.questions.map(question => [question.id, [question.code, question.starterCode, question.solutionCode].filter(Boolean).join("\n")]),
      ...tasks.filter(task => task.moduleId === module.id).map(task => [task.id, `${task.starterCode}\n${task.solution}`]),
    ];
    for (const [where, text] of items) for (const [name, pattern, taught] of rules) {
      if (module.id < taught && pattern.test(text ?? "") && !allowed.has(`${where}:${name}`)) found.push(`${where}: ${name}`);
    }
  }
  assert.deepEqual(found, []);
});
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
  ["m14-w1", "average boş listede 0 döndürüyor", "solution", "    if not scores:\n        return None\n", "    if not scores:\n        return 0.0\n"],
  ["m14-w1", "dönüş ipucu None'ı söylemiyor", "solution", "def average(scores: list[int]) -> float | None:", "def average(scores: list[int]) -> float:"],
  ["m14-w1", "boş ad kabul ediliyor", "solution", "if not sep or not name.strip() or not score.strip().isdigit():", "if not sep or not score.strip().isdigit():"],
  ["m14-w3", "yinelenen kimlik kabul ediliyor", "solution", "        if item.id in self._items:\n            raise ValueError(f\"kimlik zaten var: {item.id}\")\n", ""],
  ["m14-w3", "all sıralamıyor", "solution", "for key in sorted(self._items)]", "for key in self._items]"],
  ["m14-w3", "remove her zaman True", "solution", "return self._items.pop(item_id, None) is not None", "self._items.pop(item_id, None)\n        return True"],
  ["m14-w3", "TypeVar sınırsız", "solution", "T = TypeVar(\"T\", bound=HasId)", "T = TypeVar(\"T\")"],
  ["m14-w3", "kayıtlar sınıf düzeyinde paylaşılıyor", "solution", "    def __init__(self) -> None:\n        self._items: dict[int, T] = {}\n", "    _items: dict = {}\n"],
  ["m15-w1", "sıra hiç verilmiyor", "solution", "        if i % step == step - 1:\n            await asyncio.sleep(0)\n", ""],
  ["m15-w1", "her adımda sıra veriliyor", "solution", "        if i % step == step - 1:\n", "        if True:\n"],
  ["m15-w3", "işler sırayla bekleniyor", "solution", "    results = await asyncio.gather(\n        *(asyncio.wait_for(download(seconds, size), timeout=limit) for _, seconds, size in jobs),\n        return_exceptions=True,\n    )\n", "    results = []\n    for _, seconds, size in jobs:\n        try:\n            results.append(await asyncio.wait_for(download(seconds, size), timeout=limit))\n        except Exception as error:\n            results.append(error)\n"],
  ["m15-w3", "süre sınırı yok", "solution", "asyncio.wait_for(download(seconds, size), timeout=limit)", "download(seconds, size)"],
  ["m15-w3", "hata diğerlerini durduruyor", "solution", "        return_exceptions=True,\n", ""],
  ["m15-w3", "her hata zaman aşımı sayılıyor", "solution", "isinstance(result, TimeoutError)", "isinstance(result, Exception)"],
  ["workshop4-build", "boş satırlar da sayılıyor", "solution", "for line in text.splitlines() if line.strip())", "for line in text.splitlines())"],
  ["workshop4-build", "olmayan dosya denetlenmiyor", "solution", "    if not path.exists():\n        print(f\"bulunamadı: {name}\")\n        continue\n", ""],
  ["workshop4-build", "eşitlerde ad sırası yok", "solution", "rows.sort(key=lambda row: (-size(row[1]), row[0]))", "rows.sort(key=lambda row: -size(row[1]))"],
  ["workshop4-build", "sıralama ters", "solution", "(-size(row[1]), row[0])", "(size(row[1]), row[0])"],
  ["workshop4-build", "boş metinde en uzun kelime hatası", "solution", "key=len, default=\"-\")", "key=len)"],
  ["workshop4-build", "--sort hiç uygulanmıyor", "solution", "if args.sort:", "if False:"],
  ["workshop5-build", "ship stok yeterliliğini denetlemiyor", "solution", "        if qty > self._stock[sku]:\n            raise ValueError(f\"yetersiz stok: {sku}\")\n", ""],
  ["workshop5-build", "low_stock sınırı dahil ediyor", "solution", "if qty < limit)", "if qty <= limit)"],
  ["workshop5-build", "sıfır adet kabul ediliyor", "solution", "if qty < 1:", "if qty < 0:"],
  ["workshop5-build", "aynı sku ikinci kez kaydediliyor", "solution", "        if product.sku in self._catalog:\n            raise ValueError(f\"zaten kayıtlı: {product.sku}\")\n", ""],
  ["workshop5-build", "Product dondurulmamış", "solution", "@dataclass(frozen=True)", "@dataclass"],
  ["workshop5-build", "negatif fiyat kabul ediliyor", "solution", "if self.price < 0:", "if False:"],
  ["workshop5-tests", "passes her zaman True", "solution", "return all(checks)", "return True"],
  ["workshop5-tests", "sınır vakası yok (hata4 kaçar)", "solution", "        a.low_stock(3) == [],\n", ""],
  ["workshop5-tests", "ikinci nesne denenmiyor (hata2 kaçar)", "solution", "        raises(lambda: b.ship(\"kalem\", 1)),\n", ""],
  ["workshop5-tests", "sıfır adet denenmiyor (hata3 kaçar)", "solution", "        raises(lambda: a.receive(\"silgi\", 0)),\n", ""],
  ["m13-w1", "yaş denetimi yok", "solution", " or not parts[2].isdigit()", ""],
  ["m13-w1", "sınır yaşı dışlanıyor", "solution", "record[\"yaş\"] >= min_age", "record[\"yaş\"] > min_age"],
  ["m13-w1", "alanlar kırpılmıyor", "solution", "[part.strip() for part in line.split(\",\")]", "line.split(\",\")"],
  ["m13-w3", "geri alma yok", "solution", "        store.clear()\n        store.update(snapshot)\n", ""],
  ["m13-w3", "hata yutuluyor", "solution", "        store.update(snapshot)\n        raise\n", "        store.update(snapshot)\n"],
  ["m13-w3", "sözlük yerinde değil, yeni nesneye bağlanıyor", "solution", "        store.clear()\n        store.update(snapshot)\n", "        store = snapshot\n"],
  ["m13-w3", "olmayan anahtar artırılabiliyor", "solution", "        key, value = op.split(\"+=\", 1)\n        if key not in store:\n            raise ValueError(f\"olmayan anahtar: {key}\")\n        store[key] += to_int(value, op)", "        key, value = op.split(\"+=\", 1)\n        store[key] = store.get(key, 0) + to_int(value, op)"],
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
  // Field names are searched with their quotes: a slug such as "type-hints" must not count as the hints field.
  for (const heavy of ["\"explanation\"", "\"prompt\"", "\"realCode\"", "\"hints\"", "\"solutionCode\"", "\"lineByLine\""]) assert.ok(!text.includes(heavy), `dizinde ${heavy} var`);
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
