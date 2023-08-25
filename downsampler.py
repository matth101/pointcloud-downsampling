import numpy as np
import csv
import time

start_time = time.time()

# Constants
MAX_NODE_POINTS = 500
MAX_DEPTH = 7

class Node: 
    def __init__(self, bounds):
        self.bounds = bounds # [min_x, min_y, min_z, max_x, max_y, max_z]
        self.points = []
        self.children = []

def build_tree(node, depth, max_depth, max_node_points):
    # if len(node.points) >= max_node_points or depth >= max_depth: # base case
    #     return

    if depth >= max_depth:
        return
    
    # print("not at base case")
    
    mid_x = (node.bounds[0] + node.bounds[3]) / 2
    mid_y = (node.bounds[1] + node.bounds[4]) / 2
    mid_z = (node.bounds[2] + node.bounds[5]) / 2

    # define new octants by substituting in midpoints for every possible combination
    # i.e. (node.bounds[0], node.bounds[1], node.bounds[2], mid_x, etc)
    child_bounds = [
        (node.bounds[0], node.bounds[1], node.bounds[2], mid_x, mid_y, mid_z),
        (mid_x, node.bounds[1], node.bounds[2], node.bounds[3], mid_y, mid_z),
        (node.bounds[0], mid_y, node.bounds[2], mid_x, node.bounds[4], mid_z),
        (mid_x, mid_y, node.bounds[2], node.bounds[3], node.bounds[4], mid_z),
        (node.bounds[0], node.bounds[1], mid_z, mid_x, mid_y, node.bounds[5]),
        (mid_x, node.bounds[1], mid_z, node.bounds[3], mid_y, node.bounds[5]),
        (node.bounds[0], mid_y, mid_z, mid_x, node.bounds[4], node.bounds[5]),
        (mid_x, mid_y, mid_z, node.bounds[3], node.bounds[4], node.bounds[5]),
    ]

    for bound in child_bounds: # for every octant
        child = Node(bound)
        node.children.append(child)
        build_tree(child, depth+1, max_depth, max_node_points)   

def assign_points(node, points):
    for point in points:
        curr = node
        while curr.children:
            mid_x = (curr.bounds[0] + curr.bounds[3]) / 2
            mid_y = (curr.bounds[1] + curr.bounds[4]) / 2
            mid_z = (curr.bounds[2] + curr.bounds[5]) / 2

            # match the point to the correct octant. This assumes the children are ordered properly:
            # FL = front-lower, FU = front-upper, BL = back-lower, BU = back-upper
            # [FL-left, FL-right, FU-left, FU-right, BL-left, BL-right, BU-left, BU-right]
            index = 0
            if point[0] > mid_x:
                index += 1
            if point[1] > mid_y:
                index += 2
            if point[2] > mid_z:
                index += 4

            curr = curr.children[index] # move to the next "candidate" node
        
        curr.points.append(point)

def traverse_and_average(node):
    if not node.children: # leaf node
        if node.points:
            average_point = np.mean(node.points, axis=0)
            node.points = [average_point]
            return
    else:
        for child_node in node.children:
            traverse_and_average(child_node)

def collect_output(node, output):
    if not node.children:
        if node.points:
            output.append(node.points[0])
            return
    else:
        for child_node in node.children:
            collect_output(child_node, output)   

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
    
    end_time = time.time()
    elapsed_time = end_time-start_time
    print(f"Parsed points; ready to begin downsampling. {elapsed_time:.2f} seconds passed.")

    build_tree(root, depth=0, max_depth=MAX_DEPTH, max_node_points=MAX_NODE_POINTS)
    end_time = time.time()
    elapsed_time = end_time-start_time
    print(f"Octree fully initialized. {elapsed_time:.2f} seconds passed.")  

    assign_points(root, np_points)
    end_time = time.time()
    elapsed_time = end_time-start_time
    print(f"Octree has been filled. {elapsed_time:.2f} seconds passed.")

    traverse_and_average(root)
    end_time = time.time()
    elapsed_time = end_time-start_time
    print(f"Points have been downsampled and consolidated. {elapsed_time:.2f} seconds passed.")

    output = []
    collect_output(root, output)

    header = ['x', 'y', 'z']
    output_name = 'output2.csv'
    np.savetxt(output_name, output, delimiter=',', header=','.join(header), comments="")

    end_time = time.time()
    print(f"Elapsed time: {end_time - start_time:.2f} seconds.")

main()


