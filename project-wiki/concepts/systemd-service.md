---
type: Configuration
title: systemd-Service
description: Service-Datei, Installation und Betrieb als systemd-Dienst. Kein Root, Logs über journalctl.
tags: [systemd, service, deployment, autostart]
status: draft
generated: { by: human:tom, at: 2026-07-26T00:00:00Z }
sources:
  - id: briefing
    resource: sources/displaypi_codex_briefing.md
    title: DisplayPi Codex Briefing
---

# systemd-Service

## Service-Datei

```text
systemd/display-controller.service
```

## Anforderungen

- **Normaler Projektbenutzer** (nicht root)
- **Korrektes Arbeitsverzeichnis** (`WorkingDirectory`)
- **Python aus `.venv`** (nicht System-Python)
- **Konfigurationspfad als Argument** (`--config config/displaypi-1.toml`)
- **Neustart nur bei unerwartetem Fehler** (`Restart=on-failure`)
- **Begrenzte Neustartfrequenz** (`RestartSec`, `StartLimitBurst`)
- **Logs über `journalctl`**
- **Benutzername nicht hart** in der Repository-Datei festlegen (Variable im Installationsskript)

## Installation

```bash
./scripts/install_service.sh
```

## Betrieb

```bash
systemctl status display-controller
journalctl -u display-controller -f
```

## Deinstallation

```bash
./scripts/uninstall_service.sh
```

## Wichtiger Hinweis

Service erst nach **erfolgreichen manuellen Hardwaretests** aktivieren. Nicht blind `systemctl enable` laufen lassen, bevor das Display funktioniert.
