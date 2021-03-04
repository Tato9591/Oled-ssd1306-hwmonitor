# SPDX-FileCopyrightText: 2017 Tony DiCola for Adafruit Industries
# SPDX-FileCopyrightText: 2017 James DeVito for Adafruit Industries
# SPDX-License-Identifier: MIT

# This example is for use on (Linux) computers that are using CPython with
# Adafruit Blinka to support CircuitPython libraries. CircuitPython does
# not support PIL/pillow (python imaging library)!

import time
import subprocess

from board import SCL, SDA
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306


# Create the I2C interface.
i2c = busio.I2C(SCL, SDA)

# Create the SSD1306 OLED class.
# The first two parameters are the pixel width and pixel height.  Change these
# to the right size for your display!
disp = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

# Clear display.
disp.fill(0)
disp.show()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new("1", (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0


# Load default font.
font = ImageFont.load_default()

# Alternatively load a TTF font.  Make sure the .ttf font file is in the same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font1 = ImageFont.truetype('Montserrat-Light.ttf', 12)
# Some other nice Icon to : https://fontawesome.com/
font_icon = ImageFont.truetype('fa-solid-900.ttf', 20)
font_text_small = ImageFont.truetype('Montserrat-Medium.ttf', 8)

while True:
    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,width,height), outline=0, fill=0)

    # https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load

    cmd = "hostname -I | cut -f 2 -d '='"
    IP = subprocess.check_output(cmd, shell=True).decode("utf-8")
    #
    cmd = "top -bn1 | grep load | awk '{printf \"CPU: %.2f\", $(NF-2)}'"
    CPU = subprocess.check_output(cmd, shell=True).decode("utf-8")
    #
    cmd = "vcgencmd measure_temp |cut -f 2 -d '='"
    Temp = subprocess.check_output(cmd, shell=True).decode("utf-8")
    #
    cmd = "free -m | awk 'NR==2{printf \"Mem: %.2f%%\", $3*100/$2 }'"
    MemUsage = subprocess.check_output(cmd, shell=True).decode("utf-8")
    #
    cmd = 'df -h | awk \'$NF=="/"{printf "HDD: %d/%d GB ", $3,$2,$5}\''
    Disk = subprocess.check_output(cmd, shell=True).decode("utf-8")

    # Write four lines of text
    # Text IP address
    draw.text((x, top), "pi@" + str(IP), font=font, fill=255)
    # Text Temperatura CPU
    draw.text((x+89, top+15), str(Temp), font=font1, fill=255)
    # Text CPU
    draw.text((x, top+8), str(CPU), font=font, fill=255)
    # Text HDD usato/totale
    draw.text((x, top+16), str(Disk), font=font, fill=255)
    # Text Memoria in uso
    draw.text((x, top+24), str(MemUsage), font=font, fill=255)

    # Icon
    # Icon Temp (62153)
    draw.text((x+73, top+13), chr(62153), font=font_icon, fill=255)
    # Icon FAN (63587)
    #draw.text((x+67, top+13), chr(63587), font=font_icon, fill=255)

    # Display image
    disp.image(image)
    disp.show()
    time.sleep(0.1)
