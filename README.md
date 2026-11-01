# terminal-animations

Animated logos for [Fastfetch](https://github.com/fastfetch-cli/fastfetch), rendered directly in an interactive Bash terminal.

The controller keeps the animation running while you edit a command line, pauses it while a submitted command runs, and resumes it when Bash returns to the prompt. The current renderer uses ANSI truecolor and Unicode upper-half blocks. GIFs are imported into a per-user library; Starfield is included as a built-in animation.

> **Project status:** early public-release candidate. The working prototype has been tested by its maintainer in Fedora Workstation 44 with GNOME/Ptyxis. Other terminal emulators and distributions still need testing. It requires a POSIX-style PTY, interactive Bash, Fastfetch, and a terminal that supports OSC 11 background queries and truecolor (OSC 11 falls back to black when unsupported).

## Requirements

- Linux or another POSIX system with `pty.fork()` support
- Bash
- Fastfetch
- Python 3.10 or newer
- Pillow and pyte (installed automatically by pip/pipx or the distribution package)
- A terminal with ANSI cursor control and 24-bit color support

## Install

Once published to PyPI, the recommended generic Linux install will be:

```bash
pipx install terminal-animations
```

For Fedora, the planned distribution route is a COPR RPM repository. The repository name and install command will be added after the first published build.

For a development checkout:

```bash
git clone https://github.com/Araragi234/Terminal-Animation.git
cd Terminal-Animation
python -m venv .venv
. .venv/bin/activate
python -m pip install -e .
```

Add the startup launcher block from [`bashrc-integration.sh`](bashrc-integration.sh) immediately before the existing `fastfetch` command in `~/.bashrc`. Keep that existing Fastfetch command. Add the management functions from the same file to `~/.bashrc` as well. Back up the file first and test in a new terminal window.

For a packaged installation, `terminal-animations` and `ta-manager` are installed as commands. The Bash snippet also supports the source-checkout fallback shown above. In addition to the short Bash functions, the `ta-manager` executable accepts the `ta-*` aliases shown by `ta-help`.

## Commands

```bash
ta-help
ta-import ~/Downloads/example.gif
ta-list
ta-default
ta-default starfield
ta-default example.gif
ta-default random
ta-random
ta-clear-default
```

- `ta-help` prints the manager's automatically generated command reference. `ta-manager help` prints the same reference. The parser owns the command registry, and its help output lists each canonical command alongside its `ta-*` CLI alias.
- `ta-import` imports one or more GIF files. Existing files are not overwritten; a numeric suffix is added for duplicate names.
- `ta-list` shows installed animations and the active default.
- `ta-default` opens an interactive selector; a name or GIF path can also be supplied.
- `ta-random` chooses from Starfield and all imported GIFs each time Fastfetch is run.
- `ta-clear-default` removes the saved choice and falls back to Starfield.

The detailed command list comes from the Python command parser, rather than a separately maintained help string. New manager subcommands automatically appear in `ta-help` when registered in `manage_animations.py`.

## Configuration and files

- Settings: `${XDG_CONFIG_HOME:-~/.config}/terminal-animations/settings.json`
- GIF library: `${XDG_DATA_HOME:-~/.local/share}/terminal-animations/gifs/`

Existing GIFs in the older source-checkout `animations/gifs/` folder are copied into the XDG data directory when the library is first accessed.

## Uninstall

Remove the startup launcher and management functions from `~/.bashrc`, then uninstall using the method you chose (`pipx uninstall terminal-animations` for pipx, or `dnf remove terminal-animations` for an RPM). User settings and imported GIFs are intentionally kept; remove them manually only if you want to delete your personal configuration:

```bash
rm -rf "${XDG_CONFIG_HOME:-$HOME/.config}/terminal-animations"
rm -rf "${XDG_DATA_HOME:-$HOME/.local/share}/terminal-animations"
```

## License

Terminal Animations is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version. See [`LICENSE`](LICENSE) for the complete license text.

Copyright (C) 2026 Araragi234.

## Contributing

Bug reports, terminal-emulator compatibility reports, documentation improvements, and code contributions are welcome. Please open an issue before starting a large change so the approach can be discussed. Contributions are accepted under the same GPL-3.0-or-later license.

See [`docs/release-plan.md`](docs/release-plan.md) for current packaging and release notes.
