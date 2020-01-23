from code.helpers.navigator import get_added_stability
import copy

class Protein:
    def __init__(self, sequence, dim3=False):
        self.sequence = sequence
        self.dim3 = dim3
        self.path = []
        self.amino_positions = {}
        self.stability = 0
        self.path_quality = 0

        # Symmetric keeps track of whether the full path is on the y-axis. If true, only
        # steps along the y-axis and in the positive x-direction will be considered.
        # This excludes mirror images with respect to the y-axis.
        self.symmetric = True

        self.initialize_path()

        self.bond_stabilities = {
            "P": {"P": (0, 0), "H": (0, 2), "C": (0, 3)},
            "H": {"P": (0, 2), "H": (-1, 0), "C": (-1, 1)},
            "C": {"P": (0, 3), "H": (-1, 1), "C": (-5, 0)},
        }

    def initialize_path(self):
        self.reset()

        if not self.dim3:
            for i, amino in enumerate(self.sequence[:2]):
                self.path.append([amino, (0, i)])
                self.amino_positions[amino].append((0, i))
        else:
            for i, amino in enumerate(self.sequence[:2]):
                self.path.append([amino, (0, 0, i)])
                self.amino_positions[amino].append((0, 0, i))

    def reset(self):
        self.path = []
        self.amino_positions = {
            "P":[],
            "H":[],
            "C":[],
        }
        self.stability = 0
        self.symmetric = True

    def add_step(self, amino, step, care=0):
        ''' adds step to path and updates relevant attributes '''
        if self.symmetric and ((not self.dim3 and step[0] != 0) or (self.dim3 and (step[0] !=0 or step[1] != 0))):
            # path no longer coincides with vertical-axis, symmetric is now false
            self.symmetric = False
        
        added_stability, added_quality = get_added_stability(self, amino, step, care)
        self.stability += added_stability
        self.path_quality += added_quality

        self.amino_positions[amino].append(step)
        self.path.append([amino, step])

    def __str__(self):
        return f"path:{self.path}, stability:{self.stability}"
