# Additional PS5 research discoveries (2026-11-19)

These are **new leads beyond** the five repositories in REPOSITORY_REVIEW.md. Sources were checked through public GitHub README/docs; no source code was imported. Statements about execution or compatibility are the authors' claims until independently reproduced.

| Project | Link | Practical NEXORA application | Licensing / caveat |
|---|---|---|---|
| prosper | https://github.com/mattias800/prosper | PS5 user-space compatibility layer: native x86-64, SELF/ELF linking, HLE, AGC→Vulkan, RDNA2→SPIR-V. Its tools include GPU timeline/replay, shader histogram, snapshot tests, and SPIR-V validation. **Top priority**: copy testing *methodology*, not code. | README explicitly states **no LICENSE file / no license granted**: do not copy code. Claims game-specific progress, not universal support. |
| ps5rs | https://github.com/claimore22/ps5rs | Rust binary analysis: SELF/ELF/PRX, NID imports, dependency graphs, unresolved NID frequency, engine fingerprints, self-authored ELF fixtures and offline dashboards. Add an original NEXORA import-coverage report. | GPL-2.0-only according to README; no code copying into GPL-3.0-or-later without license resolution. |
| opengnm-psbc | https://github.com/PS4-OpenGNM/opengnm-psbc | Reverse-direction SPIR-V→PS5 GFX10.3 shader compiler based on Mesa NIR/ACO. Valuable for shader **round-trip test generation**, instruction coverage and shader container layout. | Reverse direction from NEXORA's RDNA2→SPIR-V; not a replacement translator. Verify output on test fixtures. |
| PS5_Vulkan | https://github.com/mihawk-99/PS5_Vulkan | Native Vulkan driver research, RADV/Mesa winsys and conformance tests. Compare resource formats, memory allocation semantics and evidence quality. | Console-side Vulkan, not host emulator Vulkan backend. |
| ps5link-sdk | https://github.com/Rufidj/ps5link-sdk | PS5 homebrew ELF linker: SCE dynamic tables, NID imports, GOT/PLT, test fixtures and simple GPU draw sample. Use synthetic format/relocation tests. | Console-side SDK; avoid proprietary SDK artifacts and keys. |
| PS4-OpenGNM | https://github.com/PS4-OpenGNM/opengnm | PS4 GNM interfaces and shader formats relevant to PS5 backward compatibility. | PS4-specific, not a PS5 AGC specification. |
| shadPS4 | https://github.com/shadps4-emu/shadPS4 | Mature PS4 native-x86 emulator with shader and HLE testing ideas. | PS4 architecture differs; adapt concepts only after verification. |

## Highest-value discoveries

1. **prosper verification discipline**: validate generated SPIR-V with spirv-val; execute synthetic Vulkan shader tests; compare rendered pixel output; retain before/after captures. Its compatibility ladder separates first pixels, title screen, gameplay, visual review, hardware comparison and snapshot regression.
2. **ps5rs import coverage**: measure per-title imported NIDs, known names, resolved HLE functions, unknowns and stubs. Rank missing functions by actual usage, not guesswork. Include module/version provenance.
3. **opengnm-psbc as a generator**: generate legal self-authored test shaders and validate round trips with NEXORA's decoder and shader translator; SPIR-V→GPU ISA is the opposite direction to the emulator and not directly reusable.
4. **ps5link-sdk synthetic link tests**: exercise relocation, import and GOT/PLT semantics without commercial games.
5. **PS5_Vulkan format evidence**: use documented format tests to prioritize texture/swizzle handling and guard against unsupported-format fallbacks.

## Proposed implementation order

- [ ] NEXORA HLE import coverage report (JSON/CSV) with known/unknown/stub categories, tested on synthetic ELF.
- [ ] Shader validation gate (spirv-val) and deterministic pixel tests for supported shader operations.
- [ ] GPU frame replay/command trace with command order and fence assertions.
- [ ] Texture format/tiling correctness fixtures, then resource pressure telemetry.
- [ ] Per-title compatibility ladder and evidence-linked status records.

## Evidence and restrictions

- **Do not import** source from prosper (unlicensed), ps5rs (GPL-2.0-only), or other repositories without reviewing licenses and file provenance.
- The reported gameplay milestones in prosper are project-maintainer claims; NEXORA has not reproduced them.
- PS5 native driver projects operate in the opposite environment (host code running *on* PS5) from NEXORA (PS5 binaries running *on PC*).
- No changes here establish FPS gains or commercial-game compatibility.
