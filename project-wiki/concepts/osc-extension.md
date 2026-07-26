---
type: Protocol
title: OSC / TouchDesigner-Erweiterung
description: OSC-Adressschema, Ports und modulare Vorbereitung für TouchDesigner-Kommunikation.
tags: [osc, touchdesigner, network, future]
status: draft
generated: { by: human:tom, at: 2026-07-26T00:00:00Z }
sources:
  - id: briefing
    resource: sources/displaypi_codex_briefing.md
    title: DisplayPi Codex Briefing
---

# OSC / TouchDesigner-Erweiterung

## Status

OSC zunächst **deaktiviert** (`osc.enabled = false`), aber Modulstruktur vorbereitet.

## Adressschema

### Pi → TouchDesigner

```text
/station/1/status
/station/1/button
/station/1/touch
/station/1/relay/state
```

### TouchDesigner → Pi

```text
/station/1/display/page
/station/1/display/animation
/station/1/display/text
/station/1/relay/set
```

## Ports

| Richtung | Port |
|---|---|
| TouchDesigner empfängt | 7000 |
| displaypi-1 empfängt | 7101 |

## Bibliothek

```text
python-osc
```

## Architekturvorgabe

Die spätere OSC-Erweiterung **darf keinen Umbau des Displayrenderers** erfordern. OSC ist ein separater Input-Channel, der die gleichen Renderer-Schnittstellen verwendet.

## Konfiguration

```toml
[osc]
enabled = false
touchdesigner_host = "192.168.1.10"
send_port = 7000
receive_port = 7101
```
