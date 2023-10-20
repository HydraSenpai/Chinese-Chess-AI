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
        texture = self.piece.texture
        img = pygame.image.load(texture).convert_alpha()
        # Scale image a bit bigger to show its the one moving to user
        img_scaled = pygame.transform.scale(img, (SQUARE_SIZE, SQUARE_SIZE))
        # Center image to mouse position
        img_center = (self.mouseX, self.mouseY)
        self.piece.texture_rect = img_scaled.get_rect(center=img_center)
        surface.blit(img_scaled, self.piece.texture_rect)