# MLDA Project - Flappy bird AI (Reinforcement learning)

## Description

This is an AI made to play Flappy Bird. The Flappy Bird game was designed ourselves with images sourced online.

## Components

### [Game]('./birbgame/b_orig.py)

There are 2 versions of the game - one for users and one for the agent (agent is the AI playing the game). The main difference is the agent controls the bird in a different way and doesn't use the keyboard.

The bird has a natural falling speed and is able to go up a certain distance when jumping (spacebar for user). The bird dies if it crosses the top of the screen, falls out of the screen, or hits a pillar.

For the user, they earn points for crossing pillars. For the agent, they earn points for crossing pillars as well as survival time.

### [Model]('./birbgame/model.py)

The model consists of the Linear Deep Q Network as well as the Deep Q Trainer. The Deep Q Network only consists of 2 linear layers and a forward step while the Deep Q Trainer is able to train the model for each step the game/agent takes.

### [Agent]('./birbgame/agent.py)

The agent is initialized with the following properties:

1. n_games: The number of games
2. epsilon: Chance variable (if roll lower than epsilon, take random route. If high roll, take safe route)
3. gamma: The state distance multiplier (states further from current get less accounted for)
4. memory: state memory
5. model: Deep Q Model from above
6. trainer: Deep Q Trainer from above

The agent basically loops the following actions:

1. Get the previous state
2. Decide on next action
3. Calculate reward for doing action
4. Get new state
5. Train short memory
6. Add states, move, rewards to memory

When the current game ends, the agent trains long memory.

The agent also uses the helper function to plot graphs.

### Image sources

- [bg](https://depositphotos.com/vector-images/game-background.html)
- [birb](https://www.nicepng.com/ourpic/u2e6t4a9q8w7u2r5_chick-chicken-little-small-chick-yellow-cute-bird/)

### Video inspiration

Most of the ideas behind the program was adapted from this [snake game](https://www.youtube.com/watch?v=PJl4iabBEz0).
