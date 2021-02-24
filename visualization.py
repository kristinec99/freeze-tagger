#!/usr/bin/env python3
#
#   visualization.py
#

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from typing import NamedTuple

class Point(NamedTuple):
    """A point in 2D, usually the center of a grid cell."""

    y: int
    x: int
    
    # def center(self, diameter):
    #     return Point(self.x + diameter/2, self.y + diameter/2)

######################################################################
#
#   showgrid(M,N)
#
#   Create a figure for an M (rows) x N (column) grid.  The X-axis
#   will be the columns (to the right) and the Y-axis will be the rows
#   (top downward).
#
def showgrid(state):

    # Grab the dimensions.
    M = np.size(state, axis=0)
    N = np.size(state, axis=1)

    # # Close the old figure.
    # plt.close()

    # Create the figure and axes.
    fig, ax = plt.subplots()
    ax.set_xlim((0, M))
    ax.set_ylim((0, N))

    # turn off the axis labels
    ax.axis('off')

    # Set diameter of circle
    diameter = 1 

    # Create the color range.
    color = np.ones((M,N,3))
    for m in range(M):
        for n in range(N):
            if state[m,n] == WALL:
                color[m,n,0:3] = np.array([0.0, 0.0, 0.0])   # Black
            if state[m,n] == ROBOT:
                color[m,n,0:3] = np.array([0.0, 0.0, 0.0])   # Black
            else:
                color[m,n,0:3] = np.array([0.0, 0.0, 0.0])   # Black
    
    # Draw the robot and players
    for y in range(M+1):
        for x in range(N+1):
            # Draw the robot
            if state[y, x] == ROBOT:
                circ = Circle(p.center(diameter), diameter/2, color = 'k')
                ax.add_patch(circ) 

            # Draw the players with the corresponding color
            for i in player_colors:
                if state[y, x] == PLAYER[i]:
                    circ = Circle(p.center(diameter), diameter/2, color = player_colors[i])
                    ax.add_patch(circ) 
    

    # Draw map points
    for y in range(M+1):
        for x in range(N+1):
            p = Point(y,x)
            circ = plt.Circle(p, diameter/10, color='tab:gray')
            ax.add_patch(circ)  

    # Force the figure to pop up.
    plt.pause(0.001)