from sense_hat import SenseHat

sense = SenseHat()

temp = sense.get_temperature_from_humidity()
print("Temperature: %s C" % temp)
sense.show_message("successfully installed")