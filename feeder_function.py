import RPi.GPIO as GPIO
from time import sleep

# GPIO Pins
FRONT = 18
BACK= 19

# GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(BACK, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(FRONT, GPIO.OUT)


def feed():
	GPIO.setup(FRONT, GPIO.OUT)
	GPIO.setup(BACK, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	GPIO.output(FRONT, GPIO.HIGH)
	print("forward")
	sleep(3)
	GPIO.output(FRONT, GPIO.LOW)
	sleep(0.5)
	GPIO.setup(BACK, GPIO.OUT)
	GPIO.setup(FRONT, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	GPIO.output(BACK, GPIO.HIGH)
	print("back")
	sleep(3)
	GPIO.output(BACK, GPIO.LOW)
	

feed()
