'''
stats.py

obtain statistics to examine algorithm performance
'''
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from code.algorithms.greedy_path import generate_greedy_path
from code.algorithms.random_path import generate_random_path
from code.algorithms.chunky_path import generate_chunky_path
from code.algorithms.forward_search import forward_search
from code.classes.protein import Protein
from code.helpers.navigator import *
import seaborn as sns
from copy import deepcopy
import numpy as np
import pandas as pd
import time
import operator
import csv
import ast

amino_colors = {
    'P': 'blue',
    'H': 'red',
    'C': 'green'
}

def generate_path(protein, strategy, greed=1, care=0, chunk_size = 6, chunk_iterations = 500, step_strategy = "random", depth = 3):
    if strategy == "random":
        generate_random_path(protein)
    elif strategy == "greedy":
        generate_greedy_path(protein, greed, care)
    elif strategy == "chunky path":
        generate_chunky_path(protein, chunk_size, chunk_iterations, step_strategy, care)
    elif strategy == "forward search":
        return forward_search(protein, depth)

def get_next_unique_config(protein, strategy, configs=[], max_iterations=10000, greed=1, care=0, chunk_size = 6, chunk_iterations = 500, step_strategy = "random"):
    ''' returns first configuration not in configs '''
    for i in range(max_iterations):
        generate_path(protein, strategy, greed, care, chunk_size, chunk_iterations, step_strategy)
        config = protein.path
        if config not in configs:
            return (i, config, True)
    return (None, None, False)

def get_separating_duplicates(protein, strategy, duplication_threshold, greed=1, care=0, chunk_size=6, chunk_iterations=500, step_strategy="random", depth=3):
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

def get_best_config(protein, strategy, iterations, greed=1, care=0.2, chunk_size=6, chunk_iterations=500, step_strategy="greedy", depth=3):
    best_stability = 0
    best_config = None
    
    if strategy == 'forward search':
        # temporary fix for forward search: TODO: fix this issue
        for i in range(iterations):
            new_protein = generate_path(protein, 'forward search', iterations, depth=depth)
            stability = new_protein.stability
            print(stability)
            if stability < best_stability:
                best_stability = stability
                best_config = deepcopy(new_protein)
        return best_config

    for i in range(iterations):
        generate_path(protein, strategy, greed, care, chunk_size, chunk_iterations, step_strategy, depth)
        stability = protein.stability
        if stability < best_stability:
            best_stability = stability
            best_config = deepcopy(protein)

    protein = deepcopy(best_condig)

def get_stability_histogram(protein, strategy, iterations, greed=1, care=0, chunk_size = 6, chunk_iterations = 500, step_strategy = "random", depth=3):
    stabilities = []

    for i in range(iterations):
        generate_path(protein, strategy, greed, care, chunk_size, chunk_iterations, step_strategy)
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

def plot_path(protein):
    ''' visualisation of folded protein, depending on 3D '''
    x_positions = []
    y_positions = []
    if protein.dim3:
        z_positions = []
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

    # create the coordinates and add the specific amino value to it
    for amino, position in protein.path:
        x = position[0]
        y = position[1]
        x_positions.append(x)
        y_positions.append(y)

        if protein.dim3:
            z = position[2]
            z_positions.append(z)
            ax.scatter(x, y, z, s=140, marker='o', linewidths=1, color=amino_colors[amino])
        else:
            plt.scatter(x, y, s=160, marker='o', linewidths=1, color=amino_colors[amino])

    if protein.dim3:
        ax.plot(x_positions, y_positions, z_positions, 'ko-', alpha=0.4, ms=1)
    else:
        plt.plot(x_positions, y_positions, 'ko-', alpha=0.4, ms=1)

    plt.title(f"stability: {protein.stability}")
    plt.axis('off')
    plt.show()

def care_histogram(protein, iterations, strategy, percentage, chunk_size = 6, chunk_iterations = 100, step_strategy = "greedy"):
    """
    """
    df = pd.DataFrame()

    # use care from 0.0 to 1.1
    for i in np.arange(0, 12, 1):
        care = i/10
        stabilities = []

        for ii in range(iterations):
            generate_path(protein, strategy, greed=1, care=care, chunk_size=chunk_size, chunk_iterations=chunk_iterations, step_strategy=step_strategy)
            stabilities.append(protein.stability)

        stabilities.sort()
        dict_stability = {f'care={care}': stabilities}

        df = df.assign(**dict_stability)

    df.drop(df.tail(int((iterations / 100) * (1-percentage))).index,inplace=True)
    
    min = df.iloc[0].min()
    max = df.iloc[-1].max()

    best_care = df.iloc[0].idxmin()

    fig, axes = plt.subplots(nrows=3, ncols=4)
    fig.subplots_adjust(hspace=0.5)
    fig.suptitle(f'Distribution of different care values, best for {best_care}')
    

    for i, ax in zip(np.arange(0, 12, 1), axes.flatten()):
        care = i/10
        sns.distplot(df[f'care={care}'], ax=ax, bins=len(set(df[f'care={care}'])), color='green')
        ax.set(title=f'care = {care}')
        ax.set_xlim([min, max])
        # plt.ylim(ymin=0, ymax=150)

    plt.show()

def comparing_test(protein, it_random=0, care_random=0, it_greedy=0, care_greedy=0, it_chunky=0, care_chunky=0):

    # random 
    df_random = pd.DataFrame()
    stabilities = []
    for i in range(it_random):
        generate_path(protein, 'random', care=care_random)
        stabilities.append(protein.stability)

    stabilities.sort()
    dict_stability = {'random': stabilities}

    df_random = df_random.assign(**dict_stability)


    # greedy
    df_greedy = pd.DataFrame()
    stabilities = []
    for i in range(it_greedy):
        generate_path(protein, 'greedy', care=care_greedy)
        stabilities.append(protein.stability)

    stabilities.sort()
    dict_stability = {'greedy': stabilities}

    df_greedy = df_greedy.assign(**dict_stability)

   
    # chunky path
    df_chunky = pd.DataFrame()
    stabilities = []
    for i in range(it_chunky):
        generate_path(protein, 'chunky path', care=care_chunky)
        stabilities.append(protein.stability)

    stabilities.sort()
    dict_stability = {'chunky': stabilities}

    df_chunky = df_chunky.assign(**dict_stability)

    # get best solution
    if it_greedy > 0:
        best_greedy = int(df_greedy.iloc[0])
    else:
        best_greedy = 0
    if it_chunky > 0:
        best_chunky = int(df_chunky.iloc[0])
    else:
        best_chunky = 0
    if it_random > 0:
        best_random = int(df_random.iloc[0])
    else:
        best_random = 0

    if best_random < best_greedy and best_random < best_chunky:
        best_solution = best_random
        algorithm = 'Random'
    elif best_greedy < best_random and best_greedy < best_chunky:
        best_solution = best_greedy
        algorithm = 'Greedy'
    else:
        best_solution = best_chunky
        algorithm = 'Chunky Path'

    # Draw Plot
    plt.figure(figsize=(16,10), dpi= 80)
    sns.kdeplot(df_random["random"], shade=True, color="red", label=f'Random, care={care_random}', alpha=.7)
    sns.kdeplot(df_greedy["greedy"], shade=True, color="deeppink", label=f'Greedy, care={care_greedy}', alpha=.7)
    sns.kdeplot(df_chunky["chunky"], shade=True, color="orange", label=f'Chunky, care={care_chunky}', alpha=.7)

    # Decoration
    plt.title(f'Density Plot of algorithms, best solution={best_solution} from {algorithm}', fontsize=22)
    plt.legend()
    plt.show()

def speedtest(protein, strategy, minimum_stability, default = "y", iterations = 100, greed = 1, care = 0, chunk_size = 6, chunk_iterations = 100, step_strategy = "g"):
    '''

    '''

    start = time.time()
    counter = 0
    for i in range(iterations):
        if strategy == "g":
            generate_greedy_path(protein)
        elif strategy == "c":
            if default == "y":
                generate_chunky_path(protein)
            else:
                generate_chunky_path(protein, chunk_size, chunk_iterations, step_strategy, care)
        else:
            generate_random_path(protein)

        if protein.stability < minimum_stability:
            print("protein: ")
            print(protein)
            print()

            counter += 1

    end = time.time()
    print(f"Amount of results: {counter}")
    print(f"Time passed: {end - start}")
    print()

def csv_compiler(protein):
    '''
    makes an csv file with protein stats
    '''

    directions = get_path_directions(protein)

    with open('protein.csv', 'w') as csvfile:
        fieldnames = ['amino', 'direction', 'coordinates']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for number, amino in enumerate(protein.sequence):
            writer.writerow({'amino': amino, 'direction': directions[number], 'coordinates': protein.path[number][1]})

def csv_reader():
    '''
    creates a protein object where the path is defined in the csv file as made by csv_compiler where the filename is protein.csv and information is given as:
    amino, direction, coordinate
    '''
    sequence = ""
    coordinates = []
    with open('protein.csv') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count > 0:
                sequence += row[0]
                coordinates.append(ast.literal_eval(row[2]))
            line_count += 1

    if coordinates == [] or sequence == "":
        return f"No data found"


    if len(coordinates[0]) == 2:
        protein = Protein(sequence)
    else:
        protein = Protein(sequence, dim3=True)

    number = 2
    for amino in protein.sequence[2:]:
        protein.add_step(amino, coordinates[number])
        number += 1
