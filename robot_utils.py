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
import random
from copy import copy
import numpy as np


#
#  Robot (Emulate the actual robot)
#
#    probCmd is the probability that the command is actually executed
#
#    probProximal is a list of probabilities.  Each element
#    corresponds to the probability that the proximity sensor will
#    fire at a distance of (index+1).


M = 100
N = 100

class Robot():
    def __init__(self, players = [] ,obstacles=[], y=25, x=25, vely=0, velx=0, radius=1, dt=.1, accel=.1, \
                 probCmd=1.0, probProximal=[[1.0, 25]], t=0, manual=False):
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
        self.probCmd = probCmd
        self.probProximal = probProximal
        self.manual = manual

        # Pick a valid starting location (if not already given).
        invalid_starts = copy(obstacles)
        invalid_starts.extend(players)
        while True:
            if not self.x or not self.y:
                self.y = random.randrange(0, N)
                self.x = random.randrange(0, M)
            counter = 0
            for obstacle in invalid_starts :
                if np.sqrt((self.x - obstacle.x) ** 2 + (self.y - obstacle.y) ** 2) <= obstacle.radius:
                    counter = counter + 1
            if counter == 0:
                break
            self.y = random.randrange(0, N)
            self.x = random.randrange(0, M)

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

    def Drive(self, target, players, obstacles, current_players, keys_pressed = None):
        # Check the delta.

        # Try to move the robot and avoid obstacles            
        y = self.y + self.vely * self.dt
        x = self.x + self.velx * self.dt
        
        # Add manual control of robot motion
        if self.manual:
            # If robot is going to hit the wall, emergency break
            if (y <= 0 + self.radius) or (y > M - self.radius):
                y = self.y
                self.vely = - self.vely
            
            # If robot is going to hit the wall, emergency break
            if (x <= 0 + self.radius) or (x > N - self.radius):
                x = self.x
                self.velx = - self.velx
            
            for player in players:
                # If robot runs into active player, freeze
                if np.sqrt(np.sqrt((x - player.x) ** 2 + (y - player.y) ** 2)) < player.radius and player.froze == False:
                    current_players = self.Freeze([player.x, player.y, player.identifier], players, current_players)
                    return(current_players)
            
            for obstacle in obstacles:
                # If robot is going to hit the wall or another player, stop
                if np.sqrt((x - obstacle.x) ** 2 + (y - obstacle.y) ** 2) <= obstacle.radius + self.radius:
                    self.velx = - self.velx
                    self.vely = - self.vely
                    x = self.x
                    y = self.y
                    return
            
            # Add velocity changes due to key input
            if (keys_pressed[0]):
                self.vely = self.vely + .1
            if (keys_pressed[1]):
                self.velx = self.velx - .1
            if (keys_pressed[2]):
                self.vely = self.vely - .1
            if (keys_pressed[3]):
                self.velx = self.velx + .1
            self.y = y
            self.x = x

        # Automatic control of robot
        else:
            if not target:
                target = [random.randrange(0 + self.radius*2, M - self.radius*2), random.randrange(0 + self.radius*2, N - self.radius*2), 1, -1]
            if (y <= 0 + self.radius) or (y > N - self.radius):  # if its going to hit the wall, emergency break
                y = self.y
                self.vely = - self.vely
            if (x <= 0 + self.radius) or (x > M - self.radius):  # if its going to hit the wall, emergency break
                x = self.x
                self.velx = - self.velx
            if np.sqrt(np.sqrt((x - target[0]) ** 2 + (y - target[1]) ** 2)) < target[2] and target[3] >= 0: # if robot runs into active player, freeze
                current_players = self.Freeze(target, players, obstacles, current_players)
                return (current_players)
            # target = [random.randrange(0 + self.radius*2, N - self.radius*2), random.randrange(0 + self.radius*2, M - self.radius*2)]

            for obstacle in obstacles:
                if np.sqrt((x - obstacle.x) ** 2 + (y - obstacle.y) ** 2) <= obstacle.radius + self.radius: # if its going to hit a frozen player bounce back
                        self.velx = -self.velx
                        self.vely = -self.vely
                        return(current_players)

            while True: # if the target requires going through an obstacle, repick target
                counter = 0
                for obstacle in obstacles:
                    if self.lineIntersectCircle(obstacle.radius + self.radius, (obstacle.x, obstacle.y), (x,y), (self.target[0], self.target[1])):
                        counter = counter + 1
                        break
                if counter == 0:
                    break 
                target = [random.randrange(0 + self.radius*2, M - self.radius*2), random.randrange(0 + self.radius*2, N - self.radius*2), 1, -1]
                    # old_target = target
                    # target = [random.randrange(min(self.x, old_target[0]) - abs(self.x - old_target[0]) * .25,
                    #                            max(self.x, old_target[0]) + abs(self.x - old_target[0]) * .25),
                    #           random.randrange(min(self.y, old_target[1]) - abs(self.y - old_target[1]) * .25,
                    #                            max(self.y, old_target[1]) + abs(self.y - old_target[1]) * .25)]

            vely = self.vely + (-y + target[1] + 1 * np.sign(
                y - target[1])) * self.accel * self.dt  # weighted acceleration
            velx = self.velx + (-x + target[0] + 1 * np.sign(
                x - target[0])) * self.accel * self.dt  # weighted acceleration
            self.y = y
            self.x = x
            self.vely = vely
            self.velx = velx
            return(current_players)

    def Freeze(self, target, players, obstacles, current_players):
        for player in players:
            # If robot passes through target, then freeze player
            if player.identifier == target[3]:
                player.froze = True
                player.freezetime = player.t + 1
                current_players = current_players - 1
                return(current_players)
            
            # If robot passes through player, then freeze player
            if np.sqrt((self.x - player.x) ** 2 + (self.y - player.y) ** 2) <= player.radius + self.radius:
                player.froze = True
                player.freezetime = player.t + 1
                current_players = current_players - 1
                return(current_players)
        return(current_players)


    def Sensor(self, players):
        closest = None
        for player in players:  # list of objects player with params x, y , velx, vely, radius, identifier
            if player.froze == False:
                for k in range(len(self.probProximal)):
                    if np.sqrt((self.x - player.x) ** 2 + (self.y - player.y) ** 2) - player.radius <= self.probProximal[k][1]:
                        if not closest or np.sqrt((self.x - player.x) ** 2 + (self.y - player.y) ** 2) < np.sqrt((self.x - closest[0]) ** 2 + (self.y - closest[1]) ** 2):
                            closest = [player.x, player.y, player.radius, player.identifier]
        return closest
