from sense_hat import SenseHat
import time
import socket
import os
import threading
import select, sys

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
        
        print("\nSelect your side:")
        print("L or LEFT  - Left player")
        print("R or RIGHT - Right player")
        print("S or DOWN  - Single player")
        print("ENTER or MIDDLE - Confirm selection")

        # Create a thread to handle keyboard input
        def keyboard_input():
            nonlocal selected
            while not selected:
                try:
                    if select.select([sys.stdin], [], [], 0)[0]:  # Check if input available
                        choice = sys.stdin.readline().strip().upper()
                        if choice in ['L', 'LEFT']:
                            self.player_side = 'L'
                            self.start_screen(R=(100, 0, 0), L=(0, 0, 255), S=(100, 100, 100))
                        elif choice in ['R', 'RIGHT']:
                            self.player_side = 'R'
                            self.start_screen(R=(255, 0, 0), L=(0, 0, 100), S=(100, 100, 100))
                        elif choice in ['S', 'DOWN']:
                            self.player_side = 'S'
                            self.start_screen(R=(100, 0, 0), L=(0, 0, 100), S=(255, 255, 255))
                        elif choice == '':  # Enter key
                            if self.player_side != 'X':
                                selected = True
                except:
                    pass
                time.sleep(0.1)

        # Start keyboard input thread
        keyboard_thread = threading.Thread(target=keyboard_input)
        keyboard_thread.daemon = True
        keyboard_thread.start()

        # Handle SenseHAT input (original joystick code)
        while not selected:
            for event in sense.stick.get_events():
                if event.action == 'pressed':
                    if event.direction == 'left':
                        self.player_side = 'L'
                        self.start_screen(R=(100, 0, 0), L=(0, 0, 255), S=(100, 100, 100))
                    elif event.direction == 'right':
                        self.player_side = 'R'
                        self.start_screen(R=(255, 0, 0), L=(0, 0, 100), S=(100, 100, 100))
                    elif event.direction == 'down':
                        self.player_side = 'S'
                        self.start_screen(R=(100, 0, 0), L=(0, 0, 100), S=(255, 255, 255))
                    elif event.direction == 'middle' and self.player_side != 'X':
                        selected = True
                        break

        # Clean up and show selection
        print(f"\nSelected: {self.player_side} player")
        time.sleep(0.5)
        sense.clear()

    def display_waiting_message(self):
        # Create a scrolling "WAIT" pattern
        W = [255, 255, 255]  # White
        O = [0, 0, 0]  # Off
        
        # Make W wider (5x5 pixels)
        W_letter = [
            [W,O,O,O,W],  # W     W
            [W,O,O,O,W],  # W     W
            [W,O,W,O,W],  # W  W  W
            [W,W,O,W,W],  # WW W WW
            [W,O,O,O,W]   # W     W
        ]
        
        A_letter = [
            [W,W,W,W],  # WWWW
            [W,O,O,W],  # W  W
            [W,W,W,W],  # WWWW
            [W,O,O,W],  # W  W
            [W,O,O,W]   # W  W
        ]
        
        I_letter = [
            [W,W,W],   # WWW
            [O,W,O],   #  W
            [O,W,O],   #  W
            [O,W,O],   #  W
            [W,W,W]    # WWW
        ]
        
        T_letter = [
            [W,W,W],   # WWW
            [O,W,O],   #  W
            [O,W,O],   #  W
            [O,W,O],   #  W
            [O,W,O]    #  W
        ]
        
        # Function to draw a letter at a given x position
        def draw_letter(letter, x_pos):
            for y in range(5):
                for x in range(len(letter[0])):
                    if 0 <= x_pos + x < 8:  # Only draw if within screen bounds
                        sense.set_pixel(x_pos + x, y + 1, letter[y][x])
        
        x_pos = 8  # Start off screen
        while not self.connection_established:
            sense.clear()
            
            # Draw "WAIT" with minimal spacing between letters
            if -5 <= x_pos <= 8:
                draw_letter(W_letter, x_pos)
            if -4 <= x_pos + 6 <= 8:
                draw_letter(A_letter, x_pos + 6)
            if -4 <= x_pos + 11 <= 8:
                draw_letter(I_letter, x_pos + 11)
            if -4 <= x_pos + 15 <= 8:  # Adjusted for thinner T
                draw_letter(T_letter, x_pos + 15)
            
            x_pos -= 1  # Move text left
            if x_pos <= -19:  # Adjusted for new total width
                x_pos = 8
            
            if self.connection_established:
                sense.clear()
                return
                
            time.sleep(0.1)  # Control scroll speed

    def connection_check(self):
        self.connection_established = False

        # Check if this machine is CPI or NPI based on IP
        if self.local_ip == RIGHTPI_IP:
            # Try to connect first as client
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((LEFTPI_IP, PORT))
                    s.sendall("CONNECT".encode())
                    print("Connected to first player! Starting game...")
                    self.connection_established = True
                    sense.clear()
                    return
            except socket.error:
                # If connection fails, we're first player - show waiting screen
                self.waiting_thread = threading.Thread(target=self.display_waiting_message)
                self.waiting_thread.daemon = True
                self.waiting_thread.start()

                # Wait for second player
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    s.bind((RIGHTPI_IP, PORT))
                    s.listen(1)
                    client, addr = s.accept()
                    data = client.recv(1024).decode()
                    if data == "CONNECT":
                        print("Second player connected! Starting game...")
                        self.connection_established = True
                        sense.clear()
                        return

        elif self.local_ip == LEFTPI_IP:
            # Try to connect first as client
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((RIGHTPI_IP, PORT))
                    s.sendall("CONNECT".encode())
                    print("Connected to first player! Starting game...")
                    self.connection_established = True
                    sense.clear()
                    return
            except socket.error:
                # If connection fails, we're first player - show waiting screen
                self.waiting_thread = threading.Thread(target=self.display_waiting_message)
                self.waiting_thread.daemon = True
                self.waiting_thread.start()

                # Wait for second player
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    s.bind((LEFTPI_IP, PORT))
                    s.listen(1)
                    client, addr = s.accept()
                    data = client.recv(1024).decode()
                    if data == "CONNECT":
                        print("Second player connected! Starting game...")
                        self.connection_established = True
                        sense.clear()
                        return

    def run_menu(self):
        self.select_side()  # Select player side

        # If multiplayer mode is selected, wait for opponent connection
        if self.player_side in ['L', 'R']:
            print("Waiting for opponent to be ready...")
            self.connection_check()  # Wait for the connection
            
            # Ensure screen is clear
            sense.clear()
            
            # Show ready message
            sense.show_message("Ready!", scroll_speed=0.08, text_colour=[255, 0, 0])
            self.count_down()
        else:
            # For single-player mode
            sense.clear()
            sense.show_message("GO", scroll_speed=0.05, text_colour=[0, 255, 0])
