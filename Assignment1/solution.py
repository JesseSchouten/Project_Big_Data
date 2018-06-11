"""
We truthfully declare:
- to have contributed approximately equally to this assignment [if this is not true, modify this sentence to disclose individual contributions so we can grade accordingly]
- that we have neither helped other students nor received help from other students
- that we provided references for all code that is not our own

Yannick Hogebrug  y.r.hogebrug@student.vu.nl
Jesse Schouten j7.schouten@student.vu.nl
"""
# replace "grep" in the following lines with the correct commands for exercises 1-8
commands = {
1 : """cat hue_upload.csv hue_upload2.csv > hue_combined.csv""",
2 : """gawk -F; "{for(i=2; i<NF; i++) printf $i \";\"; print $NF}" hue_combined.csv | tr -d ^\^" > hue_combined_cleaned.csv""",
3 : """sort2 hue_combined_cleaned.csv | uniq > hue.csv""",
4 : """grep -F "lamp_change" hue.csv | wc -l""",
5 : """gawk -F; "{print $2}" hue.csv | grep -F "adherence_importance" | sort2 | uniq | wc -l""",
6 : """gawk -F; "{print $1}" hue.csv | sort2 | uniq -c""",
7 : """grep -Po [a-zA-Z]+[_]*[a-zA-Z]+ hue.csv | sort2 | uniq""",
8 : """gawk -F; "{print $2}" hue.csv | grep -F "lamp_change" | gawk -F_ "{print $3$4$5}" | sort2 | uniq -c"""}

#Setting work directory
import os
os.chdir("C:/Users/Elitebook/Desktop/ProjectBigData")

def ex9(): # for exercise 9
    #Source: https://www.quora.com/How-can-I-make-sure-the-user-inputs-a-positive-integer-in-Python
    while True:
        try:
            number = int(input("Enter a number bigger than or equal to 10: "))
            assert(number >= 10)
            break
        except:
            print("Enter a number bigger than or equal to 10")
    
    count = 0
    
    number2 = number
    numbers = [int(i) for i in str(number)]
    
    while (number > 0):
        number = number//10
        count += 1
    
    print("Total number of digits: ", count)
    print("Total number of unique digits: ", len(set(str(number2))))
    
    maximum = 0
    sum2 = 0
    
    for i in range(0, len(numbers) - 1):
        sum2 = numbers[i] + numbers[i + 1] 
        
        if sum2 > maximum :
            maximum = sum2
    
    print("Max sum of two consecutive numbers: ",maximum)
                    
#Source: https://stackoverflow.com/questions/15347174/python-finding-prime-factors
    i = 2
    factors = []
    
    while i * i <= number2:
        if number2 % i != 0:
            i += 1
        else:
            number2 //= i
            factors.append(i)
    if number2 > 1:
        factors.append(number2)
 
#Source: https://www.geeksforgeeks.org/python-get-unique-values-list/       
    unique_list = []
     
    for x in factors:
        if x not in unique_list:
            unique_list.append(x)

    print("Sum of distinct prime factors: ", sum(unique_list))
    

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
    
    
def ex11(textfile):
    
    import numpy as np
    import math
    import sys
    
    list_values = []
    
    #Storing the text file in a matrix
    with open(textfile) as f:   
        	lines = [line.rstrip('\n') for line in f] 
    
    for line in lines:
        line_values = line.split()
        for i in range(len(line_values)):
            try:
                int(line_values[i])
                list_values.append(int(line_values[i]))
            except ValueError:
                list_values.append(float('inf'))
    
    matrix = np.array(list_values).reshape(int(math.sqrt(len(list_values))), 
                                           int(math.sqrt(len(list_values))))
    
    #Algorithm of Dijkstra
    current = 0
    minimum = 0
    final_minimum = 0
    permanent = []
    remaining = []
    previous_vertex = [0] * len(matrix)
    final_path = []
    
    labels = [float('inf')] * len(matrix)
    
    for j in range(0, len(matrix[current])):
        labels[current] = minimum
        permanent.append(current)
        for i in range(0, len(matrix[current])):
            value = matrix[current][i]
            if i in permanent or value >= float('inf'):
                continue
            if final_minimum + value < labels[i]:
                labels[i] = final_minimum + value
                previous_vertex[i] = current
        remaining = [i if labels.index(i) not in permanent else 1000 
                     for i in labels]
        minimum = min(remaining)
        final_minimum = minimum 
        current = remaining.index(minimum)
    
    final_path.append(len(matrix)-1)
    search_index = previous_vertex[len(matrix)-1]
    final_path.append(search_index)
    
    while search_index != 0:
        search_index = previous_vertex[search_index]
        final_path.append(search_index)
        
    final_path = list(reversed(final_path))    
    print("Length shortest path is: ", int(labels[len(matrix)-1]))
    print("Shortest path is: ", final_path)


#First, move to directory where the data map is located
textfile_ex12 = 'data/draughts2.txt'
def ex12(textfile_ex12):
    
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
    

        
        
