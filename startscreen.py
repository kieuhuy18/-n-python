import pygame
import game_config as gc


class StartScreen:
    def __init__(self, main, assets):
        self.main = main
        self.assets = assets

        #  Start Screen Coords
        self.start_y = gc.SCREENHEIGHT
        self.end_y = 0

        #  Start ScreenImages and Rect
        self.image = self.assets.start_screen
        self.rect = self.image.get_rect(topleft=(0, 0))
        self.x, self.y = self.rect.topleft

        self.start_screen_active = False

    def input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.main.run = False
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.main.run = False
                    return False
        return True

    def update(self):
        pass

    def draw(self, window):
        window.blit(self.image, self.rect)