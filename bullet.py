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

        self.mask = pygame.mask.from_surface(self.image)
        #self.mask_image = self.mask.to_surface()

        self.bullet.add(self)

    def move(self):
        speed = gc.TANK_SPEED * 3
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

    def collide_tank(self):
        tank_collisions = pygame.sprite.spritecollide(self, self.tank, False)
        for tank in tank_collisions:
            if self.owner == tank or tank.spawning == True:
                continue   
            if pygame.sprite.collide_mask(self, tank): 
                if self.owner.Enemy == False and tank.Enemy == False:
                    self.update_owner()
                    tank.paralyze_tank(gc.TANK_PARALYSIS)
                    self.kill()
                    break

            if(self.owner.Enemy == False and tank.Enemy == True) or (self.owner.Enemy == True and tank.Enemy == False):
                if self.owner.Enemy == False and tank.Enemy == False:
                    self.update_owner()
                    tank.destroy_tank()
                    self.kill()
                    break

    def collision_bullet(self):
        Bullet_hit = pygame.sprite.spritecollide(self, self.bullet, False)
        if len(Bullet_hit) == 1:
            return
        for bullet in Bullet_hit:
            if bullet == self:
                continue
            if pygame.sprite.collide_mask(self, bullet):
                bullet.update_owner()
                bullet.kill()
                self.update_owner()
                self.kill()
                break

    def update(self):
        self.move()
        self.collide_edge_of_screen()
        self.collide_tank()
        self.collision_bullet()

    def draw(self, window):
        window.blit(self.image, self.rect)
        #window.blit(self.mask_image, self.rect)
        pygame.draw.rect(window, gc.GREEN, self.rect, 1)