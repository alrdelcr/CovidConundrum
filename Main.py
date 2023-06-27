import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
WIDTH = 800
HEIGHT = 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zombie Survival Game")

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Load images
player_img = pygame.image.load("player.png")
zombie_img = pygame.image.load("zombie.png")
bullet_img = pygame.image.load("bullet.png")

# Set up the player
player_width = 64
player_height = 64
player_x = (WIDTH - player_width) // 2
player_y = HEIGHT - player_height - 10
player_speed = 5

# Set up bullets
bullet_width = 32
bullet_height = 32
bullet_speed = 10
bullet_state = "ready"

# Set up zombies
zombie_width = 64
zombie_height = 64
zombie_x = random.randint(0, WIDTH - zombie_width)
zombie_y = random.randint(50, 150)
zombie_speed = 2

# Functions
def draw_player(x, y):
    win.blit(player_img, (x, y))

def draw_zombie(x, y):
    win.blit(zombie_img, (x, y))

def draw_bullet(x, y):
    win.blit(bullet_img, (x, y))

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle player movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x -= player_speed
            if event.key == pygame.K_RIGHT:
                player_x += player_speed
            if event.key == pygame.K_UP:
                player_y -= player_speed
            if event.key == pygame.K_DOWN:
                player_y += player_speed
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_x = player_x + (player_width - bullet_width) // 2
                    bullet_y = player_y
                    bullet_state = "fire"

    # Update player position
    if player_x < 0:
        player_x = 0
    elif player_x > WIDTH - player_width:
        player_x = WIDTH - player_width
    if player_y < 0:
        player_y = 0
    elif player_y > HEIGHT - player_height:
        player_y = HEIGHT - player_height

    # Update bullet position
    if bullet_state == "fire":
        bullet_y -= bullet_speed
        if bullet_y <= 0:
            bullet_state = "ready"

    # Update zombie position
    zombie_y += zombie_speed
    if zombie_y > HEIGHT:
        zombie_x = random.randint(0, WIDTH - zombie_width)
        zombie_y = random.randint(50, 150)

    # Check for collision between bullet and zombie
    if bullet_state == "fire" and bullet_x < zombie_x + zombie_width and bullet_x + bullet_width > zombie_x \
            and bullet_y < zombie_y + zombie_height and bullet_y + bullet_height > zombie_y:
        bullet_state = "ready"
        zombie_x = random.randint(0, WIDTH - zombie_width)
        zombie_y = random.randint(50, 150)

    # Check for collision between player and zombie
    if player_x < zombie_x + zombie_width and player_x + player_width > zombie_x \
            and player_y < zombie_y + zombie_height and player_y + player_height > zombie_y:
        running = False  # Game over if zombie reaches the player

    # Clear the screen
    win.fill(WHITE)

    # Draw game objects
    draw_player(player_x, player_y)
    draw_zombie(zombie_x, zombie_y)
    if bullet_state == "fire":
        draw_bullet(bullet_x, bullet_y)

    # Update the display
    pygame.display.update()

# Quit the game
pygame.quit()
