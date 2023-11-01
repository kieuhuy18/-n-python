import pygame
import game_config as gc
from characters import Tank, Player
from game_HUD import game_HUD
from random import choice, shuffle

class Game:
    def __init__(self, main, assets, player1 = True, player2 = False):

        #  Các thuộc tính cơ bản
        self.main = main
        self.assets = assets

        #  Các group đối tượng
        self.groups = {"All_Tanks": pygame.sprite.Group(),
                       "Bullets": pygame.sprite.Group()}
        
        self.player1_active = player1
        self.player2_active = player2

        #Màn hình Heads-Up Display (hiển thị thông tin của người chơi) (HUD)
        self.hud = game_HUD(self, self.assets)

        #level
        self.level_num = 1
        self.data = self.main.levels

        #  Đối tượng người chơi
        if self.player1_active:
            self.player1 = Player(self, self.assets, self.groups, gc.Pl1_position, "Up", "Gold", 0)
        if self.player2_active:
            self.player2 = Player(self, self.assets, self.groups, gc.Pl2_position, "Up", "Green", 0)

        self.enemies = 20

        self.create_new_stage()

        self.end_game = False

    def input(self):
        """Handle inputs for the game when it is running"""
        keypressed = pygame.key.get_pressed()
        if self.player1_active:
            self.player1.input(keypressed)
        if self.player2_active:
            self.player2.input(keypressed)

        #  pygame event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.main.run = False

            #  Keyboard shortcut to quit game
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.end_game = True
                # if event.key == pygame.K_RETURN:
                #     self.player1.lives -= 1
                # if event.key == pygame.K_SPACE:
                #     self.player2.lives -= 
                
                if event.key == pygame.K_SPACE:
                    if self.player1_active:
                        self.player1.shoot()
                if event.key == pygame.K_RETURN:
                    if self.player2_active:
                        self.player2.shoot()

                if event.key == pygame.K_LSHIFT:
                    Tank(self, self.assets, self.groups, (400, 400), "Down")
                    self.enemies -= 1
                
    def update(self):
        self.hud.update()
        for dict in self.groups.keys():
            for key in self.groups[dict]:
                key.update()

    def draw(self, window):
        """Drawing to the screen"""
        self.hud.draw(window)
        # if self.player1_active:
        #     self.player1.draw(window)
        # if self.player2_active:
        #     self.player2.draw(window)
        for dict in self.groups.keys():
            for key in self.groups[dict]:
                key.draw(window)

    def create_new_stage(self):
        #  Retrieves the specific level data
        self.current_level_data = self.data.level_data[self.level_num-1]

        #  Number of enemy tanks to spawn in the stage, and this is tracked back to Zero
        #self.enemies = random.choice([16, 17, 18, 19, 20])
        self.enemies = 5

        #  Track the number of enemies killed back down to zero
        self.enemies_killed = self.enemies

        #  Load in the level Data
        self.load_level_data(self.current_level_data)

        #  Generating the spawn queue for the computer tanks
        self.generate_spawn_queue()
        self.spawn_pos_index = 0
        self.spawn_queue_index = 0

        if self.player1_active:
            self.player1.new_stage_spawn(gc.Pl1_position)

    def load_level_data(self, level):
        """Load the level Data"""
        self.grid = []
        for i, row in enumerate(level):
            line = []
            for j, tile in enumerate(row):
                pos = (gc.SCREEN_BORDER_LEFT + (j * gc.imageSize // 2),
                       gc.SCREEN_BORDER_TOP + (i * gc.imageSize // 2))
                if int(tile) < 0:
                    line.append("   ")
                elif int(tile) == 123:
                    line.append(f"{tile}")
                elif int(tile) == 234:
                    line.append(f"{tile}")
                elif int(tile) == 345:
                    line.append(f"{tile}")
                elif int(tile) == 456:
                    line.append(f"{tile}")
                elif int(tile) == 567:
                    line.append(f"{tile}")
                else:
                    line.append(f"{tile}")
            self.grid.append(line)
        for row in self.grid:
            print(row)

    def generate_spawn_queue(self):
        """Generate a list of tanks that will be spawning during the level"""
        self.spawn_queue_ratios = gc.Tank_spawn_queue[f"queue_{str((self.level_num - 1 % 36) // 3)}"]
        self.spawn_queue = []

        for lvl, ratio in enumerate(self.spawn_queue_ratios):
            for i in range(int(round(self.enemies * (ratio / 100)))):
                self.spawn_queue.append(f"level_{lvl}")
        shuffle(self.spawn_queue)