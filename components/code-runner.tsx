"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import CodeMirror from "@uiw/react-codemirror";
import { python } from "@codemirror/lang-python";
import { LoaderCircle, Play, RotateCcw, TerminalSquare } from "lucide-react";
import { Button } from "@/components/ui/button";

type RunResult = { ok: boolean; output: string; version?: string | null };

export function usePythonRunner() {
  const workerRef = useRef<Worker | null>(null);
  const pendingRef = useRef(new Map<string, { resolve: (value: RunResult) => void; timeout: ReturnType<typeof setTimeout> }>());

  const ensureWorker = useCallback(() => {
    if (workerRef.current) return workerRef.current;
    const worker = new Worker("/py-worker.js");
    worker.onmessage = (event) => {
      const pending = pendingRef.current.get(event.data.id);
      if (!pending) return;
      clearTimeout(pending.timeout);
      pending.resolve(event.data);
      pendingRef.current.delete(event.data.id);
    };
    workerRef.current = worker;
    return worker;
  }, []);

  useEffect(() => () => workerRef.current?.terminate(), []);

  const run = useCallback((code: string, timeoutMs = 7000) => new Promise<RunResult>((resolve) => {
    const id = crypto.randomUUID();
    const worker = ensureWorker();
    const timeout = setTimeout(() => {
      worker.terminate();
      workerRef.current = null;
      pendingRef.current.delete(id);
      resolve({ ok: false, output: "Çalışma 7 saniyeyi aştı. Python ortamı güvenle sıfırlandı." });
    }, timeoutMs);
    pendingRef.current.set(id, { resolve, timeout });
    worker.postMessage({ id, code });
  }), [ensureWorker]);

  return run;
}

export function CodeRunner({ initialCode, expectedOutput, compact = false, onRun }: { initialCode: string; expectedOutput?: string; compact?: boolean; onRun?: (result: RunResult) => void }) {
  const [code, setCode] = useState(initialCode);
  const [result, setResult] = useState<RunResult | null>(null);
  const [running, setRunning] = useState(false);
  const runPython = usePythonRunner();

  useEffect(() => { setCode(initialCode); setResult(null); }, [initialCode]);

  async function execute() {
    setRunning(true);
    const next = await runPython(code);
    setResult(next);
    setRunning(false);
    onRun?.(next);
  }

  return (
    <div className="code-shell overflow-hidden">
      <div className="flex items-center justify-between border-b border-white/10 px-4 py-3">
        <div className="flex items-center gap-3 font-mono text-xs text-slate-400"><span className="border border-cyan-300 px-1.5 py-0.5 font-black text-cyan-300">PY</span><span>ornek.py / DÜZENLENEBİLİR</span></div>
        <Button variant="ghost" size="sm" className="text-slate-400 hover:bg-white/10 hover:text-white" onClick={() => { setCode(initialCode); setResult(null); }}><RotateCcw className="size-3.5" /> Sıfırla</Button>
      </div>
      <CodeMirror value={code} onChange={setCode} extensions={[python()]} theme="dark" minHeight={compact ? "120px" : "185px"} basicSetup={{ foldGutter: false, highlightActiveLine: true }} className="text-[15px]" aria-label="Python kod editörü" />
      <div className="border-t border-white/10 bg-[#060a12] p-4">
        <div className="flex flex-wrap items-center gap-3">
          <Button onClick={execute} disabled={running} className="font-bold">{running ? <LoaderCircle className="size-4 animate-spin" /> : <Play className="size-4 fill-current" />} {running ? "Python hazırlanıyor" : "Çalıştır"}</Button>
          {expectedOutput !== undefined && <span className="text-xs text-slate-500">Beklenen çıktı: <code className="text-slate-300">{expectedOutput.replace(/\n/g, " ↵ ")}</code></span>}
        </div>
        <div className={`runtime-output mt-3 min-h-11 border px-4 py-3 font-mono text-sm ${result ? (result.ok ? "border-emerald-500/40 bg-emerald-500/5 text-emerald-300" : "border-rose-500/40 bg-rose-500/5 text-rose-300") : "border-white/10 bg-black/20 text-slate-500"}`}>
          <span className="mb-1 flex items-center gap-2 text-[10px] font-bold tracking-[0.12em] text-slate-500"><TerminalSquare className="size-3.5" /> ÇIKTI {result?.version ? `· Python ${result.version}` : ""}</span>
          <pre className="whitespace-pre-wrap break-words">{result?.output || "Çalıştırınca sonuç burada görünecek."}</pre>
        </div>
      </div>
    </div>
  );
}

