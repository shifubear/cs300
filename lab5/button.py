import pigpio

# Constants
MOTOR = 18
BUTTON = False    #  
pi = pigpio.pi()
if not pi.connected:
    exit(0)
pi.set_servo_pulsewidth(MOTOR, 0)
try:
    while True:
        print('setting angle = -90 degrees')
        pi.set_servo_pulsewidth(MOTOR, 1000)
        time.sleep(DELAY)
        print('setting angle = 0 degrees')
        pi.set_servo_pulsewidth(MOTOR, 1500)
        time.sleep(DELAY)
        print('setting angle = 90 degrees')
        pi.set_servo_pulsewidth(MOTOR, 2000)
        time.sleep(DELAY)
    while duty_cycle >= 0 and duty_cycle <=100:
        duty_cycle = int(input('Enter a PWM duty cycle (enter -1 to end): '))
        if duty_cycle == -1:
            break
        pwm.ChangeDutyCycle(duty_cycle)

except KeyboardInterrupt:
    pi.stop()
