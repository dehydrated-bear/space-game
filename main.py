import pygame
import os
import random 
from random import uniform
import math

pygame.init()


WIDTH,HEIGHT=1280,720

screen=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("spaceship")
running=True
clock=pygame.time.Clock()



surf=pygame.Surface((100,200))
surf.fill("orange")

meteor_img=pygame.image.load(os.path.join("images","meteor.png")).convert_alpha()
meteor_rect=meteor_img.get_frect(center=(WIDTH/2,HEIGHT/2))
font=pygame.font.Font(os.path.join("images","Oxanium-Bold.ttf"),40)

explosion_frames=[pygame.image.load(os.path.join("images","explosion",f"{i}.png")).convert_alpha() for i in range(21)] 


laser_sound=pygame.mixer.Sound(os.path.join("audio","laser.wav"))
laser_sound.set_volume(0.3)
explosion_sound=pygame.mixer.Sound(os.path.join("audio","explosion.wav"))
explosion_sound.set_volume(0.369)
muzic=pygame.mixer.Sound(os.path.join("audio","game_music.wav"))
muzic.set_volume(0.4)
muzic.play(loops=-1)









player_surf=pygame.image.load(os.path.join('images','player.png')).convert_alpha()



laser_img=pygame.image.load(os.path.join('images','laser.png')).convert_alpha()



class Player(pygame.sprite.Sprite):
    def __init__(self,groups):
        super().__init__(groups)
        # self.original_surface=pygame.image.load(os.path.join('images','player.png')).convert_alpha()
        self.image=pygame.image.load(os.path.join('images','player.png')).convert_alpha()
        self.rect=self.image.get_frect(center= (WIDTH/2,HEIGHT/2))
        self.direction=pygame.Vector2(0,0)
        self.speed=300


        #laser shoot
        self.can_shoot=True
        self.laser_shoot_time=0
        self.laser_cooldown=400

        #mask
        self.mask=pygame.mask.from_surface(self.image)

        #transform
        # self.rotation=0
        

    def laser_timer(self):
        if not self.can_shoot:
            current_time=pygame.time.get_ticks()
            if current_time-self.laser_shoot_time >=self.laser_cooldown:
                self.can_shoot=True




        
    def update(self,dt):
        keys=pygame.key.get_pressed()
        self.direction.x=int(keys[pygame.K_RIGHT]) -int(keys[pygame.K_LEFT])
        self.direction.y=int(keys[pygame.K_DOWN]) -int(keys[pygame.K_UP])
        self.direction=self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction*self.speed*dt

        recent_keys=pygame.key.get_just_pressed()
        if recent_keys[pygame.K_SPACE] and self.can_shoot:
            Laser(laser_img,self.rect.midtop,(all_sprites,laser_sprite))
            
            self.can_shoot=False
            self.laser_shoot_time=pygame.time.get_ticks()
            laser_sound.play()

        self.laser_timer()

        #continious rotation
        # self.rotation += 20*dt
        # self.image=pygame.transform.rotozoom(self.original_surface,self.rotation,1)


class Star(pygame.sprite.Sprite):
    def __init__(self,groups):
        super().__init__(groups)
        self.image=pygame.image.load(os.path.join("images","star.png")).convert_alpha()
        
        self.rect=self.image.get_frect(center=(random.randrange(0,WIDTH),random.randrange(0,HEIGHT)))

    
        

            

        
    
            
class Laser(pygame.sprite.Sprite):
    def __init__(self,surf,pos,groups):
        super().__init__(groups)
        self.image=surf
        self.rect=self.image.get_frect(midbottom=pos)

        

    def update(self,dt):
        self.rect.centery-=400*dt
        if self.rect.bottom<0:
             self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self,frames,pos,groups):
        super().__init__(groups)
        self.frames=frames
        self.frame_index=0
        self.image=self.frames[self.frame_index ] 
        
        self.rect=self.image.get_frect(center=pos) 
        


    def update(self,dt) :
        self.frame_index += 20*dt
        if self.frame_index<len(self.frames):
            self.image=self.frames[int(self.frame_index)]  
        else:
            self.kill()
 


class Meteror(pygame.sprite.Sprite):
    def __init__(self,groups):
        super().__init__(groups)
        self.original_img=pygame.image.load(os.path.join("images","meteor.png")).convert_alpha()
        
        self.image=self.original_img
        self.rect=self.image.get_frect(center=(random.randrange(0,WIDTH),random.randrange(-200,-20)))
        self.direction=pygame.Vector2(uniform(-0.5,0.5),1)
        self.speed=random.randint(400,500)

        self.rotation=0



        
        


    def update(self,dt):
        self.rect.center += self.speed*dt*self.direction
        if self.rect.top>HEIGHT:
            self.kill()

        #rotating meteor
        self.rotation += random.randrange(40,80)*dt
        self.image=pygame.transform.rotozoom(self.original_img, self.rotation, 1)  
       


        
def collison():
    global running
    collision_sprite=pygame.sprite.spritecollide(player, meteor_sprite, True,pygame.sprite.collide_mask)
    if collision_sprite:
        running=False
        
    for laser in laser_sprite:
        collided_sprite=pygame.sprite.spritecollide(laser, meteor_sprite, True)
        if collided_sprite:
            laser.kill()
            Explosion(explosion_frames,laser.rect.midtop,all_sprites)
            explosion_sound.play()
            

def display_score():
    curr_time=pygame.time.get_ticks()
    
    text_surf=font.render(str(curr_time),True,(240,240,240))
    text_rect=text_surf.get_frect(midbottom=(WIDTH/2,HEIGHT-50))
    screen.blit(text_surf,  text_rect)
    pygame.draw.rect(screen, (240,240,240), text_rect.inflate(20, 10).move(0,- 8), 5,10)


meteor_sprite=pygame.sprite.Group()
laser_sprite=pygame.sprite.Group()

all_sprites=pygame.sprite.Group()






for i in range(20):
    Star(all_sprites)

player=Player(all_sprites)


#custom event meteor

meteor_event=pygame.event.custom_type()
pygame.time.set_timer(meteor_event,500)



while running:
    dt=clock.tick()/1000
    
    #loop

    for event in pygame.event.get():

        if event.type==pygame.QUIT:
            running=False
        if event.type==meteor_event:
            Meteror((all_sprites,meteor_sprite))
    
    
    collison()
    
    
    screen.fill('#3a2e3f')

    all_sprites.update(dt)
    display_score()



    all_sprites.draw(screen)
    
    pygame.display.update()

pygame.quit()


