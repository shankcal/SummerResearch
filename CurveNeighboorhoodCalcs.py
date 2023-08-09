import copy

from SummerResearchLib.ShubertCalculus import *

nb1 = SignedInt(1, False)
nb2 = SignedInt(2, False)
nb3 = SignedInt(3, False)
b1 = SignedInt(1, True)
b2 = SignedInt(2, True)
b3 = SignedInt(3, True)

point1 = Point(nb1, nb2, nb3)

t1t2 = Reflection(1, 2)  # t_1 - t_2
t1t3 = Reflection(1, 3)  # t_1 - t_3
t2t3 = Reflection(2, 3)  # t_2 - t_3
t1tk = Reflection(1, 0)  # t_1 - t_k
t2tk = Reflection(2, 0)  # t_2 - t_k
t3tk = Reflection(3, 0)  # t_3 - t_k

calcLists = []

calcLists.append([t1tk])
calcLists.append([t1t2, t2tk])
calcLists.append([t2tk, t1t2])
calcLists.append([t1t3, t3tk])
calcLists.append([t3tk, t1t3])
calcLists.append([t1t2, t2t3, t3tk])
calcLists.append([t1t2, t3tk, t2t3])
calcLists.append([t2t3, t1t2, t3tk])
calcLists.append([t2t3, t3tk, t1t2])
calcLists.append([t3tk, t2t3, t1t2])
calcLists.append([t3tk, t1t2, t2t3])

resultsPoints = []
resultsTeX = []

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

for calc in calcLists:
    (resultPoint, resultTeX) = performReflections(point1, calc)
    resultsPoints.append(resultPoint)
    resultsTeX.append(resultTeX + "\n")

f = open("CurveNeighboorhoodCalcsOutput.txt", "w")

maximalPoints = []

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