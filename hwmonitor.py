# SPDX-FileCopyrightText: 2017 Tony DiCola for Adafruit Industries
# SPDX-FileCopyrightText: 2017 James DeVito for Adafruit Industries
# SPDX-License-Identifier: MIT

# This example is for use on (Linux) computers that are using CPython with
# Adafruit Blinka to support CircuitPython libraries. CircuitPython does
# not support PIL/pillow (python imaging library)!
from vcgencmd import Vcgencmd
#Per documentazione vedi https://pypi.org/project/vcgencmd/
import time
import subprocess
import RPi.GPIO as GPIO
import board
from board import SCL, SDA
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

vcgm = Vcgencmd()

def get_temp():
    temp = vcgm.measure_temp()
    return(temp)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# use Pi header pin numbering convention
#|-----------Attivazione controllo automatico temparatura con ventola----------|
#|-----------------------------------------------------------------------------|
#|sudo raspi-config                                                            |
#|-----------------------------------------------------------------------------|
#|4 Performance Options                                                        |
#|- P4 Fan (yes, 14, ok, 80, ok, ok) Set the behaviour of a GPIO connected fan |
#|                                                                             |
#|Finish                                                                       |
#|-----------------------------------------------------------------------------|
#|digitare:                                                                    |
#|sudo nano /boot/config.txt                                                   |
#|modificare il valore temp=80000 in (temp=46000) o a piacere.                              |
#|> [all]                                                                      |
#|> dtoverlay=gpio-fan,gpiopin=14,temp=46000                                   |
#|                                                                             |
#|Sfruttando il **GPIO-Fan**; si spegne la ventola quando raggiunge 10° in meno|
#|del valore che abbiamo stabilito per attivarla in **config.txt**.            |
#|-----------------------------------------------------------------------------|
# Fan Set the behaviour of a GPIO connected fan
GPIO.setup(14, GPIO.OUT)
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
font_icon = ImageFont.truetype('fa-solid-900.ttf', 18)
font_icon2 = ImageFont.truetype('fa-solid-900.ttf', 20)
font_icon3 = ImageFont.truetype('fa-brands-400.ttf', 26)
font_icon4 = ImageFont.truetype('fa-solid-900.ttf', 8)
#font_text_small = ImageFont.truetype('Montserrat-Medium.ttf', 8)

while True:
    
    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,width,height), outline=0, fill=0)

    # Controllo funzionamento ventola
    Temp = get_temp()
    if Temp >= 70: # Probabilmente la ventola è fuori uso.
        draw.text((x, top+6), "Shutdown", font=font1, fill=255)
        draw.text((x, top+20), "RPI4-NAS", font=font1, fill=255)
	# Icon RPi (63419)
        draw.text((x+85, top+8), chr(63419), font=font_icon3, fill=255)
        # Display image
        disp.image(image)
        disp.show()
        time.sleep(3)
        os.system("sudo shutdown -h now")

    # https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load

    cmd = "hostname -I | cut -f 2 -d '='"
    IP = subprocess.check_output(cmd, shell=True).decode("utf-8")
    #
    cmd = "top -bn1 | grep load | awk '{printf \"CPU: %.2f\", $(NF-2)}'"
    CPU = subprocess.check_output(cmd, shell=True).decode("utf-8")
    #
    Temp = get_temp()
    #
    cmd = "free -m | awk 'NR==2{printf \"Mem: %.2f%%\", $3*100/$2 }'"
    MemUsage = subprocess.check_output(cmd, shell=True).decode("utf-8")
    #
    cmd = 'df -h | awk \'$NF=="/"{printf "HDD: %d/%d GB ", $3,$2,$5}\''
    Disk = subprocess.check_output(cmd, shell=True).decode("utf-8")

    # Write four lines of text
    # Text IP address
    draw.text((x+110, top), str(IP), font=font, fill=255)
    # Text Temperature CPU
    draw.text((x+98, top+13), str(Temp) + "°", font=font1, fill=255)
    # Text CPU
    draw.text((x, top+9), str(CPU), font=font, fill=255)
    # Text HDD used/total
    draw.text((x, top+17), str(Disk), font=font, fill=255)
    # Text Memory in use
    draw.text((x, top+25), str(MemUsage), font=font, fill=255)
    # Icon
    # Icon Wi-Fi (61931)
    draw.text((x+15, top+2), chr(61931), font=font_icon4, fill=255)
    if GPIO.input(14) == True: # pin state control = ON
        # Icon FAN (63587) ignition confirmation
        draw.text((x+76, top+13), chr(63587), font=font_icon, fill=255)
    if GPIO.input(14) == False: # pin state control = OFF
        # Icon Temp (62154) temperature state is OK
        draw.text((x+85, top+13), chr(62154), font=font_icon2, fill=255)

    # Display image
    disp.image(image)
    disp.show()
    time.sleep(0.1)
