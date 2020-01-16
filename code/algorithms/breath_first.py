from helpers.navigator import get_step_options, get_added_stability
from classes.protein import Protein
from random import choice
import copy


def generate_breath_first(protein, n = 4):
    '''
    generates an algorithm that runs n amount of amino letters and then chooses the one with the most amount of stability points,
    then goes on to the next n amount of letters
    one requirement is that: (length of the protein sequence - 2)/n is an integer.
    '''
    # reinitialize protein path
    protein.initialize_path()

    # set the amount of chunk iterations and the starting point in the protein sequence
    iterations = 100
    a = 2

    # determine the amount of chunks one can use
    number_of_chunks = round((len(protein.sequence) - a)/ n)

    # iterate over the chunks and decide the best path per chunk
    for i in range(number_of_chunks):
        best_path = [None,1]

        # make a copy of the starting states
        # this should be simpler/better, but for now it works
        # if I do not do this, it will add k amount of iterations to protein which is bad
        start_amino_positions = copy.deepcopy(protein.amino_positions)
        start_stability = copy.deepcopy(protein.stability)
        start_symmetric = copy.deepcopy(protein.symmetric)

        for i in range(iterations):
            # simply perform the algorithm to choose, now it is random
            for amino in protein.sequence[a:a+n]:
                options = get_step_options(protein)
                if options != []:
                    step = choice(options)
                    protein.add_step(amino, step)
                else:
                    # if there is no option, set stability to 100 so it will never be chosen
                    protein.stability = 100
                    break

            # save the best path and stability
            stability = protein.stability
            if stability < best_path[1]:
                best_path[0] = copy.deepcopy(protein.path)
                best_path[1] = protein.stability

            # set protein object back to starting state
            protein.return_to_start(n, start_stability, start_amino_positions, start_symmetric)

        # add best result to protein class
        if best_path[1] < 0:
            # add the chunk to the path, sometimes it is not possible because the sequence has crashed,
            # this will leave errors when we want to remove the previous position in a path, as
            # this this possition does not exist
            try:
                protein.add_chunk(best_path[0], n)
            except:
                break

        # determine next chunk
        a = a + n

    # final check for errors
    if len(protein.path) != len(protein.sequence):
        generate_breath_first(protein)
