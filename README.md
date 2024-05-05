
Asteroid Blaster is a Pygame rendition of the classic arcade game 'Asteroids'. In this pygame version, the player navigates through the asteroid field only by rotating the ship and attacking the asteroids by firing lasers.
The game ends when the player ship gets hit by an asteroid. The aim is to survive as long as possible, and score the most.


![Python 3 11 04-05-2024 22_11_04](https://github.com/AnshumaanKarna/Asteroid/assets/168951565/47e6c1fd-940c-4d4b-b2f6-bfc75130b741)


This project consists of two Python files:

finalgame.py: Contains the final version of the Asteroids Game.

training.py: Implements Q-learning to train an AI agent to play the Asteroid Blaster Game.





LEARNING APPROACH: The goal of the project is to develop an AI agent capable of playing a simplified version of the classic arcade game "Asteroids". The agent must learn to navigate a spaceship within an environment populated by moving asteroids and shoot them down while avoiding collisions, for this the training.py file was created that provides a separate game environment for the agent to train in. The agent plays the game in this game environment.
The project utilizes Q-learning, a model-free reinforcement learning algorithm. In this approach, the agent learns a policy by iteratively updating Q-values for state-action pairs based on the observed rewards.




STATE REPRESENATION: The state space is represented by a five-dimensional vector, including the player's x and y positions, the player's angle, and the positions of the closest asteroid relative to the player's position.




ACTION SPACE: The agent has three possible actions:
Rotate the spaceship left
Rotate the spaceship right
Fire a bullet




REWARD FUNTION: The reward function gives the spaceship points for shooting asteroids and avoiding crashes. The closer the spaceship gets to an asteroid, the fewer points it gets, encouraging the spaceship to stay safe while shooting.


![finalgame py - Visual Studio Code 04-05-2024 22_51_03](https://github.com/AnshumaanKarna/Asteroid/assets/168951565/c29bfe15-c535-4ad5-83cb-29ce79467974)



TRAINING AND TESTING: The agent undergoes training episodes where it interacts with the environment, updating Q-values based on observed rewards. Training continues until the agent converges to an optimal policy. The agent's ability to navigate the environment, shoot asteroids, and avoid collisions is assessed based on its behavior during testing.


![gamegame py - Visual Studio Code 04-05-2024 22_54_27](https://github.com/AnshumaanKarna/Asteroid/assets/168951565/dbab12a2-456f-4293-8b27-34fd13475f27)
