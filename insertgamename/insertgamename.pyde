# INTRO TO COMPUTER SCIENCE - Final Project.
# Priyamvada Daga (psd7123@nyu.edu) & Aigerim Zhusubalieva (az2177@nyu.edu).

# this is the source code for the game "*insert game name*".

import random, os    # imports random and os modules
path = os.getcwd()   # variable 'path' containing path to the current directory
add_library('minim') # add library for the game audio
player = Minim(this) # create an audio player for the game

# main game constants
WIDTH = 1040
HEIGHT = 720

# mini-game 2 constants
NUM_ROWS = 4
NUM_COLS = 4
BLOCK_SIZE = 100

# loading some images and sounds

background_main = loadImage(path + "/backgrounds/bg1.png")
background_start = loadImage(path + "/backgrounds/bg2.png")
mg2_start_screen = loadImage(path + "/backgrounds/bg mg2.png")
mg2_end_screen = loadImage(path + "/backgrounds/bg2 mg2.png")
mg2_end_screen_2 = loadImage(path + "/backgrounds/bg3 mg2.png")
game_over = loadImage(path + "/backgrounds/game over.png")
heart_img = loadImage(path + "/symbols/heart.png")
bheart_img = loadImage(path + "/symbols/bheart.png")

levelup_snd = player.loadFile(path + "/sounds/level_up.mp3")
collect_snd = player.loadFile(path + "/sounds/collect.mp3")


class Game:
    def __init__(self, w, h, g):
        self.w = w  # attribute describing width
        self.h = h  # attribute describing height
        self.g = g  # attribute describing ground
        self.bases = [Base(25, 430 - 380, 325, 185), Base(25 + 330, 430 - 380, 325, 185), Base(25 + 660, 430 - 380, 325, 185), Base(25, 430 - 190, 325, 185), Base(25 + 330, 430 - 190, 325, 185), Base(25 + 660, 430 - 190, 325, 185) , Base(25, 430, 325, 185), Base(25 + 330, 430, 325, 185), Base(25 + 660, 430, 325, 185)] # list attribute describing all bases i.e. all boxes in the zoom window
        self.m1count = 0    # attribute tracking number of thumbs-ups collected (required to unlock mini-game 1)
        self.m2count = 0    # attribute tracking number of claps collected (required to unlock mini-game 2)
        self.m3count = 0    # attribute tracking number of party poppers collected (required to unlock mini-game 1)
        self.thumbsups = [] # list containing Collectible objects with thumbs up image to be displayed on main screen
        self.claps = []     # list containing Collectible objects with clap image to be displayed on main screen
        self.partys = []    # list containing Collectible objects with party image to be displayed on main screen
        self.raisedhands = 0    # attribute tracking raised hands
        self.hearts = 3         # attribute tracking hearts
        self.mg2startscreen = False     # boolean attribute used to display floating start screen in mini game 2
        self.currentscreen = "START"    # variable tracking current screen 

        # initializing mini-games
        self.game2048 = Game2048()
        self.dinogame = Dino(WIDTH, HEIGHT, 400)
        self.gwd = Gwd(WIDTH, HEIGHT, HEIGHT)
        
        # reading current progress
        try:
            progress = open("progress.csv", 'r')
            spritenum = progress.readline().strip().split(",")
            self.spritenum = int(spritenum[1])
            rhs = progress.readline().strip().split(",")
            self.raisedhands = int(rhs[1])
            hts = progress.readline().strip().split(",")
            self.hearts = int(hts[1])
            cltbls = progress.readline().strip().split(",")
            self.m1count = int(cltbls[1])
            self.m2count = int(cltbls[2])
            self.m3count = int(cltbls[3])
            self.choosesprite(int(self.spritenum))
            progress.close()    
        except:
            print("new player")
        
        # calling method to display new collectibles on start screen
        self.backtomain()
    
    def choosesprite(self, spritenum):  # method to choose sprite from start screen
        self.spritenum = int(spritenum) # variable describing sprite number (for saving purposes)
        self.currentscreen = "MAIN"
        if spritenum == 1:
            self.sprite = Sprite(100, 100, 58, self.g, "girl1.png", 97, 116, 6)
        elif spritenum == 2:
            self.sprite = Sprite(100, 100, 56, self.g, "girl2.png", 95, 113, 7)
    
    def backtomain(self):   # method to appropriately add elements to collectible lists
        if self.m1count!=10:
            while len(self.thumbsups) + self.m1count != 10:
                self.thumbsups.append(Collectible("thumbsup.png"))
        if self.raisedhands >= 5 and self.m2count!=10:
            while len(self.claps) + self.m2count != 10:
                self.claps.append(Collectible("clap.png"))
        if self.raisedhands >= 10 and self.m3count!=10:
            while len(self.partys) + self.m3count != 10:
                self.partys.append(Collectible("party.png"))
            
    def display(self):  # display method for the game

        # conditionals to display appropriate screen depending on the currentscreen attribute

        # displaying appropriate elements for the "MAIN" screen.
        if self.currentscreen == "MAIN" and not self.mg2startscreen:
            image(background_main, 0, 0)
            
            # displaying collectible progress bars
            noFill()
            stroke(180)
            strokeWeight(2)
            for i in range(3):
                 rect(75, 77+(30*i), 100, 4)
            fill(0, 230, 0)
            rect(75, 77, self.m1count*10, 4)
            rect(75, 77+30, self.m2count*10, 4)
            rect(75, 77+60, self.m3count*10, 4)
            
            # displaying raised hands progress bar and hearts
            noFill()
            stroke(180)
            strokeWeight(2)
            rect(260, 77, 70, 4)
            
            fill(0, 230, 0)
            if self.raisedhands < 10:
                rect(260, 77, (self.raisedhands%5) * 14, 4)
            else:
                rect(260, 77, 5 * 14, 4)
            for i in range(3):
                image(bheart_img, 225+(35*i), 105)
            for i in range(self.hearts):
                image(heart_img, 225+(35*i), 105)
            
            # displaying collectibles
            for t in self.thumbsups:
                t.display()
            for c in self.claps:
                c.display()
            for p in self.partys:
                p.display()

            # displaying sprite
            self.sprite.display()
        
        # displaying floating start screen for mini-game 2
        elif self.mg2startscreen:
            stroke(255)
            strokeWeight(3)
            rect(100-3, 100-3-30, 1040-200+6, 720-200+6)
            image(mg2_start_screen, 100, 100-30)
        
        # displaying mini-game 2    
        elif self.currentscreen == "MINIGAME2":
            self.game2048.display()
        
        # displaying mini-game 1
        elif self.currentscreen == "MINIGAME1":
            self.dinogame.display()
        
        # displaying mini-game 3
        elif self.currentscreen == "MINIGAME3":
            self.gwd.display()
    
    def savedata(self): # method to save data, by writing csv files
        try:
            progress = open("progress.csv", 'w')
            progress.write("Sprite," + str(self.spritenum) + "\n")
            progress.write("Raised Hands," + str(self.raisedhands) + "\n")
            progress.write("Hearts," + str(self.hearts) + "\n")
            progress.write("Collectibles," + str(self.m1count) + "," + str(self.m2count) + "," + str(self.m3count) + "\n")
            progress.close()
        except:
            print("DATA NOT SAVED: sprite not chosen yet")


class Sprite():
    def __init__(self, x, y, r, g, img_name, img_w, img_h, num_frames):
        self.x = x  # attribute describing x-coordinate
        self.y = y  # attribute describing y-coordinate
        self.r = r  # attribute describing radius
        self.g = g  # attribure describing ground 
        self.vx = 0 # attribute describing speed in x-direction
        self.vy = 0 # attribute describing speed in y-direction

        self.img = loadImage(path + "/sprites/" + img_name) # attribute describing image location
        self.img_w = img_w  # attribute describing image width
        self.img_h = img_h  # attribute describing image height
        self.num_frames = num_frames    # attribute describing frames of animation
        self.frame = 0      # attribute describing current frame
        self.dir = RIGHT    # attribute describing current direction 
        self.key_handler = {LEFT:False, RIGHT:False, UP:False, DOWN:False}

    def gravity(self): # method for gravity to act on the sprite

        if self.y + self.r >= self.g:
            self.vy = 0
        else:
            self.vy += 0.3
            if self.y + self.r + self.vy > self.g:
                self.vy = self.g - (self.y + self.r)
        
        # updating sprite's ground if above a base
        for b in game.bases:
            if self.y + self.r <= b.y + b.h and self.x + self.r >= b.x and self.x + self.r <= b.x + b.w:
                self.g = b.y + b.h
                break
            else:
                self.g = game.g
        
    def update(self): # method updating sprite when dealing with possible key-presses and interactions
        self.gravity()
        
        # updating velocity in the x-direction if arrow keys used
        if self.key_handler[LEFT] == True:
            self.vx = -10
            self.dir = LEFT
        elif self.key_handler[RIGHT] == True:
            self.vx = 10
            self.dir = RIGHT
        else:
            self.vx = 0

        # updating velocity in the y-direction if arrow keys used + creating a falling motion with down key
        if self.key_handler[UP] and self.y + self.r == self.g:
            self.vy = -12
        if self.key_handler[DOWN] and self.y + self.r == self.g and self.y + self.r < game.g:
            self.y += 1
        
        # displaying sprite animation
        if frameCount%3 == 0 and self.vx != 0 and self.vy == 0:
            self.frame = (self.frame + 1) % self.num_frames
        elif self.vx == 0:
            self.frame = 0
        
        # updating x and y depending on velocity
        if not(self.x <= 0 and self.vx < 0) and not(self.x >= WIDTH - 2*self.r and self.vx > 0):
            self.x += self.vx
        self.y += self.vy
        
        # handling interactions with collectibles

        for t in game.thumbsups:
            if self.distance(t) <= self.r + t.r:
                if game.m1count < 10:
                    game.m1count += 1
                collect_snd.rewind()
                collect_snd.play()
                game.thumbsups.remove(t)
        
        for c in game.claps:
            if self.distance(c) <= self.r + c.r:
                if game.m2count < 10:
                    game.m2count += 1
                collect_snd.rewind()
                collect_snd.play()
                game.claps.remove(c)
                
        for p in game.partys:
            if self.distance(p) <= self.r + p.r:
                if game.m3count < 10:
                    game.m3count += 1
                collect_snd.rewind()
                collect_snd.play()
                game.partys.remove(p)
    
    def distance(self, target): # method for obtaining distance between sprite and target
        return ((self.x - target.x)**2 + (self.y - target.y)**2) ** 0.5
        
    def display(self):  # method to display sprite
        self.update()
        
        if self.dir == RIGHT:
            image(self.img, self.x, self.y - self.r, self.img_w, self.img_h, self.frame * self.img_w, 0, (self.frame + 1) * self.img_w, self.img_h)
        elif self.dir == LEFT:
            image(self.img, self.x, self.y - self.r, self.img_w, self.img_h, (self.frame + 1) * self.img_w, 0, self.frame * self.img_w, self.img_h)        

class Base:
    def __init__(self, x, y, w, h):
        self.x = x  # attribute describing x-coordinate
        self.y = y  # attribute describing y-coordinate
        self.w = w  # attribute describing width
        self.h = h  # attribute describing height

class Collectible():
    def __init__(self, img):
        self.x = random.randint(30,1000)    # attribute for x, random location within bounds
        self.y = random.randint(30,600)     # attribute for y, random location within bounds
        self.r = 15
        self.img = loadImage(path + "/symbols/" + img)
    
    def display(self):  # displaying image depending on which collectible
        image(self.img, self.x, self.y)


# MINI-GAME 2

class Block():

    def __init__(self, row, col, value):
        self.row = row      # attribute describing block's row
        self.col = col      # attribute describing block's column
        self.value = value  # attribute describing block's value (i.e. 2, 4, 8, 16, etc.)
        

    def display(self):
        # displaying block depending on the value and location
        if self.value <= 128: 
            self.img = loadImage(path + "/images2048/" + str(self.value) + ".png")
        else:
            self.img = loadImage(path + "/images2048/" + "toobig.png")
        image(self.img, self.col * BLOCK_SIZE + 320, self.row * BLOCK_SIZE + 50, BLOCK_SIZE, BLOCK_SIZE)
        stroke(0)
        strokeWeight(3)
        rect(self.col * BLOCK_SIZE + 320, self.row * BLOCK_SIZE + 50, BLOCK_SIZE, BLOCK_SIZE)

class Game2048(list):   # 2048 game class inheriting from list class

    def __init__(self):
        # empty 2d list for board
        for r in range(NUM_ROWS):
            ls = []
            for c in range(NUM_COLS):
                ls.append(None)
            self.append(ls)
        self.cnt = 0        # attribute used to ensure only one bonus tile is generated
        self.win = False    # attribute storing if won
        self.info = loadImage(path + "/images2048/" + "info.png")   # loading info image
        
        self.win_snd = player.loadFile(path + "/sounds/2048/win.mp3")
        self.bonus_snd = player.loadFile(path + "/sounds/2048/bonus.mp3")
        
        # adding 2 blocks to initialize the game
        self.add_new_block()
        self.add_new_block()

    def add_new_block(self):    # method for adding a new block of either 2 or 4 value at a random open location
        twelve = self.check_128()   # variable to check if 128 tile is there
        flag = False
        while flag == False:
            r = random.randint(0, 3)
            c = random.randint(0, 3)
            if twelve and self.cnt == 1:
                v = 12
                self.bonus_snd.rewind()
                self.bonus_snd.play()
            else:
                v = random.choice([2, 2, 2, 2, 4])
            if not isinstance(self[r][c], Block):
                flag = True
        new_block = Block(r, c, v)
        self[r][c] = new_block

    def display(self):
        background(0)
        noFill()
        stroke(87, 6, 140)
        strokeWeight(3)
        rect(320-3, 50-3, NUM_ROWS*BLOCK_SIZE + 3*2, NUM_COLS*BLOCK_SIZE + 3*2)
        image(self.info, 320 - 5, NUM_ROWS * BLOCK_SIZE + 50)
        for r in range(NUM_ROWS):
            for c in range(NUM_COLS):
                if isinstance(self[r][c], Block):
                    self[r][c].display()    
        
        # display messages when game over
        if self.win:
            self.win_snd.play()
            stroke(255)
            strokeWeight(3)
            rect(100-3, 100-3-30, 1040-200+6, 720-200+6)
            image(mg2_end_screen, 100, 100-30)
        elif self.game_over() and not self.win:
            stroke(255)
            strokeWeight(3)
            rect(100-3, 100-3-30, 1040-200+6, 720-200+6)
            image(mg2_end_screen_2, 100, 100-30)

    def move_left(self):    # method to move blocks left when left arrow key pressed
        movement = False    # local variable to check if any movement has happened
        alldone = False     # local variable to check if all blocks have moved
        while alldone == False:
            for r in range(NUM_ROWS):
                for c in range(0, NUM_COLS - 1, 1):
                    if isinstance(self[r][c], Block) and isinstance(self[r][c + 1], Block):
                        if self[r][c + 1].value == self[r][c].value:
                            self[r][c].value *= 2
                            self[r][c + 1] = None
                            movement = True
                        elif (self[r][c + 1].value == 128 and self[r][c].value == 12) or (self[r][c + 1].value == 12 and self[r][c].value == 128):
                            self.win = True
            
            for r in range(NUM_ROWS):
                for c in range(NUM_COLS - 1, 0, -1):
                    if isinstance(self[r][c], Block) and not isinstance(self[r][c - 1], Block):
                            self[r][c - 1] = Block(r, c - 1, self[r][c].value)
                            self[r][c] = None
                            movement = True
            alldone = True
            for r in range(NUM_ROWS):
                for c in range(NUM_COLS - 1, 0, -1):
                    if isinstance(self[r][c], Block) and (self[r][c - 1] == None or self[r][c - 1].value==self[r][c].value):
                        alldone = False
                        break
        if movement:
            self.add_new_block()
    
    def move_right(self):   # method to move blocks right when right arrow key pressed
        movement = False    # local variable to check if any movement has happened
        alldone = False     # local variable to check if all blocks have moved
        while alldone == False:
            for r in range(NUM_ROWS):
                for c in range(NUM_COLS - 1, 0, -1):
                    if isinstance(self[r][c], Block) and isinstance(self[r][c - 1], Block):
                        if self[r][c - 1].value == self[r][c].value:
                            self[r][c].value *= 2
                            self[r][c - 1] = None
                            movement = True
                        elif (self[r][c - 1].value == 128 and self[r][c].value == 12) or (self[r][c - 1].value == 12 and self[r][c].value == 128):
                            self.win = True
            
            for r in range(NUM_ROWS):
                for c in range(0, NUM_COLS - 1, 1):
                    if isinstance(self[r][c], Block) and not isinstance(self[r][c + 1], Block):
                        self[r][c + 1] = Block(r, c + 1, self[r][c].value)
                        self[r][c] = None
                        movement = True
            alldone = True
            for r in range(NUM_ROWS):
                for c in range(0, NUM_COLS - 1, 1):
                    if isinstance(self[r][c], Block) and (self[r][c + 1] == None or self[r][c + 1].value==self[r][c].value):
                        alldone = False
                        break
        if movement:
            self.add_new_block()
    
    def move_up(self):      # method to move blocks up when up arrow key pressed
        movement = False    # local variable to check if any movement has happened
        alldone = False     # local variable to check if all blocks have moved
        while alldone == False:
            for c in range(NUM_COLS):
                for r in range(0, NUM_ROWS - 1, 1):
                    if isinstance(self[r][c], Block) and isinstance(self[r + 1][c], Block):
                        if self[r + 1][c].value == self[r][c].value:
                            self[r][c].value *= 2
                            self[r + 1][c] = None
                            movement = True
                        elif (self[r + 1][c].value == 128 and self[r][c].value == 12) or (self[r + 1][c].value == 12 and self[r][c].value == 128):
                            self.win = True
            
            for c in range(NUM_COLS):
                for r in range(NUM_ROWS - 1, 0, -1):
                    if isinstance(self[r][c], Block) and not isinstance(self[r - 1][c], Block):
                        self[r - 1][c] = Block(r - 1, c, self[r][c].value)
                        self[r][c] = None
                        movement = True
            alldone = True
            for c in range(NUM_COLS):
                for r in range(NUM_ROWS - 1, 0, -1):
                    if isinstance(self[r][c], Block) and (self[r - 1][c] == None or self[r - 1][c].value==self[r][c].value):
                        alldone = False
                        break
        if movement:
            self.add_new_block()
    
    def move_down(self):    # method to move blocks down when down arrow key pressed
        movement = False    # local variable to check if any movement has happened
        alldone = False     # local variable to check if all blocks have moved
        while alldone == False:
            for c in range(NUM_COLS):
                for r in range(NUM_ROWS - 1, 0, -1):
                    if isinstance(self[r][c], Block) and isinstance(self[r - 1][c], Block):
                        if self[r - 1][c].value == self[r][c].value:
                            self[r][c].value *= 2
                            self[r - 1][c] = None
                            movement = True
                        elif (self[r - 1][c].value ==  128 and self[r][c].value == 12) or (self[r - 1][c].value ==  12 and self[r][c].value == 128):
                            self.win = True
            
            for c in range(NUM_COLS):
                for r in range(0, NUM_ROWS - 1, 1):
                    if isinstance(self[r][c], Block) and not isinstance(self[r + 1][c], Block):
                        self[r + 1][c] = Block(r + 1, c, self[r][c].value)
                        self[r][c] = None
                        movement = True
            alldone = True
            for c in range(NUM_COLS):
                for r in range(0, NUM_ROWS - 1, 1):
                    if isinstance(self[r][c], Block) and (self[r + 1][c] == None or self[r + 1][c].value==self[r][c].value):
                        alldone = False
                        break
        if movement:
            self.add_new_block()

    def check_128(self):    # method to check if the 128 tile has appeared 
        for r in range(NUM_ROWS):
            for c in range(NUM_COLS):
                if isinstance(self[r][c], Block) and self[r][c].value == 128:
                     self.cnt += 1
                     return True

    def game_over(self):    # method to check if game is over
        for r in range(NUM_ROWS):
            for c in range(NUM_COLS):
                if self[r][c] == None:
                    return False
        for r in range(NUM_ROWS):
            for c in range(NUM_COLS):
                if r + 1 < NUM_ROWS and ((self[r][c].value == self[r+1][c].value) or (self[r][c].value == 128 and self[r+1][c].value == 12) or (self[r][c].value == 12 and self[r+1][c].value == 128)): 
                    return False
                elif c + 1 < NUM_COLS and ((self[r][c].value == self[r][c+1].value) or (self[r][c].value == 128 and self[r][c+1].value== 12) or (self[r][c].value == 12 and self[r][c+1].value== 128)):
                    return False    
        return True


# MINI GAME 1

class Dino():
    def __init__(self, w, h, g):
        self.w = w
        self.h = h
        self.g = g
        self.vx = -7
        self.x_shift = 0
        self.score = 0
        
        self.start = True
        self.dead = False
        self.won = False
        
        self.suitcase = Suitcase(150, self.g - 105, 60, 105, 78)
        
        # locate enemies
        self.enemies = []
        for e in range(15):
            x = random.randint(0,1)
            if e >= 5 and x == 1:
                self.enemies.append(Plane(e*700 + self.w, self.g - 190, 50, 100))
            elif e < 5 or x == 0:    
                self.enemies.append(Palm(e*700 + self.w*2, self.g - 86, 86, 100))
        
        self.back = loadImage(path+"/images/dino/b1.png")
        self.backgrounds = []
        for b in range(2, 6):
            self.backgrounds.append(loadImage(path+"/images/dino/b"+str(b)+".png"))
            
        self.lost_img = loadImage(path+"/images/dino/lost.png")
        self.won_img = loadImage(path+"/images/dino/won.png")
        self.start_img = loadImage(path+"/images/dino/start.png")
        self.jump_snd = player.loadFile(path + "/sounds/dino/jump.mp3")
        self.dead_snd = player.loadFile(path + "/sounds/dino/dead.mp3")
        

    def display(self):
         # start menu with brief instructions
        if self.start:
            image(self.start_img, 0, 0)
        
        #end menu with game results
        elif self.won:
            image(self.won_img, 0, 0)
        elif self.dead:
            self.dead_snd.play()
            image(self.lost_img, 0, 0)
        
        #game display
        elif not self.dead:
            
            self.game_speed()
            image(self.back, 0, 0)
            
            # create parallax effect with background layers
            x = 0
            cnt = 2
            for b in self.backgrounds:
                if cnt == 2:
                    x = self.x_shift//5
                elif cnt == 3 or cnt == 4:
                    x = self.x_shift//2
                else:
                    x = self.x_shift
                w_r = int(x%self.w)
                w_l = self.w - w_r
                
                image(b, 0, 0, w_l, self.h, w_r, 0, self.w, self.h)
                image(b, w_l, 0, w_r, self.h, 0, 0, w_r, self.h)
                cnt += 1
                
            for e in self.enemies:
                e.display()
            
            # remove enemies once they are out of screen and past the suitcase    
            for e in self.enemies:
                if e.x + e.w < 0:
                    self.enemies.remove(e)
            
            self.suitcase.display()
            self.score += 1
            self.x_shift -= self.vx
    
    def game_speed(self):
        # increase the game speed accirding to the game score
        if self.score%1000 == 0 and self.score != 0:
            self.vx -= 1.5 

# class of the dino protagonist
class Suitcase():
    def __init__(self, x, y, w, h0, h1):
        self.x = x 
        self.y = y 
        self.h0 = h0
        self.h1 = h1
        self.h = h0
        self.w = w
        self.vy = 0
        self.jump = False
        self.duck = False
        self.img = loadImage(path+"/images/dino/suitcase.png")
    
    def display(self):
        self.update()
        if self.duck:
            image(self.img, self.x, self.y, self.w, self.h1, self.w, self.h0 - self.h1, self.w*2, self.h0)
        else:
            image(self.img, self.x, self.y, self.w, self.h0, 0, 0, self.w, self.h0)
    
    def update(self):
        # check for collision with enemies
        if len(game.dinogame.enemies) != 0:
            for e in game.dinogame.enemies:
                if e.x + e.w >= self.x and self.x + self.w >= e.x:
                    self.collision(e)
        # game is won if all enemies have been "dodged"
        else:
            game.dinogame.won = True
    
        # gravity effect when the suitcase in the air
        if self.y + self.h >= game.dinogame.g:
            self.y = game.dinogame.g - self.h 
            self.vy = 0
        else:
            self.vy += 1
            if self.y + self.h + self.vy > game.dinogame.g:
                self.vy = game.dinogame.g - (self.y + self.h)
        
        #jump and duck display changes
        if self.jump and self.y + self.h == game.dinogame.g:
            game.dinogame.jump_snd.rewind()
            game.dinogame.jump_snd.play()
            self.vy = -20
        elif self.duck and self.y + self.h == game.dinogame.g:
            self.vy = 0
            self.h = self.h1
            self.y = game.dinogame.g - self.h
        
        self.y += self.vy
    
    def collision(self, e):
        # check for collision 
        if isinstance(e, Palm) and self.y + self.h >= e.y:
            game.dinogame.dead = True
        elif isinstance(e, Plane) and self.x + 40 >= e.x + 30 and self.x + 20 < e.x + 70 and self.y <= e.y + e.h:
            game.dinogame.dead = True
  
# class of dino enemy
class Palm():
    def __init__(self, x, y, w, h): 
        self.x = x 
        self.y = y 
        self.w = w
        self.h = h
        self.img = loadImage(path+"/images/dino/palm.png")
        
    def display(self):
        #change x coordinates to create the suitcase rolling effect
        self.x += game.dinogame.vx
        image(self.img, self.x, self.y) 

# class of dino enemy
class Plane():
    def __init__(self, x, y, w, h):
        self.x = x 
        self.y = y 
        self.w = w
        self.h = h
        self.img = loadImage(path+"/images/dino/plane.png")
    
    def display(self):
        #change x coordinates to create the suitcase rolling effect
        self.x += game.dinogame.vx
        image(self.img, self.x, self.y)


# MINI GAME 3

# main class of the game "Get Work Done" (Gwd)
class Gwd():
    def __init__(self, w, h, g):
        self.w = w
        self.h = h
        self.g = g
        
        self.dead = False
        self.start = True
        self.won = False
       
        self.document = Document(WIDTH/2, 720, 25, self.g, "doc.png")
        
        self.num_p = 30
        self.platforms = []
        self.platforms.append(DocPlatforms(random.randint(300, 700), HEIGHT-100, 200, 20, "platform.png"))
        for p in range(self.num_p):
            if p%2 == 0:
                self.platforms.append(DocPlatforms(random.randint(275, 425), HEIGHT-p*275, 200, 20, "platform.png"))
            else:
                self.platforms.append(DocPlatforms(random.randint(575, 725), HEIGHT-p*275, 200, 20, "platform.png"))
        
        self.locate_enemies()
        
        self.background_img = loadImage(path + "/images/gwd/background.png")
        self.start_img = loadImage(path + "/images/gwd/start.png")
        self.won_img = loadImage(path + "/images/gwd/won.png")
        self.lost_img = loadImage(path + "/images/gwd/lost.png")
        self.won_snd = player.loadFile(path + "/sounds/gwd/won.mp3")
        self.lost_snd = player.loadFile(path + "/sounds/gwd/lost.mp3")
        self.kill_snd = player.loadFile(path + "/sounds/gwd/kill.mp3")
    
    # locate enemies on top of random platforms     
    def locate_enemies(self):
        
        self.enemies = []
        self.enemies_platforms = []
        
        for e in range(10):
            platform = random.randint(5, self.num_p - 4)
            while platform in self.enemies_platforms:
                platform = random.randint(5, self.num_p - 4)
            self.enemies_platforms.append(platform)
            self.enemies.append(DocEnemy(platform, 50, self.platforms))
    
    def display(self):
        image(self.background_img, 0, 0)
        
        # start menu with brief instructions with start button
        if self.start:
            image(self.start_img, 0, 0)
            
        # end screens each with exit button
        elif self.dead == True:
            self.dead_display()
            image(self.lost_img, 0, 0)
        elif len(self.enemies) == 0:
            self.won = True
            self.won_snd.play()
            image(self.won_img, 0, 0)
            
        # display during the game process
        else:
            self.document.display()
            
            for p in self.platforms:
                p.display()
            
            for e in self.enemies:
                e.display()
    
    def game_lost(self):
        image(self.lost_img, 0, 0)
    
    def game_won(self):
        image(self.won_img, 0, 0)
    
    def dead_display(self):
        self.lost_snd.play()
        image(self.document.img, self.document.x, self.document.y)
        self.document.vy += 0.02
        self.document.y += self.document.vy

# class of the protagonist (google doc)        
class Document():
    def __init__(self, x, y, r, g, img):
        self.x = x
        self.y = y
        self.r = 2*r
        self.g = g
        self.vy = 0
        self.vy = -10
        self.on_platform = False
        self.img = loadImage(path + "/images/gwd/" + img)
    
    def update(self):
        self.gravity()
        
        # move the protagonist in x-axis according to the mouse pointer location
        if mouseX >= WIDTH/2:
            self.vx = 5
        elif mouseX < WIDTH/2:
            self.vx = -5
        else:
            self.vx = 0
        
        self.x += self.vx
        self.y += self.vy
        
        # move all platforms and enemies when the protagonist jumps on a platform while it is above the middle
        if self.y <= 5*HEIGHT//8 and self.vy<=0:
            for e in game.gwd.enemies:
                e.y -= self.vy*2
            for p in game.gwd.platforms:
                p.y -= self.vy*2
        
        # remove enemies if the document jumps on them
        for e in game.gwd.enemies:
            if self.vy >= 0 and self.y + self.r >= e.y and self.y <= e.y and self.x + self.r >= e.x + 10 and self.x <= e.x + e.w - 10:
                game.gwd.kill_snd.rewind()
                game.gwd.kill_snd.play()
                game.gwd.enemies.remove(e)
                self.vy = -7
    
    def gravity(self):
        # "bounce back" from the ground(in the very beginning only) or keep falling 
        if not self.on_platform and self.y + self.r >= self.g:
            self.vy = -8
        elif self.on_platform and self.y + self.r >= self.g:
            game.gwd.dead = True
            game.gwd.document.y = 0
        else:
            self.vy += 0.2
        
        # "bounce back" from platforms to create the constant jumping effect
        for p in game.gwd.platforms: 
            if self.vy >= 0 and self.y + self.r >= p.y and self.y <= p.y + 1 and self.x + self.r >= p.x and self.x <= p.x + p.w:
                self.vy = -8
                self.on_platform = True
                break
    
    def display(self):
        self.update()
        image(self.img, self.x, self.y)

# class of antagonists         
class DocEnemy():
    def __init__(self, p, h, platforms):
        self.w = platforms[p].w - 10
        self.h = h
        self.y = platforms[p].y - self.h
        self.x = platforms[p].x + 5
        self.img = loadImage(path + "/images/gwd/enemy_" + str(random.randint(1, 3))+ ".png")
        
    def display(self):
        image(self.img, self.x, self.y, self.w, self.h)

# class of GWD platforms         
class DocPlatforms():
    def __init__(self, x, y, w, h, img):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.img = loadImage(path + "/images/gwd/" + img)
    
    def display(self):
        self.update()
        image(self.img, self.x, self.y, self.w, self.h)
    
    def update(self):
        if self.y >= HEIGHT:
            game.gwd.platforms.remove(self)

###

# initializing the game variable
game = Game(WIDTH, HEIGHT, 615)

def setup():
    size(WIDTH, HEIGHT)
    background(0)

def draw():
    
    # displaying appropriate start screen
    if game.hearts != 0:
        if game.currentscreen == "START":
            image(background_start, 0, 0)
        else:
            game.display()
    else:
        image(game_over, 0, 0)
    
    # saving data every 30s    
    if frameCount % 1800 == 0:
        game.savedata()
    
    # displaying appropriate texts and locked breakout rooms
    if game.currentscreen == "MAIN" and game.hearts != 0 and not game.mg2startscreen:
        textSize(10)
        fill(255)
        strokeWeight(0)
        if game.raisedhands < 5:
            text("LEVEL 2", 275, 83)
            fill(255, 80)
            rect(480, 670, 100, 45)
            rect(615, 670, 100, 45)
        elif game.raisedhands < 10:
            text("LEVEL 3", 275, 83)
            fill(255, 80)
            rect(615, 670, 100, 45)
            
def keyPressed():

    # changing key_handler variable when arrow keys pressed when on "MAIN" screen
    if game.currentscreen == "MAIN":
        if keyCode == LEFT:
            game.sprite.key_handler[LEFT] = True
        elif keyCode == RIGHT:
            game.sprite.key_handler[RIGHT] = True
        elif keyCode == UP:
            game.sprite.key_handler[UP] = True
        elif keyCode == DOWN:
            game.sprite.key_handler[DOWN] = True
    
    # changing key_handler variable when arrow keys pressed when on "MINIGAME2" screen
    if game.currentscreen == "MINIGAME2":
        if keyCode == LEFT:
            game.game2048.move_left()
        elif keyCode == RIGHT:
            game.game2048.move_right()
        elif keyCode == UP:
            game.game2048.move_up()
        elif keyCode == DOWN:
            game.game2048.move_down()
    
    # changing key_handler variable when arrow keys pressed when on "MINIGAME1" screen
    if game.currentscreen == "MINIGAME1":
        if keyCode == UP or keyCode == 32:
            game.dinogame.suitcase.jump = True
        elif keyCode == DOWN:
            game.dinogame.suitcase.duck = True        
    
def keyReleased():

    # changing key_handler variable when arrow keys released when on "MAIN" screen
    if game.currentscreen == "MAIN":
        if keyCode == LEFT:
            game.sprite.key_handler[LEFT] = False
        elif keyCode == RIGHT:
            game.sprite.key_handler[RIGHT] = False
        elif keyCode == UP:
            game.sprite.key_handler[UP] = False
        elif keyCode == DOWN:
            game.sprite.key_handler[DOWN] = False
    
    # changing key_handler variable when arrow keys released when on "MINIGAME1" screen
    if game.currentscreen == "MINIGAME1":
        if keyCode == UP or keyCode == 32:
            game.dinogame.suitcase.jump = False
        elif keyCode == DOWN:
            game.dinogame.suitcase.h = game.dinogame.suitcase.h0
            game.dinogame.suitcase.y = game.dinogame.g - game.dinogame.suitcase.h0
            game.dinogame.suitcase.duck = False
    
def mouseClicked():
    global game

    # deleting progress.csv file and reinitializing the game variable when game over
    if game.hearts == 0:
        os.remove("progress.csv")
        game = Game(WIDTH, HEIGHT, 615)

    # choosing sprite clicked on when on "START" screen
    elif  game.currentscreen == "START":
        if 250 <= mouseX <= 330 and 550 <= mouseY <= 720:
            game.choosesprite(2)
        elif 715 <= mouseX <= 780 and 550 <= mouseY <= 720:
            game.choosesprite(1)
    
    # saving data when button clicked
    elif game.currentscreen == "MAIN" and 891 <= mouseX <= 1003 and 9 <= mouseY <= 37:
        game.savedata()
    
    # restarting game when button clicked
    elif game.currentscreen == "MAIN" and 920 <= mouseX <= 1035 and 680 <= mouseY <= 710:
        try:
            os.remove("progress.csv")
        except:
            print("never saved")
        game = Game(WIDTH, HEIGHT, 615)

    # opening breakout room clicked on if enough raised hands collected
    elif game.currentscreen == "MAIN" and 670 <= mouseY <= 720 and 345 <= mouseX <= 715:
        if 345 <= mouseX <= 445:
            print("Breakout Room 1")
            game.currentscreen = "MINIGAME1"
        elif 480 <= mouseX <= 580 and game.raisedhands >= 5:
            print("Breakout Room 2")
            game.mg2startscreen = True
        elif 615 <= mouseX <= 715 and game.raisedhands >= 10:
            print("Breakout Room 3")
            game.currentscreen = "MINIGAME3"

    # starting mini game 2 if button clicked
    elif game.mg2startscreen and game.m2count >= 10 and (420 <= mouseX <= 620) and (465 <= mouseY <= 500):
        game.m2count -= 10
        game.currentscreen = "MINIGAME2"
        game.mg2startscreen = False

    # showing "MAIN" screen if start button not clicked
    elif game.mg2startscreen and not((420 <= mouseX <= 620) and (465 <= mouseY <= 500)):
        game.mg2startscreen = False
    
    # appropriately updating raised hands and hearts and going back to main screen after mini-game 2 over
    elif game.game2048.win or (game.game2048.game_over() and not game.game2048.win):
        if game.game2048.game_over() and not game.game2048.win:
            game.hearts -= 1
        if game.game2048.win:
            if game.hearts<3:
                game.hearts += 1
            game.raisedhands += 1
            if game.raisedhands == 5 or game.raisedhands == 10:
                levelup_snd.rewind()
                levelup_snd.play()
        game.game2048 = Game2048()
        game.currentscreen = "MAIN"
        game.backtomain()
    
    # starting mini game 1 if button clicked
    elif game.currentscreen == "MINIGAME1" and game.dinogame.start and mouseX >= 430 and mouseY >= 570 and mouseX <= 610 and mouseY <= 610 and game.m1count >= 10:
        game.m1count -= 10
        game.dinogame.start = False
    
    # showing "MAIN" screen if start button not clicked
    elif game.currentscreen == "MINIGAME1" and game.dinogame.start and not(mouseX >= 430 and mouseY >= 570 and mouseX <= 610 and mouseY <= 610):
        game.currentscreen = "MAIN"
    
    # appropriately updating raised hands and hearts and going back to main screen after mini-game 1 over    
    elif game.currentscreen == "MINIGAME1" and game.dinogame.dead or game.dinogame.won:
        if game.dinogame.dead:
            game.hearts -= 1
        if game.dinogame.won:
            if game.hearts <3:
                game.hearts += 1
            game.raisedhands += 1
            if game.raisedhands == 5 or game.raisedhands == 10:
                levelup_snd.rewind()
                levelup_snd.play()
        game.currentscreen = "MAIN"
        game.backtomain()
        game.dinogame = Dino(WIDTH, HEIGHT, 400)
    
    # starting mini game 3 if button clicked
    elif game.currentscreen == "MINIGAME3" and game.gwd.start and mouseX >= 430 and mouseY >= 570 and mouseX <= 610 and mouseY <= 610 and game.m3count >= 10:
        game.m3count -= 10
        game.gwd.start = False
    
    # showing "MAIN" screen if start button not clicked
    elif game.currentscreen == "MINIGAME3" and game.gwd.start and not(mouseX >= 430 and mouseY >= 570 and mouseX <= 610 and mouseY <= 610):
        game.currentscreen = "MAIN"
    
    # appropriately updating raised hands and hearts and going back to main screen after mini-game 3 over    
    elif game.currentscreen == "MINIGAME3" and game.gwd.dead or game.gwd.won:
        if game.gwd.dead:
            game.hearts -= 1
        if game.gwd.won:
            if game.hearts <3:
                game.hearts += 1
            game.raisedhands += 1
            if game.raisedhands == 5 or game.raisedhands == 10:
                levelup_snd.rewind()
                levelup_snd.play()
        game.currentscreen = "MAIN"
        game.backtomain()
        game.gwd = Gwd(WIDTH, HEIGHT, HEIGHT)
