#!/usr/bin/env python3
#
#   robot_utilities.py
#
#
#     robot = Robot(walls, row=0, col=0, probCmd=1.0, probProximal=[1.0])
#     robot.Command(drow, dcol)
#     True/False = robot.Sensor(drow, dcol)
#     (row, col) = robot.Position()
#
#   Simulate a robot, to give us the sensor readings.  If the starting
#   x,y are not given, pick them randomly.  Note both the command
#   and the sensor may be configured to a random probability level.
#
#  The variables are:
#
#   obstacles     List of Lists containing obstacle point and radius
#
#   probCmd       Probability the command is executed (0 to 1).
#   probProximal  NumPy 2D array of probabilities (0 to 1) and radius.  Each element is the
#                 probability that the proximity sensor will fire at a given radius.
#
#
import matplotlib.pyplot as plt
import numpy as np
import random

#
#  Robot (Emulate the actual robot)
#
#    probCmd is the probability that the command is actually executed
#
#    probProximal is a list of probabilities.  Each element
#    corresponds to the probability that the proximity sensor will
#    fire at a distance of (index+1).
#
class Robot():
    def __init__(self, players = [], obstacles = [], y = 25, x = 25, vely = 0, velx = 0, radius = .5, dt = .1, accel = 1, \
        probCmd = 1.0, probProximal = [1.0, 10], t = 0):
        # Check the positional arguments.
        assert (y >= 0 + radius) and (y < 50 - radius), "Illegal y"
        assert (x >= 0 + radius) and (x < 50- radius), "Illegal x"

        # Save the obstacles, the initial location, and the probabilities.
        self.dt             = dt
        self.t              = t
        self.players        = players
        self.obstacles      = obstacles
        self.y              = y
        self.vely           = vely
        self.x              = x
        self.velx           = velx
        self.accel          = accel
        self.radius         = radius
        self.probCmd        = probCmd
        self.probProximal   = probProximal

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
            
    def lineIntersectCircle (x1, x2, y1, y2, cx, cy, r):
        return (abs((x2-x1)*cx + (y1-y2)*cy + (x1-x2)*y1 + (y2-y1)*x1) / np.sqrt((x2-x1)^2 +(y2 - y1)^2) <= r)

    def Drive(self, target):
        # Check the delta.
        
        # Try to move the robot the given delta.
        y = self.y + self.vely * self.dt
        x = self.x + self.vely * self.dt
        if (y <= 0 + self.radius) or (y > 50 - self.radius): #if its going to hit the wall, emergency break
            y = self.y
            self.vely = 0
        if (x <= 0 + self.radius) or (x > 50 - self.radius): #if its going to hit the wall, emergency break
            x = self.x
            self.velx = 0
        if np.sqrt(np.sqrt((self.x-target[0])^2+(self.y-target[1])^2)) < target[2] and target[3]:
            self.Freeze(target)
        for obstacle in self.obstacles:
            while self.lineIntersectCircle(self.x, target[0], self.y, target[1], obstacle.x, obstacle.y, obstacle.radius):
                old_target = target
                target = [random.ranrange(min(self.x, old_target[0]) - abs(self.x-old_target[0])*.25), random.ranrange(min(self.y, old_target[1]) - abs(self.y-old_target[1])*.25)]
        vely = self.vely + (y-target[1] + 1 * np.sign(y-target[1]))  * self.accel * self.dt # weighted acceleration that weights to speed of 1
        velx = self.velx + (x-target[0] + 1 * np.sign(x-target[0]))  * self.accel * self.dt # weighted acceleration that weights to speed of 1
        self.y = y, self.x = x, self.vely = vely, self.velx = velx

    
    def Freeze(self, target):
        for player in self.players:
            if player.identifier == target[3]:
                self.obstacles.append(player)
                players.remove(player)
        for player in self.players:
            player.obstacles = self.obstacles
        

    def Sensor(self):
        closest = []
        for player in self.players: # list of objects player with params x, y , velx, vely, radius, identifier
            for k in range(len(self.probProximal)):
                if np.sqrt((self.x-players.x)^2+(self.y-player.y)^2) - player.radius <= self.probProximal[k][1]:
                    if not closest or np.sqrt((self.x-player.x)^2+(self.y-player.y)^2) < closest[3]:
                        closest =[playerx, player.y, player.radius, player.identifier,  np.sqrt((self.x-player.x)^2+(self.y-player.y)^2)]
        return closest[:4]
