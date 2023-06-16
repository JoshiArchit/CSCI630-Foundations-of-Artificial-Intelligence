"""
Filename : hw1WordLadder.py
Author : Archit Joshi
Description : CSCI630 - Foundations of Artificial Intelligence Homework 1.
Implementation of a word ladder.
Objective : Finding the path from one word to another using a dictionary of
valid words. Only one letter from starting word can be changed at each step.
Language : python3
"""

from collections import defaultdict, deque
from sys import argv
from typing import Any

class SearchDictionary:
    """
    class to create adjacency list and find path between two words from a
    dictionary of valid words.
    """

    def getInput(self, arguments : list) -> tuple:
        """
        Helper function to accept and validate commandline arguments.

        :param arguments: commandline arguments
        :return: argument list
        """
        try:
            if not arguments[1]:
                # If arguments weren't received, exit with error message
                exit(print(
                    "Usage: python hw1 <dictionary_path> <start_word> <end_word>"))
            else:
                # initialise inputs
                dictionary = arguments[1]
                start = arguments[2]
                end = arguments[3]

                return dictionary, start, end
        except:
            raise FileNotFoundError(
                "File does not exist / File path is incorrect")

    def adjacencyList(self, dictionary_path: str, start: str) -> dict:
        """
            Function to read the dictionary of legal english words and create an
            adjacency list (graph) to find all possible intermediate neighbors.

            :param dictionary_path: path to the dictionary of legal english words
            :param start: start word
            :return: adjacency list (dictionary of lists)
        """
        # Empty dictionary of lists which will act as adjacency list
        adjacency_list = defaultdict(list)

        # Open and read each word in the file
        with open(dictionary_path) as f:
            for word in f:
                word = word.strip()
                # Intermediate words need to be the same length as the inputs
                if len(word) == len(start):
                    for j in range(len(word)):
                        # Find all permutations/neighbors resulting from
                        # replacing one character
                        intermediate = word[:j] + "_" + word[j + 1:]
                        adjacency_list[intermediate].append(word)

        return adjacency_list

    def breadthFirstSearch(self, start: str, end: str,
                           adjacency_list: dict) -> Any:
        """
        Breadth first search to find the shortest path from the start word to
        the end word which can be reached by changing once character at a time.

        :param start: start word
        :param end: end word
        :param adjacency_list: graph representation of all neighbor permutations
        :return: shortest path iff it exists
        """

        # Predecessor map to keep a track of the shortest path
        predecessor = {start: None}
        # Queue to keep track of current root node
        queue = deque([start])
        # List to accumulate the shortest path
        path = []

        #
        while queue:
            for i in range(len(queue)):
                current = queue.popleft()
                if current == end:
                    break
                for j in range(len(current)):
                    # Check for all possible permutations of current word
                    intermediate = current[:j] + "_" + current[j + 1:]
                    # Get all neighbors which haven't been visited
                    for neighbor in adjacency_list[intermediate]:
                        if neighbor not in predecessor:
                            # Add neighbor to predecessor map
                            predecessor[neighbor] = current
                            queue.append(neighbor)

        # If the path from start to end was found
        if end in predecessor:
            # Construct the path in reverse from end to start using the
            # predecessor map
            current = end
            while current != start:
                path.insert(0, current)
                current = predecessor[current]
            path.insert(0, start)
            return path
        else:
            # No path was found
            return None

    def startSearch(self) -> None:
        """
        Helper function to parse input and begin search for the shortest path.

        :return: None
        """

        # Parse commandline input
        file, start, end = self.getInput(argv)
        # Create adjacency list
        graph = self.adjacencyList(file, start)
        # Find the shortest path
        path = self.breadthFirstSearch(start, end, graph)

        # Print path iff exists else print "No solution"
        if path:
            for item in path:
                print(item)
        else:
            print("No solution")


def main():
    """
        Main driver function.

        :return: None
        """

    s = SearchDictionary()
    s.startSearch()


if __name__ == "__main__":
    main()
