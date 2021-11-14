import jetson.inference
import jetson.utils
import time
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
net = jetson.inference.detectNet("ssd-mobilenet-v2", threshold=0.5)
camera = jetson.utils.videoSource(videoSource)
info = jetson.utils.cudaFont()

while True:
    img = camera.Capture()
    start_time = time.time()
    detections = net.Detect(img)
    for detection in detections:
        #item=net.GetClassDesc(detection.ClassID)
        #print(item)
        if detection.ClassID==1: # person detected
            message='{"user":"jetsonnano","message":"%d: %s"}'%(start_time,str(detection).replace("\n",""))
            print(message)
            try:
                ws.send(message)
                jetson.utils.cudaDeviceSynchronize()
                jetson.utils.saveImage("101.jpg", img)
                os.system('curl -F myFile=@101.jpg -F submit=Submit '+imageUploadURL)
            except (BrokenPipeError,websocket._exceptions.WebSocketConnectionClosedException) as e:
                try:
                    ws.connect(webSocketURL)
                    ws.send(message)
                except (BrokenPipeError,websocket._exceptions.WebSocketBadStatusException,websocket._exceptions.WebSocketConnectionClosedException) as e:
                    print("Cannot send to Web Socket, Ignored")
            #time.sleep(5)
            break

