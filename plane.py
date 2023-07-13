import random

import pygame

pygame.init()
pygame.font.init()

# 常量--------------------------------------
# 屏幕常量
SCREEN_RECT = pygame.Rect(0, 0, 480, 700)
# 帧率
FRAME = 60

# 字体样式和大小
FONT = pygame.font.SysFont('Microsoft YaHei', 20)
# 字体颜色rgb
FONT_COLOR = (46, 213, 115)

# 英雄发射子弹事件
FIRE = pygame.USEREVENT + 1
# 英雄子弹XY方向飞行速度(正相关，下同)
BULLET_SPEED_Y = 30
BULLET_SPEED_X = 15
# 英雄子弹射速(负相关)
FIRE_RATE = 20
# 英雄爆炸音效
AIYO = pygame.mixer.Sound('voice/aiyo.mp3')

# 创建敌机的定时器常量
CREATE_ENEMY = pygame.USEREVENT
# 敌机生成速度(-)
ENEMY_RATE = 500
# 敌机发射子弹事件
ENEMY_FIRE = pygame.USEREVENT + 2
# 敌机子弹射速(-)
ENEMY_FIRE_RATE = 300
# 敌机子弹速度(+)
ENEMY_BULLET_SPEED = random.randint(5,20)
# 敌机爆炸音效
EXPLOSION = pygame.mixer.Sound('voice\\bong.mp3')

# 图片文件前缀
IMG = r'images/'


# -------------------------------------------

# 类-----------------------------------------
# 游戏精灵
class GameSprite(pygame.sprite.Sprite):
    def __init__(self, image_name, speed=1):
        # 调用父类构造方法
        super().__init__()
        self.image = pygame.image.load(image_name)  # 图片
        self.rect = self.image.get_rect()  # 矩形区域
        self.speed = speed  # 速度
        self.mask = pygame.mask.from_surface(self.image)  # 图片掩码对象(非透明部分，用于碰撞检测)

    def update(self):
        self.rect.y += self.speed


'''背景类'''


class Background(GameSprite):
    def __init__(self, is_alt=False):
        super().__init__(IMG + 'background.png')
        if is_alt:
            self.rect.y = -self.rect.height

    def update(self):
        super().update()
        if self.rect.y >= SCREEN_RECT.height:
            self.rect.y = -self.rect.height


'''敌机类'''


class Enemy(GameSprite):
    def __init__(self, num):
        # 随机生成3种敌机类型
        super().__init__(IMG + 'enemy' + str(num) + '.png')
        self.id = num  # 敌机类型
        self.speed = random.randint(1, 10)
        self.rect.bottom = 0
        self.rect.x = random.randint(0, SCREEN_RECT.width - self.rect.width)
        self.bullets = pygame.sprite.Group()

    def update(self):
        super().update()
        # 飞出屏幕就删除对象
        if self.rect.y >= SCREEN_RECT.height:
            self.kill()

    def fire(self):
        bullet = Bullet(IMG + 'bullet1.png', speedy=ENEMY_BULLET_SPEED)
        bullet.rect.centerx = self.rect.centerx
        bullet.rect.y = self.rect.bottom
        self.bullets.add(bullet)

    def __del__(self):
        for i in range(30):
            self.image = pygame.image.load('images/enemy1_down1.png')
        for i in range(30):
            self.image = pygame.image.load('images/enemy1_down2.png')
        EXPLOSION.play()



# 英雄飞机类
class Hero(GameSprite):

    def __init__(self):
        super().__init__(IMG + 'me1.png', 0)
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.bottom = SCREEN_RECT.bottom - 120
        # 创建子弹精灵组
        self.bullets = pygame.sprite.Group()

    def update(self):
        self.rect.centerx, self.rect.centery = pygame.mouse.get_pos()

    def fire(self):
        # 中间子弹
        bullet_mid = Bullet(IMG + 'bomb.png')
        bullet_mid.rect.bottom = self.rect.y + 20
        bullet_mid.rect.centerx = self.rect.centerx
        # bullet_mid_left = Bullet(IMG + 'bomb.png', BULLET_SPEED_X)
        # bullet_mid_left.rect.bottom = self.rect.y + 20
        # bullet_mid_left.rect.centerx = self.rect.centerx
        # bullet_mid_right = Bullet(IMG + 'bomb.png', -BULLET_SPEED_X)
        # bullet_mid_right.rect.bottom = self.rect.y + 20
        # bullet_mid_right.rect.centerx = self.rect.centerx

        # # 两侧子弹
        # bullet_left = Bullet(IMG + 'bomb.png', -BULLET_SPEED_X, speedy=int(-BULLET_SPEED_Y / 2), rebound=True)
        # bullet_right = Bullet(IMG + 'bomb.png', BULLET_SPEED_X, speedy=int(-BULLET_SPEED_Y / 2), rebound=True)
        # bullet_right.rect.bottom = self.rect.y + 51
        # bullet_right.rect.centerx = self.rect.centerx + 32
        # bullet_left.rect.bottom = self.rect.y + 51
        # bullet_left.rect.centerx = self.rect.centerx - 32

        # self.bullets.add(bullet_mid, bullet_right, bullet_left, bullet_mid_right, bullet_mid_left)
        self.bullets.add(bullet_mid)


# 子弹类
class Bullet(GameSprite):
    def __init__(self, image_name, speedx=0, speedy=-BULLET_SPEED_Y, rebound=False):
        super().__init__(image_name)
        self.rebound = rebound
        self.speedx = speedx
        self.speedy = speedy

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()
        # 子弹反弹
        if self.rebound:
            if self.rect.x < 0 or self.rect.x > SCREEN_RECT.width:
                self.speedx = -self.speedx
