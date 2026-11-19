#!/usr/bin/env python3
"""Summarize NEXORA frame-time CSV captures using the Python standard library."""

import argparse
import csv
import json
import math
from pathlib import Path
import statistics


def percentile(values, percent):
    samples = sorted(values)
    if not samples:
        raise ValueError("No valid frame samples")
    position = (len(samples) - 1) * percent / 100
    low, high = math.floor(position), math.ceil(position)
    return samples[low] + (samples[high] - samples[low]) * (position - low)


def analyze(path):
    path = Path(path)
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames or "frame_ms" not in reader.fieldnames:
            raise ValueError("CSV requires a frame_ms column")
        frames = []
        for row in reader:
            try:
                frame_ms = float(row["frame_ms"])
            except (ValueError, TypeError):
                continue
            if math.isfinite(frame_ms) and frame_ms > 0:
                frames.append(frame_ms)

    if not frames:
        raise ValueError("No valid frame samples")

    capture_seconds = sum(frames) / 1000.0
    slowest_one_percent = sorted(frames, reverse=True)[:max(1, math.ceil(len(frames) * 0.01))]
    return {
        "source": str(path),
        "frames": len(frames),
        "capture_seconds": round(capture_seconds, 3),
        "average_fps": round(len(frames) / capture_seconds, 3),
        "average_frame_ms": round(statistics.mean(frames), 3),
        "median_frame_ms": round(statistics.median(frames), 3),
        "p95_frame_ms": round(percentile(frames, 95), 3),
        "p99_frame_ms": round(percentile(frames, 99), 3),
        "one_percent_low_fps": round(1000 / statistics.mean(slowest_one_percent), 3),
        "frames_over_33ms": sum(ms > 33.333333 for ms in frames),
        "frames_over_50ms": sum(ms > 50.0 for ms in frames),
        "stutter_over_33ms_percent": round(100 * sum(ms > 33.333333 for ms in frames) / len(frames), 3),
        "stutter_over_50ms_percent": round(100 * sum(ms > 50.0 for ms in frames) / len(frames), 3),
    }


def main():
    parser = argparse.ArgumentParser(description="Analyze a NEXORA frame-time CSV capture")
    parser.add_argument("csv_file", type=Path)
    parser.add_argument("--out", type=Path, help="Save JSON summary")
    args = parser.parse_args()
    report = json.dumps(analyze(args.csv_file), indent=2, ensure_ascii=False)
    print(report)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(report + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
