import sys, pygame

from const import *
from game import Game
from square import Square
from move import Move
from menu import Menu


class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Chinese Chess')
        colour_bg = (56,56,56)
        self.screen.fill(colour_bg)
        self.game = Game()
        self.menu = Menu()
        self.bg_surface = pygame.image.load("assets/images/bg.jpg").convert()
        self.is_playing = False
        
    def mainloop(self):
        
        game = self.game
        screen = self.screen
        board = self.game.board
        drag = self.game.dragger
        
        # Main game render loop
        while True:
            
            # Game starts on loading screen until user starts game which will switch is_playing and start game
            if not self.is_playing:
                screen.fill((50, 43, 43))
                self.menu.show_title(screen)
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT: 
                        pygame.quit()
                        sys.exit()
            
            # Game loop for game
            elif self.is_playing:
                self.screen.blit(self.bg_surface, (0,0))
                game.show_background(screen)
                game.show_log(screen)
                # game.show_last_move(screen)
                game.show_moves(screen)
                game.show_pieces(screen)
                
                
                if drag.is_dragging:
                    drag.update_blit(screen)
                
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
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
                                game.show_log(screen)
                                # game.show_last_move(screen)
                                game.show_moves(screen)
                                game.show_pieces(screen)
                                drag.update_blit(screen)
                    elif event.type == pygame.MOUSEMOTION:
                        if drag.is_dragging == True:
                            drag.update_mouse(event.pos)
                            self.screen.blit(self.bg_surface, (0,0))
                            game.show_background(screen)
                            game.show_log(screen)
                            # game.show_last_move(screen)
                            game.show_moves(screen)
                            game.show_pieces(screen)
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
                                board.move(drag.piece, move)
                                # Redraw board
                                game.show_background(screen)
                                # game.show_last_move(screen)
                                game.show_log(screen)
                                game.show_pieces(screen)
                                game.next_turn()
                                result = board.is_checkmate(game.next_player)
                                if result:
                                    print(str(game.next_player) + " has been checkmated")
                                else:
                                    print("No checkmate yet")
                                board.print_board()
                        drag.undrag_piece()
                        
                    
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            game.reset()    
                            game = self.game
                            board = self.game.board
                            drag = self.game.dragger
                    elif event.type == pygame.QUIT: 
                        pygame.quit()
                        sys.exit()
                    
            # Updates screen so put at end
            pygame.display.update()
    
main = Main()
main.mainloop()