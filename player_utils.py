#!/usr/bin/env python3
#
#   player_utils.py

import random
from copy import copy
import numpy as np
import time
from game_config import *

#
#  Player (emulate player movement)
#

class Player():
    def __init__(self, identifier, players = [], obstacles=[], y=random.randrange(0, N), x=random.randrange(0, M), vely=.1, velx=.1,
                 radius=radius, dt=dt, accel=.05, t=0,
                 color=tuple(random.sample([255, 0, 0], 3)), sample=5, T=10):
        # Check the positional arguments.
        assert (y >= 0 + radius) and (y <= N - radius), "Illegal y"
        assert (x >= 0 + radius) and (x <= M - radius), "Illegal x"

        # Save the obstacles, the initial location, and the probabilities.
        self.dt = dt
        self.t = t
        self.y = y
        self.vely = vely
        self.x = x
        self.velx = velx
        self.accelx = accel
        self.accely = accel
        self.radius = radius
        self.identifier = identifier
        self.color = color
        self.froze = False
        self.obstacled = False
        self.target = [random.randrange(0 + self.radius*2, M - self.radius*2), random.randrange(0 + self.radius*2, N - self.radius*2)]   
        self.target_identifier = -100
        self.sample = sample
        self.T = T

        # Pick a valid starting location (if not already given).
        invalid_starts = copy(obstacles)
        invalid_starts.extend(players)
        while True:
            if not self.x or not self.y:
                self.y = random.randrange(0 + self.radius*2, M - self.radius*2)
                self.x = random.randrange(0 + self.radius*2, N - self.radius*2)
            counter = 0
            for obstacle in invalid_starts:
                if np.sqrt((self.x - obstacle.x) ** 2 + (self.y - obstacle.y) ** 2) <= obstacle.radius + self.radius:
                    counter = counter + 1
            if counter == 0:
                break
                self.y = random.randrange(0 + self.radius*2, M - self.radius*2)
                self.x = random.randrange(0 + self.radius*2, N - self.radius*2)

    def Walk(self, players, obstacles, current_players, robot, frozen_players):
        # Player randomly walks
        if self.froze:
            if np.sqrt((self.x - robot.x) ** 2 + (self.y - robot.y) ** 2) > self.radius + robot.radius and not self.obstacled:
                obstacles.append(self)
                self.obstacled = True
            return(current_players, frozen_players)
        y = self.y + self.vely * self.dt
        x = self.x + self.velx * self.dt
    
        if not self.target:
                self.target = [random.randrange(0 + self.radius*2, M - self.radius*2), random.randrange(0 + self.radius*2, N - self.radius*2)]


        # If it's going to hit the wall, bounce off
        if (y <= 0 + self.radius) or (y > M - self.radius): 
            y = self.y
            self.vely = - self.vely
        if (x <= 0 + self.radius) or (x > N - self.radius):  
            x = self.x
            self.velx = - self.velx
            
        obstructions = copy(obstacles)
        obstructions.extend(players)
        
        # Once we get close to the target, pick a new one to move towards
        if self.pointIntersectCircle(x, y, self.target[0], self.target[1], self.radius + 0.1):           
            self.target = [random.randrange(0 + self.radius*2, M - self.radius*2), random.randrange(0 + self.radius*2, N - self.radius*2)]   
            self.target_identifier = -100
            if frozen_players and random.choice([1,2,3,4]) == 1:
                # tag closest player
                dist = 1000
                for player in frozen_players:
                    if ((x-player.x)**2+(y-player.y)**2) < dist:
                        self.target = [player.x, player.y]
                        dist = ((x-player.x)**2+(y-player.y)**2)
                        self.target_identifier = player.identifier

                # tag farthest player from robot
                # dist = 0
                # for player in frozen_players:
                #     if ((robot.x-player.x)**2+(robot.y-player.y)**2) + ((x-player.x)**2+(y-player.y)**2) > dist:
                #         self.target = [player.x, player.y]
                #         dist = ((robot.x-player.x)**2+(robot.y-player.y)**2) + ((x-player.x)**2+(y-player.y)**2)
                #         self.target_identifier = player.identifier
        
        
        for obstacle in obstructions: # if its going to hit another player or obstacle, bounce back
            if self.pointIntersectCircle(x, y, obstacle.x, obstacle.y, obstacle.radius + self.radius) and obstacle.identifier != self.identifier:
                if obstacle.identifier >= 0 and obstacle.froze == True:
                    current_players, frozen_players = self.Unfreeze(obstacle.identifier, obstacles, current_players, frozen_players)
                    return(current_players, frozen_players)

                self.velx = -self.velx
                self.vely = -self.vely
                return(current_players, frozen_players)
        
        # If the target requires going through an obstacle or another player, repick target
        counter = 0
        for obstacle in obstructions:
            if obstacle.identifier not in [self.identifier, self.target_identifier] and self.lineIntersectCircle(obstacle.radius + self.radius, (obstacle.x, obstacle.y), (x,y), (self.target[0], self.target[1])):
                counter = counter + 1
                break
        target = self.target
        if counter != 0:
            targets = []
            while len(targets) <= self.sample:
                target_choice = [random.randrange(max(round(x - self.radius*5), 0 + self.radius), min(round(x + self.radius*5), N - self.radius)), 
                        random.randrange(max(round(y - self.radius*5), 0 + self.radius), min(round(y + self.radius*5), M - self.radius))]
                counter = 0
                for obstacle in obstructions:
                    if obstacle.identifier not in [self.identifier, self.target_identifier] and self.lineIntersectCircle(obstacle.radius + self.radius, (obstacle.x, obstacle.y), (x,y), (target_choice[0], target_choice[1])):
                        counter = counter + 1
                        break
                if counter == 0:
                    targets.append(target_choice)
            target = targets[0]
            for target_choice in targets:
                if ((self.target[0]  - target_choice[0])**2 + (self.target[1] - target_choice[1])**2) < ((self.target[0] - target[0])**2 + (self.target[1] - target[1])**2):
                    target = target_choice
        self.accelx = (2/T * (0 - self.velx) + 1/T**2 * (target[0] - self.x))
        self.accely = (2/T * (0 - self.vely) + 1/T**2 * (target[1] - self.y))
        vely = self.vely + self.accely * self.dt  # weighted acceleration
        velx = self.velx + self.accelx * self.dt  # weighted acceleration
        self.y = y
        self.x = x
        self.vely = vely
        self.velx = velx
        return(current_players, frozen_players)

    # def lineIntersectCircle(self, x1, x2, y1, y2, cx, cy, r):
    #     return (abs((x2 - x1) * cx + (y1 - y2) * cy + (x1 - x2) * y1 + (y2 - y1) * x1) / np.sqrt(
    #         (x2 - x1) ** 2 + (y1 - y2) ** 2) <= r)

    #   Proximity of Point to Segment
    def lineIntersectCircle(self, d, p, q1, q2):
        # Precompute the relative vectors.
        (rx, ry) = ( p[0]-q1[0],  p[1]-q1[1])
        (vx, vy) = (q2[0]-q1[0], q2[1]-q1[1])

        # Precompute the vector products.
        rTv = rx*vx + ry*vy
        rTr = rx**2 + ry**2
        vTv = vx**2 + vy**2

        # Check the point-to-point distance when outside the segment range.
        if (rTv <= 0):
            return (rTr <= d**2)
        if (rTv >= vTv):
            return (rTr - 2*rTv + vTv <= d**2)

        # Check the orthogonal point-to-line distance inside the segment range.
        return ((rx*vy - ry*vx)**2 <= vTv * d**2)

    def pointIntersectCircle(self, x, y, cx, cy, r):
        return (np.sqrt((x - cx) ** 2 + (y - cy) ** 2) <= r)

    def Unfreeze(self, identifier, obstacles, current_players, frozen_players):
        for obstacle in obstacles:
            if obstacle.identifier == identifier:
                for player in frozen_players:
                    if player.identifier == identifier:
                        frozen_players.remove(player)
                obstacle.froze = False
                obstacle.obstacled = False
                obstacles.remove(obstacle)
                current_players = current_players + 1
                return(current_players, frozen_players)
        return(current_players, frozen_players)