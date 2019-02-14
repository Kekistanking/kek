import pygame
import random
import os

FPS = 60

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
            self.image = pygame.Surface([3, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 3, y2 - y1)
        else:  # горизонтальная стенка
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


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
        self.rect.x = self.x
        self.rect.y = self.y
        self.move_counter = 0
        self.move_left = False
        self.move_right = False
        self.move_up = False
        self.move_down = True
        self.change = [0, 0]

    def get_event_keyboard(self, array):
        if array[pygame.K_w] == array[pygame.K_s]:
            if array[pygame.K_a] == 1 and array[pygame.K_d] == 0:
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
                    self.move_right = False
                    self.move_up = False
                    self.move_down = False
            elif array[pygame.K_a] == 0 and array[pygame.K_d] == 1:
                self.change[0] += 1
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
                    self.move_left = False
                    self.move_right = True
                    self.move_up = False
                    self.move_down = False
            else:
                self.move_counter = 0
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
            if pygame.sprite.spritecollideany(self, horizontal_borders):
                self.rect.y -= dy
                self.image = self.images_up[movement_phase_slow]
            else:
                self.image = self.images_up[movement_phase]
            if self.move_right or self.move_left:
                if pygame.sprite.spritecollideany(self, vertical_borders):
                    self.rect.x -= dx

        elif self.move_down:
            if pygame.sprite.spritecollideany(self, horizontal_borders):
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

    def cut_sheet(self, sheet, columns, rows):
        w = sheet.get_width() // columns
        h = sheet.get_height() // rows
        self.rect = pygame.Rect(0, 0, 32, 48)
        for j in range(rows):
            temp = []
            for i in range(columns):
                a = sheet.subsurface(pygame.Rect((w * i +
                                                  16, h * j + 14), self.rect.size))
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


usuf = Player((100, 100))


class Mob(pygame.sprite.Sprite):
    def __init__(self, room, activate, x, y):
        super().__init__(mob_group, all_sprites)
        self.coordinates_of_mob = []
        self.activate = activate
        self.room = room
        self.x = random.randint(0, 560)
        self.y = random.randint(0, 560)


class Begaet(Mob):
    image = load_image("Player.png", -1)

    def __init__(self, room, activate, x, y):
        super().__init__(room, activate, x, y)
        self.image = pygame.transform.scale(Begaet.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = self.x + room[0] * const
        self.rect.y = self.y + room[1] * const

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


class Strelyaet(Mob):
    def __init__(self, room, activate, x, y):
        super().__init__(room, activate, x, y)
        sprite = pygame.sprite.Sprite()
        sprite.image = Begaet.image
        sprite.rect = sprite.image.get_rect()
        sprite.rect.x = self.x + room[0] * const
        sprite.rect.y = self.y + room[1] * const


Border(50, 30, width - 98, 30)
Border(50, height - 60, width - 98, height - 60)
Border(50, 30, 50, height - 60)
Border(width - 98, 30, width - 98, height - 60)

clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    usuf.get_event_keyboard(pygame.key.get_pressed())
    screen.blit(room_image, (0, 0))
    all_sprites.draw(screen)
    for x in mob_group:
        x.move()
    all_sprites.update()
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
