## MAZE SEARCH (pygame)
### This is a course project of CS 3310 - Introduction to Aritificial Intelligent taught by Prof. Huong Thanh Le at Troy University, Hanoi campus.

#### Credits: This game is a modified version of Maze Search from https://github.com/projeto-de-algoritmos/Graphs-List1-DanielGoncalves-LucasMacedo

**Main changes from the original version:**
* Using A* algorithm to solve the maze (the original used breadth first search)
* Add some functions to support A* algorithm
* Code organization
* Changes in UI


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
