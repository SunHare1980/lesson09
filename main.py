import pygame
import random
import sys
import math

# Инициализация Pygame
pygame.init()

# Параметры экрана
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Survival Game")

# Цвета
WHITE = (255, 255, 255)
DARK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# FPS
FPS = 60
clock = pygame.time.Clock()

# Класс игрока
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("cat.png").convert_alpha()  # Загрузка изображения кошки
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.speed = 10

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed

# Класс врага
class Enemy(pygame.sprite.Sprite):
    def __init__(self, color, speed):
        super().__init__()
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (15, 15), 15)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(0, HEIGHT - self.rect.height)
        self.speed = speed
        self.direction = pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize()
        self.change_direction_time = pygame.time.get_ticks()

    def update(self):
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed

        # Отскок от стен
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.direction.x *= -1
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.direction.y *= -1

        # Изменение направления каждые 5 секунд
        if pygame.time.get_ticks() - self.change_direction_time > 5000:
            self.change_direction()
            self.change_direction_time = pygame.time.get_ticks()

    def change_direction(self):
        player_pos = pygame.math.Vector2(player.rect.center)
        enemy_pos = pygame.math.Vector2(self.rect.center)
        self.direction = (player_pos - enemy_pos).normalize()

# Функция для отображения текста
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, DARK)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

# Основная функция
def main():
    global player
    player = Player()

    # Группы спрайтов
    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()

    all_sprites.add(player)

    # Создание врагов
    for i in range(8):
        enemy = Enemy(RED, 1)  # Медленные враги
        all_sprites.add(enemy)
        enemies.add(enemy)

    for i in range(5):
        enemy = Enemy(BLUE, 2)  # Быстрые враги
        all_sprites.add(enemy)
        enemies.add(enemy)

    start_ticks = pygame.time.get_ticks()  # Время начала игры

    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Обновление
        all_sprites.update()

        # Проверка на столкновение
        if pygame.sprite.spritecollideany(player, enemies):
            running = False

        # Отрисовка
        screen.fill(GREEN)
        all_sprites.draw(screen)

        # Расчет времени выживания
        survival_time = (pygame.time.get_ticks() - start_ticks) // 1000
        draw_text(screen, f"Time Survived: {survival_time}s", 30, WIDTH // 2, 10)

        pygame.display.flip()

    print(f"Game Over! You survived for {survival_time} seconds.")
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
