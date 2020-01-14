from helpers.navigator import get_step_options, get_added_stability
from random import choice

def generate_greedy_path(protein, greed=1)
    '''
    generates path choosing highest scoring step if any, otherwise random
    TODO: implement variable greed
    '''
    # reinitialize path
    protein.initialize_path()
    protein.initialize_h_and_c_positions()

    for amino in protein.sequence[2:]:
        options = get_step_options(protein)
        weighted_options = []
        for option in options:
            weighted_options.append((option, get_added_stability(protein, amino, option)))
            
