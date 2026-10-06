"use client";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { WritingExercise } from "@/components/writing-lab";
import rawTasks from "@/content/workshop-tasks.json";
import { moduleIndex } from "@/lib/content";
import { exams, workshops } from "@/lib/milestone-data";
import { examPassCount, examSummary, milestoneAvailable, PASS_SCORE, workshopSteps, type Exam, type ReadStep, type Workshop } from "@/lib/milestones";
import type { LearningProgress, WritingTask } from "@/lib/learning-types";

export const workshopTasks = rawTasks as WritingTask[];
type UpdateProgress = (fn: (p: LearningProgress) => LearningProgress) => void;

function ExamCard({ exam, progress, available, onExam }: { exam: Exam; progress: LearningProgress; available: boolean; onExam: (exam: Exam) => void }) {
  const { count, code } = examSummary(exam, moduleIndex);
  const attempts = progress.attempts.filter(item => item.kind === "midterm" && item.moduleId === exam.afterModule);
  return <section className="lesson-card mt-4 p-5">
    <h3 className="text-xl font-black">{exam.title} <span className="text-base font-bold text-muted-foreground">· {exam.scope}</span></h3>
    <p className="mt-3 leading-7 text-muted-foreground">{exam.description}</p>
    <p className="mt-3 text-sm">{count} soru · {code} kod yazma · geçme notu %{PASS_SCORE} ({examPassCount(count)} doğru) · isteğe bağlı {exam.minutes} dakika</p>
    <Button className="mt-4" disabled={!available} onClick={() => onExam(exam)}>Sınavı aç</Button>
    <p className="mt-3 text-sm">{attempts.length ? `${attempts.length} deneme · son sonuç %${attempts.at(-1)!.score} · en iyi %${Math.max(...attempts.map(item => item.score))}` : "Henüz tamamlanmış deneme yok."}</p>
  </section>;
}

function ReadPanel({ step, done, onSolved, onNext }: { step: ReadStep; done: boolean; onSolved: () => void; onNext?: () => void }) {
  const [answer, setAnswer] = useState("");
  const [feedback, setFeedback] = useState("");
  function check() {
    if (answer.trim().replace(/\s+/g, " ") === step.answer) { onSolved(); setFeedback(step.explanation); }
    else setFeedback(step.wrongHint);
  }
  const shown = feedback || (done ? step.explanation : "");
  return <section className="lesson-card mt-5 p-5">
    <h4 className="font-black">{step.heading}</h4>
    <pre className="code-shell mt-4 overflow-x-auto p-4 text-sm text-slate-200">{step.code}</pre>
    <label className="mt-5 block text-sm font-bold">{step.inputLabel}<input className="mt-2 block w-full border border-border bg-background p-3 font-mono" value={answer} onChange={event => setAnswer(event.target.value)} placeholder={step.placeholder} /></label>
    <Button className="mt-3" onClick={check}>Yorumumu kontrol et</Button>
    {shown && <p role="status" className="mt-4 leading-7">{shown}</p>}
    {done && onNext && <Button className="mt-4 ml-2" variant="outline" onClick={onNext}>{step.nextLabel}</Button>}
  </section>;
}

function WorkshopCard({ workshop, progress, updateProgress, available }: { workshop: Workshop; progress: LearningProgress; updateProgress: UpdateProgress; available: boolean }) {
  const steps = workshopSteps(progress, workshop);
  const [active, setActive] = useState(() => Math.max(0, steps.findIndex(item => !item.done)));
  const doneCount = steps.filter(item => item.done).length;
  const current = steps[active];
  const goNext = current.step.nextLabel && active + 1 < steps.length ? () => setActive(active + 1) : undefined;
  const task = current.step.kind === "write" ? workshopTasks.find(item => item.id === (current.step as { taskId: string }).taskId) : undefined;
  return <section className="lesson-card mt-5 p-5">
    <h3 className="text-xl font-black">{workshop.title}</h3>
    <p className="mt-3 leading-7 text-muted-foreground">{workshop.summary}</p>
    <p className="mt-3 text-sm font-bold">{doneCount === steps.length ? "✓ Atölye tamamlandı" : `${doneCount}/${steps.length} adım tamamlandı`}</p>
    <div className="mt-4 flex flex-wrap gap-2" aria-label="Atölye adımları">
      {steps.map((item, index) => <Button key={item.step.label} variant={active === index ? "default" : "outline"} disabled={!available || !item.open} aria-pressed={active === index} onClick={() => setActive(index)}>{index + 1} · {item.step.label}</Button>)}
    </div>
    {available && current.open && current.step.kind === "read" && <ReadPanel key={current.step.progressKey} step={current.step} done={current.done} onNext={goNext}
      onSolved={() => { const key = (current.step as ReadStep).progressKey; updateProgress(p => ({ ...p, workshopRead: { ...p.workshopRead, [key]: true } })); }} />}
    {available && current.open && current.step.kind === "write" && <div className="mt-5">
      {current.step.note && <p className="mb-4 text-sm leading-6 text-muted-foreground">{current.step.note}</p>}
      {task ? <WritingExercise key={task.id} task={task} progress={progress} updateProgress={updateProgress} /> : <p role="alert">Bu adımın görevi bulunamadı.</p>}
      {current.done && goNext && <Button className="mt-5" onClick={goNext}>{current.step.nextLabel}</Button>}
    </div>}
  </section>;
}

export function Milestones({ progress, updateProgress, onExam }: { progress: LearningProgress; updateProgress: UpdateProgress; onExam: (exam: Exam) => void }) {
  // One section per checkpoint, e.g. "M4 sonrası": the exam and workshops that follow that module.
  const points = [...new Set([...exams, ...workshops].map(item => item.afterModule))].sort((a, b) => a - b);
  return <div className="mx-auto max-w-3xl">
    <p className="rail-kicker text-primary">Bilgiyi bir araya getir</p>
    <h1 className="mt-3 text-3xl font-black">Ara sınav ve proje atölyeleri</h1>
    <p className="mt-4 leading-7 text-muted-foreground">Ara sınavlar önceki modülleri birlikte tekrar eder; atölyeler gerçek bir problemde önce okumayı, sonra düzeltmeyi, en sonda sıfırdan yazmayı ister. Sonuçlar bu tarayıcıda saklanır; bu çalışmalar modül testlerinin yerine geçmez.</p>
    {points.map(afterModule => {
      const available = milestoneAvailable(progress, afterModule);
      return <div key={afterModule} className="mt-8">
        <h2 className="text-2xl font-black">M{afterModule} sonrası</h2>
        {!available && <p className="mt-3 border border-amber-500 p-4" role="note">Önce M{afterModule} bitiriş testini geç. Bu çalışmalar bundan sonra açılır; önceki ilerlemen korunur.</p>}
        {exams.filter(exam => exam.afterModule === afterModule).map(exam => <ExamCard key={exam.id} exam={exam} progress={progress} available={available} onExam={onExam} />)}
        {workshops.filter(workshop => workshop.afterModule === afterModule).map(workshop => <WorkshopCard key={workshop.id} workshop={workshop} progress={progress} updateProgress={updateProgress} available={available} />)}
      </div>;
    })}
  </div>;
}
