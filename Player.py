from Settings import *


class Player:
    def __init__(self, initial_x, initial_y):
        self.pos_x = initial_x * SIZE + BORDER_THICKNESS
        self.pos_y = initial_y * SIZE + BORDER_THICKNESS
        self.matrix_pos_x = initial_x
        self.matrix_pos_y = initial_y
        self.width = SIZE - 2 * BORDER_THICKNESS
        self.height = SIZE - 2 * BORDER_THICKNESS
        self.color = WHITE

    def update(self, maze, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and self.pos_x > BORDER_THICKNESS and (
                        maze[self.matrix_pos_x][self.matrix_pos_y].left_border.color != BLACK):
                    self.pos_x -= SIZE
                    self.matrix_pos_x -= 1
                if event.key == pygame.K_RIGHT and self.pos_x + BORDER_THICKNESS < WIDTH - SIZE and (
                        maze[self.matrix_pos_x][self.matrix_pos_y].right_border.color != BLACK):
                    self.pos_x += SIZE
                    self.matrix_pos_x += 1
                if event.key == pygame.K_UP and self.pos_y > BORDER_THICKNESS and (
                        maze[self.matrix_pos_x][self.matrix_pos_y].top_border.color != BLACK):
                    self.pos_y -= SIZE
                    self.matrix_pos_y -= 1
                if event.key == pygame.K_DOWN and self.pos_y + BORDER_THICKNESS < HEIGHT - SIZE and (
                        maze[self.matrix_pos_x][self.matrix_pos_y].bottom_border.color != BLACK):
                    self.pos_y += SIZE
                    self.matrix_pos_y += 1

    def render(self, background):
        pygame.draw.rect(background, self.color, [self.pos_x, self.pos_y, self.width, self.height])
