from sense_hat import SenseHat
sense = SenseHat()

class GameBoard:
    def __init__(self):
        self.O = [0, 50, 50]

    def set_bg(self):
        background = [self.O] * 64
        sense.set_pixels(background)

    def clear(self):
        sense.clear()