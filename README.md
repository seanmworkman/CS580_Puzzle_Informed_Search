# CS580_Puzzle_Informed_Search
This program implements two Informed Searches with heuristics for the 24 puzzle problem.

The first heuristic `h1(x)` is defined as the number of misplaced tiles
AND
The second heuristic `h2(x)` is defined as the sum of the distances of every tile to its goal position.


To run with output in the terminal:
- Run `python3 puzzle.py H1` for Breadth-First-Search
- Run `python3 puzzle.py H2` for Depth-First-Search

To run with output in a txt file:
- Run `python3 puzzle.py H1 > h1_output.txt` for heuristic 1
- Run `python3 puzzle.py H2 > h2_output.txt` for heuristic 2

Options:
- Add `--quiet` to any of the above commands for a quiet run, this means each state will not be printed only the end result described below
- Example: `python3 puzzle.py H1 --quiet > h1_output.txt` `python3 puzzle.py H1 --quiet`

The end result will be `SUCCESS` followed by the elapsed time of the search

Each run randomizes the initial state of the puzzle

The goal state is:<br />
`[1,   2,  3,  4,  5]`<br />
`[6,   7,  8,  9, 10]`<br />
`[11, 12, 13, 14, 15]`<br />
`[16, 17, 18, 19, 20]`<br />
`[21, 22, 23, 24,  0]`<br />

