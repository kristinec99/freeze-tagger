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
import keyboard
from game_config import *

#
#  Robot (Emulate the actual robot)
#
#    probCmd is the probability that the command is actually executed
#
#    probProximal is a list of probabilities.  Each element
#    corresponds to the probability that the proximity sensor will
#    fire at a distance of (index+1).


class Robot():
    def __init__(self, players = [] , obstacles=[], y=N/2, x=N/2, vely=0, velx=0, radius=radius, dt=dt, accelx=accelx, accely=accely,\
                 probCmd=1.0, probProximal=[[1.0, robot_sensor_range]], t=0, manual=False, sample = 5):
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
        self.accelx = accelx
        self.accely = accely
        self.radius = radius
        self.probCmd = probCmd
        self.probProximal = probProximal
        self.manual = manual
        self.target = [M/2,N/2,-1,1,0,0]
        self.sample = sample

        # Pick a valid starting location (if not already given).
        invalid_starts = copy(obstacles)
        invalid_starts.extend(players)
        while True:
            if not self.x or not self.y:
                self.y = random.randrange(0, N)
                self.x = random.randrange(0, M)
            counter = 0
            for obstacle in invalid_starts :
                if np.sqrt((self.x - obstacle.x) ** 2 + (self.y - obstacle.y) ** 2) <= obstacle.radius + self.radius:
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

    def Drive(self, players, obstacles, current_players, frozen_players):
        # Check the delta.

        # Try to move the robot and avoid obstacles            
        y = self.y + self.vely * self.dt
        x = self.x + self.velx * self.dt
        
        target = self.target
        # Add manual control of robot motion
        # if self.manual:
        #     # If robot is going to hit the wall, emergency break
        #     if (y <= 0 + self.radius) or (y > N - self.radius):
        #         self.vely = - self.vely
        #         return(current_players, frozen_players)
            
        #     # If robot is going to hit the wall, emergency break
        #     if (x <= 0 + self.radius) or (x > M - self.radius):
        #         self.velx = - self.velx
        #         return(current_players, frozen_players)
        #     for player in players:
        #         # If robot runs into active player, freeze
        #         if np.sqrt(np.sqrt((x - player.x) ** 2 + (y - player.y) ** 2)) < player.radius and player.froze == False:
        #             current_players, frozen_players = self.Freeze([player.x, player.y, player.radius, player.identifier, player.velx, player.vely], players, obstacles, current_players, frozen_players)
        #             return(current_players, frozen_players)
            
        #     for obstacle in obstacles:
        #         if np.sqrt((x - obstacle.x) ** 2 + (y - obstacle.y) ** 2) <= obstacle.radius + self.radius: # if its going to hit a frozen player bounce back
        #                 self.velx = -self.velx
        #                 self.vely = -self.vely
        #                 return(current_players, frozen_players)
            
        #     # Add velocity changes due to key input
        #     if (keys_pressed[0]):
        #         self.vely = self.vely + .1
        #     if (keys_pressed[1]):
        #         self.velx = self.velx - .1
        #     if (keys_pressed[2]):
        #         self.vely = self.vely - .1
        #     if (keys_pressed[3]):
        #         self.velx = self.velx + .1
        #     self.y = y
        #     self.x = x
        #     return(current_players, frozen_players)
        # # Automatic control of robot
        #else:
        if not self.target:
            self.target = [random.randrange(0 + self.radius*2, M - self.radius*2), random.randrange(0 + self.radius*2, N - self.radius*2), 1, -1, 0, 0]
        target = self.target
        if (y <= 0 + self.radius) or (y > N - self.radius):  # if its going to hit the wall, emergency break
            self.vely = - self.vely
            return(current_players, frozen_players)
        if (x <= 0 + self.radius) or (x > M - self.radius):  # if its going to hit the wall, emergency break
            self.velx = - self.velx
            return(current_players, frozen_players)
        if np.sqrt(np.sqrt((x - target[0]) ** 2 + (y - target[1]) ** 2)) < target[2] and target[3] >= 0: # if robot runs into active player, freeze
            current_players, frozen_players = self.Freeze(target, players, obstacles, current_players, frozen_players)
            return (current_players, frozen_players)

        for obstacle in obstacles:
            if np.sqrt((x - obstacle.x) ** 2 + (y - obstacle.y) ** 2) <= obstacle.radius + self.radius: # if its going to hit a frozen player bounce back
                    self.velx = -self.velx
                    self.vely = -self.vely
                    return(current_players, frozen_players)

        counter = 0
        for obstacle in obstacles:
            if self.lineIntersectCircle(obstacle.radius + self.radius, (obstacle.x, obstacle.y), (x,y), (target[0], target[1])):
                counter = counter + 1
                break
        if counter != 0:
            targets = []
            while len(targets) <= self.sample:
                target_choice = [random.randrange(max(round(x - self.radius*5), 0 + self.radius), min(round(x + self.radius*5), N - self.radius)), 
                        random.randrange(max(round(y - self.radius*5), 0 + self.radius), min(round(y + self.radius*5), M - self.radius)), 1, -1, 0, 0]
                counter = 0
                for obstacle in obstacles:
                    if self.lineIntersectCircle(obstacle.radius + self.radius, (obstacle.x, obstacle.y), (x,y), (target_choice[0], target_choice[1])):
                        counter = counter + 1
                        break
                if counter == 0:
                    targets.append(target_choice)
            target = targets[0]
            for target_choice in targets:
                if ((self.target[0]  - target_choice[0])**2 + (self.target[1] - target_choice[1])**2) < ((self.target[0] - target[0])**2 + (self.target[1] - target[1])**2):
                    target = target_choice


        self.accelx = 2/T * (target[4] - self.velx) + 1/T**2 * (target[0] - self.x)
        self.accely = 2/T * (target[5] - self.vely) + 1/T**2 * (target[1] - self.y)
        vely = self.vely + self.accely * self.dt  # weighted acceleration
        velx = self.velx + self.accelx * self.dt  # weighted acceleration
        self.y = y
        self.x = x
        self.vely = vely
        self.velx = velx
        return(current_players, frozen_players)

    def Freeze(self, target, players, obstacles, current_players, frozen_players):
        for player in players:
            # If robot passes through target, then freeze player
            if player.identifier == target[3]:
                player.froze = True
                current_players = current_players - 1
                frozen_players.append(player)
                return(current_players, frozen_players)
            
            # # If robot passes through player, then freeze player
            # if np.sqrt((self.x - player.x) ** 2 + (self.y - player.y) ** 2) <= player.radius + self.radius:
            #     player.froze = True
            #     current_players = current_players - 1
            #     return(current_players)
        return(current_players, frozen_players)


    def Sensor(self, players):
        closest = None
        for player in players:  # list of objects player with params x, y , velx, vely, radius, identifier
            if player.froze == False:
                for k in range(len(self.probProximal)):
                    if np.sqrt((self.x - player.x) ** 2 + (self.y - player.y) ** 2) - player.radius <= self.probProximal[k][1]:
                        if not closest or np.sqrt((self.x - player.x) ** 2 + (self.y - player.y) ** 2) < np.sqrt((self.x - closest[0]) ** 2 + (self.y - closest[1]) ** 2):
                            closest = [player.x, player.y, player.radius, player.identifier, player.velx, player.vely]
        return closest
    
    def pointIntersectCircle(self, x, y, cx, cy, r):
        return (np.sqrt((x - cx) ** 2 + (y - cy) ** 2) <= r)
