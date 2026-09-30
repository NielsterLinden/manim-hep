"""``manim-hep seam A.mp4 B.mp4``: does clip B start exactly where clip A ended?

Compares A's last frame with B's first frame at 1920×1080. Thresholds were
calibrated on real chained 1080p clips: joints that look seamless measure a mean
difference of 0.2–0.6 and no blobs, while a misplaced object scores blobs in the
hundreds. H.264 ringing on glyph edges never fills a whole 5×5 window.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from manim_hep.cli.frames import scan, to_1080p

PIXEL_THRESHOLD = 24  # max over RGB of |difference|, on a 0–255 scale
MEAN_LIMIT = 1.0
FRACTION_LIMIT = 0.5  # percent of pixels over the threshold
BLOB_LIMIT = 50
BLOB_SIZE = 5


@dataclass(frozen=True)
class SeamResult:
    mean: float
    max: int
    fraction: float  # percent
    blobs: int

    @property
    def ok(self) -> bool:
        return (
            self.mean <= MEAN_LIMIT and self.fraction <= FRACTION_LIMIT and self.blobs <= BLOB_LIMIT
        )

    def describe(self) -> str:
        verdict = "OK" if self.ok else "FAIL"
        return (
            f"mean|d|={self.mean:.3f}  max|d|={self.max}  "
            f"over{PIXEL_THRESHOLD}={self.fraction:.3f}%  blobs={self.blobs}  -> {verdict}"
        )


def seam_metrics(a: np.ndarray, b: np.ndarray) -> SeamResult:
    """Compare two RGB frames (any 16:9 size; judged at 1080p)."""
    a, b = to_1080p(a), to_1080p(b)
    d = np.abs(a.astype(np.int16) - b.astype(np.int16)).max(axis=2)
    over = d > PIXEL_THRESHOLD
    integral = np.pad(over.astype(np.int32).cumsum(0).cumsum(1), ((1, 0), (1, 0)))
    k = BLOB_SIZE
    window = integral[k:, k:] - integral[:-k, k:] - integral[k:, :-k] + integral[:-k, :-k]
    return SeamResult(
        mean=float(d.mean()),
        max=int(d.max()),
        fraction=float(over.mean() * 100),
        blobs=int((window == k * k).sum()),
    )


def check(a_path: Path, b_path: Path) -> SeamResult:
    last = scan(a_path).frames["last"]
    first = scan(b_path).frames["first"]
    return seam_metrics(last, first)


def run(args: argparse.Namespace) -> int:
    a, b = Path(args.a), Path(args.b)
    for path in (a, b):
        if not path.is_file():
            print(f"error: {path} not found")
            return 2
    try:
        result = check(a, b)
    except ValueError as err:
        print(f"error: {err}")
        return 2
    print(f"seam {a.name} -> {b.name}: {result.describe()}")
    return 0 if result.ok else 1


def add_parser(sub) -> None:
    p = sub.add_parser(
        "seam",
        help="check that clip B starts on clip A's last frame",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("a", help="the earlier clip (its last frame is compared)")
    p.add_argument("b", help="the later clip (its first frame is compared)")
    p.set_defaults(func=run)
