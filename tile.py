import pygame
import game_config as gc


class TileType(pygame.sprite.Sprite):
    def __init__(self, pos, group, map_tile):
        super().__init__(group)
        self.group = group
        self.images = map_tile
        self.xPos = pos[0]
        self.yPos = pos[1]

    def update(self):
        pass

    def get_rect_and_size(self, position):
        self.rect = self.image.get_rect(topleft=position)
        self.width, self.height = self.image.get_size()

    def draw(self, window):
        window.blit(self.image, self.rect)

    def hit_by_bullet(self, bullet):
        pass

class BrickTile(TileType):
    def __init__(self, pos, group, map_tile):
        super().__init__(pos, group, map_tile)
        self.health = 2
        self.name = "Brick"
        self.image = self.images["small"]
        self.get_rect_and_size((self.xPos, self.yPos))

    def hit_by_bullet(self, bullet):
        bullet.update_owner()
        bullet.kill()
        self.health -= 1
        if self.health <= 0:
            self.kill()
            return
        
        #Chỉnh kích thước của gạch khi bị bắn
        if bullet.direction == "Left":
            self.image = self.images["small_left"]
            self.get_rect_and_size((self.xPos, self.yPos))
        elif bullet.direction == "Right":
            self.image = self.images["small_right"]
            self.get_rect_and_size((self.xPos + self.width//2, self.yPos))
        elif bullet.direction == "Up":
            self.image = self.images["small_top"]
            self.get_rect_and_size((self.xPos, self.yPos))
        elif bullet.direction == "Down":
            self.image = self.images["small_bot"]
            self.get_rect_and_size((self.xPos, self.yPos + self.height//2))

class SteelTile(TileType):
    def __init__(self, pos, group, map_tile):
        super().__init__(pos, group, map_tile)
        self.name = "Steel"
        self.image = self.images["small"]
        self.get_rect_and_size((self.xPos, self.yPos))

    def hit_by_bullet(self, bullet):
        bullet.update_owner()
        bullet.kill()

class ForestTile(TileType):
    def __init__(self, pos, group, map_tile):
        super().__init__(pos, group, map_tile)
        self.image = self.images["small"]
        self.get_rect_and_size((self.xPos, self.yPos))

#Ice được kế thừa từ forest
class IceTile(ForestTile):
    def __init__(self, pos, group, map_tile):
        super().__init__(pos, group, map_tile)
        self.get_rect_and_size((self.xPos, self.yPos))

class WaterTile(TileType):
    def __init__(self, pos, group, map_tile):
        super().__init__(pos, group, map_tile)
        self.image = self.images["small_1"]
        self.get_rect_and_size((self.xPos, self.yPos))
        self.frame_index = 0
        self.timer = pygame.time.get_ticks()

    def update(self):
        #Di chuyển frame nước
        if pygame.time.get_ticks() - self.timer >= 500:
            self.frame_index = 1 if self.frame_index == 0 else 0
            self.timer = pygame.time.get_ticks()
            self.image = self.images[f"small_{self.frame_index + 1}"]