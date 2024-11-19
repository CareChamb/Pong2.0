import socket

class Send():
    def __init__(self, message="DATA", address=("10.41.10.52", 1777)):  # Set to the correct receiving address
        self.message = message
        self.address = address
        self.s = socket.socket()
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self.s.connect(address)
            self.send_data()
        except socket.error as e:
            print(f"Connection error: {e}")

    def send_data(self):
        self.s.sendall(self.message.encode())
        print("Sent data.")
        self.s.close()
