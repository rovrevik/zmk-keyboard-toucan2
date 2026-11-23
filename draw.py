#!/usr/bin/env python3
import io
import shutil
import subprocess
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent
CONFIG = REPO / "keymap_drawer.config.yaml"
KEYMAP = REPO / "config" / "toucan.keymap"
LAYOUT = REPO / "boards" / "shields" / "toucan" / "toucan.dtsi"
OUT = REPO / "build" / "keymap"

# display-name from config/toucan.keymap; order controls SVG layout, omit to hide
LAYERS = [
    "BasC",
    "CsrC",
    "NumC",
    "SymC",
    "Func",
    "Mouse",
    "BasG",
    "CsrG",
    "NumG",
    "SymG",
    # "Function",
]

# parsed display-name -> SVG section header (layer_legend_map sets thumb hold labels)
LAYER_RENAME = {
    "BasC": "macOS Base (BasC CAGS)",
    "CsrC": "macOS Cursor (CsrC CAGS)",
    "NumC": "macOS Number Pad (NumC CAGS)",
    "SymC": "macOS Symbol Pad (SymC CAGS)",
    "Func": "Function Pad",
    "Mouse": "Mouse",
    "Function": "Globe",
    "BasG": "Linux Base (BasG GASC)",
    "CsrG": "Linux Cursor (CsrG GASC)",
    "NumG": "Linux Number Pad (CsrG GASC)",
    "SymG": "Linux Symbol Pad (SymG GASC)",
}

# Thumb layer-tap key positions -> hold label (same for CAGS and GASC)
THUMB_HOLD_LEGEND = {
    30: "mouse",
    31: "cursor",
    32: "number",
    34: "symbol",
}

def enrich_held_layer_legends(layers: dict[str, list]) -> None:
    """Label empty held &trans activator keys from thumb position, not CAGS/GASC base layer."""
    for layer_name, layer_keys in layers.items():
        if layer_name in ("BasC", "BasG"):
            continue
        for idx, key in enumerate(layer_keys):
            if isinstance(key, dict) and "held" in key.get("type", "") and (legend := THUMB_HOLD_LEGEND.get(idx)):
                layer_keys[idx] = {"h": legend, "type": key["type"]}

if not shutil.which("keymap"):
    raise SystemExit(f"keymap-drawer required")

parsed = subprocess.check_output(
    ["keymap", "-c", str(CONFIG), "parse", "-z", str(KEYMAP)],
    text=True,
)
data = yaml.safe_load(parsed)
layers = data["layers"]

enrich_held_layer_legends(layers)

unknown = [name for name in LAYERS if name not in layers]
if unknown:
    raise SystemExit(f"Unknown layer name(s): {', '.join(unknown)}")

name_map = {parsed: LAYER_RENAME.get(parsed, parsed) for parsed in LAYERS if parsed in layers}
data["layers"] = {name_map[parsed]: layers[parsed] for parsed in LAYERS if parsed in layers}

for combo in data.get("combos", []):
    if layer_list := combo.get("l"):
        combo["l"] = [name_map.get(name, name) for name in layer_list]

buf = io.StringIO()
yaml.safe_dump(
    data,
    buf,
    width=160,
    sort_keys=False,
    default_flow_style=None,
    allow_unicode=True,
)

OUT.mkdir(parents=True, exist_ok=True)
KEYMAP_SVG = OUT / "keymap.svg"

subprocess.run(
    [
        "keymap",
        "-c",
        str(CONFIG),
        "draw",
        "-d",
        str(LAYOUT),
        "-l",
        "default_layout",
        "-",
        "-o",
        str(KEYMAP_SVG),
    ],
    input=buf.getvalue(),
    text=True,
    check=True,
)
print(f"Generated {KEYMAP_SVG}")
