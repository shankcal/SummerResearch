
class SignedInt:
    def __init__(self, val, bar):
        self.val = val
        self.bar = bar

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

    def __str__(self):
        if self.bar:
            return f"\\bar{{{str(self.val)}}}"
        else:
            return str(self.val)

    def __repr__(self):
        return f"SignedInt({self.val}, {self.bar})"


class Point:
    def __init__(self, a, b, c, reflectedPoints=None):
        if reflectedPoints is None:
            self.reflectedPoints = []
        else:
            self.reflectedPoints = reflectedPoints
        self.pointList = [a, b, c]


    def __eq__(self, other):
        return self.pointList == other.pointList

    def __ne__(self, other):
        return self.pointList != other.pointList

    def __ge__(self, other):
        retVal = True
        for i in range(6):
            if not (self.comparisonArray[i] >= other.comparisonArray[i]):
                retVal = False
                break
        return retVal

    def __le__(self, other):
        retVal = True
        for i in range(6):
            if not (self.comparisonArray[i] <= other.comparisonArray[i]):
                retVal = False
                break
        return retVal

    def __gt__(self, other):
        retVal = True
        for i in range(6):
            if not (self.comparisonArray[i] >= other.comparisonArray[i]):
                retVal = False
                break
        return (retVal and self != other)

    def __lt__(self, other):
        retVal = True
        for i in range(6):
            if not (self.comparisonArray[i] <= other.comparisonArray[i]):
                retVal = False
                break
        return (retVal and self != other)

    def __repr__(self):
        return f"Point({self.pointList[0]}, {self.pointList[1]}, {self.pointList[2]}, reflectedPoints={self.reflectedPoints})"

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

    @property
    def comparisonArray(self):
        output = []
        output.append(self.pointList[0])
        output.extend(sorted(self.pointList[0:2]))
        output.extend(sorted(self.pointList[0:3]))

        return output

    # Convert the following to python if nessesary

    # public string getExclusionTeX()
    # {
    #     StringBuilder TeX = new StringBuilder();
    #     TeX.Append(@"x \in A^c ");
    #     var ReflectedPointsNo1s = reflectedPoints.Where(x => x != new SignedInt(1, true)).ToList();
    #     if (ReflectedPointsNo1s.Count > 0)
    #     {
    #         TeX.Append(@"\cup \{");
    #
    #         foreach (SignedInt num in ReflectedPointsNo1s)
    #         {
    #             TeX.Append((-num).ToString());
    #             if (num != reflectedPoints.Last())
    #             {
    #                 TeX.Append(",");
    #             }
    #         }
    #         TeX.Append(@"\}");
    #     }
    #     TeX.Append(".");
    #
    #     return TeX.ToString();
    # }


class Reflection:
    # i and j use 1 based indexing! ie Reflection(1,2) swaps the 0-th and 1st item
    # Reflection(i, 0) represents a t_i - t_k reflection where k>=4

    def __init__(self, i, j):
        self.i = i
        self.j = j

    def toTeX(self):
        expression = f"t_{self.i} - t_{self.j if self.j != 0 else 'k'}"
        return f"\\xrightarrow{{{expression}}}"

    @staticmethod
    def __findX(point, xLocation):
        blacklist = []
        for i in range(3):
            if i == xLocation:
                continue
            blacklist.append(point.pointList[i])
            blacklist.append(-point.pointList[i])

        possibleVals = [SignedInt(2, True), SignedInt(3, True), SignedInt(4, True)]

        for val in possibleVals:
            if val in blacklist:
                continue
            else:
                return val

        print("Error with findX method!!!! using 4bar")
        return SignedInt(4, True)

    def execute(self, point):
        x = self.i - 1
        y = self.j - 1

        if self.j == 0:
            xVal = Reflection.__findX(point, x)
            point.reflectedPoints.append(point.pointList[x])
            point.pointList[x] = xVal
        else:
            temp = point.pointList[x]
            point.pointList[x] = point.pointList[y]
            point.pointList[y] = temp

        return