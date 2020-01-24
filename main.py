import matplotlib.pyplot as plt
from code.algorithms.greedy_path import generate_greedy_path
from code.algorithms.random_path import generate_random_path
from code.algorithms.chunky_path import generate_chunky_path
from code.algorithms.forward_search import forward_search
from code.helpers.navigator import *
from code.analysis.stats import *
from code.analysis.speedtest import speedtest
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

# promt for 3D
print("Do you want to use 3D? (y for yes) ")
while True:
    dimension3 = input("")
    if dimension3:
        print()
        break

# create protein class
if dimension3 == "y":
    protein = Protein(protein_string, dim3=True)
else:
    protein = Protein(protein_string)

print("What algorithm do you want to perform on this protein?")
print("Insert r for random, g for greedy, c for chunky path and f for forward search.")

while True:
    algorithm = input("")
    if algorithm == "r" or algorithm == "g" or algorithm == "c" or algorithm == "f":
        print("You have chosen.")
        print()
        break

print("Do you want use default values for input arguments and run a single time? (y for default)")
default = input("")
print()

# run the chosen algorithm a single time with default values
if default == "y":
    if algorithm == "r":
        generate_random_path(protein)
    elif algorithm == "g":
        generate_greedy_path(protein)
    elif algorithm == "c":
        generate_chunky_path(protein)
    elif algorithm == "f":
        forward_search(protein)

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

# prompt for specific variables, according to the chosen strategy
else:
    print("Please insert the following details with care.")

    print("What is the amount of iterations? (positive integer): ")
    while True:
        amount = int(input(""))
        if amount > 0:
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


    if algorithm == "f":
        print("What is the depth?")
        while True:
            depth = int(input(""))
            if depth:
                break

    # ask user what to do with the variables he has given
    while True:
        print()
        print("What would you like to do?")
        print("Type speedtest to do a speedtest with your input, it will print proteins with values less than the minimum stability you have given.")
        print("Type best to find the best generated path with the input you have provided.")
        print("Type change to alter your variables. Note that this implies that you have to change everything up to the algorithm")
        print("Type quit to quit the program.")
        action = input("")
        print()

        if action == "speedtest" or action == "best" or action == "histogram" or action == "change" or action == "quit":
            print("Understood.")
        else:
            print("Instructions unclear.")

        print()

        if algorithm == "r":
            if action == "speedtest":
                print("How many minutes do you want to run the algorithm? (formula uses: input * 60 seconds)")
                while True:
                    minutes = float(input(""))
                    if minutes:
                        break

                speedtest(protein, "random", minutes=minutes)

            elif action == "best":
                get_best_config(protein, "random", amount)
                print(protein)
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

        elif algorithm == "g":
            if action == "speedtest":
                print("How many minutes do you want to run the algorithm? (formula uses: input * 60 seconds)")
                while True:
                    minutes = float(input(""))
                    if minutes:
                        break
                speedtest(protein, "greedy", minutes=minutes, greed=greed, care=care)

            elif action == "best":
                get_best_config(protein, "greedy", amount, greed=greed, care=care)
                print(protein)
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

        elif algorithm == "c":
            if action == "speedtest":
                print("How many minutes do you want to run the algorithm? (formula uses: input * 60 seconds)")
                while True:
                    minutes = float(input(""))
                    if minutes:
                        break

                speedtest(protein, "chunky path", minutes=minutes, care=care, chunk_size=chunk_size, chunk_iterations=chunk_iterations, step_strategy="g")

            elif action == "best":
                get_best_config(protein, "chunky path", amount, care=care, chunk_size=chunk_size, chunk_iterations=chunk_iterations, step_strategy=step_strategy)
                print(protein)
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

        elif algorithm == "f":
            if action == "speedtest":
                print("How many minutes do you want to run the algorithm? (formula uses: input * 60 seconds)")
                while True:
                    minutes = float(input(""))
                    if minutes:
                        break

                speedtest(protein, "forward search", minutes=minutes, depth=depth)

            elif action == "best":
                get_best_config(protein, "forward search", amount, depth=depth)
                print(protein)
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

        if action == "change":
            print("What algorithm do you want to perform on this protein?")
            print("Insert r for random, g for greedy, c for chunky path of f for forward search.")

            while True:
                algorithm = input("")
                if algorithm == "r" or algorithm == "g" or algorithm == "c" or algorithm == "f":
                    print("You have chosen.")
                    print()
                    break

            print("What is the amount of iterations? (positive integer): ")
            while True:
                amount = int(input(""))
                if amount > 0:
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

                print("What single step strategy do you want to use? (r for random, g for greedy): ")
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

            if algorithm == "f":
                print("What is the depth?")
                while True:
                    depth = int(input(""))
                    if depth:
                        break

        if action == "quit":
            print()
            print("I'll be back.")
            print()
            break
