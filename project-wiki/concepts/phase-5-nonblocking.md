---
type: Phase
title: Phase 5 – Nicht blockierender Betrieb
description: Event-Loop-Architektur, Signal-Handling (SIGINT/SIGTERM), geordnetes Herunterfahren.
tags: [phase, event-loop, signals, shutdown, nonblocking]
status: stable
generated: { by: human:tom, at: 2026-07-26T00:00:00Z }
sources:
  - id: briefing
    resource: sources/displaypi_codex_briefing.md
    title: DisplayPi Codex Briefing
---

# Phase 5 – Nicht blockierender Betrieb

## Anforderung

Die Hauptanwendung darf während Animationen **nicht komplett blockieren**. Das System muss gleichzeitig:
- Display aktualisieren
- Spätere Touchereignisse verarbeiten können
- Spätere OSC-Nachrichten empfangen können
- Spätere Relaisbefehle ausführen können
- Geordnet herunterfahren können

## Verbotene Muster

- **Keine langen `time.sleep()`-Ketten** im Hauptprozess
- Kein Busy-Waiting
- Kein blockierendes I/O ohne Timeout

## Signal-Handling

Folgende Signale müssen behandelt werden:
- **`SIGINT`** (Ctrl+C)
- **`SIGTERM`** (systemd stop)

### Shutdown-Sequenz

1. Animation stoppen
2. Display optional schwarz setzen (konfigurierbar)
3. Ressourcen freigeben (SPI, GPIO)
4. Logs schließen

## Architektur

- Event-Loop mit nicht-blockierendem Wait
- Frame-Timing über Zeitdifferenzen, nicht über Sleep
- Eingänge (Touch, OSC, Relais) über Polling oder Callbacks
- Zustandsmaschine für Applikationszustände (idle, playing, error, shutdown)
