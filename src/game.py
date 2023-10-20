import pygame
from const import *
from board import Board
from drag import DragHandler

class Game:
    def __init__(self):
        self.board = Board()
        self.dragger = DragHandler()
    
    # Show methods
    
    def show_background(self, surface):
        for row in range(ROWS):
            # Check if we're on river row so no borders are drawn
            if row != 4:
                # Creates a grid pattern
                for col in range(COLUMNS):
                    # Creates an individual square to represent a space on the grid
                    rect = (col * SQUARE_SIZE + 80, row * SQUARE_SIZE + 80, SQUARE_SIZE, SQUARE_SIZE)
                    pygame.draw.rect(surface, (167, 211, 151), rect)
                    # Square border
                    line_rect = (col * SQUARE_SIZE + 80, row * SQUARE_SIZE + 80, SQUARE_SIZE, SQUARE_SIZE)
                    pygame.draw.rect(surface, (0,0,0), line_rect, 1)
            else:
                # One big row for river
                river_rect = (80, row * SQUARE_SIZE + 80, WIDTH, SQUARE_SIZE)
                pygame.draw.rect(surface, (167, 211, 151), river_rect)
                # River Border
                line_rect = (80, row * SQUARE_SIZE + 80, WIDTH, SQUARE_SIZE)
                pygame.draw.rect(surface, (0,0,0), line_rect, 1)
                
        # Gives the whole board a border for good looks
        screen_rect = (80,80,WIDTH,HEIGHT)
        pygame.draw.rect(surface, (0,0,0), screen_rect, 2)
        
        # Draw King grid for red
        pygame.draw.line(surface, (0,0,0), (3*SQUARE_SIZE+80, 80), (4*SQUARE_SIZE+80, 1*SQUARE_SIZE+80), 3)
        pygame.draw.line(surface, (0,0,0), (3*SQUARE_SIZE+80, 2*SQUARE_SIZE+80), (4*SQUARE_SIZE+80, 1*SQUARE_SIZE+80), 3)
        pygame.draw.line(surface, (0,0,0), (4*SQUARE_SIZE+80, 1*SQUARE_SIZE+80), (5*SQUARE_SIZE+80, 80), 3)
        pygame.draw.line(surface, (0,0,0), (4*SQUARE_SIZE+80, 1*SQUARE_SIZE+80), (5*SQUARE_SIZE+80, 2*SQUARE_SIZE+80), 3)
        
        # Draw King grid for black
        pygame.draw.line(surface, (0,0,0), (3*SQUARE_SIZE+80, 9*SQUARE_SIZE+80), (4*SQUARE_SIZE+80, 8*SQUARE_SIZE+80), 3)
        pygame.draw.line(surface, (0,0,0), (3*SQUARE_SIZE+80, 7*SQUARE_SIZE+80), (4*SQUARE_SIZE+80, 8*SQUARE_SIZE+80), 3)
        pygame.draw.line(surface, (0,0,0), (5*SQUARE_SIZE+80, 9*SQUARE_SIZE+80), (4*SQUARE_SIZE+80, 8*SQUARE_SIZE+80), 3)
        pygame.draw.line(surface, (0,0,0), (4*SQUARE_SIZE+80, 8*SQUARE_SIZE+80), (5*SQUARE_SIZE+80, 7*SQUARE_SIZE+80), 3)

                
    def show_pieces(self, surface):
        for row in range(PIECE_ROWS):
            for col in range(PIECE_COLUMNS):
                # Check if piece is on square
                if self.board.squares[row][col].has_piece():
                    # Save piece data to variable in individual square
                    piece = self.board.squares[row][col].piece
                    
                    # Check if piece is being dragged and not to show it
                    if piece is not self.dragger.piece:
                        img = pygame.image.load(piece.texture).convert_alpha()
                        # Scale image to board size
                        img_scaled = pygame.transform.scale(img, (SQUARE_SIZE / 1.2, SQUARE_SIZE / 1.2))
                        img_center = (col * SQUARE_SIZE) + 80, (row * SQUARE_SIZE) + 80
                        piece.texture_rect = img_scaled.get_rect(center=img_center)
                        surface.blit(img_scaled, piece.texture_rect)
                    
    def show_log(self,surface):
        log_rect = (WIDTH + (SQUARE_SIZE * 2), 80, 350, HEIGHT)
        pygame.draw.rect(surface, (171,172,173), log_rect)