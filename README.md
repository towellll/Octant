# Octant
A tool for analyzing coincidental correctness test cases and fault localization.
Octant, which analyzes coincidental correctness test cases (CC) for fault localization. The tool automatically collect information about the test cases of a program and the ratio of CC. With OCTANT, researchers can effectively address the impact of CC by relabeling or removing them. Additionally, OCTANT incorporates a supervised random forest-based CC detection approach along with more than ten fault localization techniques for suspiciousness evaluation.

# I.Install

 
  ```pip install requirement.txt```

# II.Overview of Octant
[The overview of Octant.\label{step}](./overview.png)

# III.Use in Command-line 

- Parameters

Command-line in python
The list of parameters provided by Octant is as follows.
  
| parameter | description| choice|
| :-------: | :----------------------------------------------------------: | :----------------------------: |
|    -m     |             Specify a coverage matrix file path              |           customize            |
|    -b     |                Specify a buggy line file path                |           customize            |
|    -f     |        Choose formula to compute the suspicious value        | suspiciousness compute formula |
|    -t     |                     Choose cc list type                      |   prediction or ground truth   |
|    -d     | Destination path to save the output, default is the matrix input directory |           customize and optional           |


- Methods

| method | discibtion | parameter |
| :----:| :----: | :----: |
| predict | Using an algorithm to predict CC| -m -b |
| ratio | UCC| -m -b |
| remove | Remove test cases from matrix| -m -t |
| relabel | Change test case label in matrix | -m -t |
| rank | View buggy line rankings and suspiciousness value| -m -b -f|
| sfl | View all statement rankings and suspiciousness value | -m -b -f |


  
