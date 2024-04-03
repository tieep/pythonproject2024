import pygame
from config import *
import math
import random
class Spritesheet:
    def __init__(self, filename):
        self.sheet = pygame.image.load(filename).convert()

    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface((width, height))
        sprite.blit(self.sheet, (0, 0), (x, y, width, height))
        sprite.set_colorkey(BLACK)
        return sprite

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y, mapx, mapy):
        self.game = game
        # game.player = self 
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x =  mapx + x * TILE_SIZE
        self.y = mapy + y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.x_change = 0
        self.y_change = 0
        self.facing = "right"
        self.animation_loop = 1
        self.attack_loop = 0
        self.attacking = False

        self.image = self.game.character_spritesheet.get_sprite(3, 2, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x  = self.x
        self.rect.y = self.y

        self.right_animations = [self.game.character_spritesheet.get_sprite(3, 66, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(35, 66, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(67, 66, self.width, self.height)]

        self.left_animations = [self.game.character_spritesheet.get_sprite(3, 98, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(35, 98, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(67, 98, self.width, self.height)]
        
        self.rad = 0
        self.score = 0

        self.max_hp = 5
        self.max_armour = 3
        self.max_mana = 128

        self.HP = self.max_hp
        self.armour = self.max_armour
        self.mana = self.max_mana
        
        self.timer_hit = 0
        self.timer_armour = 0
        self.timer_attack = 0
        self.weapons = []
        self.weapon = None

    def set_weapons(self, weapons = None):
        if weapons == None:
            self.weapons = ["glock","ak47","sniper"]
            self.change_weapon(0)
        else:
            self.weapons = weapons
            self.change_weapon(0)

    def change_weapon(self, index):
        if self.weapons[index] == None: return False
        if self.weapons[index] == "glock":
            if self.weapon: self.weapon.kill()
            self.weapon = Glock(self.game, self)
        if self.weapons[index] == "ak47":
            if self.weapon: self.weapon.kill()
            self.weapon = AK47(self.game, self)
        if self.weapons[index] == "sniper":
            if self.weapon: self.weapon.kill()
            self.weapon = Sniper(self.game, self)

    def update(self):
        self.movement()
        self.animate()
        self.find_nearest_enemy()
        self.collide_enemy()
        self.collide_bullet()

        self.rect.x += self.x_change
        self.collide_blocks("x")
        self.rect.y += self.y_change
        self.collide_blocks("y")
        
        self.x_change = 0
        self.y_change = 0

        #TODO: sau 4s khong chien dau se hoi 1 giap / s
        if self.armour < self.max_armour and pygame.time.get_ticks() - self.timer_attack > 4000:
            if pygame.time.get_ticks() - self.timer_armour > 1000:
                self.armour += 1
                self.timer_armour = pygame.time.get_ticks()
    
    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            if(self.rect.centerx < WIN_WIDTH/2 + CAMERA_SIZE):
                for sprite in self.game.all_sprites:
                    sprite.rect.x += PLAYER_SPEED
                for attack in self.game.attacks:
                    attack.rect.x -= PLAYER_SPEED
            self.x_change = -PLAYER_SPEED
            if self.find_nearest_enemy() == None: self.facing = "left"
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            if(self.rect.centerx > WIN_WIDTH/2 - CAMERA_SIZE):
                for sprite in self.game.all_sprites:
                    sprite.rect.x -= PLAYER_SPEED
                for attack in self.game.attacks:
                    attack.rect.x += PLAYER_SPEED
            self.x_change = PLAYER_SPEED
            if self.find_nearest_enemy() == None: self.facing = "right"
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            if(self.rect.centery < WIN_HEIGHT/2 + CAMERA_SIZE):
                for sprite in self.game.all_sprites:
                    sprite.rect.y += PLAYER_SPEED
                for attack in self.game.attacks:
                    attack.rect.y -= PLAYER_SPEED
            self.y_change = -PLAYER_SPEED
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            if(self.rect.centery > WIN_HEIGHT/2 - CAMERA_SIZE):
                for sprite in self.game.all_sprites:
                    sprite.rect.y -= PLAYER_SPEED
                for attack in self.game.attacks:
                    attack.rect.y += PLAYER_SPEED
            self.y_change = PLAYER_SPEED
        
    def collide_enemy(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        if hits:
            self.get_dmg(self.game.enemies.sprites()[0].dmg)

    def get_dmg(self, dmg):
        if pygame.time.get_ticks() - self.timer_hit > 800:
            if(self.armour > 0):
                self.armour -= dmg
            else:
                self.HP -= dmg
            self.timer_attack = pygame.time.get_ticks()
            self.timer_hit = pygame.time.get_ticks()
            if(self.HP <= 0):
                self.game.playing = False

    def collide_bullet(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies_bullets, False)
        if hits:
            self.get_dmg(1)
            hits[0].kill()

    def collide_blocks(self, dir):
        hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
        if hits:
            if (dir == "x"):
                if self.x_change > 0:
                    self.rect.right = hits[0].rect.left
                if self.x_change < 0:
                    self.rect.left = hits[0].rect.right
            if (dir == "y"):
                if self.y_change > 0:
                    self.rect.bottom = hits[0].rect.top
                if self.y_change < 0:
                    self.rect.top = hits[0].rect.bottom

    def animate(self):
        if self.facing == "left":
            if self.x_change == 0 and self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(3, 98, self.width, self.height)
            else:
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
        
        if self.facing == "right":
            if self.x_change == 0 and self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(3, 66, self.width, self.height)
            else:
                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1

        if self.animation_loop >= 3:
            self.animation_loop = 1

    def find_nearest_enemy(self):
        #update rad to place the gun
        if self.y_change != 0 or self.x_change != 0:
            self.rad = math.atan2(self.y_change, self.x_change)
        nearest_enemy = None
        if(self.game.enemies.sprites()):
            nearest_enemy = min(self.game.enemies, key=lambda x: math.sqrt((x.rect.x - self.rect.x)**2 + (x.rect.y - self.rect.y)**2))
            if math.sqrt((nearest_enemy.rect.x - self.rect.x)**2 + (nearest_enemy.rect.y - self.rect.y)**2) < self.weapon.scope:
                dy = nearest_enemy.rect.y - self.rect.y
                dx = nearest_enemy.rect.x - self.rect.x
                self.rad = math.atan2(dy, dx)
        return nearest_enemy

class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y, mapx, mapy, map):
        self.game = game
        self._layer = ENERMY_LAYER
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = mapx + x * TILE_SIZE
        self.y = mapy + y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = "right"
        self.animation_loop = 1
        self.movement_loop = 0
        self.max_travel = random.randint(30, 60)

        self.image = self.game.enemy_spritesheet.get_sprite(3, 2, self.width, self.height)
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.rect.x  = self.x
        self.rect.y = self.y

        self.right_animations = [self.game.enemy_spritesheet.get_sprite(3, 66, self.width, self.height),
                            self.game.enemy_spritesheet.get_sprite(35, 66, self.width, self.height),
                            self.game.enemy_spritesheet.get_sprite(67, 66, self.width, self.height)]

        self.left_animations = [self.game.enemy_spritesheet.get_sprite(3, 98, self.width, self.height),
                            self.game.enemy_spritesheet.get_sprite(35, 98, self.width, self.height),
                            self.game.enemy_spritesheet.get_sprite(67, 98, self.width, self.height)]
    
        self.HP = 3
        self.room = map
        self.rad = 0

        self.weapon = Glock(self.game, self)
        self.weapon.delay *= 3

        self.attacking = False
        self.rand = random.randint(1, 4)

    def update(self):
        self.movement()
        self.collide_bullet()
        self.animate()
        self.rect.x += self.x_change
        self.collide_blocks("x")
        self.rect.y += self.y_change
        self.collide_blocks("y")

        self.x_change = 0
        self.y_change = 0

    def animate(self):
        if self.facing == "left":
            if self.x_change == 0 and self.y_change == 0:
                self.image = self.left_animations[0]
            else:
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
        if self.facing == "right":
            if self.x_change == 0 and self.y_change == 0:
                self.image = self.right_animations[0]
            else:
                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1

        if self.animation_loop >= 3:
            self.animation_loop = 1
        
    def collide_blocks(self, dir):
        hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
        hits += pygame.sprite.spritecollide(self, self.game.entrances, False)
        if hits:
            if (dir == "x"):
                if self.x_change > 0:
                    self.rect.right = hits[0].rect.left
                if self.x_change < 0:
                    self.rect.left = hits[0].rect.right
            if (dir == "y"):
                if self.y_change > 0:
                    self.rect.bottom = hits[0].rect.top
                if self.y_change < 0:
                    self.rect.top = hits[0].rect.bottom

    def collide_bullet(self):
        hits = pygame.sprite.spritecollide(self, self.game.bullets, False)
        if hits:
            self.HP -= hits[0].dmg
            hits[0].kill()
            if self.HP <= 0:
                self.kill()
                self.game.player.score += 1
                if self.game.player.mana <= self.game.player.max_mana - 10:
                    self.game.player.mana += 10
                else :
                    self.game.player.mana = self.game.player.max_mana

    def movement(self):
        if self.y_change != 0 or self.x_change != 0:
            self.rad = math.atan2(self.y_change, self.x_change)
        player = self.game.player
        distance = math.sqrt((player.rect.x - self.rect.x)**2 + (player.rect.y - self.rect.y)**2)
        if distance < ENEMY_SCOPE and self.room.open == False:
            self.taunted_movement(distance)
        else:
            self.normal_movement()
    
    def normal_movement(self):
        if self.rand == 1:
            self.y_change -= ENEMY_SPEED
        if self.rand == 2:
            self.y_change += ENEMY_SPEED
        if self.rand == 3:
            self.x_change -= ENEMY_SPEED
            self.facing = "left"
            self.rad = math.pi
        if self.rand == 4:
            self.x_change += ENEMY_SPEED
            self.facing = "right"
            self.rad = 0

        self.movement_loop -= 1
        if self.movement_loop <= -self.max_travel:
            self.movement_loop = 0
            self.rand = random.randint(1, 4)
            self.max_travel = random.randint(30, 60)
        pass

    def taunted_movement(self, distance = ENEMY_SCOPE):
        player = self.game.player
        dy = player.rect.y - self.rect.y
        dx = player.rect.x - self.rect.x
        self.rad = math.atan2(dy, dx)
        if distance > self.weapon.scope:
            self.x_change += ENEMY_SPEED * math.cos(self.rad)
            self.y_change += ENEMY_SPEED * math.sin(self.rad)
        elif self.weapon.can_shoot():
            self.weapon.shoot()
        
    def kill(self):
        self.weapon.kill()
        pygame.sprite.Sprite.kill(self)
class Boss(Enemy):
    def __init__(self, game, x, y, mapx, mapy, map):
        self.game = game
        # self.groups = self.game.all_sprites, self.game.boss
        # pygame.sprite.Sprite.__init__(self, self.groups)
        super().__init__(game, x, y, mapx, mapy, map)
        
        self.x = mapx + x * BOSS_SIZE
        self.y = mapy + y * BOSS_SIZE
        self.width = BOSS_SIZE
        self.height = BOSS_SIZE
        self.image = self.game.boss_spritesheet.get_sprite(0, 2, self.width, self.height)
        self.down_animations = [self.game.boss_spritesheet.get_sprite(3, 2, self.width, self.height),
                            self.game.boss_spritesheet.get_sprite(35, 2, self.width, self.height),
                            self.game.boss_spritesheet.get_sprite(67, 2, self.width, self.height)]
        
        self.up_animations = [self.game.boss_spritesheet.get_sprite(3, 34, self.width, self.height),
                            self.game.boss_spritesheet.get_sprite(35, 34, self.width, self.height),
                            self.game.boss_spritesheet.get_sprite(67, 34, self.width, self.height)]

        self.right_animations = [self.game.boss_spritesheet.get_sprite(12,83, self.width, self.height),
                            self.game.boss_spritesheet.get_sprite(93,75, self.width, self.height),
                            self.game.boss_spritesheet.get_sprite(190, 75, self.width, self.height)]

        self.left_animations = [self.game.boss_spritesheet.get_sprite(18, 160, self.width, self.height),
                            self.game.boss_spritesheet.get_sprite(113, 160, self.width, self.height),
                            self.game.boss_spritesheet.get_sprite(203, 160, self.width, self.height)]
        self.HP = 10
        self.weapon = random.choice([Glock(self.game, self), AK47(self.game, self), Sniper(self.game, self)])
        self.dmg = 0
  
    def animate(self):
        if self.facing == "left":
            if self.x_change == 0 and self.y_change == 0:
                self.image = self.game.boss_spritesheet.get_sprite(3, 66, self.width, self.height)
            else:
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
        if self.facing == "right":
            if self.x_change == 0 and self.y_change == 0:
                self.image = self.game.boss_spritesheet.get_sprite(12, 83, self.width, self.height)
            else:
                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1

        if self.animation_loop >= 3:
            self.animation_loop = 1
    def collide_blocks(self, dir):
        hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
        hits += pygame.sprite.spritecollide(self, self.game.entrances, False)
        if hits:
            if (dir == "x"):
                if self.x_change > 0:
                    self.rect.right=hits[0].rect.left
                    
                if self.x_change < 0:
                    self.rect.left = hits[0].rect.right
            if (dir == "y"):
                if self.y_change > 0:
                    self.rect.bottom = hits[0].rect.top
                 
                if self.y_change < 0:
                    self.rect.top = hits[0].rect.bottom
              
class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y, mapx, mapy):

        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = mapx + x * TILE_SIZE
        self.y = mapy + y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.image = self.game.terrain_spritesheet.get_sprite(384, 576, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Ground(pygame.sprite.Sprite):
    def __init__(self, game, x, y, mapx, mapy):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = mapx + x * TILE_SIZE
        self.y = mapy + y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.image = self.game.terrain_spritesheet.get_sprite(64, 352, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Attack(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = PLAYER_LAYER
        self.game = game
        self.x = x
        self.y = y
        self.width = WEAPON_SIZE
        self.height = WEAPON_SIZE
        self.groups = self.game.all_sprites, self.game.attacks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.animation_loop = 0
        self.image = self.game.attack_spritesheet.get_sprite(0, 0, self.width, self.height)
        
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.animate()
        self.collide()

    def collide(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, True)

    def animate(self):
        direction = self.game.player.facing

        right_animations = [self.game.attack_spritesheet.get_sprite(0, 64, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(32, 64, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(64, 64, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(96, 64, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(128, 64, self.width, self.height)]

        down_animations = [self.game.attack_spritesheet.get_sprite(0, 32, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(32, 32, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(64, 32, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(96, 32, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(128, 32, self.width, self.height)]

        left_animations = [self.game.attack_spritesheet.get_sprite(0, 96, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(32, 96, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(64, 96, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(96, 96, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(128, 96, self.width, self.height)]

        up_animations = [self.game.attack_spritesheet.get_sprite(0, 0, self.width, self.height),
                         self.game.attack_spritesheet.get_sprite(32, 0, self.width, self.height),
                         self.game.attack_spritesheet.get_sprite(64, 0, self.width, self.height),
                         self.game.attack_spritesheet.get_sprite(96, 0, self.width, self.height),
                         self.game.attack_spritesheet.get_sprite(128, 0, self.width, self.height)]
        
        if direction == "up":
            self.image = up_animations[math.floor(self.animation_loop)]
        if direction == "down":
            self.image = down_animations[math.floor(self.animation_loop)]
        if direction == "left":
            self.image = left_animations[math.floor(self.animation_loop)]
        if direction == "right":
            self.image = right_animations[math.floor(self.animation_loop)]

        self.animation_loop += 0.5
        if self.animation_loop >= 5:
            self.kill()
    #end
#end           
class Bullet(pygame.sprite.Sprite):
    def __init__(self, game, heading, rad, dmg, rad_offset, speed, owner):
        self._layer = BULLET_LAYER
        self.game = game
        self.dmg = dmg
        self.x = heading[0]
        self.y = heading[1]
        self.width = 10
        self.height = 10
        if isinstance(owner, Enemy):
            self.groups = self.game.all_sprites, self.game.enemies_bullets
        else:
            self.groups = self.game.all_sprites, self.game.bullets
            
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(WHITE)
        pygame.draw.circle(self.image, YELLOW, (self.width//2, self.height//2), self.width//2)
        self.image.set_colorkey(WHITE)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.x_change = 0
        self.y_change = 0
        self.rad = rad + random.randint(-abs(rad_offset), abs(rad_offset)) * math.pi/180
        self.max_travel = WIN_WIDTH
        self.speed = speed
        
    def movement(self):
        self.rect.x += self.speed * math.cos(self.rad)
        self.rect.y += self.speed * math.sin(self.rad)
        self.max_travel -= self.speed
        if self.max_travel <= 0:
            self.kill()

    def update(self):
        self.movement()
        self.collide_blocks()
        self.rect.x += self.x_change
        self.rect.y += self.y_change

    def collide_blocks(self):
        hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
        hits += pygame.sprite.spritecollide(self, self.game.entrances, False)
        if hits:
            self.kill()

#TODO: scope rieng cho quai va nguoi choi
#BUG: quai quay lung lai khi tan cong
class Gun(pygame.sprite.Sprite):
    def update(self):
        self.rad = self.owner.rad
        self.animate()
        self.movement()

    def animate(self):
        next_image = self.shoot_animation[math.floor(self.animation_loop)].copy()
        if self.have_left_target(): 
            next_image = pygame.transform.flip(next_image.copy(), True, False)
            rad = self.rad + math.pi
            self.owner.facing = "left"
            if self.alive():
                self.game.all_sprites.change_layer(self, self.owner._layer - 1)
                self.game.guns.change_layer(self, self.owner._layer - 1)
            self.image = pygame.transform.rotate(next_image, math.degrees(-rad))
        else: 
            self.owner.facing = "right"
            if self.alive():
                self.game.all_sprites.change_layer(self, self.owner._layer + 1)
                self.game.guns.change_layer(self, self.owner._layer + 1)
            self.image = pygame.transform.rotate(next_image, math.degrees(-self.rad))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect(center=self.rect.center)

        if self.owner.attacking:
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.animation_loop = 0
                self.owner.attacking = False

    def movement(self):
        if self.owner.facing == "right":
            self.rect.center = (self.owner.rect.centerx + self.place_right[0], self.owner.rect.centery + self.place_right[1])
        if self.owner.facing == "left":
            self.rect.center = (self.owner.rect.centerx - self.place_right[0], self.owner.rect.centery + self.place_right[1])

    def have_left_target(self):
        return (self.rad > -math.pi and self.rad < -math.pi/2) or (self.rad >= math.pi/2 and  self.rad <= math.pi)
    
    def shoot(self):
        Bullet(self.game, self.find_heading(), self.rad, self.bullet_dmg, self.rad_offset, self.speed, self.owner)
        if isinstance(self.owner, Player):
            self.owner.mana -= self.manacost

    def can_shoot(self):
        now = pygame.time.get_ticks()
        if now - self.timer > self.delay and (isinstance(self.owner, Enemy) or self.owner.mana >= self.manacost):
            self.timer = now
            return True
        return False
    
    def find_heading(self):
        center_image = (self.width/2, self.height/2)
        vector = (self.headpos[0] - center_image[0], self.headpos[1] - center_image[1])
        hypotenuse = math.sqrt(vector[0]**2 + vector[1]**2)
        alpha = math.acos(vector[0]/hypotenuse)
        if self.owner.facing == "right":
            alpha = -alpha
        headx = self.rect.centerx +  hypotenuse * math.cos(self.rad+alpha)
        heady = self.rect.centery +  hypotenuse * math.sin(self.rad+alpha)
        return headx, heady

class Glock(Gun):
    def __init__(self, game, owner, delay = GLOCK_DELAY):
        self._layer = GUN_LAYER
        self.game = game
        self.owner = owner
        self.x = self.owner.rect.centerx
        self.y = self.owner.rect.centery
        self.width = 48
        self.height = 32
        self.groups = self.game.all_sprites, self.game.guns
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.animation_loop = 0
        self.image = self.game.glock_spritesheet.get_sprite(0, 0, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        self.shoot_animation = [self.game.glock_spritesheet.get_sprite(0, 0, self.width, self.height),
                            self.game.glock_spritesheet.get_sprite(48, 0, self.width, self.height),
                            self.game.glock_spritesheet.get_sprite(96, 0, self.width, self.height),
                            self.game.glock_spritesheet.get_sprite(144, 0, self.width, self.height),
                            self.game.glock_spritesheet.get_sprite(192, 0, self.width, self.height)]
        self.timer = 0
        self.rad = self.owner.rad
        self.scope = GLOCK_SCOPE
        self.delay = delay
        self.bullet_dmg = 1
        self.rad_offset = 3

        #pos against player to place gun when facing right
        self.place_right = (8, 6)
        self.headpos = (40, 8)
        self.manacost = 0
        self.speed = GLOCK_BULLET_SPEED
        

class AK47(Gun):
    def __init__(self, game, owner, delay = AK47_DELAY):
        self._layer = GUN_LAYER
        self.game = game
        self.owner = owner
        self.x = self.owner.rect.centerx
        self.y = self.owner.rect.centery
        self.width = 64
        self.height = 16
        self.groups = self.game.all_sprites, self.game.guns
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.animation_loop = 0
        self.image = self.game.ak47_spritesheet.get_sprite(0, 0, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        self.shoot_animation = [self.game.ak47_spritesheet.get_sprite(0, 0, self.width, self.height),
                            self.game.ak47_spritesheet.get_sprite(64, 0, self.width, self.height),
                            self.game.ak47_spritesheet.get_sprite(128, 0, self.width, self.height),
                            self.game.ak47_spritesheet.get_sprite(192, 0, self.width, self.height),
                            self.game.ak47_spritesheet.get_sprite(256, 0, self.width, self.height)]
        self.timer = 0
        self.rad = self.owner.rad
        self.scope = AK47_SCOPE
        self.delay = delay
        self.bullet_dmg = 1
        self.rad_offset = 4
        #pos against player to place gun when facing right
        self.place_right = (6, 4)
        self.headpos = (48, 4)
        self.manacost = 2
        self.speed = AK47_BULLET_SPEED

class Sniper(Gun):
    def __init__(self, game, owner,delay = SNIPER_DELAY):
        self._layer = GUN_LAYER
        self.game = game
        self.owner = owner
        self.x = self.owner.rect.centerx
        self.y = self.owner.rect.centery
        self.width = 80
        self.height = 32
        self.groups = self.game.all_sprites, self.game.guns
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.animation_loop = 0
        self.image = self.game.sniper_spritesheet.get_sprite(0, 0, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        self.shoot_animation = [self.game.sniper_spritesheet.get_sprite(0, 0, self.width, self.height),
                            self.game.sniper_spritesheet.get_sprite(80, 0, self.width, self.height),
                            self.game.sniper_spritesheet.get_sprite(160, 0, self.width, self.height),
                            self.game.sniper_spritesheet.get_sprite(240, 0, self.width, self.height),
                            self.game.sniper_spritesheet.get_sprite(320, 0, self.width, self.height)]
        
        self.timer = 0
        self.rad = self.owner.rad
        self.scope = SNIPER_SCOPE
        self.delay = delay
        self.bullet_dmg = 3
        self.rad_offset = 0
        #pos against player to place gun when facing right
        self.place_right = (8, 4)
        self.headpos = (48, 6)
        self.manacost = 5
        self.speed = SNIPER_BULLET_SPEED

class Entrance(pygame.sprite.Sprite):
    def __init__(self, game, x, y, mapx, mapy):
        self.enable = True
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.entrances, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = mapx + x * TILE_SIZE
        self.y = mapy + y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.image = self.game.terrain_spritesheet.get_sprite(384, 576, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        if(self.enable): 
            self.image = self.game.terrain_spritesheet.get_sprite(704, 160, self.width, self.height)
            self.game.blocks.add(self)
            self.game.entrances.remove(self)
        else:
            self.image = self.game.terrain_spritesheet.get_sprite(95, 576, self.width, self.height)
            self.game.blocks.remove(self)
            self.game.entrances.add(self)

class Button:
    def __init__(self, x, y, width, height, fg, bg, content, fontsize):
        self.font = pygame.font.Font('Arial.ttf', fontsize)
        self.content = content
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.width = width
        self.fg = fg

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(bg)
        self.rect = self.image.get_rect()
        
        self.rect.x = self.x
        self.rect.y = self.y
        self.text = self.font.render(self.content, True, self.fg)
        self.text_rect = self.text.get_rect(center=(self.width/2, self.height/2))
        self.image.blit(self.text, self.text_rect)

    def isPressed(self, mousepos, pressed):
        if self.rect.collidepoint(mousepos):
            if pressed[0]:
                return True
        return False
    
class MyMap(pygame.sprite.Sprite): 
    def __init__(self, tilemap, game, phase_num = 0):
        self._layer = MAP_LAYER
        self.mappingpos = [0, 0]
        self.tilemap = tilemap
        self.bossmap=bossmap
        self.isDrawn = False
        self.game = game
    
        #start position of the map including the border
        self.x = 0
        self.y = 0
        #display a invisible rect to check if player is in the map, it not include the border(32 pixels block)
        self.image = pygame.Surface((WIN_WIDTH - TILE_SIZE*2, WIN_HEIGHT - TILE_SIZE*2))
        self.rect = self.image.get_rect()

        self.top = None
        self.bottom = None
        self.left = None
        self.right = None
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.entrances = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.boss=pygame.sprite.Group()
        self.boss_entrances = pygame.sprite.Group()
        self.open = True
        self.max_phase = phase_num
        self.current_phase = 1
        self.available_pos = []
        self.clear = False

    def draw(self):
        self.create_tilemap()
        self.isDrawn = True

    def checkEntrance(self, i, j):
        if(self.top != None):
            if i == 0 and j > 6 and j < 13:
                return True
        if(self.bottom != None):
            if i == 14 and j > 6 and j < 13:
                return True
        if(self.left != None):
            if j == 0 and i > 4 and i < 10:
                return True
        if(self.right != None):
            if j == 19 and i > 4 and i < 10:
                return True
        return False

    def update(self):
        self.update_phase()
        num_enemies = len(self.game.enemies.sprites())
        print(num_enemies)
        num_boss = len(self.boss.sprites())
        print("num_boss", num_boss)
        if num_enemies != 0:
        
                    for entrance in self.entrances:
                        if entrance not in self.boss_entrances:  
                            entrance.enable = False
                    self.open = True
                    for boss_entrance in self.boss_entrances:
                        boss_entrance.enable = True
                        
                    self.open = False
        if num_enemies ==0:
            for entrance in self.entrances:
                entrance.enable = True
            self.open = False
            for boss_entrance in self.boss_entrances:
                boss_entrance.enable = False
            self.open = True
        if(num_enemies == 0 and num_boss==0 and self.current_phase >= self.max_phase):
                
                self.clear = True     
        if self.rect.contains(self.game.player.rect) and self.enemies:
            for entrance in self.entrances:
                entrance.enable = True
            self.open = False
        else:
            for entrance in self.entrances:
                if entrance not in self.boss_entrances:
                    entrance.enable = False
                self.open = True
        
       
            
    def update_phase(self):
        num_enemies = len(self.enemies.sprites())
        
       
            # if self.rect.contains(self.game.player.rect) and self.boss:
            #     for boss_entrance in self.boss_entrances:
            #         boss_entrance.enable = True
            #     self.open = False
        if( num_enemies == 0 and self.current_phase < self.max_phase):
            self.current_phase += 1
            #chon 5 vi tri random de tao enemy
            enemies_pos = random.sample(self.available_pos, 1)
            for pos in enemies_pos:
                enemy = Enemy(self.game, pos[0], pos[1], self.rect.x-32, self.rect.y-32, self)
                self.enemies.add(enemy)

    def update_rect(self):
        #start position of the map including the border
        self.x = self.mappingpos[0] * WIN_WIDTH
        self.y = self.mappingpos[1] * WIN_HEIGHT
        self.rect.topleft = ( 32 + self.mappingpos[0] * WIN_WIDTH, 32 + self.mappingpos[1] * WIN_HEIGHT)
        
    def create_tilemap(self):
        boss_position = None
        for i, row in enumerate(self.tilemap):
            for j, col in enumerate(row):
                if col == 'B':
                    if(self.checkEntrance(i, j)):
                        sprite = Entrance(self.game, j, i, self.x, self.y)
                        self.entrances.add(sprite)
                      
                    else: Block(self.game, j, i, self.x, self.y)
                if col == 'E':
                    enemy = Enemy(self.game, j, i, self.x, self.y, self)
                    self.enemies.add(enemy)
                if col == 'P':
                    self.game.player = Player(self.game, j, i, self.x, self.y)
                    self.game.player.set_weapons()
                if col == "M":
                    boss= Boss(self.game, j, i, self.x, self.y, self)
                    self.boss.add(boss)    
                    
                    boss_position = (i, j)
                if boss_position:
                    boss_entrance_positions = [
                        (boss_position[0] - 2, boss_position[1]-9),
                        (boss_position[0] - 1, boss_position[1]-9),
                        (boss_position[0], boss_position[1] - 9),
                        (boss_position[0]+1, boss_position[1] -9),
                        (boss_position[0]+2,boss_position[1]-9)
        ]           
                    for pos in boss_entrance_positions:
                        sprite = Entrance(self.game, pos[1], pos[0], self.x, self.y)
                        self.boss_entrances.add(sprite)       
                if col == 'E' or col == 'P' or col == '.' :
                    self.available_pos.append([j, i])
                if(col == ' '): continue
                Ground(self.game, j, i, self.x, self.y)
        
class MapList:
    def __init__(self, tilemaps, game):
        self.maps = []
        self.pipes = []
        self.game = game
        for tilemap in tilemaps:
            self.maps.append(MyMap(tilemap, game, 2))
            
        #print(len(self.maps)) #check 
        
        self.maps.append(MyMap(bossmap, game, 1))
        #print(len(self.maps)) # check thành công ra len 6, chèn thêm map cho boss success

        self.maps[0].max_phase  = 0
        self.link(self.maps[0], self.maps[1], "right")
        self.link(self.maps[1], self.maps[2], "top")
        self.link(self.maps[1], self.maps[3], "bottom")
        self.link(self.maps[1], self.maps[4], "right")
        self.link(self.maps[4], self.maps[5], "right")
        
    def draw(self):
        self.DFS_draw(self.maps[0])

    def DFS_draw(self, map):
        map.draw()
        for adj in [map.top, map.bottom, map.left, map.right]:
            if  adj != None and not adj.isDrawn:
                self.DFS_draw(adj)

    def link(self, m1, m2, dir):
        pipe = MyMap(hpipemap, self.game)
        self.pipes.append(pipe)
        
        if(dir == "right"):
            pipe.tilemap = hpipemap
            m1.right = pipe
            pipe.right = m2
            m2.left = pipe
            m2.mappingpos = [m1.mappingpos[0] + 2, m1.mappingpos[1]]
            pipe.mappingpos = [m1.mappingpos[0] + 1, m1.mappingpos[1]]
        if(dir == "left"):
            pipe.tilemap = hpipemap
            m1.left = pipe
            pipe.left = m2
            m2.right = pipe
            m2.mappingpos = [m1.mappingpos[0] - 2, m1.mappingpos[1]]
            pipe.mappingpos = [m1.mappingpos[0] - 1, m1.mappingpos[1]]
        if(dir == "top"):
            pipe.tilemap = vpipemap
            m1.top = pipe
            pipe.top = m2
            m2.bottom = pipe
            m2.mappingpos = [m1.mappingpos[0], m1.mappingpos[1] - 2]
            pipe.mappingpos = [m1.mappingpos[0], m1.mappingpos[1] - 1]
        if(dir == "bottom"):
            pipe.tilemap = vpipemap
            m1.bottom = pipe
            pipe.bottom = m2
            m2.top = pipe
            m2.mappingpos = [m1.mappingpos[0], m1.mappingpos[1] + 2]
            pipe.mappingpos = [m1.mappingpos[0], m1.mappingpos[1] + 1]

        m1.update_rect()
        m2.update_rect()
        pipe.update_rect()

    def check_win(self):
        for map in self.maps:
            if map.clear == False:
                return False
        return True
    

class PlayerBars(pygame.sprite.Sprite):
    def __init__(self, game):
        self._layer = UI_LAYER
        self.groups = game.bars
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.font = pygame.font.Font('Arial.ttf', 16)

        self.image = pygame.Surface((180, 92))
        self.rect = self.image.get_rect()
        self.rect.x = 10
        self.rect.y = 10

        self.health_bg = pygame.Surface((128, 20))
        self.health_bg.fill(DARK_BROWN)
        self.armour_bg = pygame.Surface((128, 20))
        self.armour_bg.fill(DARK_BROWN)
        self.mana_bg = pygame.Surface((128, 20))
        self.mana_bg.fill(DARK_BROWN)

        self.health_bg_rect = self.health_bg.get_rect()
        self.armour_bg_rect = self.armour_bg.get_rect()
        self.mana_bg_rect = self.mana_bg.get_rect()
        self.health_bg_rect.topleft = (42, 8)
        self.armour_bg_rect.topleft = (42, 36)
        self.mana_bg_rect.topleft = (42, 64)

        self.health_icon = pygame.Surface((20, 20))
        self.health_icon.fill(RED)
        self.armour_icon = pygame.Surface((20, 20))
        self.armour_icon.fill(GREY)
        self.mana_icon = pygame.Surface((20, 20))
        self.mana_icon.fill(BLUE)
        
        self.health_bar = pygame.Surface((128, 20))
        self.health_bar.fill(RED)
        self.armour_bar = pygame.Surface((128, 20))
        self.armour_bar.fill(GREY)
        self.mana_bar = pygame.Surface((128, 20))
        self.mana_bar.fill(BLUE)

        self.health_bar_rect = self.health_bar.get_rect()
        self.health_bar_rect.topleft = (0 ,0)
        self.armour_bar_rect = self.armour_bar.get_rect()
        self.armour_bar_rect.topleft = (0 ,0)
        self.mana_bar_rect = self.mana_bar.get_rect()
        self.mana_bar_rect.topleft = (0 ,0)
        
        self.health_bg.blit(self.health_bar, self.health_bar_rect)
        self.armour_bg.blit(self.armour_bar, self.armour_bar_rect)
        self.mana_bg.blit(self.mana_bar, self.mana_bar_rect)

        self.image.fill(BROWN)
        self.image.blit(self.health_bg, self.health_bg_rect)
        self.image.blit(self.armour_bg, self.armour_bg_rect)
        self.image.blit(self.mana_bg, self.mana_bg_rect)
        self.image.blit(self.health_icon, (10, 8))
        self.image.blit(self.armour_icon, (10, 36))
        self.image.blit(self.mana_icon, (10, 64))
        
    def update(self):
        self.draw_HP()
        self.draw_AR()
        self.draw_MP()
        pass

    def draw_HP(self):
        self.health_bg.fill(DARK_BROWN)
        self.health_bar_rect.right = 128 * self.game.player.HP / self.game.player.max_hp
        info = self.font.render(f"{self.game.player.HP}/{self.game.player.max_hp}", True, WHITE)
        info_rect = info.get_rect()
        info_rect.center = self.health_bg_rect.center
        self.health_bg.blit(self.health_bar, self.health_bar_rect)
        self.image.blit(self.health_bg, self.health_bg_rect)
        self.image.blit(info, info_rect)
    
    def draw_AR(self):
        self.armour_bg.fill(DARK_BROWN)
        self.armour_bar_rect.right = 128 * self.game.player.armour / self.game.player.max_armour
        info = self.font.render(f"{self.game.player.armour}/{self.game.player.max_armour}", True, WHITE)
        info_rect = info.get_rect()
        info_rect.center = self.armour_bg_rect.center
        self.armour_bg.blit(self.armour_bar, self.armour_bar_rect)
        self.image.blit(self.armour_bg,  self.armour_bg_rect)
        self.image.blit(info, info_rect)
    
    def draw_MP(self):
        self.mana_bg.fill(DARK_BROWN)
        self.mana_bar_rect.right = 128 * self.game.player.mana / self.game.player.max_mana
        info = self.font.render(f"{self.game.player.mana}/{self.game.player.max_mana}", True, WHITE)
        info_rect = info.get_rect()
        info_rect.center = self.mana_bg_rect.center
        self.mana_bg.blit(self.mana_bar, self.mana_bar_rect)
        self.image.blit(self.mana_bg, self.mana_bg_rect)
        self.image.blit(info, info_rect)

