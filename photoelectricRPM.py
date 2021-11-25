import machine
import utime
import time
import threading

count = 0
num_of_holes = 200
rpm=0

def counter(pin):
    global count
    count=count+1

def icall():
    global rpm
    rpm=(count*120)/num_of_holes

p28 = machine.Pin(28, machine.Pin.IN, machine.Pin.PULL_UP)
p28.irq(trigger=machine.Pin.IRQ_RISING, handler=counter)

def loop():
    t_end = time.time() + 1    #edit +number where number is the rpm update frequency
    while time.time() < t_end:
        icall()
    
while True:     #add vehicle on off condition instead of infinite loop???
    loop()
    print("Speed: ",rpm, "RPM")
    count=0
    rpm=0
