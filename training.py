import numpy as np
import pygame
import sys
import random

class QLearningAgent:
    def __init__(self, num_actions, num_states, learning_rate=0.1, discount_factor=0.99, epsilon=0.1):
        self.num_actions = num_actions
        self.num_states = num_states
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.Q = np.zeros((num_states, num_actions))

    def select_action(self, state):
        if np.random.rand() < self.epsilon:
            return np.random.choice(self.num_actions)
        else:
            return np.argmax(self.Q[state])

    def update_q_value(self, state, action, reward, next_state):
        best_next_action = np.argmax(self.Q[next_state])
        td_target = reward + self.discount_factor * self.Q[next_state, best_next_action]
        td_error = td_target - self.Q[state, action]
        self.Q[state, action] += self.learning_rate * td_error

class AsteroidsEnvironment:
    def __init__(self):
        self.screen_width = 800
        self.screen_height = 600
        self.num_actions = 2  # Rotation and Fire

        # Define state space dimensions
        self.player_x = self.screen_width // 2
        self.player_y = self.screen_height // 2
        self.player_angle = 0
        self.bullet_speed = 10
        self.asteroids = []  # List of asteroid positions
        self.bullets = []  # List of bullet positions

        self.state_dim = 5  # Player X, Player Y, Player Angle, Asteroid X, Asteroid Y
        self.action_dim = self.num_actions

        # Calculate num_states based on discretization levels
        self.num_states = 10 ** self.state_dim  # Assuming 10 discretization levels for each dimension

        # Initialize Q-learning agent
        self.agent = QLearningAgent(self.num_actions, self.num_states)

        # Initialize Pygame
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Asteroids Game')

    def reset(self):
        # Reset player and asteroids positions
        self.player_x = self.screen_width // 2
        self.player_y = self.screen_height // 2
        self.player_angle = 0
        self.asteroids = []  # Reset asteroids
        self.bullets = []  # Reset bullets
        # Add initial asteroids
        for _ in range(5):  # Randomly spawn 5 asteroids at the beginning
            self.spawn_asteroid()
        # Return initial state
        return self.get_state()

    def get_state(self):
        # Return current state
        closest_asteroid = self.get_closest_asteroid()
        return np.array([
            self.player_x / self.screen_width,
            self.player_y / self.screen_height,
            self.player_angle / 360,
            closest_asteroid[0] / self.screen_width,
            closest_asteroid[1] / self.screen_height
        ])

    def step(self, action):
        # Execute action and return next state, reward, done flag
        if action == 0:  # Rotation
            self.player_angle += 5
        elif action == 1:  # Fire
            self.fire_bullet()

        # Update player position
        self.player_x += np.cos(np.radians(self.player_angle))
        self.player_y += np.sin(np.radians(self.player_angle))

        # Update asteroids
        for asteroid in self.asteroids:
            asteroid[0] -= 1  # Update asteroid x position

        # Update bullets
        for bullet in self.bullets:
            bullet[0] += self.bullet_speed * np.cos(np.radians(bullet[2]))
            bullet[1] += self.bullet_speed * np.sin(np.radians(bullet[2]))

        # Check for collisions, calculate reward
        reward = self.calculate_reward()
        done = self.check_termination()

        # Collision detection between bullets and asteroids
        for bullet in self.bullets:
            for asteroid in self.asteroids:
                if np.sqrt((bullet[0] - asteroid[0]) ** 2 + (bullet[1] - asteroid[1]) ** 2) < 10:  # Assuming asteroid size is 10
                    self.bullets.remove(bullet)
                    self.asteroids.remove(asteroid)
                    reward += 10  # Increment reward for destroying an asteroid

        # Update Q-value
        next_state = self.get_state()
        self.agent.update_q_value(self.get_state_index(), action, reward, self.get_state_index(next_state))

        return next_state, reward, done

    def calculate_reward(self):
        # Calculate reward based on game state
        closest_asteroid = self.get_closest_asteroid()
        distance_to_asteroid = np.sqrt((self.player_x - closest_asteroid[0]) ** 2 + (self.player_y - closest_asteroid[1]) ** 2)
        return 1 - distance_to_asteroid / np.sqrt(self.screen_width ** 2 + self.screen_height ** 2)  # Reward proportional to distance from closest asteroid

    def check_termination(self):
        # Check if episode should terminate
        player_rect = pygame.Rect(self.player_x - 10, self.player_y - 10, 20, 20)
        for asteroid in self.asteroids:
            asteroid_rect = pygame.Rect(asteroid[0] - 5, asteroid[1] - 5, 10, 10)
            if player_rect.colliderect(asteroid_rect):
                return True  # Terminate episode if player collides with an asteroid
        return False

    def get_closest_asteroid(self):
        # Return position of closest asteroid
        if not self.asteroids:
            return [0, 0]  # No asteroids, return arbitrary position
        return min(self.asteroids, key=lambda x: np.sqrt((self.player_x - x[0]) ** 2 + (self.player_y - x[1]) ** 2))

    def spawn_asteroid(self):
        # Spawn a new asteroid at a random position within the game screen
        x = random.randint(0, self.screen_width)
        y = random.randint(0, self.screen_height)
        self.asteroids.append([x, y])

    def get_state_index(self, state=None):
        # Get index of state in the Q-table
        if state is None:
            state = self.get_state()
        state_index = int(sum(coord * 10**i for i, coord in enumerate(state)))  # Discretize state for Q-table indexing
        return np.clip(state_index, 0, self.num_states - 1)  # Clip state index to ensure it's within bounds

    def fire_bullet(self):
        # Add a new bullet to the bullets list
        self.bullets.append([self.player_x, self.player_y, self.player_angle])

    def render(self):
        # Render the game state
        self.screen.fill((0, 0, 0))  # Clear the screen
        # Render player
        player_rect = pygame.Rect(self.player_x - 10, self.player_y - 10, 20, 20)
        pygame.draw.rect(self.screen, (255, 255, 255), player_rect)
        # Render asteroids
        for asteroid in self.asteroids:
            asteroid_rect = pygame.Rect(asteroid[0] - 5, asteroid[1] - 5, 10, 10)
            pygame.draw.rect(self.screen, (255, 255, 255), asteroid_rect)
        # Render bullets
        for bullet in self.bullets:
            bullet_rect = pygame.Rect(bullet[0] - 2, bullet[1] - 2, 4, 4)
            pygame.draw.rect(self.screen, (255, 255, 255), bullet_rect)
        # Update display
        pygame.display.flip()

# Create Asteroids environment
env = AsteroidsEnvironment()

# Training loop
num_episodes = 1000
for episode in range(num_episodes):
    state = env.reset()
    done = False
    while not done:
        action = env.agent.select_action(env.get_state_index())
        next_state, reward, done = env.step(action)
        env.render()  # Render the game state
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        env.clock.tick(60)  # Cap the frame rate to 60 FPS

