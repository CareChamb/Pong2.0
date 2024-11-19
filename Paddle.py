from sense_hat import SenseHat
sense = SenseHat()

class Paddle:
    def __init__(self):
        self.paddle = 3  # Starting position
        self.color = [255, 0, 0]
        self.background_color = [0, 50, 50]  # Match the board background color
        self.last_position = self.paddle

    def draw(self):
        # Only update if the paddle has moved

        # Clear the last paddle position
        sense.set_pixel(7, self.last_position, self.background_color)
        sense.set_pixel(7, self.last_position + 1, self.background_color)
        sense.set_pixel(7, self.last_position - 1, self.background_color)

        # Draw the new paddle position
        sense.set_pixel(7, self.paddle, self.color)
        sense.set_pixel(7, self.paddle + 1, self.color)
        sense.set_pixel(7, self.paddle - 1, self.color)

        # Update last position
        self.last_position = self.paddle



    def move_up(self, event):
        if event.action == 'pressed' and self.paddle > 1:
            self.paddle -= 1
            self.draw()

    def move_down(self, event):
        if event.action == 'pressed' and self.paddle < 6:
            self.paddle += 1
            self.draw()

class PaddleLeft(Paddle):
    def __init__(self):
        super().__init__()
        self.color = [100, 0, 255]


    def draw(self):
        # Clear the last paddle position
        sense.set_pixel(0, self.last_position, self.background_color)
        sense.set_pixel(0, self.last_position + 1, self.background_color)
        sense.set_pixel(0, self.last_position - 1, self.background_color)

        # Draw the new paddle position
        sense.set_pixel(0, self.paddle, self.color)
        sense.set_pixel(0, self.paddle + 1, self.color)
        sense.set_pixel(0, self.paddle - 1, self.color)

        # Update last position
        self.last_position = self.paddle



