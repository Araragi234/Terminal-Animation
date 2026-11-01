# Copyright (C) 2026 Araragi234
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
MANAGER = ROOT / "manage_animations.py"


def run_manager(*args: str, config_home: Path, data_home: Path) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["XDG_CONFIG_HOME"] = str(config_home)
    env["XDG_DATA_HOME"] = str(data_home)
    return subprocess.run(
        [sys.executable, str(MANAGER), *args],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )


def test_help_lists_commands_and_aliases(tmp_path: Path) -> None:
    result = run_manager("help", config_home=tmp_path / "config", data_home=tmp_path / "data")
    assert result.returncode == 0
    assert "import (ta-import)" in result.stdout
    assert "random (ta-random)" in result.stdout
    assert "help (ta-help)" in result.stdout


def test_random_command_persists_setting(tmp_path: Path) -> None:
    config_home = tmp_path / "config"
    data_home = tmp_path / "data"
    result = run_manager("random", config_home=config_home, data_home=data_home)
    assert result.returncode == 0
    settings = config_home / "terminal-animations" / "settings.json"
    assert '"type": "random"' in settings.read_text(encoding="utf-8")


def test_import_and_default_by_filename(tmp_path: Path) -> None:
    config_home = tmp_path / "config"
    data_home = tmp_path / "data"
    source = tmp_path / "sample.gif"
    Image.new("RGB", (4, 4), (255, 0, 0)).save(source, format="GIF")

    imported = run_manager("import", str(source), config_home=config_home, data_home=data_home)
    assert imported.returncode == 0
    assert "Imported: sample.gif" in imported.stdout

    selected = run_manager("default", "sample.gif", config_home=config_home, data_home=data_home)
    assert selected.returncode == 0
    settings = config_home / "terminal-animations" / "settings.json"
    assert '"type": "gif"' in settings.read_text(encoding="utf-8")
    assert "sample.gif" in settings.read_text(encoding="utf-8")


def test_ta_aliases_work_directly(tmp_path: Path) -> None:
    config_home = tmp_path / "config"
    data_home = tmp_path / "data"
    help_result = run_manager("ta-help", config_home=config_home, data_home=data_home)
    assert help_result.returncode == 0
    assert "random (ta-random)" in help_result.stdout

    random_result = run_manager("ta-random", config_home=config_home, data_home=data_home)
    assert random_result.returncode == 0
    settings = config_home / "terminal-animations" / "settings.json"
    assert '"type": "random"' in settings.read_text(encoding="utf-8")
