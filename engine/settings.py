#!/usr/bin/env python3
# Copyright (C) 2026 Araragi234
# SPDX-License-Identifier: GPL-3.0-or-later
"""Persistent settings and per-user data paths for terminal-animations."""

from __future__ import annotations

import json
import os
import shutil
from pathlib import Path

CONFIG_DIR = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config")) / "terminal-animations"
SETTINGS_FILE = CONFIG_DIR / "settings.json"
DATA_DIR = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share")) / "terminal-animations"
GIF_DIR = DATA_DIR / "gifs"


def get_data_dir() -> Path:
    """Return the user's writable application data directory."""
    return DATA_DIR


def get_gif_dir() -> Path:
    """Return the GIF library, migrating the old in-project library once."""
    legacy_dir = Path(__file__).resolve().parent.parent / "animations" / "gifs"
    if legacy_dir.is_dir() and legacy_dir.resolve() != GIF_DIR.resolve():
        existing = [p for p in legacy_dir.iterdir() if p.is_file() and p.suffix.lower() == ".gif"]
        if existing:
            GIF_DIR.mkdir(parents=True, exist_ok=True)
            for source in existing:
                destination = GIF_DIR / source.name
                if not destination.exists():
                    try:
                        shutil.copy2(source, destination)
                    except OSError:
                        # Keep using the normal data path; a failed migration is
                        # non-fatal and can be retried after fixing permissions.
                        pass
    GIF_DIR.mkdir(parents=True, exist_ok=True)
    return GIF_DIR


def load_settings() -> dict:
    if not SETTINGS_FILE.exists():
        return {}
    try:
        with SETTINGS_FILE.open("r", encoding="utf-8") as file:
            settings = json.load(file)
        return settings if isinstance(settings, dict) else {}
    except (OSError, json.JSONDecodeError):
        return {}


def save_settings(settings: dict) -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    temporary_file = SETTINGS_FILE.with_suffix(".tmp")
    with temporary_file.open("w", encoding="utf-8") as file:
        json.dump(settings, file, indent=4)
        file.write("\n")
    temporary_file.replace(SETTINGS_FILE)


def set_default_animation(animation_type: str, identifier: str) -> None:
    if animation_type not in ("builtin", "gif", "random"):
        raise ValueError("Animation type must be 'builtin', 'gif', or 'random'.")
    if not identifier:
        raise ValueError("An animation identifier is required.")
    if animation_type == "gif":
        identifier = str(Path(identifier).expanduser().resolve())
    settings = load_settings()
    settings["default_animation"] = {"type": animation_type, "identifier": identifier}
    save_settings(settings)


def get_default_animation():
    return load_settings().get("default_animation")


def clear_default_animation() -> None:
    settings = load_settings()
    settings.pop("default_animation", None)
    save_settings(settings)
