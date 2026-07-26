---
type: Phase
title: Phase 3 – Text & Bilder
description: Text mit DejaVu-Schrift rendern, Bilder laden und skalieren, UTF-8 und deutsche Umlaute.
tags: [phase, text, images, pillow, utf8, scaling]
status: stable
generated: { by: human:tom, at: 2026-07-26T00:00:00Z }
sources:
  - id: briefing
    resource: sources/displaypi_codex_briefing.md
    title: DisplayPi Codex Briefing
---

# Phase 3 – Text & Bilder

## CLI-Befehle

```bash
python -m display_controller.cli show-text "Displaytest"
python -m display_controller.cli show-image assets/images/test.png
```

## Text-Anforderungen

- **UTF-8** und **deutsche Umlaute** (ä, ö, ü, ß) korrekt darstellen
- **DejaVu-Schrift** verwenden (über `fonts-dejavu-core` APT-Paket)
- Textgröße und Position konfigurierbar
- Hoch- und Querformat berücksichtigen

## Bild-Anforderungen

- **Skalierungsmodi**:
  - `contain` — Bild passt ins Display, Seitenverhältnis erhalten
  - `cover` — Display füllen, Seitenverhältnis erhalten, ggf. abschneiden
  - `stretch` — Display füllen, Seitenverhältnis ignorieren
- **Alpha-Kanal** korrekt auf Hintergrund zusammensetzen (kein schwarzer Hintergrund bei Transparenz)
- Formate: PNG (mit Alpha), JPEG

## Schrift-Fallback

Wenn DejaVu nicht verfügbar ist: klare Fehlermeldung mit Hinweis auf `sudo apt install fonts-dejavu-core`.
