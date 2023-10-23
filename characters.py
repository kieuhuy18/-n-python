import pygame
import game_config as gc


class Tank(pygame.sprite.Sprite):
    def __init__(self, game, assets, groups, position, direction, colour="Silver", tank_level=0):
        super().__init__()
        #  Game Object and Assets
        self.game = game
        self.assets = assets
        self.groups = groups

        #  Sprite groups that may interact with tank
        self.tank_group = self.groups["All_Tanks"]

        #  Add tank object to the sprite group
        self.tank_group.add(self)

        #  Tank Images
        self.tank_image = self.assets.tank_image

        #  Tank Position and Direction
        self.spawn_pos = position
        self.xPos, self.yPos = self.spawn_pos
        self.direction = direction

        #  Common Tank Attributes
        self.active = True
        self.tank_level = tank_level
        self.colour = colour
        self.tank_speed =gc.Tank_speed

        #  Tank Image, Rectangle, and Frame Index
        #Note:
        self.frame_index = 0
        self.image = self.tank_image[f"Tank_{self.tank_level}"][self.colour][self.direction][self.frame_index]
        self.rect = self.image.get_rect(topleft=(self.spawn_pos))
        #Note ^

    def input(self):
        pass

    def update(self):
        pass

    def draw(self, window):
        #  If the tank is set to active, draw to screen
        if self.active:
            window.blit(self.image, self.rect)
    
    def move_tank(self, direction):
        if direction == "Up":
            self.yPos -= self.tank_speed
        elif direction == "Down":
            self.yPos += self.tank_speed
        elif direction == "Left":
            self.xPos -= self.tank_speed
        elif direction == "Right":
            self.xPos += self.tank_speed

        #Note:
        self.rect.topleft = (self.xPos, self.yPos)

class Player(Tank):
    def __init__(self, game, assets, groups, position, direction, colour, tank_level):
        super().__init__(game, assets, groups, position, direction, colour, tank_level)

    def input(self, keypressed, player):
        self.frame_index += 1
        if player == 0:
            if keypressed[pygame.K_w]:
                self.move_tank("Up")
            if keypressed[pygame.K_s]:
                self.move_tank("Down")
            if keypressed[pygame.K_a]:
                self.move_tank("Left")
            if keypressed[pygame.K_d]:
                self.move_tank("Right")
        if player == 1:
            if keypressed[pygame.K_UP]:
                self.move_tank("Up")
            if keypressed[pygame.K_DOWN]:
                self.move_tank("Down")
            if keypressed[pygame.K_LEFT]:
                self.move_tank("Left")
            if keypressed[pygame.K_RIGHT]:
                self.move_tank("Right")
        self.frame_index = self.frame_index % 2