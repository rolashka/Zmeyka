import pygame
import random

# Настройки игры
WIDTH = 640
HEIGHT = 480
FPS = 10

# Цвета
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Инициализация Pygame
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Змейка")
clock = pygame.time.Clock()

# Класс змейки
class Snake(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20, 20))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH / 2
        self.rect.y = HEIGHT / 2
        self.speedx = 20
        self.speedy = 0
        self.body = [(self.rect.x, self.rect.y)]

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        self.body.insert(0, (self.rect.x, self.rect.y))
        if len(self.body) > 20:
            self.body.pop()

    def grow(self):
        self.body.insert(0, (self.rect.x, self.rect.y))

# Класс яблока
class Apple(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20, 20))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, WIDTH - 20, 20)
        self.rect.y = random.randrange(0, HEIGHT - 20, 20)

# Создание змейки и яблок
snake = Snake()
apples = pygame.sprite.Group()
for i in range(20):
    apple = Apple()
    apples.add(apple)

# Переменная для отслеживания количества съеденных яблок
score = 0

# Игровой цикл
running = True
while running:
    # События
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                snake.speedx = -20
                snake.speedy = 0
            elif event.key == pygame.K_RIGHT:
                snake.speedx = 20
                snake.speedy = 0
            elif event.key == pygame.K_UP:
                snake.speedy = -20
                snake.speedx = 0
            elif event.key == pygame.K_DOWN:
                snake.speedy = 20
                snake.speedx = 0

# Обновление
    snake.update()

    # Проверка столкновений
    if snake.rect.left < 0 or snake.rect.right > WIDTH or snake.rect.top < 0 or snake.rect.bottom > HEIGHT:
        running = False
    apple_collision = pygame.sprite.spritecollide(snake, apples, True)
    if apple_collision:
        score += 1
        snake.grow()
        apple = Apple()
        apples.add(apple)
        if score == 20:
            print("Вы победили!")
            running = False
    for i in range(1, len(snake.body)):
        if snake.rect.colliderect(pygame.Rect(snake.body[i], (20, 20))):
            running = False

    # Отрисовка
    screen.fill(BLACK)
    apples.draw(screen)
    for i in range(len(snake.body)):
        pygame.draw.rect(screen, GREEN, [snake.body[i][0], snake.body[i][1], 20, 20])
    pygame.display.flip()

    # Задержка
    clock.tick(FPS)

# Выход из Pygame
pygame.quit()