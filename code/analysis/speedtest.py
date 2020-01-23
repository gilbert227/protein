from code.algorithms.greedy_path import generate_greedy_path
from code.algorithms.random_path import generate_random_path
from code.algorithms.chunky_path import generate_chunky_path
from code.algorithms.forward_search import forward_search
from code.algorithms.stats import *
import time

def speedtest(protein, strategy, minutes = 1, greed = 1, care = 0, chunk_size = 6, chunk_iterations = 100, step_strategy = "g"):
    '''
    tests the speed of the different algorithms and stores the stabilities as results
    '''

    results = []
    counter = 0

    t_end = time.time() + 60 * minutes
    while time.time() < t_end:
        generate_path(protein, strategy, greed, care, chunk_size, chunk_iterations, step_strategy)
        results.append(protein.stability)
        counter += 1

    return results, counter
