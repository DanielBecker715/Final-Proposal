#!/usr/bin/env python3
import sys
import time
import sqlite3
import configparser
from rich import *

#Config
config = configparser.ConfigParser()
config.read("/scripts/config.ini")

#Setup arduino card
from mfrc522 import SimpleMFRC522
reader = SimpleMFRC522()
triggerPIN = 4

#Setup arduino buzzer
import RPi.GPIO as GPIO
GPIO.cleanup() # cleanup all GPIO 
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(triggerPIN,GPIO.OUT)



def PlayAccessGranted():
    buzzer = GPIO.PWM(triggerPIN, 6000) # Set sound frequency to 2 Khz
    buzzer.start(10) # Set dutycycle to 10
    time.sleep(.2)

def PlayAccessDenied():
    buzzer = GPIO.PWM(triggerPIN, 6000) # Set sound frequency to 2 Khz
    buzzer.start(10) # Set dutycycle to 10
    time.sleep(.2)
    buzzer.ChangeFrequency(400)
    time.sleep(.2)

def getCardPermission(conn, cardid):
    cur = conn.cursor()
    
    cur.execute(""" SELECT cardid FROM allowed_cards WHERE `cardid` = ? """, (cardid,))
    rows = cur.fetchall()

    cur.execute('''INSERT INTO card_logs (cardid) VALUES(?)''', (cardid,))

    if not rows:
        print ("NO USER FOUND")
        PlayAccessDenied()
        return False
    else:
        print ("USER FOUND")
        for row in rows:
            print("User:")
            print(row)
        PlayAccessGranted()
        return True

conn = sqlite3.connect(config['projectinfo']['databasePath']+config['projectinfo']['databaseFileName'])
print ("Searching for signal")

while 1:
    id, text = reader.read()
    print("ID: ", id)
    
    with conn:
        print("Searching for userdata in database:")
        getCardPermission(conn, id)
    time.sleep(1.5)