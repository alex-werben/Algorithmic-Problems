from queue import PriorityQueue
import numpy as np
class Node:
    # right, bottom, left, up
    moves = ((0, 1), (1, 0), (0, -1), (-1, 0))
    def __init__(self, matrix_, goal_state_, parent_=None):
        self.matrix = matrix_ # matrix - current state
        self.h_x = 0
        self.g_x = 0
        self.f_x = 0
        self.parent = parent_
        self.calculate_cost(goal_state_)


    def __lt__(self, other):
        if self.f_x < other.f_x:
            return True
        elif self.f_x == other.f_x:
            if self.h_x < other.h_x:
                return True
        return False

    def calculate_cost(self, goal_state_):
        h_x = 0
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix)):
                if self.matrix[i][j] != goal_state_[i][j] and self.matrix[i][j] != 0:
                    h_x += 1
        self.h_x = h_x
        if self.parent:
            self.g_x = self.parent.g_x + 1
        else:
            self.g_x = 0
        self.f_x = self.h_x + self.g_x

    def get_empty_cell(self):
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix)):
                if self.matrix[i][j] == 0:
                    return i, j

    def create_children(self):
        zero_i, zero_j = self.get_empty_cell()
        children = []
        for move in Node.moves:
            # check if movement doesn't cross board border
            if 0 <= zero_i + move[0] < 3 and 0 <= zero_j + move[1] < 3:
                new_matrix = np.copy(self.matrix)
                new_matrix[zero_i][zero_j] = self.matrix[zero_i + move[0]][zero_j + move[1]]
                new_matrix[zero_i + move[0]][zero_j + move[1]] = 0
                children.append(new_matrix)
        return children

class A_star:
    def __init__(self, init_state_, goal_state_):
        self.open = PriorityQueue()
        self.closed = []
        self.init_state = init_state_
        self.goal_state = goal_state_
        root = Node(self.init_state, self.goal_state)
        self.open.put(root)

    def already_visited(self, matrix_):
        for matrix in self.closed:
            if np.array_equal(matrix, matrix_):
                return True
        return False

    def find_solution(self):
        i = 8
        while not self.open.empty():
            node = self.open.get()
            print(self.open.qsize())
            if node.h_x == i:
                with open(f'{i}.txt', "w") as fp:
                    print_solution_to_file(fp, node)
                i -= 1
            if node.h_x == 0:
                return node
            self.closed.append(node.matrix)
            # create children and put unique in Q
            children = node.create_children()
            for child in children:
                if not self.already_visited(child):
                    new_node = Node(child, self.goal_state, node)
                    self.open.put(new_node)


def print_solution_to_file(fp, goal_node):
    stack = []
    while goal_node:
        stack.append(goal_node)
        goal_node = goal_node.parent
    while stack:
        node = stack.pop(len(stack) - 1)
        fp.write(np.array2string(node.matrix))
        # print(node.matrix)
        if len(stack) > 0:
            fp.write("\n    V\n")
        # print(" V")

def print_solution(goal_node: Node):
    stack = []
    while goal_node:
        stack.append(goal_node)
        goal_node = goal_node.parent
    while stack:
        node = stack.pop(len(stack) - 1)
        print(node.matrix)
        if len(stack) > 0:
            print(" V")

if __name__ == "__main__":
    init_state = np.array([[7, 5, 6],
                           [8, 2, 1],
                           [4, 3, 0]])
    goal_state = np.array([[1, 2, 3],
                           [4, 5, 6],
                           [7, 8, 0]])
    puzzle = A_star(init_state, goal_state)
    solution = puzzle.find_solution()
    print_solution(solution)