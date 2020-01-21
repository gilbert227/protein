from code.classes.protein import Protein
from code.algorithms.greedy_path import generate_greedy_path
from code.algorithms.random_path import generate_random_path
from code.algorithms.chunky_path import generate_chunky_path
from random import choice
import time
import operator

def speedtest(protein, strategy, minimum_stability, default = "y", iterations = 100, greed = 1, care = 0, chunk_size = 6, chunk_iterations = 100, step_strategy = "g"):

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
            print({protein})
            print()

            counter += 1

    end = time.time()
    print(f"Amount of results: {counter}")
    print(f"Time passed: {end - start}")
