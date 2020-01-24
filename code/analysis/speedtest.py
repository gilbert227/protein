"""
Contains the speedtest method
"""

from code.analysis.stats import *
from code.classes.protein import *
import time

def speedtest(protein, strategy, minutes = 1, greed = 1, care = 0, chunk_size = 6, chunk_iterations = 100, step_strategy = "greedy"):
    '''
    returns a dictionary of the results where the key is the stability and the values the number of times this stability is found by the algorithm,
    within the specified time called minutes
    '''

    results = {}

    t_end = time.time() + 60 * minutes
    while time.time() < t_end:
        generate_path(protein, strategy, greed, care, chunk_size, chunk_iterations, step_strategy)
        if protein.stability in results:
            results[protein.stability] += 1
        else:
            results[protein.stability] = 1

    return results
