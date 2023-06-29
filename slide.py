import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
WIDTH = 800
HEIGHT = 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Covid Survival Game")

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Load images
player_img = pygame.transform.scale(pygame.image.load("player.png"), (50,50))
zombie_img = pygame.transform.scale(pygame.image.load("zombie.png"), (50,50))
syringe_img = pygame.transform.scale(pygame.image.load("syringe.png"), (30,30))
mask_img = pygame.transform.scale(pygame.image.load("mask.png"), (30,30))
hazmat_img = pygame.transform.scale(pygame.image.load("hazmat.png"), (50,50))
cure_img = pygame.transform.scale(pygame.image.load("cure.png"), (50,50))
grenade_img = pygame.transform.scale(pygame.image.load("grenade.png"), (30,30))
ammo_img = pygame.transform.scale(pygame.image.load("ammo.png"), (20,20))



# Set up the player
player_width = 32
player_height = 32
player_x = (WIDTH - player_width) // 2
player_y = HEIGHT - player_height - 10
player_speed = 1    
player_health = 100
max_health = player_health

# Set up syringe gun
syringe_width = 32
syringe_height = 32
syringe_x = player_x + (player_width - syringe_width) // 2
syringe_y = player_y - syringe_height
syringe_speed = 10
syringe_state = "ready"

# Set up mobs
mob_width = 64
mob_height = 64
mob_speed = 2
mobs = []
mob_types = ["normal", "fast", "strong"]
max_mobs = 1

# Set up power-ups
powerup_width = 32
powerup_height = 32
powerups = []
powerup_types = ["mask", "hazmat", "cure", "grenade", "ammo"]

# Game variables
wave = 1
rounds = 0
kills = 0
round_over = False
game_over = False

# Functions
def draw_player():
    win.blit(player_img, (player_x, player_y))

def draw_syringe():
    win.blit(syringe_img, (syringe_x, syringe_y))

def draw_mob(x, y):
    win.blit(zombie_img, (x, y))

def draw_powerup(x, y, powerup_type):
    if powerup_type == "mask":
        win.blit(mask_img, (x, y))
    elif powerup_type == "hazmat":
        win.blit(hazmat_img, (x, y))
    elif powerup_type == "cure":
        win.blit(cure_img, (x, y))
    elif powerup_type == "grenade":
        win.blit(grenade_img, (x, y))
    elif powerup_type == "ammo":
        win.blit(ammo_img, (x, y))

def fire_syringe():
    global syringe_state
    syringe_state = "fire"
    #   pygame.mixer.Sound("shoot.wav").play()

def is_collision(obj1_x, obj1_y, obj1_width, obj1_height, obj2_x, obj2_y, obj2_width, obj2_height):
    if obj1_x < obj2_x + obj2_width and obj1_x + obj1_width > obj2_x and obj1_y < obj2_y + obj2_height and obj1_y + obj1_height > obj2_y:
        return True
    return False

def spawn_mob():
    if len(mobs) < max_mobs:
        mob_type = random.choice(mob_types)
        mob_x = random.randint(0, WIDTH - mob_width)
        mob_y = random.randint(50, 150)
        mobs.append({"x": mob_x, "y": mob_y, "type": mob_type})

def spawn_powerup():
    powerup_type = random.choice(powerup_types)
    powerup_x = random.randint(0, WIDTH - powerup_width)
    powerup_y = random.randint(50, 150)
    powerups.append({"x": powerup_x, "y": powerup_y, "type": powerup_type})

running = True
is_sliding = False
slide_direction = None

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                is_sliding = True
                slide_direction = "LEFT"
            if event.key == pygame.K_RIGHT:
                is_sliding = True
                slide_direction = "RIGHT"
            if event.key == pygame.K_UP:
                is_sliding = True
                slide_direction = "UP"
            if event.key == pygame.K_DOWN:
                is_sliding = True
                slide_direction = "DOWN"

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT and slide_direction == "LEFT":
                is_sliding = False
            if event.key == pygame.K_RIGHT and slide_direction == "RIGHT":
                is_sliding = False
            if event.key == pygame.K_UP and slide_direction == "UP":
                is_sliding = False
            if event.key == pygame.K_DOWN and slide_direction == "DOWN":
                is_sliding = False
            if event.key == pygame.K_SPACE:
                if syringe_state == "ready":
                    syringe_x = player_x + (player_width - syringe_width) // 2
                    syringe_y = player_y - syringe_height
                    fire_syringe()

    # Handle sliding movement
    if is_sliding:
        if slide_direction == "LEFT":
            player_x -= player_speed
        if slide_direction == "RIGHT":
            player_x += player_speed
        if slide_direction == "UP":
            player_y -= player_speed
        if slide_direction == "DOWN":
            player_y += player_speed

    # Update player position
    if player_x < 0:
        player_x = 0
    elif player_x > WIDTH - player_width:
        player_x = WIDTH - player_width
    if player_y < 0:
        player_y = 0
    elif player_y > HEIGHT - player_height:
        player_y = HEIGHT - player_height

    # Update syringe position
    if syringe_state == "fire":
        syringe_y -= syringe_speed
        if syringe_y <= 0:
            syringe_state = "ready"

    # Update mobs
    for mob in mobs:
        mob["y"] += mob_speed
        if mob["y"] > HEIGHT:
            mobs.remove(mob)
            #if not round_over:
             #   player_health -= 10

        # Check for collision between syringe and mobs
        if syringe_state == "fire" and is_collision(syringe_x, syringe_y, syringe_width, syringe_height,
                                                   mob["x"], mob["y"], mob_width, mob_height):
            syringe_state = "ready"
            mobs.remove(mob)
            kills += 1

    # Check for collision between player and mobs
    for mob in mobs:
        if is_collision(player_x, player_y, player_width, player_height, mob["x"], mob["y"], mob_width, mob_height):
            player_health -= 5

    # Check for collision between player and power-ups
    for powerup in powerups:
        if is_collision(player_x, player_y, player_width, player_height, powerup["x"], powerup["y"], powerup_width, powerup_height):
            powerups.remove(powerup)
            if powerup["type"] == "mask":
                if player_health == max_health:
                    player_health += 20
            elif powerup["type"] == "hazmat":
                if player_health == max_health:
                    player_health += 50
            elif powerup["type"] == "cure":
                if player_health == max_health:
                    player_health += 100
            elif powerup["type"] == "grenade":
                if player_health == max_health:
                    player_health += 100
            elif powerup["type"] == "ammo":
                syringe_state = "ready"

    # Spawn mobs and power-ups
    if len(mobs) == 0 and not round_over:
        rounds += 1
        if rounds % 5 == 0:
            max_mobs += 1
            #mob_speed += 1
            mob_types.append("boss")
        for _ in range(wave):
            spawn_mob()
        if rounds % 3 == 0:
            spawn_powerup()
        round_over = True
    elif len(mobs) > 0:
        round_over = False

    # Game over condition
    if player_health <= 0:
        game_over = True

    # Clear the screen
    win.fill(WHITE)

    # Draw game objects
    draw_player()
    draw_syringe()
    for mob in mobs:
        draw_mob(mob["x"], mob["y"])
    for powerup in powerups:
        draw_powerup(powerup["x"], powerup["y"], powerup["type"])

    # Draw player health bar
    pygame.draw.rect(win, RED, (player_x, player_y - 10, player_health, 5))

    # Draw game information
    font = pygame.font.Font(None, 24)
    text = font.render(f"Wave: {wave} | Kills: {kills} | Rounds: {rounds}", True, RED)
    win.blit(text, (10, 10))

    # Update the display
    pygame.display.update()

# Quit the game
pygame.quit()
