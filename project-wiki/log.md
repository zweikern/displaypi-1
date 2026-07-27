# Project Wiki Update Log – displaypi-1

## 2026-07-28
- **OSC Mode**: ThreadingOSCUDPServer auf Port 7101. TouchDesigner/Mac kann Animationen triggern: `/displaypi-1/animation fog_loading|fog_ready|fog_active|off`, `/displaypi-1/fog on|off`, `/displaypi-1/mode local|osc`. Web-UI mit 🎮 Lokal / 📡 OSC Toggle — in OSC-Mode sind lokale Buttons deaktiviert.

## 2026-07-27
- **Issue – WLAN**: Nach Neustart kein WLAN (wpa_supplicant.conf fehlte, nmcli-Passwort falsch). Fix: `nmcli device wifi connect "FRITZ!Box 6591 Cable DB" --ask` + `connection.autoconnect yes`. WLAN verbindet jetzt zuverlässig. IP fix auf 192.168.178.26 über Fritz!Box reserviert (MAC wlan0: `dc:a6:32:cd:32:09`). Ethernet (MAC `dc:a6:32:cd:32:08`) optional.
- **systemd-Service**: displaypi-1.service läuft als Autostart, Port 5000.

## 2026-07-26
- **Weboberfläche**: Flask-Webserver auf Port 5000. Dark-UI mit Start/Stop-Button, Echtzeit-Status (idle/loading/ready/active), Fog-Pin-Anzeige (GPIO17: HIGH bei Active, LOW sonst). API-Endpunkte: GET /api/status, POST /api/start, POST /api/stop.
- **Fog-Sequenz**: Erste Bildserie implementiert. 5 PNG-Bilder (1402×1122) für 3 Zustände: Fog Loading (Bild01/02 blinkend), Fog Ready (Bild03 statisch), Fog Active (Bild04/05 blinkend). Skalierung auf 160×128 + ROTATE_90 für korrekte Orientierung auf dem 128×160-Display.
- **Deployment**: Git-Repo auf Raspberry Pi geklont, venv erstellt, SPI0 aktiviert.
- **Display Test – Erfolg**: ST7735R arbeitet mit Standard-Parametern (bgr=False, invert=False, rotation=0).
- **Issue – VCC/GND**: VCC und GND waren initial vertauscht → Display zeigte nur Backlight-Flackern, keine SPI-Kommunikation (RDDID=0x00). Nach Korrektur lief der Farbtest sofort.
- **Issue – CS-Konflikt**: busio.SPI + manuelles CS auf GPIO8 erzeugt Konflikt mit Hardware-CS. Mit `spidev.no_cs=True` oder der Adafruit-Bibliothek (die das intern handhabt) funktioniert es.
- **Erfolgreiche Konfiguration**: bgr=False, invert=False, rotation=0, offset=(0,0). Adafruit-circuitpython-rgb-display 3.14.6, Pillow 12.3.0.
- **Initialization**: Project wiki created from `docs/displaypi_codex_briefing.md`. Extracted 18 concept pages, created SCHEMA.md, index.md, and log.md following Karpathy's LLM Wiki pattern and OKF v0.2.
- **Schema**: Established SCHEMA.md with agent instructions, type taxonomy, and OKF v0.2 conventions.
- **Ingest**: Processed `sources/displaypi_codex_briefing.md` — the original project briefing document.
