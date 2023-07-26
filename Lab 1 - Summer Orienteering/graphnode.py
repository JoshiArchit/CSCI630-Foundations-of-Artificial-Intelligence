"""
Filename : graphnode.py
Author : Archit Joshi
Description : CSCI630 Lab 1 - Graph node representation for A* search algorithm
Language : Python 3.11
Revisions :
v1.0 - Initial node definition
v1.1 - Added terrain and elevation attributes
v1.2 - Removed parent attributes as we will use predecessor hashmap to keep
       track of the path travelled.
"""


class Node:
    """
    Node representation for graph used for A* search algorithm.
    Each node represents a single pixel on the map
    """

    # Instance variables and datatypes
    __slots__ = "xPos", "yPos", "terrain", "elevation", "cost", "mobility", "gScore"
    xPos: float
    yPos: float
    terrain: tuple
    elevation: float
    cost: float
    mobility: float

    def __init__(self, xPos, yPos) -> None:
        """
        Constructor for node object. Each node represents a single pixel on the
        map image.

        :param xPos: x position of pixel (top-left)
        :param yPos: y position of pixel (top-left)
        """
        self.xPos = xPos
        self.yPos = yPos
        self.cost = float('inf')
        self.terrain = None
        self.elevation = None
        self.mobility = None
        self.gScore = 0

    def __str__(self) -> str:
        """
        Returns string output of the node printing x-Coordinate and y-Coordinate.
        """
        output = str(self.xPos) + "," + str(self.yPos)
        return output
