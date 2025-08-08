#!/usr/bin/env bash
# pyShelf installer
# - Installs prerequisites
# - Creates pyshelf user and directories
# - Clones (or uses local tree) into /opt/pyshelf
# - Installs uv for the pyshelf user
# - uv sync + one-time DB init + static build
# - Writes config
# - Installs & starts systemd services

set -euo pipefail

REPO_URL="${REPO_URL:-https://github.com/th3r00t/pyShelf.git}"
REPO_REF="${REPO_REF:-0.8.0--dev}"
INSTALL_DIR="/opt/pyshelf"
ETC_DIR="/etc/pyshelf"
STATE_DIR="/var/lib/pyshelf"
LOG_DIR="/var/log/pyshelf"
BOOKPATH_DEFAULT="/mnt/books"
USER="pyshelf"
GROUP="pyshelf"
PUBLIC_HOST="0.0.0.0"
PORT="8080"
MODE="git" # or "local" with --local

if [[ "${1:-}" == "--local" ]]; then MODE="local"; fi

need_cmd() { command -v "$1" >/dev/null 2>&1; }
die() { echo "error: $*" >&2; exit 1; }

#--- Detect distro & install prereqs -------------------------------------------------
install_prereqs() {
  if [[ -f /etc/arch-release ]]; then
    sudo pacman -Sy --noconfirm --needed git curl python python-pip gcc base-devel libxml2 libxslt libjpeg-turbo zlib
  elif [[ -f /etc/debian_version ]]; then
    sudo apt-get update
    sudo apt-get install -y git curl python3 python3-venv python3-dev build-essential libxml2-dev libxslt1-dev libjpeg-dev zlib1g-dev
  elif [[ -f /etc/fedora-release ]]; then
    sudo dnf install -y git curl python3 python3-devel gcc gcc-c++ libxml2-devel libxslt-devel libjpeg-turbo-devel zlib-devel
  else
    die "Unsupported distro. Add your package steps here."
  fi
}

#--- Create user, dirs, config ------------------------------------------------------
setup_user_dirs() {
  if ! id -u "$USER" >/dev/null 2>&1; then
    sudo useradd --system --create-home --home-dir "$STATE_DIR" "$USER"
  fi

  sudo mkdir -p "$ETC_DIR" "$STATE_DIR" "$LOG_DIR" "$BOOKPATH_DEFAULT"
  # Try to add group if missing
  if ! getent group "$GROUP" >/dev/null 2>&1; then
    sudo groupadd -f "$GROUP" || true
    sudo usermod -g "$GROUP" "$USER" || true
  fi

  sudo chown -R "$USER":"$GROUP" "$STATE_DIR" "$LOG_DIR" || sudo chown -R "$USER":"$USER" "$STATE_DIR" "$LOG_DIR"
  sudo chown -R "$USER":"$GROUP" "$BOOKPATH_DEFAULT" || true

  # default config
  sudo tee "$ETC_DIR/config.json" >/dev/null <<JSON
{
  "TITLE": "pyShelf E-Book Server",
  "VERSION": "0.8.0-dev",
  "BOOKPATH": "$BOOKPATH_DEFAULT",
  "DB_HOST": "localhost",
  "DB_PORT": "5432",
  "DB_ENGINE": "sqlite",
  "DATABASE": "pyshelf",
  "USER": "pyshelf",
  "PASSWORD": "pyshelf",
  "BOOKSHELF": "data/shelf.json",
  "ALLOWED_HOSTS": ["localhost","127.0.0.1","[::1]","0.0.0.0"],
  "BUILD_MODE": "production"
}
JSON
}

ensure_runtime_dirs() {
  sudo mkdir -p "$INSTALL_DIR/data" "$INSTALL_DIR/src/frontend/static/styles"
  sudo chown -R "$USER":"$GROUP" "$INSTALL_DIR/data" "$INSTALL_DIR/src/frontend/static"
}


#--- Fetch source -------------------------------------------------------------------
fetch_source() {
  if [[ "$MODE" == "git" ]]; then
    sudo mkdir -p "$INSTALL_DIR"
    if [[ ! -d "$INSTALL_DIR/.git" ]]; then
      sudo git clone "$REPO_URL" "$INSTALL_DIR"
    fi
    cd "$INSTALL_DIR"
    sudo git fetch --all --tags
    sudo git checkout "$REPO_REF"
  else
    # local tree -> /opt/pyshelf
    sudo rm -rf "$INSTALL_DIR"
    sudo mkdir -p "$INSTALL_DIR"
    sudo cp -a . "$INSTALL_DIR"
    cd "$INSTALL_DIR"
  fi
  sudo chown -R "$USER":"$GROUP" "$INSTALL_DIR" || true
}

#--- Install uv for the pyshelf user ------------------------------------------------
install_uv_for_user() {
  # Install uv into /home/pyshelf/.local/bin
  sudo -u "$USER" sh -lc 'command -v uv >/dev/null 2>&1 || (curl -LsSf https://astral.sh/uv/install.sh | sh)'
  sudo -u "$USER" sh -lc 'uv --version' || die "uv not available for $USER"
}

#--- Python deps (uv) ---------------------------------------------------------------
sync_python() {
  # Ensure PYTHONPATH=src so src/ layout packages (frontend, backend) import
  sudo -u "$USER" sh -lc "cd '$INSTALL_DIR' && PYTHONPATH=src uv sync"
}

#--- One-time prework: create DB & compile static -----------------------------------
prework() {
  # Create DB/tables
  sudo -u "$USER" sh -lc "cd '$INSTALL_DIR' && PYTHONPATH=src uv run python - <<'PY'
from backend.lib.config import Config
from backend.lib.storage import Storage
import os
Storage(Config(os.getcwd())).create_tables()
print('DB initialized.')
PY"

  # Compile SASS directly (avoid importing your app module)
  sudo -u "$USER" sh -lc "cd '$INSTALL_DIR' && PYTHONPATH=src uv run python - <<'PY'
import sass, os, sys
from pathlib import Path

sass_in  = 'src/frontend/static/styles/pyShelf.sass'
css_out  = 'src/frontend/static/styles/pyShelf.css'

Path(os.path.dirname(css_out)).mkdir(parents=True, exist_ok=True)
compiled, _map = sass.compile(
    filename=sass_in,
    source_map_filename=sass_in,
    output_style='compressed',
    include_paths=['node_modules','src/frontend/static/styles']
)
with open(css_out, 'w') as f:
    f.write(compiled)
print('Static assets compiled.')
PY"
}

#--- Systemd units ------------------------------------------------------------------
install_systemd() {
  # Service: runs uvicorn against FastAPI app object
  sudo tee /etc/systemd/system/pyshelf.service >/dev/null <<UNIT
[Unit]
Description=pyShelf E-Book Server
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$INSTALL_DIR
# enable src/ layout without installing the package
Environment=PYTHONUNBUFFERED=1
Environment=PYTHONPATH=$INSTALL_DIR/src
Environment=PATH=/home/$USER/.local/bin:/usr/local/bin:/usr/bin:/bin
# NOTE: bind public by default
ExecStart=/usr/bin/env bash -lc 'uv run uvicorn frontend.FastAPIServer:app --host $PUBLIC_HOST --port $PORT'
Restart=on-failure
RestartSec=3
StandardOutput=append:$LOG_DIR/pyshelf.out.log
StandardError=append:$LOG_DIR/pyshelf.err.log
LimitNOFILE=65536

[Install]
WantedBy=multi-user.target
UNIT

  # One-shot nightly scan service+timer
  sudo tee /etc/systemd/system/pyshelf-scan.service >/dev/null <<UNIT
[Unit]
Description=pyShelf: scan library path and import new books

[Service]
Type=oneshot
User=$USER
WorkingDirectory=$INSTALL_DIR
Environment=PYTHONPATH=$INSTALL_DIR/src
Environment=PATH=/home/$USER/.local/bin:/usr/local/bin:/usr/bin:/bin
ExecStart=/usr/bin/env bash -lc 'uv run python - <<PY
import os
from backend.lib.config import Config
from backend.lib.library import Catalogue
cfg = Config(os.getcwd())
Catalogue(cfg).import_books()
PY'
UNIT

  sudo tee /etc/systemd/system/pyshelf-scan.timer >/dev/null <<'UNIT'
[Unit]
Description=Run pyShelf scan nightly

[Timer]
OnCalendar=03:30
Persistent=true
Unit=pyshelf-scan.service

[Install]
WantedBy=timers.target
UNIT

  sudo systemctl daemon-reload
  sudo systemctl enable --now pyshelf.service
  sudo systemctl enable --now pyshelf-scan.timer
}

main() {
  install_prereqs
  setup_user_dirs
  fetch_source
  install_uv_for_user
	ensure_runtime_dirs
  sync_python
  prework
  install_systemd

  echo
  echo "pyShelf installed."
  echo "  URL:    http://$PUBLIC_HOST:$PORT/"
  echo "  Config: $ETC_DIR/config.json"
  echo "  Books:  $BOOKPATH_DEFAULT"
  echo "  Repo:   $INSTALL_DIR"
  echo "  Logs:   $LOG_DIR"
}

main "$@"

