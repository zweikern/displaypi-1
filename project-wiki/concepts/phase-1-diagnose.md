---
type: Phase
title: Phase 1 – Diagnose
description: Systeminformationen abrufen, SPI prüfen, Bibliotheken und Konfiguration validieren.
tags: [phase, diagnose, cli, spi, system]
status: stable
generated: { by: human:tom, at: 2026-07-26T00:00:00Z }
sources:
  - id: briefing
    resource: sources/displaypi_codex_briefing.md
    title: DisplayPi Codex Briefing
---

# Phase 1 – Diagnose

## Befehl

```bash
python -m display_controller.cli diagnose
```

## Ausgabe (mindestens)

- Pi-Modell (z. B. "Raspberry Pi 4 Model B")
- Betriebssystemversion (z. B. "Raspberry Pi OS Lite 32-bit")
- Architektur (armv7l)
- Python-Version
- Hostname
- Erkannte SPI-Geräte (`/dev/spidev0.*`)
- Geladene Konfiguration (Pfad und Werte)
- Verfügbarkeit der Bibliotheken (adafruit-blinka, rgb-display, Pillow)
- Assetverzeichnisse (existieren sie? sind sie lesbar?)

## Fehlerbehandlung

- Fehler verständlich erklären
- Keine stillen Fehler
- Hinweise zu SPI-Aktivierung, fehlenden Paketen, Verkabelung
