from sense_hat import SenseHat
sense = SenseHat()

class Paddle:
    def __init__(self):
        self.paddle = 3  # Starting position
        self.color = [255, 0, 0]

    def draw(self):
        sense.set_pixel(7, self.paddle, self.color)
        sense.set_pixel(7, self.paddle + 1, self.color)
        sense.set_pixel(7, self.paddle - 1, self.color)

    def move_up(self, event):
        if event.action == 'pressed' and self.paddle > 1:
            self.paddle -= 1

    def move_down(self, event):
        if event.action == 'pressed' and self.paddle < 6:
            self.paddle += 1

class PaddleLeft(Paddle):
    def __init__(self):
        Paddle.__init__(self)

    def draw(self):
        sense.set_pixel(0, self.paddle, self.color)
        sense.set_pixel(0, self.paddle + 1, self.color)
        sense.set_pixel(0, self.paddle - 1, self.color)