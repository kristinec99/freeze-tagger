#!/usr/bin/env python3
#
#   player_utils.py

import matplotlib.pyplot as plt
import numpy as np
import random

#
#  Player (emulate player movement)
#
class Player():
    def __init__(self, identifier, obstacles = [], y = 25, x = 25, vely = 0, velx = 0, radius = 1, dt = .1, accel = .2, t = 0, color = tuple(random.sample([255,0,0],3))):
        # Check the positional arguments.
        assert (y >= 0 + radius) and (y < 50 - radius), "Illegal y"
        assert (x >= 0 + radius) and (x < 50- radius), "Illegal x"

        # Save the obstacles, the initial location, and the probabilities.
        self.dt             = dt
        self.t              = t
        self.obstacles      = obstacles
        self.y              = y
        self.vely           = vely
        self.x              = x
        self.velx           = velx
        self.accel          = accel
        self.radius         = radius
        self.identifier     = identifier
        self.color          = color

        # Pick a valid starting location (if not already given).
        while True:
            if not self.x or not self.y:
                self.y = random.randrange(0, 50)
                self.x = random.randrange(0, 50)
            counter = 0
            for obstacle in self.obstacles:
                if np.sqrt((self.x-obstacle.x)^2+(self.y-obstacle.y)^2) <= obstacle.radius:
                    counter = counter + 1
            if counter == 0:
                break
            self.y = random.randrange(0, 50)
            self.x = random.randrange(0, 50)
            
    def Walk(self):
        # player randomly walks
        y = self.y + self.vely * self.dt
        x = self.x + self.vely * self.dt

        # if (y <= 0 + self.radius) or (y > 50 - self.radius): #if its going to hit the wall, stop
        #     y = self.y
        #     self.vely = 0
        # if (x <= 0 + self.radius) or (x > 50 - self.radius): #if its going to hit the wall, stop
        #     x = self.x
        #     self.velx = 0

        # for obstacle in self.obstacles:
        #     while self.lineIntersectCircle(self.x, target[0], self.y, target[1], obstacle.x, obstacle.y, obstacle.radius):
        #         target = [random.randrange(0, 50), random.randrange(0, 50)]
        # vely = self.vely + (y-target[1] + .25 * np.sign(y-target[1]))  * self.accel * self.dt # weighted velocity that weights to speed of .25
        # velx = self.velx + (x-target[0] + .25 * np.sign(x-target[0]))  * self.accel * self.dt # weighted velocity that weights to speed of .25
        self.y = y, self.x = x, self.vely = vely, self.velx = velx

