import RPi.GPIO as GPIO  
from time import sleep  
GPIO.setmode(GPIO.BCM)  
  
leds = [2,3,4,17,27,22,10,9,11,5,6,13,19,26,14,15,18,23,24,25,8,7,12,16,20,21]  
leds1 = [2,3,4,17,27,22,10,9]  
leds2 = [11,5,6,13,19,26,14,15]  
leds3 = [18,23,24,25,8,7,12,16]  
leds4 = [20,21,24,25,8,7,12,16] # had to cheat a bit here as only 2 leds on board 4  
leds_back = leds[:]             # make copy of leds list so we can reverse it  
leds_back.reverse()             # reverse it  
  
for i in leds:                         # loop through leds flashing each for 0.1s  
    GPIO.setup(i, GPIO.OUT, initial=0) # sets i to output and 0V, off   
    GPIO.output(i, 1)    # sets port on  
    sleep(0.1)  
    GPIO.output(i, 0)    # sets port off  
  
for i in leds_back:      # loop through them all in reverse  
    GPIO.output(i, 1)    # sets port on  
    sleep(0.1)  
    GPIO.output(i, 0)    # sets port off  
  
try:  
    x = 0  
    while x < 100:  
        x += 1  
        # now we take each group of 8 and switch them all at the same time  
        # forwards  
        for i in range(8):  
            GPIO.output(leds1[i], 1) # sets port on  
            GPIO.output(leds2[i], 1) # sets port on  
            GPIO.output(leds3[i], 1) # sets port on  
            GPIO.output(leds4[i], 1) # sets port on  
            sleep(0.1/x)  
            GPIO.output(leds1[i], 0) # sets port off  
            GPIO.output(leds2[i], 0) # sets port off  
            GPIO.output(leds3[i], 0) # sets port off  
            GPIO.output(leds4[i], 0) # sets port off  
        # then backwards  
        for i in range(7,-1,-1):  
            GPIO.output(leds1[i], 1) # sets port on  
            GPIO.output(leds2[i], 1) # sets port on  
            GPIO.output(leds3[i], 1) # sets port on  
            GPIO.output(leds4[i], 1) # sets port on  
            sleep(0.1/x)  
            GPIO.output(leds1[i], 0) # sets port off  
            GPIO.output(leds2[i], 0) # sets port off  
            GPIO.output(leds3[i], 0) # sets port off  
            GPIO.output(leds4[i], 0) # sets port off  
finally:  
    GPIO.cleanup() # clean up the ports on exit, no matter why it exits  
