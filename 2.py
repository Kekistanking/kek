import pygame
import os

running = True

fps = 60

pygame.init()
size = width, height = 960, 540
screen = pygame.display.set_mode(size)
cords = 0, 0
all_sprites=pygame.sprite.Group()
def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image
class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def left(self):
        self.cur_frame+=1
        self.image = self.frames[4+(self.cur_frame + 1) %4]

    def right(self):
        self.cur_frame+=1
        self.image = self.frames[8+(self.cur_frame + 1) %4]


    def back(self):
        self.cur_frame+=1
        self.image = self.frames[12+(self.cur_frame + 1) %4]

    def forward(self):
        self.cur_frame+=1
        self.image = self.frames[0+(self.cur_frame + 1)%4]

a=AnimatedSprite(load_image('sold.jpg'),4,4,50,50)

clock = pygame.time.Clock()
MYEVENTTYPE=30
pygame.time.set_timer(MYEVENTTYPE, 500)
list=['left','forward','back','right']
k=0
s='left'

while running:
    screen.fill((255,255,255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if(event.type==MYEVENTTYPE):
            s=list[(k+1)%4]
            pygame.time.set_timer(MYEVENTTYPE, 500)
            k+=1
    if(s=='left'):
        a.left()
    if(s=='right'):
        a.right()
    if(s=='forward'):
        a.forward()
    if(s=='back'):
        a.back()


    all_sprites.draw(screen)
    pygame.display.flip()

