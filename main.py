from pygame import *
from scenes import GameScene, LevelsScene
import sqlite3

init()
font.init()
mixer.init()

class Game():
    def __init__(self) -> None:
        self.curs = sqlite3.connect('media/levels.sqlite').cursor()
        self.startScene = LevelsScene(self)
        self.currentScene = self.startScene
 
        display.set_caption("Shooter")
    
    def loadGameLevel(self, levelSettings):
        self.currentScene = GameScene(levelSettings, self)

    def loadLevels(self):
        self.currentScene = LevelsScene(self)

    def gameCycle(self) -> None:
        while True:
            events = event.get()
            keys = key.get_pressed()
            self.currentScene.cycle(events, keys)
            time.delay(50)


game = Game()
game.gameCycle()