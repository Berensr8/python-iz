import type { LearningModule, Question } from "./learning-types";

// Pure question-picking rules. They take already loaded questions, so they run in Node tests as well.

export function practiceQuestions(module: LearningModule) {
  return module.practiceIds.map((id) => module.questions.find((q) => q.id === id)).filter(Boolean) as Question[];
}

function seededRandom(seed: number) {
  let state = seed || 1;
  return () => ((state = (state * 1664525 + 1013904223) >>> 0) / 4294967296);
}
function shuffled<T>(items: T[], random: () => number) {
  return items.map((value) => ({ value, key: random() })).sort((a, b) => a.key - b.key).map(({ value }) => value);
}

/** A test mixes in this share of questions from earlier modules (4 of 18). */
export function previousQuestionCount(hasPrevious: boolean, count = 18) {
  return hasPrevious ? Math.round(count * 0.2) : 0;
}

/**
 * Which earlier modules a test draws its review questions from. Only a few are picked, so a test in
 * module 18 loads about five modules instead of eighteen; the seed makes the choice repeatable.
 */
export function previousModulePool(moduleId: number, seed: number, count = 18) {
  const earlier = Array.from({ length: moduleId - 1 }, (_, index) => index + 1);
  return shuffled(earlier, seededRandom(seed ^ 0x9e3779b9)).slice(0, previousQuestionCount(earlier.length > 0, count));
}

/** `previous` holds the questions of the modules named by previousModulePool. */
export function seededTestQuestions(module: LearningModule, previous: Question[], seed: number, count = 18) {
  const random = seededRandom(seed);
  const previousCount = previousQuestionCount(previous.length > 0, count);
  // Every module test includes writing, rather than leaving it to chance.
  const writing = shuffled(module.questions.filter(question => question.type === "code"), random).slice(0, Math.min(3, count - previousCount));
  const remaining = module.questions.filter(question => !writing.includes(question));
  return shuffled([...writing, ...shuffled(remaining, random).slice(0, count - previousCount - writing.length), ...shuffled(previous, random).slice(0, previousCount)], random);
}
