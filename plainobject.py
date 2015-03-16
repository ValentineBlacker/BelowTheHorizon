'''
Created on Mar 10, 2015

@author: DemiCow
'''

import prepare
import pygame

class plainObject(pygame.sprite.DirtySprite):

    def __init__(self, scene, location, image = prepare.IMAGES['sun']):            
        #init the sprite!    
        pygame.sprite.DirtySprite.__init__(self)   
        
        #load image
        
        self.location = location
        self.image = image
        self.imagesize = (30,30)       
        self.reset()
        self.light_spread = 1
        self.light_brightness = 1
        
    def reset(self):
        self.imagemaster = self.image
        
        self.number_of_frames = 2
        self.load_images()               
        
        self.rect = self.image.get_rect()   
        #initial position
        self.rect.x, self.rect.y = self.location    
       
    def load_images(self):        
        self.imagestill = pygame.Surface(self.imagesize, pygame.SRCALPHA)        
        self.imagestill.blit(self.imagemaster, (0, 0), ((0,0), self.imagesize))
        
    def update(self,scene, time_delta):        
        scene.level.blit(self.image, (self.rect.x, self.rect.y)) 
        