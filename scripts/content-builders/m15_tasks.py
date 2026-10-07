"""M15 (Eşzamanlılık) writing tasks. Imported by build_m15.py.

All three run in the browser (asyncio on the site's loop); no task starts a thread or process.
"""

tasks = []


def c(text):
    return text.strip("\n")


def task(**fields):
    for key in ("starterCode", "solution", "exampleOutput"):
        fields[key] = c(fields[key])
    for test in fields["tests"]:
        test["expectedOutput"] = c(test["expectedOutput"])
    tasks.append(fields)


W1_PROGRAM = r'''
async def heartbeat(stop, beats):
    while not stop.is_set():
        beats.append(1)
        await asyncio.sleep(0)

async def main():
    n, step = (int(part) for part in input().split())
    stop = asyncio.Event()
    beats = []
    _, total = await asyncio.gather(heartbeat(stop, beats), crunch(n, step, stop))
    print("toplam:", total)
    print("nabız:", len(beats))

asyncio.run(main())
'''

task(
    id="m15-w1", moduleId=15, sectionId="blocking-loop",
    title="Nabzı kesmeyen hesap", level="Tamamla",
    objective="Uzun bir hesap sırasında await asyncio.sleep(0) ile event loop'a düzenli sıra vererek diğer görevin de çalışmasını sağla.",
    prompt="Girdi 'n step' biçiminde. crunch(n, step, stop) 0'dan n - 1'e kadar sayıların karelerini topluyor ama hesap bitene kadar event loop'a hiç sıra vermiyor; bu yüzden heartbeat görevi yalnızca bir kez çalışabiliyor. crunch'ı tamamla: her step adımda bir (i % step == step - 1 olduğunda) await asyncio.sleep(0) ile sıra ver. Hesap bitince stop kurulmalı (hazır). Program toplamı ve heartbeat'in kaç kez çalıştığını yazar.",
    starterCode=r'''
import asyncio

async def crunch(n, step, stop):
    total = 0
    for i in range(n):
        total += i * i
        # her step adımda bir event loop'a sıra ver
    stop.set()
    return total
''' + W1_PROGRAM,
    exampleInput="3000 1000",
    exampleOutput="toplam: 8995500500\nnabız: 4",
    hints=[
        "Döngü await etmeden dönerse event loop başka görevi çalıştıramaz. Sıra vermenin en kısa yolu await asyncio.sleep(0).",
        "Döngünün içine: if i % step == step - 1: await asyncio.sleep(0). Nabız sayısı, verilen sıra sayısından bir fazladır (heartbeat ilk kez hesaptan önce çalışır).",
    ],
    solution=r'''
import asyncio

async def crunch(n, step, stop):
    total = 0
    for i in range(n):
        total += i * i
        if i % step == step - 1:
            await asyncio.sleep(0)
    stop.set()
    return total
''' + W1_PROGRAM,
    tests=[
        {"label": "Örnek", "stdin": "3000 1000", "expectedOutput": "toplam: 8995500500\nnabız: 4"},
        {"label": "Küçük adım", "stdin": "10 3", "expectedOutput": "toplam: 285\nnabız: 4"},
        {"label": "Adım hesaptan uzun", "stdin": "5 10", "expectedOutput": "toplam: 30\nnabız: 1"},
        {"label": "Her adımda", "stdin": "4 1", "expectedOutput": "toplam: 14\nnabız: 5"},
    ],
)

task(
    id="m15-w2", moduleId=15, sectionId="cancellation-timeout",
    title="Zaman aşımlı yeniden deneme", level="Düzelt",
    objective="İptalin yutulmasını, yanlış yakalanan hatayı, eksik deneme sayısını ve yalnız başarıda kapanan bağlantıyı düzelt.",
    prompt="Girdi: süre sınırı, deneme sayısı ve servisin her denemede yanıt vereceği süreler (denemeler süre sayısını aşarsa son süre kullanılır). call_with_retry her denemeyi wait_for ile sınırlar; aşılan denemede 'deneme N: zaman aşımı' yazar; yanıt gelirse 'sonuç: yanıt (deneme N)', denemeler tükenirse 'sonuç: vazgeçildi' yazılır; sonda açık kalan bağlantı sayısı (0 olmalı) yazılır. Kodda dört hata var: servis iptali yutuyor; çağıran taraf wait_for'un fırlattığı hatayı değil başka bir hatayı yakalıyor; son deneme hiç yapılmıyor; bağlantı yalnızca başarılı yolda kapanıyor (else yerine finally olmalı). Dördünü de düzelt.",
    starterCode=r'''
import asyncio

class Service:
    def __init__(self, durations):
        self.durations = durations
        self.calls = 0
        self.open = 0

    async def call(self):
        seconds = self.durations[min(self.calls, len(self.durations) - 1)]
        self.calls += 1
        self.open += 1
        try:
            await asyncio.sleep(seconds)
        except asyncio.CancelledError:
            return None
        else:
            self.open -= 1
        return "yanıt"

async def call_with_retry(service, retries, limit):
    for attempt in range(1, retries):
        try:
            result = await asyncio.wait_for(service.call(), timeout=limit)
            return f"{result} (deneme {attempt})"
        except asyncio.CancelledError:
            print(f"deneme {attempt}: zaman aşımı")
    return "vazgeçildi"

async def main():
    limit = float(input())
    retries = int(input())
    service = Service([float(part) for part in input().split()])
    print("sonuç:", await call_with_retry(service, retries, limit))
    print("açık bağlantı:", service.open)

asyncio.run(main())
''',
    exampleInput="0.5\n3\n2 2 0.1",
    exampleOutput="deneme 1: zaman aşımı\ndeneme 2: zaman aşımı\nsonuç: yanıt (deneme 3)\naçık bağlantı: 0",
    hints=[
        "Süre dolunca wait_for görevi iptal eder: görevin içinde CancelledError oluşur, dışarıya ise TimeoutError çıkar. Görev iptali yutarsa wait_for ne döndürür? range(1, retries) kaç deneme yapar? else bloğu hata olunca çalışır mı?",
        "Servisteki except bloğunda return None yerine raise yaz; call_with_retry'da except TimeoutError yakala; range(1, retries + 1) kullan; bağlantıyı kapatan else'i finally yap.",
    ],
    solution=r'''
import asyncio

class Service:
    def __init__(self, durations):
        self.durations = durations
        self.calls = 0
        self.open = 0

    async def call(self):
        seconds = self.durations[min(self.calls, len(self.durations) - 1)]
        self.calls += 1
        self.open += 1
        try:
            await asyncio.sleep(seconds)
        finally:
            self.open -= 1
        return "yanıt"

async def call_with_retry(service, retries, limit):
    for attempt in range(1, retries + 1):
        try:
            result = await asyncio.wait_for(service.call(), timeout=limit)
            return f"{result} (deneme {attempt})"
        except TimeoutError:
            print(f"deneme {attempt}: zaman aşımı")
    return "vazgeçildi"

async def main():
    limit = float(input())
    retries = int(input())
    service = Service([float(part) for part in input().split()])
    print("sonuç:", await call_with_retry(service, retries, limit))
    print("açık bağlantı:", service.open)

asyncio.run(main())
''',
    tests=[
        {"label": "Örnek", "stdin": "0.5\n3\n2 2 0.1", "expectedOutput": "deneme 1: zaman aşımı\ndeneme 2: zaman aşımı\nsonuç: yanıt (deneme 3)\naçık bağlantı: 0"},
        {"label": "İlk denemede yanıt", "stdin": "1\n2\n0.2", "expectedOutput": "sonuç: yanıt (deneme 1)\naçık bağlantı: 0"},
        {"label": "Vazgeçilir", "stdin": "0.3\n2\n1", "expectedOutput": "deneme 1: zaman aşımı\ndeneme 2: zaman aşımı\nsonuç: vazgeçildi\naçık bağlantı: 0"},
        {"label": "Son deneme yetişir", "stdin": "0.5\n4\n1 1 1 0.2", "expectedOutput": "deneme 1: zaman aşımı\ndeneme 2: zaman aşımı\ndeneme 3: zaman aşımı\nsonuç: yanıt (deneme 4)\naçık bağlantı: 0"},
    ],
)

task(
    id="m15-w3", moduleId=15, sectionId="tasks-gather",
    title="Eşzamanlı indirme raporu", level="Sıfırdan yaz",
    objective="Bütün indirmeleri aynı anda yürüt; her birine süre sınırı koy, hataları ve zaman aşımlarını sonuç olarak topla ve girdi sırasıyla raporla.",
    prompt="İlk satır süre sınırı, ikinci satır indirme sayısı, sonraki her satır 'ad süre boyut'. Bir indirme 'süre' saniye bekler; boyut negatifse ValueError('bozuk yanıt') fırlatır, değilse boyutu döndürür. Bütün indirmeleri aynı anda yürüt ve her birini süre sınırıyla çalıştır. Girdi sırasıyla 'ad: 120 bayt', 'ad: zaman aşımı' ya da 'ad: hata (bozuk yanıt)' yaz; sonra 'toplam: N bayt' (yalnız başarılılar) ve loop.time() ile ölçülen 'süre: 0.5 sn'. Bir indirmenin hatası diğerlerini durdurmamalı.",
    starterCode=r'''
import asyncio

# download(seconds, size): asyncio.sleep ile bekle; size < 0 ise ValueError("bozuk yanıt"), değilse size döndür.
# Her indirmeyi asyncio.wait_for ile süre sınırına bağla, hepsini aynı anda yürüt
# (gather(..., return_exceptions=True) hataları sonuç olarak döndürür) ve raporu girdi sırasıyla yaz.

async def main():
    limit = float(input())
    jobs = []
    for _ in range(int(input())):
        name, seconds, size = input().split()
        jobs.append((name, float(seconds), int(size)))

asyncio.run(main())
''',
    exampleInput="0.5\n3\nana 0.2 120\nlogo 0.9 40\nveri 0.1 -1",
    exampleOutput="ana: 120 bayt\nlogo: zaman aşımı\nveri: hata (bozuk yanıt)\ntoplam: 120 bayt\nsüre: 0.5 sn",
    hints=[
        "results = await asyncio.gather(*(asyncio.wait_for(download(s, b), timeout=limit) for _, s, b in jobs), return_exceptions=True). return_exceptions=True ile hatalar fırlatılmaz, listede sonuç olarak durur.",
        "Sonuçları zip(jobs, results) ile dolaş: isinstance(result, TimeoutError) → zaman aşımı, isinstance(result, ValueError) → hata, yoksa boyut. Süreyi gather'dan önce ve sonra loop.time() ile ölç.",
    ],
    solution=r'''
import asyncio

async def download(seconds, size):
    await asyncio.sleep(seconds)
    if size < 0:
        raise ValueError("bozuk yanıt")
    return size

async def main():
    limit = float(input())
    jobs = []
    for _ in range(int(input())):
        name, seconds, size = input().split()
        jobs.append((name, float(seconds), int(size)))
    loop = asyncio.get_running_loop()
    start = loop.time()
    results = await asyncio.gather(
        *(asyncio.wait_for(download(seconds, size), timeout=limit) for _, seconds, size in jobs),
        return_exceptions=True,
    )
    total = 0
    for (name, _, _), result in zip(jobs, results):
        if isinstance(result, TimeoutError):
            print(f"{name}: zaman aşımı")
        elif isinstance(result, ValueError):
            print(f"{name}: hata ({result})")
        else:
            total += result
            print(f"{name}: {result} bayt")
    print(f"toplam: {total} bayt")
    print(f"süre: {loop.time() - start:.1f} sn")

asyncio.run(main())
''',
    tests=[
        {"label": "Örnek", "stdin": "0.5\n3\nana 0.2 120\nlogo 0.9 40\nveri 0.1 -1", "expectedOutput": "ana: 120 bayt\nlogo: zaman aşımı\nveri: hata (bozuk yanıt)\ntoplam: 120 bayt\nsüre: 0.5 sn"},
        {"label": "Hepsi başarılı", "stdin": "1\n3\na 0.3 10\nb 0.1 20\nc 0.2 30", "expectedOutput": "a: 10 bayt\nb: 20 bayt\nc: 30 bayt\ntoplam: 60 bayt\nsüre: 0.3 sn"},
        {"label": "Hata diğerlerini durdurmaz", "stdin": "1\n2\nbozuk 0.1 -5\niyi 0.4 7", "expectedOutput": "bozuk: hata (bozuk yanıt)\niyi: 7 bayt\ntoplam: 7 bayt\nsüre: 0.4 sn"},
        {"label": "Hepsi zaman aşımı", "stdin": "0.2\n2\nx 1 5\ny 2 6", "expectedOutput": "x: zaman aşımı\ny: zaman aşımı\ntoplam: 0 bayt\nsüre: 0.2 sn"},
    ],
)
