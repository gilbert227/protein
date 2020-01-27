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

def compare_chunkies(protein, iterations, chunk_iterations=50, care=0, chunk_size1=4, chunk_size2=6, chunk_size3=8, chunk_size4=10):
    # chunky1
    df_chunk1 = pd.DataFrame()
    stabilities = []
    for i in range(iterations):
        generate_path(protein, 'chunky path', care=care, chunk_iterations=chunk_iterations, chunk_size=chunk_size1)
        stabilities.append(abs(protein.stability))

    stabilities.sort()
    dict_stability = {'chunk_size1': stabilities}

    df_chunk1 = df_chunk1.assign(**dict_stability)

    # chunky2
    df_chunk2 = pd.DataFrame()
    stabilities = []
    for i in range(iterations):
        generate_path(protein, 'chunky path', care=care, chunk_iterations=chunk_iterations, chunk_size=chunk_size2)
        stabilities.append(abs(protein.stability))

    stabilities.sort()
    dict_stability = {'chunk_size2': stabilities}

    df_chunk2 = df_chunk2.assign(**dict_stability)

    # chunky3
    df_chunk3 = pd.DataFrame()
    stabilities = []
    for i in range(iterations):
        generate_path(protein, 'chunky path', care=care, chunk_iterations=chunk_iterations, chunk_size=chunk_size3)
        stabilities.append(abs(protein.stability))

    stabilities.sort()
    dict_stability = {'chunk_size3': stabilities}

    df_chunk3 = df_chunk3.assign(**dict_stability)

    # chunky4
    df_chunk4 = pd.DataFrame()
    stabilities = []
    for i in range(iterations):
        generate_path(protein, 'chunky path', care=care, chunk_iterations=chunk_iterations, chunk_size=chunk_size4)
        stabilities.append(abs(protein.stability))

    stabilities.sort()
    dict_stability = {'chunk_size4': stabilities}

    df_chunk4 = df_chunk4.assign(**dict_stability)

    # get best solution
    best_chunk1 = int(df_chunk1.iloc[-1])
    best_chunk2 = int(df_chunk2.iloc[-1])
    best_chunk3 = int(df_chunk3.iloc[-1])
    best_chunk4 = int(df_chunk4.iloc[-1])

    best_solution = best_chunk3

    # Draw Plot
    sns.set()
    plt.figure(figsize=(16,10), dpi= 80)
    sns.distplot(df_chunk1["chunk_size1"], color="orange", bins = range(best_solution), label=f'n=4', kde=False, norm_hist=True)
    sns.distplot(df_chunk2["chunk_size2"], color="red",  bins = range(best_solution), label=f'n=6', kde=False, norm_hist=True)
    sns.distplot(df_chunk3["chunk_size3"], color="green", bins = range(best_solution),label=f'n=8', kde=False, norm_hist=True)
    sns.distplot(df_chunk4["chunk_size4"], color="deeppink", bins = range(best_solution),label=f'n=10', kde=False, norm_hist=True)

    # decoration
    plt.title(f'Density Plot of algorithms', fontsize=22)
    plt.xlabel('Absolute Value of Stability')
    plt.ylabel('Density')
    plt.legend()
    plt.show()
