#Создай собственный Шутер!

from pygame import *
from random import randint
class GameSprite(sprite.Sprite):
    #конструктор класса
    def __init__(self, player_image, player_x, player_y, x, y, player_speed):
        super().__init__()
 
        # каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image), (x, y))
        self.speed = player_speed
 
        # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

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
            bullet = Bullet('bullet.png', self.rect.centerx - 30, self.rect.top, 40, 40, 3 )
            bullets.add(bullet)
            count = -15
            if bonus != 0:
                for i in range(1, randint(1,6)):
                    bullet = Bullet('bullet.png', self.rect.centerx - count, self.rect.top, 40, 40, 3 )
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
#Персонажи
Starship = Player('rocket.png', 350, 420, 80, 80, 5 )
monsters = sprite.Group()
for i in range(1,6):
    monster = Enemy('ufo.png', randint(5, win_width - 80), 20, randint(60, 80),randint(30, 50), 1)
    monsters.add(monster)

bullets = sprite.Group()

asteroids = sprite.Group()
for i in range(1,3):
    rock = Asteroid('asteroid.png', randint(5, win_width - 80), 20,randint(30, 50),randint(10, 30), 1)
    asteroids.add(rock)

#Музыка
mixer.init()
mixer.music.load('space.ogg')
Space = mixer.Sound('space.ogg')
Space.set_volume(0.2)
Space.play()
fire = mixer.Sound('fire.ogg')
fire.set_volume(0.2)


while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire.play()
                Starship.fire()
                if col_bul != 0:
                    col_bul -= 1
                
                


    if finish != True:
        window.blit(background,(0, 0))
        Starship.update()
        monsters.update()
        bullets.update()
        asteroids.update()
        
        Starship.reset()
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)
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
        monster = Enemy('ufo.png', randint(5, win_width - 80), 20, randint(60, 80),randint(30, 50), 1)
        monsters.add(monster)
    
    colides = sprite.groupcollide(asteroids, bullets, True, True)
    for c in colides:
        score += 2
        rock = Asteroid('asteroid.png', randint(5, win_width - 80), 20, randint(30, 50),randint(10, 30), 1)
        asteroids.add(rock)
    
    if sprite.spritecollide(Starship, monsters, False) or lost >= max_lost:
        finish = True
        lose = font1.render("Вы проиграли!", 1 , (100, 100, 189))
        window.blit(lose, (200,200))
    if score >= goal:
        finish = True
        win = font1.render("Вы победили!", 1 , (0, 200, 189))
        window.blit(win, (200,200))
    if sprite.spritecollide(Starship, asteroids, True):
        bonus = 1






    display.update()
    clock.tick(FPS)
