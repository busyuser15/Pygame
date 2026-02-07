import pygame
import random
import sys

#Screen parameters
pygame.init()
pygame.font.init()
Game_Screen_height = 630
Game_Screen_width = 1200
hud_height = 100
hud_width = Game_Screen_width
hud= pygame.Rect(0,Game_Screen_height,hud_width,hud_height)
screen = pygame.display.set_mode((Game_Screen_width, Game_Screen_height + hud_height))
clock = pygame.time.Clock()
score = 0

#images
Background_image = pygame.image.load('Background.png').convert()
Background_image = pygame.transform.scale(Background_image, (Game_Screen_width, Game_Screen_height))

Bouncer_image = pygame.image.load('Bouncer.png')  # This is a Surface
Bouncer_image = pygame.transform.scale(Bouncer_image, (15, 15))

Slider_image = pygame.image.load('Slider.png')  # This is a Surface
Slider_image = pygame.transform.scale(Slider_image, (50, 50))

Shop_image = pygame.image.load('Shop.png')  # This is a Surface
Shop_image = pygame.transform.scale(Shop_image, (75, 75))

Player_image = pygame.image.load('Player.png')  # This is a Surface
Player_image = pygame.transform.scale(Player_image, (30, 30))

Hunter_image = pygame.image.load('Hunter.png')  # This is a Surface
Hunter_image = pygame.transform.scale(Hunter_image, (40, 40))

Key_image = pygame.image.load('Key.png')  # This is a Surface
Key_image = pygame.transform.scale(Key_image, (26, 26))

Money_image = pygame.image.load('Money.png')  # This is a Surface
Money_image = pygame.transform.scale(Money_image, (26, 26))

Wall_image = pygame.image.load('Wall.png')  # This is a Surface
Wall_image = pygame.transform.scale(Wall_image, (65, 60))

def play_again():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    pygame.display.flip()
    font = pygame.font.SysFont(None, 72)
    lines = [
        f"Game over – your score was: {score}",
        "",
        "Play again",
        "<---",
        "",
        "Quit",
        "--->"
    ]

  # CLEAR FIRST

    unans = True
    player1 = Player(screen.get_width() // 2, 500)
    while unans:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        screen.fill((200, 200, 200))
        y = screen.get_height() // 2 - 100
        for line in lines:
            text = font.render(line, True, (255, 0, 0))
            rect = text.get_rect(center=(screen.get_width() // 2, y - 100))
            screen.blit(text, rect)
            y += font.get_height() + 5
        player1.draw(screen)
        keys1 = pygame.key.get_pressed()
        if keys1[pygame.K_LEFT]:
            player1.rect.x -= 5
        if keys1[pygame.K_RIGHT]:
            player1.rect.x += 5
        if player1.rect.x < 0:
            Play_again = True
            unans = False
        if player1.rect.x >= Game_Screen_width - player1.size:
            Play_again = False
            unans = False
            pygame.quit()
        pygame.display.flip()
        clock.tick(60)
    return Play_again

    

    

def circle_rect_collide(circle_x, circle_y, radius, rect):
    # Find the closest point on the rectangle to the circle's center
    closest_x = max(rect.left, min(circle_x, rect.right))
    closest_y = max(rect.top, min(circle_y, rect.bottom))
    
    # Calculate the distance between the circle's center and this closest point
    distance_x = circle_x - closest_x
    distance_y = circle_y - closest_y
    return (distance_x ** 2 + distance_y ** 2) <= (radius ** 2)


def circles_collide(x1, y1, r1, x2, y2, r2):
    distance = math.hypot(x2 - x1, y2 - y1)
    return distance <= (r1 + r2)

class Player:
    def __init__(self,x,y, size = 30,invis = False):
        self.size = size
        self.invis = invis
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, size, size)
        self.color = (0, 0, 255)
        self.speed = 5
        self.lives = 3
        self.money = 0
        self.dash = False
        self.dashCooldown = 0
        self.dashDelay = 5000

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        screen.blit(Player_image, self.rect.topleft)

    def colliderect(self, rectang):
        return self.rect.colliderect(rectang)

class Hunter:
    size = 40
    def __init__(self,x,y):
        self.size = 40
        w = self.size
        h = self.size
        self.rect = pygame.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.color = (0, 0, 0)
        self.speed = 2
        self.age = 0

    def chase(self, player):
        dx = player.rect.x - self.rect.x
        if dx >= 0: # player is further right than hunter
            dx = min(self.speed,dx)
        else: # player is left of the hunter
            dx = max(-1*self.speed,dx)
        dy = player.rect.y - self.rect.y
        if dy >= 0: # player is below the hunter
            dy = min(self.speed,dy)
        else: # player is above the hunter
            dy = max(self.speed * -1,dy)
        self.rect.x = self.rect.x + dx
        self.rect.y = self.rect.y + dy



    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        screen.blit(Hunter_image, self.rect.topleft)

    def colliderect(self, rectang):
        return self.rect.colliderect(rectang)


class Bouncer:
    size = 15
    def __init__(self,x,y, size = 15):
        self.size = size
        self.rect = pygame.Rect(x, y, size, size)
        self.x = x
        self.y = y
        self.color = (255, 165, 0)
        self.speed = 4
        right = random.choice([-1000,1000])
        self.right=(random.randrange(800,1200)/right)
        up = random.choice([-1000,1000])
        self.up=(random.randrange(800,1200)/up)

    def move(self):
        self.rect.x += (self.speed * self.right)
        self.rect.y += (self.speed * self.up)
        

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        screen.blit(Bouncer_image, self.rect.topleft)
    def colliderect(self, rectang):
        return

class Base:
    def __init__(self,x,y,red, green, blue, size = 35):
        self.size = size
        self.rect = pygame.Rect(x, y, size, size)
        self.color = (red , green, blue )
        self.speed = 5

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

class Stall(Base):
    def __init__(self,x,y,price,text, red = 150 , green= 75, blue = 0, size = 75):
        super().__init__( x, y,red,green,blue)
        self.bought = False
        self.activate = None
        self.available = True
        self.price = 0
        self.size = size
        self.rect = pygame.Rect(x, y, size, size)
        self.text= text

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        screen.blit(Shop_image, self.rect.topleft)
    

class Wall:
    def __init__(self, Game_Screen_width, Game_Screen_height, min_w=40, max_w=120, min_h=20, max_h=60):
        self.width = random.randint(min_w, max_w)
        self.height = random.randint(min_h, max_h)
        self.x = random.randint(0, Game_Screen_width - self.width)
        self.y = random.randint(0, Game_Screen_height - self.height)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.color = (255, 255, 0)  # Yellow by default
        
    def colliderect(self, rectang):
        return self.rect.colliderect(rectang)
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

class Wall_Matrix:
    def __init__(self, Wall_height, Wall_width, Wall_x,Wall_y):
        self.width = Wall_width
        self.height = Wall_height
        self.x = Wall_x
        self.y = Wall_y
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.color = (255, 255, 0)  # Yellow by default
        
    def colliderect(self, rectang):
        return self.rect.colliderect(rectang)
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        screen.blit(Wall_image, self.rect.topleft)



class Orb:
    radius = 15
    def __init__(self, x, y):
        self.radius = 15
        self.colour = (100,100,100)
        self.x = x
        self.y = y
        self.pos = (x,y)
    def collideCircRect(self, rectang):
        closest_x = max(rectang.x, min(self.x, rectang.x + rectang.size))
        closest_y = max(rectang.y, min(self.y, rectang.y + rectang.size))
        distance_x = self.x - closest_x
        distance_y = self.y - closest_y
        return (distance_x ** 2 + distance_y ** 2) <= (self.radius ** 2)

    def draw(self, surface):
        pygame.draw.circle(surface, self.colour, self.pos,self.radius)
        screen.blit(Key_image, ((self.x - self.radius + 1), (self.y - self.radius + 1)))


class Money_Orb(Orb):
    def __init__(self, x, y):
        super().__init__( x, y)
        self.speed = 2
        self.radius = 12
        self.colour = (100,100,100)
    def move(self):
        self.y = self.y + self.speed
        self.pos = (self.x,self.y)
    def delete(self):
        if self.y > Game_Screen_width:
            self.pos = (None,None)
    def draw(self, surface):
        pygame.draw.circle(surface, self.colour, self.pos,self.radius)
        screen.blit(Money_image, ((self.x - self.radius + 1), (self.y - self.radius + 1)))

        
        

class Slider:
    size = 50
    def __init__(self,x,y, size = 50):
        self.size = size
        self.rect = pygame.Rect(x, y, size, size)
        self.x = x
        self.y = y
        self.color = (255, 255, 255)
        self.right = random.choice([-1,1])
        self.speed = random.randint(4,8)

    def move(self):
        self.rect.x += (self.speed * self.right)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        screen.blit(Slider_image, self.rect.topleft)
    def colliderect(self, rectang):
        return self.rect.colliderect(rectang)

class Shop:
    def __init__(self):
        self.w = Game_Screen_width
        self.h = Game_Screen_height
    def draw(self):
        screen.fill((100, 100, 100))
        screen.fill((200,40,100),hud, 8)
        screen.blit(Background_image, (0, 0))
        self.Home.draw(screen)
        self.End.draw(screen)
        for stall in self.stalls:
            stall.draw(screen)
        arena_current.player.draw(screen)
        font = pygame.font.SysFont(None, 75)
        line = "Shop"

        textholder = font.render(line, True, (255, 255, 255))  # Only render once!
        screen.blit(textholder, (Game_Screen_width//2,100))  # Use (x, y) position for each line

        font = pygame.font.SysFont(None, 32)
        lines = [
            f"round: {arena_current.difficulty}",
            f"lives: {arena_current.player.lives}",
            f"money: {arena_current.player.money}"
        ]

        y = Game_Screen_height + 10
        for line in lines:
            textholder = font.render(line, True, (255, 255, 255))  # Only render once!
            screen.blit(textholder, (hud.left + 10, y))  # Use (x, y) position for each line
            y += font.get_height() + 5
        
        
        
    def generate(self):
        self.stalls = []
        self.Home = Base(Game_Screen_width //2, Game_Screen_height //2,0, 200, 0)
        self.End = Base(Game_Screen_width //2, Game_Screen_height - (Game_Screen_height //15),200, 0, 0)
        self.LivesUp = Stall(30, (Game_Screen_height //4),3,"LivesUp - 3 gold")
        self.Invis = Stall(30, (Game_Screen_height //4) * 2,8,"Wall Phase - 8 gold")
        self.SpeedUp = Stall(30, (Game_Screen_height //4) * 3,2,"Speed boost - 2 gold")
        self.Dash = Stall(Game_Screen_width - 110, (Game_Screen_height //4) * 2,5,"Dash - 5 gold")
        self.stalls.append(self.LivesUp)
        self.stalls.append(self.Invis)
        self.stalls.append(self.SpeedUp)
        self.stalls.append(self.Dash)

        for stall in self.stalls:
            stall.IntTime = 0
            stall.Newtime = 0
            stall.curTime = 0

        player_Start_x = (Game_Screen_width //2)+ (self.Home.size //4)
        player_Start_y = (Game_Screen_height //2)+(self.Home.size //4)
        arena_current.player.rect.x, arena_current.player.rect.y = player_Start_x,player_Start_y

        
    def update_hud(self):
        font = pygame.font.SysFont(None, 32)
        lines = [
            f"round: {arena_current.difficulty}",
            f"lives: {arena_current.player.lives}",
            f"money: {arena_current.player.money}"
        ]

        y = Game_Screen_height + 10
        for line in lines:
            textholder = font.render(line, True, (255, 255, 255))  # Only render once!
            screen.blit(textholder, (hud.left + 10, y))  # Use (x, y) position for each line
            y += font.get_height() + 5
        
    def playerLims(self,old_x,old_y):
        if arena_current.player.rect.x < 0:
            arena_current.player.rect.x = old_x
        if arena_current.player.rect.x >= Game_Screen_width - arena_current.player.size:
            arena_current.player.rect.x = old_x
        if arena_current.player.rect.y < 0:
            arena_current.player.rect.y = old_y
        if arena_current.player.rect.y >= Game_Screen_height - (arena_current.player.size):
            arena_current.player.rect.y = old_y

    
    def update(self):
        
        old_x, old_y = arena_current.player.rect.x, arena_current.player.rect.y
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            arena_current.player.rect.x -= arena_current.player.speed
        if keys[pygame.K_RIGHT]:
            arena_current.player.rect.x += arena_current.player.speed
        if keys[pygame.K_UP]:
            arena_current.player.rect.y -= arena_current.player.speed
        if keys[pygame.K_DOWN]:
            arena_current.player.rect.y += arena_current.player.speed
        self.playerLims(old_x,old_y)
        for stall in self.stalls:
            if arena_current.player.colliderect(stall):
                stall.curTime = pygame.time.get_ticks()
                if stall.IntTime == 0:
                    stall.IntTime = pygame.time.get_ticks()
            else:
                stall.IntTime = 0
                stall.Newtime = 0
                stall.curTime = 0
             
            if stall.curTime - 2000 > stall.IntTime and stall.IntTime != 0:
                    stall.bought = True
                    print(f"bought {stall}")
                    stall.IntTime = 0
                    stall.Newtime = 0
                    stall.curTime = 0
                    print(self.LivesUp.bought)
        #for stall in self.stalls:
        #    if stall.bought and arena_current.player.money >= stall.price:
        #        stall.activate()
        #        stall.bought = False
        #        arena_current.player.money -= stall.price
                
        if self.LivesUp.bought and arena_current.player.money >= 3:
            arena_current.player.lives += 1
            self.LivesUp.bought = False
            arena_current.player.money -= 3
        
        if self.SpeedUp.bought and arena_current.player.money >= 2 and arena_current.player.speed < 8:
            arena_current.player.speed += 1
            self.SpeedUp.bought = False
            arena_current.player.money -= 2

        if self.Invis.bought and arena_current.player.money >= 8 and not arena_current.player.invis:
            arena_current.player.invis = True
            self.Invis.bought = False
            arena_current.player.money -= 8

        if self.Dash.bought and arena_current.player.money >= 5 and arena_current.player.dashDelay > 1000:
            if arena_current.player.dash == False:
                arena_current.player.dash = True
            else:
                arena_current.player.dashDelay -= 1000
            self.Dash.bought = False
            arena_current.player.money -= 5
            
        self.update_hud()
        if arena_current.player.colliderect(self.End):
            EndTime = pygame.time.get_ticks()
            while (EndTime + 500)> pygame.time.get_ticks():
                print(arena_current.player.money)
            return True
        else:
            return False
            

#top moves down avoid the top

#hunter in fog of war

#maze with lava flowing down

    

        
class Arena:
    def __init__(self,difficulty):
        self.difficulty = difficulty
        self.w = Game_Screen_width
        self.h = Game_Screen_height
        self.huntersList = []
        self.bouncersList = []
        self.slidersList = []
        self.keyPress = False
        self.unlocked = False
        self.immune = False
        self.ranTick = False
        self.moneyStop = False
        self.Passed = True
        self.dashCoolDown = 0
        
    def playerLims(self,old_x,old_y):
        if self.player.rect.x < 0:
            self.player.rect.x = old_x
        if self.player.rect.x >= Game_Screen_width - self.player.size:
            self.player.rect.x = old_x
        if self.player.rect.y < 0:
            self.player.rect.y = old_y
        if self.player.rect.y >= Game_Screen_height - self.player.size:
            self.player.rect.y = old_y
    

  
    def Generate_key(self):
        self.key = Orb(None,None)
        while self.key.pos == (None,None):
            collision = False
            self.key = Orb(random.randint(0 + Orb.radius, Game_Screen_width - Orb.radius), random.randint(Orb.radius, Game_Screen_height - Orb.radius))
            for wall in self.walls:
                if circle_rect_collide(self.key.x, self.key.y, self.key.radius, wall.rect):
                    collision = True
            if circle_rect_collide(self.key.x, self.key.y, self.key.radius, self.player.rect):
                collision = True 
            if circle_rect_collide(self.key.x, self.key.y, self.key.radius, self.End.rect):
                collision = True
            if circle_rect_collide(self.key.x, self.key.y, self.key.radius, self.Home.rect):
                collision = True
            if collision == True:
                self.key = Orb(None, None)

    def update_hud(self):
        font = pygame.font.SysFont(None, 32)
        lines = [
            f"round: {self.difficulty}",
            f"lives: {self.player.lives}",
            f"money: {self.player.money}"
        ]

        y = Game_Screen_height + 10
        for line in lines:
            textholder = font.render(line, True, (255, 255, 255))  # Only render once!
            screen.blit(textholder, (hud.left + 10, y))  # Use (x, y) position for each line
            y += font.get_height() + 5
            #hud.blit(some_icon, (10, 10))


                


    def generate_walls(self):
        #use matrix for more structure
        wall_width = Game_Screen_width//20
        wall_height = Game_Screen_height//10
        grid = ([])
        for i in range(10):
            grid.append([])
            for j in range(20):
                wall_choice = random.choice([0,1,0,0,0,0,0,0,0,0,0])
                grid[i].append(wall_choice)
        walls = []
        for i in range(2,9):
            for j in range(20):
                if grid[i][j] == 1:
                    wall = Wall_Matrix(wall_width, wall_height,wall_width * j,wall_height * i) 
                    walls.append(wall)
        return walls
       

    
    def generate(self):
        
      
        #creating home and end bases
        self.Home = Base(Game_Screen_width //2, Game_Screen_height //15,0, 200, 0)
        self.End = Base(Game_Screen_width //2, Game_Screen_height - (Game_Screen_height //15),200, 0, 0)

        #creating player
        player_Start_x = (Game_Screen_width //2)+ (self.Home.size //4)
        player_Start_y = (Game_Screen_height //15)+(self.Home.size //4)
        #initlise player
        if self.difficulty == 0:
            self.player = Player(player_Start_x,player_Start_y)
        #only reset the player position to keep attributes
        self.player.rect.x,self.player.rect.y = player_Start_x,player_Start_y

        #generate walls
        self.walls = self.generate_walls()

        #Generate key
        self.Generate_key()
        
        #based on difficulty create sliders/bouncers/hunters
        if self.difficulty > 0 and self.passed == True:
            if self.difficulty % 4 == 0 or self.difficulty % 5 == 0:
                hunter = Hunter(random.randint(0,Game_Screen_width),random.randint(Game_Screen_height//2,Game_Screen_height - Hunter.size))
                self.huntersList.append(hunter)
            if self.difficulty % 2 == 0 and self.difficulty != 4:
                for _ in range(2):
                    bouncer = Bouncer(random.randint(0,Game_Screen_width),random.randint(Game_Screen_height//2,Game_Screen_height - Bouncer.size))
                    self.bouncersList.append(bouncer)
            if self.difficulty % 3 == 0 or self.difficulty == 1:
                slider = Slider(random.randint(0,Game_Screen_width),random.randint(Game_Screen_height//4,Game_Screen_height - Slider.size))
                self.slidersList.append(slider)


    def playerLims(self,old_x,old_y):
        if self.player.rect.x < 0:
            self.player.rect.x = old_x
        if self.player.rect.x >= Game_Screen_width - self.player.size:
            self.player.rect.x = old_x
        if self.player.rect.y < 0:
            self.player.rect.y = old_y
        if self.player.rect.y >= Game_Screen_height - self.player.size:
            self.player.rect.y = old_y

    def Bouncer_lims(self,bouncer_x_list,bouncer_y_list):
        for i in range(len(self.bouncersList)):
            bouncer = self.bouncersList[i]
            if bouncer.rect.x < 0:
                bouncer.right *= -1
                bouncer.rect.x = bouncer_x_list[i]
            if bouncer.rect.x >= Game_Screen_width:
                bouncer.right *= -1
                bouncer.rect.x = bouncer_x_list[i]
        for i in range(len(self.bouncersList)):
            bouncer = self.bouncersList[i]
            if bouncer.rect.y < 0:
                bouncer.up *= -1
                bouncer.rect.y = bouncer_y_list[i]
            if bouncer.rect.y >= Game_Screen_height - bouncer.size:
                bouncer.up *= -1
                bouncer.rect.y = bouncer_y_list[i]
  
    def Slider_lims(self,old_x_Slider_List):
        for i in range(len(self.slidersList)):
            slider = self.slidersList[i]
            if slider.rect.x < 0:
                slider.right *= -1
                slider.rect.x = old_x_Slider_List[i]
            if slider.rect.x >= Game_Screen_width - 1:
                slider.right *= -1
                slider.rect.x = old_x_Slider_List[i]

        
    def draw(self):
        #initilise screen
        screen.fill((100, 100, 100))
        screen.fill((200,40,100),hud, 8)
        screen.blit(Background_image, (0, 0))
        makemoney = False
        if random.randint(0,100) == 100 and self.ranTick == False and self.keyPress:
            self.ranTick = True
            makemoney = True
        if  makemoney:
            self.money = Money_Orb(random.randint(0, Game_Screen_width), 10 )
        if self.ranTick == True:
            if self.moneyStop == False and self.money.y < Game_Screen_width -1:
                self.money.draw(screen)
                self.money.delete()
        
        self.Home.draw(screen)
        if self.unlocked:
            self.End.draw(screen)
        for wall in self.walls:
            wall.draw(screen)
        self.player.draw(screen)

        for hunter in self.huntersList:
            hunter.draw(screen)
        for slider in self.slidersList:
            slider.draw(screen)
        for bouncer in self.bouncersList:
            bouncer.draw(screen)
        if self.key.pos != (None,None):
            self.key.draw(screen)
    def new_round(self):
        self.keyPress = False
        self.unlocked = False
        self.immune = False
        self.ranTick = False
        self.moneyStop = False
        for hunter in self.huntersList:
            hunter.rect.x = random.randint(0,Game_Screen_width)
            hunter.rect.y = random.randint(Game_Screen_height//2,Game_Screen_height)
            if hunter.speed < 3:
                hunter.speed += 0.1
        for bouncer in self.bouncersList:
            bouncer.rect.y = random.randint(Game_Screen_height//2,Game_Screen_height - Bouncer.size)
            bouncer.rect.x = random.randint(0,Game_Screen_width)

    def Player_hit(self):
            self.passed = False
            self.hit = False
            self.new_round()
            self.player.lives -= 1
            if self.player.lives == 0:
                return False
            else:
                EndTime = pygame.time.get_ticks()
                while (EndTime + 500)> pygame.time.get_ticks():
                    print(self.player.money)
                return True
                

    def update(self):
        self.update_hud()
        hit = False
        lagtime = False
        bouncer_x_list = []
        bouncer_y_list = []

        if self.ranTick:
            if self.moneyStop == False and self.keyPress == True:
                self.money.move()
                self.money.delete()
            if circle_rect_collide(self.money.x, self.money.y, self.money.radius, self.player.rect):
                self.player.money += (self.difficulty + 5)//5
                self.moneyStop = True
                self.money.y = Game_Screen_width *2
        
        for bouncer in self.bouncersList:
            old_x_bouncer = bouncer.rect.x
            bouncer_x_list.append(old_x_bouncer)
        for bouncer in self.bouncersList:
            old_y_bouncer = bouncer.rect.y
            bouncer_y_list.append(old_y_bouncer)

        old_x_Slider_List = []
        for i in range(len(self.slidersList)):
            slider = self.slidersList[i]
            old_x_Slider = slider.rect.x
            old_x_Slider_List.append(old_x_Slider)
            
        old_x, old_y = self.player.rect.x, self.player.rect.y
        
                       
        if lagtime == False:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.keyPress = True
                if keys[pygame.K_SPACE] and self.player.dash and self.player.dashCooldown <= 0:
                    self.player.rect.x -= self.player.speed*20
                    self.player.Time_Used = pygame.time.get_ticks()
                    self.player.dashCooldown = -pygame.time.get_ticks() + (self.player.Time_Used + self.player.dashDelay)
                else:
                    self.player.rect.x -= self.player.speed
            if keys[pygame.K_RIGHT]:
                self.keyPress = True
                if keys[pygame.K_SPACE] and self.player.dash and self.player.dashCooldown <= 0:
                    self.player.rect.x += self.player.speed*20
                    self.player.Time_Used = pygame.time.get_ticks()
                    self.player.dashCooldown = -pygame.time.get_ticks() + (self.player.Time_Used+self.player.dashDelay)
                else:
                    self.player.rect.x += self.player.speed
            if self.player.dashCooldown > 0:
                    self.player.dashCooldown = -pygame.time.get_ticks() + (self.player.Time_Used + self.player.dashDelay)

        #creating boundaryies for walls x-axis
        for wall in self.walls:
            if self.player.colliderect(wall) and self.player.invis == False:
                self.player.rect.x = old_x  # Undo horizontal movement
                break
        if lagtime == False:
            #movement for player y-axis
            if keys[pygame.K_UP]:
                self.keyPress = True
                if keys[pygame.K_SPACE] and self.player.dash and self.player.dashCooldown <= 0:
                    self.player.rect.y -= self.player.speed*20
                    self.player.Time_Used = pygame.time.get_ticks()
                    self.player.dashCooldown = -pygame.time.get_ticks() + (self.player.Time_Used + self.player.dashDelay)

                else:
                    self.player.rect.y -= self.player.speed
            if keys[pygame.K_DOWN]:
                self.keyPress = True
                if keys[pygame.K_SPACE] and self.player.dash and self.player.dashCooldown <= 0:
                    self.player.rect.y += self.player.speed*20
                    self.player.Time_Used = pygame.time.get_ticks()
                    self.player.dashCooldown = -pygame.time.get_ticks() + (self.player.Time_Used + self.player.dashDelay)
                else:
                    self.player.rect.y += self.player.speed


            
        #creating boundaryies for walls y-axis
        for wall in self.walls:
            if self.player.colliderect(wall) and self.player.invis == False:
                self.player.rect.y = old_y  # Undo horizontal movement
                break

        #HUNTER MOVEMENT
        for hunter1 in self.huntersList:
            if self.keyPress == True:
                hunter1.chase(self.player)
            
        #Slider Movement
        for slider in self.slidersList:
            slider.move()

        #bouncer movement
        if self.keyPress == True:
            for bouncer in self.bouncersList:
                bouncer.move()

        for hunter1 in self.huntersList:
            if self.player.colliderect(hunter1):
                hit = True
        for slider in self.slidersList:
            if self.player.colliderect(slider):
                hit = True
        for bouncer in self.bouncersList:
            if self.player.colliderect(bouncer):
                hit = True

        if hit:
            if self.Player_hit():
                self.draw()
                return 0
            else:
                return -1
            

        ########
        #LIMITS#
        ########

        #outer player limits
        self.playerLims(old_x,old_y)
        self.Bouncer_lims(bouncer_x_list,bouncer_y_list)
        self.Slider_lims(old_x_Slider_List)

        #if key is picked up
        if circle_rect_collide(self.key.x, self.key.y, self.key.radius, self.player.rect):
            self.unlocked = True
            self.key.pos = (None, None)

        #if player makes it to the exit
        if self.player.colliderect(self.End) and self.unlocked == True:
            EndTime = pygame.time.get_ticks()
            self.immune = True
            self.difficulty += 1
            self.passed = True
            self.new_round()
            while (EndTime + 500)> pygame.time.get_ticks():
                print(self.player.money)
            return 1
class Maze():
    def __init__(self):
        pi = 3.14
    def generate_walls(self):
        wall_width = Game_Screen_width//20
        wall_height = Game_Screen_height//14
        grid = ([])
        for i in range(100):
            grid.append([])
            for j in range(20):
                wall_choice = 1
                grid[i].append(wall_choice)
            while sum(grid[i]) == 20:
                for j in range(3,17):
                    grid[i][j] = not(random.randint(0,20) == 1)
                    
        walls = []
        for i in range(5,99,2):
            for j in range(20):
                if grid[i][j] == 1:
                    wall = Wall_Matrix(wall_height, wall_width,wall_width * j,wall_height * i) 
                    wall.wall_speed = 1
                    walls.append(wall)
        return walls
    def update_hud(self):
        font = pygame.font.SysFont(None, 32)
        lines = [
            f"round: {self.difficulty}",
            f"lives: {self.player.lives}",
            f"money: {self.player.money}"
        ]
    def playerLims(self,old_x,old_y):
        if arena_current.player.rect.x < 0:
            arena_current.player.rect.x = old_x
        if arena_current.player.rect.x >= Game_Screen_width - arena_current.player.size:
            arena_current.player.rect.x = old_x
        if arena_current.player.rect.y < 0:
            arena_current.player.rect.y = old_y
        if arena_current.player.rect.y >= Game_Screen_height - arena_current.player.size:
            arena_current.player.rect.y = old_y
            

    def draw(self):
        #initilise screen
        screen.fill((100, 100, 100))
        screen.fill((200,40,100),hud, 8)
        screen.blit(Background_image, (0, 0))
        self.Home.draw(screen)
        self.End.draw(screen)
        for wall in self.walls:
            wall.draw(screen)
        arena_current.player.draw(screen)


    def Generate(self):
        arena_current.keyPress = False
        self.Home = Base(Game_Screen_width //2, Game_Screen_height //15,0, 200, 0)
        self.End = Base(Game_Screen_width //2, Game_Screen_height - (Game_Screen_height //15),200, 0, 0)
        player_Start_x = (Game_Screen_width //2)+ (self.Home.size //4)
        player_Start_y = (Game_Screen_height //15)+(self.Home.size //4)
        arena_current.player.rect.x, arena_current.player.rect.y = 100,100#player_Start_x,player_Start_y
        self.walls = self.generate_walls()
        
    def update_walls(self):
        
        for wall in self.walls:
            wall.rect.y -=wall.wall_speed
            if arena_current.player.colliderect(wall.rect) and arena_current.player.invis == False:
                arena_current.player.rect.y -= wall.wall_speed  # Undo horizontal movement
        for wall in self.walls:
            if wall .rect.y < -10:
                self.walls.remove(wall)
                
    def update(self):
        print(arena_current.keyPress)
        if arena_current.keyPress == True:
            self.update_walls()
        old_y = arena_current.player.rect.y
        keys1 = pygame.key.get_pressed()

        #movement for player y-axis
        if keys1[pygame.K_UP]:
            arena_current.keyPress = True
            arena_current.player.rect.y -= arena_current.player.speed

        if keys1[pygame.K_DOWN]:
            arena_current.keyPress = True
            arena_current.player.rect.y += arena_current.player.speed

        #print("end of movement y", arena_current.player.rect.y)

        for wall in self.walls:
            if arena_current.player.colliderect(wall.rect):
                arena_current.player.rect.y = old_y  # Undo horizontal movement
                break
        old_x = arena_current.player.rect.x
        #print("old x", old_x)

        


        
        if keys1[pygame.K_LEFT]:
            arena_current.keyPress = True
            if keys1[pygame.K_SPACE] and arena_current.player.dash and arena_current.player.dashCooldown <= 0:
                arena_current.player.rect.x -= arena_current.player.speed*20
                arena_current.player.Time_Used = pygame.time.get_ticks()
                arena_current.player.dashCooldown = -pygame.time.get_ticks() + (arena_current.player.Time_Used + arena_current.player.dashDelay)
            else:
                arena_current.player.rect.x -= arena_current.player.speed

        if keys1[pygame.K_RIGHT]:
            arena_current.keyPress = True
            if keys1[pygame.K_SPACE] and arena_current.player.dash and arena_current.player.dashCooldown <= 0:
                arena_current.player.rect.x += arena_current.player.speed*20
                arena_current.player.Time_Used = pygame.time.get_ticks()
                arena_current.player.dashCooldown = -pygame.time.get_ticks() + (arena_current.player.Time_Used+arena_current.player.dashDelay)
            else:
                arena_current.player.rect.x += arena_current.player.speed
        
        
        #print("end of movement x", arena_current.player.rect.x)
        
                    
        if arena_current.player.dashCooldown > 0:
                arena_current.player.dashCooldown = -pygame.time.get_ticks() + (arena_current.player.Time_Used + arena_current.player.dashDelay)

        for wall in self.walls:
            if arena_current.player.colliderect(wall.rect) and arena_current.player.invis == False:
                arena_current.player.rect.x = old_x  # Undo horizontal movement


        if arena_current.player.rect.y < 0:
            arena_current.player.lives -=1
            if  arena_current.player.lives == 0:
                return -1
            else:
                return 0
            
        if arena_current.player.colliderect(self.End):
            print(9)
            return 1
            
        #creating boundaryies for walls y-axis
        
                
        self.playerLims(old_x,old_y)
        #print("after lims y", arena_current.player.rect.y)



init = True
arena_current = Arena(0)
score = 0
passed = False

while init == True:
    arena_current.generate()
    maze = Maze()


    shop = Shop()
    running = True
    
    if score % 3 == 0 and score != 0 and passed == 1:
        shop.generate()
        shopIn = True
        arena_current.player.money +=1
        while shopIn:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
            shop.draw()
            finished = shop.update()
            if finished:
                shopIn = False
                player_Start_x = (Game_Screen_width //2)+ (shop.Home.size //4)
                player_Start_y = (Game_Screen_height //15)+(shop.Home.size //4)
                arena_current.player.rect.x = player_Start_x
                arena_current.player.rect.y = player_Start_y
                
            pygame.display.flip()
            clock.tick(60)

    
    
    #if score mod 10 start mini boss
    
    while running:
        if score % 5 == 0 and score !=0:
            maze.Generate()
            maze_running = True
            while maze_running == True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        pygame.quit()
                maze.draw()
                maze_pass = maze.update()
                if maze_pass == 0:
                    maze.Generate()
                elif maze_pass == 1:
                    score += 1
                    maze_running = False
                    running = False
                elif maze_pass == -1:
                    running = False
                    maze_running = False
                    P_A = play_again()
                    if P_A:
                        arena_current = Arena(0)
                        score = 0
                        init = True
                pygame.display.flip()
                clock.tick(60)
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
            
            #arena_current.draw()
            arena_current.draw()
            passed = arena_current.update()
            if passed == 1:
                running = False
                score += 1
            elif passed == -1:
                init = False
                running = False
                P_A = play_again()
                if P_A:
                    arena_current = Arena(0)
                    score = 0
                    init = True
            elif passed == 0:
                running = False
            pygame.display.flip()

            clock.tick(50)

