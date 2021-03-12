#!/usr/bin/env python3
from Stack import Stack
from copy import deepcopy
import time
import sys
import random
import math
import heapq

rows = 5
columns = 5
goal = [
    [1, 2, 3, 4, 5],
    [6, 7, 8, 9, 10],
    [11, 12, 13, 14, 15],
    [16, 17, 18, 19, 20],
    [21, 22, 23, 24, 0]
]

# rows = 3
# columns = 3
# goal = [
#     [1, 2, 3],
#     [4, 5, 6],
#     [7, 8, 0]
# ]

initial = []

quiet = False

# Helper function to determine if the current state matches the goal state
def goalTest(state):
    failCount = 0
    for i in range(rows):
        for j in range(columns):
            if state[i][j] != goal[i][j]:
                failCount += 1
    
    if failCount > 0:
        return False
    else:
        return True

# Helper function to get coordinates of empty space
def getEmptySpace(state):
    emptySpace = ()
    for i in range(rows):
        for j in range(columns):
            if state[i][j] == 0:
                emptySpace = (i, j)
                break
    return emptySpace

# Helper function to gather coordinates of neighbors of empty space
def getNeighbors(state):
    neighbors = []
    emptySpace = getEmptySpace(state)

    # Neighbor above
    if emptySpace[0] - 1 >= 0:
        neighbors.append((emptySpace[0] - 1, emptySpace[1]))

    # Neighbor below
    if emptySpace[0] + 1 < rows:
        neighbors.append((emptySpace[0] + 1, emptySpace[1]))

    # Neighbor left
    if emptySpace[1] - 1 >= 0:
        neighbors.append((emptySpace[0], emptySpace[1] - 1))

    # Neighbor right
    if emptySpace[1] + 1 < columns:
        neighbors.append((emptySpace[0], emptySpace[1] + 1))
    
    # print(neighbors)
    return neighbors

# Helper function to build options based on neighbors
def buildOptions(state):
    neighbors = getNeighbors(state)
    emptySpace = getEmptySpace(state)
    # print(emptySpace)
    options = []
    for i in neighbors:
        tempState = []
        tempState = deepcopy(state)
        tempElement = tempState[i[0]][i[1]]
        # print(i)
        tempState[emptySpace[0]][emptySpace[1]] = tempElement
        tempState[i[0]][i[1]] = 0
        options.append(tempState)
        # print(state)
    return options

# Helper funciton to determine if two states are the same
def areEqualStates(a, b):
    failCount = 0
    for i in range(rows):
        for j in range(columns):
            if a[i][j] != b[i][j]:
                failCount += 1
                break

    if failCount > 0:
        return False
    else:
        return True

# Helper function to check is a neighbor is in a list 
def neighborInExplored(neighbor, explored):
    failCount = 0
    matches = False
    for exploredList in explored:
        failCount = 0
        for i in range(rows):
            for j in range(columns):
                if exploredList[i][j] != neighbor[i][j]:
                    failCount += 1
        
        if failCount == 0:
            matches = True
            break
    return matches

# Helper funciton to print the state in a readable order
def printState(state):
    print('------------')
    for i in state:
        print(i)
    print('------------')

# Helper function to generate initial state
def generateInitial():
    values = random.sample(range(0, (rows * columns)), (rows * columns))
    valuesIndex = 0
    result = []
    for i in range(rows):
        list1 = []
        for j in range(columns):
            list1.append(values[valuesIndex])
            valuesIndex += 1
        result.append(list1)
    return result

# Helper function which returns the number of misplaced tiles of a state compared to the goal
def getNumberOfMisplaced(state):
    failCount = 0
    for i in range(rows):
        for j in range(columns):
            if state[i][j] != goal[i][j]:
                failCount += 1
    
    return failCount

# Helper function to sort the options based on misplaced tiles
def getStatesH1(state):
    options = buildOptions(state)
    optionsWithH1 = []
    for option in options:
        numMisplaced = getNumberOfMisplaced(option)
        optionsWithH1.append((option, numMisplaced))
    optionsWithH1.sort(key = lambda x: x[1])
    return optionsWithH1

# Helper function to get the Manhattan Distance between two points
def getDistanceBetweenPoints(x, y):
    # print("1", x, y, (abs(x[1] - x[0]) + abs(y[1] - y[0])))
    # print("2", x, y, (math.sqrt((x[1] - x[0]) ** 2 + (y[1] - y[0]) ** 2)))
    # print(x, y)
    # distance = abs(x[1] - x[0]) + abs(y[1] - y[0])
    distance = abs(x[1] - y[1]) + abs(x[0] + y[0])
    
    # print("3", x, y, distance)
    return distance

# Helper function to get coordinates of any element
def getCoordinates(state, element):
    space = ()
    for i in range(rows):
        for j in range(columns):
            if state[i][j] == element:
                space = (i, j)
                break
    return space

# Helper function for heuristic 2
def getSumDistance(state):
    stateList = []
    for i in range(rows):
        for j in range(columns):
            stateList.append(state[i][j])
    distance = sum(abs((val-1)%3 - i%3) + abs((val-1)//3 - i//3)
        for i, val in enumerate(stateList) if val)
    return distance

# Helper function to sort the options based on distance sums
def getStatesH2(state):
    options = buildOptions(state)
    optionsWithH2 = []
    for option in options:
        distanceSum = getSumDistance(option)
        optionsWithH2.append((option, distanceSum))
    optionsWithH2.sort(key = lambda x: x[1])
    return optionsWithH2

# Heuristic 1 using a heapq (priority queue)
def h1Heap(initial):
    # Create frontier heap
    frontier = []
    heapq.heapify(frontier)

    explored = []
    frontierList = []
    # Add initial state to frontier
    heapq.heappush(frontier, (initial, getNumberOfMisplaced(initial)))
    frontierList.append(initial)
    # Go through the heap until it is empty 
    while len(list(frontier)) > 0:
        # Pop the element from the heap
        state = heapq.heappop(frontier)
        # print(state)
        # Add it to explored
        explored.append(state[0])

        if not quiet:
            printState(state[0])
            # print(state[0])

        # Check if the current state is the goal state
        if goalTest(state[0]):
            return "Success"

        # Get move states ordered by misplaced tiles
        options = getStatesH1(state[0])
        # print(options)
        for neighbor in options:
            if not neighborInExplored(neighbor[0], explored) and not neighborInExplored(neighbor[0], frontierList):
                heapq.heappush(frontier, neighbor)
                frontierList.append(neighbor[0])
    return "FAILURE"


# Heuristic 1
# Number of misplaced tiles
def h1(initial):
    explored = []

    state = initial

    # Go until goal state is met
    while not goalTest(state):
        explored.append(state)
        printState(state)
        temp = state
        # Get move states ordered by misplaced tiles
        options = getStatesH1(state)
        for neighbor in options:
            # If neighbor hasn't been explored yet make it the state and break the loop
            if not neighborInExplored(neighbor[0], explored):
                state = neighbor[0]
                break
        if areEqualStates(temp, state):
            return "FAILURE"
    printState(state)
    return "SUCCESS"

# Heuristic 2
# Sum of the distances of every tile to its goal position
def h2(initial):
    explored = []

    state = initial
    
    # Go until goal state is met
    while not goalTest(state):
        explored.append(state)
        printState(state)
        # Get move states ordered by heuristic 2
        options = getStatesH2(state)
        temp = state
        for neighbor in options:
            # If neighbor hasn't been explored yet make it the state and break the loop
            if not neighborInExplored(neighbor[0], explored):
                state = neighbor[0]
                break
        if areEqualStates(temp, state):
            return "FAILURE"
    printState(state)
    return "SUCCESS"

# Heuristic 2 using a heapq (priority queue)
def h2Heap(initial):
    # Create frontier heap
    frontier = []
    heapq.heapify(frontier)

    explored = []
    frontierList = []
    # Add initial state to frontier
    heapq.heappush(frontier, (initial, getNumberOfMisplaced(initial)))
    frontierList.append(initial)
    # Go through the heap until it is empty 
    while len(list(frontier)) > 0:
        # Pop the element from the heap
        state = heapq.heappop(frontier)
        # print(state)
        # Add it to explored
        explored.append(state[0])

        if not quiet:
            printState(state[0])
            # print(state[0])

        # Check if the current state is the goal state
        if goalTest(state[0]):
            return "Success"

        # Get move states ordered by misplaced tiles
        options = getStatesH2(state[0])
        # print(options)
        for neighbor in options:
            if not neighborInExplored(neighbor[0], explored) and not neighborInExplored(neighbor[0], frontierList):
                heapq.heappush(frontier, neighbor)
                frontierList.append(neighbor[0])
    return "FAILURE"

def runSearch(mode):
    if mode.lower() == "h1":
        start_time = time.time()
        print(h1(initial))
        elapsed_time = time.time() - start_time
        print('Heuristic 1 finished in {}'.format(elapsed_time))
    elif mode.lower() == "h2":
        start_time = time.time()
        print(h2(initial))
        elapsed_time = time.time() - start_time
        print('Heuristic 2 finished in {}'.format(elapsed_time))
    elif mode.lower() == "h1heap":
        start_time = time.time()
        print(h1Heap(initial))
        elapsed_time = time.time() - start_time
        print('Heuristic 1 finished in {}'.format(elapsed_time))
    elif mode.lower() == "h2heap":
        start_time = time.time()
        print(h2Heap(initial))
        elapsed_time = time.time() - start_time
        print('Heuristic 2 finished in {}'.format(elapsed_time))

initial = generateInitial()
quiet = False
if len(sys.argv) >= 3:
    if sys.argv[2] == "--quiet":
        quiet = True
runSearch(sys.argv[1])
