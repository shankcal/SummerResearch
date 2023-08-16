# SignedInt takes two parameters as input. First it takes an int which represents the value and a boolean which
# represents weather or not the value is barred. Values should always be positive and nonzero.
# In this system 1 < 2 < ... < n < nbar < n-1bar < ... < 2bar < 1bar
import copy
import itertools
import re


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
    def __init__(self, a, b, c):
        self.reflectedPointsCount = 0
        self.determinant = True
        self.pointList = [a, b, c]

    def __eq__(self, other):
        if not (self.determinant and other.determinant):
            raise NotImplementedError("Error. At least one point is not determinant.")
        return self.pointList == other.pointList

    def __ne__(self, other):
        if not (self.determinant and other.determinant):
            raise NotImplementedError("Error. At least one point is not determinant.")
        return self.pointList != other.pointList

    def __ge__(self, other):
        if not (self.determinant and other.determinant):
            raise NotImplementedError("Error. At least one point is not determinant.")
        retVal = True
        for i in range(6):
            if not (self.comparisonArray[i] >= other.comparisonArray[i]):
                retVal = False
                break
        return retVal

    def __le__(self, other):
        if not (self.determinant and other.determinant):
            raise NotImplementedError("Error. At least one point is not determinant.")
        retVal = True
        for i in range(6):
            if not (self.comparisonArray[i] <= other.comparisonArray[i]):
                retVal = False
                break
        return retVal

    def __gt__(self, other):
        if not (self.determinant and other.determinant):
            raise NotImplementedError("Error. At least one point is not determinant.")
        retVal = True
        for i in range(6):
            if not (self.comparisonArray[i] >= other.comparisonArray[i]):
                retVal = False
                break
        return (retVal and self != other)

    def __lt__(self, other):
        if not (self.determinant and other.determinant):
            raise NotImplementedError("Error. At least one point is not determinant.")
        retVal = True
        for i in range(6):
            if not (self.comparisonArray[i] <= other.comparisonArray[i]):
                retVal = False
                break
        return (retVal and self != other)

    def __repr__(self):
        return f"Point({self.pointList[0]}, {self.pointList[1]}, {self.pointList[2]})"

    @classmethod
    def fromString(cls, string):
        pattern = r'^\(\s*\w(bar)?\s*\|\s*\w(bar)?\s*\|\s*\w(bar)?\s*\)$'
        match = re.match(pattern, string)

        if match:
            pointString = string.replace("(", "").replace(")", "")
            pointListStr = pointString.split("|")
            pointList = []
            for val in pointListStr:
                pointList.append(SignedInt.fromString(val.strip()))
            return cls(pointList[0], pointList[1], pointList[2])
        else:
            raise ValueError("Invalid input")

    def toTeX(self):
        TeX = []
        TeX.append(" ( ")
        for i in range(len(self.pointList)):
            TeX.append(str(self.pointList[i]))

            if (i < 2):
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
        output.append(self.pointList[0])
        output.extend(sorted(self.pointList[0:2]))
        output.extend(sorted(self.pointList[0:3]))

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
        for i in range(3):
            if isinstance(self.pointList[i], str):
                indeterminateLocations.append(i)
        blacklist = []
        for i in range(3):
            if i in indeterminateLocations:
                continue
            blacklist.append(self.pointList[i])
            blacklist.append(-self.pointList[i])

        possibleVals = [SignedInt(2, True), SignedInt(3, True), SignedInt(4, True)]

        if self.indeterminateValsCount == 1:
            i = 0
            for val in possibleVals:
                if val in blacklist:
                    continue
                else:
                    self.pointList[indeterminateLocations[i]] = val
                    break

        elif self.indeterminateValsCount == 2:
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

    @classmethod
    def fromTuple(cls, reflectionTuple):

        match reflectionTuple:
            case (1, 0, 0):
                i, j = 1, 2
            case (1, 1, 0):
                i, j = 1, 3
            case (0, 0, 1):
                i, j = 3, 0
            case (0, 1, 0):
                i, j = 2, 3
            case (1, 1, 1):
                i, j = 1, 0
            case (0, 1, 1):
                i, j = 2, 0
            case (0, 0, 1):
                i, j = 3, 0
            case _:
                print(reflectionTuple)
                raise NotImplementedError("Invalid Tuple")

        return cls(i, j)

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
    allowedDegrees = ((1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 0), (0, 1, 1), (1, 1, 1), (1, 1, 2))

    def __init__(self, degree, point):
        if degree in ReflectionCalculator.allowedDegrees:
            self.degree = degree
            self.reflectionList = self.__getReflectionCombinations()
            self.point = point
            self.log = CalculationResult()
        else:
            raise NotImplementedError("This Reflection is not supported")

    def __getReflectionCombinations(self):
        def permsOf(*args):
            return tuple(itertools.permutations(args))

        def r(a, b, c):
            return Reflection.fromTuple((a, b, c))

        reflectionsequences = []
        match self.degree:
            case (1, 0, 0):
                reflectionsequences.append((r(1, 0, 0),))
            case (0, 1, 0):
                reflectionsequences.append((r(0, 1, 0),))
            case (0, 0, 1):
                reflectionsequences.append((r(0, 0, 1),))
            case (1, 1, 0):
                reflectionsequences.append((r(1, 1, 0),))
                reflectionsequences.extend(permsOf(r(1, 0, 0), r(0, 1, 0)))
            case (0, 1, 1):
                reflectionsequences.append((r(0, 1, 1),))
                reflectionsequences.extend(permsOf(r(0, 1, 0), r(0, 0, 1)))
            case (1, 1, 1):
                reflectionsequences.append((r(1, 1, 1),))
                reflectionsequences.extend(permsOf(r(1, 1, 0), r(0, 0, 1)))
                reflectionsequences.extend(permsOf(r(1, 0, 0), r(0, 1, 1)))
                reflectionsequences.extend(permsOf(r(1, 0, 0), r(0, 1, 0), r(0, 0, 1)))
            case (1, 1, 2):
                reflectionsequences.extend(permsOf(r(1, 1, 1), r(0, 0, 1)))
                reflectionsequences.extend(permsOf(r(1, 1, 0), r(0, 0, 1), r(0, 0, 1)))
                reflectionsequences.extend(permsOf(r(0, 1, 1), r(1, 0, 0), r(0, 0, 1)))
                reflectionsequences.extend(permsOf(r(1, 0, 0), r(0, 1, 0), r(0, 0, 1), r(0, 0, 1)))

        return reflectionsequences

    def applyReflections(self, verbose=0):
        self.log.append(f"Applying Reflections to ${self.point.toTeX()}$ :")
        self.log.append("\n")
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

        self.log.setPoints(points)
        return

    def makePointsDeterminant(self, verbose=0):
        self.log.append("Solving for x,y, and z:")
        self.log.append("\n")
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
        self.log.setPoints(newPoints)
        return


    def findMaximalPoints(self, verbose=0):
        self.log.append("Found Maximal Points:")
        self.log.append("\n")
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
        return "\n".join(self.log)

    def append(self, message):
        self.log.append(message)
        return
    def setPoints(self, points):
        self.points = points
        return
