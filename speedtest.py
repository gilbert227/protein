import random
import time
import operator
from protein_class import Protein

protein_string = input("What is the Protein string: ")
iterations_input = int(input("How many iterations (integer): "))
strategy = input("Which strategy (greedy or random): ")
minimum_stability = int(input("What is the minimum stability (give in negative values): "))

iterations = iterations_input
protein = Protein(protein_string)



start = time.time()
counter = 0
for i in range(iterations):
    path = protein.generate_path(strategy)
    if path != None and path[1] < minimum_stability:
        print(path)
        counter += 1


end = time.time()
print(counter)
print(end - start)
