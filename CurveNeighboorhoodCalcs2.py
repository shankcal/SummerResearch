from SummerResearchLib.ShubertCalculus import *


f = open("CurveNeighboorhoodCalcsOutput2.txt", "w")

point = Point.fromString("(1|2|3)")
calculator = ReflectionCalculator((1, 1, 2), point)
result = calculator.calculateAll()

f.write(result)