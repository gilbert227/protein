''' 
weighted_construction.py

'''
from code.helpers.navigator import get_step_options, get_added_stability
from copy import deepcopy
from random import choice

def look_ahead(protein, step, depth):
    ''' get cummulative score of every path in branch '''
    # copy protein
    temp_protein = deepcopy(protein)
    amino = temp_protein.sequence[len(protein.path)]
    temp_protein.add_step(amino, step)
    weight = 0
    weight += temp_protein.stability

    if depth > 0:
        options = get_step_options(temp_protein)
        if options != []:
            for step in get_step_options(temp_protein):
                weight += look_ahead(temp_protein, step, depth-1)
    print(weight)
    return weight

def construct_weighted_path(protein, depth=1):
    ''' 
    constructs protein path based on prediction of scoring potential (weight) of each step
    '''
    protein.initialize_path()
 
    for amino in protein.sequence[2:-depth]:
        options = get_step_options(protein)
        if options == []:
            construct_weighted_path(protein, depth)
            break
        weighted_options = [[option, 0] for option in options]
        for i, step in enumerate(weighted_options):
            weighted_options[i][1] = look_ahead(protein, step[0], depth)
        best_score = min([weight for option, weight in weighted_options])
        step = choice([option for option, weight in weighted_options if weight == best_score])
        protein.add_step(amino, step)
