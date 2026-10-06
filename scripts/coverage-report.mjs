// Kapsam matrisi (A1.1): her alt başlığın hangi ders bölümüne, soruya ve yazma görevine bağlandığını raporlar.
import { readFile, readdir } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import path from "node:path";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const read = async (file) => JSON.parse(await readFile(path.join(root, file), "utf8"));
const coverage = await read("content/coverage.json");
const files = (await readdir(path.join(root, "content"))).filter(file => /^module-\d+\.json$/.test(file));
const modules = await Promise.all(files.map(file => read(`content/${file}`)));
const writingTasks = await read("content/writing-tasks.json");

const errors = [];
const sections = new Map(modules.flatMap(module => module.sections.map(section => [`m${module.id}:${section.id}`, module])));
const mapped = new Set();
const order = coverage.statuses;

for (const entry of coverage.modules) {
  const content = modules.find(module => module.id === entry.id);
  const ids = new Set();
  for (const topic of entry.subtopics) {
    if (ids.has(topic.id)) errors.push(`M${entry.id}: yinelenen alt başlık ${topic.id}.`);
    ids.add(topic.id);
    if (!order.includes(topic.status)) errors.push(`M${entry.id} ${topic.id}: bilinmeyen durum ${topic.status}.`);
    if (!(topic.depth in coverage.depths)) errors.push(`M${entry.id} ${topic.id}: bilinmeyen derinlik ${topic.depth}.`);
    if (order.indexOf(topic.status) >= order.indexOf("yazıldı") && !topic.sections.length) errors.push(`M${entry.id} ${topic.id}: "${topic.status}" ama ders bölümüne bağlı değil.`);
    if (topic.status !== "planlandı" && !content) errors.push(`M${entry.id} ${topic.id}: "${topic.status}" ama modül içeriği yok.`);
    for (const key of topic.sections) {
      if (!sections.has(key)) errors.push(`M${entry.id} ${topic.id}: bilinmeyen bölüm ${key}.`);
      else if (sections.get(key).id !== entry.id) errors.push(`M${entry.id} ${topic.id}: ${key} başka modüle ait.`);
      mapped.add(key);
    }
  }
}
for (const key of sections.keys()) if (!mapped.has(key)) errors.push(`${key}: hiçbir alt başlığa bağlı değil.`);
for (const module of modules) if (!coverage.modules.some(entry => entry.id === module.id)) errors.push(`M${module.id}: kapsam matrisinde yok.`);

const rows = coverage.modules.map(entry => {
  const content = modules.find(module => module.id === entry.id);
  const done = entry.subtopics.filter(topic => order.indexOf(topic.status) >= order.indexOf("doğrulandı")).length;
  return {
    Modül: `M${entry.id} ${entry.title}`,
    "Alt başlık": entry.subtopics.length,
    "Doğrulanmış": done,
    Bölüm: content?.sections.length ?? 0,
    Soru: content?.questions.length ?? 0,
    "Yazma görevi": writingTasks.filter(task => task.moduleId === entry.id).length,
  };
});
console.table(rows);
const all = coverage.modules.flatMap(entry => entry.subtopics);
const verified = all.filter(topic => order.indexOf(topic.status) >= order.indexOf("doğrulandı")).length;
console.log(`${all.length} alt başlıktan ${verified} tanesi doğrulanmış içerikle kapsanıyor (%${Math.round(100 * verified / all.length)}).`);

if (errors.length) {
  console.error(`\n${errors.length} kapsam hatası:\n- ${errors.join("\n- ")}`);
  process.exitCode = 1;
}
