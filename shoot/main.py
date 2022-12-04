import pygame as pg
import random as ra
import os

FPS = 60
WIDTH = 500
HEIGHT = 600

#顏色
BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,255,0)
RED = (255,0,0)
YELLOW = (255,255,0)

# 遊戲初始化 創建視窗
pg.init() #初始化
pg.mixer.init() #音效初始化 
screen = pg.display.set_mode((WIDTH,HEIGHT)) #遊戲視窗大小
pg.display.set_caption("視窗名稱") #設定視窗名稱
clock = pg.time.Clock() 

#載入圖片 需要先進行初始化
background_img = pg.image.load(os.path.join("img","background.png")).convert() 
#讀取該檔案資料結內的img資料截內background.png檔案  並轉換成pythonm用格式( .convert() )

#載入飛船圖片
player_img = pg.image.load(os.path.join("img","player.png")).convert()
player_img.set_colorkey(BLACK) #傳入RGB值 使該顏色BLACK變透明
player_mini_img = pg.transform.scale(player_img,(25, 19))
player_mini_img.set_colorkey(BLACK)
pg.display.set_icon(player_mini_img) #設定icon圖片
#載入子彈圖片
bullet_img = pg.image.load(os.path.join("img","bullet.png")).convert()
#載入石頭圖片
rock_imgs = []
for i in range(7):
    rock_imgs.append(pg.image.load(os.path.join("img",f"rock{i}.png")).convert())#自字串前面f 字串裡面就可以使用變數
#載入爆炸圖片
expl_anim = {}
expl_anim["lg"] = []
expl_anim["sm"] = []
expl_anim["player"] = []
for i in range(9):
    expl_imgs = pg.image.load(os.path.join("img",f"expl{i}.png")).convert()
    expl_imgs.set_colorkey(BLACK)
    expl_anim["lg"].append(pg.transform.scale(expl_imgs,(75,75)))
    expl_anim["sm"].append(pg.transform.scale(expl_imgs,(30,30)))
    player_expl_imgs = pg.image.load(os.path.join("img",f"player_expl{i}.png")).convert()
    player_expl_imgs.set_colorkey(BLACK)
    expl_anim["player"].append(player_expl_imgs)
#調寶圖片
power_imgs = {}
power_imgs["shield"] = pg.image.load(os.path.join("img","shield.png")).convert()
power_imgs["gun"] = pg.image.load(os.path.join("img","gun.png")).convert()

#載入背景音樂
pg.mixer.music.load(os.path.join("sound","background.ogg"))
pg.mixer.music.set_volume(0.3) #調整背景音量
#載入音校
shoot_sound = pg.mixer.Sound(os.path.join("sound","shoot.wav"))
gun_sound = pg.mixer.Sound(os.path.join("sound","pow1.wav"))
shield_sound = pg.mixer.Sound(os.path.join("sound","pow0.wav"))
die_sound = pg.mixer.Sound(os.path.join("sound","rumble.ogg"))
expls_sound = [
    pg.mixer.Sound(os.path.join("sound","expl0.wav")),
    pg.mixer.Sound(os.path.join("sound","expl1.wav"))
]

#載入字體
font_name = os.path.join("font.ttf")
#創建 一個字體
def draw_text(surf, text, size, x, y):  
    font = pg.font.Font(font_name, size) #創建文字物件 (字體,文字大小)
    text_surface = font.render(text, True, WHITE) # 把文字渲染出來 (顯示文字,是否反鋸齒True(比較滑順),文字顏色) 
    text_rect = text_surface.get_rect() #文字定位 
    text_rect.centerx = x 
    text_rect.top = y
    surf.blit(text_surface , text_rect) #畫在哪一個平面 (文字,位置)
#初始畫面
def draw_init():
    screen.blit(background_img , (0,0))
    draw_text(screen, "遊戲名稱", 64, WIDTH/2, HEIGHT/4)
    draw_text(screen, "← → 移動飛船 空白鍵發射子彈", 22, WIDTH/2, HEIGHT/2)
    draw_text(screen, "按任意鍵 開始遊戲", 18, WIDTH/2, HEIGHT*3/4)
    pg.display.update()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pg.event.get(): 
            if event.type == pg.QUIT:
                pg.quit()
                return True
            elif event.type == pg.KEYUP: 
                waiting = False 
                return False
#創建 生命條
def draw_health(surf, hp, x, y):
    if hp < 0:
        hp = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (hp/100)*BAR_LENGTH
    #條滿多少
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    #生命條外框
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    #生命條
    pg.draw.rect(surf, GREEN, fill_rect)
    #畫生命條 無第四參數 填滿矩形
    pg.draw.rect(surf, WHITE, outline_rect, 2)
    #畫外框 有第四參數 外框矩形
#創建 殘機數
def draw_lives(surf, lives, img, x, y):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 33*i
        img_rect.y = y
        surf.blit(img, img_rect)
#生成石頭
def new_rock(): #生成石頭 並重新加入群組
    r = Rock() 
    all_sprites.add(r)
    rocks.add(r) 

#定義物件
class Player(pg.sprite.Sprite): 
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        """
        self.image = pg.Surface((50,40)) 一個平面pg.Surface 大小(50,40)
        self.image.fill(GREEN) 物件顏色 """
        self.image = pg.transform.scale(player_img , (50,38)) #pg.transform.scale 使傳入圖片 改變大小
        self.rect = self.image.get_rect() #物件初始位置
        self.radius = 20 #碰撞判斷半徑 圓心是中心點
        #pg.draw.circle(self.image, RED , self.rect .center , self.radius) 碰撞圓形位置
        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 8
        self.health = 100
        self.lives = 3
        self.hidden = False
        self.hide_time = 0
        self.gun = 1
        self.gun_time = 0

    def update(self):
        now = pg.time.get_ticks()
        if self.gun > 1 and now - self.gun_time > 5000:
            self.gun -= 1
            self.gun_time = now

        if self.hidden and now - self.hide_time > 1000: # 1000毫秒 = 1秒
            self.hidden = False
            self.rect.centerx = WIDTH/2
            self.rect.bottom = HEIGHT - 10

        key_pressed = pg.key.get_pressed() #鍵盤上哪一個按鍵有被按下去 回傳一個布林值
        if key_pressed[pg.K_RIGHT]: #如果按右
            self.rect.x += self.speedx
        if key_pressed[pg.K_LEFT]: #如果按左
            self.rect.x -= self.speedx
        
        if self.rect.right > WIDTH: #如果物件右邊到達邊框 則會被卡住
            self.rect.right = WIDTH
        if self.rect.left < 0: #如果物件左邊到達邊框 則會被卡住
            self.rect.left = 0
    
    def shoot(self):
        if not(self.hidden):
            if self.gun == 1:
                bullet = Bullet(self.rect.centerx , self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()
            elif self.gun >= 2:
                bullet1 = Bullet(self.rect.left , self.rect.top)
                bullet2 = Bullet(self.rect.right , self.rect.top)
                all_sprites.add(bullet1,bullet2)
                bullets.add(bullet1,bullet2)
                shoot_sound.play()
            
        
    def hide(self):
        self.hidden = True
        self.hide_time = pg.time.get_ticks()
        self.rect.center = (WIDTH/2, HEIGHT+500)

    def gunup(self):
        self.gun += 1
        self.time = pg.time.get_ticks()

        """
        if self.rect.left > WIDTH : #如果物件的左邊位置 > WIDTH
            self.rect.right = 0  #物件右邊位置變成0
        讓物件從右邊跑出去 會 重新從左邊進來
        """

class Rock(pg.sprite.Sprite): 
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image_ori = ra.choice(rock_imgs) #從list中 隨機選取一張
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
        self.image = pg.transform.scale(bullet_img,(10,30))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()   
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10 

    def update(self):
        self.rect.y += self.speedy #往上發射
        if self.rect.bottom < 0: #當往上跑出視窗 則刪除
            self.kill()
             
class Explosion(pg.sprite.Sprite):  
    def __init__(self, center, size):
        pg.sprite.Sprite.__init__(self)
        self.size = size
        self.image = expl_anim[self.size][0]
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
            if self.frame == len(expl_anim[self.size]):
                self.kill()
            else:
                self.image = expl_anim[self.size][self.frame]
                center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = center
            
class Power(pg.sprite.Sprite):  
    def __init__(self, center):
        pg.sprite.Sprite.__init__(self)
        self.type = ra.choice(["shield","gun"])
        self.image = power_imgs[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()   
        self.rect.center = center
        self.speedy = 3

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT: 
            self.kill()

#播放背景音樂
pg.mixer.music.play(-1) #重複播放幾次 -1 = 無限

#遊戲迴圈
show_init = True
running = True
while running:
    if show_init == True:
        close = draw_init()
        if close:
            break
        show_init = False
        #創建sprite群組 
        all_sprites = pg.sprite.Group() 
        rocks = pg.sprite.Group() 
        bullets = pg.sprite.Group()
        powers = pg.sprite.Group()  
        #加入群組
        player = Player()
        all_sprites.add(player) 
        for i in range(8):
            new_rock()
        #起始分數
        score = 0 
    
    clock.tick(FPS) #這迴圈 在1秒內 最多執行 N 次 (FPS)
    # 取得輸入
    for event in pg.event.get(): 
        if event.type == pg.QUIT:
            running = False
            #如果點右上叉叉 則結束迴圈 關閉視窗
        elif event.type == pg.KEYDOWN: #KEYDOWN 鍵盤
            if event.key == pg.K_SPACE:  #K_SPACE 空白鍵
                player.shoot()

    # 更新遊戲
    all_sprites.update() #執行群組內每一個物件update函數
    
    #判斷石頭和射擊碰撞
    hits = pg.sprite.groupcollide(rocks ,bullets , True , True) 
    #當兩個群組內物件碰撞時 True=刪除 False=保留  會回傳 DICT key=rocks value=bullets
    for hit in hits: 
        ra.choice(expls_sound).play
        score += 100 - hit.radius
        expl = Explosion(hit.rect.center,"lg")
        all_sprites.add(expl)
        if ra.random() > 0.5:
            pow = Power(hit.rect.center)
            all_sprites.add(pow) 
            powers.add(pow)
        new_rock()

    #判斷飛船和石頭相撞
    hits = pg.sprite.spritecollide(player , rocks , True , pg.sprite.collide_circle) 
    #當sprite 和 群組 碰撞  群組內東西是否刪除 回傳 LIST 
    #pg.sprite.collide_circle 把矩形碰撞判斷 改成圓形 沒有第四參數 預設矩形
    for hit in hits:
        new_rock()
        expl = Explosion(hit.rect.center,"sm")
        all_sprites.add(expl)
        player.health -= hit.radius
        if player.health <= 0:
            death_expl = Explosion(player.rect.center,"player")
            all_sprites.add(death_expl)
            die_sound.play()
            player.lives -= 1
            player.health = 100
            player.hide()
    
    #判斷飛船和寶物相撞
    hits = pg.sprite.spritecollide(player , powers , True ) 
    for hit in hits:
        if hit.type == "shield":
            shield_sound.play()
            player.health += 20
            if player.health > 100:
                player.health = 100
        if hit.type == "gun":
            gun_sound.play()
            player.gunup()
        
    
    if player.lives == 0 and not(death_expl.alive()): #.alive 判斷是否存在
        show_init = True

    # 畫面顯示
    screen.fill(BLACK) #填滿顏色(R,G,B)
    screen.blit(background_img , (0,0)) #(檔案,位置) 把檔案畫入 並擺放位置 
    all_sprites.draw(screen) #把群組中的東西 畫到 screen上面
    draw_text(screen, str(score), 18, WIDTH/2 , 10)  #把分數顯示出來
    draw_health(screen, player.health, 5 , 15) #顯示生命條
    draw_lives(screen, player.lives, player_mini_img , WIDTH-100, 15 ) #顯示殘機數
    pg.display.update()

pg.quit()