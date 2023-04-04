import sys
import pygame
from settings import *
from player import Player
from car import Car
from sprite import SimpleSprite, LongSprite
from random import choice, randint

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.offset = pygame.math.Vector2()
        self.bg = pygame.image.load('./MAIN/map.png').convert()
        self.fg = pygame.image.load('./MAIN/overlay.png').convert_alpha()

    def customize_draw(self):

        self.offset.x = player.rect.centerx - WINDOW_WIDTH / 2
        self.offset.y = player.rect.centery - WINDOW_HEIGHT / 2

        display_surf.blit(self.bg, -self.offset)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_post = sprite.rect.topleft - self.offset
            display_surf.blit(sprite.image, offset_post)

        display_surf.blit(self.fg, -self.offset)


# basic setup
pygame.init()
display_surf = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("GROCERY RUN!")
pygame.display.set_icon(pygame.image.load('baby-icon.png'))
clock = pygame.time.Clock()

# groups
all_sprites = AllSprites()
obstacle_sprites = pygame.sprite.Group()

# sprites
player = Player((2062, 3274), all_sprites, obstacle_sprites)

# timer
car_timer = pygame.event.custom_type()
pygame.time.set_timer(car_timer, 50)
pos_list = []

# font
font = pygame.font.Font(None, 50)
text_surf = font.render("You won! You got the food!", True, "teal")
text_rect = text_surf.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

# rules
rules_surf = font.render("You ran out of food! Go north to the store to buy more!", True, "teal")
rules_rect = rules_surf.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

# music
music = pygame.mixer.Sound('music.mp3')
music.play(loops=-1)

# sprite setup
for file_name, pos_list in SIMPLE_OBJECTS.items():
    path = f'./OBJECTS/SIMPLE/{file_name}.png'
    surf = pygame.image.load(path).convert_alpha()
    for pos in pos_list:
        SimpleSprite(surf, pos, [all_sprites, obstacle_sprites])

for file_name, pos_list in LONG_OBJECTS.items():
    surf = pygame.image.load(f'./OBJECTS/LONG/{file_name}.png').convert_alpha()
    for pos in pos_list:
        LongSprite(surf, pos, [all_sprites, obstacle_sprites])

# game loop
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == car_timer:
            random_pos = choice(CAR_START_POSITIONS)
            if random_pos not in pos_list:
                pos_list.append(random_pos)
                pos = (random_pos[0], random_pos[1] + randint(-8, 8))
                Car(pos, [all_sprites, obstacle_sprites])
            if len(pos_list) > 5:
                del pos_list[0]

    # delta time
    dt = clock.tick() / 1000

    # draw a bg
    display_surf.fill("black")

    if player.pos.y >= 1180:
        # update
        all_sprites.update(dt)

        # draw
        all_sprites.customize_draw()

        if pygame.time.get_ticks() < 6000:
            display_surf.fill('lightpink')
            display_surf.blit(rules_surf, rules_rect)

    else:
        display_surf.fill('pink')
        display_surf.blit(text_surf, text_rect)

    # update the display
    pygame.display.update()



