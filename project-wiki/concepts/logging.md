---
type: Architecture
title: Logging
description: Strukturiertes Logging mit Rotation, microSD-Schonung und konfigurierbarem Log-Level.
tags: [logging, configuration, sd-card]
status: stable
generated: { by: human:tom, at: 2026-07-26T00:00:00Z }
sources:
  - id: briefing
    resource: sources/displaypi_codex_briefing.md
    title: DisplayPi Codex Briefing
---

# Logging

## Anforderungen

- **Lesbare Konsolenausgabe** (für interaktiven Betrieb)
- **Zeitstempel** bei jeder Log-Zeile
- **Konfigurierbares Log-Level** (`DEBUG`, `INFO`, `WARNING`, `ERROR`)
- **Rotierende Logdateien** (gegen unbegrenztes Wachstum)
- **Maximal 5 MB je Datei**, wenige Backups (z. B. 3)
- **Kein unbegrenztes Schreiben auf die microSD**
- Standardbetrieb: `INFO`
- Entwicklungsmodus: `DEBUG`

## Wichtiger Hinweis

**Hochfrequente** Animations-Frame-Ereignisse oder spätere Touchereignisse **nicht dauerhaft einzeln auf INFO loggen**. Das würde die microSD unnötig belasten und die Logdateien aufblähen. Solche Ereignisse nur auf `DEBUG` loggen oder als aggregierte Metriken.

## Konfiguration

```toml
[logging]
level = "INFO"
directory = "var/log"
maximum_file_mb = 5
backup_count = 3
```
