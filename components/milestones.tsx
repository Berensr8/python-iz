"use client";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { WritingExercise } from "@/components/writing-lab";
import rawTasks from "@/content/workshop-tasks.json";
import reading from "@/content/workshop-reading.json";
import { milestonesAvailable } from "@/lib/milestones";
import type { LearningProgress, WritingTask } from "@/lib/learning-types";

export const workshopTasks = rawTasks as WritingTask[];
export function Milestones({ progress, updateProgress, onExam }: { progress: LearningProgress; updateProgress: (fn: (p: LearningProgress) => LearningProgress) => void; onExam: () => void }) {
  const [step, setStep] = useState(0);
  const [answer, setAnswer] = useState("");
  const [feedback, setFeedback] = useState("");
  const available = milestonesAvailable(progress);
  const read = !!progress.workshopRead["workshop1"];
  const fixed = !!progress.writingResults["workshop1-fix"]?.passed;
  const built = !!progress.writingResults["workshop1-build"]?.passed;
  const attempts = progress.attempts.filter(item => item.kind === "midterm");
  return <div className="mx-auto max-w-3xl">
    <p className="rail-kicker text-primary">M1–M4 / Bilgiyi bir araya getir</p>
    <h1 className="mt-3 text-3xl font-black">Ara sınav ve proje atölyesi</h1>
    <p className="mt-4 leading-7 text-muted-foreground">Temeller, metinler, akış kontrolü ve veri yapıları aynı problemde buluşuyor. Sonuçlar bu tarayıcıda saklanır; bu çalışmalar modül testlerinin yerine geçmez.</p>
    {!available && <p className="mt-5 border border-amber-500 p-4" role="note">Önce M4 bitiriş testini geç. İki çalışma da bundan sonra açılır; önceki ilerlemen korunur.</p>}
    <section className="lesson-card mt-6 p-5">
      <h2 className="text-xl font-black">Ara Sınav 1</h2>
      <p className="mt-3 leading-7 text-muted-foreground">20 soru: her modülden 5; bunların 4'ü kod yazma. Soru havuzundan seçilmiş sabit bir tekrar sınavıdır. Başarı eşiği %70 (14 doğru); isteğe bağlı 25 dakika. İpuçları kapalı, çözüm açıklamaları sonda.</p>
      <Button className="mt-4" disabled={!available} onClick={onExam}>Ara sınavı aç</Button>
      <p className="mt-3 text-sm">{attempts.length ? `${attempts.length} deneme · son sonuç %${attempts.at(-1)!.score} · en iyi %${Math.max(...attempts.map(item => item.score))}` : "Henüz tamamlanmış deneme yok."}</p>
    </section>
    <section className="lesson-card mt-5 p-5">
      <h2 className="text-xl font-black">Atölye 1 · Harcamaları analiz et</h2>
      <p className="mt-3 leading-7 text-muted-foreground">Önce bir raporun ne yaptığını açıkla, sonra bozuk hesabı onar. Son adımda yalnız gereksinimden kendi kategori raporunu yaz. Tutarlar kuruş cinsinden tam sayıdır; float yuvarlama bu projenin konusu değil.</p>
      <p className="mt-3 text-sm font-bold">{read && fixed && built ? "✓ Atölye tamamlandı" : `${Number(read) + Number(fixed) + Number(built)}/3 adım tamamlandı`}</p>
      <div className="mt-4 flex flex-wrap gap-2" aria-label="Atölye adımları">{["1 · İncele", "2 · Düzelt", "3 · Sıfırdan yaz"].map((label, index) => <Button key={label} variant={step === index ? "default" : "outline"} disabled={!available || (index > 0 && !read) || (index > 1 && !fixed)} aria-pressed={step === index} onClick={() => setStep(index)}>{label}</Button>)}</div>
    </section>
    {available && step === 0 && <section className="lesson-card mt-5 p-5">
      <h3 className="font-black">Kodun çıktısı ne? Hangi kayıtlar eleniyor?</h3>
      <pre className="code-shell mt-4 overflow-x-auto p-4 text-sm text-slate-200">{reading.code}</pre>
      <label className="mt-5 block text-sm font-bold">Çıktı (adet ve toplam)<input className="mt-2 block w-full border border-border bg-background p-3 font-mono" value={answer} onChange={event => setAnswer(event.target.value)} placeholder="Örn. 2 200" /></label>
      <Button className="mt-3" onClick={() => { if (answer.trim().replace(/\s+/g, " ") === reading.answer) { updateProgress(p => ({ ...p, workshopRead: { ...p.workshopRead, workshop1: true } })); setFeedback(reading.explanation); } else setFeedback("Her kaydı tek başına 100 ile karşılaştır. Kategori toplamı değil, geçen kayıtların sayısı ve tutarı soruluyor."); }}>Yorumumu kontrol et</Button>
      {feedback && <p role="status" className="mt-4 leading-7">{feedback}</p>}
      {read && <Button className="mt-4 ml-2" variant="outline" onClick={() => setStep(1)}>Düzeltme adımına geç</Button>}
    </section>}
    {available && step > 0 && read && (step === 1 || fixed) && <div className="mt-5">
      <p className="mb-4 text-sm leading-6 text-muted-foreground">Kontrol listesi: sınırdaki tutarı dahil et · boş veriyi işle · birden fazla kaydı biriktir · yalnız istenen çıktıyı yazdır.</p>
      <WritingExercise key={workshopTasks[step - 1].id} task={workshopTasks[step - 1]} progress={progress} updateProgress={updateProgress} />
      {step === 1 && fixed && <Button className="mt-5" onClick={() => setStep(2)}>Kendi raporunu yaz</Button>}
    </div>}
  </div>;
}
