import numpy as np
import pygame
import sys
import random
import time

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
        self.num_actions = 2  

        self.player_x = self.screen_width // 2
        self.player_y = self.screen_height // 2
        self.player_angle = 0
        self.bullet_speed = 10
        self.asteroids = []  
        self.bullets = []  

        self.state_dim = 5 
        self.action_dim = self.num_actions

        self.num_states = 10 ** self.state_dim  

        self.agent = QLearningAgent(self.num_actions, self.num_states)

        
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Asteroids Game')

        self.last_spawn_time = time.time()

    def reset(self):
        self.player_x = self.screen_width // 2
        self.player_y = self.screen_height // 2
        self.player_angle = 0
        self.asteroids = [] 
        self.bullets = [] 
      
        for _ in range(5):  
            self.spawn_asteroid()
        return self.get_state()

    def get_state(self):
        closest_asteroid = self.get_closest_asteroid()
        return np.array([
            self.player_x / self.screen_width,
            self.player_y / self.screen_height,
            self.player_angle / 360,
            closest_asteroid[0] / self.screen_width,
            closest_asteroid[1] / self.screen_height
        ])

    def step(self, action):
        if action == 0:  
            self.player_angle += 5
        elif action == 1:  
            self.fire_bullet()
        self.player_x += np.cos(np.radians(self.player_angle))
        self.player_y += np.sin(np.radians(self.player_angle))

        for asteroid in self.asteroids:
            asteroid[0] -= 1  
        for bullet in self.bullets:
            bullet[0] += self.bullet_speed * np.cos(np.radians(bullet[2]))
            bullet[1] += self.bullet_speed * np.sin(np.radians(bullet[2]))

        reward = self.calculate_reward()
        done = self.check_termination()
        for bullet in self.bullets:
            for asteroid in self.asteroids:
                if np.sqrt((bullet[0] - asteroid[0]) ** 2 + (bullet[1] - asteroid[1]) ** 2) < 10:  
                    self.bullets.remove(bullet)
                    self.asteroids.remove(asteroid)
                    reward += 10  

        next_state = self.get_state()
        self.agent.update_q_value(self.get_state_index(), action, reward, self.get_state_index(next_state))

        return next_state, reward, done

    def calculate_reward(self):
        closest_asteroid = self.get_closest_asteroid()
        distance_to_asteroid = np.sqrt((self.player_x - closest_asteroid[0]) ** 2 + (self.player_y - closest_asteroid[1]) ** 2)
        return 1 - distance_to_asteroid / np.sqrt(self.screen_width ** 2 + self.screen_height ** 2) 

    def check_termination(self):
        player_rect = pygame.Rect(self.player_x - 10, self.player_y - 10, 20, 20)
        for asteroid in self.asteroids:
            asteroid_rect = pygame.Rect(asteroid[0] - 5, asteroid[1] - 5, 10, 10)
            if player_rect.colliderect(asteroid_rect):
                return True 
        return False

    def get_closest_asteroid(self):
        if not self.asteroids:
            return [0, 0] 
        return min(self.asteroids, key=lambda x: np.sqrt((self.player_x - x[0]) ** 2 + (self.player_y - x[1]) ** 2))

    def spawn_asteroid(self):
        min_distance_from_edge = 50
        x = random.randint(min_distance_from_edge, self.screen_width - min_distance_from_edge)
        y = random.randint(min_distance_from_edge, self.screen_height - min_distance_from_edge)
        self.asteroids.append([x, y])

    def get_state_index(self, state=None):
        if state is None:
            state = self.get_state()
        state_index = int(sum(coord * 10**i for i, coord in enumerate(state))) 
        return np.clip(state_index, 0, self.num_states - 1) 

    def fire_bullet(self):
        self.bullets.append([self.player_x, self.player_y, self.player_angle])

    def render(self):
        self.screen.fill((0, 0, 0)) 

        player_rect = pygame.Rect(self.player_x - 10, self.player_y - 10, 20, 20)
        pygame.draw.rect(self.screen, (255, 255, 255), player_rect)
   
        for asteroid in self.asteroids:
            asteroid_rect = pygame.Rect(asteroid[0] - 5, asteroid[1] - 5, 10, 10)
            pygame.draw.rect(self.screen, (255, 255, 255), asteroid_rect)

        for bullet in self.bullets:
            bullet_rect = pygame.Rect(bullet[0] - 2, bullet[1] - 2, 4, 4)
            pygame.draw.rect(self.screen, (255, 255, 255), bullet_rect)
        pygame.display.flip()

    def spawn_asteroid_timer(self):
        if time.time() - self.last_spawn_time >= 2:
            self.spawn_asteroid()
            self.last_spawn_time = time.time()

env = AsteroidsEnvironment()

num_episodes = 1000
for episode in range(num_episodes):
    state = env.reset()
    done = False
    while not done:
        action = env.agent.select_action(env.get_state_index())
        next_state, reward, done = env.step(action)
        env.render()
        env.spawn_asteroid_timer()  # Call the asteroid spawning timer function
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        env.clock.tick(60) 
