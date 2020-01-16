'''
stats.py

obtain statistics to examine algorithm performance
'''
import matplotlib.pyplot as plt
from algorithms.greedy_path import generate_greedy_path
from algorithms.random_path import generate_random_path
from classes.protein import Protein
from copy import deepcopy

amino_colors = {
    'P': 'black',
    'H': 'blue',
    'C': 'red'
}

def generate_path(protein, strategy):
    if strategy == "random":
        generate_random_path(protein)
    elif strategy == "greedy":
        generate_greedy_path(protein)

def get_next_unique_config(protein, strategy, configs=[], max_iterations=10000):
    ''' returns first configuration not in configs '''
    for i in range(max_iterations):
        generate_path(protein, strategy)
        config = protein.path
        if config not in configs:
            return (i, config, True)
    return (None, None, False)

def get_separating_duplicates(protein, strategy, duplication_threshold):
    ''' get number of duplicates generated between found unique states '''
    configs = []
    separating_duplicates = []
    found = True

    while found:
        separation, config, found = get_next_unique_config(protein, strategy, configs, duplication_threshold)
        separating_duplicates.append(separation)
        configs.append(config)
    # remove last element from configs, contains (None, None, False)
    separating_duplicates.pop()
    # plot for testing purposes, should be separate function
    plt.plot(separating_duplicates)
    plt.show()
    
    return separating_duplicates, len(separating_duplicates)

def get_best_config(protein, strategy, iterations):
    best_stability = 0
    best_config = None

    for i in range(iterations):
        generate_path(protein, strategy)
        stability = protein.stability
        if stability < best_stability:
            best_stability = stability
            best_config = deepcopy(protein)
    
    return best_config

def get_stability_histogram(protein, strategy, iterations):
    stabilities = []

    for i in range(iterations):
        generate_path(protein, strategy)
        stabilities.append(protein.stability)
    n_bins = len(set(stabilities))
    plt.hist(stabilities, bins=n_bins)
    plt.show()

def estimate_max_stability(protein):
    pass



def plot_path(protein):
    ''' visualisation of folded protein '''
    x_positions = []
    y_positions = []
    point_markers = []
    for amino, position in protein.path:
        x = position[0]
        y = position[1]
        x_positions.append(x)
        y_positions.append(y)

        plt.text(x, y, amino, horizontalalignment='center', verticalalignment='center', color=amino_colors[amino])
    plt.title(f"stability: {protein.stability}")
    plt.plot(x_positions, y_positions, 'ko-', markerfacecolor='white', markersize=15)
    plt.axis('off')
    plt.show()
