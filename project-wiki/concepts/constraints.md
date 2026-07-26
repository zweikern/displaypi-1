---
type: Constraint
title: Constraints & Non-Goals
description: Was NICHT umgesetzt wird, inkompatible Ansätze und technische Grenzen des Projekts.
tags: [constraints, non-goals, rules]
status: stable
generated: { by: human:tom, at: 2026-07-26T00:00:00Z }
sources:
  - id: briefing
    resource: sources/displaypi_codex_briefing.md
    title: DisplayPi Codex Briefing
---

# Constraints & Non-Goals

## Nicht umsetzen

- ❌ Keinen Linux-Framebuffer-Treiber (`/dev/fb0`)
- ❌ Display nicht als Desktopmonitor konfigurieren
- ❌ Keine HDMI-Spiegelung
- ❌ Kein X11 oder Wayland
- ❌ Keine Desktopumgebung
- ❌ Display-Micro-SD-Slot nicht verwenden
- ❌ Keine 230-V-Relaissteuerung
- ❌ Kein permanentes Pixelstreaming aus TouchDesigner
- ❌ Keine Installation fremder Skripte über ungeprüftes `curl | bash`

## Technische Grenzen

- Keine Pi-4-spezifischen Abhängigkeiten oder Optimierungen
- Keine Python-2-Bibliotheken
- Keine ungeprüften veralteten Beispielrepositories
- Keine 5-V-Signale an GPIO-Pins
- Nicht dauerhaft als Root ausführen

## Betriebssystem

- Raspberry Pi OS Lite bleibt die Basis
- Keine Desktopumgebung installieren
- Kein spezielles Display-Image verwenden
- Keine vollständige Systemaktualisierung (`apt full-upgrade`) erzwingen ohne Hinweis
