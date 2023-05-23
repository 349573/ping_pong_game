import sys
import pygame as pg


def ball_move(obj):
    global speed_x, speed_y
    obj.x += speed_x
    obj.y += speed_y

    if obj.top <= 0 or obj.bottom >= H:
        speed_y *= -1
    elif obj.left <= 0 or obj.right >= W:
        speed_x *= -1
    elif obj.colliderect(player) or obj.colliderect(opponent):
        speed_x *= -1

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
o_speed = 0
ball_moving = False
speed_x = speed_y = speed


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
    pg.display.update()

    ball_move(ball)