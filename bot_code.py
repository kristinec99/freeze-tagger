#!/usr/bin/env python3
#
#   bot_code.py
#
import random

import matplotlib.pyplot as plt

from player_utils import Player
from robot_utils import Robot
from visualization import *

# ######################################################################
# #
# #   Main Code
# #

t = 0
dt = .1
player_num = 3
obstacles = []
players = []
player_colors = []

# Start with an M x N size grid
M = 26
N = 26

# Define the possible status levels for each state.
WALL = 0
UNKNOWN = 1
ROBOT = 2
PLAYERS = [i + 3 for i in range(player_num)]

# Initialize states as unknown
state = np.ones((M, N)) * UNKNOWN

for i in range(player_num):
    player = Player(obstacles=obstacles, players=players, identifier=i,
                    color="#" + ''.join([random.choice('0123456789ABCDEF') for j in range(6)]),
                                        y=random.randrange(0, 50), x=random.randrange(0, 50))
    player_colors.append(player.color)
    # state[player.y, player.x] = PLAYERS[i]
    players.append(player)

robot = Robot(obstacles=obstacles, players=players, y=25, x=25)
# state[robot.y, robot.x] = ROBOT

# while players:
#     plt.close()

#     # Create the figure and axes.
#     fig, ax = plt.subplots()
#     plt.plot([0, 0, 50, 50, 0], [0, 50, 50, 0, 0], color='k', lw=.5)
#     ax.set_xlim((0, 50))
#     ax.set_ylim((0, 50))

#     # turn off the axis labels
#     ax.axis('off')

#     for player in players:
#         player.Walk(players)
#         player.t = player.t + dt
#         playertoken = plt.Circle((player.x, player.y), radius=player.radius, color=player.color)
#         ax.add_artist(playertoken)
#         # state[player.y, player.x] = PLAYERS[i]
#     for obstacle in robot.obstacles:
#         obstacletoken = plt.Circle((obstacle.x, obstacle.y), radius=obstacle.radius, color='#808080')
#         ax.add_artist(obstacletoken)
#     target = robot.Sensor(players)
#     robot.Drive(target, players)
#     robottoken = plt.Circle((robot.x, robot.y), radius=robot.radius, color='k')
#     ax.add_artist(robottoken)
#     plt.show(block=False)
#     plt.pause(0.5)
#     plt.close()
#     # state[robot.y, robot.x] = ROBOT
#     # showgrid(state)
# # Update/show the grid and show the players and robot.
# # showgrid(state)

# fig, ax = plt.subplots()
# plt.plot([0, 0, 50, 50, 0], [0, 50, 50, 0, 0], color='k', lw=.5)
# ax.set_xlim((0, 50))
# ax.set_ylim((0, 50))
# ax.axis('off')
# for obstacle in robot.obstacles:
#     obstacletoken = plt.Circle((obstacle.x, obstacle.y), radius=obstacle.radius, color='#808080')
#     ax.add_artist(obstacletoken)
# robottoken = plt.Circle((robot.x, robot.y), radius=robot.radius, color='k')
# ax.add_artist(robottoken)
# plt.show()
# input = "Press any key to end"