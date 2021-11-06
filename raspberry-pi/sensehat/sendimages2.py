#!/usr/bin/env python3
import time
import datetime
import os
import random
from time import sleep

pq='9' #png compression factor (0-9)
waittime = 5
while True: # do forever
    #os.system('fswebcam --png '+pq+' --subtitle person --save 101.png -r 640x480 -v -S 10 --set brightness=100%')

    #os.system('fswebcam --png '+pq+' --subtitle person --save 101.png -r 640x480')
    #os.system('curl -F "myFile=@101.png" -F "submit=Submit" http://nodered2021.mybluemix.net/upload')

    os.system('fswebcam --png '+pq+' --subtitle person --save 101.png -r 640x480 && curl -F myFile=@101.png -F submit=Submit http://nodered2021.mybluemix.net/upload')
    print('waiting %d seconds...' % waittime)
    time.sleep(waittime)

