import pygame

from const import *

class DragHandler:
    def __init__(self):
        self.mouseX = 0
        self.mouseY = 0
        self.initial_row = 0
        self.initial_column = 0
        self.piece = None
        self.is_dragging = False
        
        # Load Images to improve performance
        # Red images
        self.red_images = {
            'pawn' : pygame.image.load('assets/images/pieces/red_pawn.png'),
            'elephant' : pygame.image.load('assets/images/pieces/red_elephant.png'),
            'guard' : pygame.image.load('assets/images/pieces/red_guard.png'),
            'king' : pygame.image.load('assets/images/pieces/red_king.png'),
            'rook' : pygame.image.load('assets/images/pieces/red_rook.png'),
            'knight' : pygame.image.load('assets/images/pieces/red_knight.png'),
            'cannon' : pygame.image.load('assets/images/pieces/red_cannon.png'),
        }
        self.black_images = {
            'pawn' : pygame.image.load('assets/images/pieces/black_pawn.png'),
            'elephant' : pygame.image.load('assets/images/pieces/black_elephant.png'),
            'guard' : pygame.image.load('assets/images/pieces/black_guard.png'),
            'king' : pygame.image.load('assets/images/pieces/black_king.png'),
            'rook' : pygame.image.load('assets/images/pieces/black_rook.png'),
            'knight' : pygame.image.load('assets/images/pieces/black_knight.png'),
            'cannon' : pygame.image.load('assets/images/pieces/black_cannon.png'),
        }
    
    def update_mouse(self, pos):
        self.mouseX, self.mouseY = pos
        
    def save_initial_pos(self, pos):
        self.initial_row = pos[1] + 40 // SQUARE_SIZE
        self.initial_column = pos[0] + 40 // SQUARE_SIZE
        
    def drag_piece(self, piece):
        self.piece = piece
        self.is_dragging = True
        
    def undrag_piece(self):
        self.piece = None
        self.is_dragging = False
        
    def update_blit(self,surface):
        # Get piece name and use stored image instead of loading it every render
        if self.piece.colour == "red":
            image = self.red_images.get(self.piece.name)
        else:
            image = self.black_images.get(self.piece.name)
        
        # texture = self.piece.texture
        # img = pygame.image.load(texture).convert_alpha()
        
        # Scale image a bit bigger to show its the one moving to user
        img_scaled = pygame.transform.scale(image, (SQUARE_SIZE, SQUARE_SIZE))
        # Center image to mouse position
        img_center = (self.mouseX, self.mouseY)
        self.piece.texture_rect = img_scaled.get_rect(center=img_center)
        surface.blit(img_scaled, self.piece.texture_rect)