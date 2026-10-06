import type { Question, QuizDraft } from "./learning-types";

/**
 * Spacing around operators is not what a fill question tests ("-3 :" equals "-3:"),
 * but spacing between words is ("not in" must not match "notin").
 */
export function normalizeFill(value: string) {
  return value.trim().replace(/\s+/g, " ").replace(/\s*([^\w\s])\s*/gu, "$1");
}

/** Correctness for answers that need no Python run (choice and fill questions). */
export function isAnswerCorrect(question: Question, value: string) {
  if (question.type === "fill" && !question.options?.length) {
    const accepted = question.acceptedAnswers?.length ? question.acceptedAnswers : [question.answer];
    return accepted.some(answer => normalizeFill(answer) === normalizeFill(value));
  }
  return value === question.answer;
}

/** Explanation for a specific wrong choice, when the content provides one. */
export function wrongOptionFeedback(question: Question, choice: string) {
  return choice && choice !== question.answer ? question.optionFeedback?.[choice] : undefined;
}

export type AnswerKind = "choice" | "fill" | "order" | "code" | "none";
/** How a student answers this question in the app. "none" would mean it cannot be answered at all. */
export function answerKind(question: Question): AnswerKind {
  if (question.options?.length) return "choice";
  if (question.type === "fill") return "fill";
  if (question.type === "order") return "order";
  if (question.type === "code") return "code";
  return "none";
}
/** The value compared with the answer key, read from the draft exactly as the question card does. */
export function selectedAnswer(question: Question, draft: Pick<QuizDraft, "choice" | "fill" | "ordered">) {
  const kind = answerKind(question);
  return kind === "fill" ? draft.fill.trim() : kind === "order" ? draft.ordered.join("\n") : draft.choice;
}
