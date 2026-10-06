// Shared by the browser Worker and executable regression tests.
// Fresh globals and input for each case; not a hostile-code security boundary.
globalThis.pythonRuntime = {
  async execute(pyodide, code, stdin = "") {
    const scope = pyodide.toPy({ source_code: code, input_text: stdin });
    try {
      const result = await pyodide.runPythonAsync(`
import io as _io, contextlib as _contextlib, traceback as _traceback, builtins as _builtins
import os as _os, shutil as _shutil, tempfile as _tempfile, sys as _sys, importlib as _importlib
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
# Each run starts in its own empty folder so file examples give the same result every time.
_home = _os.getcwd()
_workdir = _tempfile.mkdtemp(prefix="iz-")
_os.chdir(_workdir)
# Modules the run writes and imports, sys.path edits and environment variables are undone afterwards too.
_saved_path = list(_sys.path)
_saved_env = dict(_os.environ)
_importlib.invalidate_caches()
def _from_workdir(module):
    try:
        locations = [getattr(module, "__file__", None), *(getattr(module, "__path__", None) or [])]
        return any(isinstance(location, str) and location and (not _os.path.isabs(location) or location.startswith(_workdir + _os.sep)) for location in locations)
    except Exception:
        return False
with _contextlib.redirect_stdout(_output), _contextlib.redirect_stderr(_output):
    try:
        exec(compile(source_code, "cozum.py", "exec"), _namespace)
    except BaseException as _exception:
        _ok = False
        _tb = _exception.__traceback__
        while _tb is not None and _tb.tb_frame.f_code.co_filename != "cozum.py":
            _tb = _tb.tb_next
        _error = "".join(_traceback.format_exception(type(_exception), _exception, _tb))
    finally:
        for _name in [name for name, module in list(_sys.modules.items()) if _from_workdir(module)]:
            del _sys.modules[_name]
        _sys.path[:] = _saved_path
        _os.environ.clear()
        _os.environ.update(_saved_env)
        _os.chdir(_home)
        _shutil.rmtree(_workdir, ignore_errors=True)
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
