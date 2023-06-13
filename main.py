import sys
import pygame as pg
from random import choice


def ball_start(obj):
    global speed_x, speed_y, ball_moving, score_time
    obj.center = (W // 2, H // 2)
    speed_x *= choice([-1, 1])
    speed_y *= choice ([-1, 1])

    cur_time = pg.time.get_ticks()

    if cur_time - score_time < 700:
        num_3 = score_font.render('3', True, VIOLET)
        screen.blit(num_3, [W // 2, H // 2])
    elif cur_time - score_time < 1400:
        num_3 = score_font.render('2', True, VIOLET)
        screen.blit(num_3, [W // 2, H // 2])
    elif cur_time - score_time < 2100:
        num_3 = score_font.render('1', True, VIOLET)
        screen.blit(num_3, [W // 2, H // 2])

    if cur_time - score_time < 2100:
        speed_x, speed_y = 0, 0
    else:
        speed_x = speed * choice ([-1, 1])
        speed_y = speed * choice ([-1, 1])
        score_time = None

def ball_move(obj):
    global speed_x, speed_y, player_score, opponent_score, score_time
    obj.x += speed_x
    obj.y += speed_y

    if obj.top <= 0 or obj.bottom >= H:
        speed_y *= -1
        pg.mixer.Sound.play(pong_sound)
    elif obj.left <= 0:
        score_time = pg.time.get_ticks()
        player_score += 1
        pg.mixer.Sound.play(score_sound)
    elif obj.right >= W:
        score_time = pg.time.get_ticks()
        opponent_score += 1
        pg.mixer.Sound.play(score_sound)
    if obj.colliderect(player):
        pg.mixer.Sound.play(pong_sound)
        if abs(obj.right - player.left) < 10:
            speed_x *=-1
        elif abs(obj.bottom - player.left) < 10 or abs(obj.top - player.bottom) < 10:
            speed_x *=-1
    elif obj.colliderect(opponent):
        pg.mixer.Sound.play(pong_sound)
        if abs(obj.left - opponent.right) < 10:
            speed_x *= -1
        elif abs(obj.bottom - opponent.top) < 10 or abs(obj.top - opponent.bottom) < 10:
            speed_x *= -1

def player_motion(obj, s):
    obj.y += s

    if obj.top <= 0:  # если ракетка упирается в верхнюю границу экрана
        obj.top = 0  # она блокируется
    elif obj.bottom >= H:
        obj.bottom = H


def opponent_motion(obj, p_obj, s):
    if obj.top < p_obj.y:  # если мяч выше верхней границы ракетки оппонента
        obj.y += s  # ракетка поднимается за мячом
    elif obj.bottom > p_obj.y:
        obj.y -= s

    if obj.top <= 0:
        obj.top = 0
    elif obj.bottom >= H:
        obj.bottom = H

W = 1280
H = 720
FPS = 60
clock = pg.time.Clock()

# COLORS
GRAY = (230, 230, 230)
WHITE = (255, 255, 255)
VIOLET = (230, 61, 245)


speed = 7
p_speed = 0
o_speed = 5.5
ball_moving = False
score_time = True
speed_x = speed * choice([-1, 1])
speed_y = speed * choice([-1, 1])

pg.mixer.init()
pong_sound = pg.mixer.Sound('hit.mp3')
score_sound = pg.mixer.Sound('lose.wav')
pong_sound.set_volume(0.2)
score_sound.set_volume(0.1)


player_score, opponent_score =0, 0
pg.font.init()
score_font = pg.font.SysFont('comicsans', 64)

pg.init()  # инициализируем pygame
screen = pg.display.set_mode((W, H))  # создаем экран игры разрешением 1280х720px
pg.display.set_caption('Ping Pong | PyGame')

player_img = pg.image.load('paddle.jpg').convert()
opponent_img = pg.image.load('paddle.jpg').convert()

ball_img = pg.image.load('tennis.png').convert_alpha()
ball_img = pg.transform.scale(ball_img, (50, 50)).convert_alpha()

player = player_img.get_rect()
opponent =opponent_img.get_rect()
ball = ball_img.get_rect()
player.x, player.y = W - 30, H // 2

while True:  # цикл игры
    clock.tick(FPS)
    for event in pg.event.get():  # обработчик событий pygame
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

    screen.fill(GRAY)
    pg.draw.aaline(screen, WHITE, [W // 2, 0], [W // 2, H])
    player_score_text = score_font.render(str(player_score), True, VIOLET)
    screen.blit(player_score_text, [W // 2 + 50, H * 0.25])
    screen.blit(player_img, player)
    screen.blit(opponent_img, opponent)
    screen.blit(ball_img, ball)

    opponent_score_text = score_font.render(str(opponent_score), True, VIOLET)
    screen.blit (opponent_score_text, [W // 2 - 100, H * 0.25])
    pg.display.update()

    if score_time:
        ball_start(ball)


    pg.display.update()


    keys = pg.key.get_pressed()
    if keys[pg.K_UP]:
        p_speed -= speed
    elif keys[pg.K_DOWN]:
        p_speed += speed
    else:
        p_speed = 0


    ball_move(ball)
    player_motion(player, p_speed)
    opponent_motion(opponent, ball, o_speed)
