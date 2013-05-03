# BoggleBash.py
# 15-112_FUNDAMENTALS OF PROGRAMMING_TERM PROJECT
# Aayush Tekriwal + atekriwa + Section A
# TOTAL LINES = 964 excluding python code in other imported files

# PLEASE NOTE: Due to the sheer number of graphic elements in the game
#   there are many magic numbers used to represent coordinates.
#   However, magic numbers have been avoided wherever realistically possible

from Tkinter import *
from Tkinter import Tk, Canvas, Frame, Button
from ttk import*
import tkMessageBox
import random
import optparse
import dice # A python file containing all the dice needed for the game
import os
import dictionaryset # A python file containing the english dictionary
import share # A python file containing Game Sharing Data

################################################################
############# CODE FOR BOARD AND ITS ATTRIBUTES BELOW ##########
################################################################

# Assigning variables from another file
FOURBYFOUR = dice.FOURBYFOUR #copies all 4x4 dice in a variable
FIVEBYFIVE = dice.FIVEBYFIVE #copies all 5x5 dice in a variable

# Boggle Board class contains and performs all functions to 
# do with the creation, and manipulation of the board
class BoggleBoard(object):
    def __init__(self, dimension):
        self.dimension = dimension # Stores board dimension
        self.finalBoard = self.randomDiceLetterAssign(dimension) # Random Board
        self.maxItemLength = self.maxItemLength() 
        self.boardTODictionary = self.boardTODictionary() # Dict ver. of Board

    def newBoard(self, rowsCols):
        # Creates a new empty board with the correct dimension
        temp = list()
        for row in xrange(rowsCols): temp += [[0] * rowsCols]
        return temp

    def randomDiceList(self, rowsCols): 
        # Provides a random order of dice, replicating the shaking of 
        # the boggle box
        diceList = list() # Initializing an empty list
        numberOfDice = rowsCols**2 # It is always a square board
        while (len(diceList) < numberOfDice):
            randomInteger = random.randint(0, numberOfDice - 1)
            if not(randomInteger in diceList):
                diceList.append(randomInteger)
        return diceList

    def randomDiceAssign(self, rowsCols):
        # Assigns the random dice list to each position on the board
        board = self.newBoard(rowsCols)
        randDiceList = self.randomDiceList(rowsCols)
        # Iterates through every row and column of the board
        for i in xrange(rowsCols):
            for j in xrange(rowsCols):
                board[i][j] = randDiceList[j + i * rowsCols] # Assignment
        return board

    def randomDiceLetterAssign(self, rowsCols):
        # Assigns a random letter from each dice to the particular
        # dice's position on the board
        board = self.randomDiceAssign(rowsCols)
        for i in xrange(rowsCols): # Iterates through rows
            for j in xrange(rowsCols): # Iterates through columns
                diceNumber = board[i][j]
                randInt = random.randint(0,5) # Random Assignment
                if (rowsCols == 4):
                    board[i][j] = FOURBYFOUR[diceNumber][randInt]
                elif (rowsCols == 5):
                    board[i][j] = FIVEBYFIVE[diceNumber][randInt]
        return board

    def maxItemLength(self):
        maxLen = 0
        rows = len(self.finalBoard)
        cols = len(self.finalBoard[0])
        for row in xrange(rows):
            for col in xrange(cols):
                maxLen = max(maxLen, len(str(self.finalBoard[row][col])))
        return maxLen

    # PrintBoard method was borrowed from Prof. Kosbie's 15-112 notes
    # on printing 2d lists neatly in the console
    def printBoard(self): # Used only for testing game/ playing it on consol
        if (self.finalBoard == []):
            print []
            return
        (rows, cols) = (len(self.finalBoard), len(self.finalBoard[0]))
        fieldWidth = self.maxItemLength
        print "[ ",
        for row in xrange(rows):
            if (row > 0): print "\n  ",
            print "[ ",
            for col in xrange(cols):
                if (col > 0): print ",",
                # The next 2 lines print a[row][col] with the given fieldWidth
                format = "%" + str(fieldWidth) + "s"
                print format % str(self.finalBoard[row][col]),
            print "]",
        print "]"

    def checkValidCharacters(self, word): # checks if characters in entry
                                            # Are valid based on board
        board = self.finalBoard
        boardChars = self.flattenBoard(board)
        word = word.upper()
        for c in word: # Iterates through every character of the word
            if ((not(c in boardChars))or word.count(c)>(boardChars.count(c))):
                return False
        return True

    def flattenBoard(self, board): # Hashed because its not called anywhere
        if (type(board) != list):
            return board
        elif ((type(board) == list) and (len(board) == 0)): 
            return board
        elif (type(board[0]) == list): # If the first element is a list object
            return self.flattenBoard(board[0]) + self.flattenBoard(board[1:]) 
        return [board[0]]+self.flattenBoard(board[1:])#Else,recursive case 2

    def findLocation(self, character): # Finds position of a char on board
        # Iterates through the entire board
        character = character.upper()
        board = self.finalBoard
        charLctns = list()
        for i in xrange(len(board)):
            for j in xrange(len(board[0])):
                if board[i][j] == character: # If character found
                    charLctns.append((i,j)) # Append position tuple to list
        return charLctns # return list of position tuples

    def boardTODictionary(self): # Represents the board as a dictionary
        board = self.finalBoard # Makes local copy of board
        boardDict = dict() # Initialize dict to store values
        # Iterates through every row and column of the board
        for i in xrange(len(board)):
            for j in xrange(len(board[0])):
                boardDict[(i,j)] = (board[i][j]).lower() # Assigns key and ref
        return boardDict

################################################################
################### CODE FOR DICTIONARY AND GAME SOLUTIONS BELOW
################################################################

# dictionary is global for valid reasons. It is required my multiple methods 
# Across the program
DICTIONARY  = dictionaryset.dict # stores dictionary set globally from a file
PREFIXES = dict() # Stores prefixes in a dictionary
SCORES = {3: 1, 4: 1, 5: 2, 6: 3, 7: 5, None: 11} # No. of letters --> scores
# DIRS stores all the possible directions in which to track the board
DIRS =   [(-1, -1),  (0, -1),    (1, -1),
        (-1, 0),                (1, 0),
        (-1, 1),    (0, 1),     (1, 1)]

def loadDictionary(): # Loads the dictionary, and prefixes
    global DICTIONARY # calls the global dictionary 
    global PREFIXES # calls the global prefixes
    PREFIXES = dict()
    for word in sorted(DICTIONARY):
        node = PREFIXES
        for letter in word:
            if not(letter in node):
                node[letter] = dict()
            node = node[letter]

def isPrefix(prefix): # checks if something is a prefix
    node = PREFIXES
    # Iterates through every prefix
    for character in prefix:
        if not(character in node):
            return False # Returns false if letter is not in the node
        node = node[character]
    return True # otherwose, it returns true

def findWords(board, dimension, usedPositions, prefix, position):
    # Finds all words in a board based on the board itself, dimension,
    # All used positions, the prefix, and current position
    current = prefix + board[position]
    if not isPrefix(current): # No words with this as a prefix
        return set()
    found = set()
    if current in DICTIONARY: # Checks if current route is a word
        found.add(current)
    usedPositions.add(position)
    for offset in DIRS: # Iterates through every offset
        newPosition = (position[0] + offset[0], position[1] + offset[1])
        if newPosition in usedPositions:
            continue
        if (not (0<=newPosition[0]<dimension and 0<=newPosition[1]<dimension)):
            continue
        found.update(findWords(board,dimension,usedPositions,
                        current,newPosition)) # Recursive portion of algorithm
    usedPositions.remove(position) # Removes positions from used positions 
    return found

def solve(board, dimension): # Helper method that calls find words
    answers = set()
    # iterates through the board
    for y in range(dimension):
        for x in range(dimension):
            found = findWords(board, dimension, set(), "", (x, y)) 
            answers.update(found)
    return answers

def boggleBoardSolution(boardDict, boardList):
    # Returns the Solution for a Boggle Board
    dimension = len(boardList) # Dimension of a board
    solutionKey = set() # Set to store a solution key
    loadDictionary() # loads the dictionary to search for possible words
    words = solve(boardDict, dimension)
    totalScore = 0
    for word in sorted(words):
        wordScore = SCORES.get(len(word), SCORES[None])
        totalScore += wordScore
        solutionKey.add(word) # adds words to solution key
    return (solutionKey, totalScore, len(words))

def calculateScore(canvas): # Calculates score based on characters
    totalScore = 0
    words = canvas.data.validUserWords # Makes copy of all valid user words
    for word in sorted(words): # Iterates through all words
        wordScore = SCORES.get(len(word), SCORES[None])
        totalScore += wordScore
    canvas.data.currentScore = totalScore # saves it in the struct
    displayScore(canvas) # Calls helper function to display score 

def findUnmadeWords(canvas): # searches the difference between 
    # User entered words and all possible words that could have been made
    finalList = list() # list to store all those words
    inputWords = list(canvas.data.validUserWords)
    inputWords = sorted(inputWords, key = len, reverse = True)
    unmadeSolution =  list(canvas.data.boggleBoardSolution)
    unmadeSolution = sorted(unmadeSolution, key = len, reverse = True)
    for word in inputWords: # for every valid user word
        unmadeSolution.remove(word) # Remove it from the boggle board solutions
    canvas.data.unmadeSolution = unmadeSolution 
    printSolution(canvas) # Call to helper function for displaying

def convertToDictionary(finalBoard): # Represents the board as a dictionary
        board = finalBoard # Makes local copy of board
        boardDict = dict() # Initialize dict to store values
        # Iterates through every row and column of the board
        for i in xrange(len(board)):
            for j in xrange(len(board[0])):
                boardDict[(i,j)] = (board[i][j]).lower() # Assigns key and ref
        return boardDict

################################################################
############## CODE FOR FLEX GAME SHARING BELOW ################
################################################################

# NOTE: The write file method below has been borrowed from Prof. Kosbie's 
# 15-112 lecture notes. It is used for writing the share.py file to the 
# Game's directory
def writeFile(filename, contents, mode="wt"):
    # wt stands for "write text"
    fout = None
    try:
        fout = open(filename, mode)
        fout.write(contents)
    finally:
        if (fout != None): fout.close()
    return True

def shareGame(root,canvas): # Called when the Flex Game Share button is clicked
    shareData ="shareData ="+str((canvas.data.gameTime,canvas.data.listBoard))
    writeFile("share.py", shareData, mode="wt") # Writes the selections to file
    tkMessageBox.showinfo("FlexMultiplayer", 
    """SHARING THE SAME BOARD WITH SOMEONE 
    _________________________________________\n
    -> The game with the current selections has been saved to the game's
     directory\n
    -> Please look up the file called "share.py" in the folder\n
    -> Then email it to your friend as an attachment""")

def importGame(root, canvas): # Helper function that imports a share.py file
    canvas.delete(ALL)
    importScreenBG = canvas.data.imageDict["importPageBG"]
    canvas.create_image(0,0,anchor = NW, image = importScreenBG)
    canvas.create_text(300, 500, text="LET'S BEGIN -------->",
                        font = "Helvetica 26 bold", fill = "blue")
    footer = "(c) 2013 Aayush Tekriwal."
    canvas.create_text(500, 585, text=footer, font="Helvetica 15 bold")
    canvas.create_window(900, 50, window = canvas.data.gameRules)# Rules dialog
    canvas.create_window(600, 50, window = canvas.data.restartBtn) # RESTART
    canvas.create_window(45, 17, window = canvas.data.quitBtn) # QUIT GAME
    canvas.create_window(605, 500, window = canvas.data.beginBtn) # RESTART

# Runs the import task
def runImportedGame(root, canvas):
    shareData = share.shareData
    performImport(root, canvas, shareData)

# Perform Import helper function replicates the actions that a user would
# otherwise make with the clicks on the menu scree, except, here, it does so
# Based on the data provided by the share.py file
def performImport(root, canvas, shareData):
    canvas.data.gameTime = shareData[0]
    canvas.data.totalTime = canvas.data.gameTime
    canvas.data.dimension = len(shareData[1])
    boardDict = convertToDictionary(shareData[1])
    bbSolution = boggleBoardSolution(boardDict, shareData[1])
    canvas.data.boggleBoardSolution = bbSolution[0]
    canvas.data.totalPossibleScore = bbSolution[1]
    canvas.data.totalPossiblewords = bbSolution[2]
    canvas.data.listBoard = shareData[1]
    canvas.data.displayBoard = shareData[1]
    redrawGame(canvas) # Draws game

#################################################################
################### All Graphics code Below #####################
#################################################################

def setTime(root, canvas, timeInMins): # Sets the game time 
    canvas.delete(ALL) # Deletes all canvas attributes
    initGame(root, canvas) # call to initialize game, and all attributes
    if timeInMins > -1: # If user chooses other than no time limit
        canvas.data.gameTime = (60 * timeInMins)
    canvas.data.totalTime = canvas.data.gameTime
    redrawStartScreen(canvas) # call to refraw main menu screen

def timer(canvas): # timer function to display timer 
    countdown = canvas.data.gameTime # makes copy of game time
    minutes = str(countdown / 60)
    seconds = str(countdown % 60)
    if len(minutes)==1: # Handles single digits
        minutes = "0" + minutes
    if len(seconds) == 1: # Handles single digits
        seconds =  "0" + seconds
    canvas.data.timeDisplay = "%s:%s" % (minutes, seconds)
    canvas.create_rectangle(722,474,942,550, fill="white", width="10")
    canvas.create_text(765, 512, text="TIMER: ", fill="black",
                        font="Helvetica 18 bold")
    canvas.create_text(865, 512, text=canvas.data.timeDisplay, fill="red",
                        font="Helvetica 38 bold")
    percentTimeLeft = (float(float(canvas.data.gameTime)/canvas.data.totalTime))
    # Code below draws the vertical bar timer on the right edge of canvas
    lineLen = 364.0*percentTimeLeft # Length of Timer to be drawn
    canvas.create_line(947, 99, 947, 463, fill = "black", width = 35)
    canvas.create_line(947, 459, 947, 104 , fill = "white", width = 23)
    canvas.create_line(947, 459, 947,lineLen+99,fill = "#CD35D3", width = 23)

def gameOver(canvas): # Helper function that is called when game ends
    canvas.data.gameOver = 1 # sets value of gameover to -1
    drawGameOver(canvas) # calls helper function to draw the new screen

def drawGameOver(canvas): # Helper function that draws the game over screen
    canvas.delete(ALL) # Deletes all contents of canvas, and its attributes
    background = canvas.data.imageDict["gameOverBG"] 
    canvas.create_image(0,0,anchor = NW, image = background) # bg image 
    canvas.create_text(310,22,text="SOME POSSIBLE WORDS THAT WERE NOT ENTERED",
                        font="Chalkduster 20 bold", fill="white")
    boxCoords = (20 , 40 , 610 , 580) # coordinates of words box
    canvas.create_rectangle(boxCoords, fill=None, width="10")
    canvas.create_window(780, 17, window = canvas.data.restartBtn) # Restart 
    canvas.create_window(885, 17, window = canvas.data.quitBtn) # Quit
    drawWordsScoresStats(canvas)
    drawGameOverBoard(canvas)
    findUnmadeWords(canvas)

def drawWordsScoresStats(canvas):
    # Helper function that displays all essential stats in the end of the game
    # such as the user, and total possible scores, and words
    canvas.create_text(750, 60, text="TOTAL POSSIBLE WORDS:", 
                        font="Chalkduster 18 bold", fill = "white")
    canvas.create_text(920, 60,text=canvas.data.totalPossiblewords, 
                        fill="yellow", font="Chalkduster 40 bold")
    canvas.create_text(780, 107, text="YOUR WORDS:", 
                        font="Chalkduster 18 bold", fill = "white")
    canvas.create_text(920, 107,text=len(canvas.data.validUserWords), 
                        fill="yellow", font="Chalkduster 40 bold")
    canvas.create_text(758, 150, text="HIGHEST POSSIBLE SCORE:", 
                        font="Chalkduster 18 bold", fill = "white")
    canvas.create_text(928, 150,text=canvas.data.totalPossibleScore, 
                        fill="yellow", font="Chalkduster 40 bold")
    canvas.create_text(780, 195, text="YOUR SCORE:", 
                        font="Chalkduster 18 bold", fill = "white")
    canvas.create_text(885, 195,text=canvas.data.currentScore, 
                        fill="yellow", font="Chalkduster 40 bold")

def printSolution(canvas): # Helper function that displays all the unmade words
    # On the gameover screen of the canvas
    sortedWords = canvas.data.unmadeSolution 
    maxWords = 80 # Maximum number of words to display on screen
    wordsInCol = 20
    if (len(sortedWords) > maxWords): 
        sortedWords = sortedWords[0:maxWords]
    yOffset = 60
    xOffsets = [70, 200, 330, 460] # offsets for different columns
    numberWords = len(sortedWords)
    cols = (numberWords / wordsInCol)
    for i in xrange(cols): # Iterates through every column
        offsetX = xOffsets[i]
        printWords2(canvas, sortedWords[(i*wordsInCol):((i+1)*wordsInCol)],
                    offsetX, yOffset )

def printWords2(canvas, wordList, xOffset, yOffset): 
    # Printwords 2 is a printwords function that prints on the gameover screen
    wordSpread = 25 # vertical distance between words
    for i in xrange(len(wordList)): # word in sortedWords
        if len(wordList[i])>0:
            word = wordList[i].upper()
            canvas.create_text(xOffset, yOffset, text= word,fill="white",
                    anchor = NW, font="Helvetica 18 ")
        yOffset += wordSpread # increment word space for next word

def drawGameOverCell(characters, row, col, canvas): # Draws each cell of Board
    margin1 = 200 # margin from the edge of the canvas
    margin2 = 4 # Margin to make the table have thicker borders
    cellSize = canvas.data.cellSize # size of a cell of a canvas
    left = margin1 + (col * cellSize)+ 428
    right = left + cellSize
    top = margin1 + (row * cellSize) + 25
    bottom = top + cellSize
    canvas.create_rectangle(left-4, top-4, right+4, bottom+4, fill="#04376C",
                            outline = "#04376C")
    canvas.create_rectangle(left+margin2, top+margin2, right-margin2,
                            bottom - margin2, fill= "#FDF5E6")
    canvas.create_text(left+(cellSize/2), bottom-(cellSize/2), text=characters,
                            font="Helvetica 38 bold")

def drawGameOverBoard(canvas): # Helper Function: Draws the Board
    board = canvas.data.listBoard 
    (rows, cols) = (len(board), len(board))
    if rows == 4:
        canvas.data.cellSize = 90 # Larger cell size when 4x4 board
    else:
        canvas.data.cellSize = 72 # Smaller cell size when 5x5 board
    # Function Iterates through each cell on board, and calls drawcell
    for i in xrange(rows):
        for j in xrange(cols):
            # Calls drawCell to do the job
            drawGameOverCell(board[i][j], i, j, canvas)

def setDimension(canvas): # Helper function that sets the dimension of board
    dimension = canvas.data.dimension
    canvas.data.boggleBoard = BoggleBoard(dimension)
    temp = canvas.data.boggleBoard
    brdDetails = boggleBoardSolution(temp.boardTODictionary, temp.finalBoard)
    canvas.data.boggleBoardSolution = brdDetails[0] # extracts frm brd details
    canvas.data.totalPossibleScore = brdDetails[1]# extracts frm brd details
    canvas.data.totalPossiblewords = brdDetails[2]# extracts frm brd details
    canvas.data.listBoard = temp.finalBoard # saves to struct
    canvas.data.displayBoard = temp.finalBoard # saves to struct
    redrawStartScreen(canvas)

# NOTE: This is a repetition of my own code. I used it in HW 7 :
# For rotating pieces in TETRIS
def rotate2dList(canvas): # rotates a 2D list by 90 degrees
    tempList = canvas.data.listBoard # copies the board
    newList = list()
    # Iterates through the board
    for j in xrange(len(tempList[0])-1,-1,-1):
        tempRow = list()
        for i in xrange(len(tempList)):
            tempRow.append(tempList[i][j]) 
        newList.append(tempRow) # appends new rotated vals to the list
    canvas.data.listBoard = newList
    drawBoard(canvas) # calls helper func to draw the board

def printInstructions(): # Prints all instructions of the game
    tkMessageBox.showinfo("Game Rules", """>>>- RULES OF THE GAME (Boggle) -<<< 
    _________________________________________\n
    -> Each session lasts 1, 3 or 5 minutes (Default: No Time Limit)\n
    -> Construct words from the letters of sequentially adjacent cubes \n
    -> Adjacent cubes: horizontally, vertically, and diagonally neighboring.\n
    -> Words must be three or more letters\n
    -> May include singular and plural separately, but may not repeat the same
    letter cube more than once per word\n
    -> An inbuilt spellchecker is used to verify or refute a word's validity\n
    -> Points are awarded based on word length\n\n
    * 3 or 4 letters = 1 point | 5 letters = 2 points\n
    * 6 letters = 3 points | 7 letters = 4 points\n
    * 8 letters or more = 11 points\n\n
    -> Skill is determined based on the high score for a board""")

def printHelp(canvas): # Prints help info
    pauseResumeTrigger(canvas) # Pauses the game so user does not lose time
                                # while reading the info
    tkMessageBox.showinfo("Boggle Help", """>>>------- BOGGLE HELP -------<<< 
    _________________________________________\n
    -> The remaining time for each session is shown in the countdown timer\n
    -> Click on entry box and enter words \n
    -> Click enter after every word\n
    -> Words in BLACK are VALID\n
    -> Words in RED are INVALID\n
    -> All words are checked with a combination of Webster and Oxford
    English Dictionaries\n
    -> Click the "Pause" button to PAUSE GAME\n
    -> Click the "MAIN MENU" button to return to the Main Menu\n
    -> Click the "ROTATE" button to rotate the board 90 degrees\n
    -> Points are awarded based on the length of the word""")

def getWord(canvas, event): # Takes the word input
    # It was necessary to use try and except because crash conditions 
    # cannot be handled by if conditions
    if not(canvas.data.currentScreen == 2):
        try:
            entry = canvas.data.wordEntry
            temp = str(entry.get()) # converts input to a string
            temp = temp.lower() # converts it to lowe case
            # Conditions below make sure input is withing limits, and valid
            if len(temp)>=3 and len(temp)<=15 and temp.isalpha():
                if checkWord(canvas, temp) == True:
                    canvas.data.validUserWords.add(temp)# adds to valid words
                canvas.data.allUserWords.add(temp) # adds to all User Words
            entry.delete(0 , END) # Empties the entry box for next word
            calculateScore(canvas) # calls helper func to update score
            displayUserWords(canvas) # calls helper func to display new word
        except:
            entry.delete(0 , END) # Empies entry if input is crash prone
        
def checkWord(canvas, word): # checks if a word is valid
    if word in canvas.data.boggleBoardSolution:
        return True # Word is vaid if it is in the solution set
    else:
        return False # Invalid otherwise

def displayScore(canvas): # displays the score of game so far
    boxCoords = (540,475,700,550)
    canvas.create_rectangle(boxCoords, fill="white", width="10")
    canvas.create_text(585, 513, text="SCORE: ", font="Helvetica 18 bold")
    currentScore = canvas.data.currentScore # copies current game score
    textCoord = (660, 510) 
    canvas.create_text(textCoord,text=currentScore, fill="red",
                         font="Helvetica 40 bold")

def displayUserWords(canvas):
    # Helper function that displays all the User enteres words on the canvas
    boxCoords = (55 , 185 , 420 , 550)
    canvas.create_rectangle(boxCoords, fill="#FFC773", width="10")
    canvas.create_line(245,185, 245, 550, width = 5) # Separator of cols 
    allWords = list(canvas.data.allUserWords)
    sortedWords = sorted(allWords)
    validWords = canvas.data.validUserWords
    (xOffset, yOffset) = (90, 190)
    altxOffset = 277 # alternate x offset, for spacing out second column
    if len(sortedWords) < 20: # displays only 20 words in a column
        printWords(canvas, sortedWords, validWords, xOffset, yOffset)
    else: # second column
        printWords(canvas,sortedWords[:19], validWords, xOffset, yOffset)
        printWords(canvas,sortedWords[19:38],validWords, altxOffset, yOffset)

def printWords(canvas, wordList,validWords, xOffset, yOffset):
    # Helper function that does the job of printing the words
    for i in xrange(len(wordList)): # Iterates every user entered word
        if len(wordList[i]) > 0:
            if (wordList[i] in validWords):
                canvas.create_text(xOffset, yOffset, text= wordList[i], 
                            anchor = NW, font="Helvetica 18 ")
            else:
                canvas.create_text(xOffset, yOffset, text= wordList[i],
                            fill="red", anchor = NW, font="Helvetica 18 ")
        yOffset +=18 # separate each word by 18 units

def comboFunc(root, canvas): # Combined function 
    initGame(root, canvas)  # Initializes the game
    canvas.data.isGameOver = True # Sets gameover to true

def markCurrentTimeSelection(canvas):
    # Helper function that marks current time selection with a blue box 
    # in the Background
    time = canvas.data.gameTime # copies the time selected
    if canvas.data.gameTime > 0: # Means the time is either 1, 3, or 5 mins
        time = canvas.data.gameTime / 60
    if time == -1:
        canvas.create_rectangle(395, 312, 516, 368, fill = "#86B32D",
                            outline = "#86B32D") # If no time limit
    elif time == 1:
        canvas.create_rectangle(515, 312, 636, 368, fill = "#86B32D",
                            outline = "#86B32D") # If 1 min chosen
    elif time == 3:
        canvas.create_rectangle(635, 312, 756, 368, fill = "#86B32D",
                            outline = "#86B32D") # If 3 mins chosen
    elif time == 5:
        canvas.create_rectangle(755, 312, 875, 368, fill = "#86B32D",
                            outline = "#86B32D") # If 5 mins chosen

def markCurrentBoardSelection(canvas): 
    # Helper function that marks the board selection, just like time selection
    dimensions = canvas.data.dimension
    if dimensions == 4: # If dimension chosen = 4
        canvas.create_rectangle(515, 404, 684, 460, fill = "#86B32D",
                            outline = "#86B32D")
    elif dimensions == 5: # if dimension chosen = 5
        canvas.create_rectangle(695, 404, 866, 460, fill = "#86B32D",
                            outline = "#86B32D")

# NOTE: This code is very similar to my draw cell function for TETRIS
def drawCell(characters, row, col, canvas): # Draws each cell of Board
    margin1 = 100
    margin2 = 4 # Margin to make the table have thicker borders
    cellSize = canvas.data.cellSize #canvas.data.cellSize
    left = margin1 + (col * cellSize) + 432 # 432 = distance from left edge 
                                            # of the canvas
    right = left + cellSize
    top = margin1 + (row * cellSize)
    bottom = top + cellSize
    canvas.create_rectangle(left-4, top-4, right+4, bottom+4, fill="#04376C",
                            outline = "#04376C")
    canvas.create_rectangle(left+margin2, top+margin2, right-margin2,
                            bottom - margin2, fill= "#FDF5E6")
    canvas.create_text(left+(cellSize/2), bottom-(cellSize/2), text=characters,
                            fill="black", font="Helvetica 38 bold")

# NOTE: This code is very similar to my drawBoard function for TETRIS
def drawBoard(canvas): # Helper Function: Draws the Board
    board = canvas.data.listBoard 
    (rows, cols) = (len(board), len(board)) # Finds out rows and cols
    if rows == 4: # If its a 4x4 game
        canvas.data.cellSize = 90
    else: # If its a 5x5 game
        canvas.data.cellSize = 72
    # Function Iterates through each cell on board, and calls drawcell
    for i in xrange(rows):
        for j in xrange(cols):
            drawCell(board[i][j], i, j, canvas) # Calls drawCell to do the job

def drawAbout(canvas): # Draws the About page
    canvas.delete(ALL) 
    aboutPageBG = canvas.data.imageDict["aboutPageBG"] # The image background
    canvas.create_image(0,0, anchor = NW, image = aboutPageBG)
    canvas.create_text(500, 320, text="Release Version 1.0", fill = "#DCFA71",
                        font="Helvetica 40 bold")
    canvas.create_text(500, 378, text="Developed By: Aayush Tekriwal",
                                fill = "white", font="Helvetica 30 bold")
    canvas.create_text(500, 438, text="15-112 --> Carnegie Mellon University",
                                fill = "white", font="Helvetica 30")
    footer = "(c) 2013 Aayush Tekriwal. All rights reserved."
    canvas.create_text(500, 600, text=footer, anchor = S, fill="white", 
                                font="Helvetica 15 bold")
    canvas.create_window(45, 17, window = canvas.data.quitBtn) # Quit button
    canvas.create_window(520, 540, window = canvas.data.backBtn) # Back button

def redrawGame(canvas): # Draws the Main Game
    canvas.delete(ALL)
    canvas.data.currentScreen = 1 # Sets flag to game screen
    gameBG = canvas.data.imageDict["background2"]
    canvas.create_image(0,0,anchor = NW, image = gameBG) # Game background
    (footer, boxCoords) = ("(c) 2013 Aayush Tekriwal.",(55 , 185 , 420 , 550)) 
    canvas.create_text(500, 585, text=footer, font="Helvetica 15 bold")
    canvas.create_rectangle(boxCoords, fill="#FFC773", width="10")
    canvas.create_line(245,185, 245, 550, width = 5)
    drawGameButtons(canvas) # draws all the buttons
    canvas.create_window(400, 50, window = canvas.data.pauseBtn)
    canvas.create_window(240, 160, window = canvas.data.wordEntry)
    canvas.create_window(480, 275, window = canvas.data.rotateBtn)
    drawDormantTimerAndScore(canvas)
    if canvas.data.gameTime == -1:
        canvas.create_window(830, 510, window = canvas.data.endBtn)
    if (canvas.data.gameTime > -1): timerFired(canvas)
    displayUserWords(canvas)
    drawBoard(canvas)

def drawDormantTimerAndScore(canvas):
    canvas.create_oval(540,475,700,550, fill="white", width="10")
    canvas.create_text(585, 513, text="SCORE: ", font="Helvetica 18 bold")
    canvas.create_oval(722,474,942,550, fill="white", width="10")

def drawGameButtons(canvas): 
    # draws buttons common to game and pause screens
    canvas.create_window(900, 50, window = canvas.data.gameRules)# Rules dialog
    canvas.create_window(750, 50, window = canvas.data.helpBtn)# Help dialog
    canvas.create_window(600, 50, window = canvas.data.restartBtn) # RESTART
    canvas.create_window(45, 17, window = canvas.data.quitBtn) # QUIT GAME

def pauseResumeTrigger(canvas): 
    # Helper function that pauses and resumes game
    canvas.data.isPaused = not canvas.data.isPaused # Reverses the state
    if canvas.data.isPaused == True: 
        displayPausedBoard(canvas) # Pause if true
    else:
        redrawGame(canvas) # Resume game if false

def displayPausedBoard(canvas): # Helper Function: Display Paused Board
    canvas.delete(ALL)
    pauseBG = canvas.data.imageDict["background1"] # Paused game background
    canvas.create_image(0,0,anchor = NW, image = pauseBG)
    footer = "(c) 2013 Aayush Tekriwal."
    canvas.create_text(500, 585, text=footer, font="Helvetica 15 bold")
    boxCoords = (55 , 185 , 420 , 550)
    canvas.create_rectangle(boxCoords, fill="gray", width="10")
    canvas.create_line(245,185, 245, 550, width = 5)
    drawGameButtons(canvas) #  Draws all necessart buttons
    canvas.create_window(715, 283, window = canvas.data.resumeBtn) # RESUME 
    canvas.create_oval(540,475,700,550, fill="gray", width="10")
    canvas.create_text(585, 513, text="SCORE: ", font="Helvetica 18 bold")
    canvas.create_oval(722,474,942,550, fill="gray", width="10")
    canvas.create_rectangle(539, 108, 888, 458, fill="gray", width="10")

def redrawStartScreen(canvas): # Draws the Main Menu screen
    canvas.delete(ALL)
    canvas.data.currentScreen = 2 #Sets default flag to anything but gamescreen
    drawStartScreenButtons(canvas)
    startScreenBG = canvas.data.imageDict["background1"]
    canvas.create_image(0,0,anchor = NW, image = startScreenBG)
    canvas.create_rectangle(160,310,940,370, fill="#1E66B0",
                        outline="white", width="3")
    canvas.create_text(270, 340, text="GAME TIME :",
                        font = "Helvetica 26 bold")
    markCurrentTimeSelection(canvas)
    canvas.create_rectangle(160,402,940,462, fill="#1E66B0",
                        outline="white", width="3")
    canvas.create_text(270, 435, text="BOARD :", font = "Helvetica 26 bold")
    canvas.create_text(430, 435, text="( DEFAULT : 4x4 )", fill="white", 
                        font = "Helvetica 15 bold")
    markCurrentBoardSelection(canvas)
    canvas.create_text(300, 500, text="LET'S BEGIN -------->",
                        font = "Helvetica 26 bold")
    footer = "(c) 2013 Aayush Tekriwal."
    canvas.create_text(500, 585, text=footer, font="Helvetica 15 bold")

def drawStartScreenButtons(canvas):
    # Displays all the buttons required on the start screen
    # Magin numbers inevitable because there are many buttons
    canvas.create_window(45, 17, window = canvas.data.quitBtn) # QUIT
    canvas.create_window(690, 80, window = canvas.data.aboutBtn) # PAUSE
    canvas.create_window(690, 165, window = canvas.data.instructionsBtn)#INSTR
    canvas.create_window(690, 250, window = canvas.data.importGameBtn)#INSTR
    canvas.create_window(815, 340, window = canvas.data.fiveMinuteBtn)# 5 min
    canvas.create_window(695, 340, window = canvas.data.threeMinuteBtn)# 3 min
    canvas.create_window(575, 340, window = canvas.data.oneMinuteBtn)# 1 min
    canvas.create_window(455, 340, window = canvas.data.noTimeBtn)# No limit
    canvas.create_window(600, 435, window = canvas.data.fourByFourBtn)# 4x4
    canvas.create_window(780, 435, window = canvas.data.fiveByFiveBtn)# 5x5
    canvas.create_window(690, 520, window = canvas.data.startGameBtn)# PLAY
    canvas.create_window(280, 537, window = canvas.data.shareBtn) # SHARE

#################################################################
########## Loading and variable Initializing Code Below #########
#################################################################

def initAllVariables(root, canvas): # Calls all init functions
    # INIT BUTTONS
    initButtonDefaults(canvas)
    # INIT BOARD AND DISPLAY VALUES
    initBoardAndDisplayValues(canvas)
    # INIT GAME VALUES
    initGameValues(canvas)

def initButtonDefaults(canvas): # Initialized defaults for buttons
    canvas.data.scoresBtn = 0
    canvas.data.fourByfourBtn = canvas.data.fiveByFiveBtn = 0
    canvas.data.instructionsBtn = 0
    canvas.data.startGameBtn = 0
    canvas.data.helpBtn = 0
    canvas.data.quitBtn = 0
    canvas.data.gameRules = 0
    canvas.data.restartBtn = 0
    canvas.data.aboutBtn = 0
    canvas.data.noTimeBtn = 0
    canvas.data.backBtn = 0
    canvas.data.rotateBtn = 0

def initBoardAndDisplayValues(canvas):
    canvas.data.currentScreen = 2
    canvas.data.countdown = 0
    canvas.data.currentScore = 0
    canvas.data.gameTime = -1
    canvas.data.totalTime = canvas.data.gameTime
    canvas.data.dimension = 4 # Default dimensions of a boggle game
    canvas.data.timeRemaining = 0  
    #------
    canvas.data.boggleBoard = 0 # instance of class, Not a useful variable
    canvas.data.listBoard = 0
    canvas.data.displayBoard = canvas.data.listBoard
    canvas.data.boggleBoardSolution = 0
    canvas.data.totalPossiblewords = 0
    canvas.data.totalPossibleScore = 0

def initGameValues(canvas): # Initialized gane values and flags
    canvas.data.wordEntry = 0
    canvas.data.playerNameEntry = 0
    canvas.data.validUserWords = set()
    canvas.data.allUserWords = set()
    canvas.data.cellSize = 0
    canvas.data.gameOver = 0
    canvas.data.unmadeSolution = 0
    canvas.data.ignoreNextTimerEvent = False
    canvas.data.isGameOver = False
    canvas.data.isPaused = False

def dimensionCombo(canvas,dimension): # A combo function called while setting
                                      # The dimension
    canvas.data.dimension = dimension 
    setDimension(canvas)

def loadImages(canvas):
    # NOTE: Boggle Bash logo was borrowed from the link below:
    # http://cdn.pogo.com/v/FAiFmw/img/game-thumbs/en/tn-huge-boggle.png
    # NOTE: Play Game button image was borrowed from the link below:
    # http://newproject.reprospective.co.uk/wp-content/uploads/2013/
    # 01/play_button.png
    canvas.data.imageDict = dict()
    canvas.data.imageDict["background1"] = PhotoImage(file = "bg1gif.gif")
    canvas.data.imageDict["background2"] = PhotoImage(file = "bg2gif.gif")
    canvas.data.imageDict["buttonImage"] = PhotoImage(file = "playButton.gif")
    canvas.data.imageDict["aboutPageBG"] = PhotoImage(file = "aboutPageBG.gif")
    canvas.data.imageDict["gameOverBG"] = PhotoImage(file = "gameOver.gif")
    canvas.data.imageDict["importPageBG"] = PhotoImage(file = "importGIF.gif")

def initGame(root, canvas): # Initializes all the variables and attributes
    initAllVariables(root, canvas)
    loadImages(canvas) # Loads images
    initTimeSelectionBtns(root, canvas)
    initBoardSelectionBtns(root, canvas)
    initGameStateBtns(root, canvas)
    initFeatureBtns(root, canvas)
    initShareImportBtns(root, canvas)
    wordEntry = Entry(root, width = 40)
    canvas.data.wordEntry = wordEntry
    wordEntry.focus()
    setDimension(canvas) # Sets board dimension
    canvas.pack() 
    redrawStartScreen(canvas) # Redraws the start screen

def initShareImportBtns(root, canvas): # Draws the share and import btns
    shareBtn = Button(canvas, text ="FLEX GAME SHARE", 
                    command=lambda: shareGame(root,canvas)) # THE SHARING FTR
    shareBtn.configure(width = 20)
    canvas.data.shareBtn = shareBtn # STORES BUTTON IN STRUCT
    # importGameBtn takes the user to the import Game Screen
    importGameBtn = Button(canvas, text ="IMPORT GAME", 
                        command=lambda: importGame(root,canvas))
    importGameBtn.configure(width = 25) 
    canvas.data.importGameBtn = importGameBtn 
    # The begin button runs the imported game
    beginBtn = Button(canvas, text ="BEGIN", 
                    command=lambda: runImportedGame(root,canvas))
    beginBtn.configure(width = 20)
    canvas.data.beginBtn = beginBtn 

def initTimeSelectionBtns(root, canvas): # Inits buttons for time selection
    fiveMinuteBtn = Button(canvas, text ="5 Minutes", 
                        command = lambda: setTime(root,canvas, 5))
    fiveMinuteBtn.configure(width = 10) # 5 Mins
    canvas.data.fiveMinuteBtn = fiveMinuteBtn 
    threeMinuteBtn = Button(canvas, text = "3 Minutes",
                        command = lambda: setTime(root,canvas, 3))
    threeMinuteBtn.configure(width = 10)
    canvas.data.threeMinuteBtn = threeMinuteBtn # 3 Mins
    oneMinuteBtn = Button(canvas, text = "1 Minute",
                        command = lambda: setTime(root, canvas, 1))
    oneMinuteBtn.configure(width = 10)
    canvas.data.oneMinuteBtn = oneMinuteBtn # 1 Min
    noTimeBtn = Button(canvas, text = "No Limit",
                        command = lambda: setTime(root, canvas, -1))
    noTimeBtn.configure(width = 10)
    canvas.data.noTimeBtn = noTimeBtn # No Time Limit
    endBtn = Button(text = "END GAME !", command = lambda:gameOver(canvas))
    endBtn.configure(width = 18)
    canvas.data.endBtn = endBtn # End Game

def initBoardSelectionBtns(root, canvas): # Inits buttons to do with Board
    fourByFourBtn = Button(canvas, text = "4 X 4", 
                command = lambda: dimensionCombo(canvas, 4))#setDimension(4))
    fourByFourBtn.configure(width = 15)
    canvas.data.fourByFourBtn = fourByFourBtn
    fiveByFiveBtn = Button(canvas, text = "5 X 5",
                command = lambda: dimensionCombo(canvas, 5)) #setDimension(5))
    fiveByFiveBtn.configure(width = 15)
    canvas.data.fiveByFiveBtn = fiveByFiveBtn
    rotateBtn = Button(text = "ROTATE", command = lambda:rotate2dList(canvas))
    rotateBtn.configure(width = 6)
    canvas.data.rotateBtn = rotateBtn

def initGameStateBtns(root, canvas): # Inits buttons to do with game state
    buttonImg = canvas.data.imageDict["buttonImage"]
    startGameBtn = Button(image=buttonImg,command =lambda: redrawGame(canvas))
    startGameBtn.image = buttonImg # PLAY BUTTON
    canvas.data.startGameBtn = startGameBtn 
    restartBtn = Button(text="MAIN MENU",command=lambda:comboFunc(root,canvas))
    restartBtn.configure(width = 12)
    canvas.data.restartBtn = restartBtn # RESTART
    Style().configure('red.TButton', foreground='red')
    quitBtn = Button(text = "QUIT", style='red.TButton', command = quit)
    quitBtn.configure(width = 5)
    canvas.data.quitBtn = quitBtn # QUIT
    pauseBtn = Button(text = "PAUSE", style='red.TButton',
                    command = lambda: pauseResumeTrigger(canvas))
    pauseBtn.configure(width = 12)
    canvas.data.pauseBtn = pauseBtn # PAUSE
    resumeBtn = Button(text = "RESUME", style='red.TButton',
                    command=lambda: pauseResumeTrigger(canvas))
    resumeBtn.configure(width = 30) 
    canvas.data.resumeBtn = resumeBtn # RESUME

def initFeatureBtns(root,canvas): # Inits buttons to do with game features
    instructionsBtn = Button( text = "GAME INSTRUCTIONS",
                    command = printInstructions)
    instructionsBtn.configure(width = 30)
    canvas.data.instructionsBtn = instructionsBtn # Displays Instructions
    gameRules = Button( text = "GAME RULES !",
                    command=printInstructions)
    gameRules.configure(width = 10)
    canvas.data.gameRules = gameRules # Displays Game Rules
    helpBtn = Button( text = "HELP !", command = lambda: printHelp(canvas))
    helpBtn.configure(width = 10)
    canvas.data.helpBtn = helpBtn # Displays Help Instructions
    Style().configure('blue.TButton', foreground='blue')
    aboutBtn = Button(text = "ABOUT", style='blue.TButton',
                    command=lambda: drawAbout(canvas))
    aboutBtn.configure(width = 30)
    canvas.data.aboutBtn = aboutBtn # Displays about screen
    backBtn = Button(text = "BACK",command=lambda: initGame(root, canvas))
    backBtn.configure(width = 15)
    canvas.data.backBtn = backBtn # Displays back button

#################################################################
##### Code for detecting coordinates on canvas (Development) ####
#################################################################

def printCoords(event): # Helper function, used only for locating graphics
    print "x = "+str(event.x) # Prints x coordinate, of mouse click
    print "y = "+str(event.y) # Prints y coordinate, or mouse click
    print "------"

#################################################################
###### Run and TimerFired - Controls game events and timer ######
#################################################################

def timerFired(canvas): # Helper func: Controls timer, and game states
    delay = 1000 # Milliseconds in a second
    ignoreThisTimerEvent = canvas.data.ignoreNextTimerEvent
    canvas.data.ignoreNextTimerEvent = False
    if (canvas.data.gameTime == 0): # If countdown is over
        gameOver(canvas)
    elif(canvas.data.isPaused == True and canvas.data.isGameOver == False):
        # If game is paused but not over
        displayPausedBoard(canvas) # show Pause screen
    elif (canvas.data.isGameOver == False and canvas.data.isPaused == False and
            canvas.data.gameTime >= 0 ): # If game's running
        if (ignoreThisTimerEvent == False):
            timer(canvas) # call timer
            canvas.data.gameTime -=1 # reduce seconds left by 1
            canvas.after(delay,timerFired,canvas)
    else:
        return

def run(): # Main function that triggers the rest of the game
    root = Tk() # Initializes a new root
    root.resizable(width = FALSE, height = FALSE) # The canvas is not resizable
    root.title("Boggle - Aayush Tekriwal - (15-112 Term Project)") # Title
    (width, height) = (1000,600) # Width and height of 
    canvas = Canvas(root, width = width, height = height)
    canvas.pack()
    root.canvas = canvas.canvas = canvas
    class Struct: pass
    canvas.data = Struct() # Struct stores all data for global access
    canvas.data.width = width
    canvas.data.height = height
    initGame(root, canvas) 
    #root.bind("<Button-1>", printCoords) # Unhash to help modify graphics
    root.bind("<space >", lambda event: getWord(canvas, event))
    root.bind("<Return>", lambda event: getWord(canvas, event))
    root.mainloop()

run() # Triggers the GAME
