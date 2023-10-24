import sys, pygame

from const import *
from game import Game


class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Chinese Chess')
        colour_bg = (56,56,56)
        self.screen.fill(colour_bg)
        self.game = Game()
        self.bg_surface = pygame.image.load("assets/images/bg.jpg").convert()
        
        
    def mainloop(self):
        
        game = self.game
        screen = self.screen
        board = self.game.board
        drag = self.game.dragger
        
        while True:
            
            self.screen.blit(self.bg_surface, (0,0))
            game.show_background(screen)
            game.show_pieces(screen)
            game.show_log(screen)
            if drag.is_dragging:
                drag.update_blit(screen)
            
            
            
            
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Update mouse position
                    drag.update_mouse(event.pos)
                    # Check if mouse click is in a row and column that contains a piece
                    column_clicked = (drag.mouseX + 40) // (SQUARE_SIZE) - 1
                    row_clicked = (drag.mouseY + 40) // (SQUARE_SIZE) - 1
                    if(board.squares[row_clicked][column_clicked].has_piece()):
                        piece = board.squares[row_clicked][column_clicked].piece
                        # Save initial piece position and start dragging
                        drag.save_initial_pos(event.pos)
                        drag.drag_piece(piece)
                elif event.type == pygame.MOUSEMOTION:
                    if drag.is_dragging == True:
                        drag.update_mouse(event.pos)
                        self.screen.blit(self.bg_surface, (0,0))
                        game.show_background(screen)
                        game.show_pieces(screen)
                        game.show_log(screen)
                        drag.update_blit(screen)
                elif event.type == pygame.MOUSEBUTTONUP:
                    drag.undrag_piece()
                elif event.type == pygame.QUIT: 
                    pygame.quit()
                    sys.exit()
                    
            # Updates screen so put at end
            pygame.display.update()
    
main = Main()
main.mainloop()