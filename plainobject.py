'''
Created on Mar 10, 2015

@author: DemiCow
'''

import prepare
import pygame

class plainObject(pygame.sprite.DirtySprite):

    def __init__(self, scene, location, imagetype = 'sun'):            
        #init the sprite!    
        pygame.sprite.DirtySprite.__init__(self)   
        
        #load image
        
        self.location = location
        self.image =  prepare.IMAGES[imagetype]
        self.imagetype = imagetype
        if self.imagetype == 'sun':
            self.imagesize = (30,30)     
        elif self.imagetype == 'torch':
            self.imagesize = (50,100)  
        self.reset()
        self.light_spread = 1
        self.light_brightness = 1
        
        
    def reset(self):
        self.imagemaster = self.image
        
        self.number_of_frames = 2
        self.load_images()        
        if self.imagetype == 'torch':                   
            self.shaded = True
            self.image = self.imagestill
            self.frame = 0
            self.pause = 3
            self.light_brightness = 3
        else: self.shaded = False
        self.rect = self.image.get_rect()   
        #initial position
        self.rect.x, self.rect.y = self.location    
       
    def load_images(self):        
        self.imagestill = pygame.Surface(self.imagesize, pygame.SRCALPHA)        
        self.imagestill.blit(self.imagemaster, (0, 0), ((0,0), self.imagesize))
        
        if self.imagetype == 'torch':
            self.lit = False
                #populates list of frames, using imagesize that matches frame size
            self.imageflame= []
            offsetflame = tuple((self.imagesize[0]*(i+1),0) 
                                 for i in range(2))
            
            for i in range(0,2):
                tmpimage = pygame.Surface(self.imagesize, pygame.SRCALPHA)
                tmpimage.blit(self.imagemaster, (0, 0), (offsetflame[i], self.imagesize))            
                self.imageflame.append(tmpimage)
        
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
        
    def calc_abs_pos(self, scene):
        total_abspos = 0
        for l in scene.light_sources[1:]:
            abspos =  int(abs(self.rect.x-l[2]) + abs(l[3]-self.rect.y))    
            abspos = (abspos/l[0]) - l[1]  /2
            total_abspos += abspos       
        if total_abspos == 0:
            total_abspos = 1
        if len(scene.light_sources[1:])  > 0:
            total_abspos = total_abspos/len(scene.light_sources[1:])  
        else: total_abspos = 255
        if total_abspos > 255: total_abspos= 255
        if total_abspos < 0: total_abspos = 0
        
        return total_abspos
    
    def ghost_image(self, image, color):
        shaded = image.copy()
        shaded.fill(color, special_flags=pygame.BLEND_RGBA_MULT)
        return shaded  
    
    def shaded_image(self,image, color):   
        copied = image.copy()     
        ghost = self.ghost_image(image, color)    
        copied.blit(ghost, (0,0))
        image.blit(copied, (0,0))
        return image
        
    def update(self,scene, time_delta):        
        if self.imagetype == 'torch' and self.lit == True:
            self.currentimage = self.imageflame
            self.animation()
        
        if self.imagetype == 'torch' and self.lit == False or self.shaded == True:
            abspos = 255- self.calc_abs_pos(scene)
            self.image = self.shaded_image(self.image,(abspos, abspos, abspos))  
        scene.level.blit(self.image, (self.rect.x, self.rect.y)) 
        