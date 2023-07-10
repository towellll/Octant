# Octant
A tool for analyzing coincidental correctness test cases and fault localization

- Install
  ```pip install requirement.txt```

- Usage
  | parameter |                          discibtion                          |             choice             |
| :-------: | :----------------------------------------------------------: | :----------------------------: |
|    -m     |             Specify a coverage matrix file path              |           customize            |
|    -b     |                Specify a buggy line file path                |           customize            |
|    -f     |        Choose formula to compute the suspicious value        | suspiciousness compute formula |
|    -t     |                     Choose cc list type                      |   prediction or ground truth   |
|    -d     | Destination path to save the output, default is the matrix input directory |           customize            |
