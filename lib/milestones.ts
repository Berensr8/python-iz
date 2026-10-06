import type { LearningModule, LearningProgress, Question } from "./learning-types";

// Checkpoints (cumulative exams and project workshops) are described in content/milestones.json.
// A checkpoint sits "after" a module: it opens once that module's test is passed or the next module is unlocked.
export type Exam = {
  id: string; afterModule: number; title: string; scope: string; description: string;
  minutes: number; questionIds: string[];
};
export type ReadStep = {
  kind: "read"; label: string; progressKey: string; heading: string; code: string;
  inputLabel: string; placeholder: string; answer: string; expectedOutput: string;
  wrongHint: string; explanation: string; nextLabel?: string;
};
export type WriteStep = { kind: "write"; label: string; taskId: string; note?: string; nextLabel?: string };
export type WorkshopStep = ReadStep | WriteStep;
export type Workshop = { id: string; afterModule: number; title: string; summary: string; steps: WorkshopStep[] };
export type MilestoneData = { exams: Exam[]; workshops: Workshop[] };

export const PASS_SCORE = 70;

export function examQuestions(exam: Exam, modules: LearningModule[]): Question[] {
  const all = modules.flatMap(module => module.questions);
  return exam.questionIds.map(id => {
    const question = all.find(item => item.id === id);
    if (!question) throw new Error(`Ara sınav sorusu bulunamadı: ${id}`);
    return question;
  });
}
export function examPassCount(questionCount: number) {
  return Math.ceil(questionCount * PASS_SCORE / 100);
}
export function examByModule(exams: Exam[], afterModule: number) {
  return exams.find(exam => exam.afterModule === afterModule);
}
/** Midterm attempts are stored with the module the exam follows, so that number names the exam. */
export function attemptLabel(exams: Exam[], attempt: { kind?: string; moduleId: number }) {
  if (attempt.kind !== "midterm") return `Modül ${attempt.moduleId}`;
  return examByModule(exams, attempt.moduleId)?.title ?? `Ara sınav (M${attempt.moduleId} sonrası)`;
}
export function milestoneAvailable(progress: LearningProgress, afterModule: number) {
  return progress.unlockedModule > afterModule ||
    progress.attempts.some(attempt => attempt.kind !== "midterm" && attempt.moduleId === afterModule && attempt.score >= PASS_SCORE);
}
export function stepDone(progress: LearningProgress, step: WorkshopStep) {
  return step.kind === "read" ? !!progress.workshopRead[step.progressKey] : !!progress.writingResults[step.taskId]?.passed;
}
/** Per-step completion; a step opens only after every earlier step is done. */
export function workshopSteps(progress: LearningProgress, workshop: Workshop) {
  const done = workshop.steps.map(step => stepDone(progress, step));
  return workshop.steps.map((step, index) => ({ step, done: done[index], open: done.slice(0, index).every(Boolean) }));
}
export function workshopComplete(progress: LearningProgress, workshop: Workshop) {
  return workshopSteps(progress, workshop).every(item => item.done);
}
