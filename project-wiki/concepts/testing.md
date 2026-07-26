---
type: Workflow
title: Testing
description: Unit-Tests für hardwareunabhängige Logik. Hardware-Tests separat über CLI. Mock-Strategie.
tags: [testing, pytest, mock, hardware]
status: stable
generated: { by: human:tom, at: 2026-07-26T00:00:00Z }
sources:
  - id: briefing
    resource: sources/displaypi_codex_briefing.md
    title: DisplayPi Codex Briefing
---

# Testing

## Unit-Tests (hardwareunabhängig)

Ausführung:
```bash
pytest
```

Testbereiche:
- Konfigurationsvalidierung (`test_config.py`)
- Pfadauflösung
- Asseterkennung
- GIF-Frame-Timing (`test_animation_timing.py`)
- Skalierungsberechnung
- Cachegrenzen
- Shutdownlogik
- Asset-Loading (`test_asset_loading.py`)
- Später: OSC-Adressaufbau

## Hardware-Tests

- **Separat** über CLI-Befehle ausführen
- **Nicht automatisch** mit normalen Unit-Tests laufen
- Hardwarezugriffe (SPI, GPIO) über **Mocks ersetzbar** machen

## Mock-Strategie

- `unittest.mock` oder `pytest-mock` für Hardware-Abhängigkeiten
- `MockInputProvider` für Touch-Tests
- `MockRelayController` für Relais-Tests
- SPI-Display-Treiber mocken für Rendering-Tests
