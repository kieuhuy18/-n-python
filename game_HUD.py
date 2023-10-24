import pygame
import game_config as gc

class game_HUD:
    def __init__(self, game, assets):
        self.game = game
        self.assets = assets
        self.image = self.assets.hud_images
        self.hud_overlay = self.generate_hud_overlay_screen()

    def generate_hud_overlay_screen(self):
        overlay_screen = pygame.Surface((gc.SCREENWIDTH, gc.SCREENHEIGHT))
        overlay_screen.fill(gc.GREY)
        pygame.draw.rect(overlay_screen, gc.BLACK, (gc.GAME_SCREEN))
        overlay_screen.blit(self.image["info_panel"], (gc.Info_x, gc.Info_y))
        overlay_screen.set_colorkey(gc.BLACK)
        return overlay_screen
    
    def update(self):
        pass

    def draw(self, window):
        window.blit(self.hud_overlay, (0, 0))