from classes.protein import Protein
from algorithms.greedy_path import generate_greedy_path
from algorithms.random_path import generate_random_path
from random import choice
import time
import operator

protein_string = input("What is the Protein string: ")
iterations_input = int(input("How many iterations (integer): "))
strategy = input("Which strategy (g for greedy, r for random): ")
minimum_stability = int(input("What is the minimum stability (give in negative values): "))

iterations = iterations_input
protein = Protein(protein_string)

start = time.time()
counter = 0
for i in range(iterations):
    if strategy == "g":
        generate_greedy_path(protein)
    else:
        generate_random_path(protein)

    if protein.stability < minimum_stability:
        print(protein)

        counter += 1

end = time.time()
print(counter)
print(end - start)
