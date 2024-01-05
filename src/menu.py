import sys, pygame
from pygame import font
from const import *

class Menu:
    def __init__(self):
        pass
    
    # Methods
    def show_title(self, surface):
        title_font = pygame.font.Font("assets/fonts/Inter-Regular.ttf", 120)
        title_text = title_font.render("Xiangqi", True, (255,255,255))
        surface.blit(title_text, ((SCREEN_WIDTH - title_text.get_width() - 200) // 2, 160))
        
        img = pygame.image.load("assets/images/pieces/black_elephant.png")
        img_scaled = pygame.transform.scale(img, (SQUARE_SIZE * 1.2, SQUARE_SIZE * 1.2))
        surface.blit(img_scaled, ((SCREEN_WIDTH - ((title_text.get_width() + title_text.get_rect().x) + 50)), (title_text.get_rect().y + (title_text.get_height() * 1.3))))
    
    
        img2 = pygame.image.load("assets/images/pieces/red_elephant.png")
        img_scaled2 = pygame.transform.scale(img2, (SQUARE_SIZE * 1.2, SQUARE_SIZE * 1.2))
        surface.blit(img_scaled2, ((SCREEN_WIDTH - ((title_text.get_width() + title_text.get_rect().x) - 50)), (title_text.get_rect().y + (title_text.get_height() * 1.3))))
        
    # Function to create buttons (could be changed to be created once and stored in local)
    def show_buttons(self, surface):
        self.beginner_btn = self.create_button(surface, 400, "Beginner")
        self.intermediate_btn = self.create_button(surface, 520, "Intermediate")
        self.experienced_btn = self.create_button(surface, 640, "Experienced")
    
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

        
        # Draw items on screen
        pygame.draw.rect(surface, square_colour, square_rect)
        surface.blit(button_text, (text_x, text_y))
        return square_rect
        
    # Function to check if button was clicked and return game mode if so
    def was_button_clicked(self, mouse_pos):
        if self.beginner_btn.collidepoint(mouse_pos):
            return "beginner"
        elif self.intermediate_btn.collidepoint(mouse_pos):
            return "intermediate"
        elif self.experienced_btn.collidepoint(mouse_pos):
            return "experienced"
        else:
            return None
        