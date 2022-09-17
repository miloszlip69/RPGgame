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
        self.rect.bottom = HEIGHT

    def update(self):
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

        self.image = stone_img
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


WIDTH = 1000
HEIGHT = 800

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("RPG Game")
run = True
clock = pygame.time.Clock()

# Img's

player_img = [pygame.image.load(os.path.join(img_dir, "pKnight.png")).convert()]
stone_img = pygame.image.load(os.path.join(img_dir, "stone.png")).convert()

player = Player()
all_sprites = pygame.sprite.Group(player)
platforms = pygame.sprite.Group(Platform(200, HEIGHT - 50),
                                Platform(350, HEIGHT - 120))

while run:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    screen.fill(WHITE)
    all_sprites.draw(screen)
    platforms.draw(screen)
    platforms.update()
    all_sprites.update()

    pygame.display.flip()
pygame.quit()
