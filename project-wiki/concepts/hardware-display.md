---
type: Hardware
title: Display – ST7735R (RB-TFT1.8)
description: 1,8-Zoll-SPI-Display von Joy-it mit ST7735R-Controller. 128×160 Pixel, RGB565, kein Touch.
tags: [hardware, display, st7735r, spi]
status: stable
generated: { by: human:tom, at: 2026-07-26T00:00:00Z }
sources:
  - id: briefing
    resource: sources/displaypi_codex_briefing.md
    title: DisplayPi Codex Briefing
---

# Display – ST7735R

## Identifikation

- **Hersteller:** Joy-it / SIMAC Electronics GmbH
- **Platinenbezeichnung:** `RB-TFT1.8`
- **Controller:** ST7735R
- **Auflösung:** 128 × 160 Pixel
- **Farbausgabe:** RGB565 (16-bit)
- **Schnittstelle:** SPI
- **Micro-SD-Kartenslot:** auf der Displayplatine vorhanden

## Wichtiger Hinweis

Das aktuell vorhandene Modell ist nach der sichtbaren Anschlussbelegung **kein Touchdisplay**. Es fehlen separate Anschlüsse für einen Touchcontroller wie den XPT2046.

Die erste Projektphase umfasst daher nur die Displayausgabe. Eine spätere Touchanbindung muss modular ergänzt werden können.

## Technische Daten

| Eigenschaft | Wert |
|---|---|
| Auflösung (Breite) | 128 px |
| Auflösung (Höhe) | 160 px |
| Farbtiefe | 16-bit (RGB565) |
| Schnittstelle | SPI |
| Controller-Chip | ST7735R |
| Betriebsspannung | 3,3 V |
| SD-Kartenslot | vorhanden, wird nicht genutzt |

## Display-Micro-SD-Slot

Die Anschlüsse des Display-Micro-SD-Slots bleiben unverbunden:
- `SD CS`
- `SD MOSI`
- `SD SCLK`
- `SD MISO`

Assets werden auf der System-microSD gespeichert, nicht auf dem Kartenleser des Displays.
