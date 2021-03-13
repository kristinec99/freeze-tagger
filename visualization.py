#!/usr/bin/env python3
#
#   visualization.py
#

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from typing import NamedTuple
from bot_code import constant_obstacles
from game_config import *

# Turn plot interactive mode on
plt.ion()

class Point(NamedTuple):
    """A point in 2D, usually the center of a grid cell."""

    y: int
    x: int
    
    # def center(self, diameter):
    #     return Point(self.x + diameter/2, self.y + diameter/2)

######################################################################
#
#   Visualization()
#
#   Sets up visualizer for freeze tag game.
#

class Visualization():
    # Initializes a  figure for an M (rows) x N (column) grid.  The X-axis
    #   will be the columns (to the right) and the Y-axis will be the rows
    #   (top downward).
    def __init__(self):
        # Grab the dimensions.
        self.M = M
        self.N = N
        
        # Create the figure and axes.
        self.fig, self.ax = plt.subplots()
        self.ax.set_xlim(0, self.M)
        self.ax.set_ylim(0, self.N)

        # Turn off the axis labels and ticks
        plt.xticks([])
        plt.yticks([])

        # Set diameter of circle
        self.radius = radius

        # Draw the obstacles in gray colors
        for obstacle in constant_obstacles:
            p = Point(obstacle.y, obstacle.x)
            circ = Circle(p, self.radius, color = obstacle.color)
            self.ax.add_patch(circ)

        # Force the figure to pop up.
        plt.pause(0.001)

    # Updates robot, player, and obstacle positions on the figure.
    def showgrid(self, robot, players):
        # Flush figure
        self.ax.patches = []

        # Draw the obstacles in gray colors
        for obstacle in constant_obstacles:
            p = Point(obstacle.y, obstacle.x)
            circ = Circle(p, self.radius, color = obstacle.color)
            self.ax.add_patch(circ)

        # Draw the robot
        robot_center = Point(robot.y, robot.x)
        robot_area = Circle(robot_center, self.radius, color = 'k')
        self.ax.add_patch(robot_area) 

        # Draw the players with the corresponding color
        for player in players:
            # If unfrozen, player has designated color
            if player.froze == False:
                p = Point(player.y, player.x)
                circ = Circle(p, self.radius, color = player.color)
                self.ax.add_patch(circ) 

            # If frozen, player is ice-blue
            else:
                p = Point(player.y, player.x)
                circ = Circle(p, self.radius, color = '#a6e7ff')
                self.ax.add_patch(circ)

        # Force the figure to pop up.
        plt.pause(0.001)