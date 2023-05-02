# 8 puzzle problem
# A* algorithm


## Idea:
- Find path from initial to goal state.
- Consider certain position on board as unique state.
- Use priority queue to first consider states with the lowest cost function.


## Heuristic:
- h(x) - number of cells, which are not in the right position.
- g(x) - amount of steps done to reach current state from the initial.
- f(x) = h(x) + g(x).


## Algorithm:
1. Put initial state in the priority queue.
2. Get state from queue.
3. If its `h(x) == 0`, it's a goal state and should be returned.
4. Add state in `closed` list.
5. Create new states from the taken by moving empty cell in all possible directions.
6. If a new state is not in the `closed` list, put it in the queue.
7. If queue is not empty, go to (2.)