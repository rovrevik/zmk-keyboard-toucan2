# build

The host needs Docker. The image is `zmkfirmware/zmk-build-arm:stable`, the same image the [ZMK v0.3 user-config workflow](https://github.com/zmkfirmware/zmk/blob/v0.3.0/.github/workflows/build-user-config.yml) uses. It is published for `linux/arm64` and `linux/amd64`.

From this repo:

```bash
docker compose run --rm build
```

Compose builds the image, mounts this repo at `/work`, copies `config/` into a gitignored `.west-workspace/`, and runs `west init -l config` there when `.west/` is missing. Then it runs `west update` and `west zephyr-export`, and runs [build.sh](build.sh) once inside the container. The Zephyr checkout stays in `.west-workspace/` so it does not replace [zephyr/module.yml](zephyr/module.yml).

On Linux, pass your user id so the generated trees are not root-owned:

```bash
HOST_UID="$(id -u)" HOST_GID="$(id -g)" docker compose run --rm build
```

Firmware:

- `build/toucan_left/zephyr/zmk.uf2`
- `build/toucan_right/zephyr/zmk.uf2`
- `build/settings_reset/zephyr/zmk.uf2`

The first run pulls the image and the west modules. Later runs reuse both. `.west-workspace/` and `build/` stay out of git.

## Reference

- [Toucan2 Keyboard](https://docs.beekeeb.com/toucan2-keyboard)
    - [Flashing the Toucan2 Firmware](https://docs.beekeeb.com/toucan2-keyboard/convert-toucan-to-toucan2#flashing-the-toucan2-firmware)
- [Quick Start, Keymap & Firmware](https://docs.beekeeb.com/toucan-keyboard/quick-start-keymap-and-firmware)

- [ZMK's USB logging page](https://v0-3-branch.zmk.dev/docs/development/usb-logging)
  ```bash
  # west build argument
  # -S zmk-usb-logging
  
  ls /dev/tty.usbmodem*
  sudo tio /dev/tty.usbmodemXXXX
  ```
  
- [ZMK Driver for Azoteq IQS5XX Trackpads](https://github.com/beekeeb/zmk_driver_azoteq)
  - [toucan_right.overlay](https://github.com/rovrevik/zmk-keyboard-toucan2/blob/main/boards/shields/toucan/toucan_right.overlay)
  - [azoteq,tps43-common.yaml](https://github.com/beekeeb/zmk_driver_azoteq/blob/master/dts/bindings/input/azoteq%2Ctps43-common.yaml)
  - [Azoteq TPS43](https://www.azoteq.com/product/i2c-trackpad-modules/)
  - [ZMK Pointing Devices](https://v0-3-branch.zmk.dev/docs/features/pointing)
  - [zmk-input-zoom](https://github.com/beekeeb/zmk-input-zoom)
