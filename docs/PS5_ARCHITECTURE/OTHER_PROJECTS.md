# Additional open-source PS5 emulator and research projects

Reviewed 2026-11-19. Repository descriptions are **claims by their maintainers**, not independent compatibility benchmarks.

| Project | Role | Value to NEXORA | Caution |
|---|---|---|---|
| [InoriRus/Kyty](https://github.com/InoriRus/Kyty) | Experimental PS4/PS5 emulator (C++, MIT) | Compare loader, HLE, graphics API abstractions and test harness patterns | Different architecture and incomplete compatibility; port algorithms only after reviewing licensing and tests |
| [Force67/prosperity](https://github.com/Force67/prosperity) | Low-level PS4/PS5 emulator (C++, GPL-2.0 per repository metadata) | Compare LLE vs NEXORA HLE boundaries and guest memory design | GPL-2.0-only code may be incompatible with NEXORA GPL-3.0-or-later; **do not copy source** without a license audit |
| [sharpemu/sharpemu](https://github.com/sharpemu/sharpemu) | Experimental PS5 emulator | Independent comparison of module loading, HLE and graphics design | Confirm actual implementation and license before reuse |
| [cragson/OrbisView](https://github.com/cragson/OrbisView) | PlayStation binary analysis tooling | Investigate formats, symbols and loader test fixtures | Tooling, **not** an emulator |
| [OpenProspero/AGC](https://github.com/OpenProspero/AGC) | Open GPU driver research | Compare GPU command semantics and validation strategy | Not a complete PS5 emulator |
| [iStark/PS5PCEM](https://github.com/iStark/PS5PCEM) | NEXORA upstream | Existing baseline implementation | Already integrated; avoid treating upstream claims as verified game compatibility |

**Excluded from emulator references:** [heydemoura/EglantinePS5](https://github.com/heydemoura/EglantinePS5) is described as a **Nintendo Switch 2 emulator port running on PS5**, not an emulator of PS5 games on PC. Similar search results may use 'PS5 emulator' in unrelated contexts.

## Specific comparison tasks

1. Compare Kyty and sharpemu's executable loader behavior with `src/loader/` and NEXORA's [loader architecture](../architecture/loader.md). Write format/relocation tests before implementing changes.
2. Compare Kyty's HLE API coverage and ABI tests with `src/hle/`. Prioritize real missing symbols evidenced by legally obtained test applications.
3. Use OrbisView to identify testable executable-format edge cases; do not import copyrighted game binaries.
4. Review OpenProspero AGC's publicly documented command/register semantics against `src/gpu/pm4.zig` and `src/gpu/scheduler.zig`. Preserve ordering and fence correctness.
5. Study prosperity **conceptually only** pending a GPL-2.0 compatibility determination.
6. Record per-project commit hashes, exact files examined, licenses and reproducible test outcomes before code changes.

## Why this matters for performance

- An alternative project may suggest a better implementation, but a faster algorithm cannot be assumed from code inspection alone.
- Collect **before/after frame timing and GPU command microbenchmarks** on NEXORA before adopting techniques.
- Distinguish native x86-64 guest execution, OS/HLE overhead, GPU command decoding, shader translation and GPU execution as separate bottlenecks.

Research is not evidence of commercial PS5 game compatibility.
