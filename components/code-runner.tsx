"use client";
import { useCallback, useEffect, useRef, useState } from "react";
import CodeMirror from "@uiw/react-codemirror";
import { python } from "@codemirror/lang-python";
import { LoaderCircle, Play, RotateCcw } from "lucide-react";
import { Button } from "@/components/ui/button";
import type { CodeTest } from "@/lib/learning-types";

export type RunResult = {
  ok: boolean; output: string; version?: string | null;
  cases?: (CodeTest & { ok: boolean; output: string; passed: boolean })[];
};
type RunOptions = { stdin?: string; tests?: CodeTest[] };

export function usePythonRunner() {
  const workerRef = useRef<Worker | null>(null);
  const active = useRef<{ id: string; resolve: (value: RunResult) => void; timeout: ReturnType<typeof setTimeout> } | null>(null);
  const queue = useRef(Promise.resolve());
  const mounted = useRef(true);
  const reset = useCallback((message: string) => {
    workerRef.current?.terminate(); workerRef.current = null;
    if (active.current) {
      clearTimeout(active.current.timeout);
      active.current.resolve({ ok: false, output: message });
      active.current = null;
    }
  }, []);
  useEffect(() => { mounted.current = true; return () => { mounted.current = false; reset("Çalışma iptal edildi."); }; }, [reset]);

  return useCallback((code: string, options: RunOptions = {}) => {
    const job = queue.current.then(() => new Promise<RunResult>((resolve) => {
      if (!mounted.current) { resolve({ ok: false, output: "Çalışma iptal edildi." }); return; }
      const id = crypto.randomUUID();
      try {
        if (!workerRef.current) {
          const worker = new Worker("/py-worker.js");
          worker.onmessage = ({ data }) => {
            const pending = active.current;
            if (!pending || pending.id !== data.id) return;
            clearTimeout(pending.timeout);
            if (data.status === "running") {
              pending.timeout = setTimeout(() => reset("Kodun çalışması 7 saniyeyi aştı. Ortam sıfırlandı; döngülerini kontrol et."), 7000);
            } else { active.current = null; pending.resolve(data); }
          };
          worker.onerror = () => reset("Python başlatılamadı. Bağlantını kontrol edip tekrar dene.");
          workerRef.current = worker;
        }
        active.current = { id, resolve, timeout: setTimeout(() => reset("Python 90 saniyede yüklenemedi. İnternet bağlantını kontrol edip tekrar dene."), 90000) };
        workerRef.current.postMessage({ id, code, ...options });
      } catch { reset("Python ortamı açılamadı."); resolve({ ok: false, output: "Python ortamı açılamadı." }); }
    }));
    queue.current = job.then(() => undefined, () => undefined);
    return job;
  }, [reset]);
}

export function CodeRunner({ initialCode, expectedOutput, compact = false, onRun, onChange, initialInput = "", readOnly = false }: {
  initialCode: string; expectedOutput?: string; compact?: boolean; initialInput?: string; readOnly?: boolean;
  onRun?: (result: RunResult) => void; onChange?: (code: string) => void;
}) {
  const [code, setCode] = useState(initialCode);
  const [stdin, setStdin] = useState(initialInput);
  const [result, setResult] = useState<RunResult | null>(null);
  const [running, setRunning] = useState(false);
  const revision = useRef(0);
  const runPython = usePythonRunner();
  useEffect(() => { revision.current++; setCode(initialCode); setStdin(initialInput); setResult(null); }, [initialCode, initialInput]);
  function edit(value: string) { revision.current++; setCode(value); setResult(null); onChange?.(value); }
  async function execute() {
    const current = revision.current;
    setRunning(true);
    const next = await runPython(code, { stdin });
    if (current === revision.current) { setResult(next); onRun?.(next); }
    setRunning(false);
  }
  return <div className="code-shell overflow-hidden">
    <div className="flex items-center justify-between border-b border-white/10 px-4 py-3">
      <span className="font-mono text-xs text-slate-400">PY / cozum.py</span>
      <Button variant="ghost" size="sm" disabled={running || readOnly} onClick={() => edit(initialCode)} className="text-slate-400"><RotateCcw className="size-3.5" /> Sıfırla</Button>
    </div>
    <CodeMirror value={code} onChange={edit} readOnly={readOnly || running} extensions={[python()]} theme="dark" minHeight={compact ? "140px" : "200px"} basicSetup={{ foldGutter: false }} className="text-[15px]" aria-label="Python kod editörü" />
    <div className="border-t border-white/10 bg-[#060a12] p-4">
      <label className="block text-xs text-slate-400">Program girdisi · her input() için bir satır
        <textarea aria-label="Program girdisi" value={stdin} disabled={running || readOnly} onChange={event => { revision.current++; setStdin(event.target.value); setResult(null); }} rows={2} className="mt-2 block w-full border border-white/20 bg-black/30 p-2 font-mono text-sm text-slate-200" placeholder="Örn. 18" />
      </label>
      <div className="mt-3 flex flex-wrap items-center gap-3">
        <Button onClick={execute} disabled={running || readOnly}>{running ? <LoaderCircle className="size-4 animate-spin" /> : <Play className="size-4" />} {running ? "Hazırlanıyor / çalışıyor" : "Çalıştır"}</Button>
        {expectedOutput !== undefined && <span className="text-xs text-slate-400">Örnek çıktı: <code>{expectedOutput.replace(/\n/g, " ↵ ")}</code></span>}
      </div>
      <div role="status" className={`mt-3 border p-3 font-mono text-sm ${result?.ok ? "border-emerald-500/40 text-emerald-300" : result ? "border-rose-500/40 text-rose-300" : "border-white/10 text-slate-400"}`}>
        <span className="mb-2 block text-[10px]">ÇIKTI {result?.version ? `· Python ${result.version}` : ""}</span>
        <pre className="whitespace-pre-wrap break-words">{result ? result.output || "Tamamlandı; program çıktı üretmedi." : "Çalıştırınca sonuç burada görünecek."}</pre>
      </div>
    </div>
  </div>;
}

