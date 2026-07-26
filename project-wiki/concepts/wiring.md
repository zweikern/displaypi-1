---
type: Hardware
title: Verkabelung & Pinbelegung
description: Pinbelegung des ST7735R-Displays am Raspberry Pi GPIO-Header. BCM-GPIO-Nummern und physische Pins.
tags: [hardware, wiring, gpio, spi, pinout]
status: stable
generated: { by: human:tom, at: 2026-07-26T00:00:00Z }
sources:
  - id: briefing
    resource: sources/displaypi_codex_briefing.md
    title: DisplayPi Codex Briefing
---

# Verkabelung & Pinbelegung

## Pinbelegung

| Display | Raspberry Pi | BCM-GPIO | Physischer Pin |
|---|---|---:|---:|
| `VCC` | 3,3 V | – | Pin 1 |
| `GND` | Masse | – | Pin 6 |
| `SCL` | SPI0 SCLK | GPIO 11 | Pin 23 |
| `SDA` | SPI0 MOSI | GPIO 10 | Pin 19 |
| `DC` | Data/Command | GPIO 25 | Pin 22 |
| `RES` | Reset | GPIO 24 | Pin 18 |
| `CS` | SPI0 CE0 | GPIO 8 | Pin 24 |

## Wichtige Hinweise

- Bei diesem Modul bedeuten `SCL` und `SDA` **SPI-Takt und SPI-Daten**, nicht I²C.
- Der Display-Micro-SD-Slot wird nicht verkabelt (`SD CS`, `SD MOSI`, `SD SCLK`, `SD MISO`).

## Elektrische Vorgaben

1. Raspberry Pi **vor dem Verkabeln ausschalten**.
2. **VCC und GND korrekt polen!** ⚠️ Vertauschte VCC/GND führen zu fehlender SPI-Kommunikation (Display-ID = 0x00) und nur schwachem Backlight-Flackern. Nachweislich am 2026-07-26 aufgetreten.
3. Nur **3,3-V-Logik** verwenden.
4. **Keine 5-V-Signale** an GPIO-Pins anlegen.
5. GPIO 25 (DC) und GPIO 24 (RES) sind konfigurierbar.
6. GPIO 8 (CS) = SPI0 CE0, Standard-Chip-Select.

## SPI-Konfiguration

SPI0 muss aktiviert sein:

```bash
sudo raspi-config nonint do_spi 0
```

Nach Aktivierung prüfen:

```bash
ls -l /dev/spidev0.*
```

Erwartete Ausgabe:
```
/dev/spidev0.0
/dev/spidev0.1
```

Nach SPI-Aktivierung kann ein Neustart erforderlich sein.
