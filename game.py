import time
import random

# Jeu Set!
class Game:
    def __init__(self, _id):
        self.ready = False
        self.id = _id
        self.sets = [0.5,0,0,0,0] # Joueur 0 gagne sur joueurs non existants
        self.penalties = [0,0,0,0,0]
        self.attack_time = 0
        self.time = 0
        self.ongoing_attack = False
        self.attack_just_ended = False
        self.attack_success = False
        self.attacking_player = 0
        self.selected_ij = []
        self.selected_set = []
        self.cards_abcds = [["0000" for _ in range(6)] for _ in range(3)]
        self.available_abcds = [str(((10*a+b)*10+c)*10+d) for a in range(1,4) for b in range(1,4)
                                                            for c in range(1,4) for d in range(1,4)]
        self.visible_cards = 12
        for i in range(3):
            for j in range(4):
                abcd = random.choice(self.available_abcds)
                self.cards_abcds[i][j] = abcd
                self.available_abcds.remove(abcd)
        self.players = 1
        self.left = 0
        self.no_set_votes = [False]*5

    def add_player(self):
        self.ready = True
        self.players += 1

    def remove_player(self, player):
        self.left += 1
        self.no_set_votes[player] = False

    def no_one_left(self):
        return self.players <= self.left

    def update_time(self):
        self.time = time.time()

    def cast_vote(self, player):
        self.no_set_votes[player] = True
        if self.no_set_votes.count(True) == self.players - self.left:
            if not self.available_abcds:
                self.end_game()
                return
            if self.visible_cards == 18:
                self.no_set_votes = [False]*5
                return
            i = j = 0
            added = 0
            while self.available_abcds and added < 3:
                if self.cards_abcds[i][j] == "0000":
                    abcd = random.choice(self.available_abcds)
                    self.cards_abcds[i][j] = abcd
                    self.available_abcds.remove(abcd)
                    self.visible_cards += 1
                    added += 1
                i += 1
                if i == 3:
                    i = 0
                    j += 1
            self.no_set_votes = [False]*5

    def attempt_attack(self, player):
        if not self.ongoing_attack:
            self.stop_attack()
            self.ongoing_attack = True
            self.attack_just_ended = False
            self.attacking_player = player
            self.attack_time = time.time()

    def attack_succeeded(self):
        if len(self.selected_set) < 3 or "0000" in self.selected_set:
            return False
        abcd1, abcd2, abcd3 = self.selected_set
        for i in range(4):
            if (int(abcd1[i])+int(abcd2[i])+int(abcd3[i])) % 3:
                return False
        return True

    def get_attack_clicks(self):
        return self.selected_set[:]

    def attack_click(self, data):
        if len(self.selected_set) == 3: return
        i, j = int(data[0]), int(data[2])
        abcd = self.cards_abcds[i][j]
        if abcd == "0000" or abcd in self.selected_set: return
        self.selected_ij.append((i,j))
        self.selected_set.append(self.cards_abcds[i][j])

    def winners(self):
        scores = [self.sets[i]-self.penalties[i] for i in range(5)]
        maxscores = max(scores)
        return [i for i in range(1, 5) if scores[i] == maxscores]

    def end_game(self):
        print("winners:", self.winners())

    def stop_attack(self):
        self.ongoing_attack = False
        self.attack_just_ended = True
        self.attack_success = self.attack_succeeded()
        if self.attack_success:
            self.sets[self.attacking_player] += 1
            for i, j in self.selected_ij:
                self.cards_abcds[i][j] = "0000"
            self.visible_cards -= 3
            i = j = 0
            while self.available_abcds and self.visible_cards < 12:
                if self.cards_abcds[i][j] == "0000":
                    abcd = random.choice(self.available_abcds)
                    self.cards_abcds[i][j] = abcd
                    self.available_abcds.remove(abcd)
                    self.visible_cards += 1
                i += 1
                if i == 3:
                    i = 0
                    j += 1
            self.no_set_votes = [False] * 5
        else:
            self.penalties[self.attacking_player] += 1
        self.selected_set = []
        self.selected_ij = []

    def reset_attack(self):
        self.attack_just_ended = False
        self.attacking_player = 0
        self.attack_time = 0
        self.attack_success = False