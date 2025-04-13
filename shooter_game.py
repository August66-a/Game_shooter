#Создай собственный Шутер!

from pygame import *
from random import randint

window = display.set_mode((1000,600))
display.set_caption('shooter')
clock = time.Clock()
fps = 80
background = transform.scale(image.load('galaxy.jpg'),(2000,1200))

class GameSprite(sprite.Sprite):
    def __init__(self,rx,ry,player_image,x,y):
        super().__init__()
        self.rx = rx
        self.ry = ry
        self.player_image = player_image
        self.image = transform.scale(image.load(player_image),(rx,ry))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))

class Player(GameSprite):
    def __init__(self,rx,ry,player_image,x,y):
        super().__init__(rx,ry,player_image,x,y)
    def move(self,code):
        if code == 'r':
            if self.rect.x < 955:
                self.rect.x += 7
        if code == 'l':
            if self.rect.x > 0:
                self.rect.x -= 7
        if code == 'up':
            if self.rect.y > 0:
                self.rect.y -= 4
        if code == 'dw':
            if self.rect.y < 530:
                self.rect.y += 4

class Enemy(GameSprite):
    def __init__(self,rx,ry,player_image,x,y,speed,code_flying):
        super().__init__(rx,ry,player_image,x,y)
        self.speed = speed
        self.code_flying = code_flying
    def move(self):
        if self.rx < 500:
            self.rx += self.speed
        if self.ry < 450:
            self.ry += self.speed
        x = self.rect.x
        y = self.rect.y
        y += self.speed
        self.image = transform.scale(image.load(self.player_image),(self.rx,self.ry))
        window.blit(self.image,(self.rect.x,self.rect.y))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def fly_asteroid(self):
        if self.code_flying == 'al':
            self.rect.x -= 1
            self.rect.y += 2
        if self.code_flying == 'ac':
            self.rect.y += 3
        if self.code_flying == 'ar':
            self.rect.x += 1
            self.rect.y += 2
        
    def boss_moving(self,code):
        if code == 'up':
            self.rect.y -= self.speed
        if code == 'down':
            self.rect.y += self.speed
        if code == 'left':
            self.rect.x -= self.speed
        if code == 'right':
            self.rect.x += self.speed


class Bullet(GameSprite):
    def __init__(self,rx,ry,player_image,x,y,type_s):
        super().__init__(rx,ry,player_image,x,y)
        self.type = type_s

    def move(self):
        self.rect.y -= 32
        if self.type == 'l':
            self.rect.x += 8
        if self.type == 'r':
            self.rect.x -= 8
        if self.type == 'c':
            self.rect.y -= 2
        if self.type == 'l' or self.type == 'r':
            if self.rx > 0:
                self.rx -= 2
            if self.ry > 0:
                self.ry -= 2
            self.image = transform.scale(image.load(self.player_image),(self.rx,self.ry))
            window.blit(self.image,(self.rect.x,self.rect.y))

        
number_l = 0
number_w = 0
player = Player(100,200,'laser_gun_1.png',0,400)
player_2 = Player(100,200,'laser_gun_2.png',900,400)
player_3 = Player(50,70,'rocket.png',450,400)
enemys = []

for i in range(4):
    e = Enemy(75,45,'ufo.png',randint(0,925),randint(0,100),randint(1,2),'e')
    enemys.insert(0,e)
    
bullets = []
font.init()
font = font.SysFont('Arial',50)
lost = font.render('Пропущено:' + str(number_l),True,(124,124,124))
wonn = font.render('Унитожено:' + str(number_w),True,(124,124,124))


bomb = Enemy(200,100,'big_bomb.png',randint(-500,1500),randint(-300,1200),10,'bom')


mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
strike = mixer.Sound('fire.ogg')

game = True
boss_1 = False
boss_2 = False
total_finish = False
wl = 'a'
move_code = -500
move_code_v = -300
code = 0
code_attack = 250
boss_hp = 20
code_strike = 0
bombing = False

while game:
    if not boss_1 and not total_finish and not boss_2:
        window.blit(background,(move_code,move_code_v))
        player.reset()
        player_2.reset()
        lost = font.render('Пропущено:' + str(number_l),True,(124,124,124))
        wonn = font.render('Унитожено:' + str(number_w),True,(124,124,124))
        window.blit(lost,(0,0))
        window.blit(wonn,(0,50))
        
        for e in enemys:
            e.move()
            e.reset()
            if e.rx >= 500:
                number_l += 1
                enemys.remove(e)
                e = Enemy(75,45,'ufo.png',randint(0,925),randint(0,100),randint(2,3),'e')
                enemys.insert(0,e)
        if number_l > 3:
            total_finish = True
            window.blit(background,(move_code,move_code_v))
            wl = 'Поражение'
            finish_font = font.render(wl,True,(124,124,124))
        
        if number_w >= 40:
            boss_1 = True
            wl = 'Босс'
            finish_font = font.render(wl,True,(255,12,14))
            for b in bullets:
                bullets.remove(b)
            enemys.clear()
            boss = Enemy(200,75,'ufo_2.png',randint(0,925),randint(0,100),2,'b')
            enemys.insert(0,boss)


        for b in bullets:
            if b.rect.y > 0:
                b.move()
                b.reset()
            elif b.rect.y <= 0:
                bullets.remove(b)
                
            for e in enemys:
                if sprite.collide_rect(b,e) and not boss_1:
                    enemys.remove(e)
                    if b in bullets:
                        bullets.remove(b)
                    number_w += 1
                    e = Enemy(75,45,'ufo.png',randint(0,925),randint(0,100),randint(1,2),'e')
                    enemys.insert(0,e)

        for e in event.get():
            if e.type == QUIT:
                game = False
            elif e.type == MOUSEBUTTONDOWN:
                if e.button == 1:
                    b = Bullet(60,80,'лазерный луч.png',68,360,'l')
                    b_2 = Bullet(60,80,'лазерный луч(1).png',880,360,'r')
                    strike.play()
                    bullets.append(b)
                    bullets.append(b_2)
        
        keys_pressed = key.get_pressed()

        if keys_pressed[K_d]:
            if move_code > - 1000:
                move_code -= 20
                for b in bullets:
                    b.rect.x -= 20
                for e in enemys:
                    e.rect.x -= 20
        
        if keys_pressed[K_a]:
            if move_code < 0:
                move_code += 20
                for b in bullets:
                    b.rect.x += 20
                for e in enemys:
                    e.rect.x += 20
    

    if boss_1:
        window.blit(background,(move_code,move_code_v))
        if code < 200:
            window.blit(finish_font,(250,100))
            code += 1
        player.reset()
        player_2.reset()
        if code >= 200:
            wonn = font.render('HP босса:' + str(boss_hp),True,(124,124,124))
            window.blit(wonn,(0,50))
            code += 1
            if code_strike > 0:
                code_strike -= 1
            for e in enemys:
                e.fly_asteroid()
                e.reset()
                if e.rect.y > 600:
                    enemys.remove(e)
                if sprite.collide_rect(e,player) or sprite.collide_rect(e,player_2):
                    boss_1 = False
                    total_finish = True
                    window.blit(background,(move_code,move_code_v))
                    wl = 'Поражение'
                    finish_font = font.render(wl,True,(124,12,12))

        if code > code_attack and code < code_attack + 100:
            wl = 'Атака босса!!!'
            finish_font = font.render(wl,True,(255,12,14))
            window.blit(finish_font,(250,100))
        
        if code == code_attack + 100:
            a1 = Enemy(75,45,'asteroid.png',boss.rect.x,boss.rect.y,randint(1,2),'al')
            a2 = Enemy(75,45,'asteroid.png',boss.rect.x,boss.rect.y,randint(1,2),'ac')
            a3 = Enemy(75,45,'asteroid.png',boss.rect.x,boss.rect.y,randint(1,2),'ar')
            enemys.append(a1)
            enemys.append(a2)
            enemys.append(a3)
            code_attack += 600


        for b in bullets:
            if b.rect.y > 0:
                b.move()
                b.reset()
            elif b.rect.y <= 0:
                bullets.remove(b)
                
            for e in enemys:
                if sprite.collide_rect(b,e):
                    if b in bullets:
                        bullets.remove(b)
                    boss_hp -= 1

        for e in event.get():
            if e.type == QUIT:
                game = False
            elif e.type == MOUSEBUTTONDOWN:
                if e.button == 1 and code_strike == 0:
                    b = Bullet(60,80,'лазерный луч.png',68,360,'l')
                    b_2 = Bullet(60,80,'лазерный луч(1).png',880,360,'r')
                    strike.play()
                    bullets.append(b)
                    bullets.append(b_2)
                    code_strike = 50

        keys_pressed = key.get_pressed()

        if keys_pressed[K_d]:
            if move_code > - 1000:
                move_code -= 20
                for b in bullets:
                    b.rect.x -= 20
                for e in enemys:
                    e.rect.x -= 20
        
        if keys_pressed[K_a]:
            if move_code < 0:
                move_code += 20
                for b in bullets:
                    b.rect.x += 20
                for e in enemys:
                    e.rect.x += 20

        if boss_hp <= 0:
            boss_1 = False
            boss_2 = True
            enemys.clear()
            enemys.append(boss)
            bullets.clear()
            boss_hp = 400
    
    if boss_2:
        window.blit(background,(move_code,move_code_v))
        wonn = font.render('HP босса:' + str(boss_hp),True,(124,124,124))
        window.blit(wonn,(0,50))
        player_3.reset()
        bomb.reset()
        for e in enemys:
            e.reset()
            if e.code_flying == 'b':

                min_amount_x = player_3.rect.x - e.rect.x
                min_amount_y = player_3.rect.y - e.rect.y
                if min_amount_x < 0:
                    min_amount_x = min_amount_x*(-1)
                if min_amount_y < 0:
                    min_amount_y = min_amount_y*(-1)
                nearest_x = player_3.rect.x
                nearest_y = player_3.rect.y


                if min_amount_x < min_amount_y:
                    if e.rect.y < nearest_y:
                        e.boss_moving('down')
                    elif e.rect.y > nearest_y:
                        e.boss_moving('up')
                if min_amount_x >= min_amount_y:
                    if e.rect.x < nearest_x:
                        e.boss_moving('right')
                    if e.rect.x >= nearest_x:
                        e.boss_moving('left')

        for b in bullets:
            b.move()
            b.reset()
            for e in enemys:
                if sprite.collide_rect(b,e):
                    bullets.remove(b)
                    boss_hp -= 1

        if sprite.collide_rect(player_3,bomb):
            bombing = True

        if bombing:

            min_amount_x = boss.rect.x - bomb.rect.x
            min_amount_y = boss.rect.y - bomb.rect.y
            if min_amount_x < 0:
                min_amount_x = min_amount_x*(-1)
            if min_amount_y < 0:
                min_amount_y = min_amount_y*(-1)
            nearest_x = boss.rect.x
            nearest_y = boss.rect.y


            if min_amount_x < min_amount_y:
                if bomb.rect.y < nearest_y:
                    bomb.boss_moving('down')
                elif bomb.rect.y > nearest_y:
                    bomb.boss_moving('up')
            if min_amount_x >= min_amount_y:
                if bomb.rect.x < nearest_x:
                    bomb.boss_moving('right')
                if bomb.rect.x >= nearest_x:
                    bomb.boss_moving('left')
        

        if sprite.collide_rect(bomb,boss) and bombing:
            bomb.rect.x = randint(0,500)
            bomb.rect.y = randint(0,300)
            boss_hp -= 30
            bombing = False
        if sprite.collide_rect(bomb,boss) and not bombing:
            bomb.rect.x = randint(-500,1500)
            bomb.rect.y = randint(-300,1200)

        if sprite.collide_rect(player_3,boss):
            boss_2 = False
            total_finish = True
            window.blit(background,(move_code,move_code_v))
            wl = 'Поражение'
            finish_font = font.render(wl,True,(124,12,12))


        for e in event.get():
            if e.type == QUIT:
                game = False
            elif e.type == MOUSEBUTTONDOWN:
                if e.button == 1:
                    b = Bullet(20,40,'лазерный луч(2).png',player_3.rect.x- 10,player_3.rect.y + 40,'c')
                    b_2 = Bullet(20,40,'лазерный луч(2).png',player_3.rect.x + 40,player_3.rect.y + 40,'c')
                    strike.play()
                    bullets.append(b)
                    bullets.append(b_2)

        
        keys_pressed = key.get_pressed()


        if keys_pressed[K_d]:
            if move_code > - 1000:
                move_code -= 20
                for b in bullets:
                    b.rect.x -= 20
                for e in enemys:
                    e.rect.x -= 20
                bomb.rect.x -= 20
            player_3.move('r')
        
        if keys_pressed[K_a]:
            if move_code < 0:
                move_code += 20
                for b in bullets:
                    b.rect.x += 20
                for e in enemys:
                    e.rect.x += 20
                bomb.rect.x += 20
            player_3.move('l')
        if keys_pressed[K_w]:
            if move_code_v < 0:
                move_code_v += 15
                for b in bullets:
                    b.rect.y += 15
                for e in enemys:
                    e.rect.y += 15
                bomb.rect.y += 15
            player_3.move('up')
        
        if keys_pressed[K_s]:
            if move_code_v > -600:
                move_code_v -= 15
                for b in bullets:
                    b.rect.y -= 15
                for e in enemys:
                    e.rect.y -= 15
                bomb.rect.y -= 15
            player_3.move('dw')
        if boss_hp <= 0:
            boss_2 = False
            enemys.clear()
            bullets.clear()
            window.blit(background,(move_code,move_code_v))
            wl = 'Победа'
            finish_font = font.render(wl,True,(12,124,12))
            total_finish = True

        
    if total_finish:
        window.blit(finish_font,(250,100))
        for e in event.get():
            if e.type == QUIT:
                game = False

    display.update()
    clock.tick(fps)