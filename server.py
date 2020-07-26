import socket
from _thread import *
import pickle
from game import Game
import time

server = ""
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(4)
print("Waiting for a connection, Server Started")

connected = set()
games = {}
id_count = 0


def threaded_client(conn, player_number, game_id):
    global id_count
    conn.send(str.encode(str(player_number)))

    while True:
        try:
            data = conn.recv(2048*16).decode()

            if game_id not in games or not data:
                break
            game = games[game_id]
            if game.ongoing_attack and time.time() - game.attack_time > 3:
                game.stop_attack()
            elif game.attack_just_ended and time.time() - game.attack_time > 5:
                game.reset_attack()

            if data == "att":
                game.attempt_attack(player_number)
            elif data == "mor":
                game.cast_vote(player_number)
            elif data != "get":
                game.attack_click(data)

            game.time = time.time()
            conn.sendall(pickle.dumps(game))
        except:
            break

    print("Lost connection")
    try:
        print("Closing Game", game_id)
        del games[game_id]
    except KeyError:
        pass
    id_count -= 1
    conn.close()



while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    id_count += 1
    player_number = (id_count-1) % 4 + 1
    game_id = (id_count - 1) // 4
    if id_count % 4 == 1:
        games[game_id] = Game(game_id)
        print("Creating a new game...")
    else:
        games[game_id].ready = True
        games[game_id].players += 1


    start_new_thread(threaded_client, (conn, player_number, game_id))