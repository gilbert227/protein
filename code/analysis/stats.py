'''
stats.py

includes methods to obtain statistics to examine algorithm performances
'''
from code.algorithms.greedy_path import generate_greedy_path
from code.algorithms.random_path import generate_random_path
from code.algorithms.chunky_path import generate_chunky_path
from code.algorithms.forward_search import forward_search

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.lines import Line2D
import seaborn as sns
from copy import deepcopy
import numpy as np
import pandas as pd
import operator
import time

def generate_path(protein, strategy, greed=1, care=0, chunk_size=8, chunk_iterations=50, step_strategy="greedy", depth=3):
    '''
    generates a path according to the chosen strategy
    '''
    if strategy == "random":
        generate_random_path(protein)
    elif strategy == "greedy":
        generate_greedy_path(protein, greed, care)
    elif strategy == "chunky path":
        generate_chunky_path(protein, chunk_size, chunk_iterations, step_strategy, care)
    elif strategy == "forward search":
        forward_search(protein, depth)

def get_next_unique_config(protein, strategy, configs=[], max_iterations=10000, greed=1, care=0, chunk_size=8, chunk_iterations=100, step_strategy="greedy"):
    '''
    returns first configuration not in configs
    '''
    for i in range(max_iterations):
        generate_path(protein, strategy, greed, care, chunk_size, chunk_iterations, step_strategy)
        config = protein.path
        if config not in configs:
            return (i, config, True)
    return (None, None, False)

def get_separating_duplicates(protein, strategy, duplication_threshold, greed=1, care=0, chunk_size=8, chunk_iterations=100, step_strategy="greedy", depth=3):
    '''
    gets number of duplicates generated between found unique states
    '''
    configs = []
    separating_duplicates = []
    found = True

    while found:
        separation, config, found = get_next_unique_config(protein, strategy, configs, duplication_threshold, greed, care)
        separating_duplicates.append(separation)
        configs.append(config)
    # remove last element from configs, contains (None, None, False)
    separating_duplicates.pop()
    # plot for testing purposes, should be separate function
    plt.plot(separating_duplicates)
    plt.show()

    return separating_duplicates, len(separating_duplicates)

def get_best_config(protein, strategy, iterations, greed=1, care=0, chunk_size=8, chunk_iterations=100, step_strategy="greedy", depth=3):
    '''
    generates a number of paths, defined by iterations and sets the best value as the protein object
    '''
    best_stability = 0
    best_config = None

    for i in range(iterations):
        generate_path(protein, strategy, greed, care, chunk_size, chunk_iterations, step_strategy, depth)

        stability = protein.stability
        if stability < best_stability:
            best_stability = stability
            best_config = deepcopy(protein)

    protein.__dict__ = best_config.__dict__.copy()

def speedtest(protein, strategy, minutes=1, greed=1, care=0, chunk_size=8, chunk_iterations=100, step_strategy="greedy", depth=3):
    '''
    returns a dictionary of the results where the key is the stability of the protein and the value the number of times this stability is found by the algorithm,
    within the specified time called minutes
    '''

    results = {}

    t_end = time.time() + 60 * minutes
    while time.time() < t_end:
        generate_path(protein, strategy, greed, care, chunk_size, chunk_iterations, step_strategy, depth)
        if protein.stability in results:
            results[protein.stability] += 1
        else:
            results[protein.stability] = 1

    return results
