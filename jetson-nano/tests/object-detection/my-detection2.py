import jetson.inference
import jetson.utils
import time
import cv2
import numpy as np 
import websocket
import os
imageUploadURL=os.getenv("ImageUploadURL",default="http://nodered2021.mybluemix.net/upload")
webSocketURL=os.getenv("WebSocketURL",default="wss://nodered2021.mybluemix.net/ws/chat")
videoSource=os.getenv("VideoSource",default="/dev/video0")
#websocket.enableTrace(True)
ws = websocket.WebSocket()
try:
    ws.connect(webSocketURL)
except websocket._exceptions.WebSocketBadStatusException as e:
    print("Cannot connect to Web socket")

timeStamp=time.time()
fpsFilt=0
net=jetson.inference.detectNet('ssd-mobilenet-v2',threshold=.5)
dispW=640
dispH=480
flip=2
font=cv2.FONT_HERSHEY_SIMPLEX
 
# Gstreamer code for improvded Raspberry Pi Camera Quality
#camSet='nvarguscamerasrc wbmode=3 tnr-mode=2 tnr-strength=1 ee-mode=2 ee-strength=1 ! video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! videobalance contrast=1.5 brightness=-.2 saturation=1.2 ! appsink'
#cam=cv2.VideoCapture(camSet)
#cam=jetson.utils.gstCamera(dispW,dispH,'0')
 
cam=cv2.VideoCapture(videoSource)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, dispW)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, dispH)
 
#cam=jetson.utils.gstCamera(dispW,dispH,'/dev/video1')
#display=jetson.utils.glDisplay()
#while display.IsOpen():
while True:
    #img, width, height= cam.CaptureRGBA()
    _,img = cam.read()
    height=img.shape[0]
    width=img.shape[1]
 
    frame=cv2.cvtColor(img,cv2.COLOR_BGR2RGBA).astype(np.float32)
    frame=jetson.utils.cudaFromNumpy(frame)
 
    detections=net.Detect(frame, width, height)
    for detect in detections:
        #print(detect)
        ID=detect.ClassID
        top=int(detect.Top)
        left=int(detect.Left)
        bottom=int(detect.Bottom)
        right=int(detect.Right)
        item=net.GetClassDesc(ID)
        #print(item,top,left,bottom,right)
        cv2.rectangle(img, (left, top), (right, bottom), (0, 0, 0), 2)
        cv2.putText(img, item, (left,top), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 1)
        if ID==1: # person detected
            message='{"user":"jetsonnano","message":"%d: %s"}'%(timeStamp,str(detect).replace("\n",""))
            #print(message)
            try:
                ws.send(message)
            except (BrokenPipeError,websocket._exceptions.WebSocketConnectionClosedException) as e:
                try:
                    ws.connect(webSocketURL)
                    ws.send(message)
                except (BrokenPipeError,websocket._exceptions.WebSocketBadStatusException,websocket._exceptions.WebSocketConnectionClosedException) as e:
                    print("Cannot send to Web Socket, Ignored")

    #display.RenderOnce(img,width,height)
    dt=time.time()-timeStamp
    timeStamp=time.time()
    fps=1/dt
    fpsFilt=.9*fpsFilt + .1*fps
    #print(str(round(fps,1))+' fps')
    cv2.putText(img,str(round(fpsFilt,1))+' fps',(0,30),font,1,(0,0,255),2)
    #cv2.imshow('detCam',img)
    #cv2.moveWindow('detCam',0,0)
    cv2.imwrite("101.jpg", img)
    os.system('curl -F myFile=@101.jpg -F submit=Submit '+imageUploadURL)
    #if cv2.waitKey(1)==ord('q'): break
cam.release()
cv2.destroyAllWindows()
