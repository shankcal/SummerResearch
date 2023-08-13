import itertools
import numpy as np
import random

numberPool = [1, 2, 3, 4, 5, 6]
# numberPool = [1, 2, 3]

# Finds all the permuations of the points in the numberpool without repition
points = list(itertools.permutations(numberPool, 3))
pointOrderings = []
f = open("Output.txt", "w")
for point in points:
    burhatOrdering = []
    burhatOrdering.append(point[0])
    burhatOrdering.extend(sorted(point[0:2]))
    burhatOrdering.extend(sorted(point))
    pointOrderings.append(np.array(burhatOrdering))






greater = []
less = []
equal = []
notComparible = []
# failedCount = 0
# random.shuffle(pointOrderings)

for i in range(len(pointOrderings)):
    for j in range(i+1, len(pointOrderings)):
        if np.all(pointOrderings[i] == pointOrderings[j]):
            equal.append((points[i], points[j]))
        elif (np.all(pointOrderings[i] <= pointOrderings[j])):
            less.append((points[i], points[j]))
        elif (np.all(pointOrderings[i] >= pointOrderings[j])):
            greater.append((points[i], points[j]))
        else:
            # if not(pointOrderings[i][0] <= pointOrderings[j][0] or (pointOrderings[i][0] <= pointOrderings[i][1] and pointOrderings[j][0] <= pointOrderings[j][1] and pointOrderings[i][2] >= pointOrderings[j][2] )):
            #     failedCount += 1
            #     print("Failed")
            #     print(str(points[i]) + " <> " + str(points[j]))
            notComparible.append((points[i], points[j]))

print()

print(f"Comparabile = {len(greater) + len(less)}")
print(f"Not Comparible = {len(notComparible)}")
# print(failedCount)
for item in notComparible:
    numbersUsed = []

    # All points
    # f.write(f"{item[0]} <> {item[1]} \n")

    # Points with no common values
    # for val in numberPool:
    #     if val in item[0] or val in item[1]:
    #         numbersUsed.append(val)
    #
    # if numbersUsed == numberPool:
    #     f.write(f"{item[0]} <> {item[1]} \n")

    # points begining with 1
    if item[0][0] == 1 and item[1][0] == 1:
        f.write(f"{item[0]} <> {item[1]} \n")






#

f.close()