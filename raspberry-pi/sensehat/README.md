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

Node-Red to upload and display the image


In Manage Pallette, install the node-red-contrib-image-tools
```
[{"id":"7d8e179a.283e4","type":"http response","z":"d4707ab32022142b","name":"","x":640,"y":920,"wires":[]},{"id":"25859a94.7d9976","type":"http in","z":"d4707ab32022142b","name":"","url":"/upload","method":"post","upload":true,"swaggerDoc":"","x":160,"y":920,"wires":[["d7e5df8b.97a4e8","d63bc821ef4d1e2e"]]},{"id":"e1643981.20d7c8","type":"template","z":"d4707ab32022142b","name":"text","field":"payload","fieldType":"msg","format":"handlebars","syntax":"mustache","template":"File {{name}} uploaded\n","output":"str","x":500,"y":920,"wires":[["7d8e179a.283e4"]]},{"id":"d7e5df8b.97a4e8","type":"function","z":"d4707ab32022142b","name":"toBase64","func":"msg.name = msg.req.files[0].originalname;\n\nif (msg.req.files[0].mimetype.includes('image')) {\n    msg.payload = `<img src=\"data:image/gif;base64,${msg.req.files[0].buffer.toString('base64')}\">`;\n} else {\n    msg.payload = msg.req.files[0].buffer.toString();\n}\n\nreturn msg;","outputs":1,"noerr":0,"x":350,"y":920,"wires":[["e1643981.20d7c8"]]},{"id":"d63bc821ef4d1e2e","type":"function","z":"d4707ab32022142b","name":"toBase64","func":"msg.name = msg.req.files[0].originalname;\n\nif (msg.req.files[0].mimetype.includes('image')) {\n    msg.payload = `${msg.req.files[0].buffer.toString('base64')}`;\n} else {\n    msg.payload = msg.req.files[0].buffer.toString();\n}\n\nreturn msg;","outputs":1,"noerr":0,"initialize":"","finalize":"","libs":[],"x":340,"y":960,"wires":[["7518e9142f5680d8"]]},{"id":"7518e9142f5680d8","type":"image viewer","z":"d4707ab32022142b","name":"","width":"640","data":"payload","dataType":"msg","active":true,"x":510,"y":960,"wires":[[]]}]
```
