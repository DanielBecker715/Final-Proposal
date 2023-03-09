#!/usr/bin/env python3
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
reader = SimpleMFRC522()
try:
        id = input('Enter tag data:')
        print("Hold tag to module")
        reader.write(id)
        print("Done...")
finally:
        GPIO.cleanup()
