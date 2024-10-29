import random
import time
import threading
from sense_hat import SenseHat
import Ball
import Board
import Paddle
import Send
import Listen


sense = SenseHat()


#Deffualt game class
class Game:
    def __init__(self):
        self.board = Board.GameBoard()
        self.paddle = Paddle.Paddle()
        self.ball = Ball.Ball()
        self.sleep_time = 1
        self.stop_threads = False
        self.win_con = 0
        self.address = ("10.41.10.50")
        self.address2 = ("10.41.10.68")
        self.resume_game_event = threading.Event()  # Event to control the game loop pause and resume
        self.resume_game_event.set()


        #Function to loop game (Runs in a thread at the bottom)
    def game_loop(self):
        while not self.stop_threads:
            self.resume_game_event.wait()  # Wait until the ball returns
            self.board.set_bg()
            self.paddle.draw()
            self.ball.draw()
            time.sleep(0.5)
            #self.board.clear()


    def ball_move(self):
        while not self.stop_threads:
            self.ball.move(self.paddle.paddle)
            time.sleep(self.sleep_time)


    #Function to check ball position and adjust sleep_time/wincon
    def ball_loop(self):

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





def listen(self,address,port):
    received_data = None
    while received_data is None:
        self.listen = Listen.Server((address, port))
        received_data = self.listen.WaitForConnection()

    print(f"Raw received data: {received_data}")

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
        self.resume_game_event.set()

    except Exception as e:
        print(f"Error processing received data: {e}")

    received_data = None

    # # Update the ball's state with the received data
    # position = [int(received_data[2]), int(received_data[5])]
    # velocity = [int(received_data[10:12].replace(",", "")), int(received_data[16:18].replace("]", ""))]
    # print(f"Received position: {position}, velocity: {velocity}")
    #
    # # Set ball position and velocity
    # self.ball.setposition(position)
    # self.ball.setvelocity(velocity)
    #
    # # Resume the game by setting the event
    # self.resume_game_event.set()
    #
    # received_data = None  # Reset received data after handling



    # received_data = None
    # while received_data is None:
    #     self.listen = Listen.Server((address, port))
    #     received_data = self.listen.WaitForConnection()
    # print(received_data)
    #
    # # Update the ball's state with the received data
    # position = [int(received_data[2]), int(received_data[5])]
    # velocity = [int(received_data[10:12].replace(",","")),int(received_data[16:18].replace("]",""))]
    # print(position, velocity)
    #
    # self.ball.setposition(position)
    # self.ball.setvelocity(velocity)
    # self.sleep_time = float(received_data[18:20])
    # self.ball.move(self.paddle.paddle)
    # received_data = None


#Class for Multiplayer game right side
class MPGameRight(Game):
    def __init__(self):
        super().__init__()

    def mpball_loop_right(self):
        while not self.stop_threads:
            self.resume_game_event.wait()

            if self.ball.getposition()[0] == 0:
                #self.ball.clear_pixel()  # Clear current position
                self.ball.frozen = True  # Freeze X position
                #self.resume_game_event.clear()  # Pause loop on right Pi

                # Prepare ball data to send
                send_position = self.ball.getposition()
                send_position[0] = 6  # Set to the far side for the left Pi
                send_velocity = self.ball.getvelocity()
                send_velocity[0] = -1  # Reverse the X direction

                ball_data = [send_position, send_velocity, self.sleep_time]
                print(f"Sending ball data from right to left: {ball_data}")
                self.send = Send.Send(str(ball_data), (self.address, 1777))

                # Wait for the ball to come back by blocking until data is received
                listen(self, self.address2, 1888)
                self.resume_game_event.set()  # Resume the loop after receiving data
            else:
                # Only update Y position while the ball is on the opposite side
                self.ball.draw()  # Keep the ball drawn at its last X position
            time.sleep(self.sleep_time)

    # def mpball_loop_right(self):
    #     while not self.stop_threads:
    #         self.resume_game_event.wait()
    #
    #         # Debugging ball movement
    #         print(f"Ball moving on right side: position={self.ball.getposition()}, velocity={self.ball.getvelocity()}")
    #
    #
    #         # Condition for sending the ball to the left Pi
    #         if self.ball.getposition()[0] == 0:
    #             # self.ball.clear_pixel()  # Clear only the ball's pixel
    #             # self.resume_game_event.clear()  # Pause the loop on the right Pi
    #             send_position = self.ball.getposition()
    #             send_position[0] = 6
    #             send_velocity = self.ball.getvelocity()
    #             send_velocity[0] = -1
    #
    #             ball_data = [send_position,send_velocity,self.sleep_time]
    #
    #             print(f"Sending ball data from right to left: {ball_data}")  # Debug sent data
    #             # Send ball data to the other Pi
    #             self.send = Send.Send(str(ball_data), (self.address, 1777))
    #
    #             # self.resume_game_event.clear()
    #             #self.ball.setxposition(0)
    #
    #             # Wait for the ball to come back by blocking until data is received
    #             listen(self, self.address2, 1888)
    #             self.resume_game_event.set()  # Resume the loop after receiving data
    #
    #         time.sleep(self.sleep_time)
    #         #return self.game_end()


#Class for Multiplayer game left side
class MPGameLeft(Game):
    def __init__(self):
        super().__init__()
        self.paddle = Paddle.PaddleLeft()
        self.ball = Ball.BallLeft()

    def mpball_loop_left(self):
        while not self.stop_threads:
            self.resume_game_event.wait()

            if self.ball.getposition()[0] == 7:
                # self.ball.clear_pixel()  # Clear the ball's current pixel
                self.ball.frozen = True  # Freeze X position
                # self.resume_game_event.clear()  # Pause the loop on the left Pi

                # Prepare ball data to send
                send_position = self.ball.getposition()
                send_position[0] = 1  # Set to the far side for the right Pi
                send_velocity = self.ball.getvelocity()
                send_velocity[0] = 1  # Reverse the X direction

                ball_data = [send_position, send_velocity, self.sleep_time]
                print(f"Sending ball data from left to right: {ball_data}")
                self.send = Send.Send(str(ball_data), (self.address2, 1888))

                # Wait for the ball to come back by blocking until data is received
                listen(self, self.address, 1777)
                self.resume_game_event.set()  # Resume the loop after receiving data
            else:
                # Only update Y position while the ball is on the opposite side
                self.ball.draw()  # Keep the ball drawn at its last X position
            time.sleep(self.sleep_time)

    # def mpball_loop_left(self):
    #     while not self.stop_threads:
    #         self.resume_game_event.wait()
    #
    #         print(f"Ball moving on left side: position={self.ball.getposition()}, velocity={self.ball.getvelocity()}")
    #
    #         # Condition for sending the ball to the right Pi
    #         if self.ball.getposition()[0] == 7:
    #             #self.ball.clear_pixel()  # Clear only the ball's pixel
    #             #self.resume_game_event.clear()  # Pause the loop on the left Pi
    #             send_position = self.ball.getposition()
    #             send_position[0] = 1  # Adjust to move it to the other side
    #             send_velocity = self.ball.getvelocity()
    #             send_velocity[0] = 1  # Reverse the X direction
    #
    #             ball_data = [send_position, send_velocity, self.sleep_time]
    #
    #             print(f"Sending ball data from left to right: {ball_data}")  # Debug sent data
    #
    #             # Send ball data to the right Pi
    #             self.send = Send.Send(str(ball_data), (self.address2, 1888))
    #
    #             # Clear the event (pause the game loop)
    #             print("Pausing the game loop on the left side (waiting for ball to return).")
    #             #self.resume_game_event.clear()
    #
    #             # Wait for the ball to come back by blocking until data is received
    #             listen(self, self.address, 1777)
    #             self.resume_game_event.set()  # Resume the loop after receiving data
    #
    #         time.sleep(self.sleep_time)
    #         #return self.game_end()



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
        #count_down()
        game = Game()
        sense.stick.direction_up = game.paddle.move_up
        sense.stick.direction_down = game.paddle.move_down

            # Run the game loop in a separate thread
        ballthread = threading.Thread(target=game.ball_move)
        ballthread.start()
        gamethread = threading.Thread(target=game.game_loop)
        gamethread.start()

        while game.game_end() == 0:
            result = game.ball_loop()

            if result == 1:
                game.stop_threads = True
                ballthread.join()
                game.game_win()
            elif result == 2:
                game.stop_threads = True
                gamethread.join()
                ballthread.join()
                game.game_lose()


    #Run
    #Game Type: Multiplayer (Left side)
    elif gametype == 1:  # Multiplayer left side
        game = MPGameLeft()
        sense.stick.direction_up = game.paddle.move_up
        sense.stick.direction_down = game.paddle.move_down

        # Start listening for the first ball data before starting the loop
        print("Waiting for the first ball to arrive on the left side")  # Debug
        listen(game, game.address, 1777)  # Listen for the first ball

        # Now start the game loop after receiving the first ball
        print("Starting the game loop after receiving the first ball")  # Debug
        gamethread = threading.Thread(target=game.game_loop)
        gamethread.start()

        ballthread = threading.Thread(target=game.ball_move)
        ballthread.start()

        while game.game_end() == 0:
            result = game.mpball_loop_left()
            time.sleep(1)


            if result == 1:
                game.stop_threads = True
                gamethread.join()
                ballthread.join()
                game.game_win()
            elif result == 2:
                game.stop_threads = True
                gamethread.join()
                ballthread.join()
                game.game_lose()

    # elif gametype == 1:
    #     #count_down()
    #     game = MPGameLeft()
    #     sense.stick.direction_up = game.paddle.move_up
    #     sense.stick.direction_down = game.paddle.move_down
    #
    #     # Run the game loop in a separate thread
    #
    #     print("Starting the game loop on the left side")  # Debug
    #     gamethread = threading.Thread(target=game.mpball_loop_left)
    #     gamethread.start()
    #     ballthread = threading.Thread(target=game.ball_move)
    #     ballthread.start()
    #
    #     while game.game_end() == 0:
    #         #################################################################
    #         result = game.mpball_loop_left()
    #         print(game.ball.getvelocity(), game.ball.getposition())
    #
    #
    #         if result == 1:
    #             game.stop_threads = True
    #             gamethread.join()
    #             ballthread.join()
    #             game.game_win()
    #         elif result == 2:
    #             game.stop_threads = True
    #             gamethread.join()
    #             ballthread.join()
    #             game.game_lose()

    #Run
    #Game Type: Multiplayer (Right side)
    elif gametype == 2:
        #count_down()
        game = MPGameRight()
        sense.stick.direction_up = game.paddle.move_up
        sense.stick.direction_down = game.paddle.move_down

        # Run the game loop in a separate thread
        gamethread = threading.Thread(target=game.game_loop)
        gamethread.start()
        ballthread = threading.Thread(target=game.ball_move)
        ballthread.start()

        while game.game_end() == 0:
            result = game.mpball_loop_right()
            print(game.ball.getvelocity(), game.ball.getposition())


            if result == 1:
                game.stop_threads = True
                gamethread.join()
                ballthread.join()
                game.game_win()
            elif result == 2:
                game.stop_threads = True
                gamethread.join()
                ballthread.join()
                game.game_lose()


main()


