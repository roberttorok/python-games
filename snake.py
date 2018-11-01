import pygame
import sys
import random
import math

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

FRAME_DELAY = 90

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Snake | codingboost.com')
pygame.font.init()

DOWN = 1
UP = -3
RIGHT = 2
LEFT = -4 

UNIT_SIZE = 40

class Pos:
    x = 0
    y = 0
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

class Snake:
    def __init__(self):
        self.direction = [DOWN, UP, RIGHT, LEFT][random.randint(0, 3)]
        self.body = [random_screen_unit()]
        self.head = self.body[0]
        self.eaten_foods = []


    def can_move_direction(self, new_direction):
        if len(self.body) == 1: return True
        return abs(self.direction) % 2 != abs(new_direction) % 2
            

    def change_direction(self, new_direction):
        if self.can_move_direction(new_direction):
            self.direction = new_direction


    def move_head(self, direction):
        if direction == UP or direction == DOWN:
            self.head.y += UNIT_SIZE * sign(direction)
        else:
            self.head.x += UNIT_SIZE * sign(direction)


    def leaves_screen(self):
        return not ((0 <= self.head.x <= SCREEN_WIDTH - UNIT_SIZE) and (0 <= self.head.y <= SCREEN_HEIGHT - UNIT_SIZE))


    def head_collides_with_body(self):
        for snake_part in self.body[1:]:
            if snake_part == self.head:
                return True
        return False


    def move(self):
        old_tail = self.body[-1]
        i = len(self.body) - 1
        while i > 0:
            self.body[i].x = self.body[i - 1].x
            self.body[i].y = self.body[i - 1].y
            i -= 1

        temp_list = []
        for food in self.eaten_foods:
            if food == old_tail:
                self.body.append(food)
            else:
                temp_list.append(food)
        self.eaten_foods = temp_list
        self.move_head(self.direction)
                    

    def eats_food(self, food):
        if food == self.head:
            self.eaten_foods.append(food)
            return True
        else:
            return False


def sign(num):
    if num < 0:
        return -1
    elif num == 0:
        return 0
    else:
        return 1


def random_screen_unit():
    pos = Pos()
    pos.x = random.randint(0, SCREEN_WIDTH // UNIT_SIZE - 1) * UNIT_SIZE
    pos.y = random.randint(0, SCREEN_HEIGHT // UNIT_SIZE - 1) * UNIT_SIZE
    return pos


def display_text(text, x, y):
    myfont = pygame.font.SysFont('Comic Sans MS', 30)
    textsurface = myfont.render(text, False, WHITE)
    screen.blit(textsurface, (x, y))    


snake = Snake()
food = random_screen_unit()

while True:
    screen.fill(BLACK)

    display_text("Points: %d" % (len(snake.body)), 20, 20)

    snake.move()

    if snake.leaves_screen() or snake.head_collides_with_body():
        display_text("Game Over", 280, 240)
        pygame.display.update()
        pygame.event.wait()
        pygame.quit()
        sys.exit()


    if snake.eats_food(food):
        food = random_screen_unit()

    for snake_unit in snake.body:
        pygame.draw.rect(screen, WHITE, (snake_unit.x, snake_unit.y, UNIT_SIZE, UNIT_SIZE), 0)

    pygame.draw.rect(screen, GREEN, (food.x, food.y, UNIT_SIZE, UNIT_SIZE), 0)

    pygame.display.update()
    pygame.time.delay(FRAME_DELAY)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]: snake.change_direction(UP)
    if keys[pygame.K_DOWN]: snake.change_direction(DOWN)
    if keys[pygame.K_LEFT]: snake.change_direction(LEFT)
    if keys[pygame.K_RIGHT]: snake.change_direction(RIGHT)
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

