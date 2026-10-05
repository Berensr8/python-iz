"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
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
import { CodeRunner, usePythonRunner } from "@/components/code-runner";
import { curriculum, getModule, getPracticeQuestions, learningModules, seededTestQuestions } from "@/lib/content";
import { defaultProgress, progressRepository } from "@/lib/progress-repository";
import type { LearningProgress, Question, TestAttempt } from "@/lib/learning-types";

type Stage = "lesson" | "practice" | "test" | "stats";

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

function ModuleNavigation({ activeModule, progress, onSelect, closeMobile }: { activeModule: number; progress: LearningProgress; onSelect: (id: number) => void; closeMobile?: () => void }) {
  return (
    <nav className="space-y-1" aria-label="Modüller">
      {curriculum.map((title, index) => {
        const id = index + 1;
        const available = id <= progress.unlockedModule && id <= 2;
        const current = id === activeModule;
        const isFutureContent = id > 2;
        return (
          <button key={title} disabled={!available} onClick={() => { onSelect(id); closeMobile?.(); }} className={`module-row w-full text-left ${current ? "module-row-active" : ""} disabled:cursor-not-allowed disabled:opacity-50`}>
            <span className="grid size-8 shrink-0 place-items-center border border-border font-mono text-xs font-bold">{available ? String(id).padStart(2, "0") : <LockKeyhole className="size-3.5" />}</span>
            <span className="min-w-0 flex-1"><span className="block truncate text-sm font-bold">{title}</span><span className="block text-xs text-muted-foreground">{current ? "Şu an buradasın" : isFutureContent ? "Yakında" : available ? "Açık" : "Önceki testi geç"}</span></span>
          </button>
        );
      })}
    </nav>
  );
}

function LessonView({ moduleId, progress, updateProgress, onStage }: { moduleId: number; progress: LearningProgress; updateProgress: (fn: (value: LearningProgress) => LearningProgress) => void; onStage: (stage: Stage) => void }) {
  const module = getModule(moduleId);
  const firstIncomplete = Math.max(0, module.sections.findIndex((section) => !progress.completedSections[`m${moduleId}:${section.id}`]));
  const [sectionIndex, setSectionIndex] = useState(firstIncomplete === -1 ? 0 : firstIncomplete);
  const section = module.sections[sectionIndex];
  const completeCount = module.sections.filter((item) => progress.completedSections[`m${moduleId}:${item.id}`]).length;
  const lessonDone = completeCount === module.sections.length;

  useEffect(() => setSectionIndex(Math.max(0, module.sections.findIndex((item) => !progress.completedSections[`m${moduleId}:${item.id}`]))), [moduleId]); // eslint-disable-line react-hooks/exhaustive-deps

  function completeSection() {
    const key = `m${moduleId}:${section.id}`;
    updateProgress((current) => ({ ...current, xp: current.xp + (current.completedSections[key] ? 0 : 20), lastStudyDate: todayKey(), completedSections: { ...current.completedSections, [key]: true } }));
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

      <section className="lesson-card p-5 sm:p-7"><p className="rail-kicker text-primary">{section.eyebrow}</p><p className="mt-4 text-[17px] leading-8 text-muted-foreground">{section.explanation}</p></section>
      {section.id === "variables-types" && <section className="memory-lab mt-5 lesson-card overflow-hidden p-5 sm:p-6"><p className="rail-kicker text-cyan-600 dark:text-cyan-300">Bellekte ne oluyor?</p><div className="mt-5 grid items-center gap-4 sm:grid-cols-[1fr_70px_1fr]"><div className="memory-node p-4"><span className="text-xs text-muted-foreground">İsim alanı</span><code className="mt-2 block text-lg font-black text-cyan-600 dark:text-cyan-300">user_count</code></div><div className="flex items-center justify-center"><span className="memory-arrow" /></div><div className="memory-node p-4"><span className="text-xs text-muted-foreground">int nesnesi</span><strong className="mt-2 block font-mono text-2xl text-amber-500">12</strong></div></div><p className="mt-4 text-sm leading-6 text-muted-foreground">Atama, değeri bir kutuya koymaz. Soldaki ismi sağdaki nesneye bağlar; sonraki modüllerde kopyalama tuzaklarını bu ok üzerinden izleyeceğiz.</p></section>}
      <div className="mt-5"><CodeRunner initialCode={section.code} expectedOutput={section.expectedOutput} /></div>

      <section className="note-grid mt-5 sm:grid-cols-2">
        <div className="note-card lesson-card p-5"><p className="mb-2 flex items-center gap-2 text-xs font-black uppercase tracking-[0.12em] text-primary"><BrainCircuit className="size-4" /> Neden böyle?</p><p className="leading-7 text-muted-foreground">{section.why}</p></div>
        <div className="note-card lesson-card border-amber-400/30 bg-amber-400/[0.04] p-5"><p className="mb-2 flex items-center gap-2 text-xs font-black uppercase tracking-[0.12em] text-amber-500"><Lightbulb className="size-4" /> Alternatifler</p><ul className="space-y-2 text-sm leading-6 text-muted-foreground">{section.alternatives.map((item) => <li key={item} className="flex gap-2"><span className="text-amber-500">•</span>{item}</li>)}</ul></div>
      </section>

      <section className="mt-5 lesson-card border-rose-400/25 p-5 sm:p-6"><p className="mb-3 flex items-center gap-2 text-xs font-black uppercase tracking-[0.12em] text-rose-500"><CircleAlert className="size-4" /> Sık yapılan hatalar / tuzaklar</p><div className="grid gap-3 sm:grid-cols-3">{section.traps.map((trap) => <div key={trap} className="border-l-2 border-primary bg-muted/50 p-3 text-sm leading-6 text-muted-foreground">{trap}</div>)}</div></section>

      <section className="mt-5 lesson-card overflow-hidden"><div className="border-b border-border p-5"><p className="text-xs font-black uppercase tracking-[0.12em] text-emerald-500">Gerçek kodda böyle görünür</p><p className="mt-2 text-sm text-muted-foreground">AI'ın ürettiği bir projede karşılaşabileceğin kısa bir örnek:</p></div><CodeBlock code={section.realCode} label="gercek_kod.py" /><div className="grid gap-2 p-5">{section.lineByLine.map((line, index) => <div key={line} className="flex gap-3 text-sm leading-6 text-muted-foreground"><span className="grid size-6 shrink-0 place-items-center rounded-md bg-primary/10 font-mono text-xs font-bold text-primary">{index + 1}</span>{line}</div>)}</div></section>

      <div className="mt-7 flex flex-col-reverse justify-between gap-3 border-t border-border pt-6 sm:flex-row">
        <Button variant="outline" onClick={() => setSectionIndex(Math.max(0, sectionIndex - 1))} disabled={sectionIndex === 0}>Önceki bölüm</Button>
        {lessonDone && sectionIndex === module.sections.length - 1 ? <Button onClick={() => onStage("practice")} className="font-bold"><Code2 /> Pratiğe geç</Button> : <Button onClick={completeSection} className="font-bold"><Check /> Tamamla ve devam et</Button>}
      </div>
    </div>
  );
}

function QuestionCard({ question, number, total, noHints, sound, onAnswered }: { question: Question; number: number; total: number; noHints: boolean; sound: boolean; onAnswered: (correct: boolean, hints: number) => void }) {
  const [choice, setChoice] = useState("");
  const [fill, setFill] = useState("");
  const [ordered, setOrdered] = useState<string[]>(question.lines ?? []);
  const [hintLevel, setHintLevel] = useState(0);
  const [checked, setChecked] = useState<boolean | null>(null);
  const [codeOutput, setCodeOutput] = useState("");
  const runPython = usePythonRunner();
  const [runningOrder, setRunningOrder] = useState(false);

  useEffect(() => { setChoice(""); setFill(""); setOrdered(question.lines ?? []); setHintLevel(0); setChecked(null); setCodeOutput(""); }, [question.id]);

  const selected = (question.options?.length ?? 0) > 0 ? choice : question.type === "fill" ? fill.trim() : question.type === "order" ? ordered.join("\n") : choice;
  const move = (from: number, direction: -1 | 1) => { const to = from + direction; if (to < 0 || to >= ordered.length) return; const copy = [...ordered]; [copy[from], copy[to]] = [copy[to], copy[from]]; setOrdered(copy); };

  async function checkAnswer() {
    let correct = selected === question.answer;
    if (question.type === "code") correct = codeOutput.trimEnd() === question.expectedOutput;
    if (question.type === "order") {
      setRunningOrder(true);
      const result = await runPython(ordered.join("\n"));
      setRunningOrder(false);
      correct = result.ok && result.output.trimEnd() === question.expectedOutput;
    }
    setChecked(correct); playTone(sound, correct ? "correct" : "wrong"); onAnswered(correct, hintLevel);
  }

  return (
    <div className="mx-auto max-w-3xl animate-in slide-in-from-right-2 duration-300">
      <div className="mb-5 flex items-center justify-between gap-4"><span className="eyebrow-chip">{question.type === "output" ? "Çıktıyı bul" : question.type === "bug" ? "Hatayı bul" : question.type === "fill" ? "Boşluk doldur" : question.type === "order" ? "Kod sıralama" : question.type === "code" ? "Kısa kod yaz" : "Traceback oku"}</span><span className="section-count px-3 py-1.5 font-mono text-sm text-muted-foreground">{number}/{total}</span></div>
      <h2 className="text-2xl font-black tracking-[-0.03em] sm:text-3xl">{question.prompt}</h2>
      {question.code && <div className="mt-5"><CodeBlock code={question.code} label="soru.py" /></div>}
      {question.type === "code" && <div className="mt-5"><CodeRunner initialCode={question.starterCode ?? ""} expectedOutput={noHints ? undefined : question.expectedOutput} compact onRun={(result) => setCodeOutput(result.ok ? result.output : "")} /></div>}
      {question.type === "fill" && <label className="mt-5 block"><span className="mb-2 block text-sm font-bold">Cevabın</span><input value={fill} onChange={(event) => setFill(event.target.value)} disabled={checked !== null} className="h-12 w-full border-2 border-input bg-card px-4 font-mono outline-none ring-primary/30 focus:ring-4" placeholder="Boşluğa gelecek ifadeyi yaz" /></label>}
      {(question.options ?? []).length > 0 && <div className="mt-5 grid gap-3 sm:grid-cols-2">{question.options!.map((option) => <button key={option} disabled={checked !== null} onClick={() => setChoice(option)} className={`answer-option ${choice === option ? "answer-option-selected" : ""}`}>{option}</button>)}</div>}
      {question.type === "order" && <div className="mt-5 space-y-2">{ordered.map((line, index) => <div key={`${line}-${index}`} draggable onDragStart={(event) => event.dataTransfer.setData("text/plain", String(index))} onDragOver={(event) => event.preventDefault()} onDrop={(event) => { const from = Number(event.dataTransfer.getData("text/plain")); const copy = [...ordered]; const [item] = copy.splice(from, 1); copy.splice(index, 0, item); setOrdered(copy); }} className="flex items-center gap-2 border-2 border-border bg-card p-3 font-mono text-sm"><span className="grid size-7 place-items-center border border-border bg-muted text-xs text-muted-foreground">{index + 1}</span><code className="min-w-0 flex-1 whitespace-pre-wrap">{line}</code><Button size="icon-sm" variant="ghost" onClick={() => move(index, -1)} aria-label="Yukarı taşı"><MoveUp /></Button><Button size="icon-sm" variant="ghost" onClick={() => move(index, 1)} aria-label="Aşağı taşı"><MoveDown /></Button></div>)}</div>}

      {!noHints && checked === null && <div className="mt-5 border-2 border-amber-400/40 bg-amber-400/[0.06] p-4">{hintLevel > 0 && <p className="mb-3 text-sm leading-6 text-muted-foreground">{hintLevel <= 2 ? question.hints[hintLevel - 1] : <><strong>Çözüm:</strong> <code className="inline-code">{question.answer}</code></>}</p>}<Button variant="outline" size="sm" onClick={() => setHintLevel(Math.min(3, hintLevel + 1))} disabled={hintLevel === 3}><HelpCircle /> {hintLevel === 0 ? "1. ipucu" : hintLevel === 1 ? "2. ipucu" : hintLevel === 2 ? "Çözümü göster" : "Çözüm gösterildi"}</Button></div>}

      {checked !== null && <div className={`mt-5 border-2 p-5 ${checked ? "border-emerald-500/50 bg-emerald-500/[0.08]" : "border-rose-500/50 bg-rose-500/[0.08]"}`}><p className={`flex items-center gap-2 font-black ${checked ? "text-emerald-500" : "text-rose-500"}`}>{checked ? <CheckCircle2 /> : <XCircle />}{checked ? "Doğru — mantığı yakaladın." : "Henüz değil — nedenine bakalım."}</p><p className="mt-2 leading-7 text-muted-foreground">{question.explanation}</p>{!checked && <p className="mt-2 text-sm"><strong>Doğru cevap:</strong> <code className="inline-code">{question.answer}</code></p>}</div>}

      {checked === null && <Button onClick={checkAnswer} disabled={runningOrder || (question.type !== "code" && !selected)} className="mt-6 w-full font-bold sm:w-auto">{runningOrder ? "Kod çalışıyor" : "Cevabı kontrol et"}</Button>}
    </div>
  );
}

function QuizView({ moduleId, mode, progress, updateProgress, onStage, weakOnly = false }: { moduleId: number; mode: "practice" | "test"; progress: LearningProgress; updateProgress: (fn: (value: LearningProgress) => LearningProgress) => void; onStage: (stage: Stage) => void; weakOnly?: boolean }) {
  const module = getModule(moduleId);
  const [testStarted, setTestStarted] = useState(mode === "practice");
  const [timed, setTimed] = useState(false);
  const [timeLeft, setTimeLeft] = useState(25 * 60);
  const [seed, setSeed] = useState(() => Date.now() & 0xffffffff);
  const questions = useMemo(() => {
    if (mode === "test") return seededTestQuestions(module, seed, 18);
    if (!weakOnly) return getPracticeQuestions(module);
    return [...module.questions].sort((a, b) => {
      const aResult = progress.questionResults[a.id] ?? { correct: 0, wrong: 1 };
      const bResult = progress.questionResults[b.id] ?? { correct: 0, wrong: 1 };
      return (aResult.correct / Math.max(1, aResult.correct + aResult.wrong)) - (bResult.correct / Math.max(1, bResult.correct + bResult.wrong));
    }).slice(0, 15);
  }, [mode, module, seed, weakOnly, progress.questionResults]);
  const [index, setIndex] = useState(0);
  const [answered, setAnswered] = useState(false);
  const [results, setResults] = useState<Array<{ question: Question; correct: boolean; hints: number }>>([]);
  const finished = index >= questions.length;

  useEffect(() => { setTestStarted(mode === "practice"); setIndex(0); setAnswered(false); setResults([]); setTimeLeft(25 * 60); setSeed(Date.now() & 0xffffffff); }, [moduleId, mode]);
  useEffect(() => { if (!timed || !testStarted || finished) return; const timer = window.setInterval(() => setTimeLeft((value) => { if (value <= 1) { window.clearInterval(timer); setIndex(questions.length); return 0; } return value - 1; }), 1000); return () => window.clearInterval(timer); }, [timed, testStarted, finished, questions.length]);

  const score = Math.round((results.filter((item) => item.correct).length / Math.max(1, questions.length)) * 100);

  const recordAnswer = useCallback((correct: boolean, hints: number) => {
    if (answered) return;
    const question = questions[index];
    setAnswered(true);
    setResults((current) => [...current, { question, correct, hints }]);
    updateProgress((current) => {
      const old = current.questionResults[question.id] ?? { correct: 0, wrong: 0 };
      return { ...current, xp: current.xp + (correct ? Math.max(2, 10 - hints * 2) : 1), hintUsage: { ...current.hintUsage, [question.id]: (current.hintUsage[question.id] ?? 0) + hints }, questionResults: { ...current.questionResults, [question.id]: { correct: old.correct + (correct ? 1 : 0), wrong: old.wrong + (correct ? 0 : 1) } } };
    });
  }, [answered, index, questions, updateProgress]);

  function finishOrNext() {
    setAnswered(false);
    setIndex((value) => value + 1);
    if (index === questions.length - 1) {
      const finalResults = results;
      const finalScore = Math.round((finalResults.filter((item) => item.correct).length / questions.length) * 100);
      const weakTopics = Array.from(new Set(finalResults.filter((item) => !item.correct).map((item) => item.question.topic)));
      updateProgress((current) => {
        if (mode === "practice") return { ...current, completedPractice: { ...current.completedPractice, [`m${moduleId}`]: true }, xp: current.xp + 40 };
        const attempt: TestAttempt = { moduleId, score: finalScore, date: new Date().toISOString(), weakTopics };
        return { ...current, attempts: [...current.attempts, attempt], unlockedModule: finalScore >= 70 ? Math.max(current.unlockedModule, Math.min(18, moduleId + 1)) : current.unlockedModule, xp: current.xp + (finalScore >= 70 ? 100 : 20) };
      });
      if (mode === "test" && finalScore >= 70) playTone(progress.sound, "pass");
    }
  }

  if (mode === "test" && !testStarted) return (
    <div className="mx-auto max-w-2xl pt-6 text-center"><div className="mx-auto grid size-16 place-items-center border-2 border-foreground bg-primary/10 text-primary shadow-[5px_5px_0_var(--shadow-ink)]"><Trophy className="size-8" /></div><p className="rail-kicker mx-auto mt-5 w-fit text-primary">Modül {moduleId} bitiriş testi</p><h1 className="mt-3 text-3xl font-black tracking-[-0.04em]">18 soru · geçme notu %70</h1><p className="mx-auto mt-3 max-w-xl leading-7 text-muted-foreground">İpucu yok. Sorular 40 soruluk havuzdan seçilir; Modül 2 testinin yaklaşık %20'si önceki modülden gelir.</p><label className="mx-auto mt-6 flex w-fit items-center gap-3 border-2 border-border bg-card px-4 py-3 text-sm font-bold"><Switch checked={timed} onCheckedChange={setTimed} /> 25 dakikalık süreyi aç</label><Button size="lg" className="mt-6 font-bold" onClick={() => setTestStarted(true)}><Play className="fill-current" /> Testi başlat</Button></div>
  );

  if (finished) {
    const passed = mode === "practice" || score >= 70;
    const weakTopics = Array.from(new Set(results.filter((item) => !item.correct).map((item) => item.question.topic)));
    return (
      <div className="confetti-zone mx-auto max-w-2xl pt-6 text-center">{passed && mode === "test" && Array.from({ length: 22 }, (_, i) => <span key={i} className="confetti" style={{ left: `${(i * 47) % 100}%`, animationDelay: `${(i % 8) * 0.08}s`, background: ["#2536e8", "#ffd947", "#00a77b", "#ee4b2b"][i % 4] }} />)}<div className={`mx-auto grid size-20 place-items-center border-2 border-foreground ${passed ? "bg-emerald-500/15 text-emerald-500" : "bg-rose-500/15 text-rose-500"}`}>{passed ? <Trophy className="size-10" /> : <BrainCircuit className="size-10" />}</div><h1 className="mt-5 text-4xl font-black tracking-[-0.05em]">{mode === "practice" ? "Pratik tamamlandı" : passed ? "Testi geçtin!" : "Bir tur daha güçlenelim"}</h1><p className="mt-3 text-lg text-muted-foreground">Başarı oranın <strong className="text-foreground">%{score}</strong></p><Progress value={score} className="mx-auto mt-5 h-3 max-w-sm" />{weakTopics.length > 0 && <div className="mx-auto mt-6 max-w-lg border-2 border-amber-400/40 bg-amber-400/[0.05] p-5 text-left"><p className="text-sm font-black text-amber-500">Tekrar etmen iyi olacak</p><div className="mt-3 flex flex-wrap gap-2">{weakTopics.map((topic) => <button key={topic} onClick={() => onStage("lesson")} className="border border-border bg-card px-3 py-1.5 text-sm font-bold">{topic} · derse dön</button>)}</div></div>}<div className="mt-7 flex flex-wrap justify-center gap-3">{mode === "practice" ? <Button onClick={() => onStage("test")} className="font-bold"><Trophy /> Bitiriş testine geç</Button> : passed && moduleId < 2 ? <Button onClick={() => window.dispatchEvent(new CustomEvent("python-iz-open", { detail: { moduleId: moduleId + 1, stage: "lesson" } }))} className="font-bold"><Sparkles /> Sonraki modüle geç</Button> : <Button onClick={() => { setSeed(Date.now() & 0xffffffff); setIndex(0); setResults([]); setAnswered(false); setTestStarted(false); }} variant="outline"><RotateCcw /> Yeniden dene</Button>}<Button variant="outline" onClick={() => onStage("stats")}><BarChart3 /> İstatistikler</Button></div></div>
    );
  }

  const question = questions[index];
  return (
    <div><div className="mx-auto mb-7 flex max-w-3xl items-center gap-4"><Progress value={(index / questions.length) * 100} className="h-2 flex-1" />{timed && mode === "test" && <span className="section-count px-3 py-1.5 font-mono text-sm font-bold">{String(Math.floor(timeLeft / 60)).padStart(2, "0")}:{String(timeLeft % 60).padStart(2, "0")}</span>}</div><QuestionCard key={question.id} question={question} number={index + 1} total={questions.length} noHints={mode === "test"} sound={progress.sound} onAnswered={recordAnswer} />{answered && <div className="mx-auto mt-5 flex max-w-3xl justify-end"><Button onClick={finishOrNext} className="font-bold">{index === questions.length - 1 ? "Sonucu gör" : "Sonraki soru"}</Button></div>}</div>
  );
}

function StatsView({ progress, onReview }: { progress: LearningProgress; onReview: () => void }) {
  const allQuestions = learningModules.flatMap((module) => module.questions);
  const topicStats = new Map<string, { correct: number; wrong: number; hints: number }>();
  allQuestions.forEach((question) => { const result = progress.questionResults[question.id] ?? { correct: 0, wrong: 0 }; const current = topicStats.get(question.topic) ?? { correct: 0, wrong: 0, hints: 0 }; topicStats.set(question.topic, { correct: current.correct + result.correct, wrong: current.wrong + result.wrong, hints: current.hints + (progress.hintUsage[question.id] ?? 0) }); });
  const rows = [...topicStats.entries()].filter(([, value]) => value.correct + value.wrong > 0).sort((a, b) => (a[1].correct / Math.max(1, a[1].correct + a[1].wrong)) - (b[1].correct / Math.max(1, b[1].correct + b[1].wrong)));
  const totalCorrect = Object.values(progress.questionResults).reduce((sum, item) => sum + item.correct, 0);
  const totalWrong = Object.values(progress.questionResults).reduce((sum, item) => sum + item.wrong, 0);
  const rate = Math.round((totalCorrect / Math.max(1, totalCorrect + totalWrong)) * 100);
  return (
    <div className="mx-auto max-w-5xl"><p className="rail-kicker text-primary">Öğrenme raporun</p><h1 className="brand-word mt-3 text-4xl font-black tracking-[-0.05em] sm:text-5xl">İSTATİSTİKLER</h1><div className="mt-7 grid gap-4 sm:grid-cols-3"><div className="metric-card"><span>Genel başarı</span><strong>%{rate}</strong><Progress value={rate} className="mt-3" /></div><div className="metric-card"><span>Toplam XP</span><strong>{progress.xp}</strong><p>{totalCorrect + totalWrong} soru yanıtlandı</p></div><div className="metric-card"><span>İpucu kullanımı</span><strong>{Object.values(progress.hintUsage).reduce((a, b) => a + b, 0)}</strong><p>öğrenme desteği</p></div></div><div className="mt-5 grid gap-5 lg:grid-cols-[1fr_320px]"><section className="lesson-card p-5 sm:p-6"><div className="flex items-center justify-between"><h2 className="text-lg font-black">Konu bazında başarı</h2><span className="text-xs text-muted-foreground">Zayıftan güçlüye</span></div>{rows.length === 0 ? <div className="py-12 text-center text-muted-foreground"><BrainCircuit className="mx-auto mb-3 size-8" />Soruları çözdükçe konu haritan burada oluşacak.</div> : <div className="mt-5 space-y-4">{rows.map(([topic, value]) => { const topicRate = Math.round(value.correct / Math.max(1, value.correct + value.wrong) * 100); return <div key={topic}><div className="mb-2 flex justify-between text-sm"><strong className="capitalize">{topic}</strong><span className="font-mono text-muted-foreground">%{topicRate}</span></div><Progress value={topicRate} /></div>; })}</div>}</section><aside className="lesson-card p-5 sm:p-6"><Trophy className="size-6 text-amber-400" /><h2 className="mt-4 text-lg font-black">Test geçmişi</h2>{progress.attempts.length === 0 ? <p className="mt-2 text-sm leading-6 text-muted-foreground">İlk bitiriş testinden sonra sonuçların burada görünür.</p> : <div className="mt-4 space-y-3">{[...progress.attempts].reverse().slice(0, 5).map((attempt, index) => <div key={`${attempt.date}-${index}`} className="flex items-center justify-between border-l-2 border-primary bg-muted p-3 text-sm"><span>Modül {attempt.moduleId}</span><strong className={attempt.score >= 70 ? "text-emerald-500" : "text-rose-500"}>%{attempt.score}</strong></div>)}</div>}<Button className="mt-5 w-full" onClick={onReview} disabled={rows.length === 0}><BrainCircuit /> Zayıf konulardan test</Button></aside></div></div>
  );
}

export function LearningApp() {
  const [progress, setProgress] = useState<LearningProgress>(defaultProgress);
  const [hydrated, setHydrated] = useState(false);
  const [moduleId, setModuleId] = useState(1);
  const [stage, setStage] = useState<Stage>("lesson");
  const [weakOnly, setWeakOnly] = useState(false);
  const module = getModule(moduleId);
  const completed = module.sections.filter((section) => progress.completedSections[`m${moduleId}:${section.id}`]).length;
  const lessonDone = completed === module.sections.length;
  const practiceDone = progress.completedPractice[`m${moduleId}`] === true;

  const updateProgress = useCallback((fn: (value: LearningProgress) => LearningProgress) => setProgress((current) => { const next = fn(current); progressRepository.save(next); return next; }), []);

  useEffect(() => { const stored = progressRepository.load(); setProgress(stored); document.documentElement.classList.toggle("dark", stored.theme === "dark"); setHydrated(true); }, []);
  useEffect(() => {
    const handler = (event: Event) => { const detail = (event as CustomEvent<{ moduleId: number; stage: Stage }>).detail; if (!detail || detail.moduleId > progress.unlockedModule || detail.moduleId > 2) return; setModuleId(detail.moduleId); setStage(detail.stage); window.scrollTo({ top: 0, behavior: "smooth" }); };
    window.addEventListener("python-iz-open", handler); return () => window.removeEventListener("python-iz-open", handler);
  }, [progress.unlockedModule]);
  useEffect(() => {
    const documentWithContext = document as Document & { modelContext?: { registerTool: (tool: unknown, options?: { signal?: AbortSignal }) => void | Promise<void> } };
    const context = documentWithContext.modelContext; if (!context?.registerTool) return;
    const lifecycle = new AbortController();
    void Promise.resolve(context.registerTool({ name: "get_learning_progress", title: "Öğrenme ilerlemesini getir", description: "Python İz içindeki XP, açık modül ve test geçmişini okur.", inputSchema: { type: "object", properties: {}, additionalProperties: false }, annotations: { readOnlyHint: true, untrustedContentHint: false }, execute: () => { const value = progressRepository.load(); return { xp: value.xp, unlockedModule: value.unlockedModule, attempts: value.attempts.length }; } }, { signal: lifecycle.signal })).catch(() => undefined);
    void Promise.resolve(context.registerTool({ name: "open_learning_stage", title: "Öğrenme aşamasını aç", description: "Açık bir modülün ders, pratik, test veya istatistik görünümünü açar.", inputSchema: { type: "object", properties: { moduleId: { type: "integer", minimum: 1, maximum: 2 }, stage: { type: "string", enum: ["lesson", "practice", "test", "stats"] } }, required: ["moduleId", "stage"], additionalProperties: false }, annotations: { readOnlyHint: false, untrustedContentHint: false }, execute: (input: unknown) => { const parsed = input as { moduleId: number; stage: Stage }; const current = progressRepository.load(); if (parsed.moduleId > current.unlockedModule) throw new Error("Bu modül henüz kilitli."); window.dispatchEvent(new CustomEvent("python-iz-open", { detail: parsed })); return { opened: true, ...parsed }; } }, { signal: lifecycle.signal })).catch(() => undefined);
    return () => lifecycle.abort();
  }, []);

  function changeModule(id: number) { setModuleId(id); setStage("lesson"); setWeakOnly(false); window.scrollTo({ top: 0, behavior: "smooth" }); }
  function changeStage(next: Stage) { if (next === "practice" && !lessonDone) return; if (next === "test" && !practiceDone) return; setWeakOnly(false); setStage(next); window.scrollTo({ top: 0, behavior: "smooth" }); }
  function toggleTheme() { updateProgress((current) => { const theme = current.theme === "dark" ? "light" : "dark"; document.documentElement.classList.toggle("dark", theme === "dark"); return { ...current, theme }; }); }

  if (!hydrated) return <div className="grid min-h-screen place-items-center bg-background"><div className="flex items-center gap-3 font-mono text-sm font-bold uppercase tracking-[0.12em] text-muted-foreground"><span className="size-3 animate-pulse border border-foreground bg-primary" /> Öğrenme alanın hazırlanıyor</div></div>;

  return (
    <main className="app-shell min-h-screen bg-background text-foreground">
      <header className="app-header sticky top-0 z-40 backdrop-blur-xl"><div className="mx-auto flex h-[72px] max-w-[1580px] items-center gap-3 px-4 sm:px-6"><Sheet><SheetTrigger asChild><Button variant="ghost" size="icon" className="lg:hidden" aria-label="Modülleri aç"><Menu /></Button></SheetTrigger><SheetContent side="left" className="w-[88%] overflow-y-auto p-0"><SheetHeader className="border-b-2 border-border p-5 text-left"><SheetTitle className="brand-word">ÖĞRENME YOLU</SheetTitle><SheetDescription>18 modül · ilk iki modül hazır</SheetDescription></SheetHeader><div className="p-4"><ModuleNavigation activeModule={moduleId} progress={progress} onSelect={changeModule} /><SheetClose asChild><Button variant="outline" className="mt-4 w-full" onClick={() => setStage("stats")}><BarChart3 /> İstatistikler</Button></SheetClose></div></SheetContent></Sheet><button onClick={() => { setStage("lesson"); setModuleId(1); setWeakOnly(false); }} className="flex items-center gap-3 text-left"><span className="brand-mark font-mono text-sm">&gt;_</span><span className="hidden sm:block"><span className="brand-word block text-[17px] font-black">PYTHON İZ</span><span className="block font-mono text-[10px] uppercase tracking-[0.08em] text-muted-foreground">Kodu takip et. Mantığı yakala.</span></span></button><span className="ml-3 hidden border-l-2 border-foreground pl-3 font-mono text-[10px] font-bold uppercase tracking-[0.12em] text-muted-foreground lg:block">Etkileşimli Python Lab<br />Sürüm / 01</span><div className="ml-auto flex items-center gap-1.5 sm:gap-3"><div className="utility-stat hidden items-center gap-2 px-3 py-1.5 text-sm md:flex"><Flame className="size-4 text-orange-500" /> <strong>{progress.streak} gün</strong></div><div className="utility-stat flex items-center gap-2 px-3 py-1.5 text-sm"><Sparkles className="size-4 text-amber-500" /> <strong>{progress.xp} XP</strong></div><Button variant="ghost" size="icon" onClick={() => updateProgress((current) => ({ ...current, sound: !current.sound }))} aria-label={progress.sound ? "Sesi kapat" : "Sesi aç"}>{progress.sound ? <Volume2 /> : <VolumeX />}</Button><Button variant="ghost" size="icon" onClick={toggleTheme} aria-label="Temayı değiştir">{progress.theme === "dark" ? <Sun /> : <Moon />}</Button></div></div></header>

      <div className="mx-auto grid max-w-[1580px] grid-cols-1 lg:grid-cols-[265px_minmax(0,1fr)] xl:grid-cols-[265px_minmax(0,1fr)_300px]">
        <aside className="curriculum-rail hidden min-h-[calc(100vh-72px)] px-4 py-7 lg:block"><p className="rail-kicker mb-5 px-2 text-muted-foreground">Öğrenme yolu</p><div className="max-h-[calc(100vh-145px)] overflow-y-auto pr-1 scrollbar-thin"><ModuleNavigation activeModule={moduleId} progress={progress} onSelect={changeModule} /></div></aside>

        <section className="learning-canvas min-w-0 px-4 py-6 sm:px-7 lg:px-10 lg:py-9">
          {stage !== "stats" && <Tabs value={stage} onValueChange={(value) => changeStage(value as Stage)} className="stage-switcher mx-auto mb-9 max-w-3xl"><TabsList className="grid w-full grid-cols-3"><TabsTrigger value="lesson"><BookOpen /> Ders</TabsTrigger><TabsTrigger value="practice" disabled={!lessonDone}><Code2 /> Pratik {!lessonDone && <LockKeyhole className="size-3" />}</TabsTrigger><TabsTrigger value="test" disabled={!practiceDone}><ListChecks /> Test {!practiceDone && <LockKeyhole className="size-3" />}</TabsTrigger></TabsList></Tabs>}
          {stage === "lesson" && <LessonView moduleId={moduleId} progress={progress} updateProgress={updateProgress} onStage={changeStage} />}
          {(stage === "practice" || stage === "test") && <QuizView moduleId={moduleId} mode={stage} progress={progress} updateProgress={updateProgress} onStage={changeStage} weakOnly={weakOnly} />}
          {stage === "stats" && <StatsView progress={progress} onReview={() => { const weakestModule = progress.unlockedModule >= 2 ? 2 : 1; setModuleId(weakestModule); setWeakOnly(true); setStage("practice"); }} />}
        </section>

        <aside className="progress-rail hidden min-h-[calc(100vh-72px)] px-5 py-7 xl:block"><div className="flex items-center justify-between"><p className="rail-kicker text-muted-foreground">İlerlemen</p><Button variant="ghost" size="icon-sm" onClick={() => setStage("stats")} aria-label="İstatistikleri aç"><BarChart3 /></Button></div><div className="lesson-card mt-4 p-5"><div className="flex items-center justify-between"><strong className="text-sm">Modül {moduleId}</strong><span className="font-mono text-xs text-primary">%{Math.round((completed / module.sections.length) * 100)}</span></div><Progress value={(completed / module.sections.length) * 100} className="mt-3 h-2" /><div className="mt-5 space-y-3 text-sm">{module.sections.slice(0, 5).map((section, index) => { const done = progress.completedSections[`m${moduleId}:${section.id}`]; return <button key={section.id} onClick={() => setStage("lesson")} className={`flex w-full items-center gap-3 text-left ${done ? "text-foreground" : "text-muted-foreground"}`}><span className={`grid size-6 shrink-0 place-items-center border ${done ? "border-emerald-500 bg-emerald-500/15 text-emerald-500" : "border-border"}`}>{done ? <Check className="size-3.5" /> : index + 1}</span><span className="truncate">{section.title}</span></button>; })}</div></div><div className="lesson-card mt-4 p-5"><Trophy className="size-5 text-amber-500" /><strong className="mt-3 block text-sm">Sıradaki hedef</strong><p className="mt-1 text-sm leading-6 text-muted-foreground">{lessonDone ? practiceDone ? "Bitiriş testinde %70'e ulaş." : "15 pratik sorusunu tamamla." : `${module.sections.length - completed} ders bölümü kaldı.`}</p><Progress value={lessonDone ? practiceDone ? 85 : 65 : (completed / module.sections.length) * 60} className="mt-3 h-1.5" /></div><Button variant="outline" className="mt-4 w-full" onClick={() => setStage("stats")}><BarChart3 /> İstatistikler</Button></aside>
      </div>
    </main>
  );
}

