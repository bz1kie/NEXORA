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

    pub const Summary = struct {
        samples: usize,
        average_ns: u64,
        min_ns: u64,
        max_ns: u64,
        p95_ns: u64,
        p99_ns: u64,
        frames_over_33ms: usize,
        frames_over_50ms: usize,
    };

    /// Computes robust frame pacing metrics without allocations.
    pub fn summarize(self: *const FrameSampler) ?Summary {
        if (self.count == 0) return null;
        var sorted: [capacity]u64 = undefined;
        var total: u128 = 0;
        var minimum: u64 = std.math.maxInt(u64);
        var maximum: u64 = 0;
        var over_33ms: usize = 0;
        var over_50ms: usize = 0;
        for (0..self.count) |i| {
            const value = self.interval(i).?;
            sorted[i] = value;
            total += value;
            minimum = @min(minimum, value);
            maximum = @max(maximum, value);
            if (value > 33_333_333) over_33ms += 1;
            if (value > 50_000_000) over_50ms += 1;
        }
        std.mem.sort(u64, sorted[0..self.count], {}, std.sort.asc(u64));
        const p95_index = (self.count * 95 + 99) / 100 - 1;
        const p99_index = (self.count * 99 + 99) / 100 - 1;
        return .{
            .samples = self.count,
            .average_ns = @intCast(total / self.count),
            .min_ns = minimum,
            .max_ns = maximum,
            .p95_ns = sorted[p95_index],
            .p99_ns = sorted[p99_index],
            .frames_over_33ms = over_33ms,
            .frames_over_50ms = over_50ms,
        };
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
    try std.testing.expectEqual(@as(u64, 10), sampler.interval(0).?);
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

test "summary calculates average and percentile frame time" {
    var sampler: FrameSampler = .{};
    sampler.note(1);
    sampler.note(11);
    sampler.note(31);
    sampler.note(61);
    sampler.note(101);
    const summary = sampler.summarize().?;
    try std.testing.expectEqual(@as(usize, 4), summary.samples);
    try std.testing.expectEqual(@as(u64, 25), summary.average_ns);
    try std.testing.expectEqual(@as(u64, 10), summary.min_ns);
    try std.testing.expectEqual(@as(u64, 40), summary.max_ns);
    try std.testing.expectEqual(@as(u64, 40), summary.p95_ns);
    try std.testing.expectEqual(@as(u64, 40), summary.p99_ns);
}

test "empty sampler has no summary" {
    const sampler: FrameSampler = .{};
    try std.testing.expect(sampler.summarize() == null);
}

test "frame pacing counts slow frames at strict thresholds" {
    var sampler: FrameSampler = .{};
    sampler.note(1);
    sampler.note(16_000_001);
    sampler.note(49_333_334);
    sampler.note(99_333_334);
    sampler.note(159_333_335);
    const summary = sampler.summarize().?;
    try std.testing.expectEqual(@as(usize, 2), summary.frames_over_33ms);
    try std.testing.expectEqual(@as(usize, 1), summary.frames_over_50ms);
}
