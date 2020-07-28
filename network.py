import socket
import pickle


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            with open("ip.txt", "r") as f:
                self.client.connect((f.read(), 5555))
            player_number = self.client.recv(2048*16).decode()
            assert player_number
            self.__player_number = player_number
        except (AssertionError, socket.error) as e:
            print(e)
            raise

    @property
    def player_number(self):
        return self.__player_number

    def send(self, data):
        try:
            self.client.send(str.encode(data)) #send data from client to server
            return pickle.loads(self.client.recv(2048*16)) # return to client an updated version of game
        except socket.error as e:
            print(e)