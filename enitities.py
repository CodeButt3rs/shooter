from pygame import *
from random import randint
from configs import win_height, win_width

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)

        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed

        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))


class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()


class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    def fire(self) -> Bullet:
        bullet = Bullet("media/images/bullet.png", self.rect.centerx, self.rect.top, 15, 20, -15)
        return bullet


class Enemy(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed, game):
        super().__init__(player_image, player_x, player_y, size_x, size_y, player_speed)
        self.game = game

    def update(self) -> None:
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            self.game.lost += 1

class Button(sprite.Sprite):
    def __init__(self, rect: tuple[int, int], locked, levelSettings, game) -> None:
        super().__init__()
        self.rect = Rect(rect[0], rect[1], 50, 50)
        self.locked = locked
        self.level = levelSettings
        self.game = game

    def update(self, surface) -> None:
        draw.rect(surface, (120, 120, 120) if not self.locked else (0, 0, 0), (self.rect.x, self.rect.y, 50, 50))

    def click(self):
        if self.locked:
            self.game.loadGameLevel(self.level)