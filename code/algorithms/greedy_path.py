from code.helpers.navigator import get_step_options, get_added_stability
from numpy.random import choice

def generate_greedy_path(protein, greed=1, care=0.5):
    '''
    generates path choosing highest scoring step if any, otherwise random
    TODO: implement variable greed
    '''
    # reinitialize path
    protein.initialize_path()

    # set bias for generating probability distribution from weights
    bias = 1

    for amino in protein.sequence[2:]:
        options = get_step_options(protein)
        if options != []:
            weights = []
            for option in options:
                weights.append(get_added_stability(protein, amino, option, care)[1])
            
            # apply bias for generating probability distribution
            max_weight = max(weights)
            weights = [abs(weight - max_weight) for weight in weights]
            best_score = max(weights)

            # apply greed
            weights = [greed * (weight == best_score) * (weight + bias) + (1 - greed) * (weight + ((1 - greed) * bias)) for weight in weights]

            # normalize weights
            sum_weights = sum(weights)
            weights = [weight / sum_weights for weight in weights]
            
            chosen_index = choice([i for i in range(len(options))], 1, p=weights)[0]
            protein.add_step(amino, options[chosen_index])
        else:
            # generate new greedy path if it cannot be finished
            generate_greedy_path(protein, greed, care)
            break
