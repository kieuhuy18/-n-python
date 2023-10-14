import pygame
import game_config as gc

class GameAssets:
    #Hàm cho phép set ảnh, truyền vào tên của ảnh, muốn chỉnh tỷ lệ không, nếu có thì kích thước là bao nhiêu, nếu không truyền vào kích là 0, 0
    def load_img(self, path, scale=False, size=(0, 0)):
        #truyền vào tên của ảnh, sau đó convert ảnh
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

        #Load ảnh battle_city để lấy ảnh tank từ battle_city, lưu nó vào bie6b1 spritesheet
        self.spritesheet = self.load_img("BattleCity")

        #Load ảnh số
        self.number_image_black_white = self.load_img("numbers_black_white")
        self.number_image_black_orange = self.load_img("numbers_black_orange")

        #Gọi hàm load_all_tank_images để ra 1 dictionary với tất cả các ảnh tank đã được cắt ra từ ảnh battle_city
        self.tank_image = self._load_all_tank_images()

        #Load ảnh của bảng điểm
        self.score_sheet_image = {}
        #Load ảnh cần thiết cho bảng điểm rồi đưa chúng vào mảng sroce_sheet_image đã khởi tạo
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

        #Dùng 3 dòng for vs mỗi dòng for tương ứng cho 1 ảnh lần lượt là: tank level, loại tank, hướng đi
        tank_image_dict = {}
        for tank in range(8):
            tank_image_dict[f"Tank_{tank}"] = {} #Dòng for này cho tank level
            for group in ["Gold", "Silver", "Green", "Special"]:
                tank_image_dict[f"Tank_{tank}"][group] = {} #Dòng for này cho loại xe
                for direction in ["Up", "Down", "Left", "Right"]:
                    tank_image_dict[f"Tank_{tank}"][group][direction] = [] #Dòng for này cho hướng đi của tank
        for row in range(16): 
            for col in range(16):
                surface = pygame.Surface((gc.spriteSize, gc.spriteSize))
                surface.fill(gc.BLACK)
                surface.blit(self.spritesheet, (0, 0), (col * gc.spriteSize, row * gc.spriteSize,gc.spriteSize, gc.spriteSize))
                surface.set_colorkey(gc.BLACK)

                surface = self.scale_image(surface, gc.imageSize)
                tank_level = self._sort_tanks_into_levels(row)
                tank_group = self._sort_tanks_into_groups(row, col)
                tank_direction = self._sort_tanks_by_direction(col)
                tank_image_dict[tank_level][tank_group][tank_direction].append(surface)
        return tank_image_dict

    def scale_image(self, image, scale):
        """Scales the image according to the size passed in"""
        image = pygame.transform.scale(image, (scale, scale))
        return image

    def _sort_tanks_into_levels(self, row):
        """Sorts the tanks according to the row"""
        tank_levels = {0: "Tank_0", 1: "Tank_1", 2: "Tank_2", 3: "Tank_3",
                       4: "Tank_4", 5: "Tank_5", 6: "Tank_6", 7: "Tank_7"}
        return tank_levels[row % 8]

    def _sort_tanks_into_groups(self, row, col):
        """Sort each tank image into its different colour groups"""
        if 0 <= row <= 7 and 0 <= col <= 7:
            return "Gold"
        elif 8 <= row <= 16 and 0 <= col <= 7:
            return "Green"
        elif 0 <= row <= 7 and 8 <= col <= 16:
            return "Silver"
        else:
            return "Special"

    def _sort_tanks_by_direction(self, col):
        """Returns the current tank image by direction"""
        if col == 0 or col == 1 or col == 8  or col == 9: return "Up"
        elif col == 2 or col == 3 or col == 10 or col == 11: return "Left"
        elif col == 4 or col == 5 or col == 12 or col == 13: return "Down"
        else:
            return "Right"
