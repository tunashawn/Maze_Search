import sys

from Maze import Maze
from Player import Player
from Settings import *


class Game:
    def __init__(self):
        try:
            pygame.init()
        except:
            print('The pygame module did not start successfully')

        self.start_coordinate_x = 0
        self.start_coordinate_y = 0
        self.destination_coordinate_x = 0
        self.destination_coordinate_y = 0
        self.start = False
        self.solved = False
        self.winner = False
        self.exit = False
        self.maze = None

    def load(self):
        self.background = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption('Maze Game')

        # Set the start point at the top left of the maze
        self.start_coordinate_x = 0
        self.start_coordinate_y = 0
        self.player = Player(0, 0)

        # Set the destination point at the right end of the maze
        self.destination_coordinate_x = int(WIDTH / SIZE) - 1
        self.destination_coordinate_y = int(HEIGHT / SIZE) - 1
        self.maze = Maze(self.background, self.start_coordinate_x, self.start_coordinate_y, self.destination_coordinate_x,
                         self.destination_coordinate_y)

    def update(self, event):
        if not self.solved and not self.winner:
            self.player.update(self.maze.maze, event)
        if self.player.matrix_pos_x == self.destination_coordinate_x and self.player.matrix_pos_y == self.destination_coordinate_y:
            self.winner = True

    def initial_game(self):
        self.background.fill(BLACK)
        text(self.background, "MAZE ADVENTURES",WHITE, 70, 460, 300)
        text(self.background, "A course project of CS 3310 - Introduction to Artificial Intelligent", WHITE, FONTSIZE_START - 5, 200, 400)
        text(self.background, "taught by Prof. Huong Thanh Le at Troy University, Hanoi campus.", WHITE, FONTSIZE_START - 5, 200, 440)
        text(self.background, "Student: Son Tuan Vu", WHITE, 30, 530, 500)
        text(self.background, "ID: 1575302", WHITE, 30, 530, 530)
        text(self.background, "Semester: FALL 2021", WHITE, 30, 530, 560)
        text(self.background, "PRESS (ESC) TO CLOSE GAME", WHITE, FONTSIZE_COMMANDS_INTIAL + 2, 530, 660)
        text(self.background, "Credits: This game is a modified version from MAZE ADVENTURE", WHITE,
             FONTSIZE_COMMANDS_INTIAL + 2, 400, 780)
        text(self.background, "of DanMke and lukassxp (Github)", WHITE, FONTSIZE_COMMANDS_INTIAL + 2, 530, 810)
        pygame.display.update()
        pygame.time.wait(300)
        text(self.background, "PRESS (S) TO START GAME", WHITE, FONTSIZE_COMMANDS_INTIAL + 2, 530, 630)
        pygame.display.update()
        pygame.time.wait(300)

    def render(self):
        self.background.fill(BLACK)

        self.maze.render(self.background)

        self.player.render(self.background)

        if not self.solved and not self.winner:
            pygame.draw.rect(self.background, WHITE,[WIDTH + 5, 0, 25, 25])
            pygame.draw.rect(self.background, BLUE, [WIDTH + 5, 30, 25, 25])
            pygame.draw.rect(self.background, RED,  [WIDTH + 5, 60, 25, 25])
            text(self.background, "PLAYER",         WHITE, FONTSIZE_MAZE, WIDTH + 35, 5)
            text(self.background, "STARTING POINT", WHITE, FONTSIZE_MAZE, WIDTH + 35, 35)
            text(self.background, "GOAL",           WHITE, FONTSIZE_MAZE, WIDTH + 35, 65)

            text(self.background, "-------------------------------------------", WHITE, FONTSIZE_MAZE, WIDTH + 5, 95)
            text(self.background, "PRESS (R) TO RETRY GAME",    WHITE, FONTSIZE_MAZE, WIDTH + 5, 125)
            text(self.background, "PRESS (Q) TO GIVE UP",       WHITE, FONTSIZE_MAZE, WIDTH + 5, 155)
            text(self.background, "PRESS (ESC) TO CLOSE GAME",  WHITE, FONTSIZE_MAZE, WIDTH + 5, 185)

        elif self.winner:
            text(self.background, "YOU WIN!",                   BLUE, FONTSIZE_MAZE + 5, WIDTH + 5, 5)
            text(self.background, "PRESS (R) TO RETRY GAME",    WHITE, FONTSIZE_MAZE, WIDTH + 5, 35)
            text(self.background, "PRESS (ESC) TO CLOSE GAME",  WHITE, FONTSIZE_MAZE, WIDTH + 5, 65)

        else:
            text(self.background, "YOU LOSE!",                  RED, FONTSIZE_MAZE + 5, WIDTH + 5, 5)
            text(self.background, "PRESS (R) TO RETRY GAME",    WHITE, FONTSIZE_MAZE, WIDTH + 5, 35)
            text(self.background, "PRESS (ESC) TO CLOSE GAME",  WHITE, FONTSIZE_MAZE, WIDTH + 5, 65)

        pygame.display.update()

    def run(self):
        self.load()
        self.start = False

        while not self.start:
            self.initial_game()
            pygame.display.update()
            if pygame.event.get(pygame.QUIT) or pygame.key.get_pressed()[pygame.K_ESCAPE]:
                pygame.quit()
                sys.exit(0)
            for event in pygame.event.get():
                # PRESSED S
                if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                    self.start = True
                    self.background.fill(BLACK)
                    self.maze.dfs(self.background)

        while not self.exit:
            if pygame.event.get(pygame.QUIT) or pygame.key.get_pressed()[pygame.K_ESCAPE]:
                self.exit = True
            e = pygame.event.get()
            if self.winner:
                self.background.fill(BLACK)

            # in game events
            for event in e:
                if event.type == pygame.KEYDOWN:

                    # PRESS (R): Reset the game
                    if event.key == pygame.K_r:
                        self.solved = False
                        self.winner = False
                        self.run()

                    # PRESS (Q): Solve the maze using A* Algorithm
                    if not self.solved and event.key == pygame.K_q and not self.winner:
                        self.background.fill(BLACK)
                        self.maze.a_star_search(self.background, self.player)
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