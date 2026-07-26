# VS Code Codex Briefing
## Raspberry Pi Display Controller – `displaypi-1`

**Projektstatus:** Initialer Hardware- und Softwareaufbau  
**Zielsystem:** Raspberry Pi 4 mit Raspberry Pi OS Lite (32-bit)  
**Spätere Zielhardware:** Raspberry Pi 3B  
**Entwicklungsumgebung:** VS Code auf macOS über Remote SSH  
**Hostname:** `displaypi-1`

---

## 1. Auftrag

Richte auf dem Raspberry Pi ein sauberes, reproduzierbares Python-Projekt zur Ansteuerung eines 1,8-Zoll-SPI-Displays ein.

Das Projekt soll zunächst:

1. das Display zuverlässig initialisieren,
2. Testfarben, Text und Bilder darstellen,
3. GIF-Animationen beziehungsweise vorbereitete Frame-Sequenzen abspielen,
4. ohne Desktopumgebung funktionieren,
5. später unverändert auf einem Raspberry Pi 3B laufen,
6. modular für Touch, OSC/TouchDesigner und Relais vorbereitet sein,
7. später als `systemd`-Dienst automatisch starten können.

Arbeite schrittweise. Zuerst System und Hardware prüfen, dann einen minimalen Displaytest umsetzen. Erst nach erfolgreichem Hardwaretest die vollständige Projektstruktur aufbauen.

---

## 2. Ausgangslage

Auf dem Raspberry Pi ist bereits installiert:

- Raspberry Pi OS Lite, 32-bit
- Hostname `displaypi-1`
- SSH-Zugang
- Netzwerkverbindung
- Entwicklung per VS Code Remote SSH
- 16-GB-microSD-Karte

Das Projekt wird zunächst auf einem Raspberry Pi 4 entwickelt. Es muss später auch auf einem Raspberry Pi 3B mit Raspberry Pi OS Lite 32-bit funktionieren.

Keine Pi-4-spezifischen Abhängigkeiten oder Optimierungen verwenden.

---

## 3. Hardware

### Display

- Joy-it / SIMAC Electronics GmbH
- Platinenbezeichnung `RB-TFT1.8`
- Controller ST7735R
- Auflösung 128 × 160 Pixel
- Farbausgabe RGB565
- Schnittstelle SPI
- Micro-SD-Kartenslot auf der Displayplatine

### Wichtiger Hinweis

Das aktuell vorhandene Modell ist nach der sichtbaren Anschlussbelegung **kein Touchdisplay**. Es fehlen separate Anschlüsse für einen Touchcontroller wie den XPT2046.

Die erste Projektphase umfasst daher nur die Displayausgabe. Eine spätere Touchanbindung muss modular ergänzt werden können.

---

## 4. Verkabelung

| Display | Raspberry Pi | BCM-GPIO | Physischer Pin |
|---|---|---:|---:|
| `VCC` | 3,3 V | – | Pin 1 |
| `GND` | Masse | – | Pin 6 |
| `SCL` | SPI0 SCLK | GPIO 11 | Pin 23 |
| `SDA` | SPI0 MOSI | GPIO 10 | Pin 19 |
| `DC` | Data/Command | GPIO 25 | Pin 22 |
| `RES` | Reset | GPIO 24 | Pin 18 |
| `CS` | SPI0 CE0 | GPIO 8 | Pin 24 |

Die Anschlüsse des Display-Micro-SD-Slots bleiben unverbunden:

- `SD CS`
- `SD MOSI`
- `SD SCLK`
- `SD MISO`

Bei diesem Modul bedeuten `SCL` und `SDA` SPI-Takt und SPI-Daten, nicht I²C.

Elektrische Vorgaben:

- Raspberry Pi vor dem Verkabeln ausschalten.
- Nur 3,3-V-Logik verwenden.
- Keine 5-V-Signale an GPIO-Pins anlegen.
- Assets auf der System-microSD speichern, nicht auf dem Kartenleser des Displays.

---

## 5. Entwicklungsworkflow

VS Code läuft auf dem Mac. Die Verbindung erfolgt per Remote SSH:

```bash
ssh <BENUTZER>@displaypi-1.local
```

Projektpfad auf dem Pi:

```text
/home/<BENUTZER>/display-controller
```

Der Python-Prozess läuft immer auf dem Raspberry Pi. VS Code dient nur als Remote-Editor und Terminal.

Codex soll:

1. die Umgebung auf dem Pi untersuchen,
2. das Repository direkt auf dem Pi anlegen,
3. Dateien dort bearbeiten,
4. Befehle im Remote-Terminal ausführen,
5. keine lokale Mac-Python-Umgebung für GPIO/SPI verwenden.

---

## 6. Technische Leitlinien

### Betriebssystem

- Keine Desktopumgebung installieren.
- Kein X11 und kein Wayland.
- Kein spezielles Display-Image verwenden.
- Raspberry Pi OS Lite bleibt die Basis.

### Python

- Python 3
- virtuelle Umgebung `.venv`
- Typannotationen für öffentliche Funktionen und Klassen
- verständliche Fehlerbehandlung
- strukturierte Logs
- normale Benutzerrechte, nicht dauerhaft als Root

### Bevorzugte Bibliotheken

Zuerst prüfen:

```text
adafruit-blinka
adafruit-circuitpython-rgb-display
Pillow
```

Später für OSC:

```text
python-osc
```

Eine andere Displaybibliothek ist nur zulässig, wenn die bevorzugte Lösung auf dem installierten System nachweislich nicht stabil funktioniert. Die Entscheidung muss in der README begründet werden.

Keine Python-2-Bibliotheken und keine ungeprüften veralteten Beispielrepositories verwenden.

### SPI

SPI0 aktivieren:

```bash
sudo raspi-config nonint do_spi 0
```

Prüfen:

```bash
ls -l /dev/spidev0.*
```

Erwartet:

```text
/dev/spidev0.0
/dev/spidev0.1
```

Nach Aktivierung kann ein Neustart erforderlich sein.

---

## 7. Gewünschte Projektstruktur

```text
display-controller/
├── README.md
├── pyproject.toml
├── requirements.txt
├── .gitignore
├── config/
│   └── displaypi-1.toml
├── assets/
│   ├── gifs/
│   ├── images/
│   ├── frames/
│   └── fonts/
├── scripts/
│   ├── bootstrap.sh
│   ├── run.sh
│   ├── install_service.sh
│   └── uninstall_service.sh
├── systemd/
│   └── display-controller.service
├── src/
│   └── display_controller/
│       ├── __init__.py
│       ├── app.py
│       ├── cli.py
│       ├── config.py
│       ├── display.py
│       ├── renderer.py
│       ├── animation.py
│       ├── assets.py
│       ├── diagnostics.py
│       └── osc.py
└── tests/
    ├── test_config.py
    ├── test_animation_timing.py
    └── test_asset_loading.py
```

Die Struktur darf sinnvoll angepasst werden. Displaytreiber, Rendering, Animation, Konfiguration und Netzwerklogik müssen jedoch getrennt bleiben.

---

## 8. Konfiguration

Hardwarewerte nicht verteilt im Code hardcodieren.

Beispiel `config/displaypi-1.toml`:

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

Folgende Werte müssen konfigurierbar sein:

- Rotation
- BGR-Farbreihenfolge
- X-Offset
- Y-Offset
- SPI-Taktrate
- Ziel-FPS

---

## 9. Bootstrap-Skript

`scripts/bootstrap.sh` soll möglichst idempotent sein und:

1. Betriebssystem und Pi-Modell anzeigen,
2. Benutzer, Hostname und Architektur anzeigen,
3. SPI aktivieren,
4. benötigte APT-Pakete installieren,
5. `.venv` erstellen,
6. Python-Abhängigkeiten installieren,
7. Projektverzeichnisse anlegen,
8. Berechtigungen prüfen,
9. melden, ob ein Neustart erforderlich ist.

Voraussichtliche Pakete:

```bash
sudo apt update
sudo apt install -y \
  git \
  python3 \
  python3-pip \
  python3-venv \
  python3-dev \
  fonts-dejavu-core \
  libjpeg-dev \
  zlib1g-dev
```

Keine vollständige Systemaktualisierung erzwingen, ohne vorher darauf hinzuweisen.

Shellskripte mit:

```bash
set -euo pipefail
```

---

## 10. Entwicklungsphasen

### Phase 1 – Diagnose

CLI-Befehl:

```bash
python -m display_controller.cli diagnose
```

Ausgabe mindestens:

- Pi-Modell
- Betriebssystemversion
- Architektur
- Python-Version
- Hostname
- erkannte SPI-Geräte
- geladene Konfiguration
- Verfügbarkeit der Bibliotheken
- Assetverzeichnisse

Fehler verständlich erklären.

### Phase 2 – Farbtest

```bash
python -m display_controller.cli test-colors
```

Ablauf:

1. Display initialisieren.
2. Rot, Grün, Blau, Weiß und Schwarz anzeigen.
3. Jede Farbe 1 bis 1,5 Sekunden anzeigen.
4. Test sauber beenden.

Zusätzlich:

```bash
python -m display_controller.cli test-pattern
```

Testbild mit:

- farbigen Ecken
- Rahmen
- horizontalen und vertikalen Linien
- Auflösungsangabe
- Rotation
- X-/Y-Offset
- Hostname
- Uhrzeit

Damit Orientierung, Farbreihenfolge, Offsets und Bildausschnitt prüfen.

### Phase 3 – Text und Bilder

```bash
python -m display_controller.cli show-text "Displaytest"
python -m display_controller.cli show-image assets/images/test.png
```

Anforderungen:

- Skalierungsmodi `contain`, `cover`, `stretch`
- Alpha-Kanal korrekt auf Hintergrund zusammensetzen
- UTF-8 und deutsche Umlaute
- DejaVu-Schrift verwenden können
- Hoch- und Querformat berücksichtigen

### Phase 4 – GIF und Frame-Sequenzen

```bash
python -m display_controller.cli play assets/gifs/test.gif
python -m display_controller.cli play assets/frames/test_animation/
```

Anforderungen:

- GIF mit Pillow dekodieren
- GIF-Disposal-Methoden korrekt behandeln
- Transparenz korrekt zusammensetzen
- Frame-Dauer übernehmen
- Looping optional
- Wiedergabe abbrechbar
- Ziel zunächst 15–20 FPS
- Frames auf 128 × 160 vorbereiten
- kurze Animationen bevorzugt vollständig in den RAM laden
- nicht bei jedem Loop erneut skalieren und dekodieren
- Cachegrenze beachten
- bei großen Dateien optional Streamingmodus

Beispiel:

```bash
python -m display_controller.cli play assets/gifs/test.gif --loop --fit contain
```

Benchmark:

```bash
python -m display_controller.cli benchmark-animation assets/gifs/test.gif
```

Ausgabe:

- Anzahl Frames
- mittlere FPS
- minimale und maximale Framezeit
- Dekodierzeit
- SPI-Übertragungszeit
- Cachegröße

### Phase 5 – Nicht blockierender Betrieb

Die Hauptanwendung darf während Animationen nicht komplett blockieren.

Architektur für:

- Displayaktualisierung
- spätere Touchereignisse
- spätere OSC-Nachrichten
- spätere Relaisbefehle
- geordnetes Herunterfahren

Keine langen `time.sleep()`-Ketten im Hauptprozess.

Signale behandeln:

- `SIGINT`
- `SIGTERM`

Beim Beenden:

1. Animation stoppen.
2. Display optional schwarz setzen.
3. Ressourcen freigeben.
4. Logs schließen.

---

## 11. Hauptanwendung

Start:

```bash
python -m display_controller.app --config config/displaypi-1.toml
```

Ablauf:

1. Konfiguration laden und validieren.
2. Display initialisieren.
3. Startbild anzeigen.
4. Idle-Modus starten.
5. optional konfigurierte Animation wiedergeben.
6. Signale verarbeiten.
7. Status protokollieren.

Bei Initialisierungsfehlern:

- klare Fehlermeldung
- keine stille Endlosschleife
- Fehlercode ungleich null
- Hinweise zu Verkabelung, SPI und Konfiguration

---

## 12. Spätere OSC-/TouchDesigner-Erweiterung

OSC zunächst deaktiviert lassen, aber Modulstruktur vorbereiten.

Pi zu TouchDesigner:

```text
/station/1/status
/station/1/button
/station/1/touch
/station/1/relay/state
```

TouchDesigner zu Pi:

```text
/station/1/display/page
/station/1/display/animation
/station/1/display/text
/station/1/relay/set
```

Ports:

```text
TouchDesigner empfängt: 7000
displaypi-1 empfängt:    7101
```

Die spätere OSC-Erweiterung darf keinen Umbau des Displayrenderers erfordern.

---

## 13. Spätere Touch-Erweiterung

Abstrakte Eingabeschnittstelle vorbereiten:

```python
class InputProvider:
    def poll(self) -> list["InputEvent"]:
        ...
```

Mögliche Implementierungen:

- `NoInputProvider`
- `XPT2046InputProvider`
- `GPIOButtonInputProvider`
- `MockInputProvider`

Der Displaycode darf nicht direkt von einem Touchcontroller abhängen.

---

## 14. Spätere Relais-Erweiterung

Noch keine Relais physisch ansteuern. Schnittstelle vorbereiten:

```python
class RelayController:
    def set_state(self, relay_id: int, enabled: bool) -> None:
        ...

    def all_off(self) -> None:
        ...
```

Implementierungen:

- `MockRelayController`
- später `GPIORelayController`
- später eventuell `I2CRelayController`

Sicherheitsvorgaben:

- beim Start alle Relais aus
- beim kontrollierten Shutdown alle Relais aus
- keine reine Toggle-Schnittstelle
- immer expliziten Zielzustand setzen

---

## 15. systemd

Service-Datei:

```text
systemd/display-controller.service
```

Anforderungen:

- normaler Projektbenutzer
- korrektes Arbeitsverzeichnis
- Python aus `.venv`
- Konfigurationspfad als Argument
- Neustart nur bei unerwartetem Fehler
- begrenzte Neustartfrequenz
- Logs über `journalctl`
- Benutzername nicht hart in der Repository-Datei festlegen

Installation:

```bash
./scripts/install_service.sh
```

Status und Logs:

```bash
systemctl status display-controller
journalctl -u display-controller -f
```

Deinstallation:

```bash
./scripts/uninstall_service.sh
```

Service erst nach erfolgreichen manuellen Hardwaretests aktivieren.

---

## 16. Tests

Hardwareunabhängige Tests:

- Konfigurationsvalidierung
- Pfadauflösung
- Asseterkennung
- GIF-Frame-Timing
- Skalierungsberechnung
- Cachegrenzen
- Shutdownlogik
- später OSC-Adressaufbau

```bash
pytest
```

Hardwaretests separat über CLI und nicht automatisch mit normalen Unit Tests ausführen.

Hardwarezugriffe über Mocks ersetzbar machen.

---

## 17. Logging

- lesbare Konsolenausgabe
- Zeitstempel
- konfigurierbares Log-Level
- rotierende Logdateien
- maximal 5 MB je Datei, wenige Backups
- kein unbegrenztes Schreiben auf die microSD
- Standardbetrieb `INFO`
- Entwicklungsmodus `DEBUG`

Hochfrequente Animations- oder spätere Touchereignisse nicht dauerhaft einzeln auf INFO loggen.

---

## 18. Pi-3-Kompatibilität

- Standard-SPI0 verwenden
- BCM-GPIO-Nummern verwenden
- 40-Pin-Header-kompatibel
- ARMv7/32-Bit-kompatible Abhängigkeiten
- keine Desktop- oder Hardwarebeschleunigungsabhängigkeit
- RAM-Nutzung begrenzen
- Ziel-FPS konfigurierbar
- keine Annahme von Gigabit-Ethernet

Das Pi-Modell nur diagnostisch erkennen. Die Kernlogik darf nicht nach Pi 3 oder Pi 4 verzweigen.

---

## 19. Nicht umsetzen

- keinen Linux-Framebuffer-Treiber
- Display nicht als Desktopmonitor konfigurieren
- keine HDMI-Spiegelung
- kein X11 oder Wayland
- keine Desktopumgebung
- Display-Micro-SD-Slot nicht verwenden
- keine 230-V-Relaissteuerung
- kein permanentes Pixelstreaming aus TouchDesigner
- keine Installation fremder Skripte über ungeprüftes `curl | bash`

---

## 20. README

Die README muss enthalten:

1. Projektziel
2. unterstützte Hardware
3. Hinweis: aktuelles Display ohne Touch
4. Pinbelegung
5. Installation
6. SPI-Aktivierung
7. VS-Code-Remote-SSH-Workflow
8. Testbefehle
9. GIF-Wiedergabe
10. Konfiguration
11. systemd
12. Fehlerbehebung
13. Pi-3-Kompatibilität
14. spätere OSC-, Touch- und Relaiserweiterung

Fehlerbehebung mindestens für:

- `/dev/spidev0.0` fehlt
- Display bleibt weiß
- Display bleibt schwarz
- Bild ist verschoben
- Rot und Blau vertauscht
- Anzeige gedreht
- Flackern
- GIF zu langsam
- Berechtigungsfehler
- Python-Abhängigkeit lässt sich nicht installieren

---

## 21. Abnahmekriterien

### Muss

- [ ] reproduzierbares Bootstrap-Skript
- [ ] virtuelle Python-Umgebung
- [ ] SPI-Erkennung
- [ ] ST7735R-Initialisierung
- [ ] Farbtest
- [ ] Testmuster
- [ ] Textdarstellung
- [ ] PNG-Darstellung
- [ ] GIF-Wiedergabe
- [ ] ungefähr 15 FPS oder mehr bei geeigneten Assets
- [ ] Rotation, BGR und Offsets konfigurierbar
- [ ] sauberer Abbruch per `Ctrl+C`
- [ ] begrenzte Logs
- [ ] hardwareunabhängige Unit Tests
- [ ] vorbereiteter systemd-Service
- [ ] vollständige README
- [ ] keine Pi-4-spezifische Kernabhängigkeit

### Soll

- [ ] PNG-Frame-Sequenzen
- [ ] Animationen im RAM vorladen
- [ ] Benchmarkfunktion
- [ ] Mock-Display
- [ ] vorbereitete OSC-Struktur
- [ ] abstrahierte Touch- und Relaisschnittstellen

---

## 22. Arbeitsreihenfolge für Codex

1. Systeminformationen prüfen.
2. Verkabelung anhand dieses Briefings bestätigen lassen.
3. SPI aktivieren und `/dev/spidev0.0` prüfen.
4. Minimales isoliertes Displaytestskript erstellen.
5. Farbtest durchführen.
6. Rotation, Farbreihenfolge und Offsets kalibrieren.
7. Erst danach vollständige Projektstruktur aufbauen.
8. Text- und Bilddarstellung implementieren.
9. GIF-Wiedergabe implementieren.
10. Tests und Diagnostik ergänzen.
11. README fertigstellen.
12. systemd-Service zuletzt installieren.

Nach jeder Phase:

- Änderungen zusammenfassen
- nächsten Testbefehl nennen
- auf Neustartbedarf hinweisen
- bei Fehlern erst diagnostizieren, nicht wahllos Pakete nachinstallieren

---

## 23. Erster konkreter Auftrag

Beginne ausschließlich mit:

1. Systemumgebung auf `displaypi-1` prüfen.
2. Ermitteln:
   - Betriebssystemversion
   - Architektur
   - Python-Version
   - Raspberry-Pi-Modell
   - aktueller Benutzer
   - Home-Verzeichnis
   - SPI-Status
3. Ordner `~/display-controller` anlegen.
4. Zunächst nur erstellen:
   - `README.md`
   - `scripts/bootstrap.sh`
   - `requirements.txt`
   - `display_test.py`
5. Für den ersten Test verwenden:
   - CS: GPIO 8 / CE0
   - Reset: GPIO 24
   - DC: GPIO 25
   - MOSI: GPIO 10
   - SCLK: GPIO 11
6. Farbtest auf dem ST7735R ausführen.
7. Danach auf das Ergebnis des Hardwaretests warten, bevor weitere Module generiert werden.

---

## 24. Qualitätsanforderungen

- Shellskripte mit `set -euo pipefail`
- keine absoluten Benutzerpfade im Quellcode
- Pfade relativ zum Projekt oder per Konfiguration
- Konfiguration vor Nutzung validieren
- Hardwareausnahmen nicht pauschal verschlucken
- keine Secrets im Repository
- `.gitignore` für `.venv`, Cache und Logs
- Abhängigkeiten dokumentieren und möglichst versionieren
- Boot-Konfiguration vor Änderungen sichern
- vor `sudo`-Operationen kurz den Zweck erklären
