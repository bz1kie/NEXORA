# NEXORA

Experimental PlayStation 5 emulator project based on [PS5PCEM](https://github.com/iStark/PS5PCEM).

> **Status:** project bootstrap only. The upstream emulator source has **not yet been imported**, so this repository is not currently a working PS5 emulator.

## Development approach

1. Import the upstream PS5PCEM Git history and source code, preserving its notices and GPL-3.0-or-later license.
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
