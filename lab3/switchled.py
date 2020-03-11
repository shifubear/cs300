import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

# Set up pin 12 for input
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Set up pin 16 for LED output
GPIO.setup(16, GPIO.OUT)

state = 1       # Keeps track of the last state of the input
while True:
	if GPIO.input(12)==False and state==1:
		GPIO.output(16, True)
		state = 0
	if GPIO.input(12)==True and state==0:
		GPIO.output(16, False)
		state = 1




