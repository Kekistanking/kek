import pygame
import random
import os
import math

FPS = 80

pygame.init()
size = width, height = 960, 540
screen = pygame.display.set_mode(size)
const = 3
mobs = pygame.sprite.Group()

all_sprites = pygame.sprite.Group()
mob_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
player_bullets = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
objects = pygame.sprite.Group()


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


room_image = load_image("room1.bmp")
room_image = pygame.transform.scale(room_image, (960, 540))


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


class StaticObject(pygame.sprite.Sprite):
    def __init__(self, sheet, x, y):
        super().__init__(objects, all_sprites)
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


class Chest(StaticObject):
    sheet = load_image("chest2.bmp")

    def __init__(self, x, y):
        super().__init__(Chest.sheet, x, y)
        self.get_rect(48, 40)
        self.cut_sheet(2, 1, 30, 32, 48, 40, 1, 0)
        self.image = self.frames[0]
        self.counter = 0
        self.get_borders()

    def update(self):
        self.counter += 1
        phase = (self.counter // 80) % 2
        if self.counter > 160:
            self.counter -= 160
        self.image = self.frames[phase]


class BigHole(StaticObject):
    sheet = load_image("chest2.bmp")

    def __init__(self, x, y, tw, th):
        super().__init__(Chest.sheet, x, y)
        self.get_rect(tw, th)
        self.image= pygame.Surface([0, 0])
        #self.image = pygame.Surface([self.rect.w, self.rect.h])
        self.get_borders(12, 25)


class Player(pygame.sprite.Sprite):
    sheet = load_image("playersanim.bmp", -1)

    def __init__(self, cords):
        super().__init__(player_group, all_sprites)
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
            else:
                self.move_counter = 0
                self.move_left = False
                self.move_right = False
                self.move_up = False
                self.move_down = True
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
            else:
                self.move_counter = 0
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

    def update(self):
        movement_phase = (self.move_counter // 4) % 8
        movement_phase_slow = (self.move_counter // 8) % 8
        dx = self.change[0] * 5
        dy = self.change[1] * 5
        self.rect.x += dx
        self.rect.y += dy
        if self.move_up:
            if pygame.sprite.spritecollideany(self.upper_border, horizontal_borders):
                self.rect.y -= dy
                self.image = self.images_up[movement_phase_slow]
            else:
                self.image = self.images_up[movement_phase]
            if self.move_right or self.move_left:
                if pygame.sprite.spritecollideany(self, vertical_borders):
                    self.rect.x -= dx
        elif self.move_down:
            if pygame.sprite.spritecollideany(self.lower_border, horizontal_borders):
                self.rect.y -= dy
                self.image = self.images_down[movement_phase_slow]
            else:
                self.image = self.images_down[movement_phase]
            if self.move_right or self.move_left:
                if pygame.sprite.spritecollideany(self, vertical_borders):
                    self.rect.x -= dx

        elif self.move_right:
            if pygame.sprite.spritecollideany(self, vertical_borders):
                self.rect.x -= dx
                self.image = self.images_right[movement_phase_slow]
            else:
                self.image = self.images_right[movement_phase]
            if pygame.sprite.spritecollideany(self, horizontal_borders):
                self.rect.y -= dy
        elif self.move_left:
            if pygame.sprite.spritecollideany(self, vertical_borders):
                self.rect.x -= dx
                self.image = self.images_left[movement_phase_slow]
            else:
                self.image = self.images_left[movement_phase]
            if pygame.sprite.spritecollideany(self, horizontal_borders):
                self.rect.y -= dy

        self.change = [0, 0]
        self.get_borders()

    def cut_sheet(self, sheet, columns, rows):
        w = sheet.get_width() // columns
        h = sheet.get_height() // rows
        for j in range(rows):
            temp = []
            for i in range(columns):
                a = sheet.subsurface(pygame.Rect((w * i +
                                                  17, h * j + 15), (32, 48)))
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

    def shoot(self):
        pass

    def get_borders(self):
        x = self.rect.x
        y = self.rect.y
        w = self.rect.w
        h = self.rect.h
        self.upper_border.image = pygame.Surface([w, 3])
        self.lower_border.image = pygame.Surface([w, 3])
        self.upper_border.rect = pygame.Rect(x, y, w, 3)
        self.lower_border.rect = pygame.Rect(x, y + h, w, 3)


a = Chest(200, 200)
hole1 = BigHole(361, 220, 270, 85)
hole2 = BigHole(439, 160, 110, 215)
usuf = Player((100, 100))
patrons = pygame.sprite.Group()
strelky = pygame.sprite.Group()


class Patrons(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image("pula_migela.png"), (20, 10))

    def __init__(self, list, group):
        super().__init__(group)
        self.list = list
        self.image = Patrons.image
        self.rect = self.image.get_rect()
        self.rect.x = self.list[0][0]
        self.rect.y = self.list[0][1]

    def update(self):
        self.rect.x += self.list[1][0]
        self.rect.y += self.list[1][1]


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
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

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
        if (len(pygame.sprite.spritecollide(self, beguni, False)) > 1):
            self.right()

    def right(self):
        self.cur_frame += 1
        self.image = self.frames[8 + (self.cur_frame + 1) % 4]
        self.rect.x += self.speed
        if (len(pygame.sprite.spritecollide(self, beguni, False)) > 1):
            self.left()

    def back(self):
        self.cur_frame += 1
        self.image = self.frames[12 + (self.cur_frame + 1) % 4]
        self.rect.y -= self.speed
        s = random.randint(0, 3)
        if (len(pygame.sprite.spritecollide(self, beguni, False)) > 1):
            self.forward()

    def forward(self):
        self.cur_frame += 1
        self.image = self.frames[0 + (self.cur_frame + 1) % 4]
        self.rect.y += self.speed
        s = random.randint(0, 3)
        if (len(pygame.sprite.spritecollide(self, beguni, False)) > 1):
            self.back()


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
        if (x == 0 and y == 0):
            pass
        else:
            if (x * y < 0):
                if (x < 0):
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
                    if (x > 0):
                        self.right()
                    else:
                        self.left()
                else:
                    if (x > 0):
                        self.forward()
                    else:
                        self.back()
        if (shoot):
            start_pos = (self.rect.x, self.rect.y)
            cel_x = usuf.rect.x - self.rect.x + 16 + random.randint(-32, 32)
            cel_y = usuf.rect.y - self.rect.y + 24 + random.randint(-48, 48)
            put = math.sqrt(cel_x ** 2 + cel_y ** 2)

            speed = (int(cel_x * (30 / put)), int(cel_y * (30 / put)))
            Patrons([start_pos, speed], patrons)
        else:
            pass

    def left(self):
        self.cur_frame += 1
        self.image = self.frames[4 + (self.cur_frame + 1) % 4]
        self.rect.x -= self.speed
        s = random.randint(0, 3)
        if (len(pygame.sprite.spritecollide(self, strelky, False)) > 1):
            self.right()

    def right(self, shag=5):
        self.cur_frame += 1
        self.image = self.frames[8 + (self.cur_frame + 1) % 4]
        self.rect.x += self.speed
        if (len(pygame.sprite.spritecollide(self, strelky, False)) > 1):
            self.left()

    def back(self, shag=5):
        self.cur_frame += 1
        self.image = self.frames[12 + (self.cur_frame + 1) % 4]
        self.rect.y -= self.speed
        s = random.randint(0, 3)
        if (len(pygame.sprite.spritecollide(self, strelky, False)) > 1):
            self.forward(10)

    def forward(self, shag=5):
        self.cur_frame += 1
        self.image = self.frames[0 + (self.cur_frame + 1) % 4]
        self.rect.y += self.speed
        s = random.randint(0, 3)
        if (len(pygame.sprite.spritecollide(self, strelky, False)) > 1):
            self.back(10)


sunduki = pygame.sprite.Group()

beguni = pygame.sprite.Group()
Border(50, 30, width - 60, 30)
Border(50, height - 63, width - 60, height - 63)
Border(50, 30, 50, height - 63)
Border(width - 60, 30, width - 60, height - 63)

clock = pygame.time.Clock()
running = True
MYEVENTTYPE = 30
pygame.time.set_timer(MYEVENTTYPE, 200)
Puliupdate = 29
pygame.time.set_timer(Puliupdate, 1000)
while running:
    screen.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if (event.type == MYEVENTTYPE):
            strelky.update()
            patrons.update()
            beguni.update()
            pygame.time.set_timer(MYEVENTTYPE, 200)
        if (event.type == Puliupdate):
            strelky.update(True)
            sunduki.update()
            pygame.time.set_timer(Puliupdate, 1500)

    usuf.get_event_keyboard(pygame.key.get_pressed())
    screen.blit(room_image, (0, 0))
    all_sprites.draw(screen)
    for _ in mob_group:
        _.move()
    objects.update()
    all_sprites.update()
    strelky.draw(screen)
    patrons.draw(screen)
    beguni.draw(screen)
    sunduki.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
