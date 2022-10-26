import pygame
import random
import math
import time

pi = 3.1415

max_x = 265
max_y = 400
min_x = 0
min_y = 0

ball_count = 10


def distance(xa, ya, xb, yb):
    i = math.sqrt(math.pow(xa - xb, 2) + math.pow(ya - yb, 2))
    return i


def clamp(value, lower, upper):
    return lower if value < lower else upper if value > upper else value


def opposite_rgb(r, g, b):
    return 255 - r, 255 - g, 255 - b


class Ball:
    global max_x, max_y, min_x, min_y

    def random_velocity(self):
        self.xVelocity = random.uniform(-50, 50)
        self.yVelocity = random.uniform(-50, 50)

    def __init__(self):  # , bounce_damper, ball.damper, ball_size, max_x, max_y, min_x, min_y):
        self.damper = random.uniform(.2, 1)
        # self.opp_damper = random.uniform(.5, 1)
        self.size = random.uniform(3, 20)
        self.max_x = max_x - self.size
        self.max_y = max_y - self.size
        self.min_x = min_x + self.size
        self.min_y = min_y + self.size
        self.x = self.min_x
        self.y = random.uniform(self.min_y, self.max_y)
        self.color = (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255))
        self.xVelocity = random.uniform(-50, 50)  # these could be gone with just self.random_velocity() but Im lazy
        self.yVelocity = random.uniform(-50, 50)


balls = []

for i in range(ball_count):
    balls.append(Ball())


def collision(ball_a, ball_b):
    if ball_b.x - ball_a.x > .0001:
        SlopeB = (ball_b.y - ball_a.y) / (ball_b.x - ball_a.x)
        SlopeA = -1 / SlopeB

        x = (-(SlopeB * ball_a.xVelocity - ball_a.yVelocity) + (SlopeA * ball_a.x - ball_a.y)) / (
                    SlopeA - SlopeB) - ball_a.x
        y = SlopeB * x - (SlopeB * ball_a.xVelocity - ball_a.yVelocity) - ball_a.y
        x_ = ball_a.xVelocity - x
        y_ = ball_a.yVelocity - y

        SlopeB = (ball_a.y - ball_b.y) / (ball_a.x - ball_b.x)
        SlopeA = -1 / SlopeB
        _x = (-(SlopeB * ball_b.xVelocity - ball_b.yVelocity) + (SlopeA * ball_b.x - ball_b.y)) / (
                    SlopeA - SlopeB) - ball_b.x
        _y = SlopeB * _x - (SlopeB * ball_b.xVelocity - ball_b.yVelocity) - ball_b.y
        _x_ = ball_b.xVelocity - _x
        _y_ = ball_b.yVelocity - _y

        ball_a.xVelocity = (x + _x_) * ball_a.damper
        ball_a.yVelocity = (y_ + _y) * ball_a.damper
        ball_b.xVelocity = (x_ + _x) * ball_b.damper
        ball_b.yVelocity = (y + _y_) * ball_b.damper

        ball_a.x += ball_a.xVelocity * speed * dt
        ball_a.y += ball_a.yVelocity * speed * dt
        ball_b.x += ball_b.xVelocity * speed * dt
        ball_b.y += ball_b.yVelocity * speed * dt


velocity_rand = (-50, 50)

pygame.init()
black = (255, 255, 255)
white = (0, 0, 0)
green = (0, 255, 0)

gravity = 50
screen = pygame.display.set_mode((max_y, max_x), pygame.RESIZABLE)
speed = 5
#small = .5
#collision_dist = 5

# balls = []
# for i in range(ball_count):
#    balls.append([random.randrange(min_x, max_x), random.randrange(min_y, max_y), random.randrange(-50, 50),
#                  random.randrange(-50, 50),
#                  (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255))])

clock = pygame.time.Clock()


def text_to_screen(screen, text, x, y, size=50, color=(200, 000, 000), font_type=pygame.font.get_default_font()):
    text = str(text)
    font = pygame.font.Font(font_type, size)
    text = font.render(text, True, color)
    screen.blit(text, (x, y))

pastTime = time.time()
while True:
    dt = time.time() - pastTime
    pastTime = time.time()
    screen.fill(white)
    for ball in balls:
        ball.x += ball.xVelocity * speed * dt
        ball.y += ball.yVelocity * speed * dt
        # ground fix
        ball.x = clamp(ball.x, ball.min_x, ball.max_x)
        ball.y = clamp(ball.y, ball.min_y, ball.max_y)

        # draw ball and the velocity
        pygame.draw.circle(screen, ball.color, (ball.y, ball.x), ball.size)
        pygame.draw.line(screen, (255, 0, 0), (ball.y, ball.x), (ball.y + ball.yVelocity, ball.x + ball.xVelocity))
    for ball in balls:
        if ball.x >= ball.max_x:
            ball.xVelocity = -abs(ball.xVelocity) * ball.damper
            ball.yVelocity *= ball.damper
        if ball.y >= ball.max_y:
            ball.yVelocity = -abs(ball.yVelocity) * ball.damper
            ball.xVelocity *= ball.damper
        if ball.y <= ball.min_y:
            ball.yVelocity = abs(ball.yVelocity) * ball.damper
            ball.xVelocity *= ball.damper
        if ball.x <= ball.min_x:
            ball.xVelocity = abs(ball.xVelocity) * ball.damper
            ball.yVelocity *= ball.damper
        ball.xVelocity += gravity * dt

        # print(ball)
        # print(str(ball.y) + " < " + str(max_x))

        # ball collisions
        for ball_ in balls:
            if not ball == ball_:
                if distance(ball.x, ball.y, ball_.x, ball_.y) < ball_.size + ball.size:
                    collision(ball, ball_)

        text_to_screen(screen, dt, 1, 1, 20)

    # for window resizing, quit, and button pressing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.VIDEORESIZE:
            max_y = screen.get_width()
            max_x = screen.get_height()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for ball in balls:
                    ball.xVelocity += random.randrange(*velocity_rand)
                    ball.yVelocity += random.randrange(*velocity_rand)
            if event.button == 4:
                balls.append(Ball())
            elif event.button == 5 and len(balls):
                del balls[-1]

    pygame.display.flip()
