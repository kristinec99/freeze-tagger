#!/usr/bin/env python3
#
#   demo_visualization.py
#
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from visualization import *

######################################################################
#
#   Main Code
#

# Defines counter for each state; if ondeck is empty, search failed
def counter():
    ondeck = 0                          # Number of nodes on deck
    processed = 0                       # Number of nodes processed
    unknown = 0                         # Number of nodes unknown
    for i in range(M):
        for j in range(N):
            if state[i,j] == ONDECK:
                ondeck += 1             # Counting nodes on deck
            if state[i,j] == PROCESSED:
                processed += 1          # Counting nodes processed
            if state[i,j] == 69:
                processed += 1          # Counting nodes on path
            if state[i,j] == UNKNOWN:
                unknown += 1            # Counting nodes unknown
    if ondeck == 0:
        print("Search Failed: No Nodes On-Deck.")
        quit()
    # print("Nodes on Deck:", ondeck)
    # print("Nodes Processed:", processed)
    # print("Nodes Unknown:", unknown)
    # print("-----------")

# Defines Ctogo as the Euclidean Distance between the current point and the goal
def Ctogo(position):
    (xn,yn) = position
    (xg,yg) = goal
    return np.sqrt((xn - xg)**2 + (yn - yg)**2)

# Define the grid with unknown states.
M = 11
N = 17

# Add starting position to on-deck and other states to unknown
state = np.ones((M,N)) * UNKNOWN

# Show the empty grid.
h = showgrid(state)
input('Hit return to fill in the grid')

# Populate the states.
state[ 0,0:] = WALL
state[-1,0:] = WALL
state[0:, 0] = WALL
state[0:,-1] = WALL

state[3, 4:10] = WALL
state[4,   10] = WALL
state[5,   11] = WALL
state[6,   12] = WALL
state[7,   13] = WALL
state[7:M,  7] = WALL

# Set goal
goal = (5,12)

# A* with Ctogo = Manhattan distance
c = 1

# Initialize goal at (5,12) and start at (5,4) with Ctoreach = 0, Cpath, and no parent
start = ((5,4), 0, Ctogo((5,4)), None)
state[start[0]] = ONDECK
ondeck = [start]

done = []


while True:        
    node = min(ondeck, key = lambda t: t[2])   # Picks the node with the lowest Cpath in ondeck
    (xn,yn) = node[0]

    # Check if reached goal
    if (xn,yn) == goal:
        while True:
            state[node[0]] = 69
            node = node[3]
            if node == None:
                break
        print("Goal reached!")
        break

    node_position = (xn+1, yn)
    node_Ctoreach = node[1] + 1
    node_Cpath = node_Ctoreach + c * Ctogo(node_position)
    node_parent = node
    # Check neighbors of node
    if state[xn+1,yn] == UNKNOWN:           # If new unknown node
        ondeck.append((node_position, node_Ctoreach, node_Cpath, node_parent))
        state[xn+1,yn] = ONDECK
    elif state[xn+1,yn] == ONDECK:               # If node is ondeck
        old_node = [point for point in ondeck if (xn+1,yn) == point[0]][0]
        # If old Cpath is greater than new Cpath, update node
        if old_node[2] > node_Cpath:        
            ondeck.remove(old_node)
            ondeck.append((node_position, node_Ctoreach, node_Cpath, node_parent))

    node_position = (xn-1,yn)
    node_Cpath = node_Ctoreach + c * Ctogo(node_position)
    if state[xn-1,yn] == UNKNOWN:               # If new unknown node
        ondeck.append((node_position, node_Ctoreach, node_Cpath, node_parent))
        state[xn-1,yn] = ONDECK
    elif state[xn-1,yn] == ONDECK:               # If node is ondeck
        old_node = [point for point in ondeck if (xn-1,yn) == point[0]][0]
        # If old Cpath is greater than new Cpath, update node
        if old_node[2] > node_Cpath:       
            ondeck.remove(old_node)
            ondeck.append((node_position, node_Ctoreach, node_Cpath, node_parent))

    node_position = (xn,yn+1)
    node_Cpath = node_Ctoreach + c * Ctogo(node_position)
    if state[xn,yn+1] == UNKNOWN:               # If new unknown node
        ondeck.append((node_position, node_Ctoreach, node_Cpath, node_parent))
        state[xn,yn+1] = ONDECK
    elif state[xn,yn+1] == ONDECK:               # If node is ondeck
        old_node = [point for point in ondeck if (xn,yn+1) == point[0]][0]
        # If old Cpath is greater than new Cpath, update node
        if old_node[2] > node_Cpath:        
            ondeck.remove(old_node)        
            ondeck.append((node_position, node_Ctoreach, node_Cpath, node_parent))

    node_position = (xn,yn-1)
    node_Cpath = node_Ctoreach + c * Ctogo(node_position)
    if state[xn,yn-1] == UNKNOWN:           # If new unknown node
        ondeck.append((node_position, node_Ctoreach, node_Cpath, node_parent))
        state[xn,yn-1] = ONDECK
    elif state[xn,yn-1] == ONDECK:               # If node is ondeck
        old_node = [point for point in ondeck if (xn,yn-1) == point[0]][0]
        # If old Cpath is greater than new Cpath, update node
        if old_node[2] > node_Cpath:        
            ondeck.remove(old_node)
            ondeck.append((node_position, node_Ctoreach, node_Cpath, node_parent))

    ondeck.remove(node)
    done.append(node)
    state[node[0]] = PROCESSED

    # Check node states
    counter()

# Update/show the grid and show the S/G states labelled.
showgrid(state)
input('Hit return to continue')
