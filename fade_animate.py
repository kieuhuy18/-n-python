import pygame
import game_config as gc


class Fade:
    def __init__(self, game, assets, speed=5):
        #Class thực thi việc chuyển cảnh, bằng các tạo 2 khối hình chữ nhật ở ngoài screen và đưa nó vào trong màn hình
        self.game = game
        self.level = self.game.level_num - 1
        self.assets = assets
        self.images = self.assets.hud_images
        self.speed = speed

        self.fade_active = False
        self.fade_in = True
        self.fade_out = False
        self.transition = False
        self.timer = pygame.time.get_ticks()

        # Xác định rect phía trên, tạo 2 điểm để check khi rect đã vào đúng vị trí, tạo 1 điểm để giúp di chuyển rect
        self.top_rect = pygame.Rect(0, 0 - gc.SCREENHEIGHT//2, gc.SCREENWIDTH, gc.SCREENHEIGHT//2)
        self.top_rect_start_y = self.top_rect.bottom
        self.top_rect_end_y = gc.SCREENHEIGHT // 2
        self.top_y = self.top_rect.bottom

        #Xác định rect phía dưới, tạo 2 điểm để check khi rect đã vào đúng vị trí, tạo 1 điểm để giúp di chuyển rect
        self.bot_rect = pygame.Rect(0, gc.SCREENHEIGHT, gc.SCREENWIDTH, gc.SCREENHEIGHT//2)
        self.bot_rect_start_y = self.bot_rect.top
        self.bot_rect_end_y = gc.SCREENHEIGHT // 2
        self.bot_y = self.bot_rect.top

        self.stage_pic_width, self.stage_pic_height = self.images["stage"].get_size()
        self.num_pic_width, self.num_pic_height = self.images["num_0"].get_size()

        #Tạo surface và rect cho stage number
        self.stage_image = self.create_stage_image()
        self.stage_image_rect = self.stage_image.get_rect(center=(gc.SCREENWIDTH//2, gc.SCREENHEIGHT//2))

    def update(self):
        #Có 3 giai đoạn là đi vào, chờ và đi ra

        if not self.fade_active:
            return
        
        #Đi vào
        if self.fade_in:
            self.top_y = self.move_y_fade(self.top_y, self.top_rect_start_y, self.top_rect_end_y, self.speed)
            self.top_rect.bottom = self.top_y

            self.bot_y = self.move_y_fade(self.bot_y, self.bot_rect_start_y, self.bot_rect_end_y, self.speed)
            self.bot_rect.top = self.bot_y

            #Đặt lại trạng thái cho rect
            if self.top_rect.bottom == self.top_rect_end_y and self.bot_rect.top == self.bot_rect_end_y:
                self.fade_in = False
                self.fade_out = False
                self.transition = True
                self.timer = pygame.time.get_ticks()

        #Chờ
        elif self.transition:
            if pygame.time.get_ticks() - self.timer >= 1000:
                self.fade_in = False
                self.fade_out = True
                self.transition = False

        #Đi ra
        elif self.fade_out:
            self.top_y = self.move_y_fade(self.top_y, self.top_rect_end_y, self.top_rect_start_y, self.speed)
            self.top_rect.bottom = self.top_y

            self.bot_y = self.move_y_fade(self.bot_y, self.bot_rect_end_y, self.bot_rect_start_y, self.speed)
            self.bot_rect.top = self.bot_y

            if self.top_rect.bottom == self.top_rect_start_y and self.bot_rect.top == self.bot_rect_start_y:
                self.fade_in = True
                self.fade_out = False
                self.transition = False
                self.fade_active = False
                self.game.game_on = True
                return

    def draw(self, window):
        #Vẽ phần màn hạ xuống màu xám
        pygame.draw.rect(window, gc.GREY, self.top_rect)
        pygame.draw.rect(window, gc.GREY, self.bot_rect)
        if self.transition:
            window.blit(self.stage_image, self.stage_image_rect)
            #pygame.draw.rect(window, gc.RED, self.stage_image_rect, 2)

    def move_y_fade(self, ycoord, start_pos, end_pos, speed):
        #  Dựa vào vị trí start và end để kiểm tra
        # Kiểm tra đi lên
        if start_pos > end_pos:
            ycoord -= speed
            if ycoord < end_pos:
                ycoord = end_pos

        #  Kiểm tra đi xuống
        elif start_pos < end_pos:
            ycoord += speed
            if ycoord > end_pos:
                ycoord = end_pos
        return ycoord

    def create_stage_image(self):
        # Tạo surface cho hình stage bao gồm hình stage và number
        surface = pygame.Surface((self.stage_pic_width + (self.num_pic_width * 3), self.stage_pic_height))
        surface.fill(gc.GREY)
        surface.blit(self.images["stage"], (0, 0))
        if self.level < 10:
            surface.blit(self.images["num_0"], (self.stage_pic_width + self.num_pic_width, 0))
        else:
            surface.blit(self.images[f"num_{str(self.level)[0]}"], (self.stage_pic_width + self.num_pic_width, 0))
        surface.blit(self.images[f"num_{str(self.level)[-1]}"], (self.stage_pic_width + (self.num_pic_width * 2), 0))
        return surface