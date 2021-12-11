import pygame
import sys
import os
from pygame.locals import *
import random
import numpy as np

# Init pygame
pygame.init()
font = pygame.font.Font('arial.ttf', 25)
clock = pygame.time.Clock()

# CHANGABLE VARIABLES
sw = 600
sh = 300
screen = pygame.display.set_mode((sw, sh))
framerate = 60
bg_speed = 100
start_height = 50
fall_speed = 2
jump_height = 50
multiplier = 1

# COLORS
BLUE = (0, 100, 255)  # BLUE
BLACK = (0, 0, 0)


# Don't really touch the rest here
bg = pygame.image.load(os.path.join("./images", "background.jpg"))

# Pillar settings


class Pillars:
    # Pillar class holds an array of pillars, and deletes them when they reach the end of the screen
    def __init__(self):
        self.pillars = []

    # Adding pillars at the right edge of the screen.

    def Add(self, pillar):
        self.pillars.append([pillar, 600])

    # Display the pillar with multiple rectangles
    def Show(self):
        for pillar, pos_x in self.pillars:
            for index, i in enumerate(pillar):
                if i == 1:
                    pygame.draw.rect(
                        screen, BLUE, pygame.Rect(pos_x, index, 20, 1))

    # Shifting the pillars every frame

    def Shift(self):
        for index, pillar in enumerate(self.pillars):
            pillar[1] -= bg_speed/50
            if pillar[1] < 0:
                self.pillars.pop(0)


class ScrollingBackground:

    # Actually this is not really necessary, I just wanted a scrollable background

    def __init__(self, sw, imagefile):
        pygame.mouse.set_visible(0)
        pygame.display.set_caption('Birb')
        self.img = pygame.image.load(imagefile)
        self.coord = [0, 0]
        self.coord2 = [sw, 0]
        self.x_original = self.coord[0]
        self.x2_original = self.coord2[0]

    # Updates coordinates per frame

    def UpdateCoords(self, speed_x, time):
        distance_x = speed_x * time
        self.coord[0] -= distance_x
        self.coord2[0] -= distance_x
        if self.coord2[0] <= 0:
            self.coord[0] = self.x_original
            self.coord2[0] = self.x2_original

    # Re-renders the background every frame

    def Show(self, surface):
        surface.blit(self.img, self.coord)
        surface.blit(self.img, self.coord2)


class Birb:

    # Birb sprite

    def __init__(self, sh, imagefile):
        img = pygame.image.load(imagefile)
        # Height of our birb is 25px
        self.shape = pygame.transform.scale(img, (30, 25))
        self.top = start_height

    # Re-render birb every frame

    def Show(self, surface):
        surface.blit(self.shape, (50, self.top))

    # Natural fall of birb

    def Fall(self):
        self.top += fall_speed

    # Birb jumps and goes up a certain amount.

    def Jump(self):
        self.top -= jump_height


# Initialising our variables

pillars = Pillars()
game = ScrollingBackground(sw, "./images/background.jpg")
birb = Birb(sh, "./images/birb.png")

# Main class of our birb game


class BirbGame:
    # Birbgame consists of iteration number (so we can output pillars at regular intervals) and a score.
    def __init__(self):
        self.step_iter = 0
        self.score = 0

    # Causes a new pillar to be generated

    def _new_pillar(self):
        top = random.randint(5, 20) * 10
        pillar = np.array([1] * 300)
        pillar[top:top+70] = 0
        pillars.Add(pillar)

    # Main bulk of the logic is here - it checks for basically everything at every step of the game.

    def game_step(self):

        # Checking whether the spacebar is pressed. If pressed, birbby will jump

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    birb.Jump()

        # So basically, every step we take, the game will cause birb to fall, update background, re-render birb
        # re-render background, re-render pillar, and cause the pillar to move.

        birb.Fall()
        game.UpdateCoords(bg_speed, time)
        game.Show(screen)
        birb.Show(screen)
        pillars.Show()
        pillars.Shift()

        # Checks if there is a collision.

        game_over = self._is_collision()

        # Every step taken, iteration will increase

        self.step_iter += 1

        # Generates a new pillar every 100 iterations

        if self.step_iter % 100 == 0:
            self._new_pillar()

        # Scoreboard

        text = font.render(str(self.score), True, BLACK)
        screen.blit(text, [300, 0])
        return game_over, self.score

    # Collision logic, we consider collide if birbby drops out of screen, or if pillar is hit.
    # For easier playing, we only consider top 5 pixels of birb to be hitbox.

    def _is_collision(self):
        if pillars.pillars:
            if 20 < pillars.pillars[0][1] < 50:
                if pillars.pillars[0][0][birb.top] == 1 or pillars.pillars[0][0][birb.top + 5] == 1:
                    return True
            elif pillars.pillars[0][1] == 20:
                self.score += 1
        if birb.top > sh:
            return True
        if birb.top < 0:
            return True
        return False


birbgame = BirbGame()

while True:
    time = clock.tick(framerate)/1000
    screen.blit(bg, (0, 0))
    game_over, score = birbgame.game_step()
    # Print game over in terminal once game is over.
    if game_over == True:
        print('Game over. Your score is: ' + str(score))
        sys.exit()
    pygame.display.update()
