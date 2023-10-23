import pygame
import game_config as gc
from characters import Tank, Player

class Game:
    def __init__(self, main, assets):
        """The main Game Object when playing"""
        #  Main file
        self.main = main
        self.assets = assets

        #  Object Groups
        self.groups = {"All_Tanks": pygame.sprite.Group()}

        #  Player Objects
        self.player1 = Player(self, self.assets, self.groups, (200, 200), "Up", "Gold", 0)
        self.player2 = Player(self, self.assets, self.groups, (400, 200), "Up", "Green", 0)

    def input(self):
        """Handle inputs for the game when it is running"""
        keypressed = pygame.key.get_pressed()
        self.player1.input(keypressed)
        self.player2.input(keypressed)

        #  pygame event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.main.run = False

            #  Keyboard shortcut to quit game
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.main.run = False

    def update(self):
        print("The game is being run")
        self.player1.update()
        self.player2.update()

    def draw(self, window):
        """Drawing to the screen"""
        self.player1.draw(window)
        self.player2.draw(window)