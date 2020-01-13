import random
from protein_class import Protein
import numpy as np
import matplotlib.pyplot as plt
from copy import deepcopy

class ProteinStats:
    ''' methods to obtain statistical data from protein '''

    def get_new_config(self, protein, strategy, configs=[], max_iterations=10000):
        # returns number of states found before duplicate is produced:
        for i in range(max_iterations):
            config = protein.generate_path(strategy, return_stability=False)
            if config not in configs:
                return (i, config, True)
        return (None, None, False)


    def get_separating_duplicates(self, protein, strategy, duplication_threshold):
        # get number of generated states between non-duplicate states
        configs = []
        separating_duplicates = []
        found = True

        while found:
            separation, config, found = self.get_new_config(protein, strategy, configs, duplication_threshold)
            separating_duplicates.append(separation)
            configs.append(config)
        separating_duplicates.pop()
        return separating_duplicates, len(separating_duplicates)

    
    def get_best_configuration(self, protein, strategy, iterations):
        return protein.get_best_path(iterations, strategy)

    def plot(self, path, score=None):
        x_positions = []
        y_positions = []
        point_markers = []
        for point in path.values():
            x_position = point[1][0]
            y_position = point[1][1]
            amino = point[0]
            if amino == 'H':
                amino_color = 'blue'
            elif amino == 'C':
                amino_color = 'red'
            else:
                amino_color = 'black'
            x_positions.append(x_position)
            y_positions.append(y_position)

            plt.text(x_position, y_position, amino, horizontalalignment='center', verticalalignment='center', color=amino_color)
        if score:
            plt.title(f"stability: {score}")
        plt.plot(x_positions, y_positions, 'ko-', markerfacecolor='white', markersize=15)
        plt.axis('off')
        plt.show()
    

if __name__ == "__main__":
    protein = Protein("HHPHHHPH")
    #path = ProteinStats().get_best_configuration(protein, "greedy", 100000)
    #print(path)
    #ProteinStats().plot(path[0][0], score=path[0][1])
    plt.plot(ProteinStats().get_separating_duplicates(protein, "random", 10000)[0])
    plt.show()
