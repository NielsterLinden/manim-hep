"""Reading frames from rendered clips with PyAV (no separate ffmpeg needed)."""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

FRAME_HEIGHT = 8.0  # Manim scene units
FRAME_WIDTH = 8.0 * 16 / 9
INK_DIFFERENCE = 30  # a pixel is "ink" when a channel differs this much from the background


@dataclass
class Scan:
    """What one pass over a clip found."""

    frames: dict[str, np.ndarray]
    width: int
    height: int
    fps: float
    count: int
    duration: float
    background: np.ndarray
    worst: dict[str, tuple[float, float]] = field(default_factory=dict)  # region -> (frac, t)


def time_key(t: float) -> str:
    return f"t{t:g}"


def to_1080p(img: np.ndarray) -> np.ndarray:
    """Resize a 16:9 frame to 1920×1080; other aspect ratios are an error."""
    h, w = img.shape[:2]
    if (w, h) == (1920, 1080):
        return img
    if abs(w / h - 16 / 9) > 0.01:
        raise ValueError(f"expected a 16:9 frame, got {w}x{h}")
    from PIL import Image

    return np.asarray(Image.fromarray(img).resize((1920, 1080), Image.Resampling.BICUBIC))


def _background(img: np.ndarray) -> np.ndarray:
    corners = [img[:8, :8], img[:8, -8:], img[-8:, :8], img[-8:, -8:]]
    return np.median(np.concatenate([c.reshape(-1, 3) for c in corners]), axis=0)


def region_pixels(
    img_shape: Sequence[int], box: tuple[float, float, float, float]
) -> tuple[slice, slice]:
    """Pixel rows and columns of a scene-unit box (x0, y0, x1, y1)."""
    h, w = img_shape[:2]
    x0, y0, x1, y1 = box

    def col(x: float) -> int:
        return round((x + FRAME_WIDTH / 2) / FRAME_WIDTH * w)

    def row(y: float) -> int:
        return round((FRAME_HEIGHT / 2 - y) / FRAME_HEIGHT * h)

    return slice(max(row(y1), 0), min(row(y0), h)), slice(max(col(x0), 0), min(col(x1), w))


def ink_fraction(img: np.ndarray, box: tuple[float, float, float, float], background) -> float:
    rows, cols = region_pixels(img.shape, box)
    region = img[rows, cols].astype(np.int16)
    if region.size == 0:
        return 0.0
    diff = np.abs(region - np.asarray(background, dtype=np.int16)).max(axis=2)
    return float((diff > INK_DIFFERENCE).mean())


def scan(
    path: str | Path,
    times: Iterable[float] = (),
    regions: dict[str, tuple[float, float, float, float]] | None = None,
    step: int = 1,
) -> Scan:
    """Decode a clip once: first, last and requested frames, and the worst ink in regions.

    A requested time gives the frame on screen at that moment (past the end: the
    last frame). ``regions`` are scene-unit boxes checked on every ``step``-th frame
    and on the last one.
    """
    import av

    pending = sorted(float(t) for t in times)
    frames: dict[str, np.ndarray] = {}
    worst: dict[str, tuple[float, float]] = {name: (0.0, 0.0) for name in regions or {}}
    previous = None
    background = None
    count = 0
    t = 0.0
    with av.open(str(path)) as container:
        stream = container.streams.video[0]
        fps = float(stream.average_rate or 0) or 0.0
        width, height = stream.codec_context.width, stream.codec_context.height
        for frame in container.decode(stream):
            t = float(frame.time or 0.0)
            img = frame.to_ndarray(format="rgb24")
            if previous is None:
                frames["first"] = img
                background = _background(img)
            while pending and t > pending[0] + 1e-9:
                frames[time_key(pending.pop(0))] = previous if previous is not None else img
            if regions and count % step == 0:
                _update_worst(worst, regions, img, background, t)
            previous = img
            count += 1
    if previous is None:
        raise ValueError(f"{path} contains no video frames")
    frames["last"] = previous
    for leftover in pending:
        frames[time_key(leftover)] = previous
    if regions:
        _update_worst(worst, regions, previous, background, t)
    duration = count / fps if fps else t
    return Scan(frames, width, height, fps, count, duration, background, worst)


def _update_worst(worst, regions, img, background, t) -> None:
    for name, box in regions.items():
        fraction = ink_fraction(img, box, background)
        if fraction > worst[name][0]:
            worst[name] = (fraction, t)


def save_png(img: np.ndarray, path: str | Path) -> Path:
    from PIL import Image

    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(img).save(out)
    return out
