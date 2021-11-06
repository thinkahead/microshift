## Docker container for Raspberry Pi Sensehat and USB camera

Testing the programs separately
```
python test.py
python testcam.py
python sparkles.py
```

Build and push the image
```
docker build -t karve/sensehat .
docker run --privileged --name sensehat -ti karve/sensehat bash
docker push karve/sensehat
```

This deployment in microshift will start sending images to Node-Red
```
kubectl create -f sensehat.yaml
```

Delete the deployment to stop sending image
```
kubectl delete -f sensehat.yaml
```

