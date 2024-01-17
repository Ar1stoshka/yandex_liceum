import os
import sys
import pygame
import sqlite3
import entering


pygame.init()
size = width, height = 1000, 800
SCREEN = pygame.display.set_mode(size)
pygame.display.set_caption("SPEEDY CIRCUS")
all_sprites = pygame.sprite.Group()  # создаем группы для спрайтов
back_sprite = pygame.sprite.Group()
other_sprite = pygame.sprite.Group()
clock = pygame.time.Clock()
pygame.mixer.music.load("Brian_Tyler_-_Formula_1_Theme_72716230.mp3")  # включаем музыку
pygame.mixer.music.set_volume(0.05)  # установка громкости
pygame.mixer.music.play(-1)

con = sqlite3.connect("users_data_for_game.db")  # подключаем базу данных
cursor = con.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users_data(
    id INTEGER primary key autoincrement,
    username TEXT,
    password TEXT,
    score INTEGER
)''')  # создаем таблицу в бд, если она не существует
con.commit()


def load_image(path, colorkey=None):  # функция по загрузки изображения
    full_path = os.path.join('data', path)
    if not os.path.exists(full_path):
        print(f"Файл с изображением '{full_path}' не найден")
        sys.exit()
    im = pygame.image.load(full_path)
    if colorkey is not None:
        im = im.convert()
        if colorkey == -1:
            colorkey = im.get_at((0, 0))
        im.set_colorkey(colorkey)
    else:
        im = im.convert_alpha()
    return im


class BreakRecord(pygame.sprite.Sprite):  # кнопка перехода в игру
    image = pygame.transform.scale(load_image('break_btn.PNG'),
                                   (260, 120))

    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.x, self.y = x, y
        self.sb = BreakRecord.image
        self.rect = self.sb.get_rect().move(x, y)
        self.mask = pygame.mask.from_surface(self.sb)
        self.width = self.sb.get_width()
        self.height = self.sb.get_height()


class InfoButton(pygame.sprite.Sprite):  # кнопка перехода в меню с информацией
    image = pygame.transform.scale(load_image('info.PNG'),
                                   (40, 40))

    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.x, self.y = x, y
        self.sb = InfoButton.image
        self.rect = self.sb.get_rect().move(x, y)
        self.mask = pygame.mask.from_surface(self.sb)
        self.width = self.sb.get_width()
        self.height = self.sb.get_height()


class VolButtonOn(pygame.sprite.Sprite):  # кнопка включения музыки
    image = pygame.transform.scale(load_image('muson.PNG'),
                                   (40, 40))

    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.x, self.y = x, y
        self.sb = VolButtonOn.image
        self.rect = self.sb.get_rect().move(x, y)
        self.mask = pygame.mask.from_surface(self.sb)
        self.width = self.sb.get_width()
        self.height = self.sb.get_height()


class VolButtonOff(pygame.sprite.Sprite):  # кнопка выключения музыки
    image = pygame.transform.scale(load_image('musoff.PNG'),
                                   (40, 40))

    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.x, self.y = x, y
        self.sb = VolButtonOff.image
        self.rect = self.sb.get_rect().move(x, y)
        self.mask = pygame.mask.from_surface(self.sb)
        self.width = self.sb.get_width()
        self.height = self.sb.get_height()


class VolLower(pygame.sprite.Sprite):  # кнопка уменьшения громкости
    image = pygame.transform.scale(load_image('vol-.PNG'),
                                   (30, 30))

    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.x, self.y = x, y
        self.sb = VolLower.image
        self.rect = self.sb.get_rect().move(x, y)
        self.mask = pygame.mask.from_surface(self.sb)
        self.width = self.sb.get_width()
        self.height = self.sb.get_height()


class VolHigh(pygame.sprite.Sprite):  # кнопка увеличения громкости
    image = pygame.transform.scale(load_image('vol+.PNG'),
                                   (30, 30))

    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.x, self.y = x, y
        self.sb = VolHigh.image
        self.rect = self.sb.get_rect().move(x, y)
        self.mask = pygame.mask.from_surface(self.sb)
        self.width = self.sb.get_width()
        self.height = self.sb.get_height()


class EnterButton(pygame.sprite.Sprite):  # кнопка входа в аккаунт
    image = pygame.transform.scale(load_image('enter_button.PNG'),
                                   (100, 50))

    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.x, self.y = x, y
        self.sb = EnterButton.image
        self.rect = self.sb.get_rect().move(x, y)
        self.mask = pygame.mask.from_surface(self.sb)
        self.width = self.sb.get_width()
        self.height = self.sb.get_height()


class BackButtonInfo(pygame.sprite.Sprite):  # кнопка назад из меню
    image = pygame.transform.scale(load_image('back_button.PNG'),
                                   (60, 30))

    def __init__(self, x, y):
        super().__init__(back_sprite)
        self.x, self.y = x, y
        self.sb = BackButtonInfo.image
        self.rect = self.sb.get_rect().move(x, y)
        self.mask = pygame.mask.from_surface(self.sb)
        self.width = self.sb.get_width()
        self.height = self.sb.get_height()


class PlayBreakRecord(pygame.sprite.Sprite):  # кнопка ведущая в игру
    image = pygame.transform.scale(load_image('play_btn.PNG'),
                                   (180, 90))

    def __init__(self, x, y):
        super().__init__(other_sprite)
        self.x, self.y = x, y
        self.sb = PlayBreakRecord.image
        self.rect = self.sb.get_rect().move(x, y)
        self.mask = pygame.mask.from_surface(self.sb)
        self.width = self.sb.get_width()
        self.height = self.sb.get_height()


class PlayBtn(pygame.sprite.Sprite):  # кнопка играть
    image = pygame.transform.scale(load_image('play_btn.PNG'),
                                   (30, 30))

    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.x, self.y = x, y
        self.sb = PlayBtn.image
        self.rect = self.sb.get_rect().move(x, y)
        self.mask = pygame.mask.from_surface(self.sb)
        self.width = self.sb.get_width()
        self.height = self.sb.get_height()


class BackButtonInfo1(pygame.sprite.Sprite):  # кнопка назад
    image = pygame.transform.scale(load_image('back_button.PNG'),
                                   (60, 30))

    def __init__(self, x, y):
        super().__init__(other_sprite)
        self.x, self.y = x, y
        self.sb = BackButtonInfo.image
        self.rect = self.sb.get_rect().move(x, y)
        self.mask = pygame.mask.from_surface(self.sb)
        self.width = self.sb.get_width()
        self.height = self.sb.get_height()


class Menu:  # сам класс основного меню
    def __init__(self):
        self.main_menu()

    def main_menu(self):
        pygame.mixer.music.load("Brian_Tyler_-_Formula_1_Theme_72716230.mp3")
        pygame.mixer.music.set_volume(0.05)
        pygame.mixer.music.play(-1)
        self.vol = 0.05
        self.counter_for_vol = 0
        self.break_btn = BreakRecord(375, 320)
        self.info_btn = InfoButton(958, 7)
        self.enter_button = EnterButton(450, 540)
        self.volume_button_off = VolButtonOff(960, 50)
        self.volume_button_on = VolButtonOn(960, 50)
        self.vol_h = VolHigh(965, 92)
        self.vol_l = VolLower(966, 125)

        pygame.mixer.music.unpause()
        SCREEN = pygame.display.set_mode(size)
        ''' 
        чтобы при возвращении на главный экран с экрана другого размера
        главный экран оставался таким же по размеру
        '''
        SCREEN.blit(load_image("background.PNG"), (-10, -20))  # сначала ставим картинку фона
        SCREEN.blit(load_image("OIG.jpeg"), (0, 275))  # поверх фона остальные изображения
        SCREEN.blit(load_image("OIG.jpeg"), (690, 275))
        sc = entering.global_var["score"]
        f = pygame.font.Font('Tourney-Medium.ttf', 40)
        text = f.render('YOUR SCORE: ' + sc, True,
                          (255, 255, 255))
        SCREEN.blit(text, (360, 460))
        f1 = pygame.font.Font('Tourney-Medium.ttf', 90)
        text1 = f1.render('Speedy Circus', True,
                          "#f31414")
        SCREEN.blit(text1, (190, 140))
        w = entering.global_var1["nick"]
        f2 = pygame.font.Font('Tourney-Medium.ttf', 40)
        text2 = f2.render('welcome,' + " " + w, True,
                              "#afaebe")
        SCREEN.blit(text2, (345, 260))
        all_sprites.draw(SCREEN)
        all_sprites.update()
        clock.tick(30)  # 30 кадров в секунду
        pygame.display.flip()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:  # обработка всех кнопок
                    if (self.break_btn.rect.x < event.pos[0]
                            < self.break_btn.width + self.break_btn.rect.x and
                            self.break_btn.rect.y < event.pos[1] < self.break_btn.height +
                            self.break_btn.rect.y):
                        import break_record
                    if (self.info_btn.rect.x < event.pos[0]
                            < self.info_btn.width + self.info_btn.rect.x and
                            self.info_btn.rect.y < event.pos[1] < self.info_btn.height +
                            self.info_btn.rect.y):
                        self.info_menu()
                        running = False
                    if (self.enter_button.rect.x < event.pos[0]
                            < self.enter_button.width + self.enter_button.rect.x and
                            self.enter_button.rect.y < event.pos[1] < self.enter_button.height +
                            self.enter_button.rect.y):
                        a = entering.Entering()
                        a.main_menu()
                        running = False
                    if (self.volume_button_on.rect.x < event.pos[0]
                            < self.volume_button_on.width + self.volume_button_on.rect.x and
                            self.volume_button_on.rect.y < event.pos[1] < self.volume_button_on.height +
                            self.volume_button_on.rect.y):
                        if self.counter_for_vol % 2 == 0:
                            pygame.mixer.music.pause()
                            self.volume_button_off = VolButtonOff(960, 50)
                            all_sprites.draw(SCREEN)
                            all_sprites.update()
                            pygame.display.flip()
                            self.counter_for_vol += 1
                        else:
                            pygame.mixer.music.unpause()
                            self.volume_button_on = VolButtonOn(960, 50)
                            all_sprites.draw(SCREEN)
                            all_sprites.update()
                            pygame.display.flip()
                            self.counter_for_vol += 1
                    if (self.vol_h.rect.x < event.pos[0]
                            < self.vol_h.width + self.vol_h.rect.x and
                            self.vol_h.rect.y < event.pos[1] < self.vol_h.height +
                            self.vol_h.rect.y):
                        self.vol += 0.02
                        pygame.mixer.music.set_volume(self.vol)
                    if (self.vol_l.rect.x < event.pos[0]
                            < self.vol_l.width + self.vol_l.rect.x and
                            self.vol_l.rect.y < event.pos[1] < self.vol_l.height +
                            self.vol_l.rect.y):
                        self.vol -= 0.02
                        pygame.mixer.music.set_volume(self.vol)


    def info_menu(self):  # меню с иформацией
        self.back_button = BackButtonInfo(10, 740)

        SCREEN.blit(load_image("background1.PNG"), (0, -10))
        SCREEN.blit(load_image("info_text.PNG"), (150, 150))
        pygame.mixer.music.pause()
        clock.tick(30)
        back_sprite.draw(SCREEN)
        back_sprite.update()
        pygame.display.flip()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if (self.back_button.rect.x < event.pos[0]
                            < self.back_button.width + self.back_button.rect.x and
                            self.back_button.rect.y < event.pos[1] < self.back_button.height +
                            self.back_button.rect.y):
                        self.main_menu()


if __name__ == "__main__":
    p = Menu()
    p.main_menu
