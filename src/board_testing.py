import unittest
import math
import time
from board import Board
from move import Move
from square import Square
from piece import Piece

class TestAgent(unittest.TestCase):
    def test_board(self):
        board = Board()
        # Test starting positions of few pieces
        self.assertTrue(board.squares[0][0].piece.name == 'rook')
        self.assertTrue(board.squares[0][1].piece.name == 'knight')
        self.assertTrue(board.squares[3][0].piece.name == 'pawn')
        
        # Check moving function works
        piece = Piece('pawn', 'red', 1)
        initial = Square(3, 0)
        final = Square(4, 0)
        move = Move(initial, final)
        board.move(piece, move)
        self.assertTrue(board.squares[4][0].piece.name == 'pawn')
        # Test that board successfully updates most recent move
        self.assertTrue(board.last_move == move)
        
        # Check board to string works
        board = Board()
        self.assertTrue(board.convert_board_to_string() == 'rhegkgehr/000000000/0c00000c0/p0p0p0p0p/000000000/000000000/P0P0P0P0P/0C00000C0/000000000/RHEGKGEHR')
        
        # Check string to board works
        board = Board()
        board.add_custom_board("red")
        board.add_custom_board("black")
        board.convert_string_to_board('rhegkgehr/000000000/0c00000c0/p0p0p0p0p/000000000/000000000/P0P0P0P0P/0C00000C0/000000000/RHEGKGEHR')
        
        board2 = Board()
        
        self.assertTrue(board.squares == board2.squares)
        
    def test_piece(self):
        piece = Piece('pawn', 'red', 1)
        self.assertTrue(piece.moves == [])
        
        # Add move should add one to the moves list
        initial = Square(0, 0)
        final = Square(1, 0)
        move = Move(initial, final)
        piece.add_move(move)
        self.assertTrue(len(piece.moves) == 1)
        
        # Clearing moves should empty moves list
        piece.clear_moves()
        self.assertTrue(len(piece.moves) == 0)
        
    def test_square(self):
        square = Square(0, 0)
        
        # Check methods when piece doesn't exist
        self.assertTrue(square.has_piece() == False)
        self.assertTrue(square.is_empty() == True)
        self.assertTrue(square.has_rival_piece("red") == False)
        self.assertTrue(square.has_team_piece("red") == False)
        self.assertTrue(square.empty_or_rival("red") == True)
        self.assertTrue(square.is_valid_move("red") == True)
        
        # Check methods when piece exists and is team piece
        piece = Piece('pawn', 'red', 1)
        square = Square(0, 0, piece)
        self.assertTrue(square.has_piece() == True)
        self.assertTrue(square.is_empty() == False)
        self.assertTrue(square.has_rival_piece("red") == False)
        self.assertTrue(square.has_team_piece("red") == True)
        self.assertTrue(square.empty_or_rival("red") == False)
        self.assertTrue(square.is_valid_move("red") == False)
        
        # Check methods when piece exists and is team piece
        piece = Piece('pawn', 'red', 1)
        square = Square(0, 0, piece)
        self.assertTrue(square.has_piece() == True)
        self.assertTrue(square.is_empty() == False)
        self.assertTrue(square.has_rival_piece("black") == True)
        self.assertTrue(square.has_team_piece("black") == False)
        self.assertTrue(square.empty_or_rival("black") == True)
        self.assertTrue(square.is_valid_move("black") == True)
        



    
    
if __name__ == '__main__':
    unittest.main()