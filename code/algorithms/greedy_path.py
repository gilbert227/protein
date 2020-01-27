from code.helpers.navigator import make_up_your_mind
from numpy.random import choice

def generate_greedy_path(protein, greed=1, care=0):
    '''
    generates path choosing highest scoring step if any, otherwise random
    TODO: implement variable greed
    '''
    # reinitialize path
    protein.initialize_path()

    for amino in protein.sequence[2:]:
        step = make_up_your_mind(protein, amino, greed, care)

        # check for dead end
        if not step:
            # generate new greedy path
            generate_greedy_path(protein, greed, care)
            break

        protein.add_step(amino, step[0])
