
from tkinter import Tk, Button
import pygame
import math 
from game import Game 


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GREY = (107, 112, 119)
LIGTH_GREY = (180, 185, 193)
def text_objects(text, font):
    textSurface = font.render(text, True, RED)
    return textSurface, textSurface.get_rect()




def window():
    # Define some colors


    pygame.init()

    # Set the width and height of the screen [width, height]
    #size = (1300,700)
    size = (600,600)
    n_bombs = 100

    extra_grid = 180
    total_size = (size[0], size[1] + extra_grid)


    screen = pygame.display.set_mode(total_size)

    pygame.display.set_caption("My Game")

    # Loop until the user clicks the close button.

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    


    POINTS = [20,20]
    margin=1
    width= int((-POINTS[0]*margin  +size[0])/POINTS[0]) 
    height=int((-POINTS[1]*margin  +size[1])/POINTS[1]) 
    
    game = Game(POINTS[0],POINTS[1],n_bombs)
    font = pygame.font.SysFont('Arial', height)

    font_info = pygame.font.SysFont('Arial', min(int(extra_grid/3), size[0]))

    cont_x = 0
    
    pygame.draw.rect(screen, WHITE,[0,size[1]+1,size[0],extra_grid])

    screen.blit(font_info.render(f'Bombs:{n_bombs}', True, (0,0,0)), (0,size[1]))

    for column in range(0+margin, size[0], width+margin):
        cont_y = 0
        for row in range(0+margin, size[1], height+margin):
            pygame.draw.rect(screen, GREY,[column,row,width,height] )

            cont_y +=1
        cont_x += 1
    # --- Go ahead and update the screen with what we've drawn.
    #pygame.display.flip()

    # --- Limit to 60 frames per second~´
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        mouse = pygame.mouse.get_pos()

        click = pygame.mouse.get_pressed()
        xx =math.floor(mouse[0]/(width + margin))
        yy = math.floor(mouse[1]/(height + margin))

        if xx >= POINTS[0] or yy >= POINTS[1]:
            pass
        if game.is_over:
            pygame.draw.rect(screen, WHITE,[0,size[1]+1,size[0],extra_grid])

            if game.state == 'Won':
                screen.blit(font_info.render('WON', True, (0,255,0)), (0,size[1]+ 2))
            else:
                screen.blit(font_info.render('YOU LOST', True, (255,0,0)), (0,size[1]+ 2))
        else:
            if click[0]:
                
                try:    
                    result = game.click(yy,xx)
                    if result == -1:
                        screen.blit(font.render('B', True, (255,0,0)), (xx*(width + margin) + width/4,  yy*(margin +height)))

                        # Tile had a bomb
                        pass
                    elif result is None:
                        # tile has a flag or is already open
                        pass
                    else: # puts the number of bombs on the screen

                        pygame.draw.rect(screen, LIGTH_GREY,[xx*(margin + width),yy*(margin + height),width,height] )

                        screen.blit(font.render(str(result), True, (0,0,255)), (xx*(width + margin)+ width/4,   yy*(margin +height)))

                        if result == 0:
                            # open all tiles in all directions until a tile near a bomb is found
                            new_pos = [[yy,xx]]
                            while True:
                                all_pos = []
                                for pos in new_pos:
                                    tmp,to_open = game.click_around(pos)
                                    all_pos.extend(tmp)
                                    for k in to_open:
                                        pygame.draw.rect(screen, LIGTH_GREY,[k[1]*(margin + width),k[0]*(margin + height),width,height] )

                                        screen.blit(font.render(str(k[2]), True, (0,0,255)), (k[1]*(width + margin)+ width/4,   k[0]*(margin +height)))
                                if new_pos == []:
                                    break 
                                new_pos = all_pos

                except Exception as e:
                    print(e)
                    pass

            elif click[-1]:
                # right click
                
                result = game.click(yy,xx, to_flag = 1)
                if result is None:
                    # tile is already open
                    continue
                if result:

                    screen.blit(font.render(str('F'), True, (80, 196, 49)), (5 +xx*(width + margin), yy*(margin +height)))
                else:
                    # erase the letter F from the screen -> write in white over the original image
                    screen.blit(font.render(str('F'), True, GREY), (5+xx*(width + margin), yy*(margin +height)))
                
                pygame.draw.rect(screen, WHITE,[0,size[1]+1,size[0],extra_grid])
                screen.blit(font_info.render(f'Bombs:{n_bombs - game.game_board.have_flag}', True, (0,0,0)), (0,size[1]+ 10))

        pygame.display.update()
        clock.tick(10)

# Close the window and quit.

print(int(0.51))
window()