import module01 from "@/content/module-01.json";
import module02 from "@/content/module-02.json";
import type { LearningModule } from "@/lib/learning-types";

export const learningModules = [module01, module02] as LearningModule[];

export const curriculum = [
  "Temeller", "String'ler", "Akış kontrolü", "Veri yapıları", "Referans ve kopyalama", "Fonksiyonlar",
  "Hata yönetimi", "Dosyalar", "Modüller ve ekosistem", "Standart kütüphane", "OOP 1", "OOP 2",
  "İleri yapılar", "Type hints", "Eşzamanlılık", "Kod kalitesi", "Algoritmik düşünme", "Ekosisteme bakış",
];

export function getModule(id: number) {
  return learningModules.find((item) => item.id === id) ?? learningModules[0];
}

export function getPracticeQuestions(module: LearningModule) {
  return module.practiceIds.map((id) => module.questions.find((q) => q.id === id)).filter(Boolean) as LearningModule["questions"];
}

export function seededTestQuestions(module: LearningModule, seed: number, count = 18) {
  const current = [...module.questions];
  const previous = learningModules.filter((item) => item.id < module.id).flatMap((item) => item.questions);
  let state = seed || 1;
  const random = () => ((state = (state * 1664525 + 1013904223) >>> 0) / 4294967296);
  const shuffle = <T,>(items: T[]) => items.map((value) => ({ value, key: random() })).sort((a, b) => a.key - b.key).map(({ value }) => value);
  const previousCount = previous.length ? Math.round(count * 0.2) : 0;
  // Every module test includes writing, rather than leaving it to chance.
  const writing = shuffle(current.filter(question => question.type === "code")).slice(0, Math.min(3, count - previousCount));
  const remaining = current.filter(question => !writing.includes(question));
  return shuffle([...writing, ...shuffle(remaining).slice(0, count - previousCount - writing.length), ...shuffle(previous).slice(0, previousCount)]);
}

