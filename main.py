import pygame
import game_config as gc
from game_assets import GameAssets
from game import Game
from level_editor import LevelEditor
from levels import LevelData
from startscreen import StartScreen

class MainGame:
    #Hàm khởi tạo game
    def __init__(self):
        #Khởi tạo game
        pygame.init()
        pygame.mixer.init()

        #Khởi tạo các thành phần cơ bản của game
        self.screen = pygame.display.set_mode((gc.SCREENWIDTH, gc.SCREENHEIGHT))
        pygame.display.set_caption("Battle City")
        self.clock = pygame.time.Clock()
        self.run = True

        #Gọi đối tượng game assets, game level
        self.assets = GameAssets()
        self.levels = LevelData() 

        #Màn hình bắt đầu
        self.start_screen = StartScreen(self, self.assets)
        self.start_screen_active = True
        self.assets.channel_game_start_sound.play(self.assets.game_start_sound)

        #Chế độ game
        self.game_on = False
        self.game = None

        # CHế độ edit level
        self.level_editor_on = False
        self.level_create = None

    #Hàm chạy game
    def run_gamme(self):
        while self.run:
            self.input()
            self.update()
            self.draw()
 
    def input(self): 
        if self.game_on:
            self.game.input()
            
        if self.start_screen_active:
            self.start_screen_active = self.start_screen.input()

        if self.level_editor_on:
            self.level_create.input()
            
        if not self.game_on and not self.level_editor_on and not self.start_screen_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
            
    def update(self):
        #Cài đặt fps cho game
        self.clock.tick(gc.FPS)

        #Load màn hình bắt đầu
        if self.start_screen_active:
            self.start_screen.update()

        #Tắt nhạc khi màn hình bắt đầu không hoạt động
        if not self.start_screen_active:
            self.assets.channel_game_start_sound.stop()   

        #Load Game
        if self.game_on:
            self.game.update()

        #Out ra màn hình khởi đầu khi kết thúc game
        if self.game:
            if self.game.end_game == True:
                self.start_screen = StartScreen(self, self.assets)
                self.start_screen_active = True
                self.game_on = False
                self.game = None

        #Load phần edit
        if self.level_editor_on:
            self.level_create.update()

        #Out ra màn hình khởi đầu khi kết thúc edit
        if self.level_create:
            if self.level_create.active == False: 
                self.start_screen = StartScreen(self, self.assets)
                self.start_screen_active = True
                self.level_editor_on = False
                self.level_create = None

    def draw(self):
        self.screen.fill(gc.BLACK)

        #Vẽ màn hình bắt đầu
        if self.start_screen_active:
            self.start_screen.draw(self.screen)

        #Vẽ màn hình game
        if self.game_on:
            self.game.draw(self.screen)

        # Vẽ màn hình edit
        if self.level_editor_on:
            self.level_create.draw(self.screen)
        pygame.display.update()

    #Chết độ game 
    def start_new_game(self, player1, player2):
        self.game_on = True
        self.game = Game(self, self.assets, player1, player2)
        self.start_screen_active = False

    #Chết độ edit
    def start_new_create(self):
        self.level_editor_on = True
        self.level_create = LevelEditor(self, self.assets)
        self.start_screen_active = False
    
#Chạy game
if __name__ == "__main__":
    m = MainGame()
    m.run_gamme()
    pygame.quit()