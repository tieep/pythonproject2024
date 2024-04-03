import pygame
from sprites import *
from config import *
import sys

#                            _
#                         _ooOoo_
#                        o8888888o
#                        88" . "88
#                        (| -_- |)
#                        O\  =  /O
#                     ____/`---'\____
#                   .'  \\|     |//  `.
#                  /  \\|||  :  |||//  \
#                 /  _||||| -:- |||||_  \
#                 |   | \\\  -  /'| |   |
#                 | \_|  `\`---'//  |_/ |
#                 \  .-\__ `-. -'__/-.  /
#               ___`. .'  /--.--\  `. .'___
#            ."" '<  `.___\_<|>_/___.' _> \"".
#           | | :  `- \`. ;`. _/; .'/ /  .' ; |
#           \  \ `-.   \_\_`. _.'_/_/  -' _.' /
# ===========`-.`___`-.__\ \___  /__.-'_.'_.-'================
#                         `=--=-'                              


class Game:    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('Arial.ttf', 32)
        self.running = True
        self.boss_defeated = False
        self.character_spritesheet = Spritesheet('img/character.png')
        self.terrain_spritesheet = Spritesheet('img/terrain.png')
        self.enemy_spritesheet = Spritesheet('img/enemy.png')
        self.attack_spritesheet = Spritesheet('img/attack.png')
        self.intro_background = pygame.image.load('img/introbackground.png')
        self.gameover_background = pygame.image.load('img/gameover.png')
        self.glock_spritesheet = Spritesheet('img/Glock-SpriteSheet.png')
        self.ak47_spritesheet = Spritesheet('img/AK47-SpriteSheet.png')
        self.sniper_spritesheet = Spritesheet('img/SniperRifle-SpriteSheet.png')
        self.boss_spritesheet = Spritesheet('img/boss1.jpg')
        self.t1 = pygame.time.get_ticks()
        self.player: Player = None
 
    def create_tilemap(self):
        self.maps = MapList(tilemaps, self)
        self.maps.draw()
        
    # new game start
    def new(self):
        self.playing = True
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.boss=pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        self.bullets = pygame.sprite.LayeredUpdates()
        self.guns = pygame.sprite.LayeredUpdates()
        self.entrances = pygame.sprite.LayeredUpdates()
        self.enemies_bullets = pygame.sprite.LayeredUpdates()
        #player health and armor bar
        self.bars = pygame.sprite.LayeredUpdates()
        self.create_tilemap()
        PlayerBars(self)

    def events(self):
        #game loop events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.player.facing == 'right':
                        Attack(self, self.player.rect.x + 32, self.player.rect.y)
                    if self.player.facing == 'left':
                        Attack(self, self.player.rect.x - 32, self.player.rect.y)
                    if self.player.facing == 'up':
                        Attack(self, self.player.rect.x, self.player.rect.y - 32)
                    if self.player.facing == 'down':
                        Attack(self, self.player.rect.x, self.player.rect.y + 32)
                if event.key == pygame.K_1:
                    self.player.change_weapon(0)
                elif event.key == pygame.K_2:
                    self.player.change_weapon(1)
                elif event.key == pygame.K_3:
                    self.player.change_weapon(2)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and self.player.weapon != None and self.player.weapon.can_shoot():
                    self.player.attacking = True
                    self.player.weapon.shoot()
                pass

    def update(self):
        self.all_sprites.update()
        self.bars.update()
        
    def draw(self):
        #game loop draw
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        #draw health and armor bar
        self.bars.draw(self.screen)
        self.clock.tick(FPS)
        pygame.display.update()

    def main(self):
        #game loop
        while(self.playing):
            self.events()
            self.update()
            if self.maps.check_win():
                self.playing = False
            self.draw()

    def gameover(self):
        text = self.font.render('Game Over', True, RED)
        text_rect = text.get_rect(center=(WIN_WIDTH/2, WIN_HEIGHT/2))

        restart_button = Button(10, 50, 120, 50, WHITE, BLACK,'Restart', 32)

        for sprite in self.all_sprites:
            sprite.kill()

        while(self.running):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
        
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()
            if restart_button.isPressed(mouse_pos, mouse_pressed):
                self.new()
                self.main()

            self.screen.blit(self.gameover_background, (0,0))
            self.screen.blit(text, text_rect)
            self.screen.blit(restart_button.image, restart_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()
        pass

    def win_screen(self):
        outro = True
        title = self.font.render('Pygame RPG', True, BLACK)
        title_rect = title.get_rect(x=10,y=10)
        text = self.font.render('You win!!!', True, BLUE)
        text_rect = text.get_rect(center=(WIN_WIDTH/2, WIN_HEIGHT/2))

        play_button = Button(10, 50, 120, 50, WHITE, GREY,'Play', 32)
        exit_button = Button(10, 120, 120, 50, WHITE, RED,'Exit', 32)
        while(outro):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    outro = False
            
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()
            if play_button.isPressed(mouse_pos, mouse_pressed):
                outro = False
            if exit_button.isPressed(mouse_pos, mouse_pressed):
                self.running = False
                outro = False
            self.screen.blit(self.intro_background, (0,0))
            self.screen.blit(title, title_rect)
            self.screen.blit(play_button.image, play_button.rect)
            self.screen.blit(exit_button.image, exit_button.rect)
            self.screen.blit(text, text_rect)
            self.clock.tick(FPS)
            pygame.display.update()

        if self.running:
            self.new()

    def intro_screen(self):
        intro = True
        title = self.font.render('Pygame RPG', True, BLACK)
        title_rect = title.get_rect(x=10,y=10)
        text = self.font.render('Let\'s Play', True, RED)
        text_rect = text.get_rect(center=(WIN_WIDTH/2, WIN_HEIGHT/2))

        play_button = Button(10, 50, 120, 50, WHITE, BLACK,'Play', 32)
        
        while(intro):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    intro = False
            
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()
            if play_button.isPressed(mouse_pos, mouse_pressed):
                intro = False
            
            self.screen.blit(self.intro_background, (0,0))
            self.screen.blit(title, title_rect)
            self.screen.blit(play_button.image, play_button.rect)
            self.screen.blit(text, text_rect)
            self.clock.tick(FPS)
            pygame.display.update()
        pass
def main():
    g = Game()
    g.intro_screen()
    g.new()
    while(g.running):
        g.main()
        if g.maps.check_win():
            g.win_screen()
        else: g.gameover()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()