import pygame
import game_config as gc


class ScoreScreen:
    def __init__(self, game, assets):
        self.game = game
        self.assets = assets
        self.white_nums = self.assets.number_black_white
        self.orange_nums = self.assets.number_black_orange

        self.active = False
        self.timer = pygame.time.get_ticks()

        self.images = self.assets.score_sheet_image

        self.scoresheet = self.generate_scoresheet_screen()

    def update(self):
        if not pygame.time.get_ticks() - self.timer >= 10000:
            return

        self.active = False
        self.game.change_level()

    def draw(self, window):
        window.fill(gc.BLACK)
        window.blit(self.scoresheet, (0, 0))

    def generate_scoresheet_screen(self):
        """Generate a basic template screen for the score card transition screen"""
        surface = pygame.Surface((gc.SCREENWIDTH, gc.SCREENHEIGHT))
        surface.fill(gc.BLACK)
        new_img = gc.imageSize // 2
        surface.blit(self.images["hiScore"], (new_img * 8, new_img * 4))
        surface.blit(self.images["stage"], (new_img * 12, new_img * 6))

        arrow_left = self.images["arrow"]
        # Hàm cho pheop đào ngược hình ảnh của surface vs 3 tham số truyền vào là hình ảnh muốn đảo ngược, đảo ngược theo chiều ngang, đảo ngược theo chiều dọc
        arrow_right = pygame.transform.flip(arrow_left, True, False)

        if self.game.player1_active:
            surface.blit(self.images["player1"], (new_img * 3, new_img * 8))
        if self.game.player2_active:
            surface.blit(self.images["player2"], (new_img * 21, new_img * 8))

        for num, yPos in enumerate([12.5, 15, 17.5, 20]):
            if self.game.player1_active:
                surface.blit(self.images["pts"], (new_img * 8, new_img * yPos))
                surface.blit(arrow_left, (new_img * 14, new_img * yPos))
            if self.game.player2_active:
                surface.blit(self.images["pts"], (new_img * 26, new_img * yPos))
                surface.blit(arrow_right, (new_img * 17, new_img * yPos))
            surface.blit(self.assets.tank_image[f"Tank_{num + 4}"]["Silver"]["Up"][0], (new_img * 15, new_img * (yPos - 0.5)))

        surface.blit(self.images["total"], (new_img * 6, new_img * 22))
        return surface

    def number_image(self, score, number_color):
        """Convert a number into an image"""
        num = str(score)
        length = len(num)
        score_surface = pygame.Surface((gc.imageSize//2 * length, gc.imageSize // 2))
        for index, number in enumerate(num):
            score_surface.blit(number_color[int(number)], (gc.imageSize//2 * index, 0))
        return score_surface

    def update_player_score_images(self):
        self.pl_1_score = self.number_image(self.p1_score, self.orange_nums)
        self.pl_1_score_rect = self.pl_1_score.get_rect(
            topleft=(gc.imageSize//2 * 11 - self.pl_1_score.get_width(), gc.imageSize // 2 * 10))

        self.pl_2_score = self.number_image(self.p2_score, self.orange_nums)
        self.pl_2_score_rect = self.pl_2_score.get_rect(
            topleft=(gc.imageSize // 2 * 29 - self.pl_2_score.get_width(), gc.imageSize // 2 * 10))