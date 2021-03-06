from packetInformation import *
from settings import *

import time
import threading
import math
import datetime


class Hero:

    def __init__(self, playerData, networkingObj):

        self.name = playerData["name"]
        self.userID = playerData["userID"]
        self.x = float(playerData["x"])
        self.y = float(playerData["y"])
        self.speed = float(playerData["speed"])
        self.credits = int(playerData["credits"])
        self.uridium = int(playerData["uridium"])
        self.hp = int(playerData["hp"])
        self.hpmax = int(playerData["hpmax"])
        self.shd = int(playerData["shd"])
        self.shdmax = int(playerData["shdmax"])
        self.xp = int(playerData["xp"])
        self.honor = int(playerData["honor"])
        self.company = int(playerData["company"])
        self.level = int(playerData["level"])
        self.cloaked = int(playerData["cloaked"])

        self.networking = networkingObj

        self.size = 3
        self.color = "white"

        self.busy = False

        self.guiObj = self.networking.gui.canvas.create_rectangle(
            (self.x/100 * self.networking.gui.scale)-self.size, 
            (self.y/100 * self.networking.gui.scale)-self.size, 
            (self.x/100 * self.networking.gui.scale)+self.size, 
            (self.y/100 * self.networking.gui.scale)+self.size, 
            fill=self.color
        )

        self.networking.gui.setText(newText="{0} / {1} \n{2}/{3}\n{4}cr\n{5}uri".format(
            self.name, 
            self.userID, 
            self.hp, 
            self.shd,
            self.credits,
            self.uridium
        ))

        print "start hero AI.."
        self.networking.send("S|CLK")
        threading._start_new_thread(self.heroAI, ())

    
    def hide(self):
        self.networking.gui.setColor(self.guiObj, "black")
    
    def show(self):
        self.networking.gui.setColor(self.guiObj, self.color)
    
    def distance_between_points(self, x1, y1, x2, y2):
        return math.sqrt(math.pow(int(x1) - int(x2), 2) + math.pow(int(y1) - int(y2), 2))
    
    def updatePosition(self, x, y):
        self.networking.gui.canvas.delete(self.guiObj)

        self.x = int(x)
        self.y = int(y)
        self.guiObj = self.networking.gui.canvas.create_rectangle(
            (self.x/100 * self.networking.gui.scale)-self.size, 
            (self.y/100 * self.networking.gui.scale)-self.size, 
            (self.x/100 * self.networking.gui.scale)+self.size, 
            (self.y/100 * self.networking.gui.scale)+self.size, 
            fill=self.color
        )
    
    def heroAI(self):
        while True:
            time.sleep(.2)

            # get the closest npc and collectable
            # depending on priority choose the nearest one

            if not self.busy and len(self.networking.gui.bonusBoxes) > 0:
                self.busy = True

                # get the closest bonusbox from my position
                # {distance:bbobj}
                tmpBoxes = dict()

                for box in self.networking.gui.bonusBoxes:
                    tmpBoxes[self.distance_between_points(box.x, box.y, self.x, self.y)] = box
                
                nextBox = tmpBoxes[min(tmpBoxes)]

                self.moveTo(nextBox.x, nextBox.y)
                self.networking.send("{0}|{1}".format(
                    COLLECT_BOX,
                    nextBox.boxID
                ))
                nextBox.remove()


                self.busy = False
    
    def moveTo(self, nx , ny):
        self.networking.send("{0}|{1}|{2}|{3}|{4}".format(
            SHIP_MOVEMENT,
            int(nx),
            int(ny),
            int(self.x),
            int(self.y)
        ))

        started = datetime.datetime.now()
        while self.distance_between_points(nx, ny, self.x, self.y) >= 50:
            if datetime.datetime.now() - started > datetime.timedelta(seconds=30):
                self.busy = False
                break
            time.sleep(.33)




