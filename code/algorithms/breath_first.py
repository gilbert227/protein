from helpers.navigator import get_step_options, get_added_stability
from classes.protein import Protein
from random import choice
import copy


def generate_breath_first(protein = Protein("HCPHPHPHCHHHHPCCPPHPPPHPPPPCPPPHPPPHPHHHHCHPHPHPHH"), n = 2):
    '''
    generates an algorithm that runs n amount of amino letters and then chooses the one with the most amount of stability points,
    then goes on to the next n amount of letters
    '''
    protein.initialize_path()


    a = 2
    number_of_chunks = round((len(protein.sequence) - 2)/n)
    for i in range(number_of_chunks):
        decide_best_chunk(protein, a, n)
        a = a + n

    return (protein.path, protein.stability)

def decide_best_chunk(protein, a, n):

    iterations = 1000
    best_path = [None,1]

    # make a copy of the starting states
    # this should be simpler/better, but for now it works
    # if I do not do this, it will add k amount of iterations to protein which is bad
    start_amino_positions = copy.deepcopy(protein.amino_positions)
    start_stability = copy.deepcopy(protein.stability)
    start_symmetric = copy.deepcopy(protein.symmetric)


    for i in range(iterations):
        # simply perform the algorithm to choose, I think random is best
        for amino in protein.sequence[a:a+n]:
            options = get_step_options(protein)
            if options != []:
                step = choice(options)
                protein.add_step(amino, step)

                # I do not know how to deal with crash errors here
                # there should be some more checks

        # save the best path and stability
        stability = protein.stability
        if stability < best_path[1]:
            best_path[0] = copy.deepcopy(protein.path)
            best_path[1] = protein.stability

        # set protein object back to starting state
        protein.return_to_start(n, start_stability, start_amino_positions, start_symmetric)

    # add best result to protein class
    protein.add_chunk(best_path[0], n)

    return best_path
