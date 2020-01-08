import random
from protein_class import Protein
import numpy as np
import matplotlib.pyplot as plt

protein = Protein("HHPHHHPH")
configs = []
max_duplicates = 100000

max_iter = 100000

def get_separating_iterations():
    # get number of generated states between non-duplicate states
    
    separating_iterations = []
    count = 0
    duplicate_count = 0
    
    for i in range(max_iter):
        while duplicate_count < max_duplicates:
            config = protein.generate_random_path(return_stability=False)
            if config not in configs:
                configs.append(config)
                separating_iterations.append(count)
                count = 0
            else:
                count += 1
                duplicate_count += 1
        return separating_iterations
        

if __name__ == "__main__":
    plt.plot(get_separating_iterations())
    plt.show()
