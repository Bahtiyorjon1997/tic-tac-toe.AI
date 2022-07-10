# to complete this task, I used youtube tutorial and I analyzed Santiago lemma's solusion
import pygame
import numpy as np
import random

class Model:
    def __init__(self, size, grid_size):
        self.size = size
        self.grid_size = grid_size
        self.state = np.zeros((grid_size, grid_size), dtype=np.int64)
        # self.state = np.array([[0, 0, 0], 
        #                        [0, 0, 0],
        #                        [1, 0, 2]])
        self.turn = 1
        self.winner = 0
        self.winning_line = 0

    def in_which_square(self, coordinates):
        x, y = coordinates
        square_size = self.size // self.grid_size
        
        col = x // square_size
        row = y // square_size

        return (row, col)

    def is_free(self, position):
        r, c = position
        return self.state[r][c] == 0

    def claim(self, position, player):
        if player not in [1, 2]:
            raise ValueError("Not a valid player")
        # if self.is_free(position):
        r, c = position
        self.state[r][c] = player
        self.turn += 1
        # else:
            # raise RuntimeError('Spot is taken')

    def unclaim(self, position):
        r, c = position
        self.state[r][c] = 0
        self.turn -= 1

    def get_free_spaces(self):
        free_spaces = []
        for row in range(self.state.shape[0]):
            for col in range(self.state.shape[1]):
                if self.state[row][col] == 0:
                    free_spaces.append((row, col))
        return free_spaces

    
    def check_rows(self):
        for n in range(self.state.shape[0]):
            if (self.state[n][0] != 0 and 
            np.all(self.state[n] == self.state[n][0])):
                if self.state[n][0] == 1:
                    self.winner = 1
                else:
                    self.winner = 2
                self.winning_line = ('row', n)
                return True
        return False

    def check_columns(self):
        for col in range(self.state.shape[1]):
            current_col = []
            for row in range(self.state.shape[0]):
                current_col.append(self.state[row][col])
            if (current_col[0] != 0 and
                current_col.count(current_col[0]) == len(current_col)):
                    if current_col[0] == 1:
                        self.winner = 1
                    else:
                        self.winner = 2
                    self.winning_line = ('col', col)
                    return True
        return False

    def first_diagonal(self):
        values = []
        for xy in range(self.state.shape[0]):
            values.append(self.state[xy][xy])
        if (values[0] != 0 and
            values.count(values[0]) == len(values)):
            if values[0] == 1:
                self.winner = 1
            else:
                self.winner = 2
            return True

    def second_diagonal(self):
        values = []
        y = self.state.shape[0]
        for x in range(self.state.shape[0]):
            y -= 1
            values.append(self.state[x][y])
        if (values[0] != 0 and
            values.count(values[0]) == len(values)):
            if values[0] == 1:
                self.winner = 1
            else:
                self.winner = 2
            return True

    def check_diagonals(self):
            if self.first_diagonal():
                self.winning_line = ('dia', 0)
                return True
            elif self.second_diagonal():
                self.winning_line = ('dia', 1)
                return True
            else:
                return False

    def is_board_full(self):
        for row in range(self.state.shape[0]):
            for col in range(self.state.shape[1]):
                if self.state[row][col] == 0:
                    return False
        return True

    def is_final_state(self):
        return (self.check_rows() or
                self.check_columns() or
                self.check_diagonals() or
                self.is_board_full())

    def generate_random_states(self, qty, moves):
        generated_states = []
        count = qty
        while count > 0:
            scenario = Model(self.size, self.grid_size)
            for move in range(moves):
                player = 2 if move % 2 == 0 else 1
                free_spaces = scenario.get_free_spaces()
                indx = random.randint(0, len(free_spaces) - 1)
                spot = free_spaces[indx]
                scenario.claim(spot, player)
            if not scenario.is_final_state():
                generated_states.append(scenario.state)
                count -= 1

        return generated_states

            
class View(Model):

    def __init__(self, model, screen, screen_color, grid_color, player1_color, player2_color,
                 marks_width, winning_line_width, winning_line_color):
        self.model = model
        self.screen = screen
        self.screen_color = screen_color
        self.grid_color = grid_color
        self.player1_color = player1_color
        self.player2_color = player2_color
        self.marks_width = marks_width
        self.winning_line_width = winning_line_width
        self.winning_line_color = winning_line_color

    def render_grid(self):
        x = 0
        gap = self.model.size / self.model.grid_size
        for n in range(1, self.model.grid_size):
            x = n * gap
            pygame.draw.line(self.screen, self.grid_color, (x, 0),
                             (x, self.model.size), 1)
            pygame.draw.line(self.screen, self.grid_color, (0, x),
                             (self.model.size, x), 1)

    def render_state(self):  # Move to view
        for row in range(self.model.state.shape[0]):
            for col in range(self.model.state.shape[1]):

                # square coordinates
                square_size = self.model.size // self.model.grid_size
                square_center = (
                    (square_size / 2) + (square_size * col),  # x-axis center
                    (square_size / 2) + (square_size * row))  # y-axis center
                s1 = (
                    square_size * col,  # top-left corner of the square
                    square_size * row)
                s2 = (
                    (square_size * col) + square_size,  # top-right corner
                    (square_size * row))
                s3 = (
                    (square_size * col),  # bot-left corner
                    (square_size * row) + square_size)
                s4 = (
                    (square_size * col) + square_size,  # bot-right corner
                    (square_size * row) + square_size)

                if (self.model.state[row][col] == 1):
                    pygame.draw.circle(self.screen,
                                       self.player1_color,
                                       square_center,
                                       (square_size / 2) - 2,
                                       width=self.marks_width)
                if (self.model.state[row][col] == 2):
                    pygame.draw.line(self.screen,
                                     self.player2_color,
                                     s1,
                                     s4,
                                     width=self.marks_width)
                    pygame.draw.line(self.screen,
                                     self.player2_color,
                                     s3,
                                     s2,
                                     width=self.marks_width)

    def draw_winner_line(self):
        line_height = (self.model.size / self.model.grid_size) / 2
        level_height = self.model.size / self.model.grid_size
        dir, order = self.model.winning_line
        if (dir == 'row'):
            start_pos = (0, line_height + (level_height * order))
            end_pos = (self.model.size,
                       line_height + (level_height * order))
            pygame.draw.line(self.screen,
                             self.winning_line_color,
                             start_pos,
                             end_pos,
                             width=self.winning_line_width)
        if (dir == 'col'):
            start_pos = (line_height + (level_height * order), 0)
            end_pos = (line_height + (level_height * order),
                       self.model.size)
            pygame.draw.line(self.screen,
                             self.winning_line_color,
                             start_pos,
                             end_pos,
                             width=self.winning_line_width)
        if (dir == 'dia'):
            if (order == 0):
                start_pos = (0, 0)
                end_pos = (self.model.size, self.model.size)
            if (order == 1):
                start_pos = (self.model.size, 0)
                end_pos = (0, self.model.size)
            pygame.draw.line(self.screen,
                             self.winning_line_color,
                             start_pos,
                             end_pos,
                             width=self.winning_line_width)

    def render_board(self):
        self.screen.fill(self.screen_color)
        self.render_grid()
        self.render_state()

class Controller:

    def __init__(self, size, screen_color, grid_size, grid_color, screen, player1_color,
                 player2_color, marks_width, winning_line_width,
                 winning_line_color):
        self.model = Model(size, grid_size)
        self.view = View(self.model, screen, screen_color, grid_color, player1_color,
                         player2_color, marks_width, winning_line_width,
                         winning_line_color)
        self.grid_color = grid_color

    def click_claim(self):
        mouse_position = pygame.mouse.get_pos()
        row, col = self.model.in_which_square((mouse_position))

        if (self.model.turn % 2 == 0):
            player = 2
        else:
            player = 1

        if self.model.is_free((row, col)):
            self.model.claim((row, col), player)
        else:
            print('Spot is taken, please select another one')

    def reset_board(self):
        self.model.turn = 1
        self.model.winner = 0
        for row in range(self.model.state.shape[0]):
            for col in range(self.model.state.shape[1]):
                self.model.state[row][col] = 0
