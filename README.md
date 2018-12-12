### DEPENDENCIES
Python v2.7
Python mpi4py
Python re
Open MPI v4.0

**Note:** In an n x m matrix, there must be m number of elements in each row with a 
space delimeter.

### SETUP
In main(), the default text file name is 'input.txt'. This file can be 
modified or the file name in main() can be replaced to use a different file. 

### EXECUTE
Execute with the command:

    mpirun -n  <number of rows in input file>  python transpose.py

    Ex:
    mpirun -n 3 python transpose.py

    for input.txt:
    1  2  3  4  5
    6  7  8  9  10
    11 12 13 14 15

### TERMINATION
Program will output matrix to the screen and exit. 

In the event mpi4py encounters an error prohibiting it from exiting, press 
Ctrl + C (or Ctrl + Shift + C on some laptops). Only do this once or may 
force quit mpi4py leaving hanging processes.


