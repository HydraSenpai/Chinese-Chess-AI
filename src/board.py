from square import Square
from piece import *
from const import *
from move import Move

class Board:
    def __init__(self):
        # Creates empty 8x8 board array
        self.squares = [[0,0,0,0,0,0,0,0,0] for row in range(PIECE_ROWS)]
        self.create()
        self.add_pieces('red')
        self.add_pieces('black')
        self.last_move = None
        
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
            
    def calculate_moves(self, piece, row, column):
        
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
                    if self.squares[possible_row][possible_column].empty_or_rival(piece.colour):
                        initial = Square(row, column)
                        final_piece = self.squares[possible_row][possible_column].piece
                        final = Square(possible_row, possible_column, final_piece)
                        move = Move(initial, final)
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
                        piece.add_move(move)
                        return
                    initial = Square(row, column)
                    final_piece = self.squares[possible_row][possible_column].piece
                    final = Square(possible_row, possible_column, final_piece)
                    move = Move(initial, final)
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
                        final = Square(possible_row, possible_column)
                        move = Move(initial, final)
                        piece.add_move(move)
                        return
                    initial = Square(row, column)
                    final = Square(possible_row, possible_column)
                    move = Move(initial, final)
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
                        final = Square(possible_row, possible_column)
                        move = Move(initial, final)
                        piece.add_move(move)
                        return
                    initial = Square(row, column)
                    final = Square(possible_row, possible_column)
                    move = Move(initial, final)
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
                        final = Square(possible_row, possible_column)
                        move = Move(initial, final)
                        piece.add_move(move)
                        return
                    initial = Square(row, column)
                    final = Square(possible_row, possible_column)
                    move = Move(initial, final)
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
                    if self.squares[possible_row][possible_column].empty_or_rival(piece.colour):
                        initial = Square(row, column)
                        final_piece = self.squares[possible_row][possible_column].piece
                        final = Square(possible_row, possible_column, final_piece)
                        move = Move(initial, final)
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
                    if self.squares[possible_row][possible_column].empty_or_rival(piece.colour):
                        initial = Square(row, column)
                        final_piece = self.squares[possible_row][possible_column].piece
                        final = Square(possible_row, possible_column, final_piece)
                        move = Move(initial, final)
                        piece.add_move(move)
        
        # Does not check if piece is blocking the move yet                                 
        def next_elephant_moves(row, column):
            possible_moves = []
            #Check top
            if Square.row_in_range(row+1) and Square.column_in_range(column+1):
                if self.squares[row+1][column+1].is_empty():
                    possible_moves.append((row+2, column+2))
            #Check bottom
            if Square.row_in_range(row-2) and Square.column_in_range(column-2):
                if self.squares[row-1][column-1].is_empty():
                    possible_moves.append((row-2, column-2))
            #Check Left
            if Square.row_in_range(row+2) and Square.column_in_range(column-2):
                if self.squares[row+1][column-1].is_empty():
                    possible_moves.append((row+2, column-2))
            #Check Right
            if Square.row_in_range(row-2) and Square.column_in_range(column+2):
                if self.squares[row-1][column+1].is_empty():
                    possible_moves.append((row-2, column+2))
            
            for possible_move in possible_moves:
                possible_row, possible_column = possible_move
                if Square.row_in_range(possible_row) and Square.column_in_range(possible_column):
                    if self.squares[possible_row][possible_column].empty_or_rival(piece.colour):
                        initial = Square(row, column)
                        final_piece = self.squares[possible_row][possible_column].piece
                        final = Square(possible_row, possible_column, final_piece)
                        move = Move(initial, final)
                        piece.add_move(move)
                        
        def next_pawn_moves(row, column):
            def move_red_home():
                possible_move = (row + 1, column)
                possible_row, possible_column = possible_move
                if Square.row_in_range(possible_row) and Square.column_in_range(possible_column):
                    if self.squares[possible_row][possible_column].empty_or_rival(piece.colour):
                        initial = Square(row, column)
                        final_piece = self.squares[possible_row][possible_column].piece
                        final = Square(possible_row, possible_column, final_piece)
                        move = Move(initial, final)
                        piece.add_move(move)
                        
            def move_red_rival():
                possible_moves = [
                (row+1, column),
                (row-1, column),
                (row, column+1),
                (row, column-1),
            ]
                for possible_move in possible_moves:
                    possible_row, possible_column = possible_move
                    if possible_row in range(5,10) and Square.column_in_range(possible_column):
                        if self.squares[possible_row][possible_column].empty_or_rival(piece.colour):
                            initial = Square(row, column)
                            final_piece = self.squares[possible_row][possible_column].piece
                            final = Square(possible_row, possible_column, final_piece)
                            move = Move(initial, final)
                            piece.add_move(move)
                            
            def move_black_home():
                possible_move = (row - 1, column)
                possible_row, possible_column = possible_move
                if Square.row_in_range(possible_row) and Square.column_in_range(possible_column):
                    if self.squares[possible_row][possible_column].empty_or_rival(piece.colour):
                        initial = Square(row, column)
                        final_piece = self.squares[possible_row][possible_column].piece
                        final = Square(possible_row, possible_column, final_piece)
                        move = Move(initial, final)
                        piece.add_move(move)
            def move_black_rival():
                possible_moves = [
                (row+1, column),
                (row-1, column),
                (row, column+1),
                (row, column-1),
            ]
                for possible_move in possible_moves:
                    possible_row, possible_column = possible_move
                    if possible_row in range(0,5) and Square.column_in_range(possible_column):
                        if self.squares[possible_row][possible_column].empty_or_rival(piece.colour):
                            initial = Square(row, column)
                            final_piece = self.squares[possible_row][possible_column].piece
                            final = Square(possible_row, possible_column, final_piece)
                            move = Move(initial, final)
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
                                piece.add_move(move)
                                return
                            counter += 1 
                        return
                    initial = Square(row, column)
                    final_piece = self.squares[possible_row][possible_column].piece
                    final = Square(possible_row, possible_column, final_piece)
                    move = Move(initial, final)
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
                                piece.add_move(move)
                                return
                            counter += 1 
                        return
                    initial = Square(row, column)
                    final_piece = self.squares[possible_row][possible_column].piece
                    final = Square(possible_row, possible_column, final_piece)
                    move = Move(initial, final)
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
                                piece.add_move(move)
                                return
                            counter += 1 
                        return
                    initial = Square(row, column)
                    final_piece = self.squares[possible_row][possible_column].piece
                    final = Square(possible_row, possible_column, final_piece)
                    move = Move(initial, final)
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
                                piece.add_move(move)
                                return
                            counter += 1 
                        return
                    initial = Square(row, column)
                    final_piece = self.squares[possible_row][possible_column].piece
                    final = Square(possible_row, possible_column, final_piece)
                    move = Move(initial, final)
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
        
    def in_check(self, piece, move):
        pass