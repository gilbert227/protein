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
        forward_search(protein, depth)

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

    for i in range(iterations):
        generate_path(protein, strategy, greed, care, chunk_size, chunk_iterations, step_strategy, depth)
        stability = protein.stability
        if stability < best_stability:
            best_stability = stability
            best_config = deepcopy(protein)

    protein.__dict__ = best_config.__dict__.copy()

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

def comparing_test(protein, iterations_random, iterations_greedy, iterations_chunky, care):

    df = pd.DataFrame()

    # greedy
    stabilities = []
    for i in range(iterations_greedy):
        generate_path(protein, 'greedy', care=0)
        stabilities.append(protein.stability)

    stabilities.sort()
    dict_stability = {'Greedy': stabilities}

    df = df.assign(**dict_stability)

    # greedy care=0.3
    stabilities = []
    for i in range(iterations_greedy):
        generate_path(protein, 'greedy', care=0.3)
        stabilities.append(protein.stability)

    stabilities.sort()
    dict_stability = {'GreedyC': stabilities}

    df = df.assign(**dict_stability)

    # random
    stabilities = []
    for i in range(iterations_random):
        generate_path(protein, 'random', care=care)
        stabilities.append(protein.stability)

    stabilities.sort()
    dict_stability = {'Random': stabilities}

    df = df.assign(**dict_stability)

    # chunky path
    df_chunky = pd.DataFrame()
    stabilities = []
    for i in range(iterations_chunky):
        generate_path(protein, 'chunky path', care=0)
        stabilities.append(protein.stability)

    stabilities.sort()

    dict_stability = {'Chunky': stabilities}

    df_chunky = df_chunky.assign(**dict_stability)

    # chunky path care=0.3
    stabilities = []
    for i in range(iterations_chunky):
        generate_path(protein, 'chunky path', care=0.1)
        stabilities.append(protein.stability)

    stabilities.sort()
    dict_stability = {'ChunkyC': stabilities}
    df_chunky = df_chunky.assign(**dict_stability)

    # get best value
    best_norm = df.iloc[0].min()
    best_chunkyC = df_chunky['ChunkyC'].iloc[0]
    best_chunky = df_chunky['Chunky'].iloc[0]
    if best_chunkyC < best_chunky:
        best = best_chunkyC
        alg = 'chunkyC'
    else:
        best = best_chunky
        alg = 'chunky'

    if best > best_norm:
        best = best_norm
        alg = 'norm'

    # Draw Plot
    plt.figure(figsize=(16,10), dpi= 80)
    sns.kdeplot(df["Random"], shade=True, color="g", label="Random", alpha=.7)
    sns.kdeplot(df["Greedy"], shade=True, color="deeppink", label="Greedy", alpha=.7)
    sns.kdeplot(df["GreedyC"], shade=True, color="orange", label="Greedy, care=0.3", alpha=.7)
    sns.kdeplot(df_chunky["Chunky"], shade=True, color="dodgerblue", label="Chunky", alpha=.7)
    sns.kdeplot(df_chunky["ChunkyC"], shade=True, color="red", label="ChunkyC", alpha=.7)

    # Decoration
    plt.title(f'Density Plot of algorithms, {best} {alg}', fontsize=22)
    plt.legend()
    plt.show()

    print(df)

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

    return protein
