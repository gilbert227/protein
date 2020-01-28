'''
visuals.py

contains functions that can plot the protein path, or analyze variables used
in algorithms.
'''

from code.analysis.stats import generate_path, speedtest

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.lines import Line2D
import seaborn as sns
from copy import deepcopy
import numpy as np
import time
import pandas as pd
import operator
import ast

def plot_path(protein):
    ''' visualisation of folded protein, depending on 3D '''

    amino_colors = {
    'P': 'blue',
    'H': 'red',
    'C': 'green'
    }

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
            ax.scatter(x, y, z, s=140, marker='o', linewidths=1,
                        color=amino_colors[amino], )
        else:
            plt.scatter(x, y, s=160, marker='o', linewidths=1,
                        color=amino_colors[amino], )

    if protein.dim3:
        ax.plot(x_positions, y_positions, z_positions, 'ko-', alpha=0.4, ms=1)
    else:
        plt.plot(x_positions, y_positions, 'ko-', alpha=0.4, ms=1)

    plt.title(f"stability: {protein.stability}")

    custom_lines = [Line2D([0], [0], marker='o', markersize=10, color='blue',
                        label='P', lw=0),
                    Line2D([0], [0], marker='o', markersize=10, color='red',
                        label='H', lw=0),
                    Line2D([0], [0], marker='o', markersize=10, color='green',
                        label='C', lw=0)]

    plt.legend(handles = custom_lines)

    plt.axis('off')
    plt.show()

def care_histogram(protein, iterations, strategy, percentage, max_care,
        nrows=2, ncols=2, chunk_size=8, chunk_iterations=50,
        step_strategy="greedy"):
    '''
    Plots the given strategies for different values for care in one figure with
    multiple histograms. The input argument 'percentage' is used to filter the
    amount shown in the plot. Care is tested for 0.0 until 'max_care'.
    '''

    df = pd.DataFrame()

    # use care from 0.0 to max_care
    for i in np.arange(0, max_care * 10 + 1, 1):
        care = i/10
        stabilities = []

        for ii in range(iterations):
            generate_path(protein, strategy, greed=1, care=care,
                chunk_size=chunk_size,
                chunk_iterations=chunk_iterations,
                step_strategy=step_strategy)

            stabilities.append(abs(protein.stability))

        stabilities.sort()
        dict_stability = {f'care={care}': stabilities}

        df = df.assign(**dict_stability)

    # get the desired percentage data to plot
    df.drop(df.head(int((iterations / 100) *
            (1 - percentage))).index,inplace=True)

    # used for range of x-axis for plot
    min = df.iloc[0].min()
    max = df.iloc[-1].max()

    best_care = df.iloc[-1].idxmax()

    sns.set()
    fig, axes = plt.subplots(nrows=nrows, ncols=ncols)
    fig.subplots_adjust(hspace=0.5)
    fig.suptitle(f'Distribution of different care values, best for \
                {best_care} with the {strategy} algorithm')

    sns.set_palette('pastel')
    for i, ax in zip(np.arange(0, max_care * 10 + 1, 1), axes.flatten()):
        care = i/10
        sns.distplot(df[f'care={care}'], ax=ax,
                    bins=len(set(df[f'care={care}'])), kde=False)
        ax.set(title=f'care = {care}', xlabel='stability',
                color='green', ylabel='frequency')
        ax.set_xlim([min, max])

    plt.show()

def comparing_test(protein, it_random=0, it_greedy=0, care_greedy=0,
        it_chunky=0, care_chunky=0, it_forward=0, care_forward=0):
    ''' Compares the different algorithms in a density histogram. '''

    # the random algorithm
    df_random = pd.DataFrame()
    stabilities = []
    for i in range(it_random):
        generate_path(protein, 'random')
        stabilities.append(abs(protein.stability))
    stabilities.sort()
    dict_stability = {'random': stabilities}
    df_random = df_random.assign(**dict_stability)

    # the greedy algorithm
    df_greedy = pd.DataFrame()
    stabilities = []
    for i in range(it_greedy):
        generate_path(protein, 'greedy', care=care_greedy)
        stabilities.append(abs(protein.stability))
    stabilities.sort()
    dict_stability = {'greedy': stabilities}
    df_greedy = df_greedy.assign(**dict_stability)

    # the chunky path algorithm
    df_chunky = pd.DataFrame()
    stabilities = []
    for i in range(it_chunky):
        generate_path(protein, 'chunky path', care=care_chunky)
        stabilities.append(abs(protein.stability))
    stabilities.sort()
    dict_stability = {'chunky': stabilities}
    df_chunky = df_chunky.assign(**dict_stability)

    # the foward search algorithm
    df_forward = pd.DataFrame()
    stabilities = []
    for i in range(it_forward):
        generate_path(protein, 'forward search', care=care_forward)
        stabilities.append(abs(protein.stability))
    stabilities.sort()
    dict_stability = {'forward': stabilities}
    df_forward = df_forward.assign(**dict_stability)

    # get best solution
    if it_greedy > 0:
        best_greedy = int(df_greedy.iloc[-1])
    else:
        best_greedy = 0
    if it_chunky > 0:
        best_chunky = int(df_chunky.iloc[-1])
    else:
        best_chunky = 0
    if it_random > 0:
        best_random = int(df_random.iloc[-1])
    else:
        best_random = 0
    if it_forward > 0:
        best_forward = int(df_forward.iloc[-1])
    else:
        best_forward = 0

    if (
            best_random > best_greedy and best_random > best_chunky
            and best_random > best_forward
        ):
        best_solution = best_random
        algorithm = 'Random'
    elif (
            best_greedy > best_random and best_greedy > best_chunky
            and best_greedy > best_forward
        ):
        best_solution = best_greedy
        algorithm = 'Greedy'
    elif (
            best_forward > best_random and best_forward > best_greedy \
            and best_forward > best_chunky
        ):
        best_solution = best_forward
        algorithm = 'Forward Search'
    else:
        best_solution = best_chunky
        algorithm = 'Chunky Path'

    sns.set()
    plt.figure(figsize=(16,10), dpi= 80)
    sns.distplot(df_random["random"], color="orange",
        bins = range(best_solution), label=f'Random', kde=False, norm_hist=True)
    sns.distplot(df_greedy["greedy"], color="red",
        bins = range(best_solution), label=f'Greedy, care={care_greedy}',
        kde=False, norm_hist=True)
    sns.distplot(df_chunky["chunky"], color="green",
        bins = range(best_solution),label=f'Chunky Path, care={care_chunky}',
        kde=False, norm_hist=True)
    sns.distplot(df_forward["forward"], color="deeppink",
        bins = range(best_solution),label=f'Forward Search, \
        care={care_forward}', kde=False, norm_hist=True)

    plt.title(f'Density Plot of algorithms, best solution={best_solution} \
        from {algorithm}', fontsize=22)
    plt.xlabel('Absolute Value of Stability')
    plt.ylabel('Density')
    plt.legend()
    plt.show()


def forward_depth_test(protein, minutes, depth_range):
    '''
    Plots a density plot with different depths of the forward search algorithm.
    '''

    # generate data
    stability_lists = []
    for depth in depth_range:
        stabilities = []
        # do the test for a specific period per depth
        t_end = time.time() + int(60 * minutes)
        while time.time() < t_end:
            generate_path(protein, 'forward search', depth=depth)
            stabilities.append(abs(protein.stability))

        stabilities.sort()
        stability_lists.append(stabilities)

        # used to see how much data is generated per time session
        print(len(stabilities))

    sns.set()
    sns.set_palette('bright')
    plt.figure(figsize=(18,10), dpi= 80)
    best_stability = 0
    count = 0
    for depth in depth_range:
        # plot all data in the stability lists
        data = stability_lists[count]
        if best_stability <= data[-1]:
            best_stability = data[-1]
            best_depth = depth_range[count]
        sns.distplot(data, bins = range(best_stability + 1),
            label=f'depth={depth}', kde=False, norm_hist=True)
        count += 1

    plt.title(f'Density Plot of Forward Search depths | best: \
        depth={best_depth}, value={best_stability}', fontsize=22)
    plt.xlabel('Absolute Value of Stability')
    plt.ylabel('Density')
    plt.legend()
    plt.show()


def chunk_size_test(protein, minutes, chunk_range, care=0):
    ''' Test the different kind of depth from Chunky Path algorithm. '''

    stability_lists = []
    for size in chunk_range:
        stabilities = []
        # do the test for a specific period per chunk size
        t_end = time.time() + int(60 * minutes)
        while time.time() < t_end:
            generate_path(protein, 'chunky path', chunk_size=size, care=care)
            stabilities.append(abs(protein.stability))

        stabilities.sort()
        stability_lists.append(stabilities)

        # used to see how much data is generated per time session
        print(len(stabilities))

    sns.set()
    sns.set_palette('bright')
    plt.figure(figsize=(18,10), dpi= 80)
    best_stability = 0
    count = 0
    for size in chunk_range:
        # plot all data in the stability lists
        data = stability_lists[count]
        if best_stability <= data[-1]:
            best_stability = data[-1]
            best_size = chunk_range[count]
        sns.distplot(data, bins = range(best_stability + 1),
            label=f'chunk size={size}', kde=False, norm_hist=True)
        count += 1

    plt.title(f'Density Plot of different chunk sizes | best: \
        size={best_size}, value={best_stability}', fontsize=22)
    plt.xlabel('Absolute Value of Stability')
    plt.ylabel('Density')
    plt.legend()
    plt.show()
