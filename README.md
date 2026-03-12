# py2bin

**Bundle a Python project into a self-contained native binary.**

Original idea and design by [@SigmoidBabe](https://github.com/SigmoidBabe) — this library is a packaged implementation of their concept.

```
your_project/ .py files
       │
       ▼  Stage 1 – PyzPackager
   app.pyz        (zipapp)
       │
       ▼  Stage 2 – XxdConverter   (xxd -i)
   app.h          (C hex array)
       │
       ▼  Stage 3 – CCompiler      (gcc)
   app            ← native binary, runs python3 internally
```

The binary embeds the entire ``.pyz`` as a C byte array, writes it to ``/tmp`` at
runtime, then ``execvp``s ``python3`` to run it — no extra runtime packaging needed.

---

## Requirements

* Python ≥ 3.10
* `xxd` (comes with vim on most Linux distros: `apt-get install xxd`)
* `gcc` (`apt-get install build-essential`)
* `python3` on the target machine (the binary delegates execution to it)

---

## Install

### From GitHub (recommended)

```bash
pip install git+https://github.com/YOUR_USERNAME/py2bin.git
```

### Editable / development install

```bash
git clone https://github.com/YOUR_USERNAME/py2bin.git
cd py2bin/..          # go to the PARENT of the cloned folder
pip install -e py2bin
```

---

## CLI

```bash
py2bin --project ./my_app --entry __main__.py --output ./build --name my_app
```

| Flag | Description |
|---|---|
| `--project` / `-p` | Root directory of the Python project |
| `--entry`   / `-e` | Entry-point script (relative to `--project`) |
| `--output`  / `-o` | Output directory for all build artefacts |
| `--name`    / `-n` | Base name for output files (default: project dir name) |

**Build artefacts written to `<output>/`:**

| File | Description |
|---|---|
| `<name>.pyz` | Zipapp of your project |
| `<name>.h`   | C hex-array header (`xxd -i` output) |
| `<name>_launcher.c` | Generated C launcher source |
| `<name>`     | Compiled native binary |

---

## Library API

```python
from pathlib import Path
from py2bin import Py2BinConfig, Py2BinPipeline
from py2bin import PyzPackager, XxdConverter, CCompiler

config = Py2BinConfig(
    project_dir=Path("./my_app"),
    entry_script="__main__.py",      # relative to project_dir
    output_dir=Path("./build"),
    app_name="my_app",
)

pipeline = Py2BinPipeline(
    packager=PyzPackager(),
    converter=XxdConverter(),
    compiler=CCompiler(),
)

result = pipeline.run(config)

if result.success:
    print(f"Binary ready: {result.binary_path}")
else:
    print(f"Build failed: {result.error}")
```

### Custom stage implementations

Each stage is backed by an ABC — swap in your own:

```python
from py2bin import IPackager, IConverter, ICompiler
```

| Interface | Responsibility |
|---|---|
| `IPackager`  | `pack(config) -> Path`                              |
| `IConverter` | `convert(pyz_path, output_dir, app_name) -> Path`   |
| `ICompiler`  | `compile(hex_header_path, config) -> (Path, Path)`  |

---

## Architecture

```
py2bin/
├── __init__.py              ← public API surface
├── main.py                  ← CLI (argparse)
├── pipeline.py              ← Py2BinPipeline
├── schemas/schemas.py       ← Py2BinConfig, BuildResult
├── interfaces/interfaces.py ← IPackager, IConverter, ICompiler
└── infrastructure/
    ├── packager.py          ← PyzPackager
    ├── converter.py         ← XxdConverter
    └── compiler.py          ← CCompiler
```

---

## Credits

Original idea and design by [@SigmoidBabe](https://github.com/SigmoidBabe) — this library is a packaged implementation of their concept.

---

## License

MIT
