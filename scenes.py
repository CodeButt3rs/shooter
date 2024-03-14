from pygame import *
from enitities import Player, Enemy, Button
from configs import win_height, win_width
from random import randint
import sys

levels = [
    {'id': 0, 'goal': 5, 'maxLost': 5}, {'id': 1, 'goal': 8, 'maxLost': 4}, {'id': 2, 'goal': 15, 'maxLost': 4}, {'id': 3, 'goal': 20, 'maxLost': 3}, {'id': 4, 'goal': 23, 'maxLost': 3}, 
    {'id': 5, 'goal': 25, 'maxLost': 3}, {'id': 6, 'goal': 30, 'maxLost': 2}, {'id': 7, 'goal': 35, 'maxLost': 2}, {'id': 8, 'goal': 40, 'maxLost': 2}, {'id': 9, 'goal': 50, 'maxLost': 1} 
]

levels_nums = [[i for i in range(1, 6)], [j for j in range(6, 11)]]

class MainMenuScene():
    def __init__(self) -> None:
        pass

class LevelsScene():
    def __init__(self, game) -> None:
        self.mainWindow = display.set_mode((win_width, win_height))
        self.mainWindow.fill((255, 255, 255))
        self.background = transform.scale(image.load("media/images/galaxy.jpg"), (win_width, win_height))

        self.buttons = sprite.Group()
        self.text = []
        self.gameManager = game

        self.loadText()
        self.loadButtons()
    
    def loadButtons(self) -> None:
        startPos = (255, 200)
        buttonsStatus = self.gameManager.curs.execute('select * from levels').fetchall()
        for i in levels_nums:
            for j in i:
                self.buttons.add(Button((startPos[0] + + 55 * ((j - 1) % 5 - 1), startPos[1] + 55 * (j // 6)), buttonsStatus[j - 1][1], levels[j - 1], self.gameManager))
                self.text.append(self.headerFont.render(str(j), True, (255, 255, 255)))

    def renderButtons(self) -> None:
        self.buttons.update(self.mainWindow)
        for i in levels_nums:
            for j in i:
                self.mainWindow.blit(self.text[j - 1], (257 + 55 * ((j - 1) % 5 - 1), 203 + 55 * (j // 6)))

    def loadText(self):
        self.headerFont = font.Font(None, 70)
        self.subHeaderFont = font.Font(None, 28)

        self.mainText = self.headerFont.render('Выбор уровня', True, (255, 255, 255))

    def checkButton(self, mousepos):
        for i in self.buttons.sprites():
            rect: Rect = i.rect
            if rect.collidepoint(mousepos):
                i.click()

    def render(self):
        self.mainWindow.blit(self.background,(0, 0))
        self.mainWindow.blit(self.mainText,(170, 130))
        self.renderButtons()

        display.flip()
        display.update()

    def terminate(self) -> None:
        quit()
        sys.exit()

    def cycle(self, events, keys):
        for e in events:
            if e.type == QUIT:
                self.terminate()
            if e.type == MOUSEBUTTONDOWN:
                self.checkButton(e.pos)
        self.render()

class GameScene():
    def __init__(self, levelSettings, game) -> None:
        self.score = 0
        self.goal = levelSettings['goal']
        self.lost = 0
        self.maxLost = levelSettings['maxLost']
        self.levelSettings = levelSettings
        self.fixed = False
        self.gameManager = game

        self.enemyShips = sprite.Group()
        self.bullets = sprite.Group()

        self.player = Player("media/images/spaceShip.png", 5, win_height - 100, 80, 100, 10)

        display.set_caption("Shooter")
        self.mainWindow = display.set_mode((win_width, win_height))
        self.background = transform.scale(image.load("media/images/galaxy.jpg"), (win_width, win_height))

        self.gameRunning = True

        self.loadSounds()
        self.loadText()
        self.loadEnemies() 

    def loadEnemies(self):
        for i in range(1, 6):
            self.spawnEnemy()

    def loadSounds(self) -> None:
        mixer.init()
        mixer.music.load('media/sounds/space.ogg')
        mixer.music.set_volume(0.2)
        mixer.music.play()

        self.fireSound = mixer.Sound('media/sounds/fire.ogg')
        self.fireSound.set_volume(0.1)

    def loadText(self):
        self.headerFont = font.Font(None, 80)
        self.subHeaderFont = font.Font(None, 36)

        self.winText = self.headerFont.render('Вы выиграли!', True, (255, 255, 255))
        self.loseText = self.headerFont.render('Вы проиграли!', True, (180, 0, 0))

    def renderText(self) -> None:
        text = self.subHeaderFont.render("Счет: " + str(self.score) + '/' + str(self.goal), 1, (255, 255, 255))
        self.mainWindow.blit(text, (10, 20))
        text_lose = self.subHeaderFont.render("Пропущено: " + str(self.lost) + '/' + str(self.maxLost), 1, (255, 255, 255))
        self.mainWindow.blit(text_lose, (10, 50))

    def render(self):
        self.mainWindow.set_colorkey((255,255,255))
        self.mainWindow.blit(self.background,(0,0))
        if self.gameRunning:
            self.player.update()
            self.enemyShips.update()
            self.bullets.update()

        self.player.reset(self.mainWindow)
        self.enemyShips.draw(self.mainWindow)
        self.bullets.draw(self.mainWindow)

        self.renderText()
        self.renderCollides()
        self.checkGameResults()

        if not self.gameRunning:
            self.showEndMenu()

        display.flip()
        display.update()

    def renderKeys(self, events, keys):
        pass

    def spawnEnemy(self) -> None:
        monster = Enemy("media/images/enemyShip.png", randint(80, win_width - 80), -40, 80, 50, randint(1, 5), self)
        self.enemyShips.add(monster)

    def renderCollides(self):
        collides = sprite.groupcollide(self.enemyShips, self.bullets, True, True)
        for _ in collides:
            self.score += 1
            self.spawnEnemy()
        
    def showEndMenu(self):
        draw.rect(self.mainWindow, (0, 0, 0), (270, 300, 150, 50))
        endGameText = self.subHeaderFont.render('К уровням', True, (255, 255, 255))
        self.mainWindow.blit(endGameText, (279, 311))

    def checkGameResults(self) -> None:
        if sprite.spritecollide(self.player, self.enemyShips, False) or self.lost >= self.maxLost:
            self.gameRunning = False
            self.mainWindow.blit(self.loseText, (170, 200))
        if self.score >= self.goal:
            self.fixWin()
            self.gameRunning = False
            self.mainWindow.blit(self.winText, (170, 200))

    def fixWin(self):
        if self.fixed:
            return
        self.fixed = True
        if self.levelSettings['id'] < 10:
            self.gameManager.curs.execute(f'update levels set levelStatus = True where levelId = {self.levelSettings["id"] + 1};')
            self.gameManager.curs.connection.commit()

    def terminate(self) -> None:
        quit()
        sys.exit()

    def cycle(self, events, keys):
        for e in events:
            if e.type == QUIT:
                self.terminate()
            if e.type == MOUSEBUTTONDOWN:
                if not self.gameRunning:
                    if Rect(250, 300, 150, 50).collidepoint(e.pos):
                        self.gameManager.loadLevels()
                    pass
            if self.gameRunning:
                if e.type == KEYDOWN:
                    if e.key == K_SPACE:
                        self.fireSound.play()
                        self.bullets.add(self.player.fire())
        self.render()