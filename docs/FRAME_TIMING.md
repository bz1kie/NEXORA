# NEXORA Vulkan frame timing

## Current integration

The Vulkan renderer's `reportFrameProfile()` records a monotonic timestamp into
`Renderer.nexora_frame_sampler` whenever it reports a guest flip.

The sampler is an allocation-free ring buffer holding the newest 4096 frame
intervals in nanoseconds. The first timestamp establishes a baseline and is
not counted as a frame interval. Non-increasing timestamps are ignored.

The independent `tools/profile_analyze.py` accepts CSV with a `frame_ms`
column. The Zig sampler provides `writeCsv(writer)` for this format, but
**the renderer now exposes `writeNexoraFrameCsv(writer)`, but the emulator does
not yet expose a user-facing export command or write a CSV file automatically**.

## Interpretation

These intervals measure elapsed wall-clock time between calls to the guest
flip profiling boundary. They do not directly measure GPU execution time,
Vulkan present latency, or the actual display refresh cadence. Frame pacing
and GPU timings require additional instrumentation.

## Validation

- `zig build -Doptimize=ReleaseSafe`
- `zig build test-vulkan -Doptimize=ReleaseSafe`
- `python -m unittest discover -s tests -p 'test_profile_analyze.py' -v`

Do not claim a performance improvement until matched before/after captures
are available from the same game, scene, hardware and settings.
