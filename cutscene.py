'''
Created on Mar 13, 2015

@author: DemiCow
'''

import pygame
import scene
import label


import prepare

class Cutscene0(scene.Scene):
    
    def __init__(self):        
        scene.Scene.__init__(self)
        self.next = "GAMEPLAY"
        self.init_variables()
        self.init_objects()  

    
    def init_objects(self):
        """ creates objects needed in specfic scenes"""        
        self.label = label.Label(self, font_size = 50)
        self.label.textlines = ["INTRO. AARGH."]
        self.menu = label.Label(self, font_size = 50)        
        self.menu.textlines = ["click to start game"]
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
        
        
