import pygame
import game_config as gc
from game_assets import GameAssets

class MainGame:
    #Hàm khởi tạo game
    def __init__(self):
        #Khởi tạo game
        pygame.init()
        #Set screen, caption cho game
        self.screen = pygame.display.set_mode((gc.SCREENWIDTH, gc.SCREENHEIGHT))
        pygame.display.set_caption("Battle City")
        self.clock = pygame.time.Clock()
        self.run = True
        self.assets = GameAssets()

    def run_gamme(self):
        while self.run:
            self.input()
            self.update()
            self.draw()

    #Hàm đọc sự kiện 
    def input(self):
        #Thoát ra khi ng chơi nhấn thoát
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
            
    def update(self):
        #Cài đặt fps cho game
        self.clock.tick(gc.FPS)
    
    def draw(self):
        #In lên màn hình
        self.screen.fill(gc.BLACK)
        self.screen.blit(self.assets.tank_image["Tank_0"]["Silver"]["Up"][1], (400, 400))
        pygame.display.update()

if __name__ == "__main__":
    m = MainGame()
    m.run_gamme()
    pygame.quit()