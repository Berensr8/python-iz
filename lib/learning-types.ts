export type QuestionType = "output" | "bug" | "fill" | "order" | "code" | "traceback";

export type LessonSection = {
  id: string;
  title: string;
  eyebrow: string;
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
  prompt: string;
  code?: string;
  starterCode?: string;
  options?: string[];
  lines?: string[];
  answer: string;
  expectedOutput?: string;
  expectedError?: string;
  solutionCode?: string;
  hints: string[];
  explanation: string;
};

export type LearningModule = {
  id: number;
  slug: string;
  title: string;
  description: string;
  estimatedMinutes: number;
  practiceIds: string[];
  sections: LessonSection[];
  questions: Question[];
};

export type TestAttempt = {
  moduleId: number;
  score: number;
  date: string;
  weakTopics: string[];
};

export type LearningProgress = {
  version: 1;
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
};

