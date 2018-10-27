import pygame
import sys
import random
import math

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# in ms
FRAME_DELAY = 50

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

UNIT_SIZE = 20

class Snake:
    def __init__(self):
        self.direction = [DOWN, UP, RIGHT, LEFT][random.randint(0, 3)]
        self.body = [random_screen_unit()]
        self.aten_foods = []


    def can_move_direction(self, new_direction):
        if len(self.body) == 1: return True
        return abs(self.direction) % 2 != abs(new_direction) % 2
            

    def change_direction(self, new_direction):
        if self.can_move_direction(new_direction):
            self.direction = new_direction


    def move_head(self, direction):
        self.body[0][abs(direction) % 2] += UNIT_SIZE * sign(direction)


    def leaves_screen(self):
        return self.body[0][0] < 0 or self.body[0][0] > SCREEN_WIDTH or self.body[0][1] < 0 or self.body[0][1] > SCREEN_HEIGHT


    def head_collides_with_body(self):
        head = self.body[0]
        for snake_part in self.body[1:]:
            if snake_part[0] == head[0] and snake_part[1] == head[1]:
                return True
        return False


    def move(self):
        old_tail = self.body[-1]
        i = len(self.body) - 1
        while i > 0:
            self.body[i][0] = self.body[i - 1][0]
            self.body[i][1] = self.body[i - 1][1]
            i -= 1

        temp_list = []
        for food in self.aten_foods:
            if food[0] == old_tail[0] and food[1] == old_tail[1]:
                self.body.append(list(food))
            else:
                temp_list.append(food)
        self.aten_foods = temp_list

        self.move_head(self.direction)
                    

    def eats_food(self, food):
        if food[0] == self.body[0][0] and food[1] == self.body[0][1]:
            self.aten_foods.append(list(food))
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
    return [random.randint(0, SCREEN_WIDTH // UNIT_SIZE) * UNIT_SIZE, random.randint(0, SCREEN_HEIGHT // UNIT_SIZE) * UNIT_SIZE]


def display_text(text, x, y):
    myfont = pygame.font.SysFont('Comic Sans MS', 30)
    textsurface = myfont.render(text, False, WHITE)
    screen.blit(textsurface, (x, y))    


snake = Snake()
food = random_screen_unit()

while True:
    pygame.time.delay(FRAME_DELAY)
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
        pygame.draw.rect(screen, WHITE, (snake_unit[0], snake_unit[1], UNIT_SIZE, UNIT_SIZE), 0)

    pygame.draw.rect(screen, GREEN, (food[0], food[1], UNIT_SIZE, UNIT_SIZE), 0)

    pygame.display.update()

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

