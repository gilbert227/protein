'''
greedy_path.py

implementation of greedy path-generating algorithm.
'''

from code.helpers.navigator import make_up_your_mind
from numpy.random import choice

def generate_greedy_path(protein, greed=1, care=0):
    '''
    generates path by choosing among the available options based on the step's score

    the value of greed (between 0 and 1) determines the likelhood of choosing
    highest-scoring options over others.
    '''
    # reinitialize path
    protein.initialize_path()

    for amino in protein.sequence[2:]:
        # generate step for every aminoacid in the protein sequence
        step = make_up_your_mind(protein, amino, greed, care)

        # check for dead end
        if not step:
            # generate new greedy path
            generate_greedy_path(protein, greed, care)
            break

        protein.add_step(amino, step[0])
