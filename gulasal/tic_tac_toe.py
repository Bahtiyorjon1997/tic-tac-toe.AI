import copy
import sys
import pygame
import random
import numpy as np

from necessary_values import LINE_SIZE

BOARD_WIDTH = 800
BOARD_HEIGHT = 800

ROWS = 3
COLUMNS = 3
SQUARE_SIZE = BOARD_WIDTH // COLUMNS

LINE_SIZE = 10
CIRCLE_SIZE = 10
CROSS_SIZE = 15

RADIUS = SQUARE_SIZE // 4

OFFSET = 60

# --- COLORS ---

BACKGROUND_COLOR = (255, 204, 255)
BORDER_LINE_COLOR = (255, 0, 255)
CIRCLE_SIGN_COLOR = (152, 0, 0)
CROSS_SIGN_COLOR = (76, 0, 153)



pygame.init()
screen = pygame.display.set_mode( (BOARD_WIDTH, BOARD_HEIGHT) )
pygame.display.set_caption('TIC_TAC_TOE - AI')
screen.fill( BACKGROUND_COLOR )

# --- CLASSES ---

class Board:

    def __init__(self):
        self.cells = np.zeros( (ROWS, COLUMNS) )
        self.free_cells = self.cells # [squares]
        self.signed_cells = 0

    def last_step(self, game_process=False):
        
            #returning 0 if there is no win yet
            #returning 1 if player 1 wins
            #returning 2 if player 2 wins
        

        # possible vertical wins created
        for col in range(COLUMNS):
            if self.cells[0][col] == self.cells[1][col] == self.cells[2][col] != 0:
                if game_process:
                    color = CIRCLE_SIGN_COLOR if self.cells[0][col] == 2 else CROSS_SIGN_COLOR
                    position_x = (col * SQUARE_SIZE + SQUARE_SIZE // 2, 20)
                    position_y = (col * SQUARE_SIZE + SQUARE_SIZE // 2, BOARD_HEIGHT - 20)
                    pygame.draw.line(screen, color, position_x, position_y, LINE_SIZE)
                return self.cells[0][col]

        # possible horizontal wins created
        for row in range(ROWS):
            if self.cells[row][0] == self.cells[row][1] == self.cells[row][2] != 0:
                if game_process:
                    color = CIRCLE_SIGN_COLOR if self.cells[row][0] == 2 else CROSS_SIGN_COLOR
                    position_x = (20, row * SQUARE_SIZE + SQUARE_SIZE // 2)
                    position_y = (BOARD_WIDTH - 20, row * SQUARE_SIZE + SQUARE_SIZE // 2)
                    pygame.draw.line(screen, color, position_x, position_y, LINE_SIZE)
                return self.cells[row][0]

        # descending line diagonally 
        if self.cells[0][0] == self.cells[1][1] == self.cells[2][2] != 0:
            if game_process:
                color = CIRCLE_SIGN_COLOR if self.cells[1][1] == 2 else CROSS_SIGN_COLOR
                position_x = (20, 20)
                position_y = (BOARD_WIDTH - 20, BOARD_HEIGHT - 20)
                pygame.draw.line(screen, color, position_x, position_y, CROSS_SIZE)
            return self.cells[1][1]

        # ascending line diagonally
        if self.cells[2][0] == self.cells[1][1] == self.cells[0][2] != 0:
            if game_process:
                color = CIRCLE_SIGN_COLOR if self.cells[1][1] == 2 else CROSS_SIGN_COLOR
                position_x = (20, BOARD_HEIGHT - 20)
                position_y = (BOARD_WIDTH - 20, 20)
                pygame.draw.line(screen, color, position_x, position_y, CROSS_SIZE)
            return self.cells[1][1]

        # if no win yet:
        return 0

    def put_mark(self, row, col, player):
        self.cells[row][col] = player
        self.signed_cells += 1

    def free_cell(self, row, col):
        return self.cells[row][col] == 0

    def get_free_cells(self):
        free_cells = []
        for row in range(ROWS):
            for col in range(COLUMNS):
                if self.free_cell(row, col):
                    free_cells.append( (row, col) )
        
        return free_cells

    def cells_full(self):
        return self.signed_cells == 9

    def cells_empty(self):
        return self.signed_cells == 0

class AI:

    def __init__(self, level=1, player=2):
        self.level = level
        self.player = player

    # --- RANDOM ---

    def random_choice(self, board):
        free_cells = board.get_free_cells()
        idx = random.randrange(0, len(free_cells))

        return free_cells[idx] # (row, col)

    # --- MINIMAX ---

    def minimax(self, board, maximizing):
        
        # terminal case
        case = board.last_step()

        # the first player won
        if case == 1:
            return 1, None # evaluation, moving

        # the second player won
        if case == 2:
            return -1, None

        # putting marks
        elif board.cells_full():
            return 0, None

        if maximizing:
            max_evaluation = -100
            good_position = None
            free_cells = board.get_free_cells()

            for (row, col) in free_cells:
                temperorary_board_screen = copy.deepcopy(board)
                temperorary_board_screen.put_mark(row, col, 1)
                evaluation = self.minimax(temperorary_board_screen, False)[0]
                if evaluation > max_evaluation:
                    max_evaluation = evaluation
                    good_position = (row, col)

            return max_evaluation, good_position

        elif not maximizing:
            min_evaluation = 100
            good_position = None
            free_cells = board.get_free_cells()

            for (row, col) in free_cells:
                temperorary_board_screen = copy.deepcopy(board)
                temperorary_board_screen.put_mark(row, col, self.player)
                evaluation = self.minimax(temperorary_board_screen, True)[0]
                if evaluation < min_evaluation:
                    min_evaluation = evaluation
                    good_position = (row, col)

            return min_evaluation, good_position

    # --- Evaluation ---

    def evaluation(self, main_board):
        if self.level == 0:
            # choosing randomly
            evaluation = 'random'
            moving = self.random_choice(main_board)
        else:
            # choosing by minimax algorithm
            evaluation, moving = self.minimax(main_board, False)

        print(f'AI has chosen to mark the square in pos {moving} with an evaluation of: {evaluation}')

        return moving # [row, column]

class Game:

    def __init__(self):
        self.board = Board()
        self.ai = AI()
        self.player = 1   #1-cross  #2-circles
        self.gamemode = 'ai' # [pvp or ai]
        self.running = True
        self.display_game_line()

    # --- DRAW METHODS ---

    def display_game_line(self):
        # bg
        screen.fill( BACKGROUND_COLOR )

        # vertical
        pygame.draw.line(screen, BORDER_LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, BOARD_HEIGHT), LINE_SIZE)
        pygame.draw.line(screen, BORDER_LINE_COLOR, (BOARD_WIDTH - SQUARE_SIZE, 0), (BOARD_WIDTH - SQUARE_SIZE, BOARD_HEIGHT), LINE_SIZE)

        # horizontal
        pygame.draw.line(screen, BORDER_LINE_COLOR, (0, SQUARE_SIZE), (BOARD_WIDTH, SQUARE_SIZE), LINE_SIZE)
        pygame.draw.line(screen, BORDER_LINE_COLOR, (0, BOARD_HEIGHT - SQUARE_SIZE), (BOARD_WIDTH, BOARD_HEIGHT - SQUARE_SIZE), LINE_SIZE)

    def drawing_sign(self, row, col):
        if self.player == 1:
            
            initial_descending = (col * SQUARE_SIZE + OFFSET, row * SQUARE_SIZE + OFFSET)
            final_descending = (col * SQUARE_SIZE + SQUARE_SIZE - OFFSET, row * SQUARE_SIZE + SQUARE_SIZE - OFFSET)
            pygame.draw.line(screen, CROSS_SIGN_COLOR, initial_descending, final_descending, CROSS_SIZE)
            
            initial_ascending = (col * SQUARE_SIZE + OFFSET, row * SQUARE_SIZE + SQUARE_SIZE - OFFSET)
            final_ascending = (col * SQUARE_SIZE + SQUARE_SIZE - OFFSET, row * SQUARE_SIZE + OFFSET)
            pygame.draw.line(screen, CROSS_SIGN_COLOR, initial_ascending, final_ascending, CROSS_SIZE)
        
        elif self.player == 2:
            
            board_center = (col * SQUARE_SIZE + SQUARE_SIZE // 2, row *SQUARE_SIZE + SQUARE_SIZE // 2)
            pygame.draw.circle(screen, CIRCLE_SIGN_COLOR, board_center, RADIUS, CIRCLE_SIZE)

    # --- necessary methods ---

    def process_game(self, row, col):
        self.board.put_mark(row, col, self.player)
        self.drawing_sign(row, col)
        self.switch_player()

    def switch_player(self):
        self.player = self.player % 2 + 1

    def switch_game_mode(self):
        self.gamemode = 'ai' if self.gamemode == 'pvp' else 'pvp'

    def game_finished(self):
        return self.board.last_step(game_process=True) != 0 or self.board.cells_full()

    def reset(self):
        self.__init__()

def main():

    game = Game()
    board = game.board
    ai = game.ai

    # --- loop ---

    while True:
        
        
        for event in pygame.event.get():

            
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            
            if event.type == pygame.KEYDOWN:

                
                if event.key == pygame.K_g:
                    game.switch_game_mode()

                
                if event.key == pygame.K_r:
                    game.reset()
                    board = game.board
                    ai = game.ai

                
                if event.key == pygame.K_0:
                    ai.level = 0
                
                
                if event.key == pygame.K_1:
                    ai.level = 1

           
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                row = pos[1] // SQUARE_SIZE
                col = pos[0] // SQUARE_SIZE
                
                
                if board.free_cell(row, col) and game.running:
                    game.process_game(row, col)

                    if game.game_finished():
                        game.running = False


        # AI call
        if game.gamemode == 'ai' and game.player == ai.player and game.running:

            
            pygame.display.update()

            # evaluation
            row, col = ai.evaluation(board)
            game.process_game(row, col)

            if game.game_finished():
                game.running = False
            
        pygame.display.update()

main()