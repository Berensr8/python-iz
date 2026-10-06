/** Use the final exception line, never a word merely printed by the student's code. */
export function pythonErrorHint(output: string): string | null {
  const line = output.trimEnd().split("\n").at(-1) ?? "";
  if (/^SyntaxError:.*expected ':'/.test(line)) return "Satırın sonunda iki nokta (:) eksik olabilir. if, for, while veya def satırını kontrol et.";
  if (/^(IndentationError|TabError):/.test(line)) return "Girintileri kontrol et: aynı bloktaki satırlar aynı hizada olmalı. Sekme ve boşluğu karıştırma; blok içinde dört boşluk kullan.";
  if (/^NameError:/.test(line)) return "Bu isim henüz tanımlanmamış olabilir. Yazımını, büyük/küçük harfleri ve atama satırının daha önce çalıştığını kontrol et. Metin yazıyorsan tırnak gerekir.";
  if (/^TypeError:/.test(line)) return "İşlem bu veri tipiyle yapılamıyor olabilir. Değerlerin tiplerini type(...) ile incele; input() metin döndürür. Fonksiyonun aldığı argümanları da kontrol et.";
  return null;
}
