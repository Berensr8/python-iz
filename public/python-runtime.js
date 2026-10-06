// Shared by the browser Worker and executable regression tests.
// Fresh globals and input for each case; not a hostile-code security boundary.
globalThis.pythonRuntime = {
  async execute(pyodide, code, stdin = "") {
    const scope = pyodide.toPy({ source_code: code, input_text: stdin });
    try {
      const result = await pyodide.runPythonAsync(`
import io as _io, contextlib as _contextlib, traceback as _traceback, builtins as _builtins
class _LimitedOutput(_io.StringIO):
    def write(self, value):
        if self.tell() + len(value) > 20000:
            raise RuntimeError("Çıktı sınırı aşıldı (20.000 karakter).")
        return super().write(value)
_output = _LimitedOutput()
_inputs = iter(input_text.splitlines())
def _input(prompt=""):
    print(prompt, end="")
    try:
        return next(_inputs)
    except StopIteration:
        raise EOFError("Girdi alanında yeterli satır yok.") from None
_custom_builtins = dict(vars(_builtins))
_custom_builtins["input"] = _input
_namespace = {"__name__": "__main__", "__builtins__": _custom_builtins}
_ok = True
with _contextlib.redirect_stdout(_output), _contextlib.redirect_stderr(_output):
    try:
        exec(compile(source_code, "cozum.py", "exec"), _namespace)
    except BaseException:
        _ok = False
        _error = _traceback.format_exc()
_text = _output.getvalue().rstrip("\\n")
if not _ok:
    _text = (_text + "\\n" + _error).strip("\\n")
[_ok, _text]
`, { globals: scope });
      try {
        const [ok, output] = result.toJs();
        return { ok, output };
      } finally { result.destroy(); }
    } finally { scope.destroy(); }
  },
  async assess(pyodide, code, tests) {
    const results = [];
    for (const test of tests) {
      const result = await this.execute(pyodide, code, test.stdin);
      results.push({ ...test, ...result, passed: result.ok && result.output === test.expectedOutput });
    }
    return results;
  },
};
