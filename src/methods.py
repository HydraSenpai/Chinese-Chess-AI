from square import Square
from piece import *
from const import *
from move import Move
import copy
import random
import math
import time

def print_row(rows):
        print("----------------------------------------------")
        for row in range(PIECE_ROWS):
            for column in range(PIECE_COLUMNS):    
                print(rows[row][column], end = " ")
            print("\n")
        print("-----------------------------------------------")

def next_states(rows, upper): 
        
        # rows ['h00000000H', '0000000000', '0000000000', '0000000000', '0000000000', '0000000000', '0000000000', '0000000000', 'h00000000H']

        possible_states = []
        count = 0
                                
        for row in range(PIECE_ROWS):
            for column in range(PIECE_COLUMNS):
                # Find every team piece and calculate all moves
                if (rows[row][column].isupper() and upper and rows[row][column] != '0') or (rows[row][column].islower() and not upper and rows[row][column] != '0'):
                    count+=1
                    current_piece = rows[row][column]  
                    moves = calculate_moves(rows, current_piece, row, column, upper, bool=True)
                    # print("PIECE = " + str(current_piece))
                    # Add possible moves to array
                    for move in moves:
                        # print_row(move)
                        possible_states.append(move)
        if len(possible_states) == 0:
            return []
        else:
            return possible_states
 
def is_terminal_state(rows, upper):     
                   
    for row in range(PIECE_ROWS):
        for column in range(PIECE_COLUMNS):
            # Find every team piece and calculate all moves
            if (rows[row][column] != '0') and ((upper and rows[row][column].isupper()) or (not upper and rows[row][column].islower())):
                p = rows[row][column]     
                moves = calculate_moves(rows, p, row, column, upper, bool=True)
                # Add possible moves to array
                if len(moves) >= 1:
                    return False
    return True
                      
def calculate_moves(rows, piece, row, column, upper, bool=True):
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
                if is_valid(possible_row, possible_column) and not (rows[possible_row][possible_column] == 'k' or rows[possible_row][possible_column] == 'K'):
                    moved_rows = move(rows, row, column, possible_row, possible_column, upper, piece)
                    if bool:
                        # if True:
                        if not in_check(moved_rows, upper) and not flying_general(moved_rows):
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
                    if (rows[possible_row][possible_column] == 'k' or rows[possible_row][possible_column] == 'K'):
                        return
                    moved_rows = move(rows, row, column, possible_row, possible_column, upper, piece)
                    if bool:
                        if not in_check(moved_rows, upper) and not flying_general(moved_rows):
                            moves.append(moved_rows)
                    else:
                        moves.append(moved_rows)
                    return
                if (rows[possible_row][possible_column] == 'k' or rows[possible_row][possible_column] == 'K'):
                    return
                else:
                    moved_rows = move(rows, row, column, possible_row, possible_column, upper, piece)
                    if bool:
                        if not in_check(moved_rows, upper) and not flying_general(moved_rows):
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
                    if (rows[possible_row][possible_column] == 'k' or rows[possible_row][possible_column] == 'K'):
                        return
                    moved_rows = move(rows, row, column, possible_row, possible_column, upper, piece)
                    if bool:
                        if not in_check(moved_rows, upper) and not flying_general(moved_rows):
                            moves.append(moved_rows)
                    else:
                        moves.append(moved_rows)
                    return
                if (rows[possible_row][possible_column] == 'k' or rows[possible_row][possible_column] == 'K'):
                    return
                moved_rows = move(rows, row, column, possible_row, possible_column, upper, piece)
                if bool:
                    if not in_check(moved_rows, upper) and not flying_general(moved_rows):
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
                    if (rows[possible_row][possible_column] == 'k' or rows[possible_row][possible_column] == 'K'):
                        return
                    moved_rows = move(rows, row, column, possible_row, possible_column, upper, piece)
                    if bool:
                        if not in_check(moved_rows, upper) and not flying_general(moved_rows):
                            moves.append(moved_rows)
                    else:
                        moves.append(moved_rows)
                    return
                if (rows[possible_row][possible_column] == 'k' or rows[possible_row][possible_column] == 'K'):
                    return
                moved_rows = move(rows, row, column, possible_row, possible_column, upper, piece)
                if bool:
                    if not in_check(moved_rows, upper) and not flying_general(moved_rows):
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
                    if (rows[possible_row][possible_column] == 'k' or rows[possible_row][possible_column] == 'K'):
                        return
                    moved_rows = move(rows, row, column, possible_row, possible_column, upper, piece)
                    if bool:
                        if not in_check(moved_rows, upper) and not flying_general(moved_rows):
                            moves.append(moved_rows)
                    else:
                        moves.append(moved_rows)
                    return
                if (rows[possible_row][possible_column] == 'k' or rows[possible_row][possible_column] == 'K'):
                    return
                moved_rows = move(rows, row, column, possible_row, possible_column, upper, piece)
                if bool:
                    if not in_check(moved_rows, upper) and not flying_general(moved_rows):
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
                    moved_rows = move(rows, row, column, possible_row, possible_column, upper, piece)
                    if bool:
                        if is_check(moved_rows, upper) and not flying_general(moved_rows):
                            if out_of_check(moved_rows, upper):
                                moves.append(moved_rows)
                        elif not in_check(moved_rows, upper) and not flying_general(moved_rows):
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
                    moved_rows = move(rows, row, column, possible_row, possible_column, upper, piece)
                    if bool:
                        if not in_check(moved_rows, upper) and not flying_general(moved_rows):
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
                    moved_rows = move(rows, row, column, possible_row, possible_column, upper, piece)
                    if bool:
                        if not in_check(moved_rows, upper) and not flying_general(moved_rows):
                            moves.append(moved_rows)
                    else:
                        moves.append(moved_rows)
                    
    def next_pawn_moves(row, column):
        def move_red_home():
            possible_move = (row + 1, column)
            possible_row, possible_column = possible_move
            if row_in_range(possible_row) and column_in_range(possible_column):
                if is_valid(possible_row, possible_column) and not (rows[possible_row][possible_column] == 'k' or rows[possible_row][possible_column] == 'K'):
                    moved_rows = move(rows, row, column, possible_row, possible_column, upper, piece)
                    if bool:
                        if not in_check(moved_rows, upper) and not flying_general(moved_rows):
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
                    if is_valid(possible_row, possible_column) and not (rows[possible_row][possible_column] == 'k' or rows[possible_row][possible_column] == 'K'):
                        moved_rows = move(rows, row, column, possible_row, possible_column, upper, piece)
                        if bool:
                            if not in_check(moved_rows, upper) and not flying_general(moved_rows):
                                moves.append(moved_rows)
                        else:
                            moves.append(moved_rows)
                        
        def move_black_home():
            possible_move = (row - 1, column)
            possible_row, possible_column = possible_move
            if row_in_range(possible_row) and column_in_range(possible_column):
                if is_valid(possible_row, possible_column) and not (rows[possible_row][possible_column] == 'k' or rows[possible_row][possible_column] == 'K'):
                    moved_rows = move(rows, row, column, possible_row, possible_column, upper, piece)
                    if bool:
                        if not in_check(moved_rows, upper) and not flying_general(moved_rows):
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
                    if is_valid(possible_row, possible_column) and not (rows[possible_row][possible_column] == 'k' or rows[possible_row][possible_column] == 'K'):
                        moved_rows = move(rows, row, column, possible_row, possible_column, upper, piece)
                        if bool:
                            if not in_check(moved_rows, upper) and not flying_general(moved_rows):
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
                            if (rows[possible_row][possible_column] == 'k' or rows[possible_row][possible_column] == 'K'):
                                return
                            moved_rows = move(rows, row, column, possible_row, possible_column, upper, piece)
                            if bool:
                                if not in_check(moved_rows, upper) and not flying_general(moved_rows):
                                    moves.append(moved_rows)
                            else:
                                moves.append(moved_rows)
                            return
                        counter += 1 
                    return
                if (rows[possible_row][possible_column] == 'k' or rows[possible_row][possible_column] == 'K'):
                    return
                moved_rows = move(rows, row, column, possible_row, possible_column, upper, piece)
                if bool:
                    if not in_check(moved_rows, upper) and not flying_general(moved_rows):
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
                            if (rows[possible_row][possible_column] == 'k' or rows[possible_row][possible_column] == 'K'):
                                return
                            moved_rows = move(rows, row, column, possible_row, possible_column, upper, piece)
                            if bool:
                                if not in_check(moved_rows, upper) and not flying_general(moved_rows):
                                    moves.append(moved_rows)
                            else:
                                moves.append(moved_rows)
                            return
                        counter += 1 
                    return
                if (rows[possible_row][possible_column] == 'k' or rows[possible_row][possible_column] == 'K'):
                    return
                moved_rows = move(rows, row, column, possible_row, possible_column, upper, piece)
                if bool:
                    if not in_check(moved_rows, upper) and not flying_general(moved_rows):
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
                            if (rows[possible_row][possible_column] == 'k' or rows[possible_row][possible_column] == 'K'):
                                return
                            moved_rows = move(rows, row, column, possible_row, possible_column, upper, piece)
                            if bool:
                                if not in_check(moved_rows, upper) and not flying_general(moved_rows):
                                    moves.append(moved_rows)
                            else:
                                moves.append(moved_rows)
                            return
                        counter += 1 
                    return
                if (rows[possible_row][possible_column] == 'k' or rows[possible_row][possible_column] == 'K'):
                    return
                moved_rows = move(rows, row, column, possible_row, possible_column, upper, piece)
                if bool:
                    if not in_check(moved_rows, upper) and not flying_general(moved_rows):
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
                            if (rows[possible_row][possible_column] == 'k' or rows[possible_row][possible_column] == 'K'):
                                return
                            moved_rows = move(rows, row, column, possible_row, possible_column, upper, piece)
                            # print_row(moved_rows)
                            if bool:
                                if not in_check(moved_rows, upper) and not flying_general(moved_rows):
                                    moves.append(moved_rows)
                            else:
                                moves.append(moved_rows)
                            return
                        counter += 1 
                    return
                if (rows[possible_row][possible_column] == 'k' or rows[possible_row][possible_column] == 'K'):
                    return
                moved_rows = move(rows, row, column, possible_row, possible_column, upper, piece)
                if bool:
                    if not in_check(moved_rows, upper) and not flying_general(moved_rows):
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
def flying_general(rows):
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
            return True
        if rows[row][king_col] != '0' and rows[row][king_col] != 'k' and rows[row][king_col] != 'K':
            return False
    return False
    
# Method used to calculate if moving a friendly piece results in its own checkmate (to prevent moves that put yourself in checkmate)
def in_check(rows, upper):
    piece_list = ['c', 'r', 'h', 'p', 'C', 'R', 'H', 'P']
    
    for row in range(PIECE_ROWS):
        for column in range(PIECE_COLUMNS):
            # Check for enemy pieces by finding opposite cases
            if (upper and rows[row][column].islower() and rows[row][column] != '0') or (not upper and rows[row][column].isupper() and rows[row][column] != '0'):
                p = rows[row][column]
                if p not in piece_list:
                    break
                # Calculate moves of enemy piece
                moves = calculate_moves(rows, p, row, column, (not upper), bool=False)
                # For each move opponent check whether the friendly king has been taken
                for move in moves:
                    if (upper and 'k' in move[row][column]) or (not upper and 'K' in move[row][column]):
                        return True
    return False
    
# Method used to see if king is currently in check
def is_check(rows, upper):
    piece_list = ['c', 'r', 'h', 'p', 'C', 'R', 'H', 'P']
    # Search through board to find all enemy pieces
    for row in range(PIECE_ROWS):
        for column in range(PIECE_COLUMNS):
            # Calculate all possible moves of each piece
            if (upper and rows[row][column].islower() and rows[row][column] != '0') or (not upper and rows[row][column].isupper() and rows[row][column] != '0'):
                p = rows[row][column]
                if p not in piece_list:
                    break
                moves = calculate_moves(rows, p, row, column, not upper, bool=False)
                # Search through all moves to find if any are a checkmate
                for move in moves:
                    if (upper and 'k' in move[row][column]) or (not upper and 'K' in move[row][column]):
                        checked = True
                        return True
    checked = False
    return False
    
# Method used to calculate if moving a friendly piece results in getting out of checkmate
def out_of_check(rows, upper):
    
    for row in range(PIECE_ROWS):
        for column in range(PIECE_COLUMNS):
            if (upper and rows[row][column].islower() and rows[row][column] != '0') or (not upper and rows[row][column].isupper() and rows[row][column] != '0'):
                p = rows[row][column].piece
                moves = calculate_moves(rows, p, row, column, upper, bool=False)
                for move in moves:
                    if (upper and 'k' in move[row][column]) or (not upper and 'K' in move[row][column]):
                        return False
    return True 
    
def is_checkmate(squares, colour):
    # Check if king is in check
    if not is_check(colour):
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
                    calculate_moves(squares, p, row, column, bool=False)
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
                                        calculate_moves(squares, friendly_piece, row1, column1, bool=False)
                                        # For each move calculate if there is a way to get it out of check
                                        for y in friendly_piece.moves:
                                            if out_of_check(squares, friendly_piece, y) and not flying_general(squares, friendly_piece, y):
                                                # If a move successfully gets out of check then we can stop searching for that check and move on
                                                checkmated = False
                                                row1 = PIECE_ROWS - 1
                                                column1 = PIECE_COLUMNS - 1
                                                break
                            
                            # Since no moves were found to turn checkmate false after checking all moves for a specific check
                            # Condition then the king has been checkmated
                            if checkmated == True:
                                return True
                                             
        return False

def move(rows, row, column, next_row, next_column, upper, piece):
    new_rows = rows.copy()
    # Update new_rows
    new_rows[row] = new_rows[row][:column] + '0' + new_rows[row][column + 1:]
    if upper:
        new_rows[next_row] = new_rows[next_row][:next_column] + piece.upper() + new_rows[next_row][next_column + 1:]
    else:
        new_rows[next_row] = new_rows[next_row][:next_column] + piece + new_rows[next_row][next_column + 1:]
    return new_rows  