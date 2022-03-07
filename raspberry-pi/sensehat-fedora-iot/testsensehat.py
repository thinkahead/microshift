from sense_hat import SenseHat
import time
sense = SenseHat()
while True:
   t = sense.get_temperature()
   p = sense.get_pressure()
   h = sense.get_humidity()
   msg = "Temperature = %s, Pressure=%s, Humidity=%s" % (t,p,h)
   print(msg)
   time.sleep(0.5)
