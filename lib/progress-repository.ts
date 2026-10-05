import type { LearningProgress } from "@/lib/learning-types";

export interface ProgressRepository {
  load(): LearningProgress;
  save(progress: LearningProgress): void;
  clear(): void;
}

export const defaultProgress: LearningProgress = {
  version: 1,
  xp: 0,
  streak: 1,
  lastStudyDate: null,
  unlockedModule: 1,
  completedSections: {},
  completedPractice: {},
  hintUsage: {},
  questionResults: {},
  attempts: [],
  theme: "dark",
  sound: true,
};

export class LocalStorageProgressRepository implements ProgressRepository {
  private key = "python-iz-progress-v1";

  load(): LearningProgress {
    if (typeof window === "undefined") return defaultProgress;
    try {
      const stored = window.localStorage.getItem(this.key);
      if (!stored) return { ...defaultProgress };
      return { ...defaultProgress, ...JSON.parse(stored), version: 1 };
    } catch {
      return { ...defaultProgress };
    }
  }

  save(progress: LearningProgress) {
    window.localStorage.setItem(this.key, JSON.stringify(progress));
  }

  clear() {
    window.localStorage.removeItem(this.key);
  }
}

export const progressRepository = new LocalStorageProgressRepository();

