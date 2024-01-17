import time
import random
import pygame
import os
import sys

import entering
import main


# Инициализация констант и pygame
pygame.init()
SIZE = WIDTH, HEIGHT = 1000, 800
pygame.display.set_caption("SPEEDY CIRCUS")
SCREEN = pygame.display.set_mode(SIZE)
text_showing = False


# функция, скачивающая и изменяющая по надобности изображения
def load_image(path, colorkey=None):
    fullname = os.path.join("data", path)
    if not os.path.isfile(fullname):
        print(f'Файл с изображением {fullname} не найден')
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


# класс машинок (красных или желтых)
class OtherRacoons(pygame.sprite.Sprite):
    im_random = random.choice(['racoon1.jpeg',  # чтобы при запуске игры отображались разные еноты
                               "racoon2.jpeg",
                               "racoon3.jpeg",
                               "racoon4.jpeg",
                               "racoon5.jpeg"])
    image = pygame.transform.scale(load_image(im_random), (100, 100))

    def __init__(self):
        super().__init__(all_sprites)
        self.add(other_car_sprite)
        self.other_car = OtherRacoons.image
        self.rect = self.other_car.get_rect().move(random.randrange(100, 789, 120), 0)
        self.mask = pygame.mask.from_surface(self.other_car)
        self.score = 0
        self.speed = 6
        self.count = 0

    # функция по рандомному выбору машинок и их координат
    def moving_racoon(self, other):
        if self.rect.y < 820:
            # изменение координат
            self.rect = self.rect.move(0, self.speed)
            self.count += 1
            # изменение скорости
            if self.count % 50 == 0:
                self.score += 0.5
                self.speed += 0.5
        else:
            cy = random.randrange(-1000, -150)
            cx = random.randrange(100, 789, 120)
            while cy == other.rect.y or cx == other.rect.x:
                cy = random.randrange(-1000, -150)
                cx = random.randrange(100, 789, 120)
            self.rect.y = cy
            self.rect.x = cx

        if other.rect.y < 820:
            other.rect = other.rect.move(0, self.speed)
        else:
            cy = random.randrange(-1000, -150)
            cx = random.randrange(100, 789, 120)
            while cy == self.rect.y or cx == self.rect.x:
                cy = random.randrange(-1000, -150)
                cx = random.randrange(100, 789, 120)
            other.rect.y = cy
            other.rect.x = cx


# класс болида формулы 1
class FBolid(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image('car.jpeg'), (150, 140))

    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.formula_car = FBolid.image
        self.rect = self.formula_car.get_rect().move(x, y)
        self.mask = pygame.mask.from_surface(self.formula_car)

    # функция, отслеживающая столкновение с другими объектами
    def update(self):
        global reaction
        if pygame.sprite.collide_mask(self, racoon1):
            fail_table = FailMenu(280, 50)
            fail_repeat = RepeatGame(470, 405)
            fail_main = Fail_Main(230, 405)
            if entering.global_var1["nick"] != "guest":
                data = main.cursor.execute("SELECT score FROM users_data WHERE username = ?",
                                        (entering.global_var1["nick"],)).fetchall()
                for i in data:
                    score = i[0]
                if racoon1.score > int(score):
                    query = """Update users_data set score = ? where username = ?"""
                    data = (str(racoon1.score), entering.global_var1["nick"])
                    main.cursor.execute(query, data)
                    main.con.commit()

            pygame.mixer.music.pause()

            SCREEN.blit(load_image('good_background.png'), (-200, 0))
            SCREEN.blit(load_image('good_background1.png'), (850, 0))
            fail.draw(SCREEN)
            clock.tick(30)  # 30 кадров в секунду
            pygame.display.flip()

            running1 = True
            while running1:
                for event1 in pygame.event.get():
                    if event1.type == pygame.QUIT:
                        running1 = False
                    if event1.type == pygame.MOUSEBUTTONDOWN:
                        if fail_main.rect.x < event1.pos[0] < fail_main.width + fail_main.rect.x and \
                                fail_main.rect.y < event1.pos[1] < fail_main.height + fail_main.rect.y:
                            from main import Menu
                            p = Menu()
                            p.main_menu()
                            pygame.mixer.music.pause()
                            running1 = False
                        if fail_repeat.rect.x < event1.pos[0] < fail_repeat.width + fail_repeat.rect.x and \
                                fail_repeat.rect.y < event1.pos[1] < fail_repeat.height + fail_repeat.rect.y:
                            reset()
            reaction = False
            time.sleep(1)

        if pygame.sprite.collide_mask(self, racoon2):
            fail_table = FailMenu(280, 50)
            fail_repeat = RepeatGame(470, 405)
            fail_main = Fail_Main(230, 405)
            if entering.global_var1["nick"] != "guest":
                data = main.cursor.execute("SELECT score FROM users_data WHERE username = ?",
                                        (entering.global_var1["nick"],)).fetchall()
                for i in data:
                    score = i[0]
                if racoon1.score > int(score):
                    query = """Update users_data set score = ? where username = ?"""
                    data = (str(racoon1.score), entering.global_var1["nick"])
                    main.cursor.execute(query, data)
                    main.con.commit()

            pygame.mixer.music.pause()

            SCREEN.blit(load_image('good_background.png'), (-200, 0))
            SCREEN.blit(load_image('good_background1.png'), (850, 0))
            fail.draw(SCREEN)
            clock.tick(30)  # 30 кадров в секунду
            pygame.display.flip()

            running1 = True
            while running1:
                for event1 in pygame.event.get():
                    if event1.type == pygame.QUIT:
                        running1 = False
                    if event1.type == pygame.MOUSEBUTTONDOWN:
                        if fail_main.rect.x < event1.pos[0] < fail_main.width + fail_main.rect.x and \
                                fail_main.rect.y < event1.pos[1] < fail_main.height + fail_main.rect.y:
                            from main import Menu
                            p = Menu()
                            p.main_menu()
                            pygame.mixer.music.pause()
                            running1 = False
                        if fail_repeat.rect.x < event1.pos[0] < fail_repeat.width + fail_repeat.rect.x and \
                                fail_repeat.rect.y < event1.pos[1] < fail_repeat.height + fail_repeat.rect.y:
                            reset()
            reaction = False
            time.sleep(1)

        elif self.rect.x > 770 or self.rect.x < 100:
            fail_table = FailMenu(280, 50)
            fail_repeat = RepeatGame(470, 405)
            fail_main = Fail_Main(230, 405)
            if entering.global_var1["nick"] != "guest":
                data = main.cursor.execute("SELECT score FROM users_data WHERE username = ?",
                                        (entering.global_var1["nick"],)).fetchall()
                for i in data:
                    score = i[0]
                if racoon1.score > int(score):
                    query = """Update users_data set score = ? where username = ?"""
                    data = (str(racoon1.score), entering.global_var1["nick"])
                    main.cursor.execute(query, data)
                    main.con.commit()

            SCREEN.blit(load_image('good_background.png'), (-200, 0))
            SCREEN.blit(load_image('good_background1.png'), (850, 0))
            fail.draw(SCREEN)
            clock.tick(30)  # 30 кадров в секунду
            pygame.display.flip()

            running1 = True
            while running1:
                for event1 in pygame.event.get():
                    if event1.type == pygame.QUIT:
                        running1 = False
                    if event1.type == pygame.MOUSEBUTTONDOWN:
                        if fail_main.rect.x < event1.pos[0] < fail_main.width + fail_main.rect.x and \
                                fail_main.rect.y < event1.pos[1] < fail_main.height + fail_main.rect.y:
                            from main import Menu
                            p = Menu()
                            p.main_menu()
                            pygame.mixer.music.pause()
                            running1 = False
                        if fail_repeat.rect.x < event1.pos[0] < fail_repeat.width + fail_repeat.rect.x and \
                                fail_repeat.rect.y < event1.pos[1] < fail_repeat.height + fail_repeat.rect.y:
                            reset()
            reaction = False
            time.sleep(1)


class FailMenu(pygame.sprite.Sprite):
    image = load_image('crash.jpeg')
    image = pygame.transform.scale(image, (400, 400))

    def __init__(self, x, y):
        super().__init__(fail)
        self.cm = FailMenu.image
        self.rect = self.cm.get_rect().move(x, y)
        self.mask = pygame.mask.from_surface(self.cm)
        self.width = self.cm.get_width()
        self.height = self.cm.get_height()


class Comp_Main(pygame.sprite.Sprite):
    image = load_image('menu.PNG')
    image = pygame.transform.scale(image, (245, 125))

    def __init__(self, x, y):
        super().__init__(menu)
        self.cm = Comp_Main.image
        self.rect = self.cm.get_rect().move(x, y)
        self.mask = pygame.mask.from_surface(self.cm)
        self.width = self.cm.get_width()
        self.height = self.cm.get_height()


class Fail_Main(pygame.sprite.Sprite):
    image = load_image('menu.PNG')
    image = pygame.transform.scale(image, (245, 108))

    def __init__(self, x, y):
        super().__init__(fail)
        self.cm = Fail_Main.image
        self.rect = self.cm.get_rect().move(x, y)
        self.mask = pygame.mask.from_surface(self.cm)
        self.width = self.cm.get_width()
        self.height = self.cm.get_height()


class RepeatGame(pygame.sprite.Sprite):
    image = load_image('repeat.png')
    image = pygame.transform.scale(image, (245, 108))

    def __init__(self, x, y):
        super().__init__(fail)
        self.cm = Fail_Main.image
        self.rect = self.cm.get_rect().move(x, y)
        self.mask = pygame.mask.from_surface(self.cm)
        self.width = self.cm.get_width()
        self.height = self.cm.get_height()


def reset():
    global x, y, menu, fail, racoon1, clock, racoon2, all_sprites, other_car_sprite
    pygame.mixer.music.load("F1 Mexico GP Mariachi Intro 2021 - Hermanos Rodriguez (320 kbps).mp3")
    pygame.mixer.music.set_volume(0.05)
    pygame.mixer.music.play(-1)
    x_chages, y_chages = 0, 0
    x = 340
    y = 445
    block = 10
    clock = pygame.time.Clock()
    pygame.display.set_caption("SPEEDY CIRCUS")
    all_sprites = pygame.sprite.Group()
    menu = pygame.sprite.Group()
    fail = pygame.sprite.Group()
    other_car_sprite = pygame.sprite.Group()
    robot_delivery = FBolid(x, y)
    racoon1 = OtherRacoons()
    racoon2 = OtherRacoons()
    reaction = True
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and reaction:
                    x_chages -= block
                elif event.key == pygame.K_RIGHT and reaction:
                    x_chages += block
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT \
                        or event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                    x_chages = 0
                    y_chages = 0

        robot_delivery.rect.x += x_chages
        SCREEN.fill((125, 116, 109))

        SCREEN.blit(load_image('good_background.png'), (-200, 0))
        SCREEN.blit(load_image('good_background1.png'), (850, 0))

        all_sprites.draw(SCREEN)
        racoon1.moving_racoon(racoon2)
        font = pygame.font.Font(None, 30)
        font2 = pygame.font.Font(None, 100)
        if text_showing:
            menu_main = Comp_Main(282, 385)

            menu.draw(SCREEN)
            clock.tick(30)  # 30 кадров в секунду
            pygame.display.flip()

            running1 = True
            while running1:
                for event1 in pygame.event.get():
                    if event1.type == pygame.QUIT:
                        running1 = False
                    if event1.type == pygame.MOUSEBUTTONDOWN:
                        if menu_main.rect.x < event1.pos[0] < menu_main.width + menu_main.rect.x and \
                                menu_main.rect.y < event1.pos[1] < menu_main.height + menu_main.rect.y:
                            from main import Menu
                            pygame.mixer.music.pause()
                            p = Menu()
                            p.main_menu()
                            running1 = False
            reaction = False
            time.sleep(1)
        all_sprites.update()
        clock.tick(30)
        pygame.display.update()
        f = pygame.font.Font('Jomhuria-Regular.ttf', 75)  # тут оформляем всякие дизайнерские штучки
        text = f.render('SCORE: ' + str(racoon1.score), True,
                        (255, 255, 255))
        SCREEN.blit(text, (400, 10))
        pygame.display.flip()
    pygame.quit()


reset()


