FROM zmkfirmware/zmk-build-arm:stable
WORKDIR /work

# keymap-drawer provides the `keymap` command used by draw.py.
# https://github.com/caksoylar/keymap-drawer
RUN apt-get update \
    && apt-get install -y --no-install-recommends python3-venv \
    && python3 -m venv /opt/keymap-drawer \
    && /opt/keymap-drawer/bin/pip install --no-cache-dir 'keymap-drawer==0.23.0' \
    && rm -rf /var/lib/apt/lists/*
