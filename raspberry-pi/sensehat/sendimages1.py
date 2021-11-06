import pygame, sys
from pygame.locals import *
import pygame.camera
import os
import time

waittime=5
pygame.init()
pygame.camera.init()
cam = pygame.camera.Camera("/dev/video0",(640,480)) # (352,288))
while True: # do forever
    cam.start()
    image= cam.get_image()
    pygame.image.save_extended(image,'101.jpg')
    cam.stop()
    os.system('curl -F "myFile=@101.jpg" -F "submit=Submit" http://nodered2021.mybluemix.net/upload')
    print('waiting %d seconds...' % waittime)
    time.sleep(waittime)

