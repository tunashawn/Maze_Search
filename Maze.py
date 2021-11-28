import random
from Node import Node
from Utils import *


class Maze:
    def __init__(self, background, initial_x, initial_y, final_x, final_y):
        self.maze = []
        self.total_nodes = 0
        self.maze_created = False
        self.initial_coordinate_x = initial_x
        self.initial_coordinate_y = initial_y
        self.final_coordinate_x = final_x
        self.final_coordinate_y = final_y

        x = 0
        y = 0
        for i in range(0, WIDTH, SIZE):
            self.maze.append([])
            for j in range(0, HEIGHT, SIZE):
                self.maze[x].append(Node(i, j))
                self.total_nodes += 1
                y += 1
            x += 1

        self.define_neighbors()

    def add_edge(self, node, neighbor):
        neighbor.neighbors_connected.append(node)
        node.neighbors_connected.append(neighbor)

    def remove_neighbors_visited(self, node):
        node.neighbors = [x for x in node.neighbors if not x.visited]

    def define_neighbors(self):
        for i in range(0, int(HEIGHT / SIZE)):
            for j in range(0, int(WIDTH / SIZE)):
                self.maze[i][j].matrix_pos_x = i
                self.maze[i][j].matrix_pos_y = j
                if i > 0 and j > 0 and i < int(HEIGHT / SIZE) - 1 and j < int(HEIGHT / SIZE) - 1:
                    self.maze[i][j].neighbors.append(self.maze[i + 1][j])  # bot
                    self.maze[i][j].neighbors.append(self.maze[i - 1][j])  # top
                    self.maze[i][j].neighbors.append(self.maze[i][j + 1])  # right
                    self.maze[i][j].neighbors.append(self.maze[i][j - 1])  # left
                elif i == 0 and j == 0:
                    self.maze[i][j].neighbors.append(self.maze[i][j + 1])  # right
                    self.maze[i][j].neighbors.append(self.maze[i + 1][j])  # bot
                elif i == int(HEIGHT / SIZE) - 1 and j == 0:
                    self.maze[i][j].neighbors.append(self.maze[i - 1][j])  # top
                    self.maze[i][j].neighbors.append(self.maze[i][j + 1])  # right
                elif i == 0 and j == int(WIDTH / SIZE) - 1:
                    self.maze[i][j].neighbors.append(self.maze[i][j - 1])  # left
                    self.maze[i][j].neighbors.append(self.maze[i + 1][j])  # bot
                elif i == int(HEIGHT / SIZE) - 1 and j == int(WIDTH / SIZE) - 1:
                    self.maze[i][j].neighbors.append(self.maze[i][j - 1])  # left
                    self.maze[i][j].neighbors.append(self.maze[i - 1][j])  # top
                elif j == 0:
                    self.maze[i][j].neighbors.append(self.maze[i - 1][j])  # top
                    self.maze[i][j].neighbors.append(self.maze[i][j + 1])  # right
                    self.maze[i][j].neighbors.append(self.maze[i + 1][j])  # bot
                elif i == 0:
                    self.maze[i][j].neighbors.append(self.maze[i + 1][j])  # bot
                    self.maze[i][j].neighbors.append(self.maze[i][j + 1])  # right
                    self.maze[i][j].neighbors.append(self.maze[i][j - 1])  # left
                elif i == int(HEIGHT / SIZE) - 1:
                    self.maze[i][j].neighbors.append(self.maze[i - 1][j])  # top
                    self.maze[i][j].neighbors.append(self.maze[i][j + 1])  # right
                    self.maze[i][j].neighbors.append(self.maze[i][j - 1])  # left
                elif j == int(WIDTH / SIZE) - 1:
                    self.maze[i][j].neighbors.append(self.maze[i + 1][j])  # bot
                    self.maze[i][j].neighbors.append(self.maze[i - 1][j])  # top
                    self.maze[i][j].neighbors.append(self.maze[i][j - 1])  # left

    def break_border(self, node, neightbor, color):
        # right
        if (neightbor.matrix_pos_x == node.matrix_pos_x + 1) and (neightbor.matrix_pos_y == node.matrix_pos_y):
            node.right_border.color = color
            neightbor.left_border.color = color
        # left
        elif (neightbor.matrix_pos_x == node.matrix_pos_x - 1) and (neightbor.matrix_pos_y == node.matrix_pos_y):
            node.left_border.color = color
            neightbor.right_border.color = color
        # bot
        elif (neightbor.matrix_pos_x == node.matrix_pos_x) and (neightbor.matrix_pos_y == node.matrix_pos_y + 1):
            node.bottom_border.color = color
            neightbor.top_border.color = color
        # top
        elif (neightbor.matrix_pos_x == node.matrix_pos_x) and (neightbor.matrix_pos_y == node.matrix_pos_y - 1):
            node.top_border.color = color
            neightbor.bottom_border.color = color

    def dfs(self, background):
        current_cell = random.choice(random.choice(self.maze))
        current_cell.visited = True
        current_cell.color = GREEN
        stack = [current_cell]
        visited_cells = 1

        while visited_cells != self.total_nodes or len(stack) != 0:
            self.remove_neighbors_visited(current_cell)
            if len(current_cell.neighbors) > 0:
                random_neighbor = random.choice(current_cell.neighbors)

                self.break_border(current_cell, random_neighbor, GREEN)

                self.add_edge(current_cell, random_neighbor)
                current_cell = random_neighbor
                stack.append(current_cell)
                current_cell.visited = True
                current_cell.color = GREEN
                visited_cells += 1
            else:
                current_cell.color = YELLOW

                if current_cell.top_border.color == GREEN:
                    current_cell.top_border.color = YELLOW
                if current_cell.bottom_border.color == GREEN:
                    current_cell.bottom_border.color = YELLOW
                if current_cell.right_border.color == GREEN:
                    current_cell.right_border.color = YELLOW
                if current_cell.left_border.color == GREEN:
                    current_cell.left_border.color = YELLOW

                if len(stack) == 1:
                    stack.pop()
                else:
                    stack.pop()
                    current_cell = stack[-1]
            self.render(background)
            text(background, "GENERATING MAZE", WHITE, FONTSIZE_COMMANDS_INTIAL, WIDTH/2 - 60, HEIGHT / 2)
            pygame.display.update()
        self.maze_created = True



    def bfs(self, background, player):
        """
        Using Best First Search to solve the maze
        It decides the cost based on x coordinate
        and y coordinate of the current block and
        the destination block

        :param background:
        :param player:
        :return:
        """
        initial_node = self.maze[player.matrix_pos_x][player.matrix_pos_y]
        initial_node.explored = True
        find = False
        queue = [initial_node]
        while len(queue) > 0 and not find:
            queue[0].color = PINK

            if queue[0].top_border.color == YELLOW:
                queue[0].top_border.color = PINK
            if queue[0].bottom_border.color == YELLOW:
                queue[0].bottom_border.color = PINK
            if queue[0].right_border.color == YELLOW:
                queue[0].right_border.color = PINK
            if queue[0].left_border.color == YELLOW:
                queue[0].left_border.color = PINK

            u = queue.pop(0)
            for i in u.neighbors_connected:
                if i.explored == False:
                    i.parent = u
                    i.explored = True
                    queue.append(i)
                    if i.matrix_pos_x == self.final_coordinate_x and i.matrix_pos_y == self.final_coordinate_y:
                        find = True
            self.render(background)
            text(background, "SOLVING MAZE", WHITE, FONTSIZE_COMMANDS_INTIAL, WIDTH/2 - 60, HEIGHT / 2)
            player.render(background)
            pygame.display.update()

        current = self.maze[self.final_coordinate_x][self.final_coordinate_y]
        while (current.parent).parent != None:
            current = current.parent
            current.color = GREEN   # color for the solution

            if current.top_border.color == PINK:
                current.top_border.color = GREEN
            if current.bottom_border.color == PINK:
                current.bottom_border.color = GREEN
            if current.right_border.color == PINK:
                current.right_border.color = GREEN
            if current.left_border.color == PINK:
                current.left_border.color = GREEN

            self.render(background)
            player.render(background)
            pygame.display.update()

    def render(self, background):
        for i in range(0, int(HEIGHT / SIZE)):
            for j in range(0, int(WIDTH / SIZE)):
                self.maze[i][j].render(background)
        if self.maze_created:
            self.maze[self.initial_coordinate_x][self.initial_coordinate_y].color = BEIGE
            self.maze[self.final_coordinate_x][self.final_coordinate_y].color = LIGHTBLUE
