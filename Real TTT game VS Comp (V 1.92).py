"""#!/usr/bin/env python"""
'''# coding: utf-8
#
# ***Created on Sat Oct 19 12:00:13 2024***
#
# *This code was adapted from Pirple's TicTacToe lecture

V 1.8
Has improved competing algorithm. It's now even harder to beat the comp

V 1.9
Includes records for wins, draws, and loss as long as the game does not exit. 
These stats reset upon restarting the game. The game also has better exitting
code that prevents generation of exceptions.

available at: https://pastebin.com/xHFD2jy2

author: baya_w
'''


# %% This cell draws the gamefield on console
import random, sys, os  # noqa: E402

def drawField(gameData):
    """ This is the GUI function. It picks data from the list defined below
    and then places each cell in its respective location and draws it on the
    console """
    row, col = 7, 7
    # The block below creates a grid for the game
    for numRow in range(row):
        if numRow % 2 == 0:  # This is for even row
            for numCol in range(col):
                if numCol == col - 1:  # This is the last item
                    if numCol % 2 == 0:
                        print("+")
                else:  # This is not the last item
                    if numCol % 2 == 0:
                        print("+", end="")
                    else:
                        print("-", end="")

        else:  # This is for odd row
            for numCol in range(col):
                if numCol == col - 1:  # This is the last item
                    if numCol % 2 == 0:
                        print("|")
                else:  # This is not the last item
                    if numCol % 2 == 0:
                        print("|", end="")
                    else:
                        rowIndex = (numRow - 1) // 2
                        colIndex = (numCol - 1) // 2
                        # This line below prints the entry by the player
                        print(gameData[rowIndex][colIndex], end="")


# %% This is a helper cell for the competitive move selection

def firstMove(item):
    """ This handles the first move by the computer. It checks the grid and then
    returns all the potential cells after the player has placed the first move.
    To do this, it analyses the grid and returns the most likely moves for the 
    player. The comp then uses this data to decide where to place its next move """
    for num in range(3):
        if item[num][0] == 'X' and item[num][1] == item[num][2] == ' ':
            return item[num][3] if random.randint(1, 2) else item[num][4]


def subsequentMove(item, symbol):
    """ This function helps the comp identify cases there remains only a single
    move for the player or comp to win. It returns the specifed cell and then
    returns it to the compete() or makeWin() function respectively """
    for num in range(3):
        if item[num][0] == item[num][1] == symbol and item[num][2] == ' ':
            return item[num][3]


def deepBlock(item, line, lineNo):
    """ To speak the truth, it is hard to document this function. I know that it
    identifies cells that the computer would have picked yet they are not of such
    a high priority. In such cases, it prevents the computer from selecting them
    unless they are absolutely necessary. Do you get that? That's the best I
    can do."""
    check1 = any(cell == 'X' for cell in item)
    check2 = any(cell == 'O' for cell in item)
    check3 = any(cell == ' ' for cell in item)
    if check1 and check2 and check3:
        for num in range(3):
            if item[num] == ' ':
                if line == 'row':
                    return [lineNo, num]
                elif line == 'col':
                    return [num, lineNo]
                elif line == 'diag1':
                    return [num, num]
                elif line == 'diag2':
                    if num == 1:
                        return [3, num]
                    elif num == 2:
                        return [num, num]
                    else:
                        return [1, num]
                    
                    
# %% This cell handles computer's predictive competitive offensive movement
def makeWin(gD):
    """ This function will check the grid for instances where the computer is a
    move away from winning. Such instances include O O ' '. If True, this
    function will use subsequentMove to identify these cases and then place
    the O to win the game. """
    a1, a2, a3 = gD[0][0], gD[0][1], gD[0][2]  # [1, 1], [1, 2], [1, 3]
    b1, b2, b3 = gD[1][0], gD[1][1], gD[1][2]  # [2, 1], [2, 2], [2, 3]
    c1, c2, c3 = gD[2][0], gD[2][1], gD[2][2]  # [3, 1], [3, 2], [3, 3]

    row1Var = [[a1, a2, a3, [1, 3]],
               [a1, a3, a2, [1, 2]],
               [a2, a3, a1, [1, 1]]]
    row2Var = [[b1, b2, b3, [2, 3]],
               [b1, b3, b2, [2, 2]],
               [b2, b3, b1, [2, 1]]]
    row3Var = [[c1, c2, c3, [3, 3]],
               [c1, c3, c2, [3, 2]],
               [c2, c3, c1, [3, 1]]]
    col1Var = [[a1, b1, c1, [3, 1]],
               [a1, c1, b1, [2, 1]],
               [b1, c1, a1, [1, 1]]]
    col2Var = [[a2, b2, c2, [3, 2]],
               [a2, c2, b2, [2, 2]],
               [b2, c2, a2, [1, 2]]]
    col3Var = [[a3, b3, c3, [3, 3]],
               [a3, c3, b3, [2, 3]],
               [b3, c3, a3, [1, 3]]]
    diag1Var = [[a1, b2, c3, [3, 3]],
                [a1, c3, b2, [2, 2]],
                [b2, c3, a1, [1, 1]]]
    diag2Var = [[c1, b2, a3, [1, 3]],
                [c1, a3, b2, [2, 2]],
                [b2, a3, c1, [3, 1]]]

    row1 = subsequentMove(row1Var, 'O')
    row2 = subsequentMove(row2Var, 'O')
    row3 = subsequentMove(row3Var, 'O')
    col1 = subsequentMove(col1Var, 'O')
    col2 = subsequentMove(col2Var, 'O')
    col3 = subsequentMove(col3Var, 'O')
    diag1 = subsequentMove(diag1Var, 'O')
    diag2 = subsequentMove(diag2Var, 'O')

    move = []
    move.append(row1) if row1 is not None else move
    move.append(row2) if row2 is not None else move
    move.append(row3) if row3 is not None else move
    move.append(col1) if col1 is not None else move
    move.append(col2) if col2 is not None else move
    move.append(col3) if col3 is not None else move
    move.append(diag1) if diag1 is not None else move
    move.append(diag2) if diag2 is not None else move

    if len(move) > 0:
        return move[0]
    else:
        return False
    

# %% This cell considers computer's predictive competitive defensive movement
def compete(gD):
    """ This function considers cases where the player is a move away from
    winning. For instance, if the player has X X ' ', then the comp needs to
    block the empty position to prevent the player from winning. This function
    combined with subsequentMove() will find that empty cell and fill it """
    a1, a2, a3 = gD[0][0], gD[0][1], gD[0][2]  # [1, 1], [1, 2], [1, 3]
    b1, b2, b3 = gD[1][0], gD[1][1], gD[1][2]  # [2, 1], [2, 2], [2, 3]
    c1, c2, c3 = gD[2][0], gD[2][1], gD[2][2]  # [3, 1], [3, 2], [3, 3]

    row1 = row2 = row3 = col1 = col2 = col3 = diag1 = diag2 = False

    row1Var = [[a1, a2, a3, [1, 3]],
               [a1, a3, a2, [1, 2]],
               [a2, a3, a1, [1, 1]]]
    row2Var = [[b1, b2, b3, [2, 3]],
               [b1, b3, b2, [2, 2]],
               [b2, b3, b1, [2, 1]]]
    row3Var = [[c1, c2, c3, [3, 3]],
               [c1, c3, c2, [3, 2]],
               [c2, c3, c1, [3, 1]]]
    col1Var = [[a1, b1, c1, [3, 1]],
               [a1, c1, b1, [2, 1]],
               [b1, c1, a1, [1, 1]]]
    col2Var = [[a2, b2, c2, [3, 2]],
               [a2, c2, b2, [2, 2]],
               [b2, c2, a2, [1, 2]]]
    col3Var = [[a3, b3, c3, [3, 3]],
               [a3, c3, b3, [2, 3]],
               [b3, c3, a3, [1, 3]]]
    diag1Var = [[a1, b2, c3, [3, 3]],
                [a1, c3, b2, [2, 2]],
                [b2, c3, a1, [1, 1]]]
    diag2Var = [[c1, b2, a3, [1, 3]],
                [c1, a3, b2, [2, 2]],
                [b2, a3, c1, [3, 1]]]

    row1 = subsequentMove(row1Var, 'X')
    row2 = subsequentMove(row2Var, 'X')
    row3 = subsequentMove(row3Var, 'X')
    col1 = subsequentMove(col1Var, 'X')
    col2 = subsequentMove(col2Var, 'X')
    col3 = subsequentMove(col3Var, 'X')
    diag1 = subsequentMove(diag1Var, 'X')
    diag2 = subsequentMove(diag2Var, 'X')

    # It is important to avoid the invalid options. Append only non-empty ones
    option = []
    option.append(row1) if row1 is not None else option
    option.append(row2) if row2 is not None else option
    option.append(row3) if row3 is not None else option
    option.append(col1) if col1 is not None else option
    option.append(col2) if col2 is not None else option
    option.append(col3) if col3 is not None else option
    option.append(diag1) if diag1 is not None else option
    option.append(diag2) if diag2 is not None else option
    
    '''
    In some cases, the game might move to a location where it actually it is 
    of low defensive priority. This section identifies such locations and 
    eliminates them from list of possibilities.
    '''
    row1Rem = deepBlock([a1, a2, a3], 'row', 1)
    row2Rem = deepBlock([b1, b2, b3], 'row', 2)
    row3Rem = deepBlock([c1, c2, c3], 'row', 3)
    col1Rem = deepBlock([a1, b1, c1], 'col', 1)
    col2Rem = deepBlock([a2, b2, c2], 'col', 2)
    col3Rem = deepBlock([a3, b3, c3], 'col', 3)
    diag1Rem = deepBlock([a1, b2, c3], 'diag1', 1)
    diag2Rem = deepBlock([c1, b2, a3], 'diag2', 1)

    rem = []
    rem.append(row1Rem) if row1Rem is not None else rem
    rem.append(row2Rem) if row2Rem is not None else rem
    rem.append(row3Rem) if row3Rem is not None else rem  # noqa: E711
    rem.append(col1Rem) if col1Rem is not None else rem
    rem.append(col2Rem) if col2Rem is not None else rem
    rem.append(col3Rem) if col3Rem is not None else rem
    rem.append(diag1Rem) if diag1Rem is not None else rem
    rem.append(diag2Rem) if diag2Rem is not None else rem
    
    mv = []
    if len(option) > 0:
        # This helps the program choose from among the possibilities
        if len(option) == 1:
            return option[0]
        elif len(option) > 1:
            for num in range(len(option)):
                if option[num] != rem:
                    mv = mv.append(option[num])
                    return mv if mv is not None else random.choice(option)
                
    else:
        '''This comes into effect only if the user still does not have any
        possible winning move. Player has only made just the first move'''
        row1Var = [[a1, a2, a3, [1, 2], [1, 3]],
                   [a2, a1, a3, [1, 1], [1, 3]],
                   [a3, a1, a2, [1, 1], [1, 2]]]
        row2Var = [[b1, b2, b3, [2, 2], [2, 3]],
                   [b2, b1, b3, [2, 1], [2, 3]],
                   [b3, b1, b2, [2, 1], [2, 2]]]
        row3Var = [[c1, c2, c3, [3, 2], [3, 3]],
                   [c2, c1, c3, [3, 1], [3, 3]],
                   [c3, c1, c2, [3, 1], [3, 2]]]
        col1Var = [[a1, b1, c1, [2, 1], [3, 1]],
                   [b1, a1, c1, [1, 1], [3, 1]],
                   [c1, a1, b1, [1, 1], [2, 1]]]
        col2Var = [[a2, b2, c2, [2, 2], [3, 2]],
                   [b2, a2, c2, [1, 2], [3, 2]],
                   [c2, a2, b2, [1, 2], [2, 2]]]
        col3Var = [[a3, b3, c3, [2, 3], [3, 3]],
                   [b3, a3, c3, [1, 3], [3, 3]],
                   [c3, a3, b3, [1, 3], [2, 3]]]
        diag1Var = [[a1, b2, c3, [2, 2], [3, 3]],
                    [b2, a1, c3, [1, 1], [3, 3]],
                    [c3, a1, b2, [1, 1], [2, 2]]]
        diag2Var = [[c1, b2, a3, [2, 2], [1, 3]],
                    [b2, c1, a3, [3, 1], [1, 3]],
                    [a3, c1, b2, [3, 1], [2, 2]]]

        option = []
        row1 = firstMove(row1Var)
        row2 = firstMove(row2Var)
        row3 = firstMove(row3Var)
        col1 = firstMove(col1Var)
        col2 = firstMove(col2Var)
        col3 = firstMove(col3Var)
        diag1 = firstMove(diag1Var)
        diag2 = firstMove(diag2Var)

        # Let's now combine the entries into a single list
        option.append(row1) if row1 is not None else option
        option.append(row2) if row2 is not None else option
        option.append(row3) if row3 is not None else option
        option.append(col1) if col1 is not None else option
        option.append(col2) if col2 is not None else option
        option.append(col3) if col3 is not None else option
        option.append(diag1) if diag1 is not None else option
        option.append(diag2) if diag2 is not None else option

        return random.choice(option)


# %% This cell deals with collection of data input from player
def inTake(winStat):
    entry = input()
    if str.isnumeric(entry):
        return entry
    else:
        if entry == 'Q' or entry == 'q':
            print("(Win, Draw, Lose) =",str(tuple(winStat)), '\nThank You!')
            sys.exit(0)
        else:
            print("The entered input '" + entry + "' is invalid. Try again." + 
                  "\nAlternatively, enter 'Q' to quit: ", end = '')
            return inTake(winStat)


def dataInput(posn, player, lim, winStat):  # This handles the data input for row and column no
    if player == "X":
        print('Enter ' + posn + ': ', end="")
        entry = int(inTake(winStat))
        if 1 <= entry <= lim:
            return entry
        else:
            print("Number", str(entry), "is invalid. Enter a valid number",
                  "between 1 and", lim)
            return dataInput(posn, player, lim, winStat)
    else:
        entry = random.randint(1, 3)
        return entry


# %% This cell declares the winner and ensures the game ends
def win(entry, winStat):  # Winner declaration:
    if entry == "X":
        winStat[0] += 1
        print("Congratulations! YOU HAVE WON\n")
    else:
        winStat[2] += 1
        print("AI has WON!\n")
    totPlays = winStat[0] + winStat[1] + winStat[2]
    winPerc = [winStat[0] / totPlays * 100, winStat[1] / totPlays * 100, winStat[2] / totPlays * 100]
    print("Statistics are: \nPlayer:", winStat[0],
          "\t\nDraw: " + str(winStat[1]) + "\nAI: " + str(winStat[2]) + 
            "\nPercentages:", tuple(winPerc))
    print('Press 1 to replay,\n2 to change level,' +
          '\nor anything else to exit: ', end = '')
    sel = int(inTake(winStat))
    if sel == 1:
        print("\n====================================\n")
        return [False, winStat[0], winStat[1], winStat[2]]
    elif sel == 2:
        print("\n====================================\n")
        tictactoe(True, winStat)
    else:
        print("(Win, Draw, Lose) =",str(tuple(winStat)), '\nThank You!')
        sys.exit(0)


# %% Here we check if there is a winner or not
def checkWin(gameData, winStat):  # Checks for winner
    for row in range(3):
        if gameData[row][0] == gameData[row][1] == gameData[row][2] != " ":
            return win(gameData[row][0], winStat)
    for col in range(3):
        if gameData[0][col] == gameData[1][col] == gameData[2][col] != " ":
            return win(gameData[0][col], winStat)
    if gameData[0][0] == gameData[1][1] == gameData[2][2] != " ":
        return win(gameData[0][0], winStat)
    if gameData[0][2] == gameData[1][1] == gameData[2][0] != " ":
        return win(gameData[0][2], winStat)
    return [True, winStat[0], winStat[1], winStat[2]]


# %% Here the game checks if we have a draw
def checkDraw(gameData, winStat):  # Checks for draw
    status = all(cell != " " for row in gameData for cell in row)
    if status:
        print("IT'S A DRAW!\n")
        winStat[1] += 1
        print("Statistics are:\nPlayer: " + 
            str(winStat[0]) + "\nDraw: " + str(winStat[1]) + 
            "\nAI: " + str(winStat[2]) + "\n")
        print('Press 1 to replay,\n2 to change level,' +
              '\nor anything else to exit: ', end = '')
        sel = int(inTake(winStat))
        if sel == 1:
            status = [status, winStat[0], winStat[1], winStat[2]]
            print("\n====================================\n")
            return status
        elif sel == 2:
            print("\n====================================\n")
            tictactoe(True, winStat)
        else:
            print("(Win, Draw, Lose) =",str(tuple(winStat)), '\nThank You!')
            sys.exit(0)
    else:
    	return [False, winStat[0], winStat[1], winStat[2]]



# %% This is where the action is
def tictactoe(condition, winStat):
    print("Select the difficulty level:\n1. Easy\n2. Medium\n3. Hard")
    difficulty = dataInput('dificulty selection', 'X', 3, winStat)
    os.system('cls' if os.name == 'nt' else 'clear')
    if difficulty == 1:
        print("You have selected 'Easy'")
    elif difficulty == 2:
        print("You have selected 'Medium'")
    else:
        print("You have selected 'Hard'")
    print('\nSelect data entry method of choice. You can'
          + '\n1. Use rows and columns\n' + 
          '2. Use cell numbers\n')
    print(" C O L \n |||||\n v|v|v\n 1|2|3")
    print("+-+-+-+\n|1|2|3| <- Row 1")
    print("+-+-+-+----------\n|4|5|6| <- Row 2")
    print("+-+-+-+----------\n|7|8|9| <- Row 3\n+-+-+-+\n")
    entryMethodSel = dataInput('selection', "X", 2, winStat)
    print('You have selected 2. You will use cell'
          + ' numbers 1 to 9\n') if entryMethodSel == 2 else print('You have selected 1. '
          + 'You will use row and column numbers'
          + '\n1, 2, or 3 to describe cell location\n')
    while condition:
        gameData = [[" ", " ", " "],
                    [" ", " ", " "],
                    [" ", " ", " "]]
        player = 'X'
        noDraw = noWin = True
        while noDraw and noWin:
            if player == 'X':  # Take data for 'X' and update it:
                if entryMethodSel == 2:
                    cell = dataInput('cell', player, 9, winStat)
                    if cell == 1:
                        rowReal, colReal = 1, 1
                    elif cell == 2:
                        rowReal, colReal = 1, 2
                    elif cell == 3:
                        rowReal, colReal = 1, 3
                    elif cell == 4:
                        rowReal, colReal = 2, 1
                    elif cell == 5:
                        rowReal, colReal = 2, 2
                    elif cell == 6:
                        rowReal, colReal = 2, 3
                    elif cell == 7:
                        rowReal, colReal = 3, 1
                    elif cell == 8:
                        rowReal, colReal = 3, 2
                    elif cell == 9:
                        rowReal, colReal = 3, 3
                else:
                    rowReal = dataInput('row', player, 3, winStat)
                    colReal = dataInput('column', player, 3, winStat)
                print('Your move is ' + str(tuple([rowReal, colReal])))
                rowReal -= 1
                colReal -= 1
                if gameData[rowReal][colReal] == " ":  # Validate entry is empty:
                    gameData[rowReal][colReal] = "X"
                    player = 'O'
                else:
                    print("The selected position is not empty")
            else:  # Take data for 'O' and update it:
                if difficulty == 1:
                    rowReal = dataInput('row', player, 3, winStat) - 1
                    colReal = dataInput('column', player, 3, winStat) - 1
                    if gameData[rowReal][colReal] == " ":  # Validate entry is empty:
                        move = [rowReal + 1, colReal + 1]
                        print('AI plays', tuple(move))
                        gameData[rowReal][colReal] = "O"
                        player = 'X'
                    else:
                        print("The selected position is already taken")
                elif difficulty == 3:
                    move = compete(gameData) if not makeWin(gameData) else makeWin(gameData)
                    rowReal = move[0] - 1
                    colReal = move[1] - 1
                    print('AI\'s move is', tuple(move))
                    gameData[rowReal][colReal] = "O"
                    player = 'X'
                else:
                    move = compete(gameData)
                    rowReal = move[0] - 1
                    colReal = move[1] - 1
                    print('AI plays', tuple(move))
                    gameData[rowReal][colReal] = "O"
                    player = 'X'
                    
            os.system('cls' if os.name == 'nt' else 'clear')
            drawField(gameData)
            print()
            noWin = checkWin(gameData, winStat)
            winStat = noWin[1:]
            noWin = noWin[0]
            if noWin:
                noDraw = checkDraw(gameData, winStat)
                winStat = noDraw[1:]
                noDraw = not noDraw[0]
                
                
# %% This ensures the game's repetitive nature. It also launches the game
print('Welcome to this minimalist tictactoe. You will play against an AI.')
print('You play "X". To quit the game anytime, press "Q"\n')
winStat = [0, 0, 0] # [Player, Draw, AI]
tictactoe(True, winStat)
