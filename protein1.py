import random

class Protein
    def __init__(self, sequence, dim=2):
        self.sequence   = sequence
        self.dim        = dim

    def generate_config():
        config = {}

        for number, amino in enumerate(self.sequence):

            if number in (0, 1):
                # set starting conditions
                config[number] = [amino, ()]
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
        
        return config

#testtest
