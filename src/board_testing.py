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
        
        # Check moving pawn works
        piece = Piece('pawn', 'red', 1)
        initial = Square(3, 0)
        final = Square(4, 0)
        move = Move(initial, final)
        board.move(piece, move)
        self.assertTrue(board.squares[4][0].piece.name == 'pawn')
        
    
    
    
    
if __name__ == '__main__':
    unittest.main()