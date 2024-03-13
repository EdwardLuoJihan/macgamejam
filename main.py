import pygame, sys
from pygame.locals import QUIT

pygame.init()
wn = pygame.display.set_mode((1300, 800))
pygame.display.set_caption('Angels & Demons')


#image load
#tile dimensions - 64 x 143
#border dimensions - 350 x 800
#23 x 77 for tile spawn within border
ptile = "assets/images/tile.png"
pborder = "assets/images/purgborder.png"
hborder = "assets/images/heavenborder.png"
hlborder = "assets/images/hellborder.png"

border = pygame.image.load(pborder).convert()
wn.blit(border, (475, 0))

tile = pygame.image.load(ptile).convert()
wn.blit(tile, (475+23, 77))

hborder = pygame.image.load(hborder).convert()
wn.blit(hborder, (0, 0))

hlborder = pygame.image.load(hlborder).convert()
wn.blit(hlborder, (825, 0))


while True:
   for event in pygame.event.get():
       if event.type == QUIT:
           pygame.quit()
           sys.exit()
   pygame.display.update()