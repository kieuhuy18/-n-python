import pygame
import game_config as gc

class game_HUD:
    def __init__(self, game, assets):
        self.game = game
        self.assets = assets
        self.images = self.assets.hud_images
        self.hud_overlay = self.generate_hud_overlay_screen()

        #player lives
        self.player1_active = False
        self.player1_lives = 0
        self.player1_lives_image = self.display_player_lives(self.player1_lives,self.player1_active)
        self.player2_active = False
        self.player2_lives = 0
        self.player2_lives_image = self.display_player_lives(self.player2_lives,self.player2_active)

        #level
        self.level = 1
        self.level_image = self.display_stage_number(self.level)
        self.level_image_rect = self.level_image.get_rect(topleft = (14.5 * gc.imageSize, 13 * gc.imageSize))

    def generate_hud_overlay_screen(self):
        overlay_screen = pygame.Surface((gc.SCREENWIDTH, gc.SCREENHEIGHT))
        overlay_screen.fill(gc.GREY)
        pygame.draw.rect(overlay_screen, gc.BLACK, (gc.GAME_SCREEN))
        overlay_screen.blit(self.images["info_panel"], (gc.Info_x, gc.Info_y))
        overlay_screen.set_colorkey(gc.BLACK)
        return overlay_screen

    def draw_enemies(self, window):
        row = 0
        offset_x, offset_x_2 = 14.5 * gc.imageSize, 15 * gc.imageSize
        for num in range(gc.Enemies):
            if num % 2 == 0:
                x, y = offset_x, (4 + row) * (gc.imageSize//2)
            else:
                x, y = offset_x_2, (4 + row) * (gc.imageSize//2)
                row += 1
            if num < self.enemies:
                window.blit(self.images["life"], (x, y))
            else:
                window.blit(self.images["grey_square"], (x, y))
        return

    def display_player_lives(self, lives, player_active):
        width, height = gc.imageSize, gc.imageSize // 2
        surface = pygame.Surface((width, height))
        surface.fill(gc.BLACK)
        if lives > 99:
            lives = 99
        if not player_active:
            surface.blit(self.images["grey_square"], (0, 0))
            surface.blit(self.images["grey_square"], (gc.imageSize // 2, 0))
            return surface
        if lives < 10:
            image = pygame.transform.rotate(self.images["life"], 180)
        else:
            num = str(lives)[0]
            image = self.images[f"num_{num}"]
        surface.blit(image, (0, 0))
        num = str(lives)[-1]
        image_2 = self.images[f"num_{num}"]
        surface.blit(image_2, (gc.imageSize // 2, 0))
        return surface
    
    def display_stage_number(self, level):
        width, height = gc.imageSize, gc.imageSize // 2
        surface = pygame.Surface((width, height))
        surface.fill(gc.BLACK)
        if level < 10:
            image_1 = self.images["num_0"]
        else:
            num = str(level)[0]
            image_1 = self.images[f"num_{num}"]
        surface.blit(image_1, (0, 0))
        num = str(level)[-1]
        image_2 = self.images[f"num_{num}"]
        surface.blit(image_2, (gc.imageSize // 2 ,0))
        return surface

    def update(self):
        self.enemies = self.game.enemies
        #  Update the number of player lives available
        self.player1_active = self.game.player1_active
        if self.player1_active:
            if self.player1_lives != self.game.player1.lives:
                self.player1_lives = self.game.player1.lives
                self.player1_lives_image = self.display_player_lives(self.player1_lives, self.player1_active)
        self.player2_active = self.game.player2_active
        if self.player2_active:
            if self.player2_lives != self.game.player2.lives:
                self.player2_lives = self.game.player2.lives
                self.player2_lives_image = self.display_player_lives(self.player2_lives, self.player2_active)

        if self.level != self.game.level:
            self.level = self.game.level
            self.level_image = self.display_level(self.level)

    def draw(self, window):
        window.blit(self.hud_overlay, (0, 0))

        self.draw_enemies(window)

        window.blit(self.player1_lives_image, (14.5 * gc.imageSize, 9.5 * gc.imageSize))
        window.blit(self.player2_lives_image, (14.5 * gc.imageSize, 11 * gc.imageSize))

        window.blit(self.level_image, self.level_image_rect)