---
type: Architecture
title: Display-Treiber & Rendering
description: Adafruit-Blinka + CircuitPython RGB Display Library + Pillow für den ST7735R. RGB565-Farbmodus.
tags: [display, driver, st7735r, pillow, spi, rendering]
status: stable
generated: { by: human:tom, at: 2026-07-26T00:00:00Z }
sources:
  - id: briefing
    resource: sources/displaypi_codex_briefing.md
    title: DisplayPi Codex Briefing
---

# Display-Treiber & Rendering

## Bevorzugte Bibliotheken

1. **adafruit-blinka** — GPIO-Abstraktion für Raspberry Pi
2. **adafruit-circuitpython-rgb-display** — Display-Treiber für ST7735R
3. **Pillow** — Bildverarbeitung, Text, Zeichenoperationen

Eine andere Displaybibliothek ist nur zulässig, wenn die bevorzugte Lösung auf dem installierten System **nachweislich nicht stabil** funktioniert. Die Entscheidung muss in der README begründet werden.

## Abgelehnte Ansätze

- Keine Python-2-Bibliotheken
- Keine ungeprüften veralteten Beispielrepositories
- Kein Linux-Framebuffer-Treiber (`/dev/fb0`)
- Kein X11/Wayland

## Display-Konfiguration

```toml
[display]
driver = "st7735r"
width = 128
height = 160
rotation = 0
spi_bus = 0
spi_device = 0
baudrate = 16000000
gpio_dc = 25
gpio_reset = 24
gpio_cs = 8
bgr = false
x_offset = 0
y_offset = 0
target_fps = 20
```

Konfigurierbare Werte:
- **Rotation** (0, 90, 180, 270)
- **BGR-Farbreihenfolge** (`bgr`: true/false)
- **X-Offset / Y-Offset** (Bildversatz)
- **SPI-Taktrate** (`baudrate`)
- **Ziel-FPS** (`target_fps`)

## SPI

- Bus: SPI0
- Device: CE0 (`/dev/spidev0.0`)
- GPIOs: SCLK=11, MOSI=10, CE0=8, DC=25, RESET=24

## Farbmodus

Der ST7735R gibt RGB565 (16-bit) aus. Pillow-Bilder müssen entsprechend konvertiert werden.
