#!/usr/bin/env python3
# Copyright (C) 2026 Araragi234
# SPDX-License-Identifier: GPL-3.0-or-later
"""Built-in Pillow-generated animations."""

import random
from PIL import Image, ImageDraw


class Starfield:
    """A deterministic starfield with stars moving toward the viewer."""

    def __init__(self, star_count: int = 100):
        rng = random.Random(42)
        self.stars = [(rng.uniform(-1, 1), rng.uniform(-1, 1), rng.random()) for _ in range(star_count)]

    def render(self, width: int, height: int, frame: int, background: tuple[int, int, int]):
        image = Image.new("RGB", (width, height), background)
        draw = ImageDraw.Draw(image)
        cx, cy = width / 2, height / 2
        for x, y, initial_depth in self.stars:
            depth = (initial_depth - frame * 0.008) % 1.0
            depth = max(depth, 0.025)
            screen_x = cx + (x / depth) * width * 0.12
            screen_y = cy + (y / depth) * height * 0.12
            if not (0 <= screen_x < width and 0 <= screen_y < height):
                continue
            brightness = int(100 + (1 - depth) * 155)
            color = (brightness, brightness, min(255, brightness + 15))
            radius = max(1, int((1 - depth) * 2.5))
            draw.ellipse((screen_x - radius, screen_y - radius, screen_x + radius, screen_y + radius), fill=color)
        return image
