import RPi.GPIO as GPIO
import serial
GPIO.setmode(GPIO.BOARD)  
  
# GPIO 23 set up as input. It is pulled up to stop false signals  
 
  
print "Make sure you have a button connected so that when pressed"  
print "it will connect GPIO port 23 (pin 16) to GND (pin 6)\n"  
raw_input("Press Enter when ready\n>")  
serPhone = serial.Serial("/dev/rfcomm0", 9600, timeout = 0) #initialize bluetooth
print "Waiting for falling edge on port 23"  
# now the program will do nothing until the signal on port 23   
# starts to fall towards zero. This is why we used the pullup  
# to keep the signal high and prevent a false interrupt  
  
print "During this waiting time, your computer is not"   
print "wasting resources by polling for a button press.\n"  
print "Press your button when ready to initiate a falling edge interrupt."  
try:  
    serPhone.read(2)
    print "\nFalling edge detected. Now your program can continue with"  
    print "whatever was waiting for a button press."  
except KeyboardInterrupt:  
    GPIO.cleanup()       # clean up GPIO on CTRL+C exit  
GPIO.cleanup()           # clean up GPIO on normal exit  

        