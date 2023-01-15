#!/bin/python
# Semplice script per spegnere il Raspberry Pi con la semplice pressione di un pulsante.
# by Inderpreet Singh
import RPi.GPIO as GPIO
import time
import os
# Utilizzare i numeri di pin SOC Broadcom.
# Imposta il Pin con i pullup interni abilitati e il PIN in modalità lettura.
GPIO.setwarnings(False) # Disabilita i messaggi di avviso.
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN, pull_up_down = GPIO.PUD_UP) # 10k connessa tra 3,3V e l’ingresso.
# La nostra funzione su cosa fare quando si preme il pulsante.
def Shutdown(channel):
    os.system("sudo shutdown -h now")
# Aggiungi la funzione da eseguire quando si verifica l'evento di pressione del pulsante.
GPIO.add_event_detect(4, GPIO.FALLING, callback = Shutdown, bouncetime = 2000)
LED = 15 # Definisce il numero della porta GPIO che alimenta il led.
GPIO.setup(LED, GPIO.OUT) # Abilita uscita GPIO al led.
while 1: # Ora aspetta!
    if GPIO.input(4) == 0: # Sì GPIO attivo.
        GPIO.output(LED, GPIO.HIGH) # Lo accendiamo
    else : # Altrimenti
        GPIO.output(LED, GPIO.LOW) # Lo spegniamo
time.sleep(1)
