from sys import argv
import cv2
import RPi.GPIO as GPIO

import time
import os
import spidev
import httplib, urllib

spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz=5000

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

buzzer = 25
RL = 22
GPIO.setup(RL, GPIO.OUT)
GPIO.setup(buzzer, GPIO.OUT)
GPIO.output(buzzer, False)
GPIO.output(RL, True)
time.sleep(1)

a=1
from twilio.rest import Client

# Find these values at https://twilio.com/user/account
account_sid = "AC9d3ac9f004f0b7b152afddd303d60fca"
auth_token = "23fb2c9b3e00eeeca377c469aaa33441"

client = Client(account_sid, auth_token)

# ----------------------------------------------------------------------
sleep = 2 
key ='MHSY765G31HTJGP8'  # Thingspeak channel to update 3HEXXTITMR9I5I9   JRAI9MM3TER6F8P
# ----------------------------------------------------------------------
def send_IoTData(field1,field2):   
    try:
        params = urllib.urlencode({'field1': field1, 'field2': field2,'key':key })
        headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
        conn = httplib.HTTPConnection("api.thingspeak.com:80")

        conn.request("POST", "/update", params, headers)
        response = conn.getresponse()
        print (response.status, response.reason)
        data = response.read()
        conn.close()
    except:
        return
    
def send_IoTDataField1(field1):
    try:
        params = urllib.urlencode({'field1': field1, 'key':key })
        headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
        conn = httplib.HTTPConnection("api.thingspeak.com:80")

        conn.request("POST", "/update", params, headers)
        response = conn.getresponse()
        print(response.status, response.reason)
        data = response.read()
        conn.close()
    except:
        return

def send_IoTDataField2(field2):
    try:
        params = urllib.urlencode({'field2': field2, 'key':key })
        headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
        conn = httplib.HTTPConnection("api.thingspeak.com:80")

        conn.request("POST", "/update", params, headers)
        response = conn.getresponse()
        print (response.status, response.reason)
        data = response.read()
        conn.close()
    except:
        return


def ReadChannel(channel):
  adc = spi.xfer2([1,(8+channel)<<4,0])
  data = ((adc[1]&3) << 8) + adc[2]
  return data
 
# Function to convert data to voltage level,
# rounded to specified number of decimal places.
def ConvertVolts(data,places):
  volts = (data * 3.3) / float(1023)
  volts = round(volts,places)
  return volts
 
# Function to calculate temperature from
# TMP36 data, rounded to specified
# number of decimal places.
def ConvertTemp(data,places):
 
  # ADC Value
  # (approx)  Temp  Volts
  #    0      -50    0.00
  #   78      -25    0.25
  #  155        0    0.50
  #  233       25    0.75
  #  310       50    1.00
  #  465      100    1.50
  #  775      200    2.50
  # 1023      280    3.30
 
  temp = ((data * 330)/float(1023))#-50 40
  temp = round(temp,places)
  return temp




def readChannel(channel):
  adc = spi.xfer2([1,(8+channel)<<4,0])
  data = ((adc[1]&3) << 8) + adc[2]
  return data


def readTempSensor():
    temp = readChannel(0)
    return temp


###lcd #####################

LCD_RS = 7
LCD_E  = 21
LCD_D4 = 26
LCD_D5 = 6
LCD_D6 = 13
LCD_D7 = 19

LED = 4

IN1=23
IN2=24
# Define some device constants
LCD_WIDTH = 20    # Maximum characters per line
LCD_CHR = True
LCD_CMD = False

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
LCD_LINE_3 = 0x90 # LCD RAM address for the 2nd line
LCD_LINE_4 = 0xD0 # LCD RAM address for the 2nd line

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

####lcd end here###########


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

#GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)#Button to GPIO12
      # Use BCM GPIO numbers
GPIO.setup(LCD_E, GPIO.OUT)  # E
GPIO.setup(LCD_RS, GPIO.OUT) # RS
GPIO.setup(LCD_D4, GPIO.OUT) # DB4
GPIO.setup(LCD_D5, GPIO.OUT) # DB5
GPIO.setup(LCD_D6, GPIO.OUT) # DB6
GPIO.setup(LCD_D7, GPIO.OUT) # DB7

GPIO.setup(LED, GPIO.OUT)  # LED

GPIO.setup(IN1, GPIO.OUT)  # MOTAR IN1
GPIO.setup(IN2, GPIO.OUT)  # MOTAR IN2

####################LCD#######################
def lcd_init():
  # Initialise display
  lcd_byte(0x33,LCD_CMD) # 110011 Initialise
  lcd_byte(0x32,LCD_CMD) # 110010 Initialise
  lcd_byte(0x06,LCD_CMD) # 000110 Cursor move direction
  lcd_byte(0x0C,LCD_CMD) # 001100 Display On,Cursor Off, Blink Off
  lcd_byte(0x28,LCD_CMD) # 101000 Data length, number of lines, font size
  lcd_byte(0x01,LCD_CMD) # 000001 Clear display
  time.sleep(E_DELAY)

def lcd_byte(bits, mode):
  # Send byte to data pins
  # bits = data
  # mode = True  for character
  #        False for command

  GPIO.output(LCD_RS, mode) # RS

  # High bits
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x10==0x10:
    GPIO.output(LCD_D4, True)
  if bits&0x20==0x20:
    GPIO.output(LCD_D5, True)
  if bits&0x40==0x40:
    GPIO.output(LCD_D6, True)
  if bits&0x80==0x80:
    GPIO.output(LCD_D7, True)

  # Toggle 'Enable' pin
  lcd_toggle_enable()

  # Low bits
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x01==0x01:
    GPIO.output(LCD_D4, True)
  if bits&0x02==0x02:
    GPIO.output(LCD_D5, True)
  if bits&0x04==0x04:
    GPIO.output(LCD_D6, True)
  if bits&0x08==0x08:
    GPIO.output(LCD_D7, True)

  # Toggle 'Enable' pin
  lcd_toggle_enable()

def lcd_toggle_enable():
  # Toggle enable
  time.sleep(E_DELAY)
  GPIO.output(LCD_E, True)
  time.sleep(E_PULSE)
  GPIO.output(LCD_E, False)
  time.sleep(E_DELAY)

def lcd_string(message,line):
  # Send string to display
  message = message.ljust(LCD_WIDTH," ")

  lcd_byte(line, LCD_CMD)

  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR)

#####################LCD HERE######################


##extract results
  
lcd_init()

def Gas_Reading():
    
    Gas_level = ReadChannel(0)
    Gas = ConvertVolts(Gas_level,2)
    send_IoTDataField2(Gas)
    global a
    print ("--------------------------------------------")
    print("Gas:{} PPM".format(Gas_level))
    lcd_byte(0x01, LCD_CMD)
    lcd_string('Gas:{} PPM'.format(Gas_level),LCD_LINE_1)
    time.sleep(1.0)
    
    if Gas_level > 400 and a==1:
      a=0
      GPIO.output(LED, False)
      print("Lights off")
      lcd_byte(0x01, LCD_CMD)
      lcd_string("Lights off",LCD_LINE_1)
      time.sleep(1.0)
      GPIO.output(IN1, False)
      GPIO.output(IN2, True)
      time.sleep(2)
      GPIO.output(IN1, False)
      GPIO.output(IN2, False)
      time.sleep(2)
      print("fan on")
      lcd_byte(0x01, LCD_CMD)
      lcd_string("Window Opened",LCD_LINE_1)
      GPIO.output(buzzer, True)
      time.sleep(1)
      GPIO.output(buzzer, False)
      time.sleep(1)
      
      client.api.account.messages.create(
        to="+91-8073854982",
        from_="+18704575039",
        body="Gas Detected")
    elif Gas_level < 400 and a==0:
      a=1
      GPIO.output(LED, True)
      print("Lights on")
      lcd_byte(0x01, LCD_CMD)
      lcd_string("Lights On",LCD_LINE_1)
      lcd_string("Window closed",LCD_LINE_2)
      time.sleep(1.0)


def Temp_Reading():
    global a
    Temp_level = ReadChannel(1)
    Temp = ConvertTemp(Temp_level,2)
    Temp = Temp+20

    send_IoTDataField1(Temp)
    
    print ("--------------------------------------------")
    print("Temp:{} Cel".format(Temp))
    lcd_byte(0x01, LCD_CMD)
    lcd_string('Temp:{} PPM'.format(Temp),LCD_LINE_1)
    time.sleep(1.0)
    if Temp > 40:
      GPIO.output(RL, False)
      time.sleep(1.0)
      print("stove lock")
      lcd_byte(0x01, LCD_CMD)
      lcd_string("stove lock",LCD_LINE_1)
      time.sleep(1.0)
  
lcd_byte(0x01, LCD_CMD)
lcd_string("  Smart Gas   ",LCD_LINE_1)
lcd_string("  System    ",LCD_LINE_2)

while True:
  Gas_Reading()
  Temp_Reading()






  
