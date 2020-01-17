''' 
weighted_construction.py

'''
from code.helpers.navigator import get_step_options, get_added_stability
from copy import deepcopy
from random import choice

def look_ahead(protein, step, depth):
    if depth >= 0:
        # copy protein
        temp_protein = deepcopy(protein)
        amino = protein.sequence[len(protein.path)]
        protein.add_step(amino, step)
        weight = 0
        for step in get_step_options(temp_protein):
            weight += look_ahead(temp_protein, step, depth-1)
        return weight

def construct_weighted_path(protein, depth=6):
    ''' 
    constructs protein path based on prediction of scoring potential (weight) of each step
    '''
    protein.initialize_path()
 
    for amino in protein.sequence[2:-depth]:
        weighted_options = [(option, 0) for option in get_step_options(protein)]
        for i, step in enumerate(weighted_options):
            weighted_options[i][1] = look_ahead(protein, step[0], depth)
        best_score = min([weight for option, weight in weighted_options])
        step = choice([option for option, weight in weighted_options if weight == best_score])
        protein.add_step(amino, step)
