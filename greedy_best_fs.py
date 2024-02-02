import heapq

class PuzzleNode:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.cost = 0

    def __lt__(self, other):
        return self.cost < other.cost

def manhattan_distance(state, goal_state):
    distance = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] != goal_state[i][j]:
                x, y = divmod(goal_state[i][j], 3)
                distance += abs(x - i) + abs(y - j)
    return distance

def get_blank_position(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j

def get_neighbors(node):
    i, j = get_blank_position(node.state)
    neighbors = []

    for x, y in ((i+1, j), (i-1, j), (i, j+1), (i, j-1)):
        if 0 <= x < 3 and 0 <= y < 3:
            neighbor_state = [row[:] for row in node.state]
            neighbor_state[i][j], neighbor_state[x][y] = neighbor_state[x][y], neighbor_state[i][j]
            neighbors.append(PuzzleNode(neighbor_state, parent=node))

    return neighbors

def greedy_best_first_search(initial_state, goal_state, heuristic):
    initial_node = PuzzleNode(initial_state)
    goal_node = PuzzleNode(goal_state)

    if initial_state == goal_state:
        return [initial_state]

    priority_queue = [initial_node]
    visited_states = set()

    while priority_queue:
        current_node = heapq.heappop(priority_queue)

        if current_node.state == goal_state:
            path = [current_node.state]
            while current_node.parent:
                current_node = current_node.parent
                path.append(current_node.state)
            path.reverse()
            return path

        visited_states.add(tuple(map(tuple, current_node.state)))

        neighbors = get_neighbors(current_node)
        for neighbor in neighbors:
            if tuple(map(tuple, neighbor.state)) not in visited_states:
                neighbor.cost = heuristic(neighbor.state, goal_state)
                heapq.heappush(priority_queue, neighbor)

    return None

# Example usage:
initial_state = [
    [1, 2, 3],
    [4, 0, 5],
    [6, 7, 8]
]

goal_state = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0]
]

# Heuristic function (Manhattan distance)
heuristic_function = manhattan_distance

path = greedy_best_first_search(initial_state, goal_state, heuristic_function)

if path:
    print("Solution found:")
    for state in path:
        for row in state:
            print(row)
        print()
else:
    print("No solution found.")
