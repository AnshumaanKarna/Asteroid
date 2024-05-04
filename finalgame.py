import pygame
import random
import math
import sys
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Asteroids")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)

# Fonts
font_title = pygame.font.Font(None, 64)
font_button = pygame.font.Font(None, 32)

# Load images
player_img = pygame.image.load('spaceship.png').convert_alpha()
player_img = pygame.transform.scale(player_img, (80, 60))
asteroid_img = pygame.image.load('asteroid.png').convert_alpha()
asteroid_img = pygame.transform.scale(asteroid_img, (50, 50))
laser_img = pygame.image.load('laser.png').convert_alpha()
laser_img = pygame.transform.scale(laser_img, (50, 30))

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.original_image = player_img
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.center = (screen_width // 2, screen_height // 2)
        self.angle = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.angle += 5
        if keys[pygame.K_RIGHT]:
            self.angle -= 5

        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def shoot(self):
        bullet = Bullet(self.rect.center, self.angle)
        all_sprites.add(bullet)
        bullets.add(bullet)

# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, angle):
        super().__init__()
        self.original_image = laser_img
        self.image = pygame.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect(center=pos)
        self.vel = pygame.math.Vector2(10, 0).rotate(-angle)

    def update(self):
        self.rect.move_ip(self.vel)

# Asteroid class
class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = asteroid_img
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.random_spawn()
        self.angle = random.randrange(360)
        self.vel = pygame.math.Vector2(random.uniform(1, 3), 0).rotate(-self.angle)

    def update(self):
        self.rect.move_ip(self.vel)

    def random_spawn(self):
        spawn_margin = 100
        while True:
            x = random.randrange(spawn_margin, screen_width - spawn_margin)
            y = random.randrange(spawn_margin, screen_height - spawn_margin)
            if math.hypot(x - screen_width // 2, y - screen_height // 2) > 150:
                return x, y

# Create sprites
player = Player()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
bullets = pygame.sprite.Group()
asteroids = pygame.sprite.Group()

# Welcome page function
def welcome_page():
    welcome = True

    while welcome:
        screen.fill(BLACK)

        title_text = font_title.render("Asteroids Game", True, WHITE)
        title_rect = title_text.get_rect(center=(screen_width // 2, screen_height // 4))
        screen.blit(title_text, title_rect)

        start_button = font_button.render("Start Game", True, WHITE)
        start_button_rect = start_button.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(start_button, start_button_rect)

        exit_button = font_button.render("Exit Game", True, WHITE)
        exit_button_rect = exit_button.get_rect(center=(screen_width // 2, screen_height // 2 + 50))
        screen.blit(exit_button, exit_button_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if start_button_rect.collidepoint(mouse_x, mouse_y):
                    welcome = False
                elif exit_button_rect.collidepoint(mouse_x, mouse_y):
                    pygame.quit()
                    sys.exit()

# Game loop
clock = pygame.time.Clock()
score = 0
game_over = False

# Function to display loss message
def display_loss_message():
    loss_text = font_title.render("YOU LOST", True, RED)
    loss_rect = loss_text.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(loss_text, loss_rect)
    pygame.display.flip()
    pygame.time.delay(2000)  # Display message for 4 seconds
    ask_quit()

# Function to display quit option
def ask_quit():
    screen.fill(BLACK)

    quit_button = font_button.render("Quit", True, WHITE)
    quit_button_rect = quit_button.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(quit_button, quit_button_rect)

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if quit_button_rect.collidepoint(mouse_x, mouse_y):
                    pygame.quit()
                    sys.exit()

# Spawn asteroids
def spawn_asteroid():
    asteroid = Asteroid()
    all_sprites.add(asteroid)
    asteroids.add(asteroid)
    pygame.time.set_timer(USEREVENT + 1, random.randint(1000, 3000))  # Reschedule spawning

# Welcome page
welcome_page()
spawn_asteroid()  # Initial asteroid spawn

# Game loop function
def game_loop():
    global score, game_over
    while not game_over:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    player.shoot()
            elif event.type == USEREVENT + 1:
                spawn_asteroid()

        screen.fill((0, 0, 0))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.angle += 5
        if keys[pygame.K_RIGHT]:
            player.angle -= 5

        player.image = pygame.transform.rotate(player_img, player.angle)
        player.rect = player.image.get_rect(center=player.rect.center)

        all_sprites.update()

        # Check for collisions
        hits = pygame.sprite.groupcollide(asteroids, bullets, True, True)
        for hit in hits:
            score += 1
            spawn_asteroid()

        hits = pygame.sprite.spritecollide(player, asteroids, True)
        if hits:
            game_over = True
            display_loss_message()  # Display loss message

        all_sprites.draw(screen)

        # Display score
        font = pygame.font.Font(None, 36)
        text = font.render("Score: " + str(score), True, WHITE)
        screen.blit(text, (10, 10))

        pygame.display.flip()
        clock.tick(60)

    # Show exit option
    ask_quit()

# Start the game loop
game_loop()
