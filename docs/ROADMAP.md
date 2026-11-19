# NEXORA development roadmap

## Baseline and licensing

NEXORA is intended to evolve from the upstream PS5PCEM source tree. The upstream source code and its Git history have **not yet been imported**. Preserve the upstream license (GPL-3.0-or-later), license texts, authorship notices, and source attribution during import.

## Phase 1: Instrumentation (current)

- [x] Initialize the NEXORA repository.
- [x] Create `feature/nexora-profiler`.
- [x] Add standalone CSV frame-time analysis and regression tests.
- [ ] Import upstream PS5PCEM source and Git history, then verify a clean build.
- [ ] Add per-present timestamps with minimal instrumentation overhead.
- [ ] Record CPU frame, GPU submission, pipeline-compilation, and GPU-wait intervals.
- [ ] Export frame-time data to CSV with `frame_ms`, plus optional event columns.
- [ ] Compare baseline and optimized builds using identical workloads.

## Next stages

1. RDNA2 decoder validation: cross-check instructions against AMD RDNA2 ISA.
2. Shader pipeline optimizations: report cache hit rates and compile stalls.
3. Vulkan memory optimization: reduce unnecessary allocations and copies.
4. HLE and GPU compatibility: implement verified missing functionality.
5. Build and regression CI for Windows and Linux.

## Measurement contract

Input CSV requires a column named `frame_ms`, containing strictly positive finite frame durations in milliseconds. Malformed rows are ignored. The reporter outputs average FPS, average/median frame time, p95 and p99 frame times, and a 1%-low estimate (reciprocal of mean slowest 1% frame times). Comparisons require consistent scene, settings, resolution, driver, and warm-up policy.

## Example

```shell
python -m unittest discover -s tests -v
python tools/profile_analyze.py captures/frames.csv --out captures/summary.json
```
