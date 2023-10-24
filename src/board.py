from square import Square
from piece import *
from const import *

class Board:
    def __init__(self):
        # Creates empty 8x8 board array
        self.squares = [[0,0,0,0,0,0,0,0,0] for row in range(PIECE_ROWS)]
        self.create()
        self.add_pieces('red')
        self.add_pieces('black')
    
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
            self.squares[6][0] = Square(6, 1, Pawn(colour))
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
            
  
        