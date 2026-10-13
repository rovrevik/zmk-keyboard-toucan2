#!/usr/bin/env bash

# https://zmk.dev/docs/development/local-toolchain/build-flash

set -eu

cd /work/.west-workspace

# Left half: display, ZMK Studio
west build -s zmk/app -d /work/build/toucan_left -b seeeduino_xiao_ble \
  --pristine \
  -S studio-rpc-usb-uart \
  -- \
  -DSHIELD="toucan_left rgbled_adapter nice_view_gem" \
  -DZMK_CONFIG=/work/config \
  -DZMK_EXTRA_MODULES=/work \
  -DCONFIG_ZMK_STUDIO=y

# build/toucan_left/zephyr/zmk.uf2

# Right half: trackpad
west build -s zmk/app -d /work/build/toucan_right -b seeeduino_xiao_ble \
  --pristine \
  -- \
  -DSHIELD="toucan_right rgbled_adapter" \
  -DZMK_CONFIG=/work/config \
  -DZMK_EXTRA_MODULES=/work

# build/toucan_right/zephyr/zmk.uf2

# Clear bonds and settings
west build -s zmk/app -d /work/build/settings_reset -b seeeduino_xiao_ble \
  --pristine \
  -- \
  -DSHIELD="settings_reset" \
  -DZMK_CONFIG=/work/config \
  -DZMK_EXTRA_MODULES=/work

# build/settings_reset/zephyr/zmk.uf2
