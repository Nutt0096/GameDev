import pygame
import json

class Animation:
    def __init__(self, images, idleSprite=None, looping=True, interval_time = 0.15):
        self.images = images
        self.timer = 0
        self.index = 0
        if idleSprite is None:
            self.image = self.images[self.index]
        else:
            self.image = idleSprite
        self.idleSprite = idleSprite

        self.interval_time = interval_time

        self.looping = looping #default loop

        self.times_played = 0

    def Refresh(self):
        self.timer=0
        self.index = 0
        self.times_played=0

    def update(self, dt):
        # one time animation check (attacking)
        if self.looping is False and self.times_played>0:
            return

        self.timer = self.timer + dt

        if self.timer > self.interval_time:
            self.timer = self.timer % self.interval_time

            self.index = (self.index+1) % len(self.images)
            #print(self.index)

            if self.index == 0:
                self.times_played += 1

        self.image = self.images[self.index]

    def Idle(self):
        self.image = self.idleSprite


class Sprite:
    def __init__(self, image, animation=None):
        self.image = image
        self.animation = animation



class SpriteManager:
    def __init__(self):
        self.spriteCollection = self.loadSprites(
            [
                "./sprite/Arrow.json",
                "./sprite/knight.json",
                "./sprite/wizard.json",
                "./sprite/archer.json",
            ]
        )

    def loadSprites(self, urlList):
        resDict = {} #result dictionary
        for url in urlList:
            with open(url) as jsonData:
                data = json.load(jsonData)
                mySpritesheet = SpriteSheet(data["spriteSheetURL"])
                dic = {}
                for sprite in data["sprites"]:
                    try:
                        colorkey = sprite["colorKey"]
                    except KeyError:
                        colorkey = None
                    try:
                        xSize = sprite['xsize']
                        ySize = sprite['ysize']
                    except KeyError:
                        xSize, ySize = data['size']
                    dic[sprite["name"]] = Sprite(
                        mySpritesheet.image_at(
                            sprite["x"],
                            sprite["y"],
                            sprite["scalefactor"],
                            colorkey,
                            xTileSize=xSize,
                            yTileSize=ySize,
                        )
                    )
                resDict.update(dic)
                continue
        return resDict

class SpriteSheet(object):
    def __init__(self, filename):
        try:
            self.sheet = pygame.image.load(filename)
            self.sheet = pygame.image.load(filename)
            if not self.sheet.get_alpha():
                self.sheet.set_colorkey((0, 0, 0))
        except pygame.error:
            print("Unable to load spritesheet image:", filename)
            raise SystemExit

    def image_at(self, x, y, scalingfactor, colorkey=None,
                 xTileSize=16, yTileSize=16):
        rect = pygame.Rect((x, y, xTileSize, yTileSize))
        image = pygame.Surface(rect.size)
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return pygame.transform.scale(
            image, (xTileSize * scalingfactor, yTileSize * scalingfactor)
        )