# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 13:40:25 2024

This is the code for the 'Connect 4' game assignment

@author: Baya
"""

import sys
import os


def drawField(gameData):
    """ This is the GUI function. It picks data from the defined list, places
    each cell in its respective location, and then draws it on the console """
    row, col = 13, 15
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
                        # print(' ', end = "")
                        rowIndex = (numRow - 1) // 2
                        colIndex = (numCol - 1) // 2
                        # This line below prints the entry by the player
                        print(gameData[rowIndex][colIndex], end="")


def dataIntake(lim):  # lim is the highest number that the function can return
    """This function takes intager input from the user and validates it. If
    the user enters an unexpected input, it prints a prompt and asks for a
    fresh entry"""
    sel = input()
    if sel.isdecimal():
        if 1 <= int(sel) <= lim:
            return int(sel)
        else:  # Number out of range
            print("Please enter a number between 1 and", str(lim))
            return dataIntake(lim)
    elif sel == 'q' or sel == 'Q':
        print('\nThank you. Game is exiting')
        sys.exit(0)
    else:  # Input is not a number
        print("Please enter a number between 1 and", str(lim))
        return dataIntake(lim)


def checkWin(gD):
    """This function takes in the data and then checks it to see if there is
    a win condition. It considers the rules of 'Connect 4', which are: If
    the board has any four similar pieces in a line, 'horizontally, 
    vertically, or diagonally'. If this condition is satisfied, then
    the player whose pieces are in a line has won"""
    def checkRow(gD):
        """This checks rows for win condition"""
        for rw in range(5, 2, -1):  # It checks from the bottom
            for cl in range(4):  # Leave 4 items to avoid checking beyond range of list
                if gD[rw][cl] == gD[rw][cl + 1] == gD[rw][cl + 2] == gD[rw][cl + 3] != ' ':
                    print(gD[rw][cl], 'has won.\nGame starts again')
                    return True

    def checkCol(gD):
        """This checks the columns"""
        for cl in range(7):  # Checks all columns
            for rw in range(5, 2, -1):
                if gD[rw][cl] == gD[rw - 1][cl] == gD[rw - 2][cl] == gD[rw - 3][cl] != ' ':
                    print(gD[rw][cl], 'has won.\nGame starts again')
                    return True

    def checkDiag1(gD):
        """This checks the forward diagonal"""
        for rw in range(5, 2, -1):
            for cl in range(4):
                if gD[rw][cl] == gD[rw - 1][cl + 1] == gD[rw - 2][cl + 2] == gD[rw - 3][cl + 3] != ' ':
                    print(gD[rw][cl], 'has won.\nGame starts again')
                    return True

    def checkDiag2(gD):
        """This checks the reverse diagonal"""
        for rw in range(5, 2, -1):
            for cl in range(6, 2, -1):
                if gD[rw][cl] == gD[rw - 1][cl - 1] == gD[rw - 2][cl - 2] == gD[rw - 3][cl - 3] != ' ':
                    print(gD[rw][cl], 'has won.\nGame starts again')
                    return True

    if all(cell == ' ' for row in gD for cell in row):
        return False  # If board is still empty
    elif all(cell != ' ' for row in gD for cell in row):
        print('It is a draw\nGame starts again')
        gamePlay()
        # Here the board is full with no winner
    else:
        if checkRow(gD) or checkCol(gD) or checkDiag1(gD) or checkDiag2(gD):
            # Check all winning possibilities
            return True
        else:
            return False


def placeMove(gameData, col, player):
    '''This function places the entered piece at the lowest
    possible point on the list'''
    for row in range(5, -1, -1):  # Starts from the bottom of the list
        if gameData[row][col] == ' ':
            gameData[row][col] = player
            return gameData


def makeMove(player, gameData):
    '''The purpose of this fun tion is to prevent a player
    from entering data on a full column. It only allows
    placing piece on a column that has space'''
    print('Choose column for', player + ':', end=' ')
    col = dataIntake(7) - 1
    if gameData[0][col] == ' ':
        return placeMove(gameData, col, player)
    else:
        print('Column', col + 1, 'is full. Select a different column')
        return makeMove(player, gameData)


def gamePlay():
    """This function acts as a launcher for the game."""
    print('Welcome to this 2-player "Connect 4" game'
          + '\nPlayer 1 uses "X" and player 2 uses "O"'
          + '\nPress "q" or "Q" at any time to exit\n')
    player = 'X'
    while True:  # This allows for restarting the game after a win or draw
        gameData = [[' ', ' ', ' ', ' ', ' ', ' ', ' '],
                    [' ', ' ', ' ', ' ', ' ', ' ', ' '],
                    [' ', ' ', ' ', ' ', ' ', ' ', ' '],
                    [' ', ' ', ' ', ' ', ' ', ' ', ' '],
                    [' ', ' ', ' ', ' ', ' ', ' ', ' '],
                    [' ', ' ', ' ', ' ', ' ', ' ', ' ']]
        while not checkWin(gameData):
            gameData = makeMove(player, gameData)
            os.system('cls' if os.name == 'nt' else 'clear')
            drawField(gameData)
            player = 'O' if player == 'X' else 'X'


gamePlay()
