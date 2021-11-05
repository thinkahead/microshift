## Docker container for Raspberry Pi Sensehat and USB camera

```
docker build -t sensehat .
docker run --privileged --name sensehat -ti sensehat bash
python test.py
python testcam.py
python sparkles.py
```
