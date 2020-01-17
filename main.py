import matplotlib.pyplot as plt
from code.algorithms.greedy_path import generate_greedy_path
from code.algorithms.random_path import generate_random_path
from code.algorithms.chunky_path import generate_chunky_path
from code.helpers.navigator import *
from code.analysis.stats import *
from code.analysis.speedtest import *
from code.classes.protein import Protein

print("Welcome to the User Interface!")
print()

print("Please insert the protein string with which you want to work:")

# ask for protein sequence
while True:
    protein_string = input("")
    if protein_string:
        print(f"Your string is: {protein_string}.")
        print()
        break

protein = Protein(protein_string)

print("What algorithm do you want to perform on this protein?")
print("Insert r for random, g for greedy and c for chunky path.")

while True:
    algorithm = input("")
    if algorithm == "r" or algorithm == "g" or algorithm == "c":
        print("You have chosen.")
        print()
        break

print("Do you want use default values and run a single time? (y for default)")
default = input("")

if default == "y":
    if algorithm == "r":
        generate_random_path(protein)
    elif algorithm == "g":
        generate_greedy_path(protein)
    elif algorithm == "r":
        generate_random_path(protein)

    print(protein)

print("Please insert the following details with care.")

while True:
    amount = int(input("How many times do you want to run the algorithm? (positive integer)"))
    if amount > 0:
        break
