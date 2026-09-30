"""Tiny synthetic clips for the frame and seam tests."""

from __future__ import annotations

from pathlib import Path

import av
import numpy as np


def canvas(width: int = 1920, height: int = 1080) -> np.ndarray:
    return np.full((height, width, 3), 255, dtype=np.uint8)


def with_square(img: np.ndarray, x: int, y: int, size: int = 120, value: int = 30) -> np.ndarray:
    out = img.copy()
    out[y : y + size, x : x + size] = value
    return out


def write_clip(path: Path, frames: list[np.ndarray], fps: int = 15) -> Path:
    height, width = frames[0].shape[:2]
    with av.open(str(path), "w") as container:
        stream = container.add_stream("libx264", rate=fps)
        stream.width, stream.height, stream.pix_fmt = width, height, "yuv420p"
        stream.options = {"crf": "12"}
        for img in frames:
            for packet in stream.encode(av.VideoFrame.from_ndarray(img, format="rgb24")):
                container.mux(packet)
        for packet in stream.encode():
            container.mux(packet)
    return path
