# Oled-ssd1306-hwmonitor
Per Raspberry Pi con GPIO da 40 pin dal PiZero al Pi4.
Invio mail di avviso raggiunto i 70°C; 
aggiunto spegnimento automatico se la temperatura raggiunge i 80°C, ( esempio: rottura della ventola).
Aggiornato sistema automatico ripristino dati in caso di reboot per calo tensione.
Aggiunto seconda schermata per visualizzare calendario e ora corrente.
Inserire in mail.py i parametri per inviare e ricevere la email.
Calibrato per oled 0,91 128x32 i2c.
Aggiunto spegnimento con pulsante e led per controllo.
Per problemi di convivenza con OpenMediaVault e Home Assistant Supervised, ho dovuto inserire il programma di visualizzazione per ssd1306 in Ambiente Virtuale Python.

![RPi4-NAS_00](https://www.schenardi.it/public/RPi4-NAS/images/RPi4-NAS_00.jpg)


Vedi README.pdf
