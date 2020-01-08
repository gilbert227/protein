import random
import time
from protein_class import Protein

iterations = 1
protein = Protein("HHPHHHPH")

paths = []
start = time.time()
for i in range(iterations):
    path = protein.generate_random_path()
    paths.append(path)

end = time.time()
print(end - start)
