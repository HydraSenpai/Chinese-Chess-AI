import pygame
from const import *
from board import Board
from drag import DragHandler
import math
import copy

class Game:
    def __init__(self):
        self.board = Board()
        self.dragger = DragHandler()
        self.next_player = 'red'
        # boolean to keep if game is finished
        self.is_won = False
        # variable to keep colour of losing opponent
        self.lost = None
        # variable to keep track of showing modal for when the user wants to look at board after game
        self.stay = False
        # variable to keep track of if ai is still being calculated
        self.calculating_ai = False
        
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
                        if piece.colour == "red":
                            img = self.red_images.get(piece.name)
                        else:
                            img = self.black_images.get(piece.name)
                        
                        # img = pygame.image.load(piece.texture).convert_alpha()
                        # Scale image to board size
                        img_scaled = pygame.transform.scale(img, (SQUARE_SIZE / 1.2, SQUARE_SIZE / 1.2))
                        img_center = (col * SQUARE_SIZE) + 80, (row * SQUARE_SIZE) + 80
                        piece.texture_rect = img_scaled.get_rect(center=img_center)
                        surface.blit(img_scaled, piece.texture_rect)
                    
    def show_log(self, surface, move_list):
        
        def show_move_list(moves_list):
            
            move_rect = pygame.Rect(log_rect.x, log_rect.y, log_rect.width, 50)
            
            # If move list is odd then we need to print out the first move by itself
            if not len(moves_list) % 2 == 0:
                initial_row = moves_list[0].initial.row
                initial_column = moves_list[0].initial.column
                final_row = moves_list[0].final.row
                final_column = moves_list[0].final.column
                
                # Create text for the index of history list
                index_font = pygame.font.Font("assets/fonts/Inter-Regular.ttf", 20)
                index_text = index_font.render(str(math.ceil(len(moves_list)//2) + 1), True, (0,0,0))
                text_x = move_rect.x + ((move_rect.width // 3) // 2)
                text_y = move_rect.y
                surface.blit(index_text, (text_x, text_y))
                
                # Create text for the first move in index
                index_text = index_font.render(str(initial_row)+str(initial_column)+str(final_row)+str(final_column), True, (0,0,0))
                text_x = move_rect.x + ((move_rect.width // 3) + ((move_rect.width // 3) // 4))
                text_y = move_rect.y
                surface.blit(index_text, (text_x, text_y))
            
            # If the list is odd then we have already printed the first move so we need to start positioning 1 after
            if not len(moves_list) % 2 == 0:
                start_value = 1
            else:
                start_value = 0
                               
            for i in range(start_value, len(moves_list)-1, 2):
                initial_row = moves_list[i].initial.row
                initial_column = moves_list[i].initial.column
                final_row = moves_list[i].final.row
                final_column = moves_list[i].final.column
                
                initial_row2 = moves_list[i+1].initial.row
                initial_column2 = moves_list[i+1].initial.column
                final_row2 = moves_list[i+1].final.row
                final_column2 = moves_list[i+1].final.column
                
                # Create text for the index of history list
                index_font = pygame.font.Font("assets/fonts/Inter-Regular.ttf", 20)
                index_text = index_font.render(str((len(moves_list) - i + start_value) // 2), True, (0,0,0))
                text_x = move_rect.x + ((move_rect.width // 3) // 2)
                text_y = move_rect.y + (40 * math.ceil((i + start_value) // 2))
                surface.blit(index_text, (text_x, text_y))
                                
                # Create text for the first move in index
                index_text = index_font.render(str(initial_row2)+str(initial_column2)+str(final_row2)+str(final_column2), True, (0,0,0))
                text_x = move_rect.x + ((move_rect.width // 3) + ((move_rect.width // 3) // 4))
                text_y = move_rect.y + (40 * math.ceil((i + start_value) // 2))
                surface.blit(index_text, (text_x, text_y))

                # Create text for the second move in index
                index_text = index_font.render(str(initial_row)+str(initial_column)+str(final_row)+str(final_column), True, (0,0,0))
                text_x = move_rect.x + (((move_rect.width // 3) * 2) + ((move_rect.width // 3) // 4))
                text_y = move_rect.y + (40 * math.ceil((i + start_value) // 2))
                surface.blit(index_text, (text_x, text_y))
                
                if i >= 32:
                    return
        
        log_rect = pygame.Rect(WIDTH + (SQUARE_SIZE * 2), 80, 350, HEIGHT)
        pygame.draw.rect(surface, (171,172,173), log_rect)
        reversed_list = move_list[::-1]
        show_move_list(reversed_list)
        self.show_turn(surface)
        
    def show_turn(self, surface):
        if self.next_player == "red":
            text = "It is Red's turn!"
            # colour = (233, 97, 97)
        else:
            text = "It is Black's turn!"
            # colour = (0,0,0) 
            
        # Create text for the index of history list
        index_font = pygame.font.Font("assets/fonts/Inter-Regular.ttf", 30)
        index_text = index_font.render(text, True, (255,255,255))
        surface.blit(index_text, (WIDTH + (SQUARE_SIZE * 2), 40))
        
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
                colour = (231, 247, 0)
                rect = (pos.column * SQUARE_SIZE + 80 - ((SQUARE_SIZE // 1.2) // 2), pos.row * SQUARE_SIZE + 80 - ((SQUARE_SIZE // 1.2) // 2), SQUARE_SIZE // 1.1, SQUARE_SIZE // 1.1)
                pygame.draw.ellipse(surface, colour, rect)
                
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
        if hasattr(self, 'leave_rect') and self.leave_rect != None and self.leave_rect.collidepoint(mouse_pos):
            return "leave"
        elif hasattr(self, 'stay_rect') and self.stay_rect != None and self.stay_rect.collidepoint(mouse_pos):
            return "stay"
        elif hasattr(self, 'stay_circle') and self.stay_circle != None and self.stay_circle.collidepoint(mouse_pos):
            return "exit"
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
            
    def reset(self):
        self.__init__()