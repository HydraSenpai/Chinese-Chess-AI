import sys, pygame

from const import *
from game import Game


class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Chinese Chess')
        colour_bg = (92, 84, 112)
        self.screen.fill(colour_bg)
        self.game = Game()
        
    def mainloop(self):
        
        game = self.game
        screen = self.screen
        
        while True:
            game.show_background(screen)
            game.show_pieces(screen)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    pygame.quit()
                    sys.exit()
                    
            # Updates screen so put at end
            pygame.display.update()
    
main = Main()
main.mainloop()