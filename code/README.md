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
Forward search is a constructive algorithm which generates all paths resulting from all possible decisions up to a certain depth (user defined). From these paths, it takes the paths that result in the highest stability in the fewest number of steps, and stores it. It then repeats this process until a complete path is generated.
Usage:
```
>> forward_search(protein, depth=5, retry=True)
```
Depth should be an integer number not exceeding the length of the protein. In practice, it is probably best to keep the depth below 6, depending on the user's hardware and patience. The retry argument is used to lower the depth of the search if dead ends are generated repeatedly. It should be kept as is but the function sets it to false when it calls itself after the second attempt. After completion, the protein is updated to represent the final path and the effective depth is returned (as it is not necessarily the user-defined depth).

## Helpers
In helpers/navigator.py one can find methods that are used to help determine the next coordinate in the path. Most of them are used for all algorithms. The function get_surrounding_coordinates takes a protein object and a coordinate as input and returns the positions surrounding the coordinate. Depending on the given protein's 'dim3' (Boolean) attribute, either a 2D or 3D set of coordinates is returned. From a set of surrounding coordinates, get_step_options removes those already occupied by the protein, checks for symmetry with respect to the vertical axis, and returns the options available for the next amino acid. For a given option, get_added_stability returns the added stability associated with the new step, as well as a weight which depends on the added stability and blocking penalty. make_up_your_mind is currently only used by the greedy algorithm, and generalizes the decision making process for variable greed.

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
Takes a protein, strategy (type string, name of the algorithm), and a list of configurations as input. It generates paths until one is found that is not in the list of configurations, i.e. a new unique path. It returns the number of iterations before the new configuration was found, the configuration itself, and a Boolean signifying whether a new configuration was found before the maximum number of iterations was reached (i, config, found).

```
>> get_separating_duplicates(protein, strategy, duplication_threshold, greed=1, care=0, chunk_size=6, chunk_iterations=100, step_strategy="greedy", depth=3)
```
Calls get_next_unique_config, at first with an empty list. Takes the config that is returned, adds it to the configs list, stores the number of iterations and while 'found' is returned as True, reruns the previous function. As the list of configs grows, it will take more and more iterations to produce new configurations (hence 'separating duplicates'). The number of separating duplicates is a measure of the occupation of the state space, and if an asymptote can be observed before the number of iterations is exceeded, it must be located at the size of the state space (i.e. the set of all valid paths). In practice, this can only be done for short proteins (length below 10), and serves to illustrate the enormous difference between the theoretical upper bound and the practical size of the state-space.

```
>> get_best_config(protein, strategy, iterations, greed=1, care=0, chunk_size=6, chunk_iterations=100, step_strategy="greedy", depth=3)
```
This function is used to return a best configuration within the given number of iterations. The function uses the same input as generate_path(), but has an extra argument called iterations. This is the number of times the user wants to generate a single path.

```
>> speedtest(protein, strategy, minutes=1, greed=1, care=0, chunk_size=6, chunk_iterations=100, step_strategy="greedy", depth=3)
```
This function generates paths within the given amount of time in minutes. It returns a dictionary with stabilities as keys and the number of times the stability is found as the value. All input arguments except for minutes are used a mentioned before.

### csv.py
This file contains functions to save the amino acids, directions and coordinates of a generated protein into a csv file. As well as a method to read this csv file again and generate the protein as saved by the csv file.
To save a generated protein, use:
```
>> csv_compiler(protein, csv_name="protein")
```
By default, this saves the protein into a file named protein.csv in the current directory the user is in. If the user wants to use another name, the input should be like "a_name". To read a csv file use:
```
>> protein = csv_reader("csv_file")
```
Where csv_file is the name of the csv file in which the protein is saved, it is read as a string. This function immediately creates a new protein object and generates the path by looking at the coordinates the protein takes. This object needs to be assigned to a name.

### visuals.py
This file contains functions that create histograms or plots to easily check results.

```
>> plot_path(protein)
```
This function plots a path of the folded protein, depending on the protein dimensions, the plot will be in 2D or 3D.

```
>> care_histogram(protein, iterations, strategy, percentage, chunk_size=6, chunk_iterations=100, step_strategy="greedy")
```
This function plots multiple plots in one figure. 'nrows' is the amount of plots vertically. 'ncols' is the amount of plots horizontally. Thus, nrows=3 and ncols=4 means 12 plots. Care is plotted for a range of 0.0 until 'max_care'. In the plot, only 'percentage' is shown, that is, if 90 is given 90% of the data is shown.

```
>> comparing_test(protein, it_random=0, it_greedy=0, care_greedy=0, it_chunky=0, care_chunky=0, it_forward=0, care_forward=0)
```
This function plots all the different algorithms against eachother. It plots it in a density plot, thus all the data is normalized. One can choose which algorithm is included, by setting the amount of iterations to 0 or non-zero. Care_forward is currently unused, but usefull for further studies. This function is build for a large range of applications, therefore DataFrames are used and the best solution is calculated manually.

```
>> forward_depth_test(protein, minutes, depth_range)
```
This function plots different depth sizes for the Forward Search algorithm on top of eachother. It uses a time range, with the same amount of time for all depth sizes. This is done because sometimes the time explodes and no results are found. 'depth_range' needs a tuple with all the depth sizes desired to test.

```
>> chunk_size_test(protein, minutes, chunk_range)
```
This function plots different chunk sizes for the Chunky Path algorithm against eachother. It uses a time range, with the same amount of time for all depth sizes. This is done because sometimes the time explodes and no results are found. 'chunk_range' needs a tuple with all the chunk sizes desired to test.
