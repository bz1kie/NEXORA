// SPDX-License-Identifier: GPL-3.0-or-later
//! Allocation-free frame interval recorder for the NEXORA Vulkan boundary.
//! A timestamp must be taken at the same presentation event for each frame.
const std = @import("std");

pub const FrameSampler = struct {
    pub const capacity = 4096;
    intervals_ns: [capacity]u64 = undefined,
    count: usize = 0,
    next: usize = 0,
    last_ns: ?u64 = null,

    pub fn note(self: *FrameSampler, timestamp_ns: u64) void {
        const previous = self.last_ns orelse {
            self.last_ns = timestamp_ns;
            return;
        };
        if (timestamp_ns <= previous) return;
        self.last_ns = timestamp_ns;
        self.intervals_ns[self.next] = timestamp_ns - previous;
        self.next = (self.next + 1) % capacity;
        if (self.count < capacity) self.count += 1;
    }

    pub fn interval(self: *const FrameSampler, index: usize) ?u64 {
        if (index >= self.count) return null;
        const start = if (self.count == capacity) self.next else 0;
        return self.intervals_ns[(start + index) % capacity];
    }

    /// Writes a CSV compatible with tools/profile_analyze.py.
    pub fn writeCsv(self: *const FrameSampler, writer: anytype) !void {
        try writer.writeAll("frame_ms\n");
        for (0..self.count) |i| {
            const ns = self.interval(i).?;
            try writer.print("{d}.{d:0>6}\n", .{ ns / std.time.ns_per_ms, ns % std.time.ns_per_ms });
        }
    }
};

test "first frame is a baseline and next frame records elapsed time" {
    var sampler: FrameSampler = .{};
    sampler.note(1_000_000);
    try std.testing.expectEqual(@as(usize, 0), sampler.count);
    sampler.note(17_000_000);
    try std.testing.expectEqual(@as(u64, 16_000_000), sampler.interval(0).?);
}

test "non-monotonic timestamps are not recorded" {
    var sampler: FrameSampler = .{};
    sampler.note(100);
    sampler.note(90);
    sampler.note(110);
    try std.testing.expectEqual(@as(u64, 20), sampler.interval(0).?);
}

test "backward timestamps do not distort the next valid interval" {
    var sampler: FrameSampler = .{};
    sampler.note(1_000_000);
    sampler.note(900_000);
    sampler.note(17_000_000);
    try std.testing.expectEqual(@as(usize, 1), sampler.count);
    try std.testing.expectEqual(@as(u64, 16_000_000), sampler.interval(0).?);
}

test "ring buffer retains the newest samples in chronological order" {
    var sampler: FrameSampler = .{};
    sampler.note(1);
    for (0..FrameSampler.capacity + 3) |i| sampler.note(@intCast(i + 2));
    try std.testing.expectEqual(@as(usize, FrameSampler.capacity), sampler.count);
    try std.testing.expectEqual(@as(u64, 1), sampler.interval(0).?);
    try std.testing.expectEqual(@as(u64, 1), sampler.interval(FrameSampler.capacity - 1).?);
}
