const PYODIDE_BASE = "https://cdn.jsdelivr.net/pyodide/v0.27.7/full/";
importScripts("/python-runtime.js");
let pyodideReady;
let queue = Promise.resolve();
self.onmessage = ({ data }) => {
  queue = queue.then(async () => {
    const { id, code, stdin = "", tests } = data;
    try {
      if (!pyodideReady) {
        importScripts(`${PYODIDE_BASE}pyodide.js`);
        pyodideReady = loadPyodide({ indexURL: PYODIDE_BASE });
      }
      const pyodide = await pyodideReady;
      self.postMessage({ id, status: "running" });
      const version = pyodide.runPython("import sys; '.'.join(map(str, sys.version_info[:3]))");
      if (tests?.length) {
        const cases = await self.pythonRuntime.assess(pyodide, code, tests);
        self.postMessage({ id, ok: cases.every(item => item.passed), output: "", cases, version });
      } else {
        const result = await self.pythonRuntime.execute(pyodide, code, stdin);
        self.postMessage({ id, ...result, version });
      }
    } catch (error) {
      pyodideReady = undefined;
      self.postMessage({ id, ok: false, output: String(error), version: null });
    }
  });
};

