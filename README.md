# Octant
A tool for analyzing coincidental correctness test cases and fault localization

- Install
  ```pip install requirement.txt```

- Usage

  
| parameter | description| choice|
| :-------: | :----------------------------------------------------------: | :----------------------------: |
|    -m     |             Specify a coverage matrix file path              |           customize            |
|    -b     |                Specify a buggy line file path                |           customize            |
|    -f     |        Choose formula to compute the suspicious value        | suspiciousness compute formula |
|    -t     |                     Choose cc list type                      |   prediction or ground truth   |
|    -d     | Destination path to save the output, default is the matrix input directory |           customize            |




| method | discibtion | parameter |
| :----:| :----: | :----: |
| predict | Using an algorithm to predict CC| -m -b |
| ratio | Using an algorithm to predict CC| -m -b |
| remove | Remove test cases from matrix| -m -t |
| relabel | Change test case label in matrix | -m -t |
| rank | View buggy line rankings and suspiciousness value| -m -b -f|
| sfl | View all statement rankings and suspiciousness value | -m -b -f |
