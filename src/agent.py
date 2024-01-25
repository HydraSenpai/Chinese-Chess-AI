from square import Square
from piece import *
from const import *
from move import Move
import copy
import random
import math
import time

class Agent:
    def __init__(self):
        self.debug = True  
        
    def print_row(self, rows):
        print("----------------------------------------------")
        for row in range(PIECE_ROWS):
            for column in range(PIECE_COLUMNS):    
                print(rows[row][column], end = " ")
            print("\n")
        print("-----------------------------------------------")
                                                          
    def calculate_all_possible_moves(self, board, upper, level):
        pieces = []
        possible_moves = []
        check = False
        pathDictionary = {}
        pathDictionary.clear()
        # x = first index y = second index
        # temp_board = 'r00000000R/h0c0000C0H/e00000000E/g00000000G/k00000000K/g00000000G/e00000000E/h0c0000C0H/r00000000R'
        # temp_board = 'r00p00P00R/h0c0000C0H/e00p00P00E/g00000000G/k00p00P00K/g00000000G/e00p00P00E/h0c0000C0H/r00p00P00R'
        # temp_board = 'r00000000R/h00000000H/e00p00P00E/g00000000G/k00p00P00K/g00000000G/e00p00P00E/h00000000H/r00p00P00R'
        # temp_board = '0000000000/0000000000/0000000000/0000000000/k00p00P00K/0000000000/0000000000/0000000000/0000000000'
        # temp_board = '0000000000/r0rP0000P0/0000000000/0000000000/k00000000K/0000000000/0000000000/0000000000/0000000000'
        # temp_board = '0000000000/0000000000/0000000000/0000000000/k00000P00K/0000000000/0000000000/0000000000/0000000000'
        temp_board = 'cheakaehr/000000000/0c00000c0/p0p0p0p0p/000000000/000000000/P0P0P0P0P/0C00000C0/000000000/RHEAKEAHR'
        # temp_board = 'R0eakaehr/000000000/000000000/p0p0p0p0p/000000000/000000000/P0P0P0P0P/000000000/000000000/RHEAKAEHR'
        # Where uppercase is other player
        # Will turn this into array
        split_board = temp_board.split('/')
        self.print_row(split_board)
        if level != "beginner":
            st = time.time()
            # value, best_move = self.minimax_simple(split_board, 1, True, pathDictionary)
            value, best_move = self.minimax(split_board, 3, -math.inf, math.inf, True, pathDictionary)
            self.print_row(best_move)
            # value, best_move = self.minimax(minimax_board, 3, True)
            print("END VALUE = " + str(value))
            et = time.time()
            runtime = et - st
            print("EXECUTION TIME: " + str(runtime))
            return best_move    
    
    def evaluation(self, rows, upper):
        if self.debug:
            st = time.time()
        value = 0
        
        for row in range(PIECE_ROWS):
            for column in range(PIECE_COLUMNS): 
                if (rows[row][column] == '0'):
                    pass
                elif (not upper and rows[row][column].isupper()) or (upper and rows[row][column].islower()):
                    value += 1
                else:
                    value -= 1
        # if value > -1:
        # self.print_row(rows)
        # print("EVALUATION VALUE = " + str(value))
        
        if self.debug:
            et = time.time()
            runtime = et - st
            print("EVALUATION EXECUTION TIME: " + f"{runtime:.15f}")
        return value
                          
    # Returns all moves from a given board and colour and returns them as boards
    def next_states(self, rows, upper): 
        
        # rows ['h00000000H', '0000000000', '0000000000', '0000000000', '0000000000', '0000000000', '0000000000', '0000000000', 'h00000000H']
        
        if self.debug:
            st = time.time()
        possible_states = []
        count = 0
                                
        for row in range(PIECE_ROWS):
            for column in range(PIECE_COLUMNS):
                # Find every team piece and calculate all moves
                if (rows[row][column].isupper() and upper and rows[row][column] != '0') or (rows[row][column].islower() and not upper and rows[row][column] != '0'):
                    count+=1
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
                if (upper and rows[row][column].isupper() and rows[row][column] != '0') or (not upper and rows[row][column].islower() and rows[row][column] != '0'):
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
                      
    def minimax(self, rows, depth, alpha, beta, upper, pathDictionary):
        best_move = None
         
        if depth <= 0 or self.is_terminal_state(rows, upper):
            return self.evaluation(rows, upper), best_move
        
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
        
        def is_valid(row, column):
            if upper:
                if not rows[row][column].isupper() and (rows[row][column] == '0' or rows[row][column].islower()):
                    return True
            else:
                if not rows[row][column].islower() and (rows[row][column] == '0' or not rows[row][column].isupper()):
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
                    if is_valid(possible_row, possible_column) and not self.kill_king(rows, possible_row, possible_column):
                        moved_rows = self.move(rows, row, column, possible_row, possible_column, upper, piece)
                        if bool:
                            # if True:
                            if not self.in_check(moved_rows, upper) and not self.flying_general(moved_rows):
                                moves.append(moved_rows)
                            else:
                                break
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
                    if not (rows[possible_row][possible_column] == '0' or (upper and rows[possible_row][possible_column].islower())) or (not upper and rows[possible_row][possible_column].isupper()):
                        return
                    if (upper and rows[possible_row][possible_column].islower()) or (not upper and rows[possible_row][possible_column].isupper()):
                        if self.kill_king(rows, possible_row, possible_column):
                            return
                        moved_rows = self.move(rows, row, column, possible_row, possible_column, upper, piece)
                        if bool:
                            if not self.in_check(moved_rows, upper) and not self.flying_general(moved_rows):
                                moves.append(moved_rows)
                        else:
                            moves.append(moved_rows)
                        return
                    if self.kill_king(rows, possible_row, possible_column):
                        return
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
                    if not (rows[possible_row][possible_column] == '0' or (upper and rows[possible_row][possible_column].islower())) or (not upper and rows[possible_row][possible_column].isupper()):
                        return
                    if (upper and rows[possible_row][possible_column].islower()) or (not upper and rows[possible_row][possible_column].isupper()):
                        if self.kill_king(rows, possible_row, possible_column):
                            return
                        moved_rows = self.move(rows, row, column, possible_row, possible_column, upper, piece)
                        if bool:
                            if not self.in_check(moved_rows, upper) and not self.flying_general(moved_rows):
                                moves.append(moved_rows)
                        else:
                            moves.append(moved_rows)
                        return
                    if self.kill_king(rows, possible_row, possible_column):
                        return
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
                    if not (rows[possible_row][possible_column] == '0' or (upper and rows[possible_row][possible_column].islower())) or (not upper and rows[possible_row][possible_column].isupper()):
                        return
                    if (upper and rows[possible_row][possible_column].islower()) or (not upper and rows[possible_row][possible_column].isupper()):
                        if self.kill_king(rows, possible_row, possible_column):
                            return
                        moved_rows = self.move(rows, row, column, possible_row, possible_column, upper, piece)
                        if bool:
                            if not self.in_check(moved_rows, upper) and not self.flying_general(moved_rows):
                                moves.append(moved_rows)
                        else:
                            moves.append(moved_rows)
                        return
                    if self.kill_king(rows, possible_row, possible_column):
                        return
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
                    if not (rows[possible_row][possible_column] == '0' or (upper and rows[possible_row][possible_column].islower())) or (not upper and rows[possible_row][possible_column].isupper()):
                        return
                    if (upper and rows[possible_row][possible_column].islower()) or (not upper and rows[possible_row][possible_column].isupper()):
                        if self.kill_king(rows, possible_row, possible_column):
                            return
                        moved_rows = self.move(rows, row, column, possible_row, possible_column, upper, piece)
                        if bool:
                            if not self.in_check(moved_rows, upper) and not self.flying_general(moved_rows):
                                moves.append(moved_rows)
                        else:
                            moves.append(moved_rows)
                        return
                    if self.kill_king(rows, possible_row, possible_column):
                        return
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
                    if is_valid(possible_row, possible_column) and not self.kill_king(rows, possible_row, possible_column):
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
                        if is_valid(possible_row, possible_column) and not self.kill_king(rows, possible_row, possible_column):
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
                    if is_valid(possible_row, possible_column) and not self.kill_king(rows, possible_row, possible_column):
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
                        if is_valid(possible_row, possible_column) and not self.kill_king(rows, possible_row, possible_column):
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
                                if self.kill_king(rows, possible_row, possible_column):
                                    return
                                moved_rows = self.move(rows, row, column, possible_row, possible_column, upper, piece)
                                if bool:
                                    if not self.in_check(moved_rows, upper) and not self.flying_general(moved_rows):
                                        moves.append(moved_rows)
                                else:
                                    moves.append(moved_rows)
                                return
                            counter += 1 
                        return
                    if self.kill_king(rows, possible_row, possible_column):
                        return
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
                                if self.kill_king(rows, possible_row, possible_column):
                                    return
                                moved_rows = self.move(rows, row, column, possible_row, possible_column, upper, piece)
                                if bool:
                                    if not self.in_check(moved_rows, upper) and not self.flying_general(moved_rows):
                                        moves.append(moved_rows)
                                else:
                                    moves.append(moved_rows)
                                return
                            counter += 1 
                        return
                    if self.kill_king(rows, possible_row, possible_column):
                        return
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
                                if self.kill_king(rows, possible_row, possible_column):
                                    return
                                moved_rows = self.move(rows, row, column, possible_row, possible_column, upper, piece)
                                if bool:
                                    if not self.in_check(moved_rows, upper) and not self.flying_general(moved_rows):
                                        moves.append(moved_rows)
                                else:
                                    moves.append(moved_rows)
                                return
                            counter += 1 
                        return
                    if self.kill_king(rows, possible_row, possible_column):
                        return
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
                                if self.kill_king(rows, possible_row, possible_column):
                                    return
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
                    if self.kill_king(rows, possible_row, possible_column):
                        return
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
            self.print_row(rows)
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
                        if (upper and 'k' in move[row][column]) or (not upper and 'K' in move[row][column]):
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
        piece_list = ['c', 'r', 'h', 'p', 'C', 'R', 'H', 'P']
        # Search through board to find all enemy pieces
        for row in range(PIECE_ROWS):
            for column in range(PIECE_COLUMNS):
                # Calculate all possible moves of each piece
                if (upper and rows[row][column].islower() and rows[row][column] != '0') or (not upper and rows[row][column].isupper() and rows[row][column] != '0'):
                    p = rows[row][column]
                    if p not in piece_list:
                        break
                    moves = self.calculate_moves(rows, p, row, column, not upper, bool=False)
                    # Search through all moves to find if any are a checkmate
                    for move in moves:
                        if (upper and 'k' in move[row][column]) or (not upper and 'K' in move[row][column]):
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
                if (upper and rows[row][column].islower() and rows[row][column] != '0') or (not upper and rows[row][column].isupper() and rows[row][column] != '0'):
                    p = rows[row][column].piece
                    moves = self.calculate_moves(rows, p, row, column, upper, bool=False)
                    for move in moves:
                        if (upper and 'k' in move[row][column]) or (not upper and 'K' in move[row][column]):
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
    
    def is_checkmate(self, squares, colour):
        if self.debug:
            st = time.time()
        # Check if king is in check
        if not self.is_check(colour):
            return False
        else:
            piece_list = ['c', 'r', 'h', 'p', 'C', 'R', 'H', 'P']
            # Check each move that puts the king into check and search if any move removes all checks on the king
            # Search through board to find all enemy pieces
            for row in range(PIECE_ROWS):
                for column in range(PIECE_COLUMNS):
                    # Calculate all possible moves of each enemy piece
                    if squares[row][column].has_rival_piece(colour):
                        p = squares[row][column].piece
                        self.calculate_moves(squares, p, row, column, bool=False)
                        if p not in piece_list:
                            break
                        # Filter through all moves to find any enemy moves that check the king
                        for x in p.moves:
                            if x.final.has_rival_piece(p.colour) and x.final.piece.name == 'king':
                                # If it is a check then we need to search for any friendly moves that bring the king out of check
                                
                                # Set checkmated to true to reset for each possible checkmate
                                checkmated = True
                                
                                # Search through all friendly pieces of the king being checked
                                for row1 in range(PIECE_ROWS):
                                    for column1 in range(PIECE_COLUMNS):
                                        # Calculate all possible moves of each friendly piece
                                        if squares[row1][column1].has_team_piece(colour):
                                            friendly_piece = squares[row1][column1].piece
                                            self.calculate_moves(squares, friendly_piece, row1, column1, bool=False)
                                            # For each move calculate if there is a way to get it out of check
                                            for y in friendly_piece.moves:
                                                if self.out_of_check(squares, friendly_piece, y) and not self.flying_general(squares, friendly_piece, y):
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
            new_rows[next_row] = new_rows[next_row][:next_column] + piece + new_rows[next_row][next_column + 1:]
        return new_rows                                     
    
    def kill_king(self, rows, row, column):
        if rows[row][column] == 'k' or rows[row][column] == 'K':
            return True
        return False
        
        
agent = Agent()
agent.calculate_all_possible_moves(None, True, 'random')