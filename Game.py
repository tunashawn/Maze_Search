import random
import sys

from Maze import Maze
from Player import Player
from Utils import *


class Game():
    def __init__(self):
        try:
            pygame.init()
        except:
            print('The pygame module did not start successfully')

        self.initial_coordinate_x = 0
        self.initial_coordinate_y = 0
        self.final_coordinate_x = 0
        self.final_coordinate_y = 0
        self.start = False
        self.solved = False
        self.winner = False
        self.exit = False

    def load(self):
        self.background = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption('Maze Game')
        self.initial_coordinate_x = random.randint(0, int(HEIGHT / SIZE) - 1)
        self.initial_coordinate_y = random.randint(0, int(WIDTH / SIZE) - 1)
        self.final_coordinate_x = random.randint(0, int(HEIGHT / SIZE) - 1)
        self.final_coordinate_y = random.randint(0, int(WIDTH / SIZE) - 1)
        while self.final_coordinate_x == self.initial_coordinate_x or self.final_coordinate_y == self.initial_coordinate_y:
            self.final_coordinate_x = random.randint(0, int(HEIGHT / SIZE) - 1)
            self.final_coordinate_y = random.randint(0, int(WIDTH / SIZE) - 1)
        self.maze = Maze(self.background, self.initial_coordinate_x, self.initial_coordinate_y, self.final_coordinate_x,
                         self.final_coordinate_y)
        self.player = Player(self.initial_coordinate_x, self.initial_coordinate_y)

    def update(self, event):
        if not self.solved and not self.winner:
            self.player.update(self.maze.maze, event)
        if self.player.matrix_pos_x == self.final_coordinate_x and self.player.matrix_pos_y == self.final_coordinate_y:
            self.winner = True

    def initial_game(self):
        self.background.fill(DARKBLUE)
        pygame.draw.rect(self.background, WHITE, [40, 40, 530, 580])
        pygame.draw.rect(self.background, LIGHTBLUE, [40, 100, 530, 450])
        pygame.draw.rect(self.background, BLACK, [110, 150, 380, 350])
        pygame.draw.rect(self.background, BLUE, [110, 150, 380, 100])
        text(self.background, "MAZE ADVENTURES", LIGHTORANGE, FONTSIZE_START, 125, 185)
        text(self.background, "PRESS (ESC) TO CLOSE GAME", INTERMEDIARYORANGE, FONTSIZE_COMMANDS_INTIAL + 5, 150, 375)
        pygame.display.update()
        pygame.time.wait(0)
        text(self.background, "PRESS (S) TO START GAME", INTERMEDIARYORANGE, FONTSIZE_COMMANDS_INTIAL + 5, 160, 350)
        pygame.display.update()
        pygame.time.wait(0)

    def end_of_game(self):
        self.maze.bfs(self.background, self.player)

    def render(self):
        self.background.fill(BLACK)

        self.maze.render(self.background)

        self.player.render(self.background)

        if not self.solved and not self.winner:
            pygame.draw.rect(self.background, RED, [0, HEIGHT, SIZE, SIZE])
            text(self.background, "- PLAYER", WHITE, FONTSIZE_MAZE, 0 + SIZE + 3, HEIGHT + 6)
            pygame.draw.rect(self.background, BEIGE, [0, HEIGHT + SIZE + 1, SIZE, SIZE])
            text(self.background, "- STARTING POINT", WHITE, FONTSIZE_MAZE, 0 + SIZE + 3, HEIGHT + SIZE + 1 + 6)
            pygame.draw.rect(self.background, LIGHTBLUE, [0, HEIGHT + 2 * SIZE + 2, SIZE, SIZE])
            text(self.background, "- GOAL", WHITE, FONTSIZE_MAZE, 0 + SIZE + 3, HEIGHT + 2 * SIZE + 1 + 6)

            text(self.background, "PRESS (R) TO RETRY GAME", WHITE, FONTSIZE_MAZE, 200, HEIGHT)
            text(self.background, "PRESS (Q) TO GIVE UP", WHITE, FONTSIZE_MAZE, 200, HEIGHT + 30)
            text(self.background, "PRESS (ESC) TO CLOSE GAME", WHITE, FONTSIZE_MAZE, 200, HEIGHT + 60)
        elif self.winner:
            text(self.background, "YOU WIN", BLUE, FONTSIZE_MAZE + 3, 200, HEIGHT)
            text(self.background, "PRESS (R) TO RETRY GAME", WHITE, FONTSIZE_MAZE, 200, HEIGHT + 30)
            text(self.background, "PRESS (ESC) TO CLOSE GAME", WHITE, FONTSIZE_MAZE, 200, HEIGHT + 60)
        else:
            text(self.background, "YOU LOSE", RED, FONTSIZE_MAZE + 3, 200, HEIGHT)
            text(self.background, "PRESS (R) TO RETRY GAME", WHITE, FONTSIZE_MAZE, 200, HEIGHT + 30)
            text(self.background, "PRESS (ESC) TO CLOSE GAME", WHITE, FONTSIZE_MAZE, 200, HEIGHT + 60)

        pygame.display.update()

    def run(self):
        self.load()
        while not self.start:
            self.initial_game()
            pygame.display.update()
            if pygame.event.get(pygame.QUIT) or pygame.key.get_pressed()[pygame.K_ESCAPE]:
                pygame.quit()
                sys.exit(0)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                    self.start = True
        pygame.display.update()

        self.background.fill(BLACK)
        self.maze.dfs(self.background)

        while not self.exit:
            if pygame.event.get(pygame.QUIT) or pygame.key.get_pressed()[pygame.K_ESCAPE]:
                self.exit = True
            e = pygame.event.get()
            if self.winner:
                self.background.fill(BLACK)
            for event in e:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.solved = False
                        self.winner = False
                        self.run()
                    if not self.solved and event.key == pygame.K_q and not self.winner:
                        self.background.fill(BLACK)
                        self.end_of_game()
                        self.solved = True
            self.update(e)
            self.render()

        pygame.quit()
        sys.exit(0)


def main():
    mygame = Game()
    mygame.run()


if __name__ == '__main__':
    main()