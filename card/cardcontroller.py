#!/usr/bin/env python3
import os, configparser, time, sqlite3
from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO
import switch.switchcontroller as switch

#Config
config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), '..', 'config.ini'))


#Setup arduino card
reader = SimpleMFRC522()
triggerPIN = 4

#Setup arduino buzzer
GPIO.cleanup() # cleanup all GPIO 
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(triggerPIN,GPIO.OUT)


def PlayAccessGranted():
    buzzer = GPIO.PWM(triggerPIN, 4000) # Set sound frequency to 2 Khz
    buzzer.start(10) # Set dutycycle to 10
    time.sleep(.2)
    buzzer.ChangeFrequency(6000)
    time.sleep(.2)

def PlayAccessDenied():
    buzzer = GPIO.PWM(triggerPIN, 6000) # Set sound frequency to 2 Khz
    buzzer.start(10) # Set dutycycle to 10
    time.sleep(.2)
    buzzer.ChangeFrequency(350)
    time.sleep(.2)

        

def getCardPermission(cardid):
    conn = sqlite3.connect(config['projectinfo']['databasePath']+config['projectinfo']['databaseFileName'])
    cur = conn.cursor()
    
    cur.execute(""" SELECT cardid, firstname FROM users WHERE `cardid` = ? """, (cardid,))
    rows = cur.fetchall()

    cur.execute('''INSERT INTO card_logs (cardid,time) VALUES(?,?)''', (cardid,"d"))
    conn.close()
    if not rows:
        print ("Card denied!")
        PlayAccessDenied()
        return False
    else:
        print ("Access granted, "+rows[0][1])
        PlayAccessGranted()
        return True


def listenForCard():
    print ("Searching for signal")
    id, text = reader.read()
    print("----------------")
    print(f"Read card with ID: {id}")
    
    print("Searching for userdata in database:")
    if (getCardPermission(id)):
        switch.enableAllPorts()
    time.sleep(1.5)