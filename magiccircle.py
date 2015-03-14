'''
Created on Mar 10, 2015

@author: DemiCow
'''

import prepare
import pygame

class magicCircle(pygame.sprite.DirtySprite):

    def __init__(self, scene, target, image = prepare.IMAGES['sun']):            
        #init the sprite!    
        pygame.sprite.DirtySprite.__init__(self)   
        
        #load image
        self.target = target
        self.location = (self.target.rect.centerx, self.target.rect.centery)
        self.image = image
        self.imagesize = (30,30)       
        self.reset()
        
    def reset(self):
        self.imagemaster = self.image
        
        self.number_of_frames = 6
        self.load_images()                
        self.image = pygame.transform.scale(self.image,(self.target.imagesize[0] + 200, self.target.imagesize[1] + 200))
        self.image.fill((50,50,50,1), special_flags= 0)  
        self.rect = self.image.get_rect()   
        #initial position
        self.rect.x, self.rect.y = self.location    
        self.image = self.imagefloating
        
    def load_images(self):        
        self.imagestill = pygame.Surface(self.imagesize, pygame.SRCALPHA)        
        self.imagestill.blit(self.imagemaster, (0, 0), ((0,0), self.imagesize))
        
    def update(self,scene, time_delta):
        self.rect.center = scene.mc.rect.center   
        scene.level.blit(self.image, (self.rect.x, self.rect.y), special_flags = pygame.BLEND_RGBA_ADD) 
        