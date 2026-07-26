#!/usr/bin/env bash
# ============================================================
# install_service.sh – displaypi-1 systemd-Dienst installieren
# ============================================================
set -euo pipefail

USER="${1:-$USER}"
SERVICE_NAME="displaypi-1"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
SERVICE_FILE="$PROJECT_DIR/systemd/${SERVICE_NAME}.service"
SYSTEMD_DIR="/etc/systemd/system"

echo "=== displaypi-1 systemd Installation ==="
echo "Benutzer:  $USER"
echo "Projekt:   $PROJECT_DIR"
echo ""

# 1. Service-Datei vorbereiten
echo "[1/4] Service-Datei erstellen..."
TMP_SERVICE=$(mktemp)
sed "s/{{USER}}/$USER/g" "$SERVICE_FILE" | sudo tee "$SYSTEMD_DIR/${SERVICE_NAME}.service" > /dev/null
echo "  -> $SYSTEMD_DIR/${SERVICE_NAME}.service"

# 2. systemd reload
echo "[2/4] systemd daemon-reload..."
sudo systemctl daemon-reload

# 3. Service aktivieren (Autostart)
echo "[3/4] Service aktivieren..."
sudo systemctl enable "$SERVICE_NAME"

# 4. Service starten
echo "[4/4] Service starten..."
sudo systemctl start "$SERVICE_NAME"

echo ""
echo "=== Installation abgeschlossen ==="
echo "Status:   systemctl status $SERVICE_NAME"
echo "Logs:     journalctl -u $SERVICE_NAME -f"
echo "Stop:     sudo systemctl stop $SERVICE_NAME"
echo "Deaktivieren: sudo systemctl disable $SERVICE_NAME"
