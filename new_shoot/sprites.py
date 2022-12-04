import pygame as pg
import random as ra
import os

from settings import *

#定義物件
class Player(pg.sprite.Sprite): 
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.load_img()
        self.image = pg.transform.scale(self.player_img , (50,38)) #pg.transform.scale 使傳入圖片 改變大小
        self.rect = self.image.get_rect() #物件初始位置
        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 8
        self.speedy = 8
        self.health = 100
        self.lives = 3
        self.hidden = False
        self.hide_time = 0
        self.gun = 1
        self.gun_time = 0
    
    def load_img(self):
        self.player_img = pg.image.load(os.path.join("img","player.png")).convert()
        self.player_img.set_colorkey(BLACK) #傳入RGB值 使該顏色BLACK變透明
        self.player_mini_img = pg.transform.scale(self.player_img,(25, 19))
        self.player_mini_img.set_colorkey(BLACK)
        
    def update(self):
        now = pg.time.get_ticks()
        if self.gun > 1 and now - self.gun_time > 5000:
            self.gun -= 1
            self.gun_time = now

        if self.hidden and now - self.hide_time > 1000: # 1000毫秒 = 1秒
            self.hidden = False
            self.rect.centerx = WIDTH/2
            self.rect.bottom = HEIGHT - 10
        if not(self.hidden):
            key_pressed = pg.key.get_pressed() #鍵盤上哪一個按鍵有被按下去 回傳一個布林值
            if key_pressed[pg.K_RIGHT]: #如果按右
                self.rect.x += self.speedx
            if key_pressed[pg.K_LEFT]: #如果按左
                self.rect.x -= self.speedx
            if key_pressed[pg.K_UP]: #如果按上
                self.rect.y -= self.speedy
            if key_pressed[pg.K_DOWN]: #如果按下
                self.rect.y += self.speedy
            
            if self.rect.right > WIDTH: #如果物件右邊到達邊框 則會被卡住
                self.rect.right = WIDTH
            if self.rect.left < 0: #如果物件左邊到達邊框 則會被卡住
                self.rect.left = 0
            if self.rect.bottom > HEIGHT - 10:
                self.rect.bottom = HEIGHT - 10
            if self.rect.top < 30:
                self.rect.top = 30

    def hide(self):
        self.hidden = True
        self.hide_time = pg.time.get_ticks()
        self.rect.center = (WIDTH/2, HEIGHT+500)

    def gunup(self):
        self.gun += 1
        if self.gun > 2:
            self.gun = 2
        self.time = pg.time.get_ticks()

class Rock(pg.sprite.Sprite): 
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.load_img()
        self.image_ori = ra.choice(self.rock_imgs) #從list中 隨機選取一張
        self.image_ori.set_colorkey(BLACK)
        self.image = self.image_ori.copy()
        #每一次複製 都是原本的圖片 
        self.rect = self.image.get_rect() 
        self.radius = int(self.rect.width *0.85 / 2)  #碰撞判斷半徑
        #pg.draw.circle(self.image, RED , self.rect.center , self.radius)
        self.rect.x = ra.randrange(0 , WIDTH - self.rect.width)
        self.rect.y = ra.randrange(-180 , -100) #初始生成高度
        self.speedy = ra.randrange(2 , 10)
        self.speedx = ra.randrange(-3 , 3)
        self.total_degree = 0 #一開始是0度
        self.rot_degree = ra.randrange(-3 , 3) #每次旋轉度數

    def load_img(self):
        self.rock_imgs = []
        for i in range(7):
            self.rock_imgs.append(pg.image.load(os.path.join("img",f"rock{i}.png")).convert())#自字串前面f 字串裡面就可以使用變數 

    def rotate(self): #石頭旋轉
        self.total_degree += self.rot_degree
        self.total_degree = self.total_degree % 360
        self.image = pg.transform.rotate(self.image_ori,self.total_degree) 
        #(旋轉圖片,旋轉角度) 因為每次旋轉都會疊加 所以寫每次都用原本圖片旋轉
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center
        #因為每次旋轉都會造成中心點偏移 因此要重新定位成原本的中心點

    def update(self):
        self.rotate()
        self.rect.y += self.speedy #落下速度
        self.rect.x += self.speedx #水平速度
        if self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right < 0: #如果超出視窗 則重製
            self.rect.x = ra.randrange(0 , WIDTH - self.rect.width)
            self.rect.y = ra.randrange(-180 , -100)
            self.speedy = ra.randrange(2 , 10)
            self.speedx = ra.randrange(-3 , 3)


class Bullet(pg.sprite.Sprite): 
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.load_img()
        self.image = pg.transform.scale(self.bullet_img,(10,30))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()   
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10 

    def update(self):
        self.rect.y += self.speedy #往上發射
        if self.rect.bottom < 0: #當往上跑出視窗 則刪除
            self.kill()

    def load_img(self):
        self.bullet_img = pg.image.load(os.path.join("img","bullet.png")).convert()

class Explosion(pg.sprite.Sprite):  
    def __init__(self, center, size):
        pg.sprite.Sprite.__init__(self)
        self.load_img()
        self.size = size
        self.image = self.expl_anim[self.size][0]
        self.rect = self.image.get_rect()   
        self.rect.center = center
        self.frame = 0 
        self.last_update = pg.time.get_ticks()
        self.frame_rate = 50 #每50毫秒更新

    def update(self):
        now = pg.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(self.expl_anim[self.size]):
                self.kill()
            else:
                self.image = self.expl_anim[self.size][self.frame]
                center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = center

    def load_img(self):
        self.expl_anim = {}
        self.expl_anim["lg"] = []
        self.expl_anim["sm"] = []
        self.expl_anim["player"] = []
        for i in range(9):
            expl_imgs = pg.image.load(os.path.join("img",f"expl{i}.png")).convert()
            expl_imgs.set_colorkey(BLACK)

            self.expl_anim["lg"].append(pg.transform.scale(expl_imgs,(75,75)))
            self.expl_anim["sm"].append(pg.transform.scale(expl_imgs,(30,30)))

            player_expl_imgs = pg.image.load(os.path.join("img",f"player_expl{i}.png")).convert()
            player_expl_imgs.set_colorkey(BLACK)
            self.expl_anim["player"].append(player_expl_imgs)

class Power(pg.sprite.Sprite):  
    def __init__(self, center):
        pg.sprite.Sprite.__init__(self)
        self.load_img()
        self.type = ra.choice(["shield","gun"])
        self.image = self.power_imgs[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()   
        self.rect.center = center
        self.speedy = 3

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT: 
            self.kill()
    
    def load_img(self):
        self.power_imgs = {}
        self.power_imgs["shield"] = pg.image.load(os.path.join("img","shield.png")).convert()
        self.power_imgs["gun"] = pg.image.load(os.path.join("img","gun.png")).convert()
