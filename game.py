import pygame
import random

from pygame.locals import (
    K_p,
    K_LEFT,
    K_RIGHT,
    KEYDOWN,
    QUIT
)

pygame.init()
pygame.mixer.init()

ballHitPlayer_Sound = pygame.mixer.Sound("soundEffects/playerHit.wav")
ballHitWall_Sound = pygame.mixer.Sound("soundEffects/wallHit.wav")
ballHitEnemy_Sound = pygame.mixer.Sound("soundEffects/enemyHit.wav")

screenWidth = 1200
screenHeight = 800
columnWidth = 400
gameAreaWidth = screenWidth - columnWidth

playerHeight = 15
playerWidth = 70

enemyHeight = playerHeight
enemyWidth = playerWidth

internalWallsHeight = 500
internalWallsWidth = 2

ballRadius = 8

screen = pygame.display.set_mode((screenWidth, screenHeight))
screenBgColor = pygame.Color("#30323d")
pygame.display.set_caption("Pong Game")


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surface = pygame.Surface((playerWidth, playerHeight))
        self.image = self.surface
        self.surface.fill(pygame.Color("#E8C547"))
        self.rect = self.surface.get_rect()
        self.rect.x = (gameAreaWidth - playerWidth) // 2
        self.rect.y = (screenHeight - playerHeight)

    def updatePlayer(self, pressedKeys):
        if pressedKeys[K_LEFT]:
            self.rect.move_ip(-2, 0)
        if pressedKeys[K_RIGHT]:
            self.rect.move_ip((2, 0))
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= gameAreaWidth:
            self.rect.right = gameAreaWidth


player = Player()


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surface = pygame.Surface((enemyWidth, enemyHeight))
        self.image = self.surface
        self.surface.fill(pygame.Color("#FF674D"))
        self.rect = self.surface.get_rect()
        self.rect.x = (gameAreaWidth - enemyWidth) // 2
        self.rect.y = enemyHeight
        self.ball = None

    def setBall(self, ball):
        self.ball = ball

    def updateEnemy(self):
        if self.ball:
            ballCenter = self.ball.rect.centerx
            enemyCenter = self.rect.centerx
            ballSpeed = max(abs(self.ball.speed[0]), abs(self.ball.speed[1]))
            if ballCenter < enemyCenter:
                self.rect.move_ip(-ballSpeed, 0)
            elif ballCenter > enemyCenter:
                self.rect.move_ip(ballSpeed, 0)
            if self.rect.left < 0:
                self.rect.left = 0
            elif self.rect.right > gameAreaWidth:
                self.rect.right = gameAreaWidth


enemy = Enemy()


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super(Ball, self).__init__()
        self.ballRadius = ballRadius
        self.ballDiameter = ballRadius * 2
        self.surface = pygame.Surface((self.ballDiameter, self.ballDiameter), pygame.SRCALPHA)
        self.image = self.surface
        pygame.draw.circle(self.surface, pygame.Color("#F6F7EB"), (ballRadius, ballRadius), ballRadius)
        self.rect = self.surface.get_rect()
        self.rect.x = (gameAreaWidth - self.ballDiameter)
        self.rect.y = (screenHeight - self.ballDiameter) // 2
        self.speed = [1, 1]
        self.screenHeight = screenHeight
        self.gameAreaWidth = gameAreaWidth

    def updateBall(self):
        self.rect.move_ip(self.speed)
        if self.rect.left < 0 or self.rect.right > screenWidth or self.rect.right > gameAreaWidth:
            ballHitWall_Sound.play()
            self.speed[0] = -self.speed[0]
        if self.rect.top < 0 or self.rect.bottom > screenHeight:
            ballHitWall_Sound.play()
            self.speed[1] = -self.speed[1]
        if self.rect.colliderect(player.rect):
            self.speed[1] = -1
            ballHitPlayer_Sound.play()
        if self.rect.colliderect(enemy.rect):
            ballHitEnemy_Sound.play()
            options = [-self.speed[0] + random.randint(0, 2), -self.speed[1] + random.randint(0, 2)]
            option = random.randint(0, 1)
            if option == 0:
                self.speed[0] = options[0]
            elif option == 1:
                self.speed[1] = options[1]


ball = Ball()
enemy.setBall(ball)

allSprites = pygame.sprite.Group()
allSprites.add(player)
allSprites.add(enemy)
allSprites.add(ball)

scoreBoardWidth = 400
scoreBoardHeight = screenHeight


class ScoreBoard(pygame.sprite.Sprite):
    def __init__(self):
        super(ScoreBoard, self).__init__()
        self.scoreBoardWidth = scoreBoardWidth
        self.scoreBoardHeight = scoreBoardHeight
        self.surface = pygame.Surface((scoreBoardWidth, scoreBoardHeight))
        self.rect = self.surface.get_rect()
        self.image = self.surface
        self.surface.fill(pygame.Color("#E2E8CE"))
        self.rect = self.surface.get_rect(center=(gameAreaWidth + columnWidth // 2, screenHeight // 2))

        self.titleFont = pygame.font.SysFont("Arial", 40)
        self.titleText = self.titleFont.render("ScoreBoard", True, pygame.Color("#262626"), pygame.Color("#ACBFA4"))
        self.titleRect = self.titleText.get_rect(center=(gameAreaWidth + columnWidth // 2, 20))

    def drawBoard(self, screen):
        screen.blit(self.surface, self.rect)
        screen.blit(self.titleText, self.titleRect)


scoreBoard = ScoreBoard()

paused = False


def pausedGame():
    global paused
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == K_p:
                    paused = False


gameRunning = True
while gameRunning:
    for event in pygame.event.get():
        if event.type == QUIT:
            gameRunning = False
        if event.type == KEYDOWN:
            if event.key == K_p:
                pausedGame()

    screen.fill(screenBgColor)

    pressedKeys = pygame.key.get_pressed()
    player.updatePlayer(pressedKeys)

    screen.blit(ball.surface, ball.rect)
    screen.blit(enemy.surface, enemy.rect)
    screen.blit(ball.surface, ball.rect)

    scoreBoard.drawBoard(screen)

    ball.updateBall()
    enemy.updateEnemy()

    allSprites.draw(screen)

    pygame.display.flip()
    pygame.display.update()


pygame.quit()
