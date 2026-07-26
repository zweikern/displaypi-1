---
type: Workflow
title: Bootstrap-Skript
description: Idempotentes Setup-Skript für den Raspberry Pi. SPI, Pakete, venv, Berechtigungen.
tags: [bootstrap, setup, shell, apt, spi, venv]
status: stable
generated: { by: human:tom, at: 2026-07-26T00:00:00Z }
sources:
  - id: briefing
    resource: sources/displaypi_codex_briefing.md
    title: DisplayPi Codex Briefing
---

# Bootstrap-Skript

## Pfad

```text
scripts/bootstrap.sh
```

## Eigenschaften

- **Idempotent** (mehrfach ausführbar ohne Schaden)
- `set -euo pipefail`

## Ablauf

1. **Betriebssystem und Pi-Modell anzeigen** (`/proc/device-tree/model`, `uname -a`)
2. **Benutzer, Hostname und Architektur anzeigen**
3. **SPI aktivieren**: `sudo raspi-config nonint do_spi 0`
4. **Benötigte APT-Pakete installieren**:

```bash
sudo apt update
sudo apt install -y \
  git \
  python3 \
  python3-pip \
  python3-venv \
  python3-dev \
  fonts-dejavu-core \
  libjpeg-dev \
  zlib1g-dev
```

5. **`.venv` erstellen**: `python3 -m venv .venv`
6. **Python-Abhängigkeiten installieren** aus `requirements.txt`
7. **Projektverzeichnisse anlegen** (`assets/gifs`, `assets/images`, `assets/frames`, `assets/fonts`, `var/log`)
8. **Berechtigungen prüfen** (SPI-Device, GPIO)
9. **Melden, ob ein Neustart erforderlich ist** (nach SPI-Aktivierung)

## Hinweise

- Keine vollständige Systemaktualisierung ohne vorherigen Hinweis
- Shellskripte mit `set -euo pipefail`
