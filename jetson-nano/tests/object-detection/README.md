# Object detection and sending messages to Node Red

Build the images
```
docker build -t docker.io/karve/jetson-inference:r32.6.1 .
docker push docker.io/karve/jetson-inference:r32.6.1
```

Create a deployment
```
oc apply -f inference.yaml
```

Refer to https://github.com/thinkahead/microshift/blob/main/raspberry-pi/sensehat/README.md#node-red-to-upload-and-display-the-image-along-with-sensehat-readings for setting up your own image viewer and web socket chat on Node Red
