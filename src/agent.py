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
        self.debug = False  
        
                                                   
    def calculate_all_possible_moves(self, board, colour, level):
        pieces = []
        possible_moves = []
        check = False
        pathDictionary = {}
        pathDictionary.clear()
        temp_board = 'rkeakaekr/000000000/0c00000c0/p0p0p0p0p/000000000/000000000/P0P0P0P0P/0C00000C0/000000000/RKEAKAEKR'
        
        # RECEIVE BOARD IN FORMAT rkeakaekr/000000000/0c00000c0/p0p0p0p0p/000000000/000000000/P0P0P0P0P/0C00000C0/000000000/RKEAKAEKR
        # Where uppercase is other player
        # Will turn this into array
        split_board = temp_board.split('/')
        
        # Here we can insert moves into algorithm to find optimal move
        if level != "beginner":
            st = time.time()
            minimax_board = copy.deepcopy(board)
            value, best_move = self.minimax(split_board, 3, -math.inf, math.inf, True, pathDictionary)
            # value, best_move = self.minimax(minimax_board, 3, True)
            print("END VALUE = " + str(value))
            et = time.time()
            runtime = et - st
            print("EXECUTION TIME: " + str(runtime))
            return best_move
        
        else:
            # We need to first calculate if king is in check to filter moves
            if board.is_check(colour):
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
                                    if board.is_check(p.colour) and not board.flying_general(p, x):
                                        if board.out_of_check(p, x):
                                            pieces.append(p)
                                            possible_moves.append(x)
                                    elif not board.in_check(p, x) and not board.flying_general(p, x):
                                        pieces.append(p)
                                        possible_moves.append(x)
                                elif check:
                                    if not board.in_check(p, x) and not board.flying_general(p, x):
                                        if board.out_of_check(p,x):
                                            pieces.append(p)
                                            possible_moves.append(x)
                                elif not board.in_check(p, x) and not board.flying_general(p, x):
                                    pieces.append(p)
                                    possible_moves.append(x)
            if len(possible_moves) == 0:
                return None
            if level == "beginner":
                choice = random.randint(0, len(possible_moves) - 1)
                board.move(pieces[choice], possible_moves[choice])
                return board       
    
    def evaluation(self, squares, maximum):
        if self.debug:
            st = time.time()
        value = 0
        print("EVALUATION VALUE = " + str(value))
        if self.debug:
            et = time.time()
            runtime = et - st
            print("EVALUATION EXECUTION TIME: " + f"{runtime:.15f}")
        return value
                          
    # Returns all moves from a given board and colour and returns them as boards
    def next_states(self, squares, colour):
        
        if self.debug:
            st = time.time()
        possible_states = []
        count = 0
                                
        for row in range(PIECE_ROWS):
                for column in range(PIECE_COLUMNS):
                    # Find every team piece and calculate all moves
                    if squares[row][column].has_team_piece(colour):
                        count+=1
                        p = squares[row][column].piece     
                        p.clear_moves()
                        self.calculate_moves(squares, p, row, column, bool=True)
                        # Add possible moves to array
                        for x in p.moves:
                            temp_squares = self.move(squares, p, x)
                            possible_states.append(temp_squares)
                            print("NEXT STATE")
                            print("PIECE = " + str(p.name) + " " + "INITIAL = " + str(x.initial.row) + " " + str(x.initial.column) + " " + "FINAL = " + str(x.final.row) + " " + str(x.final.column))
                        p.clear_moves()
        if self.debug:
            et = time.time()
            runtime = et - st
            print("NEXT STATES EXECUTION TIME: " + f"{runtime:.15f}")
        if len(possible_states) == 0:
            return []
        else:
            return possible_states
 
    def is_terminal_state(self, squares, colour):     
        if self.debug:
            st = time.time()                   
        for row in range(PIECE_ROWS):
                for column in range(PIECE_COLUMNS):
                    # Find every team piece and calculate all moves
                    if squares[row][column].has_team_piece(colour):
                        p = squares[row][column].piece     
                        p.clear_moves()
                        self.calculate_moves(squares, p, row, column, bool=True)
                        # Add possible moves to array
                        if len(p.moves) >= 1:
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
                      
    def minimax(self, squares, depth, alpha, beta, maximum, pathDictionary):
        best_move = None
        
        colour = "red"
        if not maximum:
            colour = "black"
            
        if depth <= 0 or self.is_terminal_state(squares, colour):
            return self.evaluation(squares, maximum), best_move
        
        if maximum:
            print("MINIMAX MAX")
            if str(squares) in pathDictionary:
                return pathDictionary[str(squares)], best_move
            value = -math.inf
            states = self.next_states(squares, "black")
            for s in states:
                eval, _ = self.minimax(s, depth - 1, alpha, beta, False, pathDictionary)
                if eval > value:
                    value = eval
                    best_move = s
                alpha = max(alpha, value)
                if value >= beta:
                    pathDictionary[str(squares)] = value
                    break
            pathDictionary[str(squares)] = value
            return value, best_move
        
        else:
            print("MINIMAX MIN")
            if str(squares) in pathDictionary:
                return pathDictionary[str(squares)], best_move
            value = math.inf
            states = self.next_states(squares, "red")
            for s in states:
                eval, _ = self.minimax(s, depth - 1, alpha, beta, True, pathDictionary)
                if eval < value:
                    value = eval
                    best_move = s
                beta = min(beta, value)
                if value <= alpha:
                    pathDictionary[str(squares)] = value
                    break
            pathDictionary[str(squares)] = value
            return value, best_move

    def calculate_moves(self, squares, piece, row, column, bool=True):
        
        
        def next_knight_moves(row, column):
            possible_moves = []
            #Check top
            if Square.row_in_range(row-1) and Square.column_in_range(column):
                if squares[row-1][column].is_empty():
                    possible_moves.append((row-2, column-1))
                    possible_moves.append((row-2, column+1))
            #Check bottom
            if Square.row_in_range(row+1) and Square.column_in_range(column):
                if squares[row+1][column].is_empty():
                    possible_moves.append((row+2, column-1))
                    possible_moves.append((row+2, column+1))
            #Check Left
            if Square.row_in_range(row) and Square.column_in_range(column-1):
                if squares[row][column-1].is_empty():
                    possible_moves.append((row-1, column-2))
                    possible_moves.append((row+1, column-2))
            #Check Right
            if Square.row_in_range(row) and Square.column_in_range(column+1):
                if squares[row][column+1].is_empty():
                    possible_moves.append((row-1, column+2))
                    possible_moves.append((row+1, column+2))
                
            for possible_move in possible_moves:
                possible_row, possible_column = possible_move
                if Square.row_in_range(possible_row) and Square.column_in_range(possible_column):
                    if squares[possible_row][possible_column].is_valid_move(piece.colour):
                        initial = Square(row, column)
                        final_piece = squares[possible_row][possible_column].piece
                        final = Square(possible_row, possible_column, final_piece)
                        move = Move(initial, final)
                        if bool:
                            if not self.in_check(squares, piece, move) and not self.flying_general(squares, piece, move):
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
                    if not squares[possible_row][possible_column].empty_or_rival(piece.colour):
                        return
                    if squares[possible_row][possible_column].has_rival_piece(piece.colour):
                        initial = Square(row, column)
                        final_piece = squares[possible_row][possible_column].piece
                        final = Square(possible_row, possible_column, final_piece)
                        move = Move(initial, final)
                        if bool:
                            if not self.in_check(squares, piece, move) and not self.flying_general(squares, piece, move):
                                piece.add_move(move)
                        else:
                            piece.add_move(move)
                        return
                    initial = Square(row, column)
                    final_piece = squares[possible_row][possible_column].piece
                    final = Square(possible_row, possible_column, final_piece)
                    move = Move(initial, final)
                    if bool:
                        if not self.in_check(squares, piece, move) and not self.flying_general(squares, piece, move):
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
                    if not squares[possible_row][possible_column].empty_or_rival(piece.colour):
                        return
                    if squares[possible_row][possible_column].has_rival_piece(piece.colour):
                        initial = Square(row, column)
                        final_piece = squares[possible_row][possible_column].piece
                        final = Square(possible_row, possible_column, final_piece)
                        move = Move(initial, final)
                        if bool:
                            if not self.in_check(squares, piece, move) and not self.flying_general(squares, piece, move):
                                piece.add_move(move)
                        else:
                            piece.add_move(move)
                        return
                    initial = Square(row, column)
                    final_piece = squares[possible_row][possible_column].piece
                    final = Square(possible_row, possible_column, final_piece)
                    move = Move(initial, final)
                    if bool:
                        if not self.in_check(squares, piece, move) and not self.flying_general(squares, piece, move):
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
                    if not squares[possible_row][possible_column].empty_or_rival(piece.colour):
                        return
                    if squares[possible_row][possible_column].has_rival_piece(piece.colour):
                        initial = Square(row, column)
                        final_piece = squares[possible_row][possible_column].piece
                        final = Square(possible_row, possible_column, final_piece)
                        move = Move(initial, final)
                        if bool:
                            if not self.in_check(squares, piece, move) and not self.flying_general(squares, piece, move):
                                piece.add_move(move)
                        else:
                            piece.add_move(move)
                        return
                    initial = Square(row, column)
                    final_piece = squares[possible_row][possible_column].piece
                    final = Square(possible_row, possible_column, final_piece)
                    move = Move(initial, final)
                    if bool:
                        if not self.in_check(squares, piece, move) and not self.flying_general(squares, piece, move):
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
                    if not squares[possible_row][possible_column].empty_or_rival(piece.colour):
                        return
                    if squares[possible_row][possible_column].has_rival_piece(piece.colour):
                        initial = Square(row, column)
                        final_piece = squares[possible_row][possible_column].piece
                        final = Square(possible_row, possible_column, final_piece)
                        move = Move(initial, final)
                        if bool:
                            if not self.in_check(squares, piece, move) and not self.flying_general(squares, piece, move):
                                piece.add_move(move)
                        else:
                            piece.add_move(move)
                        return
                    initial = Square(row, column)
                    final_piece = squares[possible_row][possible_column].piece
                    final = Square(possible_row, possible_column, final_piece)
                    move = Move(initial, final)
                    if bool:
                        if not self.in_check(squares, piece, move) and not self.flying_general(squares, piece, move):
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
                    if squares[possible_row][possible_column].is_valid_move(piece.colour):
                        initial = Square(row, column)
                        final = Square(possible_row, possible_column)
                        move = Move(initial, final)
                        if bool:
                            if self.is_check(squares, piece.colour) and not self.flying_general(squares, piece, move):
                                if self.out_of_check(squares, piece, move):
                                    piece.add_move(move)
                            elif not self.in_check(squares, piece, move) and not self.flying_general(squares, piece, move):
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
                    if squares[possible_row][possible_column].is_valid_move(piece.colour):
                        initial = Square(row, column)
                        final_piece = squares[possible_row][possible_column].piece
                        final = Square(possible_row, possible_column, final_piece)
                        move = Move(initial, final)
                        if bool:
                            if not self.in_check(squares, piece, move) and not self.flying_general(squares, piece, move):
                                piece.add_move(move)
                        else:
                            piece.add_move(move)
                                         
        def next_elephant_moves(row, column):
            possible_moves = []
            #Check top
            if Square.row_in_range(row+2) and Square.column_in_range(column+2):
                if squares[row+1][column+1].is_empty():
                    if piece.colour == "red" and row+2 <= 4 or piece.colour == "black":
                        possible_moves.append((row+2, column+2))
            #Check bottom
            if Square.row_in_range(row-2) and Square.column_in_range(column-2):
                if squares[row-1][column-1].is_empty():
                    if piece.colour == "black" and row-2 >= 5 or piece.colour == "red":
                        possible_moves.append((row-2, column-2))
            #Check Left
            if Square.row_in_range(row+2) and Square.column_in_range(column-2):
                if squares[row+1][column-1].is_empty():
                    if piece.colour == "red" and row+2 <= 4 or piece.colour == "black":
                        possible_moves.append((row+2, column-2))
            #Check Right
            if Square.row_in_range(row-2) and Square.column_in_range(column+2):
                if squares[row-1][column+1].is_empty():
                    if piece.colour == "black" and row-2 >= 5 or piece.colour == "red":
                        possible_moves.append((row-2, column+2))
            
            for possible_move in possible_moves:
                possible_row, possible_column = possible_move
                if Square.row_in_range(possible_row) and Square.column_in_range(possible_column):
                    if squares[possible_row][possible_column].is_valid_move(piece.colour):
                        initial = Square(row, column)
                        final_piece = squares[possible_row][possible_column].piece
                        final = Square(possible_row, possible_column, final_piece)
                        move = Move(initial, final)
                        if bool:
                            if not self.in_check(squares, piece, move) and not self.flying_general(squares, piece, move):
                                piece.add_move(move)
                        else:
                            piece.add_move(move)
                        
        def next_pawn_moves(row, column):
            def move_red_home():
                possible_move = (row + 1, column)
                possible_row, possible_column = possible_move
                if Square.row_in_range(possible_row) and Square.column_in_range(possible_column):
                    if squares[possible_row][possible_column].is_valid_move(piece.colour):
                        initial = Square(row, column)
                        final_piece = squares[possible_row][possible_column].piece
                        final = Square(possible_row, possible_column, final_piece)
                        move = Move(initial, final)
                        if bool:
                            if not self.in_check(squares, piece, move) and not self.flying_general(squares, piece, move):
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
                        if squares[possible_row][possible_column].is_valid_move(piece.colour):
                            initial = Square(row, column)
                            final_piece = squares[possible_row][possible_column].piece
                            final = Square(possible_row, possible_column, final_piece)
                            move = Move(initial, final)
                            if bool:
                                if not self.in_check(squares, piece, move) and not self.flying_general(squares, piece, move):
                                    piece.add_move(move)
                            else:
                                piece.add_move(move)
                            
            def move_black_home():
                possible_move = (row - 1, column)
                possible_row, possible_column = possible_move
                if Square.row_in_range(possible_row) and Square.column_in_range(possible_column):
                    if squares[possible_row][possible_column].is_valid_move(piece.colour):
                        initial = Square(row, column)
                        final_piece = squares[possible_row][possible_column].piece
                        final = Square(possible_row, possible_column, final_piece)
                        move = Move(initial, final)
                        if bool:
                            if not self.in_check(squares, piece, move) and not self.flying_general(squares, piece, move):
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
                        if squares[possible_row][possible_column].is_valid_move(piece.colour):
                            initial = Square(row, column)
                            final_piece = squares[possible_row][possible_column].piece
                            final = Square(possible_row, possible_column, final_piece)
                            move = Move(initial, final)
                            if bool:
                                if not self.in_check(squares, piece, move) and not self.flying_general(squares, piece, move):
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
                    if not squares[possible_row][possible_column].is_empty():
                        # Check whether a rival piece is in a square after the first blocking piece
                        counter += 1
                        # Loop after blocking piece to find next piece
                        while(Square.row_in_range(row + counter)):
                            next_move = (row + counter, column)
                            possible_row, possible_column = next_move
                            # If piece is team piece then no jump occurs and return
                            if squares[possible_row][possible_column].has_team_piece(piece.colour):
                                return
                            # If piece is rival then add move to possible moves
                            if squares[possible_row][possible_column].has_rival_piece(piece.colour):
                                initial = Square(row, column)
                                final_piece = squares[possible_row][possible_column].piece
                                final = Square(possible_row, possible_column, final_piece)
                                move = Move(initial, final)
                                if bool:
                                    if not self.in_check(squares, piece, move) and not self.flying_general(squares, piece, move):
                                        piece.add_move(move)
                                else:
                                    piece.add_move(move)
                                return
                            counter += 1 
                        return
                    initial = Square(row, column)
                    final_piece = squares[possible_row][possible_column].piece
                    final = Square(possible_row, possible_column, final_piece)
                    move = Move(initial, final)
                    if bool:
                        if not self.in_check(squares, piece, move) and not self.flying_general(squares, piece, move):
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
                    if not squares[possible_row][possible_column].is_empty():
                        # Check whether a rival piece is in a square after the first blocking piece
                        counter += 1
                        # Loop after blocking piece to find next piece
                        while(Square.row_in_range(row - counter)):
                            next_move = (row - counter, column)
                            possible_row, possible_column = next_move
                            # If piece is team piece then no jump occurs and return
                            if squares[possible_row][possible_column].has_team_piece(piece.colour):
                                return
                            # If piece is rival then add move to possible moves
                            if squares[possible_row][possible_column].has_rival_piece(piece.colour):
                                initial = Square(row, column)
                                final_piece = squares[possible_row][possible_column].piece
                                final = Square(possible_row, possible_column, final_piece)
                                move = Move(initial, final)
                                if bool:
                                    if not self.in_check(squares, piece, move) and not self.flying_general(squares, piece, move):
                                        piece.add_move(move)
                                else:
                                    piece.add_move(move)
                                return
                            counter += 1 
                        return
                    initial = Square(row, column)
                    final_piece = squares[possible_row][possible_column].piece
                    final = Square(possible_row, possible_column, final_piece)
                    move = Move(initial, final)
                    if bool:
                        if not self.in_check(squares, piece, move) and not self.flying_general(squares, piece, move):
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
                    if not squares[possible_row][possible_column].is_empty():
                        # Check whether a rival piece is in a square after the first blocking piece
                        counter += 1
                        # Loop after blocking piece to find next piece
                        while(Square.column_in_range(column + counter)):
                            next_move = (row, column + counter)
                            possible_row, possible_column = next_move
                            # If piece is team piece then no jump occurs and return
                            if squares[possible_row][possible_column].has_team_piece(piece.colour):
                                return
                            # If piece is rival then add move to possible moves
                            if squares[possible_row][possible_column].has_rival_piece(piece.colour):
                                initial = Square(row, column)
                                final_piece = squares[possible_row][possible_column].piece
                                final = Square(possible_row, possible_column, final_piece)
                                move = Move(initial, final)
                                if bool:
                                    if not self.in_check(squares, piece, move) and not self.flying_general(squares, piece, move):
                                        piece.add_move(move)
                                else:
                                    piece.add_move(move)
                                return
                            counter += 1 
                        return
                    initial = Square(row, column)
                    final_piece = squares[possible_row][possible_column].piece
                    final = Square(possible_row, possible_column, final_piece)
                    move = Move(initial, final)
                    if bool:
                        if not self.in_check(squares, piece, move) and not self.flying_general(squares, piece, move):
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
                    if not squares[possible_row][possible_column].is_empty():
                        # Check whether a rival piece is in a square after the first blocking piece
                        counter += 1
                        # Loop after blocking piece to find next piece
                        while(Square.column_in_range(column - counter)):
                            next_move = (row, column - counter)
                            possible_row, possible_column = next_move
                            # If piece is team piece then no jump occurs and return
                            if squares[possible_row][possible_column].has_team_piece(piece.colour):
                                return
                            # If piece is rival then add move to possible moves
                            if squares[possible_row][possible_column].has_rival_piece(piece.colour):
                                initial = Square(row, column)
                                final_piece = squares[possible_row][possible_column].piece
                                final = Square(possible_row, possible_column, final_piece)
                                move = Move(initial, final)
                                if bool:
                                    if not self.in_check(squares, piece, move) and not self.flying_general(squares, piece, move):
                                        piece.add_move(move)
                                else:
                                    piece.add_move(move)
                                return
                            counter += 1 
                        return
                    initial = Square(row, column)
                    final_piece = squares[possible_row][possible_column].piece
                    final = Square(possible_row, possible_column, final_piece)
                    move = Move(initial, final)
                    if bool:
                        if not self.in_check(squares, piece, move) and not self.flying_general(squares, piece, move):
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
    def flying_general(self, squares, piece, move):
        if self.debug:
            st = time.time()
        # new_piece = self.copy_piece(piece)
        # squares = self.copy_squares()
        # self.move_squares(squares, new_piece, move)
        temp_squares = self.move(squares, piece, move)
        
        # Find top king piece
        for row in range(3):
            for column in range(PIECE_COLUMNS):
                if temp_squares[row][column].has_piece() and temp_squares[row][column].piece.name == "king":
                    # king = temp_squares[row][column].piece
                    king_col = column
                    king_row = row     
                       
        # Loop through row which king is on and check for rule by checking a piece is between it or no king at the end 
        for row in range(king_row+1, PIECE_ROWS):
            if temp_squares[row][king_col].has_piece() and temp_squares[row][king_col].piece.name == "king":
                if self.debug:
                    et = time.time()
                    runtime = et - st
                    print("FLYING GENERAL EXECUTION TIME: " + f"{runtime:.15f}")
                return True
            if temp_squares[row][king_col].has_piece() and temp_squares[row][king_col].piece.name != "king":
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
    def in_check(self, squares, piece, move):
        if self.debug:
            st = time.time()
        temp_squares = self.move(squares, piece, move)
        
        for row in range(PIECE_ROWS):
            for column in range(PIECE_COLUMNS):
                if temp_squares[row][column].has_rival_piece(piece.colour):
                    p = temp_squares[row][column].piece
                    self.calculate_moves(temp_squares, p, row, column, bool=False)
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
    def is_check(self, squares, next_player):
        if self.debug:
            st = time.time()
        temp_squares = squares.copy()
        # Search through board to find all enemy pieces
        for row in range(PIECE_ROWS):
            for column in range(PIECE_COLUMNS):
                # Calculate all possible moves of each piece
                if temp_squares[row][column].has_rival_piece(next_player):
                    p = temp_squares[row][column].piece
                    self.calculate_moves(temp_squares, p, row, column, bool=False)
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
    def out_of_check(self, squares, piece, move):
        if self.debug:
            st = time.time()
        temp_squares = self.move(squares, piece, move)
        
        for row in range(PIECE_ROWS):
            for column in range(PIECE_COLUMNS):
                if temp_squares[row][column].has_rival_piece(piece.colour):
                    p = temp_squares[row][column].piece
                    self.calculate_moves(temp_squares, p, row, column, bool=False)
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
    
    def is_checkmate(self, squares, colour):
        if self.debug:
            st = time.time()
        # Check if king is in check
        if not self.is_check(colour):
            return False
        else:
            # Check each move that puts the king into check and search if any move removes all checks on the king
            # Search through board to find all enemy pieces
            for row in range(PIECE_ROWS):
                for column in range(PIECE_COLUMNS):
                    # Calculate all possible moves of each enemy piece
                    if squares[row][column].has_rival_piece(colour):
                        p = squares[row][column].piece
                        self.calculate_moves(squares, p, row, column, bool=False)
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

    def move(self, squares, piece, move):
        initial = move.initial
        final = move.final
        
        # squares_copy = copy.deepcopy(squares)
        
        # Update squares
        squares[initial.row][initial.column].piece = None
        squares[final.row][final.column].piece = piece
        
        return squares                                     