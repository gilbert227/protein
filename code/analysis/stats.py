'''
stats.py

obtain statistics to examine algorithm performance
'''
import matplotlib.pyplot as plt
from algorithms.greedy_path import generate_greedy_path
from algorithms.random_path import generate_random_path

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
    ''' get number of generated duplicates between found unique states '''
    configs = []
    separating_duplicates = []
    found = True

    while found:
        separation, config, found = get_next_unique_config(protein, strategy, configs, duplication_threshold)
        separating_duplicates.append(separation)
        configs.append(config)
    separating_duplicates.pop()
    plt.plot(separating_duplicates)
    plt.show()
    return separating_duplicates, len(separating_duplicates)
