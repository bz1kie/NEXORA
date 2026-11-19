# NEXORA

Experimental PlayStation 5 emulator project based on [PS5PCEM](https://github.com/iStark/PS5PCEM).

> **Status:** experimental development. The upstream PS5PCEM source and Git history were imported into the `import/ps5pcem-upstream-44485557126` branch. A verified NEXORA emulator build is still pending.

## Development approach

1. Preserve the imported upstream PS5PCEM Git history, source code, copyright notices, and GPL-3.0-or-later license.
2. Keep the original emulator architecture operational and establish repeatable baseline benchmarks.
3. Add CPU/GPU frame profiling and regression tests.
4. Incrementally optimize shader translation, Vulkan rendering, memory management, and HLE behavior.

## Phase 1 — profiling utilities

The `tools/profile_analyze.py` script consumes frame-time CSV and emits repeatable summary metrics. Example:

```bash
python tools/profile_analyze.py path/to/frames.csv
python -m unittest discover -s tests -v
```

## License and attribution

NEXORA is intended as a modified version of PS5PCEM. Upstream PS5PCEM is licensed under **GPL-3.0-or-later**. Retain upstream copyright and license notices when importing its code. Do not remove attribution. The NEXORA-specific code in this repository is also offered under **GPL-3.0-or-later**.

Upstream: https://github.com/iStark/PS5PCEM
