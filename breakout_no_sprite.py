import pygame
import sys
import random
import math
import os

os.environ['SDL_VIDEO_WINDOW_POS'] = "20,20"

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)


class Util():
    def intersects(self, a, b, c, min, max):
        disc = b ** 2 - 4 * a * c
        if disc < 0:
            return False
        s1 = (-b + math.sqrt(disc)) / (2 * a)
        s2 = (-b - math.sqrt(disc)) / (2 * a)
        return (min <= s1 <= max) or (min <= s2 <= max)


class Brick():
    WIDTH = 100
    HEIGHT = 25
    GAP_X = 30
    GAP_Y = 20

    def __init__(self, screen, x, y):
        self.x = x
        self.y = y
        self.screen = screen
        self.util = Util()


    def draw(self):
        pygame.draw.rect(self.screen, WHITE,
                         (self.x, self.y, self.WIDTH, self.HEIGHT), 0)


    def collides_ball(self, ball):
        intersects_x = False
        intersects_y = False

        intersects_x = self.util.intersects(
            1, -2 * ball.x, (ball.y - self.y)**2 - ball.radius**2 + ball.x**2, self.x, self.x + self.WIDTH)
        intersects_x = intersects_x or self.util.intersects(
            1, -2 * ball.x, (ball.y - self.y - self.HEIGHT)**2 - ball.radius**2 + ball.x**2, self.x, self.x + self.WIDTH)

        intersects_y = self.util.intersects(
            1, -2 * ball.y, (ball.x - self.x)**2 - ball.radius**2 + ball.y**2, self.y, self.y + self.HEIGHT)
        intersects_y = intersects_y or self.util.intersects(
            1, -2 * ball.y, (ball.x - self.x - self.WIDTH)**2 - ball.radius**2 + ball.y**2, self.y, self.y + self.HEIGHT)

        return intersects_x, intersects_y


class Paddle():
    MOVE_STEPS = 10
    WIDTH = 200
    HEIGHT = 30

    def __init__(self, screen, x, y):
        self.x = x
        self.y = y
        self.screen = screen
        self.util = Util()

    def draw(self):
        pygame.draw.rect(self.screen, WHITE,
                         (self.x, self.y, self.WIDTH, self.HEIGHT), 0)

    def move_left(self, balls):
        self.x = self.x - self.MOVE_STEPS if self.x - self.MOVE_STEPS > 0 else self.x

    def move_right(self):
        self.x = self.x + self.MOVE_STEPS if self.x + \
            self.MOVE_STEPS < SCREEN_WIDTH else self.x

    def collides_ball(self, ball):
        intersects_x = False
        intersects_y = False

        intersects_x = intersects_x or self.util.intersects(
            1, -2 * ball.x, (ball.y - self.y)**2 - ball.radius**2 + ball.x**2, self.x, self.x + self.WIDTH)
        intersects_y = intersects_y or self.util.intersects(
            1, -2 * ball.y, (ball.x - self.x)**2 - ball.radius**2 + ball.y**2, self.y, self.y + self.HEIGHT)
        intersects_y = intersects_y or self.util.intersects(
            1, -2 * ball.y, (ball.x - self.x - self.WIDTH)**2 - ball.radius**2 + ball.y**2, self.y, self.y + self.HEIGHT)

        return intersects_x, intersects_y


class Ball():
    RADIUS = 10
    MOVE_STEPS = 5

    def __init__(self, screen, x, y):
        self.x = x
        self.y = y
        self.direction_x = 1
        self.direction_y = 1
        self.screen = screen
        self.radius = self.RADIUS

    def draw(self):
        pygame.draw.circle(self.screen, GREEN, (self.x, self.y), self.RADIUS)

    def move(self):
        self.x = self.x + self.MOVE_STEPS * self.direction_x
        self.y = self.y + self.MOVE_STEPS * self.direction_y

        if self.x + self.RADIUS > SCREEN_WIDTH:
            self.direction_x = -1

        if self.x - self.RADIUS < 0:
            self.direction_x = 1

        if self.y + self.RADIUS > SCREEN_HEIGHT:
            self.direction_y = -1

        if self.y - self.RADIUS < 0:
            self.direction_y = 1

    def flip_direction_x(self):
        self.direction_x = self.direction_x * -1

    def flip_direction_y(self):
        self.direction_y = self.direction_y * -1


def create_bricks(screen):
    bricks = []
    for x in range(0, 6):
        for y in range(0, 4):
            bricks.append(Brick(screen, x * (Brick.WIDTH +
                                             Brick.GAP_X), y * (Brick.HEIGHT + Brick.GAP_Y)))
    return bricks


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Breakout Game | codingboost.com')
    clock = pygame.time.Clock()

    done = False

    paddle = Paddle(screen, 100, SCREEN_HEIGHT - 30)
    ball1 = Ball(screen, 100, 100)
    bricks = create_bricks(screen)
    balls = [ball1]

    while not done:
        screen.fill(BLACK)

        last_key = None
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            paddle.move_left(balls)

        if keys[pygame.K_RIGHT]:
            paddle.move_right()

        # event = pygame.event.wait()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        paddle.draw()
        for ball in balls:
            ball.move()
            ball.draw()

        for ball in balls:
            paddle_ball_intersects_x, paddle_ball_intersects_y = paddle.collides_ball(
                ball)
            if paddle_ball_intersects_x:
                ball.flip_direction_y()
            if paddle_ball_intersects_y:
                ball.flip_direction_x()

        for brick in bricks:
            hit = False
            for ball in balls:
                intersects_x, intersects_y = brick.collides_ball(ball)
                if intersects_x or intersects_y:
                    if intersects_x:
                        ball.direction_y = ball.direction_y * -1
                    if intersects_y:
                        ball.direction_x = ball.direction_x * -1
                    bricks.remove(brick)
                    hit = True
                    break

            if not hit:
                brick.draw()

        pygame.display.update()
        clock.tick(60)


main()
