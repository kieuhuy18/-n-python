import pygame
import game_config as gc

class GameAssets:
    #Hàm load ảnh
    def load_img(self, path, scale=False, size=(0, 0)):
        #truyền vào tên của ảnh, sau đó convert
        img = pygame.image.load(f"assets/pic/{path}.png").convert_alpha()
        # nếu có chỉnh tỷ lệ thì sẽ chuyển đổi sang kích thước mong muốn
        if scale:
            img = pygame.transform.scale(img,size)
        return img
    
    #Hàm khởi tạo cho ảnh
    def __init__(self):
        #Load 2 ảnh bắt đầu
        self.star_screen = self.load_img("start_screen", True, (gc.SCREENWIDTH,gc.SCREENHEIGHT))
        self.star_screen_token = self.load_img("token", True, (gc.imageSize,gc.imageSize))

        #Load spritesheet (ảnh battle_city)
        self.spritesheet = self.load_img("BattleCity")

        #Load ảnh số với màu
        self.number_image_black_white = self.load_img("numbers_black_white")
        self.number_image_black_orange = self.load_img("numbers_black_orange")

        #Dùng hàm để lấy ra tất cả ảnh tank
        self.tank_image = self._load_all_tank_images()

        # load dict chứa tọa độ của các đối tượng trên spritesheet
        self.bullet_images = self.get_specified_images(self.spritesheet, gc.BULLETS, gc.BLACK)
        self.shield_images = self.get_specified_images(self.spritesheet, gc.SHIELD, gc.BLACK)
        self.spawn_star_images = self.get_specified_images(self.spritesheet, gc.SPAWN_STAR, gc.BLACK)
        self.power_up_images = self.get_specified_images(self.spritesheet, gc.POWER_UPS, gc.BLACK)
        self.flag = self.get_specified_images(self.spritesheet, gc.FLAG, gc.BLACK)
        self.explosions = self.get_specified_images(self.spritesheet, gc.EXPLOSIONS, gc.BLACK)
        self.score = self.get_specified_images(self.spritesheet, gc.SCORE, gc.BLACK)
        self.hud_images = self.get_specified_images(self.spritesheet, gc.HUD_INFO, gc.BLACK, transparent=False)
        self.context = self.get_specified_images(self.spritesheet, gc.CONTEXT, gc.BLACK)

        self.brick_tiles = self.get_specified_images(self.spritesheet, gc.MAP_TILES["bricks"], gc.BLACK)
        self.steel_tiles = self.get_specified_images(self.spritesheet, gc.MAP_TILES["steel"], gc.BLACK)
        self.forest_tiles = self.get_specified_images(self.spritesheet, gc.MAP_TILES["forest"], gc.BLACK)
        self.ice_tiles = self.get_specified_images(self.spritesheet, gc.MAP_TILES["ice"], gc.BLACK)
        self.water_tiles = self.get_specified_images(self.spritesheet, gc.MAP_TILES["water"], gc.BLACK)
        self.number_black_white = self.get_specified_images(self.number_image_black_white, gc.NUMS, gc.BLACK)
        self.number_black_orange = self.get_specified_images(self.number_image_black_orange, gc.NUMS, gc.BLACK) 

        #Load ảnh của bảng điểm
        self.score_sheet_image = {}
        for image in ["hiScore", "arrow", "player1", "player2", "pts", "stage", "total"]:
            self.score_sheet_image[image] = self.load_img(image)

    #Hàm lấy ra dictionary gồm tất cả ảnh của tank
    def _load_all_tank_images(self):
        #Nếu khai báo thủ công thì sẽ có dạng như sau:
        # tank_image_dict ={
        #     "Tank_0":{"Gold":{"Up": [], "Down": [], "Left": [], "Right": []},
        #               "Silver":{"Up": [], "Down": [], "Left": [], "Right": []},
        #               "Green":{"Up": [], "Down": [], "Left": [], "Right": []},
        #               "Special":{"Up": [], "Down": [], "Left": [], "Right": []}
        #               },
        #     "Tank_1":{"Gold":{"Up": [], "Down": [], "Left": [], "Right": []},
        #               "Silver":{"Up": [], "Down": [], "Left": [], "Right": []},
        #               "Green":{"Up": [], "Down": [], "Left": [], "Right": []},
        #               "Special":{"Up": [], "Down": [], "Left": [], "Right": []},
        #               },.....
        # }

        #Dùng 3 dòng for vs mỗi dòng for thay cho khai báo thủ công với lần lượt phần tử là: tank level, loại tank, hướng đi
        tank_image_dict = {}
        for tank in range(8):
            tank_image_dict[f"Tank_{tank}"] = {}
            for group in ["Gold", "Silver", "Green", "Special"]:
                tank_image_dict[f"Tank_{tank}"][group] = {}
                for direction in ["Up", "Down", "Left", "Right"]:
                    tank_image_dict[f"Tank_{tank}"][group][direction] = []

        #Duyệt ma trận 16 * 16 tương ứng vs ảnh tank trong spritesheet
        for row in range(16): 
            for col in range(16):
                #đưa ảnh lên surface
                surface = pygame.Surface((gc.spriteSize, gc.spriteSize))
                surface.fill(gc.BLACK)
                surface.blit(self.spritesheet, (0, 0), (col * gc.spriteSize, row * gc.spriteSize,gc.spriteSize, gc.spriteSize))
                surface.set_colorkey(gc.BLACK)
                surface = self.scale_image(surface, gc.spriteScale)

                #sắp xếp tank theo dict đã phân
                tank_level = self.sort_levels(row)
                tank_group = self.sort_groups(row, col)
                tank_direction = self.sort_direction(col)
                tank_image_dict[tank_level][tank_group][tank_direction].append(surface)
        return tank_image_dict

    #Chỉnh sửa kích thước ảnh
    def scale_image(self, image, scale):
        width, height = image.get_size()
        image = pygame.transform.scale(image, (scale * width, scale * height))
        return image

    #Sắp xếp các ảnh tank theo loại đã phân
    def sort_levels(self, row):
        tank_levels = {0: "Tank_0", 1: "Tank_1", 2: "Tank_2", 3: "Tank_3", 4: "Tank_4", 5: "Tank_5", 6: "Tank_6", 7: "Tank_7"}
        return tank_levels[row % 8]

    def sort_groups(self, row, col):
        if 0 <= row <= 7 and 0 <= col <= 7:
            return "Gold"
        elif 8 <= row <= 16 and 0 <= col <= 7:
            return "Green"
        elif 0 <= row <= 7 and 8 <= col <= 16:
            return "Silver"
        else:
            return "Special"

    def sort_direction(self, col):
        if col == 0 or col == 1 or col == 8  or col == 9: return "Up"
        elif col == 2 or col == 3 or col == 10 or col == 11: return "Left"
        elif col == 4 or col == 5 or col == 12 or col == 13: return "Down"
        else:
            return "Right"

    #Lấy ảnh cho các dict ngoài tank
    def get_specified_images(self, spritesheet, image_dict, color, transparent = True):
        img_dict ={}
        for key, pos in image_dict.items():
            img = self._get_images(spritesheet, pos[0], pos[1], pos[2], pos[3],color, transparent)
            img_dict.setdefault(key, img)
        return img_dict

    def _get_images(self, spritesheet, xpos, ypos, width, height, color, transparent = True):
        surface = pygame.Surface((width, height))
        surface.fill(color)
        surface.blit(spritesheet,(0, 0), (xpos, ypos, width, height))
        if transparent:
            surface.set_colorkey(color)
        surface = self.scale_image(surface, gc.spriteScale)
        return surface       