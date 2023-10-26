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

    def move(self):
        speed = gc.Tank_speed * 3
        if self.direction == "Up":
            self.yPos -= speed
        elif self.direction == "Down":
            self.yPos += speed
        elif self.direction == "Left":
            self.xPos -= speed
        elif self.direction == "Right":
            self.xPos += speed
        self.rect.center = (self.xPos, self.yPos)

    def collide_edge_of_screen(self):
        if self.rect.top <= gc.SCREEN_BORDER_TOP or self.rect.bottom >= gc.SCREEN_BORDER_BOTTOM or self.rect.left <= gc.SCREEN_BORDER_LEFT or self.rect.right >= gc.SCREEN_BORDER_RIGHT:
            self.update_owner()
            self.kill()
            
    def update_owner(self):
        if self.owner.bullet_sum > 0:
            self.owner.bullet_sum -= 1

    def update(self):
        self.move()
        self.collide_edge_of_screen()

    def draw(self, window):
        window.blit(self.image, self.rect)
        pygame.draw.rect(window, gc.GREEN, self.rect, 1)