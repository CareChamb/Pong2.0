from sense_hat import SenseHat
import time
import socket
import os
import threading

sense = SenseHat()

#constants
RIGHTPI_IP = "10.41.10.52"
LEFTPI_IP = "10.41.10.55"
PORT = 65432


class Menu:
    def __init__(self):
        self.local_ip = self.get_local_ip()
        self.player_side = None  # 'L' for Left, 'R' for Right
        self.connection_established = False
        self.waiting_thread = None  # Thread to handle "Waiting..." message display

    def get_local_ip(self):
        # Get the first IP address of the local machine
        return os.popen("hostname -I").read().strip().split()[0]

    def start_screen(self, R=(100, 0, 0), L=(0, 0, 100), O=(0, 0, 0),S=(100,100,100)):
        screen = [
            L, O, O, O, O, R, R, R,
            L, O, O, O, O, R, O, R,
            L, O, O, O, O, R, R, O,
            L, L, L, S, S, R, O, R,
            O, O, S, O, O, O, O, O,
            O, O, O, S, S, O, O, O,
            O, O, O, O, O, S, O, O,
            O, O, S, S, S, O, O, O
        ]
        sense.set_pixels(screen)


    def count_down(self):
        white = (255, 255, 255)
        three = [
            (1, 1), (2, 1), (3, 1), (4, 1), (5, 2), (5, 3),
            (3, 4), (4, 4), (5, 4), (5, 5), (5, 6), (1, 6), (2, 6), (3, 6), (4, 6)
        ]
        two = [
            (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (5, 2), (5, 3), (4, 4),
            (3, 4), (2, 4), (1, 4), (1, 5), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6)
        ]
        one = [
            (3, 1), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6)
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


    def select_side(self):
        self.start_screen()  # Show initial screen
        self.player_side = 'X'  # Default to nothing

        selected = False
        while not selected:
            for event in sense.stick.get_events():
                if event.action == 'pressed':
                    if event.direction == 'left':
                        self.player_side = 'L'
                        self.start_screen(R=(100, 0, 0), L=(0, 0, 255),S=(100, 100, 100))

                    elif event.direction == 'right':
                        self.player_side = 'R'
                        self.start_screen(R=(255, 0, 0), L=(0, 0, 100),S=(100, 100, 100))

                    elif event.direction == 'down':
                        self.player_side = 'S'
                        self.start_screen(R=(100, 0, 0), L=(0, 0, 100),S=(255, 255, 255))


                    elif event.direction == 'middle':
                        selected = True
                        break

        time.sleep(0.5)
        sense.clear()

    def display_waiting_message(self):
        # Display a looping "Waiting..." message until connection is established
        while not self.connection_established:
            sense.show_message("Waiting...", scroll_speed=0.1)

    def connection_check(self):
        # Start the "Waiting..." message in a separate thread
        self.waiting_thread = threading.Thread(target=self.display_waiting_message)
        self.waiting_thread.start()

        message = "False"

        # Check if this machine is CPI or NPI based on IP
        if self.local_ip == RIGHTPI_IP:
            for i in range(2):
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    s.bind((RIGHTPI_IP, PORT))
                    s.listen(1)
                    s.settimeout(2)
                    print(f"Listening for data... attempt {i + 1}")
                    try:
                        client, addr = s.accept()
                        print(f"Got a connection from: {addr}")
                        data = client.recv(1024)
                        message = data.decode()
                        client.close()

                        if message == "True":
                            print("Both machines are synchronized! Starting the game.")
                            self.connection_established = True
                            self.waiting_thread.join()  # Stop the waiting message
                            return
                    except socket.timeout:
                        print("Listening timed out, no connection received.")
                    except socket.error as e:
                        print(f"Listening failed: {e}")

            # If no connection, try to connect as a client
            while not self.connection_established:
                smessage = "True"
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    try:
                        s.connect((LEFTPI_IP, PORT))
                        s.sendall(smessage.encode())
                        print("Message sent to LEFTPI_IP")
                        print("Both machines are synchronized! Starting the game.")
                        self.connection_established = True
                        self.waiting_thread.join()  # Stop the waiting message
                        return
                    except socket.error as e:
                        print(f"Connection to LEFTPI_IP failed: {e}, retrying...")
                    time.sleep(2)

        elif self.local_ip == LEFTPI_IP:
            for i in range(2):
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    s.bind((LEFTPI_IP, PORT))
                    s.listen(1)
                    s.settimeout(2)
                    print(f"Listening for data... attempt {i + 1}")
                    try:
                        client, addr = s.accept()
                        print(f"Got a connection from: {addr}")
                        data = client.recv(1024)
                        message = data.decode()
                        client.close()

                        if message == "True":
                            print("Both machines are synchronized! Starting the game.")
                            self.connection_established = True
                            self.waiting_thread.join()  # Stop the waiting message
                            return
                    except socket.timeout:
                        print("Listening timed out, no connection received.")
                    except socket.error as e:
                        print(f"Listening failed: {e}")

            # If no connection, try to connect as a client
            while not self.connection_established:
                smessage = "True"
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    try:
                        s.connect((RIGHTPI_IP, PORT))
                        s.sendall(smessage.encode())
                        print("Message sent to RIGHTPI_IP")
                        print("Both machines are synchronized! Starting the game.")
                        self.connection_established = True
                        self.waiting_thread.join()  # Stop the waiting message
                        return
                    except socket.error as e:
                        print(f"Connection to RIGHTPI_IP failed: {e}, retrying...")
                    time.sleep(2)

    def run_menu(self):
        self.select_side()  # Select player side

        # If multiplayer mode is selected, wait for opponent connection
        if self.player_side in ['L', 'R']:
            print("Waiting for opponent to be ready...")
            self.connection_check()  # Wait for the connection
            sense.show_message("!!!Ready!!!", scroll_speed=0.1, text_colour=[255, 0, 0])
            self.count_down()
        else:
            # For single-player mode, directly show the start message
            sense.show_message("GO", scroll_speed=0.05, text_colour=[0, 255, 0])
            #self.count_down()
