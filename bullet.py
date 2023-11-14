import pygame
import game_config as gc

class Bullet(pygame.sprite.Sprite):
    def __init__(self, groups, owner, pos, direction, assets):
        super().__init__()
        self.assets = assets
        self.group = groups
        self.xPos, self.yPos = pos
        self.direction = direction
        self.owner = owner

         #  Các mảng 
        self.tank = self.group["All_Tanks"]
        self.bullet = self.group["Bullets"]

        #Load ảnh đạn
        self.images = self.assets.bullet_images
        self.image = self.images[self.direction]
        self.rect = self.image.get_rect(center = (self.xPos, self.yPos))

        #Hàm va chạm mask
        #Mask dùng để kiểm tra va chạm pixel
        self.mask = pygame.mask.from_surface(self.image)

        # thêm đối tượng hiện tại vào gr bullets
        self.bullet.add(self)

    def move(self):
        speed = gc.TANK_SPEED * 2
        if self.direction == "Up":
            self.yPos -= speed
        elif self.direction == "Down":
            self.yPos += speed
        elif self.direction == "Left":
            self.xPos -= speed
        elif self.direction == "Right":
            self.xPos += speed
        self.rect.center = (self.xPos, self.yPos)

    def collide_edge_of_screen(self):
        #Kiểm tra đường viền
        if self.rect.top <= gc.SCREEN_BORDER_TOP or self.rect.bottom >= gc.SCREEN_BORDER_BOTTOM or self.rect.left <= gc.SCREEN_BORDER_LEFT or self.rect.right >= gc.SCREEN_BORDER_RIGHT:
            self.update_owner()
            #Nếu va chạm sẽ hủy bỏ đối tượng
            self.kill()

    # countdown số đạn bằng bullet_sum, cho bullet_sum = 0, khi bắn +1, nếu va chạm sẽ giảm xuống 1
    def update_owner(self):
        if self.owner.bullet_sum > 0:
            self.owner.bullet_sum -= 1

    def collide_tank(self):
        #Hàm va chạm kiểm tra va chạm giữa các đối tượng
        tank_collisions = pygame.sprite.spritecollide(self, self.tank, False)
        #Vòng lặp xét va chạm giữa đạn vs xe tank
        for tank in tank_collisions:

            #Vì hàm va chạm luôn tính va chạm với chính đối tượng gốc nên phải loại bỏ ra khỏi vòng lặp
            if self.owner == tank or tank.spawning == True:
                continue

            if pygame.sprite.collide_mask(self, tank): 
                #Nếu bắn nhầm đồng đội sẽ khiến đồng đội bị tê liệt
                if self.owner.enemy == False and tank.enemy == False:
                    self.update_owner()
                    tank.paralyze_tank(gc.TANK_PARALYSIS)
                    self.kill()
                    break
            
                #Bắn trúng địch sẽ tiêu diệt đạn cùng với tank
                if(self.owner.enemy == False and tank.enemy == True) or (self.owner.enemy == True and tank.enemy == False):
                    self.update_owner()
                    if not self.owner.enemy:
                        self.owner.score_list.append(gc.Tank_Criteria[tank.level]["score"])
                    tank.destroy_tank()
                    self.kill()
                    break

    def collision_with_obstacle(self):
        #Load mảng có thể phá hủy vào hàm
        obstacle_collide = pygame.sprite.spritecollide(self, self.group["Destructable_Tiles"], False)
        for obstacle in obstacle_collide:
            obstacle.hit_by_bullet(self)

    def collision_bullet(self):
        Bullet_hit = pygame.sprite.spritecollide(self, self.bullet, False)
        #Nếu chỉ có 1 đối tượng trong mảng va chạm, hàm sẽ không thực hiện
        if len(Bullet_hit) == 1:
            return
        
        for bullet in Bullet_hit:
            #Vì hàm va chạm luôn tính va chạm với chính đối tượng gốc nên phải loại bỏ ra khỏi vòng lặp
            if bullet == self:
                continue

            #Hủy 2 viện đan c=khi chúng va chạm với nhau
            if pygame.sprite.collide_mask(self, bullet):
                bullet.update_owner()
                bullet.kill()
                self.update_owner()
                self.kill()
                break

    def update(self):
        self.move()
        self.collide_edge_of_screen()
        self.collide_tank()
        self.collision_bullet()
        self.collision_with_obstacle()

    def draw(self, window):
        window.blit(self.image, self.rect)
        #pygame.draw.rect(window, gc.GREEN, self.rect, 1)