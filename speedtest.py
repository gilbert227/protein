import random
import time
import operator
from protein_class import Protein

iterations = 10
protein = Protein("CHHCPH")

start = time.time()
for i in range(iterations):
    path = protein.generate_path('random')
    if path != None and path[1] < 1:
        print(path)

end = time.time()
print(end - start)
