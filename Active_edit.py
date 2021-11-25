import time
import serial
import gpiozero
import board
import neopixel

Battery_pin = gpiozero.LED(23)
FP_cap = gpiozero.Button(24)
lock = gpiozero.LED(25)
Enroll_pin = gpiozero.Button(27, pull_up=False)
Sidestand = gpiozero.Button(22)                                                 #perimary Condition
Batterybutton = gpiozero.Button(10)
Vehicle_Moving = gpiozero.Button(23)                                            #Primary Condition


pixel_pin = board.D18
num_pixels = 5
ORDER = neopixel.GRBW
pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=1, auto_write=False, pixel_order=ORDER
)


import adafruit_fingerprint
# If using with Linux/Raspberry Pi and hardware UART:
uart = serial.Serial("/dev/ttyS0", baudrate=57600, timeout=1)

# If using with Linux/Raspberry Pi 3 with pi3-disable-bt
# uart = serial.Serial("/dev/ttyAMA0", baudrate=57600, timeout=1)

finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)

##################################################


def get_fingerprint():
    """Get a finger print image, template it, and see if it matches!"""          #waits for the image and scans it in the data base for a match
    print("Waiting for image...")
    while finger.get_image() != adafruit_fingerprint.OK:
        pass
    print("Templating...")
    if finger.image_2_tz(1) != adafruit_fingerprint.OK:
        return False
    print("Searching...")
    if finger.finger_search() != adafruit_fingerprint.OK:
        return False
    return True




# pylint: disable=too-many-statements
def enroll_finger(location):                                                     #waits for the Image to create the Model , and veryfies it by asking it for the 2nd time.{It saves the tempelet number by appending the previous number}
    """Take a 2 finger images and template it, then store in 'location'"""
    for fingerimg in range(1, 3):
        if fingerimg == 1:
            print("Place finger on sensor...", end="", flush=True)
        else:
            print("Place same finger again...", end="", flush=True)

        while True:
            i = finger.get_image()
            if i == adafruit_fingerprint.OK:
                print("Image taken")
                break
            if i == adafruit_fingerprint.NOFINGER:
                print(".", end="", flush=True)
            elif i == adafruit_fingerprint.IMAGEFAIL:
                print("Imaging error")
                return False
            else:
                print("Other error")
                return False

        print("Templating...", end="", flush=True)
        i = finger.image_2_tz(fingerimg)
        if i == adafruit_fingerprint.OK:
            print("Templated")
        else:
            if i == adafruit_fingerprint.IMAGEMESS:
                print("Image too messy")
            elif i == adafruit_fingerprint.FEATUREFAIL:
                print("Could not identify features")
            elif i == adafruit_fingerprint.INVALIDIMAGE:
                print("Image invalid")
            else:
                print("Other error")
            return False

        if fingerimg == 1:
            print("Remove finger")
            time.sleep(1)
            while i != adafruit_fingerprint.NOFINGER:
                i = finger.get_image()

    print("Creating model...", end="", flush=True)
    i = finger.create_model()
    if i == adafruit_fingerprint.OK:
        print("Created")
    else:
        if i == adafruit_fingerprint.ENROLLMISMATCH:
            print("Prints did not match")
        else:
            print("Other error")
        return False

    print("Storing model #%d..." % location, end="", flush=True)
    i = finger.store_model(location)
    if i == adafruit_fingerprint.OK:
        print("Stored")
    else:
        if i == adafruit_fingerprint.BADLOCATION:
            print("Bad storage location")
        elif i == adafruit_fingerprint.FLASHERR:
            print("Flash storage error")
        else:
            print("Other error")
        return False

    return True

def Solenoid():
    while Vehicle_Moving == 0                                                                             #Battery bay solenoid
        match = get_fingerprint()
        if match == True:
            Battery_pin.on()
            print("Solenoid is open")
            pixels.fill((255, 0, 0, 0))
            pixels.show()
            time.sleep(5)
            Battery_pin.off()
            print("solenoid Closed")
            pixels.fill((0, 0, 255, 0))
            pixels.show()
        else:
            print("NO match Found")
            pixels.fill((0, 255, 0, 0))
            pixels.show()
            time.sleep(0.5)
            pixels.fill((0, 0, 0, 0))
            pixels.show()
            time.sleep(0.5)
            pixels.fill((0, 255, 0, 0))
            pixels.show()
            Battery_pin.off()
            pixels.fill(0)
def Locking():                                                                   #relay for shorting the motor wires
    match = get_fingerprint()
    if match == True:
        lock.toggle()
        print("lock toggled")
    else:
        lock.off()
def get_num(max_number):                                                         #asks user for a number to store the new enrolled finger to.
    """Use input() to get a valid number from 0 to the maximum size
    of the library. Retry till success!"""
    i = -1
    while (i > max_number - 1) or (i < 0):
        try:
            i = int(input("Enter ID # from 0-{}: ".format(max_number - 1)))
        except ValueError:
            pass
    return i




##################################################

# initialize LED color                                                            #Main starts
led_color = 1
led_mode = 3

    # Turn on LED
finger.set_led(color=led_color, mode=led_mode)
finger.set_led(color=3, mode=1)
Enroll_pin.when_pressed = lambda: enroll_finger(get_num(finger.library_size))
Sidestand.when_pressed = Stand


while 1:
    sidestand = gpiozero.Button(22)
    enroll_pin = gpiozero.Button(27, pull_up=False)
    battery_button = gpiozero.Button(10)
    vehicle_moving = gpiozero.Button(23)

    #side stand down (0) and vehcle  moving (1)
    if(sidestand or vehicle_moving):
        continue
    else:
        if(Batterybutton):
            #open baterry code
            #continue
        elif(enroll_pin):
            #enroll proceess
            #continue
        elif:
            #unlock process
            #continue
