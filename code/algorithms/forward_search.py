''' 
forward_search.py

search of stable configuration of protein by looking ahead. Chooses the best stability
with the least number of steps (within the user-defined depth) and updates the protein's
path accordingly. Repeats this procedure until the full protein is generated
'''
from code.helpers.navigator import get_step_options
from copy import deepcopy
from random import choice

def forward_search(protein, depth=5, retry=True):
    ''' 
    looks for the best score with the least steps within the user-defined depth
    
    if dead-ends are generated repeatedly, calls itself with lowered depth and retry set to False
    
    manipulates path attribute of given Protein object and returns the effective depth in case this
    differs from the user-defined depth (for checking purposes)
    '''
    
    protein.initialize_path()

    # check if path is fully generated
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
            return forward_search(protein, depth, retry=False)
    return depth

def look_ahead(protein, depth, paths):
    ''' 
    recursive function generating all paths (daughters) to the input Protein object (parent)
    
    stores all the resulting Protein objects in a list that is passed down through the recursive process
    '''
    for option in get_step_options(protein):

        # make temporary copy of protein to manipulate
        temp_protein = deepcopy(protein)

        # add option to the temporary copy
        temp_protein.add_step(temp_protein.sequence[len(temp_protein.path)], option)
        
        # add temporary copy to the paths list
        paths.append((temp_protein.stability, len(temp_protein.path), temp_protein))
        
        # function is called recursively with reduced depth until search depth is reached (depth == 0)
        if depth > 0 and len(temp_protein.path) < len(temp_protein.sequence):
            # generate all daughters of temporary protein until the required depth
            look_ahead(temp_protein, depth - 1, paths)
