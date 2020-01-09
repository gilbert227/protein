import random
import time
import operator
from protein_class import Protein

iterations = 100000
protein = Protein("HHPHPHPHPHHHHPHPPPHPPPHPPPPHPPPHPPPHPHHHHPHPHPHPHH")

start = time.time()
for i in range(iterations):
    path = protein.generate_path('greedy')
    if path != None and path[1] < -15:
        print(path)

end = time.time()
print(end - start)
