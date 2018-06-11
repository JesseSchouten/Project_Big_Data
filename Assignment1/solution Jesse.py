"""
We truthfully declare:
- to have contributed approximately equally to this assignment [if this is not true, modify this sentence to disclose individual contributions so we can grade accordingly]
- that we have neither helped other students nor received help from other students
- that we provided references for all code that is not our own

Name Student 1 email@vu.nl
Name Student 2 email@vu.nl
"""
# replace "grep" in the following lines with the correct commands for exercises 1-8
commands = {
1 : """grep""",
2 : """grep""",
3 : """grep""",
4 : """grep""",
5 : """grep""",
6 : """grep""",
7 : """grep""",
8 : """grep"""}

import os
os.chdir("C:/Users/Jesse/OneDrive/Bureaublad laptop Jesse/Pre-master/Project big data/W1/data-week-1")

def ex9(): # for exercise 9
    None

#First, move to directory where the data map is located
outfile = 'data/outfile.txt'
textfile1 = 'data/textfile1.txt'
textfile2 = 'data/textfile2.txt'
def ex10(textfile1,textfile2,outfile): 
    with open(textfile1) as f1:
        linesf1 = [line.rstrip('\n') for line in f1]
        
    with open(textfile2) as f2:
        linesf2 = [line.rstrip('\n') for line in f2]
    
    result = [linesf1[i] for i in range(0,len(linesf1)) if linesf1[i] not in linesf2]
    
    outfile = open(outfile, 'w')
    
    outfile.write("\n".join(sorted(result)))
    
    outfile.close()
    
    
def ex11(filename):
    None

#First, move to directory where the data map is located
textfile='data/draughts2.txt'
def ex12(textfile):
    
    def readCoordinate(c):
        clist = []
        x = c[1:2]
        y = c[3:4]
        clist.append(x)
        clist.append(y)
        return clist
    
    def printLine(l):
        for i in l:
            print(i, end = '')
            
    def printFirstLineOfBoard():              
       Start=[" ","_","_","_","_"]
       Mid = ["_","_","_","_"]
       End = ["_","_","_"," "]
       
       startLine = Start + 8* Mid + End
       
       printLine(startLine)
       print("")
           
    def printBoard(clist,plist):
        board = [] 
        for k in range(0,30):
            boardLineStartAndMid = ["|"," "," "," "] 
            boardLineEnd = ["|"," "," "," ","|"]
            boardLine1 = boardLineStartAndMid * 9 + boardLineEnd
            boardLine2 = boardLineStartAndMid * 9 + boardLineEnd
            boardEndlineEnd = ["|","_","_","_","|"]
            boardEndline = ["|","_","_","_"]
            boardEndLine = boardEndline * 9 + boardEndlineEnd
            
            board.append(boardLine1)
            board.append(boardLine2)
            board.append(boardEndLine)
               
        # A dictionary to translate coordinates from the file to the place
        # on the correct position in the board variable, the beginline is excluded as its seperatly printed 
        # for example: (1,1) is located at board[28,2], (1,2) at board[25,2] and (2,1) at board[28,6]
        # note: x and y at board are mirrored! so board[y,x]
        xCoordinatedict = {1:2,2:6,3:10,4:14,5:18,6:22,7:26,8:30,9:34,10:38}
        yCoordinatedict = {1:28,2:25,3:22,4:19,5:16,6:13,7:10,8:7,9:4,10:1} 
        
        for i in range(0,len(clist)):
            x = int(clist[i][0])
            y = int(clist[i][1])
            if x % y == 0:
                boardX = xCoordinatedict.get(x)
                boardY = yCoordinatedict.get(y)
                board[boardY][boardX] = str(plist[i]) 
            else: next
        
        printFirstLineOfBoard()
        
        for j in range(0,30):     
            printLine(board[j]) 
            print("")
          
    #main of ex12
    import re as re
    #read line of file
    with open(textfile) as f:
        flines = f.readlines()
        
    coordinateList = []
    pieceList = []
    #is it in the desired format?
    for line in flines:
        match = re.search(r'(^[\(\S][0-9]+,[0-9]+\))(\t)(.)',line)
        if match:
            coordinateList.append(readCoordinate(match.group(1)))
            pieceList.append(match.group(3))
        else:next         
    
    #A board with size 10x10 is assumed
    printBoard(coordinateList,pieceList)
    

        
        
