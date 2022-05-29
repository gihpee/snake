import pygame
import sys
import os
import copy
import random

pygame.init()
FPS = 20
screen = pygame.display.set_mode((500, 600))
clock = pygame.time.Clock()
f1 = pygame.font.Font(None, 35)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()
    return image


def load_higscore(name):
    fullname = os.path.join('data', name)
    m = open(fullname, 'r')
    z = m.read()
    m.close()
    return z


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    fon = pygame.transform.scale(load_image('start.png'), (500, 600))
    screen.blit(fon, (0, 0))


class GameOver(pygame.sprite.Sprite):
    image = load_image("gameover.png")

    def __init__(self, group):
        super().__init__(group)
        self.image = GameOver.image
        self.rect = self.image.get_rect()
        self.rect.x = -500
        self.rect.y = 0
        self.v = 200

    def update(self):
        if self.rect.x >= 0:
            self.rect.x = 0
        else:
            self.rect.x += self.v / 10


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 30

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size


class Snake(Board):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.board[15][15] = 'S'
        self.board[15][16] = 'S'
        self.snake = list()
        self.snake.append([15, 16])
        self.snake.append([15, 15])
        self.y, self.x = random.randint(1, 29), random.randint(1, 29)
        self.board[self.y][self.x] = 'A'
        self.end_flag = False
        self.score = 0
        self.apple_image = load_image('appl.png')
        self.grass_image = load_image('gras.png')
        self.highscore = int(load_higscore('highscore.txt'))

    def move(self, direction):
        if not self.end_flag:
            k = copy.deepcopy(self.snake)
            if direction == 119:
                self.snake[0][0] -= 1
            if direction == 100:
                self.snake[0][1] -= 1
            if direction == 275:
                self.snake[0][0] += 1
            if direction == 97:
                self.snake[0][1] += 1
            if self.snake[0][0] >= 30 or self.snake[0][0] < 0 or self.snake[0][1] >= 30 or self.snake[0][
                1] < 0 or self.snake.count(self.snake[0]) > 1:
                q = open(os.path.join('data', 'highscore.txt'), 'w')
                q.seek(0)
                q.write(str(self.highscore))
                q.close()
                game_over(self.score)
                self.end_flag = True
            else:
                for i in range(1, len(self.snake), 1):
                    self.snake[i] = k[i - 1]

                self.board = [[0] * self.width for _ in range(self.height)]
                self.board[self.y][self.x] = 'A'
                for el in self.snake:
                    self.board[el[0]][el[1]] = 'S'
                if self.snake[0][0] == self.y and self.snake[0][1] == self.x:
                    self.board[self.y][self.x] = 'S'
                    self.y, self.x = random.randint(1, 29), random.randint(1, 29)
                    self.board[self.y][self.x] = 'A'
                    if self.snake[-2][0] == self.snake[-1][0]:
                        self.snake.append([self.snake[-1][0], self.snake[-1][1] - 1])
                    else:
                        self.snake.append([self.snake[-1][0] - 1, self.snake[-1][1]])
                    self.score += 1
                    if self.highscore < self.score:
                        self.highscore = self.score

    def render(self, screen):
        a, b = 0, 0
        for i in range(self.top, self.height * self.cell_size + self.top, self.cell_size):
            b = 0
            for j in range(self.left, self.width * self.cell_size + self.left, self.cell_size):
                pygame.draw.rect(screen, (28, 75, 8), (j, i, self.cell_size, self.cell_size))
                if self.board[a][b] == 'S':
                    pygame.draw.rect(screen, (20, 20, 20), (j + 1, i + 1, self.cell_size - 2, self.cell_size - 2))
                elif self.board[a][b] == 'A':
                    screen.blit(self.apple_image, (j + 1, i + 1))
                else:
                    screen.blit(self.grass_image, (j + 1, i + 1))
                text_score = f1.render('score: {}'.format(self.score), 1, (255, 255, 255))
                screen.blit(text_score, (20, 540))
                text_highscore = f1.render('highscore: {}'.format(self.highscore), 1, (255, 255, 255))
                screen.blit(text_highscore, (300, 540))
                b += 1
            a += 1


def game_over(score):
    global gm_flag, points
    gm_flag = True
    points = score


snake_board = Snake(30, 30)
snake_board.set_view(25, 50, 15)
snake_direction = 275
start_flag = True
gm_flag = False
all_sprites = pygame.sprite.Group()
GameOver(all_sprites)
points = 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if start_flag:
                if 400 >= event.pos[0] >= 100 and 200 <= event.pos[1] <= 285:
                    snake_board = Snake(30, 30)
                    snake_board.set_view(25, 50, 15)
                    snake_direction = 275
                    start_flag = False
                    FPS = 20
                elif 350 >= event.pos[0] >= 150 and 350 <= event.pos[1] <= 420:
                    terminate()
            elif gm_flag:
                if 400 >= event.pos[0] >= 100 and 250 <= event.pos[1] <= 340:
                    start_flag = True
                    gm_flag = False
                    all_sprites = pygame.sprite.Group()
                    GameOver(all_sprites)
                elif 350 >= event.pos[0] >= 150 and 400 <= event.pos[1] <= 470:
                    terminate()
        elif event.type == pygame.KEYDOWN:
            print(event.key)
            if event.key in [115, 119, 100, 97]:
                snake_direction = event.key
    if start_flag:
        start_screen()
    elif gm_flag:
        FPS = 50
        all_sprites.draw(screen)
        all_sprites.update()
        text_score = f1.render('score: {}'.format(points), 1, (255, 0, 0))
        screen.blit(text_score, (200, 540))
    else:
        screen.fill((0, 0, 0))
        snake_board.move(snake_direction)
        snake_board.render(screen)
    pygame.display.flip()
    clock.tick(FPS)
