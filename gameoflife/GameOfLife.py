import pygame
import sys
import random


class GameOfLife:

    def __init__(self):
        pygame.init()
        self.SIZE = (self.WIDTH, self.HEIGHT) = (640, 480)
        self.VOID_COLOR = (0, 0, 0)
        self.ALIVE_COLOR = (0, 255, 30)
        self.CELL_RADIUS = 4
        self.CELL_SIZE = int(self.CELL_RADIUS * 2)
        self.screen = pygame.display.set_mode(self.SIZE)
        self.cols = self.WIDTH // self.CELL_SIZE
        self.rows = self.HEIGHT // self.CELL_SIZE
        self.grids = [[], []]
        self.grids[0] = [[0 for c in range(self.cols)] for r in range(self.rows)]
        self.grids[1] = [[0 for c in range(self.cols)] for r in range(self.rows)]
        self.active_grid = 0
        self.last_update_completed = 0
        self.MAX_FPS = 20
        self.pause = False

    def set_grid(self, val=None):
        for i in range(self.rows):
            for j in range(self.cols):
                if val is None:
                    self.grids[self.active_grid][i][j] = random.choice([0, 1])
                else:
                    self.grids[self.active_grid][i][j] = val

    def life_rules(self, i, j):
        if self.alive_neighbors(i, j) < 2:  # UNDERPOPULATION
            self.grids[(self.active_grid + 1) % 2][i][j] = 0
        elif self.alive_neighbors(i, j) > 3:  # OVERPOPULATION
            self.grids[(self.active_grid + 1) % 2][i][j] = 0
        elif self.alive_neighbors(i, j) == 3:  # BIRTH
            self.grids[(self.active_grid + 1) % 2][i][j] = 1
        else:
            self.grids[(self.active_grid + 1) % 2][i][j] = self.grids[self.active_grid][i][j]

    def alive_neighbors(self, i, j):
        count = 0
        for r in range(i - 1, i + 2):
            r %= self.rows
            for c in range(j - 1, j + 2):
                if r == i and c == j:
                    continue
                c %= self.cols
                if self.grids[self.active_grid][r][c]:
                    count += 1

        return count

    def update_generation(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.life_rules(i, j)
        self.active_grid = (self.active_grid + 1) % 2

    def draw_grid(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.grids[self.active_grid][i][j] == 1:
                    color = self.ALIVE_COLOR
                else:
                    color = self.VOID_COLOR
                pygame.draw.circle(self.screen, color,
                                   (j * self.CELL_SIZE + self.CELL_RADIUS,
                                    i * self.CELL_SIZE + self.CELL_RADIUS),
                                   self.CELL_RADIUS, 0)
        pygame.display.flip()

    def draw_dot(self, pos):
        if self.grids[self.active_grid][pos[1] // self.CELL_SIZE][pos[0] // self.CELL_SIZE]:
            self.grids[self.active_grid][pos[1] // self.CELL_SIZE][pos[0] // self.CELL_SIZE] = 0
            color = self.VOID_COLOR
        else:
            self.grids[self.active_grid][pos[1] // self.CELL_SIZE][pos[0] // self.CELL_SIZE] = 1
            color = self.ALIVE_COLOR
        pygame.draw.circle(self.screen, color,
                           (pos[1] * self.CELL_SIZE + self.CELL_RADIUS,
                            pos[0] * self.CELL_SIZE + self.CELL_RADIUS),
                           self.CELL_RADIUS, 0)
        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.unicode == 'r':
                    self.set_grid()
                    self.draw_grid()
                elif event.unicode == 's':
                    if self.pause:
                        self.pause = False
                    else:
                        self.pause = True
                elif event.unicode == 'q':
                    sys.exit()
                elif event.unicode == 'f':
                    self.set_grid(0)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                self.draw_dot(pos)
            if event.type == pygame.QUIT:sys.exit()

    def run(self):
        self.set_grid()
        while True:
            self.handle_events()
            if self.pause:
                self.draw_grid()
                continue
            self.draw_grid()
            self.update_generation()
            self.cap_fps()

    def cap_fps(self):
        ms_between_updates = (1.0 / self.MAX_FPS) * 1000
        now = pygame.time.get_ticks()
        ms_since_last_update = now - self.last_update_completed
        time_to_sleep = ms_between_updates - ms_since_last_update
        if time_to_sleep > 0:
            pygame.time.delay((int(time_to_sleep)))
        self.last_update_completed = now


if __name__ == '__main__':
    game = GameOfLife()
    game.run()
