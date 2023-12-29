import pygame
from pygame import font
from const import *

class Menu:
    def __init__(self):
        self.title_font = pygame.font.Font("assets/fonts/Inter-Regular.ttf", 120)
        print(pygame.font.get_fonts())
    
    # Methods
    def show_title(self, surface):
        title_text = self.title_font.render("Xiangqi", True, (255,255,255))
        surface.blit(title_text, ((SCREEN_WIDTH - title_text.get_width()) // 2, 160))
        
    def create_button(self, surface):
        pass