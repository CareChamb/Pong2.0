import socket

class Server():
    def __init__(self, address=('10.41.10.51', 1777), MaxClient=1):
        self.s = socket.socket()
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind(address)
        self.s.listen(MaxClient)

    def WaitForConnection(self):
        print("listening for data...")
        self.Client, self.Adr = self.s.accept()
        print(f'Got a connection from: {str(self.Adr)}')
        return self.receive_data()

    def receive_data(self):
        data = self.Client.recv(1777)  # Receive the data from the client
        decoded_data = data.decode()

        print(f"Received data: {decoded_data}")

        # Close the client connection
        self.Client.close()
        self.stop_server()
        return decoded_data

    def stop_server(self):
        print("stopped listening")
        self.s.close()
