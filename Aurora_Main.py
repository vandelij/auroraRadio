import RPi.GPIO as GPIO
import time

led_on = False
count = 0

def setupGPIO():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(18, GPIO.OUT, initial=GPIO.LOW)
    #GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def flashLED(count):
    for i in range(count):
        GPIO.output(18, GPIO.HIGH)
        time.sleep(.2)
        GPIO.output(18, GPIO.LOW)
        time.sleep(.2)

print('Test of flashing LED')
count = int(input('Enter the number of LEd flashes: '))
setupGPIO()
flashLED(count)
print('Program exiting')