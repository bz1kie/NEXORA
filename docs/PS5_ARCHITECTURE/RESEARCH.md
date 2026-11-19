# PS5 research notebook for NEXORA

This is a **source-linked engineering digest**, not a mirror of third-party articles or a copy of Sony's SDK. Findings below are separated into independently documented hardware facts, public research observations, and NEXORA-specific hypotheses. Last reviewed: 2026-11-19.

## Sources and reliability

| Source | Scope | What is established | Limitations / next verification |
|---|---|---|---|
| [PS5 Developer Wiki — CPU](https://www.psdevwiki.com/ps5/CPU) | CPU | AMD Zen 2-derived x86-64, 8 cores / 16 threads, variable clock up to 3.5 GHz | Hardware specifications alone do not establish guest ABI or native execution correctness |
| [PS5 Developer Wiki — GPU](https://www.psdevwiki.com/ps5/GPU) | GPU | AMD RDNA 2-based GPU, 2.23 GHz peak, ray tracing | Does not document complete AGC/PM4 packet semantics |
| [PS5 Developer Wiki — Memory](https://www.psdevwiki.com/ps5/Memory) | Memory | Eight 2 GB GDDR6 devices (16 GB total) | Does not establish exact guest virtual address layout |
| [OpenProspero/AGC](https://github.com/OpenProspero/AGC) | GPU research | Public clean-room driver research, command validation and backend capability boundaries | Host Vulkan/OpenGL frontends are not proof of complete GPU execution; confirm each register/packet against tests |
| [etaHEN PS5 package writeup](https://github.com/etaHEN/etaHEN/blob/main/PS5%20technical%20writeups/pkg-writeup.md) | Package installation | PS5 package installation interfaces differ from earlier PS4 BGFT workflows | Focused on console-side installation, **not** a drop-in emulator package parser; do not transplant privilege-escalation steps |
| [Upstream emulator architecture](https://github.com/iStark/PS5PCEM/blob/main/docs/README.md) | Existing implementation | Documents loader, native CPU, HLE, GPU scheduling, RDNA2 translation and Vulkan/D3D12 | Upstream implementation claims must be checked against NEXORA code and reproducible traces |

Wiki material is licensed separately (GFDL 1.2); **link and paraphrase** rather than copying article text into GPL source. Do not import proprietary firmware, SDKs, keys, decrypted game content or unlicensed code.

## Architecture: how the pieces interact

1. **Loader / process:** map ELF/SELF images, relocations, imports, TLS and guest memory. See [loader](../architecture/loader.md), [memory](../architecture/memory.md).
2. **CPU / HLE:** run compatible x86-64 guest instructions natively while intercepting platform-specific calls and maintaining guest ABI, thread scheduling and synchronization. See [CPU](../architecture/cpu.md), [HLE](../architecture/hle.md).
3. **AGC / GPU command stream:** decode packets and preserve register state, submission order, waits and resource hazards. See [GPU](../architecture/gpu.md), [command processors](../architecture/command-processors.md).
4. **Shader translation:** decode GFX10/RDNA2 shader instructions and lower supported semantics into host SPIR-V. See [RDNA2](../architecture/rdna2.md).
5. **Host graphics:** Vulkan (primary) or experimental D3D12 allocates host resources, translates commands, synchronizes and presents. See [Vulkan](../architecture/vulkan.md), [D3D12](../architecture/d3d12.md).

**Important distinction:** PS5's unified 16 GB GDDR6 is not equivalent to the host PC's separately budgeted system RAM and discrete GPU VRAM. The host must track residency, aliases, copies and eviction; the number of guest address-space bytes reserved is not the same as committed physical memory.

## Actionable performance investigations

| Priority | Hypothesis to test | NEXORA locations | Required measurement | Acceptance criterion |
|---|---|---|---|---|
| P0 | Shader compilation or duplicate pipelines cause stalls | `src/d3d12/shader_cache.zig`, `src/gpu/shaders.zig`, Vulkan backend | compilation count, cache hit/miss, compile wall time per shader hash | Fewer repeated compilations without image differences |
| P0 | Guest submit / PM4 decode dominates CPU time | `src/gpu/frame_timing.zig`, `src/gpu/pm4.zig`, `src/gpu/scheduler.zig` | submit count, CPU submit time, wait durations, PM4 packet counts | Reduced P95/P99 on identical capture; no changed command order |
| P1 | Unnecessary barriers or resource transitions stall GPU | `src/vulkan/backend.zig`, `src/gpu/resource_preparation.zig` | GPU timestamp queries, barrier counts, fence wait times | Reduced GPU idle/wait time, identical rendered output |
| P1 | Host copies and texture churn exceed VRAM budget | `src/d3d12/texture_cache.zig`, `src/d3d12/surface_cache.zig`, Vulkan resources | upload bytes/frame, cache hit ratio, allocation/eviction counts | Lower transfers, no stale resource aliasing |
| P1 | Worker overhead outweighs parallelism on short jobs | `src/gpu/worker_policy.zig`, `src/gpu/command_workers.zig` | queue latency, work duration, active workers | Faster matched workload; deterministic scheduling preserved |

### Measurement rules

- Compare the **same title, scene, resolution, renderer, settings and hardware** before/after; collect multiple runs after warmup.
- Report frame-time P50/P95/P99, 1% low FPS, frames over 33.33/50 ms, shader compilation time and host GPU utilization where available.
- **Do not sum overlapping CPU and GPU durations** as if they were exclusive portions of a frame. Use GPU timestamp queries for GPU execution; host CPU timers measure submission/driver overhead.
- Never assume higher worker count is faster: use the existing worker policy as an experimental variable.
- Prefer one reversible change per benchmark, and add correctness regression tests for command order, synchronization and shader outputs.

## Immediate next engineering tasks

- [ ] Add **shader compilation counters** and cache hit/miss telemetry at actual compilation and lookup sites.
- [ ] Add GPU timestamp-based execution timing (separate from CPU-side Vulkan submission).
- [ ] Export per-frame CPU submit time, submit calls and frame interval to a versioned CSV schema.
- [ ] Produce a reproducible graphics/compute microbenchmark using legally distributable test shaders and PM4 fixtures.
- [ ] Compare OpenProspero AGC's documented packet/register validation with `src/gpu/pm4.zig` and write targeted unit tests, without importing unreviewed code.
- [ ] Record provenance, test results and measured gains in this notebook before merging optimizations.

## What remains unknown

The sources above do **not** provide a complete PS5 GPU register specification, proprietary firmware API contract or evidence that NEXORA can execute all commercial games. Any claim of compatibility or FPS improvement must be supported by tests and reproducible captures.
