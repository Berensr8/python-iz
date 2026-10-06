"use client";
import { useRef, useState } from "react";
import { Check, Code2, HelpCircle, Play, RotateCcw } from "lucide-react";
import { Button } from "@/components/ui/button";
import { CodeRunner, usePythonRunner, type RunResult } from "@/components/code-runner";
import rawTasks from "@/content/writing-tasks.json";
import type { LearningProgress, WritingTask } from "@/lib/learning-types";
import { recordWriting } from "@/lib/progress-repository";

export const writingTasks = rawTasks as WritingTask[];
type Update = (fn: (progress: LearningProgress) => LearningProgress) => void;

export function WritingLab({ moduleId, progress, updateProgress }: { moduleId: number; progress: LearningProgress; updateProgress: Update }) {
  const tasks = writingTasks.filter(task => task.moduleId === moduleId);
  const [selected, setSelected] = useState(tasks[0].id);
  const task = tasks.find(item => item.id === selected) ?? tasks[0];
  return <div className="mx-auto max-w-3xl">
    <p className="eyebrow-chip"><Code2 className="size-4" /> YAZMA ATÖLYESİ / MODÜL {moduleId}</p>
    <h1 className="mt-4 text-4xl font-black tracking-tight">Bu kez kod senin.</h1>
    <p className="mt-4 leading-7 text-muted-foreground">Önce tamamla, sonra hatayı düzelt, sonunda boş editörden kendi programını kur. Çalıştırmak denemek içindir; görevi bitirmek için bütün kontrol girdilerini geçmelisin.</p>
    <div className="my-6 grid gap-2 sm:grid-cols-3" aria-label="Yazma görevleri">
      {tasks.map((item, i) => <button key={item.id} onClick={() => setSelected(item.id)} className={`answer-option text-left ${item.id === task.id ? "answer-option-selected" : ""}`} aria-pressed={item.id === task.id}>
        <span className="block font-mono text-xs text-primary">0{i + 1} / {item.level}</span>
        <strong className="mt-2 block">{item.title}</strong>
        <span className="mt-2 block text-xs text-muted-foreground">{progress.writingResults[item.id]?.passed ? progress.writingResults[item.id].independent ? "✓ İpucusuz çözüldü" : "✓ Yardımla çözüldü" : "Henüz tamamlanmadı"}</span>
      </button>)}
    </div>
    <WritingExercise key={task.id} task={task} progress={progress} updateProgress={updateProgress} />
  </div>;
}

function WritingExercise({ task, progress, updateProgress }: { task: WritingTask; progress: LearningProgress; updateProgress: Update }) {
  const [initialCode, setInitialCode] = useState(progress.writingDrafts[task.id] ?? task.starterCode);
  const [editorKey, setEditorKey] = useState(0);
  const code = useRef(initialCode);
  const revision = useRef(0);
  const [hint, setHint] = useState(0);
  const [solution, setSolution] = useState(false);
  const [checking, setChecking] = useState(false);
  const busy = useRef(false);
  const [result, setResult] = useState<RunResult | null>(null);
  const run = usePythonRunner();
  function edit(value: string) {
    code.current = value; revision.current++; setResult(null);
    updateProgress(current => ({ ...current, writingDrafts: { ...current.writingDrafts, [task.id]: value } }));
  }
  function help() { updateProgress(current => ({ ...current, writingHelp: { ...current.writingHelp, [task.id]: true } })); }
  async function assess() {
    if (busy.current) return;
    busy.current = true; setChecking(true);
    const submittedRevision = revision.current;
    const next = await run(code.current, { tests: task.tests });
    if (submittedRevision === revision.current) {
      setResult(next);
      // Infrastructure failures are not learning attempts.
      if (next.cases) updateProgress(current => recordWriting(current, task.id, next.ok, !!current.writingHelp[task.id]));
    }
    busy.current = false; setChecking(false);
  }
  return <>
    <section className="lesson-card p-5 sm:p-6">
      <p className="rail-kicker text-primary">Kazanım</p><p className="mt-2 font-bold">{task.objective}</p>
      <h2 className="mt-5 text-xl font-black">Görev / {task.title}</h2><p className="mt-3 leading-7 text-muted-foreground">{task.prompt}</p>
      <div className="mt-4 grid gap-3 sm:grid-cols-2"><div className="border border-border p-3"><span className="text-xs text-muted-foreground">Örnek girdi</span><pre className="mt-2 whitespace-pre-wrap font-mono text-sm">{task.exampleInput}</pre></div><div className="border border-border p-3"><span className="text-xs text-muted-foreground">Beklenen çıktı</span><pre className="mt-2 whitespace-pre-wrap font-mono text-sm">{task.exampleOutput}</pre></div></div>
      <p className="mt-3 text-xs leading-5 text-muted-foreground">Her input() bir satır okur. Otomatik değerlendirmede yalnızca istenen sonucu yazdır; “Sayı gir:” gibi istemler ekleme.</p>
    </section>
    <div className="mt-5"><CodeRunner key={editorKey} initialCode={initialCode} initialInput={task.exampleInput} onChange={edit} readOnly={checking} /></div>
    <div className="mt-3 flex flex-wrap items-center justify-between gap-3"><span className="text-xs text-muted-foreground">Taslak bu tarayıcıda saklanır; cihazlar arasında eşitlenmez.</span><Button variant="ghost" size="sm" disabled={checking} onClick={() => { if (!window.confirm("Bu görevin taslağı başlangıç koduyla değiştirilsin mi?")) return; edit(task.starterCode); setInitialCode(task.starterCode); setEditorKey(value => value + 1); }}><RotateCcw /> Başlangıca dön</Button></div>
    <div className="mt-5 flex flex-wrap gap-3"><Button disabled={checking} onClick={assess}><Play />{checking ? "Kontrol ediliyor…" : "Çözümümü test et"}</Button><Button variant="outline" disabled={checking || hint >= task.hints.length} onClick={() => { help(); setHint(value => value + 1); }}><HelpCircle /> İpucu al</Button><Button variant="ghost" disabled={checking || solution} onClick={() => { help(); setSolution(true); }}>Örnek çözümü göster</Button></div>
    {hint > 0 && <div className="lesson-card mt-4 border-amber-500/40 p-4"><p className="font-bold">İpucu {hint}</p><p className="mt-2 text-sm leading-6">{task.hints[hint - 1]}</p></div>}
    {solution && <section className="lesson-card mt-4 p-4"><h3 className="font-bold">Bir olası çözüm</h3><pre className="mt-3 overflow-auto font-mono text-sm">{task.solution}</pre><p className="mt-3 text-xs text-muted-foreground">Aynı çıktıyı üreten farklı doğru yöntemler de kabul edilir. Çözümü görmek bu görevi “yardımlı” olarak işaretler.</p></section>}
    {result && <section aria-live="polite" className={`lesson-card mt-5 p-5 ${result.ok ? "border-emerald-500/50" : "border-amber-500/50"}`}>
      <h3 className="flex items-center gap-2 font-black">{result.ok && <Check />}{result.cases ? `${result.cases.filter(item => item.passed).length}/${result.cases.length} kontrol geçti` : "Çalışma tamamlanamadı"}</h3>
      <p className="mt-2 text-sm leading-6 text-muted-foreground">{result.ok ? "Çözümün farklı girdilerde çalışıyor. Şimdi her satırın neden gerekli olduğunu kendine açıkla." : result.output || "Bir sınır durumunu kaçırmış olabilirsin. Girdi, beklenen ve kendi çıktını karşılaştırıp yeniden dene."}</p>
      {result.cases?.map((item, index) => <details key={index} className="mt-3 border-t border-border pt-3"><summary className="cursor-pointer text-sm font-bold">{item.passed ? "✓" : "×"} {item.label}</summary><div className="mt-2 grid gap-3 text-xs sm:grid-cols-3">{[["Girdi", item.stdin], ["Beklenen", item.expectedOutput], ["Senin çıktın", item.output]].map(([label, value]) => <div key={label}><strong>{label}</strong><pre className="mt-1 whitespace-pre-wrap break-words font-mono">{value || "(boş çıktı)"}</pre></div>)}</div></details>)}
    </section>}
    <p className="mt-5 text-xs leading-5 text-muted-foreground">Kontroller gönderimden sonra açılır. Tarayıcıda çalışan bu testler öğrenme içindir; gizli veya güvenli bir sınav sistemi değildir. Tüm kontrolleri ilk kez geçmek +30 XP kazandırır.</p>
  </>;
}
