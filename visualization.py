#!/usr/bin/env python3
#
#   visualization.py
#

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from typing import NamedTuple

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
    def __init__(self, state, player_colors):
        # Create the figure and axes.
        self.fig, self.ax = plt.subplots()
        self.ax.set_xlim((0, M))
        self.ax.set_ylim((0, N))
    
        # Grab the dimensions.
        self.M = np.size(state, axis=0)
        self.N = np.size(state, axis=1)

        # Turn off the axis labels.
        self.ax.axis('off')

        # Store player colors
        self.player_colors = player_colors

        # Set diameter of circle
        self.diameter = 1 

        # Force the figure to pop up.
        plt.pause(0.001)

    # Updates robot, player, and obstacle positions on the figure.
    def showgrid(self, state):
        # Draw the robot and players
        for y in range(M+1):
            for x in range(N+1):
                # Draw the robot
                if state[y, x] == ROBOT:
                    p = Point(y,x)
                    circ = Circle(p.center(self.diameter), self.diameter/2, color = 'k')
                    self.ax.add_patch(circ) 

                # Draw the players with the corresponding color
                for i in self.player_colors:
                    if state[y, x] == PLAYER[i]:
                        p = Point(y,x)
                        circ = Circle(p.center(self.diameter), self.diameter/2, color = self.player_colors[i])
                        self.ax.add_patch(circ) 
        
        # Force the figure to pop up.
        plt.pause(0.001)

# class DynamicUpdate():
#     # Grab the dimensions.
#     M = 26
#     N = 26

#     def on_launch(self):
#         # Set up plot
#         self.figure, self.ax = plt.subplots()
#         self.lines, = self.ax.plot([],[], 'o')
        
#         # Scale axes with known lims
#         self.ax.set_xlim(0, self.M)
#         self.ax.set_ylim(0, self.N)

#         # turn off the axis labels and ticks
#         plt.xticks([])
#         plt.yticks([])

#     def on_running(self, xdata, ydata):
#         # Update data (with the new _and_ the old points)
#         self.lines.set_xdata(xdata)
#         self.lines.set_ydata(ydata)
        
#         # We need to draw *and* flush
#         self.figure.canvas.draw()
#         self.figure.canvas.flush_events()

#     # Example
#     def __call__(self):
#         import numpy as np
#         import time
#         self.on_launch()
#         xdata = []
#         ydata = []
#         for x in np.arange(0,10,0.5):
#             xdata.append(x)
#             ydata.append(np.exp(-x**2)+10*np.exp(-(x-7)**2))
#             if len(xdata) > 1:
#                 del xdata[0]
#             if len(ydata) > 1:
#                 del ydata[0]
#             self.on_running(xdata, ydata)
#             time.sleep(0.01)
#         return xdata, ydata


# # Start with an M x N size grid
# M = 26
# N = 26

# # Initialize states as unknown
# state = np.ones((M, N))

# d = DynamicUpdate()
# d()