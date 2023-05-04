import pygame

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    QUIT
)

pygame.init()
pygame.mixer.init()

ballHitPlayer_Sound = pygame.mixer.Sound("soundEffects/playerHit.wav")
ballHitWall_Sound = pygame.mixer.Sound("soundEffects/wallHit.wav")

screenWidth = 1200
screenHeight = 800

playerHeight = 15
playerWidth = 70

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
        self.rect.x = ((screenWidth / 2) - (playerWidth / 2))
        self.rect.y = (screenHeight - playerHeight)

    def updatePlayer(self, pressedKeys):
        if pressedKeys[K_UP]:
            self.rect.move_ip(0, -2)
        if pressedKeys[K_DOWN]:
            self.rect.move_ip(0, 2)
        if pressedKeys[K_LEFT]:
            self.rect.move_ip(-2, 0)
        if pressedKeys[K_RIGHT]:
            self.rect.move_ip((2, 0))
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= screenHeight:
            self.rect.bottom = screenHeight
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= screenWidth:
            self.rect.right = screenWidth


player = Player()


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super(Ball, self).__init__()
        self.ballRadius = ballRadius
        self.ballDiameter = ballRadius * 2
        self.surface = pygame.Surface((self.ballDiameter, self.ballDiameter), pygame.SRCALPHA)
        self.image = self.surface
        pygame.draw.circle(self.surface, pygame.Color("#F07167"), (ballRadius, ballRadius), ballRadius)
        self.rect = self.surface.get_rect()
        self.rect.x = (screenWidth / 2) - ballRadius
        self.rect.y = (screenHeight / 2) - ballRadius
        self.speed = [1, 1]
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight

    def updateBall(self):
        self.rect.move_ip(self.speed)
        playerCenter = player.rect.centerx
        ballCenter = self.rect.centerx
        if self.rect.top <= 0 or self.rect.bottom >= screenHeight or self.rect.left <= 0 or self.rect.right >= screenWidth:
            ballHitWall_Sound.play()
        if ballCenter >= screenWidth:
            self.rect.right = screenWidth
        if ballCenter <= 0:
            self.rect.left = 0
        if self.rect.top <= 0 and ballCenter <= 0:
            self.rect.top = 0
        if self.rect.bottom >= screenHeight and ballCenter >= screenHeight:
            self.rect.bottom = screenHeight

        if self.rect.left < 0 or self.rect.right > self.screenWidth:
            self.speed[0] = -self.speed[0]
        if self.rect.top < 0 or self.rect.bottom > self.screenHeight:
            self.speed[1] = -self.speed[1]
        if self.rect.colliderect(player.rect):
            ballHitPlayer_Sound.play()
            if ballCenter < playerCenter - playerWidth / 4:
                self.speed[0] = -abs(self.speed[0])
                self.speed[1] = -self.speed[1]
            elif ballCenter > playerCenter + playerWidth / 4:
                self.speed[0] = abs(self.speed[0])
                self.speed[1] = -self.speed[1]
            else:
                self.speed[1] = -self.speed[1]


ball = Ball()

allSprites = pygame.sprite.Group()
allSprites.add(player)
allSprites.add(ball)

gameRunning = True
while gameRunning:
    for event in pygame.event.get():
        if event.type == QUIT:
            gameRunning = False

    screen.fill(screenBgColor)

    pressedKeys = pygame.key.get_pressed()
    player.updatePlayer(pressedKeys)
    screen.blit(ball.surface, ball.rect)

    ball.updateBall()

    allSprites.draw(screen)

    pygame.display.flip()

    pygame.display.update()

pygame.quit()
