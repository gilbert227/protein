from code.helpers.navigator import get_step_options, get_added_stability
from code.classes.protein import Protein
from code.algorithms.random_path import *
from random import choice
import copy
import math

def change_path(protein):
    '''
    algorithm that changes a generated path
    '''
    print(protein.path)
