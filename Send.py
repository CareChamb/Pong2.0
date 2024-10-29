import socket, time,os, random


class Send():
   def __init__(self, message="DATA", address=("10.41.10.51", 1777)):
       self.message = message
       self.address = address
       self.s = socket.socket()
       self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
       self.s.connect(address)
       self.send_data()

   def send_data(self):

      self.s.sendall(self.message.encode())
      print("Sent data.")
      self.s.close()