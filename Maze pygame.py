#Random maze generator game

import pygame
from mazelib import Maze
from mazelib.generate.Prims import Prims
import random


pygame.init()
Screen_height = 700
Screen_width = 700
screen = pygame.display.set_mode((Screen_width, Screen_height))
clock = pygame.time.Clock()
score = 0

class Player:
    def __init__(self,x,y, size = 20):
        self.size = size
        self.rect = pygame.Rect(x, y, size, size)
        self.color = (0, 0, 255)
        self.speed = 5

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
    def colliderect(self, rectang):
        return self.rect.colliderect(rectang)

class Base:
    def __init__(self,x,y,red, green, blue, size = 35):
        self.size = size
        self.rect = pygame.Rect(x, y, size, size)
        self.color = (red , green, blue )
        self.speed = 5

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

class Wall:
    def __init__(self, wall_width, wall_height, wall_x, wall_y):
        self.wall_width = wall_width
        self.wall_height = wall_height
        self.wall_x = wall_x
        self.wall_y = wall_y
        self.rect = pygame.Rect(self.wall_x, self.wall_y, self.wall_width, self.wall_height)
        self.color = (255, 255, 0)  # Yellow by default
    def colliderect(self, rectang):
        return self.rect.colliderect(rectang)
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

init = True        
while init:
    #inityilaise maze grid
    rows = random.randrange(4, 13, 2)
    cols = random.randrange(4, 13, 2)
    m = Maze()
    m.generator = Prims(rows, cols)
    m.generate()

    print(m)

    grid_rows = len(m.grid)
    grid_cols = len(m.grid[0])  
    cell_width = Screen_width // (grid_cols )

    posN = []

    for i in range (grid_cols -1):
        print (grid_cols ,"cols")
        print (grid_rows, "rows")
        if m.grid[1][i] == 0:
            posN.append(i)
    m.grid[0][posN[random.randint(0,len(posN)-1)]] = 0 #starting position

    posN = []
    for i in range (grid_cols):
        print(i)
        print (grid_cols ,"cols")
        print (grid_rows, "rows")
        
        if m.grid[grid_rows - 2][i] == 0:
            posN.append(i)
    print(posN)
    m.grid[grid_rows-1][posN[random.randint(0,len(posN)-1)]] = 0 #end position


    cell_height = Screen_height // (grid_rows + (grid_rows // 4))
    maze_height = cell_height * grid_rows
    top_margin = (Screen_height - maze_height) // 2
    maze_bottom_y = top_margin + maze_height
    space_below = Screen_height - maze_bottom_y
    center_x = Screen_width // 2
    center_y_above_maze = top_margin // 2
    center_y_below_maze = maze_bottom_y + (space_below // 2)

    player = Player(0, 0)
    player.rect.x = center_x - player.size // 2
    player.rect.y = center_y_above_maze - player.size // 2
    Home = Base(0, 0, 0, 100, 0)
    Home.rect.x = center_x - Home.size // 2
    Home.rect.y = center_y_above_maze - Home.size // 2
    End = Base(0, 0, 100, 0, 0)
    End.rect.x = center_x - End.size // 2
    End.rect.y = center_y_below_maze - End.size // 2

    walls = []
    for row in range(grid_rows):
        for col in range(grid_cols):
            if m.grid[row][col] == 1:  # 1 means wall
                wall_x = int(col * cell_width)
                wall_y = int(row * cell_height) + top_margin
                wall_w = int(cell_width + 1)
                wall_h = int(cell_height + 1)
                wall = Wall(wall_w, wall_h, wall_x, wall_y)
                walls.append(wall)



               
    running = True
    while running == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                init = False
                pygame.quit()
        screen.fill((100, 100, 100))
        #ENTER EVERY DRAWING BELOW
        End.draw(screen)
        Home.draw(screen)
        player.draw(screen)
        for wall in walls:
            wall.draw(screen)
        old_x, old_y = player.rect.x, player.rect.y
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.rect.x -= player.speed
        if keys[pygame.K_RIGHT]:
            player.rect.x += player.speed

        for wall in walls:
            if player.colliderect(wall):
                player.rect.x = old_x  # Undo horizontal movement
                break
        if keys[pygame.K_UP]:
            player.rect.y -= player.speed
        if keys[pygame.K_DOWN]:
            player.rect.y += player.speed

        for wall in walls:
            if player.colliderect(wall):
                player.rect.y = old_y  # Undo horizontal movement
                break

        if player.colliderect(End):
            score = score + 1
            player.rect.x = center_x - player.size // 2
            player.rect.y = center_y_above_maze - player.size // 2
            running = False

            
            
        #outer limits
        if player.rect.x < 0:
            player.rect.x = old_x
        if player.rect.x >= Screen_width - 1:
            player.rect.x = old_x
        if player.rect.y < 0:
            player.rect.y = old_y
        if player.rect.y >= Screen_height -1:
            player.rect.y = old_y


        
        pygame.display.flip()

        clock.tick(60)


