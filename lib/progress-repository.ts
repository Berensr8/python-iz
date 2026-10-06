import { z } from "zod";
import type { LearningProgress } from "@/lib/learning-types";

const count = z.number().int().nonnegative().max(Number.MAX_SAFE_INTEGER);
const flags = z.record(z.boolean());
const schema = z.object({
  version: z.literal(2).default(2), xp: count.default(0), streak: count.default(0),
  lastStudyDate: z.string().regex(/^\d{4}-\d{2}-\d{2}$/).nullable().default(null),
  unlockedModule: z.number().int().min(1).max(18).default(1),
  completedSections: flags.default({}), completedPractice: flags.default({}),
  hintUsage: z.record(count).default({}),
  questionResults: z.record(z.object({ correct: count, wrong: count })).default({}),
  attempts: z.array(z.object({ moduleId: z.number().int().min(1).max(18), score: z.number().min(0).max(100), date: z.string().datetime(), weakTopics: z.array(z.string()) })).default([]),
  theme: z.enum(["light", "dark"]).default("dark"), sound: z.boolean().default(true),
  writingDrafts: z.record(z.string().max(50000)).default({}), writingHelp: flags.default({}),
  writingResults: z.record(z.object({ passed: z.boolean(), independent: z.boolean(), attempts: count })).default({}),
});

export const defaultProgress: LearningProgress = schema.parse({});
export function parseProgress(value: unknown): LearningProgress {
  if (!value || typeof value !== "object") throw new Error("İlerleme verisi geçersiz.");
  const raw = value as Record<string, unknown>;
  if (raw.version !== 1 && raw.version !== 2) throw new Error("Bu ilerleme sürümü desteklenmiyor.");
  return schema.parse({ ...raw, version: 2 });
}
export function studyDay(date = new Date()) {
  return new Intl.DateTimeFormat("en-CA", { timeZone: "Europe/Istanbul" }).format(date);
}
export function markStudy(progress: LearningProgress, date = new Date()): LearningProgress {
  const today = studyDay(date);
  if (progress.lastStudyDate === today) return progress;
  const yesterday = studyDay(new Date(date.getTime() - 86400000));
  return { ...progress, lastStudyDate: today, streak: progress.lastStudyDate === yesterday ? progress.streak + 1 : 1 };
}
export function recordWriting(progress: LearningProgress, id: string, passed: boolean, helped: boolean): LearningProgress {
  const old = progress.writingResults[id];
  return { ...markStudy(progress), xp: progress.xp + (passed && !old?.passed ? 30 : 0),
    writingResults: { ...progress.writingResults, [id]: {
      passed: passed || !!old?.passed,
      independent: !!old?.independent || (passed && !helped),
      attempts: (old?.attempts ?? 0) + 1,
    } },
  };
}

export class LocalStorageProgressRepository {
  private key = "python-iz-progress-v2";
  load(): LearningProgress {
    if (typeof window === "undefined") return structuredClone(defaultProgress);
    try {
      const stored = window.localStorage.getItem(this.key) ?? window.localStorage.getItem("python-iz-progress-v1");
      return stored ? parseProgress(JSON.parse(stored)) : structuredClone(defaultProgress);
    } catch {
      this.warn("Kayıtlı ilerleme okunamadı. Eski kayıt değiştirilmedi; bu oturum geçici çalışır.");
      return structuredClone(defaultProgress);
    }
  }
  private blocked = false;
  private warn(message: string) {
    this.blocked = true;
    window.dispatchEvent(new CustomEvent("python-iz-storage-error", { detail: message }));
  }
  save(progress: LearningProgress) {
    if (this.blocked) return;
    try { window.localStorage.setItem(this.key, JSON.stringify(progress)); }
    catch { this.warn("Tarayıcı ilerlemeyi kaydedemedi. Bu oturumdaki kodunu ayrılmadan kopyala."); }
  }
  clear() {
    window.localStorage.removeItem(this.key);
    window.localStorage.removeItem("python-iz-progress-v1");
  }
}
export const progressRepository = new LocalStorageProgressRepository();

