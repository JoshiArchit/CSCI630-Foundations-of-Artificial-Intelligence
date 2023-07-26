"""
Filename : lab1.py
Author : Archit Joshi
Description : CSCI630 - Lab 1 : Summer Orienteering (A* algorithm implementation)
Language : Python 3.11
Revisions :
v1.0 - Added getInput() to parseInputs, hardcoded legend values and
       speed values for each terrain type.
v1.1 - Parsing terrain data from long data to float data (395 cols only).
v1.2 - Parsing image data to lists using PIL Image library.
v1.3 - Parsing "control" points data to lists. Input parsing completed.
v1.4 - Graph node class definition (check graphnode.py). Import added.
v1.5 - Adjusted terrain dictionary key datatype.
v1.6 - Begin A* Search with pairs of control points.
v1.7 - Troubleshooting and debugging for control point and node selection logic.
v1.8 - Added case for "OutOfBounds" pixels.
v1.9 - Addition of getChildren() function and troubleshooting.
v1.10 - Calculation of f(n) = g(n) + h(n)
v1.11 - A* algorithm completed.
v1.12 - getChildren() function rewritten to resolve bugs and get correct children.
v1.13 - Image drawing and troubleshooting.
v1.14 - Calculating final distance using 3D euclidian distance.
v1.15 - Added a validate input function separate of Orienteering class.
v1.16 - Bug Fixes for img.putpixel() and Divide by zero/TLE
"""

import math
from PIL import Image
from sys import argv


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


class Orienteering:
    """
    Class to parse Inputs, construct a graph and use A* search to find the
    optimal path for an orienteering track.
    """

    # Instance variables and data types
    __slots__ = 'imageData', 'controlData', 'elevationData', 'nodeList', 'finalPath', 'gScore'
    imageData: list[list]
    controlData: list[list]
    elevationData: list
    nodeList: list
    finalPath: list[list]

    def __init__(self) -> None:
        """
        Constructor to instantiate empty list datastructures.
        """
        self.imageData = []
        self.controlData = []
        self.elevationData = []
        self.nodeList = []
        self.finalPath = []

    """
    Terrain Color Legend for each pixel on image
    {(R, G, B) : 'TerrainType'}
    """
    terrainLegend = {
        (248, 148, 18) : "OpenLand",
        (255, 192, 0)  : "RoughMeadow",
        (255, 255, 255): "EasyMoveForest",
        (2, 208, 60)   : "SlowRunForest",
        (2, 136, 40)   : "WalkForest",
        (5, 73, 24)    : "ImpassibleVegetation",
        (0, 0, 255)    : "LakeSwampMarsh",
        (71, 51, 3)    : "PavedRoad",
        (0, 0, 0)      : "Footpath",
        (205, 0, 101)  : "OutOfBounds"
    }

    """
    Terrain Speed Map on a scale of 0-5 (Slowest - Fastest)
    {'TerrainType' : Speed}
    """
    terrainSpeed = {
        "OpenLand"            : 5,
        "RoughMeadow"         : 1,
        "EasyMoveForest"      : 2,
        "SlowRunForest"       : 2.5,
        "WalkForest"          : 3,
        "ImpassibleVegetation": 0.5,
        "LakeSwampMarsh"      : 0.5,
        "PavedRoad"           : 5,
        "Footpath"            : 4,
        "OutOfBounds"         : 0
    }

    def parseInput(self, elevationFile: str, imageFile: str,
                   controlFile: str) -> None:
        """
        Driver function to parse commandline input and call parser functions
        to create data structures.

        @param elevationFile: mpp.txt file
        @param imageFile: terrain.png file
        @param controlFile: txt file with control points
        @return: None
        """
        self.parseElevationFile(elevationFile)
        self.parseImageFile(imageFile)
        self.parseControlFile(controlFile)

        # Create graph nodes
        self.createNodes()

    def parseElevationFile(self, file: str) -> None:
        """
        Read 500*400 mpp.txt file and store 500*395 data points in
        elevationData data structure. Convert each data point from long to
        float before storage.

        @param file: path to file containing elevation data
        @return: None
        """

        # Open the file and parse each row as a list and store it
        with open(file) as f:
            for line in f:
                # Skip last 5 entries to read only 395 entries in each row
                row = line.strip().split()[:-5]
                # Convert long to float values
                for i in range(len(row)):
                    row[i] = float(row[i])
                self.elevationData.append(row)
        f.close()

    def parseImageFile(self, file: str) -> None:
        """
        Parse image file using PIL and store 500*395 data points in imageData
        data structure in RGB format.

        @param file: path to png image file
        @return: None
        """
        img = Image.open(file)
        raw_data = list(img.getdata())
        row = []
        col = 0

        for pixel in raw_data:
            # Skip the alpha value and parse on RGB values
            row.append(pixel[:3])
            col += 1
            # Append list of 395 data points to the data structure
            if col == 395:
                self.imageData.append(row)
                row = []
                col = 0

        img.close()

    def parseControlFile(self, file: str) -> None:
        """
        Parse the control data points input file and store in controlData
        datastructure.

        @param file: path to control file data
        @return: None
        """
        with open(file) as f:
            for line in f:
                data = line.strip().split()
                for i in range(len(data)):
                    # Convert each item in list to int datatype from str
                    data[i] = int(data[i])
                self.controlData.append(data)

        f.close()

    def createNodes(self) -> None:
        """
        Create 500*395 nodes for each pixel on the terrain.png image file using
        the Node class from graphnodes.py . Get attribute information from
        elevationData, imageData and terrain dictionary structures for
        each node.
        @return:
        """

        for y in range(500):
            row = []
            for x in range(395):
                # Create node with x-coordinate and y-coordinate
                node = Node(y, x)
                # Classify node terrain using legend
                node.terrain = self.terrainLegend[self.imageData[y][x]]
                # Add elevation retrieved from mpp.txt file
                node.elevation = self.elevationData[y][x]
                # Add mobility from terrain legend
                node.mobility = self.terrainSpeed[node.terrain]
                row.append(node)
            self.nodeList.append(row)

    def beginSearch(self) -> None:
        """
        Iterate through list of control points and find a path for each pair
        iff one exists using A* search.

        @return: None
        """
        for i in range(len(self.controlData) - 1):
            # Prepare start and destination input for A* search
            start = self.nodeList[self.controlData[i][1]][
                self.controlData[i][0]
            ]
            destination = self.nodeList[self.controlData[i + 1][1]][
                self.controlData[i + 1][0]]
            self.aStarSearch(start, destination)

    def nodeWithLowestCost(self, nodeList: list[Node]) -> Node:
        """
        Helper function that returns the node with the lowest cost from a list
        of nodes.

        @param nodeList: List of nodes
        @return: node with the least cost associated with it
        """

        lowest_cost = float("inf")
        least_cost_node = None
        # Iterate through node list to find one with lowest cost
        for node in nodeList:
            if node.cost < lowest_cost:
                lowest_cost = node.cost
                least_cost_node = node
        return least_cost_node

    def getChildren(self, node: Node) -> list[Node]:
        """
        Function to get children of a node using its x and y Coordinates.

        @param node: node whose children need to be retrieved.
        @return: list of the children for a node
        """

        children = []
        x = node.xPos
        y = node.yPos

        # Children for pixels in a corner
        if x == 0 and y == 0:
            # Bottom left corner
            children.append(self.nodeList[x][y + 1])
            children.append(self.nodeList[x + 1][y])
        elif x == 0 and y == 394:
            # Top left corner
            children.append(self.nodeList[x + 1][y])
            children.append(self.nodeList[x][y - 1])
        elif x == 499 and y == 0:
            # Bottom right corner
            children.append(self.nodeList[x][y + 1])
            children.append(self.nodeList[x - 1][y])
        elif x == 499 and y == 394:
            # Top right corner
            children.append(self.nodeList[x - 1][y])
            children.append(self.nodeList[x][y - 1])
        # Children for pixels on edges
        elif x == 0 and 0 < y < 394:
            # Left edge
            children.append(self.nodeList[x + 1][y])
            children.append(self.nodeList[x][y + 1])
            children.append(self.nodeList[x][y - 1])
        elif x == 499 and 0 < y < 394:
            # Right edge
            children.append(self.nodeList[x - 1][y])
            children.append(self.nodeList[x][y + 1])
            children.append(self.nodeList[x][y - 1])
        elif 499 > x > 0 == y:
            # Bottom edge
            children.append(self.nodeList[x][y + 1])
            children.append(self.nodeList[x - 1][y])
            children.append(self.nodeList[x + 1][y])
        elif 0 < x < 499 and y == 394:
            # Top edge
            children.append(self.nodeList[x][y - 1])
            children.append(self.nodeList[x - 1][y])
            children.append(self.nodeList[x + 1][y])
        else:
            # Children for other pixels in the middle
            children.append(self.nodeList[x - 1][y])
            children.append(self.nodeList[x + 1][y])
            children.append(self.nodeList[x][y - 1])
            children.append(self.nodeList[x][y + 1])

        return children

    def getGScore(self, current: Node, child: Node) -> float:
        """
        Calculate and return cost associated for path between a node and its
        child (g(n)).

        @param current: Node at (x, y)
        @param child: child of the node at (x', y')
        @return: cost of path between two nodes
        """

        # Real world value for calculating distance
        longitude = 10.29
        latitude = 7.55

        if current.mobility == 0 or child.mobility == 0:
            return float('inf')

        # Ensure positive mobility values
        mobility_current = max(0.01, current.mobility)
        mobility_child = max(0.01, child.mobility)

        if current.xPos == child.xPos:
            # Determine which pixel the travel is on for speed value
            if current.yPos > child.yPos:
                mobility = current.mobility
            else:
                mobility = child.mobility
            # Travel along y-axis upwards or downwards / travel along longitude
            dist = (math.sqrt(
                (longitude ** 2) + (child.elevation - current.elevation) ** 2))
        else:
            if current.xPos > child.xPos:
                mobility = child.mobility
            else:
                mobility = current.mobility
            # Travel along x-axis left or right / travel along latitude
            dist = (math.sqrt(
                (latitude ** 2) + (child.elevation - current.elevation) ** 2))

        # speed = distance / time ; thus ; time = distance / speed
        # factor of 100**2 introduced to reduce clustering and repetition of nodes
        time = (dist / mobility) / (100 * 2)

        return time

    def getHScore(self, current: Node, destination: Node) -> float:
        """
        Return the heuristic cost (h(n)) for travelling from an arbitrary node
        to the destination. Here we assume there is a straightforward path from
        the node to the destination without any obstacles or restrictions.
        Formula used : Euclidian distance in a 3d plane.

        @param current: arbitrary node
        @param destination: final node in the path
        @return: cost of travel between the 2 nodes
        """

        # time = distance / speed. As for a heuristic we assume speed to be
        # uniform and constant i.e speed = 1

        cost = math.sqrt(
            ((current.xPos - destination.xPos) ** 2 +
             (current.yPos - destination.yPos) ** 2 +
             (current.elevation - destination.elevation) ** 2)
        )

        return cost

    def getFScore(self, node: Node, child: Node, destination: Node) -> float:
        """
        Calculate total score for travel between one node to another.
        f(n) = g(n) + h(n)

        @param node: arbitrary node
        @param child: child of the arbitrary node
        @param destination: final node in the path
        @return: cost of travel between an arbitrary node and its child.
        """
        cost = self.getGScore(node, child) + self.getHScore(node, destination)

        return cost

    def aStarSearch(self, start: Node, destination: Node) -> None:
        """
        A* search to find an optimal path between two nodes using heuristic
        guided search.

        @param start: Starting node at (x, y)
        @param destination: Destination node at (x', y')
        @return: None
        """

        # Exit case if the node is out of bounds
        if start.mobility == 0 or destination.mobility == 0:
            print("No path exists.")
            return

        # Predecessor map to keep track of the trail to construct final path
        predecessor = {start: None}
        start.cost = 0
        openList = [start]  # List of nodes yet to be visited
        closeList = []  # List of nodes that have been visited

        # Run algorithm till there are still more nodes left to be visited
        while len(openList) != 0:
            # Get node with the least cost from open list
            current = self.nodeWithLowestCost(openList)

            if current == destination:
                # path found. Construct path
                self.constructPath(current, start, predecessor)
                return

            # Node has been visited. Remove from open and add to closed list.
            openList.remove(current)
            closeList.append(current)

            # Get all children for the current node
            children = self.getChildren(current)
            for child in children:
                # If child has not been visited already
                if child not in closeList:
                    # Child has been discovered again but by a different route
                    if child in openList:
                        score = self.getFScore(current, child, destination)
                        if score < child.cost:
                            # Update the child's score to new lowest score
                            child.cost = score
                            # Update the child's parent to current node
                            predecessor[child] = current
                    # If this is the first time the node has been discovered
                    else:
                        # Get cost for the child
                        child.cost = self.getFScore(current, child,
                                                    destination)
                        # Update child's parent to current node
                        predecessor[child] = current
                        openList.append(child)

        print("No path exists.")

    def constructPath(self, node: Node, start: Node,
                      predecessorMap: dict) -> None:
        """
        Construct a path between start node and destination using the
        predecessor hashmap. Append the points in the path to finalPath
        instance variable.

        @param node: destination node
        @param start: start node
        @param predecessorMap: Hashmap with {node:parent} mapping
        @return: None
        """

        # Back track from destination node back to the start using the hashmap
        while node != start:
            point = [node.xPos, node.yPos, node.elevation]
            # Append the coordinates of the path to finalPath instance variable
            self.finalPath.insert(0, point)
            node = predecessorMap[node]

        # Append start to the finalPath instance variable
        point = [start.xPos, start.yPos, start.elevation]
        self.finalPath.insert(0, point)
        return

    def drawPath(self, file: str, outputFile: str) -> None:
        """
        Draw the path on the output image using (x,y) coordinates from the
        finalPath instance variable using PIL.

        @param file: path terrain image file
        @param outputFile: name for the output terrain map file with the path
        @return: None
        """

        img = Image.open(file)
        print(img.size)
        # Draw each pixel from the finalPath variable onto the terrain image
        for pixel in self.finalPath:
            img.putpixel((pixel[1], pixel[0]), (255, 0, 0))
        # Save output file with provided argument name
        self.putControlPixel(img)
        img.save(outputFile)
        img.close()

    def putControlPixel(self, img):
        """
        Helper function to put different color pixels on the control points and
        their direct linear and diagonal neighbors to highlight them on the
        final path.

        @param img: Image object
        @return:
        """
        color1 = (135, 31, 120)  # Light Purple RGB value tuple
        color2 = (77, 0, 75)  # Deep Purple RGB value tuple

        # Loop through all control points
        for item in self.controlData:
            # Get linear neighbors for a point A(x,y)
            linear_neighbors = [[item[0] + 1, item[1]],  # A(x+1, y)
                                [item[0] - 1, item[1]],  # A(x-1, y)
                                [item[0], item[1] + 1],  # A(x, y+1)
                                [item[0], item[1] - 1]]  # A(x, y-1)
            # Get diagonal neighbors for a point A(x,y)
            diagonal_neighbors = [[item[0] - 1, item[1] + 1],  # A(x-1, y+1)
                                  [item[0] + 1, item[1] + 1],  # A(x+1, y+1)
                                  [item[0] - 1, item[1] - 1],  # A(x-1, y-1)
                                  [item[0] + 1, item[1] - 1]]  # A(x+1, y-1)
            # Put deep purple pixel at each linear neighbor
            print(linear_neighbors)
            for neighbor in linear_neighbors:
                x, y = neighbor
                if 0 <= x < img.width and 0 <= y < img.height:
                    img.putpixel((x, y), color2)
            # Put deep purple pixel at each diagonal neighbor
            for neighbor in diagonal_neighbors:
                x, y = neighbor
                if 0 <= x < img.width and 0 <= y < img.height:
                    img.putpixel((x, y), color2)
            # Put light purple pixel at control point
            img.putpixel((item[0], item[1]), color1)
        return

    def getFinalDistance(self) -> float:
        """
        Using the points from finalPath calculate the total 3D distance
        travelled along the path.

        @return:None
        """
        longitude = 10.29
        latitude = 7.55

        distance = 0

        # Iterate through each coordinate and calculate distance
        for i in range(len(self.finalPath) - 1):
            z1 = self.finalPath[i][2]
            z2 = self.finalPath[i + 1][2]

            if self.finalPath[i][0] == self.finalPath[i + 1][0]:
                # Travel along y-axis upwards or downwards / travel along longitude
                distance += math.sqrt((longitude ** 2) + ((z1 - z2) ** 2))
            else:
                # Travel along x-axis left or right / travel along latitude
                distance += math.sqrt((latitude ** 2) + ((z1 - z2) ** 2))

        return round(distance, 3)


def validateInput(arguments) -> tuple:
    """
    Helper function to check if sufficient arguments were provided via
    commandline.

    @param arguments: Commandline arguments
    @return: List of file names
    """
    if len(arguments) < 5:
        exit("Insufficient arguments. Usage : python3 lab1.py {terrain.png} "
             "{mpp.txt} {red.txt} {redOut.png} ")
    else:
        return arguments[1], arguments[2], arguments[3], arguments[4]


def main() -> None:
    """
    Main function to read commandline arguments and start with Orienteering.
    @return: None
    """
    terrain_image, elevations, controlPoints, outputFile = validateInput(
        argv)
    o = Orienteering()
    o.parseInput(elevations, terrain_image, controlPoints)
    o.beginSearch()
    o.drawPath(terrain_image, outputFile)
    print(f"Total distance travelled : {o.getFinalDistance()} meters")


if __name__ == "__main__":
    main()
