#!/usr/bin/env python3
#
#   player_utils.py

import random
from copy import deepcopy
import numpy as np


#
#  Player (emulate player movement)
#


class Player():
    def __init__(self, identifier, players = [], obstacles=[], y=random.randrange(0, 50), x=random.randrange(0, 50), vely=0, velx=0,
                 radius=1, dt=.1, accel=.2, t=0,
                 color=tuple(random.sample([255, 0, 0], 3))):
        # Check the positional arguments.
        assert (y >= 0 + radius) and (y <= 50 - radius), "Illegal y"
        assert (x >= 0 + radius) and (x <= 50 - radius), "Illegal x"

        # Save the obstacles, the initial location, and the probabilities.
        self.dt = dt
        self.t = t
        self.y = y
        self.vely = vely
        self.x = x
        self.velx = velx
        self.accel = accel
        self.radius = radius
        self.identifier = identifier
        self.color = color

        # Pick a valid starting location (if not already given).
        invalid_starts = deepcopy(obstacles)
        invalid_starts.extend(players)
        while True:
            if not self.x or not self.y:
                self.y = random.randrange(0, 50)
                self.x = random.randrange(0, 50)
            counter = 0
            for obstacle in invalid_starts:
                if np.sqrt((self.x - obstacle.x) ** 2 + (self.y - obstacle.y) ** 2) <= obstacle.radius:
                    counter = counter + 1
            if counter == 0:
                break
            self.y = random.randrange(0, 50)
            self.x = random.randrange(0, 50)

    def Walk(self, players, obstacles):
        # player randomly walks
        y = self.y + self.vely * self.dt
        x = self.x + self.vely * self.dt

        if (y <= 0 + self.radius) or (y > 50 - self.radius):  # if its going to hit the wall, stop
            y = self.y
            self.vely = - self.vely
        if (x <= 0 + self.radius) or (x > 50 - self.radius):  # if its going to hit the wall, stop
            x = self.x
            self.velx = - self.velx
        target = [random.randrange(0, 50), random.randrange(0, 50)]

        invalid_objects = deepcopy(obstacles)
        invalid_objects.extend(players)
        for obstacle in invalid_objects : # if its going to hit the wall or another player, stop
            if np.sqrt((self.x - obstacle.x) ** 2 + (self.y - obstacle.y) ** 2) <= obstacle.radius:
                if obstacle.identifier >= 0:
                    Unfreeze(obstacle.identifier, players, obstacles)
                self.velx = -self.velx
                self.vely = -self.vely
                return

        while True: # if the target requires going through an obstacle, repick target
            counter = 0
            for obstacle in obstacles:
                if self.lineIntersectCircle(self.x, target[0], self.y, target[1], obstacle.x, obstacle.y,
                                        obstacle.radius):
                    counter = counter + 1
            if counter == 0:
                break 
            target = [random.randrange(0, 50), random.randrange(0, 50)]

        vely = self.vely + (y - target[1] + .25 * np.sign(
            y - target[1])) * self.accel * self.dt  # weighted velocity that weights to speed of .25
        velx = self.velx + (x - target[0] + .25 * np.sign(
            x - target[0])) * self.accel * self.dt  # weighted velocity that weights to speed of .25
        # velx = 0
        # vely = 0
        self.y = y
        self.x = x
        self.vely = vely
        self.velx = velx

    def lineIntersectCircle(self, x1, x2, y1, y2, cx, cy, r):
        return (abs((x2 - x1) * cx + (y1 - y2) * cy + (x1 - x2) * y1 + (y2 - y1) * x1) / np.sqrt(
            (x2 - x1) ** 2 + (y2 - y1) ** 2) <= r)

    def Unfreeze(self, identifier, players, obstacles):
        for obstacle in obstacles:
            if obstacle.identifier == identifier:
                players.append(obstacle)
                obstacles.remove(obstacles)

