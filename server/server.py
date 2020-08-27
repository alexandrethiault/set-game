import socket
from _thread import *
import pickle
import time

from game import Game


server = ""
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(4)
print("Server started, waiting for connections")

games = {}
nothing_changed = {}
id_count = 0


def threaded_client(conn, player_number, game_id):
    global id_count
    conn.send(str.encode(str(player_number)))

    while True:
        try:
            data = conn.recv(2048*16).decode()

            if (game_id not in games) or (not data) or (game_id + 10 <= id_count//4 and len(games)>10):
                break
            game = games[game_id]
            if game.ongoing_attack and time.time() - game.attack_time > 3:
                game.stop_attack()
                nothing_changed[game_id] = [False]*4
            elif game.attack_just_ended and time.time() - game.attack_time > 5:
                game.reset_attack()
                nothing_changed[game_id] = [False]*4

            if data == "att":
                game.attempt_attack(player_number)
                nothing_changed[game_id] = [False]*4
            elif data == "mor":
                game.cast_vote(player_number)
                nothing_changed[game_id] = [False]*4
            elif data == "esc":
                conn.sendall(pickle.dumps(game))
                nothing_changed[game_id] = [False]*4
                break
            elif data != "get": # "i,j"
                if game.ongoing_attack and game.attacking_player == player_number:
                    game.attack_click(data)
                    nothing_changed[game_id] = [False]*4

            game.update_time()
            if not nothing_changed[game_id][player_number-1]:
                conn.sendall(pickle.dumps(game))
                nothing_changed[game_id][player_number-1] = True
            elif game.ongoing_attack:
                conn.sendall(pickle.dumps(game.time)) # 12 octets
            else:
                conn.sendall(b'0') # 1 octet
        except:
            break

    print(f"Lost connection to Game {game_id} - Player {player_number}")
    try:
        game.remove_player(player_number)
        if game.no_one_left():
            print(f"Closing Game {game_id}")
            del games[game_id]
            del nothing_changed[game_id]
            conn.close()
            if game_id == id_count // 4:
                id_count = game_id * 4 + 4
    except (UnboundLocalError, KeyError):
        pass


def main():
    global id_count

    while True:
        conn, addr = s.accept()

        player_number = id_count % 4 + 1
        game_id = id_count // 4
        if id_count % 4 == 0:
            games[game_id] = Game(game_id)
            nothing_changed[game_id] = [False]*4
            print(f"Creating Game {game_id}")
        else:
            games[game_id].add_player()
            nothing_changed[game_id] = [False]*4
        print(f"Connected to {addr} as Game {game_id} - Player {player_number}")
        id_count += 1

        start_new_thread(threaded_client, (conn, player_number, game_id))

main()
