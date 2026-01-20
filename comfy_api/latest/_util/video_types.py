from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from fractions import Fraction
from typing import Optional
from .._input import ImageInput, AudioInput

class VideoCodec(str, Enum):
    AUTO = "auto"
    H264 = "h264"
    VP9 = "vp9"

    @classmethod
    def as_input(cls) -> list[str]:
        """
        Returns a list of codec names that can be used as node input.
        """
        return [member.value for member in cls]


class VideoContainer(str, Enum):
    AUTO = "auto"
    MP4 = "mp4"
    WEBM = "webm"

    @classmethod
    def as_input(cls) -> list[str]:
        """
        Returns a list of container names that can be used as node input.
        """
        return [member.value for member in cls]

    @classmethod
    def get_extension(cls, value) -> str:
        """
        Returns the file extension for the container.
        """
        if isinstance(value, str):
            value = cls(value)
        if value == VideoContainer.MP4 or value == VideoContainer.AUTO:
            return "mp4"
        if value == VideoContainer.WEBM:
            return "webm"
        return ""


class VideoSpeedPreset(str, Enum):
    """Encoding speed presets - slower = better compression at same quality."""
    AUTO = "auto"
    FASTEST = "Fastest"
    FAST = "Fast"
    BALANCED = "Balanced"
    QUALITY = "Quality"
    BEST = "Best"

    @classmethod
    def as_input(cls) -> list[str]:
        return [member.value for member in cls]

    def to_ffmpeg_preset(self, codec: str = "h264") -> str:
        """Convert to FFmpeg preset string for the given codec."""
        h264_map = {
            VideoSpeedPreset.FASTEST: "ultrafast",
            VideoSpeedPreset.FAST: "veryfast",
            VideoSpeedPreset.BALANCED: "medium",
            VideoSpeedPreset.QUALITY: "slow",
            VideoSpeedPreset.BEST: "veryslow",
            VideoSpeedPreset.AUTO: "medium",
        }
        vp9_map = {
            VideoSpeedPreset.FASTEST: "0",
            VideoSpeedPreset.FAST: "1",
            VideoSpeedPreset.BALANCED: "2",
            VideoSpeedPreset.QUALITY: "3",
            VideoSpeedPreset.BEST: "4",
            VideoSpeedPreset.AUTO: "2",
        }
        if codec in ("vp9", "libvpx-vp9"):
            return vp9_map.get(self, "2")
        return h264_map.get(self, "medium")


def quality_to_crf(quality: int, codec: str = "h264") -> int:
    """
    Map 0-100 quality percentage to codec-appropriate CRF value.

    Args:
        quality: 0-100 where 100 is best quality
        codec: The codec being used (h264, vp9, etc.)

    Returns:
        CRF value appropriate for the codec
    """
    quality = max(0, min(100, quality))

    if codec in ("h264", "libx264"):
        # h264: CRF 0-51 (lower = better), typical range 12-40
        # quality 100 → CRF 12, quality 0 → CRF 40
        return int(40 - (quality / 100) * 28)
    elif codec in ("vp9", "libvpx-vp9"):
        # vp9: CRF 0-63 (lower = better), typical range 15-50
        # quality 100 → CRF 15, quality 0 → CRF 50
        return int(50 - (quality / 100) * 35)
    # Default fallback
    return 23

@dataclass
class VideoComponents:
    """
    Dataclass representing the components of a video.
    """

    images: ImageInput
    frame_rate: Fraction
    audio: Optional[AudioInput] = None
    metadata: Optional[dict] = None


