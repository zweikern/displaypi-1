---
type: Workflow
title: Entwicklungsworkflow
description: VS Code Remote SSH vom Mac zum Raspberry Pi. Projektpfade, Arbeitsweise und Terminalnutzung.
tags: [workflow, vscode, ssh, remote, development]
status: stable
generated: { by: human:tom, at: 2026-07-26T00:00:00Z }
sources:
  - id: briefing
    resource: sources/displaypi_codex_briefing.md
    title: DisplayPi Codex Briefing
---

# Entwicklungsworkflow

## Verbindung

VS Code läuft auf dem Mac. Die Verbindung zum Raspberry Pi erfolgt per **Remote SSH**:

```bash
ssh <BENUTZER>@displaypi-1.local
```

Die Verbindungsdaten sind in `.env` im Projekt-Root konfiguriert:
- `DISPLAYPI_HOST=displaypi-1.local`
- `DISPLAYPI_USER=pi`

## Projektpfade

| Ort | Pfad |
|---|---|
| Lokal (Mac) | `/Users/tom/Documents/Coding/displaypi-1` |
| Remote (Pi) | `/home/<BENUTZER>/display-controller` |

## Arbeitsweise

1. **Codex arbeitet direkt auf dem Pi**: Das Repository wird auf dem Pi angelegt. Dateien werden dort bearbeitet.
2. **Befehle im Remote-Terminal**: Alle Shell-Befehle laufen auf dem Pi.
3. **Python läuft auf dem Pi**: GPIO/SPI-Zugriff ist nur dort möglich.
4. **Keine lokale Mac-Python-Umgebung** für GPIO/SPI verwenden.
5. VS Code dient nur als Remote-Editor und Terminal.

## Git

Das Repository wird auf dem Pi mit Git versioniert. Commit und Push vom Pi aus oder vom Mac (wenn das Repo lokal gespiegelt ist).
