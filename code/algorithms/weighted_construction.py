''' 
weighted_construction.py

breadth-first search of stable configuration of protein 
'''
from code.helpers.navigator import get_step_options, get_added_stability
from copy import deepcopy
from random import choice

def look_ahead(protein, step, depth):
    ''' get cummulative score of every path in branch '''
    # copy protein
    temp_protein = deepcopy(protein)
    amino = temp_protein.sequence[len(protein.path)]
    weight = get_added_stability(temp_protein, amino, step)[0]
    temp_protein.add_step(amino, step)

    if depth > 0:
        options = get_step_options(temp_protein)
        if options != []:
            for step in options:
                weight += look_ahead(temp_protein, step, depth-1)
        else:
            # penalty for dead ends
            weight += 10
    return weight

def construct_weighted_path(protein, depth=1):
    ''' 
    constructs protein path based on prediction of scoring potential (weight) of each step
    '''
    protein.initialize_path()
    length = len(protein.sequence)

    for amino in protein.sequence[2:]:
        options = get_step_options(protein)
        weighted_options = [[option, 0] for option in options]
        for i, step in enumerate(weighted_options):
            # calculate depth of look-ahead depending on position in sequence
            look_depth = depth - (int((i + depth) > length) * (length - i - 2))
            weighted_options[i][1] = look_ahead(protein, step[0], look_depth)
        best_score = min([weight for option, weight in weighted_options])
        step = choice([option for option, weight in weighted_options if weight == best_score])
        protein.add_step(amino, step)

