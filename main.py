import pygame
import os
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900,500
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Dino Blast!")

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
BLUE = (0,0,255)

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('ASSETS', 'hit.wav'))
BULLET_FIRE_SOUND_BLUE = pygame.mixer.Sound(os.path.join('ASSETS', 'ice.wav'))
BULLET_FIRE_SOUND_RED = pygame.mixer.Sound(os.path.join('ASSETS', 'fire.wav'))

HEALTH_FONT = pygame.font.SysFont('impact', 40)
WINNER_FONT = pygame.font.SysFont('impact', 100)

FPS = 60
VEL = 5
BULLET_VEL = 10
MAX_BULLETS = 3
DINO_WIDTH, DINO_HEIGHT = 75,80

BLUE_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

RED_DINO_IMAGE = pygame.image.load(
    os.path.join('ASSETS', 'redDino.png'))
RED_DINO = pygame.transform.scale(RED_DINO_IMAGE, (DINO_WIDTH, DINO_HEIGHT))
BLUE_DINO_IMAGE = pygame.image.load(
    os.path.join('ASSETS', 'blueDino.png'))
BLUE_DINO = pygame.transform.scale(BLUE_DINO_IMAGE, (DINO_WIDTH, DINO_HEIGHT))


BLUE_DINO_SHOOT = pygame.image.load(
    os.path.join('ASSETS', 'blueShoot.png'))
BLUE_SHOOT = pygame.transform.scale(BLUE_DINO_SHOOT, (DINO_WIDTH, DINO_HEIGHT))

RED_DINO_SHOOT = pygame.image.load(
    os.path.join('ASSETS', 'redShoot.png'))
RED_SHOOT = pygame.transform.scale(RED_DINO_SHOOT, (DINO_WIDTH, DINO_HEIGHT))


FOREST = pygame.transform.scale(pygame.image.load(os.path.join('ASSETS', 'forest.png')), (WIDTH, HEIGHT))


def draw_window(blue, red, blue_bullets, red_bullets, blue_health, red_health):
    WIN.blit(FOREST, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)
    blue_health_text = HEALTH_FONT.render("Health: " + str(blue_health), 1, WHITE)
    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
    WIN.blit(blue_health_text, (WIDTH - blue_health_text.get_width() - 10, 10))
    WIN.blit(red_health_text, (10, 10))

    WIN.blit(BLUE_DINO, (blue.x, blue.y))
    WIN.blit(RED_DINO, (red.x, red.y))

    for bullet in blue_bullets:
        pygame.draw.rect(WIN, BLUE, bullet)

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    pygame.display.update()

def blue_handle_movement(keys_pressed, blue):
    if keys_pressed[pygame.K_a] and blue.x - VEL > 0:  # left
        blue.x -= VEL
    if keys_pressed[pygame.K_d] and blue.x + VEL + blue.width < BORDER.x:  # right
        blue.x += VEL
    if keys_pressed[pygame.K_w] and blue.y - VEL > 0:# up
        blue.y -= VEL
    if keys_pressed[pygame.K_s] and blue.y + VEL + blue.height < HEIGHT: # down
        blue.y += VEL


def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:  # left
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH:  # right
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0:# up
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT: # down
        red.y += VEL

def handle_bullets(blue_bullets, red_bullets, blue, red):
    for bullet in blue_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            blue_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            blue_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if blue.colliderect(bullet):
            pygame.event.post(pygame.event.Event(BLUE_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WINBOX = pygame.draw.rect(WIN, BLACK, (200,200,500,100))
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(4000)

def main():
    blue = pygame.Rect(100, 250,DINO_WIDTH, DINO_HEIGHT)
    red = pygame.Rect(725, 250,DINO_WIDTH, DINO_HEIGHT)

    blue_bullets = []
    red_bullets = []

    red_health = 10
    blue_health = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(blue_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(blue.x + blue.width, blue.y + blue.height//2 - 2, 10, 5)
                    blue_bullets.append(bullet)
                    BULLET_FIRE_SOUND_BLUE.play()
                    WIN.blit(BLUE_DINO, (blue.x, blue.y))

                if event.key == pygame.K_RSHIFT and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND_RED.play()
                    WIN.blit(RED_DINO, (red.x, red.y))

            if event.type == BLUE_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == RED_HIT:
                blue_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ""
        if blue_health <= 0:
            winner_text = "Blue Wins!"

        if red_health <= 0:
            winner_text = "Red Wins!"

        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        blue_handle_movement(keys_pressed, blue)
        red_handle_movement(keys_pressed, red)

        handle_bullets(blue_bullets, red_bullets, blue, red)

        draw_window(blue, red, blue_bullets, red_bullets, blue_health, red_health)

    main()

if __name__ == "__main__":
    main()