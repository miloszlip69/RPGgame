import pygame

pygame.init()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.speedx = None
        self.speedy = None
        self.image = pygame.Surface([50, 50])
        self.image.fill((0, 0, 0))

        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)

    def update(self):
        self.speedx = 0
        self.speedy = 0

        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        if keystate[pygame.K_UP]:
            self.speedy = -8
        if keystate[pygame.K_DOWN]:
            self.speedy = 8

        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        elif self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        elif self.rect.top < 0:
            self.rect.top = 0


WIDTH = 1000
HEIGHT = 800

screen = pygame.display.set_mode([WIDTH, HEIGHT])
run = True
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group(Player())

while run:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    screen.fill((255, 255, 255))
    all_sprites.draw(screen)
    all_sprites.update()

    pygame.display.flip()
pygame.quit()
