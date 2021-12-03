from sense_hat import SenseHat

sense = SenseHat()

temp = sense.get_temperature_from_pressure()
#temp = sense.get_temperature_from_humidity()
print("Temperature: %s C" % temp)
sense.show_message("{:.1f} C".format(temp))
