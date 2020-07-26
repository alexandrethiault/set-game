import pygame
from network import Network
import os
import time
import pickle
pygame.font.init()

width = 600
height = 600
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")

images = {}
for name in os.listdir("./images"):
    if name.endswith(".png"):
        image = pygame.image.load(f"./images/{name}").convert_alpha()
        rect = image.get_rect()
        image = pygame.transform.scale(image, (rect.w//10, rect.h//10))
        images[name[-8:-4]] = image
        print(name)

class CardSlot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.abcd = "0000"
        self.width = 70
        self.height = 110

    def draw(self):
        if self.abcd != "0000":
            win.blit(images[self.abcd], (self.x, self.y))

    def click(self, pos):
        x, y = pos
        return self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height

cards = [[CardSlot(50 + 80*j, 50 + 120*i) for j in range(27)] for i in range(3)]

def message_display(text, size, xc=width//2, yc=height//2, color=(0,0,0)):
    lines = text.split("\n")
    y = yc - (len(lines)-1)*size//2
    font = pygame.font.SysFont("comicsansms", size)
    for line in lines:
        surface = font.render(line, True, color)
        rectangle = surface.get_rect()
        rectangle.center = (xc, y)
        win.blit(surface, rectangle)
        y += size

def redrawWindow(game, player):
    win.fill((250, 243, 152))
    delay = 0
    if not(game.connected()):
        message_display("En attente d'un\nadversaire...", 60)
    else:
        if game.ongoing_attack:
            remaining_time = round(3. - (game.time - game.attack_time), 1)
            if game.attacking_player == player:
                text=f"SET! {remaining_time}"
            else:
                text=f"Joueur {game.attacking_player} : SET! {remaining_time}"
        elif game.attack_just_ended:
            delay = 500
            if game.attack_success:
                if game.attacking_player == player:
                    text = "Bravo ! +1 point"
                else:
                    text = f"1 point pour\nle joueur {game.attacking_player}..."
            else:
                if game.attacking_player == player:
                    text = "Raté ! -1 point..."
                else:
                    text = f"Raté ! -1 point pour\nle joueur {game.attacking_player}"
        else:
            text = ""
        message_display(text, 60, yc=500, color=(0, 255,255))

        for i in range(3):
            for j in range(27):
                card = cards[i][j]
                card.abcd = game.cards_abcds[i][j]
                card.draw()

    pygame.display.update()
    pygame.time.delay(delay)



def main():
    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = int(n.player_number)
    print("You are player", player)

    while run:
        clock.tick(60)
        try:
            game = n.send("get")
            """
            game in client.py will always be a copy of the only game that matters, stored
            in server.py. That copy can lag behind the main one and sending an attack can be
            refused if it appears the copy didn't register another player's attack that came
            before.
            """
        except:
            run = False
            print("Couldn't get game")
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    game = n.send("att") # attempt attack
                elif event.key in (pygame.K_BACKSPACE, pygame.K_5, pygame.K_LEFTPAREN):
                    game = n.send("mor")

            if event.type == pygame.MOUSEBUTTONDOWN and game.attacking_player == player:
                pos = pygame.mouse.get_pos()
                for i in range(3):
                    for j in range(27):
                        card = cards[i][j]
                        if card.click(pos) and game.connected():
                            n.send(f"{i},{j}")

        redrawWindow(game, player)

def menu_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        win.fill((128, 128, 128))
        message_display("Cliquer pour\nse connecter !", 60, color=(255, 0, 0))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False

    main()

while True:
    menu_screen()