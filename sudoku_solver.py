#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import pygame, time

width, height = 600, 600

impossibles = [[[] for c in range(9)] for r in range(9)]

grid = np.zeros([9,9])


grid = [[5,3,0,0,7,0,0,0,0],
        [6,0,0,1,9,5,0,0,0],
        [0,9,8,0,0,0,0,6,0],
        [8,0,0,0,6,0,0,0,3],
        [4,0,0,8,0,3,0,0,1],
        [7,0,0,0,2,0,0,0,6],
        [0,6,0,0,0,0,2,8,0],
        [0,0,0,4,1,9,0,0,5],
        [0,0,0,0,8,0,0,7,9]]


"""
grid = [[0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0]]
"""
"""
grid = [[0,7,2,5,0,0,0,0,0],
        [0,3,0,0,0,4,0,0,0],
        [0,0,0,0,0,2,0,1,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,4,7,3,0,0,0,0],
        [1,5,7,0,0,0,0,0,0],
        [9,0,8,0,0,0,5,0,0],
        [0,0,0,0,0,0,4,2,0],
        [0,0,0,9,0,0,3,7,0]]
"""

grid = np.array(grid)

given = np.full([9,9], False)

for row in range(9):
    for col in range(9):
        if grid[row, col] != 0:
            given[row, col] = True

problem = Exception("Oops, there's an error :/")

def print_(grid=grid):
    charWidth, charHeight = 2*grid.shape[1]-1, 2*grid.shape[0]-1
    
    print("+{}+".format("-"*charWidth))
    
    for row in range(grid.shape[0]):
        print("|{}|".format("|".join([str(int(i)) if i > 0 else " " for i in grid[row]])))
        
        if row < grid.shape[0]-1:
            print("|{}|".format("-"*charWidth))
    
    print("+{}+".format("-"*charWidth))

def draw(selected=None):
    window.fill((255,255,255))
    
    #Numbers
    for Y in range(grid.shape[0]):
        for X in range(grid.shape[1]):
            if grid[Y, X] != 0:
                txtSurf = fontMain.render(str(grid[Y, X]), 1, (0,0,0))
                txtSize = fontMain.size(str(grid[Y, X]))
                
                if given[Y, X]:
                    pygame.draw.rect(window, (200,200,200), [X*width/9, Y*height/9, width/9+1, height/9+1])
                
                window.blit(txtSurf, [(X+0.5)*(width/9) - txtSize[0]/2, (Y+0.5)*(height/9) - txtSize[1]/2])
            
            else:
                for n in range(len(impossibles[Y][X])):
                    number = impossibles[Y][X][n]
                    #Impossibles
                    txtSurf = fontImp.render(str(number), 1, (100,0,0))
                    txtSize = fontImp.size(str(number))
                    
                    window.blit(txtSurf, [X*(width/9) + n*width/9/9, (Y+1)*(height/9) - txtSize[1]])
    
    #Grid lines
    for Y in range(9):
        lineWidth = 3 if Y%3 == 0 else 1
        
        pygame.draw.line(window, (0,0,0), [0, Y * (height/9)], [width, Y * (height/9)], lineWidth)
    
    for X in range(9):
        lineWidth = 3 if X%3 == 0 else 1
        
        pygame.draw.line(window, (0,0,0), [X * (width/9),0], [X * (width/9),height], lineWidth)
    
    #Selected
    if selected != None:
        pygame.draw.rect(window, (0,255,0), [selected[0]*(width/9), selected[1]*(height/9), width/9, height/9], 4)
    
    pygame.display.flip()

def getGroup(x,y):
    return grid[y*3:y*3+4,x*3:x*3+4]

def algorithm(grid=grid):
    changed = False
    
    for y in range(grid.shape[0]):
        for x in range(grid.shape[1]):
            draw([x,y])
            
            group = (x//3, y//3)
            
            
            if y%3 == 0 and x%3 == 0:
                for i in range(1,10):
                    if not i in getGroup(*group):
                        """
                        indicesY, indicesX = np.where(grid == i)
                        
                        indices = [[indicesX[j], indicesY[j]] for j in xrange(len(indicesX))]
                        
                        notHere = []
                    
                        for coords in indices:
                            if group[0]*3 <= coords[0] < (group[0]+1)*3:
                                for j in xrange(3):
                                    notHere.append([coords[0], j])
                            
                            elif group[1]*3 <= coords[1] < (group[1]+1)*3:
                                for j in xrange(3):
                                    notHere.append([j, coords[1]])
                        
                        print("group: {}| i: {}| notHere: {}".format(group, i, notHere))
                        
                        if len(notHere) == np.count_nonzero(getGroup(*group) == 0)-1:
                            stop = False
                            
                            for y2 in range(3):
                                for x2 in range(3):
                                    if getGroup(*group)[y2,x2] == 0 and not [x2,y2] in notHere:
                                        grid[group[1]*3+y2, group[0]*3+x2] = i
                                        
                                        changed = True
                                        
                                        stop = True
                                        break
                                if stop:
                                    break
                        """
                        
                        #Compter les impossibles, si compte est bon...
                        impossibles_in_group = []
                        
                        for y2 in range(3):
                            for x2 in range(3):
                                if i in impossibles[group[1]*3+y2][group[0]*3+x2] and not i in impossibles_in_group:
                                    impossibles_in_group.append([x2,y2])
                        
                        if len(impossibles_in_group) == 8:
                            Xs, Ys = [], []
                            
                            """
                            for y2 in range(3):
                                for x2 in range(3):
                                    if getGroup(*group)[y2,x2] != 0:
                                        Xs.append(x2)
                                        Ys.append(y2)
                            """
                            
                            for coords in impossibles_in_group:
                                Xs.append(coords[0])
                                Ys.append(coords[1])
                            
                            Xs = {0: Xs.count(0),1: Xs.count(1),2: Xs.count(2)}
                            Ys = {0: Ys.count(0),1: Ys.count(1),2: Ys.count(2)}
                            
                            Xs, Ys = sorted(Xs.items(), key=lambda item: item[1]), sorted(Ys.items(), key=lambda item: item[1])
                            
                            #input("Ok pour {}? {}| {}|{}".format(i, impossibles_in_group, Xs, Ys))
                            grid[group[1]*3+Ys[0][0], group[0]*3+Xs[0][0]] = i
                            
                            changed = True
            
            
            if grid[y, x] != 0:
                #Add to impossibles
                
                if impossibles[y][x] != list(range(1,10)):
                    impossibles[y][x] = list(range(1,10))
                
                
                #Column
                for c in range(9):
                    if not grid[y,x] in impossibles[y][c]:
                        impossibles[y][c].append(grid[y, x])
                        
                        changed = True
                
                #Row
                for r in range(9):
                    if not grid[y,x] in impossibles[r][x]:
                        impossibles[r][x].append(grid[y, x])
                        
                        changed = True
                
                #9x9 group
                for y2 in range(3):
                    for x2 in range(3):
                        posX, posY = group[0]*3+x2, group[1]*3+y2
                        
                        if not grid[y,x] in impossibles[posY][posX]:
                            impossibles[posY][posX].append(grid[y, x])
                            
                            changed = True
                
                time.sleep(0.01)
                #input()
                
                draw([x,y])
            
            else:
                
                impossibles_here = impossibles[y][x]
                
                if len(impossibles_here) == 9:
                    print(x,y)
                    
                    input()
                    raise problem
                
                elif len(impossibles_here) == 8:
                    grid[y, x] = [i for i in range(1,10) if not i in impossibles_here][0]
                    changed = True
    
    return changed



if __name__ == "__main__":
    pygame.init()
    
    window = pygame.display.set_mode([width, height])
    
    fontMain = pygame.font.SysFont("dejavusans", 30, bold=True)
    fontImp = pygame.font.SysFont("dejavusans", 15)
    
    draw()
    print_()
    input()
    goOn = True
    
    while goOn:
        goOn = algorithm()
        
        draw()
        print_()
        
        #input()
        
        if np.count_nonzero(grid == 0) == 0:
            break
    
    draw()
    print_()
    
    input("Fin")
