from code.analysis.stats import generate_path, speedtest

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.lines import Line2D
import seaborn as sns
from copy import deepcopy
import numpy as np
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
            ax.scatter(x, y, z, s=140, marker='o', linewidths=1, color=amino_colors[amino], )
        else:
            plt.scatter(x, y, s=160, marker='o', linewidths=1, color=amino_colors[amino], )

    if protein.dim3:
        ax.plot(x_positions, y_positions, z_positions, 'ko-', alpha=0.4, ms=1)
    else:
        plt.plot(x_positions, y_positions, 'ko-', alpha=0.4, ms=1)

    plt.title(f"stability: {protein.stability}")

    custom_lines = [Line2D([0], [0], marker='o', markersize=10, color='blue', label='P', lw=0),
                    Line2D([0], [0], marker='o', markersize=10, color='red', label='H', lw=0),
                    Line2D([0], [0], marker='o', markersize=10, color='green', label='C', lw=0)]

    plt.legend(handles = custom_lines)

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

    sns.set()
    fig, axes = plt.subplots(nrows=3, ncols=4)
    fig.subplots_adjust(hspace=0.5)
    fig.suptitle(f'Distribution of different care values, best for {best_care} with algorithm {strategy}')

    sns.set_palette('pastel')
    for i, ax in zip(np.arange(0, 12, 1), axes.flatten()):
        care = i/10
        sns.distplot(df[f'care={care}'], ax=ax, bins=len(set(df[f'care={care}'])), color="green", kde=False)
        ax.set(title=f'care = {care}', xlabel='stability', ylabel='frequency')
        ax.set_xlim([min, max])

    plt.show()

def comparing_test(protein, it_random=0, it_greedy=0, care_greedy=0, it_chunky=0, care_chunky=0, it_forward=0, care_forward=0):

    # random
    df_random = pd.DataFrame()
    stabilities = []
    for i in range(it_random):
        generate_path(protein, 'random')
        stabilities.append(abs(protein.stability))

    stabilities.sort()
    dict_stability = {'random': stabilities}

    df_random = df_random.assign(**dict_stability)


    # greedy
    df_greedy = pd.DataFrame()
    stabilities = []
    for i in range(it_greedy):
        generate_path(protein, 'greedy', care=care_greedy)
        stabilities.append(abs(protein.stability))

    stabilities.sort()
    dict_stability = {'greedy': stabilities}

    df_greedy = df_greedy.assign(**dict_stability)


    # chunky path
    df_chunky = pd.DataFrame()
    stabilities = []
    for i in range(it_chunky):
        generate_path(protein, 'chunky path', care=care_chunky)
        stabilities.append(abs(protein.stability))

    stabilities.sort()
    dict_stability = {'chunky': stabilities}
    df_chunky = df_chunky.assign(**dict_stability)

    # foward search
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

    if best_random > best_greedy and best_random > best_chunky and best_random > best_forward:
        best_solution = best_random
        algorithm = 'Random'
    elif best_greedy > best_random and best_greedy > best_chunky and best_greedy > best_forward:
        best_solution = best_greedy
        algorithm = 'Greedy'
    elif best_forward > best_random and best_forward > best_greedy and best_forward > best_chunky:
        best_solution = best_forward
        algorithm = 'Forward Search'
    else:
        best_solution = best_chunky
        algorithm = 'Chunky Path'

    # Draw Plot
    sns.set()
    plt.figure(figsize=(16,10), dpi= 80)
    sns.distplot(df_random["random"], color="orange", bins = range(best_solution), label=f'Random', kde=False, norm_hist=True)
    sns.distplot(df_greedy["greedy"], color="red",  bins = range(best_solution), label=f'Greedy, care={care_greedy}', kde=False, norm_hist=True)
    sns.distplot(df_chunky["chunky"], color="green", bins = range(best_solution),label=f'Chunky Path, care={care_chunky}', kde=False, norm_hist=True)
    sns.distplot(df_forward["forward"], color="deeppink", bins = range(best_solution),label=f'Forward Search, care={care_forward}', kde=False, norm_hist=True)

    # decoration
    plt.title(f'Density Plot of algorithms, best solution={best_solution} from {algorithm}', fontsize=22)
    plt.xlabel('Absolute Value of Stability')
    plt.ylabel('Density')
    plt.legend()
    plt.show()


def speed_test_plot(protein, time):

    results = speedtest(protein, 'random', minutes=time)
    df = pd.DataFrame.from_dict(results, orient='index')
    df = df.sort_index()
    df = df.reindex(list(range(df.index.min(),df.index.max()+1)),fill_value=0)
    print(df)

    sns.set()
    plt.figure(figsize=(16,10), dpi= 80)
    plt.hist(df[0], bins=df.index[-1], color="orange")

    plt.legend()
    plt.show()

def forward_depth_test(protein, minutes, depth_range):

    # generate data
    stability_lists = []
    for depth in depth_range:
        stabilities = []
        t_end = time.time() + int(60 * minutes)
        while time.time() < t_end:
            generate_path(protein, 'forward search', depth=depth)
            stabilities.append(abs(protein.stability))

        stabilities.sort()
        stability_lists.append(stabilities)

        print(len(stabilities))

    # draw plot
    sns.set()
    sns.set_palette('bright')
    plt.figure(figsize=(18,10), dpi= 80)
    best_stability = 0
    count = 0
    for depth in depth_range:
        data = stability_lists[count]
        if best_stability <= data[-1]:
            best_stability = data[-1]
            best_depth = depth_range[count]
        sns.distplot(data, bins = range(best_stability + 1), label=f'depth={depth}', kde=False, norm_hist=True)
        count += 1

    plt.title(f'Density Plot of Forward Search depths | best: depth={best_depth}, value={best_stability}', fontsize=22)
    plt.xlabel('Absolute Value of Stability')
    plt.ylabel('Density')
    plt.legend()
    plt.show()


def chunky_path_care(protein, iterations, max_care, max_chunk_size):

    # get dataframe for different cares
    column_names = ['stability', 'care', 'size']
    df = pd.DataFrame(columns = column_names)

    for chunk_size in range(max_chunk_size + 1):
        stabilities_care = []
        for i in range(int(max_care * 10 + 1)):
            stabilities = []
            care = i / 10
            for i in range(iterations):
                generate_path(protein, 'chunky path', care=care)
                dic = {'stability': [protein.stability], 'care': [care], 'size': [chunk_size]}
                df_temp = pd.DataFrame(data=dic)
                df = pd.concat([df, df_temp])



    # fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')

    # ax.scatter(list(df['size']), list(df['care']), list(df['stability']), c='r', marker='o')

    # ax.set_xlabel('Size')
    # ax.set_ylabel('Care')
    # ax.set_zlabel('Stability')

    # plt.show()

    with sns.axes_style('white'):
        sns.jointplot(df['size'], df['care'], df['stability'], kind='hex')


def depth_forward_test(protein, iterations, max_depth=5, care=0):

    # foward search
    df_forward = pd.DataFrame()

    for depth in range(max_depth):
        stabilities = []
        for i in range(iterations):
            generate_path(protein, 'forward search', care=care, depth=depth)
            stabilities.append(protein.stability)

        stabilities.sort()
        dict_stability = {f'{depth}': stabilities}
        df_forward = df_forward.assign(**dict_stability)

    # best path
    best_value = int(df_forward.iloc[0].min())
    best_algorithm = int(df_forward.iloc[0].idxmin())

    # plot
    plt.figure(figsize=(16,10), dpi= 80)
    for depth in range(max_depth):
        sns.distplot(df_forward[f'{depth}'], label=f'Depth={depth}', kde=False, rug=True)

    # Decoration
    plt.title(f'Density Plot of different depths of Forward Search algorithm, best value={best_value} for depth={best_algorithm}', fontsize=22)
    plt.legend()
    plt.show()
