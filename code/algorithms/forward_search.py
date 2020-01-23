''' 
forward_search.py

search of stable configuration of protein by looking ahead
'''
from code.helpers.navigator import get_step_options
from copy import deepcopy
from random import choice

def forward_search(protein, depth=5, care=0):
    protein.initialize_path()
    while len(protein.path) < len(protein.sequence):
        paths = []
        look_ahead(protein, depth, paths, care)
        try:
            # catch exception if path remains empty after look_ahead
            best_score = min([temp_protein.path_quality for temp_protein in paths])
            quickest = min([len(temp_protein.path) for temp_protein in paths if temp_protein.path_quality == best_score])
            protein = deepcopy(choice([temp_protein for temp_protein in paths if temp_protein.path_quality == best_score and len(temp_protein.path) == quickest]))
        except:
            # try again
            return forward_search(protein, depth, care)
    return protein

def look_ahead(protein, depth, paths, care):
    for option in get_step_options(protein):
        temp_protein = deepcopy(protein)
        temp_protein.add_step(temp_protein.sequence[len(temp_protein.path)], option, care)
        paths.append(temp_protein)
        if depth > 0 and len(temp_protein.path) < len(temp_protein.sequence):
            look_ahead(temp_protein, depth - 1, paths, care)

