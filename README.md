# BlackAlps badge

This repository contains the blackAlps badge source, along with utilities to create user-created apps.

## Easy start

The easiest way is to use [Ampy](https://github.com/scientifichackers/ampy/tree/c0b568cf12b017bd9dfd7d61a7132b7d760278a0)
to store new files on the badge. To install on MacOS or GNU/Linux, simply type:

```bash
pip3 install --user adafruit-ampy
```

Once it's installed, on MacOS you can type the following to have a look at the
badge and to upload a new file:

```bash
ampy --port /dev/tty.usbserial-14410 ls
```

You can add the [template](utils/app_template/template.py) to the [apps](badgeOS/apps)
directory, and then upload it to the badge:

```bash
cp utils/app_template/template.py badgeOS/apps/myapp.py
ampy --port /dev/tty.usbserial-14410 put ./badgeOS/apps/myapp.py apps/myapp.py
```

Now you need to reset the board. The `ampy reset` doesn't seem to work, so you
need to remove and add the battery again.
