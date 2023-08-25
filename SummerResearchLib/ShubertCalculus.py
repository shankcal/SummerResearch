# SignedInt takes two parameters as input. First it takes an int which represents the value and a boolean which
# represents weather or not the value is barred. Values should always be positive and nonzero.
# In this system 1 < 2 < ... < n < nbar < n-1bar < ... < 2bar < 1bar
import copy
import itertools
import re

class IncompatiblePointOperationError(ValueError):
    pass


class SignedInt:
    def __init__(self, val, bar):
        self.val = val
        self.bar = bar

    @classmethod
    def fromString(cls, string):
        if string.endswith("bar"):
            val = int(string.rstrip("bar"))
            bar = True
        else:
            val = int(string)
            bar = False
        return cls(val, bar)

    # This property is invoked any time two signed ints are compared. The property returns an int which can then
    # be compared with the normal <, >, <=, >= operators.
    @property
    def comparisonVal(self):
        sign = -1 if self.bar else 1
        return sign * (self.val - 999999)

    def __eq__(self, other):
        a = self.comparisonVal
        b = other.comparisonVal
        return a == b

    def __ne__(self, other):
        a = self.comparisonVal
        b = other.comparisonVal
        return a != b

    def __neg__(self):
        return SignedInt(self.val, not self.bar)

    def __le__(self, other):
        a = self.comparisonVal
        b = other.comparisonVal
        return a <= b

    def __lt__(self, other):
        a = self.comparisonVal
        b = other.comparisonVal
        return a < b

    def __gt__(self, other):
        a = self.comparisonVal
        b = other.comparisonVal
        return a > b

    def __ge__(self, other):
        a = self.comparisonVal
        b = other.comparisonVal
        return a >= b

    # Returns latex code to represent the number.
    def __str__(self):
        if self.bar:
            return f"\\bar{{{str(self.val)}}}"
        else:
            return str(self.val)

    def __repr__(self):
        return f"SignedInt({self.val}, {self.bar})"


# Points are as  a 3 element list of SignedInts representing the point itself and a list of reflected points.
# Currently, the list of reflected points is unused however it may be used in the future.
class Point:
    def __init__(self, *args):
        self.reflectedPointsCount = 0
        self.determinant = True
        self.pointList = []
        for arg in args:
            self.pointList.append(arg)

    def __eq__(self, other):
        self._checkComparibility(other)
        return self.pointList == other.pointList

    def __len__(self):
        return len(self.pointList)

    def __ne__(self, other):
        self._checkComparibility(other)
        return self.pointList != other.pointList

    def __ge__(self, other):
        self._checkComparibility(other)
        retVal = True
        for i in range(len(self.comparisonArray)):
            if not (self.comparisonArray[i] >= other.comparisonArray[i]):
                retVal = False
                break
        return retVal

    def __le__(self, other):
        self._checkComparibility(other)
        retVal = True
        for i in range(6):
            if not (self.comparisonArray[i] <= other.comparisonArray[i]):
                retVal = False
                break
        return retVal

    def __gt__(self, other):
        self._checkComparibility(other)
        retVal = True
        for i in range(len(self.comparisonArray)):
            if not (self.comparisonArray[i] >= other.comparisonArray[i]):
                retVal = False
                break
        return (retVal and self != other)

    def __lt__(self, other):
        self._checkComparibility(other)
        retVal = True
        for i in range(len(self.comparisonArray)):
            if not (self.comparisonArray[i] <= other.comparisonArray[i]):
                retVal = False
                break
        return (retVal and self != other)

    def _checkComparibility(self, other):
        if len(self) != len(other):
            raise IncompatiblePointOperationError("Attempting to compare incopatible points."
                                                  " The lengths of the points must equal.")
        if not (self.determinant and other.determinant):
            raise IncompatiblePointOperationError("Attempting to compare incopatible points."
                                                  " At least one point in indeterminant.")
        return

    def __repr__(self):
        elements = ', '.join(str(element) for element in self.pointList)
        return f"Point({elements})"

    @classmethod
    def fromString(cls, string):
        pattern = r"^\((\s*\d+(bar)?\s*\|)+\s*\d+(bar)?\s*\)$"
        match = re.match(pattern, string)

        if match:
            pointString = string.replace("(", "").replace(")", "")
            pointListStr = pointString.split("|")
            pointList = []
            for val in pointListStr:
                pointList.append(SignedInt.fromString(val.strip()))
            return cls(*pointList)
        else:
            raise ValueError("Invalid input")

    def toTeX(self):
        TeX = []
        TeX.append(" ( ")
        for i in range(len(self.pointList)):
            TeX.append(str(self.pointList[i]))

            if (i < len(self.pointList) - 1):
                TeX.append(r" \vert ")
            else:
                TeX.append(" ) ")

        return "".join(TeX)

    # This property is invoked every time a comparison is made between two points.
    # This property outputs a list of length 6. The first element is the first element, of the point.
    # The next two elements are the min and max of the first two elements of the point respectively
    # And the final three elements are the ordering of all the elements of the points.
    @property
    def comparisonArray(self):
        output = []
        for i in range(len(self)):
            output.extend(sorted(self.pointList[0:i+1]))
        return output

    @property
    def indeterminateValsCount(self):
        count = 0
        for val in self.pointList:
            if isinstance(val, str):
                count += 1
        return count

    def makeDeterminant(self):
        if self.indeterminateValsCount == 0:
            return
        indeterminateLocations = []
        for i in range(len(self)):
            if isinstance(self.pointList[i], str):
                indeterminateLocations.append(i)
        blacklist = [] # Blacklist needs to be for each reflected Point
        for i in range(len(self)):
            if i in indeterminateLocations:
                continue
            blacklist.append(self.pointList[i])
            blacklist.append(-self.pointList[i])

        possibleVals = []

        for i in range(2, 2 + len(self) + 1):
            possibleVals.append(SignedInt(i, True))

        if self.indeterminateValsCount == 1:
            i = 0
            for val in possibleVals:
                if val in blacklist:
                    continue
                else:
                    self.pointList[indeterminateLocations[i]] = val
                    break

        elif self.indeterminateValsCount == 2: # This will not work
            i = 0
            for val in possibleVals:
                if val in blacklist:
                    continue
                else:
                    self.pointList[indeterminateLocations[i]] = val
                    i += 1
                    if i == 2:
                        break

        self.determinant = True
        return




class Reflection:
    # i and j use 1 based indexing! ie Reflection(1,2) swaps the 0-th and 1st item
    # Reflection(i, 0) represents a t_i - t_k reflection where k>=4

    def __init__(self, i, j):
        self.i = i
        self.j = j



    def toTeX(self):
        expression = f"t_{self.i} - t_{self.j if self.j != 0 else 'k'}"
        return f"\\xrightarrow{{{expression}}}"


    # This method performs the reflection. If j is 0, the reflection is treated as a t_i - t_k reflection where k >= 4
    # The point then becomes indeterminate.
    def execute(self, point):
        x = self.i - 1
        y = self.j - 1

        if self.j == 0:
            # 1 is added because the count is about to increase by 1
            xVal = "x" if point.indeterminateValsCount + 1 == 1 else "y"
            point.pointList[x] = xVal
            point.determinant = False
        else:
            temp = point.pointList[x]
            point.pointList[x] = point.pointList[y]
            point.pointList[y] = temp

        return


class ReflectionCalculator:

    def __init__(self, n):
        self.degree = n
        self.reflectionList = self.__getReflectionCombinations()
        vals = []
        for i in range(1, n+1):
            vals.append(SignedInt(i, False))
        self.point = Point(*vals)
        self.log = CalculationResult()

    def __getReflectionCombinations(self):
        def __getComps(n):
            comps = []
            for num in range(2 ** (n - 1)):  # Generate all the n-1 digit numbers
                current = []
                a = 1
                for i in range(n - 2, -1, -1):  # From left to right loop through each digit
                    reset = (num >> i) & 1  # get the binary representation of the current digit
                    if reset:
                        current.append(a)
                        a = 1
                    else:
                        a += 1
                current.append(a)
                comps.append(tuple(current))

            comps.sort(key=len)
            return comps

        comps = __getComps(self.degree)

        reflectionSequences = []
        for comp in comps:
            reflectionSequence = []
            i = 1
            j = 1
            for val in comp:
                i = j
                j = i + val if (i + val) <= self.degree else 0
                reflectionSequence.append(Reflection(i, j))

            reflectionSequences.extend(list(itertools.permutations(reflectionSequence)))
        return reflectionSequences

    def applyReflections(self, verbose=0):
        self.log.append(f"Applying Reflections to ${self.point.toTeX()}$ :")
        self.log.append("")
        points = []
        for reflectionSequence in self.reflectionList:
            pointCopy = copy.deepcopy(self.point)
            TeX = [r"\[", pointCopy.toTeX()]
            for reflection in reflectionSequence:
                TeX.append(reflection.toTeX())
                reflection.execute(pointCopy)
                TeX.append(pointCopy.toTeX())
            points.append(pointCopy)
            TeX.append(r"\]")
            self.log.append("".join(TeX))
        self.log.append("")
        self.log.setPoints(points)

        return

    def makePointsDeterminant(self, verbose=0):
        self.log.append("Solving for x, y, and z:")
        self.log.append("")
        points = self.log.getPoints()
        newPoints = []
        for point in points:
            TeX = [r"\[", point.toTeX(), r"\rightarrow "]
            point.makeDeterminant()
            TeX.append(point.toTeX())
            TeX.append(r"\]")
            if point not in newPoints:
                newPoints.append(point)
            self.log.append("".join(TeX))
        self.log.append("")
        self.log.setPoints(newPoints)
        return


    def findMaximalPoints(self, verbose=0):
        self.log.append("Found Maximal Points:")
        self.log.append("")
        points = self.log.getPoints()
        newPoints = []
        for maximalPointCandidate in points:
            foundGreaterPoint = False

            for otherPoint in points:
                if maximalPointCandidate < otherPoint:
                    foundGreaterPoint = True
                    break

            if not foundGreaterPoint:
                newPoints.append(maximalPointCandidate)
                self.log.append(fr"\[ {maximalPointCandidate.toTeX()} \]")

        self.log.setPoints(newPoints)
        return

    def calculateAll(self, verbose=0):
        self.applyReflections(verbose=verbose)
        self.makePointsDeterminant(verbose=verbose)
        self.findMaximalPoints(verbose=verbose)
        return self.log.getLog()



class CalculationResult:
    def __init__(self):
        self.points = []
        self.log = []

    def getPoints(self):
        return self.points

    def getLog(self):
        return "".join(self.log)

    def append(self, message):
        self.log.append(message + "\n")
        return
    def setPoints(self, points):
        self.points = points
        return


