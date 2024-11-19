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

        self.sleep_time = .5
        self.stop_threads = False
        self.win_con = 0
        self.ending = 0
        self.localip = ("10.41.10.55")
        self.remoteip = ("10.41.10.52")


    #Function to loop game (Runs in a thread at the bottom)
    def game_loop(self):
        self.board.set_bg()  # Set background
        time.sleep(0.1)  # Small delay to ensure the paddle is visible
        self.paddle.draw()  # Draw paddle position

        last_position = self.ball.getposition()  # Track last ball position
        while not self.stop_threads:
            self.board.set_bg()  # Clear and reset the background
            # Get the current position
            current_position = self.ball.getposition()


            # Draw the ball at the current position
            sense.set_pixel(int(current_position[0]), int(current_position[1]), self.ball.get_random_color())

            # Update the last position to the current position
            self.paddle.draw()  # Draw paddle position

            time.sleep(0.05)  # Faster display rate for smooth visuals


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
        if self.ball.getposition()[0] == 7:  # Lose condition
            print("Right player loses.")
            self.send = Send.Send(str(["END", 2]), (self.localip, 1777))  # Send loss message
            time.sleep(.5)
            self.stop_threads = True  # Stop threads to prevent further actions
            time.sleep(.5)
            return 2
        elif self.win_con >= 5:  # Win condition
            print("Right player wins.")
            self.send = Send.Send(str(["END", 1]), (self.localip, 1777))  # Send win message to other player
            time.sleep(.5)
            self.stop_threads = True  # Stop threads to prevent further actions
            time.sleep(.5)
            return 1
        else:
            return 0  # Continue game


    def game_end_left(self):
        if self.ball.getposition()[0] == 0:  # Lose condition
            print("Left player loses.")
            self.send = Send.Send(str(["END", 2]), (self.remoteip, 1888))  # Send loss message
            self.stop_threads = True  # Stop threads to prevent further actions
            self.game_lose()  # Display loss screen
            return 2
        elif self.win_con >= 5:  # Win condition
            print("Left player wins.")
            self.send = Send.Send(str(["END", 1]), (self.remoteip, 1888))  # Send win message to other player
            self.stop_threads = True  # Stop threads to prevent further actions
            self.game_win()  # Display win screen
            return 1
        else:
            return 0  # Continue game


    def game_win(self):
        self.draw_box([0, 255, 0])
        time.sleep(1)
        sense.show_message("WINNER!!!", text_colour=[0, 255, 0])

    def game_lose(self):
        self.draw_box([255, 0, 0])
        time.sleep(1)
        sense.show_message("LOSER!!!", text_colour=[255, 0, 0])

    def win_con(self):
        self.win_con = 1
        print(self.win_con)


    #Function to draw ending spiral
    def draw_box(self, color):
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

    def mpball_loop_right(self):
        while not self.stop_threads:
            self.board.set_bg()  # Clear background
            self.paddle.draw()  # Draw left paddle
            self.ball.draw()  # Draw ball to avoid trails


            if self.ball.getposition()[0] == 0:
                self.ball.setxposition(0)  # set X to 0 before freezing
                self.ball.frozen = True  # Freeze X position
                self.ball.opposite_side = True  # Enable opposite side bouncing

                send_position = self.ball.getposition()
                send_position[0] = 6  # Set to the far side for the left Pi
                send_velocity = self.ball.getvelocity()
                send_velocity[0] = -1  # Reverse the X direction


                ball_data = [send_position, send_velocity, self.sleep_time, self.ending]
                print(f"Sending ball data from right to left: {ball_data}")
                self.send = Send.Send(str(ball_data), (self.localip, 1777))
                listen(self, self.remoteip, 1888)
                self.ball.frozen = False
                self.ball.opposite_side = False  # Reset opposite side bouncing

            time.sleep(0.05)
            return Game.ball_loop(self)


#Class for Multiplayer game left side
class MPGameLeft(Game):
    def __init__(self):
        super().__init__()
        self.paddle = Paddle.PaddleLeft()
        self.ball = Ball.BallLeft()

    def mpball_loop_left(self):
        while not self.stop_threads:
            self.board.set_bg()  # Clear background
            self.paddle.draw()  # Draw left paddle
            self.ball.draw()  # Draw ball to avoid trails



            if self.ball.getposition()[0] == 7:
                self.ball.setxposition(7)  #set X to 7 before freezing
                self.ball.frozen = True  # Freeze X position
                self.ball.opposite_side = True  # Enable opposite side bouncing

                send_position = self.ball.getposition()
                send_position[0] = 1  # Set to the far side for the right Pi
                send_velocity = self.ball.getvelocity()
                send_velocity[0] = 1  # Reverse the X direction

                ball_data = [send_position, send_velocity, self.sleep_time, self.ending]
                print(f"Sending ball data from left to right: {ball_data}")
                self.send = Send.Send(str(ball_data), (self.remoteip, 1888))
                listen(self, self.localip, 1777)
                self.ball.frozen = False
                self.ball.opposite_side = False  # Reset opposite side bouncing after listening

            time.sleep(0.05)
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