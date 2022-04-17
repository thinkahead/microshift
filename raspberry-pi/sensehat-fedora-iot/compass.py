# Make a Compass
from sense_hat import SenseHat
import time

hat = SenseHat()
while True:
    bearing = hat.get_compass()
    print ('bearing: {:.0f} to north'.format(bearing))
