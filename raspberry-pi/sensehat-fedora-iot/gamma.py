from sense_hat import SenseHat
sense = SenseHat()
pixels = [3*[c] for c in range(64)]
sense.set_pixels(pixels)
