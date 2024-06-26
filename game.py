import pygame
from pygame.locals import *
import random
import copy

pygame.init()
screen_width = 550
screen_height = 600
screen = pygame.display.set_mode((screen_width,screen_height),RESIZABLE)
pygame.display.set_caption("WATER SORT!!!")
fps=60
timer=pygame.time.Clock()
font=pygame.font.Font("freesansbold.ttf",24)

new_game=True
tubes=10
tube_colors=[]
color_choices=["red","orange","light blue","dark blue","dark green","pink","purple","yellow","grey","brown" , "light green","white"]
selected=False
select_rect= 100 # a rectangle that never existed
dest_rect=100
win=False


#initializing the game.
def generate_start():
    tubes_numbers=random.randint(10,14)
    tubes_colors=[]
    available_colors=[]
    for i in range(tubes_numbers):
        tubes_colors.append([])
        if(i < tubes_numbers-2):
            for j in range(4):
                available_colors.append(i)
    for i in range(tubes_numbers-2):
        for j in range(4):
            color=random.choice(available_colors)
            tubes_colors[i].append(color)    
            available_colors.remove(color)    
    #print(tubes_numbers,"\n\n",tubes_colors)            
    return tubes_numbers,tubes_colors

#tube drawing on screen with colored rectangles
def draw_tubes(tubes_nos,tubes_cols):
    tube_boxes=[]
    if(tubes_nos%2==0):
        tubes_per_row=tubes_nos//2
        #offset if extra tube was needed
        offset=False
    else:
        tubes_per_row=tubes_nos//2 +1
        offset=True
    spacing=screen_width/tubes_per_row
    for i in range(tubes_per_row):
        for j in range(len(tubes_cols[i])):    
            #screen name,color needed, position(x-axis,y-axis,weidth,height), opacity , border radius
            pygame.draw.rect(screen,color_choices[tubes_cols[i][j]] , [10+spacing*i,200-(50*j),65,50],0,3)  
        box=pygame.draw.rect(screen,"blue",[10+spacing*i,50,65,200],5,3)  
        if select_rect==i:
            pygame.draw.rect(screen,"green",[10+spacing*i,50,65,200],3,3)
        tube_boxes.append(box)    
    if offset:
        for i in range(tubes_per_row-1):
            for j in range(len(tubes_cols[i+tubes_per_row])):    
                #screen name,color needed, position(x-axis,y-axis,weidth,height), opacity , border radius
                pygame.draw.rect(screen,color_choices[tubes_cols[i+tubes_per_row][j]] , [(spacing*0.5)+10+spacing*i,450-(50*j),65,50],0,3)  
            box=pygame.draw.rect(screen,"blue",[(spacing*0.5)+10+spacing*i,300,65,200],5,3) 
            if select_rect==i+tubes_per_row:
              pygame.draw.rect(screen,"green",[(spacing*0.5)+10+spacing*i,300,65,200],3,3)  
            tube_boxes.append(box) 
    else:
        for i in range(tubes_per_row):
            for j in range(len(tubes_cols[i+tubes_per_row])):    
                #screen name,color needed, position(x-axis,y-axis,weidth,height), opacity , border radius
                pygame.draw.rect(screen,color_choices[tubes_cols[i+tubes_per_row][j]] , [10+spacing*i,450-(50*j),65,50],0,3)  
            box=pygame.draw.rect(screen,"blue",[10+spacing*i,300,65,200],5,3)
            if select_rect==i+tubes_per_row:
              pygame.draw.rect(screen,"green",[10+spacing*i,300,65,200],3,3)  
            tube_boxes.append(box)              
    return tube_boxes

#determine the top color of the selected and destination tube
def calc_move(colors,selected_rect,destination):
    chain=True
    length=1
    #destination
    color_on_top=100
    #selected
    color_to_move=100
    #there should be a color to move
    if len(colors[selected_rect])>0:
        color_to_move=colors[selected_rect][-1]
        for i in range(1,len(colors[selected_rect])):
            #if there are 2 boxes with same color we need to move that too
            if chain:
                if colors[selected_rect][-1-i]==color_to_move:
                    length=length+1
                else:
                    chain=False
    #there should be space in destination                
    if 4 > len(colors[destination]): 
        #if destination empty it can occupy any color
        if(len(colors[destination])==0): 
            color_on_top=color_to_move
        else:
            color_on_top=colors[destination][-1]

    if color_on_top==color_to_move:
        for i in range(length):
            if(len(colors[destination])<4):
                if(len(colors[selected_rect])>0):
                    colors[destination].append(color_on_top)
                colors[selected_rect].pop(-1)
    return colors

#cheak to see if all same colors or empty
def cheak_victory(colors):
    won=True
    for i in range(len(colors)):
        if(len(colors[i])>0):
            if(len(colors[i])!=4):
                won=False
            else:
                main_color=colors[i][-1]
                for j in range(len(colors[i])):
                    if(colors[i][j]!=main_color):
                        won=False 
                           
    return won


#dynamic changes here
run = True
while run:

    #fills the background
    screen.fill("black")

    #setting a time constant
    timer.tick(fps)

    #generate new game when needed.
    if new_game:
        tubes,tube_colors=generate_start()
        initial_colors = copy.deepcopy(tube_colors)
        new_game=False
    else:
        tube_rects=draw_tubes(tubes,tube_colors)    
        
    #winning condition
    win=cheak_victory(tube_colors) 

    for event in pygame.event.get():

        #to close while pressing on close button
        if event.type==pygame.QUIT:
            run=False
        
        if event.type==KEYUP:
            if event.key==pygame.K_SPACE:
                tube_colors=copy.deepcopy(initial_colors)
            if event.key==pygame.K_RETURN:
                new_game=True    

        #on button click action    
        if event.type==pygame.MOUSEBUTTONDOWN:
            if not selected:
                for item in range(len(tube_rects)):
                    #gets the item (rectangle we clicked on)
                    if(tube_rects[item].collidepoint(event.pos)):
                        selected=True 
                        select_rect= item   

            else:
                for item in range(len(tube_rects)):
                    #gets the item (rectangle we clicked on)
                    if(tube_rects[item].collidepoint(event.pos)):
                        dest_rect= item
                        tube_colors=calc_move(tube_colors, select_rect, dest_rect)  
                        selected=False 
                        select_rect=100

    #draw victory text if you win, and leave instructions to restart
    if win:
        victory_text= font.render("YOU WIN !!!, Press Enter For A New Game!!!",True,"white")
        screen.blit(victory_text,(30,265))
    restart_text=font.render("Stuck? Space- Reset, Enter- New Board!",True,"white")    
    screen.blit(restart_text,(10,10))


    #updates items needed
    pygame.display.flip()
pygame.quit()            