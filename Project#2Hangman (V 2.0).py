# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 17:02:21 2024

This is the homework code for the project "Hangman"
The game offers two play modes.
    1. Against the computer and 
    2. Against a fellow human
An added feature of the game is that after completion it starts again and 
updates a list of the winners. That is,it is possible to play it indeffinately 
unless the player decides to quit

@author: Baya
"""

from random import choice
import os


"""Below is a dictionary from which the computer chooses the words that it 
enters in the game for the player to guess"""
    
dictList = ['APPLE','BANANA','ORANGE','GRAPE','LEMON','CHERRY','PEACH','MELON',
            'BERRY','PEAR','ANT','BEAR','CAT','DOG','FROG','HORSE','LION',
            'TIGER','ZEBRA','SHARK','PLANE','AIR','WATER','FIRE','EARTH','WIND',
            'STORM','CLOUD','SKY','RAIN','SNOW','CROCODILE','BOOK','PEN',
            'PENCIL','PAPER','ERASER','CHAIR','TABLE','DESK','SHELF','BOARD',
            'CAR','TRUCK','TRAIN','PLANE','BOAT','SHIP','BIKE','SCOOTER','BUS',
            'VAN','HOUSE','ROOM','DOOR','WINDOW','WALL','FLOOR','CEILING','ROOF',
            'GARDEN','FENCE','RIVER','LAKE','OCEAN','STREAM','POND','BEACH',
            'HILL','MOUNTAIN','VALLEY','DESERT','TREE','FLOWER','GRASS','LEAF',
            'BRANCH','ROOT','SEED','FRUIT','BARK','FOREST','SHOE','HAT','SHIRT',
            'PANTS','DRESS','COAT','BELT','SOCK','GLOVE','SCARF','BREAD','MILK',
            'CHEESE','BUTTER','MEAT','RICE','PASTA','SOUP','SUGAR','SALT','CUP',
            'PLATE','BOWL','SPOON','FORK','KNIFE','GLASS','POT','PAN','KETTLE',
            'TIME','DAY','NIGHT','WEEK','MONTH','YEAR','MORNING','EVENING',
            'NOON','MIDNIGHT','FRIEND','FAMILY','PARENT','CHILD','BROTHER',
            'SISTER','UNCLE','AUNT','COUSIN','NEIGHBOR','CITY','TOWN','VILLAGE',
            'STREET','ROAD','BRIDGE','PARK','SQUARE','MARKET','HARBOR','MUSIC',
            'SONG','DANCE','NOTE','BEAT','DRUM','GUITAR','PIANO','VIOLIN',
            'VOICE','LIGHT','DARK','COLOR','SHADE','SHAPE','LINE','CIRCLE',
            'SQUARE','TRIANGLE','STAR','COLD','HOT','WARM','COOL','DRY','WET',
            'SOFT','HARD','ROUGH','SMOOTH','JUMP','RUN','WALK','CLIMB','SWIM',
            'FLY','SIT','STAND','SLEEP','EAT','HAPPY','SAD','ANGRY','CALM',
            'TIRED','EXCITED','BORED','SCARED','PROUD','BRAVE','SCHOOL','TEACHER',
            'STUDENT','CLASS','LESSON','HOMEWORK','EXAM','TEST','SUBJECT','GRADE'
            ,'COMPUTER','PHONE','SCREEN','KEYBOARD','MOUSE','TABLET','CAMERA',
            'PRINTER','CABLE','CHARGER','ANIMAL','HUMAN','PLANT','FISH','BIRD',
            'INSECT','REPTILE','MAMMAL','AMPHIBIAN','CREATURE','ENERGY','POWER',
            'LIGHT','HEAT','SOUND','MOTION','FORCE','SPEED','STRENGTH','WEIGHT',
            'STONE','ROCK','SAND','CLAY','SOIL','DUST','GLASS','METAL','PLASTIC',
            'WOOD','TOOL','HAMMER','SAW','DRILL','WRENCH','NAIL','SCREW','PLIERS',
            'BLADE','TAPE','TOY','BALL','DOLL','PUZZLE','GAME','KITE','BALLOON',
            'CAR','ROBOT','BLOCK','FOOD','DRINK','FRUIT','VEGETABLE','MEAT',
            'GRAIN','SNACK','CANDY','ICE','SAUCE','MONEY','COIN','CASH','BANK',
            'WALLET','CARD','BILL','PRICE','SHOP','MARKET','MAP','FLAG','SIGN',
            'SIGNAL','CHART','GRAPH','SYMBOL','CODE','LETTER','NUMBER','WORK',
            'JOB','TASK','GOAL','PLAN','IDEA','SKILL','TOOL','TEAM','PROJECT',
            'HEALTH','BODY','MIND','HEART','BONE','MUSCLE','BLOOD','SKIN','ORGAN',
            'LOVE','HATE','FEAR','HOPE','JOY','PAIN','DREAM','WISH','CARE',
            'THOUGHT','FISH','CRAB','SHRIMP','WHALE','SEAL','OTTER','EEL',
            'ELEPHANT','DOLPHIN','TURTLE','CLAM','LAMP','FAN','LIGHT','SWITCH',
            'PLUG','BULB','WIRE','CORD','SOCKET','BATTERY','WAR','PEACE','FIGHT',
            'ARMY','SOLDIER','WEAPON','TANK','BOMB','PLANE','MISSILE','BOOK',
            'LIBRARY','AUTHOR','STORY','NOVEL','POEM','PAGE','CHAPTER','TITLE',
            'WORD','EARTH','MOON','SUN','STAR','PLANET','COMET','ASTEROID',
            'GALAXY','SPACE','UNIVERSE','DOCTOR','NURSE','PATIENT','MEDICINE',
            'PILL','CURE','TREATMENT','HOSPITAL','CLINIC','HEALTH','FRIEND',
            'ENEMY','ALLY','PARTNER','STRANGER','VISITOR','NEIGHBOR','RIVAL',
            'GUEST','LEADER','MUSIC','ART','DANCE','SPORT','GAME','PLAY','SONG',
            'TUNE','BAND','STAGE','KEY','LOCK','DOOR','GATE','WALL','ROOF',
            'FLOOR','STAIRS','WINDOW','ROOM']


def drawMan(s,guessedWord,wrongWord):
    """This function draws the hang man based on the progress of player 2"""
    def easy(s): # Easy level
        print("     _______")
        print("     "+s[0]+"     |")
        print("     "+s[1]+"     |")
        print("    "+s[3] + s[2] + s[4]+"    |")
        print("   "+s[6] + " "+s[5]+" "+s[7]+"   |")
        print("     "+s[8] + "     |")
        print("    "+s[9]+" "+s[10]+"    |")
        print("   "+s[11]+"   "+s[12]+"   |")
        print("   "+s[13]+"   "+s[14]+"   |")
        print("  "+s[16]+s[15]+"   "+s[17]+s[18]+"  |")
        print("           |")
        print("   ________|____\n")
        print("")
        
        
    def hard(s): # Hard level
        print("     _______")
        print("     "+s[0]+"     |")
        print("     "+s[1]+"     |")
        print("    "+s[3] + s[2] + s[4]+"    |")
        print("     "+s[5]+"     |")
        print("     "+s[6] + "     |")
        print("    "+s[7]+" "+s[8]+"    |")
        print("   "+s[10]+s[9]+" "+s[11]+s[12]+"   |")
        print("           |")
        print("   ________|____\n")
        print("")
        
    easy(s) if dif[0] == 1 else hard(s)
    gWord = wWord = ""
    for let in guessedWord:
        gWord += let + " "
    for let in wrongWord:
        wWord += let + " "
    print("Progress so far:",gWord)
    print("")
    print("Wrong letters so far:",wWord)
    print("")


def guess(collector):
    """This function updates all the variables that need to be
    updated when player 2 guesses a letter"""
    s = collector[0]
    wrongWord = collector[1]
    guessedWord = collector[2]
    wordList = collector[3]
    fullMan = collector[4]
    letter = input("Enter one letter at a time: ").upper()
    if letter in guessedWord or letter in wrongWord:
        print("You have already entered", letter + ". Try again", end = " ")
        # Ideally,this should move the cursor up 2 lines
        # print("\033[2A",end="")
        # print("\r") # I don't yet know why it doesn't work...
        return guess(collector)
    if len(letter) != 1:
        # The player should only enter 1 letter at a time
        return guess(collector)
    for num in range(len(wordList)):
        if wordList[num] == letter:
            # Updates the correct letter in the guessed word
            guessedWord[num] = letter

    if letter not in wordList:
        wrongWord.append(letter)
        for num in range(len(wrongWord)):
            s[num] = fullMan[num]
    os.system('cls' if os.name == 'nt' else 'clear')
    drawMan(s,guessedWord,wrongWord)
    return [s,wrongWord,guessedWord,wordList,fullMan]


def checkWin(col): # s,wrongWord,guessedWord,wordList,fullMan
    """This function checks if there is a winner and then returns either True
    or False to allow the program to continue or stop"""
    word = ''
    for let in col[3]:
        word += let + ' '
    if col[2] == col[3]:
        winCount[1] += 1
        print(player[1],"won and saved the man.\nThe word is:   ", word)
        print("Statistics are:\n" + player[0] + ":",winCount[0],"\n" +
              player[1] + ":", winCount[1])
        input("\nPress enter to continue")
        return True
    elif col[2] != col[3] and col[0] == col[4]:
        winCount[0] += 1
        print("Player 1 has won.\nThe word was:  ", word)
        print("Statistics are:\n" + player[0] + ":",winCount[0],"\n" +
              player[1] + ":", winCount[1])
        input("\nPress enter to continue")
        return True
    else:
        return False


def gameLauncher(dictList):
    print('Press 1 for 2-player mode or\n"enter"',
          'to play against the computer',end = " ")
    sel = input()
    sel = int(sel) if sel.isdecimal() else sel
    print('\nSelect level of difficulty\nPress 1 for Easy or "enter" for hard')
    dif[0] = input()
    dif[0] = int(dif[0]) if dif[0].isdecimal() else dif[0]
    while True:
        if sel != 1:
            player[0],player[1] = "Computer","You"
            wordList = list(choice(dictList))
        else:
            player[0],player[1] = "Player 1","Player 2"
            print("Player 1 will enter a word and Player 2 will start guessing it")
            # Collect the input and ensure it is in upper case letters
            wordList = list(input("Player 1 please enter the word: ").upper()) 
        os.system('cls' if os.name == 'nt' else 'clear')
    
        if dif[0] == 1:
            fullMan = ['|', '⁠O', '|', '_', '_', '|', '/',
                       '\\', 'A', '/', '\\', '/', '\\', '|',
                       '|', '|', '_', '|', '_']
            """These are the characters that will be used to draw the hanging man"""
        else:
            fullMan = ['|', '⁠O', '|', '_', '_', '|', 'A', 
                       '/', '\\', '|', '_', '|', '_']
            
        # The following lists will come in handy later in the execution.
        s = []  # The variable that contains the data for the hangman to be displayed
        wrongWord = []
        guessedWord = []
        for num in range(len(fullMan)):
            s.append(" ")  # This populates the s[] with " "
    
        for num in range(len(wordList)):
            guessedWord.append(
                " ") if wordList[num] == " " else guessedWord.append("_")
            # If the character is " ",then there is no need to guess it.
    
        collector = [s,wrongWord,guessedWord,wordList,fullMan]
        while not checkWin(collector):  # Only run if there is no winner
            collector = guess(collector)  # Collect the variables from the function


print("Welcome to this minimalist 'Hangman game'")
player = [" ", " "]
winCount = [0, 0]
dif = [1]
gameLauncher(dictList)