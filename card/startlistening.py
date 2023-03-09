#!/usr/bin/env python3
import sys
import time
import sqlite3
from database import *

#Import functions to enable and disable the ports of the switch
import sys
sys.path.insert(0, '..')
#from switch import activateallports

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


def create_connection(db_file):
    conn = None

    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def select_specific_card(conn, cardid):
    """
    Query tasks by priority
    :param conn: the Connection object
    :param priority:
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT cardid FROM allowed_users WHERE cardid = %s" %  (cardid))

    rows = cur.fetchall()

    if not rows:
        print ("NO USER FOUND")
        PlayAccessDenied()
    else:
        print ("USER FOUND")
        for row in rows:
            print("User:")
            print(row)
        PlayAccessGranted()

#def activatePorts():
#    

#def main():
#    database = "/scripts/allowed_users.db"

    # create a database connection
#    conn = sqlite3.connect(database)
#    with conn:
#        print("Gettitng user from database:")
#        select_specific_card(conn, "12345")


print ("Searching for signal")
while 1:
    id, text = reader.read()
    print("ID: ", id)
    database = "/scripts/database/allowed_users.db"
    # create a database connection
    conn = sqlite3.connect(database)
    with conn:
        print("Searching for userdata in database:")
        select_specific_card(conn, id)
    time.sleep(1.5)
#    GPIO.cleanup()
