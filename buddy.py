'''
Created on Mar 9, 2015

@author: DemiCow
'''

import pygame
import prepare
import maincharacter


typedict = {'snek': {'image': prepare.IMAGES['snek'], 'imagesize' :(100,100)}}


class Buddy(maincharacter.mainCharacter):

    def __init__(self, scene, location, buddytype):            
        #init the sprite!    
        pygame.sprite.DirtySprite.__init__(self)   
        
        #load image
        self.location = location
        self.image = typedict[buddytype]['image']
        self.imagesize = typedict[buddytype]['imagesize']
        self.speed = scene.speed
        self.max_speed = scene.speed 
        if scene.mc.facing == 'right':
            self.velocity = [4, 0]
        else: self.velocity = [-4, 0]
        
        self.grav = 0.4
        self.gravity = 1
        self.terminal_velocity = 5
        self.jump_velocity = -100        
        self.grav = 0.4
        self.gravity = 1
        self.terminal_velocity = 5
        self.jump_velocity = -100
        self.light_spread = 3
        self.light_brightness = 5
        self.hp_factor = 1
        self.reset()
    
    def load_images(self):
        # load the image if the sprite is still
        self.imagestill = pygame.Surface(self.imagesize, pygame.SRCALPHA)        
        self.imagestill.blit(self.imagemaster, (0, 0), ((0,0), self.imagesize))
        
        #make a list of frames for the sprite viewed from the front
        self.imagewalking= []        
        offsetwalking = []
        
        #row 0, 1, 2,3 = idle
        for x in range(1):
            for i in range(self.number_of_frames):
                offsetwalking.append((self.imagesize[0]*i,x*self.imagesize[1]))    
        
               
        for i in range(0,self.number_of_frames):
            
            tmpimg = pygame.Surface(self.imagesize, pygame.SRCALPHA)            
            tmpimg.blit(self.imagemaster, (0, 0), (offsetwalking[i], self.imagesize))          
            self.imagewalking.append(tmpimg)    
        self.imagejumping = self.imagewalking 
        
    def animation(self):    
        if self.frame>=len(self.currentimage):
            self.frame = 0  
        delay = 10       
        
        self.pause += 1
        if self.pause >= delay:
            self.pause = 0
            self.frame += 1
            if self.frame >= len(self.currentimage):
                self.frame = 0               
                
        self.image = self.currentimage[self.frame]      
    
        
    def reset(self):
        self.imagemaster = self.image
        
        self.number_of_frames = 3
        self.load_images()
        self.image = self.imagestill
        self.imageidle = self.imagewalking
        self.currentimage = self.imagewalking
        self.facing = 'right'        
        self.rect = self.image.get_rect() 
        self.rect.inflate_ip(20,0)
       
        self.phase = "idle"
                     
        self.pause = 0
        self.delay = 5
        self.frame = 0
        self.pos = (0,0)
        
        #initial position
        self.rect.x, self.rect.y = self.location    
        
        self.frame_start_pos = 0
       
        
        self.on_moving = False    
        
        
        
        
    def do_wall(self, scene, side):        
        if side == False:
            pass        
        elif side == 'left':
            self.rect.x += 10
            self.velocity[0] = -self.velocity[0]
        elif side == 'right':
            self.rect.x -= 10
            self.velocity[0] = -self.velocity[0]
        elif side == 'both':
            self.velocity[0] = 0
        
       
        
    def move(self, scene):   
        self.rect.x += self.velocity[0] 
        self.rect.y += self.velocity[1]     
        
 
    def check_visible(self,scene):
        return self.rect.colliderect(scene.viewport.inflate(800,600))
    
    def update(self,scene, time_delta):       
        if self.check_visible(scene):   
            collidelist = self.check_collisions(scene.collisionblocks)
            self.falling = self.check_falling(collidelist)        
            self.do_fall()
            wall = self.check_wall(collidelist) 
            if self.rect.bottom >= scene.level_size[1] - scene.mainmap.pixel_tile_size[1]: 
                self.rect.bottom = scene.level_size[1] - scene.mainmap.pixel_tile_size[1]
                self.falling = False
            self.do_wall(scene,wall)     
            self.animation()
            if self.velocity[0] <= 0:            
                self.flip()
            else: pass
            
            self.change_state()
                           
            self.move(scene)    
            scene.level.blit(self.image, (self.rect.x, self.rect.y), special_flags= 0) 
            
#class Snake (Buddy):            
   