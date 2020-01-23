''' 
forward_search.py

search of stable configuration of protein by looking ahead
'''
from code.helpers.navigator import get_step_options
from copy import deepcopy
from random import choice

def forward_search(protein, depth=5, retry=True):
    protein.initialize_path()
    while len(protein.path) < len(protein.sequence):
        paths = []
        look_ahead(protein, depth, paths)
        try:
            # catch exception if path remains empty after look_ahead (dead end)

            # filter most stable paths
            best_paths = [(length, protein) for stability, length, protein in paths if stability == min([stability for stability, length, protein in paths])]
            # filter shortest paths to best stability
            quickest_best_paths = [protein for length, protein in best_paths if length == min([length for length, protein in best_paths])]
            path_update = deepcopy(choice(quickest_best_paths))
            protein.__dict__ = path_update.__dict__.copy()
        except:
            # try again if dead end is reached, once with same depth, then one shallower
            if not retry:
                depth -= 1
            return forward_search(protein, depth - 1)
    return depth

def look_ahead(protein, depth, paths):
    for option in get_step_options(protein):
        temp_protein = deepcopy(protein)
        temp_protein.add_step(temp_protein.sequence[len(temp_protein.path)], option)
        paths.append((temp_protein.stability, len(temp_protein.path), temp_protein))
        if depth > 0 and len(temp_protein.path) < len(temp_protein.sequence):
            look_ahead(temp_protein, depth - 1, paths)
