import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { loadPyodide } from "pyodide";
import { defaultProgress, parseProgress, markStudy, recordWriting, studyDay } from "../lib/progress-repository.ts";
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
}
const alternate = await runtime.assess(py, "value = int(input())\nprint(60 * value)", tasks[0].tests);
check("Farklı doğru çözüm kabul edilir", () => assert.ok(alternate.every(item => item.passed)));
await runtime.execute(py, "leaked_name = 99");
const isolated = await runtime.execute(py, "print(leaked_name)");
check("Çalışmalar arasında değişken sızmaz", () => assert.ok(!isolated.ok && isolated.output.includes("NameError")));
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
check("v1 ilerlemesi XP, tema ve dersler korunarak v2'ye taşınır", () => {
  assert.equal(migrated.version, 2); assert.equal(migrated.xp, 170); assert.equal(migrated.theme, "light");
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
console.log(`\n${checks} regresyon kontrolü geçti; ${tasks.length * 4} atölye referans vakası doğrulandı.`);
