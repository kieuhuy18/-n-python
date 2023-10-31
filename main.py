import pygame
import game_config as gc
from game_assets import GameAssets
from game import Game
from level_editor import LevelEditor
from levels import LevelData
from startscreen import StartScreen

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
        self.levels = LevelData() 

        self.start_screen = StartScreen(self, self.assets)
        self.start_screen_active = True

        #Gọi đối tượng game
        self.game_on = False
        self.game = Game(self, self.assets, True, True)

        self.level_editor_on = False
        self.Creator = LevelEditor(self, self.assets)

    #Hàm chạy game chính
    def run_gamme(self):
        while self.run:
            self.input()
            self.update()
            self.draw()
 
    def input(self): 
        if self.game_on:
            self.game.input()

        if self.start_screen_active:
            self.start_screen_active = self.start_screen.input()

        if self.level_editor_on:
            self.Creator.input()
            
        if not self.game_on and not self.level_editor_on and not self.start_screen_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
            
    def update(self):
        #Cài đặt fps cho game
        self.clock.tick(gc.FPS)

        if self.start_screen_active:
            self.start_screen.update()

        if self.game_on:
            self.game.update()

        if self.level_editor_on:
            self.Creator.update()

    def draw(self):
        self.screen.fill(gc.BLACK)

        if self.game_on:
            self.game.draw(self.screen)

        if self.start_screen_active:
            self.start_screen.draw(self.screen)
        
        if self.level_editor_on:
            self.Creator.draw(self.screen)
        pygame.display.update()

#Chạy game
if __name__ == "__main__":
    m = MainGame()
    m.run_gamme()
    pygame.quit()