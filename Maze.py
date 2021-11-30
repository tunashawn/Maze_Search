import random

import pygame.time

from Node import Node
from Settings import *


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
        """
        Using randomized depth first search algorithm to generate the maze
        :param background:
        :return:
        """
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
            text(background, "GENERATING MAZE", WHITE, 60, WIDTH / 2 - 120, HEIGHT / 2 - 50)
            pygame.display.update()
        self.maze_created = True

    def color_explored_node(self, node):
        node.color = PINK
        if node.top_border.color == YELLOW:
            node.top_border.color = PINK
        if node.bottom_border.color == YELLOW:
            node.bottom_border.color = PINK
        if node.right_border.color == YELLOW:
            node.right_border.color = PINK
        if node.left_border.color == YELLOW:
            node.left_border.color = PINK

    def color_solution(self, current):
        current.color = GREEN  # color for the solution

        if current.top_border.color == PINK:
            current.top_border.color = GREEN
        if current.bottom_border.color == PINK:
            current.bottom_border.color = GREEN
        if current.right_border.color == PINK:
            current.right_border.color = GREEN
        if current.left_border.color == PINK:
            current.left_border.color = GREEN

    def calculate_cost(self, node):
        """Calculate g(n), h(n), and total cost"""
        # Calculate g(n)
        node.cost_to_reach = node.parent.cost_to_reach + 1
        # Calculate h(n)
        node.estimate_cost = (self.final_coordinate_x - node.matrix_pos_x) + (
                self.final_coordinate_y - node.matrix_pos_y)
        # Calculate total cost = g(n) + h(n)
        node.total_cost = node.cost_to_reach + node.estimate_cost

    def a_star_search(self, background, player):
        """Solving the maze using A* Search Algorithm
        Find the way from the current position of the player to the goal"""
        # Set the start_node to the current position of the player
        start_node = self.maze[player.matrix_pos_x][player.matrix_pos_y]
        start_node.explored = True
        found = False

        # Set cost_to_reach for the start node
        start_node.cost_to_reach = 0

        # Put the start_node to to frontier
        frontier = [start_node]

        # Keep exploring the map until there are no
        # node to be explored or until reach the destination
        while len(frontier) > 0 and not found:
            # Sort the frontier by total_cost: g(n) + h(n)
            # This works like a priority queue
            frontier.sort(key=lambda x: x.total_cost)

            # Pop out the node with smallest total_cost
            node = frontier.pop(0)

            # All the node that this algorithm visited
            # will be colored in PINK
            self.color_explored_node(node)

            # Traverse through neighbor nodes
            for neighbor in node.neighbors_connected:
                # Set the current nodes to be the parent of the neighbor nodes
                # that are not explored yet
                # Then add it to the frontier
                if neighbor.explored is False:
                    neighbor.parent = node
                    neighbor.explored = True

                    # Calculate g(n), h(n), and total cost for this node
                    self.calculate_cost(neighbor)

                    frontier.append(neighbor)
                    # If this node is the destination, then set the found = True
                    # Then stop exploring the maze
                    if neighbor.matrix_pos_x == self.final_coordinate_x and neighbor.matrix_pos_y == self.final_coordinate_y:
                        found = True

            self.render(background)
            text(background, "SOLVING MAZE USING A* ALGORITHM", WHITE, 60, WIDTH / 2 - 180, HEIGHT / 2 - 50)
            player.render(background)
            pygame.display.update()

        # Now start from the goal node
        current = self.maze[self.final_coordinate_x][self.final_coordinate_y]
        # Draw the path to from the goal to the position of player
        # Using color of GREEN
        while (current.parent).parent is not None:
            current = current.parent
            # Color the path by GREEN
            self.color_solution(current)

            self.render(background)
            player.render(background)
            pygame.display.update()

    def render(self, background):

        for i in range(0, int(HEIGHT / SIZE)):
            for j in range(0, int(WIDTH / SIZE)):
                self.maze[i][j].render(background)
        if self.maze_created:
            self.maze[self.initial_coordinate_x][self.initial_coordinate_y].color = BLUE
            self.maze[self.final_coordinate_x][self.final_coordinate_y].color = RED
