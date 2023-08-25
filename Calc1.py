import copy

from SummerResearchLib.ShubertCalculus import *

f = open("Calc1Output.txt", "w")

calc = ReflectionCalculator(8, verbosity=0)
result = calc.calculateAll()
f.write(result)

f.close()

