import pygame
import random
import os
import math

FPS = 80
pygame.init()
size = width, height = 960, 620
screen = pygame.display.set_mode(size)
const = 3
mobs = pygame.sprite.Group()
floor=0
all_sprites = pygame.sprite.Group()
mob_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
player_bullets = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
objects = pygame.sprite.Group()
hod_up=pygame.sprite.Group()
hod_down=pygame.sprite.Group()
hod_left=pygame.sprite.Group()
hod_right=pygame.sprite.Group()
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

class information_about_pers():
    def __init__(self,a,b):
        self.start_x=a
        self.start_y=b
        self.finish_x=width
        self.finish_y=height
    def minimap(self,room):
        for i in range(3):
            for u in range(3):
                if(i*3+u==room):
                    pygame.draw.rect(screen,(255,0,0),[self.start_x+(u*(height-self.start_y)//3),self.start_y+(i*(height-self.start_y)//3),(height-self.start_y)//3-1,(height-self.start_y)//3-1],0)
                else:
                    pygame.draw.rect(screen,(100,100,100),[self.start_x+(u*(height-self.start_y)//3),self.start_y+(i*(height-self.start_y)//3),(height-self.start_y)//3-1,(height-self.start_y)//3-1],0)
    def inventar(self):
        for i in range(3):
            for u in range(3):
                pygame.draw.rect(screen,(0,0,0),[self.finish_x-((i+1)*(height-self.start_y)//3),self.finish_y-((u+1)*(height-self.start_y)//3),(height-self.start_y)//3-1,(height-self.start_y)//3-1],0)

    def life(self,life):
        len=int(width-(self.finish_y-self.start_y)*2)
        green=int(len*(life/100))
        pygame.draw.rect(screen,(0,255,0),[self.start_x,self.start_y,self.finish_x,self.finish_y],0)
        if(life!=100):
            pygame.draw.rect(screen,(0,0,0),[green+self.finish_y-self.start_y,self.start_y,len-green,self.finish_y],0)

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

    def __init__(self, cords,room):
        super().__init__(player_group, all_sprites)
        self.main_floor=0
        self.room=room
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
        self.life=100
        self.is_change=True


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

    def cut_sheet(self, sheet, columns, rows,is_door=False):

            w = sheet.get_width() // columns
            h = sheet.get_height() // rows
            for j in range(rows):
                temp = []
                for i in range(columns):
                    a = sheet.subsurface(pygame.Rect((w * i +17, h * j + 15), (32, 48)))
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
    def change_room(self,a):
        global beguni,strelky
        if(a==(0,1)):
            if(self.room==self.lift):
                self.exit.kill()
            self.room+=3
            self.rect.x=15
            self.rect.y=280
        elif(a==(0,-1)):
            if(self.room==self.lift):
                self.exit.kill()
            self.room-=3
            self.rect.x=450
            self.rect.y=470
        elif(a==(1,0)):
            if(self.room==self.lift):
                self.exit.kill()
            self.room+=1
            self.rect.x=450
            self.rect.y=10

        elif(a==(-1,0)):
            if(self.room==self.lift):
                self.exit.kill()
            self.room-=1
            self.rect.x=880
            self.rect.y=280


        else:
            pass
        self.is_change=True

        beguni=pygame.sprite.Group()
        strelky=pygame.sprite.Group()
        mobs=self.floor[self.room]
        for count in range(mobs[0]):
            mob=Strelyaet(strelky,random.randint(30,900),random.randint(30,580),load_image('sold.bmp',-1),4,4,10-count)
        for count in range(mobs[1]):
            mob=Begaet(beguni,random.randint(30,900),random.randint(30,580),load_image('kek.png',-1),4,4,20-count)
        global hod_down,hod_left,hod_up,hod_right

        hod_up=pygame.sprite.Group()
        hod_down=pygame.sprite.Group()
        hod_left=pygame.sprite.Group()
        hod_right=pygame.sprite.Group()
        image=pygame.transform.scale(load_image('vorota.png',-1),(60,60))
        if(self.room not in [0,1,2]):
            hod=pygame.sprite.Sprite()
            hod.image= image
            hod.rect=hod.image.get_rect()
            hod.rect.x=450
            hod.rect.y=10
            hod_up.add(hod)
        if(self.room not in [0,3,6]):
            hod=pygame.sprite.Sprite()
            hod.image=image
            hod.rect=hod.image.get_rect()
            hod.rect.x=15
            hod.rect.y=280
            hod_left.add(hod)
        if(self.room not in [6,7,8]):
            hod=pygame.sprite.Sprite()
            hod.image=image
            hod.rect=hod.image.get_rect()
            hod.rect.x=450
            hod.rect.y=470
            hod_down.add(hod)
        if(self.room not in [2,5,8]):
            hod=pygame.sprite.Sprite()
            hod.image=image
            hod.rect=hod.image.get_rect()
            hod.rect.x=880
            hod.rect.y=280
            hod_right.add(hod)
        global patrons
        patrons=pygame.sprite.Group()
        if(self.room==self.lift):
            self.exit=pygame.sprite.Sprite()
            self.exit.image=pygame.transform.scale(load_image('exit.png',-1),(60,60))
            self.exit.rect=self.exit.image.get_rect()
            self.exit.rect.x=width-200
            self.exit.rect.y=height-200



    def floor_change(self):
        self.floor={}
        self.keys=0
        self.all_keys=random.randint(0,9)

        self.lift=random.randint(0,8)
        for i in range(9):
            strelki=random.randint(3,4)
            beguni=random.randint(2,4)
            if(i== self.lift):
                self.floor[i]=(strelki,beguni,True)
            else:
                self.floor[i]=(strelki,beguni,False)
        self.change_room((0,0))
        self.floor_update()
    def floor_update(self):
        self.main_floor+=1


room=-1
a = Chest(200, 200)
hole1 = BigHole(361, 220, 270, 85)
hole2 = BigHole(439, 160, 110, 215)
usuf = Player((50, 50),0)
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


class Ship(pygame.sprite.Sprite):
    image=load_image('ship.png',-1)
    def __init__(self, group, x, y):
        super().__init__(group)
        self.image=Ship.image
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
    def update(self):
        self.draw(screen)
ships=pygame.sprite.Group()

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
        self.start_coords_x=max(30,x-50)
        self.start_coords_y=max(30,y-50)
        self.finish_coords_x=min(width-30,x+50)
        self.finish_coords_y=min(height-30,y+50)

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
            cel_x = usuf.rect.x - self.rect.x + 16
            cel_y = usuf.rect.y - self.rect.y + 24
            put = math.sqrt(cel_x ** 2 + cel_y ** 2)
            speed = (int(cel_x * (30 / put)), int(cel_y * (30 / put)))
            Patrons([start_pos, speed], patrons)
            cel_x = usuf.rect.x - self.rect.x + 16+150
            cel_y = usuf.rect.y - self.rect.y + 24+150
            put = math.sqrt(cel_x ** 2 + cel_y ** 2)
            speed = (int(cel_x * (30 / put)), int(cel_y * (30 / put)))
            Patrons([start_pos, speed], patrons)
            cel_x = usuf.rect.x - self.rect.x + 16-150
            cel_y = usuf.rect.y - self.rect.y + 24-150
            put = math.sqrt(cel_x ** 2 + cel_y ** 2)
            speed = (int(cel_x * (30 / put)), int(cel_y * (30 / put)))
            Patrons([start_pos, speed], patrons)
            cel_x = usuf.rect.x - self.rect.x + 16+150
            cel_y = usuf.rect.y - self.rect.y + 24-150
            put = math.sqrt(cel_x ** 2 + cel_y ** 2)
            speed = (int(cel_x * (30 / put)), int(cel_y * (30 / put)))
            Patrons([start_pos, speed], patrons)
            cel_x = usuf.rect.x - self.rect.x + 16-150
            cel_y = usuf.rect.y - self.rect.y + 24+150
            put = math.sqrt(cel_x ** 2 + cel_y ** 2)
            speed = (int(cel_x * (30 / put)), int(cel_y * (30 / put)))
            Patrons([start_pos, speed], patrons)

        else:
            pass

    def left(self):
        self.cur_frame += 1
        self.image = self.frames[4 + (self.cur_frame + 1) % 4]
        if(self.rect.x-self.speed>=self.start_coords_x):
            self.rect.x -= self.speed



    def right(self, shag=5):
        self.cur_frame += 1
        self.image = self.frames[8 + (self.cur_frame + 1) % 4]
        if(self.rect.x+self.speed<=self.finish_coords_x):
            self.rect.x += self.speed


    def back(self, shag=5):
        self.cur_frame += 1
        self.image = self.frames[12 + (self.cur_frame + 1) % 4]
        if(self.rect.y-self.speed>=self.start_coords_y):
            self.rect.y -= self.speed



    def forward(self, shag=5):
        self.cur_frame += 1
        self.image = self.frames[0 + (self.cur_frame + 1) % 4]
        if(self.rect.y+self.speed<=self.finish_coords_y):
            self.rect.y += self.speed




sunduki = pygame.sprite.Group()
beguni = pygame.sprite.Group()
Border(50, 30, width - 60, 30)
Border(50, height - 143, width - 60, height - 143)
Border(50, 30, 50, height - 143)
Border(width - 60, 30, width - 60, height - 143)
clock = pygame.time.Clock()
running = True
MYEVENTTYPE = 30
pygame.time.set_timer(MYEVENTTYPE, 200)
Puliupdate = 29
pygame.time.set_timer(Puliupdate, 1000)
BEGUNI=28
pygame.time.set_timer(BEGUNI, 100)
map=information_about_pers(0,520)
usuf.is_change=True
usuf.floor_change()
usuf.change_room((1,0))
is_grob=False
grob=pygame.sprite.Group()
is_usuf_killed=False
while running:
    screen.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if (event.type == MYEVENTTYPE and not is_usuf_killed):
            strelky.update()
            patrons.update()
            beguni.update()
            if(usuf.life<=10):
                x=pygame.sprite.spritecollide(usuf,patrons,False)
                if(usuf.life-len(x)*2<=0):
                    x=usuf.rect.x
                    y=usuf.rect.y
                    usuf.life=0
                    usuf.kill()
                    sprite=pygame.sprite.Sprite()
                    sprite.image=pygame.transform.scale(load_image('grob.jpg',-1),(80,80))
                    sprite.rect=sprite.image.get_rect()
                    sprite.rect.x=x
                    sprite.rect.y=y
                    grob.add(sprite)
                    is_grob=True
                else:
                    x=pygame.sprite.spritecollide(usuf,patrons,True)
                    if(x!=[]):
                        usuf.life-=len(x)*2



            else:
                x=pygame.sprite.spritecollide(usuf,patrons,True)
                if(x!=[]):
                    usuf.life-=len(x)*2



            pygame.time.set_timer(MYEVENTTYPE, 200)
        if (event.type == Puliupdate):
            strelky.update(True)
            pygame.time.set_timer(Puliupdate, 1500)
        if(event.type == pygame.KEYDOWN):
            if(event.key==103):
                if(pygame.sprite.spritecollideany(usuf,hod_right) is not None):
                    usuf.change_room((1,0))
                    usuf.rect.x=15+50
                    usuf.rect.y=280
                elif(pygame.sprite.spritecollideany(usuf,hod_left) is not None):
                    usuf.change_room((-1,0))
                    usuf.rect.x=880-50
                    usuf.rect.y=280
                elif(pygame.sprite.spritecollideany(usuf,hod_up) is not None):
                    usuf.change_room((0,-1))
                    usuf.rect.x=450
                    usuf.rect.y=470-50
                elif(pygame.sprite.spritecollideany(usuf,hod_down) is not None):
                    usuf.change_room((0,1))
                    usuf.rect.x=450
                    usuf.rect.y=10+50
            elif(event.key==ord('o')):
                if(usuf.room==usuf.lift and usuf.keys==usuf.all_keys and pygame.sprite.collide_mask(usuf,usuf.exit) is not None):
                    usuf.floor_change()
                    usuf.change_room((0,0))


            if(event.type==BEGUNI and not is_usuf_killed):
                 x=pygame.sprite.spritecollide(usuf,beguni,False)
                 if(usuf.life-len(x)*2<=0):
                        x=usuf.rect.x
                        y=usuf.rect.y
                        usuf.kill()
                        is_usuf_killed=True
                        usuf.life=0
                        sprite=pygame.sprite.Sprite()
                        sprite.image=pygame.transform.scale(load_image('grob.jpg',-1),(80,80))
                        sprite.rect=sprite.image.get_rect()
                        sprite.rect.x=x
                        sprite.rect.y=y
                        grob.add(sprite)
                        is_grob=True
                 else:
                        if(x!=[]):
                            usuf.life-=len(x)

                 pygame.time.set_timer(BEGUNI, 100)



    if(usuf.is_change and len(beguni)==0 and len(strelky)==0):
        sunduki.update()
        is_change=False
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
    ships.draw(screen)
    map.life(usuf.life)
    map.minimap(usuf.room)
    map.inventar()
    hod_down.draw(screen)
    hod_up.draw(screen)
    hod_left.draw(screen)
    hod_right.draw(screen)
    if(usuf.floor[usuf.room][-1]):
        screen.blit(usuf.exit.image,usuf.exit.rect)
    x=pygame.sprite.spritecollide(usuf,beguni,False)


    if(is_grob):
        grob.draw(screen)


    pygame.display.flip()
    clock.tick(60)

pygame.quit()
