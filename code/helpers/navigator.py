'''
    navigator.py

    supporting functions for navigating proteins and surroundings
'''


def get_surrounding_coordinates(coordinate):
    ''' returns positions surrounding inserted coordinate '''
    return [
        (coordinate[0] + 1, coordinate[1]),
        (coordinate[0] - 1, coordinate[1]),
        (coordinate[0], coordinate[1] + 1),
        (coordinate[0], coordinate[1] - 1)
    ]


def get_step_options(protein):
    positions = [point[1] for point in protein.path]
    coordinate = positions[-1]
    if protein.symmetric:
        # reduced options if path has not strayed from y-axis to eliminate mirrorred configurations
        return [
            (coordinate[0] + 1  , coordinate[1]),
            (coordinate[0]      , coordinate[1] + 1),
        ]

    else:
        options = get_surrounding_coordinates(coordinate)
        for position in positions:
            if position in options: options.remove(position)
        return options


def get_added_stability(protein, amino, step, care=0):
    ''' returns the added stability for a step from a partial chain of aminoacids '''
    if amino == "P":
        return 0, 0

    positions = get_surrounding_coordinates(step)
    # remove last position in path to prevent counting bonds along the protein chain
    positions.remove(protein.path[-1][1])

    added_stability = 0
    weight = 0
    for amino_neighbor, amino_positions in protein.amino_positions.items():
        for position in positions:
            if position in amino_positions:
                binding_score, blocking_penalty = protein.bond_stabilities[amino][amino_neighbor]
                added_stability += binding_score
                weight += (binding_score + blocking_penalty * care)
    return added_stability, weight


def get_path_directions(path):
    '''
    converts path into format as specified by case assignment (TODO: add file writer)
    directions between subsequent aminoacids are signified by numbers, where:
       -1, 1 represent unit steps along the x-axis
       -2, 2 represent unit steps along the y-axis
       0 terminates the sequence
    '''
    # obtain positions from path
    positions = [point[1] for point in path]

    directions = []
    for i in range(len(positions)-1):
        # append appropriate number for each step's direction
        directions.append(
            (-1) * (positions[i + 1][0] - positions[i][0]) +
            (-2) * (positions[i + 1][1] - positions[i][1])
        )
    # append 0 to terminate the sequence
    directions.append(0)
    return directions
