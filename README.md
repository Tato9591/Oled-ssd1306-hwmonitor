# Oled-ssd1306-hwmonitor



Per Raspberry pi a 40 pin dal PiZero al Pi4



```

sudo apt-get update

```



```

sudo apt-get install -y python3 git python3-pip

```



```

sudo apt-get install -y python3-pil

```



```

sudo pip3 install adafruit-circuitpython-ssd1306

```



```

sudo apt-get install -y i2c-tools

```



```

sudo raspi-config

```



> 3 Interface Options 

>

> - P5 IC2

>

> Finish



```

sudo reboot

```



Eseguire il comando seguente dal prompt del terminale per analizzare/rilevare i dispositivi I2C :



```

sudo i2cdetect -y 1

```



 Dovrebbe essere visualizzato quanto segue:



<img src="https://www.schenardi.it/public\RPi4-NAS\images\i2c.PNG" alt="i2c" style="zoom:50%;" />



Accelerare la visualizzazione Per ottenere migliori prestazioni, eseguire questa modifica di configurazione con: 



```

sudo nano /boot/config.txt

```



 e aggiungere alla voce presente che trovi **,i2c_baudrate=400000**



>  dtparam=i2c_arm=on,i2c_baudrate=400000 



Usare **CTRL+O** per salvare, **Invio** e quindi **CTRL+X** per uscire .



Collegamento ssd1306 128x32 al GPIO del Raspberry Pi.



<img src="https://www.schenardi.it/public\RPi4-NAS\images\sch_ssd1306.png" alt="sch_ssd1306" style="zoom:50%;" />







###### Verifica del dispositivo OLED 128x32 I2C



Scaricare



```

git clone https://github.com/Tato9591/Oled-ssd1306-hwmonitor.git

```



```

cd Oled-ssd1306-hwmonitor

```



```

python3 hwmonitor.py

```



e dovresti vedere qualcosa come la seguente immagine:



<img src="https://www.schenardi.it/public\RPi4-NAS\images\hwmonitor.jpg" alt="hwmonitor" style="zoom: 25%;" />