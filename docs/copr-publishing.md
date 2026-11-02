# Fedora COPR publishing

The COPR workflow submits a source RPM when a `v*` Git tag is pushed. COPR
builds it and publishes the resulting RPM in a DNF repository. Publishing is
not active until a COPR project and GitHub Actions credentials are configured.

## One-time maintainer setup

1. Create or sign in to a Fedora Account System account and create a public
   COPR project named `terminal-animations`. Enable the Fedora chroots you
   intend to support.
2. On the COPR API page, generate an API token with permission to submit builds
   to that project.
3. In the GitHub repository settings, add the repository variable
   `COPR_PROJECT` with the value `owner/terminal-animations` (use the COPR
   username or group that owns the project).
4. Add these repository Actions secrets from the COPR API token block:
   `COPR_USERNAME`, `COPR_LOGIN`, and `COPR_TOKEN`.
5. Push a version tag such as `v0.1.0` to submit the matching source tree.

The token must remain in GitHub Actions secrets; do not commit it to the
repository. Builds can also be started from the Actions page with
`workflow_dispatch`.

## Installing and updating

After COPR has completed the first successful build, Fedora users enable the
repository once, then install the package:

```bash
sudo dnf install dnf-plugins-core
sudo dnf copr enable owner/terminal-animations
sudo dnf install terminal-animations
```

Replace `owner` with the COPR username or group selected above. Once the
repository is enabled, `sudo dnf update` can discover later package builds.
