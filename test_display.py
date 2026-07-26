#!/usr/bin/env python3
"""Minimaler Displaytest für ST7735R – Phase 1 & 2."""

import time
import board
import busio
import digitalio
from PIL import Image, ImageDraw


def init_display():
    """ST7735R initialisieren (128x160, SPI0)."""
    import adafruit_rgb_display.st7735 as st7735

    spi = busio.SPI(clock=board.SCK, MOSI=board.MOSI)
    cs = digitalio.DigitalInOut(board.D8)        # CE0 = GPIO 8, Pin 24
    dc = digitalio.DigitalInOut(board.D25)       # GPIO 25, Pin 22
    reset = digitalio.DigitalInOut(board.D24)    # GPIO 24, Pin 18

    display = st7735.ST7735R(
        spi, cs=cs, dc=dc, rst=reset,
        width=128, height=160, rotation=0, bgr=False,
    )
    return display


def diagnose():
    """Systeminformationen ausgeben."""
    import platform
    import os

    print("=== DISPLAYPI-1 DIAGNOSE ===")
    try:
        with open("/proc/device-tree/model", "r") as f:
            print(f"Pi-Modell:       {f.read().strip()}")
    except Exception:
        print("Pi-Modell:       unbekannt")

    print(f"Betriebssystem:  {platform.system()} {platform.release()}")
    print(f"Architektur:     {platform.machine()}")
    print(f"Python:          {platform.python_version()}")
    print(f"Hostname:        {platform.node()}")

    spi_devices = [f for f in os.listdir("/dev") if f.startswith("spidev")]
    found = spi_devices if spi_devices else ["NICHT GEFUNDEN!"]
    print(f"SPI-Geräte:      {found}")

    try:
        import adafruit_rgb_display.st7735  # noqa: F401
        print("Display-Lib:     adafruit-circuitpython-rgb-display OK")
    except ImportError:
        print("Display-Lib:     FEHLT!")

    try:
        from PIL import Image  # noqa: F401
        print("Pillow:          OK")
    except ImportError:
        print("Pillow:          FEHLT!")

    print("=" * 35)


def test_colors(display):
    """Rot, Grün, Blau, Weiß, Schwarz anzeigen."""
    colors = [
        ("ROT",     (255, 0, 0)),
        ("GRUEN",   (0, 255, 0)),
        ("BLAU",    (0, 0, 255)),
        ("WEISS",   (255, 255, 255)),
        ("SCHWARZ", (0, 0, 0)),
        ("CYAN",    (0, 255, 255)),
        ("MAGENTA", (255, 0, 255)),
        ("GELB",    (255, 255, 0)),
    ]

    for name, color in colors:
        print(f"  Zeige {name}...")
        image = Image.new("RGB", (display.width, display.height), color)
        draw = ImageDraw.Draw(image)
        text_color = (255, 255, 255) if sum(color) < 400 else (0, 0, 0)
        draw.text((5, 5), name, fill=text_color)
        display.image(image)
        time.sleep(1.0)


if __name__ == "__main__":
    diagnose()

    print("\nInitialisiere Display...")
    try:
        display = init_display()
        print("Display initialisiert! 128x160 ST7735R\n")
    except Exception as e:
        print(f"FEHLER bei Display-Init: {e}")
        print("\nPrüfe:")
        print("  1. Verkabelung (siehe project-wiki/concepts/wiring.md)")
        print("  2. SPI aktiviert? ls -l /dev/spidev0.*")
        print("  3. Benutzer in Gruppe spi? groups")
        raise SystemExit(1)

    try:
        test_colors(display)
        print("\nFarbtest abgeschlossen.")
    except KeyboardInterrupt:
        print("\nAbgebrochen.")
    finally:
        black = Image.new("RGB", (display.width, display.height), (0, 0, 0))
        display.image(black)
        print("Display aus.")
