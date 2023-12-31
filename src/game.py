import pygame
from const import *
from board import Board
from drag import DragHandler

class Game:
    def __init__(self):
        self.board = Board()
        self.dragger = DragHandler()
        self.next_player = 'red'
        # boolean to keep if game is finished
        self.is_won = False
        # variable to keep colour of losing opponent
        self.lost = None
    
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
        
    def show_moves(self, surface):
        if self.dragger.is_dragging:
            piece = self.dragger.piece
            for move in piece.moves:
                colour = '#C86464'
                rect = (move.final.column * SQUARE_SIZE + 80 - ((SQUARE_SIZE // 1.2) // 2), move.final.row * SQUARE_SIZE + 80 - ((SQUARE_SIZE // 1.2) // 2), SQUARE_SIZE // 1.1, SQUARE_SIZE // 1.1)
                pygame.draw.ellipse(surface, colour, rect)
                
    def next_turn(self):
        if self.next_player == 'red':
            self.next_player = 'black'
        else: 
            self.next_player = 'red'
            
            
    def show_last_move(self, surface):
        if self.board.last_move:
            initial = self.board.last_move.initial
            final = self.board.last_move.final
            for pos in [initial, final]:
                colour = (167, 211, 151)
                rect = (pos.column * SQUARE_SIZE + 80 - ((SQUARE_SIZE // 1.2) // 2), pos.row * SQUARE_SIZE + 80 - ((SQUARE_SIZE // 1.2) // 2), SQUARE_SIZE // 1.1, SQUARE_SIZE // 1.1)
                pygame.draw.rect(surface, colour, rect)
                
    def show_winning_modal(self, surface, loser):
        # Create background for modal
        rect_colour = (56,56,56)
        rect_width = SQUARE_SIZE * 8
        rect_height = SQUARE_SIZE * 3
        modal_rect = pygame.Rect((SCREEN_WIDTH - rect_width) // 2, (SCREEN_HEIGHT - rect_height) // 2, rect_width, rect_height)
        pygame.draw.rect(surface, rect_colour, modal_rect)
        
        # Create text for modal loser
        modal_font = pygame.font.Font("assets/fonts/Inter-Regular.ttf", 50)
        if loser == "red":
            winner = "black"
        else:
            winner = "red"
        loser_text = modal_font.render(str(winner).capitalize() + " checkmated " + str(loser).capitalize() + "!", True, (255,255,255))
        text_x = modal_rect.x + (modal_rect.width - loser_text.get_width()) // 2
        text_y = modal_rect.y + 30
        surface.blit(loser_text, (text_x, text_y))
        
        # Create text for modal
        modal_font = pygame.font.Font("assets/fonts/Inter-Regular.ttf", 30)
        button_text = modal_font.render("Exit to main menu or review game?", True, (255,255,255))
        text_x = modal_rect.x + (modal_rect.width - button_text.get_width()) // 2
        text_y = modal_rect.y + SQUARE_SIZE + 30
        surface.blit(button_text, (text_x, text_y))
        
        # Create leave to main menu button
        rect_colour = (233, 97, 97)
        rect_width = SQUARE_SIZE * 1.5
        rect_height = SQUARE_SIZE // 2
        self.leave_rect = pygame.Rect((SCREEN_WIDTH - rect_width) // 2 - 80, (modal_rect.y + modal_rect.height - 70), rect_width, rect_height)
        leave_rect = self.leave_rect
        pygame.draw.rect(surface, rect_colour, leave_rect)
        
        # Create text for leave button
        modal_font = pygame.font.Font("assets/fonts/Inter-Regular.ttf", 20)
        button_text = modal_font.render("Exit", True, (0,0,0))
        text_x = leave_rect.x + (leave_rect.width - button_text.get_width()) // 2
        text_y = leave_rect.y + 7
        surface.blit(button_text, (text_x, text_y))
        
        # Create stay button
        rect_colour = (233, 97, 97)
        rect_width = SQUARE_SIZE * 1.5
        rect_height = SQUARE_SIZE // 2
        self.stay_rect = pygame.Rect((SCREEN_WIDTH - rect_width) // 2 + 80, (modal_rect.y + modal_rect.height - 70), rect_width, rect_height)
        stay_rect = self.stay_rect
        pygame.draw.rect(surface, rect_colour, stay_rect)
        
        # Create text for stay button
        modal_font = pygame.font.Font("assets/fonts/Inter-Regular.ttf", 20)
        button_text = modal_font.render("Stay", True, (0,0,0))
        text_x = stay_rect.x + (stay_rect.width - button_text.get_width()) // 2
        text_y = stay_rect.y + 7
        surface.blit(button_text, (text_x, text_y))
        
    # Function to check if button was clicked and return game mode if so
    def was_button_clicked(self, mouse_pos):
        if self.leave_rect.collidepoint(mouse_pos):
            return "leave"
        elif self.stay_rect.collidepoint(mouse_pos):
            return "stay"
        else:
            return None
        
    def reset(self):
        self.__init__()