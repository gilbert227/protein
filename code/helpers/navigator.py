'''
    navigator.py

    supporting functions for navigating proteins and surroundings
'''


def get_surrounding_coordinates(protein, coordinate):
    ''' returns positions surrounding inserted coordinate depending on the third dimension'''
    if not protein.dim3:
        return [
            (coordinate[0] + 1, coordinate[1]),
            (coordinate[0] - 1, coordinate[1]),
            (coordinate[0], coordinate[1] + 1),
            (coordinate[0], coordinate[1] - 1)
            ]
    else:
        return [
        (coordinate[0] + 1, coordinate[1], coordinate[2]),
        (coordinate[0] - 1, coordinate[1], coordinate[2]),
        (coordinate[0], coordinate[1] + 1, coordinate[2]),
        (coordinate[0], coordinate[1] - 1, coordinate[2]),
        (coordinate[0], coordinate[1], coordinate[2] + 1),
        (coordinate[0], coordinate[1], coordinate[2] - 1)
        ]


def get_step_options(protein):
    positions = [point[1] for point in protein.path]
    coordinate = positions[-1]
    if protein.symmetric:
        # reduced options if path has not strayed from y-axis to eliminate mirrorred configurations
        if not protein.dim3:
            return [
                (coordinate[0] + 1  , coordinate[1]),
                (coordinate[0]      , coordinate[1] + 1)
                ]
        else:
            return [
                (coordinate[0] + 1  , coordinate[1], coordinate[2]),
                (coordinate[0]      , coordinate[1] + 1, coordinate[2]),
                (coordinate[0]      , coordinate[1], coordinate[2] + 1)
            ]

    else:
        options = get_surrounding_coordinates(protein, coordinate)
        for position in positions:
            if position in options: options.remove(position)
        return options


def get_added_stability(protein, amino, step, care=0):
    ''' returns the added stability for a step from a partial chain of aminoacids '''
    if amino == "P" and care == 0:
        return 0, 0

    positions = get_surrounding_coordinates(protein, step)
    # remove last position in path to prevent counting bonds along the protein chain
    positions.remove(protein.path[-1][1])

    added_stability = 0
    weight = 0
    for amino_neighbor, amino_positions in protein.amino_positions.items():
        for position in positions:
            if position in amino_positions:
                binding_score, blocking_penalty = protein.bond_stabilities[amino][amino_neighbor]
                added_stability += binding_score
                weight += binding_score + blocking_penalty**(care)
    return added_stability, weight
