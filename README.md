# CS580_Puzzle_Informed_Search
This program implements two Informed Searches with heuristics for the 24 puzzle problem.

The first heuristic `h1(x)` is defined as the number of misplaced tiles
AND
The second heuristic `h2(x)` is defined as the sum of the distances of every tile to its goal position.


To run with output in the terminal:
- Run `python3 puzzle.py H1` for heuristic 1
- Run `python3 puzzle.py H2` for heuristic 2
- Run `python3 puzzle.py H1HEAP` for heuristic 1 using a heap/priority queue
- Run `python3 puzzle.py H2HEAP` for heuristic 2 using a heap/priority queue

To run with output in a txt file:
- Run `python3 puzzle.py H1 > h1_output.txt` for heuristic 1
- Run `python3 puzzle.py H2 > h2_output.txt` for heuristic 2
- Run `python3 puzzle.py H1HEAP > h1Heap_output.txt` for heuristic 1 using a heap/priority queue
- Run `python3 puzzle.py H2HEAP > h2Heap_output.txt` for heuristic 2 using a heap/priority queue

Options:
- Add `--quiet` to any of the above commands for a quiet run, this means each state will not be printed only the end result described below
- Example: `python3 puzzle.py H1 --quiet > h1_output.txt` `python3 puzzle.py H1 --quiet`

The end result will be `SUCCESS` or `FAILURE` followed by the elapsed time of the search

Each run randomizes the initial state of the puzzle

The goal state is:<br />
`[1,   2,  3,  4,  5]`<br />
`[6,   7,  8,  9, 10]`<br />
`[11, 12, 13, 14, 15]`<br />
`[16, 17, 18, 19, 20]`<br />
`[21, 22, 23, 24,  0]`<br />

## Analysis
`h1Heap()` and `h2Heap()` implements the heuristics  using a priority queue as the data strucutre. 
`h1()` and `h2()` use the same heuristics as the priority queue functions. These two are implemented with lists, these get themselves trapped by previously visited states failing to find a solution more often than not. They can both solve specific start states but since each start state is randomized they aren't the most effective implementations. The heap/priority queue functions allow for much more movement therefore not getting themselves stuck. They are much slower than the successful non-heap functions but have a higher success rate.

Each run was stopped at 30 minutes (except on success or failure), see the respective txt files for the results.
