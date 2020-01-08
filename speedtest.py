import random
import time
from protein_class import Protein

iterations = 100000
protein = Protein("HHPHPHPHPHHHHPHPPPHPPPHPPPPHPPPHPPPHPHHHHPHPHPHPHH")

start = time.time()
for i in range(iterations):
    protein.generate_random_path()

end = time.time()
print(end - start)
