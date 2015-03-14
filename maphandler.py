'''
Created on Mar 8, 2015

@author: DemiCow
'''

import pygame, prepare


#CREDIT FOR PORTIONS OF MAP CODE: Christopher Breinholt


class MapTile(pygame.sprite.DirtySprite):

    def __init__(self, image, x, y):
        pygame.sprite.DirtySprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self._set_visible(False)

        

class foregroundMap:

    def __init__(self, level_size):
        #self.tiles = []        
        self.map_width, self.map_height = 0, 0
        
        #self.tiletypes = []
        self.tile_size = (level_size)
        self.pixel_tile_size = (50,50)
        self.tile_size_x = self.tile_size[0]
        self.tile_size_y = self.tile_size[1]
        self.reset()
        
        
        
    def load_images(self):
        self.tileset = prepare.MAPS['demoimage']        
        self.startinglocation= (0, 0)
        
    def generate(self):
        #self.tiles = []
        self.load_images()
        self.map_width = 1#random.randint(30, 50)
        self.map_height = 1#random.randint(30, 50)
        #print "Generated new map that is " + str(self.map_width) + "x" + str(self.map_height) + " tiles in size."
        for y in range(0, self.map_height):
            for x in range(0, self.map_width):
                
                tile_image = pygame.surface.Surface(self.tile_size, pygame.SRCALPHA)  
              
                tile_image.blit(self.tileset, (self.startinglocation))#, (0, 0, self.tile_size_x, self.tile_size_y)
                
                self.tile=(MapTile(tile_image, x*self.tile_size_x, y*self.tile_size_y))
                self.tile.shadedimage = self.shaded_image(self.tile.image, (0,0,0,220))
                #self.tiletypes.append(i)
                
    def find_blocktiles(self):
        size_x = self.pixel_tile_size[0]
        size_y = self.pixel_tile_size[1]
              
        for y in range(0, self.tile_size[1]/size_y):
            for x in range(0,self.tile_size[0]/size_x):  
                color = list(self.pixelmap.get_at((x,y)) [:-1])                
                
                #regular blocks - red
                if color == [255,0,0]:    
                    bumprect = pygame.Rect((x *size_x), (y*size_y),size_x, size_y)                 
                    self.block_list.append(bumprect)                     
                  
                #water blocks - blue
                if color == [0,0,255]:
                    waterblock =pygame.Rect((x *size_x), (y*size_y),size_x, size_y)                 
                    self.waterblock_list.append(waterblock)   
                    
                #hp blocks - yellow
                if color == [255,255,0]:
                    hpblock =pygame.Rect((x *size_x), (y*size_y),size_x, size_y)                 
                    self.hp_block_list.append(hpblock)   
                
                #gate = white. better only have one of these.
                if color == [255,255,255]:
                    self.gatecenter =pygame.Rect((x *size_x), (y*size_y),size_x, size_y)     
                                    
                else: pass
    
    def ghost_image(self, image, color):
        shaded = image.copy()
        shaded.fill(color, special_flags=pygame.BLEND_RGBA_MULT)
        return shaded

    def shaded_image(self,image, color):
        copied = image.copy()
        ghost = self.ghost_image(image, color)
        copied.blit(ghost, (0,0))
        return copied   
    
    def update(self,scene, time_delta):          
        tile = self.tile            
        levelrect = scene.level.get_rect()
        levelrect.center = scene.level.get_rect().center        
        sub_image = pygame.Surface.subsurface(tile.shadedimage,levelrect)       
        scene.level.blit(sub_image, (levelrect.x, levelrect.y), (0, 0, self.tile_size_x, self.tile_size_y))
         
    def reset(self):  
        """creates our map images"""   
        self.generate()
        self.pixelmap = prepare.MAPS['demo']
        self.block_list = []  
        self.waterblock_list = []     
        self.hp_block_list = []
        self.gatecenter = None        
        self.find_blocktiles()
        
                
#can probably get rid of these classes when we pass in file to load as argument, or change/expand them.
class backgroundMap(foregroundMap):
    
    
    def load_images(self):
        self.tileset = prepare.IMAGES['testbackground']
        self.startinglocation= (0,0)
    
    def find_blocktiles(self):
        pass
    def shift_blocktiles(self):        
        pass
    def check_bounds(self):
        pass
    def update(self,scene, time_delta):          
        tile = self.tile                
        scene.level.blit(tile.image, (tile.rect.x, tile.rect.y ), (0, 0, self.tile_size_x, self.tile_size_y))
    
class stillBackground(foregroundMap): 
    def __init__(self, resolution, surface, image):
        self.image = image
        self.tiles = []        
        self.map_width, self.map_height = 0, 0
        self.screen = surface        
        self.tile_size = (self.level_size)
        self.tile_size_x = self.tile_size[0]
        self.tile_size_y = self.tile_size[1]
        self.dark = False
        self.generate()  
        self.leftedge = self.tile.rect.left
        self.rightedge = self.tile.rect.right
        self.speed = 1
     
    def load_images(self):
        self.speed = 6       
        self.tileset = prepare.IMAGES[self.image]
   
    def update(self,scene):  
        
        #self.leftedge =  self.tile.rect.left - scene.camera.x
        #self.rightedge = self.tile.rect.right - scene.camera.x
        
        if self.dark == False:
            self.screen.blit(self.tile.image, (0,0), special_flags= 0)
        if self.dark == True:
            self.screen.blit(self.tile.image, (0,0), special_flags= 3)
            

