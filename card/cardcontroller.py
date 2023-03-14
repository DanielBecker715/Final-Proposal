#!/usr/bin/env python3
import sys, os
import time
import sqlite3
import configparser

#Config
config = configparser.ConfigParser()
config.read("/scripts/config.ini")

import switch.cisco_communication as switch

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

        
conn = sqlite3.connect(config['projectinfo']['databasePath']+config['projectinfo']['databaseFileName'])
print ("Searching for signal")

def getCardPermission(cardid):
    cur = conn.cursor()
    
    cur.execute(""" SELECT cardid, firstname FROM users WHERE `cardid` = ? """, (cardid,))
    rows = cur.fetchall()

    cur.execute('''INSERT INTO card_logs (cardid,time) VALUES(?,?)''', (cardid,"d"))

    if not rows:
        print ("Card denied!")
        PlayAccessDenied()
        return False
    else:
        print ("Access granted, "+rows[0][1])
        PlayAccessGranted()
        return True


def startListening():
    while 1:
        id, text = reader.read()
        print("----------------")
        print(f"Read card with ID: {id}")
        
        with conn:
            print("Searching for userdata in database:")
            if (getCardPermission(id)):
                switch.enableAllPorts()
        time.sleep(1.5)
