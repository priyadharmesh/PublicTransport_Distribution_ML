import urllib.request
import requests
import threading
import json

import random

def thingspeak_post():
##    threading.Timer(15,thingspeak_post).start()
    val1=random.randint(60,560)
    val2=random.randint(46,50)
    val3=random.randint(50,55)
    val4=random.randint(37,50)
    val5=random.randint(20,180)
    val6=random.randint(40,45)
    val7=random.randint(46,50)
    URl='https://api.thingspeak.com/update?api_key=4YSF6M6ZCRGYIE02&field1=10&field2=20&field3=30&field4=40&field5=50&field6=60&field7=70'
    KEY='4YSF6M6ZCRGYIE02'
    HEADER='&field1={}&field2={}&field3={}&field4={}&field5={}&field6={}&field7={}'.format(val1,val2,val3,val4,val5,val6,val7)
    NEW_URL = URl+KEY+HEADER
    print(NEW_URL)
    data=urllib.request.urlopen(NEW_URL)
    print(data)
    
if __name__ == '__main__':
    thingspeak_post()
