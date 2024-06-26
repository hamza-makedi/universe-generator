from ursina import *
from camera import CameraMovement
from random import *
import random
import requests
from io import BytesIO
from PIL import Image
from urllib.parse import urlencode
import urllib.request

app = Ursina()

player = CameraMovement(x=500, gravity=0)
player.speed = 100


colors = [
    color.white,
    color.black,
    color.red,
    color.green,
    color.blue,
    color.yellow,
    color.orange,
    color.pink,
    color.brown,
    color.cyan,
    color.magenta,
    color.gray,
    color.olive,
    color.lime,
    color.gold
]


class StarSystem:
    global colors
    def __init__(self,x,y,z):
        self.x = int(x)
        self.y = int(y)
        self.z = int(z)
        self.nLehmer = (((self.x & 0xFFFF)) | ((self.y & 0xFFFF) ) | (self.z & 0xFFFF ))

        self.starExist = self.rndInt(0,30)==1
        if not self.starExist:return

        self.starDiameter = self.rndInt(10,40)
        self.starColor = (colors[self.rndInt(0,len(colors)-1)])

        
        planet_texture = load_texture(f"textures/planet{self.rndInt(0,49)}.gif")
        self.ent = Entity(model='sphere',
                    texture=planet_texture,
                    scale=self.starDiameter,
                    position=(self.x,self.y,self.z)
                )

    def Lehmer32(self):
        self.nLehmer += 0xe130fc15
        tmp = (self.nLehmer & 0xFFFFFFFF) * 0x4a39b70d
        m1 = (tmp >> 32) ^ tmp
        tmp = (m1 & 0xFFFFFFFF) * 0x12fad5c9
        m2 = (tmp >> 32) ^ tmp
        return m2

    def rndInt(self ,minval ,maxval):
        return (self.Lehmer32() % (maxval - minval)) + minval




nSector = (3000,3000,3000)
screenSector = [0,0,0]
starsVisible = []

for screenSector[0] in range(-nSector[0],nSector[0],500):
    for screenSector[1] in range(-nSector[1],nSector[1],500):
        for screenSector[2] in range(-nSector[2],nSector[2],500):
            star = StarSystem(screenSector[0]+randint(0,300),screenSector[1]+randint(0,300),screenSector[2]+randint(0,300))
            if star.starExist:
                starsVisible.append(star)
                #starsVisible.append(PointLight(parent=scene, color=star.starColor, position=(star.x,star.y,star.z), radius=star.starDiameter//100))



skybox_image = load_texture("milky_way.jpg")
Sky(texture=skybox_image, shader=None)

def input(key):
    if key=='escape':
        quit()
    if key=='b':
        mouse.locked = not mouse.locked

app.run()