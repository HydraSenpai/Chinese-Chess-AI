import pygame
from const import *
from board import Board

class Game:
    def __init__(self):
        self.board = Board()
    
    # Show methods
    
    def show_background(self, surface):
        for row in range(ROWS):
            if row != 4:
                for col in range(COLUMNS):
                    rect = (col * SQUARE_SIZE + 80, row * SQUARE_SIZE + 80, SQUARE_SIZE, SQUARE_SIZE)
                    pygame.draw.rect(surface, (167, 211, 151), rect)
                    for i in range(4):
                        line_rect = (col * SQUARE_SIZE + 80, row * SQUARE_SIZE + 80, SQUARE_SIZE, SQUARE_SIZE)
                        pygame.draw.rect(surface, (0,0,0), line_rect, 1)
            else:
                river_rect = (80, row * SQUARE_SIZE + 80, WIDTH, SQUARE_SIZE)
                pygame.draw.rect(surface, (167, 211, 151), river_rect)
                for i in range(4):
                    line_rect = (80, row * SQUARE_SIZE + 80, WIDTH, SQUARE_SIZE)
                    pygame.draw.rect(surface, (0,0,0), line_rect, 1)
        screen_rect = (80,80,WIDTH,HEIGHT)
        pygame.draw.rect(surface, (0,0,0), screen_rect, 2)
        

                
    def show_pieces(self, surface):
        for row in range(PIECE_ROWS):
            for col in range(PIECE_COLUMNS):
                # Check if piece is on square
                if self.board.squares[row][col].has_piece():
                    # Save piece data to variable in individual square
                    piece = self.board.squares[row][col].piece
                    img = pygame.image.load(piece.texture).convert_alpha()
                    # Scale image to board size
                    img_scaled = pygame.transform.scale(img, (SQUARE_SIZE, SQUARE_SIZE))
                    img_center = (col * SQUARE_SIZE) + 80, (row * SQUARE_SIZE) + 80
                    piece.texture_rect = img_scaled.get_rect(center=img_center)
                    surface.blit(img_scaled, piece.texture_rect)