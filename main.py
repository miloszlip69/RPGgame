import pygame
import math
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
HELL_COLOR = (80, 20, 20)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = player_img[0]
        self.image = pygame.transform.scale(self.image, (14 * 4, 25 * 4))
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT - 300)
        self.spawnPoint = (WIDTH / 2, HEIGHT - 300)

        self.speedx = 0
        self.speedy = 0
        self.rotation = "right"
        self.flip = False
        self.onGround = True
        self.living = True

        self.item = Sword()
        self.keystate = None
        self.stats_open = False

    def update(self):
        stamina.onUse = False
        self.keystate = pygame.key.get_pressed()

        self.speedx = 0
        if not self.speedy > 5:
            self.speedy += 1

        if self.keystate[pygame.K_d]:
            self.speedx = 6
            self.rotation = "right"
        if self.keystate[pygame.K_a]:
            self.speedx = -6
            self.rotation = "left"
        if self.keystate[pygame.K_SPACE] and self.onGround:
            self.speedy = -20
            self.onGround = False
        if self.keystate[pygame.K_LSHIFT] and stamina.amount > 0:
            stamina.onUse = True
            self.speedx *= 1.8

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

        if self.rotation == "right":
            self.image = player_img[0]
        elif self.rotation == "left":
            self.image = pygame.transform.flip(player_img[0], True, False)

        self.image = pygame.transform.scale(self.image, (14 * 4, 25 * 4))
        self.image.set_colorkey(BLACK)
        if not self.living:
            self.item = None
        if self.item:
            self.item.draw()
            self.item.update()

    def die(self):
        self.rect.center = self.spawnPoint


class Sword(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.mouseC = []
        self.angle = 0
        self.dx = 0
        self.dy = 0
        self.speed = 2

        self.onPlayer = True
        self.mouse_x = 0
        self.mouse_y = 0

        self.image = sword_img
        self.image = pygame.transform.scale(self.image, (16 * 2, 16 * 2))
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.rect.size = (32, 32)
        self.rect.topleft = (WIDTH / 2, HEIGHT / 2)

    def update(self):
        self.mouseC = pygame.mouse.get_pressed()
        if self.onPlayer:
            self.speed = 2
            self.rect.center = player.rect.center
            self.angle = math.atan2(self.mouse_y - self.rect.centery, self.mouse_x - self.rect.centerx)
            self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
            self.image = pygame.transform.rotate(sword_img, (180 / math.pi) * - self.angle)
            self.image = pygame.transform.scale(self.image, (16 * 2, 16 * 2))
            self.image.set_colorkey(BLACK)
            if self.mouseC[0]:
                self.onPlayer = False

        else:
            self.speed += 0.5
            self.dx = int(math.cos(self.angle) * self.speed)
            self.dy = int(math.sin(self.angle) * self.speed)

            if self.rect.top > 0 and self.rect.bottom < HEIGHT and self.rect.left > 0 and self.rect.right < WIDTH:
                self.rect.x += self.dx
                self.rect.y += self.dy
            else:
                self.onPlayer = True
            for i in blocks:
                if self.rect.colliderect(i.rect):
                    self.onPlayer = True
                    i.destroy()

    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))


class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, unbreakable, BlockId):
        pygame.sprite.Sprite.__init__(self)

        self.unbreakable = unbreakable
        self.image = blocks_img[BlockId]
        self.image = pygame.transform.scale(self.image, (16 * 2, 16 * 2))
        self.image.set_colorkey(BLACK)
        self.blockID = BlockId

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        collide = self.rect.colliderect(player.rect)
        if collide:
            if self.blockID == 3:
                player.die()
            if player.speedy < 0:
                player.speedy = 3
            if self.rect.top + 7 > player.rect.bottom > self.rect.top:
                player.rect.bottom = self.rect.top + 1
                player.speedy = 0
                player.onGround = True
            else:
                if self.rect.left < player.rect.right < self.rect.left + 12:
                    player.rect.right = self.rect.left
                elif self.rect.right > player.rect.left > self.rect.right - 12:
                    player.rect.left = self.rect.right

    def destroy(self):
        if not self.unbreakable:
            self.kill()


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
            pygame.draw.line(screen, YELLOW, [self.rect.right, self.rect.centery],
                             [self.rect.right + self.amount, self.rect.centery], 6)
        if self.onUse:
            self.amount -= 1
            self.cooldown = 60
        elif self.cooldown < 0:
            self.amount += 1
        if self.amount > self.maxAmount:
            self.amount = self.maxAmount


def world_gen():
    for i in range(32):
        blocks.add(Block(i * 32, HEIGHT - 16, True, 3))

    for i in blocks:
        if 600 > i.rect.x > 200:
            blocks.remove(i)
            blocks.add(Block(i.rect.centerx, i.rect.centery, False, 2))


WIDTH = 1000
HEIGHT = 600

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("RPG Game")
run = True
clock = pygame.time.Clock()

# Img's

player_img = [pygame.image.load(os.path.join(img_dir, "pKnight.png")).convert()]
widgets = [pygame.image.load(os.path.join(img_dir, "stamina.png")).convert()]
sword_img = pygame.image.load(os.path.join(img_dir, "sword.png")).convert()
blocks_img = [pygame.image.load(os.path.join(img_dir, "grass.png")).convert(),
              pygame.image.load(os.path.join(img_dir, "stone.png")).convert(),
              pygame.image.load(os.path.join(img_dir, "magma.png")).convert(),
              pygame.image.load(os.path.join(img_dir, "lava.png")).convert()]

player = Player()
stamina = Stamina()
all_sprites = pygame.sprite.Group(player, stamina)
blocks = pygame.sprite.Group()
world_gen()

while run:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False

    screen.fill(HELL_COLOR)
    all_sprites.draw(screen)
    blocks.draw(screen)
    blocks.update()
    all_sprites.update()
    pygame.display.flip()
pygame.quit()
