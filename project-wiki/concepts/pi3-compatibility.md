---
type: Constraint
title: Pi-3-Kompatibilität
description: Einschränkungen für die Raspberry-Pi-3B-Kompatibilität. ARMv7, 32-bit, RAM, GPIO.
tags: [compatibility, pi3, armv7, constraints]
status: stable
generated: { by: human:tom, at: 2026-07-26T00:00:00Z }
sources:
  - id: briefing
    resource: sources/displaypi_codex_briefing.md
    title: DisplayPi Codex Briefing
---

# Pi-3-Kompatibilität

## Grundsatz

Das Projekt wird zunächst auf einem **Raspberry Pi 4** entwickelt. Es muss später **unverändert** auf einem **Raspberry Pi 3B** mit Raspberry Pi OS Lite 32-bit funktionieren.

## Vorgaben

- **Standard-SPI0** verwenden (kein SPI1 oder SPI2)
- **BCM-GPIO-Nummern** verwenden (nicht Pin-Nummern oder WiringPi)
- **40-Pin-Header-kompatibel** (Pi 3 und Pi 4 haben den gleichen GPIO-Header)
- **ARMv7/32-Bit-kompatible** Abhängigkeiten (keine aarch64-only Wheels)
- **Keine Desktop- oder Hardwarebeschleunigungsabhängigkeit** (kein X11, kein OpenGL)
- **RAM-Nutzung begrenzen** (Pi 3B hat nur 1 GB RAM vs. Pi 4 bis zu 8 GB)
- **Ziel-FPS konfigurierbar** (Pi 3B ist langsamer)
- **Keine Annahme von Gigabit-Ethernet** (Pi 3B hat nur 100 Mbit)

## Erkennung

Das Pi-Modell nur **diagnostisch** erkennen (z. B. über `/proc/device-tree/model`). Die Kernlogik **darf nicht nach Pi 3 oder Pi 4 verzweigen**.
