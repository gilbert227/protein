import random
from protein_class import Protein
import numpy as np
import matplotlib.pyplot as plt

protein = Protein("HCPHPHPHCHHHHPCCPPHPPPHPPPPCPPPHPPPHPHHHHCHPHPHPHH")
configs = []
max_separating_duplicates = 30

def get_separating_duplicates():
    # get number of generated states between non-duplicate states

    separating_duplications = []
    duplicate_count = 0

    while duplicate_count < max_separating_duplicates:
        config = protein.generate_path("greedy", return_stability=False)
        if config not in configs:
            configs.append(config)
            separating_duplications.append(duplicate_count)
            duplicate_count = 0
        else:
            duplicate_count += 1
    return separating_duplications


if __name__ == "__main__":
    plt.plot(get_separating_duplicates())
    plt.show()
