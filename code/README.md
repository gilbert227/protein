# Code

In this map one can find all python code used for the project. The code is supposed to be used as package, and is divided in four sections.

## Classes
In the project, the protein sequence that needs to be folded is an object. As input arguments it takes the protein string and a Boolean value for using 3D. Usage:

```
protein = Protein("your_protein_string", dim3=True/False)
```

The protein class is very useful as it keeps track of the path and stability of a protein.

## Algorithms
In the map algorithms one can find all algorithms used to fold a protein string. There are four algorithms to be found in this map. They can all be runned by a method in analysis/stats.py.

### Random
The first algorithm is a random algorithm which can be found in random_path.py. This algorithm randomly chooses coordinates to determine the new position in the protein path.
Usage:
```
>> generate_random_path(protein)
```
The path generated is saved in the protein object. This is the same for the other algorithms.

### Greedy
The second algorithm is a greedy algorithm which can be found in greedy_path.py. This algorithm will gather points as quick as possible. So it will choose for the option which gives the most points. This algorithm takes one input argument, named care. Care is the factor that gives a penalty for placing amino acids who cannot make points next to amino acids who do have potential to make points. For example, placing a P next to a C will result in a penalty. These factors can be found classes/protein.py.
Usage:
```
>> generate_greedy_path(protein, care=0)
```
By default, care is 0. Care should be a float between 0 and 1.

### Chunky path
After that is an algorithm that is called chunky path, this algorithm divides a protein sequence in chunks of a given size and simulates this certain part of the sequence for a given number of times. It keeps track of the best path by using the number of stability points the path provides. After a chunk is determined to be the best, this whole chunk will be added to the final path. Note that the path in a chunk is made by using a random or greedy algorithm, depending on the users choice.
Usage:
```
>> generate_chunky_path(protein, chunk_size = 6, iterations = 50, step_strategy = "greedy", care = 0):
```
Where chunk_size is the size of the chunks, iterations is the number of times a chunk is made and step_strategy is the strategy for which the chunks will generate its individual steps. This argument should be either "greedy" or "random". If the step_strategy is greedy, the care factor will also play a role.

### Forward Search
Forward search
Usage:
```
>> forward_search(protein, depth=5, retry=True)
```


## Helpers


## Analysis
