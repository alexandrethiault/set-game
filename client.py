import pygame
from network import Network
import os

pygame.font.init()

width = 600
height = 600
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Set! (Chargement...)")

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

cards = [[CardSlot(65 + 80*((j+1)%6), 50 + 120*i) for j in range(6)] for i in range(3)]

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
    if not game.ready:
        message_display("En attente d'un\nadversaire...", 60)
    else:
        if game.ongoing_attack:
            xc = width // 2 - (game.players - 1) * 60 + (game.attacking_player - 1) * 120
            remaining_time = round(3. - (game.time - game.attack_time), 1)
            text=f"SET! {remaining_time}"
            message_display(text, 20, xc, yc=500, color=(0, 255,255))
        elif game.attack_just_ended:
            xc = width // 2 - (game.players - 1) * 60 + (game.attacking_player - 1) * 120
            delay = 500
            color = (0, 255, 0)
            if game.attack_success:
                if game.attacking_player == player:
                    text = "Bravo !\n+1 point"
                else:
                    text = f"+1 point"
            else:
                color = (255, 0, 0)
                if game.attacking_player == player:
                    text = "Raté !\n-1 point..."
                else:
                    text = f"-1 point"
            message_display(text, 20, xc, 500, color)

        for i in range(3):
            for j in range(6):
                card = cards[i][j]
                card.abcd = game.cards_abcds[i][j]
                card.draw()

        x = width // 2 - (game.players-1) * 60
        for i in range(1, game.players+1):
            message_display(f"Joueur {i}", 20, x, 450, (0, 0, 0))
            message_display(f"{game.sets[i]}", 20, x, 475, (0, 255, 0))
            if game.penalties[i]: message_display(f" -{game.penalties[i]}", 20, x+15, 475, (255, 0, 0))
            x += 120

    pygame.display.update()
    pygame.time.delay(delay)

def main():
    run = True
    clock = pygame.time.Clock()
    try:
        n = Network()
    except:
        return 1
    player = int(n.player_number)
    print("You are player", player)
    pygame.display.set_caption(f"Set! (Joueur {player})")
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
                elif event.key in (pygame.K_BACKSPACE, pygame.K_RETURN, pygame.K_5, pygame.K_p, pygame.K_LEFTPAREN):
                    game = n.send("mor")
                elif event.key == pygame.K_ESCAPE:
                    game = n.send("esc")
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for i in range(3):
                    for j in range(6):
                        card = cards[i][j]
                        if card.click(pos) and game.ready:
                            n.send(f"{i},{j}") # ne marche que si c'est ce client qui attaque

        redrawWindow(game, player)
    return 0

def menu_screen(code):
    run = True
    clock = pygame.time.Clock()
    pygame.display.set_caption("Set! (Non connecté)")

    while run:
        clock.tick(60)
        win.fill((128, 128, 128))
        if code==0:
            text = "Cliquer pour\nse connecter !"
        else:
            text = "La connexion\na écoué...\nCliquer pour\nretenter de\nse connecter."
        message_display(text, 60, color=(255, 0, 0))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                win.fill((128, 128, 128))
                text = "Tentative de\n connexion..."
                message_display(text, 60, color=(255, 0, 0))
                pygame.display.update()
                run = False

    return main()

_code = 0
while True:
    _code = menu_screen(_code)