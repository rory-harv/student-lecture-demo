
# octree implementation 

import numpy as np
from typing import List

class OctNode(object):

    def __init__(self, pos, size, depth, data):

        self.pos = pos  # position
        self.size = size    
        self.depth = depth  
        self.isLeafNode = True  # initializes all nodes as leaves first
        self.data = data    # stored data
        self.branches = []  

        half = size / 2     # store half value for computations 

        # create a bounding box for a octree cube
        self.lower = (pos[0] - half, pos[1] - half, pos[2] - half)   # lower bound of bounding box
        self.upper = (pos[0] + half, pos[1] + half, pos[2] + half)   # upper bound of bounding box


class Octree(object):

    def __init__(self, worldSize, origin=(0, 0, 0), max_type="nodes", max_value=10):

        # creates the root bounding cube for the octree

        self.root = OctNode(origin, worldSize, 0, [])   # creates the root as an initialized leaf node
        self.worldSize = worldSize  # size of 3d world space
        self.limit_nodes = (max_type=="nodes")  # max nodes so nothing subdivides
        self.limit = max_value  # max value of node


