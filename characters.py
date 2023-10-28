import pygame
import game_config as gc
from bullet import Bullet


class Tank(pygame.sprite.Sprite):
    def __init__(self, game, assets, groups, position, direction, enemy = True, colour="Silver", tank_level=0):
        super().__init__()
        #  Các thuộc tính cơ bản
        self.game = game
        self.assets = assets
        self.group = groups
        self.tank_group = self.group["All_Tanks"]

        #  Thêm đối tượng tank vào group
        self.tank_group.add(self)

        #  Tank Images
        self.tank_images = self.assets.tank_image
        self.spawn_images = self.assets.spawn_star_images

        #  Tank Position and Direction
        self.spawn_pos = position
        self.xPos, self.yPos = self.spawn_pos
        self.direction = direction

        #Tank Spawning/ Active
        self.active = False
        self.spawning = True

        #  Common Tank Attributes
        self.tank_level = tank_level
        self.colour = colour
        self.tank_speed =gc.TANK_SPEED

        self.Enemy = enemy

        #  Tank Image, Rectangle, and Frame Index
        #Note:
        self.frame_index = 0
        self.image = self.tank_images[f"Tank_{self.tank_level}"][self.colour][self.direction][self.frame_index]
        self.rect = self.image.get_rect(topleft=(self.spawn_pos)) 
        self.width, self.height = self.image.get_size()
        #Note ^

        #Shoot cooldown
        self.bullet_limit = 1
        self.bullet_sum = 0

        # Làm tê liệt tank
        self.paralyzed = False
        self.paralysis = gc.TANK_PARALYSIS
        self.paralysis_timer = pygame.time.Clock()

        #spawn images
        self.spawn_image = self.spawn_images[f"star_{self.frame_index}"]
        self.spawn_time = pygame.time.get_ticks()
        self.spawn_ani_time = pygame.time.get_ticks()

    def input(self):
        pass

    def update(self):
        if self.spawning:
            if pygame.time.get_ticks() - self.spawn_ani_time >= 50:
                self.spawn_animation()
            if pygame.time.get_ticks() - self.spawn_time > 2000:
                self.frame_index = 0
                self.spawning = False
                self.active = True
            return
        
        if self.paralyzed:
            if pygame.time.get_ticks() - self.paralysis_timer >= self.paralysis:
                self.paralyzed = False

    def draw(self, window):
        if self.spawning:
            window.blit(self.spawn_image, self.rect)
        #  If the tank is set to active, draw to screen
        if self.active:
            window.blit(self.image, self.rect)
            pygame.draw.rect(window, gc.RED, self.rect, 1)
    
    def move_tank(self, direction):
        if self.spawning:
            return
        
        self.direction = direction

        if self.paralyzed:
            return
        
        if direction == "Up":
            self.yPos -= self.tank_speed
            if self.yPos < gc.SCREEN_BORDER_TOP:
                self.yPos = gc.SCREEN_BORDER_TOP
        elif direction == "Down":
            self.yPos += self.tank_speed
            if self.yPos + self.height > gc.SCREEN_BORDER_BOTTOM:
                self.yPos = gc.SCREEN_BORDER_BOTTOM - self.height
        elif direction == "Left":
            self.xPos -= self.tank_speed
            if self.xPos < gc.SCREEN_BORDER_LEFT:
                self.xPos = gc.SCREEN_BORDER_LEFT
        elif direction == "Right":
            self.xPos += self.tank_speed
            if self.xPos + self.width > gc.SCREEN_BORDER_RIGHT:
                self.xPos = gc.SCREEN_BORDER_RIGHT - self.width

        #Note:
        self.rect.topleft = (self.xPos, self.yPos)
        self.tank_move_animation()
        self.tank_collision()

    def tank_move_animation(self):
        self.frame_index += 1
        self.frame_index = self.frame_index % 2
        self.image = self.tank_images[f"Tank_{self.tank_level}"][self.colour][self.direction][self.frame_index]  

    def spawn_animation(self):
        self.frame_index += 1
        self.frame_index = self.frame_index % 4
        self.spawn_image = self.spawn_images[f"star_{self.frame_index}"]
        spawn_ani_timer = pygame.time.get_ticks()

    def tank_collision(self):    
        tank_coll = pygame.sprite.spritecollide(self, self.tank_group, False) #Hàm trả về danh sách các sprite xung đột, luôn có 1 tank trong này
        if len(tank_coll) == 1:
            return
        for tank in tank_coll:
            if tank == self:
                continue
            if self.direction == "Right":
                if self.rect.right >= tank.rect.left and self.rect.bottom > tank.rect.top and self.rect.top < tank.rect.bottom:
                    self.rect.right = tank.rect.left
                    self.xPos = self.rect.x
            elif self.direction == "Left":
                if self.rect.left <= tank.rect.right and self.rect.bottom > tank.rect.top and self.rect.top < tank.rect.bottom:
                    self.rect.left = tank.rect.right
                    self.xPos = self.rect.x
            elif self.direction == "Up":
                if self.rect.top <= tank.rect.bottom and self.rect.left < tank.rect.right and self.rect.right > tank.rect.left:
                    self.rect.top = tank.rect.bottom
                    self.yPos = self.rect.y
            elif self.direction == "Down":
                if self.rect.bottom >= tank.rect.top and self.rect.left < tank.rect.right and self.rect.right > tank.rect.left:
                    self.rect.bottom = tank.rect.top
                    self.yPos = self.rect.y

    def shoot(self):
        if self.bullet_sum >= self.bullet_limit:
            return
        bulletT = Bullet(self.group, self, self.rect.center, self.direction, self.assets)
        self.bullet_sum += 1

    def paralyze_tank(self, paralysis_time):
        self.paralysis = paralysis_time
        self.paralyzed = True
        self.paralysis_timer = pygame.time.get_ticks()

class Player(Tank):
    def __init__(self, game, assets, group, position, direction, colour, tank_level):
        super().__init__(game, assets, group, position, direction, False, colour, tank_level)
        self.lives = 3

    def input(self, keypressed):
        if self.colour == "Gold":
            if keypressed[pygame.K_w]:
                self.move_tank("Up")
            elif keypressed[pygame.K_s]:
                self.move_tank("Down")
            elif keypressed[pygame.K_a]:
                self.move_tank("Left")
            elif keypressed[pygame.K_d]:
                self.move_tank("Right")

        if self.colour == "Green":
            if keypressed[pygame.K_UP]:
                self.move_tank("Up")
            elif keypressed[pygame.K_DOWN]:
                self.move_tank("Down")
            elif keypressed[pygame.K_LEFT]:
                self.move_tank("Left")
            elif keypressed[pygame.K_RIGHT]:
                self.move_tank("Right")
