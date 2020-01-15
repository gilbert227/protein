import sys

sys.path.append('../')


from code.helpers.navigator import get_step_options, get_added_stability

from random import choice
import time

protein_string = input("What is the Protein string: ")
iterations_input = int(input("How many iterations (integer): "))
strategy = input("Which strategy (g for greedy or r for random): ")
minimum_stability = int(input("What is the minimum stability (give in negative values): "))


iterations = iterations_input
protein = Protein(protein_string)

start = time.time()

for i in range(iterations):
    generate_greedy_path(protein)
    if protein.stability < minimum_stability:
        print(protein.path)
        print(protein.stability)

end = time.time()

print(end - start)
