import os
import socket
import pickle


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ippath = "ip.txt"
        if not os.path.isfile(ippath): ippath = "../" + ippath
        with open(ippath, "r") as f:
            self.client.connect((f.read(), 5555))
        self.client.send(str.encode("Hi!")) #discard connections that don't say hi
        player_number = self.client.recv(2048*16).decode()
        assert player_number
        self.__player_number = player_number

    @property
    def player_number(self):
        return self.__player_number

    def send(self, data):
        self.client.send(str.encode(data)) #send data from client to server
        try:
            return pickle.loads(self.client.recv(2048*16)) # return to client an updated version of game
        except pickle.UnpicklingError:
            return b'0'
