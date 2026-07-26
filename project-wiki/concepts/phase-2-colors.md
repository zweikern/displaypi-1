---
type: Phase
title: Phase 2 – Farb- und Mustertest
description: Display initialisieren und Testfarben sowie ein Diagnosemuster anzeigen.
tags: [phase, display, colors, test, pattern]
status: stable
generated: { by: human:tom, at: 2026-07-26T00:00:00Z }
sources:
  - id: briefing
    resource: sources/displaypi_codex_briefing.md
    title: DisplayPi Codex Briefing
---

# Phase 2 – Farb- und Mustertest

## Farbtest

```bash
python -m display_controller.cli test-colors
```

Ablauf:
1. Display initialisieren
2. **Rot**, **Grün**, **Blau**, **Weiß** und **Schwarz** anzeigen
3. Jede Farbe **1 bis 1,5 Sekunden** anzeigen
4. Test sauber beenden (Display nicht in undefiniertem Zustand lassen)

## Mustertest

```bash
python -m display_controller.cli test-pattern
```

Testbild mit:
- **Farbigen Ecken** (Orientierung prüfen)
- **Rahmen** (Rand prüfen)
- **Horizontalen und vertikalen Linien** (Auflösung prüfen)
- **Auflösungsangabe** (128×160)
- **Rotation** (aktueller Wert)
- **X-/Y-Offset** (aktueller Wert)
- **Hostname**
- **Uhrzeit**

## Zweck

Damit können Orientierung, Farbreihenfolge (BGR), Offsets und Bildausschnitt geprüft werden, bevor komplexere Darstellungen folgen.
