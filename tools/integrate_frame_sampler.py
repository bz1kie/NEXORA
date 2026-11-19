#!/usr/bin/env python3
"""One-time, checked insertion of the NEXORA frame sampler into Vulkan flip profiling."""
from pathlib import Path

path = Path("src/vulkan/backend.zig")
source = path.read_text(encoding="utf-8")
replacements = [
    (
        "    frame_rate_counter: FrameRateCounter = .{},",
        "    frame_rate_counter: FrameRateCounter = .{},\n"
        "    nexora_frame_sampler: @import(\"frame_sampler.zig\").FrameSampler = .{},",
    ),
    (
        "    /// Selects the registered display-buffer allocation named by a flip.",
        "    /// Export captured guest flip intervals as frame_ms CSV.\n"
        "    pub fn writeNexoraFrameCsv(self: *const Renderer, writer: anytype) !void {\n"
        "        try self.nexora_frame_sampler.writeCsv(writer);\n"
        "    }\n\n"
        "    /// Selects the registered display-buffer allocation named by a flip.",
    ),
    (
        "        const now = hostTimestampNs();\n"
        "        if (self.frame_rate_sink) |sink| {",
        "        const now = hostTimestampNs();\n"
        "        if (now != 0) self.nexora_frame_sampler.note(now);\n"
        "        if (self.frame_rate_sink) |sink| {",
    ),
]
for before, after in replacements:
    if after in source:
        continue
    occurrences = source.count(before)
    if occurrences != 1:
        raise SystemExit(f"Expected exactly one anchor, found {occurrences}: {before!r}")
    source = source.replace(before, after, 1)
path.write_text(source, encoding="utf-8")
print("Integrated NEXORA frame sampling into reportFrameProfile")
