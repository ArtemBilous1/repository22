import pygame
import cv2
import numpy as np
import random

#  Pygame
pygame.init()

#  параметри екрану
win = pygame.display.set_mode((1200, 720))
pygame.display.set_caption("Spaceship Game")

# зображення
player = pygame.image.load("spaceship.png")
player = pygame.transform.scale(player, (50, 50))
bg = pygame.image.load("kosmos.jpg")
bg = pygame.transform.scale(bg, (1200, 720))
meteor_img = pygame.image.load("meteor.png")
meteor_img = pygame.transform.scale(meteor_img, (50, 50))
enemy_img = pygame.image.load("enemy.png")
enemy_img = pygame.transform.scale(enemy_img, (50, 50))
bullet_img = pygame.image.load("bullet.png")
bullet_img = pygame.transform.scale(bullet_img, (10, 30))

#координати гравця
x, y = (1200 // 2) - (50 // 2), (720 // 2) - (50 // 2)
speed = 5

# метеорити
meteors = []
for _ in range(5):
    meteor_x = random.randint(0, 1150)
    meteor_y = random.randint(-150, -50)
    meteors.append([meteor_x, meteor_y])

meteor_speed = 3

# вороги
enemies = []
for _ in range(5):
    enemy_x = random.randint(0, 1150)
    enemy_y = random.randint(-150, -50)
    enemies.append([enemy_x, enemy_y])

enemy_speed = 2

# кулі від кораблю
bullets = []
bullet_speed = 7

# лічильник
score = 0

# таймер для ракет
last_bullet_time = 0
bullet_cooldown = 1000  

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def main_menu():
    cap = cv2.VideoCapture('space_video.mp4')
    font = pygame.font.SysFont("comicsans", 50)
    button_font = pygame.font.SysFont("comicsans", 30)
    credit_font = pygame.font.SysFont("comicsans", 20)
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos):
                    run = False
                    game_loop()
                if exit_button.collidepoint(event.pos):
                    pygame.quit()
                    quit()

        ret, frame = cap.read()
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = cap.read()

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = np.rot90(frame)
        frame = pygame.surfarray.make_surface(frame)
        frame = pygame.transform.scale(frame, (1200, 720))

        win.blit(frame, (0, 0))

        play_button = pygame.Rect(500, 300, 200, 50)
        pygame.draw.rect(win, (0, 128, 0), play_button)
        draw_text('Play', button_font, (255, 255, 255), win, 570, 310)

        exit_button = pygame.Rect(500, 400, 200, 50)
        pygame.draw.rect(win, (128, 0, 0), exit_button)
        draw_text('Exit', button_font, (255, 255, 255), win, 570, 410)

        draw_text('made by Artem Bilous', credit_font, (255, 255, 255), win, 10, 690)

        pygame.display.update()

    cap.release()

def game_loop():
    global x, y, score, last_bullet_time
    run = True
    credit_font = pygame.font.SysFont("comicsans", 20)
    score_font = pygame.font.SysFont("comicsans", 30)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and x > 0:
            x -= speed
        if keys[pygame.K_RIGHT] and x < 1150:
            x += speed
        if keys[pygame.K_UP] and y > 0:
            y -= speed
        if keys[pygame.K_DOWN] and y < 670:
            y += speed

        # випуск куль кд 1сек
        current_time = pygame.time.get_ticks()
        if keys[pygame.K_SPACE] and current_time - last_bullet_time > bullet_cooldown:
            bullets.append([x + 20, y])
            last_bullet_time = current_time

        for enemy in enemies:
            enemy[1] += enemy_speed
            if enemy[1] > 720:
                enemy[0] = random.randint(0, 1150)
                enemy[1] = random.randint(-150, -50)

        for meteor in meteors:
            meteor[1] += meteor_speed
            if meteor[1] > 720:
                meteor[0] = random.randint(0, 1150)
                meteor[1] = random.randint(-150, -50)

        for bullet in bullets:
            bullet[1] -= bullet_speed
            if bullet[1] < 0:
                bullets.remove(bullet)

        win.blit(bg, (0, 0))
        win.blit(player, (x, y))

        for enemy in enemies:
            win.blit(enemy_img, (enemy[0], enemy[1]))

        for meteor in meteors:
            win.blit(meteor_img, (meteor[0], meteor[1]))

        for bullet in bullets:
            win.blit(bullet_img, (bullet[0], bullet[1]))

        draw_text('made by Artem Bilous', credit_font, (255, 255, 255), win, 10, 690)
        draw_text(f'Score: {score}', score_font, (255, 255, 255), win, 10, 10)

        pygame.display.update()

        # зіткнення з ворогами
        player_rect = pygame.Rect(x, y, 50, 50)
        for enemy in enemies:
            enemy_rect = pygame.Rect(enemy[0], enemy[1], 50, 50)
            if player_rect.colliderect(enemy_rect):
                run = False

        #  зіткнення з метеоритами
        for meteor in meteors:
            meteor_rect = pygame.Rect(meteor[0], meteor[1], 50, 50)
            if player_rect.colliderect(meteor_rect):
                run = False

        #  зіткнення куль з ворогами
        for bullet in bullets:
            bullet_rect = pygame.Rect(bullet[0], bullet[1], 10, 30)
            for enemy in enemies:
                enemy_rect = pygame.Rect(enemy[0], enemy[1], 50, 50)
                if bullet_rect.colliderect(enemy_rect):
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    enemies.append([random.randint(0, 1150), random.randint(-150, -50)])
                    score += 1
                    break

        pygame.time.delay(10)

    pygame.quit()

main_menu()
