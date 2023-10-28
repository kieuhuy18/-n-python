import pygame
import game_config as gc
from characters import Tank, Player
from game_HUD import game_HUD

class Game:
    def __init__(self, main, assets, player1 = True, player2 = False):

        #  Các thuộc tính cơ bản
        self.main = main
        self.assets = assets

        #  Các group đối tượng
        self.groups = {"All_Tanks": pygame.sprite.Group(),
                       "Bullets": pygame.sprite.Group()}
        
        self.player1_active = player1
        self.player2_active = player2

        #Màn hình Heads-Up Display (hiển thị thông tin của người chơi) (HUD)
        self.hud = game_HUD(self, self.assets)

        #level
        self.level = 1

        #  Đối tượng người chơi
        if self.player1_active:
            self.player1 = Player(self, self.assets, self.groups, (200, 200), "Up", "Gold", 0)
        if self.player2_active:
            self.player2 = Player(self, self.assets, self.groups, (400, 200), "Up", "Green", 0)

        self.enemies = 20

    def input(self):
        """Handle inputs for the game when it is running"""
        keypressed = pygame.key.get_pressed()
        if self.player1_active:
            self.player1.input(keypressed)
        if self.player2_active:
            self.player2.input(keypressed)

        #  pygame event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.main.run = False

            #  Keyboard shortcut to quit game
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.main.run = False
                # if event.key == pygame.K_RETURN:
                #     self.player1.lives -= 1
                # if event.key == pygame.K_SPACE:
                #     self.player2.lives -= 
                
                if event.key == pygame.K_SPACE:
                    if self.player1_active:
                        self.player1.shoot()
                if event.key == pygame.K_RETURN:
                    if self.player2_active:
                        self.player2.shoot()

                if event.key == pygame.K_RETURN:
                    Tank(self, self.assets, self.groups, (400, 400), "Down")
                    self.enemies -= 1
                
    def update(self):
        self.hud.update()
        # if self.player1_active:
        #     self.player1.update()
        # if self.player2_active:
        #     self.player2.update()
        for dict in self.groups.keys():
            for key in self.groups[dict]:
                key.update()

    def draw(self, window):
        """Drawing to the screen"""
        self.hud.draw(window)
        # if self.player1_active:
        #     self.player1.draw(window)
        # if self.player2_active:
        #     self.player2.draw(window)
        for dict in self.groups.keys():
            for key in self.groups[dict]:
                key.draw(window)