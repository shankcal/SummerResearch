from SummerResearchLib.ShubertCalculus import *


f = open("Calc2Output.txt", "w")

point = Point.fromString("(1|2|3)")
calculator = ReflectionCalculator((1, 1, 2), point)
result = calculator.calculateAll()

f.write(result)