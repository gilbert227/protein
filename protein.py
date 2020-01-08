import random
import time


algorithm = "HHPHHHPH"
dim = 2
min_stability = 0

start = time.time()

# determine the amount of experiments to do
for i in range(1):
    dict = {}
    crash = 0
    path = []

    for number, amino in enumerate(algorithm):
        if number in (0,1):
            # set starting conditions
            dict[number] = [amino, (number, 0)]
            path.append((amino, 1))
        else:
            # randomly determine which path to follow
            prev_coordinate = dict[number-1][1]

            options = [(prev_coordinate[0] + 1, prev_coordinate[1]), (prev_coordinate[0] - 1, prev_coordinate[1]),
            (prev_coordinate[0], prev_coordinate[1] + 1), (prev_coordinate[0], prev_coordinate[1] - 1)]

            # delete all options where a point is already taken
            for i in dict.values():
                if i[1] in options:
                     options.remove(i[1])

            if options == []:
                crash = 1
                break

            new_coordinate = random.choice(options)

            for i in range(dim):
                if new_coordinate[i] - prev_coordinate[i] == 1:
                    movement = i + 1
                elif new_coordinate[i] - prev_coordinate[i] == -1:
                    movement = -i - 1

            path.append((amino, movement))

            dict[number] = [amino, new_coordinate]

    stability = 0

    # consider all coordinates in the random experiments
    if crash == 0:
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

    #     # print(dict)
    #     # print(f"The stability is {round(stability)}")
    # else:
    #     print("The sequence crashed")

    if stability <= min_stability:
        min_stability = stability
        best_path = [path, stability]

print(best_path)

end = time.time()
print(end - start)
