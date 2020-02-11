#!/usr/bin/python
import time, serial
import RPi.GPIO as GPIO


LCD_RS = 7
LCD_E  = 11
LCD_DATA4 = 36
LCD_DATA5 = 22
LCD_DATA6 = 23
LCD_DATA7 = 26
GPIO_TRIGGER = 18
GPIO_ECHO = 24



LCD_WIDTH = 16      
LCD_LINE_1 = 0x80   
LCD_LINE_2 = 0xC0   
LCD_CHR = GPIO.HIGH
LCD_CMD = GPIO.LOW
E_PULSE = 0.0005
E_DELAY = 0.0005

def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance

def lcd_send_byte(bits, mode):
    GPIO.output(LCD_RS, mode)
    GPIO.output(LCD_DATA4, GPIO.LOW)
    GPIO.output(LCD_DATA5, GPIO.LOW)
    GPIO.output(LCD_DATA6, GPIO.LOW)
    GPIO.output(LCD_DATA7, GPIO.LOW)
    if bits & 0x10 == 0x10:
      GPIO.output(LCD_DATA4, GPIO.HIGH)
    if bits & 0x20 == 0x20:
      GPIO.output(LCD_DATA5, GPIO.HIGH)
    if bits & 0x40 == 0x40:
      GPIO.output(LCD_DATA6, GPIO.HIGH)
    if bits & 0x80 == 0x80:
      GPIO.output(LCD_DATA7, GPIO.HIGH)
    time.sleep(E_DELAY)    
    GPIO.output(LCD_E, GPIO.HIGH)  
    time.sleep(E_PULSE)
    GPIO.output(LCD_E, GPIO.LOW)  
    time.sleep(E_DELAY)      
    GPIO.output(LCD_DATA4, GPIO.LOW)
    GPIO.output(LCD_DATA5, GPIO.LOW)
    GPIO.output(LCD_DATA6, GPIO.LOW)
    GPIO.output(LCD_DATA7, GPIO.LOW)
    if bits&0x01==0x01:
      GPIO.output(LCD_DATA4, GPIO.HIGH)
    if bits&0x02==0x02:
      GPIO.output(LCD_DATA5, GPIO.HIGH)
    if bits&0x04==0x04:
      GPIO.output(LCD_DATA6, GPIO.HIGH)
    if bits&0x08==0x08:
      GPIO.output(LCD_DATA7, GPIO.HIGH)
    time.sleep(E_DELAY)    
    GPIO.output(LCD_E, GPIO.HIGH)  
    time.sleep(E_PULSE)
    GPIO.output(LCD_E, GPIO.LOW)  
    time.sleep(E_DELAY)  

def display_init():
    lcd_send_byte(0x33, LCD_CMD)
    lcd_send_byte(0x32, LCD_CMD)
    lcd_send_byte(0x28, LCD_CMD)
    lcd_send_byte(0x0C, LCD_CMD)  
    lcd_send_byte(0x06, LCD_CMD)
    lcd_send_byte(0x01, LCD_CMD)  

def lcd_message(message):
    message = message.ljust(LCD_WIDTH," ")  
    for i in range(LCD_WIDTH):
      lcd_send_byte(ord(message[i]),LCD_CHR)
    
if __name__ == '__main__':
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    GPIO.setup(LCD_E, GPIO.OUT)
    GPIO.setup(LCD_RS, GPIO.OUT)
    GPIO.setup(LCD_DATA4, GPIO.OUT)
    GPIO.setup(LCD_DATA5, GPIO.OUT)
    GPIO.setup(LCD_DATA6, GPIO.OUT)
    GPIO.setup(LCD_DATA7, GPIO.OUT)
    GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
    GPIO.setup(GPIO_ECHO, GPIO.IN)
    GPIO.setup(12, GPIO.OUT) #pin for motor 1
    GPIO.setup(15, GPIO.OUT) #pin for direction 1
    GPIO.setup(32, GPIO.OUT) #pin for motor 2
    GPIO.setup(16, GPIO.OUT) #pin for direction 2

    

    pwmOne = GPIO.PWM(12, 1000)
    pwmTwo = GPIO.PWM(32, 1000)
    
    pwmOne.start(0)
    pwmTwo.start(0)

    serPhone = serial.Serial("/dev/rfcomm0", 9600, timeout = 0) #initialize bluetooth
    serPhone.baudrate = 9600
    pwmPower = 100
    updateLCD = False
    
    while True:
        data = serPhone.read(2)
        data = data.decode("utf-8")
        data = data.lstrip(' ')
        print("Data: ", data)
        
        if("OH" in data):
            pwmPower = 100
        if("NP" in data):
            pwmPower = 90
        if("EP" in data):
            pwmPower = 80
            
            
        #move forward
        if("TF" in data):
            GPIO.output(15, 1)
            GPIO.output(16, 0)
            while("TS" not in data):
                data = serPhone.read(2).decode("utf-8").lstrip(" ");
                time.sleep(1/32)
                pwmOne.ChangeDutyCycle(pwmPower)
                pwmTwo.ChangeDutyCycle(pwmPower)
                updateLCD = True
                print("Data: ", data)
            
        #move backward
        if("TB" in data):
            GPIO.output(15, 0)
            GPIO.output(16, 1)
            while("TS" not in data):
                data = serPhone.read(2).decode("utf-8").lstrip(" ");
                time.sleep(1/32)
                pwmOne.ChangeDutyCycle(pwmPower)
                pwmTwo.ChangeDutyCycle(pwmPower)
                updateLCD = True
                print("Data: ", data)   
    
        #turn left
        if("TL" in data):
            GPIO.output(15, 0)
            GPIO.output(16, 0)
            while("TS" not in data):
                data = serPhone.read(2).decode("utf-8").lstrip(" ");
                time.sleep(1/32)
                pwmOne.ChangeDutyCycle(pwmPower)
                pwmTwo.ChangeDutyCycle(pwmPower)
                updateLCD = True
                print("Data: ", data)
            
            
        #turn right
        if("TR" in data):
            GPIO.output(15, 1)
            GPIO.output(16, 1)
            while("TS" not in data):
                data = serPhone.read(2).decode("utf-8").lstrip(" ");
                time.sleep(1/32)
                pwmOne.ChangeDutyCycle(pwmPower)
                pwmTwo.ChangeDutyCycle(pwmPower)
                updateLCD = True
                print("Data: ", data)
                
                
        pwmOne.ChangeDutyCycle(0)
        pwmTwo.ChangeDutyCycle(0)
        if(updateLCD):
            display_init()
            dist = "%5.2f" % distance()
            msg = "Distance: "
            for i in range(len(msg)):
                lcd_send_byte(LCD_LINE_1, LCD_CMD)
                lcd_message(msg)
                lcd_send_byte(LCD_LINE_2, LCD_CMD)
                lcd_message(dist)
                updateLCD = False
                time.sleep(0.0005)
                
    
    GPIO.cleanup()