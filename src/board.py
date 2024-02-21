from square import Square
from piece import *
from const import *
from move import Move
import copy
import time

class Board:
    def __init__(self):
        # Creates empty 8x8 board array
        self.squares = [[0,0,0,0,0,0,0,0,0] for row in range(PIECE_ROWS)]
        self.create()
        self.add_pieces('red')
        self.add_pieces('black')
        # self.add_custom_board("red")
        # self.add_custom_board("black")
        self.last_move = None
        self.is_in_check = False
        # Variable used to store if king is in check (updated each turn)
        self.checked = False
        self.debug = False
        self.count = 0
        
    def print_board(self):
        print("----------------------------------------------")
        for x in self.squares:
            for i in x:
                if not hasattr(i.piece, 'name'):
                    print("----",end = " ")
                else:
                    print(" " + i.piece.colour[0:1].upper() + i.piece.name[0:1] + " ",end = " ")
            print("\n")
        print("-----------------------------------------------")
        
    def move(self, piece, move):
        initial = move.initial
        final = move.final
        
        # Update squares
        self.squares[initial.row][initial.column].piece = None
        self.squares[final.row][final.column].piece = piece
        
        piece.moved = True
        
        # Clear valid moves
        piece.clear_moves()
        
        # Set last move
        self.last_move = move

    def move_squares(self, squares, piece, move):
        initial = move.initial
        final = move.final
        
        # Update squares
        squares[initial.row][initial.column].piece = None
        squares[final.row][final.column].piece = piece
        
        piece.moved = True
        
        # Clear valid moves
        piece.clear_moves()
        
        # Set last move
        self.last_move = move
                       
    def revoke_move(self, piece, move):
        initial = move.initial
        final = move.final
        
        # Update squares
        self.squares[initial.row][initial.column].piece = piece
        self.squares[final.row][final.column].piece = None
        
        piece.moved = False
        
        # Clear valid moves
        piece.clear_moves()
              
    def valid_move(self, piece, move):
        return move in piece.moves
        # for i in piece.moves:
        #     if move.initial.row == i.initial.row and move.initial.column == i.initial.column and move.final.row == i.final.row and move.final.column == i.final.column:
        #         return True
        # return False
    
    def create(self):
        # Looping each square and creating corresponding Square object
        for row in range(PIECE_ROWS):
            for col in range(PIECE_COLUMNS):
                self.squares[row][col] = Square(row, col)
        
    def add_pieces(self, colour):
        if colour == 'red':
            # Create all pawns
            self.squares[3][0] = Square(3, 1, Pawn(colour))
            self.squares[3][2] = Square(3, 2, Pawn(colour))
            self.squares[3][4] = Square(3, 4, Pawn(colour))
            self.squares[3][6] = Square(3, 6, Pawn(colour))
            self.squares[3][8] = Square(3, 8, Pawn(colour))
            
            # Create Cannon
            self.squares[2][1] = Square(3, 1, Cannon(colour))
            self.squares[2][7] = Square(3, 7, Cannon(colour))
                
            # Create Knights
            self.squares[0][1] = Square(0, 1, Knight(colour))
            self.squares[0][7] = Square(0, 7, Knight(colour))
            
            # Create Elephant
            self.squares[0][2] = Square(0, 2, Elephant(colour))
            self.squares[0][6] = Square(0, 6, Elephant(colour))
            
            # Create Rooks
            self.squares[0][0] = Square(0, 0, Rook(colour))
            self.squares[0][8] = Square(0, 8, Rook(colour))
            # self.squares[9][7] = Square(9, 7, Rook(colour))
            # self.squares[9][8] = Square(9, 8, Rook(colour))
            
            # Create Guard
            self.squares[0][3] = Square(0, 3, Guard(colour))
            self.squares[0][5] = Square(0, 5, Guard(colour))
            
            # Create King
            self.squares[0][4] = Square(0, 4, King(colour))
        else:
            # Create all pawns
            self.squares[6][0] = Square(6, 0, Pawn(colour))
            self.squares[6][2] = Square(6, 2, Pawn(colour))
            self.squares[6][4] = Square(6, 4, Pawn(colour))
            self.squares[6][6] = Square(6, 6, Pawn(colour))
            self.squares[6][8] = Square(6, 8, Pawn(colour))
            
            # Create Cannon
            self.squares[7][1] = Square(7, 1, Cannon(colour))
            self.squares[7][7] = Square(7, 7, Cannon(colour))
                
            # Create Knights
            self.squares[9][1] = Square(9, 1, Knight(colour))
            self.squares[9][7] = Square(9, 7, Knight(colour))
            
            # Create Elephant
            self.squares[9][2] = Square(9, 2, Elephant(colour))
            self.squares[9][6] = Square(9, 6, Elephant(colour))
            
            # Create Rooks
            self.squares[9][0] = Square(9, 0, Rook(colour))
            self.squares[9][8] = Square(9, 8, Rook(colour))
            
            # Create Guard
            self.squares[9][3] = Square(9, 3, Guard(colour))
            self.squares[9][5] = Square(9, 5, Guard(colour))
            
            # Create King
            self.squares[9][4] = Square(9, 4, King(colour))
       
    def add_custom_board(self, colour):
        if colour == 'red':    
                               
            # Create Knights
            self.squares[2][2] = Square(2, 2, Knight(colour))

            # Create Rooks
            self.squares[6][4] = Square(6, 4, Rook(colour))
            
            # Create King
            self.squares[0][4] = Square(0, 4, King(colour))
        else:      
            # Create Cannon
            self.squares[0][8] = Square(0, 8, Cannon(colour))
            
            
            # Create Guard
            self.squares[9][3] = Square(9, 3, Guard(colour))
            self.squares[9][5] = Square(9, 5, Guard(colour))
            
            # Create King
            self.squares[9][4] = Square(9, 4, King(colour))
            
    def calculate_moves(self, piece, row, column, bool=True):
        
        
        def next_knight_moves(row, column):
            possible_moves = []
            #Check top
            if Square.row_in_range(row-1) and Square.column_in_range(column):
                if self.squares[row-1][column].is_empty():
                    possible_moves.append((row-2, column-1))
                    possible_moves.append((row-2, column+1))
            #Check bottom
            if Square.row_in_range(row+1) and Square.column_in_range(column):
                if self.squares[row+1][column].is_empty():
                    possible_moves.append((row+2, column-1))
                    possible_moves.append((row+2, column+1))
            #Check Left
            if Square.row_in_range(row) and Square.column_in_range(column-1):
                if self.squares[row][column-1].is_empty():
                    possible_moves.append((row-1, column-2))
                    possible_moves.append((row+1, column-2))
            #Check Right
            if Square.row_in_range(row) and Square.column_in_range(column+1):
                if self.squares[row][column+1].is_empty():
                    possible_moves.append((row-1, column+2))
                    possible_moves.append((row+1, column+2))
                
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
                    if not self.squares[possible_row][possible_column].empty_or_rival(piece.colour):
                        return
                    if self.squares[possible_row][possible_column].has_rival_piece(piece.colour):
                        initial = Square(row, column)
                        final_piece = self.squares[possible_row][possible_column].piece
                        final = Square(possible_row, possible_column, final_piece)
                        move = Move(initial, final)
                        if bool:
                            if not self.in_check(piece, move) and not self.flying_general(piece, move):
                                piece.add_move(move)
                        else:
                            piece.add_move(move)
                        return
                    initial = Square(row, column)
                    final_piece = self.squares[possible_row][possible_column].piece
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
                    if not self.squares[possible_row][possible_column].empty_or_rival(piece.colour):
                        return
                    if self.squares[possible_row][possible_column].has_rival_piece(piece.colour):
                        initial = Square(row, column)
                        final_piece = self.squares[possible_row][possible_column].piece
                        final = Square(possible_row, possible_column, final_piece)
                        move = Move(initial, final)
                        if bool:
                            if not self.in_check(piece, move) and not self.flying_general(piece, move):
                                piece.add_move(move)
                        else:
                            piece.add_move(move)
                        return
                    initial = Square(row, column)
                    final_piece = self.squares[possible_row][possible_column].piece
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
                    if not self.squares[possible_row][possible_column].empty_or_rival(piece.colour):
                        return
                    if self.squares[possible_row][possible_column].has_rival_piece(piece.colour):
                        initial = Square(row, column)
                        final_piece = self.squares[possible_row][possible_column].piece
                        final = Square(possible_row, possible_column, final_piece)
                        move = Move(initial, final)
                        if bool:
                            if not self.in_check(piece, move) and not self.flying_general(piece, move):
                                piece.add_move(move)
                        else:
                            piece.add_move(move)
                        return
                    initial = Square(row, column)
                    final_piece = self.squares[possible_row][possible_column].piece
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
                    if not self.squares[possible_row][possible_column].empty_or_rival(piece.colour):
                        return
                    if self.squares[possible_row][possible_column].has_rival_piece(piece.colour):
                        initial = Square(row, column)
                        final_piece = self.squares[possible_row][possible_column].piece
                        final = Square(possible_row, possible_column, final_piece)
                        move = Move(initial, final)
                        if bool:
                            if not self.in_check(piece, move) and not self.flying_general(piece, move):
                                piece.add_move(move)
                        else:
                            piece.add_move(move)
                        return
                    initial = Square(row, column)
                    final_piece = self.squares[possible_row][possible_column].piece
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
                    if self.squares[possible_row][possible_column].is_valid_move(piece.colour):
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
                        
            def move_red_rival():
                possible_moves = [
                (row+1, column),
                (row, column+1),
                (row, column-1),
            ]
                for possible_move in possible_moves:
                    possible_row, possible_column = possible_move
                    if possible_row in range(5,10) and Square.column_in_range(possible_column):
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
                            
            def move_black_home():
                possible_move = (row - 1, column)
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
            def move_black_rival():
                possible_moves = [
                (row-1, column),
                (row, column+1),
                (row, column-1),
            ]
                for possible_move in possible_moves:
                    possible_row, possible_column = possible_move
                    if possible_row in range(0,5) and Square.column_in_range(possible_column):
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
                    if not self.squares[possible_row][possible_column].is_empty():
                        # Check whether a rival piece is in a square after the first blocking piece
                        counter += 1
                        # Loop after blocking piece to find next piece
                        while(Square.row_in_range(row + counter)):
                            next_move = (row + counter, column)
                            possible_row, possible_column = next_move
                            # If piece is team piece then no jump occurs and return
                            if self.squares[possible_row][possible_column].has_team_piece(piece.colour):
                                return
                            # If piece is rival then add move to possible moves
                            if self.squares[possible_row][possible_column].has_rival_piece(piece.colour):
                                initial = Square(row, column)
                                final_piece = self.squares[possible_row][possible_column].piece
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
                    final_piece = self.squares[possible_row][possible_column].piece
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
                    if not self.squares[possible_row][possible_column].is_empty():
                        # Check whether a rival piece is in a square after the first blocking piece
                        counter += 1
                        # Loop after blocking piece to find next piece
                        while(Square.row_in_range(row - counter)):
                            next_move = (row - counter, column)
                            possible_row, possible_column = next_move
                            # If piece is team piece then no jump occurs and return
                            if self.squares[possible_row][possible_column].has_team_piece(piece.colour):
                                return
                            # If piece is rival then add move to possible moves
                            if self.squares[possible_row][possible_column].has_rival_piece(piece.colour):
                                initial = Square(row, column)
                                final_piece = self.squares[possible_row][possible_column].piece
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
                    final_piece = self.squares[possible_row][possible_column].piece
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
                    if not self.squares[possible_row][possible_column].is_empty():
                        # Check whether a rival piece is in a square after the first blocking piece
                        counter += 1
                        # Loop after blocking piece to find next piece
                        while(Square.column_in_range(column + counter)):
                            next_move = (row, column + counter)
                            possible_row, possible_column = next_move
                            # If piece is team piece then no jump occurs and return
                            if self.squares[possible_row][possible_column].has_team_piece(piece.colour):
                                return
                            # If piece is rival then add move to possible moves
                            if self.squares[possible_row][possible_column].has_rival_piece(piece.colour):
                                initial = Square(row, column)
                                final_piece = self.squares[possible_row][possible_column].piece
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
                    final_piece = self.squares[possible_row][possible_column].piece
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
                    if not self.squares[possible_row][possible_column].is_empty():
                        # Check whether a rival piece is in a square after the first blocking piece
                        counter += 1
                        # Loop after blocking piece to find next piece
                        while(Square.column_in_range(column - counter)):
                            next_move = (row, column - counter)
                            possible_row, possible_column = next_move
                            # If piece is team piece then no jump occurs and return
                            if self.squares[possible_row][possible_column].has_team_piece(piece.colour):
                                return
                            # If piece is rival then add move to possible moves
                            if self.squares[possible_row][possible_column].has_rival_piece(piece.colour):
                                initial = Square(row, column)
                                final_piece = self.squares[possible_row][possible_column].piece
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
                    final_piece = self.squares[possible_row][possible_column].piece
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
        
    
    # Method used to check if a particular move will put the kings in check by having no pieces inbetween       
    def flying_general(self, piece, move):
        if self.debug:
            st = time.time()
        # new_piece = self.copy_piece(piece)
        # squares = self.copy_squares()
        # self.move_squares(squares, new_piece, move)
        temp_piece = copy.deepcopy(piece)
        temp_board = copy.deepcopy(self)
        temp_board.move(temp_piece, move)
        
        # Find top king piece
        for row in range(3):
            for column in range(PIECE_COLUMNS):
                if temp_board.squares[row][column].has_piece() and temp_board.squares[row][column].piece.name == "king":
                    # king = temp_board.squares[row][column].piece
                    king_col = column
                    king_row = row     
                       
        # Loop through row which king is on and check for rule by checking a piece is between it or no king at the end 
        for row in range(king_row+1, PIECE_ROWS):
            if temp_board.squares[row][king_col].has_piece() and temp_board.squares[row][king_col].piece.name == "king":
                if self.debug:
                    et = time.time()
                    runtime = et - st
                    print("FLYING GENERAL EXECUTION TIME: " + f"{runtime:.15f}")
                return True
            if temp_board.squares[row][king_col].has_piece() and temp_board.squares[row][king_col].piece.name != "king":
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
    def in_check(self, piece, move):
        if self.debug:
            st = time.time()
        temp_piece = copy.deepcopy(piece)
        temp_board = copy.deepcopy(self)
        temp_board.move(temp_piece, move)
        
        for row in range(PIECE_ROWS):
            for column in range(PIECE_COLUMNS):
                if temp_board.squares[row][column].has_rival_piece(piece.colour):
                    p = temp_board.squares[row][column].piece
                    temp_board.calculate_moves(p, row, column, bool=False)
                    for x in p.moves:
                        if x.final.has_rival_piece(p.colour) and x.final.piece.name == 'king':
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
    def is_check(self, next_player):
        if self.debug:
            st = time.time()
        temp_board = copy.deepcopy(self)
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
    def out_of_check(self, piece, move):
        if self.debug:
            st = time.time()
        temp_piece = copy.deepcopy(piece)
        temp_board = copy.deepcopy(self)
        temp_board.move(temp_piece, move)
        
        for row in range(PIECE_ROWS):
            for column in range(PIECE_COLUMNS):
                if temp_board.squares[row][column].has_rival_piece(piece.colour):
                    p = temp_board.squares[row][column].piece
                    temp_board.calculate_moves(p, row, column, bool=False)
                    for x in p.moves:
                        if x.final.has_rival_piece(p.colour) and x.final.piece.name == 'king':
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
    
    def is_checkmate(self, colour):
        if self.debug:
            st = time.time()
        # Check if king is in check
        if not self.is_check(colour):
            return False
        else:
            # Check each move that puts the king into check and search if any move removes all checks on the king
            temp_board = copy.deepcopy(self)
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
                                
    def copy_squares(self):
        if self.debug:
            st = time.time()
        new_squares = [[0,0,0,0,0,0,0,0,0] for row in range(PIECE_ROWS)]
        
        for row in range(PIECE_ROWS):
            for column in range(PIECE_COLUMNS):
                new_squares[row][column] = self.squares[row][column]
                    
        if self.debug:
            et = time.time()
            runtime = et - st
            print("COPY SQUARES EXECUTION TIME: " + f"{runtime:.15f}")
        return new_squares 
    
    def copy_piece(self, piece):
        new_piece = Piece(piece.name, piece.colour, piece.value)
        return new_piece

    def convert_board_to_string(self):
        # temp_board = 'rhegkgehr/000000000/0c00000c0/p0p0p0p0p/000000000/000000000/P0P0P0P0P/0C00000C0/000000000/RHEGKGEHR'
        board_string = ''
        for row in range(PIECE_ROWS):
            for column in range(PIECE_COLUMNS):
                if self.squares[row][column].has_piece():
                    piece =  self.squares[row][column].piece
                    if piece.name == 'knight':
                        if piece.colour == 'black':
                            board_string += 'H'
                        else:
                            board_string += 'h'
                    else:
                        if piece.colour == 'black':
                            board_string += self.squares[row][column].piece.name[0].upper()
                        else:
                            board_string += self.squares[row][column].piece.name[0]
                else:
                    board_string += '0'
            board_string += '/'
            
        board_string = board_string[:-1]  
        return board_string

    def convert_string_to_board(self, string):
        string = '/'.join(string)
        names = {
            'r' : 'rook',
            'h' : 'knight',
            'g' : 'guard',
            'e' : 'elephant',
            'p' : 'pawn',
            'c' : 'cannon',
            'k' : 'king'
        }
        row = 0 
        column = 0
        for char in string:
            if char == '/':
                column = -1
                row += 1
            elif char == '0':
                self.squares[row][column].piece = None
            elif char.isupper():
                piece = Piece(names[char.lower()], 'black', 0)
                self.squares[row][column].piece = piece
            else:
                piece = Piece(names[char], 'red', 0)
                self.squares[row][column].piece = piece
            column += 1
                
        
                          
                                                              