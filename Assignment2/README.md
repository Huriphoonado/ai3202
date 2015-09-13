#Assignment 2

###Implementation of A* Search with Manhattan distance and Diagonal Shortcut heuristics

The program should be called with command line arguments indicating the world to be used (World1.txt, World2.txt) and then the heuristic (Manhattan, DiagonalShortcut). For example:

```
python Payne_Assignment2.py World1.txt Manhattan
python Payne_Assignment2.py World2.txt DiagonalShortcut
```

###Diagonal Sortcut Heuristic

I chose to explore the Diagonal Shortcut heuristic because I noticed the Manhattan heuristic did not produce the best possible paths when only considering total horizontal and vertical distances. For example, in World 1 rather than taking a diagonal path and avoiding the mountains, the horse first travels up and then to the right crashing into mountains. This is because the heuristic is weighted so high and does not consider diagonal paths that a path space diagonal from the target node appears less favorable than a mountain space horizontal to the target node. (Reducing the weight of the Manhattan heuristic from 10 to 5 produces better results.)

The Diagonal Shortcut heuristic subtracts the cost of moving diagonally from the current node to the target node. First it calculates the Manhattan distance: 10 * (dx + dy) then calculates the savings of taking as many diagonal steps to the end node as possible and subtracts that amount: (14 - (2 * 10)) * min(dx, dy).

The Diagonal Shortcut heuristic produces better paths than the Manhattan Distance heuristic on both worlds, but must evaluate more nodes overall.

* World 1
  * Manhattan Distance: Path costs 156 and explores 32 total nodes
  * Diagonal Shortcut: Path costs 130 and explores 39 total nodes
* World 2
  * Manhattan Distance: Path costs 144 and explores 31 total nodes
  * Diagonal Shortcut: Path costs 142 and explores 40 total nodes
