"""Tests for the source-level GPU wait inventory."""
import tempfile
from pathlib import Path
import unittest

from tools.gpu_wait_audit import audit


class WaitAuditTests(unittest.TestCase):
    def test_detects_sites_without_comment_false_positives(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "backend.zig").write_text(
                "// vkWaitForFences in a comment\n"
                "const result = vkWaitForFences(device, 1, fences, 1, timeout);\n"
                "vkQueueWaitIdle(queue);\n"
                "some_other_call();\n", encoding="utf-8")
            result = audit(root)
            self.assertEqual(result["candidate_count"], 2)
            self.assertEqual([x["line"] for x in result["candidates"]], [2, 3])
            self.assertEqual(result["candidates"][0]["category"], "vulkan_fence_wait")

    def test_zig_condition_wait(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "queue.zig").write_text("condition.wait(&mutex);\\n", encoding="utf-8")
            result = audit(root)
            self.assertEqual(result["candidate_count"], 1)
            self.assertEqual(result["candidates"][0]["category"], "zig_condition_wait")

    def test_empty_tree(self):
        with tempfile.TemporaryDirectory() as temp:
            self.assertEqual(audit(Path(temp))["candidate_count"], 0)

    def test_missing_directory(self):
        with self.assertRaises(ValueError):
            audit(Path("/definitely/nonexistent/nexora/wait/audit"))


if __name__ == "__main__":
    unittest.main()
