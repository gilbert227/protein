from helpers.navigator import get_added_stability
import copy

class Protein:
    def __init__(self, sequence):
        self.sequence = sequence
        self.path = []
        self.amino_positions = {}
        self.stability = 0

        # Symmetric keeps track of whether the full path is on the y-axis. If true, only
        # steps along the y-axis and in the positive x-direction will be considered.
        # This excludes mirror images with respect to the y-axis.
        self.symmetric = True

        self.initialize_path()

        self.bond_stabilities = {
            "P": {"P": 0, "H":  0, "C":  0},
            "H": {"P": 0, "H": -1, "C": -1},
            "C": {"P": 0, "H": -1, "C": -5},
        }

    def initialize_path(self):
        self.reset()

        for i, amino in enumerate(self.sequence[:2]):
            self.path.append([amino, (0, i)])
            self.amino_positions[amino].append((0, i))

    def reset(self):
        self.path = []
        self.amino_positions = {
            "P":[],
            "H":[],
            "C":[],
        }
        self.stability = 0
        self.symmetric = True

    def add_step(self, amino, step):
        ''' adds step to path and updates relevant attributes '''
        if self.symmetric == True and step[1] != 0:
            # path no longer coincides with y-axis, symmetric is now false
            self.symmetric = False
        self.stability += get_added_stability(self, amino, step)
        self.amino_positions[amino].append(step)
        self.path.append([amino, step])

    def return_to_start(self, n, start_stability, start_amino_positions, start_symmetric):
        '''
        method to let the bread_first method return to its starting positions
        '''
        del self.path[-n:]
        self.stability = start_stability
        self.amino_positions = copy.deepcopy(start_amino_positions)
        self.symmetric = start_symmetric

    def add_chunk(self, best_path, n):
        for amino, step in best_path[-n:]:
            self.add_step(amino, step)


    def __str__(self):
        return f"path:{self.path}, stability:{self.stability}"
