#Written by Kenneth on 14August2019
#Leader Raspberry Pi as AP
#Volume setting:- amixer cset numid=1 100%
#TX power:- iw dev wlan0 set txpower limit 1000

import subprocess
import time
from time import gmtime, strftime
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17,GPIO.OUT)
GPIO.setup(27,GPIO.OUT)

GPIO.setup(18,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.output(17, GPIO.LOW)
GPIO.output(27, GPIO.LOW)


#in range
#dbmref = 100
pingref = 10.00
#trigger out of range
#dbmref = 10

vol = 'amixer cset numid=1 100%'
txpower = 'iw dev wlan0 set txpower limit 1000'
#cmd0= 'ping -c3 -s1000 10.1.1.2 | grep rtt | cut -f5 -d"/"'
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

def enroll():
    alive=[]
    for ip in range(2,5):
      ipaddress='10.1.1.' + str(ip)
      cmd= 'ping -c3 -s1000 ' + str(ipaddress)+' | grep rtt | cut -f5 -d"/"'
      ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
      output = ps.communicate()[0]
      if output != '':
#      if output == '':
        alive.append(ipaddress)
        print (alive)
    return alive

def ascheck():
    cmd= 'iw wlan0 station dump'
    output=ps(cmd)
    if output!='':

#    if output=='':
#      print(output)

#     Wifi associated LED
      GPIO.output(27, GPIO.HIGH)
      print('WIFI Associated')
    else:
      print('No WIFI Association')
      GPIO.output(27, GPIO.LOW)

ps(txpower)
ps(vol)
alive=[]
while True:
    ascheck()
    if GPIO.input(18)== True:
      alive=enroll()
      print (alive)

    print(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
    for i in alive:
      cmd0= 'ping -c10 -s1400 ' + i + ' | grep rtt | cut -f5 -d"/"'
      print(cmd0)
      output = ps(cmd0)
      if output == '':
         output=1000
#      print(output)
      if float(output) > pingref:
         GPIO.output(17, GPIO.HIGH)
         print("Kayaker Out of Range")
         alert()
      else:
         GPIO.output(17, GPIO.LOW)

         print("Kayakers Are IN Range")
    time.sleep(3)
