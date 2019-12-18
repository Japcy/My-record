import pygame
from plane_sprites import *


class Plane_game(object):
    """飞机大战主程序"""

    def __init__(self):
        print('游戏初始化')
        # 创建游戏窗口
        self.screen = pygame.display.set_mode((SCREEN_RECT.size))
        # 创建游戏时钟
        self.clock = pygame.time.Clock()
        # 调用私有方法，创建精灵和精灵组
        self.__create_sprites()
        #设置定时器事件，创建敌机
        pygame.time.set_timer(CREATE_ENEMY_EVENT, 1000)
        pygame.time.set_timer(HERO_FIRE_EVENT, 500)

    def __create_sprites(self):
        # 创建背景精灵和精灵组
        bg1 = Background()
        bg2 = Background(True)
        self.back_group = pygame.sprite.Group(bg1, bg2)
        # 创建敌机精灵组
        self.enemy_group = pygame.sprite.Group()
        # 创建英雄精灵和精灵组
        self.hero = Hero()
        self.hero_group = pygame.sprite.Group(self.hero)

    def start_game(self):
        print('游戏开始...')
        while True:
            # 设置刷新帧率
            self.clock.tick(FRAME_PER_SEC)
            # 事件监听
            self.__event_handler()
            # 碰撞检测
            self.__check_collide()
            # 更新、绘制精灵组
            self.__update_sprites()
            # 更新显示
            pygame.display.update()
            pass

    def __event_handler(self):
        for event in pygame.event.get():
        # 判断是否退出游戏
            if event.type == pygame.QUIT:
                Plane_game.__game_over()
            elif event.type == CREATE_ENEMY_EVENT:
                # print('敌机出现...')
                # 创建敌机精灵
                enemy = Enemy()
                # 添加敌机到敌机精灵组
                self.enemy_group.add(enemy)
            elif event.type == HERO_FIRE_EVENT:
                self.hero.fire()

            # 事件监听的键盘输入方式，按一次键盘捕获一次
            # elif event.type == pygame.KEYDOWN and event.key ==pygame.K_RIGHT:
            #     print('向右移动...')

        # 使用键盘模块，可以按住键盘不放，持续捕捉键盘输入
        keys_pressed = pygame.key.get_pressed()
        # 判断元组中对应的按键索引值是否为1
        if keys_pressed[pygame.K_RIGHT]:
            # print('向右移动...')
            self.hero.rect.x += 5
        elif keys_pressed[pygame.K_LEFT]:
            self.hero.rect.x += -5
        elif keys_pressed[pygame.K_UP]:
            self.hero.rect.y += -5
        elif keys_pressed[pygame.K_DOWN]:
            self.hero.rect.y += 5
        else:
            self.hero.speed = 0

    def __check_collide(self):
        # 子弹摧毁敌机(两个精灵组检测碰撞，两组中所有的精灵都参与检测)
        count_enemies = pygame.sprite.groupcollide(self.hero.bullets, self.enemy_group, True, True)
        # 敌机撞毁英雄(一个精灵和一个精灵组碰撞)
        enemies = pygame.sprite.spritecollide(self.hero, self.enemy_group, True)
        # 判断毁掉的敌机列表是否有内容，如果有，英雄牺牲,游戏结束
        if len(enemies) > 0:
            self.hero.kill()
            Plane_game.__game_over()

    def __update_sprites(self):
        self.back_group.update()
        self.back_group.draw(self.screen)

        self.enemy_group.update()
        self.enemy_group.draw(self.screen)

        self.hero_group.update()
        self.hero_group.draw(self.screen)

        self.hero.bullets.update()
        self.hero.bullets.draw(self.screen)

    @staticmethod
    def __game_over():
        print('游戏结束')
        pygame.quit()
        exit()


if __name__ == '__main__':
    game = Plane_game()
    game.start_game()