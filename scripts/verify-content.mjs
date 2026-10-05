import { readFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import path from "node:path";
import { loadPyodide } from "pyodide";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const files = ["content/module-01.json", "content/module-02.json"];
const modules = await Promise.all(files.map(async (file) => JSON.parse(await readFile(path.join(root, file), "utf8"))));
const pyodide = await loadPyodide();
const version = pyodide.runPython("import sys; tuple(sys.version_info[:3])").toJs();

if (version[0] < 3 || (version[0] === 3 && version[1] < 12)) {
  throw new Error(`Python 3.12+ gerekli; doğrulayıcı ${version.join(".")} çalıştırıyor.`);
}

let checked = 0;
const failures = [];

async function execute(code) {
  const stdout = [];
  const stderr = [];
  pyodide.setStdout({ batched: (value) => stdout.push(value) });
  pyodide.setStderr({ batched: (value) => stderr.push(value) });
  try {
    await pyodide.runPythonAsync(code);
    return { output: [...stdout, ...stderr].join("\n").trimEnd(), error: null };
  } catch (error) {
    const text = String(error);
    const name = text.match(/\n([A-Za-z]+(?:Error|Exception)):/)?.[1] ?? text.match(/^([A-Za-z]+(?:Error|Exception)):/)?.[1] ?? "PythonError";
    return { output: [...stdout, ...stderr].join("\n").trimEnd(), error: name };
  }
}

async function verifyCode(label, code, expectedOutput, expectedError) {
  const result = await execute(code);
  checked += 1;
  if (expectedError) {
    if (result.error !== expectedError) failures.push(`${label}: ${expectedError} beklendi, ${result.error ?? "hata yok"} alındı.`);
    return;
  }
  if (result.error) failures.push(`${label}: beklenmeyen ${result.error}.`);
  else if (result.output !== expectedOutput) failures.push(`${label}: çıktı ${JSON.stringify(expectedOutput)} olmalı, ${JSON.stringify(result.output)} alındı.`);
}

for (const module of modules) {
  if (module.sections.length < 8) failures.push(`Modül ${module.id}: ders kapsamı eksik (${module.sections.length}).`);
  if (module.questions.length < 40) failures.push(`Modül ${module.id}: soru havuzu 40'tan küçük.`);
  if (module.practiceIds.length < 15) failures.push(`Modül ${module.id}: pratik 15 sorudan küçük.`);
  const ids = new Set(module.questions.map((question) => question.id));
  if (ids.size !== module.questions.length) failures.push(`Modül ${module.id}: yinelenen soru kimliği var.`);
  for (const practiceId of module.practiceIds) if (!ids.has(practiceId)) failures.push(`Modül ${module.id}: bilinmeyen pratik sorusu ${practiceId}.`);

  for (const section of module.sections) {
    await verifyCode(`M${module.id} ders ${section.id}`, section.code, section.expectedOutput);
    await verifyCode(`M${module.id} gerçek kod ${section.id}`, section.realCode, section.realOutput);
  }
  for (const question of module.questions) {
    if (question.type === "output") await verifyCode(question.id, question.code, question.expectedOutput);
    if (["fill", "order", "code"].includes(question.type) && question.solutionCode) await verifyCode(`${question.id} çözüm`, question.solutionCode, question.expectedOutput);
    if (question.expectedError) await verifyCode(`${question.id} hata`, question.code, undefined, question.expectedError);
  }
}

if (failures.length) {
  console.error(`\n${failures.length} doğrulama hatası:\n- ${failures.join("\n- ")}`);
  process.exitCode = 1;
} else {
  console.log(`Python ${version.join(".")} ile ${checked} çalıştırılabilir içerik doğrulandı.`);
  console.log(`${modules.length} modül · ${modules.reduce((sum, item) => sum + item.questions.length, 0)} soru · tüm çıktılar doğru.`);
}
