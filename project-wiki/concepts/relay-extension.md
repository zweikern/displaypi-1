---
type: Architecture
title: Relais-Erweiterung
description: RelayController-Abstraktion mit Sicherheitsvorgaben. Noch keine physische Ansteuerung.
tags: [relay, gpio, safety, future]
status: draft
generated: { by: human:tom, at: 2026-07-26T00:00:00Z }
sources:
  - id: briefing
    resource: sources/displaypi_codex_briefing.md
    title: DisplayPi Codex Briefing
---

# Relais-Erweiterung

## Status

Noch **keine Relais physisch ansteuern**. Schnittstelle abstrakt vorbereiten.

## Abstrakte Schnittstelle

```python
class RelayController:
    def set_state(self, relay_id: int, enabled: bool) -> None:
        ...

    def all_off(self) -> None:
        ...
```

## Implementierungen

| Klasse | Zweck |
|---|---|
| `MockRelayController` | Platzhalter für Tests und Entwicklung |
| `GPIORelayController` | Später: Relais über GPIO-Pins |
| `I2CRelayController` | Später: Relais über I²C-Expander |

## Sicherheitsvorgaben

1. **Beim Start alle Relais aus** (fail-safe)
2. **Beim kontrollierten Shutdown alle Relais aus** (explizit in Shutdown-Sequenz)
3. **Keine reine Toggle-Schnittstelle** — immer expliziten Zielzustand setzen (`set_state(id, True/False)`)
4. Keine 230-V-Relaissteuerung in diesem Projekt

## Integration

Der `RelayController` wird in die Event-Loop der Hauptanwendung integriert (siehe [Phase 5](phase-5-nonblocking.md)).
