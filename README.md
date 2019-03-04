# Borah routing implementation by Guillaume Guérin and Anthony Prudhomme for ECE 6133

## Getting started

To run the project, open any terminal, go to the project root (inside borah-routing) and run the following command:

    python main.py [filename] [MST method]

Mandatory parameters:

[filename]: the filename parameters correspond to the name of the file you want to read the points from e.g. : points_10_5.pts.txt

[MST method]: it can either be prim or kruskal. This is the name of the method you want to the program to use to make the MST.

Example:
    python main.py points_10_5.pts.txt prim

## If you want to try the program with a file that wasn't provided in the project resource

Put your file in the "Points" folder located at the root of the project.
Put that filename as parameter to the run command (as explained above).

### If you encounter any issue, contact aprudhomme3@gatech.edu or gguerin3@gatech.edu