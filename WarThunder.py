from pygame import *
from random import randint
from time import time as timer

class Celestial(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y)) #картинка
        self.speed = speed #скорость

        #хит-бокс
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class SpaceShip(Celestial):
    def move(self):
        action = key.get_pressed()
        if action[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        elif action[K_d] and self.rect.x < 1100:
            self.rect.x += self.speed
    
    def fire(self):
        bullet = Bullet("laxer.png", self.rect.centerx, self.rect.top, 10, 20, -30)
        bullets.add(bullet)

missed_enemy = 0
score = 0
win_score = 10
lose_score = 3
width = 1200
height = 700

class Enemy(Celestial):
    def update(self):
        global missed_enemy
        self.rect.y += self.speed
        if self.rect.y >= 700:
            self.rect.y = 0
            self.rect.x = randint(0, width-100)
            self.speed = randint(4, 8)
            missed_enemy += 1

class Bullet(Celestial):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y <= 0:
            self.kill()


bullets = sprite.Group()

window = display.set_mode((width, height))
display.set_caption("War Thunder 3")
background = transform.scale(image.load("space.jpg"), (width, height))

mixer.init()
mixer.music.load("space.mp3")
mixer.music.play()
shoot = mixer.Sound("shoot.ogg")
font.init()
font2 = font.SysFont("Arial", 40) #None -> "Arial"
font1 = font.SysFont("Arial", 100)
win = font1.render("ПОБЕДА", True, (0, 0, 250))
lose =  font1.render("ПОРАЖЕНИЕ", True, (0,0,0))
crash = font1.render("Столкновение", True, (255, 0, 0))

player = SpaceShip("ship.png", 600, 570, 100, 100, 25)
aliens = sprite.Group()
for i in range(5):
    alien = Enemy('alien.png', randint(0, width - 100), -50, 60, 60, randint(4, 7)) 
    aliens.add(alien)

asteroids = sprite.Group()
for i in range(3):
    aster = Enemy("asteroid.png", randint(0, width - 100), -50, 100, 100, randint(1, 4)) 
    asteroids.add(aster)

reload_capacity = False
count_fire = 0
hp = 3
lose_score = 3
game = True
run = True
while game == True:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if count_fire < 8 and reload_capacity == False:
                    count_fire += 1
                    player.fire()
                    shoot.play()
                elif count_fire >= 8 and reload_capacity == False:
                    reload_time = timer()
                    reload_capacity = True

    if run == True:           
        window.blit(background, (0, 0))
        player.reset()
        player.move()
        aliens.update()
        aliens.draw(window)
        bullets.update()
        bullets.draw(window)
        asteroids.update()
        asteroids.draw(window)

        if reload_capacity == True:
            temp_time = timer()
            if temp_time - reload_time < 2:
                rel_text = font2.render("Перезарядка орудия...", True, (255,255,255))
                window.blit(rel_text, (400, 650))
            else:
                count_fire = 0
                reload_capacity = False

        collides = sprite.groupcollide(aliens, bullets, True, True)
        for i in collides:
            score += 1
            alien = Enemy('alien.png', randint(0, width - 100), -50, 80, 80, randint(4, 8)) 
            aliens.add(alien)
        
        if sprite.spritecollide(player, aliens, False) or sprite.spritecollide(player, asteroids, False):
            sprite.spritecollide(player, aliens, True)
            sprite.spritecollide(player, asteroids, True)
            hp -= 1

        if hp == 0 or missed_enemy >= lose_score:
            run = False
            window.blit(lose, (500, 300)) 

        if score >= win_score:
            run = False
            window.blit(win, (500, 300))          

        text = font2.render("Счет: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))
        text_lose = font2.render("Пропущено: " + str(missed_enemy), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))
        text_life = font2.render("Кол-во жизней " + str(hp), True, (62, 161, 237))
        window.blit(text_life, (10, 80))      
    display.update()

    time.delay(60)
