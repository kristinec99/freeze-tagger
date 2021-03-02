#!/usr/bin/env python3
#
#   bot_code.py
#
import random

import matplotlib.pyplot as plt
# import keyboard
from copy import deepcopy
from player_utils import Player
from robot_utils import Robot
from visualization import *

# ######################################################################
# #
# #   Main Code
# #

t = 0
dt = .1
player_num = 5
constant_obstacles = []

# Start with an M x N size grid
M = 100
N = 100

# Initialize states as unknown
def main():
    obstacles = deepcopy(constant_obstacles)
    players = []
    current_players = player_num
    
    # Set up players
    for i in range(player_num):
        radius = 1
        player = Player(obstacles=obstacles, players=players, identifier=i,
                        color="#" + ''.join([random.choice('0123456789ABCDEF') for j in range(6)]),
                                            y=random.randrange(0 + radius*2, M - radius*2), x=random.randrange(0 + radius*2, N - radius*2),
                                            vely=random.randrange(0, 2), velx=random.randrange(0, 2), radius = radius)
        # state[player.y, player.x] = PLAYERS[i]
        players.append(player)
    
    # Ask if user wants to enable manual mode.
    manual_ask = input('Manual Mode y/n \n')
    while not (manual_ask == 'y') and not (manual_ask == 'n'):
            manual_ask = input('Manual Mode y/n \n')
    if manual_ask == 'y':
        robot = Robot(obstacles=obstacles, players=players, y=25, x=25, manual=True)
    elif manual_ask == 'n':
        robot = Robot(obstacles=obstacles, players=players, y=25, x=25, manual=False)

    # Create the figure and axes.
    v = Visualization()
    while current_players > 0:
        for player in players:
            current_players = player.Walk(players, obstacles, current_players)
            player.t = player.t + dt
            # v.showgrid(robot, players)

        target = robot.Sensor(players)
        if not robot.manual:
            current_players = robot.Drive(target, players, obstacles, current_players)
        if robot.manual:
            pressed = [False, False, False, False]
            try:  # used try so that if user pressed other than the given key error will not be shown
                if keyboard.is_pressed('w'):  # if key 'w' is pressed 
                    pressed[0] = True
                if keyboard.is_pressed('a'):  # if key 'a' is pressed 
                    pressed[1] = True
                if keyboard.is_pressed('s'):  # if key 's' is pressed 
                    pressed[2] = True
                if keyboard.is_pressed('d'):  # if key 'd' is pressed 
                    pressed[3] = True
                break  # finishing the loop
            except:
                break  # if user pressed a key other than the given key the loop will break
            current_players = robot.Drive(target, players, obstacles, current_players, keys_pressed = pressed)
        robot.t = robot.t + robot.dt
        v.showgrid(robot, players)

    input("Press any key to end \n")

if __name__ == "__main__":
    main() 