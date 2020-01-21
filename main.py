import matplotlib.pyplot as plt
from code.algorithms.greedy_path import generate_greedy_path
from code.algorithms.random_path import generate_random_path
from code.algorithms.chunky_path import generate_chunky_path
from code.helpers.navigator import *
from code.analysis.stats import *
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

print("Do you want to use 3D? (y for yes) ")
while True:
    dimension3 = input("")
    if dimension3:
        print()
        break

if dimension3 == "y":
    protein = Protein(protein_string, dim3=True)
else:
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
print()

if default == "y":
    if algorithm == "r":
        generate_random_path(protein)
    elif algorithm == "g":
        generate_greedy_path(protein)
    elif algorithm == "c":
        generate_chunky_path(protein)

    print(protein)
    print()

    print("Type plot to plot this path, or type csv to save the results in a csv file called protein.csv, or anything else to quit.")
    while True:
        action_best = input("")

        if action_best == "plot":
            plot_path(protein)
        elif action_best == "csv":
            csv_compiler(protein)
        else:
            break

else:
    print("Please insert the following details with care.")

    print("What is the amount of iterations? (positive integer): ")
    while True:
        amount = int(input(""))
        if amount > 0:
            break

    print("What is the minimum required stability to print to path? (integer, used for speedtest)")
    if amount > 1:
        while True:
            minimum_stability = int(input(""))
            if minimum_stability:
                break

    if algorithm == "g":
        print("What is the greed factor? (float): ")
        while True:
            greed = float(input(""))
            if greed:
                break

        print("Do you want to want the care factor to be 0? (y for yes)")
        use_care = input("")
        if use_care == "y":
            care = 0
        else:
            print("Please give the care factor value now (float): ")
            while True:
                care = float(input(""))
                if care:
                    break


    if algorithm == "c":
        print("What is the chunk size? (positive integer): ")
        while True:
            chunk_size = int(input(""))
            if chunk_size > 0:
                break

        print("How many chunk iterations? (positive integer): ")
        while True:
            chunk_iterations = int(input(""))
            if chunk_iterations > 0:
                break

        print("What step strategy? (r for random, g for greedy): ")
        while True:
            step_strategy = input("")
            if step_strategy == "r" or step_strategy == "g":
                break

        if step_strategy == "g":
            print("Do you want to want the care factor to be 0? (y for yes)")
            use_care = input("")
            if use_care == "y":
                care = 0
            else:
                print("Please give the care factor value now (float): ")
                while True:
                    care = float(input(""))
                    if care:
                        break
        else:
            care = 0

    while True:
        print()
        print("What would you like to do?")
        print("Type speedtest to do a speedtest with your input, it will print proteins with values less than the minimum stability you have given.")
        print("Type best to find the best generated path with the input you have provided.")
        print("Type histogram to create a histogram of the stabilities found.")
        action = input("")
        print()

        if action == "speedtest" or action == "best" or action == "histogram":
            print("Understood.")
        else:
            print("Instructions unclear.")

        print()

        if algorithm == "r":
            if action == "speedtest":
                speedtest(protein, "r", minimum_stability, iterations=amount)
            elif action == "best":
                best = get_best_config(protein, "random", amount)
                print(best)
                print()

                print("Type plot to plot this path, or type csv to save the results in a csv file called protein.csv, or anything else to continue with something else.")
                while True:
                    action_best = input("")

                    if action_best == "plot":
                        plot_path(protein)
                    elif action_best == "csv":
                        csv_compiler(protein)
                    else:
                        break

            elif action == "histogram":
                get_stability_histogram(protein, "random", amount)

        elif algorithm == "g":
            if action == "speedtest":
                speedtest(protein, "g", minimum_stability, iterations=amount, greed=greed, care=care)
            elif action == "best":
                best = get_best_config(protein, "greedy", amount, greed=greed, care=care)
                print(best)
                print()

                print("Type plot to plot this path, or type csv to save the results in a csv file called protein.csv, or anything else to continue with something else.")
                while True:
                    action_best = input("")

                    if action_best == "plot":
                        plot_path(protein)
                    elif action_best == "csv":
                        csv_compiler(protein)
                    else:
                        break

            elif action == "histogram":
                get_stability_histogram(protein, "greedy", amount, greed=greed, care=care)

        elif algorithm == "c":
            if action == "speedtest":
                speedtest(protein, "c", minimum_stability, iterations=amount, care=care, chunk_size=chunk_size, chunk_iterations=chunk_iterations, step_strategy="g")
            elif action == "best":
                best = get_best_config(protein, "chunky path", amount, care=care, chunk_size=chunk_size, chunk_iterations=chunk_iterations, step_strategy=step_strategy)
                print(best)
                print()

                print("Type plot to plot this path, or type csv to save the results in a csv file called protein.csv, or anything else to continue with something else.")
                while True:
                    action_best = input("")

                    if action_best == "plot":
                        plot_path(protein)
                    elif action_best == "csv":
                        csv_compiler(protein)
                    else:
                        break

            elif action == "histogram":
                get_stability_histogram(protein, "chunky path", amount, care=care, chunk_size=chunk_size, chunk_iterations=chunk_iterations, step_strategy=step_strategy)
