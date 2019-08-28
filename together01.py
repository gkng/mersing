#Written by Kenneth on 14August2019
#Leader Raspberry Pi as AP
#Volume setting:- amixer cset numid=1 100%

import subprocess
import time
from time import gmtime, strftime
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17,GPIO.OUT)
GPIO.output(17, GPIO.LOW)


#in range
#dbmref = 100
pingref = 100.00
#trigger out of range
#dbmref = 10

vol = 'amixer cset numid=1 10%'
cmd0= 'ping -c3 -s1000 10.1.1.2 | grep rtt | cut -f5 -d"/"'
#cmd1= 'ping -c3 10.1.1.2 | grep received | cut -f4 -d" "'


#Non-lead commands
#cmd0 = 'ping -c3 10.1.1.2 | grep packets | cut -f4 -d","'
#cmd1 = 'iwconfig wlan0 | grep Link | cut -f3 -d"="'

def ps(cmd):
    ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    output = ps.communicate()[0]
    return output

def alert():
    subprocess.call(['aplay','AirHorn.wav'])


ps(vol)

while True:
    print(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
    output = ps(cmd0)
    if output == '':
       output=1000
       print(output)


#    ps0output=int(output[5:-3])
#    print (ps0output)

#    output = ps(cmd1)
#    ps1output=abs(int(output[0:4]))
#    print (output)
#    print (ps1output)

    if float(output) > pingref:
       GPIO.output(17, GPIO.HIGH)
       print("Kayaker Out of Range")
#       alert()
    else:
       GPIO.output(17, GPIO.LOW)
       print("Kayakers Are IN Range")
    time.sleep(3)
