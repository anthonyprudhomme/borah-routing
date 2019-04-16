# Borah routing implementation by Guillaume Guérin and Anthony Prudhomme for ECE 6133

## Getting started

    python -m pip install -U matplotlib
    python -m pip install -U networkx

To run the project, open any terminal, go to the project root (inside borah-routing) and run the following command:

Example Usages:
    python main.py --input points_10_5.pts.txt --mst_alg prim --num_pass 10 --show_progress

    -h, --help          show this help message and exit
    -i INPUT, --input INPUT
                        Input points file.
    -mst {prim,kruskal}, --mst_alg {prim,kruskal}
                        Minimum spanning tree algorithm.
    -pass NUM_PASS, --num_pass NUM_PASS
                        Number of pass you want to run.
    -prog, --show_progress
                        Shows an updated graph for each new added Steiner
                        point. /!\ Performance will be highly degraded in that
                        case. /!\

Mandatory parameters:

[--input]: the filename parameters correspond to the name of the file you want to read the points from e.g. : points_10_5.pts.txt

[--mst_alg]: it can either be "prim" or "kruskal". This is the name of the method you want to the program to use to make the MST.

## If you want to try the program with a file that wasn't provided in the project resource

Put your file in the "Points" folder located at the root of the project.
Put that filename as parameter to the run command (as explained above).

### If you encounter any issue, contact aprudhomme3@gatech.edu or gguerin3@gatech.edu