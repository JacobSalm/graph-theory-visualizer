# Graph Theory Visualizer

An interactive graph theory visualizer built with Python and Pygame.

Create graphs, build valid walks, and step through an algorithm that removes closed subwalks until the result is a path or cycle.

## How to Use

### 1. Edit Graph

Press:

```text
1

Controls:

Left click empty space → create vertex
Click two vertices → create edge
Click the same two vertices again → remove edge
Hover over a vertex + press X → delete vertex
Right click → open menu
2. Build a Walk

Press:

2

Then click connected vertices in order.

Example:

W = a -> b -> c -> d -> b -> e

Controls:

Backspace = remove last step
C         = clear walk

The program only allows valid moves along existing edges.

3. Run Algorithm

Press:

3

Then press:

SPACE

to move through the algorithm one step at a time.

The program displays:

W = original walk
P = current walk
C = shortest closed subwalk

The algorithm stops when P becomes either a path or a cycle.

Quick Controls
Key	Action
1	Edit Graph
2	Build Walk
3	Run Algorithm
Space	Next algorithm step
X	Delete hovered vertex
Backspace	Undo walk step
C	Clear walk
Right Click	Open menu
Esc	Cancel / close menu