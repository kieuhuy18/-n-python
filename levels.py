import pygame
import os
import csv

class LevelData:
    def __init__(self):
        self.level_data = self.load_level_data()

    def load_level_data(self):
        #Mảng chứa các mảng 2 chiều map
        gameStages = []
        # Duyệt các file trong folder
        for stage in os.listdir("levels"):
            # tạo mảng 2 chiều
            level_data = [[] for i in range(27)]
            with open(f"levels/{stage}", newline="") as csvFile:
                #đọc các phần tử được cách nhau bởi dấu ,
                reader = csv.reader(csvFile, delimiter=",")
                #add phần tử trong file vào mảng
                for i, row in enumerate(reader):
                    for j, tile in enumerate(row):
                        level_data[i].append(int(tile))
            #add mảng map vào mảng lớn
            gameStages.append(level_data)
        return gameStages

    def save_level_data(self, level_data):
        #số lượng ký tự của màn
        number = len(level_data)
        for i in range(number): 
            #gán num là string số màn
            num = str(i + 1) if len(str(i + 1)) > 1 else "0" + str(i + 1) 
            #Lưu file
            with open(f"levels/BattleCityLevel{num}.csv", "w", newline="") as csvFile:
                writer = csv.writer(csvFile, delimiter=",")
                for row in level_data[i]:
                    writer.writerow(row)
        return