import copy

from SummerResearchLib.ShubertCalculus import *

f = open("CurveNeighboorhoodCalcsOutput.txt", "w")

point = Point.fromString("(1|2|3)")
calculator = ReflectionCalculator((1, 1, 1), point)
result = calculator.calculateAll()

f.write(result)

f.close()

