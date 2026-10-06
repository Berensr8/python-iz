import type { LearningModule, LearningProgress } from "./learning-types";

// A cumulative checkpoint reuses assessed questions, but never unlocks a module.
export const midtermIds = [
  "m1-q05", "m1-q11", "m1-q23", "m1-q27", "m1-q38",
  "m2-q03", "m2-q14", "m2-q25", "m2-q29", "m2-q40",
  "m3-q01", "m3-q03", "m3-q06", "m3-q19", "m3-q27",
  "m4-q10", "m4-q13", "m4-q17", "m4-q21", "m4-q35",
];
export function midtermQuestions(modules: LearningModule[]) {
  const all = modules.flatMap(module => module.questions);
  return midtermIds.map(id => { const question = all.find(q => q.id === id); if (!question) throw new Error(`Ara sınav sorusu bulunamadı: ${id}`); return question; });
}
export function milestonesAvailable(progress: LearningProgress) {
  return progress.unlockedModule >= 5 || progress.attempts.some(attempt => attempt.kind !== "midterm" && attempt.moduleId === 4 && attempt.score >= 70);
}
