from Colors import *
import random
import pygame
import time
import os
pygame.init()

screen_width = 1200
screen_height = 700
fps = 50
x = True
rep = None
score = 0
enemy_attr = []
music = {}

images = (
    pygame.image.load("images/bgb.png"),
    random.choice([pygame.image.load("images/ship.png"), pygame.image.load("images/ship1.png")]),
    pygame.image.load("images/bullet.png"),
    pygame.image.load("images/none.png"),
    random.choice([pygame.image.load("images/corona1.png"),
                   pygame.image.load("images/corona3.png"), pygame.image.load("images/corona4.png"),
                   pygame.image.load("images/corona5.png"), pygame.image.load("images/corona6.png")]),
    pygame.image.load("images/start.png"),
    pygame.image.load("images/start1.jpg")
)

music['start'] = pygame.mixer.Sound("music/start.wav")
music['bg'] = pygame.mixer.Sound("music/bg.wav")
music['fire'] = pygame.mixer.Sound("music/fire.wav")
music['blast'] = pygame.mixer.Sound("music/blast.wav")

ship = pygame.transform.scale(pygame.transform.rotate(images[1], 270), (65, 65))
ship_x = (screen_width / 9)
ship_y = (screen_height - ship.get_height()) / 2

bullet_list = []
fired = []

pos = []

gameWindow = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("GoCorona - by Om Londhe")
clock = pygame.time.Clock()


def enemy():
    enemy_x = random.randrange(10, screen_width - 21)
    enemy_y = random.randrange(65, (screen_height - 65))
    img = images[4]
    pos.append([img, enemy_x, enemy_y])
    return pos


def fire():
    bullet = pygame.transform.scale(pygame.transform.rotate(images[2], 45), (75, 75))
    bullet_x = ship_x
    bullet_y = ship_y + (ship.get_height() - ship.get_height() - 4.5)
    bullet_velocity = 25
    bullet_list.append([bullet, bullet_x, bullet_y, bullet_velocity])
    return bullet_list


def check_collision():
    global score
    for i in fired:
        for j in enemy_attr:
            if (abs(j[2] - i[2]) < 15) and (abs(j[2] - i[2]) > 0) and (abs(j[1] < i[1])) and \
                    (abs(j[1] - i[1]) > 0):
                score = score + 1
                music['blast'].play()
                enemy_attr.remove(j)
                fired.remove(i)


def show_text(text, color, x, y):
    txt = font.render(text, True, color)
    gameWindow.blit(txt, (x, y))


if not os.path.exists("hs.txt"):
    with open("hs.txt", 'w') as hs:
        hs.write("0")

with open("hs.txt", 'r') as hs:
    h_score = hs.read()


font = pygame.font.SysFont(None, 51)
exit_game = False


def start():
    music['start'].play()
    global exit_game
    while not exit_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN or (event.type == pygame.MOUSEBUTTONDOWN):
                mainloop()
        gameWindow.blit(pygame.transform.scale(images[0], (screen_width, screen_height)).convert_alpha(), (0, 0))
        gameWindow.blit(ship, (ship_x, ship_y))
        gameWindow.blit(images[5], (700, 0))
        gameWindow.blit(pygame.transform.scale(images[6], (250, 250)).convert_alpha(), (0, 0))
        start_font = pygame.font.SysFont(None, 75)
        start_text = start_font.render("Press Any Key to Stop Coronavirus !!!", True,
                                       random.choice([white, black, brown, yellow, green, red, orange, purple]))
        gameWindow.blit(start_text, (150, 500))
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()


def mainloop():
    music['bg'].play()
    global ship_x, ship_y, fired, h_score, rep, enemy_attr, exit_game
    enemy_attr = enemy()
    difficulty = 5

    while not exit_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    fired = fire()
                    music['fire'].play()

        key_hold = pygame.key.get_pressed()
        if key_hold[pygame.K_UP] or key_hold[pygame.K_w]:
            if not ship_y <= 60:
                ship_y = ship_y - 9
        if key_hold[pygame.K_DOWN] or key_hold[pygame.K_s]:
            if not ship_y >= screen_height - 80:
                ship_y = ship_y + 9
        if key_hold[pygame.K_a] or key_hold[pygame.K_LEFT]:
            if not ship_x <= 10:
                ship_x = ship_x - 9
        if key_hold[pygame.K_d] or key_hold[pygame.K_RIGHT]:
            if not ship_x >= (screen_width - ship.get_width() - 10):
                ship_x = ship_x + 9

        gameWindow.blit(pygame.transform.scale(images[0], (screen_width, screen_height)).convert_alpha(), (0, 0))
        for bullet in fired:
            bullet[1] = bullet[1] + bullet[3]
            gameWindow.blit(bullet[0], (bullet[1], bullet[2]))
            check_collision()
            if bullet[1] >= screen_width:
                fired.remove(bullet)
        gameWindow.blit(ship, (ship_x, ship_y))

        for enemy_details in enemy_attr:
            gameWindow.blit(pygame.transform.scale(enemy_details[0], (60, 60)), (enemy_details[1], enemy_details[2]))
            if enemy_details[1] < -65:
                enemy_attr.remove(enemy_details)

        timer = time.clock()
        if int(timer % difficulty) == 0 and (rep != int(timer)):
            enemy_attr = enemy()
            for enemy_details in enemy_attr:
                gameWindow.blit(pygame.transform.scale(enemy_details[0], (60, 60)), (enemy_details[1], enemy_details[2]))
                rep = int(timer)

        if int(timer % 75) == 0 and int(timer) != 0 and difficulty != 1:
            difficulty = random.randrange(1, 5)

        if int(h_score) <= score:
            h_score = score
            with open("hs.txt", 'w') as hs:
                hs.write(str(h_score))

        show_text(f"Score: {score}", white, 5, 5)
        show_text(f"High-Score {h_score}", white, 900, 5)
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()


start()
