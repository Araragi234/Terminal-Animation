#!/usr/bin/env python3
# Copyright (C) 2026 Araragi234
# SPDX-License-Identifier: GPL-3.0-or-later
"""Decode animated GIFs into resized RGB frames."""

from PIL import Image, ImageSequence


def load_gif(path, max_width: int, max_height: int, background: tuple[int, int, int]):
    frames = []
    with Image.open(path) as gif:
        for frame in ImageSequence.Iterator(gif):
            image = frame.convert("RGBA").copy()
            image.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
            canvas = Image.new("RGBA", image.size, (*background, 255))
            image = Image.alpha_composite(canvas, image).convert("RGB")
            duration = frame.info.get("duration", gif.info.get("duration", 100))
            frames.append((image, max(20, duration) / 1000))
    if not frames:
        raise ValueError("The GIF contains no frames.")
    return frames
