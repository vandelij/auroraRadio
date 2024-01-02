##########################



import RPi.GPIO as GPIO
import time
import os
import signal
import subprocess

led_on = False
count = 0

def setupGPIO():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(18, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def flashLED(count):
    for i in range(count):
        print('Flash!')
        GPIO.output(18, GPIO.HIGH)
        time.sleep(.2)
        GPIO.output(18, GPIO.LOW)
        time.sleep(.2)

# print('Test of flashing LED')
# count = int(input('Enter the number of LEd flashes: '))
# setupGPIO()
# flashLED(count)
def switch(ev=None):
    global led_on, count, gnu_radio_script
    led_on = not led_on
    count += 1

    if led_on == True:
        print("Turning on\tcount: " + str(count))
        GPIO.output(18, GPIO.HIGH)
        #start recording the radio
        print('Start radio recording') 
        gnu_radio_script = subprocess.Popen("~/Desktop/Aurora_Radio/gnu_script_to_run/rtl_sdr_test.py", shell=True, preexec_fn=os.setsid)
    else:
        print("Turning off\tcount: " + str(count))
        GPIO.output(18, GPIO.LOW)
        print('Killing Radio Recording')
        os.killpg(os.getpgid(gnu_radio_script.pid), signal.SIGTERM)


def detectButtonPress():
    GPIO.add_event_detect(25, GPIO.FALLING, callback=switch, bouncetime=300)


def waitForEvents():
    while True:
        time.sleep(1)

def main():
    print("# # # LED Program # # #")
    print("LED:\tpin 18")
    print("Button:\tpin 25")

    print('Test of flashing LED')
    count = int(input('Enter the number of LEd flashes: '))
    setupGPIO()
    flashLED(count)

    detectButtonPress()
    print('Now waiting for the user to push the button (short with the grey-brown wire to ground)')
    waitForEvents()
    print('Program exiting')

if __name__ == "__main__":
    try:
        main()

    #turn off the LED when the program ends
    except KeyboardInterrupt:
        print("Killing LEDs")
        GPIO.output(18, GPIO.LOW)
        