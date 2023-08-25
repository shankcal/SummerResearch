import copy

from SummerResearchLib.ShubertCalculus import *

f = open("Calc1Output.txt", "w")

calc = ReflectionCalculator(4)
result = calc.calculateAll()
f.write(result)

f.close()

