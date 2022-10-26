# TO USE RUN 
# pip install -r requirements.txt
# in console and then start the program

import sys
import pygame
from pygame.math import Vector2
import time
import random

# Ball or player object
class ball (pygame.sprite.Sprite):

    def __init__(self, pos, *groups):
        super().__init__(*groups)
        self.image = pygame.Surface((20, 20))
        self.image.fill(pygame.Color('dodgerblue'))
        self.rect = self.image.get_rect(center=pos)
        self.health = 5
        self.invincible = False
    
    def sethealth(self, health):
        self.health = health
    
    def set_invincible(self):
        self.invincible = True
    
    def unset_invincible(self):
        self.invincible = False
    
# Bullet object
class bullet (pygame.sprite.Sprite):

    def __init__(self, pos, *groups):
        super().__init__(*groups)
        self.image = pygame.Surface((60, 60))
        self.image.fill(pygame.Color('sienna1'))
        self.rect = self.image.get_rect(center=pos)
    
    def setcolor(self, color):
        self.image.fill(pygame.Color(color))

class shield (pygame.sprite.Sprite):
    def __init__(self, pos, *groups):
        super().__init__(*groups)
        self.image = pygame.Surface((10, 10))
        self.image.fill(pygame.Color("blue"))
        self.rect = self.image.get_rect(center = pos)


class heal (pygame.sprite.Sprite):
    def __init__ (self, pos, *groups):
        super().__init__(*groups)
        self.image = pygame.Surface((10, 10))
        self.image.fill(pygame.Color("red"))
        self.rect = self.image.get_rect(center = pos)

# Shield - deletes bullets
# HP system
# Heal
# Damage cooldown
# Cubes ~ to screen size (and player as well)

# Game over screen
def gameOver(score, screen):
   
    font = pygame.font.SysFont('TimesNewRoman', 30)
    textsurface = font.render(f'Game over; Score: {score}', False, (255, 255, 255))
    textsurfaceinstructions = font.render('Press SPACE to continue, ENTER to exit', False, (255, 255, 255))
    
    while True:
        screen.fill((20,20,20))
        screen.blit(textsurface,(200, 200))
        screen.blit(textsurfaceinstructions, (100, 300))
        pygame.display.update()
        break

def gameStart(screen):
    font = pygame.font.SysFont('TimesNewRoman', 30)
    textsurfaceinstructions = font.render('Press SPACE to continue, ENTER to exit', False, (255, 255, 255))
    
    while True:
        screen.fill((20,20,20))
        screen.blit(textsurfaceinstructions, (100, 300))
        pygame.display.update()
        break
    
    

# Main game body 



def main():
    # Screen and groups setup
    
    #gameStart(screen)
    
    clock = pygame.time.Clock()
    all_sprites = pygame.sprite.Group()
    bullet_group = pygame.sprite.Group()
    shield_group = pygame.sprite.Group()
    heal_group = pygame.sprite.Group()
    all_sprites.add(bullet_group)
    all_sprites.add(heal_group)
    all_sprites.add(shield_group)
    player = ball((100, 300), all_sprites)
    
      
    # INIT, do not edit
    done = False
    score = 0
    time_snapshot = time.time()
    time_start = time.time()
    time_last_damaged = time.time()
    invincible_time_start = time.time()
    
    
    # =====================
    # SETUP GAME PARAMETERS 
    
    enemy_spawn_delay = 0.7
    bullets_per_delay = 2
    bullet_speed = 7
    damage_cooldown = 0.5
    invincible_time = 10
    
    # =====================
    
    # Active game loop
    while not done:
        for event in pygame.event.get():
            
            # On Quit method
            if event.type == pygame.QUIT:
                done = True
                
            # Follow the mouse motion type
            elif event.type == pygame.MOUSEMOTION:
                player.rect.center = event.pos
        
        # Check invincibility timer and other effects
        if time.time() - invincible_time_start > invincible_time and player.invincible==True:
                player.unset_invincible()
                print("Shield ended!")
        
        # Move entities     
        for item in bullet_group:
            item.rect.left -= bullet_speed
        
        for item in shield_group:
            item.rect.left -= bullet_speed
        
        for item in heal_group:
            item.rect.left -= bullet_speed
        
        # Update score
        score = int(time.time() - time_start)
        
        # SPAWN new entities
        if (time.time()-time_snapshot) >= enemy_spawn_delay:
            w, h = pygame.display.get_surface().get_size()
            for create in range (bullets_per_delay):
                bullet_group.add(bullet((w+100, random.randint(0, h))))
                
                if random.randint(0,100)<=5:
                    heal_group.add(heal((w+180, random.randint(0, h))))
                
                if random.randint(0, 100) <= 5 :
                    shield_group.add(shield((w+180, random.randint(0, h))))
                
            all_sprites.add(bullet_group)
            all_sprites.add(heal_group)
            all_sprites.add(shield_group)
            time_snapshot = time.time()
     
        all_sprites.update()
        
        
        # Check which enemies collided with the player.
        collided_enemies = pygame.sprite.spritecollide(player, bullet_group, False)
        collided_heals = pygame.sprite.spritecollide(player, heal_group, False)
        collided_shields = pygame.sprite.spritecollide(player, shield_group, False)

        screen.fill((30, 30, 30))
        all_sprites.draw(screen)
        
        if collided_heals !=[]:
            for healitem in collided_heals:
                healitem.kill()
                player.sethealth(5)
                print(f'Healed! Health: {player.health}')
            
        if collided_shields !=[]:
            for shielditem in collided_shields:
                shielditem.kill()
                player.set_invincible()
                invincible_time_start = time.time() 
                print("SHIELD COLLECTED")
        
        # Lose on collision
        if (collided_enemies != []):
            
            cooldown_flag = False
            
            if player.invincible == True:
                player.unset_invincible()
                time_last_damaged = time.time()
                print("Shield used!")
            
            if time.time() - time_last_damaged > damage_cooldown:
                cooldown_flag = True
                time_last_damaged = time.time()
                player.health -= 1
                print (f'Health: {player.health}')
                
                if player.health == 0:
                    done = True
            
            for enemy in collided_enemies:
                # Draw rects around the collided enemies.
                if cooldown_flag == True:
                    enemy.kill()
                    pygame.draw.rect(screen, (0, 190, 120), enemy.rect, 4)
                    
                # else:
                #     enemy.setcolor("red")
        
        # Update screen
        pygame.display.flip()
        clock.tick(30)
    
    # Gameover screen output
    gameOver(score, screen)
    
    # Keybinds in gameover menu
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_SPACE:
                    main()

# Main class to run the program

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((1600, 900), pygame.RESIZABLE)
    main()