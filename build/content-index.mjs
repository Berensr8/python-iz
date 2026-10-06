// The module index: what the app needs to know about every module without loading its text.
// Section and question ids, titles and question types are enough for navigation, statistics,
// exam cards and weak-topic planning; the full module is fetched only when a lesson or a quiz needs it.
import { readdirSync, readFileSync } from "node:fs";
import path from "node:path";

export function summarizeModule(module) {
  return {
    id: module.id,
    slug: module.slug,
    title: module.title,
    description: module.description,
    contentVersion: module.contentVersion,
    estimatedMinutes: module.estimatedMinutes,
    practiceIds: module.practiceIds,
    sections: module.sections.map(section => ({ id: section.id, title: section.title })),
    questions: module.questions.map(question => ({ id: question.id, type: question.type, sectionId: question.sectionId, difficulty: question.difficulty })),
  };
}

export function moduleFiles(contentDir) {
  return readdirSync(contentDir).filter(file => /^module-\d+\.json$/.test(file)).sort();
}

export function buildContentIndex(contentDir) {
  return moduleFiles(contentDir)
    .map(file => summarizeModule(JSON.parse(readFileSync(path.join(contentDir, file), "utf8"))))
    .sort((a, b) => a.id - b.id);
}
