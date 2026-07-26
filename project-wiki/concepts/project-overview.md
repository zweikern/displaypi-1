---
type: Project
title: Project Overview – displaypi-1
description: Ziel, Auftrag und Projektstatus des Raspberry Pi Display Controllers.
tags: [overview, status, pi4, pi3]
status: stable
generated: { by: human:tom, at: 2026-07-26T00:00:00Z }
sources:
  - id: briefing
    resource: sources/displaypi_codex_briefing.md
    title: DisplayPi Codex Briefing
---

# Project Overview

## Auftrag

Auf dem Raspberry Pi wird ein sauberes, reproduzierbares Python-Projekt zur Ansteuerung eines **1,8-Zoll-SPI-Displays** eingerichtet.

## Projektstatus

- **Phase:** Initialer Hardware- und Softwareaufbau
- **Zielsystem (aktuell):** Raspberry Pi 4 mit Raspberry Pi OS Lite (32-bit)
- **Spätere Zielhardware:** Raspberry Pi 3B
- **Entwicklungsumgebung:** VS Code auf macOS über Remote SSH
- **Hostname:** `displaypi-1`

## Ziele (geordnet)

1. Display zuverlässig initialisieren
2. Testfarben, Text und Bilder darstellen
3. GIF-Animationen / Frame-Sequenzen abspielen
4. Ohne Desktopumgebung funktionieren
5. Später unverändert auf Raspberry Pi 3B laufen
6. Modular für Touch, OSC/TouchDesigner und Relais vorbereitet sein
7. Später als `systemd`-Dienst automatisch starten

## Ausgangslage

- Raspberry Pi OS Lite, 32-bit (kein Desktop)
- Hostname `displaypi-1`
- SSH-Zugang eingerichtet
- Netzwerkverbindung vorhanden
- Entwicklung per VS Code Remote SSH
- 16-GB-microSD-Karte

## Reihenfolge

1. System und Hardware prüfen (Diagnose)
2. Minimalen Displaytest umsetzen (Farben/Muster)
3. Nach erfolgreichem Hardwaretest: vollständige Projektstruktur aufbauen
