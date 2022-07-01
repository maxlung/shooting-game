
import pygame
import random
import os
FPS=60
WHITE=(255,255,255)
GREEN=(0,255,0)
RED=(255,0,0)
YELLOW=(255,255,0)
BLACK=(0,0,0)
WIDTH=500
HEIGHT=600
rock_num = 20
last_game_score = 0
highest_score = 0
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("OnlyMyRailGun")
clock = pygame.time.Clock()


background_img = pygame.image.load(os.path.join("img","background.jpg")).convert()
background2_img = pygame.image.load(os.path.join("img","background2.jpg")).convert()
player_img = pygame.image.load(os.path.join("img","q2.png")).convert()
player_mini_img = pygame.transform.scale(player_img,(24, 34))
player_mini_img.set_colorkey(BLACK)
icon_img = pygame.image.load(os.path.join("img","icon1.jpg")).convert()
icon_mini_img = pygame.transform.scale(icon_img,(34, 34))
pygame.display.set_icon(icon_mini_img)
#rock_img = pygame.image.load(os.path.join("img","rock.png")).convert()
bullet_img = pygame.image.load(os.path.join("img","coin.png")).convert()

power_imgs = {}
img_shield = pygame.image.load(os.path.join("img","shield.png")).convert()
img_gun = pygame.image.load(os.path.join("img","gun.png")).convert()
img_star = pygame.image.load(os.path.join("img","star.png")).convert()
power_imgs['shield'] = pygame.transform.scale(img_shield, (30, 30))
power_imgs['gun'] = pygame.transform.scale(img_gun, (40, 40))
power_imgs['star'] =pygame.transform.scale(img_star, (30, 30))

rock_imgs = []
for i in range(7):
    rock_imgs.append(pygame.image.load(os.path.join("img", "rock%s.png"%i)).convert())

expl_anim = {}
expl_anim['lg'] = []
expl_anim['sm'] = []
expl_anim['player'] = []
for i in range(9):
    expl_img = pygame.image.load(os.path.join("img","expl%s.png"%i)).convert()
    expl_img.set_colorkey(BLACK)
    expl_anim['lg'].append(pygame.transform.scale(expl_img, (75, 75)))
    expl_anim['sm'].append(pygame.transform.scale(expl_img, (30, 30)))
    player_expl_img = pygame.image.load(os.path.join("img","player_expl%s.png"%i)).convert()
    player_expl_img.set_colorkey(BLACK)
    expl_anim['player'].append(player_expl_img)


shoot_sound = pygame.mixer.Sound(os.path.join("sound","shoot.wav"))
shoot_sound.set_volume(0.3)
expl1 = pygame.mixer.Sound(os.path.join("sound","expl0.wav"))
expl1.set_volume(0.3)
expl2 = pygame.mixer.Sound(os.path.join("sound","expl1.wav"))
expl2.set_volume(0.3)
expl_sounds = [expl1,expl2]

gun_sound = pygame.mixer.Sound(os.path.join("sound2","magase.wav")) 
shield_sound = pygame.mixer.Sound(os.path.join("sound2","yoroshiku.wav"))
star_sound = pygame.mixer.Sound(os.path.join("sound2","sasuga.wav"))
gun_sound.set_volume(0.3)
shield_sound.set_volume(0.3)
star_sound.set_volume(0.3)

die_sound1 = pygame.mixer.Sound(os.path.join("sound2","daijuobu.wav"))
die_sound1.set_volume(0.3)
die_sound2 = pygame.mixer.Sound(os.path.join("sound2","ganbade.wav"))
die_sound2.set_volume(0.3)
die_sound3 = pygame.mixer.Sound(os.path.join("sound2","gomen.wav"))
die_sound3.set_volume(0.3)
die_sounds = [die_sound1, die_sound2, die_sound3]

pygame.mixer.music.load(os.path.join("sound","background.wav"))
pygame.mixer.music.set_volume(0.7)

font_name = os.path.join("font1.ttf")
def new_rock():
    rock = Rock()
    all_sprites.add(rock)
    rocks.add(rock)

def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, RED)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)

def draw_health(surf, hp, x, y):
    if hp <0:
        hp = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (hp/100)*BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)
    
def draw_lifes(surf, lifes, img, x, y):
    for i in range(lifes):
        img_rect = img.get_rect()
        img_rect.x = x + 30*i
        img_rect.y = y
        surf.blit(img, img_rect)

def draw_init():
    screen.blit(background2_img, (0,0))
    draw_text(screen, '某科學的超生存戰!(困難)', 42, WIDTH/2, HEIGHT/4)
    draw_text(screen, 'A,D操控美琴  空白鍵發射電磁砲', 22, WIDTH/2, HEIGHT/2)
    draw_text(screen, '上一場遊戲分數:%s'%last_game_score, 22, WIDTH/2, 330)
    draw_text(screen, '本次遊玩最高分:%s'%highest_score, 22, WIDTH/2, 360)
    draw_text(screen, '按任意鍵遊玩!', 18, WIDTH/2, HEIGHT*3/4)
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type== pygame.QUIT:
                pygame.QUIT()
                return True
            elif event.type== pygame.KEYDOWN:
                waiting = False
                return False
class Player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #why
        self.image = pygame.transform.scale(player_img,(48,69) )
        self.image.set_colorkey(BLACK)
        self.rect=self.image.get_rect()
        self.radius = 22
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 8
        self.health = 100
        self.lifes = 3
        self.hidden = False
        self.hide_time = 0
        self.gun = 1
        self.gun_time = 0
        self.gunsp = 1
        self.gunsp_time = 0
        self.shooting = False
        self.shoot_time = 0


    def update(self):
        now = pygame.time.get_ticks()
        if self.gun > 1 and now - self.gun_time > 5000:
            self.gun -=1
            self.gun_time = 0
        if self.gunsp > 1 and now - self.gunsp_time > 5000:
            self.gunsp -=1
            self.gunsp_time = 0
        if self.hidden and now - self.hide_time >1000:
            self.hidden = False
            self.rect.centerx = WIDTH/2
            self.rect.bottom = HEIGHT - 10
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_d]: 
            self.rect.x+=self.speedx
        if key_pressed[pygame.K_a]: 
            self.rect.x-= self.speedx
        
        if self.rect.right > WIDTH :
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        
        if self.shooting and self.gunsp ==1 :
            if now - self.shoot_time >= 200 :
                self.shoot()
        elif self.shooting and self.gunsp >=2 :
            if now - self.shoot_time >= 100 :
                self.shoot()
            
    def shoot(self):
        if not(self.hidden):
            if self.gun == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()
                self.shoot_time = pygame.time.get_ticks()
            elif self.gun >=2:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shoot_sound.play()
                self.shoot_time = pygame.time.get_ticks()    
    
    def hide(self):
        self.hidden = True
        self.hide_time = pygame.time.get_ticks()
        self.rect.center = (WIDTH/2, HEIGHT+500)
    def gunup(self):
        self.gun += 1
        self.gun_time = pygame.time.get_ticks()
    def gunspup(self):
        self.gunsp += 1
        self.gunsp_time = pygame.time.get_ticks()

        
class Rock(pygame.sprite.Sprite):
    def __init__(self): 
        pygame.sprite.Sprite.__init__(self) #why 
        self.image_ori = random.choice(rock_imgs)
        self.image_ori.set_colorkey(BLACK)
        self.image = self.image_ori.copy()
        self.rect=self.image.get_rect()
        self.radius = int(self.rect.width/2)
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = random.randrange(0,WIDTH - self.rect.width)
        self.rect.bottom = random.randrange(-180,-100)
        self.speedy = random.randrange(2, 10)
        self.speedx = random.randrange(-3, 3)
        self.total_degree = 0
        self.rot_degree = random.randrange(-3,3)

    def rotate(self):
        self.total_degree += self.rot_degree
        self.total_degree = self.total_degree % 360
        self.image =  pygame.transform.rotate(self.image_ori, self.total_degree)
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center
    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT or self.rect.left> WIDTH or self.rect.right<0:
            self.rect.centerx = random.randrange(0,WIDTH - self.rect.width)
            self.rect.bottom = random.randrange(-100,-40)
            self.speedy = random.randrange(2, 10)
            self.speedx = random.randrange(-3, 3)

class Bullet(pygame.sprite.Sprite): 
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self) 
        self.image = pygame.transform.scale(bullet_img,(20,20))
        self.image.set_colorkey(BLACK)
        self.rect=self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

class Explosion(pygame.sprite.Sprite): 
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self) 
        self.size = size
        self.image = expl_anim[self.size][0]
        self.rect=self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now -self.last_update > self.frame_rate:
            self.last_update =now
            self.frame += 1
            if self.frame == len(expl_anim[self.size]):
                self.kill()
            else:
                self.image = expl_anim[self.size][self.frame] #why
                center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = center

class Power(pygame.sprite.Sprite): 
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun', 'star']) 
        self.image = power_imgs[self.type]
        self.image.set_colorkey(BLACK)
        self.rect=self.image.get_rect()
        self.rect.center = center
        self.speedy = 3

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()

all_sprites = pygame.sprite.Group()
rocks = pygame.sprite.Group()
bullets = pygame.sprite.Group()
powers = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
score = 0
for i in range(rock_num):
    new_rock()
pygame.mixer.music.play(-1)

show_init = True
running=True
while running :
    if show_init:
        close = draw_init()
        if close:
            break
        show_init = False
    clock.tick(FPS)
    #取得輸入
    for event in pygame.event.get():
        if event.type== pygame.QUIT:
            running=False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shooting = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                player.shooting = False
        



  #遊戲更新
    all_sprites.update()
    hits = pygame.sprite.groupcollide(rocks, bullets, True, True)
    for hit in hits:
        random.choice(expl_sounds).play()
        score += hit.radius
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        if random.random()> 0.97:
            pow =Power(hit.rect.center)
            all_sprites.add(pow)
            powers.add(pow)
        new_rock()
    
    hits = pygame.sprite.spritecollide(player, rocks, True, pygame.sprite.collide_circle) #????????????
    for hit in hits:
        new_rock()
        player.health -= hit.radius
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        if player.health <=0:
            death_expl = Explosion(player.rect.center, 'player')
            all_sprites.add(death_expl)
            random.choice(die_sounds).play()
            player.lifes -= 1
            player.health = 100
            player.hide()

    
    hits = pygame.sprite.spritecollide(player, powers, True)       
    for hit in hits:
        if hit.type == 'shield':
            player.health += 20
            shield_sound.play() 
            if player.health > 100:
                player.health = 100

        elif hit.type == 'gun':
            player.gunup()
            gun_sound.play()
        elif hit.type == 'star':
            player.gunspup()
            gun_sound.play()
    if player.lifes == 0 and not(death_expl.alive()):
        last_game_score=score
        if last_game_score > highest_score:
            highest_score = last_game_score
        show_init = True
        all_sprites = pygame.sprite.Group()
        rocks = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powers = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        score = 0
        for i in range(rock_num):
            new_rock()
    #畫面顯示
    screen.fill(BLACK)
    screen.blit(background_img, (0,0))
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH/2, 10)
    draw_health(screen, player.health, 5, 15)
    draw_lifes(screen, player.lifes, player_mini_img, WIDTH-100, 15)
    pygame.display.update()
pygame.quit()