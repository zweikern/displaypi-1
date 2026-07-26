---
type: Configuration
title: Konfiguration – displaypi-1.toml
description: TOML-Konfigurationsschema für den Display Controller. Alle konfigurierbaren Werte mit Erklärung.
tags: [configuration, toml, hardware, display, spi, logging]
status: stable
generated: { by: human:tom, at: 2026-07-26T00:00:00Z }
sources:
  - id: briefing
    resource: sources/displaypi_codex_briefing.md
    title: DisplayPi Codex Briefing
---

# Konfiguration

## Grundsatz

Hardwarewerte **nicht im Code hardcodieren**. Alle Werte über `config/displaypi-1.toml`.

## Vollständiges Schema

```toml
[station]
id = 1
hostname = "displaypi-1"
mode = "local"

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

[assets]
directory = "assets"
preload_animations = true
maximum_cache_mb = 128

[logging]
level = "INFO"
directory = "var/log"
maximum_file_mb = 5
backup_count = 3

[osc]
enabled = false
touchdesigner_host = "192.168.1.10"
send_port = 7000
receive_port = 7101
```

## Zwingend konfigurierbar

Folgende Werte MÜSSEN über die Konfiguration änderbar sein:
- **Rotation** (`display.rotation`)
- **BGR-Farbreihenfolge** (`display.bgr`)
- **X-Offset** (`display.x_offset`)
- **Y-Offset** (`display.y_offset`)
- **SPI-Taktrate** (`display.baudrate`)
- **Ziel-FPS** (`display.target_fps`)

## Sektionen

| Sektion | Zweck |
|---|---|
| `[station]` | Identifikation und Betriebsmodus |
| `[display]` | Hardware-Parameter des ST7735R |
| `[assets]` | Asset-Pfade und Cache |
| `[logging]` | Log-Level und Rotation |
| `[osc]` | OSC/TouchDesigner (später) |
