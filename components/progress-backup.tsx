"use client";
import { useRef, useState } from "react";
import { Download, Upload } from "lucide-react";
import { Button } from "@/components/ui/button";
import type { LearningProgress } from "@/lib/learning-types";
import { exportProgress, importProgress, parseProgress, progressRepository, studyDay } from "@/lib/progress-repository";
import { expireQuiz } from "@/lib/quiz-engine";

function download(text: string, name: string) {
  const url = URL.createObjectURL(new Blob([text], { type: "application/json" }));
  const link = document.createElement("a"); link.href = url; link.download = name;
  document.body.appendChild(link); link.click(); link.remove();
  window.setTimeout(() => URL.revokeObjectURL(url), 1000);
}
export function ProgressBackup({ progress, onRestore }: { progress: LearningProgress; onRestore: (progress: LearningProgress) => void }) {
  const [candidate, setCandidate] = useState<LearningProgress | null>(null);
  const [fileName, setFileName] = useState("");
  const [message, setMessage] = useState("");
  const [busy, setBusy] = useState(false);
  const readId = useRef(0);
  async function choose(file?: File) {
    const id = ++readId.current;
    setCandidate(null); setMessage(""); setFileName(file?.name ?? "");
    if (!file) return;
    setBusy(true);
    try {
      if (file.size > 5 * 1024 * 1024) throw new Error("Dosya 5 MB sınırını aşıyor.");
      const parsed = importProgress(await file.text());
      if (id === readId.current) setCandidate(parsed);
    } catch { if (id === readId.current) setMessage("Yedek okunamadı: dosya bozuk, uyumsuz veya 5 MB sınırından büyük. Mevcut ilerlemen değiştirilmedi."); }
    finally { if (id === readId.current) setBusy(false); }
  }
  function restore() {
    if (!candidate) return;
    try {
      const restored = progressRepository.restore(expireQuiz(candidate));
      onRestore(restored); setCandidate(null); setMessage("Yedek geri yüklendi. Önceki yerel kaydın kurtarma kopyası bu tarayıcıda tutuluyor.");
    } catch { setMessage("Geri yüklenemedi; mevcut ilerleme değiştirilmedi. Tarayıcı depolama alanını kontrol et."); }
  }
  return <section className="lesson-card mx-auto mt-6 max-w-5xl p-5 sm:p-6">
    <h2 className="text-xl font-black">İlerleme yedeği</h2>
    <p className="mt-3 leading-7 text-muted-foreground">Dersler, XP, kod taslakları ve son soru oturumu bu tarayıcıda saklanır. Cihaz değiştirmeden veya tarayıcı verilerini temizlemeden önce yedek indir. Dosya kodlarını ve cevaplarını içerir; güvendiğin bir yerde tut.</p>
    <div className="mt-5 flex flex-wrap gap-3">
      <Button variant="outline" onClick={() => { try { download(exportProgress(progress), "python-iz-yedek-" + studyDay() + ".json"); setMessage("Yedek dosyası indirmeye hazırlandı."); } catch { setMessage("Yedek oluşturulamadı. Kod taslaklarını kopyalayarak koru."); } }}><Download />Yedek indir</Button>
      <Button variant="ghost" onClick={() => { try { const old = progressRepository.previousBackup(); if (!old) { setMessage("Henüz geri yükleme öncesi kurtarma kopyası yok."); return; } download(exportProgress(parseProgress(JSON.parse(old))), "python-iz-geri-yukleme-oncesi.json"); setMessage("Önceki kayıt indirmeye hazırlandı; geri yüklemek için bu dosyayı seçebilirsin."); } catch { setMessage("Kurtarma kaydı okunamadı. Mevcut ilerlemen değiştirilmedi."); } }}>Önceki kaydı indir</Button>
    </div>
    <label className="mt-5 block font-bold"><span className="flex items-center gap-2"><Upload className="size-4" />Yedek dosyası seç</span><input type="file" accept="application/json,.json" className="mt-3 block w-full text-sm file:mr-3 file:border file:border-border file:bg-muted file:p-2 file:text-foreground" onChange={event => { void choose(event.target.files?.[0]); event.target.value = ""; }} /></label>
    {busy && <p role="status" className="mt-3">Dosya kontrol ediliyor…</p>}
    {candidate && <div className="mt-5 border-2 border-amber-500/50 p-4">
      <h3 className="font-black">Geri yüklemeden önce kontrol et</h3><p className="mt-2 break-words text-sm">Dosya: {fileName}</p>
      <p className="mt-2 text-sm">Şu an: {progress.xp} XP · {progress.attempts.length} test. Yedek: {candidate.xp} XP · {candidate.attempts.length} test · {Object.keys(candidate.writingDrafts).length} kod taslağı.</p>
      <p className="mt-3 leading-6">Bu işlem mevcut ilerlemenin yerine yedeği koyar; birleştirmez. Önceki yerel kayıt için kurtarma kopyası saklanır. Yedekteki süreli sınavın bitiş saati değişmez; süre dolmuşsa sonuç hesaplanır.</p>
      <div className="mt-4 flex flex-wrap gap-3"><Button onClick={restore}>Onayla ve geri yükle</Button><Button variant="outline" onClick={() => { setCandidate(null); setMessage("Geri yükleme iptal edildi; ilerlemen değişmedi."); }}>Vazgeç</Button></div>
    </div>}
    {message && <p role="status" className="mt-4 text-sm leading-6">{message}</p>}
  </section>;
}
