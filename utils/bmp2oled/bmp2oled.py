import pygame
import sys

image = pygame.image.load(sys.argv[1])
buffer = bytearray((image.get_height() // 8) * image.get_width())
i = 0
for y in range(image.get_height() // 8):
    for x in range(image.get_width()):
        byte = 0
        for bit in range(8):
            pixel = image.get_at((x, y * 8 + bit))
            if pixel[0] != 255:
                byte |= (1 << bit)
        buffer[i] = byte
        i += 1
print(repr(buffer))
