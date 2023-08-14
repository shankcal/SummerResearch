import copy

from SummerResearchLib.ShubertCalculus import *

nb1 = SignedInt(1, False)
nb2 = SignedInt(2, False)
nb3 = SignedInt(3, False)
b1 = SignedInt(1, True)
b2 = SignedInt(2, True)
b3 = SignedInt(3, True)

point1 = Point.fromString("(2 | 3 | 1  )")

t1t2 = Reflection(1, 2)  # t_1 - t_2
t1t3 = Reflection(1, 3)  # t_1 - t_3
t2t3 = Reflection(2, 3)  # t_2 - t_3
t1tk = Reflection(1, 0)  # t_1 - t_k
t2tk = Reflection(2, 0)  # t_2 - t_k
t3tk = Reflection(3, 0)  # t_3 - t_k

calcLists = []

calcLists.append([t1tk])               # (1, 1, 1)
calcLists.append([t1t2, t2tk])         # (1, 0, 0) + (0, 1, 1)
calcLists.append([t2tk, t1t2])         # (0, 1, 1) + (1, 0, 0)
calcLists.append([t1t3, t3tk])         # (1, 1, 0) + (0, 0, 1)
calcLists.append([t3tk, t1t3])         # (0, 0, 1) + (1, 1, 0)
calcLists.append([t1t2, t2t3, t3tk])   # (1, 0, 0) + (0, 1, 0) + (0, 0, 1)
calcLists.append([t1t2, t3tk, t2t3])   # (1, 0, 0) + (0, 0, 1) + (0, 1, 0)
calcLists.append([t2t3, t1t2, t3tk])   # (0, 1, 0) + (1, 0, 0) + (0, 0, 1)
calcLists.append([t2t3, t3tk, t1t2])   # (0, 1, 0) + (0, 0, 1) + (1, 0, 0)
calcLists.append([t3tk, t2t3, t1t2])   # (0, 0, 1) + (0, 1, 0) + (1, 0, 0)
calcLists.append([t3tk, t1t2, t2t3])   # (0, 0, 1) + (1, 0, 0) + (0, 1, 0)

resultsPoints = []
resultsTeX = []


# This function performs all the reflections on the given point using a list of reflections. The program also generates
# LaTeX code to show all the intermediate steps of the reflections. The function returns a tuple with the 0th entry
# being the actual point after all the reflections and the 1st entry a string of the LaTeX code.
def performReflections(point, reflections):
    pointCopy = copy.deepcopy(point)
    TeX = []
    TeX.append(r"\[")
    TeX.append(pointCopy.toTeX())
    for reflection in reflections:
        TeX.append(reflection.toTeX())
        reflection.execute(pointCopy)
        TeX.append(pointCopy.toTeX())

    TeX.append(r"\]")

    return pointCopy, ''.join(TeX)


# Perform all the calcuations given in the calcLists to point1.
for calc in calcLists:
    (resultPoint, resultTeX) = performReflections(point1, calc)
    resultsPoints.append(resultPoint)
    resultsTeX.append(resultTeX + "\n")

f = open("CurveNeighboorhoodCalcsOutput.txt", "w")

maximalPoints = []


# This alrgotithm finds all the maximal points. For each point, the program loops through every point until or unless
# it finds a point that is strictly greater than the point current point of the outer loop. Any point not found to have
# any strictly greater points is added to the maximal points list.
for point_i in resultsPoints:
    foundGreaterPoint = False

    for point_j in resultsPoints:
        if point_i < point_j:
            foundGreaterPoint = True
            break

    if not foundGreaterPoint:
        maximalPoints.append(point_i)


f.write("Reflection Calculations: \n")
f.writelines(resultsTeX)
f.write("Maximal Points: \n")
f.writelines([point.toTeX() + "\n" for point in maximalPoints])

f.close()

test = ReflectionCalculator((1,1,2))

items = test.reflectionList
for item in items:
    for reflection in item:
        print(reflection.toTeX())
    print()