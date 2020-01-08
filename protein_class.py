import random

class Protein:
    def __init__(self, sequence):
        self.sequence = sequence

    def generate_random_path(self, return_stability=True):
        path = {}
        h_positions = []
        stability = 0
        for index, amino in enumerate(self.sequence):
            if index in (0, 1):
                # set starting conditions -- exclude rotations of solution
                next_coordinate = (0, index)
                path[index] = [amino, next_coordinate]

                if amino == "H":
                    h_positions.append(next_coordinate)

            else:
                # iterate through sequence
                next_coordinate = self.random_step(path, index)
                if not next_coordinate:
                    return None
                path[index] = [amino, next_coordinate]

                if amino == "H":
                    stability += self.get_added_stability(path, next_coordinate, h_positions)
                    h_positions.append(next_coordinate)

        if not return_stability:
            return path
        return (path, stability)


    def random_step(self, path, index):
        '''returns coordinates for randomly chosen step if possible'''
        prev_coordinate = path[index-1][1]
        options = self.get_surrounding_coordinates(prev_coordinate)

        for i in path.values():
            if i[1] in options:
            # remove occupied locations from options
                options.remove(i[1])
        if options == []:
            return None
        return random.choice(options)


    def get_added_stability(self, path, coordinate, h_positions):
        '''calculate added stability for given step by evaluating surrounding positions'''

        # get positions to evaluate
        positions = self.get_surrounding_coordinates(coordinate)

        # remove previous coordinate in path from positions
        positions.remove(path[len(path) - 2][1])

        for position in positions:
            if position in h_positions:
                return -1
        return 0


    def get_surrounding_coordinates(self, coordinate):
        return [
            (coordinate[0] + 1, coordinate[1]),
            (coordinate[0] - 1, coordinate[1]),
            (coordinate[0], coordinate[1] + 1),
            (coordinate[0], coordinate[1] - 1)
            ]

    def determine_directions(self, path):
        '''determines the directions a path has taken, where 1 is a step to the right, -1 to the left,
        2 goes up and -2 is down. 0 means that the path has ended, this method needs only the path as input'''
        directions = []
        for number in range(len(self.sequence)):
            if number == len(self.sequence) - 1:
                directions.append(0)
            else:
                if path[number][1][0] == path[number + 1][1][0]:
                    if path[number][1][1] > path[number + 1][1][1]:
                        directions.append(-2)
                    else:
                        directions.append(2)
                else:
                    if path[number][1][0] > path[number + 1][1][0]:
                        directions.append(-1)
                    else:
                        directions.append(1)
        return directions

# testtest
