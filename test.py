import socket, time,os, random, Send, Listen
import os



class test:
    def __init__(self):

        ip1 = "10.41.10.68"
        ip2 = "10.41.10.51"


        i = input("S or L: ").upper()

        if i == "S":
            while i != "Q":
                message = input("input data: ")
                self.send = Send.Send(message,(ip2,1777))
                time.sleep(1)
                received_data = None
                while received_data is None:
                    self.listen = Listen.Server((ip1, 1888), 1)
                    received_data = self.listen.WaitForConnection()
                data = received_data
                print(data)





        elif i == "L":
            received_data = None
            while received_data is None:
                self.listen = Listen.Server((ip2, 1777), 1)
                received_data = self.listen.WaitForConnection()
                data = received_data



                while i != "Q":

                    position = data[2:6]
                    velocity = data[10:14]
                    sleep_time = data[17:20]

                    print(f"position:{position}  velocity:{velocity}  sleep time:{sleep_time}")


                    message = input("type y to send: ").upper()
                    if message == "Y":
                        ball_data = [
                            (0,3),
                            (1, 1),
                            sleep_time
                        ]
                        self.send = Send.Send(str(ball_data),(ip1, 1888))
                        time.sleep(1)
                        received_data = None
                        break




test()






































