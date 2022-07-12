from ctypes import sizeof
import enum
import os
import time
import argparse
from math import floor

import io

from rpi_ws281x import PixelStrip, Color

import xwd_module as xwd_mod
import led_func_module as led_mod
from matrix_config import matrices

# LED strip configuration:
LED_COUNT = 384        # Number of LED pixels.
LED_PIN = 13          # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN = 10        # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10          # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 4  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 1       # set to '1' for GPIOs 13, 19, 41, 45 or 53

FRAMEBUFFER_PATH = "../frameBuffer/Xvfb_screen0"


if __name__ == "__main__":
    # Create NeoPixel object with appropriate configuration.
    strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    file_lenght = os.stat(FRAMEBUFFER_PATH).st_size
    print("File Size", file_lenght)
    
    #with io.open(FRAMEBUFFER_PATH, "rb", buffering=0) as f:
    if True:
        # memory-map the file, size 0 means whole file
        #mm = mmap.mmap(f.fileno(), 0, access=1)

        f = io.open(FRAMEBUFFER_PATH, mode="rb", buffering=0)
        
        xwd = xwd_mod.xwd_open(f)

        print("Virtual Frame Buffer stats:")
        print(" Visual Class:", xwd.visual_class)
        print(" Header Length:", xwd.header_size)
        print(" Screen Width:", xwd.pixmap_width)
        print(" Screen Height:", xwd.pixmap_height)
        print(" Bytes per line:", xwd.bytes_per_line)

        offset_after_header = f.tell()
        print("Start offset after header", offset_after_header)

        program_start = time.time()
        try:
            while True:
                f = io.open(FRAMEBUFFER_PATH, mode="rb", buffering=0)
                # measure time
                loop_start = time.time()

                # reset file pointer to 0 to read the file again
                xwd = xwd_mod.xwd_open(f)
                #f.seek(offset_after_header, os.SEEK_SET)

                #line reading is dependent on memory mapping
                line_index = 0
                for line in xwd:
                    lineIt = iter(line)
                    currline = list(zip(lineIt, lineIt, lineIt))

                    mat_index = 0
                    for mat in matrices:
                        if floor(mat[1] / 8) == floor(line_index / 8):
                            pxl_to_map = currline[mat[0]:mat[0]+8] #one line of matrix
                            [ strip.setPixelColor(( mat_index * 64) + ((line_index % 8)* 8) + ind, Color(px[0],px[1],px[2])) for ind, px in enumerate(pxl_to_map) ]
                        mat_index += 1
                    line_index += 1

                strip.show()
                #show statistics
                print(f"Frame Time: {round(time.time()-loop_start, 3)}", f" Time since Start: {round(time.time()-program_start, 1)}", end="\r")

        except KeyboardInterrupt:
            led_mod.fastColorWipe(strip, Color(0, 0, 0))
            strip.show()

        f.close()

    led_mod.fastColorWipe(strip, Color(0, 0, 0))
    strip.show()
    print("", end="\r")