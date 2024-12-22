#!/usr/bin/env python
# coding: utf-8

# -*- coding: utf-8 -*-
"""
## Created on Tue Dec 10 00:07:25 2024

This is the final exam for the 'Pythin is Easy Class'

I chose to work with the Freecell card game due to the love that I have
for it. I also believe that it'll be a good challenge for me

Basically, the Freecell is a single player game and it doesn't depend on luck. 
Winning depends on the player's strategy, tactics, and the dealt deck.

It uses the following rules:
    1. The goal is to move all cards to the foundation pile/home.
       The cards must be arranged in their suits from A, 2...10, J, Q, K
    2. The freecells can hold any one card at a time
    3. The cards can be arranged in the columns in alternating colors
       from K, Q, J, 10, ... 2, A. That is, a black card can
       only be placed on a red one in descending order, and vice versa
    4. A column remains empty when the last card is removed from it
    5. Any card can be moved to an empty column
    6. The number of cards that can be moved to a different column 
       depends on the number of freecells and empty columns.
       You cannot move more cards than the availability of 
       space to hold the cards being moved.(Freecells or empty columns)


@author: Baya

"""


from os import system, name
from random import shuffle
from sys import exit
from time import sleep, time


# Self explanatory 
def printHelp(lim):
    help = """

This is the FreeCell game. It uses the following rules:

1.  The goal is to move all cards to the foundation pile/home. The cards must be arranged in their suits from A, 2...10, J, Q, K
    
2.  The freecells can hold any one card at a time

3.  The cards can be arranged in the columns in alternating colors from K, Q, J, 10, ... 2, A. That is, a black card can only be placed on a red one in descending order, and vice versa

4.  A column remains empty when the last card is removed from it

5.  Any card can be moved to an empty column

6.  The number of cards that can be moved to a different column depends on the number of freecells and empty columns. You cannot move more cards than the availability of space to hold the cards being moved. (Freecells or empty columns)
"""
    print(help, "\nEnter '--resume' to continue with the game")
    entry = input().upper()
    if entry == "--resume".upper() or entry == "resume".upper():
        return inTake(lim)
    else:
        printHelp(lim)


# Creates a new deck of 52 cards in all their 4 suits
def createDeck():
    '''This function creates the deck of 52 cards complete
    with their symbols'''
    suit  = ['♥', '♦', '♣', '♠']
    cardTemplate = []
    # This created a template that will represent the card deck of 52 cards
    for num in range(1, 14):
        if num == 1:
            cardTemplate.append('A')
        elif num == 11:
            cardTemplate.append('J')
        elif num == 12:
            cardTemplate.append('Q')
        elif num == 13:
            cardTemplate.append('K')
        else:
            cardTemplate.append(str(num))

    # Here we give the cards the suit  symbols
    cardDeck = []
    for symbol in suit :
        for num in range(len(cardTemplate)):
            cardDeck.append(cardTemplate[num] + symbol)

    return cardDeck


# Prints the freecells and foundation pile as in a natural Free Cell game
def printHeader():
    """Prints the freecell and home"""
    red = "\033[33m"
    black = "\033[36m"
    reset = "\033[0m"
    print("[", end = "")
    for item in freeCells:
        if item in redDeck:
            color = red
        elif item in blackDeck:
            color = black
        else:
            color = reset
        item = "  " if item == " " else item
        print(f"{color}{item} {reset}", end = " ")

    print("]", end = "  [")
    for item in home:
        if item in redDeck:
            color = red
        elif item in blackDeck:
            color = black
        else:
            color = reset
        item = "  " if item == " " else item
        print(f"{color}{item} {reset}", end = " ")

    hePerc, diPerc, flPerc, spPerc = 0, 0, 0, 0
    for num in range(13):
        if home[0] == heSuit[num]:
            hePerc = num + 1
        if home[1] == diSuit[num]:
            diPerc = num + 1
        if home[2] == flSuit[num]:
            flPerc = num + 1
        if home[3] == spSuit[num]:
            spPerc = num + 1

    winPerc = hePerc + diPerc + flPerc + spPerc
    winPerc = round((winPerc * 100) / 52)
    print("]", str(winPerc) + "%\n")


# Name is self explanatory
def printGameField():
    """Prints the 8 columns in a natural way as they would appear on a 
    normal Freecell game. It also prints the Freecells and home"""
    duration[1] = time() - duration[0] + duration[1]
    duration[0] = time()
    printHeader()
    longListLen = 0
    red = "\033[33m"
    black = "\033[36m"
    reset = "\033[0m"
    for num in range(8):
        if len(column[num]) >= longListLen:
            longListLen = len(column[num])

    # Remember that while playing the game, the column length will change
    # This variable finds the longest of them
    for num in range(7):
        print("", num + 1, end = "   ")
    print(" 8")
    for n in range(longListLen):
        for i in range(8):
            if i == 7:
                # We use try...except to avoid outOfRange errors
                try:
                    color = red if column[i][n] in redDeck else black
                    print(f" {color}{column[i][n]} {reset}")
                except:
                    print('    ')
            else:
                try:
                    if len(column[i][n]) == 3:
                        color = red if column[i][n] in redDeck else black
                        print(f" {color}{column[i][n]} {reset}", end = '')
                    else:
                        color = red if column[i][n] in redDeck else black
                        print(f" {color}{column[i][n]} {reset}", end = ' ')
                except:
                    print("     ", end = "")

    if not proMode[0]:
        print(f'\n{red}Red suits are:    ♥ and ♦   {reset}while \n{black}Black suits are:  ♣ and ♠  {reset}')
    else:
        print("    Time > ", end = "")
        print(str(round(duration[1]//60)) + ":" + str(round(duration[1]%60)))


# Works with colToHome
def populateHome(card, i):
    """Places the cd card from column[i] to its specific home/foundation pile location."""

    def placeCard(card, subDeck, posn, i):
        """Validates the card for placement at the respective home 
        location given by posn"""
        for n in range(1, 13):
            if card == subDeck[n] and home[posn] == subDeck[n - 1]:
                home[posn] = card

        if home[posn] != card: # Card not placed
            column[i].append(card) # Return it to its initia column
            print("The card", card, "cannot go home")
            sleep(delayT2[0])

    if card in heSuit :
        # This card should go to home[0] (Hearts)
        if home[0] == ' ' and card == 'A♥':
            home[0] = card 
        else:
            placeCard(card, heSuit , 0, i)
    elif card in diSuit :
        # This card belongs to home[1] (Diamonds)
        if home[1] == ' ' and card == 'A♦':
            home[1] = card 
        else:
            placeCard(card, diSuit , 1, i)
    elif card in flSuit :
        # This card belongs to home[2] (Flowers)
        if home[2] == ' ' and card == 'A♣':
            home[2] = card
        else:
            placeCard(card, flSuit , 2, i)
    else:
        # This card belongs to home[3] (Spade)
        if home[3] == ' ' and card == 'A♠':
            home[3] = card
        else:
            placeCard(card, spSuit , 3, i)


# Moves 1 card from column to foundation pile 
def colToHome(colIndex):
    """Chooses the last card to take it to the home deck and updates 
    the specific column appropriately"""
    if len(column[colIndex]) > 0:
        populateHome(column[colIndex].pop(), colIndex)
    else:
        print("The selected column is empty")
        sleep(delayT2[0])


# Works with tryAddToCol
def checkNumbers(card, colDeck, lastCard):
    """Let's see if the card's number is acceptable, that is they
    will be in descending order if successfully placed"""
    if card in redDeck:
        cardDeck = heSuit  if card in heSuit  else diSuit 
    else:
        cardDeck = spSuit  if card in spSuit  else flSuit 
    for num in range(13):
        if card == cardDeck[num] and lastCard == colDeck[num + 1]:
            return True


# Works with colToCol
def tryAddToCol(card, col):
    """Checks if the card can fit at the end of column[col]"""
    # Check if the receiving column is empty. If so, just proceed
    if len(column[col]) == 0:
        return True
    else: # If column is not empty, then do the following
        lastCard = column[col][-1] # This is the last card in the column
        if card in blackDeck and lastCard in redDeck: # Colors agree
            colDeck = heSuit  if lastCard in heSuit  else diSuit 
            return True if checkNumbers(card, colDeck, lastCard) else False
        elif card in redDeck and lastCard in blackDeck: # Colors agree
            colDeck = spSuit  if lastCard in spSuit  else flSuit 
            return True if checkNumbers(card, colDeck, lastCard) else False
        else:
            return False


# Allows for movement of 1 card between columns
def colToCol(col1, col2):
    """Moves the last card found in col1 to the end of col2"""
    col = col2 # I prefer working with col :) 😊
    if len(column[col1]) != 0:
        card = column[col1][-1]
        if tryAddToCol(card, col):
            # If the function returns True, then proceed
            column[col].append(column[col1].pop())
        else:
            print("You cannot move the card", card, "to column", col + 1)
            sleep(delayT2[0])
    else:
        print("Nothing to move from column", col1 + 1)
        sleep(delayT2[0])


# Very complex...
def moveBlockColToCol(col1, col2):
    """Allows for the movement of more than 1 cards from col1 to col 2.
    It's an improvement of and may replace colToCol() when complete"""

    def movableCards(dest):
        """Returns the highest possible nunber of cards movabe based on the 
        current game state. dest is the condition of receiving column. If it
        is occupied: True, if unocupied: False"""
        avaFrCes, emptyCol = 0, 0 # availableFreeCels, amptyColimns 
        for num in range(4):
            if freeCells[num] == ' ':
                avaFrCes += 1
        for num in range(8):
            if len(column[num]) ==0:
                emptyCol += 1

        if not dest: # destination occupied or not
            emptyCol -= 1
        cards = (avaFrCes + 1) * (emptyCol + 1)
        return 13 if cards >= 13 else  cards # Number of cards that can be received

    def checkCards(col1, donLength):
        """Checks the donating column for the maximum no of cards that can be moved.
        It, thus, checks the color and number sequence to ensure they allow for 
        movement of the cards. It returns the maximum number of cards that can
        be donated from column[col1]"""

        def smart(colm, num, suit, nextSuit):
            """A smart way of checking the number sequence"""
            for i in range(12): # Color and rank of cards following each other
                if colm[num] == suit[i] and colm[num - 1] == nextSuit[i + 1]:
                    return True
                else:
                    pass
                    # return False

        length = 1 # This is the number that it will return
        test = True # This determines whether the card block is still consistent
        colm = column[col1]
        num = 0
        while test and donLength > 1:
            donLength -= 1
            num -= 1
            if colm[num] in heSuit:
                if colm[num - 1] in blackDeck:
                    nextSuit = flSuit if colm[num -1] in flSuit else spSuit
                    if smart(colm, num, heSuit, nextSuit):
                        test = True
                        length += 1
                    else:
                        test = False
                else:
                    test = False
                    pass
            elif colm[num] in diSuit:
                if colm[num - 1] in blackDeck:
                    nextSuit = flSuit if colm[num -1] in flSuit else spSuit
                    if smart(colm, num, diSuit, nextSuit):
                        test = True
                        length += 1
                    else:
                        test = False
                else:
                    test = False
                    pass
            elif colm[num] in flSuit:
                if colm[num - 1] in redDeck:
                    nextSuit = heSuit if colm[num -1] in heSuit else diSuit
                    if smart(colm, num, flSuit, nextSuit):
                        test = True
                        length += 1
                    else:
                        test = False
                else:
                    test = False
                    pass
            else: # spSuit 
                if colm[num - 1] in redDeck:
                    nextSuit = heSuit if colm[num -1] in heSuit else diSuit
                    if smart(colm, num, spSuit, nextSuit):
                        test = True
                        length += 1
                    else:
                        test = False
                else:
                    test = False
                    pass

        # column[col1] = column[col1][:-length]
        return length

    recLength = movableCards(True if len(column[col2]) != 0 else False)
    donLength = len(column[col1]) if len(column[col1]) <= recLength else recLength
    donLength = checkCards(col1, donLength)
    donatedColumn = column[col1][-donLength:]
    if len(column[col2]) == 0: # This is for empty receiving columns
        column[col2] = donatedColumn
        column[col1] = column[col1][:-donLength]
    else: # For non-empty receiving columns
        hostCard = column[col2][-1]
        # recSuit = redDeck if card in redDeck else blackDeck
        if hostCard in redDeck:
            hostSuit = heSuit if hostCard in heSuit else diSuit
        else:
            hostSuit = flSuit if hostCard in flSuit else spSuit

        for i in range(13):
            if hostCard == hostSuit[i]:
                break # i is the index of the card in receiving column

        succeed, colorOk = False, False
        for num in range(len(donatedColumn)):
            # donatedColumn contains all the cards that can be moved from column[col1]
            if hostCard in redDeck: # Red receiving card
                if donatedColumn[num] in blackDeck:
                    donDeck = flSuit if donatedColumn[num] in flSuit else spSuit
                    colorOk = True
                    if donatedColumn[num] == donDeck[i - 1]: # Color & no of base card in donated list ok
                        forward = donatedColumn[num:]
                        back = donatedColumn[:num]
                        succeed = True
                        break
            else: # Black receiving card
                if donatedColumn[num] in redDeck:
                    donDeck = heSuit if donatedColumn[num] in heSuit else diSuit
                    colorOk = True
                    if donatedColumn[num] == donDeck[i - 1]:
                        forward = donatedColumn[num:]
                        back = donatedColumn[:num]
                        succeed = True
                        break

            if succeed:
                break

        if not colorOk:
            print("\nColor sequence mismatch. Can't move from column", col1 + 1, "to column", col2 + 1)
            sleep(delayT2[0])

        if not succeed:
            print("\nCannot move from column", col1 + 1, "to column", col2 + 1)
            sleep(delayT2[0])
        else:
            for num in range(len(forward)):
                column[col2].append(forward[num])
                column[col1].pop()

            for num in range(len(back)):
                pass
                # column[col1].append(back[num])


# Handles card movement between freecells and columns
def maintainFreeCell(action, col, posn = 0):
    """action = 1 > add to freecell from column[col] 
    or 2 > remove from freecell[posn] to column[col]
    col is the column index and posn is the freecell index.
    The function updates the freecells accordingly"""
    if action == 1: # Add to freecell
        if freeCells[posn] == " ":
            freeCells[posn] = column[col].pop()
        else:
            if ' ' in freeCells:
                for num in range(4):
                    if freeCells[num] == " ":
                        freeCells[num] = column[col].pop()
                        break
            else:
                print("There is no Free cell")
                sleep(delayT2[0])
    else: # Remove from freecell
        if freeCells[posn] != ' ': # Check if cell is empty
            card = freeCells[posn]
            if tryAddToCol(card, col):
                # If the function returns True, then proceed
                column[col].append(card)
                freeCells[posn] = ' ' # Remove the card from freecell
            else:
                print("You cannot move the card", card, "to column", col + 1)
                sleep(delayT2[0])
        else: # The cell is empty
            print("The selected freecell is empty")
            sleep(delayT2[0])


# Handles movement of cards from freecell to foundation pile 
def freeToHome(num):
    """Takes the card at freeCells[num] and tests whether it can go home. If so,
    it transfers it and updates the freeCells list appropriately"""

    def moveCard(card, subDeck, posn, num):
        """Validates the card for placement at the respective home 
        location given by posn"""
        for n in range(1, 13):
            if card == subDeck[n] and home[posn] == subDeck[n - 1]:
                home[posn] = card
                freeCells[num] = " "

        # If the card is invalid for placement, this is executed
        if home[posn] != card:
            freeCells[num] = card
            print("The card", card, "cannot go home")
            sleep(delayT2[0])

    card = freeCells[num]
    if card != ' ':
        if card in heSuit :
            if home[0] == ' ' and card == heSuit[0]:
                home[0] = card
                freeCells[num] = ' '
            else:
                freeCells[num] = ' '
                moveCard(card, heSuit , 0, num)
        elif card in diSuit :
            if home[1] == ' ' and card == diSuit[0]:
                home[1], freeCells[num] = card, ' '
            else:
                freeCells[num] = ' '
                moveCard(card, diSuit , 1, num)
        elif card in flSuit :
            if home[2] == ' ' and card == flSuit[0]:
                home[2], freeCells[num] = card, ' '
            else:
                moveCard(card, flSuit , 2, num)
        else:
            if home[3] == ' ' and card == spSuit[0]:
                home[3], freeCells[num] = card, ' '
            else:
                moveCard(card, spSuit , 3, num)

    else:
        print("The chosen cell is empty.")
        sleep(delayT2[0])


# Gets called during start of game to initiate the data
def createSession():
    """Tries retrieving saved game. If impossible it creates a new session
    containing shuffled deck and blank home and free cells"""
    try:
        with open("data/freecell.txt", "r", encoding = "utf-8") as retrieveGame:
            columnStr = retrieveGame.read().split('\n')
            # Creates a list
            if 2 < len(columnStr) <= 12: # Checks the integrity of the retrieved data

                for num in range(4):
                    freeCells[num] = columnStr[0].split(',')[num]
                    home[num] = columnStr[1].split(',')[num]

                # For cases when some columns were already blank, use this
                if home == [heSuit[12], diSuit[12], flSuit[12], spSuit[12]]:
                    for num in range(4):
                        home[num] = ' '
                    raise Exception
                for num in range(2, 10):
                    col = num - 2
                    column[col] = columnStr[num].split(",")
                for num in range(len(column)):
                    if column[num] == ['']:
                        column[num] = []
                durationStr = columnStr[10].split(",")
                duration[0], duration[1] = time(), float(durationStr[1])

            else:
                print('Sorry', player[0], 'No saved game found. Dealing a new deck')
                raise Exception
            print("Successfully loaded last saved game")
            

    except Exception as e:
        print(e)
        print("Created new game session successfully")
        shuffle(deck)
        duration[0] = time()
        duration[1] = 0
        for num in range(8):
            column[num] = []
            
        for i in range(7):
            for num in range(8):
                try:
                    column[num].append(deck.pop())
                except:
                    pass

        saveSession() # In case the data doesn't exist, then save the created one


# Useful only for saving the game data
def saveSession():
    """saves the current game data for retrieval at a later time"""
    try:
        with open("data/freecell.txt", "w", encoding = "utf-8") as saveGame:
            for num in range(4):
                saveGame.write(freeCells[num] + ',')
            saveGame.write("\n")
            for num in range(4):
                saveGame.write(home[num] + ',')
            saveGame.write("\n")
            for col in range(8):
                if len(column[col]) == 0:
                    saveGame.write("\n")
                for num in range(len(column[col])):
                    if num == len(column[col]) - 1:
                        saveGame.write(column[col][num] + "\n")
                    else:
                        saveGame.write(column[col][num] + ",")
            saveGame.write(str(duration[0]) + ",")
            saveGame.write(str(duration[1]) + "\n")

    except Exception as e:
        print(e)
        pass


# Checks for win condition and saves the game
def checkWin():
    """Checks the game for win condition and archives the current game"""
    saveSession() # This updates the game after each move
    longListLen = 0
    for col in column:
        longListLen = len(col) if len(col) > longListLen else longListLen
    if home != [heSuit[12], diSuit[12], flSuit[12], spSuit[12]]:
        return False
    else:
        return True


# Collects user input, validates it and returns it appropriately 
def inTake(lim):
    """Takes input from the user and validates it before returning
    it to the calling function. It also provides for calling the help,
    restarting, changing autoMode, and exiting the game. It ignores
    all unexpected inputs without creating a Traceback"""
    entry = input()
    if len(entry) > 0:
        if entry.isdecimal():
            entry = int(entry)
            if 1 <= entry <= lim:
                return entry
            else:
                print("Select a number between 1 and", lim)
                return inTake(lim)

        else:
            entry = entry.upper()
            if entry == 'help'.upper() or entry == '--help'.upper():
                # Print help message
                return printHelp(lim)
            elif entry.upper() == 'exit'.upper() or entry == '--exit'.upper():
                saveSession()
                exit(0)
            elif entry.upper() == "restart".upper():
                deck = createDeck()
                shuffle(deck)
                #print(deck)
                for num in range(4):
                    home[num] = ' '
                    freeCells[num] = ' '
                for num in range(8):
                    column[num] = []
                for i in range(7):
                    for num in range(8):
                        try:
                            column[num].append(deck.pop())
                        except Exception as e:
                            print(e)
                            pass

                
                duration[0] = time()
                duration[1] = 0
                saveSession()
            elif entry.upper() == "auto".upper():
                if autoMode[0]:
                    autoMode[0] = False
                else:
                    autoMode[0] = True
                    autoSendHome()
            elif entry.upper() == "off".upper():
                proMode[0] = True
            elif entry.upper() == "on".upper():
                proMode[0] = False

    else:
        return inTake(lim)


# Automates movement of cards to foundation pile
def autoSendHome():
    """Moves the cards that are ready to move to home without needing
    player's interaction."""

    def autoColToHome(card, suit, posn):
        """Checks the passed card against the respective home position. If
        the home[posn] contains a card that is a number less than the card,
        this function returns True, otherwise False"""
        if card == suit[0] and home[posn] == ' ':
            return True
        else:
            for i in range(1, 13):
                if card == suit[i] and home[posn] == suit[i - 1]:
                    return True

    #2. A card that can go its index should be popped to its respective home[posn]

    def simplify(card):
        """Returns the card's suit and suit's position at foundation pile"""
        if card in heSuit:
            return [heSuit, 0]
        elif card in diSuit:
            return [diSuit, 1]
        elif card in flSuit:
            return [flSuit, 2]
        else:
            return [spSuit, 3]

    #1. Start by checking all the 8 cards at the end of columns against the home
    rerun = False # I use this to decide whether to run this autoSendHome() again
    for num in range(8):
        if len(column[num]) > 0:
            card = column[num][-1]
            suit = simplify(card)[0]
            posn = simplify(card)[1]
            if autoColToHome(card, suit, posn):
                home[posn] = column[num].pop()
                system('cls' if name == 'nt' else 'clear')
                print("Please Wait! Game busy\n")
                printGameField()
                sleep(delayT[0])
                rerun = True

    #3. Next check the 4 free cells            
    for num in range(4):
        card = freeCells[num]
        if card != ' ':
            suit = simplify(card)[0]
            posn = simplify(card)[1]
            if autoColToHome(card, suit, posn):
                home[posn] = card
                freeCells[num] = ' '
                system('cls' if name == 'nt' else 'clear')
                print("Please Wait! Game busy\n")
                printGameField()
                sleep(delayT[0])
                rerun = True

    if rerun:
        autoSendHome()


# This is where all the action is!
def gamePlay():
    """Launches the game and calls all the required functions for the 
    game to play"""
    system('cls' if name == 'nt' else 'clear')
    printGameField()
    if proMode[0]:
        print("\nHey", player[0], "enter 'on' to display prompts", end = " ")
    else:
        print("\nHey", player[0] + ", choose to move card from:")
        print("1.  Column to freecell")
        print("2.  Freecell to column")
        print("3.  Column to column", end = "")
        if not autoMode[0]:
            print("\n4.  Column to foundation pile")
            print("5.  Freecell to foundation pile", end = "")
        print(".   Or you can enter")
        # print("Alternatively", player[0] + ", you can enter")
        print("'restart' to start a new game")
        print("'--help' for rules")
        print("'exit' to end the game")
        print("'off' to hide prompts")
        print("'auto' to disable auto movement.   ", end = "") if autoMode[0] else print("'auto' to enable auto movement", end = " ")

    sel = inTake(5) if not autoMode[0] else inTake(3)

    try:
        if sel == 1:
            # column to freecell
            print("Remove from column no? ", end = "")
            maintainFreeCell(1, inTake(8) - 1)
        elif sel == 2:
            # freecell to column
            print("From cell")
            print("1:" + freeCells[0], " 2:" + freeCells[1], " 3:" + freeCells[2], " or 4:" + freeCells[3], '  ', end = "")
            posn = inTake(4) - 1
            if freeCells[posn] != ' ':
                print("To column: ", end = "")
                col = inTake(8) - 1
                maintainFreeCell(2, col, posn)
            else:
                system('cls' if name == 'nt' else 'clear')
                printHeader()
                print("Cell", posn + 1, "is empty")
                sleep(1)
        elif sel == 3:
            # column to column colToCol(col1, col2)
            print("Move from column: ", end = "")
            col1 = inTake(8) - 1
            print("To column: ", end = "")
            col2 = inTake(8) - 1
            colToCol(col1, col2) if not autoMode[0] else moveBlockColToCol(col1, col2)
        elif sel == 4:
            # column to home colToHome(colIndex)
            print("Send home from column: ", end = "")
            colToHome(inTake(8) - 1)
        elif sel == 5:
            # freecell to home freeToHome(num)
            print("Send home from column: ", end = "")
            print("1:", freeCells[0], " 2:",freeCells[1], " 3:", freeCells[2], " or 4:", freeCells[3], '   ', end = "")
            posn = inTake(4) - 1
            if freeCells[posn] != ' ':
                freeToHome(posn)
            else:
                system('cls' if name == 'nt' else 'clear')
                printHeader()
                print("Cell", posn + 1, "is empty")
                sleep(1)

    except Exception as e:
        print(e)
        pass

    if autoMode[0]:
        autoSendHome()
        # print("The comp is cheating")
    if checkWin():
        system('cls' if name == 'nt' else 'clear')
        printGameField()
        print("\n\nCongratulations", player[0], "you have won!\nAll cards are sorted at the foundation pile!")
        return
    else:
        gamePlay()


deck = createDeck() # Creates a default deck
heSuit  = deck[:13] # Hearts Suit 
diSuit  = deck[13:26] # Diamonds Suit 
flSuit  = deck[26:39] # Flowers Suit 
spSuit  = deck[39:] # Spades Suit 

# This arranges the black and red cards
blackDeck = [] # flSuit  and spSuit 
redDeck = [] # heSuit  and diSuit 
for num in range(13):
    blackDeck.append(spSuit [num])
    blackDeck.append(flSuit [num])
    redDeck.append(diSuit [num])
    redDeck.append(heSuit [num])
proMode = [True]
autoMode = [True]
duration = ['', '']
freeCells = [' ', ' ', ' ', ' '] # Vacant slots for free cells
home = [' ', ' ', ' ', ' '] # Vacant slots for home cells
column = [[], [], [], [], [], [], [], []] # Will contain all the 8 columns
createSession() # Tries retrieving saved game. If impossible it creates a new session
player = [[]]
delayT2 = [2]
delayT = [0.25] # This is the duration of delay between auto moves to home
print("Welcome to this Freecell game. \nPlease enter your name to continue")
player[0] = input().title()
if not proMode[0]:
    print("\nWelcome", player[0] + ", please note that the game will always save",
      "your progress so that you can continue at a later time.",
      "It will also help you by making all possible moves to foundation pile")

    print("To disable auto movement of cards to foundation pile, enter '1', Otherwise press enter")
    autoMode[0] = False if input() == '1' else True
    print("Auto movement is on") if autoMode[0] else print("Auto movement is off")
    input("\nLet's get into it.")
    sleep(delayT2[0])
gamePlay()