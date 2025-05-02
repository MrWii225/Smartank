import RPi.GPIO as GPIO
from time import sleep

# GPIO Pins
FRONT = 18
BACK= 19

# GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(BACK, GPIO.OUT)
GPIO.setup(FRONT, GPIO.OUT)


def feed():
	GPIO.output(FRONT, GPIO.HIGH)
	sleep(3)
	GPIO.output(FRONT, GPIO.LOW)
	sleep(0.25)
	GPIO.output(BACK, GPIO.HIGH)
	print("back")
	sleep(3)
	GPIO.output(BACK, GPIO.LOW)
	

#feed()
