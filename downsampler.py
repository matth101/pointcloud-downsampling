import numpy as np
import csv

class Node: 
    def __init__(self, bounds):
        self.bounds = bounds # min_x, min_y, min_z
        self.points = []
        self.children = []

def main():


    # Parse csv into an array
    # with open('input.csv', 'r') as input:
    #     reader = csv.DictReader(input)
    #     for row in reader:
    #         x = float(row['x'])
    #         y = float(row['y'])
    #         z = float(row['z'])
    #         points.append([x, y, z])

    np_points = np.genfromtxt('input.csv', delimiter=',', skip_header=1)

    min_coords = np.min(np_points, axis=0)
    max_coords = np.max(np_points, axis=0)

    root_bounds = np.concatenate((min_coords, max_coords))
    root = Node(root_bounds)



