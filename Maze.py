from itertools import count
import pygame
import numpy as np
from queue import PriorityQueue
import queue
import os
import sys
import math
import random

global enterPress
enterPress = False

# initializing colors
one = (169, 147, 224)
two = (206, 171, 147)
three = (151, 134, 110)
four = (255, 251, 233)
five = (107, 225, 165)
six = (255, 0, 0)
seven = (0, 255, 0)
vehicle = (50, 44, 36)

pygame.init()

size = (332, 332)
screen = pygame.display.set_mode(size) # added display size

pygame.display.set_caption("Autonomous Delivery Robot")

width = 20
height = 20
margin = 2

grid = [[0 for x in range(15)] for y in range(15)] # 15x15 grid

done = False
clock = pygame.time.Clock() # added clock
found = False
neighbour = []

def savegrid(): # Save the grid to a text file
    global grid
    script_dir = os.path.dirname(__file__)  # Get the directory of the current script
    file_path = os.path.join(script_dir, "maze.txt")

    np.savetxt(file_path, grid)
    print(f"Grid saved to {file_path}")

def loadgrid(index): # Load the grid from a text file
    global grid
    script_dir = os.path.dirname(__file__)  # Get the directory of the current script

    file_path = os.path.join(script_dir, "Maze1", "maze.txt")
    print("maze 1 loaded")

    try:
        grid = np.loadtxt(file_path).tolist()
    except FileNotFoundError:
        print(f"Error: File not found for index {index}")


def startp(maze, i, j): # Find the starting point
    for x in range(len(maze[0])):
        try:
            i = maze[x].index(2)
            j = x
            print(j)
            return i, j
        except:
            pass


def neighbourr(): # Find the neighbours of each cell
    global grid, neighbour
    neighbour = [[] for col in range(len(grid)) for row in range(len(grid))] # Create a list of neighbours for each cell
    count = 0
    for i in range(len(grid)):  # Iterate through each cell in the grid
        for j in range(len(grid)):
            neighbour[count] == []
            if i > 0 and grid[i - 1][j] != 1:   # Check if the cell is not a wall
                neighbour[count].append((i - 1, j))     # Add the neighbour to the list
            if j > 0 and grid[i][j - 1] != 1:   # Check if the cell is not a wall
                neighbour[count].append((i, j - 1))     # Add the neighbour to the list
            if i < len(grid) - 1 and grid[i + 1][j] != 1:   
                neighbour[count].append((i + 1, j))
            if j < len(grid) - 1 and grid[i][j + 1] != 1:
                neighbour[count].append((i, j + 1))
            count += 1


def h(p1, p2): # euclean distance
    x1, y1 = p1
    x2, y2 = p2
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)


def clear_shortest_path(came_from, start, end):     # Clear the shortest path from the grid of previous path
    current = end
    path = []
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()  # Reverse the path to start from the beginning

    for node in path:
        # Update the grid to visualize the pathfinding process
        grid[node[0]][node[1]] = 0
        # Redraw the grid on the screen
        draw_grid(screen, grid)
        pygame.display.flip()
        pygame.time.wait(50)  # Adjust the delay between each step (milliseconds)


def animate_shortest_path(came_from, start, end): # Animate the shortest path
    current = end
    path = []
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()  # Reverse the path to start from the beginning

    for node in path:
        # Update the grid to visualize the pathfinding process
        grid[node[0]][node[1]] = 4
        # Redraw the grid on the screen
        draw_grid(screen, grid)
        pygame.display.flip()
        pygame.time.wait(50)  # Adjust the delay between each step (milliseconds)

def draw_grid(screen, grid): # Draw the grid on the screen
    screen.fill(two)
    for row in range(15):
        for column in range(15):
            if grid[row][column] == 1:
                color = three
            elif grid[row][column] == 2:
                color = one
            elif grid[row][column] == 3:
                color = five
            elif grid[row][column] == 4:
                color = one
            else:
                color = four
            pygame.draw.rect(
                screen,
                color,
                [
                    margin + (margin + width) * column,
                    margin + (margin + height) * row,
                    width,
                    height,
                ],
            )


def a_star(start, end, came_from): # A* algorithm
    global grid, neighbour
    neighbourr()

    new_start = goal_positions.pop(0) # choosing the end as a start

    count = 0
    open_set = PriorityQueue()  # Priority queue to store the nodes to be evaluated
    open_set.put((0, count, start)) # Add the start node to the queue  
    open_set_his = {start}  # Set to keep track of the nodes in the queue

    g_score = [float("inf") for row in grid for spot in row]    # g_score holds the cost from the start node to each node
    g_score[start[0] * len(grid[0]) + start[1]] = 0
    f_score = [float("inf") for row in grid for spot in row] 
    f_score[start[0] * len(grid[0]) + start[1]] = h(start, end) # f_score holds the total estimated cost from the start node to the goal node through each node

    while not open_set.empty():     # Iterate until the open set is empty
        current = open_set.get()[2] # Get the node with the lowest f_score value from the queue 2 is the index of the node
        open_set_his.remove(current)  # Remove the current node from the queue

        if current == end:  # Check if the goal node has been reached
            print("finishing")
            # short_path(came_from, end)
            return came_from, start, end, new_start
        
        for nei in neighbour[current[0] * len(grid[0]) + current[1]]:   # Iterate through the neighbours of the current node
            
            temp_g_score = g_score[current[0] * len(grid[0]) + current[1]] + 1  # Calculate the tentative g_score value

            if temp_g_score < g_score[nei[0] * len(grid[0]) + nei[1]]:  # Check if the new g_score value is less than the current g_score value
                came_from[nei] = current # Update the path to the neighbour
                g_score[nei[0] * len(grid[0]) + nei[1]] = temp_g_score # Update the g_score value
                f_score[nei[0] * len(grid[0]) + nei[1]] = temp_g_score + h(nei, end) # Update the f_score value
                if nei not in open_set_his: # Check if the neighbour is not in the queue
                    count += 1 # Increment the count
                    open_set.put((f_score[nei[0] * len(grid[0]) + nei[1]], count, nei))     # Add the neighbour to the queue
                    open_set_his.add(nei)   # Add the neighbour to the set

    return None

def draw_grid_end(grid):

    for row in range(15):
        for column in range(15):
            if grid[row][column] == 1:
                color = three
            elif grid[row][column] == 2:
                color = one
            elif grid[row][column] == 3:
                color = five
            elif grid[row][column] == 4:
                color = one
            elif grid[row][column] == 5:
                color = six
            elif grid[row][column] == 6:
                color = seven
            elif grid[row][column] == 10:
                color = vehicle
            else:
                color = four
            pygame.draw.rect(
                screen,
                color,
                [
                    margin + (margin + width) * column,
                    margin + (margin + height) * row,
                    width,
                    height,
                ],
            )

    return

loadgrid(0)


def clear_previous_vehicles():
    global grid, vehicle_positions

    # Iterate through the list of vehicle positions and reset those cells back to empty (0)
    for row, col in vehicle_positions:
        grid[row][col] = 0  # Reset the cell to an empty cell (0)

    # Clear the list of vehicle positions after resetting the grid
    vehicle_positions = []  # Reset the list of vehicle positions to empty


def random_generate_vehicles():
    global grid, start_row, start_column
   # Get the dimensions of the grid
    rows = len(grid)
    cols = len(grid[0])

    # Initialize the number of vehicles to place
    num_vehicles = 4

    # Randomly place vehicles on the grid
    while num_vehicles > 0:
        row = random.randint(0, rows - 1)
        col = random.randint(0, cols - 1)

        # Check if the cell is empty (0), not the start node (2), not the goal node (3), and not an already placed vehicle or obstacle (1)
        if grid[row][col] == 0 and (row != start_row or col != start_column):
            # Place the vehicle on the grid
            grid[row][col] = 1  # Use the same value as obstacle (1) to represent vehicles
            vehicle_positions.append((row, col))
            # Decrement the number of vehicles left to place
            num_vehicles -= 1
    draw_grid_end(grid)
    pygame.display.flip()

vehicle_positions = []

goal_positions = []
def generate_goal_nodes(grid, start_row, start_column, num_goals=5):

    # Iterate until we have generated the required number of goal nodes
    while len(goal_positions) < num_goals:
        # Generate a random row and column within the grid size
        row = random.randint(0, len(grid) - 1)
        column = random.randint(0, len(grid[0]) - 1)

        # Check if the generated position is valid
        if (row != start_row or column != start_column) and grid[row][column] == 0:
            # Check if the generated position is not already a goal node
            if (row, column) not in goal_positions:
                # Add the position to the list of goal positions
                goal_positions.append((row, column))
                # Mark this position as a goal node (3)
                grid[row][column] = 3

    sort_goal_positions(start)

    return grid


# sorting the goal nodes by euclean distance
def sort_goal_positions(start):
    goal_positions.sort(key=lambda start: math.sqrt((start[0] - start_row)**2 + (start[1] - start_column)**2))    


# function to delete the goal node dynamically
def deleted_goal_nodes(row, column, grid, num_goals):

    for i in goal_positions:
        print(i)

    num_goals -= 1
    goal_positions.remove((row,column))
    # print("goal removed")
    # print("new list is ")
    for i in goal_positions:
        print(i)

# function to add the goal node dynamically
def add_goal_node(row, column, grid, num_goals):
    num_goals += 2
    goal_positions.append((row,column))
    

# initializing starting node
start = (1,1)
start_row = 1
start_column = 1
grid[start_row][start_column] = 2
num_goals = 5
grid = generate_goal_nodes(grid, start_row, start_column, num_goals)
# random_generate_vehicles() # generating vehicles

draw_grid_end(grid)

while not done:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                print("Exit")
                pygame.quit()
            if event.key == pygame.K_s:
                print("Saving Maze")
                savegrid()
            if event.key == pygame.K_l:
                print("Loading Maze")
                loadgrid(0)

            if event.key == pygame.K_RETURN:
                
                came_from = {}
                # print("length", len(goal_positions))
                # for i in goal_positions:
                #     print(i)
                
                for i in range(len(goal_positions)):

                    if (sum(x.count(2) for x in grid)) <= num_goals:

                        sort_goal_positions(start)
                        end = goal_positions[0]
                        enterPress = True
                        # print("start : ", start)
                        # print("end : ", end)
                        # print("Solving...")
                        result = a_star(start, end, came_from)
                        if result:
                            # Unpack result tuple
                            came_from, start, end, new_start = result
                            print("came from", came_from)
                            animate_shortest_path(came_from, start, end)
                            clear_shortest_path(came_from, start, end)
                            # clear_previous_vehicles()
                              
                            came_from.clear() # clearing the came from dictionary

                        else:
                            print("No path found!")

                        pygame.time.wait(1000)
                        # random_generate_vehicles()
                        # pygame.time.wait(2000)

                        start = new_start # updating the start to new_start returned

            if event.key == pygame.K_r:

                grid = [[0 for x in range(15)] for y in range(15)]
        if pygame.mouse.get_pressed()[2]:  # Right mouse button
            column = pos[0] // (width + margin)
            row = pos[1] // (height + margin)

            # Check if the clicked cell is not the start node
            if grid[row][column] != 2:

                if (sum(x.count(2) for x in grid)) < 1 or (sum(x.count(3) for x in grid)) < 1:
                    if (sum(x.count(2) for x in grid)) == 0:
                        if grid[row][column] == 2:
                            grid[row][column] = 0
                            
                        elif grid[row][column] == 3:
                            grid[row][column] = 0
                            deleted_goal_nodes(row, column, grid, num_goals)
                        else:
                            grid[row][column] = 2
                            start = (row,column)

                    else:
                        if grid[row][column] == 3:
                            grid[row][column] = 0
                            deleted_goal_nodes(row, column, grid, num_goals)
                        elif grid[row][column] == 2:
                            grid[row][column] = 0
                        else:
                            grid[row][column] = 3
                            add_goal_node(row, column, grid, num_goals)

                elif (sum(x.count(2) for x in grid)) == 1 and (sum(x.count(3) for x in grid)) >= 1:
                    if grid[row][column] == 3:
                            grid[row][column] = 0
                            deleted_goal_nodes(row, column, grid, num_goals)
                    else:
                            grid[row][column] = 3
                            add_goal_node(row, column, grid, num_goals)

                else:
                    if grid[row][column] == 2:
                        grid[row][column] = 0
                    if grid[row][column] == 3:
                        grid[row][column] = 0

                        deleted_goal_nodes(row, column, grid, num_goals)

                    if grid[row][column] == 1:
                        grid[row][column] = 0

        if pygame.mouse.get_pressed()[0]:  # Left mouse button
            column = pos[0] // (width + margin)
            row = pos[1] // (height + margin)

            # Check if the clicked cell is not the start node
            if grid[row][column] != 2:
                grid[row][column] = 1  # Set the clicked cell to 1 (wall or obstacle)
            # if grid[row][column] == 1:
            #     grid[row][column] = 0

    pos = pygame.mouse.get_pos()
    x = pos[0]
    y = pos[1]
    screen.fill(two)

    # draw grid function
    draw_grid_end(grid)
    
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
