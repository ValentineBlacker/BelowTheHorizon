'''
Created on Mar 8, 2015

@author: DemiCow
'''

import pygame
import prepare
import maincharacter

    


class Baddie(maincharacter.mainCharacter):

    def __init__(self, scene, location, image = prepare.IMAGES['mc'], imagesize = (100,100)):            
        #init the sprite!    
        pygame.sprite.DirtySprite.__init__(self)   
        
        #load image
        self.location = location
        self.image = image
        self.imagesize = imagesize
        self.speed = scene.speed
        self.max_speed = scene.speed 
        self.velocity = [4, 0]
        self.grav = 0.4
        self.gravity = 1
        self.terminal_velocity = 5
        self.jump_velocity = -100
        self.velocity = [4, 0]
        self.grav = 0.4
        self.gravity = 1
        self.terminal_velocity = 5
        self.jump_velocity = -100
        self.reset()
        
    def reset(self):
        self.imagemaster = self.image
        
        self.number_of_frames = 6
        self.load_images()
        self.image = self.imagestill
        self.currentimage = self.imageidle
        self.facing = 'right'        
        self.rect = self.image.get_rect() 
       
        self.phase = "idle"
                     
        self.pause = 0
        self.delay = 11
        self.frame = 0
        self.pos = (0,0)
        
        #initial position
        self.rect.x, self.rect.y = self.location  
        self.frame_start_pos = 0
       
        
        self.on_moving = False    
        
        
    def ghost_image(self, image, color):
        shaded = image.copy()
        shaded.fill(color, special_flags=pygame.BLEND_RGBA_MULT)
        return shaded    
        
    def do_wall(self, scene, side):  
               
        if side == False:
            pass
        elif side == 'left':
            self.rect.x += 10
            self.velocity[0] = -self.velocity[0]
        elif side == 'right':
            self.rect.x -= 10
            self.velocity[0] = -self.velocity[0]
        else:             
            self.velocity[0] = -self.velocity[0]

  
       
        
    def move(self, scene):   
        self.rect.x += self.velocity[0] 
        self.rect.y += self.velocity[1]     
        
    def calc_abs_pos(self, scene,targetrect):
        """calculates distance from scene playable character/s"""
        #light source tuple is (spread, brightness, rect.x, rect.y)  
        total_abspos = 0
        for l in scene.light_sources:
            abspos =  int(abs(self.rect.x-l[2]) + abs(l[3]-self.rect.y))    
            abspos = (abspos/l[0]) - l[1]/2  
            if abspos > 255: abspos= 255
            if abspos < 0: abspos = 0 
            total_abspos += abspos  
        
        if total_abspos > 255: total_abspos= 255
        if total_abspos < 0: total_abspos = 0        
        return total_abspos
    
    
    
    def check_visible(self,scene):
        return self.rect.colliderect(scene.viewport.inflate(800,600))
    
    def update(self,scene, time_delta):               
        if self.check_visible(scene):  
            collidelist = self.check_collisions(scene.collisionblocks)
            self.falling = self.check_falling(collidelist)        
            self.do_fall()
            wall = self.check_wall(collidelist) 
              
            self.do_wall(scene,wall)     
            self.animation()
            if self.facing == 'left':            
                self.flip()
            
            self.change_state()
                           
            self.move(scene)      
            abspos = 255- self.calc_abs_pos(scene,scene.player.rect)
            self.image = self.shaded_image(self.image,(abspos, abspos, abspos))     
                     
            scene.level.blit(self.image, (self.rect.x, self.rect.y), special_flags= 0) 
   