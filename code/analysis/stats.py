'''
stats.py

obtain statistics to examine algorithm performance
'''
import matplotlib.pyplot as plt
from code.algorithms.greedy_path import generate_greedy_path
from code.algorithms.random_path import generate_random_path
from code.algorithms.chunky_path import generate_chunky_path
from code.classes.protein import Protein
from copy import deepcopy
import numpy as np
import pandas as pd

amino_colors = {
    'P': 'black',
    'H': 'blue',
    'C': 'red'
}

def generate_path(protein, strategy, greed=1, care=0, chunk_size = 6, chunk_iterations = 500, step_strategy = "random"):
    if strategy == "random":
        generate_random_path(protein)
    elif strategy == "greedy":
        generate_greedy_path(protein, greed, care)
    elif strategy == "chunky path":
        generate_chunky_path(protein, chunk_size, chunk_iterations, step_strategy, care)

def get_next_unique_config(protein, strategy, configs=[], max_iterations=10000, greed=1, care=0):
    ''' returns first configuration not in configs '''
    for i in range(max_iterations):
        generate_path(protein, strategy, greed, care)
        config = protein.path
        if config not in configs:
            return (i, config, True)
    return (None, None, False)

def get_separating_duplicates(protein, strategy, duplication_threshold, greed=1, care=0):
    ''' get number of duplicates generated between found unique states '''
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

def get_best_config(protein, strategy, iterations, greed=1, care=0):
    best_stability = 0
    best_config = None

    for i in range(iterations):
        generate_path(protein, strategy, greed, care)
        stability = protein.stability
        if stability < best_stability:
            best_stability = stability
            best_config = deepcopy(protein)

    return best_config

def get_stability_histogram(protein, strategy, iterations, greed=1, care=0):
    stabilities = []

    for i in range(iterations):
        generate_path(protein, strategy, greed, care)
        stabilities.append(protein.stability)

    n_bins = len(set(stabilities))
    plt.hist(stabilities, bins=n_bins)
    plt.show()

    n = len(stabilities)
    mean = sum(stabilities)/n
    skew_num = 0
    skew_denom = 0
    for stability in stabilities:
        skew_num += (stability - mean)**3
        skew_denom += (stability - mean)**2
    skewness = (skew_num / n) / (skew_denom/(n-1))**(3/2)
    return mean, skewness

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

def get_stability_histogram(protein, strategy, iterations, greed=1, care=0):
    stabilities = []

    for i in range(iterations):
        generate_path(protein, strategy, greed, care)
        stabilities.append(protein.stability)

    n_bins = len(set(stabilities))
    plt.hist(stabilities, bins=n_bins)
    plt.show()

    n = len(stabilities)
    mean = sum(stabilities)/n
    skew_num = 0
    skew_denom = 0
    for stability in stabilities:
        skew_num += (stability - mean)**3
        skew_denom += (stability - mean)**2
    skewness = (skew_num / n) / (skew_denom/(n-1))**(3/2)
    return mean, skewness

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

def comparing_test(protein, strategy, iterations, greed=1, care_hist=True, freq_table=True):

    # GREEDY CARE ITERATIONS -----------------------------------------------------------------------
    if care_hist == True:
        count = 0

        # use care from 0.0 to 1.1
        for i in np.arange(0, 12, 1):
            count += 1
            stabilities = []

            for ii in range(iterations):
                generate_path(protein, strategy, greed=greed, care=i/10)
                stabilities.append(protein.stability)

            df = pd.DataFrame(stabilities, columns=['Stability'])
            df.sort_values(by=['Stability'], inplace=True)

            quantile = int(df.quantile(.01))

            df = df[df['Stability'] <= quantile]

            n_bins = len(set(df['Stability']))
            plt.subplot(3, 4, count)

            mean = sum(stabilities)/iterations
            plt.title(f'care = {i / 10}, mean = {mean}, quartile = {quantile}')
            plt.hist(df['Stability'], bins=n_bins, color='green')

        plt.show()

def care_histogram(protein, iterations, strategy, percentage):
    """
    """
    count = 0

    # use care from 0.0 to 1.1
    for i in np.arange(0, 12, 1):
        count += 1
        stabilities = []

        for ii in range(iterations):
            generate_path(protein, strategy, 1, i/10)
            stabilities.append(protein.stability)

        # make dataframe using pandas
        df = pd.DataFrame(stabilities, columns=['Stability'])
        df.sort_values(by=['Stability'], inplace=True)

        # get the desired range of data
        percentile = int(df.quantile(percentage))
        df = df[df['Stability'] <= percentile]

        mean = sum(stabilities)/iterations

        # plot the histograms
        n_bins = len(set(df['Stability']))
        plt.subplot(3, 4, count)
        plt.title(f'care = {i / 10}, mean = {mean}')
        plt.hist(df['Stability'], bins=n_bins, color='green')

    plt.show()
