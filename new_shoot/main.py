import pygame as pg
import random as ra
import os

from sprites import * 
from settings import *

class Game:
    # 主要結構
    def __init__(self):
        pg.init()
        pg.mixer.init()#音效初始化 

        self.screen = pg.display.set_mode((WIDTH,HEIGHT)) #遊戲視窗大小
        pg.display.set_caption(TITLE) #設定視窗名稱
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = os.path.join(FONT)   
        self.load_data()

    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.player = Player()
        self.all_sprites.add(self.player)
        self.rocks = pg.sprite.Group() 
        self.bullets = pg.sprite.Group()
        self.powers = pg.sprite.Group()
        for i in range(ROCKNUMBER):
            self.new_rock()
        self.score = 0
        self.run()

    def run(self):
        pg.mixer.music.play(-1) #重複播放幾次 -1 = 無限
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)#這迴圈 在1秒內 最多執行 N 次 (FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        self.all_sprites.update()

        #判斷飛船和石頭相撞
        pr_hits = pg.sprite.spritecollide(self.player , self.rocks , True , pg.sprite.collide_circle) 
        #當sprite 和 群組 碰撞  群組內東西是否刪除 回傳 LIST 
        #pg.sprite.collide_circle 把矩形碰撞判斷 改成圓形 沒有第四參數 預設矩形
        for hit in pr_hits:
            self.new_rock()
            expl = Explosion(hit.rect.center,"sm")
            self.all_sprites.add(expl)
            self.player.health -= hit.radius
            if self.player.health <= 0:
                death_expl = Explosion(self.player.rect.center,"player")
                self.all_sprites.add(death_expl)
                self.die_sound.play()
                self.player.lives -= 1
                # 判斷是否生命歸0
                if self.player.lives == 0: 
                        self.playing = False
                self.player.health = 100
                self.player.hide()

    
        #判斷石頭和射擊碰撞
        rb_hits = pg.sprite.groupcollide(self.rocks ,self.bullets , True , True) 
        #當兩個群組內物件碰撞時 True=刪除 False=保留  會回傳 DICT key=rocks value=bullets
        for hit in rb_hits: 
            ra.choice(self.expls_sound).play
            self.score += 100 - hit.radius
            expl = Explosion(hit.rect.center,"lg")
            self.all_sprites.add(expl)
            if ra.random() > 0.5:
                pow = Power(hit.rect.center)
                self.all_sprites.add(pow) 
                self.powers.add(pow)
            self.new_rock()
        
        #判斷飛船和寶物相撞
        pp_hits = pg.sprite.spritecollide(self.player , self.powers , True ) 
        for hit in pp_hits:
            if hit.type == "shield":
                self.shield_sound.play()
                self.player.health += 20
                if self.player.health > 100:
                    self.player.health = 100
            if hit.type == "gun":
                self.gun_sound.play()
                self.player.gunup()  
                   
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

            elif event.type == pg.KEYDOWN: #KEYDOWN 鍵盤
                if event.key == pg.K_SPACE:  #K_SPACE 空白鍵
                    self.shoot()

        
    def draw(self):
        self.screen.fill(BLACK) #填滿顏色(R,G,B)
        self.screen.blit(self.background_img , (0,0)) #(檔案,位置) 把檔案畫入 並擺放位置 
        self.all_sprites.draw(self.screen)
        self.draw_text(self.screen, str(self.score), 18, WIDTH/2 , 10)  #把分數顯示出來
        self.draw_health(self.screen, self.player.health, 5, 15) #顯示生命條
        self.draw_lives(self.screen, self.player.lives, self.player.player_mini_img , WIDTH-100, 15 ) #顯示殘機數
        pg.display.update()
    
    #生成石頭
    def new_rock(self):
        r = Rock() 
        self.all_sprites.add(r)
        self.rocks.add(r)
    
    #射擊
    def shoot(self):
        if not(self.player.hidden):
            if self.player.gun == 1:
                self.bullet = Bullet(self.player.rect.centerx , self.player.rect.top)
                self.all_sprites.add(self.bullet)
                self.bullets.add(self.bullet)
                self.shoot_sound.play()
            elif self.player.gun >= 2:
                bullet1 = Bullet(self.player.rect.left , self.player.rect.top)
                bullet2 = Bullet(self.player.rect.right , self.player.rect.top)
                self.all_sprites.add(bullet1,bullet2) 
                self.bullets.add(bullet1,bullet2)
                self.shoot_sound.play()

    # 其他
    # 讀取檔案
    def load_data(self):
        with open("HS_FILE.txt", 'r') as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0
        #self.dir = os.path.dirname(__file__)
        #img_dir = os.path.join(self.dir,'img')
        self.background_img = pg.image.load(os.path.join("img","background.png")).convert()

        #載入背景音樂
        pg.mixer.music.load(os.path.join("sound","background.ogg"))
        pg.mixer.music.set_volume(0.3) #調整背景音量

        self.shoot_sound = pg.mixer.Sound(os.path.join("sound","shoot.wav"))
        self.gun_sound = pg.mixer.Sound(os.path.join("sound","pow1.wav"))
        self.shield_sound = pg.mixer.Sound(os.path.join("sound","pow0.wav"))
        self.die_sound = pg.mixer.Sound(os.path.join("sound","rumble.ogg"))
        self.expls_sound = [
        pg.mixer.Sound(os.path.join("sound","expl0.wav")),
        pg.mixer.Sound(os.path.join("sound","expl1.wav"))
        ]
    
    #創建 一個字體
    def draw_text(self, surf, text, size, x, y):
        font = pg.font.Font(self.font_name, size) #創建文字物件 (字體,文字大小)
        text_surface = font.render(text, True, WHITE) # 把文字渲染出來 (顯示文字,是否反鋸齒True(比較滑順),文字顏色) 
        text_rect = text_surface.get_rect() #文字定位 
        text_rect.centerx = x 
        text_rect.top = y
        surf.blit(text_surface , text_rect) #畫在哪一個平面 (文字,位置)

    #創建 生命條
    def draw_health(self, surf, hp, x, y):
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
    def draw_lives(self, surf, lives, img, x, y):
        for i in range(lives):
            img_rect = img.get_rect()
            img_rect.x = x + 33*i
            img_rect.y = y
            surf.blit(img, img_rect)
    
    #開始畫面
    def show_start_screen(self):
        pg.mixer.music.play(-1) #重複播放幾次 -1 = 無限
        self.screen.blit(self.background_img , (0,0))
        self.draw_text(self.screen, TITLE, 64, WIDTH/2, HEIGHT/4)
        self.draw_text(self.screen, "← → 移動飛船  空白鍵發射子彈", 22, WIDTH/2, HEIGHT/2)
        self.draw_text(self.screen, "按ENTER鍵 開始遊戲", 18, WIDTH/2, HEIGHT*3/4)
        pg.display.update()

        self.wait_for_key()
        pg.mixer.music.fadeout(500) 

    #結束畫面
    def show_go_screen(self):
        # game over/continue
        if not self.running: # 是否運行
            return
        
        pg.mixer.music.play(-1) #重複播放幾次 -1 = 無限
        self.screen.fill(BLACK) # 背景填充
        # 繪製文字
        self.draw_text(self.screen,"GAME OVER", 48,  WIDTH / 2, HEIGHT / 4)
        self.draw_text(self.screen,"Score: " + str(self.score), 22, WIDTH / 2, HEIGHT / 2)
        self.draw_text(self.screen,"Press Enter to play again", 22, WIDTH / 2, HEIGHT * 3 / 4)
        # 判斷分数
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text(self.screen,"NEW HIGH SCORE!", 22, WIDTH / 2, HEIGHT / 2 + 40)
            #紀錄最高分數到文件
            with open(os.path.join("HS_FILE.txt"), 'w') as f:
                f.write(str(self.score))
        else:
            self.draw_text(self.screen,"High Score: " + str(self.highscore), 22, WIDTH / 2, HEIGHT / 2 + 40)
        pg.display.flip()
        
        self.wait_for_key()
        pg.mixer.music.fadeout(500)
    
    #離開畫面
    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT: #點擊退出，结束循環
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP: 
                    if event.key == pg.K_RETURN:  #K_RETURN ENTER鍵
                        waiting = False


# 遊戲開始
g = Game()
g.show_start_screen()

while g.running:
    g.new()
    g.show_go_screen()
    
pg.quit()

    
