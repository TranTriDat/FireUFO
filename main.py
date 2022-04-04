import pygame
import math
import random
from pygame import mixer

# Intialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800,600))

# Background
background = pygame.image.load("background.png")

# Background Sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# Caption and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load("player.png")
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

# Enemy
EnemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 10

for i in range(num_of_enemies):
    EnemyImg.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(3)
    enemyY_change.append(40)

# Bullet

# Ready - You cant see the bullet on the screen
# Fire - The bullet is currently moving
BulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 0
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)

textX = 10
textY = 10

# Game Over Text
over_font = pygame.font.Font("freesansbold.ttf", 64)

def show_score(x, y):
    score = font.render("Score : "+str(score_value), True, (255,255,255))
    screen.blit(score, (x,y))

def player(x,y):
    screen.blit(playerImg, (x,y))

def game_over_text():
    over_text = over_font.render("Game Over", True, (255,255,255))
    screen.blit(over_text, (200, 250 ))

def enemy(x, y, i):
    screen.blit(EnemyImg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(BulletImg, (x+16, y+10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    return False

# Game Loop
running = True
while running:

    # RGB = Red - Green - Blue
    screen.fill((0,0,0))

    # Background Image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystoke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change -= 5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5

            if event.key == pygame.K_UP:
                playerY_change -= 5
            if event.key == pygame.K_DOWN:
                playerY_change = 5

            if event.key == pygame.K_x:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bulletX = playerX
                    bulletY = playerY
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerX_change = 0.0
                playerY_change = 0.0

    # Checking for boundaries of spaceship so it doesnt go out of bound
    playerX += playerX_change
    playerY += playerY_change

    if playerX <= 0 :
        playerX = 0
    elif playerX >= 736 :
        playerX = 736

    if playerY <= 0:
        playerY = 0
    elif playerY > 530:
        playerY = 530

    # Enemy movement
    for i in range(num_of_enemies):
        # Game Over
        if enemyY[i] > 580:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        # enemyY[i] += enemyY_change[i]

        if enemyX[i] <= 0 :
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736 :
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        # if enemyY[i] <= 0:
        #     enemyY_change[i] = 4
        # elif enemyY[i] > 530:
        #     enemyY_change[i] = -4

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            # print(score)
            enemyX[i] = random.randint(0,735)
            enemyY[i] = random.randint(50,150)
        enemy(enemyX[i], enemyY[i], i)


    # Bullet Movement
    if bulletY <= 0 :
        bulletY = 0
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
