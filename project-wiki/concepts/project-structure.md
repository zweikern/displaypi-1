---
type: Architecture
title: Projektstruktur
description: Verzeichnislayout des display-controller Projekts. Module, Trennung der Zuständigkeiten, erweiterbar.
tags: [architecture, structure, modules, python]
status: stable
generated: { by: human:tom, at: 2026-07-26T00:00:00Z }
sources:
  - id: briefing
    resource: sources/displaypi_codex_briefing.md
    title: DisplayPi Codex Briefing
---

# Projektstruktur

## Gewünschtes Layout

```text
display-controller/
├── README.md
├── pyproject.toml
├── requirements.txt
├── .gitignore
├── config/
│   └── displaypi-1.toml
├── assets/
│   ├── gifs/
│   ├── images/
│   ├── frames/
│   └── fonts/
├── scripts/
│   ├── bootstrap.sh
│   ├── run.sh
│   ├── install_service.sh
│   └── uninstall_service.sh
├── systemd/
│   └── display-controller.service
├── src/
│   └── display_controller/
│       ├── __init__.py
│       ├── app.py
│       ├── cli.py
│       ├── config.py
│       ├── display.py
│       ├── renderer.py
│       ├── animation.py
│       ├── assets.py
│       ├── diagnostics.py
│       └── osc.py
└── tests/
    ├── test_config.py
    ├── test_animation_timing.py
    └── test_asset_loading.py
```

## Modulverantwortlichkeiten

| Modul | Zuständigkeit |
|---|---|
| `app.py` | Hauptanwendung, Event-Loop, Lebenszyklus |
| `cli.py` | CLI-Befehle (diagnose, test-colors, play, etc.) |
| `config.py` | TOML-Konfiguration laden und validieren |
| `display.py` | ST7735R-Initialisierung, SPI-Kommunikation |
| `renderer.py` | Zeichenoperationen, Text, Bilder, Skalierung |
| `animation.py` | GIF-Dekodierung, Frame-Timing, Cache |
| `assets.py` | Asset-Pfade, Preloading, Cache-Verwaltung |
| `diagnostics.py` | Systeminformationen, SPI-Check |
| `osc.py` | OSC-Server/Client (später) |

## Trennungsprinzipien

- Displaytreiber, Rendering, Animation, Konfiguration und Netzwerklogik müssen **getrennt** bleiben.
- Struktur darf sinnvoll angepasst werden, aber die Trennung der Zuständigkeiten muss erhalten bleiben.
