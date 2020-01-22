''' 
weighted_construction.py

search of stable configuration of protein by looking ahead
'''
from code.helpers.navigator import get_step_options, get_added_stability
from copy import deepcopy
from random import choice

def look_ahead(protein, amino, step, depth, penalty, depth_multiplier):
    ''' get cummulative score of every path in branch '''
    # start by calculating added stability of step, 
    # if end of search depth is reached, this is returned
    weight = (depth_multiplier ** depth) * get_added_stability(protein, amino, step)[0]

    if depth > 1:
        # copy protein
        temp_protein = deepcopy(protein)
        # get next aminoacid
        temp_amino = temp_protein.sequence[len(temp_protein.path)]
        temp_protein.add_step(temp_amino, step)
        options = get_step_options(temp_protein)
        if options != []:
            for step in options:
                weight += look_ahead(temp_protein, temp_amino, step, depth-1, penalty, depth_multiplier)
        else:
            # penalty for dead ends
            weight += penalty
    return weight

def construct_weighted_path(protein, depth=1, penalty=10, depth_multiplier=10):
    ''' 
    constructs protein path based on prediction of scoring potential (weight) of each step
    '''
    protein.initialize_path()
    length = len(protein.sequence)

    for i, amino in enumerate(protein.sequence[2:]):
        options = get_step_options(protein)
        weighted_options = [[option, 0] for option in options]
        for j, step in enumerate(weighted_options):
            # calculate depth of look-ahead depending on position in sequence
            look_depth = depth - (int((i + depth) >= length) * (length - i))
            weighted_options[j][1] = look_ahead(protein, amino, step[0], look_depth, penalty, depth_multiplier)
        best_score = min([weight for option, weight in weighted_options])
        step = choice([option for option, weight in weighted_options if weight == best_score])
        protein.add_step(amino, step)

