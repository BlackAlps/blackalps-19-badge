# bmp2oled

This script converts a bitmap image to a byte array to be displayed on the OLEd screen.

## Dependancies

This script needs pyGame to be used :

```
pip install pygame
```

## Usage

Create the bytearray with bmp2oled :
```
python3 bmp2oled.py <image>
```

Then, use this sample code to display the image on the screen :
```
import framebuf

byte_array = <bmp2oled output>

width = 128
height = 64

oled.fill(0)
fb = framebuf.FrameBuffer(byte_array,width ,height , framebuf.MVLSB)
oled.blit(fb, 0,0)
oled.show()
```

