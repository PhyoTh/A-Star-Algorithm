# Grid World: Search Algorithm Visualization

This project visualizes different search algorithms (DFS, BFS, UCS, and A\*) finding paths in a grid world environment with obstacles and varying terrain costs.

## Project Structure

The project consists of several Python files:

- `main.py` - Main entry point and UI handling
- `game.py` - Grid and node classes for the environment
- `ai.py` - Implementation of search algorithms
- `test.py` - Test cases runner
- `tests` - Pre-configured test maps

## How It Works

### Environment

The grid world consists of a 25x25 grid where:

- **Yellow node**: Starting point
- **Orange node**: Goal point
- **Blue tiles**: Puddles (cannot be traversed)
- **Green tiles**: Grass (higher movement cost)
- **Black tiles**: Normal terrain (standard movement cost)

### Search Algorithms

The project implements four classic search algorithms:

#### 1. Depth-First Search (DFS)

- Uses a stack data structure (LIFO)
- Explores as far as possible along each branch before backtracking
- Not guaranteed to find the shortest path
- Implementation: Uses a list as a stack

#### 2. Breadth-First Search (BFS)

- Uses a queue data structure (FIFO)
- Explores all nodes at the present depth before moving to nodes at the next depth
- Guarantees shortest path in terms of number of steps (not cost)
- Implementation: Uses `collections.deque`

#### 3. Uniform Cost Search (UCS)

- Uses a priority queue ordered by path cost
- Always expands the node with the lowest path cost
- Guarantees shortest path in terms of cost
- Implementation: Uses `heapq` with cost as priority

#### 4. A\* Search

- Extension of UCS that uses a heuristic to guide the search
- Uses Manhattan distance as the heuristic function
- More efficient than UCS while still guaranteeing optimal paths
- Implementation: Uses `heapq` with (cost + heuristic) as priority

### Visual Indicators

While running a search:

- **Grey tiles**: Nodes in the frontier (to be explored)
- **Dark Grey tiles**: Nodes that have been explored
- **Red path**: Final solution path from start to goal

## How Components Interact

1. **Grid Class**: Maintains the state of the environment

   - Manages the collection of nodes
   - Handles rendering and updates
   - Provides methods for saving/loading grid configurations

2. **Node Class**: Represents each cell in the grid

   - Stores attributes like terrain type (normal, grass, puddle)
   - Manages visual state (frontier, explored, path)
   - Calculates traversal cost

3. **AI Class**: Implements search algorithms

   - Maintains frontier and explored sets
   - Steps through search algorithms one node at a time
   - Reconstructs solution path once goal is found

4. **GridWorld Class**: Main UI controller
   - Manages PyGame interface
   - Handles user input
   - Controls simulation flow (start/pause/reset)

## Algorithm Implementation Details

### Common Elements

All algorithms share:

- A frontier data structure (varies by algorithm)
- An explored set to avoid cycles
- A dictionary to track the previous node for path reconstruction

### A\* Implementation

```python
def astar_step(self):
    if not self.frontier:  # Empty frontier means no path exists
        self.failed = True
        self.finished = True
        return

    # Get node with lowest f(n) = g(n) + h(n)
    current_total_cost, current = heappop(self.frontier_heap)

    if current in self.explored:  # Skip if already explored
        return
    self.explored.add(current)

    if current == self.grid.goal:  # Goal found
        self.finished = True
        return

    # Add neighbors to the frontier
    for neighbor in get_neighbors(current):
        if valid_and_not_explored(neighbor):
            # g(n): Cost so far
            new_cost = self.cost_dict[current] + self.grid.nodes[neighbor].cost()

            # h(n): Manhattan distance heuristic
            heuristic = manhattan_distance(neighbor, self.grid.goal)

            # Only update if we found a better path
            if new_cost < self.cost_dict.get(neighbor, float('inf')):
                self.cost_dict[neighbor] = new_cost
                self.previous[neighbor] = current
                # Store with f(n) as priority
                heappush(self.frontier_heap, (new_cost + heuristic, neighbor))
```

## Running the Project

1. Start the application:

   ```
   python main.py
   ```

2. Interface controls:
   - Enter: Start/pause search
   - 1-4: Switch algorithm (DFS, BFS, UCS, A\*)
   - m: Generate random map
   - c: Clear current path
   - s/g: Place start/goal
   - p/r: Place puddle/grass
   - x: Clear node
3. Run test cases:
   ```
   python main.py -t
   ```
4. Load specific test case:
   ```
   python main.py -l 0
   ```

## Algorithm Comparison

- **DFS**: Fast exploration but often produces suboptimal paths
- **BFS**: Guarantees shortest path by steps but not by cost
- **UCS**: Guarantees optimal path but explores more nodes than necessary
- **A\***: Usually explores fewer nodes than UCS while still finding optimal paths

The application visualizes this by showing how many nodes each algorithm explores before finding the goal.
