---
okf_version: "0.2"
---

# Project Wiki Index – displaypi-1

## Project Overview

- [Project Overview](concepts/project-overview.md) — Ziel, Auftrag und Projektstatus des Raspberry Pi Display Controllers
- [Constraints & Non-Goals](concepts/constraints.md) — Was NICHT umgesetzt wird und Kompatibilitätsvorgaben

## Hardware

- [Display – ST7735R](concepts/hardware-display.md) — 1,8-Zoll-SPI-Display, Controller, Auflösung, Farbausgabe
- [Verkabelung & Pinbelegung](concepts/wiring.md) — Display-Pinout, BCM-GPIO-Zuordnung, elektrische Vorgaben
- [Pi-3-Kompatibilität](concepts/pi3-compatibility.md) — Einschränkungen und Vorgaben für den Raspberry Pi 3B

## Entwicklung & Workflow

- [Entwicklungsworkflow](concepts/development-workflow.md) — VS Code Remote SSH, Projektpfade, Arbeitsweise
- [Bootstrap-Skript](concepts/bootstrap.md) — Idempotentes Setup-Skript für den Raspberry Pi

## Software-Architektur

- [Projektstruktur](concepts/project-structure.md) — Verzeichnislayout, Module, Trennung der Zuständigkeiten
- [Display-Treiber & Rendering](concepts/display-rendering.md) — Adafruit-Blinka, ST7735R, Pillow, RGB565
- [Animation & GIF-Wiedergabe](concepts/animation.md) — Frame-Dekodierung, Disposal-Methoden, Caching
- [Konfiguration](concepts/configuration.md) — TOML-Schema, konfigurierbare Werte, Hardware-Mapping

## Entwicklungsphasen

- [Phase 1 – Diagnose](concepts/phase-1-diagnose.md) — Systeminformationen, SPI-Check, Bibliotheksverfügbarkeit
- [Phase 2 – Farbtest](concepts/phase-2-colors.md) — Display-Initialisierung, Farb- und Mustertests
- [Phase 3 – Text & Bilder](concepts/phase-3-text-images.md) — Textrendering, Bildskalierung, UTF-8
- [Phase 4 – GIF & Frames](concepts/phase-4-gif.md) — Animation, Benchmark, Streaming-Modus
- [Phase 5 – Nicht blockierend](concepts/phase-5-nonblocking.md) — Event-Loop, Signal-Handling, Shutdown

## Erweiterungen (geplant)

- [OSC / TouchDesigner](concepts/osc-extension.md) — Adressschema, Ports, modulare Vorbereitung
- [Touch-Erweiterung](concepts/touch-extension.md) — InputProvider-Abstraktion, XPT2046
- [Relais-Erweiterung](concepts/relay-extension.md) — RelayController, Sicherheitsvorgaben

## Betrieb

- [systemd-Service](concepts/systemd-service.md) — Service-Datei, Installation, Journal
- [Logging](concepts/logging.md) — Log-Level, Rotation, microSD-Schonung
- [Testing](concepts/testing.md) — Unit-Tests, Hardware-Tests, Mock-Strategie

## Quellen

- [DisplayPi Codex Briefing](sources/displaypi_codex_briefing.md) — Originales Projekt-Briefing (immutable)
