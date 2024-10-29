import random
from sense_hat import SenseHat
sense = SenseHat()

class Ball:
    def __init__(self):
        self.position = [3, 3]  # Starting position
        self.velocity = [-1, 1]  # Initial velocity
        self.frozen = False

    def getposition(self):
        return self.position

    def getvelocity(self):
        return self.velocity

    def setposition(self, position):
        self.position = position

    def setxposition(self, position):
        self.position[0] = position

    def setvelocity(self, velocity):
        self.velocity = velocity

    def get_random_color(self):
        return [random.randrange(50, 255) for _ in range(3)]

    def draw(self):
        color = self.get_random_color()
        sense.set_pixel(self.position[0], self.position[1], color)

    def move(self, paddle_position):
        # Move Y position only if frozen, skip X updates
        if not self.frozen:
            self.position[0] += self.velocity[0]
            if self.position[0] == 7 or self.position[0] == 0:
                self.velocity[0] = -self.velocity[0]

        self.position[1] += self.velocity[1]
        if self.position[1] == 7 or self.position[1] == 0:
            self.velocity[1] = -self.velocity[1]

        if self.position[0] == 6 and (paddle_position - 1) <= self.position[1] <= (paddle_position + 1):
            self.velocity[0] = -self.velocity[0]
    # def move(self, paddle_position):
    #     self.position[0] += self.velocity[0]
    #     if self.position[0] == 7 or self.position[0] == 0:
    #         self.velocity[0] = -self.velocity[0]
    #
    #     self.position[1] += self.velocity[1]
    #     if self.position[1] == 7 or self.position[1] == 0:
    #         self.velocity[1] = -self.velocity[1]
    #
    #     if self.position[0] == 6 and (paddle_position - 1) <= self.position[1] <= (paddle_position + 1):
    #         self.velocity[0] = -self.velocity[0]

    def clear_pixel(self):
        """Set the ball's current pixel to the background color."""
        sense.set_pixel(self.position[0], self.position[1], [0, 0, 0])

class BallLeft(Ball):
    def __init__(self):
        super().__init__()

        def move(self, paddle_position):
            if not self.frozen:  # Respect frozen state for X position
                self.position[0] += self.velocity[0]
                if self.position[0] == 7 or self.position[0] == 0:
                    self.velocity[0] = -self.velocity[0]

            self.position[1] += self.velocity[1]
            if self.position[1] == 7 or self.position[1] == 0:
                self.velocity[1] = -self.velocity[1]

    # def move(self, paddle_position):
    #     self.position[0] += self.velocity[0]
    #     if self.position[0] == 7 or self.position[0] == 0:
    #         self.velocity[0] = -self.velocity[0]
    #
    #     self.position[1] += self.velocity[1]
    #     if self.position[1] == 7 or self.position[1] == 0:
    #         self.velocity[1] = -self.velocity[1]
    #
    #     if self.position[0] == 1 and (paddle_position - 1) <= self.position[1] <= (paddle_position + 1):
    #         self.velocity[0] = -self.velocity[0]