#!/usr/bin/env bash

# https://zmk.dev/docs/development/local-toolchain/build-flash

set -eu

cd /work/.west-workspace

ZMK_USB_LOGGING=0

# Left half: display, ZMK Studio
west build -s zmk/app -d /work/build/toucan_left -b seeeduino_xiao_ble \
  --pristine \
  -S studio-rpc-usb-uart \
  ${ZMK_USB_LOGGING:+-S zmk-usb-logging} \
  -- \
  -DSHIELD="toucan_left rgbled_adapter nice_view_gem" \
  -DZMK_CONFIG=/work/config \
  -DZMK_EXTRA_MODULES=/work \
  -DCONFIG_ZMK_STUDIO=y

# build/toucan_left/zephyr/zmk.uf2

# Right half: trackpad
# https://zmk.dev/docs/development/usb-logging
west build -s zmk/app -d /work/build/toucan_right -b seeeduino_xiao_ble \
  --pristine \
  ${ZMK_USB_LOGGING:+-S zmk-usb-logging} \
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
