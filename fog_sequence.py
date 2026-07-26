#!/usr/bin/env python3
"""Fog-Machine Status-Sequenz – 3 Programmzustaende mit Bildwechsel."""

import time
import board
import busio
import digitalio
from PIL import Image


def init_display():
    """ST7735R initialisieren (128x160, SPI0)."""
    import adafruit_rgb_display.st7735 as st7735
    spi = busio.SPI(clock=board.SCK, MOSI=board.MOSI)
    cs = digitalio.DigitalInOut(board.D8)
    dc = digitalio.DigitalInOut(board.D25)
    reset = digitalio.DigitalInOut(board.D24)

    display = st7735.ST7735R(
        spi, cs=cs, dc=dc, rst=reset,
        width=128, height=160, rotation=0, bgr=False,
    )
    return display


def load_image(path, size=(128, 160)):
    """Laedt PNG, skaliert und spiegelt horizontal."""
    img = Image.open(path).convert("RGB")
    img = img.resize((160, 128), Image.LANCZOS).transpose(Image.ROTATE_90)
    return img


if __name__ == "__main__":
    print("Initialisiere Display...")
    display = init_display()
    print("OK.\n")

    base = "/home/tom/display-controller/img"
    print("Lade Bilder...")
    img01 = load_image(f"{base}/bild01_fog loading.png")
    img02 = load_image(f"{base}/bild02_fog loading.png")
    img03 = load_image(f"{base}/bild03_fog_ready.png")
    img04 = load_image(f"{base}/bild04_fog_active.png")
    img05 = load_image(f"{base}/bild05_fog_active.png")
    print("OK.\n")

    FLASH_DELAY = 0.5
    STATE_DELAY = 3.0

    try:
        while True:
            # Zustand 1: Fog Loading (blinkend)
            print(">>> FOG LOADING (Bild01/02)")
            start = time.monotonic()
            toggle = False
            while time.monotonic() - start < STATE_DELAY:
                display.image(img02 if toggle else img01)
                toggle = not toggle
                time.sleep(FLASH_DELAY)

            # Zustand 2: Fog Ready (statisch)
            print(">>> FOG READY (Bild03)")
            display.image(img03)
            time.sleep(3.0)

            # Zustand 3: Fog Active (blinkend)
            print(">>> FOG ACTIVE (Bild04/05)")
            start = time.monotonic()
            toggle = False
            while time.monotonic() - start < STATE_DELAY:
                display.image(img05 if toggle else img04)
                toggle = not toggle
                time.sleep(FLASH_DELAY)

            print("--- Zyklus Ende ---\n")

    except KeyboardInterrupt:
        print("\nBeende...")
    finally:
        black = Image.new("RGB", (128, 160), (0, 0, 0))
        display.image(black)
        print("Display aus.")
