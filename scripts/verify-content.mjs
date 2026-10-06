import { readFile, readdir } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import path from "node:path";
import { loadPyodide } from "pyodide";
import "../public/python-runtime.js";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const files = (await readdir(path.join(root, "content"))).filter(file => /^module-\d+\.json$/.test(file)).map(file => `content/${file}`);
const modules = await Promise.all(files.map(async (file) => JSON.parse(await readFile(path.join(root, file), "utf8"))));
const pyodide = await loadPyodide();
const version = pyodide.runPython("import sys; tuple(sys.version_info[:3])").toJs();

if (version[0] < 3 || (version[0] === 3 && version[1] < 12)) {
  throw new Error(`Python 3.12+ gerekli; doğrulayıcı ${version.join(".")} çalıştırıyor.`);
}

let checked = 0;
const failures = [];

async function execute(code, stdin = "") {
  const stdout = [];
  const stderr = [];
  pyodide.setStdout({ batched: (value) => stdout.push(value) });
  pyodide.setStderr({ batched: (value) => stderr.push(value) });
  try {
    const result = await globalThis.pythonRuntime.execute(pyodide, code, stdin);
    if (!result.ok) throw new Error(result.output);
    return { output: result.output.trimEnd(), error: null };
  } catch (error) {
    const text = String(error);
    // Library errors carry a module prefix in the traceback, e.g. json.decoder.JSONDecodeError.
    const name = text.match(/\n(?:[a-z_]+\.)*([A-Za-z]+(?:Error|Exception)):/)?.[1] ?? text.match(/^([A-Za-z]+(?:Error|Exception)):/)?.[1] ?? "PythonError";
    return { output: [...stdout, ...stderr].join("\n").trimEnd(), error: name };
  }
}

async function verifyCode(label, code, expectedOutput, expectedError, stdin = "") {
  const result = await execute(code, stdin);
  checked += 1;
  if (expectedError) {
    if (result.error !== expectedError) failures.push(`${label}: ${expectedError} beklendi, ${result.error ?? "hata yok"} alındı.`);
    return;
  }
  if (result.error) failures.push(`${label}: beklenmeyen ${result.error}.`);
  else if (result.output !== expectedOutput) failures.push(`${label}: çıktı ${JSON.stringify(expectedOutput)} olmalı, ${JSON.stringify(result.output)} alındı.`);
}

modules.sort((a, b) => a.id - b.id);
modules.forEach((module, index) => { if (module.id !== index + 1) failures.push(`Modül kimlikleri 1'den ardışık olmalı; ${index + 1} yerine ${module.id} bulundu.`); });
const writingTasks = JSON.parse(await readFile(path.join(root, "content/writing-tasks.json"), "utf8"));
const workshopTasks = JSON.parse(await readFile(path.join(root, "content/workshop-tasks.json"), "utf8"));
const milestones = JSON.parse(await readFile(path.join(root, "content/milestones.json"), "utf8"));
const sectionKeys = new Set(modules.flatMap(module => module.sections.map(section => `m${module.id}:${section.id}`)));

for (const module of modules) {
  if (!Number.isInteger(module.contentVersion) || module.contentVersion < 1) failures.push(`Modül ${module.id}: contentVersion eksik.`);
  const sectionIds = new Set(module.sections.map(section => section.id));
  for (const section of module.sections) {
    if (!["browser", "mixed"].includes(section.runtime) || !section.sources?.length || section.sources.some(source => !source.title || !source.url.startsWith("https://"))) failures.push(`M${module.id} ${section.id}: kaynak/ortam etiketi eksik.`);
    if (!section.objectives?.length) failures.push(`M${module.id} ${section.id}: kazanım (objectives) eksik.`);
    for (const prerequisite of section.prerequisites ?? ["?"]) {
      const key = prerequisite.includes(":") ? prerequisite : `m${module.id}:${prerequisite}`;
      if (!sectionKeys.has(key)) failures.push(`M${module.id} ${section.id}: bilinmeyen önkoşul ${prerequisite}.`);
    }
  }
  const assessed = new Set(module.questions.map(question => question.sectionId));
  for (const id of sectionIds) if (!assessed.has(id)) failures.push(`M${module.id} ${id}: bu bölümü ölçen soru yok.`);
  for (const question of module.questions) {
    if (!question.id.startsWith(`m${module.id}-`)) failures.push(`${question.id}: kimlik m${module.id}- ile başlamalı.`);
    if (!sectionIds.has(question.sectionId)) failures.push(`${question.id}: bilinmeyen sectionId ${question.sectionId}.`);
    if (![1, 2, 3].includes(question.difficulty)) failures.push(`${question.id}: difficulty 1–3 olmalı.`);
    if (question.options?.length && !question.options.includes(question.answer)) failures.push(`${question.id}: cevap seçeneklerde yok.`);
    // A question the student cannot answer (no options, no input) blocks the whole practice and test.
    if (!question.answer) failures.push(`${question.id}: cevap anahtarı (answer) eksik.`);
    if (!question.options?.length && !["fill", "order", "code"].includes(question.type)) failures.push(`${question.id}: ${question.type} sorusunda seçenek yok; öğrenci cevap veremez.`);
    if (question.options?.length && (question.options.length < 3 || new Set(question.options).size !== question.options.length)) failures.push(`${question.id}: en az üç, birbirinden farklı seçenek gerekli.`);
    for (const [option, reason] of Object.entries(question.optionFeedback ?? {})) {
      if (!question.options?.includes(option) || option === question.answer || !reason) failures.push(`${question.id}: geçersiz optionFeedback "${option}".`);
    }
    if (["bug", "traceback"].includes(question.type) && question.options?.some(option => option !== question.answer && !question.optionFeedback?.[option])) failures.push(`${question.id}: her yanlış seçenek için gerekçe gerekli.`);
    if (question.acceptedAnswers && !question.acceptedAnswers.includes(question.answer)) failures.push(`${question.id}: acceptedAnswers asıl cevabı içermeli.`);
    // Each accepted fill answer, placed into the blank, must produce the same output.
    if (question.type === "fill" && !question.options?.length) {
      if ((question.code?.match(/___/g) ?? []).length !== 1) failures.push(`${question.id}: kodda tam bir ___ boşluğu olmalı.`);
      else for (const answer of question.acceptedAnswers ?? [question.answer]) await verifyCode(`${question.id} kabul "${answer}"`, question.code.replace("___", answer), question.expectedOutput);
    }
  }
}
for (const task of [...writingTasks, ...workshopTasks]) {
  if (!sectionKeys.has(`m${task.moduleId}:${task.sectionId}`)) failures.push(`${task.id}: bilinmeyen bölüm ${task.sectionId}.`);
  if (task.tests.length < 3) failures.push(`${task.id}: en az üç test gerekli.`);
  for (const test of task.tests) await verifyCode(`${task.id} ${test.label}`, task.solution, test.expectedOutput, undefined, test.stdin);
}
for (const module of modules) if (writingTasks.filter(task => task.moduleId === module.id).length < 3) failures.push(`Modül ${module.id}: en az üç yazma görevi gerekli.`);

// Ara sınavlar ve atölyeler (content/milestones.json)
const allQuestions = new Map(modules.flatMap(module => module.questions.map(question => [question.id, question])));
const taskIds = new Set(workshopTasks.map(task => task.id));
const usedTasks = new Set();
const usedKeys = new Set();
const checkpointIds = new Set();
for (const exam of milestones.exams) {
  const label = `Ara sınav ${exam.id}`;
  if (checkpointIds.has(exam.id)) failures.push(`${label}: yinelenen kimlik.`);
  checkpointIds.add(exam.id);
  if (!Number.isInteger(exam.afterModule) || exam.afterModule < 1 || exam.afterModule > modules.length) failures.push(`${label}: afterModule geçersiz.`);
  if (!Number.isInteger(exam.minutes) || exam.minutes < 25 || exam.minutes > 60) failures.push(`${label}: süre 25–60 tam dakika olmalı.`);
  if (new Set(exam.questionIds).size !== exam.questionIds.length) failures.push(`${label}: yinelenen soru var.`);
  const questions = exam.questionIds.map(id => allQuestions.get(id));
  exam.questionIds.forEach((id, index) => { if (!questions[index]) failures.push(`${label}: bilinmeyen soru ${id}.`); });
  const known = questions.filter(Boolean);
  if (known.length < 20 || known.length > 30) failures.push(`${label}: 20–30 soru olmalı (${known.length}).`);
  if (known.filter(question => question.type === "code").length < 3) failures.push(`${label}: en az üç kod yazma sorusu gerekli.`);
  const inScope = new Set(known.map(question => Number(/^m(\d+)-/.exec(question.id)[1])));
  for (let id = 1; id <= exam.afterModule; id++) if (!inScope.has(id)) failures.push(`${label}: M${id}'den soru yok.`);
  if ([...inScope].some(id => id > exam.afterModule)) failures.push(`${label}: kapsam dışı (M${exam.afterModule} sonrası) modülden soru var.`);
  if (exam.scope !== (exam.afterModule === 1 ? "M1" : `M1–M${exam.afterModule}`)) failures.push(`${label}: scope "${exam.scope}" afterModule ile uyuşmuyor.`);
  if (known.some(question => question.type === "traceback" || question.type === "bug") === false) failures.push(`${label}: hata bulma/traceback sorusu da içermeli.`);
}
for (const workshop of milestones.workshops) {
  const label = `Atölye ${workshop.id}`;
  if (checkpointIds.has(workshop.id)) failures.push(`${label}: yinelenen kimlik.`);
  checkpointIds.add(workshop.id);
  if (!Number.isInteger(workshop.afterModule) || workshop.afterModule < 1 || workshop.afterModule > modules.length) failures.push(`${label}: afterModule geçersiz.`);
  if (workshop.steps.length < 3) failures.push(`${label}: en az üç adım gerekli.`);
  if (workshop.steps.at(-1)?.kind !== "write") failures.push(`${label}: son adım sıfırdan yazma olmalı.`);
  for (const [index, step] of workshop.steps.entries()) {
    const where = `${label} adım ${index + 1}`;
    if (!step.label) failures.push(`${where}: etiket eksik.`);
    if (index < workshop.steps.length - 1 && step.nextLabel === undefined) failures.push(`${where}: sonraki adım düğmesi (nextLabel) eksik.`);
    if (step.kind === "write") {
      if (!taskIds.has(step.taskId)) failures.push(`${where}: bilinmeyen görev ${step.taskId}.`);
      if (usedTasks.has(step.taskId)) failures.push(`${where}: görev ${step.taskId} birden çok adımda.`);
      usedTasks.add(step.taskId);
    } else if (step.kind === "read") {
      if (usedKeys.has(step.progressKey)) failures.push(`${where}: yinelenen progressKey ${step.progressKey}.`);
      usedKeys.add(step.progressKey);
      for (const field of ["heading", "code", "inputLabel", "placeholder", "answer", "expectedOutput", "wrongHint", "explanation"]) if (!step[field]) failures.push(`${where}: ${field} eksik.`);
      if (step.answer.trim().replace(/\s+/g, " ") !== step.expectedOutput.trim().replace(/\s+/g, " ")) failures.push(`${where}: answer ile expectedOutput uyuşmuyor.`);
      // The reading answer is whatever the code really prints.
      await verifyCode(`${label} okuma`, step.code, step.expectedOutput);
    } else failures.push(`${where}: bilinmeyen adım türü ${step.kind}.`);
  }
}
for (const task of workshopTasks) if (!usedTasks.has(task.id)) failures.push(`Atölye görevi ${task.id} hiçbir atölyede kullanılmıyor.`);

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
    if (["fill", "order", "code"].includes(question.type) && question.solutionCode) await verifyCode(`${question.id} çözüm`, question.solutionCode, question.expectedOutput, undefined, question.exampleInput);
    if (question.type === "code") {
      if (!question.tests || question.tests.length < 3) failures.push(`${question.id}: en az üç test gerekli.`);
      for (const test of question.tests ?? []) await verifyCode(`${question.id} ${test.label}`, question.solutionCode, test.expectedOutput, undefined, test.stdin);
    }
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
