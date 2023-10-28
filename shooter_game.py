#Создай собственный Шутер!

from pygame import *
from random import randint
class GameSprite(sprite.Sprite):
    #конструктор класса
    def __init__(self, player_image, player_x, player_y, x, y, player_speed, sk_y):
        super().__init__()
 
        # каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image), (x, y))
        self.speed = player_speed
 
        # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.sk_y = sk_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))




class Player(GameSprite):
    def update(self):
        global col_bul
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[K_w] and self.rect.y > 15:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_height - 80:
            self.rect.y += self.speed
        if keys[K_r] and col_bul == 0:
            col_bul = 15

    def fire(self):
        if col_bul != 0:
            bullet = Bullet('bullet.png', self.rect.centerx - 30, self.rect.top, 40, 40, 3, 0 )
            bullets.add(bullet)
            count = -15
            if bonus != 0:
                for i in range(1, randint(1,6)):
                    bullet = Bullet('bullet.png', self.rect.centerx - count, self.rect.top, 40, 40, 3, 0 )
                    bullets.add(bullet)
                    count += 15

lost = 0
score = 0
bonus = 0
col_bul = 15


class Enemy(GameSprite):
    def update(self):
            self.rect.y += self.speed
            global lost
            if self.rect.y > win_height - 20:
                self.rect.x = randint(80, win_width - 80)
                self.rect.y = 0
                lost += 1

class Asteroid(GameSprite):
    def update(self):
            self.rect.y += self.speed
            if self.rect.y > win_height - 20:
                self.rect.x = randint(80, win_width - 80)
                self.rect.y = 0

class MiniBoss(GameSprite):
    def update(self):
            self.rect.y += self.sk_y
            self.rect.x += self.speed
            global lost
            if self.rect.y > win_height - 20:
                self.rect.x = randint(200, 720)
                self.rect.y = 0
                lost += 2
                self.kill()
            if self.rect.x >= 800:
                self.speed = -1 * self.speed
            elif self.rect.x <= 100:
                self.speed = -1 * self.speed

class Killer(GameSprite):
    def update(self):
        if self.rect.y < Starship.rect.y:
            self.rect.y += self.sk
        elif self.rect.y > Starship.rect.y:
            self.rect.y -= self.sk
        if self.rect.x > Starship.rect.x:
            self.rect.x -= self.speed
        if self.rect.x < Starship.rect.x:
            self.rect.x += self.speed




class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
    
        if self.rect.y < 5:
            self.kill()


font.init()
font1 = font.SysFont("Arial", 80)
font2 = font.SysFont("Arial", 36)


win_width = 1200
win_height = 800
window = display.set_mode((win_width, win_height))
display.set_caption("Шутер")
background = transform.scale(image.load("galaxy.jpg"), (win_width, win_height))

run = True
finish = False
clock = time.Clock()
FPS = 60
max_lost = 3
goal = 1000
goal_score = 10
bad_luck = 10
puli = 0

#Персонажи
Starship = Player('rocket.png', 350, 420, 80, 80, 5, 0 )
Killer = Killer('rocket.png', 350, 20, 60, 60, 5, 1 )
monsters = sprite.Group()
for i in range(1,6):
    monster = Enemy('ufo.png', randint(5, win_width - 80), 20, randint(60, 80),randint(30, 50), 1, 0)
    monsters.add(monster)

bullets = sprite.Group()

asteroids = sprite.Group()
for i in range(1,3):
    rock = Enemy('asteroid.png', randint(5, win_width - 80), 20,randint(30, 50),randint(10, 30), 1, 0)
    asteroids.add(rock)

stars = sprite.Group()
for i in range(1,3):
    star = Asteroid('star.png', randint(5, win_width - 80), 20 ,randint(40, 50),randint(20, 30), 1, 0,)
    stars.add(star)

minibosses = sprite.Group()
#Музыка
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire = mixer.Sound('fire.ogg')



while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                Starship.fire()
                if col_bul != 0:
                    col_bul -= 1
                if bonus == 1:
                    puli -= 1
                    if puli == 0:
                        bonus = 0
                
                


    if finish != True:
        window.blit(background,(0, 0))
        Starship.update()
        minibosses.update()
        Killer.update()
        monsters.update()
        bullets.update()
        asteroids.update()
        stars.update()
        
        Starship.reset()
        Killer.reset()
        minibosses.draw(window)
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)
        stars.draw(window)

        if lost == 0:
            color = (200, 200, 200)
        elif lost == 1:
            color = (0, 200, 200)
        elif lost == 2:
            color = (200, 0, 0)

        text = font2.render('Счёт: ' + str(score), 1, (200, 200, 200))
        window.blit(text, (5, 10))
        text_lose = font2.render("Пропущено: " + str(lost), 1, color)
        window.blit(text_lose, (5, 30))
        text_bul = font2.render("Патронов: " + str(col_bul), 1, color)
        window.blit(text_bul, (5, 50))
        


    colides = sprite.groupcollide(monsters, bullets, True, True)
    for c in colides:
        score += 1
        monster = Enemy('ufo.png', randint(5, win_width - 80), 20, randint(60, 80),randint(30, 50), 1, 0)
        monsters.add(monster)

    colides = sprite.groupcollide(minibosses, bullets, True, True)
    for c in colides:
        score += 10

    
    colides = sprite.groupcollide(asteroids, bullets, True, True)
    for c in colides:
        score += 2
        rock = Asteroid('asteroid.png', randint(5, win_width - 80), 20, randint(30, 50),randint(10, 30), 1, 0)
        asteroids.add(rock)

    colides = sprite.groupcollide(stars, bullets, True, True)
    
    if sprite.spritecollide(Starship, monsters, False) or lost >= max_lost or sprite.spritecollide(Starship, asteroids, False):
        finish = True
        lose = font1.render("Вы проиграли!", 1 , (100, 100, 189))
        window.blit(lose, (200,200))

    if score >= goal:
        finish = True
        win = font1.render("Вы победили!", 1 , (0, 200, 189))
        window.blit(win, (200,200))

    if sprite.spritecollide(Starship, stars, True):
        bonus = 1
        puli = 15

    if score >= goal_score:
        star = Asteroid('star.png', randint(5, win_width - 80), 20 ,randint(40, 50),randint(20, 30), 1, 0)
        stars.add(star)
        goal_score += 10

    if score >= bad_luck:
        miniboss = MiniBoss("kil.png", randint(200, 790), 20, 80, 80, 1, 1)
        minibosses.add(miniboss)
        bad_luck += 100




    display.update()
    clock.tick(FPS)