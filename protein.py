import random

algorithm = "HHPHHHPH"

# determine the amount of experiments to do
for i in range(20):
    dict = {}

    for number, amino in enumerate(algorithm):
        if number in (0,1):
            # set starting conditions
            dict[number] = [amino, (number, 0)]
        else:
            # randomly determine which path to follow
            prev_coordinate = dict[number-1][1]

            options = [(prev_coordinate[0] + 1, prev_coordinate[1]), (prev_coordinate[0] - 1, prev_coordinate[1]),
            (prev_coordinate[0], prev_coordinate[1] + 1), (prev_coordinate[0], prev_coordinate[1] - 1)]

            # delete all options where a point is already taken
            for i in dict.values():
                if i[1] in options:
                     options.remove(i[1])

            new_coordinate = random.choice(options)

            dict[number] = [amino, new_coordinate]

    stability = 0

    # consider all coordinates in the random experiments
    for number in range(len(algorithm)):
        current_coordinate = dict[number]
        exact_coordinate = current_coordinate[1]

        if current_coordinate[0] == 'H':
            options = [(exact_coordinate[0] + 1, exact_coordinate[1]), (exact_coordinate[0] - 1, exact_coordinate[1]),
            (exact_coordinate[0], exact_coordinate[1] + 1), (exact_coordinate[0], exact_coordinate[1] - 1)]

            # erase connected points from options
            if number == 0:
                coordinate_to_delete = [dict[number + 1][1]]
            elif number == len(algorithm) - 1:
                coordinate_to_delete = [dict[number - 1][1]]
            else:
                coordinate_to_delete = [dict[number - 1][1], dict[number + 1][1]]

            for i in coordinate_to_delete:
                options.remove(i)

            # check for connections to the current point
            for i in dict.values():
                if i[0] == 'H':
                    if i[1] in options:
                        stability -= 0.5

    print(dict)
    print(f"The stability is {round(stability)}")
