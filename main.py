from typing import Any
from pygame import *
from random import *

w , h = 700,500
window = display.set_mode((w,h))
display.set_caption("Asteroids")

game = True
finish = False
clock = time.Clock()
FPS = 60
bakground=transform.scale(image.load("galaxy.jpg") ,(w, h))

class GameSprite(sprite.Sprite):
    def __init__(self, pImage, pX, pY, sizeX, sizeY, pSpeed):
        super().__init__()
        self.image = transform.scale(image.load(pImage), (sizeX, sizeY))
        self.speed = pSpeed
        self.rect = self.image.get_rect()
        self.rect.x = pX
        self.rect.y = pY
    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y)) 

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT]:
            self.rect.x -= self.speed
        if keys[K_RIGHT]:
            self.rect.x += self.speed

    def fire (self):
        bullet = Bullet("bullet.png",self.rect.centerx-7, self.rect.top,15,30,15)
        bullets.add(bullet)

ship = Player ("rocket1.png",10,h-100,65,95,4)

lost = 0
class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        global hearts 
        if self.rect.y > h :
            try:
                # hearts.opp(Len(hearts)-1) - справа на ліво
                hearts.pop(0) # - зліва на прово
            except:
                pass
            self.rect.y = 0
            self.rect.x = randint (0, w-50)
            lost += 1

asteroids = sprite.Group()

for i in range(6):
    pics = ["asteroid.png","ufo.png"]
    asteroid = Enemy(choice(pics),randint(0,w-50),-40,50,50,randint(1,2))
    asteroids.add(asteroid)
score = 0

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0 :
            self.kill()

bullets = sprite.Group()
mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()

fire_sound = mixer.Sound("fire.ogg")
fire_sound.set_volume(0.2)

font.init()
maintfort = font.Font("Ettlora.ttf",40)

from time import time as timer
reload_time = False
num_fire = 0

hearts = []
lives = 10
hX = 300
for i in range(lives):
    heart = GameSprite("heart.png",hX,10,40,37,0)
    hearts.append(heart)
    hX += 40

restart = GameSprite("reset.png",240,200,222,125,0)
start = GameSprite("start (1).png",240,250,222,100,0)
exit = GameSprite("exit.png",5,5,60,60,0)
finish = True


while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and reload_time == False:
                    ship.fire()
                    fire_sound.play()
                    num_fire += 1 
                if num_fire >= 5 and reload_time == False:
                    reload_time = True
                    reload_start = timer()
            if e.key == K_r:
                for a in asteroids:
                    a.rect.y = -100
                    a.rect.x = randint(0, w-100)
                finish, score, lost = 0,0,0
                hearts = []
                lives = 10
                hX = 300
                for i in range(lives):
                    heart = GameSprite("heart.png", hX, 10, 40, 37, 0)
                    hearts.append(heart)
                    hX += 40

        if e.type == MOUSEBUTTONDOWN:
            if e.button == 1:
                x, y = e.pos
                if restart.rect.collidepoint(x,y):
                    for a in asteroids:
                        a.rect.y = -100
                        a.rect.x = randint(0, w-100)
                    finish, score, lost = 0,0,0
                    hearts = []
                    lives = 10
                    hX = 300
                    for i in range(lives):
                        heart = GameSprite("heart.png", hX, 10, 40, 37, 0)
                        hearts.append(heart)
                        hX += 40
                if start.rect.collidepoint(x,y):
                    finish = False
                if exit.rect.collidepoint(x,y):
                    game = False

    if finish:
         window.blit(bakground,(0 ,0))
         start.draw()
         exit.draw()

    if not finish:
        window.blit(bakground,(0,0))
        for heart in hearts :
            heart.draw()
        score_text = maintfort.render("Killed:" +str(score),True,(0,255,0))
        lost_text =  maintfort.render("Missed:"+str(lost),True,(0,255,0))
        window.blit (score_text,(5,10))
        window.blit (lost_text,(5,50))

        if reload_time:
            reload_end = timer()
            if reload_end - reload_start < 3:
                reload = maintfort.render("RELOADING...",True,(0,255,0))
                window.blit(reload,(200,200))
            else:
                num_fire = 0
                reload_time = False

        asteroids.update()
        asteroids.draw(window)
        ship.draw()
        ship.update()
        bullets.update()
        bullets.draw(window)

        if sprite.spritecollide(ship,asteroids,False):
            restart.draw()
            lose_text = maintfort.render("YOU LOST",True,(0,255,0))
            window.blit(lose_text,(200,200))
            finish = True 

        collides = sprite.groupcollide(bullets,asteroids,True,True)
        for c in collides:
            score += 1
            pics = ["asteroid.png","ufo.png"]
            asteroid = Enemy(choice(pics),randint(0,w-50), -40,50,50,randint(1,2),)
            asteroids.add(asteroid)
            

        if lost >= 10:
            restart.draw()
            lose_text = maintfort.render ("YOU LOSE",True,(0,255,0))
            window.blit(lose_text,(200,200))
            finish =True

        for heart in hearts:
            
            heart.draw()

    display.update()
    clock.tick(60)