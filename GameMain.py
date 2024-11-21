import random
import time
import threading
from sense_hat import SenseHat
import Ball
import Board
import Paddle
import Send
import Listen
from Menu import Menu


sense = SenseHat()

#Deffualt game class
class Game:
    def __init__(self):

        self.board = Board.GameBoard()
        self.paddle = Paddle.Paddle()
        self.ball = Ball.Ball()

        self.lives = 3  # Initialize with 3 lives
        self.sleep_time = .5
        self.stop_threads = False
        self.win_con = 0
        self.ending = 0
        self.RIGHTPI_IP = "10.41.10.52"
        self.LEFTPI_IP = "10.41.10.55"
        self.is_multiplayer = False


    #Function to loop game (Runs in a thread at the bottom)
    def game_loop(self):
        self.board.set_bg()  # Set background
        time.sleep(0.1)  # Small delay to ensure the paddle is visible
        self.paddle.draw()  # Draw paddle position

        last_position = self.ball.getposition()  # Track last ball position
        while not self.stop_threads:
            self.board.set_bg()  # Clear and reset the background
            self.draw_lives()  # Draw lives first
            self.paddle.draw()  # Draw paddle
            self.ball.draw()  # Draw ball
            time.sleep(0.05)

    def draw_lives(self):
        # Draw lives at top middle of screen
        for i in range(self.lives):
            sense.set_pixel(3 + i, 0, [75, 75, 75])  # White pixels for lives

    def ball_move(self):
        while not self.stop_threads:
            self.ball.move(self.paddle.paddle)

            if self.ball.getposition()[0] == 6 and (self.paddle.paddle - 1) <= self.ball.getposition()[1] <= (
                    self.paddle.paddle + 1):
                if self.get_random_increment() == 1 and self.sleep_time > 0.1:
                    self.sleep_time = round(self.sleep_time - 0.1, 1)
                    print(self.sleep_time)

            time.sleep(self.sleep_time)


    #Function to check ball position and adjust sleep_time/wincon
    def ball_loop(self):

        if self.ball.getposition()[0] == 6 and (self.paddle.paddle - 1) <= self.ball.getposition()[1] <= (self.paddle.paddle + 1):
            if self.get_random_increment() == 1 and self.sleep_time > 0.1:
                self.sleep_time = round(self.sleep_time - 0.1,1)
                print(f"SLEEP TIME DECREASE  {self.sleep_time}")
            if self.sleep_time < 0.2:
                Game.win_con(self)
                print(f"WIN CON INCREASE  {self.win_con}")

        time.sleep(self.sleep_time)

        return self.game_end()

    def ball_loop_Left(self):

        if self.ball.getposition()[0] == 1 and (self.paddle.paddle - 1) <= self.ball.getposition()[1] <= (self.paddle.paddle + 1):
            if self.get_random_increment() == 1 and self.sleep_time > 0.1:
                self.sleep_time = round(self.sleep_time - 0.1,1)
                print(f"SLEEP TIME DECREASE  {self.sleep_time}")
            if self.sleep_time < 0.2:
                Game.win_con(self)
                print(f"WIN CON INCREASE  {self.win_con}")

        time.sleep(self.sleep_time)

        return self.game_end_left()

    #Functions get game ending
    def game_end(self):
        if self.ball.getposition()[0] == 7:  # Ball hits back wall
            if self.lives <= 0:  # Already at 0 lives and hit the wall again
                print("Right player loses.")
                if self.is_multiplayer:
                    self.send = Send.Send(str(["END", 2]), (self.RIGHTPI_IP, 1777))
                time.sleep(.5)
                self.stop_threads = True
                time.sleep(.5)
                return 2
            else:
                self.lives -= 1  # Decrease lives
                # Reset ball to in front of right paddle
                self.ball.setposition([5, self.paddle.paddle])  # Place ball in front of paddle
                self.ball.setvelocity([-1, self.ball.getvelocity()[1]])  # Keep original y velocity
                time.sleep(0.5)  # Brief pause
        elif self.win_con >= 5:  # Win condition
            print("Right player wins.")
            if self.is_multiplayer:
                self.send = Send.Send(str(["END", 1]), (self.RIGHTPI_IP, 1777))
            time.sleep(.5)
            self.stop_threads = True
            time.sleep(.5)
            return 1
        return 0


    def game_end_left(self):
        if self.ball.getposition()[0] == 0:  # Ball hits back wall
            if self.lives <= 0:  # Already at 0 lives and hit the wall again
                print("Left player loses.")
                if self.is_multiplayer:
                    self.send = Send.Send(str(["END", 2]), (self.LEFTPI_IP, 1888))
                self.stop_threads = True
                self.game_lose()
                return 2
            else:
                self.lives -= 1  # Decrease lives
                # Reset ball to in front of left paddle
                self.ball.setposition([2, self.paddle.paddle])  # Place ball in front of paddle
                self.ball.setvelocity([1, self.ball.getvelocity()[1]])  # Keep original y velocity
                time.sleep(0.5)  # Brief pause
        elif self.win_con >= 5:  # Win condition
            print("Left player wins.")
            if self.is_multiplayer:
                self.send = Send.Send(str(["END", 1]), (self.LEFTPI_IP, 1888))
            self.stop_threads = True
            self.game_win()
            return 1
        return 0


    def game_win(self):
        self.draw_box([0, 255, 0])
        time.sleep(1)
        sense.show_message("WINNER!!!", text_colour=[0, 255, 0])

    def game_lose(self):
        self.draw_box([255, 0, 0])
        time.sleep(1)
        sense.show_message("LOSER!!!", text_colour=[255, 0, 0])

    def win_con(self):
        self.win_con += 1
        print(self.win_con)


    #Function to draw ending spiral
    def draw_box(self, color=[0, 255, 0]):  # Set default color to green
        spiral = [
            (0,0), (1,0), (2,0), (3,0), (4,0), (5,0), (6,0), (7,0),
            (7,1), (7,2), (7,3), (7,4), (7,5), (7,6), (7,7),
            (6,7), (5,7), (4,7), (3,7), (2,7), (1,7), (0,7),
            (0,6), (0,5), (0,4), (0,3), (0,2), (0,1),
            (1,1), (2,1), (3,1), (4,1), (5,1), (6,1),
            (6,2), (6,3), (6,4), (6,5), (6,6),
            (5,6), (4,6), (3,6), (2,6), (1,6),
            (1,5), (1,4), (1,3), (1,2),
            (2,2), (3,2), (4,2), (5,2),
            (5,3), (5,4), (5,5),
            (4,5), (3,5), (2,5),
            (2,4), (2,3),
            (3,3), (4,3),
            (4,4), (3,4)
        ]
        for pos in spiral:
            sense.set_pixel(pos[0], pos[1], color)
            time.sleep(0.01)


    #Function to flip a coin
    def get_random_increment(self):
        num = random.randint(0, 1)
        return num


def listen(self, address, port):
    received_data = None
    while received_data is None:
        self.listen = Listen.Server((address, port))
        received_data = self.listen.WaitForConnection()
        print(f"Raw received data: {received_data}")

    if received_data == "['END', 1]":
        print("Received end-game signal. Opponent has won.")
        self.stop_threads = True
        self.game_lose()  # Show loss screen
        return  # Exit immediately

    elif received_data == "['END', 2]":
        print("Received end-game signal. Opponent has lost.")
        self.stop_threads = True
        self.game_win()  # Show win screen
        return  # Exit immediately


    try:
        # Assuming the data is sent as a list [position, velocity, sleep_time]
        received_data = eval(received_data)  # Parse the string into a list
        position = received_data[0]
        velocity = received_data[1]
        self.sleep_time = received_data[2]


        print(f"Parsed position: {position}, velocity: {velocity}, sleep_time: {self.sleep_time}")  # Debug parsed data

        # Set the ball's position and velocity
        self.ball.setposition(position)
        self.ball.setvelocity(velocity)

        self.ball.frozen = False

        # Resume the game by setting the event
        print("Setting resume_game_event to continue the loop after receiving data.")


    except Exception as e:
        print(f"Error processing received data: {e}")

    received_data = None

#Class for Multiplayer game right side
class MPGameRight(Game):
    def __init__(self):
        super().__init__()
        self.is_multiplayer = True

    def mpball_loop_right(self):
        while not self.stop_threads:
            self.board.set_bg()
            self.paddle.draw()
            self.ball.draw()

            current_pos = self.ball.getposition()
            
            # Check if ball is at position 1 (one pixel after bouncing off left wall)
            if current_pos[0] == 1:
                send_position = [6, current_pos[1]]
                send_velocity = [-1, self.ball.getvelocity()[1]]

                ball_data = [send_position, send_velocity, self.sleep_time, self.ending]
                print(f"Sending ball data from right to left: {ball_data}")
                self.send = Send.Send(str(ball_data), (self.LEFTPI_IP, 1888))
                self.ball.frozen = True  # Keep ball bouncing in place
                self.ball.opposite_side = True  # Enable opposite side bouncing
                listen(self, self.RIGHTPI_IP, 1777)

            time.sleep(0.01)
            return Game.ball_loop(self)


#Class for Multiplayer game left side
class MPGameLeft(Game):
    def __init__(self):
        super().__init__()
        self.paddle = Paddle.PaddleLeft()
        self.ball = Ball.BallLeft()
        self.is_multiplayer = True
        self.just_received = False  # Track if we just received the ball

    def mpball_loop_left(self):
        # First listen for initial ball data
        if self.ball.frozen:
            listen(self, self.LEFTPI_IP, 1888)
            self.just_received = True  # Mark that we just received the ball

        while not self.stop_threads:
            self.board.set_bg()
            self.paddle.draw()
            self.ball.draw()

            current_pos = self.ball.getposition()
            
            # Reset just_received flag when ball moves away from receive position
            if current_pos[0] < 5:
                self.just_received = False
            
            # Check if ball is at position 5 and we didn't just receive it
            if current_pos[0] == 5 and not self.just_received:
                send_position = [1, current_pos[1]]
                send_velocity = [1, self.ball.getvelocity()[1]]

                ball_data = [send_position, send_velocity, self.sleep_time, self.ending]
                print(f"Sending ball data from left to right: {ball_data}")
                self.send = Send.Send(str(ball_data), (self.RIGHTPI_IP, 1777))
                self.ball.frozen = True
                self.ball.opposite_side = True
                listen(self, self.LEFTPI_IP, 1888)
                self.just_received = True  # Mark that we just received the ball

            time.sleep(0.01)
            return Game.ball_loop_Left(self)

    def ball_move(self):
        while not self.stop_threads:
            self.ball.move(self.paddle.paddle)

            if self.ball.getposition()[0] == 1 and (self.paddle.paddle - 1) <= self.ball.getposition()[1] <= (
                    self.paddle.paddle + 1):
                if self.get_random_increment() == 1 and self.sleep_time > 0.1:
                    self.sleep_time = round(self.sleep_time - 0.1, 1)
                    print(self.sleep_time)

            time.sleep(self.sleep_time)


def main():
    # Initialize and run the menu
    menu = Menu()
    menu.run_menu()  # Select side and wait for connection synchronization

    # Determine the game type based on the player's side
    if menu.player_side == 'L':
        print("Starting Multiplayer Game as Left Player")
        game = MPGameLeft()  # Initialize left player multiplayer game
    elif menu.player_side == 'R':
        print("Starting Multiplayer Game as Right Player")
        game = MPGameRight()  # Initialize right player multiplayer game
    elif menu.player_side == 'S':
        print("Starting Single Player Game")
        game = Game()  # Initialize single-player game directly

    # Configure the Sense HAT joystick to control the paddle
    sense.stick.direction_up = game.paddle.move_up
    sense.stick.direction_down = game.paddle.move_down

    # Set up game threads for game loop and ball movement
    gamethread = threading.Thread(target=game.game_loop)
    gamethread.start()
    ballthread = threading.Thread(target=game.ball_move)
    ballthread.start()

    # Run game ending checks
    while not game.stop_threads:
        if menu.player_side == 'L':
            game.ending = game.mpball_loop_left()
        elif menu.player_side == 'R':
            game.ending = game.mpball_loop_right()
        elif menu.player_side == 'S':
            game.ending = game.ball_loop()

        # Handle game end conditions
        if game.ending == 1:
            game.stop_threads = True
            gamethread.join()
            ballthread.join()
            game.game_win()
        elif game.ending == 2:
            game.stop_threads = True
            gamethread.join()
            ballthread.join()
            game.game_lose()
main()