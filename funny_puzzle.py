import heapq
from queue import PriorityQueue
import numpy as np

""" 
INPUT: 
    Two states (if second state is omitted then it is assumed that it is the goal state)

RETURNS:
    A scalar that is the sum of Manhattan distances for all tiles.
"""
def get_manhattan_distance(from_state, to_state=[1, 2, 3, 4, 5, 6, 7, 0, 0]):
    distance = 0
    
    for countFrom in range(len(from_state)):
        if from_state[countFrom] == 0:
            # print("if", from_state[countFrom])
            continue
        else:
            # print("else", from_state[countFrom])
            # Find xy of from_state number
            tempCount = 0
            nextRow = 0
            for findxy in range(len(from_state)):
                if from_state[findxy] == from_state[countFrom]:
                    if tempCount > 5:
                        nextRow += 2
                        tempCount += -6
                    if tempCount > 2:
                        nextRow += 1
                        tempCount += -3
                    fromX = tempCount
                    fromY = nextRow
                    break
                else:
                    tempCount += 1
            # Find xy of to_state number
            tempCount = 0
            nextRow = 0
            for findxy in range(len(to_state)):
                if to_state[findxy] == from_state[countFrom]:
                    if tempCount > 5:
                        nextRow += 2
                        tempCount += -6
                    if tempCount > 2:
                        nextRow += 1
                        tempCount += -3
                    toX = tempCount
                    toY = nextRow
                    break
                else:
                    tempCount += 1
            
            manhattan = abs(fromX - toX) + abs(fromY - toY)
            #print("num:", from_state[countFrom], "fromX:", fromX, "fromY:", fromY, "toX:", toX, "toY:", toY, "manhattan:", manhattan)
            distance += manhattan
            """
            tempDistance = 0
            nextRow = 0
            for countTo in range(len(to_state)):
                if from_state[countFrom] == to_state[countTo]:
                    if tempDistance > 3: # Down a row
                        nextRow += 1
                        tempDistance += -3
                    if tempDistance > 3: # Down another row
                        nextRow += 1
                        tempDistance += -3
                    manhattan = abs(tempDistance - 0) + abs(nextRow - 0)
                    print("from_state:", from_state[countFrom], "to_state:", to_state[countTo], "tempDistance:", tempDistance, "nextRow:", nextRow, "manhattan:", manhattan)
                    distance += manhattan
                    break
                else:
                    tempDistance += 1
    """
            
    return distance

"""
INPUT: 
    A state (list of length 9)

WHAT IT DOES:
    Prints the list of all the valid successors in the puzzle. 
"""
def print_succ(state):
    succ_states = get_succ(state)

    for succ_state in succ_states:
        print(succ_state, "h={}".format(get_manhattan_distance(succ_state)))


def swapHelper(state, x, y):
    swapped = state[:]
    temp = swapped[x]
    swapped[x] = swapped[y]
    swapped[y] = temp

    return swapped

"""
INPUT: 
    A state (list of length 9)

RETURNS:
    A list of all the valid successors in the puzzle (don't forget to sort the result as done below). 
"""
def get_succ(state):
    possibleSwaps = {
        '0':[1,3],
        '1':[0,2,4],
        '2':[1,5],
        '3':[0,4,6],
        '4':[1,3,5,7],
        '5':[2,4,8],
        '6':[3,7],
        '7':[4,6,8],
        '8':[5,7],
    } # Indices

    succ_states = []

    # First zero in index
    zero1 = state.index(0)
    for x in possibleSwaps[str(zero1)]:
        swap = state[:]
        temp = swap[zero1]
        swap[zero1] = swap[x]
        swap[x] = temp

        if swap == state:
            continue
        else:
            succ_states.append(swap)

    # Second zero in index
    subsetOffsetLength = len(state[:zero1]) + 1
    subsetState = state[zero1+1:]
    zero2 = subsetState.index(0) + subsetOffsetLength
    for x in possibleSwaps[str(zero2)]:
        swap = state[:]
        temp = swap[zero2]
        swap[zero2] = swap[x]
        swap[x] = temp

        if swap == state:
            continue
        else:
            succ_states.append(swap)

    return sorted(succ_states)

"""
INPUT: 
    An initial state (list of length 9)

OUTPUT:
    Prints a path of configurations from initial state to goal state along  h values, number of moves, and max queue number in the format specified in the pdf.
"""
def solve(state, goal_state=[1, 2, 3, 4, 5, 6, 7, 0, 0]):
    # closed, opened, visited = []
    closed = []
    opened = []
    visited = []
    maxQueueLength = []
    parent = 0
    openedMaxLength = 0
    heapq.heappush(opened, (get_manhattan_distance(state), state, (parent, get_manhattan_distance(state), -1)))

    while True:
        if len(opened) == 0:
            break # open is empty

        tempState = heapq.heappop(opened)
        closed.append(tempState)
        maxQueueLength.append(tempState[1])

        gStartNode = tempState[2][0] + 1
        # print("gStartNode:", gStartNode)

        if tempState[1] == goal_state:
            break # SOLVED

        next = get_succ(tempState[1])
        for testTempState in next:
            whileH = get_manhattan_distance(testTempState)
            # print("whileH:", whileH)
            temp = (gStartNode + whileH, testTempState, (gStartNode, whileH, parent)) # Next
            # print("temp:", temp)
            if testTempState in maxQueueLength:
                # print("CONTINUE")
                continue

            heapq.heappush(opened, temp)

        parent += 1
        # print("parent:", parent)
        # print("len(opened):", len(opened))
        # print("openedMaxLength:", openedMaxLength)
        if len(opened) > openedMaxLength:
            openedMaxLength = len(opened)
        visited.extend(next)

    # Solution Path to print
    node = closed[-1]
    solutionPath = []
    while node[2][2] > 0:
        node = closed[node[2][2]]
        # print("node:", node)
        solutionPath.append(node)

    begin = (get_manhattan_distance(state), state, (0, get_manhattan_distance(state), -1))
    # print("begin:", begin)
    solutionPath.append(begin)
    solutionPath.reverse()
    solutionPath.append(tempState)
    # print("tempState:", tempState)
    # print("solutionPath[0][1]:", solutionPath[0][1])
    # print("solutionPath[0][2][0]:", solutionPath[0][2][0])
    # print("solutionPath[0][2][1]:", solutionPath[0][2][1])
    for i in range(len(solutionPath)):
        currentMove = str(solutionPath[i][1])
        # print("solutionPath[i][1]:", solutionPath[i][1])
        toPrintH = str(solutionPath[i][2][1])
        # print("solutionPath[i][2][1]:", solutionPath[i][2][1])
        totalMoves = str(solutionPath[i][2][0])
        # print("solutionPath[i][2][0]:", solutionPath[i][2][0])
        print(currentMove + " h=" + toPrintH + " moves: " + totalMoves)
    print("Max queue length:", openedMaxLength)


if __name__ == "__main__":
    print_succ([2,5,1,4,0,6,7,0,3])
    print()

    print(get_manhattan_distance([2,5,1,4,0,6,7,0,3], [1, 2, 3, 4, 5, 6, 7, 0, 0]))
    #print(get_manhattan_distance([2,5,1,4,3,6,7,0,0], [1, 2, 3, 4, 5, 6, 7, 0, 0]))
    print()

    solve([2,5,1,4,0,6,7,0,3])
    print()
    solve([4,3,0,5,1,6,7,2,0])
    print()
    solve([3,4,6,0,0,1,7,2,5])
    print()
