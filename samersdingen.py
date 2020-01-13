import random
import operator
import time

class Protein:
    def _init_(self, sequence):
        self.sequence = sequence

    def generate_path(self, strategy, sequence, first_step, return_stability=True):
        '''returns a path, the user can choose which strategy to use
        strategies for now are: random, greedy'''
        path = {}
        h_positions = []
        c_positions = []
        stability = 0
        symmetric = True

        enum_sequence = list(enumerate(sequence))

        # set starting conditions -- exclude rotations of solution
        if first_step == True:
            for i in (0,1):
                path[i] = [enum_sequence[i][1], [0,i]]
                if enum_sequence[i][1] == 'H':
                    h_positions.append([0,i])
                if enum_sequence[i][1] == 'C':
                    c_positions.append([0,i])

            enum_sequence.pop(0)
            enum_sequence.pop(0)
        else:
            path[0] = [enum_sequence[0][1], [0,0]]
            if enum_sequence[0][1] == 'H':
                h_positions.append([0,0])
            if enum_sequence[0][1] == 'C':
                c_positions.append([0,0])

            enum_sequence.pop(0)

        for index, amino in enum_sequence:
            if symmetric == True and first_step == True:
                 # choose which strategy to take
                if strategy == 'random':
                    next_coordinate = self.random_step(path, index, True)
                elif strategy == 'greedy':
                    if amino == 'H' or amino == 'C':
                        next_coordinate = self.greedy_step(path, index, amino, h_positions, c_positions, True)
                    else:
                        next_coordinate = self.random_step(path, index, True)

                # duplicate
                if not next_coordinate:
                    return None
                path[index] = [amino, next_coordinate]

                if amino == 'H':
                    stability += self.get_added_stability(path, next_coordinate, amino, h_positions, c_positions, symmetric)
                    h_positions.append(next_coordinate)

                if amino == 'C':
                    stability += self.get_added_stability(path, next_coordinate, amino, h_positions, c_positions, symmetric)
                    c_positions.append(next_coordinate)

                # check wether the new coordinate deviated from x=0
                if next_coordinate[0] != 0:
                    symmetric = False

            else:
                # iterate through sequence
                 # choose which strategy to take
                if strategy == 'random':
                    next_coordinate = self.random_step(path, index, False)
                elif strategy == 'greedy':
                    if amino == 'H' or amino == 'C':
                        next_coordinate = self.greedy_step(path, index, amino, h_positions, c_positions, False)
                    else:
                        next_coordinate = self.random_step(path, index, False)
                if not next_coordinate:
                    return None
                path[index] = [amino, next_coordinate]

                if amino == 'H':
                    stability += self.get_added_stability(path, next_coordinate, amino, h_positions, c_positions, symmetric)
                    h_positions.append(next_coordinate)

                if amino == 'C':
                    stability += self.get_added_stability(path, next_coordinate, amino, h_positions, c_positions, symmetric)
                    c_positions.append(next_coordinate)

        if not return_stability:
            return path
        return [path, stability]

    def random_step(self, path, index, symmetric):
        '''returns coordinates for randomly chosen step if possible'''
        prev_coordinate = path[index-1][1]
        options = self.get_surrounding_coordinates(prev_coordinate, symmetric)

        for i in path.values():
            if i[1] in options:
            # remove occupied locations from options
                options.remove(i[1])
        if options == []:
            return None
        return random.choice(options)

    def greedy_step(self, path, index, amino, h_positions, c_positions, symmetric):
        '''returns coordinates for greedy algorithm step if possible'''
        prev_coordinate = path[index-1][1]
        options = self.get_surrounding_coordinates(prev_coordinate, symmetric)

        for i in path.values():
            if i[1] in options:
            # remove occupied locations from options
                options.remove(i[1])
        if options == []:
            return None

        if len(options) == 1:
            return options[0]

        values = []
        for coordinate in options:
            points = self.get_added_stability(path, coordinate, amino, h_positions, c_positions, symmetric, False)
            values.append([coordinate, points])

        greediest = min(map(operator.itemgetter(1), values))

        new_coordinates = []
        for i in values:
            if i[1] == greediest:
                new_coordinates.append(i[0])

        return random.choice(new_coordinates)

    def get_added_stability(self, path, coordinate, amino, h_positions, c_positions, symmetric, random_step=True):
        '''calculate added stability for given step by evaluating surrounding positions'''

        # get positions to evaluate
        positions = self.get_surrounding_coordinates(coordinate, symmetric)

        # remove previous coordinate in path from positions
        if symmetric == False and random_step:
            positions.remove(path[len(path) - 2][1])

        added_stability = 0
        for position in positions:
            if amino == 'H':
                if position in h_positions:
                    added_stability -= 1
                if position in c_positions:
                    added_stability -= 1
            if amino == 'C':
                if position in c_positions:
                    added_stability -= 5
                elif position in h_positions:
                    added_stability -= 1

        return added_stability


    def get_surrounding_coordinates(self, coordinate, symmetric):

        # options if symmetric, to avoid extra dubplicates
        if symmetric:
            return [
                [coordinate[0] + 1, coordinate[1]],
                [coordinate[0], coordinate[1] + 1],
            ]

        else:
            return [
                [coordinate[0] + 1, coordinate[1]],
                [coordinate[0] - 1, coordinate[1]],
                [coordinate[0], coordinate[1] + 1],
                [coordinate[0], coordinate[1] - 1]
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

    def get_best_path(self, iterations, strategy, sequence):
        start_time = time.time()

        best_path = [0,0]

        for i in range(iterations):
            path = self.generate_path(strategy, sequence, True)

            if path and path[1] <= best_path[1]:
                best_path = path

        return best_path, (time.time() - start_time)


    def small_grid(self):

        # get good solution
        starting_sequence = self.get_best_path(10000, 'greedy', self.sequence)[0]

        print(starting_sequence)

        # get all occupied points
        occupied_points = []

        for i in range(len(starting_sequence[0])):
            occupied_points.append(starting_sequence[0][i][1])


        # devide sequence in parts of 6, rounding up
        chunked_sequence = [['H', 'P', 'H', 'P', 'P', 'H'], ['H', 'P', 'H', 'P', 'P', 'H'], ['P', 'H', 'H', 'P', 'P', 'H'], ['P', 'H']]

        # make small grid around starting and end points small sequence
        amount_chunks = - (- len(starting_sequence) // 6)

        # start and end points
        start_points = []
        end_points = []
        count = 0
        for chunk in chunked_sequence:
            start_points.append(starting_sequence[0][count * 6][1])
            end_points.append(starting_sequence[0][count * 6 + len(chunk) - 1][1])

            count += 1

        count = 0
        location_in_sequence = 0
        for chunk in chunked_sequence:

            # TO DO:    test the stability of the chunk in the sequence


            concentrated_occupied_points = []
            length_chunk = len(chunk)
            while True:
                for i in range(1):
                    # prase false to make sure no rotation is excluded
                    transformed_chunk = self.generate_path('random', chunk, False)

                    # translate chunk to location in sequence
                    for ii in range(length_chunk):
                        transformed_chunk[0][ii][1] = [x + y for x, y in zip(start_points[count], transformed_chunk[0][ii][1])]

                    # check wether the random transformation still connects to the end point
                    if transformed_chunk[0][length_chunk - 1][1] == end_points[count]:

                        # check if the new transformations crosses the old sequence
                        points_chunk = []
                        for i in range(length_chunk):
                            points_chunk.append(transformed_chunk[0][i][1])

                        # filter the point that are occupied, but not by the chunk
                        concentrated_occupied_points = occupied_points[:(location_in_sequence)]
                        concentrated_occupied_points.append(occupied_points[(location_in_sequence + length_chunk):])

                        # check if the points cross
                        for point in points_chunk:
                            if point in concentrated_occupied_points:
                                return False
