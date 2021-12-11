# TensorFlow Lite Python object detection example with Jetson Nano (No GPU), SenseHat and Node Red

This example uses [TensorFlow Lite](https://tensorflow.org/lite) with Python on
a Raspberry Pi to perform real-time object detection using images streamed from
the USB Camera. It draws a bounding box around each detected object
when the object score is above a given threshold.

## Build the docker image and run the container
```
docker build -t docker.io/karve/object-detection-jetsonnano .
docker push docker.io/karve/object-detection-jetsonnano:latest
docker run --rm -d --privileged docker.io/karve/object-detection-jetsonnano:latest
```

You should see the camera feed appear on the Node Red image viewer if the image has a person.
Put some objects in front of the camera, like a coffee mug or keyboard, and
you'll see boxes drawn around those that the model recognizes, including the
label and score for each. It also prints the number of frames per second (FPS)
at the top-left corner of the screen. 

For more information about executing inferences with TensorFlow Lite, read
[TensorFlow Lite inference](https://www.tensorflow.org/lite/guide/inference).

References
- Tensorflow Lite examples https://github.com/tensorflow/examples/tree/master/lite/examples/object_detection/raspberry_pi
- Latest tflite runtimes https://google-coral.github.io/py-repo/tflite-runtime/
- Latest numpy https://pypi.org/project/numpy/#files
