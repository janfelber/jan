import math
import random

import pygame
from pygame import mixer

# Intialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800,600))

# Background
background = pygame.image.load('background.png')

# Sound
mixer.music.load("back.mp3")
mixer.music.play(-1)

# Caption and Icon
pygame.display.set_caption("Star Wars")
icon = pygame.image.load('logo.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 5

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('sith-enemy.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# Rocket
rocketImg = pygame.image.load('missile.png')
rocketX = 0
rocketY = 480
rocketX_change = 4
rocketY_change = 10
rocket_state = "ready"  # cant see the bullet on screen

# Score

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
testY = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_rocket(x, y):
    global rocket_state
    rocket_state = "fire"
    screen.blit(rocketImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, rocketX, rocketY):
    distance = math.sqrt((math.pow(enemyX - rocketX, 2)) + (math.pow(enemyY - rocketY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game loop
running = True
while running:

    screen.fill((0, 0, 0))
    # background image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if rocket_state == "ready":
                    rocket_Sound = mixer.Sound('blaster.wav')
                    rocket_Sound.play()
                    # Aby missile neprenasledovala raketu, nastavenie ze rocketX ma brat ako keby bol player X, vsetko co obsahuje playerX a je to spolu s missile treba vymenit za rocketX
                    rocketX = playerX
                    fire_rocket(rocketX, rocketY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # 5 = 5 + -0.1 -> 5 = 5 - 0.1
    # 5 = 5 + 0.1

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy Movement
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 430:
            mixer.music.load("back.mp3")
            mixer.music.stop()
            gameoverSound = mixer.Sound("GameOver.wav")
            gameoverSound.play(0)

            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], rocketX, rocketY)
        if collision:
            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.play()
            rocketY = 480
            rocket_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Rocket Movement
    if rocketY <= 0:
        rocketY = 480
        rocket_state = "ready"

    if rocket_state == "fire":
        fire_rocket(rocketX, rocketY)
        rocketY -= rocketY_change


    player(playerX, playerY)
    show_score(textX, testY)
    pygame.display.update()