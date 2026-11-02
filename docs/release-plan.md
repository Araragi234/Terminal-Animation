# Release and packaging notes

## Project license

Terminal Animations is licensed under GNU GPL version 3 or (at your option) any later version (`GPL-3.0-or-later`). The complete license text is in the repository root `LICENSE` file. Project metadata declares the same SPDX identifier.

## GitHub

- Canonical source repository: https://github.com/Araragi234/Terminal-Animation
- Continuous integration runs the test suite and compile checks on Python 3.10–3.14.
- Version tags use the form `v0.1.0`.

## PyPI

The project defines console entry points `terminal-animations` and `ta-manager`. The GitHub Actions workflow uses PyPI Trusted Publishing. Before publishing a tag, configure the PyPI project to trust this GitHub repository and the `pypi` GitHub Actions environment. Never commit a PyPI token to Git.

Build and validate locally with:

```bash
python -m pip install --upgrade build twine
python -m build
python -m twine check dist/*
```

## Fedora and Arch packaging

Fedora COPR publishing is prepared in `.github/workflows/publish-copr.yml`.
It requires a COPR project plus the `COPR_PROJECT` repository variable and
`COPR_USERNAME`, `COPR_LOGIN`, and `COPR_TOKEN` Actions secrets. See
`docs/copr-publishing.md` for setup and the one-time DNF repository enablement.
An Arch AUR PKGBUILD remains a separate community packaging task. Continue
testing on additional terminal emulators and distributions before advertising
broad compatibility.

## Compatibility status

The prototype has been tested by its maintainer on Fedora Workstation 44 using GNOME/Ptyxis. Konsole and other terminal emulators still need direct testing. The controller requires interactive Bash, Fastfetch, a POSIX PTY, ANSI cursor control, truecolor, and an OSC 11 background-color query (with a black fallback if unsupported).
