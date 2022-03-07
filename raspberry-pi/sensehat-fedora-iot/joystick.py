from sense_hat import SenseHat
from time import sleep
sense = SenseHat()

e = (0, 0, 0)
w = (255, 255, 255)

sense.clear()
while True:
    up, down, left, right, push = sense.get_state() 
    if up: sense.show_letter("U")      # Up arrow
    elif down: sense.show_letter("D")  # Down arrow
    elif left: sense.show_letter("L")  # Left arrow
    elif right: sense.show_letter("R") # Right arrow
    elif push: sense.show_letter("M")  # Enter key
      
