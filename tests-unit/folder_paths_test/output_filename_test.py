"""Tests for folder_paths.format_output_filename and get_timestamp functions."""

import sys
import os
import unittest

# Add the ComfyUI root to the path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import folder_paths


class TestGetTimestamp(unittest.TestCase):
    """Tests for get_timestamp function."""

    def test_returns_string(self):
        """Should return a string."""
        result = folder_paths.get_timestamp()
        self.assertIsInstance(result, str)

    def test_format_matches_expected_pattern(self):
        """Should return format YYYYMMDD-HHMMSS-ffffff."""
        result = folder_paths.get_timestamp()
        # Pattern: 8 digits, hyphen, 6 digits, hyphen, 6 digits
        pattern = r"^\d{8}-\d{6}-\d{6}$"
        self.assertRegex(result, pattern)

    def test_is_filesystem_safe(self):
        """Should not contain characters that are unsafe for filenames."""
        result = folder_paths.get_timestamp()
        unsafe_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|', ' ']
        for char in unsafe_chars:
            self.assertNotIn(char, result)


class TestFormatOutputFilename(unittest.TestCase):
    """Tests for format_output_filename function."""

    def test_basic_format(self):
        """Should format filename with counter and timestamp."""
        result = folder_paths.format_output_filename("test", 1, "png")
        # Pattern: test_00001_YYYYMMDD-HHMMSS-ffffff_.png
        pattern = r"^test_00001_\d{8}-\d{6}-\d{6}_\.png$"
        self.assertRegex(result, pattern)

    def test_counter_padding(self):
        """Should pad counter to 5 digits."""
        result = folder_paths.format_output_filename("test", 42, "png")
        self.assertIn("_00042_", result)

    def test_extension_with_leading_dot(self):
        """Should handle extension with leading dot."""
        result = folder_paths.format_output_filename("test", 1, ".png")
        self.assertTrue(result.endswith("_.png"))
        self.assertNotIn("..png", result)

    def test_extension_without_leading_dot(self):
        """Should handle extension without leading dot."""
        result = folder_paths.format_output_filename("test", 1, "webm")
        self.assertTrue(result.endswith("_.webm"))

    def test_batch_num_replacement(self):
        """Should replace %batch_num% placeholder."""
        result = folder_paths.format_output_filename("test_%batch_num%", 1, "png", batch_num="3")
        self.assertIn("test_3_", result)
        self.assertNotIn("%batch_num%", result)

    def test_custom_timestamp(self):
        """Should use provided timestamp instead of generating one."""
        custom_ts = "20260101-120000-000000"
        result = folder_paths.format_output_filename("test", 1, "png", timestamp=custom_ts)
        self.assertIn(custom_ts, result)

    def test_different_extensions(self):
        """Should work with various extensions."""
        extensions = ["png", "webp", "webm", "svg", "glb", "safetensors", "latent"]
        for ext in extensions:
            result = folder_paths.format_output_filename("test", 1, ext)
            self.assertTrue(result.endswith(f"_.{ext}"))


if __name__ == "__main__":
    unittest.main()
