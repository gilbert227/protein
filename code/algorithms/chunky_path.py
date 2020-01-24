"""
- greed function
- 
""" 

from code.helpers.navigator import get_step_options, get_added_stability
from random import choice
import copy
import math

def generate_chunky_path(protein, chunk_size = 6, iterations = 50, step_strategy = "greedy", care = 0):

    # this is the starting amino letter in the sequence, as the first two are already set, we start with index 2
    start = 2
    protein.initialize_path()

    # determine if the whole path can be made in chunks
    chunks = math.floor((len(protein.sequence) - start)/chunk_size)
    chars_left = len(protein.sequence) - start - (chunk_size * chunks)

    crash = False

    for chunk in range(chunks):
        best_stability = 100

        # simulate the paths in the chunks
        for i in range(iterations):
            simulation = copy.deepcopy(protein)

            # used to check if the first letter in a chunk has a coordinate to go to
            counter = 0
            first_letter_stuck = False

            # create the paths, choose between using a random step or a greedy step in method
            for amino in simulation.sequence[start:start + chunk_size]:
                if step_strategy == "random":
                    # perform random step algorithm
                    options = get_step_options(simulation)
                    if options != []:
                        step = choice(options)
                        simulation.add_step(amino, step)
                        counter += 1
                    else:
                        if counter == 0:
                            first_letter_stuck = True
                        # the chunk could not be finished, add a 100 stability points so it will not be chosen as best chunk
                        simulation.stability += 100
                        break
                else:
                    # perform greedy step algorithm
                    options = get_step_options(simulation)
                    if options != []:
                        weighted_options = []
                        for option in options:
                            weighted_options.append((option, get_added_stability(simulation, amino, option, care)[1]))
                        best_score = min([weight for option, weight in weighted_options])
                        step = choice([option for option, weight in weighted_options if weight == best_score])
                        simulation.add_step(amino, step)
                        counter += 1
                    else:
                        if counter == 0:
                            first_letter_stuck = True
                        # the chunk could not be finished, add a 100 stability points so it will not be chosen as best chunk
                        simulation.stability += 100
                        break

            # stop iterating over chunks if the first letter has no where to go
            if first_letter_stuck:
                break

            # determine the chunk with the best stability
            if simulation.stability < best_stability:
                best_stability = copy.deepcopy(simulation.stability)
                best_path = copy.deepcopy(simulation.path)



        if best_stability > 0:
            # the sequence crashed and has no options left, so stop iterating over chunks
            crash = True
            break
        else:
            # add the best path to the protein object
            for amino, step in best_path[-chunk_size:]:
                protein.add_step(amino, step)
            start += chunk_size

    # if there are remaining letters, add them by using a random or greedy method
    if not crash and chars_left > 0:
        for amino in protein.sequence[start:len(protein.sequence)]:
            if step_strategy == "random":
                # perform random step algorithm
                options = get_step_options(protein)
                if options != []:
                    step = choice(options)
                    protein.add_step(amino, step)
                else:
                    crash = True
                    break
            else:
                # perform greedy step algorithm
                options = get_step_options(protein)
                if options != []:
                    weighted_options = []
                    for option in options:
                        weighted_options.append((option, get_added_stability(protein, amino, option, care)[1]))
                    best_score = min([weight for option, weight in weighted_options])
                    step = choice([option for option, weight in weighted_options if weight == best_score])
                    protein.add_step(amino, step)

    # the sequence crashed somewhere, so start a new path
    if crash:
        generate_chunky_path(protein)
