#!/usr/bin/env python3
#
#   player_utils.py

import random
from copy import copy
import numpy as np
import time

#
#  Player (emulate player movement)
#

M = 100
N = 100

class Player():
    def __init__(self, identifier, players = [], obstacles=[], y=random.randrange(0, N), x=random.randrange(0, M), vely=0, velx=0,
                 radius=1, dt=.1, accel=.05, t=0,
                 color=tuple(random.sample([255, 0, 0], 3))):
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
        self.accel = accel
        self.radius = radius
        self.identifier = identifier
        self.color = color
        self.froze = False
        self.target = [random.randrange(0 + self.radius*2, M - self.radius*2), random.randrange(0 + self.radius*2, N - self.radius*2)]   
        self.freezetime = 0

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

    def Walk(self, players, obstacles, current_players):
        # Player randomly walks
        if self.froze:
            if self.t == self.freezetime:
                obstacles.append(self)
            return(current_players)
        y = self.y + self.vely * self.dt
        x = self.x + self.velx * self.dt

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
        if self.pointIntersectCircle(x, y, self.target[0], self.target[1], self.radius + 1):
            self.target = [random.randrange(0 + self.radius*2, M - self.radius*2), random.randrange(0 + self.radius*2, N - self.radius*2)]   
        
        for obstacle in obstructions: # if its going to hit another player or obstacle, bounce back
            if self.pointIntersectCircle(x, y, obstacle.x, obstacle.y, obstacle.radius + self.radius) and obstacle.identifier != self.identifier:
                # if obstacle.identifier >= 0 and obstacle.froze == True:
                    # current_players = self.Unfreeze(obstacle.identifier, players, obstacles, current_players)
                    # return(current_players)

                self.velx = -self.velx
                self.vely = -self.vely
                return(current_players)
        
        # If the target requires going through an obstacle or another player, repick target
        while True: 
            counter = 0
            for obstacle in obstructions:
                # Checks if the player's path to its target goes through an obstacle
                if obstacle.identifier != self.identifier and self.lineIntersectCircle(obstacle.radius + self.radius, (obstacle.x, obstacle.y), (x,y), (self.target[0], self.target[1])):
                    counter = counter + 1
                    print(f"path of {self.color} at position ({self.x}, {self.y}) with target ({self.target[0]}, {self.target[1]}) intersects with obstacle {obstacle.color} at position ({obstacle.x}, {obstacle.y})")
                # If the player position is inside an obstacle, move away
                if obstacle.identifier != self.identifier and self.pointIntersectCircle(x, y, obstacle.x, obstacle.y, obstacle.radius + self.radius):
                    print(f"{self.color} intersects with obstacle color {obstacle.color}")
            if counter == 0:
                break
            self.target = [random.randrange(max(round(x - self.radius*5), 0 + self.radius), min(round(x + self.radius*5), N - self.radius)), 
                           random.randrange(max(round(y - self.radius*5), 0 + self.radius), min(round(y + self.radius*5), M - self.radius))]
            

        

        # while True: 
        #     counter = 0
        #     for obstacle in invalid_target:
        #         if obstacle.identifier != self.identifier and self.lineIntersectCircle(self.x, self.target[0], 
        #             self.y, self.target[1], obstacle.x, obstacle.y, obstacle.radius):
        #             counter = counter + 1
        #             break
        #     if counter == 0:
        #         break 
        #     self.target = [random.randrange(0 + self.radius*2, N - self.radius*2), random.randrange(0 + self.radius*2, M - self.radius*2)]   
            

        vely = self.vely + (-y + self.target[1] + 1 * np.sign(
            y - self.target[1])) * self.accel * self.dt  # weighted acceleration
        velx = self.velx + (-x + self.target[0] + 1 * np.sign(
            x - self.target[0])) * self.accel * self.dt  # weighted acceleration
        # velx = 0
        # vely = 0
        self.y = y
        self.x = x
        self.vely = vely
        self.velx = velx
        return(current_players)

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

    def Unfreeze(self, identifier, players, obstacles, current_players):
        for obstacle in obstacles:
            if obstacle.identifier == identifier:
                print(identifier)
                obstacle.froze == False
                obstacles.remove(obstacle)
                current_players = current_players + 1
                return(current_players)
        return(current_players)