#!/usr/bin/env python3
"""Weboberflaeche fuer displaypi-1 – Status & Testroutine-Steuerung."""

import threading
import time
import board
import busio
import digitalio
from flask import Flask, jsonify, render_template_string
from PIL import Image

# ── GPIO Setup ────────────────────────────────────────────────────
FOG_PIN = 17  # GPIO 17, Pin 11 – Nebelausgang

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(FOG_PIN, GPIO.OUT, initial=GPIO.LOW)

# ── Display Setup ─────────────────────────────────────────────────
def init_display():
    import adafruit_rgb_display.st7735 as st7735
    spi = busio.SPI(clock=board.SCK, MOSI=board.MOSI)
    cs = digitalio.DigitalInOut(board.D8)
    dc = digitalio.DigitalInOut(board.D25)
    reset = digitalio.DigitalInOut(board.D24)
    return st7735.ST7735R(
        spi, cs=cs, dc=dc, rst=reset,
        width=128, height=160, rotation=0, bgr=False,
    )

display = init_display()

# ── Bildlader ─────────────────────────────────────────────────────
BASE = "/home/tom/display-controller/img"

def load_image(path):
    img = Image.open(path).convert("RGB")
    return img.resize((160, 128), Image.LANCZOS).transpose(Image.ROTATE_90)

IMG = {
    "load1":  load_image(f"{BASE}/bild01_fog loading.png"),
    "load2":  load_image(f"{BASE}/bild02_fog loading.png"),
    "ready":  load_image(f"{BASE}/bild03_fog_ready.png"),
    "act1":   load_image(f"{BASE}/bild04_fog_active.png"),
    "act2":   load_image(f"{BASE}/bild05_fog_active.png"),
}

# ── App-State ─────────────────────────────────────────────────────
app_state = {
    "running": False,
    "status": "idle",     # idle | loading | ready | active
    "fog_pin": "LOW",
    "thread": None,
}

def set_fog(state):
    """Setzt den Nebel-GPIO und aktualisiert den Status."""
    if state == "active":
        GPIO.output(FOG_PIN, GPIO.HIGH)
        app_state["fog_pin"] = "HIGH"
    else:
        GPIO.output(FOG_PIN, GPIO.LOW)
        app_state["fog_pin"] = "LOW"

def fog_loop():
    """Hintergrund-Thread: Endlos-Schleife der 3 Zustaende."""
    FLASH = 0.5
    STATE = 3.0

    while app_state["running"]:
        # ── Loading ──
        app_state["status"] = "loading"
        set_fog("low")
        start = time.monotonic()
        toggle = False
        while app_state["running"] and (time.monotonic() - start < STATE):
            display.image(IMG["load2"] if toggle else IMG["load1"])
            toggle = not toggle
            time.sleep(FLASH)

        if not app_state["running"]:
            break

        # ── Ready ──
        app_state["status"] = "ready"
        set_fog("low")
        display.image(IMG["ready"])
        time.sleep(3.0)

        if not app_state["running"]:
            break

        # ── Active ──
        app_state["status"] = "active"
        set_fog("active")
        start = time.monotonic()
        toggle = False
        while app_state["running"] and (time.monotonic() - start < STATE):
            display.image(IMG["act2"] if toggle else IMG["act1"])
            toggle = not toggle
            time.sleep(FLASH)

    # Cleanup
    app_state["status"] = "idle"
    set_fog("low")
    black = Image.new("RGB", (128, 160), (0, 0, 0))
    display.image(black)

# ── Flask App ─────────────────────────────────────────────────────
app = Flask(__name__)

HTML = """<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>displaypi-1 – Fog Control</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, sans-serif; background: #1a1a2e;
               color: #eee; display: flex; justify-content: center;
               align-items: center; min-height: 100vh; }
        .panel { background: #16213e; border-radius: 16px; padding: 2rem;
                 text-align: center; max-width: 360px; width: 100%;
                 box-shadow: 0 8px 32px rgba(0,0,0,.4); }
        h1 { font-size: 1.4rem; margin-bottom: 1.5rem; color: #e94560; }
        .btn { display: inline-block; padding: 14px 40px; font-size: 1.1rem;
               border: none; border-radius: 8px; cursor: pointer;
               font-weight: 600; transition: .2s; margin: .5rem; }
        .btn-start { background: #0f3460; color: #e94560; }
        .btn-start:hover { background: #1a1a4e; }
        .btn-stop  { background: #e94560; color: #fff; }
        .btn-stop:hover  { background: #c73a52; }
        .btn:disabled { opacity: .4; cursor: not-allowed; }
        .status-row { display: flex; justify-content: space-between;
                      margin: 1.2rem 0; padding: .8rem 1rem;
                      background: #0f3460; border-radius: 8px; }
        .status-label { color: #aaa; font-size: .85rem; }
        .status-value { font-weight: 600; }
        .dot { display: inline-block; width: 10px; height: 10px;
               border-radius: 50%; margin-right: 6px; }
        .dot-green { background: #00ff88; box-shadow: 0 0 8px #00ff88; }
        .dot-red   { background: #ff4444; box-shadow: 0 0 8px #ff4444; }
        .dot-gray  { background: #555; }
    </style>
</head>
<body>
<div class="panel">
    <h1>⚡ displaypi-1</h1>

    <button class="btn btn-start" id="btnStart" onclick="startRoutine()">
        ▶ Testroutine starten
    </button>
    <button class="btn btn-stop" id="btnStop" onclick="stopRoutine()" disabled>
        ⏹ Stop
    </button>

    <div class="status-row">
        <span class="status-label">Status</span>
        <span class="status-value" id="statusText">🟢 idle</span>
    </div>
    <div class="status-row">
        <span class="status-label">Fog Pin (GPIO17)</span>
        <span class="status-value" id="fogPin">
            <span class="dot dot-gray"></span> LOW
        </span>
    </div>
</div>

<script>
function updateStatus() {
    fetch('/api/status')
        .then(r => r.json())
        .then(data => {
            const running = data.running;
            document.getElementById('btnStart').disabled = running;
            document.getElementById('btnStop').disabled = !running;

            const statusMap = {
                'idle':    '⚪ idle',
                'loading': '🟡 fog loading',
                'ready':   '🟢 fog ready',
                'active':  '🔴 fog active',
            };
            document.getElementById('statusText').textContent =
                statusMap[data.status] || data.status;

            const fogEl = document.getElementById('fogPin');
            if (data.fog_pin === 'HIGH') {
                fogEl.innerHTML = '<span class="dot dot-green"></span> HIGH';
            } else {
                fogEl.innerHTML = '<span class="dot dot-red"></span> LOW';
            }
        });
}
function startRoutine() { fetch('/api/start', {method:'POST'}).then(updateStatus); }
function stopRoutine()  { fetch('/api/stop',  {method:'POST'}).then(updateStatus); }

setInterval(updateStatus, 500);
updateStatus();
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
    })

@app.route("/api/start", methods=["POST"])
def api_start():
    if not app_state["running"]:
        app_state["running"] = True
        t = threading.Thread(target=fog_loop, daemon=True)
        app_state["thread"] = t
        t.start()
    return jsonify({"ok": True})

@app.route("/api/stop", methods=["POST"])
def api_stop():
    app_state["running"] = False
    return jsonify({"ok": True})

if __name__ == "__main__":
    print("displaypi-1 Webinterface: http://0.0.0.0:5000")
    app.run(host="0.0.0.0", port=5000, debug=False)
