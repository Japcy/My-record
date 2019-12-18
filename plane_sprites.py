import random
import pygame


# 屏幕大小常量
SCREEN_RECT = pygame.Rect(0, 0, 480, 700)
# 刷新的帧率
FRAME_PER_SEC = 60
# 创建敌机的定时器常量
CREATE_ENEMY_EVENT = pygame.USEREVENT
# 英雄发射子弹事件
HERO_FIRE_EVENT = pygame.USEREVENT + 1


class Game_sprite(pygame.sprite.Sprite):
    '''飞机大战游戏精灵'''

    def __init__(self, image_name, speed = 1):
        # 调用父类的初始化方法
        super().__init__()
        # 定义对象属性
        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()
        self.speed = speed

    def update(self):
        # 在垂直方向移动
        self.rect.y += self.speed


class Background(Game_sprite):
    '''游戏背景精灵'''
    def __init__(self, is_alt=False):
        # 调用父类方法实现精灵创建
        super().__init__('./images/background.png')
        if is_alt:
            self.rect.y = -self.rect.height

    def update(self):
    # 调用父类方法
        super().update()
        # 判断是否移出屏幕，如果移出屏幕，将图像设置到屏幕上方
        if self.rect.y >= SCREEN_RECT.height:
            self.rect.y = -self.rect.height


class Enemy(Game_sprite):
    '''敌机精灵'''

    def __init__(self):
        # 调用父类方法，创建敌机精灵，指定敌机图片
        super().__init__('./images/enemy1.png')
        # 指定敌机初始速度
        self.speed = random.randint(1, 5)
        # 指定敌机初始位置
        self.rect.bottom = 0
        self.rect.x = random.randint(0, SCREEN_RECT.width - self.rect.width)

    def update(self):
        # 调用父类方法，保持垂直方向飞行
        super().update()
        # 判断是否飞出屏幕，如果是，从精灵组删除敌机
        if self.rect.y >= SCREEN_RECT.height:
            # print('飞出屏幕，需要删除')
            # 将精灵从所有精灵组中移出，并在内存中销毁
            self.kill()

    def __del__(self):
        '''在销毁之前做一件事'''
        # print('敌机挂了 %s' % self.rect)
        pass


class Hero(Game_sprite):
    '''英雄精灵'''

    def __init__(self):
        super().__init__('./images/me1.png', 0)
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.bottom = SCREEN_RECT.bottom - 120
        # 创建子弹的精灵组
        self.bullets = pygame.sprite.Group()

    def update(self):

        # 水平方向移动
        # self.rect.x += self.speed
        # self.rect.y += self.speed

        # 控制英雄不能跑到屏幕外面
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.right > SCREEN_RECT.right:
            self.rect.right = SCREEN_RECT.right
        elif self.rect.y < 0:
            self.rect.y = 0
        elif self.rect.bottom > SCREEN_RECT.bottom:
            self.rect.bottom = SCREEN_RECT.bottom

    def fire(self):

        for i in (0, 1, 2):

            # 创建子弹精灵
            bullet = Bullet()
            # 设置精灵位置
            bullet.rect.bottom = self.rect.y - i * 20
            bullet.rect.centerx = self.rect.centerx
            # 将精灵添加到精灵组
            self.bullets.add(bullet)


class Bullet(Game_sprite):
    '''子弹精灵'''

    def __init__(self):
        # 调用父类方法，设置子弹图片，初始速度
        super().__init__('./images/bullet1.png', -6)

    def update(self):
        # 调用父类方法，让子弹沿垂直方向飞行
        super().update()
        # 判断子弹是否飞出屏幕
        if self.rect.bottom < 0:
            self.kill()


    def __del__(self):
        pass