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
GPIO.setup(18,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.output(17, GPIO.LOW)


#in range
#dbmref = 100
pingref = 100.00
#trigger out of range
#dbmref = 10

vol = 'amixer cset numid=1 50%'
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
    for ip in range(1,5):
      print('10.1.1.' + str(ip))
      ipaddress='10.1.1.' + str(ip)
      cmd= 'ping -c3 -s1000 ' + str(ipaddress)+' | grep rtt | cut -f5 -d"/"'
      ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
      output = ps.communicate()[0]
      if output != '':
#      if output == '':
        alive.append(ipaddress)
        print (alive)
    return alive


ps(vol)
#enroll()

alive=enroll()
print (alive)
while True:
    print(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
    for i in alive:
#       print (i)
      cmd0= 'ping -c3 -s1000 ' + i + ' | grep rtt | cut -f5 -d"/"'
      print(cmd0)
      output = ps(cmd0)
      if output == '':
         output=1000
         print(output)
      if float(output) > pingref:
         GPIO.output(17, GPIO.HIGH)
         print("Kayaker Out of Range")
         alert()
      else:
         GPIO.output(17, GPIO.LOW)
         print("Kayakers Are IN Range")
    time.sleep(3)
