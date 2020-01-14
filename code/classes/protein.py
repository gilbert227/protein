from helpers import navigator

class Protein:
    def __init__(self, sequence):
        self.sequence = sequence
        self.path = []
        self.amino_positions = {} 
        self.stability = 0
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

    def add_step(
    def __str__(self):
        print(f"path:{self.path}, stability:{self.stability}")
