---
type: Architecture
title: Animation & GIF-Wiedergabe
description: GIF-Dekodierung mit Pillow, Disposal-Methoden, Frame-Caching, Benchmark und Streaming-Modus.
tags: [animation, gif, frames, pillow, caching, performance]
status: stable
generated: { by: human:tom, at: 2026-07-26T00:00:00Z }
sources:
  - id: briefing
    resource: sources/displaypi_codex_briefing.md
    title: DisplayPi Codex Briefing
---

# Animation & GIF-Wiedergabe

## CLI-Befehle

```bash
python -m display_controller.cli play assets/gifs/test.gif
python -m display_controller.cli play assets/frames/test_animation/
python -m display_controller.cli play assets/gifs/test.gif --loop --fit contain
python -m display_controller.cli benchmark-animation assets/gifs/test.gif
```

## GIF-Anforderungen

- GIF mit **Pillow** dekodieren
- **GIF-Disposal-Methoden** korrekt behandeln (0–3)
- Transparenz korrekt auf Hintergrund zusammensetzen
- **Frame-Dauer** aus GIF übernehmen (in Millisekunden)
- **Looping** optional (Endlosschleife oder einmalig)
- Wiedergabe **abbrechbar** (Signal-Handling)

## Performance

- Ziel: **15–20 FPS**
- Frames auf **128 × 160** vorbereiten (kein teures Runtime-Scaling)
- Kurze Animationen bevorzugt **vollständig in RAM** laden
- **Nicht bei jedem Loop erneut skalieren und dekodieren**
- **Cachegrenze** beachten (`maximum_cache_mb` in der Konfiguration)
- Bei großen Dateien optional **Streaming-Modus**

## Benchmark

Ausgabe von `benchmark-animation`:
- Anzahl Frames
- Mittlere FPS
- Minimale und maximale Framezeit
- Dekodierzeit
- SPI-Übertragungszeit
- Cachegröße

## Disposal-Methoden (GIF89a)

| Code | Methode | Bedeutung |
|---|---|---|
| 0 | None | Kein Disposal |
| 1 | Do Not Dispose | Vorheriger Frame bleibt sichtbar |
| 2 | Restore to Background | Hintergrund wiederherstellen |
| 3 | Restore to Previous | Vorherigen Frame wiederherstellen |
