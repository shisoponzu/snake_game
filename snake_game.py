import pygame
import random

WINDOW_W = 800
WINDOW_H = 600
WINDOW_SIZE = (WINDOW_W, WINDOW_H)
COLOR_WHITE = (255, 255, 255)
COLOR_GREEN = (0, 100, 55)
COLOR_RED = (255, 0, 0)
COLOR_BLACK = (0, 0, 0)

SNAKE_SIZE = 10

FOOD_QUANTITY = 10
FOOD_SIZE = 10
FOOD_X = range(0, 800, 10)
FOOD_Y = range(0, 600, 10)

GAMEOVER_TEXT = "GAME OVER"
RETRY_TEXT = "RETRY: F5"
SCORE = 0

FRAME_RATE = 10

pygame.init()

FONT = pygame.font.SysFont(None, 50)

screen = pygame.display.set_mode(WINDOW_SIZE)
clock = pygame.time.Clock()

def is_gameover(x, y, snake_pos):
    if x > WINDOW_W or x < 0 or y > WINDOW_H or y < 0:
        return True
    
    elif (x, y) in snake_pos:
        return True
    
    return False

def draw_snake(x, y):
    pygame.draw.rect(
        screen,
        COLOR_GREEN,
        (x, y, SNAKE_SIZE, SNAKE_SIZE)
    )

def generate_food(foods):
    x = random.choice(FOOD_X)
    y = random.choice(FOOD_Y)
    while (x, y) in foods or (x, y) == (200, 100):
        x = random.choice(FOOD_X)
        y = random.choice(FOOD_Y)
    return (x, y)

def draw_food(x, y):
    pygame.draw.rect(
        screen,
        COLOR_RED,
        (x, y, FOOD_SIZE, FOOD_SIZE)
    )

def draw_text(text, color, position):
    label = FONT.render(text, True, color)
    screen.blit(label, position)

def main():
    x = 200
    y = 100
    x_speed = 0
    y_speed = 0

    snake_len = 1
    snake_pos = []

    foods = []
    for _ in range(FOOD_QUANTITY):
        food = generate_food(foods)
        foods.append(food)

    score = 0

    running = True
    try_again = False

    while running:
        clock.tick(FRAME_RATE)

        x += x_speed
        y += y_speed

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and y_speed == 0:
                    y_speed = -SNAKE_SIZE
                    x_speed = 0
                elif event.key == pygame.K_DOWN and y_speed == 0:
                    y_speed = SNAKE_SIZE
                    x_speed = 0
                elif event.key == pygame.K_LEFT and x_speed == 0:
                    x_speed = -SNAKE_SIZE
                    y_speed = 0
                elif event.key == pygame.K_RIGHT and x_speed == 0:
                    x_speed = SNAKE_SIZE
                    y_speed = 0

                elif event.key == pygame.K_q:
                    running = False

        if is_gameover(x, y, snake_pos):
            running = False
            try_again = True

        if (x, y) in foods:
            foods.remove((x, y))
            foods.append(generate_food(foods))
            
            snake_len += 1
            score += 1

        score_txt = "Score: " + str(score)

        screen.fill(COLOR_WHITE)

        if snake_len > 1:
            snake_pos.append((x, y))
            if len(snake_pos) > snake_len:
                snake_pos.pop(0)

            for pos in snake_pos:
                draw_snake(pos[0], pos[1])

        else:
            draw_snake(x, y)

        for food in foods:
            draw_food(food[0], food[1])

        draw_text(score_txt, COLOR_BLACK, (25, 25))

        pygame.display.flip()

    if try_again:
        retry(score)

def retry(score):
    running = True
    try_again = False

    while running:
        clock.tick(FRAME_RATE)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F5:
                    running = False
                    try_again = True
                elif event.key == pygame.K_q:
                    running = False

        if score >= 0:
            score_txt = "Score: " + str(score)

            screen.fill((100, 100, 100))

            draw_text(GAMEOVER_TEXT, COLOR_BLACK, (WINDOW_W/2 - 100, WINDOW_H/2 - 100))
            draw_text(score_txt, COLOR_BLACK, (WINDOW_W/2, WINDOW_H/2))
            draw_text(RETRY_TEXT, COLOR_RED, (WINDOW_W/2 + 100, WINDOW_H/2 + 100))
            draw_text("END : Q", COLOR_RED, (WINDOW_W/2 + 135, WINDOW_H/2 + 140))
            
            pygame.display.flip()

        else:
            screen.fill((100, 100, 100))
            draw_text("Move: arrow keys", COLOR_WHITE, (WINDOW_W/2 - 100, WINDOW_H/2 -100))
            draw_text("Start: F5", COLOR_WHITE, (WINDOW_W/2 - 100, WINDOW_H/2))
            draw_text("END : Q", COLOR_RED, (WINDOW_W/2 + 135, WINDOW_H/2 + 140))
            
            pygame.display.flip()

    if try_again:
        main()

retry(-1)

pygame.quit()