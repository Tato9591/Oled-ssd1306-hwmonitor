import smtplib
import time

#-----------------------------------------------------------------------------#
#Se stiamo utilizzando il servizio Gmail di Google per inviare posta.         |
#Abbiamo bisogno di alcune modifiche alle impostazioni, per consentire        |
#l'accesso, è necessario impostare "Accesso meno sicuro alle app"             |
#nell'account Google. ‎‎Se la verifica in due passaggi è in corso, non possiamo |
#utilizzare l'accesso meno sicuro.‎                                            |
#Per completare questa configurazione, vai alla console di amministrazione    |
#di Google e cerca la configurazione meno sicura dell'app.‎                    |
#-----------------------------------------------------------------------------#


FROM = "modifica@from.it"
TO = "modifica@to.com"

OGGETTO = "modifica_oggetto"
TEXT = "modifica_TEXT.\n\n"

message = f"From: {FROM}\nTo: {TO}\nSubject: {OGGETTO}\n\n{TEXT}"

def send_email():
    server = smtplib.SMTP('modifica_SMTP', modifica_PORTA)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login("modifica_user", "modifica_password")
    server.sendmail(FROM, TO, message)
    server.quit()

#per utilizzo in un altro file .py
#
#from mail import send_mail
#import time
#    
#while True:
#    send_email()
#    time.sleep(0.5)
#    break
#
