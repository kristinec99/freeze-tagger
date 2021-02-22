#!/usr/bin/env python3
#
#   visualization.py
#
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from typing import NamedTuple

# Define the possible status levels for each state.
WALL      = 0
UNKNOWN   = 1
ONDECK    = 2
PROCESSED = 3
PLAYER    = 4

#
#   Defines points based on an M (rows) x N (column) grid.  The X-axis
#   will be the columns (to the right) and the Y-axis will be the rows
#   (top downward).
#

class Point(NamedTuple):
    """A point in 2D, usually the center of a grid cell."""

    y: int
    x: int
    
    def center(self, diameter):
        return Point(self.x + diameter/2, self.y + diameter/2)

# Generates a random color
def random_color():
    rgbl=[255,0,0]
    random.shuffle(rgbl)
    return tuple(rgbl)

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

    # Close the old figure.
    plt.close()

    # Create the figure and axes.
    fig = plt.figure()
    ax = plt.axes()

    # turn off the axis labels
    ax.axis('off')

    # Set diameter of circle
    diameter = 1

    # Draw the robot and players
    if state == PLAYER:
        circ = Circle(p.center(diameter), diameter/2, color = random_color())
    ax.add_patch(circ)   

    # Create the color range.
    color = np.ones((M,N,3))
    for m in range(M):
        for n in range(N):
            if state[m,n] == WALL:
                color[m,n,0:3] = np.array([0.0, 0.0, 0.0])   # Black

    # Draw map points
    # for point in points:
    #     p = point
    #     circ = Circle(p.center(diameter), diameter/2, color=color[p.y, p.x, 0:3])
    #     ax.add_patch(circ)

    # Force the figure to pop up.
    plt.pause(0.001)