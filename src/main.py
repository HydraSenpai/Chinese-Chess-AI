import sys, pygame
import time
from const import *
from game import Game
from square import Square
from move import Move
from menu import Menu
from log import Log
from agent import Agent

class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Chinese Chess')
        icon = pygame.image.load("assets/images/pieces/black_king.png")
        pygame.display.set_icon(icon)
        colour_bg = (56,56,56)
        self.screen.fill(colour_bg)
        self.game = Game()
        self.menu = Menu()
        self.log = Log()
        self.agent = Agent()
        self.bg_surface = pygame.image.load("assets/images/bg.jpg").convert()
        self.is_playing = False
        self.ai_level = None
        self.clock = pygame.time.Clock()
        
    def mainloop(self):
        
        game = self.game
        screen = self.screen
        log = self.log
        board = self.game.board
        drag = self.game.dragger
        agent = self.agent
        
        # Main game render loop
        while True:
            
            # Game starts on loading screen until user starts game which will switch is_playing and start game
            if not self.is_playing:
                screen.fill((50, 43, 43))
                self.menu.show_title(screen)
                self.menu.show_buttons(screen)
                
                # Only input checks should be for quitting and clicking difficulty to start game
                for event in pygame.event.get():
                    if event.type == pygame.QUIT: 
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        # Check if the mouse click occurred within the buttons box
                        result = self.menu.was_button_clicked(event.pos)
                        if not result:
                            break
                        else:
                            self.ai_level = result
                            self.is_playing = True
            
            # Game loop for game
            elif self.is_playing:
                self.screen.blit(self.bg_surface, (0,0))
                game.show_background(screen)
                game.show_last_move(screen)
                game.show_log(screen, log.move_list)
                game.show_pieces(screen)
                
                # If game is won then show winning modal to allow user to leave or stay looking at board
                if game.is_won:
                    if not game.stay:
                        game.show_winning_modal(screen, game.lost)
                    else:
                        game.show_exit_button(screen)
                    # Only checks should be for quitting and clicking one of two menu buttons (exit to menu or stay)
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT: 
                            pygame.quit()
                            sys.exit()
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            # Checks if a button was clicked on the modal and returns the type clicked
                            leave_or_stay = game.was_button_clicked(event.pos)
                            if not leave_or_stay:
                                break
                            else:
                                # If leave return to main menu and reset game objects
                                if leave_or_stay == "leave":
                                    self.is_playing = False
                                    game.reset()
                                    game = self.game
                                    board = self.game.board
                                    drag = self.game.dragger
                                    log.clear_list()
                                # If stay remove modal
                                elif leave_or_stay == "stay":
                                    game.stay = True
                                elif leave_or_stay == "exit":
                                    self.is_playing = False
                                    game.reset()
                                    game = self.game
                                    board = self.game.board
                                    drag = self.game.dragger
                                    log.clear_list()
                                
                # Main game input
                elif not game.is_won:
                    game.show_background(screen)
                    game.show_log(screen, log.move_list)
                    game.show_last_move(screen)
                    game.show_moves(screen)
                    game.show_pieces(screen)
                    game.show_exit_button(screen)
                    
                    
                    if drag.is_dragging:
                        drag.update_blit(screen)
                    
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            # Check if exit button was clicked to leave application
                            leave_or_stay = game.was_button_clicked(event.pos)
                            if leave_or_stay == "exit":
                                self.is_playing = False
                                game.reset()
                                game = self.game
                                board = self.game.board
                                drag = self.game.dragger
                                log.clear_list()
                                break
                            # Update mouse position
                            drag.update_mouse(event.pos)
                            # Check if mouse click is in a row and column that contains a piece
                            column_clicked = (drag.mouseX + 40) // (SQUARE_SIZE) - 1
                            row_clicked = (drag.mouseY + 40) // (SQUARE_SIZE) - 1
                            # print("Row Clicked = " + str(row_clicked))
                            # print("Column Clicked = " + str(column_clicked))
                            if column_clicked > 8 or column_clicked < 0 or row_clicked > 9 or row_clicked < 0:
                                break
                            if(board.squares[row_clicked][column_clicked].has_piece()):
                                piece = board.squares[row_clicked][column_clicked].piece
                                # Check colour is equal to turn
                                if piece.colour == game.next_player:
                                    # Clear before valid move
                                    piece.clear_moves()
                                    # Calculate moves
                                    board.calculate_moves(piece, row_clicked, column_clicked, bool=True)
                                    # Save initial piece position and start dragging
                                    drag.save_initial_pos(event.pos)
                                    drag.drag_piece(piece)
                                    # Show methods
                                    self.screen.blit(self.bg_surface, (0,0))
                                    game.show_background(screen)
                                    game.show_log(screen, log.move_list)
                                    game.show_last_move(screen)
                                    game.show_moves(screen)
                                    game.show_pieces(screen)
                                    game.show_exit_button(screen)
                                    drag.update_blit(screen)
                        elif event.type == pygame.MOUSEMOTION:
                            if drag.is_dragging == True:
                                drag.update_mouse(event.pos)
                                self.screen.blit(self.bg_surface, (0,0))
                                game.show_background(screen)
                                game.show_log(screen, log.move_list)
                                game.show_last_move(screen)
                                game.show_moves(screen)
                                game.show_pieces(screen)
                                game.show_exit_button(screen)
                                drag.update_blit(screen) 
                        elif event.type == pygame.MOUSEBUTTONUP:
                            if drag.is_dragging:
                                drag.update_mouse(event.pos)
                                # Save released grid position
                                released_row = (drag.mouseY + 40) // (SQUARE_SIZE) - 1
                                released_column = (drag.mouseX + 40) // (SQUARE_SIZE) - 1
                                # print("Row Released = " + str(released_row))
                                # print("Column Released = " + str(released_column))
                                # Create possible move
                                initial = Square((drag.initial_row + 40) // (SQUARE_SIZE) - 1, (drag.initial_column + 40) // (SQUARE_SIZE) - 1)
                                final = Square(released_row, released_column)
                                move = Move(initial, final)
                                # Start moving process
                                if board.valid_move(drag.piece, move):
                                    if board.squares[released_row][released_column].has_piece():    
                                        sound = pygame.mixer.Sound("assets/sounds/capture.wav")
                                        sound.play()
                                    else:
                                        # Play move sound
                                        sound = pygame.mixer.Sound("assets/sounds/move.wav")
                                        sound.play()
                                    board.move(drag.piece, move)
                                    # Add move to log
                                    log.add_to_list(move)
                                    # Redraw board
                                    game.show_background(screen)
                                    game.show_last_move(screen)
                                    game.show_log(screen, log.move_list)
                                    game.show_pieces(screen)
                                    game.show_exit_button(screen)
                                    game.next_turn()
                                    # Check if checkmate has occurred at end of each turn
                                    result = board.is_checkmate(game.next_player)
                                    if result:
                                        print(str(game.next_player) + " has been checkmated")
                                        game.is_won = True
                                        game.lost = game.next_player
                                        sound = pygame.mixer.Sound("assets/sounds/win.mp3")
                                        sound.play()
                                    else:
                                        print("No checkmate yet")
                                    # REMOVE THESE LINES TO PLAY AGAINST OTHER PLAYER -----------------------
                                    # If turn is black then do agent move instead
                                    if game.next_player == "black": 
                                        agent.update_board(board)
                                        agent_result = agent.calculate_all_possible_moves(game.next_player)
                                        # If no move can be calculated then king is in check and game is over
                                        if agent_result == None:
                                            game.is_won = True
                                            game.lost = game.next_player
                                            sound = pygame.mixer.Sound("assets/sounds/win.mp3")
                                            sound.play()
                                        else:
                                            agent_piece, agent_move = agent_result 
                                            # Play sound for AI
                                            if board.squares[agent_move.final.row][agent_move.final.column].has_piece():    
                                                sound = pygame.mixer.Sound("assets/sounds/capture.wav")
                                                sound.play()
                                            else:
                                                # Play move sound
                                                sound = pygame.mixer.Sound("assets/sounds/move.wav")
                                                sound.play()
                                            board.move(agent_piece, agent_move)
                                            log.add_to_list(agent_move)
                                            # Redraw board
                                            game.show_log(screen, log.move_list)
                                            game.next_turn()
                                    # -----------------------------------------------------------------------        
                            drag.undrag_piece()
                            
                        # Pressing R resets the game if playing
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_r:
                                game.reset()    
                                game = self.game
                                board = self.game.board
                                drag = self.game.dragger
                                log.clear_list()
                        elif event.type == pygame.QUIT: 
                            pygame.quit()
                            sys.exit()
                    
            # Updates screen so put at end
            pygame.display.update()
            
            self.clock.tick(60)
    
main = Main()
main.mainloop()