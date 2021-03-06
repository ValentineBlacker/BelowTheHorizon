'''
Created on Mar 8, 2015

@author: DemiCow
'''

import pygame 
from pygame import display, image
import prepare
import sys



class Control(object):
    """Control class for entire project. Contains the game loop, and contains
    the event_loop which passes events to States as needed. Logic for flipping
    states is also found here."""
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.state_dict = {}
        self.state_name = None
        self.state = None
        
        self.fps = prepare.FPS
        self.time = 0
         
        self.done = False 
        self.pause = False
            
    def setup_states(self, state_dict, start_state):
        """Given a dictionary of States and a State to start in,
        builds the self.state_dict."""
        self.state_dict = state_dict
        self.state_name = start_state
        self.state = self.state_dict[self.state_name]    
        
    def update(self, time,time_delta):
        """Checks if a state is done or has called for a game quit.
        State is flipped if neccessary and State.update is called."""
        self.time = pygame.time.get_ticks()
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.flip_state()
        self.state.update(self.time,time_delta)

    def flip_state(self):
        """When a State changes to done necessary startup and cleanup functions
        are called and the current State is changed."""
        previous,self.state_name = self.state_name, self.state.next
        persist = self.state.cleanup()
        self.state = self.state_dict[self.state_name]
        self.state.startup(self.time, persist)
        self.state.previous = previous
        
    def quit(self):
        self.done = True               
        pygame.quit() 
        sys.exit(0)
     
    def event_loop(self):
        """events- mouse click, escape to exit game. squid controlled by mouse if not android"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    self.quit()
                if event.key == pygame.K_p:
                    self.toggle_poggle()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    self.toggle_poggle()
            self.state.get_event(event)
            
    def toggle_poggle(self):
        if self.pause == True:
            self.pause = False
            pygame.display.set_caption(prepare.CAPTION)
        else: 
            self.pause = True
            pygame.display.set_caption("PAUSED")
            
            
    def main(self):
        """Main loop for entire program."""
        while not self.done:            
            self.event_loop()
            time_delta = self.clock.tick(self.fps)/1000.0
            #pygame.display.set_caption(str(self.clock.get_fps()))
            if not self.pause:
                self.update(self.time,time_delta)  
            pygame.display.flip()    
            self.time = pygame.time.get_ticks()/self.fps          
            
class Scene(object):
    def __init__(self):    
        """sets up things needed in all scenes. not meant to be used on its own."""    
         
    
        self.start_time = 0
        self.time = 0
        resolution = prepare.RESOLUTION
        self.screen = prepare.SCREEN
        self.screen_center = ((resolution[0]/2), (resolution[1]/2))
        self.field_length = resolution[0]
        self.field_height = resolution[1]
        self.fullscreen = 0
        self.screen_center = ((resolution[0]/2), (resolution[1]/2))
       
        self.MASTER_SPEED = prepare.MASTER_SPEED
        #camera determines what's visible and what's off screen
        self.camera = self.screen.get_rect()
                 
        self.keys = pygame.key.get_pressed()
        pygame.key.set_repeat(50000, 50000)      
        self.sprites = []
        self.maps = []
        self.groups = []
         
        self.clicked = False
        
        self.done = False
        self.quit = False
        self.next = None
        self.previous = None
        self.persist = {}
        
        #variables to standardize timing across game
        self.micro_time = 500
        self.short_time = 15000
        self.mid_time = 65000
        self.long_time = 185000
        
    def startup(self, time, persistant):
        """Add variables passed in persistant to the proper attributes and
        set the start time of the State to the current time."""
        self.persist = persistant
        self.start_time = time
            
    def cleanup(self):
        """Add variables that should persist to the self.persist dictionary.
        Then reset State.done to False."""
        self.done = False
        return self.persist
        
    def get_event(self, event):
        """Processes events that were passed from the main event loop.
        Must be overloaded in children."""
        if event.type == pygame.MOUSEBUTTONDOWN:            
            self.clicked = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.clicked = False
     
               
    def fill_background(self):
        pass
      
    def init_variables(self):
        """ place to store all variables needed in scene"""
        pass
        
    def init_objects(self):
        """ creates objects needed in specfic scenes"""
        pass
    
  
    def make_sprite_group(self, sprites):

        """ create a group called groupName
            containing all the sprites in the sprites 
            list.  This group will be added after the 
            sprites group, and will automatically
            clear, update, and draw
        """
        tempgroup = pygame.sprite.LayeredDirty(sprites)
        return tempgroup

    

    def add_group(self, group):

        """ adds a sprite group to the groups list for
            automatic processing 
        """
        self.groups.append(group)
                   

    def update(self, time, time_delta):
        self.time = time
        self.fill_background()
        for sprite in self.sprites:
            sprite.update(self, time_delta)        
        self.mouse_controls(time_delta)
        self.update_specifics(time, time_delta)
        self.keys = pygame.key.get_pressed()
        
    def update_specifics(self, time, time_delta):
        pass
        
    
    def mouse_controls(self, time_delta):
        pass
  
    

