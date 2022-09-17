import pygame
import os

pygame.init()
img_dir = os.path.join(os.path.dirname(__file__), 'img')

# Colors

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
SKY_BLUE = (40, 100, 155)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.speedx = 0
        self.speedy = 0
        self.onGround = True

        self.image = player_img[0]
        self.image = pygame.transform.scale(self.image, (14 * 4, 25 * 4))
        self.image.set_colorkey(BLACK)

        self.angle = None
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)

    def update(self):
        stamina.onUse = False

        self.speedx = 0
        if not self.speedy > 4:
            self.speedy += 1

        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_a]:
            self.speedx = -6
        if keystate[pygame.K_d]:
            self.speedx = 6
        if keystate[pygame.K_SPACE] and self.onGround:
            self.speedy = -20
            self.onGround = False
        if keystate[pygame.K_LSHIFT] and stamina.amount > 0:
            stamina.onUse = True
            self.speedx *= 3

        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        elif self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > HEIGHT:
            self.onGround = True
            self.rect.bottom = HEIGHT
            self.speedy = 0
        elif self.rect.top < 0:
            self.rect.top = 0


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.image = blocks_img[0]
        self.image = pygame.transform.scale(self.image, (16 * 2, 16 * 2))

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        collide = self.rect.colliderect(player.rect)

        if collide:
            if player.speedy < 0:
                player.speedy = 3
            if self.rect.top + 7 > player.rect.bottom > self.rect.top:
                player.rect.bottom = self.rect.top + 1
                player.speedy = 0
                player.onGround = True
            else:
                if self.rect.left < player.rect.right < self.rect.left + 7:
                    player.rect.right = self.rect.left - 1
                elif self.rect.right > player.rect.left > self.rect.right - 7:
                    player.rect.left = self.rect.right + 1


class Stamina(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = widgets[0]
        self.image = pygame.transform.scale(self.image, (16 * 2, 16 * 2))
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.rect.topleft = (50, 50)

        self.onUse = False
        self.amount = 100
        self.maxAmount = 100

        self.cooldown = 60

    def update(self):
        self.cooldown -= 1

        if self.amount > 0:
            pygame.draw.line(screen, YELLOW, [self.rect.right, self.rect.centery], [self.rect.right + self.amount, self.rect.centery], 6)
        if self.onUse:
            self.amount -= 1
            self.cooldown = 60
        elif self.cooldown < 0:
            self.amount += 1
        if self.amount > self.maxAmount:
            self.amount = self.maxAmount


WIDTH = 1920
HEIGHT = 1080

screen = pygame.display.set_mode([WIDTH, HEIGHT], pygame.FULLSCREEN)
pygame.display.set_caption("RPG Game")
run = True
clock = pygame.time.Clock()

# Img's

player_img = [pygame.image.load(os.path.join(img_dir, "pKnight.png")).convert()]
widgets = [pygame.image.load(os.path.join(img_dir, "stamina.png")).convert()]
blocks_img = [pygame.image.load(os.path.join(img_dir, "grass.png")).convert(),
              pygame.image.load(os.path.join(img_dir, "stone.png")).convert()]

player = Player()
stamina = Stamina()
all_sprites = pygame.sprite.Group(player, stamina)
platforms = pygame.sprite.Group()
for i in range(128):
    platforms.add(Platform(i * 32 - 16, HEIGHT - 16))

while run:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    screen.fill(SKY_BLUE)
    all_sprites.draw(screen)
    platforms.draw(screen)
    platforms.update()
    all_sprites.update()

    pygame.display.flip()
pygame.quit()
