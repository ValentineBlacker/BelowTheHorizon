'''
Created on Mar 8, 2015

@author: DemiCow
'''

import pygame
import scene
import maphandler
import maincharacter
import baddie
import prepare
import boat
import buddy
import label

#LEVEL RECT MUST BE BIGGER THAN RESOLUTION

class gamePlay(scene.Scene):
    def __init__(self):        
        scene.Scene.__init__(self)
        self.next = "ENDING"
        self.init_variables()
        self.init_objects()   
        
       
    def init_variables(self): 
        """ init all variables needed in scene"""
        self.speed = self.MASTER_SPEED * 3  
        self.collisionblocks = []
        self.max_hp = 10
        self.hp = self.max_hp
        self.hp_block_amount = 3
        self.boatdock = 350
        self.hour = 1
        
                                                            
    def init_objects(self):
        """ creates objects needed in specfic scenes"""  
        self.level_size = (4000,1600)
        self.level = pygame.Surface((self.level_size)).convert()
        self.level_rect = self.level.get_rect()
        self.viewport = self.screen.get_rect( )
       
        self.mainmap = maphandler.foregroundMap(self.level_size) 
        
        self.background = pygame.Surface(self.screen.get_size())
        self.backgroundrect = self.background.get_rect()
        self.spawn_location = (100,800)  
        self.mc = maincharacter.mainCharacter(self, self.spawn_location)               
        self.player = self.mc
        
        self.boat = boat.Boat(self, (0, self.level_size[1]-(self.mainmap.pixel_tile_size[1]*2)))
        
        self.buddies = []
        self.buddyGroup = self.make_sprite_group(self.buddies)
        self.add_group(self.buddyGroup)        
        self.update_light_sources()
                
        self.baddies = [baddie.Baddie(self,(500+ (n*800),1400),image = prepare.IMAGES['mc']) for n in xrange(1)]           
        self.baddieGroup = self.make_sprite_group(self.baddies)        
        self.add_group(self.baddieGroup)        
        
        #
        
        #sun = magiccircle.magicCircle(self, self.mc)
        
        self.label = label.Label(self, (500,500), (300,300))
        
        self.label.textlines = ["hour {0}".format(self.label.int_to_roman[self.hour])]
        self.label.backgroundcolor = self.label.transparent_color        
        self.label.viewport_ready = True
        self.label.toggle_visible(True)        
                        
        self.continuelabel = label.Label(self,(500,400), (300,500), 25)
        self.continuelabel.textlines = ["continue", "quit"]
        self.continuelabel.backgroundcolor = self.continuelabel.transparent_color
        self.continuelabel.clickable = True
        self.continuelabel.toggle_visible(False)
        self.continuelabel.viewport_ready = True
        
        self.sprites = [self.mainmap, self.baddieGroup, self.buddyGroup, self.mc, self.boat, self.continuelabel, self.label] 
        self.center_viewport()         
        self.liferect = pygame.Rect(10,10,10,self.hp*10)
                
    def startup(self, time, persistant):        
        self.start_time = time     
        self.set_music()    
        return scene.Scene.startup(self, time, persistant)
    
    def cleanup(self):        
        return scene.Scene.cleanup(self)
    
    def set_music(self):
        pass
        #self.background_music = pygame.mixer.Sound(prepare.SOUNDS[self.background_songs[self.wave_number]])              
        #self.background_music.play(loops=-1)
    
      
    def get_event(self, event):
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_x:
                self.kill_buddy()
            elif event.key == pygame.K_w:
                self.create_buddy()
                
       
    def mouse_controls(self, time_delta):        
        pass     
    
    def new_level(self):
        self.label.toggle_visible(True)                      
        self.label.textlines = ["Hour {0}".format(self.label.int_to_roman[self.hour])]
        self.mc.reset()        
        for b in self.baddies:
            b.reset()
        for b in self.buddyGroup:
            b.kill() 
        self.mainmap.reset()
        self.center_viewport()
        self.hp = self.max_hp
        
    def quit_to_title(self):
        self.done = True
        self.new_level()        
        
    def handle_life_bar(self):
        if self.hp < 0: self.hp = 0
        if self.hp > self.max_hp: self.hp = self.max_hp
        rectbitlist = []
        for i in range(self.hp):            
            rectbit = pygame.Rect(10,120 -(i*12),10, 10)            
            rectbit.clamp_ip(self.level_rect)
            rectbitlist.append(rectbit)
            pygame.draw.rect(self.screen, (255,255,255), rectbit)
        
    def check_if_dead(self):              
        if self.mc.rect.top>= self.level_size[1] - self.mainmap.pixel_tile_size[1]:
            self.on_death()
            #self.mc.rect.x, self.mc.rect.y = (9000,9000)            
            return True
        elif self.hp <= 0:
           # self.hp = 100
            self.on_death()
            return True
        else: return False
        
    def on_death(self):       
        self.mc.controllable = False
        self.start_time= self.time        
        self.label.toggle_visible(True)        
        self.label.textlines = ["Game Over"]
        self.continuelabel.toggle_visible(True)
        
    def ending_label(self):
        self.label.textlines = ["Hour Cleared"]
        self.label.toggle_visible(True)
        
    def handle_dead_menu(self):
        """called if player runs out of lives"""        
        key_pressed =  pygame.key.get_pressed()
        if self.clicked == True or key_pressed[pygame.K_RETURN]:
            if self.continuelabel.option_highlighted == 0:   
                self.label.toggle_visible(False)            
                self.continuelabel.toggle_visible(False)
                self.new_level()
            elif self.continuelabel.option_highlighted == 1:
                self.quit_to_title()
        else: pass
        
    def check_if_at_gate(self):
        if self.mc.rect.colliderect(self.mainmap.gatecenter):
            return True
        else: return False
        
    def check_hp_blocks(self):
        for h in self.mainmap.hp_block_list:
            if self.mc.rect.colliderect(h):
                if self.hp < self.max_hp:
                    self.hp += self.hp_block_amount
                self.mainmap.hp_block_list.remove(h)
                    
    
    def update_light_sources(self):
        self.light_sources =  [ (self.mc.light_spread, self.mc.light_brightness, self.mc.rect.x, self.mc.rect.y)]       
        buddylights = [(b.light_spread, b.light_brightness, b.rect.x, b.rect.y) for b in self.buddyGroup]        
        for b in buddylights:
            self.light_sources.append(b)        
        
    def draw_blocks(self, switch):   
        #light source tuple is (spread, brightness, rect.x, rect.y)       
        if switch == True:       
            for x in self.mainmap.block_list:
                if x.colliderect(self.viewport):
                    total_abspos = 0
                    for l in self.light_sources:
                        abspos =  int(abs(x.x-l[2]) + abs(l[3]-x.y))    
                        abspos = (abspos/l[0]) - l[1]  /2
                        total_abspos += abspos       
                    if total_abspos == 0:
                        total_abspos = 1
                    total_abspos = total_abspos/len(self.light_sources)  
                    if total_abspos > 255: total_abspos= 255
                    if total_abspos < 0: total_abspos = 0
                    pygame.draw.rect(self.level, (255-total_abspos,255-total_abspos,255-total_abspos), x)
                
            for x in self.mainmap.waterblock_list:
                if x.colliderect(self.viewport):
                    total_abspos = 0
                    for l in self.light_sources:
                        abspos =  int(abs(x.x-l[2]) + abs(l[3]-x.y))    
                        abspos = (abspos/l[0]) - l[1]  /2
                        total_abspos += abspos       
                    if total_abspos == 0:
                        total_abspos = 1
                    total_abspos = total_abspos/len(self.light_sources)  
                    if total_abspos > 255: total_abspos= 255
                    if total_abspos < 0: total_abspos = 0
                    pygame.draw.rect(self.level, (0,0,255-total_abspos), x)
                
            for x in self.mainmap.hp_block_list:
                pygame.draw.rect(self.level, (255,255,255), x)
            
            pygame.draw.rect(self.level, (255,255,0), self.mainmap.gatecenter)
            

        else: pass
    
    def center_viewport(self):
        self.viewport.centerx = self.player.rect.centerx
        self.viewport.centery = self.player.rect.centery
                
    def create_buddy(self):
        newbuddy = buddy.Buddy(self,self.mc.rect.center, 'snek')            
        self.buddyGroup.add(newbuddy)
        self.hp -= newbuddy.hp_factor        
        
    def kill_buddy(self):
        b = [b for b in self.buddyGroup if b.rect.colliderect(self.mc.rect)]
        for a in b:
            a.kill()
            self.hp += a.hp_factor
                          
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
            
    def blit_labels(self):
        """well, it's come down to this. have to blit them here so they don't slide around"""
        """hey I could do this for the background"""
        self.screen.blit(self.label.image, (self.label.rect.x, self.label.rect.y), special_flags= 0)
        self.label.rect.clamp_ip(self.level_rect)
        self.screen.blit(self.continuelabel.image, (self.continuelabel.rect.x, self.continuelabel.rect.y), special_flags= 0)
        self.continuelabel.rect.clamp_ip(self.level_rect)
    
    def update_specifics(self, time, time_delta): 
        """things that need to be updated in individual scenes"""        
        
        if self.time - self.start_time > self.long_time*time_delta:
            self.label.toggle_visible(False)
        
        self.draw_blocks(True)       
        self.update_viewport((self.player.total_displacement))          
        self.screen.blit(self.level, (0,0), self.viewport)
        self.collisionblocks = [b for b in self.mainmap.block_list]
        self.collisionblocks.append(self.boat.rect)
        
        self.handle_life_bar()
        self.update_light_sources()   
        self.check_hp_blocks()
        if self.check_if_at_gate(): self.quit_to_title()
        
        if self.check_if_dead(): 
            self.handle_dead_menu()
            
        if self.mc.rect.colliderect(self.boat.rect):            
            self.update_viewport(self.boat.velocity)
            self.mc.rect.x += self.boat.velocity[0]
            
        self.blit_labels()
        
def main():    
    import title
    import cutscene
    run_it = scene.Control()
    state_dict = {"TITLE" : title.Title(),
                  "INTRO" : cutscene.Cutscene0(),
                  "GAMEPLAY" : gamePlay(),
                  "ENDING": cutscene.Cutscene1()
                   }
    run_it.setup_states(state_dict, "GAMEPLAY")
    run_it.main()   
    
if __name__ == "__main__":
    main()