import random
import time
import threading
from sense_hat import SenseHat
import Ball
import Board
import Paddle

sense = SenseHat()

#Deffualt game class
class Game:
    def __init__(self):
        self.board = Board.GameBoard()
        self.paddle = Paddle.Paddle()
        self.ball = Ball.Ball()
        self.sleep_time = 0.5
        self.stop_threads = False
        self.win_con = 0

    #Function to loop game (Runs in a thread at the bottom)
    def game_loop(self):
        while not self.stop_threads:
            self.board.set_bg()
            self.paddle.draw()
            self.ball.draw()
            time.sleep(0.05)
            self.board.clear()


    #Function to check ball position and adjust sleep_time/wincon
    def ball_loop(self):
        self.ball.move(self.paddle.paddle)
        if self.ball.getposition()[0] == 6 and (self.paddle.paddle - 1) <= self.ball.getposition()[1] <= (self.paddle.paddle + 1):
            if self.get_random_increment() == 1 and self.sleep_time > 0.1:
                self.sleep_time = round(self.sleep_time - 0.1,1)
                print(self.sleep_time)
            if self.sleep_time < 0.2:
                Game.win_con(self)
        time.sleep(self.sleep_time)
        return self.game_end()


    #Functions get game ending
    def game_end(self):
        if self.ball.position[0] == 8:                      # Lose con
            return 2
        elif self.win_con >= 4:                             # Win con
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


#Class for Multiplayer game right side
class MPGameRight(Game):
    def __init__(self):
        super().__init__()
        self.board = Board.GameBoard()
        self.paddle = Paddle.Paddle()
        self.ball = Ball.Ball()
        self.sleep_time = 0.5
        self.stop_threads = False
        self.win_con = 0

    def mpball_loop_right(self):
        self.ball.move(self.paddle.paddle)
        if self.ball.getposition()[0] == 0: ########################## Send Ball to other screen Con
            print(self.ball.getposition(), self.ball.getvelocity(), self.sleep_time)
            #
            # This is the stuff that will happen when the ball go's off-screen.
            #
        if self.ball.getposition()[0] == 6 and (self.paddle.paddle - 1) <= self.ball.getposition()[1] <= (
                self.paddle.paddle + 1):
            if self.get_random_increment() == 1 and self.sleep_time > 0.1:
                self.sleep_time = round(self.sleep_time - 0.1, 1)
                print(self.sleep_time)
            if self.sleep_time < 0.2:
                Game.win_con(self)

        time.sleep(self.sleep_time)
        return self.game_end()

#Class for Multiplayer game left side
class MPGameLeft(Game):
    def __init__(self):
        super().__init__()
        self.board = Board.GameBoard()
        self.paddle = Paddle.PaddleLeft()
        self.ball = Ball.BallLeft()
        self.sleep_time = 0.5
        self.stop_threads = False
        self.win_con = 0

    def mpball_loop_left(self):
        self.ball.move(self.paddle.paddle)
        if self.ball.getposition()[0] == 7: ########################## Send Ball to other screen Con
            print(self.ball.getposition(), self.ball.getvelocity(), self.sleep_time)
            #
            # This is the stuff that will happen when the ball go's off-screen.
            #
        if self.ball.getposition()[0] == 1 and (self.paddle.paddle - 1) <= self.ball.getposition()[1] <= (
                self.paddle.paddle + 1):
            if self.get_random_increment() == 1 and self.sleep_time > 0.1:
                self.sleep_time = round(self.sleep_time - 0.1, 1)
                print(self.sleep_time)
            if self.sleep_time < 0.2:
                Game.win_con(self)

        time.sleep(self.sleep_time)
        return self.game_end()


def main():

    #Function to return game type
    def game_type(response):
        if response == "S":
            return 0
        elif response == "M":
            response = input("Select Player (L for left -- R for right) ").upper()
            if response == "L":
                return 1
            elif response == "R":
                return 2


    #Function to display countdown
    def count_down():
        white = (255,255,255)
        three = [
            (1, 1), (2, 1), (3, 1), (4, 1), (5, 2), (5, 3),
            (3, 4), (4, 4), (5, 4), (5, 5), (5, 6), (1, 6), (2, 6), (3, 6),(4,6)
        ]
        two = [
            (1, 1), (2, 1), (3, 1), (4, 1), (5, 1),  (5, 2), (5, 3),(4, 4),
            (3, 4), (2, 4), (1, 4), (1, 5), (1, 6),(2, 6), (3, 6), (4, 6), (5, 6)
        ]
        one = [
        (3, 1), (4, 1), (4, 2),  (4, 3),  (4, 4),  (4, 5), (4, 6)
        ]
        sense.clear()
        for pixel in three:
            sense.set_pixel(pixel[0], pixel[1], white)
        time.sleep(1)
        sense.clear()
        for pixel in two:
            sense.set_pixel(pixel[0], pixel[1], white)
        time.sleep(1)
        sense.clear()
        for pixel in one:
            sense.set_pixel(pixel[0], pixel[1], white)
        time.sleep(1)
        sense.clear()


    #Ask player for game type
    print("Welcome to Pi-Pong 2.0")
    gametype = game_type(input("Which game type would you like to play? (S for Single or M for Multi): ").upper())


    #Run
    #Game Type: Single player
    if gametype == 0:
        count_down()
        game = Game()
        sense.stick.direction_up = game.paddle.move_up
        sense.stick.direction_down = game.paddle.move_down

            # Run the game loop in a separate thread
        thread1 = threading.Thread(target=game.game_loop)
        thread1.start()

        while game.game_end() == 0:
            result = game.ball_loop()

            if result == 1:
                game.stop_threads = True
                thread1.join()
                game.game_win()
            elif result == 2:
                game.stop_threads = True
                thread1.join()
                game.game_lose()


    #Run
    #Game Type: Multiplayer (Left side)
    elif gametype == 1:
        count_down()
        game = MPGameLeft()
        sense.stick.direction_up = game.paddle.move_up
        sense.stick.direction_down = game.paddle.move_down
        # Run the game loop in a separate thread
        thread2 = threading.Thread(target=game.game_loop)
        thread2.start()

        while game.game_end() == 0:
            result = game.mpball_loop_left()

            if result == 1:
                game.stop_threads = True
                thread2.join()
                game.game_win()
            elif result == 2:
                game.stop_threads = True
                thread2.join()
                game.game_lose()

    #Run
    #Game Type: Multiplayer (Right side)
    elif gametype == 2:
        count_down()
        game = MPGameRight()
        sense.stick.direction_up = game.paddle.move_up
        sense.stick.direction_down = game.paddle.move_down
        # Run the game loop in a separate thread
        thread2 = threading.Thread(target=game.game_loop)
        thread2.start()

        while game.game_end() == 0:
            result = game.mpball_loop_right()

            if result == 1:
                game.stop_threads = True
                thread2.join()
                game.game_win()
            elif result == 2:
                game.stop_threads = True
                thread2.join()
                game.game_lose()


main()


