# Code

In this map one can find all python code used for the project. The code is supposed to be used as package, and is divided in four sections.

## Classes
In the project, the protein sequence that needs to be folded is an object. As input arguments it takes the protein string and a Boolean value for using 3D. Usage:

```
protein = Protein("your_protein_string", dim3=True/False)
```

The protein class is very useful as it keeps track of the path and stability of a protein.

## Algorithms
In the map algorithms one can find all algorithms used to fold a protein string. There are four algorithms to be found in this map. They can all be run by a method in analysis/stats.py.

### Random
The first algorithm is a random algorithm which can be found in random_path.py. This algorithm randomly chooses coordinates to determine the new position in the protein path.
Usage:
```
>> generate_random_path(protein)
```
The path generated is saved in the protein object. This is the same for the other algorithms.

### Greedy
The second algorithm is a greedy algorithm which can be found in greedy_path.py. This algorithm will gather points as quick as possible. So it will choose for the option which gives the most points. This algorithm takes two input arguments, named care and Greedy. Care is the factor that gives a penalty for placing amino acids who cannot make points next to amino acids who do have potential to make points. For example, placing a P next to a C will result in a penalty. These factors can be found classes/protein.py.
# GREGORIUS GREED UITLEG
Usage:
```
>> generate_greedy_path(protein, greed=1, care=0)
```
By default, care is 0. Care should be a float between 0 and 1. Whereas greed is 1 by default, and should be a float between 0 and 1 as well.

### Chunky path
After that is an algorithm that is called chunky path, this algorithm divides a protein sequence in chunks of a given size and simulates this certain part of the sequence for a given number of times. It keeps track of the best path by using the number of stability points the path provides. After a chunk is determined to be the best, this whole chunk will be added to the final path. Note that the path in a chunk is made by using a random or greedy algorithm, depending on the users choice.
Usage:
```
>> generate_chunky_path(protein, chunk_size=6, iterations=50, step_strategy="greedy", care=0):
```
Where chunk_size is the size of the chunks, iterations is the number of times a chunk is made and step_strategy is the strategy for which the chunks will generate its individual steps. This argument should be either "greedy" or "random". If the step_strategy is greedy, the care factor will also play a role. This method is not compatible with the greed variable.

### Forward Search
# GREGORIUS LEG UIT
Forward search
Usage:
```
>> forward_search(protein, depth=5, retry=True)
```


## Helpers
In helpers/navigator.py one can find methods that are used to help determine the next coordinate in the path. Most of them are used for all algorithms. get_surrounding_coordinates returns all surrounding coordinates given the current coordinate, depending on 3D. get_step_options removes the already occupied coordinates from the surrounding coordinates and checks for symmetric properties in the vertical axis. get_added_stability calculates the extra stability a new step provides. make_up_your_mind is only used for the greedy algorithm, where it determines ...
# Kan gregor deze uitleg even afmaken?

## Analysis
In this map one can find the methods to generate results and analyze the case. There are multiple files with methods.

### stats.py:
This file contains the methods:

```
>> generate_path(protein, strategy, greed=1, care=0, chunk_size=6, chunk_iterations=100, step_strategy="greedy", depth=3)
```
This method is used to have a single method that can run all algorithms. This method also requires an input argument for which algorithm to use, called strategy. This should take the values: "random", "greedy", "chunky path" or "forward search". The rest of the input arguments are all the same as the input arguments of the algorithms.

```
>> get_next_unique_config(protein, strategy, configs=[], max_iterations=10000, greed=1, care=0, chunk_size=6, chunk_iterations=100, step_strategy="greedy")
```

#GREGORIUS LEG UIT

```
>> get_separating_duplicates(protein, strategy, duplication_threshold, greed=1, care=0, chunk_size=6, chunk_iterations=100, step_strategy="greedy", depth=3)
```
#GREGORIUS LEG UIT

```
>> get_best_config(protein, strategy, iterations, greed=1, care=0, chunk_size=6, chunk_iterations=100, step_strategy="greedy", depth=3)
```
This method is used to return a best configuration within the given number of iterations. The method uses the same input as generate_path(), but has an extra argument called iterations. This is the number of times the user wants to generate a single path.

```
>> speedtest
```

### csv.py
This file contains methods to save the amino acids, directions and coordinates of a generated protein into a csv file. As well as a method to read this csv file again and generate the protein as saved by the csv file.
To save a generated protein, use:
```
>> csv_compiler(protein, csv_name="protein")
```
By default, this saves the protein into a file named protein.csv in the current directory the user is in. If the user wants to use another name, the input should be like "a_name". To read a csv file use:
```
>> protein = csv_reader("csv_file")
```
Where csv_file is the name of the csv file in which the protein is saved, it is read as a string. This method immediately creates a new protein object and generates the path by looking at the coordinates the protein takes. This object needs to be assigned to a name.

### visuals.py
#WACHTEN TOT SAMER AF HEEFT
