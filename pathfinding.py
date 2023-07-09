from queue import PriorityQueue
import math
import os
import random

obstacle_locations =[[7,7],[8,7],[9,7],[7,8],[6,8],[5,8],[4,8]]
delivery_point=[9,9]
start_point=[0,0]
path=[]

grid_size = 10

class Tile:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.travelled = False
        self.neighbours=[]

    def position(self):
        return self.x, self.y    

    def set_neighbours(self, grid):
        self.neighbours=[]
        if self.x < grid_size-1 and not list(grid[self.x+1][self.y].position()) in obstacle_locations:
            self.neighbours.append(grid[self.x+1][self.y])   
        if self.x > 0 and not list(grid[self.x-1][self.y].position()) in obstacle_locations:
            self.neighbours.append(grid[self.x-1][self.y])
        if self.y < grid_size-1 and not list(grid[self.x][self.y+1].position()) in obstacle_locations:
            self.neighbours.append(grid[self.x][self.y+1])
        if self.y > 0 and not list(grid[self.x][self.y-1].position()) in obstacle_locations:
            self.neighbours.append(grid[self.x][self.y-1])
        if self.x < grid_size-1 and self.y < grid_size-1 and not list(grid[self.x+1][self.y+1].position()) in obstacle_locations: 
            self.neighbours.append(grid[self.x+1][self.y+1])
        if self.x > 0 and self.y > 0 and not list(grid[self.x-1][self.y-1].position()) in obstacle_locations: 
            self.neighbours.append(grid[self.x-1][self.y-1])    
        if self.x < grid_size-1 and self.y > 0 and not list(grid[self.x+1][self.y-1].position()) in obstacle_locations: 
            self.neighbours.append(grid[self.x+1][self.y-1])    
        if self.x > 0 and self.y < grid_size-1 and not list(grid[self.x-1][self.y+1].position()) in obstacle_locations: 
            self.neighbours.append(grid[self.x-1][self.y+1])   

    def is_obstacle(self):
        return [self.x,self.y] in obstacle_locations 

    def __lt__(self, other):
	    return False                       

def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return round(math.sqrt((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2)))

def generate_obstacles(count):
    obstacle_locations=[]
     
    for i in range(count):
        new_obstacle = []
        while new_obstacle in obstacle_locations or new_obstacle == start_point or new_obstacle == delivery_point:
            new_obstacle = [random.randint(0,grid_size-1),random.randint(0,grid_size-1)]
        obstacle_locations.append(new_obstacle) 
    return obstacle_locations       

def create_grid():
    grid_=[]
    for a in range(grid_size):
        grid_.append([])
        for b in range(grid_size):
            tile=Tile(a,b)
            grid_[a].append(tile)
    return grid_  
grid=create_grid()

def clear():
    os.system('cls')

def display_grid():    
    for x in grid:
        grid_line="" 
        for tile in x:
            fill = ". "
            if list(tile.position()) in obstacle_locations:
                fill = "[]"
            if list(tile.position()) in path:
                fill = "##"   
            if list(tile.position()) == delivery_point:
                fill = "ED"
            if list(tile.position()) == start_point:
                fill = "ST"           
            grid_line+=fill
        print(grid_line)
def construct_path(origin, current):
    path.append(delivery_point)
    while current in origin:
        current = origin[current]
        path.append(list(current.position()))    

def pathfind(grid,start,end):
    count=0 
    open_set=PriorityQueue()
    open_set.put((0,count,start))
    origin_tile={}
    g_score={tile:float("inf") for x in grid for tile in x}
    g_score[start]=0
    f_score={tile:float("inf") for x in grid for tile in x}
    f_score[start]=h(start.position(),end.position())
    open_set_hash={start}

    while not open_set.empty():
        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            construct_path(origin_tile, end)
            print(f"\nSolved!\n")
            print(f"Reached Destination in {len(path)-1} Steps\n")
            return True

        for neighbour in current.neighbours:
            temp_g_score = g_score[current]+1 

            if temp_g_score < g_score[neighbour]:
                origin_tile[neighbour]=current
                g_score[neighbour]=temp_g_score
                f_score[neighbour]=temp_g_score+h(neighbour.position(),end.position())  
                if neighbour not in open_set_hash:
                    count+=1
                    open_set.put((f_score[neighbour], count, neighbour))
                    open_set_hash.add(neighbour)  

    print("\nUnable to reach delivery point\n")
    construct_path(origin_tile, current)
    return False

clear()
print("\nGrid Layout: \n")
# Create Grid
for x in grid:
    grid_line=[]  
    for tile in x:
        tile.set_neighbours(grid) 

# Display Starting Grid         
display_grid()
input("\nSolve? Press Enter ")
clear()

# Run Algorith and Display Result 
pathfind(grid,grid[start_point[0]][start_point[1]],grid[delivery_point[0]][delivery_point[1]])
print(f"Path: {path[::-1]}\n")
display_grid()

input("\nRandomise Grid and re-run? Press Enter ")

# Run Again --------------------------------------------------------------
while True:

    size_input=int(input(f'What Grid Size Would You Like? Enter an Integer: '))
    if size_input < 5: size_input=5
    if size_input > 100: size_input=100

    clear()
    grid_size=size_input
    path=[]
    grid=create_grid()
    print("\nGrid Layout: \n")

    # Generate Obstacles
    obstacle_locations=generate_obstacles(round(20*(grid_size/10)*(grid_size/10)))
    delivery_point=[grid_size-1,grid_size-1]

    # Create Random Grid
    for x in grid:
        grid_line=[]  
        for tile in x:
            tile.set_neighbours(grid) 

    display_grid()
    input("\nPress Enter to Solve ")
    clear()

    # Run Algorithm and Display Result
    pathfind(grid,grid[start_point[0]][start_point[1]],grid[delivery_point[0]][delivery_point[1]])        
    display_grid()

    print("\nRandomise Grid Again?")



