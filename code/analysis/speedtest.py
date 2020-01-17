from code.classes.protein import Protein
from code.algorithms.greedy_path import generate_greedy_path
from code.algorithms.random_path import generate_random_path
from code.algorithms.chunky_path import generate_chunky_path
from random import choice
import time
import operator

def speedtest():
    protein_string = input("What is the Protein string: ")
    iterations_input = int(input("How many iterations (integer): "))
    strategy = input("Which strategy (g for greedy, c for chunky path, r for random): ")
    if strategy == "c":
        default = input("Do you want to use default values(y for yes): ")
        if default != "y":
            n = int(input("What is n (positive integer): "))
            chunk_iterations = int(input("How many chunk iterations (positive integer): "))
            step_strategy = input("What step strategy (random by default, give another letter for greedy): ")
            if step_strategy != "random":
                care = float(input("What is the care(should be a float): "))
    minimum_stability = int(input("What is the minimum stability (give in negative values): "))

    iterations = iterations_input
    protein = Protein(protein_string)

    start = time.time()
    counter = 0
    for i in range(iterations):
        if strategy == "g":
            generate_greedy_path(protein)
        elif strategy == "c":
            if default == "y":
                generate_chunky_path(protein)
            else:
                generate_chunky_path(protein, n, chunk_iterations, step_strategy, care)
        else:
            generate_random_path(protein)

        if protein.stability < minimum_stability:
            print(protein)

            counter += 1

    end = time.time()
    print(counter)
    print(end - start)
