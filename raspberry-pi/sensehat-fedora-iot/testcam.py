import pygame, sys
from pygame.locals import *
import pygame.camera
pygame.init()
pygame.camera.init()
cam = pygame.camera.Camera("/dev/video0",(352,288))
cam.start()
image= cam.get_image()
pygame.image.save(image,'101.bmp')
cam.stop()
