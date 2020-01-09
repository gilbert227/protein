import random
import time
import operator
from protein_class import Protein

iterations = 100
protein = Protein("HPHHPHPH")

start = time.time()
for i in range(iterations):
    path = protein.generate_path('random')
    print(path)

end = time.time()
print(end - start)
