import pygame.event

from plane import *


class PlaneGame:
    '''初始化'''

    def __init__(self):
        print('游戏初始化...')
        # 1.创建主窗口
        self.screen = pygame.display.set_mode(SCREEN_RECT.size)
        # 2.创建时钟
        self.clock = pygame.time.Clock()
        # 3.调用私有方法，创建精灵和精灵组
        self.__create_sprites()
        # 4.设置定时器事件
        pygame.time.set_timer(CREATE_ENEMY, ENEMY_RATE)
        pygame.time.set_timer(FIRE, FIRE_RATE)
        pygame.time.set_timer(ENEMY_FIRE, ENEMY_FIRE_RATE)
        # 5.初始化变量
        self.destoried = 0  # 击败敌机数量
        self.my_font = FONT  # 字体对象
        self.kills = self.my_font.render('杀敌数:' + str(0), True, FONT_COLOR, None)  # 杀敌数

    '''创建精灵和精灵组(游戏中的各种物品)'''

    def __create_sprites(self):
        # 创建背景精灵和背景精灵组
        bg = Background()
        bg2 = Background(True)
        self.back_group = pygame.sprite.Group(bg, bg2)

        # 创建敌机列表和敌机精灵组
        self.enemy_group = pygame.sprite.Group()

        # 创建英雄精灵和英雄精灵组
        self.hero = Hero()
        self.hero_group = pygame.sprite.Group(self.hero)

    '''开始游戏'''

    def start_game(self):
        print('开始游戏')
        while True:
            self.clock.tick(FRAME)
            self.__event_handler()
            self.__update_sprites()
            self.__check_collide()
            self.__show_status_bar()
            pygame.display.update()

    '''事件监听'''

    def __event_handler(self):
        for event in pygame.event.get():
            # 判断是否退出游戏
            if event.type == pygame.QUIT:
                PlaneGame.__game_over()
            # 创建敌机
            elif event.type == CREATE_ENEMY:
                e = Enemy(random.randint(1, 3))
                self.enemy_group.add(e)
            # 英雄发射子弹
            elif event.type == FIRE:
                self.hero.fire()
            # 敌机发射子弹
            elif event.type == ENEMY_FIRE:
                for i in self.enemy_group.sprites():
                    i.fire()

    '''碰撞检测'''

    def __check_collide(self):
        # 英雄飞机子弹销毁敌机
        lst = pygame.sprite.groupcollide(self.hero.bullets, self.enemy_group, True, True, pygame.sprite.collide_mask)
        # 敌机撞毁英雄飞机
        enemies = pygame.sprite.spritecollide(self.hero, self.enemy_group, True, collided=pygame.sprite.collide_mask)
        enemies = []
        enemies2 = []
        # 英雄子弹和敌机子弹抵消，敌机击毁英雄飞机
        for e in self.enemy_group.sprites():
            pygame.sprite.groupcollide(self.hero.bullets, e.bullets, True, True, pygame.sprite.collide_mask)
            enemies2 = pygame.sprite.spritecollide(self.hero, e.bullets, True, collided=pygame.sprite.collide_mask)

        # 更新杀敌数
        self.destoried += len(lst)
        self.kills = self.my_font.render('杀敌数:' + str(self.destoried), True, FONT_COLOR, None)

        if enemies or enemies2:
            self.hero.kill()
            print('这都能挂?')
            self.__game_over()

    '''游戏状态显示'''

    def __show_status_bar(self):
        self.screen.blit(self.kills, (0, SCREEN_RECT.height - self.kills.get_rect().height))

    '''更新精灵组'''

    def __update_sprites(self):
        self.back_group.update()
        self.back_group.draw(self.screen)
        self.enemy_group.update()
        self.enemy_group.draw(self.screen)
        for i in self.enemy_group.sprites():
            i.bullets.update()
            i.bullets.draw(self.screen)
        self.hero_group.update()
        self.hero_group.draw(self.screen)
        self.hero.bullets.update()
        self.hero.bullets.draw(self.screen)

    '''结束游戏'''

    @staticmethod
    def __game_over():
        print('游戏结束')
        pygame.quit()
        exit(0)


'''主函数'''
if __name__ == '__main__':
    p = PlaneGame()
    p.start_game()
