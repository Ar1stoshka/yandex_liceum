import sys
import pygame
import os
import hashlib
import main                               # для возвращения на главный экран


pygame.init()  # инициализация
size = width, height = 700, 500  # размеры экрана
SCREEN = pygame.display.set_mode(size)
pygame.display.set_caption("SPEEDY CIRCUS")
all_sprites = pygame.sprite.Group() # группа для всех спрайтов
clock = pygame.time.Clock()
global_var = globals()  # переменная в которой будет передаваться результат пользователя из класса в класс
global_var["score"] = "0"
global_var1 = globals()  # переменная в которой будет передаваться ник из класса в класс
global_var1["nick"] = "guest"


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


class TextInput(pygame.sprite.Sprite):  # класс отвечающий за поля ввода информации
    def __init__(self, x, y, width=100, height=50, color=(0, 37, 62),
                 bgcolor="#4a4f6a", selectedColor="#7d808f"):
        super().__init__()
        self.text_value = ""  # хранит данные пользователя
        self.isSelected = False  # нажал ли пользователь на поле ввода
        self.color = color  # цвет текста
        self.bgcolor = bgcolor  # цвет самого поля ввода
        self.selectedColor = selectedColor  # цвет поля, когда пользователь вводит данные

        self.font = pygame.font.Font('Jomhuria-Regular.ttf', 55)  # шрифт текста
        self.text = self.font.render(self.text_value, True, self.color)
        self.bg = pygame.Rect(x, y, width, height, border_radius=5)  # границы и размеры поля ввода

    def clicked(self, mousePos):  # функция определяющяя выбранное поле ввода
        if self.bg.collidepoint(mousePos):
            self.isSelected = not self.isSelected
            return True
        return False

    def update_text(self, new_text):  # функция обновления текста
        temp = self.font.render(new_text, True, self.color)
        if temp.get_rect().width >= (self.bg.width - 20):  # если длина текста больше чем может вместить поле
            return  #  то новый текст просто больше не отображается
        self.text_value = new_text
        self.text = temp

    def render(self, display):  # функция, размещающая текст и рисующая само поле ввода
        self.pos = self.text.get_rect(center=(self.bg.x + self.bg.width / 2,
                                              self.bg.y + self.bg.height / 2))
        if self.isSelected:  # если поле выбрано то оно рисуется другим цветом
            pygame.draw.rect(display, self.selectedColor, self.bg, border_radius=8)
        else:
            pygame.draw.rect(display, self.bgcolor, self.bg, border_radius=8)
        display.blit(self.text, self.pos)  # отображаем текст


class CustomGroup(pygame.sprite.Group):  # создаем свой класс, отвечающий за группировку полей ввода
    # ибо нельзя чтобы два поля были выбранны одновременно
    def __init__(self):
        super().__init__()
        self.current = None


class BackButton(pygame.sprite.Sprite):  # класс кнопки возвращения на главное меню
    image = pygame.transform.scale(load_image('back_button.PNG'),
                                   (60, 30))

    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.x, self.y = x, y
        self.sb = BackButton.image
        self.rect = self.sb.get_rect().move(x, y)
        self.mask = pygame.mask.from_surface(self.sb)
        self.width = self.sb.get_width()
        self.height = self.sb.get_height()


class EnterBtn(pygame.sprite.Sprite):  # класс кнопки подтверждающей вход/регистрацию
    image = pygame.transform.scale(load_image('Снимок.PNG'),
                                   (160, 70))

    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.x, self.y = x, y
        self.sb = EnterBtn.image
        self.rect = self.sb.get_rect().move(x, y)
        self.mask = pygame.mask.from_surface(self.sb)
        self.width = self.sb.get_width()
        self.height = self.sb.get_height()


class Entering:  # класс, отвечающий за окно входа в аккаунт
    def __init__(self):
        self.main_menu()

    def main_menu(self):
        self.back_button = BackButton(7, 465)  # задаем положение кнопок
        self.enter_btn = EnterBtn(280, 380)
        self.score = ""  # переменная где хранится максимальный результат пользователя из бд

        SCREEN = pygame.display.set_mode(size)
        '''
        чтобы при возвращении на главный экран с экрана другого размера
        главный экран оставался таким же по размеру
        '''
        SCREEN.fill((0, 37, 62))
        f = pygame.font.Font('Tourney-Medium.ttf', 45)  # тут оформляем всякие дизайнерские штучки
        text = f.render('Welcome to the', True,
                          (255, 255, 255))
        SCREEN.blit(text, (170, 10))
        f1 = pygame.font.Font('Tourney-Medium.ttf', 70)
        text1 = f1.render('Speedy Circus', True,
                        "#f31414")
        f2 = pygame.font.Font('Jomhuria-Regular.ttf', 35)
        text2 = f2.render('username:', True,
                          "#e0dbca")
        f3 = pygame.font.Font('Jomhuria-Regular.ttf', 35)
        text3 = f3.render('password:', True,
                          "#e0dbca")
        SCREEN.blit(text3, (193, 270))
        SCREEN.blit(text2, (193, 170))
        SCREEN.blit(text1, (110, 50))
        f4 = pygame.font.Font('Jomhuria-Regular.ttf', 35)
        text4 = f4.render("*if you don't have an account, just create it right here", True,
                          "#797884")
        SCREEN.blit(text4, (143, 460))
        image = main.load_image("OIG.jpeg")
        image = pygame.transform.scale(image, (160, 160))
        SCREEN.blit(image, (10, 195))  # поверх фона остальные изображения
        SCREEN.blit(image, (545, 195))
        TextInputGroup = CustomGroup()  # создаем группу для полей ввода
        username = TextInput(x=190, y=200, width=340, height=46)  # поле ввода ника
        TextInputGroup.add(username)
        password = TextInput(x=190, y=300, width=340, height=46)  # поле ввода пароля
        TextInputGroup.add(password)
        ibeam = pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_IBEAM)  # определяут место появления
        # текстового курсора при щелчке мышью
        pygame.mixer.music.pause()  # при открытии данного окна музыка ставится на паузу
        clock.tick(30)
        all_sprites.draw(SCREEN)  # отрисовка всех спрайтов
        all_sprites.update()
        pygame.display.flip()
        running = True
        while running:
            mouse_pos = pygame.mouse.get_pos()  # получение позиции курсора
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # если координаты мышки в
                    # пределах какой либо кнопки
                    if (self.back_button.rect.x < event.pos[0]
                            < self.back_button.width + self.back_button.rect.x and
                            self.back_button.rect.y < event.pos[1] < self.back_button.height +
                            self.back_button.rect.y):
                        a = main.Menu()
                        a.main_menu()
                        pygame.quit()
                        sys.exit()
                    if (self.enter_btn.rect.x < event.pos[0]
                            < self.enter_btn.width + self.enter_btn.rect.x and
                            self.enter_btn.rect.y < event.pos[1] < self.enter_btn.height +
                            self.enter_btn.rect.y):
                        un = username.text_value
                        pw = password.text_value
                        if len(un) == 0 or len(pw) == 0:
                            warning = pygame.font.Font('Jomhuria-Regular.ttf', 35)
                            text4 = warning.render('required fields are missing', True,
                                              "#e0dbca")
                            SCREEN.blit(text4, (240, 350))
                            continue
                        data = main.cursor.execute("SELECT username, password FROM users_data").fetchall()
                        if (un, hashlib.md5(pw.encode()).hexdigest(), ) in data:  # если пароль и никнейм уже в БД
                            data1 = main.cursor.execute("SELECT score FROM users_data WHERE username = ?",
                                                  (un,)).fetchall()
                            global_var["score"] = str(*data1[0])
                            global_var1["nick"] = un
                            a = main.Menu()
                            a.main_menu()
                            pygame.quit()
                            sys.exit()
                        if (un, hashlib.md5(pw.encode()).hexdigest(), ) not in data:  # если пароль и никнейм не в БД
                            main.cursor.execute("INSERT INTO users_data (username, password, score) VALUES (?, ?, ?)",
                                                (un, hashlib.md5(pw.encode()).hexdigest(), 0))
                            main.con.commit()
                            global_var["score"] = "0"
                            global_var1["nick"] = un
                            a = main.Menu()
                            a.main_menu()
                            pygame.quit()
                            sys.exit()
                    for textinput in TextInputGroup:
                        if textinput.clicked(mouse_pos):
                            if TextInputGroup.current:
                                TextInputGroup.current.isSelected = False
                            textinput.isSelected = True
                            TextInputGroup.current = textinput
                            break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:  # если пользователь стирает
                        TextInputGroup.current.update_text(TextInputGroup.current.text_value[:-1])
                if event.type == pygame.TEXTINPUT:  # если пользователь вводит данные
                    TextInputGroup.current.update_text(TextInputGroup.current.text_value + event.text)
                for textinput in TextInputGroup:  # отрисовка поля
                    textinput.update(mouse_pos)
                    textinput.render(SCREEN)
                if TextInputGroup.current and TextInputGroup.current.bg.collidepoint(mouse_pos):
                    pygame.mouse.set_cursor(ibeam)
                else:
                    pygame.mouse.set_cursor(pygame.cursors.Cursor())
                pygame.display.update()

