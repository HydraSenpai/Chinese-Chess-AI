import sys, pygame
from pygame import font
from const import *

class Settings:
    def __init__(self):
        pass

    def show_title(self, surface):
        # Methods
        title_font = pygame.font.Font("assets/fonts/Inter-Regular.ttf", 120)
        title_text = title_font.render("Settings", True, (255,255,255))
        surface.blit(title_text, ((SCREEN_WIDTH - title_text.get_width()) // 2, 160))
        
    def show_exit_button(self, surface):
        # Create exit button
        circle_colour = (233, 97, 97)
        circle_size = SQUARE_SIZE // 4
        self.stay_circle = pygame.Rect((SCREEN_WIDTH - circle_size * 2), 20, circle_size, circle_size)
        stay_circle = self.stay_circle
        pygame.draw.circle(surface, circle_colour, stay_circle.center, circle_size)
        
        # Create text for stay button
        modal_font = pygame.font.Font("assets/fonts/Inter-Regular.ttf", 30)
        button_text = modal_font.render("X", True, (0,0,0))
        text_x = stay_circle.x + (stay_circle.width - button_text.get_width()) // 2
        text_y = stay_circle.y // 2
        surface.blit(button_text, (text_x, text_y))
        
    # Function to check if button was clicked and return game mode if so
    def was_button_clicked(self, mouse_pos):
        if hasattr(self, 'stay_circle') and self.stay_circle != None and self.stay_circle.collidepoint(mouse_pos):
            return "exit"
        else:
            return None