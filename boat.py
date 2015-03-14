'''
Created on Mar 13, 2015

@author: DemiCow
'''

import prepare
import pygame

class Boat(pygame.sprite.DirtySprite):

    def __init__(self, scene, location, image = prepare.IMAGES['boat']):            
        #init the sprite!    
        pygame.sprite.DirtySprite.__init__(self)   
        
        #load image        
        self.location = location
        self.image = image
        self.imagesize = (300,150)       
        self.reset()
        self.frame = 0
        self.pause = 0
        self.floating = True
        self.light_spread = 1
        self.light_brightness = 1
        
    def reset(self):
        self.imagemaster = self.image
        
        self.number_of_frames = 2
        self.load_images()   
        self.rect = self.imagestand.get_rect()   
        self.rect.inflate_ip (0, -125)
        #initial position
        self.rect.x, self.rect.y = self.location   
        self.image = self.imagestand
        self.currentimage = self.imagemoving        
        self.velocity = [0,0]
        
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
        
    def load_images(self):        
        #intial placeholder image
        self.imagestand = pygame.Surface(self.imagesize, pygame.SRCALPHA)        
        self.imagestand.blit(self.imagemaster, (0, 0), ((0,0), self.imagesize))       
        
        #populates list of frames, using imagesize that matches frame size
        self.imagemoving= []
        offsetmoving = tuple((self.imagesize[0]*i,0) 
                             for i in range(self.number_of_frames))
        
        for i in range(0,self.number_of_frames):
            tmpimage = pygame.Surface(self.imagesize, pygame.SRCALPHA)
            tmpimage.blit(self.imagemaster, (0, 0), (offsetmoving[i], self.imagesize))            
            self.imagemoving.append(tmpimage)
            
    def float_along(self,scene):
        if self.floating == True:
            if self.rect.colliderect(scene.mc.rect):
                if self.rect.x < scene.boatdock:
                    self.velocity[0] = 4
                else: 
                    self.floating = False
                    self.velocity[0] = 0
        
    def update(self,scene, time_delta):        
        self.animation()        
        if self.floating == True:
            self.float_along(scene)
            self.rect.x += self.velocity[0]
        scene.level.blit(self.image, (self.rect.x, self.rect.top - 100)) 
        