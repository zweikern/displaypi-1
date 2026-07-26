---
type: Architecture
title: Touch-Erweiterung
description: Abstrakte InputProvider-Schnittstelle für zukünftige Touch-Eingabe (XPT2046, GPIO-Buttons).
tags: [touch, input, abstraction, future]
status: draft
generated: { by: human:tom, at: 2026-07-26T00:00:00Z }
sources:
  - id: briefing
    resource: sources/displaypi_codex_briefing.md
    title: DisplayPi Codex Briefing
---

# Touch-Erweiterung

## Status

Derzeit **nicht implementiert**. Das aktuelle Display-Modell (RB-TFT1.8) hat keinen Touchcontroller. Die Schnittstelle wird abstrakt vorbereitet.

## Abstrakte Eingabeschnittstelle

```python
class InputProvider:
    def poll(self) -> list["InputEvent"]:
        ...
```

## Mögliche Implementierungen

| Klasse | Zweck |
|---|---|
| `NoInputProvider` | Platzhalter, kein Touch vorhanden (aktueller Stand) |
| `XPT2046InputProvider` | Touchcontroller XPT2046 über SPI |
| `GPIOButtonInputProvider` | Physische Taster an GPIO-Pins |
| `MockInputProvider` | Für Tests und Entwicklung |

## Architekturvorgabe

Der Displaycode **darf nicht direkt von einem Touchcontroller abhängen**. Die gesamte Touch-Interaktion läuft über `InputProvider`.
