import pygame
import game_config as gc
from characters import EnemyTank, PlayerTank
from game_HUD import game_HUD
from random import choice, shuffle
from tile import BrickTile, SteelTile, ForestTile, IceTile, WaterTile
from fade_animate import Fade
from score_screen import ScoreScreen
from eagle import Eagle

class Game:
    def __init__(self, main, assets, player1 = True, player2 = False):

        #  Các thuộc tính cơ bản
        self.main = main
        self.assets = assets

        #  Các group đối tượng
        self.groups = {"Ice_Tiles": pygame.sprite.Group(),
                       "Water_Tiles": pygame.sprite.Group(),
                       "Player_Tanks": pygame.sprite.Group(),
                       "All_Tanks": pygame.sprite.Group(),
                       "Bullets": pygame.sprite.Group(),
                       "Destructable_Tiles": pygame.sprite.Group(),
                       "Impassable_Tiles": pygame.sprite.Group(),
                       "Eagle": pygame.sprite.GroupSingle(),
                       "Explosion": pygame.sprite.Group(),
                       "Forest_Tiles": pygame.sprite.Group()}
        
        self.top_score = 180903
        self.player1_active = player1
        self.p1_score = 0
        self.player2_active = player2
        self.p2_score = 0

        #Màn hình Heads-Up Display (hiển thị thông tin của người chơi) (HUD)
        self.hud = game_HUD(self, self.assets)

        #level
        self.level_num = 1
        self.level_complete = False
        self.level_translation_timer = None
        self.data = self.main.levels

        #Level fade
        self.fade = Fade(self, self.assets, 10)

        # Màn hình điểm số
        self.score_screen = ScoreScreen(self, self.assets)

        #  Đối tượng người chơi
        if self.player1_active:
            self.player1 = PlayerTank(self, self.assets, self.groups, gc.Pl1_position, "Up", "Gold", 0)
        if self.player2_active:
            self.player2 = PlayerTank(self, self.assets, self.groups, gc.Pl2_position, "Up", "Green", 0)

        # Đối tượng kẻ địch
        self.enemies = 20
        self.enemy_tank_spawn_timer = gc.TANK_SPAWNING_TIME
        self.enemy_spawn_positions = [gc.Pc1_position, gc.Pc2_position, gc.Pc3_position]

        # Khởi tạo map
        self.create_new_stage()

        self.end_game = False
        self.game_on = False

    def input(self):
        keypressed = pygame.key.get_pressed()

        #Hoạt động của người chơi
        if self.player1_active:
            self.player1.input(keypressed)
        if self.player2_active:
            self.player2.input(keypressed)

        for event in pygame.event.get():
            #  Thoát game
            if event.type == pygame.QUIT:
                self.main.run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.end_game = True
                
                if event.key == pygame.K_SPACE:
                    if self.player1_active:
                        self.player1.shoot()
                if event.key == pygame.K_RETURN:
                    if self.player2_active:
                        self.player2.shoot()
                
    def update(self):
        self.hud.update()

        if self.fade.fade_active:
            self.fade.update()
            if not self.fade.fade_active:
                for tank in self.groups["All_Tanks"]:
                    tank.spawn_timer = pygame.time.get_ticks()
            return

        for dict in self.groups.keys():
            if dict == "Player_Tanks":
                continue
            for key in self.groups[dict]:
                key.update()

        self.spawn_enemy_tanks()

        if self.enemies_killed <= 0 and self.level_complete == False:
            self.level_complete = True
            self.level_transition_timer = pygame.time.get_ticks()

        #  Stage Complete, load next stage
        if self.level_complete:
            if pygame.time.get_ticks() - self.level_transition_timer >= gc.TRANSITION_TIMER:
                self.stage_transition()
                # self.level_num += 1
                # self.create_new_stage()

    def draw(self, window):
        self.hud.draw(window)

        if self.score_screen.active:
            self.score_screen.draw(window)
            return

        for dict in self.groups.keys():
            if dict == "Impassable_Tiles":
                continue
            if self.fade.fade_active == True and (dict == "All_Tanks" or dict == "Player_Tanks"):
                continue
            for key in self.groups[dict]:
                key.draw(window)
            
        if self.fade.fade_active:
            self.fade.draw(window)

    def create_new_stage(self):
        # Đặt các groups ngoại trừ
        for key, value in self.groups.items():
            if key == "Player_Tanks":
                continue
            value.empty()

        #  Xét level hiện tại
        self.current_level_data = self.data.level_data[self.level_num-1]

        #  Số lượng kẻ địch, giảm dần khi xe tăng địch xuất hiện
        #self.enemies = random.choice([16, 17, 18, 19, 20])
        self.enemies = 10

        #  Số lượng kẽ địch bị tiêu diệt
        self.enemies_killed = self.enemies

        #  Load Map
        self.load_level_data(self.current_level_data)
        self.eagle = Eagle(self, self.assets, self.groups)
        self.level_complete = False

        self.fade.level = self.level_num
        self.fade.stage_image = self.fade.create_stage_image()
        self.fade.fade_active = True

        #  Tạo hàng chờ kẻ địch
        self.generate_spawn_queue()
        self.spawn_pos_index = 0
        self.spawn_queue_index = 0
        print(self.spawn_queue)

        # Tạo vị trí xuất hiện của người chơi
        if self.player1_active:
            self.player1.new_stage_spawn(gc.Pl1_position)
        if self.player2_active:
            self.player2.new_stage_spawn(gc.Pl2_position)

    def load_level_data(self, level):
        # Tạo lưới
        self.grid = []

        #Load ma trận
        for i, row in enumerate(level):
            line = []
            for j, tile in enumerate(row):
                pos = (gc.SCREEN_BORDER_LEFT + (j * gc.imageSize // 2),
                       gc.SCREEN_BORDER_TOP + (i * gc.imageSize // 2))
                if int(tile) < 0:
                    line.append("   ")
                elif int(tile) == 123: # Load Gạch: 123
                    line.append(f"{tile}")
                    map_tile = BrickTile(pos, self.groups["Destructable_Tiles"], self.assets.brick_tiles)
                    self.groups["Impassable_Tiles"].add(map_tile)
                elif int(tile) == 234: # Load thép: 234
                    line.append(f"{tile}")
                    map_tile = SteelTile(pos, self.groups["Destructable_Tiles"], self.assets.steel_tiles)
                    self.groups["Impassable_Tiles"].add(map_tile)
                elif int(tile) == 345: # Load rừng: 345
                    line.append(f"{tile}")
                    map_tile = ForestTile(pos, self.groups["Forest_Tiles"], self.assets.forest_tiles)
                elif int(tile) == 456: # Load băng: 456
                    line.append(f"{tile}")
                    map_tile = IceTile(pos, self.groups["Ice_Tiles"], self.assets.ice_tiles)
                elif int(tile) == 567: # Load nước: 567
                    line.append(f"{tile}")
                    map_tile = WaterTile(pos, self.groups["Water_Tiles"], self.assets.water_tiles)
                    self.groups["Impassable_Tiles"].add(map_tile)
                else:
                    line.append(f"{tile}")
            self.grid.append(line)

    def generate_spawn_queue(self):
        #Tạo hàng chờ với tỷ lệ dựa trên level hiện tại
        self.spawn_queue_ratios = gc.Tank_spawn_queue[f"queue_{str((self.level_num - 1 % 36) // 3)}"]
        self.spawn_queue = []

        #Dựa trên tỷ lệ tạo hàng chờ kẻ địch
        for lvl, ratio in enumerate(self.spawn_queue_ratios):
            for i in range(int(round(self.enemies * (ratio / 100)))):
                self.spawn_queue.append(f"level_{lvl}")
        shuffle(self.spawn_queue)

    def spawn_enemy_tanks(self):
        #Nếu không còn kẻ địch cần xuất hiện, dừng hàm
        if self.enemies == 0:
            return
        
        # Kiểm tra xem thời gian đã đủ để tạo kẻ địch mới hay chưa
        if pygame.time.get_ticks() - self.enemy_tank_spawn_timer >= gc.TANK_SPAWNING_TIME:
            position = self.enemy_spawn_positions[self.spawn_pos_index % 3]
            tank_level = gc.Tank_Criteria[self.spawn_queue[self.spawn_queue_index % len(self.spawn_queue)]]["image"]
            if tank_level == 7:
                EnemyTank(self, self.assets, self.groups, position, "Down", "Special", tank_level)
            else:
                EnemyTank(self, self.assets, self.groups, position, "Down", "Silver", tank_level)
            #  Reset the enemy tank spawn timer
            self.enemy_tank_spawn_timer = pygame.time.get_ticks()
            self.spawn_pos_index += 1
            self.spawn_queue_index += 1
            self.enemies -= 1

    def stage_transition(self):
        if not self.score_screen.active:
            self.score_screen.timer = pygame.time.get_ticks()
            if self. player1_active:
                self.score_screen.player_1_score = self.p1_score
                self.score_screen.player_1_killed = sorted(self.player1.score_list)
            if self. player2_active:
                self.score_screen.player_2_score = self.p2_score
                self.score_screen.player_2_killed = sorted(self.player2.score_list)
            self.score_screen.update_basic_info(self.top_score, self.level_num)
        self.score_screen.active = True
        self.score_screen.update()

    def change_level(self, p1_score, p2_score):
        self.level_num += 1
        self.level_num = self.level_num % len(self.data.level_data)
        self.p1_score = p1_score
        self.p2_score = p2_score
        self.create_new_stage()