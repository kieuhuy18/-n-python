import pygame
import game_config as gc

class Bullet(pygame.sprite.Sprite):
    def __init__(self, groups, owner, pos, direction, assets):
        super().__init__()
        self.assets = assets
        self.group = groups

         #  Các thuộc tính cơ bản
        self.tank = self.group["All_Tanks"]
        self.bullet = self.group["Bullets"]

        #  Thêm đối tượng tank vào group
        self.xPos, self.yPos = pos
        self.direction = direction

        self.owner = owner

        self.images = self.assets.bullet_images
        self.image = self.images[self.direction]
        self.rect = self.image.get_rect(center = (self.xPos, self.yPos))

        self.bullet.add(self)

    def update(self):
        pass

    def draw(self, window):
        window.blit(self.image, self.rect)
        pygame.draw.rect(window, gc.GREEN, self.rect, 1)