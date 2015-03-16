'''
Created on Mar 8, 2015

@author: DemiCow
'''

import pygame
import prepare

class mainCharacter(pygame.sprite.DirtySprite):

    def __init__(self, scene, location, image = prepare.IMAGES['rishi'], imagesize = (100,175)):            
        #init the sprite!    175,306
        pygame.sprite.DirtySprite.__init__(self)   
        
        #load image
        self.imagemaster = image
        #self.imagemaster = self.ghost_image(image,(255,0,255,150))
        self.location = location
        self.imagesize = imagesize
        self.number_of_frames = 6
        self.load_images()
        
        self.image = self.imagestill
        self.currentimage = self.imageidle
              
        self.rect = self.image.get_rect() 
                          
        
        #use same movement speed as map           
        self.speed = scene.speed
                
        #variables for animation
        self.pause = 2
        self.delay = 10
        self.frame = 0
        self.pos = (0,0)
        
        self.grav = 0.4
        self.gravity = 1
        self.terminal_velocity = 5
        self.jump_velocity = -100
               
        self.jump_power = -10.0
        self.jump_cut_magnitude = -3.0
        self.max_speed = 6#scene.speed
        self.reset()
        #self.rect.inflate_ip(5,-5)           
        self.light_spread = 1
        self.light_brightness = 1
        
    def load_images(self):
        # load the image if the sprite is still
        self.imagestill = pygame.Surface(self.imagesize, pygame.SRCALPHA)        
        self.imagestill.blit(self.imagemaster, (0, 0), ((0,0), self.imagesize))
        
        #make a list of frames for the sprite viewed from the front
        self.imageidle= []        
        offsetidle = []
        
        #row 0, 1, 2,3 = idle
        for x in range(2):
            for i in range(self.number_of_frames):
                offsetidle.append((self.imagesize[0]*i,x*self.imagesize[1]))    
        new_list = list(reversed(offsetidle))
        # plays backwards after it plays forward. 48 frames.
        offsetidle = offsetidle + new_list
       
        for i in range(0,self.number_of_frames*2):
            
            tmpimg = pygame.Surface(self.imagesize, pygame.SRCALPHA)            
            tmpimg.blit(self.imagemaster, (0, 0), (offsetidle[i], self.imagesize))          
            self.imageidle.append(tmpimg)     
            
        #row 2 = walking
            
        self.imagewalking= []        
        offsetwalking = []
        for i in range(self.number_of_frames):
            offsetwalking.append((self.imagesize[0]*i,2*self.imagesize[1]))
       
        for i in range(0,self.number_of_frames):
            tmpimg = pygame.Surface(self.imagesize, pygame.SRCALPHA)            
            tmpimg.blit(self.imagemaster, (0, 0), (offsetwalking[i], self.imagesize))            
            self.imagewalking.append(tmpimg)   
            
        self.imagejumping= []        
        offsetjumping = []
        for i in range(self.number_of_frames):
            offsetjumping.append((self.imagesize[0]*i,3*self.imagesize[1]))
       
        for i in range(0,self.number_of_frames):
            tmpimg = pygame.Surface(self.imagesize, pygame.SRCALPHA)            
            tmpimg.blit(self.imagemaster, (0, 0), (offsetjumping[i], self.imagesize))            
            self.imagejumping.append(tmpimg)  
    
         
    
    def check_keys(self, scene, wall):
        """Find the player's self.velocity[0] based on currently held keys."""
        keys = scene.keys   
        if self.controllable == True:    
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                if self.velocity[0] > -self.max_speed :
                    if wall is not 'left':
                        self.velocity[0] -= 1
                    else: self.velocity[0] = 0
                self.facing = 'left'
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                if self.velocity[0] < self.max_speed :
                    if wall is not 'right':
                        self.velocity[0] += 1
                    else: self.velocity[0] = 0
                self.facing = 'right'
            if keys[pygame.K_SPACE]:
                self.jump(wall)
            if not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT] :                       
                if self.velocity[0] is not 0:
                    if self.velocity[0] > 0:
                        self.velocity[0] -=1
                    elif self.velocity[0] < 0:
                        self.velocity[0] +=1
         
    def do_fall(self):
        """If the player is falling, add gravity to the current y velocity."""
        if self.falling == True:
            if self. velocity[1] < self.terminal_velocity:
                self.velocity[1] += self.grav
            else: pass
        else:
            self.velocity[1] = 0
          
    def change_state(self):
        if self.falling == False:
            if  self.velocity[0] is not 0:   
                self.walking()  
            else:             
                self.idle()
        else: self.jumping()
         
    
    def check_falling(self, collidelist):
        """If player is not contacting the ground, enter fall state."""
        #collidelist = self.check_collisions(obstacles)  
        if (collidelist[5] == 1 and collidelist[6]== 1) or (collidelist[6]== 1 and collidelist[7] == 1):
            return False
        else: return True
        
    def check_wall(self, collidelist):   
        if collidelist[10] == 1 or collidelist[8] == 1 or collidelist[3] == 1:
            return 'left'
        elif collidelist[9] == 1 or collidelist[8] == 1 or collidelist[4] == 1:         
            return 'right'
        else: return False
        
    def do_wall(self, side):        
        if side == False:
            pass
        elif side == 'left':
            if self.velocity[0] < 0:
                self.velocity[0] = 0
        elif side == 'right':
            if self.velocity[0] > 0:
                self.velocity[0] = 0
        
    def jump(self, wall):
        """Called when the user presses the jump button."""                
        if self.falling == False: 
            self.velocity[1] = self.jump_power            
            self.on_moving = False    
            
    def idle(self):
        self.phase = 'idle'
        self.currentimage = self.imageidle
        #self.x, self.y = 0
        
    def walking(self):
        self.phase = 'walking'         
        self.currentimage = self.imagewalking   
        
    def jumping(self):
        self.phase = 'jumping'
        self.currentimage = self.imagejumping             

    
    def animation(self):
        
        if self.phase == 'jumping':            
            if self.velocity[1] < 0:
                               
                if self.frame < 2:
                    self.frame += 1
                else: self.frame = 2
            elif self.velocity[1] >= 0:
                
                if self.frame < 3:
                    self.frame = 3
                elif self.frame > 3 and self.frame < len(self.currentimage)-2:
                    self.frame += 1
                else: self.frame = len(self.currentimage)-2
                
        else :
            #flip through the frames of animation
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
    
        
    def move_and_calculate_displacement(self, scene, wall):  
        #displacement is used to calculate viewport movement    
        original_pos= self.rect.topleft 
        
        self.check_keys(scene, wall)        
        
        self.rect.x += self.velocity[0] 
        self.rect.y += self.velocity[1]        
        end_pos = self.rect.topleft
        self.total_displacement = (end_pos[0]-original_pos[0], end_pos[1]-original_pos[1])
     
     
    def ghost_image(self, image, color):
        shaded = image.copy()
        shaded.fill(color, special_flags=pygame.BLEND_MULT)
        return shaded

    def shaded_image(self,image, color):
        copied = image.copy()
        ghost = self.ghost_image(image, color)
        copied.blit(ghost, (0,0))
        return copied 
    
     
    def flip(self):
        """ flips sprite horizontally"""        
        self.image = pygame.transform.flip(self.image, True, False) 

    def update(self,scene, time_delta):  
        
        collidelist = self.check_collisions(scene.collisionblocks)
        wall = self.check_wall(collidelist) 
        self.move_and_calculate_displacement(scene, wall)
            
        self.falling = self.check_falling(collidelist)        
        self.do_fall()
       
          
        self.do_wall(wall)     
        self.animation()
        if self.facing == 'left':            
            self.flip()
        
        self.change_state()
                       
        
        #self.check_bounds(scene) 
               
        scene.level.blit(self.image, (self.rect.x, self.rect.y), special_flags= 0) 
   
    def check_collisions(self, collisionblocks):
        #This checks 8 points on the outside of the rectangle for collisions, and checks if any of them are colliding or not.
        #we don't really care with which block they're colliding.
            rect = self.rect    
            wallright = (rect.right, rect.bottom - rect.height/4)    
            wallleft = (rect.left, rect.bottom - rect.height/4)      
            rectlist = [rect.topleft, rect.midtop, rect.topright,rect.midleft, rect.midright, rect.bottomleft, rect.midbottom, rect.bottomright, rect.center, wallright, wallleft]            
            collidedblock_indices = self.rect.collidelistall(collisionblocks)            
            blocklist = []   
            collidelist = [0,0,0,0,0,0,0,0,0,0,0]       
            if collidedblock_indices:         
                for c in collidedblock_indices:
                    blocklist.append(collisionblocks[c])                      
                #for b in blocklist:                                         
                    #collidelist = [b.collidepoint(c) for c in rectlist] 
                                   
                for c in rectlist:                                       
                    for b in blocklist:       
                        if collidelist[rectlist.index(c)] is not 1:                   
                            collidelist[rectlist.index(c)]= b.collidepoint(c)                                    
          
            return collidelist  
    
            
    def check_bounds(self,scene):    
        
        #keeps ya from walkin' off the edge        
        mapleft = -self.imagesize[0]/2
        mapright = scene.level_size[0]
        maptop = 0#-self.imagesize[1]/2
        mapbottom = scene.level_size[1]
            
        if self.rect.left < mapleft:            
            self.rect.left = mapleft  
                
        if self.rect.top < maptop:
            self.topside = True
            
          
        if self.rect.right >= mapright:             
            self.rect.right = mapright
            
            
        if self.rect.bottom > mapbottom:
            self.bottomside = True
                    
    
    def reset (self):           
        self.facing = 'right'  
        self.phase = "idle"
        
        self.velocity = [0, 0]
        
        
        self.controllable = False
        #initial position
        self.rect.x, self.rect.y = self.location    
        
        self.frame_start_pos = 0
        self.total_displacement = (0,0)
        
        #init variables to be used later
        self.on_moving = False    
    