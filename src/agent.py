from square import Square
from piece import *
from const import *
from move import Move
import numpy as np
from collections import defaultdict
from node import Node
from montecarlo import SearchTree
import copy
import random
import math
import time

class Agent:
    def __init__(self):
        self.debug = False  
        # EVALUATIVE PIECES
        self.evaluate = ['p', 'r', 'c', 'h', 'P', 'R', 'C', 'H']
        # PIECE WEIGHTS
        self.weights = {
            'p': -30,
            'g': -120,
            'e':  -120,
            'h':  -270,
            'c': -285,
            'r': -600,
            'k': -6000,
            'P': 30,
            'G': 120,
            'E':  120,
            'H':  270,
            'C': 285,
            'R': 600,
            'K': 6000
        }
        # UPPER PIECE SQUARE TABLES
        self.PST_upper = {
            # PAWN SQUARE TABLE
            'P':
            [ 0,   3,   6,   9,   12,   9,   6,   3,   0, 
             18,  36,  56,  80,  120,  80,  56,  36,  18,
             14,  26,  42,  60,   80,  60,  42,  26,  14,
             10,  20,  30,  34,   40,  34,  30,  20,  10,
              6,  12,  18,  18,   20,  18,  18,  12,   6, 
              2,   0,   8,   0,    8,   0,   8,   0,   2,  
              0,   0,  -2,   0,    4,   0,  -2,   0,   0,
              0,   0,   0,   0,    0,   0,   0,   0,   0,     
              0,   0,   0,   0,    0,   0,   0,   0,   0,
              0,   0,   0,   0,    0,   0,   0,   0,   0
            ],
            # SKIP GUARD
            # SKIP ELEPHANT
            # HORSE SQUARE TABLE
            'H':
                [ 4,   8,  16,  12,    4,  12,  16,   8,   4, 
              4,  10,  28,  16,    8,  16,  28,  10,   4,
             12,  14,  16,  20,   18,  20,  16,  14,  12,
              8,  24,  18,  24,   20,  24,  18,  24,   8,
              6,  16,  14,  18,   16,  18,  14,  16,   6, 
              4,  12,  16,  14,   12,  14,  16,  12,   4,
              2,   6,   8,   6,   10,   6,   8,   6,   2,
              4,   2,   8,   8,    4,   8,   8,   2,   4,     
              0,   2,   4,   4,   -2,   4,   4,   2,   0,
              0,  -4,   0,   0,    0,   0,   0,  -4,   0,
            ],
            # CANNON SQUARE TABLE
            'C':[ 6,   4,   0, -10,  -12, -10,   0,   4,   6,
              2,   2,   0,  -4,  -14,  -4,   0,   2,   2,
              2,   2,   0, -10,   -8, -10,   0,   2,   2,
              0,   0,  -2,   4,   10,   4,  -2,   0,   0,
              0,   0,   0,   2,    8,   2,   0,   0,   0, 
             -2,   0,   4,   2,    6,   2,   4,   0,  -2,
              0,   0,   0,   2,    4,   2,   0,   0,   0,
              4,   0,   8,   6,   10,   6,   8,   0,   4,     
              0,   2,   4,   6,    6,   6,   4,   2,   0,
              0,   0,   2,   6,    6,   6,   2,   0,   0,
            ],
            # ROOK SQUARE TABLE
            'R':[14,  14,  12,  18,   16,  18,  12,  14,  14,
             16,  20,  18,  24,   26,  24,  18,  20,  16,
             12,  12,  12,  18,   18,  18,  12,  12,  12,
             12,  18,  16,  22,   22,  22,  16,  18,  12,
             12,  14,  12,  18,   18,  18,  12,  14,  12, 
             12,  16,  14,  20,   20,  20,  14,  16,  12,
              6,  10,   8,  14,   14,  14,   8,  10,   6,
              4,   8,   6,  14,   12,  14,   6,   8,   4,     
              8,   4,   8,  16,    8,  16,   8,   4,   8,
             -2,  10,   6,  14,   12,  14,   6,  10,  -2,
            ]
        }
        # LOWER PIECE SQUARE TABLES
        self.PST_lower = {
            # PAWN SQUARE TABLE
            'p':[ 
             0,   0,   0,   0,   0,   0,   0,   0,   0,
             0,   0,   0,   0,   0,   0,   0,   0,   0,
             0,   0,   0,   0,   0,   0,   0,   0,   0,
             0,   0,  -2,   0,   4,   0,  -2,   0,   0,
             2,   0,   8,   0,   8,   0,   8,   0,   2,
             6,  12,  18,  18,  20,  18,  18,  12,   6,
             10,  20,  30,  34,  40,  34,  30,  20,  10,
             14,  26,  42,  60,  80,  60,  42,  26,  14,
             18,  36,  56,  80, 120,  80,  56,  36,  18,
             0,   3,   6,   9,  12,   9,   6,   3,   0,
            ],
            # SKIP GUARD
            # SKIP ELEPHANT
            # HORSE SQUARE TABLE
            'h':[ 
             0,  -4,   0,   0,   0,   0,   0,  -4,   0,
             0,   2,   4,   4,  -2,   4,   4,   2,   0,
             4,   2,   8,   8,   4,   8,   8,   2,   4,
             2,   6,   8,   6,  10,   6,   8,   6,   2,
             4,  12,  16,  14,  12,  14,  16,  12,   4,
             6,  16,  14,  18,  16,  18,  14,  16,   6,
             8,  24,  18,  24,  20,  24,  18,  24,   8,
             12,  14,  16,  20,  18,  20,  16,  14,  12,
             4,  10,  28,  16,   8,  16,  28,  10,   4,
             4,   8,  16,  12,   4,  12,  16,   8,   4,
            ],
            # CANNON SQUARE TABLE
            'c':[ 
             0,   0,   2,   6,   6,   6,   2,   0,   0,
             0,   2,   4,   6,   6,   6,   4,   2,   0,
             4,   0,   8,   6,  10,   6,   8,   0,   4,
             0,   0,   0,   2,   4,   2,   0,   0,   0,
             -2,   0,   4,   2,   6,   2,   4,   0,  -2,
             0,   0,   0,   2,   8,   2,   0,   0,   0,
             0,   0,  -2,   4,  10,   4,  -2,   0,   0,
             2,   2,   0, -10,  -8, -10,   0,   2,   2,
             2,   2,   0,  -4, -14,  -4,   0,   2,   2,
             6,   4,   0, -10, -12, -10,   0,   4,   6,
            ],
            # ROOK SQUARE TABLE
            'r':[ 
             -2,  10,   6,  14,  12,  14,   6,  10,  -2,
             8,   4,   8,  16,   8,  16,   8,   4,   8,
             4,   8,   6,  14,  12,  14,   6,   8,   4,
             6,  10,   8,  14,  14,  14,   8,  10,   6,
             12,  16,  14,  20,  20,  20,  14,  16,  12,
             12,  14,  12,  18,  18,  18,  12,  14,  12,
             12,  18,  16,  22,  22,  22,  16,  18,  12,
             12,  12,  12,  18,  18,  18,  12,  12,  12,
             16,  20,  18,  24,  26,  24,  18,  20,  16,
             14,  14,  12,  18,  16,  18,  12,  14,  14,
            ],
        }  
        
    def print_row(self, rows):
        print("----------------------------------------------")
        for row in range(PIECE_ROWS):
            for column in range(PIECE_COLUMNS):    
                print(rows[row][column], end = " ")
            print("\n")
        print("-----------------------------------------------")
                                                          
    def calculate_all_possible_moves(self, board, upper, level):
        pathDictionary = {}
        pathDictionary.clear()
        # x = first index y = second index
        # temp_board = 'r00000000R/h0c0000C0H/e00000000E/g00000000G/k00000000K/g00000000G/e00000000E/h0c0000C0H/r00000000R'
        # temp_board = 'r00p00P00R/h0c0000C0H/e00p00P00E/g00000000G/k00p00P00K/g00000000G/e00p00P00E/h0c0000C0H/r00p00P00R'
        # temp_board = 'r00000000R/h00000000H/e00p00P00E/g00000000G/k00p00P00K/g00000000G/e00p00P00E/h00000000H/r00p00P00R'
        # temp_board = '0000000000/0000000000/0000000000/0000000000/k00p00P00K/0000000000/0000000000/0000000000/0000000000'
        # temp_board = '0000000000/r0rP0000P0/0000000000/0000000000/k00000000K/0000000000/0000000000/0000000000/0000000000'
        # temp_board = '0000000000/0000000000/0000000000/0000000000/k00000P00K/0000000000/0000000000/0000000000/0000000000'
        # temp_board = 'rhegkgehr/000000000/0c00000c0/p0p0p0p0p/000000000/000000000/P0P0P0P0P/0C00000C0/000000000/RHEGKGEHR'
        # temp_board = 'R0eakaehr/000000000/000000000/p0p0p0p0p/000000000/000000000/P0P0P0P0P/000000000/000000000/RHEAKAEHR'
        # Where uppercase is other player
        # Will turn this into array
        split_board = board.split('/')
        self.print_row(split_board)
        st = time.time()
        if level == "beginner":
            # RANDOM MOVE CALL
            possible_states = self.next_states(split_board, upper)
            best_move = possible_states[random.randint(0, len(possible_states) - 1)]
            self.print_row(best_move)
            
        
        elif level == "experienced":
            # MINIMAX CALL
            # print("is check")
            # if self.is_check(split_board, upper):
            #     print("is check")
            #     states = []
            #     possible_states = self.next_states(split_board, upper)
            #     for i in possible_states:
            #         if not self.is_check(i, not upper):
            #             states.append(i)
            #             print(i)
            #     if states == []:
            #         return []
            #     best_move = states[random.randint(0, len(states) - 1)]
            # else:
            value, best_move = self.minimax(split_board, 3, -math.inf, math.inf, True, pathDictionary)
            if best_move == None:
                best_move = self.next_states(split_board, True)
                if best_move != None:
                    best_move = best_move[0]
            self.print_row(best_move)
            print("END VALUE = " + str(value))

            
        else:
            # MONTE CARLO CALL
            best_move = self.monte_carlo(split_board, True)
            
        et = time.time()
        runtime = et - st
        print("EXECUTION TIME: " + str(runtime))
        return best_move    
    
    def evaluation(self, rows, upper):
        if self.debug:
            st = time.time()
        value = 0
        
        if self.is_check(rows, not upper):
            # print('choosing check move')
            value = 100
        
        
        for row in range(PIECE_ROWS):
            for column in range(PIECE_COLUMNS): 
                if (rows[row][column] == '0'):
                    pass
                else:
                    p = rows[row][column]
                    value += self.weights[p]
                    if p in self.evaluate:
                        if p.isupper():
                            value += self.PST_upper[p][(row*9)+column]
                        else:
                            value -= self.PST_lower[p][(row*9)+column]                    
        if self.debug:
            et = time.time()
            runtime = et - st
            print("EVALUATION EXECUTION TIME: " + f"{runtime:.15f}")
        if upper:
            return value
        return -value     

    # Returns all moves from a given board and colour and returns them as boards
    def next_states(self, rows, upper): 

        if self.debug:
            st = time.time()
        possible_states = []
                                
        for row in range(PIECE_ROWS):
            for column in range(PIECE_COLUMNS):
                # Find every team piece and calculate all moves
                if (rows[row][column].isupper() and upper and rows[row][column] != '0') or (rows[row][column].islower() and not upper and rows[row][column] != '0'):
                    current_piece = rows[row][column]  
                    moves = self.calculate_moves(rows, current_piece, row, column, upper, bool=True)
                    # print("PIECE = " + str(current_piece))
                    # Add possible moves to array
                    for move in moves:
                        # self.print_row(move)
                        possible_states.append(move)
        if self.debug:
            et = time.time()
            runtime = et - st
            print("NEXT STATES EXECUTION TIME: " + f"{runtime:.15f}")
        if len(possible_states) == 0:
            return []
        else:
            return possible_states
 
    def is_terminal_state(self, rows, upper):     
        if self.debug:
            st = time.time()                   
        for row in range(PIECE_ROWS):
            for column in range(PIECE_COLUMNS):
                # Find every team piece and calculate all moves
                if (rows[row][column] != '0') and ((upper and rows[row][column].isupper()) or (not upper and rows[row][column].islower())):
                    p = rows[row][column]     
                    moves = self.calculate_moves(rows, p, row, column, upper, bool=True)
                    # Add possible moves to array
                    if len(moves) >= 1:
                        if self.debug:
                            et = time.time()
                            runtime = et - st
                            print("IS TERMINAL STATE EXECUTION TIME: " + f"{runtime:.15f}")
                        return False
        if self.debug:
            et = time.time()
            runtime = et - st
            print("IS TERMINAL STATE EXECUTION TIME: " + f"{runtime:.15f}")
        return True
                      
    def calculate_moves(self, rows, piece, row, column, upper, bool=True):
        moves = []
        # [rkeakaekr],
        # [000000000],
        # [0c00000c0],
        # [p0p0p0p0p],
        # [000000000],
        # [000000000],
        # [P0P0P0P0P],
        # [0C00000C0],
        # [000000000],
        # [RKEAKAEKR]
        
        def row_in_range(row):
            if row < 0 or row > 9:
                return False
            return True
        
        def column_in_range(row):
            if row < 0 or row > 8:
                return False
            return True
        
        def is_valid(moving_row, moving_column):
            if upper:
                if not rows[moving_row][moving_column].isupper() and (rows[moving_row][moving_column] == '0' or rows[moving_row][moving_column].islower()):
                    return True
            else:
                if not rows[moving_row][moving_column].islower() and (rows[moving_row][moving_column] == '0' or rows[moving_row][moving_column].isupper()):
                    return True
            return False
                
        def next_knight_moves(row, column):
            possible_moves = []
            #Check top
            if row_in_range(row-1) and column_in_range(column) and rows[row-1][column] == '0':
                possible_moves.append((row-2, column-1))
                possible_moves.append((row-2, column+1))
            #Check bottom
            if row_in_range(row+1) and column_in_range(column) and rows[row+1][column] == '0':
                possible_moves.append((row+2, column-1))
                possible_moves.append((row+2, column+1))
            #Check Left
            if row_in_range(row) and column_in_range(column-1) and rows[row][column-1] == '0':
                possible_moves.append((row-1, column-2))
                possible_moves.append((row+1, column-2))
            #Check Right
            if row_in_range(row) and column_in_range(column+1) and rows[row][column+1] == '0':
                possible_moves.append((row-1, column+2))
                possible_moves.append((row+1, column+2))
                
            for possible_move in possible_moves:
                possible_row, possible_column = possible_move
                if row_in_range(possible_row) and column_in_range(possible_column):
                    if is_valid(possible_row, possible_column):
                    # if is_valid(possible_row, possible_column) and not (rows[possible_row][possible_column] == 'k' or rows[possible_row][possible_column] == 'K'):
                        if rows[possible_row][possible_column] == 'k' or rows[possible_row][possible_column] == 'K':
                            moved_rows = self.move(rows, row, column, possible_row, possible_column, upper, piece)
                            if not bool:
                                moves.append(moved_rows)
                        else:
                            moved_rows = self.move(rows, row, column, possible_row, possible_column, upper, piece)
                            if bool:
                                # if True:
                                if not self.in_check(moved_rows, upper) and not self.flying_general(moved_rows) and not (rows[possible_row][possible_column] == 'k' or rows[possible_row][possible_column] == 'K'):
                                    moves.append(moved_rows)
                            else:
                                moves.append(moved_rows)
    
        def next_rook_moves(row, column):
            #Downward Check
            def downward_check():
                counter = 1
                next_move = (row + counter, column)
                while(row_in_range(row + counter)):
                    next_move = (row + counter, column)
                    possible_row, possible_column = next_move
                    if not (rows[possible_row][possible_column] == '0' or (upper and rows[possible_row][possible_column].islower()) or (not upper and rows[possible_row][possible_column].isupper())):
                        return
                    if (upper and rows[possible_row][possible_column].islower()) or (not upper and rows[possible_row][possible_column].isupper()):
                        # if (rows[possible_row][possible_column] == 'k' or rows[possible_row][possible_column] == 'K'):
                        #     return
                        if rows[possible_row][possible_column] == 'k' or rows[possible_row][possible_column] == 'K':
                            moved_rows = self.move(rows, row, column, possible_row, possible_column, upper, piece)
                            if not bool:
                                moves.append(moved_rows)
                        else:
                            moved_rows = self.move(rows, row, column, possible_row, possible_column, upper, piece)
                            if bool:
                                if not self.in_check(moved_rows, upper) and not self.flying_general(moved_rows):
                                    moves.append(moved_rows)
                            else:
                                moves.append(moved_rows)
                        return
                    # if (rows[possible_row][possible_column] == 'k' or rows[possible_row][possible_column] == 'K'):
                    #     return
                    else:
                        if rows[possible_row][possible_column] == 'k' or rows[possible_row][possible_column] == 'K':
                            moved_rows = self.move(rows, row, column, possible_row, possible_column, upper, piece)
                            if not bool:
                                moves.append(moved_rows)
                        else:
                            moved_rows = self.move(rows, row, column, possible_row, possible_column, upper, piece)
                            if bool:
                                if not self.in_check(moved_rows, upper) and not self.flying_general(moved_rows):
                                    moves.append(moved_rows)
                            else:
                                moves.append(moved_rows)
                    counter += 1
            #Upward Check
            def upward_check():
                counter = 1
                next_move = (row - counter, column)
                while(row_in_range(row - counter)):
                    next_move = (row - counter, column)
                    possible_row, possible_column = next_move
                    if not (rows[possible_row][possible_column] == '0' or (upper and rows[possible_row][possible_column].islower()) or (not upper and rows[possible_row][possible_column].isupper())):
                        return
                    if (upper and rows[possible_row][possible_column].islower()) or (not upper and rows[possible_row][possible_column].isupper()):
                        # if (rows[possible_row][possible_column] == 'k' or rows[possible_row][possible_column] == 'K'):
                        #     return
                        if rows[possible_row][possible_column] == 'k' or rows[possible_row][possible_column] == 'K':
                            moved_rows = self.move(rows, row, column, possible_row, possible_column, upper, piece)
                            if not bool:
                                moves.append(moved_rows)
                        else:
                            moved_rows = self.move(rows, row, column, possible_row, possible_column, upper, piece)
                            if bool:
                                if not self.in_check(moved_rows, upper) and not self.flying_general(moved_rows):
                                    moves.append(moved_rows)
                            else:
                                moves.append(moved_rows)
                        return
                    # if (rows[possible_row][possible_column] == 'k' or rows[possible_row][possible_column] == 'K'):
                    #     return
                    if rows[possible_row][possible_column] == 'k' or rows[possible_row][possible_column] == 'K':
                        moved_rows = self.move(rows, row, column, possible_row, possible_column, upper, piece)
                        if not bool:
                            moves.append(moved_rows)
                    else:
                        moved_rows = self.move(rows, row, column, possible_row, possible_column, upper, piece)
                        if bool:
                            if not self.in_check(moved_rows, upper) and not self.flying_general(moved_rows):
                                moves.append(moved_rows)
                        else:
                            moves.append(moved_rows)
                    counter += 1
            #Right Check
            def right_check():
                counter = 1
                next_move = (row, column + counter)
                while(column_in_range(column + counter)):
                    next_move = (row, column + counter)
                    possible_row, possible_column = next_move
                    if not (rows[possible_row][possible_column] == '0' or (upper and rows[possible_row][possible_column].islower()) or (not upper and rows[possible_row][possible_column].isupper())):
                        return
                    if (upper and rows[possible_row][possible_column].islower()) or (not upper and rows[possible_row][possible_column].isupper()):
                        # if (rows[possible_row][possible_column] == 'k' or rows[possible_row][possible_column] == 'K'):
                        #     return
                        if rows[possible_row][possible_column] == 'k' or rows[possible_row][possible_column] == 'K':
                            moved_rows = self.move(rows, row, column, possible_row, possible_column, upper, piece)
                            if not bool:
                                moves.append(moved_rows)
                        else:
                            moved_rows = self.move(rows, row, column, possible_row, possible_column, upper, piece)
                            if bool:
                                if not self.in_check(moved_rows, upper) and not self.flying_general(moved_rows):
                                    moves.append(moved_rows)
                            else:
                                moves.append(moved_rows)
                        return
                    # if (rows[possible_row][possible_column] == 'k' or rows[possible_row][possible_column] == 'K'):
                    #     return
                    if rows[possible_row][possible_column] == 'k' or rows[possible_row][possible_column] == 'K':
                        moved_rows = self.move(rows, row, column, possible_row, possible_column, upper, piece)
                        if not bool:
                            moves.append(moved_rows)
                    else:
                        moved_rows = self.move(rows, row, column, possible_row, possible_column, upper, piece)
                        if bool:
                            if not self.in_check(moved_rows, upper) and not self.flying_general(moved_rows):
                                moves.append(moved_rows)
                        else:
                            moves.append(moved_rows)
                    counter += 1
            #Left Check
            def left_check():
                counter = 1
                next_move = (row, column - counter)
                while(column_in_range(column - counter)):
                    next_move = (row, column - counter)
                    possible_row, possible_column = next_move
                    # print(str(possible_row) + " " + str(possible_column))
                    if not (rows[possible_row][possible_column] == '0' or (upper and rows[possible_row][possible_column].islower()) or (not upper and rows[possible_row][possible_column].isupper())):
                        return
                    if (upper and rows[possible_row][possible_column].islower()) or (not upper and rows[possible_row][possible_column].isupper()):
                        if rows[possible_row][possible_column] == 'k' or rows[possible_row][possible_column] == 'K':
                            moved_rows = self.move(rows, row, column, possible_row, possible_column, upper, piece)
                            if not bool:
                                moves.append(moved_rows)
                        else:
                            moved_rows = self.move(rows, row, column, possible_row, possible_column, upper, piece)
                            if bool:
                                if not self.in_check(moved_rows, upper) and not self.flying_general(moved_rows):
                                    moves.append(moved_rows)
                            else:
                                moves.append(moved_rows)
                        return
                    # if (rows[possible_row][possible_column] == 'k' or rows[possible_row][possible_column] == 'K'):
                    #     return
                    if rows[possible_row][possible_column] == 'k' or rows[possible_row][possible_column] == 'K':
                        moved_rows = self.move(rows, row, column, possible_row, possible_column, upper, piece)
                        if not bool:
                            moves.append(moved_rows)
                    else:
                        moved_rows = self.move(rows, row, column, possible_row, possible_column, upper, piece)
                        if bool:
                            if not self.in_check(moved_rows, upper) and not self.flying_general(moved_rows):
                                moves.append(moved_rows)
                        else:
                            moves.append(moved_rows)
                    counter += 1
            downward_check()
            upward_check()
            left_check()
            right_check()
            
        def next_king_moves(row, column):
            possible_moves = [
                (row+1, column),
                (row-1, column),
                (row, column+1),
                (row, column-1),
            ]
            max_column = 6
            min_column = 3
            if piece.islower():
                max_row = 3
                min_row = 0
            else:
                max_row = 10
                min_row = 7
                
            for possible_move in possible_moves:
                possible_row, possible_column = possible_move
                if possible_column in range(min_column, max_column) and possible_row in range(min_row, max_row):
                    if is_valid(possible_row, possible_column):
                        moved_rows = self.move(rows, row, column, possible_row, possible_column, upper, piece)
                        if bool:
                            if self.is_check(moved_rows, upper) and not self.flying_general(moved_rows):
                                if self.out_of_check(moved_rows, upper):
                                    moves.append(moved_rows)
                            elif not self.in_check(moved_rows, upper) and not self.flying_general(moved_rows):
                                moves.append(moved_rows)
                        else:
                            moves.append(moved_rows)
                        
        def next_guard_moves(row, column):
            possible_moves = [
                (row+1, column+1),
                (row-1, column-1),
                (row-1, column+1),
                (row+1, column-1),
            ]
            max_column = 6
            min_column = 3
            if piece.islower():
                max_row = 3
                min_row = 0
            else:
                max_row = 10
                min_row = 7
            for possible_move in possible_moves:
                possible_row, possible_column = possible_move
                if possible_column in range(min_column, max_column) and possible_row in range(min_row, max_row):
                    if is_valid(possible_row, possible_column):
                        moved_rows = self.move(rows, row, column, possible_row, possible_column, upper, piece)
                        if bool:
                            if not self.in_check(moved_rows, upper) and not self.flying_general(moved_rows):
                                moves.append(moved_rows)
                        else:
                            moves.append(moved_rows)
                                         
        def next_elephant_moves(row, column):
            possible_moves = []
            #Check top right
            if row_in_range(row+2) and column_in_range(column+2) and rows[row+1][column+1] == '0':
                if (piece.islower() and row+2 <= 4) or piece.isupper():
                # if piece.colour == "red" and row+2 <= 4 or piece.colour == "black":
                    possible_moves.append((row+2, column+2))
            #Check top left
            if row_in_range(row-2) and column_in_range(column-2) and rows[row-1][column-1] == '0':
                if (piece.isupper() and row-2 >= 5) or piece.islower():
                # if piece.colour == "black" and row-2 >= 5 or piece.colour == "red":
                    possible_moves.append((row-2, column-2))
            #Check bottom left
            if row_in_range(row+2) and column_in_range(column-2) and rows[row+1][column-1] == '0':
                if (piece.islower() and row+2 <= 4) or piece.isupper():
                # if piece.colour == "red" and row+2 <= 4 or piece.colour == "black":
                    possible_moves.append((row+2, column-2))
            #Check bottom right
            if row_in_range(row-2) and column_in_range(column+2) and rows[row-1][column+1] == '0':
                if (piece.isupper() and row-2 >= 5) or piece.islower():
                # if piece.colour == "black" and row-2 >= 5 or piece.colour == "red":
                    possible_moves.append((row-2, column+2))
            
            for possible_move in possible_moves:
                possible_row, possible_column = possible_move
                if row_in_range(possible_row) and column_in_range(possible_column):
                    if is_valid(possible_row, possible_column):
                        moved_rows = self.move(rows, row, column, possible_row, possible_column, upper, piece)
                        if bool:
                            if not self.in_check(moved_rows, upper) and not self.flying_general(moved_rows):
                                moves.append(moved_rows)
                        else:
                            moves.append(moved_rows)
                        
        def next_pawn_moves(row, column):
            def move_red_home():
                possible_move = (row + 1, column)
                possible_row, possible_column = possible_move
                if row_in_range(possible_row) and column_in_range(possible_column):
                    if is_valid(possible_row, possible_column):
                    # if is_valid(possible_row, possible_column) and not (rows[possible_row][possible_column] == 'k' or rows[possible_row][possible_column] == 'K'):
                        if rows[possible_row][possible_column] == 'k' or rows[possible_row][possible_column] == 'K':
                            moved_rows = self.move(rows, row, column, possible_row, possible_column, upper, piece)
                            if not bool:
                                moves.append(moved_rows)
                        else:
                            moved_rows = self.move(rows, row, column, possible_row, possible_column, upper, piece)
                            if bool:
                                if not self.in_check(moved_rows, upper) and not self.flying_general(moved_rows):
                                    moves.append(moved_rows)
                            else:
                                moves.append(moved_rows)
                        
            def move_red_rival():
                possible_moves = [
                (row+1, column),
                (row, column+1),
                (row, column-1),
            ]
                for possible_move in possible_moves:
                    possible_row, possible_column = possible_move
                    if possible_row in range(5,10) and column_in_range(possible_column):
                        if is_valid(possible_row, possible_column):
                            # print(str(possible_row) + " " + str(possible_column))
                        # if is_valid(possible_row, possible_column) and not (rows[possible_row][possible_column] == 'k' or rows[possible_row][possible_column] == 'K'):
                            if rows[possible_row][possible_column] == 'k' or rows[possible_row][possible_column] == 'K':
                                moved_rows = self.move(rows, row, column, possible_row, possible_column, upper, piece)
                                if not bool:
                                    moves.append(moved_rows)
                            else:
                                moved_rows = self.move(rows, row, column, possible_row, possible_column, upper, piece)
                                if bool:
                                    if not self.in_check(moved_rows, upper) and not self.flying_general(moved_rows):
                                        moves.append(moved_rows)
                                else:
                                    moves.append(moved_rows)
                            
            def move_black_home():
                possible_move = (row - 1, column)
                possible_row, possible_column = possible_move
                if row_in_range(possible_row) and column_in_range(possible_column):
                    if is_valid(possible_row, possible_column):
                    # if is_valid(possible_row, possible_column) and not (rows[possible_row][possible_column] == 'k' or rows[possible_row][possible_column] == 'K'):
                        if rows[possible_row][possible_column] == 'k' or rows[possible_row][possible_column] == 'K':
                            moved_rows = self.move(rows, row, column, possible_row, possible_column, upper, piece)
                            if not bool:
                                moves.append(moved_rows)
                        else:
                            moved_rows = self.move(rows, row, column, possible_row, possible_column, upper, piece)
                            if bool:
                                if not self.in_check(moved_rows, upper) and not self.flying_general(moved_rows):
                                    moves.append(moved_rows)
                            else:
                                moves.append(moved_rows)
            def move_black_rival():
                possible_moves = [
                (row-1, column),
                (row, column+1),
                (row, column-1),
            ]
                for possible_move in possible_moves:
                    possible_row, possible_column = possible_move
                    if possible_row in range(0,5) and column_in_range(possible_column):
                        if is_valid(possible_row, possible_column):
                        # if is_valid(possible_row, possible_column) and not (rows[possible_row][possible_column] == 'k' or rows[possible_row][possible_column] == 'K'):
                            if rows[possible_row][possible_column] == 'k' or rows[possible_row][possible_column] == 'K':
                                moved_rows = self.move(rows, row, column, possible_row, possible_column, upper, piece)
                                if not bool:
                                    moves.append(moved_rows)
                            else:
                                moved_rows = self.move(rows, row, column, possible_row, possible_column, upper, piece)
                                if bool:
                                    if not self.in_check(moved_rows, upper) and not self.flying_general(moved_rows):
                                        moves.append(moved_rows)
                                else:
                                    moves.append(moved_rows)
            
            if piece.islower():
                if row < 5:
                    move_red_home()
                else:
                    move_red_rival()
            else:
                if row > 4:
                    move_black_home()
                else:
                    move_black_rival()
                    
        def next_cannon_moves(row, column):     
            #Downward Check
            def downward_check():
                counter = 1
                next_move = (row + counter, column)
                while(row_in_range(row + counter)):
                    next_move = (row + counter, column)
                    possible_row, possible_column = next_move
                    if not rows[possible_row][possible_column] == '0':
                        # Check whether a rival piece is in a square after the first blocking piece
                        counter += 1
                        # Loop after blocking piece to find next piece
                        while(row_in_range(row + counter)):
                            next_move = (row + counter, column)
                            possible_row, possible_column = next_move
                            # If piece is team piece then no jump occurs and return
                            if (upper and rows[possible_row][possible_column].isupper()) or (not upper and rows[possible_row][possible_column].islower()):
                                return
                            # If piece is rival then add move to possible moves
                            if (upper and rows[possible_row][possible_column].islower()) or (not upper and rows[possible_row][possible_column].isupper()):
                                # if (rows[possible_row][possible_column] == 'k' or rows[possible_row][possible_column] == 'K'):
                                #     return
                                if rows[possible_row][possible_column] == 'k' or rows[possible_row][possible_column] == 'K':
                                    moved_rows = self.move(rows, row, column, possible_row, possible_column, upper, piece)
                                    if not bool:
                                        moves.append(moved_rows)
                                else:
                                    moved_rows = self.move(rows, row, column, possible_row, possible_column, upper, piece)
                                    if bool:
                                        if not self.in_check(moved_rows, upper) and not self.flying_general(moved_rows):
                                            moves.append(moved_rows)
                                    else:
                                        moves.append(moved_rows)
                                return
                            counter += 1 
                        return
                    # if (rows[possible_row][possible_column] == 'k' or rows[possible_row][possible_column] == 'K'):
                    #     return
                    if rows[possible_row][possible_column] == 'k' or rows[possible_row][possible_column] == 'K':
                        moved_rows = self.move(rows, row, column, possible_row, possible_column, upper, piece)
                        if not bool:
                            moves.append(moved_rows)
                    else:    
                        moved_rows = self.move(rows, row, column, possible_row, possible_column, upper, piece)
                        if bool:
                            if not self.in_check(moved_rows, upper) and not self.flying_general(moved_rows):
                                moves.append(moved_rows)
                        else:
                            moves.append(moved_rows)
                    counter += 1
            #Upward Check
            def upward_check():
                counter = 1
                next_move = (row - counter, column)
                # Loop until check either isn't on board or is intercepted by own piece or rival piece
                while(row_in_range(row - counter)):
                    next_move = (row - counter, column)
                    possible_row, possible_column = next_move
                    # Check whether move contains a blocking piece
                    if not rows[possible_row][possible_column] == '0':
                        # Check whether a rival piece is in a square after the first blocking piece
                        counter += 1
                        # Loop after blocking piece to find next piece
                        while(row_in_range(row - counter)):
                            next_move = (row - counter, column)
                            possible_row, possible_column = next_move
                            # If piece is team piece then no jump occurs and return
                            if (upper and rows[possible_row][possible_column].isupper()) or (not upper and rows[possible_row][possible_column].islower()):
                                return
                            # If piece is rival then add move to possible moves
                            if (upper and rows[possible_row][possible_column].islower()) or (not upper and rows[possible_row][possible_column].isupper()):
                                # if (rows[possible_row][possible_column] == 'k' or rows[possible_row][possible_column] == 'K'):
                                #     return
                                if rows[possible_row][possible_column] == 'k' or rows[possible_row][possible_column] == 'K':
                                    moved_rows = self.move(rows, row, column, possible_row, possible_column, upper, piece)
                                    if not bool:
                                        moves.append(moved_rows)
                                else:         
                                    moved_rows = self.move(rows, row, column, possible_row, possible_column, upper, piece)
                                    if bool:
                                        if not self.in_check(moved_rows, upper) and not self.flying_general(moved_rows):
                                            moves.append(moved_rows)
                                    else:
                                        moves.append(moved_rows)
                                return
                            counter += 1 
                        return
                    # if (rows[possible_row][possible_column] == 'k' or rows[possible_row][possible_column] == 'K'):
                    #     return
                    if rows[possible_row][possible_column] == 'k' or rows[possible_row][possible_column] == 'K':
                        moved_rows = self.move(rows, row, column, possible_row, possible_column, upper, piece)
                        if not bool:
                            moves.append(moved_rows)
                    else:
                        moved_rows = self.move(rows, row, column, possible_row, possible_column, upper, piece)
                        if bool:
                            if not self.in_check(moved_rows, upper) and not self.flying_general(moved_rows):
                                moves.append(moved_rows)
                        else:
                            moves.append(moved_rows)
                    counter += 1
            #Right Check
            def right_check():
                counter = 1
                next_move = (row, column + counter)
                while(column_in_range(column + counter)):
                    next_move = (row, column + counter)
                    possible_row, possible_column = next_move
                    if not rows[possible_row][possible_column] == '0':
                        # Check whether a rival piece is in a square after the first blocking piece
                        counter += 1
                        # Loop after blocking piece to find next piece
                        while(column_in_range(column + counter)):
                            next_move = (row, column + counter)
                            possible_row, possible_column = next_move
                            # If piece is team piece then no jump occurs and return
                            if (upper and rows[possible_row][possible_column].isupper()) or (not upper and rows[possible_row][possible_column].islower()):
                                return
                            # If piece is rival then add move to possible moves
                            if (upper and rows[possible_row][possible_column].islower()) or (not upper and rows[possible_row][possible_column].isupper()):
                                # if (rows[possible_row][possible_column] == 'k' or rows[possible_row][possible_column] == 'K'):
                                #     return
                                if rows[possible_row][possible_column] == 'k' or rows[possible_row][possible_column] == 'K':
                                    moved_rows = self.move(rows, row, column, possible_row, possible_column, upper, piece)
                                    if not bool:
                                        moves.append(moved_rows)
                                else:
                                    moved_rows = self.move(rows, row, column, possible_row, possible_column, upper, piece)
                                    if bool:
                                        if not self.in_check(moved_rows, upper) and not self.flying_general(moved_rows):
                                            moves.append(moved_rows)
                                    else:
                                        moves.append(moved_rows)
                                return
                            counter += 1 
                        return
                    # if (rows[possible_row][possible_column] == 'k' or rows[possible_row][possible_column] == 'K'):
                    #     return
                    if rows[possible_row][possible_column] == 'k' or rows[possible_row][possible_column] == 'K':
                        moved_rows = self.move(rows, row, column, possible_row, possible_column, upper, piece)
                        if not bool:
                            moves.append(moved_rows)
                    else:
                        moved_rows = self.move(rows, row, column, possible_row, possible_column, upper, piece)
                        if bool:
                            if not self.in_check(moved_rows, upper) and not self.flying_general(moved_rows):
                                moves.append(moved_rows)
                        else:
                            moves.append(moved_rows)
                    counter += 1
            #Left Check
            def left_check():
                counter = 1
                next_move = (row, column - counter)
                while(column_in_range(column - counter)):
                    next_move = (row, column - counter)
                    possible_row, possible_column = next_move
                    if not rows[possible_row][possible_column] == '0':
                        # Check whether a rival piece is in a square after the first blocking piece
                        counter += 1
                        # Loop after blocking piece to find next piece
                        while(column_in_range(column - counter)):
                            next_move = (row, column - counter)
                            possible_row, possible_column = next_move
                            # If piece is team piece then no jump occurs and return
                            if (upper and rows[possible_row][possible_column].isupper()) or (not upper and rows[possible_row][possible_column].islower()):
                                return
                            # If piece is rival then add move to possible moves
                            if (upper and rows[possible_row][possible_column].islower()) or (not upper and rows[possible_row][possible_column].isupper()):
                                # if (rows[possible_row][possible_column] == 'k' or rows[possible_row][possible_column] == 'K'):
                                #     return
                                if rows[possible_row][possible_column] == 'k' or rows[possible_row][possible_column] == 'K':
                                    moved_rows = self.move(rows, row, column, possible_row, possible_column, upper, piece)
                                    if not bool:
                                        moves.append(moved_rows)
                                else:        
                                    moved_rows = self.move(rows, row, column, possible_row, possible_column, upper, piece)
                                    # self.print_row(moved_rows)
                                    if bool:
                                        if not self.in_check(moved_rows, upper) and not self.flying_general(moved_rows):
                                            moves.append(moved_rows)
                                    else:
                                        moves.append(moved_rows)
                                return
                            counter += 1 
                        return
                    # if (rows[possible_row][possible_column] == 'k' or rows[possible_row][possible_column] == 'K'):
                    #     return
                    if rows[possible_row][possible_column] == 'k' or rows[possible_row][possible_column] == 'K':
                        moved_rows = self.move(rows, row, column, possible_row, possible_column, upper, piece)
                        if not bool:
                            moves.append(moved_rows)
                    else:
                        moved_rows = self.move(rows, row, column, possible_row, possible_column, upper, piece)
                        if bool:
                            if not self.in_check(moved_rows, upper) and not self.flying_general(moved_rows):
                                moves.append(moved_rows)
                        else:
                            moves.append(moved_rows)
                    counter += 1
            downward_check()
            upward_check()
            left_check()
            right_check()

        if piece.lower() == 'p':
            next_pawn_moves(row, column)
        elif piece.lower() == 'c':
            next_cannon_moves(row, column)
        elif piece.lower() == 'h':
            next_knight_moves(row, column)
        elif piece.lower() == 'e':
            next_elephant_moves(row, column)
        elif piece.lower() == 'g':
            next_guard_moves(row, column)
        elif piece.lower() == 'k':
            next_king_moves(row, column)
        elif piece.lower() == 'r':
            next_rook_moves(row, column)
        
        return moves
               
    # Method used to check if a particular move will put the kings in check by having no pieces inbetween       
    def flying_general(self, rows):
        if self.debug:
            st = time.time()
        king_row = None    
        # Find top king piece
        for row in range(3):
            for column in range(PIECE_COLUMNS):
                if rows[row][column] == 'k' or rows[row][column] == 'K':
                    king_col = column
                    king_row = row    
        if king_row == None:
            print("hello")
        # Loop through row which king is on and check for rule by checking a piece is between it or no king at the end 
        for row in range(king_row+1, PIECE_ROWS):
            if rows[row][king_col] == 'k' or rows[row][king_col] == 'K':
                if self.debug:
                    et = time.time()
                    runtime = et - st
                    print("FLYING GENERAL EXECUTION TIME: " + f"{runtime:.15f}")
                return True
            if rows[row][king_col] != '0' and rows[row][king_col] != 'k' and rows[row][king_col] != 'K':
                if self.debug:
                    et = time.time()
                    runtime = et - st
                    print("FLYING GENERAL EXECUTION TIME: " + f"{runtime:.15f}")
                return False
        if self.debug:
            et = time.time()
            runtime = et - st
            print("FLYING GENERAL EXECUTION TIME: " + f"{runtime:.15f}")
        return False
    
    # Method used to calculate if moving a friendly piece results in its own checkmate (to prevent moves that put yourself in checkmate)
    def in_check(self, rows, upper):
        if self.debug:
            st = time.time()
        piece_list = ['c', 'r', 'h', 'p', 'C', 'R', 'H', 'P']
        
        for row in range(PIECE_ROWS):
            for column in range(PIECE_COLUMNS):
                # Check for enemy pieces by finding opposite cases
                if (upper and rows[row][column].islower() and rows[row][column] != '0') or (not upper and rows[row][column].isupper() and rows[row][column] != '0'):
                    p = rows[row][column]
                    if p not in piece_list:
                        break
                    # Calculate moves of enemy piece
                    moves = self.calculate_moves(rows, p, row, column, (not upper), bool=False)
                    # For each move opponent check whether the friendly king has been taken
                    for move in moves:
                        # print(move)
                        if (not upper and not ('k' in move[0] or 'k' in move[1] or 'k' in move[2])) or (upper and not ('K' in move[7] or 'K' in move[8] or 'K' in move[9])):
                        # if (upper and 'k' in move[row][column]) or (not upper and 'K' in move[row][column]):
                                if self.debug:
                                    et = time.time()
                                    runtime = et - st
                                    print("IN CHECK EXECUTION TIME: " + f"{runtime:.15f}")
                                return True
        if self.debug:
            et = time.time()
            runtime = et - st
            print("IN CHECK EXECUTION TIME: " + f"{runtime:.15f}")
        return False
    
    # Method used to see if king is currently in check
    def is_check(self, rows, upper):
        if self.debug:
            st = time.time()
        # piece_list = ['c', 'C']
        piece_list = ['c', 'r', 'h', 'p', 'C', 'R', 'H', 'P']
        # Search through board to find all enemy pieces
        for row in range(PIECE_ROWS):
            for column in range(PIECE_COLUMNS):
                # Calculate all possible moves of each piece
                if (upper and rows[row][column].islower() and rows[row][column] != '0') or (not upper and rows[row][column].isupper() and rows[row][column] != '0'):
                    p = rows[row][column]
                    if p not in piece_list:
                        pass
                    else:
                        moves = self.calculate_moves(rows, p, row, column, not upper, bool=False)
                        # Search through all moves to find if any are a check
                        for move in moves:
                            # print(move)
                            if (not upper and not ('k' in move[0] or 'k' in move[1] or 'k' in move[2])) or (upper and not ('K' in move[7] or 'K' in move[8] or 'K' in move[9])):
                                self.checked = True
                                if self.debug:
                                    et = time.time()
                                    runtime = et - st
                                    print("IS CHECK EXECUTION TIME: " + f"{runtime:.15f}")
                                return True
        self.checked = False
        if self.debug:
            et = time.time()
            runtime = et - st
            print("IS CHECK EXECUTION TIME: " + f"{runtime:.15f}")
        return False
    
    # Method used to calculate if moving a friendly piece results in getting out of checkmate
    def out_of_check(self, rows, upper):
        if self.debug:
            st = time.time()
        
        for row in range(PIECE_ROWS):
            for column in range(PIECE_COLUMNS):
                # Check for rival pieces
                if (upper and rows[row][column].islower() and rows[row][column] != '0') or (not upper and rows[row][column].isupper() and rows[row][column] != '0'):
                    p = rows[row][column]
                    moves = self.calculate_moves(rows, p, row, column, not upper, bool=False)
                    # Calculate enemy piece moves and then check if player is still in check
                    for move in moves:
                        if (not upper and not ('k' in move[0] or 'k' in move[1] or 'k' in move[2])) or (upper and not ('K' in move[7] or 'K' in move[8] or 'K' in move[9])):
                            if self.debug:
                                et = time.time()
                                runtime = et - st
                                print("OUT OF CHECK EXECUTION TIME: " + f"{runtime:.15f}")
                            return False
        if self.debug:
            et = time.time()
            runtime = et - st
            print("OUT OF CHECK EXECUTION TIME: " + f"{runtime:.15f}")
        return True 
    
    # Method used to check whether a side is in checkmate
    def is_checkmate(self, rows, upper):
        if self.debug:
            st = time.time()
        # Check if king is in check
        if not self.is_check(rows, upper):
            return False
        else:
            piece_list = ['c', 'r', 'h', 'p', 'C', 'R', 'H', 'P']
            # Check each move that puts the king into check and search if any move removes all checks on the king
            # Search through board to find all enemy pieces
            for row in range(PIECE_ROWS):
                for column in range(PIECE_COLUMNS):
                    # Calculate all possible moves of each enemy piece
                    if (upper and rows[row][column].islower() and rows[row][column] != '0') or (not upper and rows[row][column].isupper() and rows[row][column] != '0'):
                        p = rows[row][column]
                        moves = self.calculate_moves(rows, p, row, column, not upper, bool=False)
                        if p not in piece_list:
                            break
                        # Filter through all moves to find any enemy moves that check the king
                        for move in moves:
                            if (not upper and not ('k' in move[0] or 'k' in move[1] or 'k' in move[2])) or (upper and not ('K' in move[7] or 'K' in move[8] or 'K' in move[9])):
                                print("kills king")
                                print(move)
                                # If it is a check then we need to search for any friendly moves that bring the king out of check
                                # Set checkmated to true to reset for each possible checkmate
                                checkmated = True
                                
                                print("friendly moves")
                                # Search through all friendly pieces of the king being checked
                                for row1 in range(PIECE_ROWS):
                                    for column1 in range(PIECE_COLUMNS):
                                        # Calculate all possible moves of each friendly piece
                                        if (upper and rows[row1][column1].isupper() and rows[row1][column1] != '0') or (not upper and rows[row1][column1].islower() and rows[row1][column1] != '0'):
                                            friendly_piece = rows[row1][column1]
                                            friendly_moves = self.calculate_moves(rows, friendly_piece, row1, column1, upper, bool=False)
                                            for i in friendly_moves:
                                                print(i)
                                            # For each move check if it gets the king out of check
                                            print("escaping moves")
                                            for friendly_move in friendly_moves:
                                                if self.out_of_check(friendly_move, upper) and not self.flying_general(friendly_move):
                                                    print(friendly_move)
                                                    # If a move successfully gets out of check then we can stop searching for that check and move on
                                                    checkmated = False
                                                    row1 = PIECE_ROWS - 1
                                                    column1 = PIECE_COLUMNS - 1
                                                    break
                                
                                # Since no moves were found to turn checkmate false after checking all moves for a specific check
                                # Condition then the king has been checkmated
                                if checkmated == True:
                                    if self.debug:
                                        et = time.time()
                                        runtime = et - st
                                        print("IS CHECKMATE EXECUTION TIME: " + f"{runtime:.15f}")
                                    return True
                                
            if self.debug:
                et = time.time()
                runtime = et - st
                print("IS CHECKMATE EXECUTION TIME: " + f"{runtime:.15f}")                    
            return False

    def move(self, rows, row, column, next_row, next_column, upper, piece):
        new_rows = rows.copy()
        # Update new_rows
        new_rows[row] = new_rows[row][:column] + '0' + new_rows[row][column + 1:]
        if upper:
            new_rows[next_row] = new_rows[next_row][:next_column] + piece.upper() + new_rows[next_row][next_column + 1:]
        else:
            new_rows[next_row] = new_rows[next_row][:next_column] + piece.lower() + new_rows[next_row][next_column + 1:]
        return new_rows                                     

    def minimax(self, rows, depth, alpha, beta, upper, pathDictionary):
        best_move = None
         
        if self.is_checkmate(rows, not upper):
            return 10000, best_move
        if depth <= 0:
            return self.evaluation(rows, not upper), best_move
        
        if upper:   
            if str(rows) in pathDictionary:
                return pathDictionary[str(rows)], best_move
            value = -math.inf
            states = self.next_states(rows, True)
            for s in states:
                eval, _ = self.minimax(s, depth - 1, alpha, beta, False, pathDictionary)
                if eval > value:
                    value = eval
                    best_move = s
                alpha = max(alpha, value)
                if value >= beta:
                    pathDictionary[str(rows)] = value
                    break
            pathDictionary[str(rows)] = value
            return value, best_move
        else:
            if str(rows) in pathDictionary:
                return pathDictionary[str(rows)], best_move
            value = math.inf
            states = self.next_states(rows, False)
            for s in states:
                eval, _ = self.minimax(s, depth - 1, alpha, beta, True, pathDictionary)
                if eval < value:
                    value = eval
                    best_move = s
                beta = min(beta, value)
                if value <= alpha:
                    pathDictionary[str(rows)] = value
                    break
            pathDictionary[str(rows)] = value
            return value, best_move
        
    def monte_carlo(self, rows, turn):
        print('start MCTS')
        # Create MC agent and root node
        root = Node(rows, not turn)
        mcts = SearchTree(root)
        best_node = mcts.best_action(2)
        print('done')
        self.print_row(best_node)
        return best_node

    def get_ordered_moves(rows, upper):
        pass               
    
agent = Agent()


temp_board = '00ek0r000/000000000/0000c0000/0000c0000/000000000/000000000/000000000/000000000/000000000/0000K0000'
board = temp_board.split('/')
print(agent.is_terminal_state(board, True))