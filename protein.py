import random

algorithm = "HHPHHHPH"


for i in range(1):
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

    for number in range(len(algorithm)):
        current_coordinate = dict[number]
        exact_coordinate = current_coordinate[1]

        if number == 0:
            coordinates_to_delete = dict[number + 1]
        elif number == len(algorithm) - 1:
            coordinates_to_delete = dict[number - 1]
        else:
            coordinates_to_delete = (dict[number - 1], dict[number + 1])

        options = [(exact_coordinate[0] + 1, exact_coordinate[1]), (exact_coordinate[0] - 1, exact_coordinate[1]),
        (exact_coordinate[0], exact_coordinate[1] + 1), (exact_coordinate[0], exact_coordinate[1] - 1)]

        print(current_coordinate)
        print(coordinates_to_delete)
        print(options)

    print(dict)
