import pygame
import creatures
import gameboard
from vars import SCREENWIDTH, SCREENHEIGHT, CAPTION, FPS, BLACK, BACKGROUNDGREY, RED, TITLEFONT, COLUMNCOUNT, ROWCOUNT, BUTTONHEIGHT, BUTTONWIDTH, BUTTONPAD, BUTTONCOLOR, GAMESPEED



WIN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption(CAPTION)


def main():
    run = True
    MaxFPS = FPS
    tickTimer = 0
    clock = pygame.time.Clock()
    tiles = []
    gridlines = []
    buttons = []
    runSimulation = False
    mouseClick = False

    buttons.append(gameboard.Button(BUTTONPAD,BUTTONPAD + 25,BUTTONWIDTH,BUTTONHEIGHT,BUTTONCOLOR,"Start / Stop"))
    
    creatures.create_tiles(tiles)

    for tile in tiles:
        tile.find_neighbors(tiles)



    for tile in tiles:
        if tile.row == 20:
            if tile.column == 21:
                tile.alive = True
        if tile.row == 21:
            if tile.column == 22:
                tile.alive = True
        if tile.row == 22:
            if tile.column ==20:
                tile.alive = True
            if tile.column == 21:
                tile.alive = True
            if tile.column == 22:
                tile.alive = True

        if tile.row == 18:
            if tile.column == 21:
                tile.alive = True
            if tile.column == 22:
                tile.alive = True
            if tile.column == 23:
                tile.alive = True


    gameboard.create_grid(WIN, gridlines)

    
    def redraw_window():
        
        WIN.fill(BACKGROUNDGREY)
        for tile in tiles:
            tile.highlight_cell(pygame.mouse.get_pos())
            tile.draw(WIN)

        for gridline in gridlines:
            gridline.draw(WIN)

        for button in buttons:
            button.highlight(pygame.mouse.get_pos())
            button.draw(WIN)
            

        pygame.display.update()

    while run:

        mouseClick = False

        clock.tick(MaxFPS)

        redraw_window()



        if runSimulation == True:

            if tickTimer > int(MaxFPS/GAMESPEED):

                for tile in tiles:
                    tile.live_or_die()
            
                for tile in tiles:
                    tile.reaper()
                
                tickTimer = 0
 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseClick = True

               
        for button in buttons:
            runSimulation = button.button_function(pygame.mouse.get_pos(), mouseClick, runSimulation)

        for tile in tiles:
            tile.alive = tile.toggle_cell(pygame.mouse.get_pos(), mouseClick, tile.alive)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: # left
            delay +=1
        
        tickTimer +=1



def main_menu():
    
    run = True

    while run:

        WIN.fill(BLACK)
        titleLabel = TITLEFONT.render("Press the mouse to begin...", 1, (255,255,255))
        WIN.blit(titleLabel, (SCREENWIDTH/2 - titleLabel.get_width()/2, 350))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()

    pygame.quit()


main_menu()
