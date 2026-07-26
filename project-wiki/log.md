# Project Wiki Update Log – displaypi-1

## 2026-07-26
- **Deployment**: Git-Repo auf Raspberry Pi geklont, venv erstellt, SPI0 aktiviert.
- **Display Test – Erfolg**: ST7735R arbeitet mit Standard-Parametern (bgr=False, invert=False, rotation=0).
- **Issue – VCC/GND**: VCC und GND waren initial vertauscht → Display zeigte nur Backlight-Flackern, keine SPI-Kommunikation (RDDID=0x00). Nach Korrektur lief der Farbtest sofort.
- **Issue – CS-Konflikt**: busio.SPI + manuelles CS auf GPIO8 erzeugt Konflikt mit Hardware-CS. Mit `spidev.no_cs=True` oder der Adafruit-Bibliothek (die das intern handhabt) funktioniert es.
- **Erfolgreiche Konfiguration**: bgr=False, invert=False, rotation=0, offset=(0,0). Adafruit-circuitpython-rgb-display 3.14.6, Pillow 12.3.0.
- **Initialization**: Project wiki created from `docs/displaypi_codex_briefing.md`. Extracted 18 concept pages, created SCHEMA.md, index.md, and log.md following Karpathy's LLM Wiki pattern and OKF v0.2.
- **Schema**: Established SCHEMA.md with agent instructions, type taxonomy, and OKF v0.2 conventions.
- **Ingest**: Processed `sources/displaypi_codex_briefing.md` — the original project briefing document.
