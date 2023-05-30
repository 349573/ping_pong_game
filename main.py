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
    elif obj.left <= 0:
        score_time = pg.time.get_ticks()
        player_score += -1
    elif obj.right >= W:
        score_time = pg.time.get_ticks()
        opponent_score += 1
    elif obj.colliderect(player) or obj.colliderect(opponent):
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

# игровые сущности
player = pg.Rect(W - 20, H // 2, 10, 150)
opponent = pg.Rect(10, H // 2, 10, 150)
ball = pg.Rect(W // 2 - 15, H // 2 - 15, 30, 30)


speed = 7
p_speed = 0
o_speed = speed
ball_moving = False
score_time = True
speed_x = speed * choice([-1, 1])
speed_y = speed * choice([-1, 1])



player_score, opponent_score =0, 0
pg.font.init()
score_font = pg.font.SysFont('comicsans', 64)

pg.init()  # инициализируем pygame
screen = pg.display.set_mode((W, H))  # создаем экран игры разрешением 1280х720px
pg.display.set_caption('Ping Pong | PyGame')

while True:  # цикл игры
    clock.tick(FPS)
    for event in pg.event.get():  # обработчик событий pygame
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

    screen.fill(GRAY)
    pg.draw.rect(screen, VIOLET, player)
    pg.draw.rect(screen, VIOLET, opponent)
    pg.draw.aaline(screen, WHITE, [W // 2, 0], [W // 2, H])
    pg.draw.ellipse(screen, VIOLET, ball)
    player_score_text = score_font.render(str(player_score), True, VIOLET)
    screen.blit(player_score_text, [W // 2 + 50, H * 0.25])


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
