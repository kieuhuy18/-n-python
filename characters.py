import pygame
from bullet import Bullet
import game_config as gc

class Tank(pygame.sprite.Sprite):
    def __init__(self, game, assets, groups, position, direction, enemy=True, colour="Silver", tank_level=0):
        super().__init__()
        #  Game Object and Assets
        self.game = game
        self.assets = assets
        self.groups = groups

        #  Sprite groups that may interact with tank
        self.tank_group = self.groups["All_Tanks"]
        self.player_group = self.groups["Player_Tanks"]

        #  Add tank object to the sprite group
        self.tank_group.add(self)

        #  Tank Images
        self.tank_images = self.assets.tank_image
        self.spawn_images = self.assets.spawn_star_images

        #  Tank Position and Direction
        self.spawn_pos = position
        self.xPos, self.yPos = self.spawn_pos
        self.direction = direction

        #  Tank Spawning / Active
        self.spawning = True
        self.active = False

        #  Common Tank Attributes
        self.tank_level = tank_level
        self.colour = colour
        self.tank_speed = gc.TANK_SPEED
        self.enemy = enemy
        self.tank_health = 1

        #  Tank Image, Rectangle, and Frame Index
        self.frame_index = 0
        self.image = self.tank_images[f"Tank_{self.tank_level}"][self.colour][self.direction][self.frame_index]
        self.rect = self.image.get_rect(topleft=(self.spawn_pos))
        self.width, self.height = self.image.get_size()

        #  Shoot Cooldowns and Bullet Totals
        self.bullet_limit = 1
        self.bullet_sum = 0

        #  Tank paralysis
        self.paralyzed = False
        self.paralysis = gc.TANK_PARALYSIS
        self.paralysis_timer = pygame.time.get_ticks()

        #  Spawn images
        self.spawn_image = self.spawn_images[f"star_{self.frame_index}"]
        self.spawn_timer = pygame.time.get_ticks() # Overall spawn timer
        self.spawn_anim_timer = pygame.time.get_ticks()  # Spawn star anim timer

        #  Tank Image Mask Dictionary
        self.mask_dict = self.get_various_masks()
        self.mask = self.mask_dict[self.direction]
        #self.mask_image = self.mask.to_surface()
        self.mask_direction = self.direction

    def input(self):
        pass

    def update(self):
        #  Update the spawning animations
        if self.spawning:
            #  Update the spawning star animations, if the required amount of time has passed.
            if pygame.time.get_ticks() - self.spawn_anim_timer >= 50:
                self.spawn_animation()
            #  if total spawn timer seconds passed, change self.spawning.
            if pygame.time.get_ticks() - self.spawn_timer > 2000:
                self.frame_index = 0
                self.spawning = False
                self.active = True
            return

        if self.paralyzed:
            if pygame.time.get_ticks() - self.paralysis_timer >= self.paralysis:
                self.paralyzed = False

    def draw(self, window):
        #  if tank is spawning in, draw the spawn star
        if self.spawning:
            window.blit(self.spawn_image, self.rect)

        #  If the tank is set to active, draw to screen
        if self.active:
            window.blit(self.image, self.rect)
            #window.blit(self.mask_image, self.rect)
            pygame.draw.rect(window, gc.RED, self.rect, 1)

    #  Tank movement
    def grid_alignment_movement(self, pos):
        if pos % (gc.imageSize//2) != 0:
            if pos % (gc.imageSize // 2) < gc.imageSize // 4:
                pos -= (pos % (gc.imageSize // 4))
            elif pos % (gc.imageSize // 2) > gc.imageSize // 4:
                pos += (gc.imageSize//4) - (pos % (gc.imageSize//4))
            else:
                return pos
        return pos

    def move_tank(self, direction):
        """Move the tank in the passed direction"""
        if self.spawning:
            return

        self.direction = direction

        if self.paralyzed:
            self.image = self.tank_images[f"Tank_{self.tank_level}"][self.colour][self.direction][self.frame_index]
            return

        if direction == "Up":
            self.yPos -= self.tank_speed
            self.xPos = self.grid_alignment_movement(self.xPos)
            if self.yPos < gc.SCREEN_BORDER_TOP:
                self.yPos = gc.SCREEN_BORDER_TOP
        elif direction == "Down":
            self.yPos += self.tank_speed
            self.xPos = self.grid_alignment_movement(self.xPos)
            if self.yPos + self.height > gc.SCREEN_BORDER_BOTTOM:
                self.yPos = gc.SCREEN_BORDER_BOTTOM - self.height
        elif direction == "Left":
            self.xPos -= self.tank_speed
            self.yPos = self.grid_alignment_movement(self.yPos)
            if self.xPos < gc.SCREEN_BORDER_LEFT:
                self.xPos = gc.SCREEN_BORDER_LEFT
        elif direction == "Right":
            self.xPos += self.tank_speed
            self.yPos = self.grid_alignment_movement(self.yPos)
            if self.xPos + self.width > gc.SCREEN_BORDER_RIGHT:
                self.xPos = gc.SCREEN_BORDER_RIGHT - self.width

        #  Update the Tank Rectangle Position
        self.rect.topleft = (self.xPos, self.yPos)
        #  Update the Tank Animation
        self.tank_movement_animation()
        #  Check for tank collisions with other tanks
        self.tank_on_tank_collisions()
        #  Check for tank collisions with obstacles
        self.tank_collisions_with_obstacles()

    #  Tank Animations
    def tank_movement_animation(self):
        """update the animation images to simulate the tank moving"""
        self.frame_index += 1
        imagelistlength = len(self.tank_images[f"Tank_{self.tank_level}"][self.colour][self.direction])
        self.frame_index = self.frame_index % imagelistlength
        self.image = self.tank_images[f"Tank_{self.tank_level}"][self.colour][self.direction][self.frame_index]
        if self.mask_direction != self.direction:
            self.mask_direction = self.direction
            self.mask = self.mask_dict[self.mask_direction]
            #self.mask_image = self.mask.to_surface()

    def spawn_animation(self):
        """Cycle through the spawn star images to simulate a spawning icon"""
        self.frame_index += 1
        self.frame_index = self.frame_index % len(self.spawn_images)
        self.spawn_image = self.spawn_images[f"star_{self.frame_index}"]
        self.spawn_anim_timer = pygame.time.get_ticks()

    def get_various_masks(self):
        """Creates and returns a dictionary of masks for all directions"""
        images = {}
        for direction in ["Up", "Down", "Left", "Right"]:
            image_to_mask = self.tank_images[f"Tank_{self.tank_level}"][self.colour][direction][0]
            images.setdefault(direction, pygame.mask.from_surface(image_to_mask))
        return images

    #  Tank Collisions
    def tank_on_tank_collisions(self):
        """Check if the tank collides with another tank"""
        tank_collision = pygame.sprite.spritecollide(self, self.tank_group, False)
        if len(tank_collision) == 1:
            return

        for tank in tank_collision:
            #  Skip the tank if it is the current object
            if tank == self:
                continue

            if self.direction == "Right":
                if self.rect.right >= tank.rect.left and \
                    self.rect.bottom > tank.rect.top and self.rect.top < tank.rect.bottom:
                    self.rect.right = tank.rect.left
                    self.xPos = self.rect.x
            elif self.direction == "Left":
                if self.rect.left <= tank.rect.right and \
                    self.rect.bottom > tank.rect.top and self.rect.top < tank.rect.bottom:
                    self.rect.left = tank.rect.right
                    self.xPos = self.rect.x
            elif self.direction == "Up":
                if self.rect.top <= tank.rect.bottom and \
                    self.rect.left < tank.rect.right and self.rect.right > tank.rect.left:
                    self.rect.top = tank.rect.bottom
                    self.yPos = self.rect.y
            elif self.direction == "Down":
                if self.rect.bottom >= tank.rect.top and \
                    self.rect.left < tank.rect.right and self.rect.right > tank.rect.left:
                    self.rect.bottom = tank.rect.top
                    self.yPos = self.rect.y

    def tank_collisions_with_obstacles(self):
        """Perform collision checks with tank and obstacles"""
        wall_collision = pygame.sprite.spritecollide(self, self.groups["Impassable_Tiles"], False)
        for obstacle in wall_collision:
            if self.direction == "Right":
                if self.rect.right >= obstacle.rect.left:
                    self.rect.right = obstacle.rect.left
                    self.xPos = self.rect.x
            elif self.direction == "Left":
                if self.rect.left <= obstacle.rect.right:
                    self.rect.left = obstacle.rect.right
                    self.xPos = self.rect.x
            elif self.direction == "Down":
                if self.rect.bottom >= obstacle.rect.top:
                    self.rect.bottom = obstacle.rect.top
                    self.yPos = self.rect.y
            elif self.direction == "Up":
                if self.rect.top <= obstacle.rect.bottom:
                    self.rect.top = obstacle.rect.bottom
                    self.yPos = self.rect.y

    #  Tank Shooting
    def shoot(self):
        if self.bullet_sum >= self.bullet_limit:
            return

        bullet = Bullet(self.groups, self, self.rect.center, self.direction, self.assets)
        self.bullet_sum += 1

    #  Actions affecting tanks
    def paralyze_tank(self, paralysis_time):
        """If player tank is hit by player tank, or if the freeze power up is used"""
        self.paralysis = paralysis_time
        self.paralyzed = True
        self.paralysis_timer = pygame.time.get_ticks()

    def destroy_tank(self):
        """Method to damage a tanks health, and if health at zero, destroy the tank"""
        self.tank_health -= 1
        #  If health reaches zero, destroy tank
        if self.tank_health <= 0:
            self.kill()
            return

class Player(Tank):
    def __init__(self, game, assets, groups, position, direction, colour, tank_level):
        super().__init__(game, assets, groups, position, direction, False, colour, tank_level)
        self.player_group.add(self)
        #  Player Lives
        self.lives = 3

    def input(self, keypressed):
        """Move the player tanks"""
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

    def new_stage_spawn(self, spawn_pos):
        self.tank_group.add(self)
        self.xPos, self.yPos = spawn_pos
        self.rect.topleft = (self.xPos, self.yPos)