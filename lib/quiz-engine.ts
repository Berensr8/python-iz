import type { LearningProgress, Question, QuizDraft, QuizSession } from "./learning-types";

// Content lists the right option first in most questions, so every attempt shuffles the options.
// The seed is the session and question, which keeps the order stable across refreshes and saves.
function seededShuffle<T>(items: readonly T[], seed: string): T[] {
  let state = 2166136261;
  for (const char of seed) state = Math.imul(state ^ char.charCodeAt(0), 16777619) >>> 0;
  const next = () => { state = (Math.imul(state, 1664525) + 1013904223) >>> 0; return state / 4294967296; };
  const result = [...items];
  for (let index = result.length - 1; index > 0; index--) {
    const other = Math.floor(next() * (index + 1));
    [result[index], result[other]] = [result[other], result[index]];
  }
  return result;
}

export function createQuiz(id: string, moduleId: number, mode: QuizSession["mode"], questions: Question[], timed: boolean, weakOnly = false, now = Date.now(), minutes = 25): QuizSession {
  if (!questions.length || new Set(questions.map(q => q.id)).size !== questions.length) throw new Error("Geçerli, benzersiz sorular gerekli.");
  return { id, moduleId, mode, weakOnly, questions: questions.map(question => structuredClone(question.options && question.options.length > 1 ? { ...question, options: seededShuffle(question.options, `${id}:${question.id}`) } : question)), startedAt: now,
    deadline: mode !== "practice" && timed ? now + minutes * 60 * 1000 : null,
    index: 0, drafts: {}, answers: {}, completedAt: null, finishReason: null };
}
export function initialDraft(question: Question): QuizDraft {
  return { choice: "", fill: "", ordered: [...question.lines ?? []], code: question.starterCode ?? "", hints: 0, stdin: question.exampleInput ?? "" };
}
export function quizSummary(session: QuizSession) {
  const correct = session.questions.filter(q => session.answers[q.id]?.correct).length;
  const answered = session.questions.filter(q => session.answers[q.id]).length;
  return { correct, answered, unanswered: session.questions.length - answered,
    score: Math.round(100 * correct / session.questions.length),
    passed: correct / session.questions.length >= 0.7,
    weakTopics: [...new Set(session.questions.filter(q => !session.answers[q.id]?.correct).map(q => q.topic))] };
}
export function secondsLeft(session: QuizSession, now = Date.now()) {
  return session.deadline === null ? null : Math.max(0, Math.ceil((session.deadline - now) / 1000));
}
function matching(progress: LearningProgress, id: string) {
  const session = progress.activeQuiz;
  return session?.id === id && session.completedAt === null ? session : null;
}
function studied(progress: LearningProgress, now: number) {
  const format = (time: number) => new Intl.DateTimeFormat("en-CA", { timeZone: "Europe/Istanbul" }).format(new Date(time));
  const day = format(now);
  return { ...progress, lastStudyDate: day, streak: progress.lastStudyDate === day ? progress.streak : progress.lastStudyDate === format(now - 86400000) ? progress.streak + 1 : 1 };
}
export function finishQuiz(progress: LearningProgress, id: string, reason: "submitted" | "timeout", now = Date.now()): LearningProgress {
  const session = matching(progress, id);
  if (!session) return progress;
  const expired = session.deadline !== null && now >= session.deadline;
  if (reason === "timeout" && !expired) return progress;
  if (!expired && session.questions.some(q => !session.answers[q.id])) return progress;
  const summary = quizSummary(session);
  const completedAt = expired ? session.deadline! : now;
  const finished: QuizSession = { ...session, index: session.questions.length, completedAt, finishReason: expired ? "timeout" : "submitted" };
  // A restored/replayed completed session must never grant its result twice.
  if (progress.creditedQuizIds.includes(id) || progress.attempts.some(attempt => attempt.sessionId === id)) return { ...progress, activeQuiz: finished };
  const practiceKey = `m${session.moduleId}`;
  const regularPractice = session.mode === "practice" && !session.weakOnly;
  const bonus = session.mode !== "practice" ? (summary.passed ? 100 : 20) : regularPractice && !progress.completedPractice[practiceKey] ? 40 : 0;
  return { ...studied(progress, now), activeQuiz: finished, xp: progress.xp + bonus,
    creditedQuizIds: [...progress.creditedQuizIds, id],
    completedPractice: regularPractice ? { ...progress.completedPractice, [practiceKey]: true } : progress.completedPractice,
    unlockedModule: session.mode === "test" && summary.passed ? Math.max(progress.unlockedModule, Math.min(18, session.moduleId + 1)) : progress.unlockedModule,
    attempts: session.mode !== "practice" ? [...progress.attempts, { kind: session.mode === "midterm" ? "midterm" : "module", sessionId: id, moduleId: session.moduleId, score: summary.score, date: new Date(completedAt).toISOString(), weakTopics: summary.weakTopics, reason: finished.finishReason! }] : progress.attempts,
  };
}
export function expireQuiz(progress: LearningProgress, now = Date.now()) {
  return progress.activeQuiz ? finishQuiz(progress, progress.activeQuiz.id, "timeout", now) : progress;
}
export function saveQuizDraft(progress: LearningProgress, id: string, questionId: string, draft: QuizDraft, now = Date.now()) {
  const checked = expireQuiz(progress, now);
  const session = matching(checked, id);
  if (!session || session.questions[session.index]?.id !== questionId || session.answers[questionId]) return checked;
  return { ...checked, activeQuiz: { ...session, drafts: { ...session.drafts, [questionId]: draft } } };
}
export function answerQuiz(progress: LearningProgress, id: string, questionId: string, correct: boolean, now = Date.now()): LearningProgress {
  const checked = expireQuiz(progress, now);
  const session = matching(checked, id);
  if (!session || session.questions[session.index]?.id !== questionId || session.answers[questionId] || progress.creditedQuizIds.includes(id)) return checked;
  const hints = session.mode !== "practice" ? 0 : session.drafts[questionId]?.hints ?? 0;
  const old = checked.questionResults[questionId] ?? { correct: 0, wrong: 0 };
  return { ...studied(checked, now), xp: checked.xp + (correct ? Math.max(2, 10 - hints * 2) : 1),
    questionResults: { ...checked.questionResults, [questionId]: { correct: old.correct + Number(correct), wrong: old.wrong + Number(!correct) } },
    hintUsage: { ...checked.hintUsage, [questionId]: (checked.hintUsage[questionId] ?? 0) + hints },
    activeQuiz: { ...session, answers: { ...session.answers, [questionId]: { correct, hints, submittedAt: now } } },
  };
}
export function nextQuizQuestion(progress: LearningProgress, id: string, expectedQuestionId: string, now = Date.now()): LearningProgress {
  const checked = expireQuiz(progress, now);
  const session = matching(checked, id);
  if (!session || session.questions[session.index]?.id !== expectedQuestionId || !session.answers[expectedQuestionId]) return checked;
  return session.index === session.questions.length - 1 ? finishQuiz(checked, id, "submitted", now) : { ...checked, activeQuiz: { ...session, index: session.index + 1 } };
}
