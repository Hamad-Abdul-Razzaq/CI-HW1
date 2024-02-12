import pygame

screen = pygame.display.set_mode((0,0))
image = pygame.image.load("vk.jpeg")
size = image.get_size()
screen = pygame.display.set_mode((size[0]*5, size[1]*4))
r = 0
c = 0
for i in range(1,21):
    image = pygame.image.load(f"vk_0_{500*i}.jpg")
    screen.blit(image, (size[0]*c, size[1]*r))
    c += 1
    if c == 5:
        c = 0
        r += 1
pygame.image.save(screen, "virat_kohli_all.jpg")
