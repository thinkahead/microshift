from sense_hat import SenseHat
from time import sleep

sense = SenseHat()

r = (255, 0, 0)     # red
o = (255, 64, 0)   # orange
y = (255, 255, 0)   # yellow
g = (0, 255, 0)     # green
c = (0, 255, 255)   # cyan
b = (0, 0, 255)     # blue
p = (255, 0, 255)   # purple
n = (255, 128, 128) # pink
w =(255, 255, 255)  # white
k = (0, 0, 0)       # blank

rainbow = [r, o, y, g, c, b, p, n]

heart = [
        k, r, r, k, k, r, r, k,
        r, r, r, r, r, r, r, r,
        r, r, r, r, r, r, r, r,
        r, r, r, r, r, r, r, r,
        r, r, r, r, r, r, r, r,
        k, r, r, r, r, r, r, k,
        k, k, r, r, r, r, k, k,
        k, k, k, r, r, k, k, k
        ]

while True:
    sense.clear(p)
    sleep(2)
    sense.set_pixels(heart)
    sleep(2)
    sense.clear()
    for y in range(8):
        colour = rainbow[y]
        for x in range(8): sense.set_pixel(x, y, colour)
        sleep(1)
    sleep(1)
    sense.show_message("THANK YOU!", text_colour = w, back_colour = k)
    sleep(3)
