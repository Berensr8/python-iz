"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import {
  BarChart3, BookOpen, BrainCircuit, Check, CheckCircle2,
  CircleAlert, Code2, Flame, HelpCircle, Lightbulb, ListChecks, LockKeyhole, Menu, Moon,
  MoveDown, MoveUp, Play, RotateCcw, Sparkles, Sun, Trophy, Volume2, VolumeX, XCircle,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { Switch } from "@/components/ui/switch";
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Sheet, SheetClose, SheetContent, SheetDescription, SheetHeader, SheetTitle, SheetTrigger } from "@/components/ui/sheet";
import { AlertDialog, AlertDialogAction, AlertDialogCancel, AlertDialogContent, AlertDialogDescription, AlertDialogFooter, AlertDialogHeader, AlertDialogTitle } from "@/components/ui/alert-dialog";
import { CodeRunner, usePythonRunner } from "@/components/code-runner";
import { curriculum, getModule, getPracticeQuestions, getSection, learningModules, questionModuleId, seededTestQuestions } from "@/lib/content";
import { isAnswerCorrect, selectedAnswer, wrongOptionFeedback } from "@/lib/answer-check";
import { completeLesson, decodeTransfer, defaultProgress, markStudy, progressRepository } from "@/lib/progress-repository";
import type { LearningProgress, Question, QuizDraft } from "@/lib/learning-types";

import { WritingLab, writingTasks } from "@/components/writing-lab";

import { createQuiz, initialDraft, quizSummary, secondsLeft, saveQuizDraft, answerQuiz, nextQuizQuestion, expireQuiz } from "@/lib/quiz-engine";
import { Milestones } from "@/components/milestones";
import { exams, workshops } from "@/lib/milestone-data";
import { attemptLabel, examByModule, examPassCount, examQuestions, milestoneAvailable, workshopSteps, type Exam } from "@/lib/milestones";
import { ProgressBackup, type IncomingProgress } from "@/components/progress-backup";

type Stage = "lesson" | "practice" | "writing" | "test" | "stats" | "midterm" | "milestones";
type OpenRequest = { moduleId: number; stage: Stage; sectionId?: string };

/** Opens the lesson section a question assesses; LearningApp validates and applies it. */
function openSection(moduleId: number, sectionId: string) {
  window.dispatchEvent(new CustomEvent<OpenRequest>("python-iz-open", { detail: { moduleId, stage: "lesson", sectionId } }));
}

function SectionLink({ question }: { question: Question }) {
  const moduleId = questionModuleId(question.id);
  const section = getSection(moduleId, question.sectionId);
  if (!section) return null;
  return <Button variant="outline" size="sm" className="mt-3" onClick={() => openSection(moduleId, section.id)}><BookOpen />Dersi aç: {section.title}</Button>;
}

function todayKey() {
  return new Intl.DateTimeFormat("en-CA", { timeZone: "Europe/Istanbul" }).format(new Date());
}

function playTone(enabled: boolean, kind: "correct" | "wrong" | "pass") {
  if (!enabled) return;
  const AudioContextClass = window.AudioContext || (window as typeof window & { webkitAudioContext?: typeof AudioContext }).webkitAudioContext;
  if (!AudioContextClass) return;
  const context = new AudioContextClass();
  const oscillator = context.createOscillator();
  const gain = context.createGain();
  oscillator.connect(gain); gain.connect(context.destination);
  oscillator.frequency.value = kind === "wrong" ? 180 : kind === "pass" ? 660 : 480;
  oscillator.type = kind === "wrong" ? "sawtooth" : "sine";
  gain.gain.setValueAtTime(0.06, context.currentTime);
  gain.gain.exponentialRampToValueAtTime(0.001, context.currentTime + (kind === "pass" ? 0.45 : 0.18));
  oscillator.start(); oscillator.stop(context.currentTime + (kind === "pass" ? 0.45 : 0.18));
  oscillator.onended = () => void context.close();
}

function CodeBlock({ code, label = "ornek.py" }: { code: string; label?: string }) {
  return (
    <div className="code-shell overflow-hidden">
      <div className="flex items-center gap-3 border-b border-white/10 px-4 py-3 font-mono text-xs text-slate-400">
        <span className="border border-cyan-300 px-1.5 py-0.5 font-black text-cyan-300">PY</span><span>{label} / SALT OKUNUR</span>
      </div>
      <pre className="overflow-x-auto p-5 font-mono text-[15px] leading-7 text-slate-200"><code>{code}</code></pre>
    </div>
  );
}

function ModuleNavigation({ activeModule, progress, onSelect, closeMobile }: { activeModule: number; progress: LearningProgress; onSelect: (id: number, locked: boolean) => void; closeMobile?: () => void }) {
  return (
    <nav className="space-y-1" aria-label="Modüller">
      {curriculum.map((title, index) => {
        const id = index + 1;
        const isFutureContent = !learningModules.some(module => module.id === id);
        // A locked module stays locked (lock icon, label) but can still be opened after a warning.
        const locked = id > progress.unlockedModule;
        const available = !locked && !isFutureContent;
        const current = id === activeModule;
        return (
          <button key={title} disabled={isFutureContent} title={locked && !isFutureContent ? "Kilitli: önceki modülleri bitirmen önerilir" : undefined} onClick={() => { onSelect(id, locked); closeMobile?.(); }} className={`module-row w-full text-left ${current ? "module-row-active" : ""} ${locked && !isFutureContent ? "opacity-70" : ""} disabled:cursor-not-allowed disabled:opacity-50`}>
            <span className="grid size-8 shrink-0 place-items-center border border-border font-mono text-xs font-bold">{available ? String(id).padStart(2, "0") : <LockKeyhole className="size-3.5" />}</span>
            <span className="min-w-0 flex-1"><span className="block truncate text-sm font-bold">{title}</span><span className="block text-xs text-muted-foreground">{current ? "Şu an buradasın" : isFutureContent ? "Yakında" : available ? "Açık" : "Kilitli · uyarıyla açılır"}</span></span>
          </button>
        );
      })}
    </nav>
  );
}

function LessonView({ moduleId, progress, updateProgress, onStage, focus }: { moduleId: number; progress: LearningProgress; updateProgress: (fn: (value: LearningProgress) => LearningProgress) => void; onStage: (stage: Stage) => void; focus: { sectionId: string; nonce: number } | null }) {
  const module = getModule(moduleId);
  const firstIncomplete = Math.max(0, module.sections.findIndex((section) => !progress.completedSections[`m${moduleId}:${section.id}`]));
  // Keyed by module and focus nonce: a module change or "Dersi aç" request remounts this view, so state starts fresh here.
  const focusIndex = focus ? module.sections.findIndex((item) => item.id === focus.sectionId) : -1;
  const [sectionIndex, setSectionIndex] = useState(focusIndex >= 0 ? focusIndex : firstIncomplete);
  const section = module.sections[sectionIndex];
  const completeCount = module.sections.filter((item) => progress.completedSections[`m${moduleId}:${item.id}`]).length;
  const lessonDone = completeCount === module.sections.length;
  const sectionKey = `m${moduleId}:${section.id}`;
  const canComplete = !!progress.lessonRuns[sectionKey] || !!progress.completedSections[sectionKey];

  function completeSection() {
    if (!canComplete) return;
    const key = `m${moduleId}:${section.id}`;
    updateProgress((current) => completeLesson(current, key));
    if (sectionIndex < module.sections.length - 1) setSectionIndex(sectionIndex + 1);
  }

  return (
    <div className="mx-auto max-w-3xl">
      <div className="lesson-intro mb-6">
        <span className="lesson-number" aria-hidden="true">{String(moduleId).padStart(2, "0")}</span>
        <div className="relative z-10 flex flex-wrap items-start justify-between gap-4">
          <div><p className="eyebrow-chip mb-4"><BookOpen className="size-4" /> RUN / MODÜL {moduleId} / DERS</p><h1 className="lesson-title">{section.title}</h1><p className="lesson-summary mt-5 text-base leading-7 text-muted-foreground">{section.summary}</p></div>
          <span className="section-count px-3 py-1.5 text-xs font-bold text-muted-foreground">{sectionIndex + 1}/{module.sections.length} BÖLÜM</span>
        </div>
      </div>

      <div className="chapter-track mb-7 flex gap-2 overflow-x-auto pb-2 scrollbar-none" aria-label="Ders bölümleri">
        {module.sections.map((item, index) => <button key={item.id} onClick={() => setSectionIndex(index)} data-current={index === sectionIndex} data-done={!!progress.completedSections[`m${moduleId}:${item.id}`]} className="min-w-10 flex-1" aria-label={`${index + 1}. bölüm: ${item.title}`} />)}
      </div>

      <section className="lesson-card p-5 sm:p-7"><p className="rail-kicker text-primary">{section.eyebrow}</p><p className="mt-4 text-[17px] leading-8 text-muted-foreground">{section.explanation}</p>{section.objectives.length > 0 && <div className="mt-5 border-t border-border pt-4"><p className="text-xs font-black uppercase tracking-[0.12em] text-muted-foreground">Bu bölümün sonunda</p><ul className="mt-2 space-y-1 text-sm leading-6">{section.objectives.map((item) => <li key={item} className="flex gap-2"><Check className="mt-1 size-3.5 shrink-0 text-primary" />{item}</li>)}</ul></div>}</section>
      {section.id === "variables-types" && <section className="memory-lab mt-5 lesson-card overflow-hidden p-5 sm:p-6"><p className="rail-kicker text-cyan-600 dark:text-cyan-300">Bellekte ne oluyor?</p><div className="mt-5 grid items-center gap-4 sm:grid-cols-[1fr_70px_1fr]"><div className="memory-node p-4"><span className="text-xs text-muted-foreground">İsim alanı</span><code className="mt-2 block text-lg font-black text-cyan-600 dark:text-cyan-300">user_count</code></div><div className="flex items-center justify-center"><span className="memory-arrow" /></div><div className="memory-node p-4"><span className="text-xs text-muted-foreground">int nesnesi</span><strong className="mt-2 block font-mono text-2xl text-amber-500">12</strong></div></div><p className="mt-4 text-sm leading-6 text-muted-foreground">Atama, değeri bir kutuya koymaz. Soldaki ismi sağdaki nesneye bağlar; sonraki modüllerde kopyalama tuzaklarını bu ok üzerinden izleyeceğiz.</p></section>}
      {section.depth === "okuma" && <p className="mt-5 text-sm font-bold text-primary">Okuma düzeyi · Önce davranışını tanı; kendi kodunda kullanmak zorunda değilsin.</p>}
      {section.runtime && <aside className="mt-5 border-l-2 border-primary pl-4 text-sm leading-6 text-muted-foreground"><strong className="text-foreground">Çalışma ortamı: </strong>{section.runtimeNote ?? (section.runtime === "mixed" ? "Editördeki örnekler tarayıcıda çalışır. Anlatımdaki subprocess komutları için yerel Python gerekir." : "Tarayıcıda çalışır · Python 3.12")}</aside>}
      {section.sources?.length ? <nav aria-label="Ders kaynakları" className="mt-3 flex flex-wrap gap-x-4 gap-y-2 text-xs">{section.sources.map((source) => <a key={source.url} href={source.url} target="_blank" rel="noreferrer" className="underline decoration-primary/50 underline-offset-4 hover:text-primary">{source.title} ↗</a>)}</nav> : null}
      <div className="mt-5"><CodeRunner key={sectionKey} initialCode={section.code} expectedOutput={section.expectedOutput} onRun={result => { if (result.version) updateProgress(current => ({ ...current, lessonRuns: { ...current.lessonRuns, [sectionKey]: true } })); }} /></div>
      {!canComplete && <p className="mt-3 text-sm text-muted-foreground">Bölümü tamamlamak için önce kodu en az bir kez çalıştır. Hata alman da bir denemedir; çıktıyı okuyup tekrar deneyebilirsin.</p>}

      <section className="note-grid mt-5 sm:grid-cols-2">
        <div className="note-card lesson-card p-5"><p className="mb-2 flex items-center gap-2 text-xs font-black uppercase tracking-[0.12em] text-primary"><BrainCircuit className="size-4" /> Neden böyle?</p><p className="leading-7 text-muted-foreground">{section.why}</p></div>
        <div className="note-card lesson-card border-amber-400/30 bg-amber-400/[0.04] p-5"><p className="mb-2 flex items-center gap-2 text-xs font-black uppercase tracking-[0.12em] text-amber-500"><Lightbulb className="size-4" /> Alternatifler</p><ul className="space-y-2 text-sm leading-6 text-muted-foreground">{section.alternatives.map((item) => <li key={item} className="flex gap-2"><span className="text-amber-500">•</span>{item}</li>)}</ul></div>
      </section>

      <section className="mt-5 lesson-card border-rose-400/25 p-5 sm:p-6"><p className="mb-3 flex items-center gap-2 text-xs font-black uppercase tracking-[0.12em] text-rose-500"><CircleAlert className="size-4" /> Sık yapılan hatalar / tuzaklar</p><div className="grid gap-3 sm:grid-cols-3">{section.traps.map((trap) => <div key={trap} className="border-l-2 border-primary bg-muted/50 p-3 text-sm leading-6 text-muted-foreground">{trap}</div>)}</div></section>

      <section className="mt-5 lesson-card overflow-hidden"><div className="border-b border-border p-5"><p className="text-xs font-black uppercase tracking-[0.12em] text-emerald-500">Gerçek kodda böyle görünür</p><p className="mt-2 text-sm text-muted-foreground">Kendi projende veya AI'ın ürettiği kodda karşılaşabileceğin kısa bir örnek:</p></div><CodeBlock code={section.realCode} label="gercek_kod.py" /><div className="grid gap-2 p-5">{section.lineByLine.map((line, index) => <div key={line} className="flex gap-3 text-sm leading-6 text-muted-foreground"><span className="grid size-6 shrink-0 place-items-center rounded-md bg-primary/10 font-mono text-xs font-bold text-primary">{index + 1}</span>{line}</div>)}</div></section>

      <div className="mt-7 flex flex-col-reverse justify-between gap-3 border-t border-border pt-6 sm:flex-row">
        <Button variant="outline" onClick={() => setSectionIndex(Math.max(0, sectionIndex - 1))} disabled={sectionIndex === 0}>Önceki bölüm</Button>
        {lessonDone && sectionIndex === module.sections.length - 1 ? <Button onClick={() => onStage("practice")} className="font-bold"><Code2 /> Pratiğe geç</Button> : <Button onClick={completeSection} disabled={!canComplete} className="font-bold"><Check /> Tamamla ve devam et</Button>}
      </div>
    </div>
  );
}

function QuestionCard({ question, number, total, noHints, sound, draft, answer, onDraft, onAnswered }: {
  question: Question; number: number; total: number; noHints: boolean; sound: boolean;
  draft: QuizDraft; answer?: { correct: boolean }; onDraft: (draft: QuizDraft) => void; onAnswered: (correct: boolean) => void;
}) {
  const [editorStart] = useState(draft.code);
  const [inputStart] = useState(draft.stdin);
  const [running, setRunning] = useState(false);
  const [error, setError] = useState("");
  const checkLock = useRef(false);
  const runPython = usePythonRunner();
  const checked = answer?.correct ?? null;
  const disabled = running || checked !== null;
  const selected = selectedAnswer(question, draft);
  const edit = (patch: Partial<QuizDraft>) => { if (!disabled) onDraft({ ...draft, ...patch }); };
  function move(from: number, direction: -1 | 1) {
    if (disabled) return;
    const to = from + direction;
    if (to < 0 || to >= draft.ordered.length) return;
    const copy = [...draft.ordered]; [copy[from], copy[to]] = [copy[to], copy[from]];
    edit({ ordered: copy });
  }
  async function checkAnswer() {
    if (checkLock.current || disabled) return;
    checkLock.current = true; setError(""); setRunning(true);
    let correct = isAnswerCorrect(question, selected);
    if (question.type === "code" || question.type === "order") {
      const result = await runPython(question.type === "code" ? draft.code : draft.ordered.join("\n"), question.type === "code" ? { tests: question.tests } : {});
      if (question.type === "code" && !result.cases) {
        setError(result.output || "Değerlendirme tamamlanamadı. Tekrar dene.");
        checkLock.current = false; setRunning(false); return;
      }
      correct = question.type === "code" ? result.ok : result.ok && result.output.trimEnd() === question.expectedOutput;
    }
    onAnswered(correct);
    if (!noHints) playTone(sound, correct ? "correct" : "wrong");
    setRunning(false);
  }
  return <div className="mx-auto max-w-3xl">
    <div className="mb-5 flex items-center justify-between gap-4"><span className="eyebrow-chip">{question.type === "output" ? "Çıktıyı bul" : question.type === "bug" ? "Hatayı bul" : question.type === "fill" ? "Boşluk doldur" : question.type === "order" ? "Kod sıralama" : question.type === "code" ? "Kısa kod yaz" : "Traceback oku"}</span><span className="section-count px-3 py-1.5 font-mono text-sm">{number}/{total}</span></div>
    <h2 className="text-2xl font-black tracking-tight sm:text-3xl">{question.prompt}</h2>
    {question.code && <div className="mt-5"><CodeBlock code={question.code} label="soru.py" /></div>}
    {question.type === "code" && <div className="mt-5"><CodeRunner initialCode={editorStart} initialInput={inputStart} expectedOutput={noHints ? undefined : question.expectedOutput} compact onChange={code => edit({ code })} onInputChange={stdin => edit({ stdin })} readOnly={disabled} /></div>}
    {question.type === "fill" && !question.options?.length && <label className="mt-5 block"><span className="mb-2 block font-bold">Cevabın</span><input value={draft.fill} onChange={event => edit({ fill: event.target.value })} disabled={disabled} className="h-12 w-full border-2 border-input bg-card px-4 font-mono" placeholder="Boşluğa gelecek ifadeyi yaz" /></label>}
    {!!question.options?.length && <div className="mt-5 grid gap-3 sm:grid-cols-2">{question.options.map(option => <button key={option} disabled={disabled} onClick={() => edit({ choice: option })} className={"answer-option " + (draft.choice === option ? "answer-option-selected" : "")}>{option}</button>)}</div>}
    {question.type === "order" && <div className="mt-5 space-y-2">{draft.ordered.map((line, index) => <div key={index} className="flex items-center gap-2 border-2 border-border bg-card p-3 font-mono text-sm"><span>{index + 1}</span><code className="min-w-0 flex-1 whitespace-pre-wrap">{line}</code><Button size="icon-sm" variant="ghost" disabled={disabled || index === 0} onClick={() => move(index, -1)} aria-label="Yukarı taşı"><MoveUp /></Button><Button size="icon-sm" variant="ghost" disabled={disabled || index === draft.ordered.length - 1} onClick={() => move(index, 1)} aria-label="Aşağı taşı"><MoveDown /></Button></div>)}</div>}
    {!noHints && checked === null && <div className="mt-5 border-2 border-amber-400/40 p-4">{draft.hints > 0 && <p className="mb-3 whitespace-pre-wrap text-sm leading-6">{draft.hints <= 2 ? question.hints[draft.hints - 1] : question.answer}</p>}<Button variant="outline" size="sm" disabled={disabled || draft.hints === 3} onClick={() => edit({ hints: Math.min(3, draft.hints + 1) })}><HelpCircle />{draft.hints < 2 ? (draft.hints + 1) + ". ipucu" : "Çözümü göster"}</Button></div>}
    {checked !== null && !noHints && <div className={"mt-5 border-2 p-5 " + (checked ? "border-emerald-500/50" : "border-rose-500/50")}><p className="font-black">{checked ? "Doğru — mantığı yakaladın." : "Henüz değil — nedenine bakalım."}</p>{!checked && wrongOptionFeedback(question, draft.choice) && <p className="mt-2 leading-7"><strong>Seçtiğin “{draft.choice}”:</strong> {wrongOptionFeedback(question, draft.choice)}</p>}<p className="mt-2 leading-7 text-muted-foreground">{question.explanation}</p>{!checked && <><pre className="mt-3 whitespace-pre-wrap font-mono text-sm">{question.answer}</pre><SectionLink question={question} /></>}</div>}
    {checked !== null && noHints && <p className="mt-5 text-sm">Yanıt kaydedildi. Açıklamalar test tamamlanınca açılacak.</p>}
    {error && <p role="alert" className="mt-4 text-rose-500">{error}</p>}
    {checked === null && <Button onClick={checkAnswer} disabled={disabled || (question.type !== "code" && !selected)} className="mt-6">{running ? "Kod kontrol ediliyor…" : noHints ? "Yanıtı kaydet" : "Cevabı kontrol et"}</Button>}
  </div>;
}

function QuizView({ moduleId, mode, exam, progress, updateProgress, onStage, weakOnly = false }: { moduleId: number; mode: "practice" | "test" | "midterm"; exam?: Exam; progress: LearningProgress; updateProgress: (fn: (value: LearningProgress) => LearningProgress) => void; onStage: (stage: Stage) => void; weakOnly?: boolean }) {
  const [timed, setTimed] = useState(false);
  const [newRound, setNewRound] = useState(false);
  const [now, setNow] = useState(Date.now());
  const [message, setMessage] = useState("");
  const stored = progress.activeQuiz;
  const session = !newRound && stored?.moduleId === moduleId && stored.mode === mode && stored.weakOnly === weakOnly ? stored : null;
  useEffect(() => {
    if (!session || session.completedAt !== null || session.deadline === null) return;
    const timer = window.setInterval(() => setNow(Date.now()), 500);
    return () => window.clearInterval(timer);
  }, [session?.id, session?.completedAt, session?.deadline]);

  function start() {
    if (stored && stored.completedAt === null && !window.confirm("Devam eden oturumun yerine yeni bir oturum başlatılsın mı? Önceki cevapların soru istatistiklerinde kalır; tamamlanmamış oturum için bitiriş ödülü verilmez.")) return;
    const module = getModule(moduleId);
    const questions = mode === "midterm" ? (exam ? examQuestions(exam, learningModules) : []) : mode === "test" ? seededTestQuestions(module, Date.now() & 0xffffffff, 18) : !weakOnly ? getPracticeQuestions(module) :
      learningModules.flatMap(item => item.questions)
        .filter(question => (progress.questionResults[question.id]?.wrong ?? 0) > 0)
        .sort((a, b) => {
          const ra = progress.questionResults[a.id], rb = progress.questionResults[b.id];
          return ra.correct / (ra.correct + ra.wrong) - rb.correct / (rb.correct + rb.wrong);
        }).slice(0, 15);
    if (!questions.length) { setMessage("Tekrar gerektiren yanıtlanmış soru yok. Yeni konular için ders ve pratiğe geçebilirsin."); return; }
    if (mode === "midterm" && (!exam || !milestoneAvailable(progress, exam.afterModule))) return;
    const next = createQuiz(crypto.randomUUID(), moduleId, mode, questions, timed, weakOnly, Date.now(), exam?.minutes);
    updateProgress(current => ({ ...current, activeQuiz: next }));
    setNow(Date.now()); setNewRound(false);
  }
  if (!session) return <div className="mx-auto max-w-2xl lesson-card p-6">
    <p className="rail-kicker text-primary">{mode === "midterm" && exam ? `${exam.title} · ${exam.scope}` : `Modül ${moduleId}`} / {weakOnly ? "Zayıf konu tekrarı" : mode !== "practice" ? "Bitiriş testi" : "Pratik"}</p>
    <h1 className="mt-4 text-3xl font-black">{mode !== "practice" ? (mode === "midterm" && exam ? `${exam.questionIds.length} soru · geçme notu %70` : "18 soru · geçme notu %70") : weakOnly ? "Yanlışlarından yeni bir tur" : "Öğrendiklerini dene"}</h1>
    <p className="mt-4 leading-7 text-muted-foreground">{mode !== "practice" ? "En az 3 kod yazma sorusu var. İpuçları kapalı; açıklamalar sonuçta açılır. Süreli testte sayfayı kapatmak süreyi durdurmaz. Süre sonunda boş sorular puana katkı sağlamaz." : "Cevapların, kodun ve ipuçların bu tarayıcıda saklanır. İstersen derse dönüp sonra aynı sorudan devam edebilirsin."}</p>
    <p className="mt-3 text-sm text-muted-foreground">Bu bir yerel öğrenme aracıdır. Cihazlar arasında otomatik eşitleme veya güvenli sınav denetimi yoktur; tek sekmede çalış.</p>
    {mode !== "practice" && <label className="mt-5 flex items-center gap-3"><Switch checked={timed} onCheckedChange={setTimed} />{mode === "midterm" && exam ? exam.minutes : 25} dakikalık süreyi aç</label>}
    {stored?.completedAt === null && <p className="mt-4 text-sm">Modül {stored.moduleId} için devam eden bir oturum var. Üstteki “Oturuma dön” düğmesiyle sürdürebilirsin.</p>}
    <Button className="mt-6" onClick={start}><Play />{mode !== "practice" ? "Testi başlat" : "Pratiği başlat"}</Button>
    {message && <p role="status" className="mt-4">{message}</p>}
  </div>;
  const summary = quizSummary(session);
  if (session.completedAt !== null) {
    return <div className="mx-auto max-w-3xl">
      <section className="lesson-card p-6"><p className="rail-kicker text-primary">{session.finishReason === "timeout" ? "Süre doldu · sonuç kaydedildi" : "Oturum tamamlandı"}</p>
        <h1 className="mt-4 text-3xl font-black">{mode !== "practice" ? summary.passed ? "Testi geçtin!" : "Bir tur daha güçlenelim" : weakOnly ? "Tekrar tamamlandı" : "Pratik tamamlandı"}</h1>
        <p className="mt-4 text-lg">%{summary.score} · {summary.correct} doğru / {session.questions.length} soru</p>
        <p className="mt-2 text-sm text-muted-foreground">{summary.unanswered} boş soru. Sonuç ve bitiriş ödülü bu oturum için yalnızca bir kez kaydedilir.</p>
        <Progress value={summary.score} className="mt-5" />
        <div className="mt-5 flex flex-wrap gap-3">
          <Button variant="outline" onClick={() => setNewRound(true)}><RotateCcw />Yeni tur</Button>
          {mode === "practice" && !weakOnly && <Button onClick={() => onStage("test")}>Yazma / bitiriş adımına geç</Button>}
          {mode === "test" && summary.passed && learningModules.some(module => module.id === moduleId + 1) && <Button onClick={() => window.dispatchEvent(new CustomEvent("python-iz-open", { detail: { moduleId: moduleId + 1, stage: "lesson" } }))}>Sonraki modül</Button>}
          <Button variant="outline" onClick={() => onStage("stats")}><BarChart3 />İstatistikler</Button>
        </div>
      </section>
      <h2 className="mt-7 text-xl font-black">Yanıt incelemesi</h2>
      {mode === "midterm" && <Button className="mt-4" variant="outline" onClick={() => onStage("milestones")}>Atölye ve ara sınavlara dön</Button>}
      <div className="mt-4 space-y-3">{session.questions.map(question => {
        const answer = session.answers[question.id], draft = session.drafts[question.id];
        return <details key={question.id} className="lesson-card p-4"><summary className="cursor-pointer font-bold">{!answer ? "Boş" : answer.correct ? "✓" : "×"} · {question.prompt}</summary>
          <p className="mt-3 text-sm leading-6">{question.explanation}</p>
          {draft && <><p className="mt-3 text-sm font-bold">Senin yanıtın / taslağın</p><pre className="mt-2 whitespace-pre-wrap break-words text-sm">{question.type === "code" ? draft.code : question.type === "order" ? draft.ordered.join("\n") : draft.choice || draft.fill || "(boş)"}</pre></>}
          {draft && !answer?.correct && wrongOptionFeedback(question, draft.choice) && <p className="mt-3 text-sm leading-6"><strong>Bu seçenek neden yanlış:</strong> {wrongOptionFeedback(question, draft.choice)}</p>}
          <p className="mt-3 text-sm font-bold">Referans cevap</p><pre className="mt-2 whitespace-pre-wrap break-words text-sm">{question.answer}</pre>
          {!answer?.correct && <SectionLink question={question} />}
        </details>;
      })}</div>
    </div>;
  }
  const question = session.questions[session.index];
  const draft = session.drafts[question.id] ?? initialDraft(question);
  const remaining = secondsLeft(session, now);
  return <div>
    <div className="mx-auto mb-6 flex max-w-3xl flex-wrap items-center gap-4"><Progress value={100 * summary.answered / session.questions.length} className="min-w-24 flex-1" /><span className="text-sm">{summary.answered}/{session.questions.length} yanıt kaydedildi</span>{remaining !== null && <span role="timer" aria-label="Kalan süre" className="section-count px-3 py-2 font-mono">{String(Math.floor(remaining / 60)).padStart(2, "0")}:{String(remaining % 60).padStart(2, "0")}</span>}</div>
    <QuestionCard key={session.id + question.id} question={question} number={session.index + 1} total={session.questions.length} noHints={mode !== "practice"} sound={progress.sound} draft={draft} answer={session.answers[question.id]}
      onDraft={value => updateProgress(current => saveQuizDraft(current, session.id, question.id, value))}
      onAnswered={correct => updateProgress(current => answerQuiz(current, session.id, question.id, correct))} />
    {session.answers[question.id] && <div className="mx-auto mt-5 flex max-w-3xl justify-end"><Button onClick={() => updateProgress(current => nextQuizQuestion(current, session.id, question.id))}>{session.index === session.questions.length - 1 ? "Sonucu gör" : "Sonraki soru"}</Button></div>}
  </div>;
}

function StatsView({ progress, onReview }: { progress: LearningProgress; onReview: () => void }) {
  // Modules opened early (while still locked) count once the student has answered something in them.
  const openModules = learningModules.filter((module) => module.id <= progress.unlockedModule || module.questions.some((question) => progress.questionResults[question.id]));
  // Per lesson section, so every weak row can link straight to the lesson that teaches it.
  const sectionRows = openModules.flatMap((module) => module.sections.map((section) => {
    const questions = module.questions.filter((question) => question.sectionId === section.id);
    const results = questions.map((question) => progress.questionResults[question.id]).filter(Boolean);
    return { module, section, total: questions.length, attempted: results.length,
      correct: results.reduce((sum, item) => sum + item.correct, 0), wrong: results.reduce((sum, item) => sum + item.wrong, 0),
      // Wrong at least once and never answered correctly since: a misconception, not just an unseen topic.
      misread: questions.filter((question) => { const item = progress.questionResults[question.id]; return item && item.wrong > 0 && item.correct === 0; }).length };
  }));
  const rows = sectionRows.filter((row) => row.attempted > 0).sort((a, b) => a.correct / (a.correct + a.wrong) - b.correct / (b.correct + b.wrong));
  const unseen = sectionRows.reduce((sum, row) => sum + row.total - row.attempted, 0);
  const misread = sectionRows.reduce((sum, row) => sum + row.misread, 0);
  const totalCorrect = Object.values(progress.questionResults).reduce((sum, item) => sum + item.correct, 0);
  const totalWrong = Object.values(progress.questionResults).reduce((sum, item) => sum + item.wrong, 0);
  const rate = Math.round((totalCorrect / Math.max(1, totalCorrect + totalWrong)) * 100);
  return (
    <div className="mx-auto max-w-5xl"><p className="rail-kicker text-primary">Öğrenme raporun</p><h1 className="brand-word mt-3 text-4xl font-black tracking-[-0.05em] sm:text-5xl">İSTATİSTİKLER</h1><div className="lesson-card mt-6 p-5"><h2 className="font-black">Kod yazma / ayrı beceri takibi</h2>{workshops.map(workshop => { const steps = workshopSteps(progress, workshop); return <p key={workshop.id} className="mt-2 text-sm">{workshop.title}: {steps.filter(item => item.done).length}/{steps.length} adım tamamlandı.</p>; })}<p className="mt-2 text-sm leading-6 text-muted-foreground">{writingTasks.filter(task => progress.writingResults[task.id]?.passed).length}/{writingTasks.length} görev tamamlandı · {writingTasks.filter(task => progress.writingResults[task.id]?.independent).length} görev ipucusuz çözüldü. Bu ölçüm, okuma sorularındaki başarıdan ayrıdır.</p></div><div className="mt-7 grid gap-4 sm:grid-cols-3"><div className="metric-card"><span>Genel başarı</span><strong>%{rate}</strong><Progress value={rate} className="mt-3" /></div><div className="metric-card"><span>Toplam XP</span><strong>{progress.xp}</strong><p>{totalCorrect + totalWrong} soru yanıtlandı</p></div><div className="metric-card"><span>İpucu kullanımı</span><strong>{Object.values(progress.hintUsage).reduce((a, b) => a + b, 0)}</strong><p>öğrenme desteği</p></div></div><div className="mt-5 grid gap-5 lg:grid-cols-[1fr_320px]"><section className="lesson-card p-5 sm:p-6"><div className="flex items-center justify-between"><h2 className="text-lg font-black">Ders bölümü bazında başarı</h2><span className="text-xs text-muted-foreground">Zayıftan güçlüye</span></div><p className="mt-2 text-sm leading-6 text-muted-foreground">Açık modüllerde <strong>{misread}</strong> soru yanlış yanıtlandı ve henüz doğru çözülmedi (yanlış öğrenilmiş olabilir); <strong>{unseen}</strong> soru hiç denenmedi (henüz çalışılmamış).</p>{rows.length === 0 ? <div className="py-12 text-center text-muted-foreground"><BrainCircuit className="mx-auto mb-3 size-8" />Soruları çözdükçe konu haritan burada oluşacak.</div> : <div className="mt-5 space-y-4">{rows.map((row) => { const rowRate = Math.round(row.correct / (row.correct + row.wrong) * 100); return <div key={`${row.module.id}:${row.section.id}`}><div className="mb-2 flex items-center justify-between gap-3 text-sm"><button className="min-w-0 truncate text-left font-bold underline-offset-4 hover:underline" onClick={() => openSection(row.module.id, row.section.id)} title="Bu bölümün dersini aç">M{row.module.id} · {row.section.title}</button><span className="shrink-0 font-mono text-muted-foreground">{row.misread > 0 && <span className="mr-2 text-rose-500">{row.misread} yanlış</span>}{row.attempted}/{row.total} soru · %{rowRate}</span></div><Progress value={rowRate} /></div>; })}</div>}</section><aside className="lesson-card p-5 sm:p-6"><Trophy className="size-6 text-amber-400" /><h2 className="mt-4 text-lg font-black">Test geçmişi</h2>{progress.attempts.length === 0 ? <p className="mt-2 text-sm leading-6 text-muted-foreground">İlk bitiriş testinden sonra sonuçların burada görünür.</p> : <div className="mt-4 space-y-3">{[...progress.attempts].reverse().slice(0, 5).map((attempt, index) => <div key={`${attempt.date}-${index}`} className="flex items-center justify-between border-l-2 border-primary bg-muted p-3 text-sm"><span>{attemptLabel(exams, attempt)}</span><strong className={attempt.score >= 70 ? "text-emerald-500" : "text-rose-500"}>%{attempt.score}</strong></div>)}</div>}<Button className="mt-5 w-full" onClick={onReview} disabled={rows.length === 0}><BrainCircuit /> Zayıf konulardan test</Button></aside></div></div>
  );
}

export function LearningApp() {
  const [progress, setProgress] = useState<LearningProgress>(defaultProgress);
  const [hydrated, setHydrated] = useState(false);
  const progressRef = useRef(progress);
  const [storageWarning, setStorageWarning] = useState("");
  const [moduleId, setModuleId] = useState(1);
  const [stage, setStage] = useState<Stage>("lesson");
  const [weakOnly, setWeakOnly] = useState(false);
  const [focus, setFocus] = useState<{ sectionId: string; nonce: number } | null>(null);
  // A locked module the student asked to open; waits for confirmation of the warning.
  const [pendingModule, setPendingModule] = useState<number | null>(null);
  // Progress that arrived through a transfer link (#aktar=...) and waits for the student's decision.
  const [incoming, setIncoming] = useState<IncomingProgress | null>(null);
  const [incomingError, setIncomingError] = useState("");
  const [mountedAt] = useState(() => Date.now());
  const [reminderSnoozed, setReminderSnoozed] = useState(true);
  const module = getModule(moduleId);
  const completed = module.sections.filter((section) => progress.completedSections[`m${moduleId}:${section.id}`]).length;
  const lessonDone = completed === module.sections.length;
  const practiceDone = progress.completedPractice[`m${moduleId}`] === true;
  const writingDone = writingTasks.filter(task => task.moduleId === moduleId).every(task => progress.writingResults[task.id]?.passed);

  const updateProgress = useCallback((fn: (value: LearningProgress) => LearningProgress) => {
    const current = progressRef.current;
    const next = fn(current);
    if (next === current) return;
    const studied = next.lastStudyDate === todayKey() ? markStudy({ ...next, lastStudyDate: current.lastStudyDate, streak: current.streak }) : next;
    progressRef.current = studied;
    progressRepository.save(studied);
    setProgress(studied);
  }, []);
  function restoreProgress(value: LearningProgress) {
    progressRef.current = value; setProgress(value); setStorageWarning("");
    document.documentElement.classList.toggle("dark", value.theme === "dark");
    setModuleId(1); setWeakOnly(false);
  }
  function resumeQuiz() {
    const session = progressRef.current.activeQuiz;
    if (!session) return;
    setModuleId(session.moduleId); setStage(session.mode); setWeakOnly(session.weakOnly);
  }

  useEffect(() => { const handler = (event: Event) => setStorageWarning((event as CustomEvent<string>).detail); window.addEventListener("python-iz-storage-error", handler); return () => window.removeEventListener("python-iz-storage-error", handler); }, []);
  useEffect(() => {
    if (!hydrated) return;
    const tick = () => updateProgress(current => expireQuiz(current));
    tick(); const timer = window.setInterval(tick, 500);
    window.addEventListener("focus", tick); document.addEventListener("visibilitychange", tick);
    return () => { window.clearInterval(timer); window.removeEventListener("focus", tick); document.removeEventListener("visibilitychange", tick); };
  }, [hydrated, updateProgress]);
  useEffect(() => {
    if (!hydrated) return;
    const match = /^#aktar=(.+)$/.exec(window.location.hash);
    if (!match) return;
    // The code is only read here; drop it from the address bar and history right away.
    window.history.replaceState(null, "", window.location.pathname + window.location.search);
    decodeTransfer(match[1]).then(
      value => { setIncoming({ progress: value, source: "Bağlantıdan gelen ilerleme" }); setIncomingError(""); setStage("stats"); },
      error => { setIncoming(null); setIncomingError(`Bağlantıdaki aktarım kodu okunamadı.${error instanceof Error ? ` Neden: ${error.message.replace(/\.$/, "")}.` : ""} Mevcut ilerlemen değiştirilmedi.`); setStage("stats"); },
    );
  }, [hydrated]);
  useEffect(() => {
    const stored = expireQuiz(progressRepository.load());
    try { setReminderSnoozed(Date.parse(window.localStorage.getItem("python-iz-backup-snooze") ?? "") > Date.now()); } catch { setReminderSnoozed(false); }
    progressRef.current = stored; setProgress(stored); progressRepository.save(stored);
    document.documentElement.classList.toggle("dark", stored.theme === "dark");
    if (stored.activeQuiz && learningModules.some(item => item.id === stored.activeQuiz?.moduleId)) {
      setModuleId(stored.activeQuiz.moduleId); setStage(stored.activeQuiz.mode); setWeakOnly(stored.activeQuiz.weakOnly);
    }
    setHydrated(true);
  }, []);
  useEffect(() => {
    const handler = (event: Event) => {
      const detail = (event as CustomEvent<OpenRequest>).detail;
      if (!detail || detail.moduleId > progress.unlockedModule || !learningModules.some(module => module.id === detail.moduleId) || !["lesson", "practice", "writing", "test", "stats"].includes(detail.stage)) return;
      const target = getModule(detail.moduleId);
      if (detail.stage === "practice" && !target.sections.every(section => progress.completedSections[`m${target.id}:${section.id}`])) return;
      if (detail.stage === "test" && (!progress.completedPractice[`m${target.id}`] || !writingTasks.filter(task => task.moduleId === target.id).every(task => progress.writingResults[task.id]?.passed))) return;
      if (detail.stage === "lesson" && detail.sectionId && getSection(detail.moduleId, detail.sectionId)) setFocus({ sectionId: detail.sectionId, nonce: Date.now() });
      setModuleId(detail.moduleId); setStage(detail.stage); setWeakOnly(false); window.scrollTo({ top: 0, behavior: "smooth" });
    };
    window.addEventListener("python-iz-open", handler); return () => window.removeEventListener("python-iz-open", handler);
  }, [progress]);
  useEffect(() => {
    const documentWithContext = document as Document & { modelContext?: { registerTool: (tool: unknown, options?: { signal?: AbortSignal }) => void | Promise<void> } };
    const context = documentWithContext.modelContext; if (!context?.registerTool) return;
    const lifecycle = new AbortController();
    void Promise.resolve(context.registerTool({ name: "get_learning_progress", title: "Öğrenme ilerlemesini getir", description: "Python İz içindeki XP, açık modül ve test geçmişini okur.", inputSchema: { type: "object", properties: {}, additionalProperties: false }, annotations: { readOnlyHint: true, untrustedContentHint: false }, execute: () => { const value = progressRepository.load(); return { xp: value.xp, unlockedModule: value.unlockedModule, attempts: value.attempts.length }; } }, { signal: lifecycle.signal })).catch(() => undefined);
    void Promise.resolve(context.registerTool({ name: "open_learning_stage", title: "Öğrenme aşamasını aç", description: "Açık bir modülün ders, pratik, test veya istatistik görünümünü açar.", inputSchema: { type: "object", properties: { moduleId: { type: "integer", minimum: 1, maximum: Math.max(...learningModules.map(module => module.id)) }, stage: { type: "string", enum: ["lesson", "practice", "writing", "test", "stats"] } }, required: ["moduleId", "stage"], additionalProperties: false }, annotations: { readOnlyHint: false, untrustedContentHint: false }, execute: (input: unknown) => { const parsed = input as { moduleId: number; stage: Stage }; const current = progressRepository.load(); if (parsed.moduleId > current.unlockedModule) throw new Error("Bu modül henüz kilitli."); window.dispatchEvent(new CustomEvent("python-iz-open", { detail: parsed })); return { opened: true, ...parsed }; } }, { signal: lifecycle.signal })).catch(() => undefined);
    return () => lifecycle.abort();
  }, []);

  // Ordinary navigation drops a pending "Dersi aç" focus so a remounted lesson starts at the first unfinished section.
  function changeModule(id: number) { setFocus(null); setModuleId(id); setStage("lesson"); setWeakOnly(false); window.scrollTo({ top: 0, behavior: "smooth" }); }
  function markBackup() { updateProgress(current => ({ ...current, lastBackupAt: new Date().toISOString() })); }
  function snoozeReminder() {
    setReminderSnoozed(true);
    try { window.localStorage.setItem("python-iz-backup-snooze", new Date(Date.now() + 7 * 86400000).toISOString()); } catch { /* the reminder simply returns next visit */ }
  }
  // Worth a nudge once there is something to lose and no backup in the last two weeks.
  const backupStale = progress.xp >= 100 && (!progress.lastBackupAt || mountedAt - Date.parse(progress.lastBackupAt) > 14 * 86400000);
  function selectModule(id: number, locked: boolean) { if (locked) setPendingModule(id); else changeModule(id); }
  function changeStage(next: Stage) { setFocus(null); if (next === "practice" && !lessonDone) return; if (next === "test" && (!practiceDone || !writingDone)) { setStage("writing"); return; } setWeakOnly(false); setStage(next); window.scrollTo({ top: 0, behavior: "smooth" }); }
  function toggleTheme() { updateProgress((current) => { const theme = current.theme === "dark" ? "light" : "dark"; document.documentElement.classList.toggle("dark", theme === "dark"); return { ...current, theme }; }); }

  if (!hydrated) return <div className="grid min-h-screen place-items-center bg-background"><div className="flex items-center gap-3 font-mono text-sm font-bold uppercase tracking-[0.12em] text-muted-foreground"><span className="size-3 animate-pulse border border-foreground bg-primary" /> Öğrenme alanın hazırlanıyor</div></div>;

  return (
    <main className="app-shell min-h-screen bg-background text-foreground">
      <AlertDialog open={pendingModule !== null} onOpenChange={(open) => { if (!open) setPendingModule(null); }}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Bu modül henüz kilitli</AlertDialogTitle>
            <AlertDialogDescription>
              {pendingModule !== null && curriculum[pendingModule - 1]} modülünü açmadan önce önceki modülleri ve testlerini bitirmen önerilir; yeni konular öncekilerin üzerine kurulur. Yine de açabilirsin, ilerlemen kaydedilir.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>Vazgeç</AlertDialogCancel>
            <AlertDialogAction onClick={() => { if (pendingModule !== null) changeModule(pendingModule); setPendingModule(null); }}>Yine de aç</AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
      <header className="app-header sticky top-0 z-40 backdrop-blur-xl"><div className="mx-auto flex h-[72px] max-w-[1580px] items-center gap-3 px-4 sm:px-6"><Sheet><SheetTrigger asChild><Button variant="ghost" size="icon" className="lg:hidden" aria-label="Modülleri aç"><Menu /></Button></SheetTrigger><SheetContent side="left" className="w-[88%] overflow-y-auto p-0"><SheetHeader className="border-b-2 border-border p-5 text-left"><SheetTitle className="brand-word">ÖĞRENME YOLU</SheetTitle><SheetDescription>{curriculum.length} modül · {learningModules.length} modül hazır</SheetDescription></SheetHeader><div className="p-4"><ModuleNavigation activeModule={moduleId} progress={progress} onSelect={selectModule} /><SheetClose asChild><Button variant="outline" className="mt-4 w-full" onClick={() => setStage("stats")}><BarChart3 /> İstatistikler</Button></SheetClose></div></SheetContent></Sheet><button onClick={() => { setStage("lesson"); setModuleId(1); setWeakOnly(false); }} className="flex items-center gap-3 text-left"><span className="brand-mark font-mono text-sm">&gt;_</span><span className="hidden sm:block"><span className="brand-word block text-[17px] font-black">PYTHON İZ</span><span className="block font-mono text-[10px] uppercase tracking-[0.08em] text-muted-foreground">Kodu anla. Kendin yaz.</span></span></button><span className="ml-3 hidden border-l-2 border-foreground pl-3 font-mono text-[10px] font-bold uppercase tracking-[0.12em] text-muted-foreground lg:block">Etkileşimli Python Lab<br />Sürüm / 01</span><div className="ml-auto flex items-center gap-1.5 sm:gap-3"><div className="utility-stat hidden items-center gap-2 px-3 py-1.5 text-sm md:flex"><Flame className="size-4 text-orange-500" /> <strong>{progress.streak} gün</strong></div><div className="utility-stat flex items-center gap-2 px-3 py-1.5 text-sm"><Sparkles className="size-4 text-amber-500" /> <strong>{progress.xp} XP</strong></div><Button variant="ghost" size="icon" onClick={() => updateProgress((current) => ({ ...current, sound: !current.sound }))} aria-label={progress.sound ? "Sesi kapat" : "Sesi aç"}>{progress.sound ? <Volume2 /> : <VolumeX />}</Button><Button variant="ghost" size="icon" onClick={toggleTheme} aria-label="Temayı değiştir">{progress.theme === "dark" ? <Sun /> : <Moon />}</Button></div></div></header>

      <div className="mx-auto grid max-w-[1580px] grid-cols-1 lg:grid-cols-[265px_minmax(0,1fr)] xl:grid-cols-[265px_minmax(0,1fr)_300px]">
        <aside className="curriculum-rail hidden min-h-[calc(100vh-72px)] px-4 py-7 lg:block"><p className="rail-kicker mb-5 px-2 text-muted-foreground">Öğrenme yolu</p><div className="max-h-[calc(100vh-145px)] overflow-y-auto pr-1 scrollbar-thin"><ModuleNavigation activeModule={moduleId} progress={progress} onSelect={selectModule} /></div></aside>

        <section className="learning-canvas min-w-0 px-4 py-6 sm:px-7 lg:px-10 lg:py-9">
          {!["stats", "midterm", "milestones"].includes(stage) && <Tabs value={stage} onValueChange={(value) => changeStage(value as Stage)} className="stage-switcher mx-auto mb-9 max-w-3xl"><TabsList className="grid h-auto w-full grid-cols-2 sm:grid-cols-4"><TabsTrigger value="lesson"><BookOpen /> Ders</TabsTrigger><TabsTrigger value="writing"><Code2 /> Kod yaz</TabsTrigger><TabsTrigger value="practice" disabled={!lessonDone}><Code2 /> Pratik {!lessonDone && <LockKeyhole className="size-3" />}</TabsTrigger><TabsTrigger value="test" disabled={!practiceDone || !writingDone} title="Önce pratiği ve üç yazma görevini tamamla"><ListChecks /> Test {(!practiceDone || !writingDone) && <LockKeyhole className="size-3" />}</TabsTrigger></TabsList></Tabs>}
          <div className="mx-auto mb-6 flex max-w-3xl flex-wrap gap-2"><Button variant="outline" onClick={() => setStage("milestones")}>Ara sınav ve atölye</Button>{["milestones", "midterm", "stats"].includes(stage) && <Button variant="ghost" onClick={() => changeStage("lesson")}>Derse dön</Button>}</div>
          {stage === "milestones" && <Milestones progress={progress} updateProgress={updateProgress} onExam={(exam) => { if (milestoneAvailable(progress, exam.afterModule)) { setFocus(null); setModuleId(exam.afterModule); setWeakOnly(false); setStage("midterm"); } }} />}
          {stage === "midterm" && examByModule(exams, moduleId) && milestoneAvailable(progress, moduleId) && <QuizView key={moduleId} moduleId={moduleId} mode="midterm" exam={examByModule(exams, moduleId)} progress={progress} updateProgress={updateProgress} onStage={changeStage} />}
          {storageWarning && <p role="alert" className="mb-5 border border-amber-500 p-3 text-sm">{storageWarning}</p>}
          {backupStale && !reminderSnoozed && stage !== "stats" && <div role="note" className="mx-auto mb-5 flex max-w-3xl flex-wrap items-center gap-3 border border-amber-500 p-3 text-sm leading-6"><span className="min-w-0 flex-1">İlerlemen yalnızca bu tarayıcıda saklanıyor{progress.lastBackupAt ? "; son yedeğin 2 haftadan eski" : " ve henüz yedek almadın"}. Yedek alabilir ya da başka cihaza aktarabilirsin.</span><Button size="sm" onClick={() => setStage("stats")}>Yedek al / aktar</Button><Button size="sm" variant="ghost" onClick={snoozeReminder}>1 hafta sonra hatırlat</Button></div>}
          {moduleId > progress.unlockedModule && !["stats", "midterm", "milestones"].includes(stage) && <p role="note" className="mx-auto mb-5 max-w-3xl border border-amber-500 p-3 text-sm leading-6">Bu modül kilitli: önceki modülleri ve testlerini bitirmen önerilir. Burada çalıştıkların kaydedilir.</p>}
          {progress.activeQuiz && (stage !== progress.activeQuiz.mode || moduleId !== progress.activeQuiz.moduleId || weakOnly !== progress.activeQuiz.weakOnly) && <div className="lesson-card mx-auto mb-5 flex max-w-3xl flex-wrap items-center justify-between gap-3 p-4"><p className="text-sm">Modül {progress.activeQuiz.moduleId} · {progress.activeQuiz.completedAt === null ? "Devam eden oturumun saklanıyor. Süreli testte saat işlemeye devam eder." : "Son oturumunun sonucu hazır."}</p><Button variant="outline" onClick={resumeQuiz}>Oturuma dön</Button></div>}
          {stage === "writing" && <WritingLab key={moduleId} moduleId={moduleId} progress={progress} updateProgress={updateProgress} />}
          {stage === "lesson" && <LessonView key={`${moduleId}:${focus?.nonce ?? ""}`}moduleId={moduleId} progress={progress} updateProgress={updateProgress} onStage={changeStage} focus={focus} />}
          {(stage === "practice" || stage === "test") && <QuizView key={`${moduleId}:${stage}:${weakOnly}`} moduleId={moduleId} mode={stage} progress={progress} updateProgress={updateProgress} onStage={changeStage} weakOnly={weakOnly} />}
          {stage === "stats" && <StatsView progress={progress} onReview={() => { const weakestModule = Math.max(...learningModules.filter(item => item.id <= progress.unlockedModule).map(item => item.id)); setModuleId(weakestModule); setWeakOnly(true); setStage("practice"); }} />}
          {stage === "stats" && <ProgressBackup progress={progress} onRestore={restoreProgress} onBackup={markBackup} incoming={incoming} incomingError={incomingError} onIncomingHandled={() => { setIncoming(null); setIncomingError(""); }} />}
        </section>

        <aside className="progress-rail hidden min-h-[calc(100vh-72px)] px-5 py-7 xl:block"><div className="flex items-center justify-between"><p className="rail-kicker text-muted-foreground">İlerlemen</p><Button variant="ghost" size="icon-sm" onClick={() => setStage("stats")} aria-label="İstatistikleri aç"><BarChart3 /></Button></div><div className="lesson-card mt-4 p-5"><div className="flex items-center justify-between"><strong className="text-sm">Modül {moduleId}</strong><span className="font-mono text-xs text-primary">%{Math.round((completed / module.sections.length) * 100)}</span></div><Progress value={(completed / module.sections.length) * 100} className="mt-3 h-2" /><div className="mt-5 space-y-3 text-sm">{module.sections.slice(0, 5).map((section, index) => { const done = progress.completedSections[`m${moduleId}:${section.id}`]; return <button key={section.id} onClick={() => setStage("lesson")} className={`flex w-full items-center gap-3 text-left ${done ? "text-foreground" : "text-muted-foreground"}`}><span className={`grid size-6 shrink-0 place-items-center border ${done ? "border-emerald-500 bg-emerald-500/15 text-emerald-500" : "border-border"}`}>{done ? <Check className="size-3.5" /> : index + 1}</span><span className="truncate">{section.title}</span></button>; })}</div></div><div className="lesson-card mt-4 p-5"><Trophy className="size-5 text-amber-500" /><strong className="mt-3 block text-sm">Sıradaki hedef</strong><p className="mt-1 text-sm leading-6 text-muted-foreground">{lessonDone ? practiceDone ? "Bitiriş testinde %70'e ulaş." : "15 pratik sorusunu tamamla." : `${module.sections.length - completed} ders bölümü kaldı.`}</p><Progress value={lessonDone ? practiceDone ? 85 : 65 : (completed / module.sections.length) * 60} className="mt-3 h-1.5" /></div><Button variant="outline" className="mt-4 w-full" onClick={() => setStage("stats")}><BarChart3 /> İstatistikler</Button></aside>
      </div>
    </main>
  );
}

