# SPDX-FileCopyrightText: 2017 Tony DiCola for Adafruit Industries
# SPDX-FileCopyrightText: 2017 James DeVito for Adafruit Industries
# SPDX-License-Identifier: MIT

# This example is for use on (Linux) computers that are using CPython with
# Adafruit Blinka to support CircuitPython libraries. CircuitPython does
# not support PIL/pillow (python imaging library)!
from vcgencmd import Vcgencmd
#Per documentazione vedi https://pypi.org/project/vcgencmd/
from pathlib import Path
from mail import send_email # inserire i dati in mail.py
from datetime import datetime
import time
import os
import subprocess
from gpiozero import LED
import RPi.GPIO as GPIO
import board
from board import SCL, SDA
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import locale
vcgm = Vcgencmd()
# impostare la scritta dei giorni settimana e mesi, in italiano.
locale.setlocale(locale.LC_ALL, 'it_IT.utf-8')
def get_temp():
    temp = vcgm.measure_temp()
    return(temp)

def get_ora():
    ora=time.strftime("%H")
    minuti=time.strftime("%M")
    orario=ora+":"+minuti
    return(orario)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
led = LED(15)
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
#|modificare il valore temp=80000 in (temp=55000) per stagione estiva.         |
#|> [all]                                                                      |
#|> dtoverlay=gpio-fan,gpiopin=14,temp=55000                                   |
#|                                                                             |
#|Sfruttando il **GPIO-Fan**; si spegne la ventola quando raggiunge 10° in meno|
#|del valore che abbiamo stabilito per attivarla in **config.txt**.            |
#|-----------------------------------------------------------------------------|
# Fan Set the behaviour of a GPIO connected fan
GPIO.setup(14, GPIO.OUT)
# pulsante di spegnimento
GPIO.setup(4, GPIO.IN, pull_up_down = GPIO.PUD_UP)
# uscita led.
GPIO.setup(15, GPIO.OUT)
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
font2 = ImageFont.truetype('Montserrat-Light.ttf', 14)
# Some other nice Icon to : https://fontawesome.com/
font_icon = ImageFont.truetype('fa-solid-900.ttf', 18)
font_icon2 = ImageFont.truetype('fa-solid-900.ttf', 20)
font_icon3 = ImageFont.truetype('fa-brands-400.ttf', 26)
font_icon4 = ImageFont.truetype('fa-solid-900.ttf', 8)
#font_text_small = ImageFont.truetype('Montserrat-Medium.ttf', 8)

posta = 0 # variabile per segnalare invio mail
Cont = 0  # variabile per decidere scrittura giornaliera su FAN.txt
inizioDay = "00:00" # inizio giornata
fineDay = "23:59"   # fine giornata
ContFAN = 0 # variabile conteggio accensioni ventola
ValPinFAN = 0 # variabile controllo pin accensione ventola

if Path('ENEL.txt').is_file(): # controllo esistenza file
    f = open("ENEL.txt","r+")  # se esiste recupero dato dopo reboot
    for line in f:
        val = line.strip()
        Cont = int(val) # variabile controllo per scrivere su FAN.txt
    f.close()
    time.sleep(0.5)
else:
    writepath = 'ENEL.txt' # se non esiste lo creo
    mode = 'a' if os.path.exists(writepath) else 'w+'
    with open(os.open(writepath, os.O_CREAT | os.O_WRONLY, 0o777), mode) as f:
        f.write(str(Cont)) # scrivo valore
        f.close()
        time.sleep(0.5)
if Path('FanBkp.txt').is_file(): # controllo esistenza file
    f = open("FanBkp.txt","r+")  # se esiste recupero dato dopo reboot
    for line in f:
        val = line.strip()
        ContFAN = int(val) # variabile conteggio accensioni ventola
    f.close()
    time.sleep(0.5)
else:
    writepath = 'FanBkp.txt' # se non esiste lo creo
    mode = 'a' if os.path.exists(writepath) else 'w+'
    with open(os.open(writepath, os.O_CREAT | os.O_WRONLY, 0o777), mode) as f:
        f.write(str(ContFAN)) # scrivo il valore
        f.close()
        time.sleep(0.5)
i=0
while True:
    i+=1
    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    #
    now = datetime.now()
    GOW = now.strftime("%A - wk.%W")
    DMY = now.strftime("%d/%m/%Y  %H:%M")
    # registrazione su file FAN.txt delle attivazioni della ventola at Day
    Ora = get_ora()
    Day = time.ctime()
    writepath = 'FAN.txt'
    mode = 'a' if os.path.exists(writepath) else 'w'
    with open(os.open(writepath, os.O_CREAT | os.O_WRONLY, 0o777), mode) as f:
        if os.stat("FAN.txt").st_size == 0: # file vuoto
            f.write(Day) # scrittura prima volta oltre le ore 00:00
            f.close()                       
            time.sleep(0.5)
            Cont = 1
        if Ora == inizioDay and Cont == 0:
            Cont = 1
            f.write(Day)
            f.close()
            time.sleep(0.5)
        if Ora == fineDay and Cont == 1:
            Cont = 0
            testo=" FAN si è attivata " +str(ContFAN)+ " volte.\n"
            f.write(testo)
            f.close()
            time.sleep(0.5)
            ContFAN = 0 # azzeramento contatore accensioni ventola
            with open("FanBkp.txt","w+") as S:
                S.write(str(ContFAN))
                S.close()
                time.sleep(0.5)
        with open("ENEL.txt","w+") as S:
            val = Cont
            S.write(str(val))
            S.close()
            time.sleep(0.5)
            
    # Controllo integrità della ventola.
    Temp = get_temp()
    if Temp >= 80 or GPIO.input(4) == False: # Probabilmente la ventola è fuori uso o hai premuto il pulsante, mi spengo.
        led.blink()
        draw.text((x, top+6), "Shutdown", font=font1, fill=255)
        draw.text((x, top+20), "RPI4-NAS-HAS", font=font1, fill=255)
	# Icon brand RPi (63419)
        draw.text((x+95, top+8), chr(63419), font=font_icon3, fill=255)
        # Display image
        disp.image(image)
        disp.show()
        time.sleep(5)
        os.system("sudo shutdown -h now")
        break
    if Temp >= 70 and posta == 0: # primo avviso con mail.
        posta += 1
        send_email()
        time.sleep(0.5)

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
    draw.text((x+30, top), str(IP), font=font, fill=255)
    # Text Temperature CPU
    draw.text((x+98, top+11), str(Temp) + "°", font=font1, fill=255)
    # Text CPU
    draw.text((x, top+9), str(CPU), font=font, fill=255)
    # Text HDD used/total
    draw.text((x, top+17), str(Disk), font=font, fill=255)
    # Text Memory in use
    draw.text((x, top+25), str(MemUsage), font=font, fill=255)
    # Icon
    # Icon Wi-Fi (61931)
    draw.text((x+15, top+2), chr(61931), font=font_icon4, fill=255)
    if posta == 1:
        # Icon Mail (61664) inviato email di avviso poi mi spengo.
        draw.text((x, top+2), chr(61664), font=font_icon4, fill=255)
    if GPIO.input(14) == True: # pin state control = ON
        if ValPinFAN == 0:
            ContFAN += 1
            with open("FanBkp.txt","w+") as f:
                f.write(str(ContFAN)) # backup variabile dopo reboot
                f.close()
                time.sleep(0.5)
            ValPinFAN = 1
        # Icon FAN (63587) ignition confirmation
        draw.text((x+76, top+13), chr(63587), font=font_icon, fill=255)
    if GPIO.input(14) == False: # pin state control = OFF
        draw.text((x+98,top+27), chr(63587), font=font_icon4, fill=255)
        ValPinFAN = 0
        # Icon Temp (62154) temperature state is OK
        if Temp > 60 and Temp < 80:
            draw.text((x+85, top+13), chr(62152), font=font_icon2, fill=255)
        if Temp > 40 and Temp <= 60:
            draw.text((x+85, top+13), chr(62153), font=font_icon2, fill=255)
        if Temp <= 40:
            draw.text((x+85, top+13), chr(62154), font=font_icon2, fill=255)
    # visualizza conteggio accensione giornaliero del FAN.
    if ContFAN < 10:
        draw.text((x+98,top+24), "  00"+str(ContFAN), font=font, fill=255)
    if ContFAN < 100:
        draw.text((x+98,top+24), "  0"+str(ContFAN), font=font, fill=255)
    if ContFAN >= 100:
        draw.text((x+98,top+24), "  "+str(ContFAN), font=font, fill=255) 
        

    # Display image
    disp.image(image)
    disp.show()
    time.sleep(0.1)
    if i==15:
        i=0
        # visualizza seconda schermata con calendario e orario
        draw.rectangle((0,0,width,height),outline=0,fill=0)
        #
        draw.text((x,top), str(GOW), font=font2, fill=255)
        draw.text((x,top+18), str(DMY), font=font2, fill=255)
        # Display image
        disp.image(image)
        disp.show()
        time.sleep(1.5)
