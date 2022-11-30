import pygame, sys, math

class Mario(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        #self.bg = pygame.image.load("background.png")
       
        self.x, self.y = x, y
        self.width, self.height = 40,55#self.image.get_width(), self.image.get_height()
        #self.rect = self.image.get_rect(center = (x,y))#.inflate(-5,-0.9)
        self.rect = pygame.Rect(x, y, 45,55)#pygame.Rect(250, 400,45,55)
        #self.hitbox = pygame.Rect(self.rect.x + 8, self.rect.y + 5, 35,48)
        
        self.jump = False
        self.walking_right = False
        self.walking_left = False
        self.facing_right = True
        self.facing_left = False
        self.gravity = 1
        self.y_vel = 0
        self.speed = 10
        self.slowing_down = 6
        self.walk_left,self.walk_right = [],[]
        for i in range(1,4):                
            self.walk_left.append(pygame.transform.scale(pygame.image.load("l{}.png".format(i)), (50,55)))
            self.walk_right.append(pygame.transform.scale(pygame.image.load("r{}.png".format(i)), (50,55)))
        
       
        self.walk_count = 0
        
       #print(self.hitbox.x,self.hitbox.y, self.rect.width, self.rect.height)
            
    def update(self):
        self.draw()
        self.move()

    def draw(self):
        mario_group.draw(screen)
        #self.hitbox = pygame.Rect(self.rect.x + 8, self.rect.y + 5, 35,48)
        #print(self.hitbox.x,self.hitbox.y, self.hitbox.width, self.hitbox.height)
        
        #pygame.draw.rect(screen, (0,0,0), self.rect, 2)
        

    def move(self):
        dx = 0
        dy = 0
        
        
        # Standing direction
        def standing_direction():
            if self.facing_left:
                self.image = pygame.transform.scale(pygame.image.load("idle_left.png"), (55, 55))
            elif self.facing_right:
                self.image = pygame.transform.scale(pygame.image.load("idle_right.png"), (55, 55))
            return self.image

        # walking animation
        def walking_animation():
            if self.walking_left:
                self.image = self.walk_left[int(self.walk_count)]
            elif self.walking_right:
                self.image = self.walk_right[int(self.walk_count)]
            return self.image

        # Jump direction
        def jump_direction():
            if self.facing_left and self.jump:
                self.image = pygame.transform.scale(pygame.image.load("jumping_left.png"), (55, 55))
            elif self.facing_right and self.jump:
                self.image = pygame.transform.scale(pygame.image.load("jumping_right.png"), (55, 55))
            return self.image
        
        # Gravity
        def gravity():
            if not(self.jump):   
                self.y_vel += self.gravity 
                if self.y_vel > 20:
                    self.y_vel = 0


        
            

                    
        
        # key events and motions
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_UP] or keys[pygame.K_SPACE]) and self.jump == False:
            self.jump = True
            self.y_vel = -17
            
            
            
        if keys[pygame.K_LEFT]:
            dx -= self.speed
            self.x = self.rect.x
            self.walking_left = True
            self.facing_left  = True
            self.walking_right = False
            self.facing_right = False

        if keys[pygame.K_LEFT] == False:
            #self.image = pygame.transform.scale(pygame.image.load("standing_left.png"), (50, 55))
            self.image = standing_direction()
            self.walking_left = False
            
        if keys[pygame.K_RIGHT]:
            dx += self.speed
            self.x = self.rect.x
            self.walking_right = True
            self.facing_right = True
            self.walking_left = False
            self.facing_left = False

        if keys[pygame.K_RIGHT] == False:
            #self.image = pygame.transform.scale(pygame.image.load("standing_left.png"), (50, 55))
            self.image = standing_direction()
            self.walking_right = False


        # Jump mechanics
        if self.jump:
            self.image = jump_direction()
            dy += self.y_vel
            self.y_vel += 1
            if self.y_vel > 10:
                self.y_vel = 10

        # add gravity
        gravity()
        

        # Walking and turning animation  
        if self.walk_count >= len(self.walk_left):
            self.walk_count = 0

        if self.walking_left:
            if self.jump:
                self.image = jump_direction()
            elif event.key == pygame.K_RIGHT:
                self.image = pygame.transform.scale(pygame.image.load("skid_left.png"), (50, 55))
                self.rect.x += self.slowing_down
                #self.x = self.rect.x
            else:
                self.image = walking_animation()#self.walk_left[self.walk_count//3]
                self.walk_count += 0.1    
           
        if self.walking_right:
            if self.jump:
                self.image = jump_direction()
            elif event.key == pygame.K_LEFT:
                self.image = pygame.transform.scale(pygame.image.load("skid_right.png"), (50, 55))
                self.rect.x -= self.slowing_down
                #self.x = self.rect.x
            else:
                self.image = walking_animation()#self.walk_right[self.walk_count//3]
                self.walk_count += 0.1
                
        
        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height
            dy = 0


        
        # collision detection
    
        for tile in world.tile_list:
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width,  self.height): #self.hitbox.x + dx, self.hitbox.y, self.hitbox.width, self.hitbox.height
            #if abs(floor.rect.right - (self.rect.left + dx))<2:
                dx = 0
        
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height): #self.hitbox.x, self.hitbox.y + dy, self.hitbox.width,  self.hitbox.height
                #block above player; jumping
                if self.y_vel < 0:
                    dy = (tile[1].bottom - self.rect.top) 
                    self.y_vel = 0
                
                #block below player; falling
                elif self.y_vel > 0:
                    dy = (tile[1].top - self.rect.bottom) 
                    self.y_vel = 0
                    if self.jump:
                       # self.y_vel = 0
                        self.jump = False
       # print(self.y_vel)

        '''
        def tweening(tile):
            b = True
            if b:
                tile[1].y -= 5
                b = False
            tile[1].y += 5
           # screen.blit(tile[0], (tile[1].x, tile[1].y + 5))
            '''


        for tile in block.tile_list:
            b = False
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width,  self.height): #self.hitbox.x + dx, self.hitbox.y, self.hitbox.width, self.hitbox.height
            #if abs(floor.rect.right - (self.rect.left + dx))<2:
                dx = 0
        
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height): #self.hitbox.x, self.hitbox.y + dy, self.hitbox.width,  self.hitbox.height
                #block above player; jumping
                if self.y_vel < 0:
                    dy = (tile[1].bottom - self.rect.top)
                    start_pos = tile[1].y
                    #tweening(tile)
                    
                    
                    block_speed = 18
                    self.y_vel = 0
                
                    
                
                #block below player; falling
                elif self.y_vel > 0:
                    dy = (tile[1].top - self.rect.bottom) 
                    self.y_vel = 0
                    if self.jump:
                        self.jump = False

        
                
                
    


        # update y displacement
        dy += self.y_vel
        
        # update coordinates
        self.rect.x += dx; self.x = self.rect.x
        self.rect.y += dy; self.y = self.rect.y
        

        
        #scroll screen
        '''
        screen_scroll = 0
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right > screen_width - scroll_thresh:
            self.rect.x -= self.speed
            screen_scroll = -self.speed
            self.x += self.speed
        if self.x > 1600: 
            self.rect.x += self.speed
            screen_scroll = 0
        #print(self.x, screen_scroll)
        return screen_scroll'''
        
        


        
                        




class Goomba(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("goomba1.png"), (40,40))
        self.x, self.y = x, y
        self.width, self.height = 40, 40
        self.rect = self.image.get_rect(center = (x, y))
        #print(self.rect.width,self.rect.height)
        self.walking_left = True
        self.walking_right = False
        self.speed = 2
        self.y_vel = 0
        self.gravity = 1
        
        self.walk_left, self.walk_right = [], []
        for i in range(1,3):
            self.walk_left.append(pygame.transform.scale(pygame.image.load("goomba{}.png".format(i)), (40,40)))
        for i in range(2,0, -1):
            self.walk_right.append(pygame.transform.scale(pygame.image.load("goomba{}.png".format(i)), (40,40)))
            
        self.walk_count = 0
       

    def draw(self):
        goomba_group.draw(screen)
        #pygame.draw.rect(screen, (0,0,0), self.rect, 2)
        

    def update(self):
        self.draw()
        self.move()
        
    def move(self):
        dx = 0
        dy = 0
        
        def walking_animation(dx):
            #if self.walking_left or self.speed > 0:
            if self.speed > 0:
                #print(1)
                dx -= self.speed
                self.image = self.walk_left[int(self.walk_count)]
                self.walk_count += 0.15
                
            #elif self.walking_right or self_speed < 0:
            elif self.speed < 0:
                #print(2)
                dx -= self.speed
                self.image = self.walk_right[int(self.walk_count)]
                self.walk_count += 0.15
            return self.image, dx
        
        def gravity():
            self.y_vel += self.gravity 
            if self.y_vel > 20:
                self.y_vel = 0


        if self.walk_count >= len(self.walk_right):
            self.walk_count = 0


        self.image, dx = walking_animation(dx)[0], walking_animation(dx)[1]
        '''
        if self.walking_left:
            #self.walking_right = False 
            self.image = walking_animation()
            dx -= self.speed
            self.walk_count += 0.15
            
        if self.walking_right:
            #self.walking_left = False
            self.image = walking_animation()
            dx += self.speed
            self.walk_count += 0.15
        '''

        gravity()
        

        for tile in world.tile_list:
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width,  self.height): #self.hitbox.x + dx, self.hitbox.y, self.hitbox.width, self.hitbox.height
            #if abs(floor.rect.right - (self.rect.left + dx))<2:
                dx = 0
            
                
        
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height): #self.hitbox.x, self.hitbox.y + dy, self.hitbox.width,  self.hitbox.height        
                #block below player; falling
                if self.y_vel > 0:
                    dy = (tile[1].top - self.rect.bottom) 
                    self.y_vel = 0
                    #if self.jump:
                       # self.y_vel = 0
                     #   self.jump = False
            
            
        
                    
        
        
    
        for tile in block.tile_list:
            
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width,  self.height): #self.hitbox.x + dx, self.hitbox.y, self.hitbox.width, self.hitbox.height
            #if abs(floor.rect.right - (self.rect.left + dx))<2:
                #print(1)
                #self.speed *= -1
                pass
                
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height): #self.hitbox.x, self.hitbox.y + dy, self.hitbox.width,  self.hitbox.height
                
                    
                
                #block below player; falling
                if self.y_vel > 0:
                    dy = (tile[1].top - self.rect.bottom) 
                    self.y_vel = 0
                    


        
        

        dy += self.y_vel
        
        self.rect.x += dx
        self.rect.y += dy



'''
class World(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.bg = pygame.image.load("background.png")#, pygame.image.load("background2.png")]
        self.floor = pygame.transform.scale(pygame.image.load("floor.png"), (40,40))
        self.floor_rect = self.floor.get_rect()
        
    
            
    def draw_floor(self):
        for i in range(0, 15):
            screen.blit(self.floor, (self.floor.get_width() * i, 760 - self.floor.get_height()))
            screen.blit(self.floor, (self.floor.get_width() * i, 800 - self.floor.get_height()))
'''
class Blocks(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.tile_list = []

        
        brick_img = pygame.transform.scale(pygame.image.load("brick.png"), (40,40))
        for i in range(3,5):
            brick_img_rect = brick_img.get_rect(center = (40*i, 600))
            tile = brick_img, brick_img_rect
            self.tile_list.append(tile)

        
        block_img = pygame.transform.scale(pygame.image.load("block.png"), (30,30))
        for y in range(0,5):
            for x in range(0,5):
                if y == 0 or not(y > x):
                    block_img_rect = block_img.get_rect(center = (500 + 30*x, 708-30*y))
                    tile = block_img, block_img_rect
                    self.tile_list.append(tile)


        
        

                                    
        
        self.q_list = []
        self.current = 0
        for i in range(1,4):
            self.q_list.append(pygame.transform.scale(pygame.image.load("q{}.png".format(i)), (45,45)))



        pipe_img = pygame.transform.scale(pygame.image.load("pipe.png"), (180,150))
        pipe_img_rect = pygame.Rect(851, 598, 79, 130)#pipe_img.get_rect(center = (300, 650))
        tile = pipe_img, pipe_img_rect
        self.tile_list.append(tile)

        

               
        
        
        
            
    def draw(self):
        
        for tile in self.tile_list:
            if tile == self.tile_list[-1]:
                screen.blit(tile[0], (800,582))
                #pygame.draw.rect(screen, (255,0,0), tile[1], 2)
            else:
                screen.blit(tile[0], tile[1])
                #pygame.draw.rect(screen, (255,0,0), tile[1], 2)
        
        
        
        
        self.current += 0.25
        if self.current >= len(self.q_list):
            self.current = 0
        screen.blit(self.q_list[int(self.current)], self.q_list[0].get_rect(center = (197, 599)))
        
      #  pygame.draw.rect(screen, (255,0,0), self.q_list[0].get_rect(center = (197, 599)), 2)

        


class World():
    def __init__(self):
        self.bg = pygame.transform.scale(pygame.image.load("sky2.png"), (screen_width, screen_height))#, pygame.image.load("background2.png")]
        self.tile_list = []



        #floor
        floor_img = pygame.transform.scale(pygame.image.load("floor.png"), (40,40))
        for i in range(30):
            floor_img_rect = floor_img.get_rect(center = (40 * i, 741))
            tile = floor_img, floor_img_rect
            self.tile_list.append(tile)
            floor_img_rect = floor_img.get_rect(center = (40 * i, 780))
            tile =  floor_img, floor_img_rect
            self.tile_list.append(tile)
        
        #floor_img_rect = floor_img.get_rect(center = (400, 600))
        #tile = floor_img, floor_img_rect
        #self.tile_list.append(tile)
        #floor_img_rect = floor_img.get_rect(center = (200, 698))
        #tile = floor_img, floor_img_rect
        #self.tile_list.append(tile)

        
    def draw(self):
       
        screen_scroll = mario.move()
        self.draw_sky(screen_scroll)
            
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            
            #pygame.draw.rect(screen, (250,0,0), tile[1], 2)
        
        #pygame.draw.rect(screen, (255,0,0), self.pipe_img_rect, 2)



    def draw_sky(self,x):
        global bg_scroll
        bg_width = self.bg.get_width()
        tiles = math.ceil(screen_width / bg_width) + 1
        screen.blit(self.bg, (0,0))
        #bg_scroll += x
        #for i in range(0,tiles):
         #   screen.blit(self.bg, (i*bg_width+bg_scroll,0))
            #self.bg.append(self.bg.pop(1))
        #if abs(bg_scroll - 400) > bg_width :
         #   bg_scroll = 0
  
        
        
            

        
        
    

'''
class Floor(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("floor.png"), (40,40))
        self.x, self.y = x, y
        self.rect = self.image.get_rect(center = (x, y))
        World(self.rect)
        
        
    def update(self):
        pass
        #pygame.draw.rect(screen, (255,0,0), self.rect, 2)
'''

        
    #def update(self):
        
        
        


pygame.init()
clock = pygame.time.Clock() 

screen_width, screen_height = 1200, 800
screen = pygame.display.set_mode((screen_width, screen_height))

#scroll_thresh = 400 
#bg_scroll = 0
    
mario = Mario(250,698)
mario_group = pygame.sprite.Group()
mario_group.add(mario)

goomba = Goomba(600,500)
goomba_group = pygame.sprite.Group()
goomba_group.add(goomba)


block = Blocks()
world = World()


#world_floor_group = pygame.sprite.Group()
#world_floor_group.add(world.draw_floor)

'''
floor_group = pygame.sprite.Group()
for i in range(15): 
    floor = Floor(40 * i, 778 - 37)
    floor_group.add(floor)
    floor2 = Floor(40 * i, 800 - 20)
    floor_group.add(floor2)
'''

#for i in floor_group:
 #   print(i.rect.top)
                        

    


while True:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    

    
    screen.fill((250,250,250))
    
    #world.draw_floor()
   # floor_group.draw(screen)
    #floor_group.update()
    world.draw()
    block.draw()

    #scroll -= 5
    #if abs(scroll) > bg_width:
     #   scroll = 0


    mario_group.update()
    goomba_group.update()
    
    pygame.display.flip()
    clock.tick(25)
