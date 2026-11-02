%global _description %{expand:
Animated Fastfetch logos rendered directly in an interactive Bash terminal.
The controller keeps the animation running while editing a command line and
pauses it while commands run. It supports built-in Starfield and imported GIFs.}

Name:           terminal-animations
Version:        0.1.0
Release:        2%{?dist}
Summary:        Animated Fastfetch logos for interactive Bash terminals
License:        GPL-3.0-or-later
URL:            https://github.com/Araragi234/Terminal-Animation
Source0:        %{name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros
BuildRequires:  python3-build
BuildRequires:  python3-pytest
BuildRequires:  python3-pillow
BuildRequires:  python3-pyte
BuildRequires:  python3-setuptools
BuildRequires:  python3-wheel

%description %{_description}

%prep
%autosetup -n %{name}-%{version}

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files -l engine interactive_shell manage_animations

%check
%pytest -q
XDG_CONFIG_HOME=%{_builddir}/test-config \
XDG_DATA_HOME=%{_builddir}/test-data \
PYTHONPATH=%{buildroot}%{python3_sitelib} \
%{buildroot}%{_bindir}/ta-manager help
for command in ta-import ta-list ta-default ta-random ta-clear-default ta-help; do
    env XDG_CONFIG_HOME=%{_builddir}/test-config \
        XDG_DATA_HOME=%{_builddir}/test-data \
        PYTHONPATH=%{buildroot}%{python3_sitelib} \
        PATH=%{buildroot}%{_bindir}:$PATH \
        "$command" --help >/dev/null
done

%files -f %{pyproject_files}
%{_bindir}/ta-import
%{_bindir}/ta-list
%{_bindir}/ta-default
%{_bindir}/ta-random
%{_bindir}/ta-clear-default
%{_bindir}/ta-help
%{_bindir}/ta-manager
%{_bindir}/terminal-animations
%doc README.md docs/license-notice.md bashrc-integration.sh

%changelog
* Mon Nov 02 2026 Araragi234 - 0.1.0-2
- Install the ta-* manager aliases as executable commands

* Mon Nov 02 2026 Araragi234 - 0.1.0-1
- Initial Fedora RPM packaging
