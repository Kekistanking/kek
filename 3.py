import pygame
import random
import os
import math
import sys

FPS = 80
pygame.init()
difficulty = 0
size = width, height = 960, 620
screen = pygame.display.set_mode(size)
const = 3
mobs = pygame.sprite.Group()
floor = 0
all_sprites = pygame.sprite.Group()
mob_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
player_bullets = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
life = pygame.sprite.Group()
objects = pygame.sprite.Group()
hod_up = pygame.sprite.Group()
hod_down = pygame.sprite.Group()
hod_left = pygame.sprite.Group()
hod_right = pygame.sprite.Group()


def terminate():  # Выход из программы
    pygame.quit()
    sys.exit()


#  Загрузка изображения
def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname).convert()

    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    image.convert_alpha()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((3, 3))
        image.set_colorkey(colorkey)
    return image


# Меню
def start_screen():
    fon_list = []
    fon_list.append(load_image('NewGame.png'))
    fon_list.append(load_image('RulesMenu.png'))
    fon_list.append(load_image('RecordListMenu.png'))
    fon_list.append(load_image('Exit.png'))
    for i in range(4):
        fon_list[i] = pygame.transform.scale(fon_list[i], (960, 620))
    counter = 4
    screen.blit(fon_list[0], (0, 0))
    while True:
        pygame.mouse.set_visible(False)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == 13:
                    if counter % 4 == 0:
                        usuf.floor_change()
                        usuf.room = random.randint(1, 8)
                        usuf.main_floor = 0
                        usuf.rect.x = 50
                        usuf.rect.y = 50
                        usuf.life = 100
                        usuf.is_change = True
                        main()
                        return
                    elif counter % 4 == 3:
                        terminate()
                    elif counter % 4 == 1:
                        return rules_screen()
                    else:
                        return record_screen()
                if event.key == pygame.K_w:
                    counter -= 1
                elif event.key == pygame.K_s:
                    counter += 1
        try:
            screen.blit(fon_list[counter % 4], (0, 0))
            pygame.display.flip()
        except Exception:
            return


# Правила
def rules_screen():
    spisok = []
    global difficulty
    counter = difficulty - 1
    fon1 = pygame.transform.scale(load_image("RulesEasy.png"), (960, 620))
    fon2 = pygame.transform.scale(load_image("RulesNormal.png"), (960, 620))
    fon3 = pygame.transform.scale(load_image("RulesHard.png"), (960, 620))
    spisok.append(fon1)
    spisok.append(fon2)
    spisok.append(fon3)
    screen.blit(spisok[counter % 3], (0, 0))
    try:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.KEYDOWN:
                    if event.key == 13:
                        start_screen()
                    if event.key == pygame.K_LEFT:
                        counter -= 1
                    elif event.key == pygame.K_RIGHT:
                        counter += 1
            screen.blit(spisok[counter % 3], (0, 0))
            difficulty = counter % 3 + 1
            pygame.display.flip()

    except Exception:
        pass


# Рекорды
def record_screen():
    fon = pygame.transform.scale(load_image("Blank.png"), (960, 620))
    font = pygame.font.Font(None, 64)
    with open("data/records.txt", 'r') as records:
        rlist = [line for line in records]
    color = pygame.Color("White")
    screen.blit(fon, (0, 0))
    temp = []
    for x in rlist:
        a = int(x.split(" ")[-1])
        v = x.rfind(" ")
        b = x[:v]
        temp.append((a, b))
    temp.sort(reverse=True)
    if len(temp) > 5:
        for i in range(5):
            text = "%s %d" % (temp[i][1], temp[i][0])
            txt_surface = font.render(text, True, color)
            screen.blit(txt_surface, (100, i * 50 + 100))
    else:
        for i in range(len(temp)):
            text = "%s %d" % (temp[i][1], temp[i][0])
            txt_surface = font.render(text, True, color)
            screen.blit(txt_surface, (100, i * 50 + 100))
    try:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.KEYDOWN:
                    if event.key == 13:
                        start_screen()
            pygame.display.flip()
    except Exception:
        pass


# Запись рекорда
def get_record():
    fon = pygame.transform.scale(load_image("Blank.png"), (960, 620))
    color = pygame.Color("White")
    font = pygame.font.Font(None, 64)
    screen.blit(fon, (0, 0))
    text1 = "Введите имя"
    txt_surface1 = font.render(text1, True, color)
    screen.blit(txt_surface1, (400, 100))
    pygame.display.flip()
    input_box = pygame.Rect(340, 200, 400, 64)
    text = ""
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    with open("data/records.txt", 'a') as records:
                        records.write("\n%s %d" % (text, usuf.main_floor))
                    start_screen()
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    if len(text) < 13:
                        text += event.unicode
        try:
            screen.blit(fon, (0, 0))
            screen.blit(txt_surface1, (400, 100))
            txt_surface = font.render(text, True, color)
            screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
            pygame.draw.rect(screen, color, input_box, 2)
            pygame.display.flip()
        except Exception:
            return


# Пауза
def pause_game():
    try:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
                    if event.key == pygame.K_RETURN:
                        start_screen()
    except Exception:
        pass


room_image = load_image("room1.bmp")
room_image = pygame.transform.scale(room_image, (960, 540))


# Миникарта, полоса жизней, инвентарь
class InformationAboutPers:
    def __init__(self, a, b, list=[]):
        self.start_x = a
        self.start_y = b
        self.finish_x = width
        self.finish_y = height
        self.list = list

    def minimap(self, room):
        for i in range(3):
            for u in range(3):
                if i * 3 + u == room:
                    pygame.draw.rect(screen, (255, 0, 0),
                                     [self.start_x + (u * (height - self.start_y) // 3),
                                      self.start_y + (i * (height - self.start_y) // 3),
                                      (height - self.start_y) // 3 - 1,
                                      (height - self.start_y) // 3 - 1], 0)
                else:
                    pygame.draw.rect(screen, (100, 100, 100),
                                     [self.start_x + (u * (height - self.start_y) // 3),
                                      self.start_y + (i * (height - self.start_y) // 3),
                                      (height - self.start_y) // 3 - 1,
                                      (height - self.start_y) // 3 - 1], 0)

    def inventar(self):
        for i in range(3):
            for u in range(3):
                if (i * 3 + u in self.list):
                    pygame.draw.rect(screen, (0, 255, 0),
                                     [self.finish_x - ((i + 1) * (height - self.start_y) // 3),
                                      self.finish_y - ((u + 1) * (height - self.start_y) // 3),
                                      (height - self.start_y) // 3 - 1,
                                      (height - self.start_y) // 3 - 1], 0)
                else:
                    pygame.draw.rect(screen, (0, 0, 0),
                                     [self.finish_x - ((i + 1) * (height - self.start_y) // 3),
                                      self.finish_y - ((u + 1) * (height - self.start_y) // 3),
                                      (height - self.start_y) // 3 - 1,
                                      (height - self.start_y) // 3 - 1], 0)

    def life(self, life):
        len = int(width - (self.finish_y - self.start_y) * 2)
        green = int(len * (life / 100))
        pygame.draw.rect(screen, (0, 255, 0),
                         [self.start_x, self.start_y, self.finish_x, self.finish_y], 0)
        if (life != 100):
            pygame.draw.rect(screen, (0, 0, 0),
                             [green + self.finish_y - self.start_y, self.start_y, len - green,
                              self.finish_y], 0)

    def get_key(self, number):
        i = number // 3
        u = number % 3

        pygame.draw.rect(screen, (0, 255, 0),
                         [self.finish_x - ((i + 1) * (height - self.start_y) // 3),
                          self.finish_y - ((u + 1) * (height - self.start_y) // 3),
                          (height - self.start_y) // 3 - 1, (height - self.start_y) // 3 - 1], 0)


class Border(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1, y1, x2, y2):
        super().__init__()
        if x1 == x2:  # вертикальная стенка
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:  # горизонтальная стенка
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


# Пули игрока
class PlayerBullet(pygame.sprite.Sprite):
    ball = load_image("ball.png", -1)
    ball = pygame.transform.scale(ball, (20, 20))
    ball_crush = load_image("ball_crush.png", -1)
    ball_crush = pygame.transform.scale(ball_crush, (20, 20))

    def __init__(self, x, y, t, speed, direction):
        super().__init__(all_sprites, player_bullets)
        self.image = PlayerBullet.ball
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.time = t
        self.direction = direction

    def update(self):
        self.time += 1
        if self.speed == -1 or self.speed == -2:
            self.speed -= 1
            return
        if self.direction == "right":
            self.rect.x += self.speed
            if self.time >= 35:
                self.speed -= 1
                self.rect.y += 2
        elif self.direction == "left":
            self.rect.x -= self.speed
            if self.time >= 35:
                self.speed -= 1
                self.rect.y += 2
        elif self.direction == "up":
            self.rect.y -= self.speed
            if self.time >= 35:
                self.speed -= 1
        elif self.direction == "down":
            self.rect.y += self.speed
            if self.time >= 35:
                self.speed -= 1
        if self.speed == 3:
            self.image = PlayerBullet.ball_crush
        if self.speed <= 0:
            all_sprites.remove(self)
            player_bullets.remove(self)
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.image = PlayerBullet.ball_crush
            self.speed = -1
        elif pygame.sprite.spritecollideany(self, horizontal_borders):
            self.image = PlayerBullet.ball_crush
            self.speed = -1
        x = pygame.sprite.spritecollide(self, strelky, False)
        y = pygame.sprite.spritecollide(self, beguni, False)
        if len(x) != 0:
            pygame.sprite.spritecollide(self, strelky, True)
            self.image = PlayerBullet.ball_crush
            self.kill()
            usuf.floor[usuf.room] = (
                usuf.floor[usuf.room][0] - len(x), usuf.floor[usuf.room][1],
                usuf.floor[usuf.room][2],
                usuf.floor[usuf.room][3], usuf.floor[usuf.room][4])
        elif len(y) != 0:
            pygame.sprite.spritecollide(self, beguni, True)
            self.image = PlayerBullet.ball_crush
            self.kill()
            usuf.floor[usuf.room] = (
                usuf.floor[usuf.room][0], usuf.floor[usuf.room][1] - len(y),
                usuf.floor[usuf.room][2],
                usuf.floor[usuf.room][3], usuf.floor[usuf.room][4])


# Твердый предмет
class StaticObject(pygame.sprite.Sprite):
    def __init__(self, sheet, x, y):
        super().__init__(objects)
        self.frames = []
        self.sheet = sheet
        self.x = x
        self.y = y

    def cut_sheet(self, columns, rows, fw, fh, tw, th, ox, oy):
        w = self.sheet.get_width() // columns
        h = self.sheet.get_height() // rows
        for j in range(rows):
            for i in range(columns):
                frame_location = (w * i + ox, h * j + oy)
                a = self.sheet.subsurface(pygame.Rect(
                    frame_location, (fw, fh)))
                a = pygame.transform.scale(a, (tw, th))
                self.frames.append(a)

    def get_rect(self, tw, th):
        self.rect = pygame.Rect(self.x, self.y, tw, th)

    def get_borders(self, ox=12, oy=20):
        x = self.rect.x
        y = self.rect.y
        w = self.rect.w
        h = self.rect.h
        Border(x + ox, y, x + ox, y + h - oy)
        Border(x + w - ox, y, x + w - ox, y + h - oy)
        Border(x + ox, y, x + w - ox, y)
        Border(x + ox, y + h - oy, x + w - ox, y + h - oy)


# Сундук
class Chest(StaticObject):
    sheet = load_image("chest2.bmp")

    def __init__(self, x, y):
        super().__init__(Chest.sheet, x, y)
        self.get_rect(48, 40)
        self.cut_sheet(2, 1, 30, 32, 48, 40, 1, 0)
        self.image = self.frames[0]
        self.counter = 0
        self.get_borders()

    def open_chest(self):
        self.image = self.frames[1]

    def close_chest(self):
        self.image = self.frames[0]


life = pygame.sprite.Group()
special = pygame.sprite.Group()


class Special(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(special)
        self.image = pygame.transform.scale(load_image('star.png', -1), (64, 64))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(60, 150)
        self.rect.y = random.randint(60, 150)

    def get(self, i):
        usuf.special = 600
        self.kill()
        self.special_bullet = 10


# хил, выпадающий из сундуков
class Heal(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(life)
        self.image = pygame.transform.scale(load_image('Heal.png', -1), (64, 64))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(60, 150)
        self.rect.y = random.randint(60, 150)

    def get(self, i):
        usuf.list_life[i] = True
        usuf.life = min(100, usuf.life + random.randint(10, 20 + usuf.main_floor * 4))
        self.kill()


# Крест по центру комнаты
class BigHole(StaticObject):
    sheet = load_image("chest2.bmp")

    def __init__(self, x, y, tw, th):
        super().__init__(Chest.sheet, x, y)
        self.get_rect(tw, th)
        self.image = pygame.Surface([0, 0])
        # self.image = pygame.Surface([self.rect.w, self.rect.h])
        self.get_borders(12, 25)


# Класс игрока
class Player(pygame.sprite.Sprite):
    sheet = load_image("playersanim.bmp", -1)

    def __init__(self, cords, room):
        super().__init__(player_group, all_sprites)
        self.main_floor = 1
        self.picked = False
        self.room = room
        self.x = cords[0]
        self.y = cords[1]
        self.image = pygame.Surface((1, 1))
        self.images_down = []
        self.images_up = []
        self.images_left = []
        self.images_right = []
        self.cut_sheet(Player.sheet, 9, 4)
        self.rect = pygame.Rect(0, 0, 75, 45)
        self.rect.x = self.x
        self.rect.y = self.y
        self.move_counter = 0
        self.move_left = False
        self.move_right = False
        self.move_up = False
        self.move_down = True
        self.change = [0, 0]
        self.upper_border = pygame.sprite.Sprite()
        self.lower_border = pygame.sprite.Sprite()
        self.get_borders()
        self.life = 100
        self.is_change = True
        self.shoot_cooldown = 0
        self.bullet_speed = 10
        self.map = InformationAboutPers(0, 520)
        self.anim = "down"
        self.special = 0

    # Получение значений клавиш
    def get_event_keyboard(self, array):
        if array[pygame.K_w] == array[pygame.K_s]:
            if array[pygame.K_a] == 1 and array[pygame.K_d] == 0:
                self.move_right = False
                self.change[0] -= 1
                if self.move_left and self.move_up:
                    self.move_up = False
                    self.move_counter = 0
                elif self.move_left and self.move_down:
                    self.move_down = False
                    self.move_counter = 0
                elif self.move_left:
                    self.move_counter += 1
                else:
                    self.move_counter = 0
                    self.move_left = True
                self.anim = "left"
            elif array[pygame.K_a] == 0 and array[pygame.K_d] == 1:
                self.change[0] += 1
                self.move_left = False
                if self.move_right and self.move_up:
                    self.move_up = False
                    self.move_counter = 0
                elif self.move_right and self.move_down:
                    self.move_down = False
                    self.move_counter = 0
                elif self.move_right:
                    self.move_counter += 1
                else:
                    self.move_counter = 0
                    self.move_right = True
                self.anim = "right"
            else:
                self.move_counter = 0
                self.move_left = False
                self.move_right = False
                self.move_up = False
                self.move_down = True
                self.anim = "down"
        elif array[pygame.K_a] == array[pygame.K_d]:
            if array[pygame.K_w] == 1 and array[pygame.K_s] == 0:
                self.change[1] -= 1
                if self.move_up:
                    self.move_counter += 1
                else:
                    self.move_counter = 0
                    self.move_left = False
                    self.move_right = False
                    self.move_up = True
                    self.move_down = False
                self.anim = "up"
            elif array[pygame.K_w] == 0 and array[pygame.K_s] == 1:
                self.change[1] += 1
                if self.move_down:
                    self.move_counter += 1
                else:
                    self.move_counter = 0
                    self.move_left = False
                    self.move_right = False
                    self.move_up = False
                    self.move_down = True
                self.anim = "down"
        else:
            if array[pygame.K_s] == array[pygame.K_a] == 1:
                self.change[1] += 1
                self.change[0] -= 1
                if self.move_down:
                    self.move_counter += 1
                    self.move_left = True
                else:
                    self.move_counter = 0
                    self.move_left = True
                    self.move_right = False
                    self.move_up = False
                    self.move_down = True
                self.anim = "down"
            elif array[pygame.K_s] == array[pygame.K_d] == 1:
                self.change[1] += 1
                self.change[0] += 1
                if self.move_down:
                    self.move_counter += 1
                    self.move_right = True
                else:
                    self.move_counter = 0
                    self.move_left = False
                    self.move_right = True
                    self.move_up = False
                    self.move_down = True
                self.anim = "down"
            elif array[pygame.K_w] == array[pygame.K_a] == 1:
                self.change[1] -= 1
                self.change[0] -= 1
                if self.move_up:
                    self.move_counter += 1
                    self.move_left = True
                else:
                    self.move_counter = 0
                    self.move_left = True
                    self.move_right = False
                    self.move_up = True
                    self.move_down = False
                self.anim = "up"
            elif array[pygame.K_w] == array[pygame.K_d] == 1:
                self.change[1] -= 1
                self.change[0] += 1
                if self.move_up:
                    self.move_counter += 1
                    self.move_right = True
                else:
                    self.move_counter = 0
                    self.move_left = False
                    self.move_right = True
                    self.move_up = True
                    self.move_down = False
                self.anim = "up"
        if array[pygame.K_UP]:
            self.anim = "up"
            self.shoot("up")
        elif array[pygame.K_DOWN]:
            self.anim = "down"
            self.shoot("down")
        elif array[pygame.K_RIGHT]:
            self.anim = "right"
            self.shoot("right")
        elif array[pygame.K_LEFT]:
            self.anim = "left"
            self.shoot("left")

    def update(self):
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        movement_phase = (self.move_counter // 4) % 8
        movement_phase_slow = (self.move_counter // 8) % 8
        dx = self.change[0] * 5
        dy = self.change[1] * 5
        self.rect.x += dx
        self.rect.y += dy
        move_speed = "normal"
        if self.move_up:
            if pygame.sprite.spritecollideany(self.upper_border, horizontal_borders):
                self.rect.y -= dy
                move_speed = "slow"
            if self.move_right or self.move_left:
                if pygame.sprite.spritecollideany(self, vertical_borders):
                    self.rect.x -= dx
        elif self.move_down:
            if pygame.sprite.spritecollideany(self.lower_border, horizontal_borders):
                self.rect.y -= dy
                move_speed = "slow"
            if self.move_right or self.move_left:
                if pygame.sprite.spritecollideany(self, vertical_borders):
                    self.rect.x -= dx
        elif self.move_right:
            if pygame.sprite.spritecollideany(self, vertical_borders):
                self.rect.x -= dx
                move_speed = "slow"
            if pygame.sprite.spritecollideany(self, horizontal_borders):
                self.rect.y -= dy
        elif self.move_left:
            if pygame.sprite.spritecollideany(self, vertical_borders):
                self.rect.x -= dx
                move_speed = "slow"
            if pygame.sprite.spritecollideany(self, horizontal_borders):
                self.rect.y -= dy
        if self.anim == "up":
            if move_speed == "slow":
                self.image = self.images_up[movement_phase_slow]
            else:
                self.image = self.images_up[movement_phase]
        elif self.anim == "down":
            if move_speed == "slow":
                self.image = self.images_down[movement_phase_slow]
            else:
                self.image = self.images_down[movement_phase]
        elif self.anim == "right":
            if move_speed == "slow":
                self.image = self.images_right[movement_phase_slow]
            else:
                self.image = self.images_right[movement_phase]
        else:
            if move_speed == "slow":
                self.image = self.images_left[movement_phase_slow]
            else:
                self.image = self.images_left[movement_phase]

        self.change = [0, 0]
        self.get_borders()
        self.special -= 1

    def cut_sheet(self, sheet, columns, rows, is_door=False):

        w = sheet.get_width() // columns
        h = sheet.get_height() // rows
        for j in range(rows):
            temp = []
            for i in range(columns):
                a = sheet.subsurface(pygame.Rect((w * i + 17, h * j + 15), (32, 48)))
                a = pygame.transform.scale(a, (80, 45))
                temp.append(a)
            if j == 0:
                self.images_up = temp
            elif j == 1:
                self.images_left = temp
            elif j == 2:
                self.images_down = temp
            elif j == 3:
                self.images_right = temp

    # Стрельба
    def shoot(self, direction):
        if self.shoot_cooldown == 0:
            t = 0
            speed = self.bullet_speed
            if direction == "right":
                x = self.rect.x + self.rect.w
                y = random.randint(self.rect.y - 10, self.rect.y + 10)
            elif direction == "left":
                x = self.rect.x - 20
                y = random.randint(self.rect.y - 10, self.rect.y + 10)
            elif direction == "up":
                x = random.randint(self.rect.x + 20, self.rect.x + 40)
                y = self.rect.y - 20
            elif direction == "down":
                x = random.randint(self.rect.x + 20, self.rect.x + 40)
                y = self.rect.y + self.rect.h - 30
            if self.special > 0:
                PlayerBullet(x, y, t, 5, direction)
                self.shoot_cooldown = 0
            else:
                PlayerBullet(x, y, t, speed, direction)
                self.shoot_cooldown = 20

    # Границы персонажа
    def get_borders(self):
        x = self.rect.x
        y = self.rect.y
        w = self.rect.w
        h = self.rect.h
        self.upper_border.image = pygame.Surface([w, 3])
        self.lower_border.image = pygame.Surface([w, 3])
        self.upper_border.rect = pygame.Rect(x, y, w, 3)
        self.lower_border.rect = pygame.Rect(x, y + h, w, 3)

    # меняем комнату
    def change_room(self, a):
        for _ in chest:
            _.close_chest()
        for _ in player_bullets:
            all_sprites.remove(_)
        for _ in special:
            _.kill()
        player_bullets.empty()
        global beguni, strelky
        if a == (0, 1):
            if self.room == self.lift:
                self.exit.kill()
            self.room += 3
            self.rect.x = 30
            self.rect.y = 280
        elif a == (0, -1):
            if self.room == self.lift:
                self.exit.kill()
            self.room -= 3
            self.rect.x = 430
            self.rect.y = 450
        elif a == (1, 0):
            if self.room == self.lift:
                self.exit.kill()
            self.room += 1
            self.rect.x = 450
            self.rect.y = 30

        elif a == (-1, 0):
            if self.room == self.lift:
                self.exit.kill()
            self.room -= 1
            self.rect.x = 700
            self.rect.y = 280

        else:
            pass
        self.is_change = True

        beguni = pygame.sprite.Group()
        strelky = pygame.sprite.Group()
        mobs = self.floor[self.room]

        for count in range(mobs[0]):
            mob = Strelyaet(strelky, random.randint(100, 800), random.randint(80, 430),
                            load_image('sold1.bmp', -1), 4, 4,
                            5 - count + usuf.main_floor // 2)
        for count in range(mobs[1]):
            mob = Begaet(beguni, random.randint(200, 700), random.randint(150, 300),
                         load_image('kek.png', -1), 4, 4,
                         13 - count + usuf.main_floor // 2)
        global hod_down, hod_left, hod_up, hod_right, life
        life = pygame.sprite.Group()
        hod_up = pygame.sprite.Group()
        hod_down = pygame.sprite.Group()
        hod_left = pygame.sprite.Group()
        hod_right = pygame.sprite.Group()
        image = pygame.transform.scale(load_image('vorota.png', -1), (60, 60))
        if self.room not in [0, 1, 2]:
            hod = pygame.sprite.Sprite()
            hod.image = image
            hod.rect = hod.image.get_rect()
            hod.rect.x = 450
            hod.rect.y = -20
            hod_up.add(hod)
        if self.room not in [0, 3, 6]:
            hod = pygame.sprite.Sprite()
            hod.image = image
            hod.rect = hod.image.get_rect()
            hod.rect.x = 15
            hod.rect.y = 280
            hod_left.add(hod)
        if self.room not in [6, 7, 8]:
            hod = pygame.sprite.Sprite()
            hod.image = image
            hod.rect = hod.image.get_rect()
            hod.rect.x = 450
            hod.rect.y = 470
            hod_down.add(hod)
        if self.room not in [2, 5, 8]:
            hod = pygame.sprite.Sprite()
            hod.image = image
            hod.rect = hod.image.get_rect()
            hod.rect.x = 890
            hod.rect.y = 280
            hod_right.add(hod)
        global patrons, keys
        patrons = pygame.sprite.Group()
        # лифт на следующий этаж
        if self.room == self.lift:
            self.exit = pygame.sprite.Sprite()
            self.exit.image = pygame.transform.scale(load_image('luk.png', -1), (60, 60))
            self.exit.rect = self.exit.image.get_rect()
            self.exit.rect.x = width - 200
            self.exit.rect.y = height - 200
        keys = pygame.sprite.Group()

    # меняем этаж
    def floor_change(self):
        self.picked = False
        self.floor = {}
        self.keys = 0
        self.special_bullet = random.randint(0, 9)
        self.list_life = [False for i in range(9)]
        usuf.map.list = []
        self.all_keys = 8
        self.list_keys = [random.randint(0, 8) for i in range(self.all_keys)]
        self.lift = random.randint(0, 8)
        # идет распределение мобов и ключей по комнатам
        for i in range(9):
            list_keys = []
            for u in range(len(self.list_keys)):
                if (self.list_keys[u] == i):
                    list_keys.append(u)
            strelki = random.randint(2, 3 + self.main_floor // 2)
            beguni = random.randint(2, 4 + self.main_floor // 2)
            if (i == self.lift):
                self.floor[i] = (strelki, beguni, True, False, list_keys)
            else:
                self.floor[i] = (strelki, beguni, False, False, list_keys)
        self.change_room((0, 0))
        self.floor_update()
        self.life = min(100, self.life + 10)

    def floor_update(self):
        self.main_floor += 1


a = Chest(200, 200)
chest = pygame.sprite.Group()
chest.add(a)

hole1 = BigHole(361, 220, 270, 85)
hole2 = BigHole(439, 160, 110, 215)
usuf = Player((50, 50), 0)
patrons = pygame.sprite.Group()
strelky = pygame.sprite.Group()


# пули крипов
class Patrons(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image("pula_migela.png", -1), (80, 80))

    def __init__(self, list, group):
        super().__init__(group)
        self.list = list
        self.image = Patrons.image
        self.rect = self.image.get_rect()
        self.rect.x = self.list[0][0]
        self.rect.y = self.list[0][1]

    def update(self):
        self.rect.x += self.list[1][0] // 2
        self.rect.y += self.list[1][1] // 2
        if (pygame.sprite.collide_mask(self, usuf)):
            usuf.life -= 2 * difficulty
            self.kill()
        if (
                                self.rect.x <= 30 or self.rect.x >= width - 30 or self.rect.y <= 30 or self.rect.y >= height - 30):
            self.kill()


# бегающие мобы
class Begaet(pygame.sprite.Sprite):
    image = load_image("kek.png", -1)

    def __init__(self, group, x, y, sheet, columns, rows, speed):
        super().__init__(group)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.speed = speed

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))

    def move(self):
        a = usuf.rect.x
        b = usuf.rect.y
        if self.rect.x < a:
            self.rect.x += 1
        elif self.rect.x > a:
            self.rect.x -= 1
        if self.rect.y < b:
            self.rect.y += 1
        elif self.rect.y > b:
            self.rect.y -= 1

    def update(self):
        x = usuf.rect.x - self.rect.x
        y = usuf.rect.y - self.rect.y
        if (x == 0 and y == 0):
            pass
        else:
            if (x * y < 0):
                if (x <= 0):
                    if (abs(x) > abs(y)):
                        self.left()
                    else:
                        self.forward()
                else:
                    if (abs(x) > abs(y)):
                        self.right()
                    else:
                        self.back()
            else:
                if (abs(x) > abs(y)):
                    if (x >= 0):
                        self.right()
                    else:
                        self.left()
                else:
                    if (x >= 0):
                        self.forward()
                    else:
                        self.back()

    def left(self):
        self.cur_frame += 1
        self.image = self.frames[4 + (self.cur_frame + 1) % 4]
        self.rect.x -= self.speed
        s = random.randint(0, 3)

    def right(self):
        self.cur_frame += 1
        self.image = self.frames[8 + (self.cur_frame + 1) % 4]
        self.rect.x += self.speed

    def back(self):
        self.cur_frame += 1
        self.image = self.frames[12 + (self.cur_frame + 1) % 4]
        self.rect.y -= self.speed
        s = random.randint(0, 3)

    def forward(self):
        self.cur_frame += 1
        self.image = self.frames[0 + (self.cur_frame + 1) % 4]
        self.rect.y += self.speed
        s = random.randint(0, 3)


keys = pygame.sprite.Group()


# ключи
class Keys(pygame.sprite.Sprite):
    def __init__(self, group, sheet, columns, rows, frame, x, y):
        super().__init__(group)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = frame
        self.image = self.frames[random.randint(0, 3)]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))


# стрелки
class Strelyaet(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image('migel.png', -1), (50, 50))
    image.set_colorkey((255, 255, 255))

    def __init__(self, group, x, y, sheet, columns, rows, speed):
        super().__init__(group)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.speed = speed
        self.start_coords_x = max(30, x - 80)
        self.start_coords_y = max(30, y - 80)
        self.finish_coords_x = min(width - 30, x + 80)
        self.finish_coords_y = min(height - 30, y + 80)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self, shoot=False):
        x = usuf.rect.x - self.rect.x
        y = usuf.rect.y - self.rect.y
        if x == 0 and y == 0:
            pass
        else:
            if x * y < 0:
                if x < 0:
                    if abs(x) > abs(y):
                        self.left()
                    else:
                        self.forward()
                else:
                    if abs(x) > abs(y):
                        self.right()
                    else:
                        self.back()
            else:
                if abs(x) > abs(y):
                    if x > 0:
                        self.right()
                    else:
                        self.left()
                else:
                    if x > 0:
                        self.forward()
                    else:
                        self.back()
        if (shoot):
            # расчитывается координаты вектора на который смещается пуля
            start_pos = (self.rect.x, self.rect.y)
            cel_x = usuf.rect.x - self.rect.x + 16
            cel_y = usuf.rect.y - self.rect.y + 24
            put = math.sqrt(cel_x ** 2 + cel_y ** 2)
            speed = (int(cel_x * (30 / put)), int(cel_y * (30 / put)))
            Patrons([start_pos, speed], patrons)
            cel_x = usuf.rect.x - self.rect.x + 16 + 150
            cel_y = usuf.rect.y - self.rect.y + 24 + 150
            put = math.sqrt(cel_x ** 2 + cel_y ** 2)
            speed = (int(cel_x * (30 / put)), int(cel_y * (30 / put)))
            Patrons([start_pos, speed], patrons)
            cel_x = usuf.rect.x - self.rect.x + 16 - 150
            cel_y = usuf.rect.y - self.rect.y + 24 - 150
            put = math.sqrt(cel_x ** 2 + cel_y ** 2)
            speed = (int(cel_x * (30 / put)), int(cel_y * (30 / put)))
            Patrons([start_pos, speed], patrons)
            cel_x = usuf.rect.x - self.rect.x + 16 + 150
            cel_y = usuf.rect.y - self.rect.y + 24 - 150
            put = math.sqrt(cel_x ** 2 + cel_y ** 2)
            speed = (int(cel_x * (30 / put)), int(cel_y * (30 / put)))
            Patrons([start_pos, speed], patrons)
            cel_x = usuf.rect.x - self.rect.x + 16 - 150
            cel_y = usuf.rect.y - self.rect.y + 24 + 150
            put = math.sqrt(cel_x ** 2 + cel_y ** 2)
            speed = (int(cel_x * (30 / put)), int(cel_y * (30 / put)))
            Patrons([start_pos, speed], patrons)

        else:
            pass

    def left(self):
        self.cur_frame += 1
        self.image = self.frames[4 + (self.cur_frame + 1) % 4]
        if (self.rect.x - self.speed >= self.start_coords_x):
            self.rect.x -= self.speed

    def right(self, shag=5):
        self.cur_frame += 1
        self.image = self.frames[8 + (self.cur_frame + 1) % 4]
        if (self.rect.x + self.speed <= self.finish_coords_x):
            self.rect.x += self.speed

    def back(self, shag=5):
        self.cur_frame += 1
        self.image = self.frames[12 + (self.cur_frame + 1) % 4]
        if (self.rect.y - self.speed >= self.start_coords_y):
            self.rect.y -= self.speed

    def forward(self, shag=5):
        self.cur_frame += 1
        self.image = self.frames[0 + (self.cur_frame + 1) % 4]
        if self.rect.y + self.speed <= self.finish_coords_y:
            self.rect.y += self.speed


beguni = pygame.sprite.Group()


def main():
    Border(50, 30, width - 60, 30)
    Border(50, height - 143, width - 60, height - 143)
    Border(50, 30, 50, height - 143)
    Border(width - 60, 30, width - 60, height - 143)
    Border(5, 5, 5, height - 5)
    Border(5, 5, width - 5, 5)
    Border(5, height - 5, width - 5, height - 5)
    Border(width - 5, 5, width - 5, height - 5)
    clock = pygame.time.Clock()
    running = True
    MYEVENTTYPE = 30
    pygame.time.set_timer(MYEVENTTYPE, 100)
    Puliupdate = 29
    pygame.time.set_timer(Puliupdate, 1000)
    BEGUNI = 28
    pygame.time.set_timer(BEGUNI, 100)
    usuf.is_change = True
    usuf.floor_change()
    is_grob = False
    grob = pygame.sprite.Group()
    is_usuf_killed = False

    while running:

        screen.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == MYEVENTTYPE and not is_usuf_killed:
                strelky.update()
                patrons.update()
                beguni.update()
                if usuf.life <= 0:
                    x = usuf.rect.x
                    y = usuf.rect.y
                    usuf.life = 0
                    sprite = pygame.sprite.Sprite()
                    sprite.image = pygame.transform.scale(load_image('grob.jpg', -1), (80, 80))
                    sprite.rect = sprite.image.get_rect()
                    sprite.rect.x = x
                    sprite.rect.y = y
                    grob.add(sprite)
                    is_grob = True
                    get_record()

                pygame.time.set_timer(MYEVENTTYPE, 100)
            if event.type == Puliupdate:
                strelky.update(True)
                pygame.time.set_timer(Puliupdate, 1500)
            if event.type == pygame.KEYDOWN:
                if event.key == 103:
                    if pygame.sprite.spritecollideany(usuf, hod_right) is not None:
                        usuf.change_room((1, 0))
                        usuf.rect.x = 15 + 45
                        usuf.rect.y = 280
                    elif pygame.sprite.spritecollideany(usuf, hod_left) is not None:
                        usuf.change_room((-1, 0))
                        usuf.rect.x = 880 - 60
                        usuf.rect.y = 280
                    elif pygame.sprite.spritecollideany(usuf, hod_up) is not None:
                        usuf.change_room((0, -1))
                        usuf.rect.x = 450
                        usuf.rect.y = 470 - 40
                    elif pygame.sprite.spritecollideany(usuf, hod_down) is not None:
                        usuf.change_room((0, 1))
                        usuf.rect.x = 450
                        usuf.rect.y = 10 + 2
                elif event.key == ord('o'):
                    if (usuf.room == usuf.lift and len(
                            usuf.map.list) == usuf.all_keys and
                                pygame.sprite.collide_mask(usuf, usuf.exit)
                            is not None):
                        usuf.floor_change()
                        usuf.change_room((0, 0))
                if event.key == pygame.K_ESCAPE:
                    pause_game()

            if event.type == BEGUNI and not is_usuf_killed:
                x = pygame.sprite.spritecollide(usuf, beguni, False)
                if usuf.life - len(x) * 6 <= 0:
                    x = usuf.rect.x
                    y = usuf.rect.y
                    is_usuf_killed = True
                    usuf.life = 0
                    sprite = pygame.sprite.Sprite()
                    sprite.image = pygame.transform.scale(load_image('grob.jpg', -1), (80, 80))
                    sprite.rect = sprite.image.get_rect()
                    sprite.rect.x = x
                    sprite.rect.y = y
                    grob.add(sprite)
                    is_grob = True
                    get_record()
                else:
                    if x != []:
                        usuf.life -= len(x) * 2 * difficulty

                pygame.time.set_timer(BEGUNI, 200)
        # открытие сундуков и дроп с них
        if usuf.is_change and usuf.floor[usuf.room][0] == 0 and usuf.floor[usuf.room][1] == 0:
            usuf.floor[usuf.room] = [usuf.floor[usuf.room][0], usuf.floor[usuf.room][1],
                                     usuf.floor[usuf.room][2], True,
                                     usuf.floor[usuf.room][4]]
            for _ in chest:
                if usuf.floor[usuf.room][3]:
                    _.open_chest()
                    if usuf.room == usuf.special_bullet and usuf.picked is False:
                        spec = Special()
                        if pygame.sprite.spritecollideany(usuf, special):
                            print(1)
                            spec.get(usuf.room)
                            usuf.picked = True
                    if not usuf.list_life[usuf.room]:
                        hil = Heal()
                    if pygame.sprite.spritecollideany(usuf, life) is not None:
                        usuf.list_life[usuf.room] = True
                        hil.get(usuf.room)
                    for u in (usuf.floor[usuf.room][4]):
                        if u not in usuf.map.list:
                            key = Keys(keys, load_image('keys.bmp', -1), 4, 1, u,
                                       random.randint(80, 200),
                                       random.randint(80, 200))

            usuf.is_change = False
        try:
            usuf.get_event_keyboard(pygame.key.get_pressed())
        except Exception:
            return
        screen.blit(room_image, (0, 0))
        all_sprites.draw(screen)
        for _ in mob_group:
            _.move()
        objects.update()
        chest.draw(screen)
        all_sprites.update()
        objects.update()
        strelky.draw(screen)
        patrons.draw(screen)
        beguni.draw(screen)
        special.draw(screen)
        usuf.map.life(usuf.life)
        usuf.map.minimap(usuf.room)
        usuf.map.inventar()
        hod_down.draw(screen)
        hod_up.draw(screen)
        hod_left.draw(screen)
        chest.draw(screen)
        hod_right.draw(screen)
        if usuf.floor[usuf.room][2]:
            screen.blit(usuf.exit.image, usuf.exit.rect)
        x = pygame.sprite.spritecollide(usuf, beguni, False)
        lifes_get = pygame.sprite.spritecollide(usuf, life, False)
        if len(lifes_get) != 0:
            hil.get(usuf.room)
            usuf.list_life[usuf.room] = True
        if is_grob:
            grob.draw(screen)
        keys.draw(screen)
        life.draw(screen)
        for i in pygame.sprite.spritecollide(usuf, keys, False):
            usuf.map.list.append(i.cur_frame)
        pygame.sprite.spritecollide(usuf, keys, True)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


start_screen()
