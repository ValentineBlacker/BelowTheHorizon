'''
Created on Mar 8, 2015

@author: DemiCow
'''

import pygame, prepare


#CREDIT FOR PORTIONS OF MAP CODE: Christopher Breinholt

COLOR_KEY = (255, 0, 255)
ELLIPSE_SIZE = (400, 400)

class MapTile(pygame.sprite.DirtySprite):

    def __init__(self, image, x, y):
        pygame.sprite.DirtySprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self._set_visible(False)

        

class foregroundMap:

    def __init__(self, scene, shaded = True):
        #self.tiles = []        
        self.map_width, self.map_height = 0, 0
        
        #self.tiletypes = []
        self.tile_size = scene.level_size
        self.pixel_tile_size = (50,50)
        self.tile_size_x = self.tile_size[0]
        self.tile_size_y = self.tile_size[1]
        self.ellipse_rect = pygame.Rect((0,0), ELLIPSE_SIZE)
        self.reset(scene)
        self.shaded = shaded
        
        self.hole = None
        self.hole = pygame.Surface(prepare.RESOLUTION).convert_alpha()
        self.cdx = self.cdy = 0
        
    def load_images(self,scene):
        if scene.hour > 1:
            use_hour = 1
        else: use_hour = scene.hour
        self.tileset = prepare.MAPS["hour{0}image".format(use_hour)]             
        self.startinglocation= (0, 0)
        
        
        
    def generate(self,scene):
        #self.tiles = []
        self.load_images(scene)
        self.map_width = 1#random.randint(30, 50)
        self.map_height = 1#random.randint(30, 50)
        #print "Generated new map that is " + str(self.map_width) + "x" + str(self.map_height) + " tiles in size."
        for y in range(0, self.map_height):
            for x in range(0, self.map_width):
                
                tile_image = pygame.surface.Surface(self.tile_size, pygame.SRCALPHA)  
              
                tile_image.blit(self.tileset, (self.startinglocation))#, (0, 0, self.tile_size_x, self.tile_size_y)
                
                self.tile=(MapTile(tile_image, x*self.tile_size_x, y*self.tile_size_y))
                #self.tile.shadedimage = self.shaded_image(self.tile.image, (0,0,0,220))
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
                    
                #torch locations - green
                if color == [0,255,0]:
                    torch =pygame.Rect((x *size_x), (y*size_y),size_x, size_y*2)                 
                    self.torch_block_list.append(torch)   
                
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
        image.blit(copied, (0,0))
        return image
    
    def make_hole_alpha(self, scene):
        
        self.hole.fill((2,2,2,255- (scene.background_illumination))) 
        
        l = scene.light_sources[0]
        ellipse_rect = pygame.Rect((0,0), (250,200))
        #offset_x = abs(scene.viewport.left - l[2])
        #offset_y = abs(scene.viewport.top - l[3])
        offset_x = (l[2]-scene.viewport.left ) 
        offset_y = (l[3]-scene.viewport.top)     
        
        ellipse_rect.center = [offset_x, offset_y]   
        pygame.draw.ellipse(self.hole, (0,0,0,0), ellipse_rect)
        
        for l in scene.light_sources[1:]:        
            ellipse_rect = pygame.Rect((0,0), (100*l[0],100*l[0]))
            offset_x = (l[2]-scene.viewport.left ) 
            offset_y = (l[3]-scene.viewport.top)     
        
            ellipse_rect.center = [offset_x, offset_y]   
            
            pygame.draw.ellipse(self.hole, (0,0,0,50-l[1]), ellipse_rect)
       
    
    def draw_blocks(self, scene, switch):   
        #light source tuple is (spread, brightness, rect.x, rect.y)       
        if switch == True:       
            for x in scene.mainmap.block_list:
                if x.colliderect(scene.viewport):
                    total_abspos = 0
                    for l in scene.light_sources[1:]:
                        abspos =  int(abs(x.x-l[2]) + abs(l[3]-x.y))    
                        abspos = (abspos/l[0]) - l[1]  /2
                        total_abspos += abspos       
                    if total_abspos == 0:
                        total_abspos = 1
                    if len(scene.light_sources[1:])  > 0:
                        total_abspos = total_abspos/len(scene.light_sources[1:])  
                    else: total_abspos = 255
                    if total_abspos > 255: total_abspos= 255
                    if total_abspos < 0: total_abspos = 0
                    pygame.draw.rect(scene.level, (255-total_abspos,255-total_abspos,255-total_abspos), x)
                
            for x in scene.mainmap.waterblock_list:
                if x.colliderect(scene.viewport):
                    total_abspos = 0
                    for l in scene.light_sources[1:]:
                        abspos =  int(abs(x.x-l[2]) + abs(l[3]-x.y))    
                        abspos = (abspos/l[0]) - l[1]  /2
                        total_abspos += abspos       
                    if total_abspos == 0:
                        total_abspos = 1
                    if len(scene.light_sources[1:]) > 0:
                        total_abspos = total_abspos/len(scene.light_sources[1:])  
                    else: total_abspos = 255
                    if total_abspos > 255: total_abspos= 255
                    if total_abspos < 0: total_abspos = 0
                    pygame.draw.rect(scene.level, (0,0,255-total_abspos), x)
                
            #for x in scene.mainmap.hp_block_list:
                #pygame.draw.rect(scene.level, (255,255,255), x)
            if self.gatecenter is not None:
                pygame.draw.rect(scene.level, (255,255,0), self.gatecenter)
            

        else: pass
    
    def update(self,scene, time_delta):   
        
        tile = self.tile            
        levelrect = scene.level.get_rect()
        levelrect.center = scene.level.get_rect().center    
        
        if self.shaded == True:   
            self.make_hole_alpha(scene)
            
        sub_image = pygame.Surface.subsurface(tile.image,levelrect)  
        sub_image_topleft = (scene.viewport.topleft)
        
        scene.level.blit(sub_image, (levelrect.x, levelrect.y), (0, 0, self.tile_size_x, self.tile_size_y))
        if self.shaded == True:
            scene.level.blit(self.hole, (sub_image_topleft), (0, 0, self.tile_size_x, self.tile_size_y))
        self.draw_blocks(scene, True)
         
    def reset(self,scene):  
        """creates our map images"""   
        self.generate(scene)
        self.pixelmap = prepare.MAPS["hour{0}".format(scene.hour)]  
        self.block_list = []  
        self.waterblock_list = []     
        self.hp_block_list = []
        self.torch_block_list = []
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
            

