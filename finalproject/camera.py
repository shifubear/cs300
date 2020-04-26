from picamera import PiCamera
from time import sleep

camera = PiCamera()

sleep(2)
camera.capture("image.jpg")