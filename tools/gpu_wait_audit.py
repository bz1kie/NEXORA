#!/usr/bin/env python3
"""Static inventory of likely blocking GPU synchronization sites.

This is a source-code audit, NOT a runtime GPU profiler. Counts are
candidate sites and must be manually reviewed for semantics.
"""
import argparse
import json
from pathlib import Path
import re

PATTERNS = {
    "vulkan_fence_wait": re.compile(r"\b(?:vkWaitForFences|waitForFences|wait_for_fences)\b", re.I),
    "vulkan_idle_wait": re.compile(r"\b(?:vkDeviceWaitIdle|vkQueueWaitIdle|deviceWaitIdle|queueWaitIdle|wait_idle)\b", re.I),
    "host_condition_wait": re.compile(r"\b(?:Condition|condition_variable|waitForSingleObject|WaitForSingleObject)\b"),
    "host_thread_join": re.compile(r"\b(?:pthread_join|WaitForMultipleObjects)\b"),
}
EXTENSIONS = {".zig", ".c", ".cc", ".cpp", ".h", ".hpp"}
MAX_MATCHES = 10000


def audit(root: Path):
    if not root.is_dir():
        raise ValueError(f"Not a directory: {root}")
    matches = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix not in EXTENSIONS:
            continue
        if any(part in {".git", "zig-cache", "zig-out", "node_modules", "vendor", "third_party", "3rdparty"} for part in path.parts):
            continue
        for lineno, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            if line.lstrip().startswith(("//", "/*", "*", "#")):
                continue
            for category, pattern in PATTERNS.items():
                if pattern.search(line):
                    matches.append({"file": path.relative_to(root).as_posix(), "line": lineno, "category": category})
                    if len(matches) >= MAX_MATCHES:
                        raise ValueError("Too many candidate sites; narrow the audit root")
    return {"root": str(root), "candidate_count": len(matches), "candidates": matches,
            "note": "Static matches are not measured waits; inspect call sites and instrument runtime durations."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path("src"))
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    result = json.dumps(audit(args.root), indent=2)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(result + "\n", encoding="utf-8")
    print(result)


if __name__ == "__main__":
    main()
