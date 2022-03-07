from sense_hat import SenseHat

sense = SenseHat()
sense.set_rotation(90)

temp = sense.get_temperature_from_pressure()
#temp = sense.get_temperature_from_humidity()
print("Temperature: %s C" % temp)
sense.show_message("{:.1f} C".format(temp),text_colour=(255,255,255))
