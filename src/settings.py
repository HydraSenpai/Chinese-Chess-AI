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
        
    def show_sounds_option(self, surface, sound_option):
        # TITLE
        sound_font = pygame.font.Font("assets/fonts/Inter-Regular.ttf", 40)
        sound_text = sound_font.render("Sounds", True, (255,255,255))
        surface.blit(sound_text, (200, 400))
        
        #ON BUTTON
        # Create Solid Square for on button
        button_width, button_height = 150, 60
        if sound_option == True:
            square_colour = (233, 97, 97)
        else:
            square_colour = (80, 10, 10)
        self.square_rect = pygame.Rect(700, 390, button_width, button_height)
        
        # Create text for button
        button_font = pygame.font.Font("assets/fonts/Inter-Regular.ttf", 25)
        button_text = button_font.render("ON", True, (255, 255, 255))

        # Calculate the position to center the text within the square
        text_x = self.square_rect.x + (self.square_rect.width - button_text.get_width()) // 2
        text_y = self.square_rect.y + (self.square_rect.height - button_text.get_height()) // 2
        
        # Draw items on screen
        pygame.draw.rect(surface, square_colour, self.square_rect)
        surface.blit(button_text, (text_x, text_y))
        
        #OFF BUTTON
        # Create Solid Square for on button
        button_width, button_height = 150, 60
        if sound_option == False:
            square_colour = (233, 97, 97)
        else:
            square_colour = (80, 10, 10)
        self.off_square_rect = pygame.Rect(850, 390, button_width, button_height)
        
        # Create text for button
        button_font = pygame.font.Font("assets/fonts/Inter-Regular.ttf", 25)
        button_text = button_font.render("OFF", True, (255, 255, 255))

        # Calculate the position to center the text within the square
        text_x = self.off_square_rect.x + (self.off_square_rect.width - button_text.get_width()) // 2
        text_y = self.off_square_rect.y + (self.off_square_rect.height - button_text.get_height()) // 2

        # Draw items on screen
        pygame.draw.rect(surface, square_colour, self.off_square_rect)
        surface.blit(button_text, (text_x, text_y))
        
    def was_sound_clicked(self, mouse_pos):
        if hasattr(self, 'off_square_rect') and self.off_square_rect != None and self.off_square_rect.collidepoint(mouse_pos):
            return "off"
        elif hasattr(self, 'square_rect') and self.square_rect != None and self.square_rect.collidepoint(mouse_pos):
            return "on"
        else:
            return None
        
    def show_screen_options(self, surface, screen_option):
        # TITLE
        sound_font = pygame.font.Font("assets/fonts/Inter-Regular.ttf", 40)
        sound_text = sound_font.render("Screen", True, (255,255,255))
        surface.blit(sound_text, (200, 550))
        
        #medium BUTTON
        # Create Solid Square for large button
        button_width, button_height = 150, 60
        if screen_option == "medium":
            square_colour = (233, 97, 97)
        else:
            square_colour = (80, 10, 10)
        self.medium_screen_rect = pygame.Rect(850, 540, button_width, button_height)
        
        # Create text for button
        button_font = pygame.font.Font("assets/fonts/Inter-Regular.ttf", 25)
        button_text = button_font.render("Medium", True, (255, 255, 255))

        # Calculate the position to center the text within the square
        text_x = self.medium_screen_rect.x + (self.medium_screen_rect.width - button_text.get_width()) // 2
        text_y = self.medium_screen_rect.y + (self.medium_screen_rect.height - button_text.get_height()) // 2

        # Draw items on screen
        pygame.draw.rect(surface, square_colour, self.medium_screen_rect)
        surface.blit(button_text, (text_x, text_y))
        
        #large BUTTON
        # Create Solid Square for large button
        button_width, button_height = 150, 60
        if screen_option == "large":
            square_colour = (233, 97, 97)
        else:
            square_colour = (80, 10, 10)
        self.large_screen_rect = pygame.Rect(700, 540, button_width, button_height)
        
        # Create text for button
        button_font = pygame.font.Font("assets/fonts/Inter-Regular.ttf", 25)
        button_text = button_font.render("Large", True, (255, 255, 255))

        # Calculate the position to center the text within the square
        text_x = self.large_screen_rect.x + (self.large_screen_rect.width - button_text.get_width()) // 2
        text_y = self.large_screen_rect.y + (self.large_screen_rect.height - button_text.get_height()) // 2

        # Draw items on screen
        pygame.draw.rect(surface, square_colour, self.large_screen_rect)
        surface.blit(button_text, (text_x, text_y))
        
        #FULLSCREEN BUTTON
        # Create Solid Square for fullscreen button
        button_width, button_height = 150, 60
        if screen_option == "full":
            square_colour = (233, 97, 97)
        else:
            square_colour = (80, 10, 10)
        self.full_screen_rect = pygame.Rect(550, 540, button_width, button_height)
        
        # Create text for button
        button_font = pygame.font.Font("assets/fonts/Inter-Regular.ttf", 25)
        button_text = button_font.render("Fullscreen", True, (255, 255, 255))

        # Calculate the position to center the text within the square
        text_x = self.full_screen_rect.x + (self.full_screen_rect.width - button_text.get_width()) // 2
        text_y = self.full_screen_rect.y + (self.full_screen_rect.height - button_text.get_height()) // 2
        
        # Draw items on screen
        pygame.draw.rect(surface, square_colour, self.full_screen_rect)
        surface.blit(button_text, (text_x, text_y))
               
    def was_screen_clicked(self, mouse_pos):
        if hasattr(self, 'medium_screen_rect') and self.medium_screen_rect != None and self.medium_screen_rect.collidepoint(mouse_pos):
            return "medium"
        elif hasattr(self, 'large_screen_rect') and self.large_screen_rect != None and self.large_screen_rect.collidepoint(mouse_pos):
            return "large"
        elif hasattr(self, 'full_screen_rect') and self.full_screen_rect != None and self.full_screen_rect.collidepoint(mouse_pos):
            return "full"
        else:
            return None
                   
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