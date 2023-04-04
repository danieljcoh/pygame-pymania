import pygame, sys
from os import walk


class Player(pygame.sprite.Sprite):

    def __init__(self, pos, groups, collision_sprites):

        super().__init__(groups)

        # import the assets for the animations
        self.import_assets()
        self.frame_index = 0
        self.status = 'UP'  # determines which way the char is facing
        # self.image = self.animation[self.frame_index]
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center=pos)

        # float based movement
        self.pos = pygame.math.Vector2(self.rect.center)
        self.direction = pygame.math.Vector2()
        self.speed = 175

        # collisions
        self.collision_sprites = collision_sprites
        self.hitbox = self.rect.inflate(0, -self.rect.height / 2)

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.collision_sprites.sprites():
                if sprite.hitbox.colliderect(self.hitbox):
                    if hasattr(sprite, 'name') and sprite.name == 'car':
                        pygame.quit()
                        sys.exit()
                    if self.direction.x > 0:  # moving right
                        self.hitbox.right = sprite.hitbox.left
                        self.rect.centerx = self.hitbox.centerx
                        self.pos.x = self.hitbox.centerx
                    if self.direction.x < 0:  # moving left
                        self.hitbox.left = sprite.hitbox.right
                        self.rect.centerx = self.hitbox.centerx
                        self.pos.x = self.hitbox.centerx
        else:
            for sprite in self.collision_sprites.sprites():
                if sprite.hitbox.colliderect(self.hitbox):
                    if hasattr(sprite, 'name') and sprite.name == 'car':
                        pygame.quit()
                        sys.exit()
                    if sprite.hitbox.colliderect(self.hitbox):
                        if self.direction.y > 0:  # moving down
                            self.hitbox.bottom = sprite.hitbox.top
                            self.rect.centery = self.hitbox.centery
                            self.pos.y = self.hitbox.centery
                        if self.direction.y < 0:  # moving up
                            self.hitbox.top = sprite.hitbox.bottom
                            self.rect.centery = self.hitbox.centery
                            self.pos.y = self.hitbox.centery

    def import_assets(self):
        self.animations = {}
        for index, folder in enumerate(walk('./PLAYER')):
            if index == 0:
                for name in folder[1]:
                    self.animations[name] = []
            else:
                for file_name in folder[2]:
                    path = folder[0] + '/' + file_name
                    surf = pygame.image.load(path).convert_alpha()
                    key = folder[0].split("/")[2]
                    self.animations[key].append(surf)

    def move(self, dt):
        # normalize the vector
        # print(self.direction)
        if pygame.time.get_ticks() > 6000:
            if self.direction.magnitude() != 0:
                self.direction = self.direction.normalize()

            # horizontal movement + collision
            self.pos.x += self.direction.x * self.speed * dt
            self.hitbox.centerx = round(self.pos.x)
            self.rect.centerx = self.hitbox.centerx
            self.collision('horizontal')

            # vertical movement + collision
            self.pos.y += self.direction.y * self.speed * dt
            self.hitbox.centery = round(self.pos.y)
            self.rect.centery = self.hitbox.centery
            self.collision('vertical')

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.status = 'RIGHT'
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.status = 'LEFT'
            self.direction.x = -1
        else:
            self.direction.x = 0

        if keys[pygame.K_UP]:
            self.status = 'UP'
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.status = 'DOWN'
            self.direction.y = 1
        else:
            self.direction.y = 0

    def animate(self, dt):
        current_animation = self.animations[self.status]
        if self.direction.magnitude() != 0:
            self.frame_index += 10 * dt  # where did this number 10 come from?
            if self.frame_index >= len(current_animation):
                self.frame_index = 0
        else:
            self.frame_index = 0
        self.image = current_animation[int(self.frame_index)]

    def restrict(self):
        # limiting the movement of the player
        if self.rect.left < 640:
            self.pos.x = 640 + self.rect.width / 2
            self.hitbox.left = 640
            self.rect.left = 640

        if self.rect.right > 2560:
            self.pos.x = 2560 - self.rect.width / 2
            self.hitbox.right = 2560
            self.rect.right = 2560

        if self.rect.bottom > 3500:
            self.pos.y = 3500 - self.rect.height / 2
            self.rect.bottom = 3500
            self.hitbox.centery = self.rect.centery

    def update(self, dt):
        self.input()
        self.move(dt)
        self.animate(dt)
        self.restrict()


