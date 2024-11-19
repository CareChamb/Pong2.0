import random
from sense_hat import SenseHat
sense = SenseHat()

class Ball:
    def __init__(self):
        self.position = [1, 3]  # Starting position
        self.velocity = [1, 1]  # Initial velocity
        self.frozen = False
        self.opposite_side = False

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

    def bounce_opposite_side(self):
        if self.opposite_side:
            self.position[0] = 1  # Set to the far side away from paddle
            self.position[1] += self.velocity[1]
            if self.position[1] == 7 or self.position[1] == 0:
                self.velocity[1] = -self.velocity[1]

    def move(self, paddle_position):
        if not self.frozen:
            # Move the ball in x direction
            self.position[0] += self.velocity[0]

            # Check for wall collisions on x-axis
            if self.position[0] >= 7 or self.position[0] <= 0:
                self.velocity[0] = -self.velocity[0]

            # Move the ball in y direction
            self.position[1] += self.velocity[1]

            # Check for wall collisions on y-axis
            if self.position[1] >= 7 or self.position[1] <= 0:
                self.velocity[1] = -self.velocity[1]

            # Right paddle collision detection
            if self.position[0] == 6:
                if (paddle_position - 1) <= self.position[1] <= (paddle_position + 1):
                    self.velocity[0] = -self.velocity[0]
                elif self.position[1] == (paddle_position + 2) or self.position[1] == (paddle_position - 2):
                    self.velocity[0] = -self.velocity[0]
                    self.velocity[1] = -self.velocity[1]
        else:
            self.bounce_opposite_side()  # Bounce on the far side if frozen


class BallLeft(Ball):
    def __init__(self):
        super().__init__()

    def bounce_opposite_side(self):
        if self.opposite_side:
            self.position[0] = 6  # Set to the far side away from paddle
            self.position[1] += self.velocity[1]
            if self.position[1] == 7 or self.position[1] == 0:
                self.velocity[1] = -self.velocity[1]

    def move(self, paddle_position):
        if not self.frozen:
            # Move the ball in x direction
            self.position[0] += self.velocity[0]

            # Check for wall collisions on x-axis
            if self.position[0] >= 7 or self.position[0] <= 0:
                self.velocity[0] = -self.velocity[0]

            # Move the ball in y direction
            self.position[1] += self.velocity[1]

            # Check for wall collisions on y-axis
            if self.position[1] >= 7 or self.position[1] <= 0:
                self.velocity[1] = -self.velocity[1]

            # Left paddle collision detection
            if self.position[0] == 1:
                if (paddle_position - 1) <= self.position[1] <= (paddle_position + 1):
                    self.velocity[0] = -self.velocity[0]
                elif self.position[1] == (paddle_position + 2) or self.position[1] == (paddle_position - 2):
                    self.velocity[0] = -self.velocity[0]
                    self.velocity[1] = -self.velocity[1]
        else:
            self.bounce_opposite_side()  # Bounce on the far side if frozen
