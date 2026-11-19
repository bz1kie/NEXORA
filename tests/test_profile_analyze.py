"""Unit tests for the standalone frame-time analyzer."""

import csv
from pathlib import Path
import tempfile
import unittest

from tools.profile_analyze import analyze, percentile


class AnalyzerTests(unittest.TestCase):
    def write_capture(self, values):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        path = Path(temporary.name) / "capture.csv"
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle)
            writer.writerow(["frame_ms"])
            for value in values:
                writer.writerow([value])
        return path

    def test_constant_60fps(self):
        result = analyze(self.write_capture([1000 / 60] * 100))
        self.assertEqual(result["frames"], 100)
        self.assertAlmostEqual(result["average_fps"], 60.0, delta=0.001)
        self.assertAlmostEqual(result["p99_frame_ms"], 1000 / 60, delta=0.001)

    def test_rejects_invalid_samples(self):
        result = analyze(self.write_capture(["", "bad", -1, 0, "nan", 20]))
        self.assertEqual(result["frames"], 1)
        self.assertEqual(result["average_fps"], 50.0)

    def test_missing_header(self):
        with self.assertRaisesRegex(ValueError, "frame_ms"):
            path = self.write_capture([1])
            path.write_text("other\n1\n", encoding="utf-8")
            analyze(path)

    def test_percentile_interpolates(self):
        self.assertEqual(percentile([10, 20, 30], 50), 20)


if __name__ == "__main__":
    unittest.main()
