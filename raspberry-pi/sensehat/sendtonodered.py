import pygame, sys
from pygame.locals import *
import pygame.camera
import os
import time
from sense_hat import SenseHat
import websocket

imageUploadURL=os.getenv("ImageUploadURL",default="http://nodered2021.mybluemix.net/upload")
webSocketURL=os.getenv("WebSocketURL",default="wss://nodered2021.mybluemix.net/ws/chat")
videoSource=os.getenv("VideoSource",default="/dev/video0")

#websocket.enableTrace(True)
ws = websocket.WebSocket()
try:
    ws.connect(webSocketURL)
except websocket._exceptions.WebSocketBadStatusException as e:
    print("Cannot connect to Web socket")

sense = SenseHat()

waittime=5
pygame.init()
pygame.camera.init()
cam = pygame.camera.Camera(videoSource,(640,480)) # (352,288))
while True: # do forever
    cam.start()
    image= cam.get_image()
    pygame.image.save_extended(image,'101.jpg')
    cam.stop()
    os.system('curl -F myFile=@101.jpg -F submit=Submit '+imageUploadURL)
    start_time = time.time()
    temp = sense.get_temperature_from_pressure()
    if temp == 0: temp = sense.get_temperature_from_pressure()
    #temp = sense.get_temperature_from_humidity()
    sense.show_message("{:.1f} C".format(temp))
    message='{"user":"raspberrypi4","message":"%d: %s"}'%(start_time,"Temperature: %s C" % temp)
    print(message)
    try:
        ws.send(message)
    except (BrokenPipeError,websocket._exceptions.WebSocketConnectionClosedException) as e:
        try:
            ws.connect(webSocketURL)
            ws.send(message)
        except (BrokenPipeError,websocket._exceptions.WebSocketBadStatusException,websocket._exceptions.WebSocketConnectionClosedException) as e:
            print("Cannot send to Web Socket, Ignored")

    print('waiting %d seconds...' % waittime)
    time.sleep(waittime)
