import pygame
import random
import os
import math

FPS = 60
pygame.init()
size = width, height = 800, 600
screen = pygame.display.set_mode(size)
const = 3
mobs = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()


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
            colorkey = image.get_at((0, 0))

    return image


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 30

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self):

        for i in range(self.height):
            for q in range(self.width):
                x = (self.cell_size, self.cell_size)
                start = (self.left + self.cell_size * q, self.top + self.cell_size * i)
                pygame.draw.rect(screen, pygame.Color(255, 255, 255), start + x, 1)


class Player(pygame.sprite.Sprite):
    image = load_image("Pudge.png")
    images_down = []
    images_up = []
    images_left = []
    images_right = []
    for i in range(8):
        images_up.append(load_image("back_%d.png" % i))
        images_down.append(load_image("back_%d.png" % i))
        images_left.append(load_image("back_%d.png" % i))
        images_right.append(load_image("back_%d.png" % i))

    def __init__(self, cords):
        super().__init__(all_sprites)
        self.image = Player.image
        self.x = cords[0]
        self.y = cords[1]
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.move_counter = 0
        self.move_left = False
        self.move_right = False
        self.move_up = False
        self.move_down = True


    def get_event_keyboard(self, array):
        if array[pygame.K_w] == array[pygame.K_s]:
            if array[pygame.K_a] == 1 and array[pygame.K_d] == 0:
                self.rect.x -= 1
                if self.move_left:
                    self.move_counter += 1
                else:
                    self.move_counter = 0
                    self.move_left = True
                    self.move_right = False
                    self.move_up = False
                    self.move_down = False
            elif array[pygame.K_a] == 0 and array[pygame.K_d] == 1:
                self.rect.x += 1
                if self.move_right:
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
                self.rect.y -= 1
                if self.move_up:
                    self.move_counter += 1
                else:
                    self.move_counter = 0
                    self.move_left = False
                    self.move_right = False
                    self.move_up = True
                    self.move_down = False
            elif array[pygame.K_w] == 0 and array[pygame.K_s] == 1:
                self.rect.y += 1
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
                self.rect.y += 1
                self.rect.x -= 1
                if self.move_down:
                    self.move_counter += 1
                else:
                    self.move_counter = 0
                    self.move_left = False
                    self.move_right = False
                    self.move_up = False
                    self.move_down = True
            elif array[pygame.K_s] == array[pygame.K_d] == 1:
                self.rect.y += 1
                self.rect.x += 1
                if self.move_down:
                    self.move_counter += 1
                else:
                    self.move_counter = 0
                    self.move_left = False
                    self.move_right = False
                    self.move_up = False
                    self.move_down = True
            elif array[pygame.K_w] == array[pygame.K_a] == 1:
                self.rect.y -= 1
                self.rect.x -= 1
                if self.move_up:
                    self.move_counter += 1
                else:
                    self.move_counter = 0
                    self.move_left = False
                    self.move_right = False
                    self.move_up = True
                    self.move_down = False
            elif array[pygame.K_w] == array[pygame.K_d] == 1:
                self.rect.y -= 1
                self.rect.x += 1
                if self.move_up:
                    self.move_counter += 1
                else:
                    self.move_counter = 0
                    self.move_left = False
                    self.move_right = False
                    self.move_up = True
                    self.move_down = False

    def update(self):
        self.move_counter = self.move_counter % 8
        if self.move_up:
            self.image = Player.images_up[self.move_counter]
        elif self.move_down:
            self.image = Player.images_down[self.move_counter]
        elif self.move_right:
            self.image = Player.images_right[self.move_counter]
        elif self.move_left:
            self.image = Player.images_left[self.move_counter]


usuf = Player((20, 20))


class mob(pygame.sprite.Sprite):
    def __init__(self):
        self.list=[]
        self.patrons_list=[]
        self.sprites=pygame.sprite.Group()

    def update_person(self,number):
        if(self.list[number][2]=='migel_strelok'):
            start_coords=self.list[number][0][0],self.list[number][0][1]
            finish_coords=usuf.rect.x,usuf.rect.y


            speed=(finish_coords[0]-start_coords[0])/10,(finish_coords[1]-start_coords[1])/10


            mobs.patrons_list.append([start_coords,speed,'patron'])
    def update_patrons(self):
        i=0
        global height,width
        while(i<(len(self.patrons_list))):

            if(self.patrons_list[i][-1]=='patron'):

                if(self.patrons_list[i][0][0]>width or self.patrons_list[i][0][0]<0 or self.patrons_list[i][0][1]>height or self.patrons_list[i][0][1]<0):
                    del self.patrons_list[i]
                    i-=1
                else:
                    k=self.patrons_list[i][0]
                    s=self.patrons_list[i][1]
                    self.patrons_list[i][0]=(k[0]+s[0]*0.5,k[1]+s[1]*0.5)

            i+=1



    def render(self):
        self.sprites=pygame.sprite.Group()
        for i in range(len(self.list)):
            if(self.list[i][-1]=='migel_strelok'):
                sprite=pygame.sprite.Sprite()
                sprite.image=pygame.transform.scale(load_image('migel.png'),(50,50))
                sprite.rect=sprite.image.get_rect()
                sprite.rect.x=self.list[i][0][0]
                sprite.rect.y=self.list[i][0][1]
                self.sprites.add(sprite)
        for i in range(len(self.patrons_list)):
            if(self.patrons_list[i][-1]=='patron'):
                sprite=pygame.sprite.Sprite()
                sprite.image=pygame.transform.scale(load_image('pula_migela.png'),(40,20))
                sprite.rect=sprite.image.get_rect()
                sprite.rect.x=self.patrons_list[i][0][0]
                sprite.rect.y=self.patrons_list[i][0][1]
                self.sprites.add(sprite)






mobs=mob()

class Begaet():
    image = load_image("migel.png", -1)
    def __init__(self, room, x, y):
        self.image = pygame.transform.scale(Begaet.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = self.x + room[0] * self.const
        self.rect.y = self.y + room[1] * self.const
        mobs.list.append([x,y,random.randint(10,20)])


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


class strelyaet():
    def __init__(self, room,  x=0, y=0):
        global const
        sprite = pygame.sprite.Sprite()
        sprite.image = load_image('migel.png',-1)
        sprite.rect = sprite.image.get_rect()
        self.x=max(random.randint(1,560),x)
        self.y=max(random.randint(1,560),y)
        sprite.rect.x = self.x + room[0] * const
        sprite.rect.y = self.y + room[1] * const
        mobs.list.append([(self.x,self.y),2000,'migel_strelok'])





clock = pygame.time.Clock()
running = True

strelyaet((3,4))
strelyaet((2,5))
strelyaet((7,19))
print (mobs.list)

all_time=0
MYEVENTTYPE_1=30
pygame.time.set_timer(MYEVENTTYPE_1,2000)
MYEVENTTYPE_2=31
pygame.time.set_timer(MYEVENTTYPE_2,500)
while running:
    screen.fill((255,255,255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == MYEVENTTYPE_1:
            all_time+=500
            for u in range(len(mobs.list)):
                if(mobs.list[u][1]<=all_time):
                    mobs.update_person(u)
                    mobs.list[u][1]=mobs.list[u][1]+5000
            pygame.time.set_timer(MYEVENTTYPE_1,2000)
        if event.type == MYEVENTTYPE_2:
             mobs.update_patrons()
             mobs.render()
             pygame.time.set_timer(MYEVENTTYPE_2,500)

    usuf.get_event_keyboard(pygame.key.get_pressed())

    all_sprites.draw(screen)
    mobs.sprites.draw(screen)
    all_sprites.update()
    pygame.display.flip()
    clock.tick(200)

pygame.quit()
