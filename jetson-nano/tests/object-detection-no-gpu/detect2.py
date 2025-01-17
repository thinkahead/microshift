import argparse
import sys
import time

import cv2
from object_detector import ObjectDetector
from object_detector import ObjectDetectorOptions
import utils
import os
import websocket

imageUploadURL=os.getenv("ImageUploadURL",default="http://mynodered.mybluemix.net/upload")
webSocketURL=os.getenv("WebSocketURL",default="wss://mynodered.mybluemix.net/ws/chat")

ws = websocket.WebSocket()
try:
    ws.connect(webSocketURL)
except websocket._exceptions.WebSocketBadStatusException as e:
    print("Cannot connect to Web socket")

def run(model: str, camera_id: int, width: int, height: int, num_threads: int) -> None:
  """Continuously run inference on images acquired from the camera.

  Args:
    model: Name of the TFLite object detection model.
    camera_id: The camera id to be passed to OpenCV.
    width: The width of the frame captured from the camera.
    height: The height of the frame captured from the camera.
    num_threads: The number of CPU threads to run the model.
  """

  # Variables to calculate FPS
  counter, fps = 0, 0
  start_time = time.time()

  # Start capturing video input from the camera
  cap = cv2.VideoCapture(camera_id)
  cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
  cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

  # Visualization parameters
  row_size = 20  # pixels
  left_margin = 24  # pixels
  text_color = (0, 0, 255)  # red
  font_size = 1
  font_thickness = 1
  fps_avg_frame_count = 10

  # Initialize the object detection model
  options = ObjectDetectorOptions(num_threads=num_threads, score_threshold=0.3, max_results=3, enable_edgetpu=False)
  detector = ObjectDetector(model_path=model, options=options)

  # Continuously capture images from the camera and run inference
  while cap.isOpened():
    success, image = cap.read()
    if not success: sys.exit('ERROR: Unable to read from webcam. Please verify your webcam settings.')

    counter += 1
    image = cv2.flip(image, 1)

    # Run object detection estimation using the model.
    detections = detector.detect(image)
    print(detections)
    for detection in detections:
        for category in detection.categories:
            if category.label=='person':
                print('Found person')
                break
        else: continue
        break
    else: continue

    message='{"user":"jetsonnano","message":"%d: %s"}'%(start_time,detections)
    #print(message)
    try:
        ws.send(message)
    except (BrokenPipeError,websocket._exceptions.WebSocketConnectionClosedException) as e:
        try:
            ws.connect(webSocketURL)
            ws.send(message)
        except (BrokenPipeError,websocket._exceptions.WebSocketBadStatusException,websocket._exceptions.WebSocketConnectionClosedException) as e:
            print("Cannot send to Web Socket, Ignored")

    # Draw keypoints and edges on input image
    image = utils.visualize(image, detections)

    # Calculate the FPS
    if counter % fps_avg_frame_count == 0:
      end_time = time.time()
      fps = fps_avg_frame_count / (end_time - start_time)
      start_time = time.time()

    # Show the FPS
    fps_text = 'FPS = {:.1f}'.format(fps)
    text_location = (left_margin, row_size)
    cv2.putText(image, fps_text, text_location, cv2.FONT_HERSHEY_PLAIN, font_size, text_color, font_thickness)

    #cv2.imshow('object_detector', image)
    cv2.imwrite("101.jpg", image)
    os.system('curl -F myFile=@101.jpg -F submit=Submit '+imageUploadURL)

  cap.release()
  cv2.destroyAllWindows()

def main():
  parser = argparse.ArgumentParser(
      formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument(
      '--model',
      help='Path of the object detection model.',
      required=False,
      default='efficientdet_lite0.tflite')
  parser.add_argument(
      '--cameraId', help='Id of camera.', required=False, type=int, default=0)
  parser.add_argument(
      '--frameWidth',
      help='Width of frame to capture from camera.',
      required=False,
      type=int,
      default=640)
  parser.add_argument(
      '--frameHeight',
      help='Height of frame to capture from camera.',
      required=False,
      type=int,
      default=480)
  parser.add_argument(
      '--numThreads',
      help='Number of CPU threads to run the model.',
      required=False,
      type=int,
      default=4)
  args = parser.parse_args()

  run(args.model, int(args.cameraId), args.frameWidth, args.frameHeight, int(args.numThreads))


if __name__ == '__main__':
  main()
