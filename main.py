import pygame, sys
import pygame.midi
from pygame.locals import QUIT
import mido
import time

pygame.init()
wn = pygame.display.set_mode((1300, 800))
pygame.display.set_caption('Symphony of Seperation')


#image load
#tile dimensions - 64 x 143
#border dimensions - 350 x 800
#23 x 77 for tile spawn within border
ptileimg = "assets/images/tile.png"
pborder = "assets/images/purgborder.png"
hborder = "assets/images/heavenborder.png"
hlborder = "assets/images/hellborder.png"

border = pygame.image.load(pborder).convert_alpha()
wn.blit(border, (475, 0))

ptile = pygame.image.load(ptileimg).convert_alpha()
# wn.blit(ptile, (475+23, 77))

hborder = pygame.image.load(hborder).convert_alpha()
wn.blit(hborder, (0, 0))

hlborder = pygame.image.load(hlborder).convert_alpha()
wn.blit(hlborder, (825, 0))

#piano tiles
class Tile:
    def __init__(self, column):
        self.y = 0
        if column == 1:
            self.x = 475+23
        elif column == 2:
            self.x = 475+23+64+18.5
        elif column == 3:
            self.x = 475+23*2+64*2+8.5
        elif column == 4:
            self.x = 475+23*3+64*3+4
        
        self.image = ptile

    def draw(self):
        wn.blit(self.image,(self.x,self.y))

    def move(self,speedy):
        self.y += speedy

# midi = mido.MidiFile('assets/sounds/sound1.midi')
# pygame.midi.init()
# player = pygame.midi.Output(0)
# player.set_instrument(0)
# for i in midi:
#     try:
#         if i.note == 38 and i.velocity > 60:
#             print(i)
#             player.note_on(note=i.note, velocity=i.velocity, channel=i.channel)
#             time.sleep(i.time)
#             player.note_off(note=i.note, velocity=i.velocity, channel=i.channel)
#         else:
#             time.sleep(i.time)
#     except:
#         print(i)

tile_group = []

for i in range(1,5):
    tile_group.append(Tile(i))

while True:
    wn.fill((0,0,0))
    for tile in tile_group:
       tile.move(3)
       tile.draw()
    for event in pygame.event.get():
       if event.type == QUIT:
           pygame.quit()
           sys.exit()

    wn.blit(border, (475, 0))
    wn.blit(hborder, (0, 0))
    wn.blit(hlborder, (825, 0))
    pygame.display.update()
    pygame.time.Clock().tick(120)