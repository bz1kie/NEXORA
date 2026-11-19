# Repository-level review: independent PS5 projects

Reviewed 2026-11-19 against public GitHub repository trees and the files linked below. **Scope:** all five repositories were inspected at the repository-tree level; the selected architecture and diagnostics documents below were read. This is not a line-by-line audit of thousands of source files. Treat repository README claims as project claims, not NEXORA compatibility evidence.

## Kyty — InoriRus/Kyty

- Source: https://github.com/InoriRus/Kyty/blob/main/README.md
- Tree inspected: ~3,165 entries. C++, MIT according to repository metadata and README.
- Maintainer says **some simple PS4 games and PS5 homebrew** can run, with graphics errors, freezes and low FPS. Audio I/O, MP4, networking and multi-user are listed as missing.
- **NEXORA action:** compare executable loader and HLE import resolution against `docs/architecture/loader.md` and `src/hle/`. Use independently authored synthetic fixtures. Do not infer commercial PS5 compatibility from Kyty's screenshots.
- **Performance:** benchmark module lookup and guest-to-host dispatch only if equivalent workloads can be reproduced.

## Prosperity — Force67/prosperity

- Source: https://github.com/Force67/prosperity/blob/master/delta/gpu/README.md
- Tree inspected: ~4,172 entries. Repository metadata reports GPL-2.0; verify exact license text and per-file notices before any reuse.
- GPU is explicitly layered into PS4 and PS5 command processors, common GCN/SPIR-V translation, a guest-independent renderer and Vulkan/OpenGL/D3D12 RHI. It documents a test-enforced layering check (`tests/check_layering.py`).
- **NEXORA action:** introduce an architectural dependency test that rejects direct host graphics API coupling in GPU packet decoding. Compare conceptual boundaries with `src/gpu/pm4.zig`, `src/gpu/scheduler.zig` and `src/vulkan/backend.zig`.
- **License warning:** do not copy Prosperity code into GPL-3.0-or-later NEXORA unless an explicit compatibility determination permits it. Read architecture descriptions as research.

## SharpEmu — sharpemu/sharpemu

- Sources: https://github.com/sharpemu/sharpemu/blob/main/README.md and https://github.com/sharpemu/sharpemu/blob/main/docs/image-memory-diagnostics.md
- Tree inspected: ~2,183 entries. C# experimental PS5 emulator with PS4 backward-compatibility mode. Repository license metadata reports GPL-2.0; README header says GPL-2.0-or-later, so **license scope must be checked per file**.
- Its documented image diagnostics distinguish **allocated**, **indexed**, and **pending** bytes; counts live device allocations, large cached images, image ownership, dirty-buffer overlap and cache retention reasons. It explicitly warns that retention counts are visits, not unique images, and that eligibility is not proof of safe removal.
- **NEXORA action (high priority):** build equivalent *original* GPU-resource telemetry: live bytes vs cumulative allocations, cached vs pending, largest allocations, eviction reason, dirty/owned state, and host allocation limits. Keep diagnostics read-only initially.
- **Performance:** measure VRAM pressure and texture churn on identical scenes before tuning eviction heuristics.

## OrbisView — cragson/OrbisView

- Source: https://github.com/cragson/OrbisView/blob/master/README.md
- Small tree (~18 entries). **Correction to earlier research:** this is primarily a **live PS5 memory/process inspection tool**, not an ELF/SELF parser or standalone emulator.
- It documents typed memory reads, hex/ASCII pattern searches, process enumeration, address history and a console payload. Some firmware/memory regions may be restricted.
- **NEXORA action:** use its *interface ideas* to design an offline, emulator-owned guest-memory inspector for synthetic test programs. No console payloads, remote access, exploit integration or proprietary SDK dependency is needed.

## OpenProspero / OpenAGC

- Sources: https://github.com/OpenProspero/AGC/blob/main/README.md and https://github.com/OpenProspero/AGC/blob/main/docs/shader-toolchain.md
- Tree inspected: ~144 entries. GPL-3.0 per repository metadata; inspect actual file notices for GPL-3.0-or-later scope.
- Project distinguishes **host simulation** of memory/buffers/fences from narrow console-verified GPU compute and a qualified draw/pixel test. It expressly does **not** claim a general working GPU backend from a single proven draw.
- Shader toolchain notes distinguish compiler source revision, patch hash, binary digest and shader artifact integrity. Integrity checks do not prove shader semantic correctness.
- **NEXORA action:** adopt the *testing discipline*: synthetic draw/compute fixtures with expected output, guards around destination buffers, recorded shader provenance and separately tagged host-only vs hardware-proven behavior.
- **Performance:** compare shader translation results against deterministic fixtures; only optimize after preserving identical output.

## Cross-project priorities for NEXORA

| Priority | Original NEXORA change | Evidence motivating it | Verification |
|---|---|---|---|
| P0 | GPU image-cache/VRAM diagnostic report | SharpEmu image-memory diagnostics | No effect on eviction behavior; counters consistent across create/reuse/destroy |
| P0 | Shader cache hit/miss and compile-time counters | OpenAGC shader provenance; NEXORA shader pipeline | Warm runs reduce redundant compile count; output unchanged |
| P0 | Host-vs-guest GPU timing separation | Prosperity renderer/RHI layering; NEXORA frame sampler | CPU submit and GPU execution shown as overlapping measurements, never added |
| P1 | Guest command decoder isolation tests | Prosperity GPU architecture | Unit test detects forbidden dependency |
| P1 | Synthetic ELF/SELF and HLE ABI fixtures | Kyty loader/HLE design | Import/relocation/thread tests deterministic |
| P2 | Read-only guest memory inspector | OrbisView UI | Only emulator-owned test memory; no remote payload required |

## Safety, reproducibility and provenance

- All findings above derive from public README/docs, repository metadata and trees; no unreviewed third-party implementation code was copied.
- Save source repository commit hashes before using a specific algorithm; URLs to moving `main`/`master` are not immutable.
- Record exact source path, source license, local test, performance baseline and resulting NEXORA commit in follow-up research.
- No claims of verified PS5 game compatibility or FPS gains follow from these comparisons.
