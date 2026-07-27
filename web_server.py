#!/usr/bin/env python3
"""Weboberflaeche + OSC-Server fuer displaypi-1 – Lokal- & OSC-Modus."""

import threading
import time
import board
import busio
import digitalio
from flask import Flask, jsonify, render_template_string
from PIL import Image
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import ThreadingOSCUDPServer

FOG_PIN = 17
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(FOG_PIN, GPIO.OUT, initial=GPIO.LOW)

def init_display():
    import adafruit_rgb_display.st7735 as st7735
    spi = busio.SPI(clock=board.SCK, MOSI=board.MOSI)
    cs = digitalio.DigitalInOut(board.D8)
    dc = digitalio.DigitalInOut(board.D25)
    reset = digitalio.DigitalInOut(board.D24)
    return st7735.ST7735R(spi, cs=cs, dc=dc, rst=reset,
                          width=128, height=160, rotation=0, bgr=False)

display = init_display()
display_lock = threading.Lock()

BASE = "/home/tom/display-controller/img"

def load_image(path):
    img = Image.open(path).convert("RGB")
    return img.resize((160, 128), Image.LANCZOS).transpose(Image.ROTATE_90)

IMG = {
    "load1": load_image(f"{BASE}/bild01_fog loading.png"),
    "load2": load_image(f"{BASE}/bild02_fog loading.png"),
    "ready": load_image(f"{BASE}/bild03_fog_ready.png"),
    "act1":  load_image(f"{BASE}/bild04_fog_active.png"),
    "act2":  load_image(f"{BASE}/bild05_fog_active.png"),
}
BLACK = Image.new("RGB", (128, 160), (0, 0, 0))

app_state = {
    "running": False, "status": "idle", "fog_pin": "LOW",
    "mode": "local", "thread": None, "osc_active": False,
}

def set_fog(on):
    GPIO.output(FOG_PIN, GPIO.HIGH if on else GPIO.LOW)
    app_state["fog_pin"] = "HIGH" if on else "LOW"

def show_image(key):
    with display_lock:
        display.image(IMG.get(key, BLACK))

def switch_mode(mode):
    if app_state["mode"] == mode:
        return
    was_running = app_state["running"]
    app_state["running"] = False
    if app_state["thread"] and app_state["thread"].is_alive():
        app_state["thread"].join(timeout=1.0)
    app_state["mode"] = mode
    app_state["status"] = "idle"
    app_state["osc_active"] = False
    set_fog(False)
    with display_lock:
        display.image(BLACK)
    if was_running:
        app_state["running"] = True
        target = osc_cycle if mode == "osc" else fog_loop
        t = threading.Thread(target=target, daemon=True)
        app_state["thread"] = t
        t.start()

def osc_cycle():
    while app_state["running"] and app_state["mode"] == "osc":
        time.sleep(0.1)
    if not app_state["running"]:
        with display_lock:
            display.image(BLACK)

def fog_loop():
    FLASH = 0.5
    STATE = 3.0
    while app_state["running"] and app_state["mode"] == "local":
        app_state["status"] = "loading"
        set_fog(False)
        start = time.monotonic()
        toggle = False
        while app_state["running"] and app_state["mode"] == "local" \
                and (time.monotonic() - start < STATE):
            with display_lock:
                display.image(IMG["load2"] if toggle else IMG["load1"])
            toggle = not toggle
            time.sleep(FLASH)
        if not app_state["running"] or app_state["mode"] != "local":
            break
        app_state["status"] = "ready"
        set_fog(False)
        with display_lock:
            display.image(IMG["ready"])
        for _ in range(30):
            if not app_state["running"] or app_state["mode"] != "local":
                break
            time.sleep(0.1)
        if not app_state["running"] or app_state["mode"] != "local":
            break
        app_state["status"] = "active"
        set_fog(True)
        start = time.monotonic()
        toggle = False
        while app_state["running"] and app_state["mode"] == "local" \
                and (time.monotonic() - start < STATE):
            with display_lock:
                display.image(IMG["act2"] if toggle else IMG["act1"])
            toggle = not toggle
            time.sleep(FLASH)
    app_state["status"] = "idle"
    set_fog(False)
    with display_lock:
        display.image(BLACK)

# ── OSC Server ────────────────────────────────────────────────────
PFX = "/displaypi-1"

def osc_animation(addr, *args):
    if app_state["mode"] != "osc":
        return
    name = str(args[0]) if args else "off"
    maps = {
        "fog_loading": ("loading", "load1"),
        "fog_ready": ("ready", "ready"),
        "fog_active": ("active", "act1"),
    }
    if name in maps:
        s, key = maps[name]
        app_state["status"] = s
        show_image(key)
        set_fog(name == "fog_active")
        app_state["osc_active"] = True
    else:
        app_state["status"] = "idle"
        app_state["osc_active"] = False
        show_image("off")
        set_fog(False)

def osc_fog(addr, *args):
    if app_state["mode"] != "osc":
        return
    state = str(args[0]) if args else "off"
    set_fog(state.lower() == "on")

def osc_mode(addr, *args):
    mode = str(args[0]) if args else "local"
    if mode in ("local", "osc"):
        switch_mode(mode)

disp = Dispatcher()
disp.map(f"{PFX}/animation", osc_animation)
disp.map(f"{PFX}/fog", osc_fog)
disp.map(f"{PFX}/mode", osc_mode)

osc_server = ThreadingOSCUDPServer(("0.0.0.0", 7101), disp)
threading.Thread(target=osc_server.serve_forever, daemon=True).start()
print("OSC Server listening on port 7101")

# ── Flask ─────────────────────────────────────────────────────────
app = Flask(__name__)

HTML = r"""<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>displaypi-1</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,sans-serif;background:#1a1a2e;color:#eee;
     display:flex;justify-content:center;align-items:center;min-height:100vh}
.panel{background:#16213e;border-radius:16px;padding:2rem;text-align:center;
       max-width:380px;width:100%;box-shadow:0 8px 32px rgba(0,0,0,.4)}
h1{font-size:1.4rem;margin-bottom:1rem;color:#e94560}
.mode-row{display:flex;gap:.5rem;margin-bottom:1.2rem;justify-content:center}
.mode-btn{flex:1;padding:10px;border:none;border-radius:6px;cursor:pointer;
          font-weight:600;font-size:.9rem;transition:.2s}
.mode-local{background:#0f3460;color:#e94560}
.mode-osc{background:#533483;color:#c084fc}
.mode-active{box-shadow:0 0 0 2px #fff}
.btn{display:inline-block;padding:14px 40px;font-size:1.1rem;border:none;
     border-radius:8px;cursor:pointer;font-weight:600;transition:.2s;margin:.5rem}
.btn-start{background:#0f3460;color:#e94560}
.btn-start:hover{background:#1a1a4e}
.btn-stop{background:#e94560;color:#fff}
.btn-stop:hover{background:#c73a52}
.btn:disabled{opacity:.4;cursor:not-allowed}
.osc-warn{background:#533483;color:#e0b0ff;padding:10px;border-radius:8px;
          margin:.8rem 0;font-size:.85rem;display:none}
.status-row{display:flex;justify-content:space-between;margin:.8rem 0;
            padding:.8rem 1rem;background:#0f3460;border-radius:8px}
.status-label{color:#aaa;font-size:.85rem}
.status-value{font-weight:600}
.dot{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:6px}
.dot-green{background:#00ff88;box-shadow:0 0 8px #00ff88}
.dot-red{background:#ff4444;box-shadow:0 0 8px #ff4444}
</style>
</head>
<body>
<div class="panel">
<h1>⚡ displaypi-1</h1>
<div class="mode-row">
  <button class="mode-btn mode-local" id="btnLocal"
          onclick="setMode('local')">🎮 Lokal</button>
  <button class="mode-btn mode-osc" id="btnOsc"
          onclick="setMode('osc')">📡 OSC</button>
</div>
<div id="oscWarning" class="osc-warn">
  ⚠ OSC-Mode – TouchDesigner steuert. Lokal deaktiviert.
</div>
<button class="btn btn-start" id="btnStart" onclick="startRoutine()">▶ Start</button>
<button class="btn btn-stop" id="btnStop" onclick="stopRoutine()" disabled>⏹ Stop</button>
<div class="status-row">
  <span class="status-label">Modus</span>
  <span class="status-value" id="modeText">🎮 Lokal</span>
</div>
<div class="status-row">
  <span class="status-label">Status</span>
  <span class="status-value" id="statusText">⚪ idle</span>
</div>
<div class="status-row">
  <span class="status-label">OSC Port</span>
  <span class="status-value">7101</span>
</div>
<div class="status-row">
  <span class="status-label">Fog GPIO17</span>
  <span class="status-value" id="fogPin">
    <span class="dot dot-red"></span> LOW</span>
</div>
</div>
<script>
function updateStatus(){fetch('/api/status').then(r=>r.json()).then(d=>{
 let isOsc=d.mode==='osc',r=d.running;
 document.getElementById('btnLocal').className=
   'mode-btn mode-local'+(isOsc?'':' mode-active');
 document.getElementById('btnOsc').className=
   'mode-btn mode-osc'+(isOsc?' mode-active':'');
 document.getElementById('modeText').textContent=isOsc?'📡 OSC':'🎮 Lokal';
 document.getElementById('oscWarning').style.display=isOsc?'block':'none';
 document.getElementById('btnStart').disabled=r||isOsc;
 document.getElementById('btnStop').disabled=!r||isOsc;
 let m={'idle':'⚪ idle','loading':'🟡 fog loading',
        'ready':'🟢 fog ready','active':'🔴 fog active'};
 document.getElementById('statusText').textContent=m[d.status]||d.status;
 document.getElementById('fogPin').innerHTML=
   d.fog_pin==='HIGH'
     ?'<span class="dot dot-green"></span> HIGH'
     :'<span class="dot dot-red"></span> LOW';})}
function setMode(m){fetch('/api/mode/'+m,{method:'POST'}).then(updateStatus)}
function startRoutine(){fetch('/api/start',{method:'POST'}).then(updateStatus)}
function stopRoutine(){fetch('/api/stop',{method:'POST'}).then(updateStatus)}
setInterval(updateStatus,500);updateStatus();
</script>
</body>
</html>"""

@app.route("/")
def index():
    return render_template_string(HTML)

@app.route("/api/status")
def api_status():
    return jsonify({
        "running": app_state["running"],
        "status": app_state["status"],
        "fog_pin": app_state["fog_pin"],
        "mode": app_state["mode"],
        "osc_active": app_state["osc_active"],
    })

@app.route("/api/start", methods=["POST"])
def api_start():
    if not app_state["running"] and app_state["mode"] == "local":
        app_state["running"] = True
        t = threading.Thread(target=fog_loop, daemon=True)
        app_state["thread"] = t
        t.start()
    return jsonify({"ok": True})

@app.route("/api/stop", methods=["POST"])
def api_stop():
    app_state["running"] = False
    return jsonify({"ok": True})

@app.route("/api/mode/<mode>", methods=["POST"])
def api_mode(mode):
    if mode in ("local", "osc"):
        app_state["running"] = False
        switch_mode(mode)
    return jsonify({"ok": True, "mode": app_state["mode"]})

if __name__ == "__main__":
    print("displaypi-1 Web: http://0.0.0.0:5000 | OSC: :7101")
    app.run(host="0.0.0.0", port=5000, debug=False)
