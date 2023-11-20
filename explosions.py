import pygame

class Explosion(pygame.sprite.Sprite):
    def __init__(self, assets, group, pos, explode_type=1):
        super().__init__()
        self.assets = assets
        self.group = group
        self.explosion_group = self.group["Explosion"]
        self.explosion_group.add(self)

        self.pos = pos
        self.explode_type = explode_type
        self.frame_index = 1
        self.images = self.assets.explosions
        self.image = self.images["explode_1"]
        self.rect = self.image.get_rect(center=self.pos)
        self.anim_timer = pygame.time.get_ticks()

    def update(self):
        if pygame.time.get_ticks() - self.anim_timer >= 100:
            self.frame_index += 1
            #Hủy hoạt ảnh khi chọn mức 5, frame đi hết mảng hình ảnh trong nổ
            if self.frame_index >= len(self.images):
                self.kill()
            #Hủy hoạt ảnh khi chọn mức 1, frame qua 3
            if self.explode_type == 1 and self.frame_index > 3:
                self.kill()
            self.anim_timer = pygame.time.get_ticks()
            self.image = self.images[f"explode_{self.frame_index}"]
            self.rect = self.image.get_rect(center=self.pos)

    def draw(self, window):
        window.blit(self.image, self.rect)