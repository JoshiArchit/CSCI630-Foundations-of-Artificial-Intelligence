"""
Filename : lab1.py
Author : Archit Joshi
Description : CSCI630 - Lab 1 : Summer Orienteering. Implementation of the A*
algorithm to find the shortest distance across an orienteering trail with
different elevations.
Language : python3
"""


class Orienteering:
    """
    Class with methods to superimpose terrain and elevation data,
    construct a graph and initiate A* search.
    """
    __slots__ = 'imageData', 'controlData', 'elevationData', 'nodeList', 'finalPath', 'gScore'

    def __init__(self):
        """
        Constructor for initiating empty variables.
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

    def parseElevationFile(self, file):
        """
        Parse 500*400 mpp.txt file data and store 500*395 data points in
        elevationData datastructure. Convert each data point to float before
        storage.

        :param file: path to file containing elevation data.
        :return: None
        """

        with open(file) as f:
            for line in f:
                # Skip last 5 entries to read only 395 entries in each row
                row = line.strip().split()[:-5]
                # Convert long to float value
                for i in range(len(row)):
                    row[i] = float(row[i])
                self.elevationData.append(row)
        f.close()

    def parseImageFile(self, file):
        pass

    def parseControlFile(self, file):
        pass

    def createNodes(self):
        pass


def validateInput(arguments):
    """
    Helper function to validate input.
    :param arguments: commandline arguments
    :return: paths to input files
    """

    if len(arguments) < 5:
        exit("Insufficient arguments. Usage : python3 lab1.py {terrain.png} "
             "{mpp.txt} {red.txt} {redOut.png} ")
    else:
        return arguments[1], arguments[2], arguments[3], arguments[4]


def main():
    """
    Main function to initiate search for the shortest path.
    :return: None
    """
    terrain_image, elevations, controlPoints, outputFile = validateInput(argv)


if __name__ == "__main__":
    main()
