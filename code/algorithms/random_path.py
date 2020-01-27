from code.helpers.navigator import get_step_options
from random import choice

def generate_random_path(protein):
    ''' generates random path '''
    # reinitialize protein path
    protein.initialize_path()

    for amino in protein.sequence[2:]:
        options = get_step_options(protein)
        if options != []:
            step = choice(options)
            protein.add_step(amino, step)
        else:
            # generate new path if path cannot be finished
            generate_random_path(protein)
            break
