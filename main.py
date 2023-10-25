import pygame
import game_config as gc
from game_assets import GameAssets
from game import Game

class MainGame:

    #Hàm khởi tạo game
    def __init__(self):
        #Khởi tạo game
        pygame.init()

        #Khởi tạo các thành phần cơ bản của game
        self.screen = pygame.display.set_mode((gc.SCREENWIDTH, gc.SCREENHEIGHT))
        pygame.display.set_caption("Battle City")
        self.clock = pygame.time.Clock()
        self.run = True

        #Gọi đối tượng game assets
        self.assets = GameAssets() 

        #Gọi đối tượng game
        self.game_on = True
        self.game = Game(self, self.assets, True, True)

    #Hàm chạy game chính
    def run_gamme(self):
        while self.run:
            self.input()
            self.update()
            self.draw()
 
    def input(self): 
        if self.game_on:
            self.game.input()
            
        if not self.game_on:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
            
    def update(self):
        #Cài đặt fps cho game
        self.clock.tick(gc.FPS)

        if self.game_on:
            self.game.update()
    
    def draw(self):
        self.screen.fill(gc.BLACK)

        #self.screen.blit(self.assets.bullet_images["Up"], (400, 400))

        if self.game_on:
            self.game.draw(self.screen)
        pygame.display.update()

#Chạy game
if __name__ == "__main__":
    m = MainGame()
    m.run_gamme()
    pygame.quit()