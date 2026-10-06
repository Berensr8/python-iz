export type QuestionType = "output" | "bug" | "fill" | "order" | "code" | "traceback";

export type CodeTest = { label: string; stdin: string; expectedOutput: string };
export type WritingTask = {
  id: string; moduleId: number; sectionId: string; title: string;
  level: "Tamamla" | "Düzelt" | "Sıfırdan yaz";
  objective: string; prompt: string; starterCode: string;
  exampleInput: string; exampleOutput: string;
  hints: string[]; solution: string; tests: CodeTest[];
};

export type LessonSection = {
  id: string;
  title: string;
  eyebrow: string;
  objectives: string[];
  /** Section ids (same module) or "m<id>:<sectionId>" for earlier modules. */
  prerequisites: string[];
  sources?: { title: string; url: string }[];
  runtime?: "browser" | "mixed";
  summary: string;
  explanation: string;
  code: string;
  expectedOutput: string;
  why: string;
  alternatives: string[];
  traps: string[];
  realCode: string;
  realOutput: string;
  lineByLine: string[];
};

export type Question = {
  id: string;
  type: QuestionType;
  topic: string;
  /** Lesson section this question assesses; wrong answers link back to it. */
  sectionId: string;
  difficulty: 1 | 2 | 3;
  prompt: string;
  code?: string;
  starterCode?: string;
  options?: string[];
  lines?: string[];
  answer: string;
  /** Fill questions: every accepted spelling, including `answer`. */
  acceptedAnswers?: string[];
  /** Why each wrong option is wrong, keyed by option text. */
  optionFeedback?: Record<string, string>;
  expectedOutput?: string;
  expectedError?: string;
  solutionCode?: string;
  tests?: CodeTest[];
  exampleInput?: string;
  hints: string[];
  explanation: string;
};

export type LearningModule = {
  id: number;
  slug: string;
  title: string;
  description: string;
  contentVersion: number;
  estimatedMinutes: number;
  practiceIds: string[];
  sections: LessonSection[];
  questions: Question[];
};

export type TestAttempt = {
  sessionId?: string;
  reason?: "submitted" | "timeout";
  moduleId: number;
  score: number;
  date: string;
  weakTopics: string[];
};

export type LearningProgress = {
  version: 3;
  xp: number;
  streak: number;
  lastStudyDate: string | null;
  unlockedModule: number;
  completedSections: Record<string, boolean>;
  completedPractice: Record<string, boolean>;
  hintUsage: Record<string, number>;
  questionResults: Record<string, { correct: number; wrong: number }>;
  attempts: TestAttempt[];
  theme: "light" | "dark";
  sound: boolean;
  writingDrafts: Record<string, string>;
  writingHelp: Record<string, boolean>;
  writingResults: Record<string, { passed: boolean; independent: boolean; attempts: number }>;
  activeQuiz: QuizSession | null;
  creditedQuizIds: string[];
};

export type QuizDraft = { choice: string; fill: string; ordered: string[]; code: string; hints: number; stdin: string };
export type QuizSession = {
  id: string; moduleId: number; mode: "practice" | "test"; weakOnly: boolean;
  questions: Question[]; startedAt: number; deadline: number | null;
  index: number; drafts: Record<string, QuizDraft>;
  answers: Record<string, { correct: boolean; hints: number; submittedAt: number }>;
  completedAt: number | null; finishReason: "submitted" | "timeout" | null;
};

