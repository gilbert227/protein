import random
from copy import copy

algorithm = "HHPHHHPH"

dict = {}

for number, amino in enumerate(algorithm):

    if number in (0,1):
        # set starting conditions
        dict[number] = [amino, (number, 0)]
    else:
        prev_coordinate = dict[number-1][1]

        options = [(prev_coordinate[0] + 1, prev_coordinate[1]), (prev_coordinate[0] - 1, prev_coordinate[1]),
        (prev_coordinate[0], prev_coordinate[1] + 1), (prev_coordinate[0], prev_coordinate[1] - 1)]

        for i in dict.values():
            if i[1] in options:
                 options.remove(i[1])

        new_coordinate = random.choice(options)

        dict[number] = [amino, new_coordinate]

print(dict)
