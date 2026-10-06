import type { Question } from "./learning-types";

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
