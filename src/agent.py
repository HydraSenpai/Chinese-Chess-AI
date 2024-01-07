from square import Square
from piece import *
from const import *
from move import Move
import copy
import random
import math

class Agent:
    def __init__(self):
        self.board = None
        # self.depth = 1
    
    def update_board(self, board):
        self.board = board        
          
    def calculate_moves(self, piece, row, column, bool=True):
    
        def next_knight_moves(row, column):
            possible_moves = []
            #Check top
            if Square.row_in_range(row-1) and Square.column_in_range(column):
                if self.board.squares[row-1][column].is_empty():
                    possible_moves.append((row-2, column-1))
                    possible_moves.append((row-2, column+1))
            #Check bottom
            if Square.row_in_range(row+1) and Square.column_in_range(column):
                if self.board.squares[row+1][column].is_empty():
                    possible_moves.append((row+2, column-1))
                    possible_moves.append((row+2, column+1))
            #Check Left
            if Square.row_in_range(row) and Square.column_in_range(column-1):
                if self.board.squares[row][column-1].is_empty():
                    possible_moves.append((row-1, column-2))
                    possible_moves.append((row+1, column-2))
            #Check Right
            if Square.row_in_range(row) and Square.column_in_range(column+1):
                if self.board.squares[row][column+1].is_empty():
                    possible_moves.append((row-1, column+2))
                    possible_moves.append((row+1, column+2))
                
            for possible_move in possible_moves:
                possible_row, possible_column = possible_move
                if Square.row_in_range(possible_row) and Square.column_in_range(possible_column):
                    if self.board.squares[possible_row][possible_column].is_valid_move(piece.colour):
                        initial = Square(row, column)
                        final_piece = self.board.squares[possible_row][possible_column].piece
                        final = Square(possible_row, possible_column, final_piece)
                        move = Move(initial, final)
                        if bool:
                            if not self.in_check(piece, move) and not self.flying_general(piece, move):
                                piece.add_move(move)
                            else:
                                break
                        else:
                            piece.add_move(move)
    
        def next_rook_moves(row, column):
            #Downward Check
            def downward_check():
                counter = 1
                next_move = (row + counter, column)
                while(Square.row_in_range(row + counter)):
                    next_move = (row + counter, column)
                    possible_row, possible_column = next_move
                    if not self.board.squares[possible_row][possible_column].empty_or_rival(piece.colour):
                        return
                    if self.board.squares[possible_row][possible_column].has_rival_piece(piece.colour):
                        initial = Square(row, column)
                        final_piece = self.board.squares[possible_row][possible_column].piece
                        final = Square(possible_row, possible_column, final_piece)
                        move = Move(initial, final)
                        if bool:
                            if not self.in_check(piece, move) and not self.flying_general(piece, move):
                                piece.add_move(move)
                        else:
                            piece.add_move(move)
                        return
                    initial = Square(row, column)
                    final_piece = self.board.squares[possible_row][possible_column].piece
                    final = Square(possible_row, possible_column, final_piece)
                    move = Move(initial, final)
                    if bool:
                        if not self.in_check(piece, move) and not self.flying_general(piece, move):
                            piece.add_move(move)
                    else:
                        piece.add_move(move)
                    counter += 1
            #Upward Check
            def upward_check():
                counter = 1
                next_move = (row - counter, column)
                while(Square.row_in_range(row - counter)):
                    next_move = (row - counter, column)
                    possible_row, possible_column = next_move
                    if not self.board.squares[possible_row][possible_column].empty_or_rival(piece.colour):
                        return
                    if self.board.squares[possible_row][possible_column].has_rival_piece(piece.colour):
                        initial = Square(row, column)
                        final_piece = self.board.squares[possible_row][possible_column].piece
                        final = Square(possible_row, possible_column, final_piece)
                        move = Move(initial, final)
                        if bool:
                            if not self.in_check(piece, move) and not self.flying_general(piece, move):
                                piece.add_move(move)
                        else:
                            piece.add_move(move)
                        return
                    initial = Square(row, column)
                    final_piece = self.board.squares[possible_row][possible_column].piece
                    final = Square(possible_row, possible_column, final_piece)
                    move = Move(initial, final)
                    if bool:
                        if not self.in_check(piece, move) and not self.flying_general(piece, move):
                            piece.add_move(move)
                    else:
                        piece.add_move(move)
                    counter += 1
            #Right Check
            def right_check():
                counter = 1
                next_move = (row, column + counter)
                while(Square.column_in_range(column + counter)):
                    next_move = (row, column + counter)
                    possible_row, possible_column = next_move
                    if not self.board.squares[possible_row][possible_column].empty_or_rival(piece.colour):
                        return
                    if self.board.squares[possible_row][possible_column].has_rival_piece(piece.colour):
                        initial = Square(row, column)
                        final_piece = self.board.squares[possible_row][possible_column].piece
                        final = Square(possible_row, possible_column, final_piece)
                        move = Move(initial, final)
                        if bool:
                            if not self.in_check(piece, move) and not self.flying_general(piece, move):
                                piece.add_move(move)
                        else:
                            piece.add_move(move)
                        return
                    initial = Square(row, column)
                    final_piece = self.board.squares[possible_row][possible_column].piece
                    final = Square(possible_row, possible_column, final_piece)
                    move = Move(initial, final)
                    if bool:
                        if not self.in_check(piece, move) and not self.flying_general(piece, move):
                            piece.add_move(move)
                    else:
                        piece.add_move(move)
                    counter += 1
            #Left Check
            def left_check():
                counter = 1
                next_move = (row, column - counter)
                while(Square.column_in_range(column - counter)):
                    next_move = (row, column - counter)
                    possible_row, possible_column = next_move
                    if not self.board.squares[possible_row][possible_column].empty_or_rival(piece.colour):
                        return
                    if self.board.squares[possible_row][possible_column].has_rival_piece(piece.colour):
                        initial = Square(row, column)
                        final_piece = self.board.squares[possible_row][possible_column].piece
                        final = Square(possible_row, possible_column, final_piece)
                        move = Move(initial, final)
                        if bool:
                            if not self.in_check(piece, move) and not self.flying_general(piece, move):
                                piece.add_move(move)
                        else:
                            piece.add_move(move)
                        return
                    initial = Square(row, column)
                    final_piece = self.board.squares[possible_row][possible_column].piece
                    final = Square(possible_row, possible_column, final_piece)
                    move = Move(initial, final)
                    if bool:
                        if not self.in_check(piece, move) and not self.flying_general(piece, move):
                            piece.add_move(move)
                    else:
                        piece.add_move(move)
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
            if piece.colour == 'red':
                max_row = 3
                min_row = 0
            else:
                max_row = 10
                min_row = 7
                
            for possible_move in possible_moves:
                possible_row, possible_column = possible_move
                if possible_column in range(min_column, max_column) and possible_row in range(min_row, max_row):
                    if self.board.squares[possible_row][possible_column].is_valid_move(piece.colour):
                        initial = Square(row, column)
                        final = Square(possible_row, possible_column)
                        move = Move(initial, final)
                        if bool:
                            if self.is_check(piece.colour) and not self.flying_general(piece, move):
                                if self.out_of_check(piece, move):
                                    piece.add_move(move)
                            elif not self.in_check(piece, move) and not self.flying_general(piece, move):
                                piece.add_move(move)
                        else:
                            piece.add_move(move)
                        
        def next_guard_moves(row, column):
            possible_moves = [
                (row+1, column+1),
                (row-1, column-1),
                (row-1, column+1),
                (row+1, column-1),
            ]
            max_column = 6
            min_column = 3
            if piece.colour == 'red':
                max_row = 3
                min_row = 0
            else:
                max_row = 10
                min_row = 7
            for possible_move in possible_moves:
                possible_row, possible_column = possible_move
                if possible_column in range(min_column, max_column) and possible_row in range(min_row, max_row):
                    if self.board.squares[possible_row][possible_column].is_valid_move(piece.colour):
                        initial = Square(row, column)
                        final_piece = self.board.squares[possible_row][possible_column].piece
                        final = Square(possible_row, possible_column, final_piece)
                        move = Move(initial, final)
                        if bool:
                            if not self.in_check(piece, move) and not self.flying_general(piece, move):
                                piece.add_move(move)
                        else:
                            piece.add_move(move)
        
        # Does not check if piece is blocking the move yet                                 
        def next_elephant_moves(row, column):
            possible_moves = []
            #Check top
            if Square.row_in_range(row+2) and Square.column_in_range(column+2):
                if self.squares[row+1][column+1].is_empty():
                    if piece.colour == "red" and row+2 <= 4 or piece.colour == "black":
                        possible_moves.append((row+2, column+2))
            #Check bottom
            if Square.row_in_range(row-2) and Square.column_in_range(column-2):
                if self.squares[row-1][column-1].is_empty():
                    if piece.colour == "black" and row-2 >= 5 or piece.colour == "red":
                        possible_moves.append((row-2, column-2))
            #Check Left
            if Square.row_in_range(row+2) and Square.column_in_range(column-2):
                if self.squares[row+1][column-1].is_empty():
                    if piece.colour == "red" and row+2 <= 4 or piece.colour == "black":
                        possible_moves.append((row+2, column-2))
            #Check Right
            if Square.row_in_range(row-2) and Square.column_in_range(column+2):
                if self.squares[row-1][column+1].is_empty():
                    if piece.colour == "black" and row-2 >= 5 or piece.colour == "red":
                        possible_moves.append((row-2, column+2))
            
            for possible_move in possible_moves:
                possible_row, possible_column = possible_move
                if Square.row_in_range(possible_row) and Square.column_in_range(possible_column):
                    if self.squares[possible_row][possible_column].is_valid_move(piece.colour):
                        initial = Square(row, column)
                        final_piece = self.squares[possible_row][possible_column].piece
                        final = Square(possible_row, possible_column, final_piece)
                        move = Move(initial, final)
                        if bool:
                            if not self.in_check(piece, move) and not self.flying_general(piece, move):
                                piece.add_move(move)
                        else:
                            piece.add_move(move)
                        
        def next_pawn_moves(row, column):
            def move_red_home():
                possible_move = (row + 1, column)
                possible_row, possible_column = possible_move
                if Square.row_in_range(possible_row) and Square.column_in_range(possible_column):
                    if self.board.squares[possible_row][possible_column].is_valid_move(piece.colour):
                        initial = Square(row, column)
                        final_piece = self.board.squares[possible_row][possible_column].piece
                        final = Square(possible_row, possible_column, final_piece)
                        move = Move(initial, final)
                        if bool:
                            if not self.in_check(piece, move) and not self.flying_general(piece, move):
                                piece.add_move(move)
                        else:
                            piece.add_move(move)
                        
            def move_red_rival():
                possible_moves = [
                (row+1, column),
                (row, column+1),
                (row, column-1),
            ]
                for possible_move in possible_moves:
                    possible_row, possible_column = possible_move
                    if possible_row in range(5,10) and Square.column_in_range(possible_column):
                        if self.board.squares[possible_row][possible_column].is_valid_move(piece.colour):
                            initial = Square(row, column)
                            final_piece = self.board.squares[possible_row][possible_column].piece
                            final = Square(possible_row, possible_column, final_piece)
                            move = Move(initial, final)
                            if bool:
                                if not self.in_check(piece, move) and not self.flying_general(piece, move):
                                    piece.add_move(move)
                            else:
                                piece.add_move(move)
                            
            def move_black_home():
                possible_move = (row - 1, column)
                possible_row, possible_column = possible_move
                if Square.row_in_range(possible_row) and Square.column_in_range(possible_column):
                    if self.board.squares[possible_row][possible_column].is_valid_move(piece.colour):
                        initial = Square(row, column)
                        final_piece = self.board.squares[possible_row][possible_column].piece
                        final = Square(possible_row, possible_column, final_piece)
                        move = Move(initial, final)
                        if bool:
                            if not self.in_check(piece, move) and not self.flying_general(piece, move):
                                piece.add_move(move)
                        else:
                            piece.add_move(move)
            def move_black_rival():
                possible_moves = [
                (row-1, column),
                (row, column+1),
                (row, column-1),
            ]
                for possible_move in possible_moves:
                    possible_row, possible_column = possible_move
                    if possible_row in range(0,5) and Square.column_in_range(possible_column):
                        if self.board.squares[possible_row][possible_column].is_valid_move(piece.colour):
                            initial = Square(row, column)
                            final_piece = self.board.squares[possible_row][possible_column].piece
                            final = Square(possible_row, possible_column, final_piece)
                            move = Move(initial, final)
                            if bool:
                                if not self.in_check(piece, move) and not self.flying_general(piece, move):
                                    piece.add_move(move)
                            else:
                                piece.add_move(move)
            
            if piece.colour == 'red':
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
                while(Square.row_in_range(row + counter)):
                    next_move = (row + counter, column)
                    possible_row, possible_column = next_move
                    if not self.board.squares[possible_row][possible_column].is_empty():
                        # Check whether a rival piece is in a square after the first blocking piece
                        counter += 1
                        # Loop after blocking piece to find next piece
                        while(Square.row_in_range(row + counter)):
                            next_move = (row + counter, column)
                            possible_row, possible_column = next_move
                            # If piece is team piece then no jump occurs and return
                            if self.board.squares[possible_row][possible_column].has_team_piece(piece.colour):
                                return
                            # If piece is rival then add move to possible moves
                            if self.board.squares[possible_row][possible_column].has_rival_piece(piece.colour):
                                initial = Square(row, column)
                                final_piece = self.board.squares[possible_row][possible_column].piece
                                final = Square(possible_row, possible_column, final_piece)
                                move = Move(initial, final)
                                if bool:
                                    if not self.in_check(piece, move) and not self.flying_general(piece, move):
                                        piece.add_move(move)
                                else:
                                    piece.add_move(move)
                                return
                            counter += 1 
                        return
                    initial = Square(row, column)
                    final_piece = self.board.squares[possible_row][possible_column].piece
                    final = Square(possible_row, possible_column, final_piece)
                    move = Move(initial, final)
                    if bool:
                        if not self.in_check(piece, move) and not self.flying_general(piece, move):
                            piece.add_move(move)
                    else:
                        piece.add_move(move)
                    counter += 1
            #Upward Check
            def upward_check():
                counter = 1
                next_move = (row - counter, column)
                # Loop until check either isn't on board or is intercepted by own piece or rival piece
                while(Square.row_in_range(row - counter)):
                    next_move = (row - counter, column)
                    possible_row, possible_column = next_move
                    # Check whether move contains a blocking piece
                    if not self.board.squares[possible_row][possible_column].is_empty():
                        # Check whether a rival piece is in a square after the first blocking piece
                        counter += 1
                        # Loop after blocking piece to find next piece
                        while(Square.row_in_range(row - counter)):
                            next_move = (row - counter, column)
                            possible_row, possible_column = next_move
                            # If piece is team piece then no jump occurs and return
                            if self.board.squares[possible_row][possible_column].has_team_piece(piece.colour):
                                return
                            # If piece is rival then add move to possible moves
                            if self.board.squares[possible_row][possible_column].has_rival_piece(piece.colour):
                                initial = Square(row, column)
                                final_piece = self.board.squares[possible_row][possible_column].piece
                                final = Square(possible_row, possible_column, final_piece)
                                move = Move(initial, final)
                                if bool:
                                    if not self.in_check(piece, move) and not self.flying_general(piece, move):
                                        piece.add_move(move)
                                else:
                                    piece.add_move(move)
                                return
                            counter += 1 
                        return
                    initial = Square(row, column)
                    final_piece = self.board.squares[possible_row][possible_column].piece
                    final = Square(possible_row, possible_column, final_piece)
                    move = Move(initial, final)
                    if bool:
                        if not self.in_check(piece, move) and not self.flying_general(piece, move):
                            piece.add_move(move)
                    else:
                        piece.add_move(move)
                    counter += 1
            #Right Check
            def right_check():
                counter = 1
                next_move = (row, column + counter)
                while(Square.column_in_range(column + counter)):
                    next_move = (row, column + counter)
                    possible_row, possible_column = next_move
                    if not self.board.squares[possible_row][possible_column].is_empty():
                        # Check whether a rival piece is in a square after the first blocking piece
                        counter += 1
                        # Loop after blocking piece to find next piece
                        while(Square.column_in_range(column + counter)):
                            next_move = (row, column + counter)
                            possible_row, possible_column = next_move
                            # If piece is team piece then no jump occurs and return
                            if self.board.squares[possible_row][possible_column].has_team_piece(piece.colour):
                                return
                            # If piece is rival then add move to possible moves
                            if self.board.squares[possible_row][possible_column].has_rival_piece(piece.colour):
                                initial = Square(row, column)
                                final_piece = self.board.squares[possible_row][possible_column].piece
                                final = Square(possible_row, possible_column, final_piece)
                                move = Move(initial, final)
                                if bool:
                                    if not self.in_check(piece, move) and not self.flying_general(piece, move):
                                        piece.add_move(move)
                                else:
                                    piece.add_move(move)
                                return
                            counter += 1 
                        return
                    initial = Square(row, column)
                    final_piece = self.board.squares[possible_row][possible_column].piece
                    final = Square(possible_row, possible_column, final_piece)
                    move = Move(initial, final)
                    if bool:
                        if not self.in_check(piece, move) and not self.flying_general(piece, move):
                            piece.add_move(move)
                    else:
                        piece.add_move(move)
                    counter += 1
            #Left Check
            def left_check():
                counter = 1
                next_move = (row, column - counter)
                while(Square.column_in_range(column - counter)):
                    next_move = (row, column - counter)
                    possible_row, possible_column = next_move
                    if not self.board.squares[possible_row][possible_column].is_empty():
                        # Check whether a rival piece is in a square after the first blocking piece
                        counter += 1
                        # Loop after blocking piece to find next piece
                        while(Square.column_in_range(column - counter)):
                            next_move = (row, column - counter)
                            possible_row, possible_column = next_move
                            # If piece is team piece then no jump occurs and return
                            if self.board.squares[possible_row][possible_column].has_team_piece(piece.colour):
                                return
                            # If piece is rival then add move to possible moves
                            if self.board.squares[possible_row][possible_column].has_rival_piece(piece.colour):
                                initial = Square(row, column)
                                final_piece = self.board.squares[possible_row][possible_column].piece
                                final = Square(possible_row, possible_column, final_piece)
                                move = Move(initial, final)
                                if bool:
                                    if not self.in_check(piece, move) and not self.flying_general(piece, move):
                                        piece.add_move(move)
                                else:
                                    piece.add_move(move)
                                return
                            counter += 1 
                        return
                    initial = Square(row, column)
                    final_piece = self.board.squares[possible_row][possible_column].piece
                    final = Square(possible_row, possible_column, final_piece)
                    move = Move(initial, final)
                    if bool:
                        if not self.in_check(piece, move) and not self.flying_general(piece, move):
                            piece.add_move(move)
                    else:
                        piece.add_move(move)
                    counter += 1
            downward_check()
            upward_check()
            left_check()
            right_check()

        if piece.name == 'pawn':
            next_pawn_moves(row, column)
        elif piece.name == 'cannon':
            next_cannon_moves(row, column)
        elif piece.name == 'knight':
            next_knight_moves(row, column)
        elif piece.name == 'elephant':
            next_elephant_moves(row, column)
        elif piece.name == 'guard':
            next_guard_moves(row, column)
        elif piece.name == 'king':
            next_king_moves(row, column)
        elif piece.name == 'rook':
            next_rook_moves(row, column)
          
    def move(self, piece, move):
        initial = move.initial
        final = move.final
        
        # Update squares
        self.board.squares[initial.row][initial.column].piece = None
        self.board.squares[final.row][final.column].piece = piece
        
        piece.moved = True
        
        # Clear valid moves
        piece.clear_moves()
        
        # Set last move
        self.last_move = move
        
    # Method used to check if a particular move will put the kings in check by having no pieces inbetween       
    def flying_general(self, piece, move):
        temp_piece = copy.deepcopy(piece)
        temp_board = copy.deepcopy(self.board)
        temp_board.move(temp_piece, move)
        
        # Find top king piece
        for row in range(3):
            for column in range(PIECE_COLUMNS):
                if temp_board.squares[row][column].has_piece() and temp_board.squares[row][column].piece.name == "king":
                    # king = temp_board.board.squares[row][column].piece
                    king_col = column
                    king_row = row     
                       
        # Loop through row which king is on and check for rule by checking a piece is between it or no king at the end 
        for row in range(king_row+1, PIECE_ROWS):
            if temp_board.squares[row][king_col].has_piece() and temp_board.squares[row][king_col].piece.name == "king":
                return True
            if temp_board.squares[row][king_col].has_piece() and temp_board.squares[row][king_col].piece.name != "king":
                return False
        return False
    
    # Method used to calculate if moving a friendly piece results in its own checkmate (to prevent moves that put yourself in checkmate)
    def in_check(self, piece, move):
        temp_piece = copy.deepcopy(piece)
        temp_board = copy.deepcopy(self.board)
        temp_board.move(temp_piece, move)
        
        for row in range(PIECE_ROWS):
            for column in range(PIECE_COLUMNS):
                if temp_board.squares[row][column].has_rival_piece(piece.colour):
                    p = temp_board.squares[row][column].piece
                    temp_board.calculate_moves(p, row, column, bool=False)
                    for x in p.moves:
                        if x.final.has_rival_piece(p.colour) and x.final.piece.name == 'king':
                            return True
        return False
    
    # Method used to see if king is currently in check
    def is_check(self, next_player):
        temp_board = copy.deepcopy(self.board)
        # Search through board to find all enemy pieces
        for row in range(PIECE_ROWS):
            for column in range(PIECE_COLUMNS):
                # Calculate all possible moves of each piece
                if temp_board.squares[row][column].has_rival_piece(next_player):
                    p = temp_board.squares[row][column].piece
                    temp_board.calculate_moves(p, row, column, bool=False)
                    # Search through all moves to find if any are a checkmate
                    for x in p.moves:
                        if x.final.has_rival_piece(p.colour) and x.final.piece.name == 'king':
                            # print('is check method = True')
                            self.checked = True
                            return True
        # print('is check method = False')
        self.checked = False
        return False
    
    # Method used to calculate if moving a friendly piece results in getting out of checkmate
    def out_of_check(self, piece, move):
        temp_piece = copy.deepcopy(piece)
        temp_board = copy.deepcopy(self.board)
        temp_board.move(temp_piece, move)
        
        for row in range(PIECE_ROWS):
            for column in range(PIECE_COLUMNS):
                if temp_board.squares[row][column].has_rival_piece(piece.colour):
                    p = temp_board.squares[row][column].piece
                    temp_board.calculate_moves(p, row, column, bool=False)
                    for x in p.moves:
                        if x.final.has_rival_piece(p.colour) and x.final.piece.name == 'king':
                            print("out of check method = False")
                            return False
        print("out of check method = True")
        return True 
    
    def is_checkmate(self, colour):
        print(str(colour))
        # Check if king is in check
        if not self.is_check(colour):
            return False
        else:
            # Check each move that puts the king into check and search if any move removes all checks on the king
            temp_board = copy.deepcopy(self.board)
            # Search through board to find all enemy pieces
            for row in range(PIECE_ROWS):
                for column in range(PIECE_COLUMNS):
                    # Calculate all possible moves of each enemy piece
                    if temp_board.squares[row][column].has_rival_piece(colour):
                        p = temp_board.squares[row][column].piece
                        temp_board.calculate_moves(p, row, column, bool=False)
                        # Filter through all moves to find any enemy moves that check the king
                        for x in p.moves:
                            if x.final.has_rival_piece(p.colour) and x.final.piece.name == 'king':
                                print(str(p.name) + ", " + str(p.colour) + ", " + str(x.initial.row) + "," + str(x.initial.column))
                                # If it is a check then we need to search for any friendly moves that bring the king out of check
                                
                                # Set checkmated to true to reset for each possible checkmate
                                checkmated = True
                                
                                # Search through all friendly pieces of the king being checked
                                for row1 in range(PIECE_ROWS):
                                    for column1 in range(PIECE_COLUMNS):
                                        # Calculate all possible moves of each friendly piece
                                        if temp_board.squares[row1][column1].has_team_piece(colour):
                                            friendly_piece = temp_board.squares[row1][column1].piece
                                            temp_board.calculate_moves(friendly_piece, row1, column1, bool=False)
                                            # For each move calculate if there is a way to get it out of check
                                            for y in friendly_piece.moves:
                                                print(str(friendly_piece.name) + " " + str(friendly_piece.colour))
                                                print(y.initial.row)
                                                print(y.initial.column)
                                                print(y.final.row)
                                                print(y.final.column)
                                                if self.out_of_check(friendly_piece, y) and not self.flying_general(friendly_piece, y):
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
                                
    def calculate_all_possible_moves(self, colour, level):
        pieces = []
        possible_moves = []
        check = False
        pathDictionary = {}
        pathDictionary.clear()
        moves = []
        scores = []
        # We need to first calculate if king is in check to filter moves
        if self.is_check(colour):
            check = True
        else:
            check = False
                                
        for row in range(PIECE_ROWS):
                for column in range(PIECE_COLUMNS):
                    # Find every team piece and calculate all moves
                    if self.board.squares[row][column].has_team_piece(colour):
                        p = self.board.squares[row][column].piece     
                        p.clear_moves()
                        self.board.calculate_moves(p, row, column, bool=False)
                        # Add possible moves to array
                        for x in p.moves:
                            if p.name == 'king':
                                if self.is_check(p.colour) and not self.flying_general(p, x):
                                    if self.out_of_check(p, x):
                                        pieces.append(p)
                                        possible_moves.append(x)
                                elif not self.in_check(p, x) and not self.flying_general(p, x):
                                    pieces.append(p)
                                    possible_moves.append(x)
                            elif check:
                                if not self.in_check(p, x) and not self.flying_general(p, x):
                                    if self.out_of_check(p,x):
                                        pieces.append(p)
                                        possible_moves.append(x)
                            elif not self.in_check(p, x) and not self.flying_general(p, x):
                                pieces.append(p)
                                possible_moves.append(x)
        if len(possible_moves) == 0:
            return None
        if level == "beginner":
            choice = random.randint(0, len(possible_moves) - 1)
            return (pieces[choice], possible_moves[choice])
        else:
        # Here we can insert moves into algorithm to find optimal move
            choice = random.randint(0, len(possible_moves) - 1)
            return (pieces[choice], possible_moves[choice])
    
    def evaluation(self, move):
        return random.randint(1, 10000)
 
    # Returns all moves from a given board and colour and returns them as boards
    def next_states(self, board, colour):
        possible_states = []
        check = False
        # We need to first calculate if king is in check to filter moves
        if self.is_check(colour):
            check = True
        else:
            check = False
                                
        for row in range(PIECE_ROWS):
                for column in range(PIECE_COLUMNS):
                    # Find every team piece and calculate all moves
                    if board.squares[row][column].has_team_piece(colour):
                        p = board.squares[row][column].piece     
                        p.clear_moves()
                        board.calculate_moves(p, row, column, bool=False)
                        # Add possible moves to array
                        for x in p.moves:
                            if p.name == 'king':
                                if self.is_check(p.colour) and not self.flying_general(p, x):
                                    if self.out_of_check(p, x):
                                        temp = copy.deepcopy(board)
                                        temp.move(p, x)
                                        possible_states.append(temp)
                                elif not self.in_check(p, x) and not self.flying_general(p, x):
                                    temp = copy.deepcopy(board)
                                    temp.move(p, x)
                                    possible_states.append(temp)
                            elif check:
                                if not self.in_check(p, x) and not self.flying_general(p, x):
                                    if self.out_of_check(p,x):
                                        temp = copy.deepcopy(board)
                                        temp.move(p, x)
                                        possible_states.append(temp)
                            elif not self.in_check(p, x) and not self.flying_general(p, x):
                                temp = copy.deepcopy(board)
                                temp.move(p, x)
                                possible_states.append(temp)
        if len(possible_states) == 0:
            return None
        else:
            return possible_states
            
    def minimax(self, position, depth, alpha, beta, maximum, pathDictionary, moves, scores):
        print(depth)
        if maximum:
            colour = "black"
        else:
            colour = "red"
            
        if depth <= 0 or self.next_states(position, colour) == None:
            return self.evaluation(position)
            
        if maximum:
            if str(position.squares) in pathDictionary:
                return pathDictionary[str(position.squares)]
            maxEval = -math.inf
            next_turns = self.next_states(position, colour)
            for child in next_turns:
                eval = self.minimax(child, depth - 1, alpha, beta, False, pathDictionary, moves, scores)
                maxEval = max(maxEval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            moves.append(position.squares)
            scores.append(maxEval)
            pathDictionary[str(position.squares)] = maxEval
            
            return maxEval
        
        else:
            if str(position.squares) in pathDictionary:
                return pathDictionary[str(position.squares)]
            minEval = math.inf
            next_turns = self.next_states(position, colour)
            for child in next_turns:
                eval = self.minimax(child, depth - 1, alpha, beta, True, pathDictionary, moves, scores)
                minEval = min(minEval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            moves[maxEval] = position.squares
            pathDictionary[str(position.squares)] = minEval
            return minEval
        
            
        
        