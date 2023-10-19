import pygame
import game_config as gc

class Game:
    def __init__(self, main, assets):
        """Main game khi chơi"""
        #  Main file
        self.main = main
        self.assets = assets

    def input(self):
        """Xử lý input khi game đang chạy"""
        #  xử lý sự kiện quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.main.run = False

            #  khi nhấn nút esc 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.main.run = False

    def update(self):
        print("The game is being run")

    def draw(self, window):
        """Drawing to the screen"""
        pass