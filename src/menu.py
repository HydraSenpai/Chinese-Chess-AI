import pygame
from pygame import font
from const import *

class Menu:
    def __init__(self):
        pass
    
    # Methods
    def show_title(self, surface):
        title_font = pygame.font.Font("assets/fonts/Inter-Regular.ttf", 120)
        title_text = title_font.render("Xiangqi", True, (255,255,255))
        surface.blit(title_text, ((SCREEN_WIDTH - title_text.get_width()) // 2, 160))
    
    def show_buttons(self, surface):
        self.create_button(surface, 400, "Beginner")
        self.create_button(surface, 520, "Intermediate")
        self.create_button(surface, 640, "Experienced")
    
    def create_button(self, surface, height, text):
        # Create Solid Square for button
        button_width, button_height = (SCREEN_WIDTH // 5 * 3), 90
        square_colour = (233, 97, 97)
        square_rect = pygame.Rect((SCREEN_WIDTH - button_width) // 2, height, button_width, button_height)
        
        # Create text for button
        button_font = pygame.font.Font("assets/fonts/Inter-Regular.ttf", 40)
        button_text = button_font.render(text, True, (255, 255, 255))

        # Calculate the position to center the text within the square
        text_x = square_rect.x + (square_rect.width - button_text.get_width()) // 2
        text_y = square_rect.y + (square_rect.height - button_text.get_height()) // 2

        # Create circles for border radius(optional)
        
        # Draw items on screen
        pygame.draw.rect(surface, square_colour, square_rect)
        surface.blit(button_text, (text_x, text_y))