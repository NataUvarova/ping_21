import pygame
import sys
from time import sleep

pygame.init()

# --- Налаштування ---
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong Deluxe")

# --- Кольори ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 215, 0)

# --- Музика і звуки ---
try:
    pygame.mixer.music.load("music.mp3")  # фоновий трек
    pygame.mixer.music.play(-1)
except:
    print("⚠️ Не знайдено music.mp3")

try:
    bounce_sound = pygame.mixer.Sound("bounce.wav")
    score_sound = pygame.mixer.Sound("score.wav")
except:
    bounce_sound = None
    score_sound = None

# --- Зображення ---
try:
    background = pygame.image.load("pexels-joshsorenson-976873.jpg")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
except:
    background = pygame.Surface((WIDTH, HEIGHT))
    background.fill((0, 0, 0))

try:
    paddle_img = pygame.image.load("pngwing.com.png")
    paddle_img = pygame.transform.scale(paddle_img, (40, 100))
except:
    paddle_img = pygame.Surface((40, 100))
    paddle_img.fill((255, 255, 255))

# --- Шрифти ---
font_big = pygame.font.SysFont("Arial", 72)
font = pygame.font.SysFont("Arial", 48)
font_small = pygame.font.SysFont("Arial", 32)

# --- Початкові значення ---
ball_radius = 15
paddle_speed = 6
ball_speed_x, ball_speed_y = 5, 5
score_left, score_right = 0, 0
winning_score = 5

clock = pygame.time.Clock()


# --- Функція відображення тексту ---
def draw_text(text, font, color, surface, x, y, center=False):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)


# --- Меню ---
def show_menu():
    while True:
        window.blit(background, (0, 0))
        draw_text("PING PONG", font_big, YELLOW, window, WIDTH // 2, HEIGHT // 3, True)
        draw_text("Натисни ENTER, щоб почати", font_small, WHITE, window, WIDTH // 2, HEIGHT // 2, True)
        draw_text("ESC — вихід", font_small, WHITE, window, WIDTH // 2, HEIGHT // 2 + 50, True)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()


# --- Екран перемоги ---
def show_winner(winner):
    window.blit(background, (0, 0))
    draw_text(f"Переміг {winner}!", font_big, YELLOW, window, WIDTH // 2, HEIGHT // 2 - 50, True)
    draw_text("Натисни ENTER, щоб зіграти ще", font_small, WHITE, window, WIDTH // 2, HEIGHT // 2 + 50, True)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False


# --- Основна гра ---
def game():
    global score_left, score_right
    left_y = HEIGHT // 2 - 50
    right_y = HEIGHT // 2 - 50
    ball_x, ball_y = WIDTH // 2, HEIGHT // 2
    ball_speed_x, ball_speed_y = 5, 5
    score_left, score_right = 0, 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and left_y > 0:
            left_y -= paddle_speed
        if keys[pygame.K_s] and left_y < HEIGHT - 100:
            left_y += paddle_speed

        if keys[pygame.K_UP] and right_y > 0:
            right_y -= paddle_speed
        if keys[pygame.K_DOWN] and right_y < HEIGHT - 100:
            right_y += paddle_speed

        ball_x += ball_speed_x
        ball_y += ball_speed_y

        # Відбиття від стін
        if ball_y - ball_radius <= 0 or ball_y + ball_radius >= HEIGHT:
            ball_speed_y *= -1
            if bounce_sound:
                bounce_sound.play()

        # Відбиття від ракеток
        if (50 <= ball_x - ball_radius <= 90 and left_y < ball_y < left_y + 100):
            ball_speed_x *= -1
            ball_x = 90 + ball_radius
            if bounce_sound:
                bounce_sound.play()

        if (WIDTH - 90 <= ball_x + ball_radius <= WIDTH - 50 and right_y < ball_y < right_y + 100):
            ball_speed_x *= -1
            ball_x = WIDTH - 90 - ball_radius
            if bounce_sound:
                bounce_sound.play()

        # Голи
        if ball_x < 0:
            score_right += 1
            if score_sound:
                score_sound.play()
            ball_x, ball_y = WIDTH // 2, HEIGHT // 2
            ball_speed_x *= -1
            sleep(0.5)

        if ball_x > WIDTH:
            score_left += 1
            if score_sound:
                score_sound.play()
            ball_x, ball_y = WIDTH // 2, HEIGHT // 2
            ball_speed_x *= -1
            sleep(0.5)

        # Перемога
        if score_left == winning_score:
            show_winner("Лівий гравець")
            return
        if score_right == winning_score:
            show_winner("Правий гравець")
            return

        # Малювання
        window.blit(background, (0, 0))
        window.blit(paddle_img, (50, left_y))
        window.blit(paddle_img, (WIDTH - 90, right_y))
        pygame.draw.circle(window, WHITE, (ball_x, ball_y), ball_radius)
        draw_text(f"{score_left} : {score_right}", font, WHITE, window, WIDTH // 2 - 40, 20)
        pygame.display.flip()
        clock.tick(60)


# --- Запуск ---
show_menu()
while True:
    game()