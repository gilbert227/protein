from helpers.navigator import get_step_options, get_added_stability
from random import choice

def generate_greedy_path(protein, care=0.5, greed=1):
    '''
    generates path choosing highest scoring step if any, otherwise random
    TODO: implement variable greed
    '''
    # reinitialize path
    protein.initialize_path()

    for amino in protein.sequence[2:]:
        options = get_step_options(protein)
        if options != []:
            weighted_options = []
            for option in options:
                weighted_options.append((option, get_added_stability(protein, amino, option, care)[1]))
            best_score = min([weight for option, weight in weighted_options])
            step = choice([option for option, weight in weighted_options if weight == best_score])    
            protein.add_step(amino, step)
        else:
            # generate new greedy path if it cannot be finished
            generate_greedy_path(protein, care, greed)
            break

