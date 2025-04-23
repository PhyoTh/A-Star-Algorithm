# A\* Algorithm Implementation

This project demonstrates various search algorithms including DFS, BFS, UCS, and A\* in a grid world environment. It provides a visual interface to observe how each algorithm explores the space and finds paths.

## Documentation

For detailed information about how the project works, algorithm implementations, and component interactions, please see the [Documentation](./Documentation.md).

## Setting Up

First, make sure you have Python 3.\* and the latest pip version. Here is the preferred way to set up:

1. Install [anaconda](https://docs.anaconda.com/anaconda/install/) to set up a virtual environment
2. Run `conda create -n cse150b python=3.12`
3. Run `conda activate cse150b`
4. To install PyGame, `pip install pygame`. We will use PyGame for all assignments in this class.

You can run `conda deactivate` to deactivate the virtual environment. The next time you want to work on the project,
type `conda activate cse150b` first to use the exact same environment with PyGame installed.

## Usage

Run `python main.py` to open the grid world window. By pressing `enter` you can see how the search algorithms find a path.

- Press 1, 2, 3, or 4 to switch between DFS, BFS, UCS, and A\* respectively
- The `tests` file contains test maps that can be loaded with `python main.py -l [test case number]`
- Run `python main.py -t` to automatically test all algorithms on the provided test cases

## Controls

- **Esc**: Exit application
- **Enter**: Start/pause search
- **1-4**: Select algorithm (DFS, BFS, UCS, A\*)
- **c**: Clear path
- **m**: Generate random board
- **s/g**: Place start/goal
- **p/r**: Place puddle/grass
- **x**: Clear node
- **w/l**: Save/load board

## Screenshots

[You could add screenshots of your application here]

## Acknowledgements

This project demonstrates classic search algorithms from the field of artificial intelligence.
