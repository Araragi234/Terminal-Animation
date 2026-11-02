#!/usr/bin/env python3
# Copyright (C) 2026 Araragi234
# SPDX-License-Identifier: GPL-3.0-or-later
"""Import GIFs and choose the default animation for terminal-animations."""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

from PIL import Image

from engine.settings import get_default_animation, set_default_animation, clear_default_animation, get_gif_dir

GIF_DIR = get_gif_dir()


def gif_files() -> list[Path]:
    GIF_DIR.mkdir(parents=True, exist_ok=True)
    return sorted((p for p in GIF_DIR.iterdir() if p.is_file() and p.suffix.lower() == ".gif"),
                  key=lambda p: p.name.casefold())


def copy_gif(source: Path) -> Path:
    if not source.is_file():
        raise FileNotFoundError(source)
    if source.suffix.lower() != ".gif":
        raise ValueError("file extension must be .gif")
    with Image.open(source) as image:
        if image.format != "GIF":
            raise ValueError("file contents are not GIF format")
        image.verify()

    GIF_DIR.mkdir(parents=True, exist_ok=True)
    destination = GIF_DIR / source.name
    stem, suffix = destination.stem, destination.suffix
    number = 1
    while destination.exists() and source.resolve() != destination.resolve():
        destination = GIF_DIR / f"{stem}_{number}{suffix}"
        number += 1
    if source.resolve() != destination.resolve():
        shutil.copy2(source, destination)
    return destination


def import_gifs(sources: list[str]) -> int:
    imported = 0
    for raw in sources:
        source = Path(raw).expanduser()
        try:
            destination = copy_gif(source)
        except (OSError, ValueError) as error:
            print(f"Couldn't import {source}: {error}", file=sys.stderr)
            continue
        print(f"Imported: {destination.name}")
        imported += 1
    return imported


def show_animations() -> list[tuple[str, str, str]]:
    items = [("Starfield (built-in)", "builtin", "starfield")]
    items.extend((path.name, "gif", str(path.resolve())) for path in gif_files())
    return items


def print_list() -> None:
    default = get_default_animation() or {"type": "builtin", "identifier": "starfield"}
    print("Available animations:")
    print("  Starfield (built-in)")
    for path in gif_files():
        print(f"  {path.name}")
    print("  Random (choose a different animation on each Fastfetch run)")
    print()
    if default.get("type") == "random":
        current = "Random"
    elif default.get("type") == "builtin":
        current = "Starfield (built-in)"
    else:
        current = Path(default.get("identifier", "")).name
    print(f"Default: {current}")


def set_named_default(value: str) -> None:
    normalized = value.strip()
    if normalized.casefold() in {"random", "shuffle"}:
        set_default_animation("random", "all")
        print("Default animation set to Random. A selection will be made for each Fastfetch run.")
        return
    if normalized.casefold() in {"starfield", "builtin", "default"}:
        set_default_animation("builtin", "starfield")
        print("Default animation set to Starfield.")
        return

    candidate = Path(normalized).expanduser()
    if candidate.is_file():
        try:
            candidate = copy_gif(candidate)
        except (OSError, ValueError) as error:
            raise SystemExit(f"Couldn't use {candidate}: {error}")
    else:
        # Accept a library filename without requiring its full path.
        candidate = GIF_DIR / normalized
    if not candidate.is_file() or candidate.suffix.lower() != ".gif":
        raise SystemExit(f"Animation not found: {value!r}. Use 'ta-list' to see available choices.")
    set_default_animation("gif", str(candidate.resolve()))
    print(f"Default animation set to {candidate.name}.")


def choose_interactively() -> None:
    items = show_animations()
    print("Choose the default animation:")
    for index, (label, _kind, _identifier) in enumerate(items, 1):
        print(f"  {index}. {label}")
    print(f"  {len(items) + 1}. Random")
    print("  0. Cancel")
    try:
        choice = input("Selection: ").strip()
        number = int(choice)
    except (ValueError, EOFError):
        print("No change made.")
        return
    if number == 0:
        print("No change made.")
    elif 1 <= number <= len(items):
        _label, kind, identifier = items[number - 1]
        set_default_animation(kind, identifier)
        print(f"Default animation updated: {items[number - 1][0]}")
    elif number == len(items) + 1:
        set_default_animation("random", "all")
        print("Default animation set to Random.")
    else:
        print("Invalid selection; no change made.")


def build_parser() -> argparse.ArgumentParser:
    """Build the command parser; argparse renders help from this registry.

    Add new commands here and both `ta-help` and `ta-manager --help` will
    automatically include them with their current descriptions.
    """
    parser = argparse.ArgumentParser(
        prog="ta-manager",
        description="Import GIFs and manage the animation shown by Fastfetch.",
        epilog="Examples: ta-import ~/Downloads/*.gif | ta-default random | ta-list",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command")

    importer = subparsers.add_parser(
        "import", aliases=["ta-import"],
        help="import GIF file(s) into your personal animation library",
        description="Copy one or more GIF files into the terminal-animations library.",
    )
    importer.add_argument("files", nargs="+", help="GIF file(s) to import")

    subparsers.add_parser(
        "list", aliases=["ta-list"],
        help="list available animations and the saved default",
        description="Show Starfield, imported GIFs, Random, and the current default.",
    )

    default_parser = subparsers.add_parser(
        "default", aliases=["ta-default"],
        help="choose or set the default animation",
        description="Choose interactively, or specify starfield, random, or a GIF.",
    )
    default_parser.add_argument(
        "animation", nargs="?", help="starfield, random, a library GIF name, or a GIF path"
    )

    subparsers.add_parser(
        "random", aliases=["ta-random"],
        help="set Random (a fresh selection on each Fastfetch run) as the default",
        description="Select a random built-in or imported GIF every time Fastfetch runs.",
    )
    subparsers.add_parser(
        "clear-default", aliases=["ta-clear-default"],
        help="clear the saved default (Starfield becomes the fallback)"
    )
    subparsers.add_parser(
        "help", aliases=["ta-help"],
        help="show this automatically generated command list"
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    aliases = {
        "ta-import": "import",
        "ta-list": "list",
        "ta-default": "default",
        "ta-random": "random",
        "ta-clear-default": "clear-default",
        "ta-help": "help",
    }
    command = aliases.get(args.command, args.command)
    if command in (None, "help"):
        parser.print_help()
        return 0
    if command == "import":
        count = import_gifs(args.files)
        print(f"Imported {count} GIF{'s' if count != 1 else ''}.")
        return 0 if count else 1
    if command == "list":
        print_list()
    elif command == "default":
        if args.animation:
            set_named_default(args.animation)
        else:
            choose_interactively()
    elif command == "random":
        set_default_animation("random", "all")
        print("Default animation set to Random. A selection will be made for each Fastfetch run.")
    elif command == "clear-default":
        clear_default_animation()
        print("Saved default cleared. Starfield will be used as the fallback.")
    return 0


def _alias_entrypoint(command: str) -> int:
    """Run a manager subcommand through its dedicated console script."""
    return main([command, *sys.argv[1:]])


def import_cli() -> int:
    return _alias_entrypoint("import")


def list_cli() -> int:
    return _alias_entrypoint("list")


def default_cli() -> int:
    return _alias_entrypoint("default")


def random_cli() -> int:
    return _alias_entrypoint("random")


def clear_default_cli() -> int:
    return _alias_entrypoint("clear-default")


def help_cli() -> int:
    return _alias_entrypoint("help")


if __name__ == "__main__":
    raise SystemExit(main())
