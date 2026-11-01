#!/usr/bin/env python3
# Copyright (C) 2026 Araragi234
# SPDX-License-Identifier: GPL-3.0-or-later
"""Truecolor half-block image rendering and terminal background detection."""

from __future__ import annotations

import os
import re
import select
import sys
import time

FALLBACK_BACKGROUND = (0, 0, 0)


def detect_background(stdin_fd: int) -> tuple[int, int, int]:
    """Query the terminal background using OSC 11; use black if unsupported."""
    sys.stdout.write("\033]11;?\033\\")
    sys.stdout.flush()
    response = bytearray()
    deadline = time.monotonic() + 0.5
    pattern = re.compile(
        rb"\x1b\]11;rgb:([0-9a-fA-F]{1,4})/([0-9a-fA-F]{1,4})/([0-9a-fA-F]{1,4})"
    )
    while time.monotonic() < deadline:
        readable, _, _ = select.select([stdin_fd], [], [], 0.05)
        if not readable:
            continue
        response.extend(os.read(stdin_fd, 256))
        match = pattern.search(response)
        if match:
            rgb = []
            for component in match.groups():
                value = int(component, 16)
                maximum = (1 << (4 * len(component))) - 1
                rgb.append(round(value * 255 / maximum))
            return tuple(rgb)
    return FALLBACK_BACKGROUND


def render_image(image, background: tuple[int, int, int]) -> list[str]:
    """Convert an RGB PIL image to terminal rows using upper-half blocks."""
    image = image.convert("RGB")
    width, height = image.size
    pixels = image.load()
    lines = []
    for y in range(0, height, 2):
        line = []
        for x in range(width):
            top = pixels[x, y]
            bottom = pixels[x, y + 1] if y + 1 < height else background
            line.append(
                f"\033[38;2;{top[0]};{top[1]};{top[2]}m"
                f"\033[48;2;{bottom[0]};{bottom[1]};{bottom[2]}m▀"
            )
        line.append("\033[0m")
        lines.append("".join(line))
    return lines
