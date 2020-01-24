# Code

In this map one can find all python code used for the project. The code is supposed to be used as package, and is divided in four sections.

## Algorithms
In the map algorithms one can find all algorithms used to fold a protein string. There are four algorithms to be found in this map.

### Random
The first algorithm is a random algorithm which can be found in random_path.py. This algorithm randomly chooses coordinates to determine the new position in the protein path.

### Greedy
The second algorithm is a greedy algorithm which can be found in greedy_path.py. This algorithm will gather points as quick as possible. So it will choose for the option which gives the most points. There are two important input arguments in this algorithm, named care and greedy.
Care is the factor that gives a penalty for placing P (or H) Amino acids next to C. Greed is .... *WHAT DOET GREEED*

### Chunky path
After that is an algorithm that is called chunky path, this algorithm divides a protein sequence in chunks of a given size and simulates this certain part of the sequence for a given number of times. It keeps track of the best path by using the number of stability points the path provides. After a chunk is determined to be the best, this whole chunk will be added to the final path. Note that the path in a chunk is made by using a random or greedy algorithm, depending on the users choice.

### Forward Search
*FORWAAARRDDD NOW*

## Classes
In the project, the protein sequence that needs to be folded is an object. As input it takes the protein string and a Boolean value for using 3D. Usage:

```
protein = Protein("your_protein_string", dim3=True/False)
```

The protein class is very useful as it keeps track of the path and stability of a protein.

## Helpers


## Analysis
