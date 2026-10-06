"use client";
import { useMemo, useRef, useState } from "react";
import { Copy, Download, Link2, Upload } from "lucide-react";
import { Button } from "@/components/ui/button";
import type { LearningProgress } from "@/lib/learning-types";
import { decodeTransfer, encodeTransfer, exportProgress, importProgress, mergeProgress, parseProgress, progressRepository, studyDay } from "@/lib/progress-repository";
import { expireQuiz } from "@/lib/quiz-engine";

export type IncomingProgress = { progress: LearningProgress; source: string };

function download(text: string, name: string) {
  const url = URL.createObjectURL(new Blob([text], { type: "application/json" }));
  const link = document.createElement("a"); link.href = url; link.download = name;
  document.body.appendChild(link); link.click(); link.remove();
  window.setTimeout(() => URL.revokeObjectURL(url), 1000);
}
function summary(value: LearningProgress) {
  const sections = Object.values(value.completedSections).filter(Boolean).length;
  return `${value.xp} XP · ${sections} bölüm · ${value.attempts.length} test · ${Object.keys(value.writingDrafts).length} kod taslağı`;
}
export function ProgressBackup({ progress, onRestore, onBackup, incoming, incomingError, onIncomingHandled }: {
  progress: LearningProgress; onRestore: (progress: LearningProgress) => void; onBackup: () => void;
  incoming?: IncomingProgress | null; incomingError?: string; onIncomingHandled?: () => void;
}) {
  const [candidate, setCandidate] = useState<IncomingProgress | null>(incoming ?? null);
  const [message, setMessage] = useState(incomingError ?? "");
  const [busy, setBusy] = useState(false);
  const [code, setCode] = useState("");
  const [pasted, setPasted] = useState("");
  const [now] = useState(() => Date.now());
  const readId = useRef(0);
  // What the student would end up with if they merge; computed once per candidate, never saved.
  const merged = useMemo(() => {
    if (!candidate) return null;
    try { return mergeProgress(progress, candidate.progress); } catch { return null; }
  }, [candidate, progress]);

  async function inspect(read: () => Promise<LearningProgress>, source: string, failure: string) {
    const id = ++readId.current;
    setCandidate(null); setMessage(""); setBusy(true);
    try {
      const parsed = await read();
      if (id === readId.current) setCandidate({ progress: parsed, source });
    } catch (error) {
      if (id === readId.current) setMessage(`${failure}${error instanceof Error && error.message ? ` Neden: ${error.message.replace(/\.$/, "")}.` : ""} Mevcut ilerlemen değiştirilmedi.`);
    } finally { if (id === readId.current) setBusy(false); }
  }
  function choose(file?: File) {
    if (!file) { ++readId.current; setCandidate(null); setMessage(""); return; }
    void inspect(async () => {
      if (file.size > 5 * 1024 * 1024) throw new Error("Dosya 5 MB sınırını aşıyor.");
      return importProgress(await file.text());
    }, `Dosya: ${file.name}`, "Yedek okunamadı: dosya bozuk veya uyumsuz.");
  }
  function apply(next: LearningProgress, done: string) {
    try {
      const saved = progressRepository.restore(expireQuiz(next));
      onRestore(saved); setCandidate(null); setPasted(""); onIncomingHandled?.();
      setMessage(`${done} Önceki yerel kaydın kurtarma kopyası bu tarayıcıda tutuluyor.`);
    } catch { setMessage("Uygulanamadı; mevcut ilerleme değiştirilmedi. Tarayıcı depolama alanını kontrol et."); }
  }
  async function makeCode() {
    setBusy(true); setMessage("");
    try { setCode(await encodeTransfer(progress)); onBackup(); }
    catch { setMessage("Aktarım kodu oluşturulamadı. Yedek dosyası indirmeyi dene."); }
    finally { setBusy(false); }
  }
  async function copy(text: string, what: string) {
    try { await navigator.clipboard.writeText(text); setMessage(`${what} panoya kopyalandı.`); }
    catch { setMessage("Otomatik kopyalanamadı; kutudaki metni seçip elle kopyala."); }
  }
  const link = code ? `${window.location.origin}${window.location.pathname}#aktar=${code}` : "";
  const days = progress.lastBackupAt ? Math.floor((now - Date.parse(progress.lastBackupAt)) / 86400000) : null;

  return <section className="lesson-card mx-auto mt-6 max-w-5xl p-5 sm:p-6">
    <h2 className="text-xl font-black">İlerleme yedeği ve aktarım</h2>
    <p className="mt-3 leading-7 text-muted-foreground">Dersler, XP, kod taslakları ve son soru oturumu yalnızca bu tarayıcıda saklanır. Tarayıcı verilerini temizlersen, özel pencerede çalışırsan ya da başka bir cihaza geçersen kaybolabilir. Yedek dosyası kodlarını ve cevaplarını içerir; güvendiğin bir yerde tut.</p>
    <p className="mt-3 text-sm font-bold">{days === null ? "Henüz yedek almadın." : `Son yedek / aktarım: ${days <= 0 ? "bugün" : `${days} gün önce`}.`}</p>
    <div className="mt-4 flex flex-wrap gap-3">
      <Button variant="outline" onClick={() => { try { download(exportProgress(progress), "python-iz-yedek-" + studyDay() + ".json"); onBackup(); setMessage("Yedek dosyası indirmeye hazırlandı."); } catch { setMessage("Yedek oluşturulamadı. Kod taslaklarını kopyalayarak koru."); } }}><Download />Yedek indir</Button>
      <Button variant="ghost" onClick={() => { try { const old = progressRepository.previousBackup(); if (!old) { setMessage("Henüz geri yükleme öncesi kurtarma kopyası yok."); return; } download(exportProgress(parseProgress(JSON.parse(old))), "python-iz-geri-yukleme-oncesi.json"); setMessage("Önceki kayıt indirmeye hazırlandı; geri yüklemek için bu dosyayı seçebilirsin."); } catch { setMessage("Kurtarma kaydı okunamadı. Mevcut ilerlemen değiştirilmedi."); } }}>Önceki kaydı indir</Button>
    </div>

    <h3 className="mt-8 font-black">Başka cihaza aktar</h3>
    <ol className="mt-2 list-decimal space-y-1 pl-5 text-sm leading-6 text-muted-foreground">
      <li>Bu cihazda aktarım kodu ya da bağlantı oluştur.</li>
      <li>Diğer cihazda bağlantıyı aç ya da kodu aşağıdaki kutuya yapıştır.</li>
      <li>Gelen ilerleme seninkiyle <strong>birleşir</strong>; iki taraftaki hiçbir şey silinmez.</li>
    </ol>
    <Button className="mt-4" variant="outline" disabled={busy} onClick={() => void makeCode()}>Aktarım kodu oluştur</Button>
    {code && <div className="mt-4">
      <label className="block text-sm font-bold" htmlFor="transfer-code">Aktarım kodun</label>
      <textarea id="transfer-code" readOnly rows={4} value={code} onFocus={event => event.currentTarget.select()} className="mt-2 block w-full border border-border bg-background p-3 font-mono text-xs break-all" />
      <div className="mt-3 flex flex-wrap gap-3">
        <Button variant="outline" onClick={() => void copy(code, "Kod")}><Copy />Kodu kopyala</Button>
        <Button variant="outline" onClick={() => void copy(link, "Bağlantı")}><Link2 />Bağlantıyı kopyala</Button>
      </div>
      <p className="mt-3 text-sm leading-6 text-muted-foreground">Kod ilerlemenin tamamını, kod taslakları dahil, içerir. Yalnızca kendi cihazlarına gönder; herkese açık bir yere yapıştırma. Bağlantı çok uzun geldiğinde (örneğin bir mesajlaşma uygulaması keserse) kodu kullan.</p>
    </div>}
    <label className="mt-6 block font-bold" htmlFor="paste-code">Koddan içe aktar</label>
    <textarea id="paste-code" rows={3} value={pasted} onChange={event => setPasted(event.target.value)} placeholder="PYIZ1.…" className="mt-2 block w-full border border-border bg-background p-3 font-mono text-xs break-all" />
    <Button className="mt-3" variant="outline" disabled={busy || !pasted.trim()} onClick={() => void inspect(() => decodeTransfer(pasted), "Aktarım kodu", "Aktarım kodu okunamadı.")}>Kodu kontrol et</Button>

    <label className="mt-6 block font-bold"><span className="flex items-center gap-2"><Upload className="size-4" />Yedek dosyası seç</span><input type="file" accept="application/json,.json" className="mt-3 block w-full text-sm file:mr-3 file:border file:border-border file:bg-muted file:p-2 file:text-foreground" onChange={event => { choose(event.target.files?.[0]); event.target.value = ""; }} /></label>
    {busy && <p role="status" className="mt-3">Kontrol ediliyor…</p>}
    {candidate && <div className="mt-5 border-2 border-amber-500/50 p-4">
      <h3 className="font-black">Uygulamadan önce kontrol et</h3>
      <p className="mt-2 break-words text-sm">Kaynak: {candidate.source}</p>
      <p className="mt-2 text-sm">Şu an bu cihazda: {summary(progress)}</p>
      <p className="mt-1 text-sm">Gelen: {summary(candidate.progress)}</p>
      {merged && <p className="mt-1 text-sm font-bold">Birleşince: {summary(merged)}</p>}
      <p className="mt-3 leading-6 text-sm">Birleştirmek önerilir: ikisinde de tamamlanan her şey korunur. XP ve soru sayaçları toplanmaz, büyük olan alınır; böylece aynı çalışma iki kez sayılmaz. Tema ve devam eden sınav bu cihazdakiyle kalır. &quot;Yerine koy&quot; ise bu cihazdaki ilerlemeyi gelenle değiştirir. İkisinde de önceki yerel kayıt için kurtarma kopyası saklanır.</p>
      <div className="mt-4 flex flex-wrap gap-3">
        <Button disabled={!merged} onClick={() => merged && apply(merged, "İlerlemeler birleştirildi.")}>Birleştir (önerilir)</Button>
        <Button variant="outline" onClick={() => apply(candidate.progress, "İlerleme gelenle değiştirildi.")}>Yerine koy</Button>
        <Button variant="ghost" onClick={() => { setCandidate(null); setMessage("İptal edildi; ilerlemen değişmedi."); onIncomingHandled?.(); }}>Vazgeç</Button>
      </div>
    </div>}
    {message && <p role="status" className="mt-4 text-sm leading-6">{message}</p>}
  </section>;
}
