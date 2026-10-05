const PYODIDE_VERSION = "0.27.7";
const PYODIDE_BASE = `https://cdn.jsdelivr.net/pyodide/v${PYODIDE_VERSION}/full/`;
let pyodideReady;

async function getPyodide() {
  if (!pyodideReady) {
    importScripts(`${PYODIDE_BASE}pyodide.js`);
    pyodideReady = loadPyodide({ indexURL: PYODIDE_BASE });
  }
  return pyodideReady;
}

self.onmessage = async (event) => {
  const { id, code } = event.data;
  try {
    const pyodide = await getPyodide();
    const version = pyodide.runPython("import sys; '.'.join(map(str, sys.version_info[:3]))");
    const chunks = [];
    pyodide.setStdout({ batched: (value) => chunks.push(value) });
    pyodide.setStderr({ batched: (value) => chunks.push(value) });
    await pyodide.runPythonAsync(code);
    self.postMessage({ id, ok: true, output: chunks.join("\n").trimEnd(), version });
  } catch (error) {
    self.postMessage({ id, ok: false, output: String(error).replace(/^PythonError: /, ""), version: null });
  }
};

