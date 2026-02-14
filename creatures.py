import pygame
from vars import TILEWIDTH, TILEHEIGHT, RED, DEADCELLCOLOR, HIGHLIGHT, XOFFSET, XPAD, YOFFSET, YPAD, GAMEBOARDSTARTX, GAMEBOARDSTARTY, COLUMNCOUNT, ROWCOUNT, ALIVECELLCOLOR


class Tile():
     def __init__(self, x, y, column, row):
         self.x = x
         self.y = y
         self.originalColor = DEADCELLCOLOR
         self.column = column
         self.row = row
         self.alive = False
         self.willLive = False
         self.highlight = False
         self.livingNeighbors = 0
         self.neighbors = []

     def draw(self, window):
         

         if self.alive == True:
             self.color = ALIVECELLCOLOR
         else:
             self.color = DEADCELLCOLOR

         if self.highlight == True:
             self.color = HIGHLIGHT

         pygame.draw.rect(window, self.color, (self.x, self.y, TILEWIDTH, TILEHEIGHT))

     def highlight_cell(self, mousePos):

         self.highlight = False

         if self.x <= mousePos[0]:
             if self.x + TILEWIDTH > mousePos[0]:
                 if self.y <= mousePos[1]:
                    if self.y + TILEHEIGHT > mousePos[1]:
                        self.highlight = True


     def find_neighbors(self,tiles):

         for tile in tiles:

                if self.column == tile.column-1:
                    if self.row == tile.row-1:
                        self.neighbors.append(tile)
                    if self.row == tile.row:
                        self.neighbors.append(tile)
                    if self.row == tile.row+1:
                        self.neighbors.append(tile)
                if self.column == tile.column:
                    if self.row == tile.row-1:
                        self.neighbors.append(tile)
                    if self.row == tile.row+1:
                        self.neighbors.append(tile)
                if self.column == tile.column+1:
                    if self.row == tile.row-1:
                        self.neighbors.append(tile)
                    if self.row == tile.row:
                        self.neighbors.append(tile)
                    if self.row == tile.row+1:
                        self.neighbors.append(tile)


     def live_or_die(self):

         
         self.livingNeighbors = 0

         
         for neighbor in self.neighbors:
             if neighbor.alive == True:
                 self.livingNeighbors += 1

         self.willLive = False

         if self.alive == True:
            if self.livingNeighbors == 2:
                    self.willLive = True
         if self.livingNeighbors == 3:
                 self.willLive = True
             
     def reaper(self):

         if self.willLive == False:
             self.alive = False
         else:
             self.alive = True

     def toggle_cell(self, mousePos, clicked, cellAlive):
           
         if self.x <= mousePos[0]:
             if self.x + TILEWIDTH > mousePos[0]:
                 if self.y <= mousePos[1]:
                    if self.y + TILEHEIGHT > mousePos[1]:
                        if clicked == True:
                            if cellAlive == True:
                                cellAlive = False
                            else:
                                cellAlive = True
        
         return(cellAlive)


def highlightNeighbors(neighbors):
    for neighbor in neighbors:
        neighbor.highlight = True


def create_tiles(listOfTiles):

    x = GAMEBOARDSTARTX
    y = GAMEBOARDSTARTY

    for i in range(0, ROWCOUNT):

        for j in range(0, COLUMNCOUNT):

            listOfTiles.append(Tile(GAMEBOARDSTARTX + TILEWIDTH*j, GAMEBOARDSTARTY + TILEWIDTH*i, j+1, i+1))

