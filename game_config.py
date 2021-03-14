import random

t = 0
dt = .1
player_num = random.randrange(20, 25)
obstacles_num = random.randrange(3, 5)


# Start with an M x N size grid with robots/players of a specified radius 
M = 100
N = 100
radius = 1

# Robot Settings
robot_sensor_range = 200
accelx = .1
accely = .1
sample = 10
T = 1       # Time constant of convergence


#
#  Obstacle (set up constant obstacles)
#

class Obstacle():
    def __init__(self, identifier = -1, y=random.randrange(0, N), x=random.randrange(0, M), radius=radius, color='#808080'):
        self.y = y
        self.x = x
        self.radius = radius
        self.identifier = identifier
        self.color = color

constant_obstacles = []
for i in range(obstacles_num):
    obstacle = Obstacle(y=random.randrange(0 + radius*2, M - radius*2), 
                x=random.randrange(0 + radius*2, N - radius*2))
    constant_obstacles.append(obstacle)


