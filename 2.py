import pygame
import os

running = True

fps = 60
clock = pygame.time.Clock()
pygame.init()
size = width, height = 300, 300
screen = pygame.display.set_mode(size)
screen.fill(pygame.Color("white"))
pygame.mouse.set_visible(False)
cords = 0, 0


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


image = load_image("creature.png")

while running:
    screen.fill(pygame.Color("white"))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    k = pygame.key.get_pressed()
    if k[pygame.K_UP] == 1:
        a, b = cords
        cords = a, b - 10
    if k[pygame.K_DOWN] == 1:
        a, b = cords
        cords = a, b + 10
    if k[pygame.K_RIGHT] == 1:
        a, b = cords
        cords = a + 10, b
    if k[pygame.K_LEFT] == 1:
        a, b = cords
        cords = a - 10, b
    screen.blit(image, cords)
    clock.tick(fps)
    pygame.display.flip()

pygame.quit()
