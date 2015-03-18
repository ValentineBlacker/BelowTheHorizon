'''
Created on Mar 13, 2015

@author: DemiCow
'''

import pygame
import scene
import label
import maphandler
import maincharacter
import boat

class Cutscene0(scene.Scene):
    
    def __init__(self):        
        scene.Scene.__init__(self)
        self.next = "GAMEPLAY"
        self.init_variables()
        self.init_objects()  
    
    def init_variables(self):
        self.speed = self.MASTER_SPEED * 3  
        self.collisionblocks = []
        self.max_hp = 10
        self.hp = self.max_hp
        self.hp_block_amount = 3
        self.boatdock = 800
        self.hour = 0
        
    
    def init_objects(self):
        """ creates objects needed in specfic scenes"""        
        """self.label = label.Label(self, font_size = 50)
        self.label.textlines = ["INTRO. AARGH."]
        self.menu = label.Label(self, font_size = 50)        
        self.menu.textlines = ["click to start game"]
        self.menu.clickable = True
        self.menu.rect.y += 300  """      
        self.level_size = (800,6000)
        self.level = pygame.Surface((self.level_size)).convert()
        self.level_rect = self.level.get_rect()
        self.viewport = self.screen.get_rect( )
       
        self.mainmap = maphandler.foregroundMap(self, False)         
        
        self.spawn_location = (300,0)  
        self.mc = maincharacter.mainCharacter(self, self.spawn_location)               
        self.player = self.mc
        self.update_light_sources()
        self.boat = boat.Boat(self, (270, self.level_size[1]-(self.mainmap.pixel_tile_size[1]*2)))
        self.sprites = [self.mainmap, self.mc, self.boat]
        
    def get_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:            
            self.clicked = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.clicked = False         
        if event.type == pygame.KEYUP:    
            if event.key == pygame.K_x:
                pass
    
    def update_viewport(self, speed):
        """
        Viewport enabling variable scroll speed based on player's location
        on the screen.  Here scrolling begins when the player crosses 1/3rd of
        the screen.  Scrolling begins at half the speed of the player, but once
        the player reaches the halfway point scrolling matches the player's own
        speed.
        """        
        player = self.player
        for i in (0,1):
            first_third = self.viewport[i]+self.viewport.size[i]//3
            second_third = first_third+self.viewport.size[i]//3
            player_center = player.rect.center[i]
            mult = 0
            if speed[i] > 0 and player_center >= first_third:
                mult = 0.5 if player_center < self.viewport.center[i] else 1                
            elif speed[i] < 0 and player_center <= second_third:
                mult = 0.5 if player_center > self.viewport.center[i] else 1                
            self.viewport[i] += mult*speed[i]
        self.viewport.clamp_ip(self.level_rect)
        
        
    def update_light_sources(self):       
        self.light_sources =  [ (self.mc.light_spread, self.mc.light_brightness, self.mc.rect.centerx, self.mc.rect.centery)]     
        
    def mouse_controls(self, time_delta):
        pass
           
    
    def startup(self, time, persistant):
        self.start_time = time        
        return scene.Scene.startup(self, time, persistant)
    
    def cleanup(self):        
        return scene.Scene.cleanup(self)
           
                    
    def update_specifics(self, time, time_delta): 
        """things that need to be updated in individual scenes"""        
          
        self.update_viewport((self.player.total_displacement))          
        self.screen.blit(self.level, (0,0), self.viewport)
        self.collisionblocks = [b for b in self.mainmap.block_list]
        self.collisionblocks.append(self.boat.rect)
        
            
        if self.mc.rect.colliderect(self.boat.rect):                      
            self.update_viewport(self.boat.velocity)
            self.mc.rect.x += self.boat.velocity[0]
           
        if self.mc.rect.right >= self.level_size[0]:
            self.done = True
                    
                
class Cutscene1(scene.Scene):
    def __init__(self):        
        scene.Scene.__init__(self)
        self.next = "TITLE"
        self.init_variables()
        self.init_objects()  

    
    def init_objects(self):
        """ creates objects needed in specfic scenes"""
        self.collision_time = -100
        self.shield_time = -100
        self.speed = self.MASTER_SPEED       
        self.label = label.Label(self, font_size = 50)
        self.label.textlines = ["THANK YOU FOR PLAYING", "BELOW THE HORIZON"]
        self.menu = label.Label(self, font_size = 50)        
        self.menu.textlines = ["click to go back to title"]
        self.menu.clickable = True
        self.menu.rect.y += 300
        self.background = pygame.Surface(self.screen.get_size())
        self.backgroundrect = self.background.get_rect()
        self.background.fill(pygame.color.Color("black"))
        self.screen.blit(self.background, (0, 0))
        self.sprites = [self.label, self.menu]
        
        
        
    def mouse_controls(self, time_delta):
        pass
           
    
    def startup(self, time, persistant):
        self.start_time = time        
        return scene.Scene.startup(self, time, persistant)
    
    def cleanup(self):        
        return scene.Scene.cleanup(self)
           
    def fill_background(self):
        self.screen.blit(self.background, (0, 0))
                
    def update_specifics(self, time,time_delta):       
        """update title screen""" 
        if self.clicked ==True:
            if self.menu.option_highlighted == 0:
                self.done = True
        
    
        
def main():
    pygame.init()
    pygame.mixer.init()
    import gameplay
    import title
    run_it = scene.Control()
    state_dict = {"TITLE" : title.Title(),
                  "INTRO" : Cutscene0(),
                  "GAMEPLAY" : gameplay.gamePlay(),
                  "ENDING": Cutscene1()
                   }
    run_it.setup_states(state_dict, "INTRO")
    run_it.main()   
    
if __name__ == "__main__":
    main()
        
        
