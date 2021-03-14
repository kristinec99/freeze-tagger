#!/usr/bin/env python3
#
#   bot_code.py
#
import random

import matplotlib.pyplot as plt
import keyboard
from copy import deepcopy
from player_utils import Player
from robot_utils import Robot
from visualization import *
from game_config import *

# ######################################################################
# #
# #   Main Code
# #

# Initialize states as unknown
def main():
    obstacles = deepcopy(constant_obstacles)
    players = []
    frozen_players = []
    current_players = player_num
    
    # Set up players
    for i in range(player_num):
        player = Player(obstacles=obstacles, players=players, identifier=i,
                        color="#" + ''.join([random.choice('0123456789ABCDEF') for j in range(6)]),
                                            y=random.randrange(0 + radius*2, M - radius*2), x=random.randrange(0 + radius*2, N - radius*2),
                                            vely=random.randrange(0, 2), velx=random.randrange(0, 2), radius = radius)
        # state[player.y, player.x] = PLAYERS[i]
        players.append(player)
    
    # Ask if user wants to enable manual mode.
    # manual_ask = input('Manual Mode y/n \n')
    # while not (manual_ask == 'y') and not (manual_ask == 'n'):
    #         manual_ask = input('Manual Mode y/n \n')
    # if manual_ask == 'y':
    #     robot = Robot(obstacles=obstacles, players=players, manual=True)
    # elif manual_ask == 'n':
    robot = Robot(obstacles=obstacles, players=players, manual=False, sample=sample)

    # Create the figure and axes.
    v = Visualization()
    while current_players > 0:
        for player in players:
            current_players, frozen_players = player.Walk(players, obstacles, current_players, robot, frozen_players)
            player.t = player.t + dt
            # v.showgrid(robot, players)

        target = robot.Sensor(players)
        robot.target = target
        # if not robot.manual:
        current_players, frozen_players = robot.Drive(players, obstacles, current_players, frozen_players)
        # if robot.manual:
        #     pressed = [False, False, False, False]
        #     try:  # used try so that if user pressed other than the given key error will not be shown
        #         if keyboard.is_pressed('w'):  # if key 'w' is pressed 
        #             pressed[0] = True
        #         if keyboard.is_pressed('a'):  # if key 'a' is pressed 
        #             pressed[1] = True
        #         if keyboard.is_pressed('s'):  # if key 's' is pressed 
        #             pressed[2] = True
        #         if keyboard.is_pressed('d'):  # if key 'd' is pressed 
        #             pressed[3] = True
        #         break  # finishing the loop
        #     except:
        #         break  # if user pressed a key other than the given key the loop will break
        #     current_players = robot.Drive(players, obstacles, current_players)
        robot.t = robot.t + robot.dt
        v.showgrid(robot, players)

    input("Press any key to end \n")

if __name__ == "__main__":
    main() 