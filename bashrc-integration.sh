# Copyright (C) 2026 Araragi234
# SPDX-License-Identifier: GPL-3.0-or-later
# terminal-animations: load this snippet from ~/.bashrc.
# Put the startup launcher block immediately BEFORE your existing `fastfetch`
# command. Keep that existing command unchanged.

# Start the animation-aware Bash controller only for interactive terminals.
if [[ $- == *i* && -t 1 && -z ${TERMINAL_ANIMATIONS_ACTIVE:-} ]]; then
    if command -v terminal-animations >/dev/null 2>&1; then
        exec terminal-animations
    elif [[ -x "$HOME/Projects/terminal-animations/.venv/bin/python" \
            && -f "$HOME/Projects/terminal-animations/interactive_shell.py" ]]; then
        # Development checkout fallback; packaged installs use the command above.
        exec "$HOME/Projects/terminal-animations/.venv/bin/python" \
            "$HOME/Projects/terminal-animations/interactive_shell.py"
    fi
fi

# Animation-management commands. `ta-help` delegates to argparse, so the help
# listing is generated from the manager's registered commands automatically.
_ta_manager() {
    if command -v ta-manager >/dev/null 2>&1; then
        command ta-manager "$@"
        return $?
    fi

    local _ta_root="$HOME/Projects/terminal-animations"
    local _ta_python="$_ta_root/.venv/bin/python"
    local _ta_script="$_ta_root/manage_animations.py"
    if [[ -x "$_ta_python" && -f "$_ta_script" ]]; then
        "$_ta_python" "$_ta_script" "$@"
        return $?
    fi

    printf 'terminal-animations: ta-manager was not found. Install the package or check your development checkout.\n' >&2
    return 127
}

ta-help()        { _ta_manager help; }
ta-import()      { _ta_manager import "$@"; }
ta-list()        { _ta_manager list; }
ta-default()     { _ta_manager default "$@"; }
ta-random()      { _ta_manager random; }
ta-clear-default(){ _ta_manager clear-default; }
