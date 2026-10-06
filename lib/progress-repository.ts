import { z } from "zod";
import type { LearningProgress } from "@/lib/learning-types";

const count = z.number().int().nonnegative().max(Number.MAX_SAFE_INTEGER);
const flags = z.record(z.boolean());
const shortText = z.string().max(50000);
const questionSchema = z.object({
  id: z.string().min(1).max(100), type: z.enum(["output", "bug", "fill", "order", "code", "traceback"]),
  topic: shortText, prompt: shortText, answer: shortText, hints: z.array(shortText).max(10), explanation: shortText,
  // Sessions saved before content v2 lack these; defaults keep them loadable.
  sectionId: z.string().max(100).default(""), difficulty: z.union([z.literal(1), z.literal(2), z.literal(3)]).default(2),
  acceptedAnswers: z.array(shortText).max(20).optional(), optionFeedback: z.record(shortText).optional(),
  code: shortText.optional(), starterCode: shortText.optional(), options: z.array(shortText).max(100).optional(),
  lines: z.array(shortText).max(100).optional(), expectedOutput: shortText.optional(), expectedError: shortText.optional(),
  solutionCode: shortText.optional(), exampleInput: shortText.optional(),
  tests: z.array(z.object({ label: shortText, stdin: shortText, expectedOutput: shortText })).max(100).optional(),
});
// Quiz and exam clocks are whole minutes between 25 and 60 (each exam names its own length in milestones.json).
const validDuration = (milliseconds: number) => milliseconds >= 25 * 60000 && milliseconds <= 60 * 60000 && milliseconds % 60000 === 0;
const sessionSchema = z.object({
  id: z.string().min(1).max(100), moduleId: z.number().int().min(1).max(18), mode: z.enum(["practice", "test", "midterm"]), weakOnly: z.boolean(),
  questions: z.array(questionSchema).min(1).max(100), startedAt: count, deadline: count.nullable(), index: count,
  drafts: z.record(z.object({ choice: shortText, fill: shortText, ordered: z.array(shortText).max(100), code: shortText, hints: z.number().int().min(0).max(3), stdin: shortText })),
  answers: z.record(z.object({ correct: z.boolean(), hints: z.number().int().min(0).max(3), submittedAt: count })),
  completedAt: count.nullable(), finishReason: z.enum(["submitted", "timeout"]).nullable(),
}).superRefine((session, context) => {
  const ids = new Set(session.questions.map(q => q.id));
  const invalid = ids.size !== session.questions.length || session.index > session.questions.length ||
    (session.completedAt === null && session.index >= session.questions.length) ||
    (session.completedAt === null) !== (session.finishReason === null) ||
    (session.completedAt !== null && session.index !== session.questions.length) ||
    (session.deadline !== null && (session.mode === "practice" || !validDuration(session.deadline - session.startedAt))) ||
    [...Object.keys(session.answers), ...Object.keys(session.drafts)].some(id => !ids.has(id)) ||
    session.questions.slice(0, session.index).some(q => !session.answers[q.id] && session.finishReason !== "timeout");
  if (invalid) context.addIssue({ code: z.ZodIssueCode.custom, message: "Sınav oturumu tutarsız." });
});
const schema = z.object({
  version: z.literal(3).default(3), xp: count.default(0), streak: count.default(0),
  lastStudyDate: z.string().regex(/^\d{4}-\d{2}-\d{2}$/).nullable().default(null),
  unlockedModule: z.number().int().min(1).max(18).default(1),
  completedSections: flags.default({}), completedPractice: flags.default({}),
  lessonRuns: flags.default({}),
  workshopRead: flags.default({}),
  hintUsage: z.record(count).default({}),
  questionResults: z.record(z.object({ correct: count, wrong: count })).default({}),
  attempts: z.array(z.object({ kind: z.enum(["module", "midterm"]).optional(), sessionId: z.string().optional(), reason: z.enum(["submitted", "timeout"]).optional(), moduleId: z.number().int().min(1).max(18), score: z.number().min(0).max(100), date: z.string().datetime(), weakTopics: z.array(z.string()) })).default([]),
  theme: z.enum(["light", "dark"]).default("dark"), sound: z.boolean().default(true),
  writingDrafts: z.record(z.string().max(50000)).default({}), writingHelp: flags.default({}),
  writingResults: z.record(z.object({ passed: z.boolean(), independent: z.boolean(), attempts: count })).default({}),
  activeQuiz: sessionSchema.nullable().default(null), creditedQuizIds: z.array(z.string().max(100)).default([]),
  lastBackupAt: z.string().datetime().nullable().default(null),
});

export const defaultProgress: LearningProgress = schema.parse({});
export function parseProgress(value: unknown): LearningProgress {
  if (!value || typeof value !== "object") throw new Error("İlerleme verisi geçersiz.");
  const raw = value as Record<string, unknown>;
  if (raw.version !== 1 && raw.version !== 2 && raw.version !== 3) throw new Error("Bu ilerleme sürümü desteklenmiyor.");
  return schema.parse({ ...raw, version: 3 });
}
export function exportProgress(progress: LearningProgress) {
  return JSON.stringify({ app: "python-iz", formatVersion: 1, exportedAt: new Date().toISOString(), progress: parseProgress(progress) }, null, 2);
}
export function importProgress(text: string): LearningProgress {
  if (new TextEncoder().encode(text).length > 5 * 1024 * 1024) throw new Error("Yedek dosyası 5 MB sınırını aşıyor.");
  const value = JSON.parse(text);
  if (!value || value.app !== "python-iz" || value.formatVersion !== 1) throw new Error("Geçerli bir Python İz yedeği seç.");
  return parseProgress(value.progress);
}
const later = (a: string | null, b: string | null) => (a ?? "") >= (b ?? "") ? a : b;
const maxBy = (a: Record<string, number>, b: Record<string, number>) =>
  Object.fromEntries([...new Set([...Object.keys(a), ...Object.keys(b)])].map(key => [key, Math.max(a[key] ?? 0, b[key] ?? 0)]));
const anyTrue = (a: Record<string, boolean>, b: Record<string, boolean>) =>
  Object.fromEntries([...new Set([...Object.keys(a), ...Object.keys(b)])].map(key => [key, !!(a[key] || b[key])]));

/**
 * Combines progress from two devices without losing anything either side earned: completions are
 * unioned and counters take the larger value. Counters are never summed, because both devices may
 * already contain the same earlier work. The local theme/sound choice and live quiz stay as they are.
 */
export function mergeProgress(local: LearningProgress, incoming: LearningProgress): LearningProgress {
  const questionResults = { ...local.questionResults };
  for (const [id, result] of Object.entries(incoming.questionResults)) {
    const mine = questionResults[id];
    questionResults[id] = mine ? { correct: Math.max(mine.correct, result.correct), wrong: Math.max(mine.wrong, result.wrong) } : result;
  }
  const writingResults = { ...local.writingResults };
  for (const [id, result] of Object.entries(incoming.writingResults)) {
    const mine = writingResults[id];
    writingResults[id] = !mine ? result : {
      passed: mine.passed || result.passed,
      independent: (mine.passed && mine.independent) || (result.passed && result.independent),
      attempts: Math.max(mine.attempts, result.attempts),
    };
  }
  const attempts = new Map<string, LearningProgress["attempts"][number]>();
  for (const attempt of [...local.attempts, ...incoming.attempts]) attempts.set(`${attempt.kind ?? "module"}|${attempt.sessionId ?? ""}|${attempt.moduleId}|${attempt.date}`, attempt);
  // The streak belongs to whichever side studied most recently.
  const newer = (incoming.lastStudyDate ?? "") > (local.lastStudyDate ?? "") ? incoming : local;
  return parseProgress({
    ...local,
    xp: Math.max(local.xp, incoming.xp),
    streak: local.lastStudyDate === incoming.lastStudyDate ? Math.max(local.streak, incoming.streak) : newer.streak,
    lastStudyDate: newer.lastStudyDate,
    unlockedModule: Math.max(local.unlockedModule, incoming.unlockedModule),
    completedSections: anyTrue(local.completedSections, incoming.completedSections),
    completedPractice: anyTrue(local.completedPractice, incoming.completedPractice),
    lessonRuns: anyTrue(local.lessonRuns, incoming.lessonRuns),
    workshopRead: anyTrue(local.workshopRead, incoming.workshopRead),
    hintUsage: maxBy(local.hintUsage, incoming.hintUsage),
    questionResults,
    attempts: [...attempts.values()].sort((a, b) => a.date.localeCompare(b.date)),
    writingDrafts: { ...incoming.writingDrafts, ...local.writingDrafts },
    writingHelp: anyTrue(local.writingHelp, incoming.writingHelp),
    writingResults,
    creditedQuizIds: [...new Set([...local.creditedQuizIds, ...incoming.creditedQuizIds])],
    lastBackupAt: later(local.lastBackupAt, incoming.lastBackupAt),
  });
}

// Transfer code: "PYIZ1." + base64url(gzip(JSON)); "PYIZ1R." is the uncompressed fallback for old browsers.
const TRANSFER_LIMIT = 5 * 1024 * 1024;
const toBase64Url = (bytes: Uint8Array) => {
  let binary = "";
  for (let index = 0; index < bytes.length; index += 0x8000) binary += String.fromCharCode(...bytes.subarray(index, index + 0x8000));
  return btoa(binary).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
};
const fromBase64Url = (text: string) => Uint8Array.from(atob(text.replace(/-/g, "+").replace(/_/g, "/")), char => char.charCodeAt(0));
async function runStream(stream: CompressionStream | DecompressionStream, input: Uint8Array) {
  const writer = stream.writable.getWriter();
  void writer.write(input as BufferSource).catch(() => undefined); void writer.close().catch(() => undefined);
  const reader = stream.readable.getReader();
  const chunks: Uint8Array[] = []; let size = 0;
  for (;;) {
    const { done, value } = await reader.read();
    if (done) break;
    size += value.length;
    if (size > TRANSFER_LIMIT) { void reader.cancel(); throw new Error("Aktarım kodu çok büyük."); }
    chunks.push(value);
  }
  const out = new Uint8Array(size); let offset = 0;
  for (const chunk of chunks) { out.set(chunk, offset); offset += chunk.length; }
  return out;
}
export async function encodeTransfer(progress: LearningProgress) {
  // A running exam belongs to this device and its clock; only the learning record travels.
  const json = JSON.stringify({ app: "python-iz", formatVersion: 1, progress: { ...parseProgress(progress), activeQuiz: null } });
  const bytes = new TextEncoder().encode(json);
  if (typeof CompressionStream === "undefined") return "PYIZ1R." + toBase64Url(bytes);
  return "PYIZ1." + toBase64Url(await runStream(new CompressionStream("gzip"), bytes));
}
export async function decodeTransfer(code: string): Promise<LearningProgress> {
  const text = code.replace(/\s+/g, "");
  const raw = text.startsWith("PYIZ1R.");
  if (!raw && !text.startsWith("PYIZ1.")) throw new Error("Bu bir Python İz aktarım kodu değil.");
  const body = text.slice(raw ? 7 : 6);
  if (body.length > TRANSFER_LIMIT || !/^[A-Za-z0-9_-]+$/.test(body)) throw new Error("Aktarım kodu bozuk.");
  let bytes: Uint8Array;
  try { bytes = fromBase64Url(body); } catch { throw new Error("Aktarım kodu bozuk."); }
  if (!raw) {
    if (typeof DecompressionStream === "undefined") throw new Error("Bu tarayıcı sıkıştırılmış kodu açamıyor; yedek dosyasını kullan.");
    try { bytes = await runStream(new DecompressionStream("gzip"), bytes); } catch (error) { throw error instanceof Error && error.message.includes("büyük") ? error : new Error("Aktarım kodu bozuk."); }
  }
  return importProgress(new TextDecoder().decode(bytes));
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

export function completeLesson(progress: LearningProgress, key: string): LearningProgress {
  if (progress.completedSections[key] || !progress.lessonRuns[key]) return progress;
  return { ...markStudy(progress), xp: progress.xp + 20, completedSections: { ...progress.completedSections, [key]: true } };
}

export class LocalStorageProgressRepository {
  private key = "python-iz-progress-v3";
  load(): LearningProgress {
    if (typeof window === "undefined") return structuredClone(defaultProgress);
    try {
      const stored = window.localStorage.getItem(this.key) ?? window.localStorage.getItem("python-iz-progress-v2") ?? window.localStorage.getItem("python-iz-progress-v1");
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
    if (this.blocked) return false;
    try { window.localStorage.setItem(this.key, JSON.stringify(progress)); return true; }
    catch { this.warn("İlerleme bu tarayıcıya kaydedilemedi. Ayrılmadan İstatistikler bölümünden yedek indir."); return false; }
  }
  restore(progress: LearningProgress) {
    const validated = parseProgress(progress);
    // localStorage.setItem is atomic: quota failure leaves the current record intact.
    const previous = window.localStorage.getItem(this.key) ?? window.localStorage.getItem("python-iz-progress-v2") ?? window.localStorage.getItem("python-iz-progress-v1");
    if (previous) window.localStorage.setItem("python-iz-before-import", previous);
    window.localStorage.setItem(this.key, JSON.stringify(validated));
    this.blocked = false;
    return validated;
  }
  previousBackup() {
    return window.localStorage.getItem("python-iz-before-import");
  }
  clear() {
    window.localStorage.removeItem(this.key);
    window.localStorage.removeItem("python-iz-progress-v2");
    window.localStorage.removeItem("python-iz-progress-v1");
  }
}
export const progressRepository = new LocalStorageProgressRepository();

