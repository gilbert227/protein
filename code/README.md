# Code

In this directory one can find all python code used for the project. The code is supposed to be used as package, and is divided in four sections.

## Classes
In the project, the protein sequence that needs to be folded is an object. As input arguments it takes the protein string and a Boolean value for using 3D. Usage:

```
protein = Protein("your_protein_string", dim3=True/False)
```

The protein class is very useful as it keeps track of the path and stability of a protein.

## Algorithms
The algorithms directory contains all the algorithms used to fold a protein string. There are four algorithms to be found in this folder.

### Random
The first algorithm is a random algorithm which can be found in random_path.py. This algorithm randomly chooses coordinates surrounding the current position to determine the new position in the protein path. Excluding positions already taken by the path ensures valid solutions. Usage:
```
>> generate_random_path(protein)
```
The path generated is saved in the protein object. This is the same for the other algorithms.

### Greedy
The second algorithm is a greedy algorithm which can be found in greedy_path.py. This algorithm will gather points as quickly as possible. So it will choose for the option which gives the most points. This algorithm takes two input arguments, named care and Greedy. Care is the factor that gives a penalty for placing amino acids who cannot make points next to amino acids who do have potential to make points. For example, placing a P next to a C will result in a penalty. These factors can be found classes/protein.py.
Greedy supports variable greed, which should be a float between 0 and 1. When greed is set to 1, it will always choose among the best scoring options. If not, a probability distribution is generated between higher and lower scoring options. Lowering the greed results in lower scoring options becoming more likely to be chosen. The score on which the distribution is based is a function of the added stability, the blocking penalty and the care that is set by the user.
Usage:
```
>> generate_greedy_path(protein, greed=1, care=0)
```
By default, care is 0. Care should be a float between 0 and 1.

### Chunky path
After that is an algorithm that is called chunky path. This algorithm divides a protein sequence in chunks of a given size and simulates this certain part of the sequence for a given number of times. It keeps track of the best path by using the number of stability points the path provides. After a chunk is determined to be the best, this whole chunk will be added to the final path. Note that the path in a chunk is made by using a random or greedy algorithm, depending on the users choice.
Usage:
```
>> generate_chunky_path(protein, chunk_size=6, iterations=50, step_strategy="greedy", care=0):
```
Where chunk_size is the size of the chunks, iterations is the number of times a chunk is made and step_strategy is the strategy for which the chunks will generate its individual steps. This argument should be either "greedy" or "random". If the step_strategy is greedy, the care factor will also play a role. This method is not compatible with the greed variable.

### Forward Search
Forward search is a constructive algorithm which generates all paths resulting from all posible decisions up to a certain depth (user defined). From these paths, it takes the paths that result in the highest stability in the fewest number of steps, and stores it. It then repeats this process untill a complete path is generated.
Usage:
```
>> forward_search(protein, depth=5, retry=True)
```
Depth should be an integer number not exceeding the length of the protein. In practice, it is probably best to keep the depth below 6, depending on the user's hardware and patience. The retry argument is used to lower the depth of the search if dead ends are generated repeatedly. It should be kept as is but the function sets it to false when it calls itself after the second attempt. After completion, the protein is updated to represent the final path and the effective depth is returned (as it is not necessarilly the user-defined depth).

## Helpers
In helpers/navigator.py one can find methods that are used to help determine the next coordinate in the path. Most of them are used for all algorithms. The function get_surrounding_coordinates takes a protein object and a coordinate as input and returns the positions surrounding the coordinate. Depending on the given protein's 'dim3' (boolean) attribute, either a 2D or 3D set of coordinates is returned. From a set of surrounding coordinates, get_step_options removes those already occupied by the protein, checks for symmetry with respect to the vertical axis, and returns the options available for the next aminoacid. For a given option, get_added_stability returns the added stability associated with the new step, as well as a weight which depends on the added stability and blocking penalty. make_up_your_mind is currently only used by the greedy algorithm, and generalizes the decision making process for variable greed.

## Analysis
This folder holds all functions to generate results and analyze the case. There are separate files for generating data (stats.py) and analyzing/visualizing (visuals.py).

### stats.py:
This file contains the following functions:

```
>> generate_path(protein, strategy, greed=1, care=0, chunk_size=6, chunk_iterations=100, step_strategy="greedy", depth=3)
```
This function is used to have a single method that can run all algorithms. This method also requires an input argument for which algorithm to use, called strategy. This should take the values: "random", "greedy", "chunky path" or "forward search". The rest of the input arguments are all the same as the input arguments of the algorithms.

```
>> get_next_unique_config(protein, strategy, configs=[], max_iterations=10000, greed=1, care=0, chunk_size=6, chunk_iterations=100, step_strategy="greedy")
```
Takes a protein, strategy (type string, name of the algorithm), and a list of configurations as input. It generates paths until one is found that is not in the list of configurations, i.e. a new unique path. It returns the number of iterations before the new configuration was found, the configuration itself, and a boolean signifying whether a new configuration was found before the maximum number of iterations was reached (i, config, found).

```
>> get_separating_duplicates(protein, strategy, duplication_threshold, greed=1, care=0, chunk_size=6, chunk_iterations=100, step_strategy="greedy", depth=3)
```
Calls get_next_unique_config, at first with an empty list. Takes the config that is returned, adds it to the configs list, stores the number of iterations and while 'found' is returned as True, reruns the previous function. As the list of configs grows, it will take more and more iterations to produce new configurations (hence 'separating duplicates'). The number of separating duplicates is a measure of the occupation of the state space, and if an asymptote can be observed before the number of iterations is exceeded, it must be located at the size of the state space (i.e. the set of all valid paths). In practice, this can only be done for short proteins (length below 10), and serves to illustrate the enourmous difference between the theoretical upper bound and the practical size of the state-space.

```
>> get_best_config(protein, strategy, iterations, greed=1, care=0, chunk_size=6, chunk_iterations=100, step_strategy="greedy", depth=3)
```
This method is used to return a best configuration within the given number of iterations. The method uses the same input as generate_path(), but has an extra argument called iterations. This is the number of times the user wants to generate a single path.

### csv.py
This file contains methods to save the amino acids, directions and coordinates of a generated protein into a csv file. As well as a method to read this csv file again and generate the protein as saved by the csv file.
To save a generated protein, use:
```
>> csv_compiler(protein)
```
This saves the protein into a file named protein.csv in the current directory the user is in. To read a csv file use:
```
>> csv_reader(csv_file)
```
Where csv_file is the name of the csv file in which the protein is saved. This method immediately creates a new protein object and generates the path by looking at the coordinates the protein takes.
