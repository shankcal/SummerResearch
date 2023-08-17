import itertools
from SummerResearchLib.ShubertCalculus import *

# Key takeaway: Any point with 2 indeterminate values of the form (a|x|y), (x|a|y), or (x|y|a) where a is in
# {1,2,3,...,3bar,2bar} has exactly one solution

# Solutions:
# a in {1, 4, 5, 6,..., 4bar}:
# (a|x|y) -> (a|2bar|3bar)
# (x|a|y) -> (2bar|a|3bar)
# (x|y|a) -> (2bar|3bar|a)

# a in {3, 3bar}:
# (a|x|y) -> (a|2bar|4bar)
# (x|a|y) -> (2bar|a|4bar)
# (x|y|a) -> (2bar|4bar|a)

# a in {2, 2bar}
# (a|x|y) -> (a|3bar|4bar)
# (x|a|y) -> (3bar|a|4bar)
# (x|y|a) -> (3bar|4bar|a)

def create_1_X_Y_points(default):
    pointList = []
    x_y_list = list(itertools.permutations(numberPool, 2))

    for x,y in x_y_list:
        pointList.append(Point(default, x, y))

    return pointList


def create_X_1_Y_points(default):
    pointList = []
    x_y_list = list(itertools.permutations(numberPool, 2))

    for x,y in x_y_list:
        pointList.append(Point(x, default, y))

    return pointList

def create_X_Y_1_points(default):
    pointList = []
    x_y_list = list(itertools.permutations(numberPool, 2))

    for x,y in x_y_list:
        pointList.append(Point(x, y, default))

    return pointList

def findMaximalPoints(pointList):
    maximalPoints = []

    for maximalPointCandidate in pointList:
        foundGreaterPoint = False
        for otherPoint in pointList:
            if otherPoint > maximalPointCandidate:
                foundGreaterPoint = True
                break
        if not foundGreaterPoint:
            maximalPoints.append(maximalPointCandidate)

    return maximalPoints

numberPool = [SignedInt(6, True), SignedInt(5, True), SignedInt(4, True), SignedInt(3, True)]

defaultNum = SignedInt(2, True)

list1 = create_1_X_Y_points(defaultNum)
maximalList1 = findMaximalPoints(list1)

list2 = create_X_1_Y_points(defaultNum)
maximalList2 = findMaximalPoints(list2)

list3 = create_X_Y_1_points(defaultNum)
maximalList3 = findMaximalPoints(list3)


print("List 1:")
for item in maximalList1:
    print(item.toTeX())

print("List 2:")
for item in maximalList2:
    print(item.toTeX())

print("List 3:")
for item in maximalList3:
    print(item.toTeX())