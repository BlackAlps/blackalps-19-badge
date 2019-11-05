# Badge full firmware image

This is the firmware image flashed on all the badges.

To reflash the badge, simply reboot the badge in bootloader mode by connecting the two pads in J9 together.
Then, type the following command (you'll need [ESPTool](https://github.com/espressif/esptool)):

```
python3 esptool.py --port /dev/ttyUSB0 --baud 460800 write_flash -z 0x1000 image.bin
```

