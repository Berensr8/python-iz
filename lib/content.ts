import contentIndex from "virtual:content-index";
import type { LearningModule, ModuleSummary } from "@/lib/learning-types";

// Every content/module-NN.json is picked up at build time; adding a module needs no code change.
// Two views of the same files:
//  - moduleIndex: structure only (ids, titles, question types). Always in the main bundle, a few KB per module.
//  - loadModule: the full text, one separate chunk per module, fetched the first time it is needed.
export const moduleIndex: ModuleSummary[] = [...contentIndex].sort((a, b) => a.id - b.id);

// A non-generic glob declaration in the toolchain types shadows Vite's, hence the cast.
const moduleLoaders = import.meta.glob("../content/module-*.json", { import: "default" }) as unknown as Record<string, () => Promise<LearningModule>>;
const loaderById = new Map(Object.entries(moduleLoaders).map(([file, load]) => [Number(/module-(\d+)\.json$/.exec(file)?.[1]), load] as const));
const loaded = new Map<number, LearningModule>();
const pending = new Map<number, Promise<LearningModule>>();

export const curriculum = [
  "Temeller", "String'ler", "Akış kontrolü", "Veri yapıları", "Referans ve kopyalama", "Fonksiyonlar",
  "Hata yönetimi", "Dosyalar", "Modüller ve ekosistem", "Standart kütüphane", "OOP 1", "OOP 2",
  "İleri yapılar", "Type hints", "Eşzamanlılık", "Kod kalitesi", "Algoritmik düşünme", "Ekosisteme bakış",
];

export function getModuleSummary(id: number) {
  return moduleIndex.find((item) => item.id === id) ?? moduleIndex[0];
}

export function getSection(moduleId: number, sectionId: string) {
  return moduleIndex.find((item) => item.id === moduleId)?.sections.find((section) => section.id === sectionId);
}

/** Module that owns a question, derived from its id prefix ("m2-q10" → 2). */
export function questionModuleId(questionId: string) {
  return Number(/^m(\d+)-/.exec(questionId)?.[1] ?? 0);
}

/** The full module if it has been fetched already. */
export function loadedModule(id: number) {
  return loaded.get(id);
}

/** Fetches a module's text once; simultaneous callers share one request, and a failed fetch can be retried. */
export function loadModule(id: number): Promise<LearningModule> {
  const ready = loaded.get(id);
  if (ready) return Promise.resolve(ready);
  const running = pending.get(id);
  if (running) return running;
  const load = loaderById.get(id);
  if (!load) return Promise.reject(new Error(`Modül ${id} bulunamadı.`));
  const request = load().then(
    (module) => { loaded.set(id, module); pending.delete(id); return module; },
    (error) => { pending.delete(id); throw error; },
  );
  pending.set(id, request);
  return request;
}

export function loadModules(ids: number[]) {
  return Promise.all([...new Set(ids)].map(loadModule));
}

/** Warms the cache while the browser is idle so opening the next lesson feels instant; failures are ignored. */
export function prefetchModules(ids: number[]) {
  const run = () => ids.filter((id) => loaderById.has(id) && !loaded.has(id)).forEach((id) => void loadModule(id).catch(() => undefined));
  if (typeof window !== "undefined" && "requestIdleCallback" in window) window.requestIdleCallback(run, { timeout: 4000 });
  else setTimeout(run, 1500);
}

// A failed dynamic import() is remembered by the browser for the lifetime of the page: the same chunk
// keeps failing even after the network is back. The only reliable retry is a reload, so the screen the
// student was on is saved for the new page load to reopen.
const returnKey = "python-iz-return";
export type ReturnTarget = { moduleId: number; stage: string };

export function reloadToRetry(target: ReturnTarget) {
  try { window.sessionStorage.setItem(returnKey, JSON.stringify(target)); } catch { /* the reload still helps */ }
  window.location.reload();
}

/** The screen to reopen after reloadToRetry; reading it removes it, so it applies once. */
export function takeReturnTarget(): ReturnTarget | null {
  try {
    const raw = window.sessionStorage.getItem(returnKey);
    window.sessionStorage.removeItem(returnKey);
    const value = raw ? JSON.parse(raw) : null;
    return value && typeof value.stage === "string" && moduleIndex.some((item) => item.id === value.moduleId) ? { moduleId: value.moduleId, stage: value.stage } : null;
  } catch { return null; }
}
