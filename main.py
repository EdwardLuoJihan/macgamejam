import pygame, sys
import pygame.midi
from pygame.locals import *
import mido
import time
from pygame import mixer
import random

pygame.init()
screen = pygame.display.set_mode((1300, 800))
pygame.display.set_caption('Symphony of Seperation')
wn = pygame.Surface((1300, 800))
mixer.init()

#any other variables
screen_shake = 0
default_shake = 25
mainclock = pygame.time.Clock()
aparticles = {
    "smallbg":[],
    "largetiles":[]
}
mixer.music.load('assets/sounds/boom.wav')
mixer.music.set_volume(0.2)

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
        self.y = -143
        self.vis = True
        self.column = column
        if column == 1:
            self.x = 475+23
        elif column == 2:
            self.x = 475+23+64+16
        elif column == 3:
            self.x = 475+23*2+64*2+10
        elif column == 4:
            self.x = 475+23*3+64*3+4

        self.image = ptile

    def draw(self):
        if self.vis:
            wn.blit(tile_surf((20, 20, 60), self.x, self.y), ((self.x, self.y)), special_flags=BLEND_RGB_ADD)
            wn.blit(self.image,(self.x,self.y))

    def move(self,speedy):
        self.y += speedy

    def getpos(self):
        return self.x, self.y
    
    def v(self, vis):
        self.vis = vis

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

#particle system

def circle_surf(radius, color):
    surf = pygame.Surface((radius * 2, radius * 2))
    pygame.draw.circle(surf, color, (radius, radius), radius)
    surf.set_colorkey((0, 0, 0))
    return surf

def tile_surf(color, x, y):
    surf = pygame.Surface((64, 143))
    pygame.draw.rect(surf, color, (x, y, 64, 143), 0)
    surf.set_colorkey((0, 0, 0))
    return surf

def create_particle(minx, maxx, my, color, velocity, direction, duration, sizemin, sizemax, t):
    if t == 1:
        aparticles["smallbg"].append([[random.randint(minx, maxx), my], [random.randint(0, velocity) / 10 - 1, -2], duration, random.randint(sizemin, sizemax)])
    
    for particle in aparticles["smallbg"]:
        particle[0][1] += particle[1][1]
        particle[2] -= 0.1
        if t == 1:
            particle[3] -= 0.01
        elif t == 2:
            particle[3] -= .1
        #particle[1][1] += 0.1 gravity
        pygame.draw.circle(wn, color, [int(particle[0][0]), int(particle[0][1])], int(particle[3]))
        radius = particle[3] * 2
        wn.blit(circle_surf(radius, (20, 20, 60)), (int(particle[0][0] - radius), int(particle[0][1] - radius)), special_flags=BLEND_RGB_ADD)
        if particle[2] <= 0 or particle[3] <= 0:
            aparticles["smallbg"].remove(particle)
    if t == 2:
        aparticles["largetiles"].append([[random.randint(minx, maxx), my], [random.randint(0, velocity) / 10 - 1, -2], duration, random.randint(sizemin, sizemax), color])
    
    for particle in aparticles["largetiles"]:
        if particle[0][1] <= 20:
            if particle[4] == (255, 33, 122):
                print("recieved red orb - penalize player")
            else:
                print("recieved purple orb - move player")
            aparticles["largetiles"].remove(particle)
        else:
            particle[0][1] += particle[1][1]
            particle[2] -= 0.1
            if t == 1:
                particle[3] -= 0.01
            elif t == 2:
                particle[3] -= .1
            #particle[1][1] += 0.1 gravity
            pygame.draw.circle(wn, particle[4], [int(particle[0][0]), int(particle[0][1])], int(particle[3]))
            radius = particle[3] * 2
            wn.blit(circle_surf(radius, (20, 20, 60)), (int(particle[0][0] - radius), int(particle[0][1] - radius)), special_flags=BLEND_RGB_ADD)
            if particle[2] <= 0 or particle[3] <= 0:
                aparticles["largetiles"].remove(particle)


while True:
    wn.fill((0,0,0))
    screen.fill((0,0,0))

    #print(pygame.mouse.get_pos())

    #particle
    create_particle(500, 800, 722, (129, 71, 189), 30, -2, 80, 4, 5, t=1)

    if len(tile_group) == 0:
        for i in range(1,5):
            tile_group.append(Tile(i))
    
    events = pygame.event.get()

    c1 = [i for i in tile_group if i.column == 1]
    c2 = [i for i in tile_group if i.column == 2]
    c3 = [i for i in tile_group if i.column == 3]
    c4 = [i for i in tile_group if i.column == 4]

    for tile in tile_group:
        x, y = tile.getpos()
        c = tile.column
        if y >= 780:
            match c:
                case 1:
                    c1.remove(tile)
                case 2:
                    c2.remove(tile)
                case 3:
                    c3.remove(tile)
                case 4:
                    c4.remove(tile)
            tile_group.remove(tile)
            tile.v(False)
            screen_shake = default_shake
            create_particle(x, x+50, y, (255, 33, 122), 20, -2, 80, 20, 20, t=2)
            mixer.music.set_volume(0.1)
            mixer.music.play()

        tile.move(4)
        tile.draw()
    
    #bounds for clicking area: ymin = 560 ymax = 780

    for event in events:
        if event.type == pygame.KEYDOWN:
            mixer.music.set_volume(0.2)
            if event.key == pygame.K_z: #1
                try:
                    tile = c1[0]
                    x, y = tile.getpos()
                    if y >= 510 and y <= 725:
                        tile_group.remove(tile)
                        c1.remove(tile)
                        tile.v(False)
                        screen_shake = default_shake
                        create_particle(x, x+50, y+71, (84, 16, 148), 20, -2, 80, 20, 20, t=2)
                        mixer.music.play()
                except:
                    pass
            if event.key == pygame.K_x: #2
                try:
                    tile = c2[0]
                    x, y = tile.getpos()
                    if y >= 510 and y <= 725:
                        tile_group.remove(tile)
                        c2.remove(tile)
                        tile.v(False)
                        screen_shake = default_shake
                        create_particle(x, x+50, y+71, (84, 16, 148), 20, -2, 80, 20, 20, t=2)
                        mixer.music.play()
                except:
                    pass
            if event.key == pygame.K_c: #3
                try:
                    tile = c3[0]
                    x, y = tile.getpos()
                    if y >= 510 and y <= 725:
                        tile_group.remove(tile)
                        c3.remove(tile)
                        tile.v(False)
                        screen_shake = default_shake
                        create_particle(x, x+50, y+71, (84, 16, 148), 20, -2, 80, 20, 20, t=2)
                        mixer.music.play()
                except:
                    pass
            if event.key == pygame.K_v: #4
                try:
                    tile = c4[0]
                    x, y = tile.getpos()
                    if y >= 510 and y <= 725:
                        tile_group.remove(tile)
                        c4.remove(tile)
                        tile.v(False)
                        screen_shake = default_shake
                        create_particle(x, x+50, y+71, (84, 16, 148), 20, -2, 80, 20, 20, t=2)
                        mixer.music.play()
                except:
                    pass
        if event.type == QUIT:
           pygame.quit()
           sys.exit()
    
    if screen_shake > 0:
        screen_shake -= 1

    render_offset = [0,0]
    if screen_shake:
        render_offset[0] = random.randint(0, 10) - 4
        render_offset[1] = random.randint(0, 10) - 4
        
    wn.blit(border, (475, 0))
    wn.blit(hborder, (0, 0))
    wn.blit(hlborder, (825, 0))
    screen.blit(wn, render_offset)
    pygame.display.update()
    mainclock.tick(120)