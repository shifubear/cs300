# Shion Fukuzawa and Lauren Ebels
# button.py
#
# Upon button input, rotates servo motor to random position. 
#

import pigpio
import random
import time

# Constants
MOTOR  = 18
BUTTON = 12
BUTTONWAIT = False    # When false, waiting for button. When true, random move 
DEBOUNCE = 1000 #debounce time, in us
pi = pigpio.pi()

def move_to_angle(degrees):
    pw = (degrees * 1000/180) + 500
    pi.set_servo_pulsewidth(MOTOR, pw)

def intCallback(g, level, tick):
    if level == 0:
        #button press
        pass
    else:
        angle = random.randint(-90, 90)
        move_to_angle(angle)


pressTick = pi.get_current_tick() #initializing var
pi.set_mode(BUTTON, pigpio.INPUT)
pi.set_glitch_filter(BUTTON, DEBOUNCE)
pi.set_pull_up_down(BUTTON, pigpio.PUD_UP) #this depends on how the switch is connected. In this case it is between GPIO and GND
cb = pi.callback(BUTTON, pigpio.EITHER_EDGE, intCallback)

try:
    while True:
        time.sleep(1)
    
except KeyboardInterrupt:
    pi.stop()
