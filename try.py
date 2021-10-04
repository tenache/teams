# -*- coding: utf-8 -*-
"""
Created on Wed Sep 29 20:45:17 2021

@author: Usuario
"""
from classes import player
from classes import allPlayers
from time import sleep
import csv
import dill
from makePlayerList import makePlayerList

players = []
User = input('Who are you? ')

try:
    with open(f'{User}.pkl','rb') as file:
        allInfo = dill.load(file)
except FileNotFoundError:
    players,names,talents = makePlayerList('players.csv')
except FileNotFoundError:
    print('please load a csv file with all the players names with the name "players.csv"')
finally:
    pass

allInfo = allPlayers(user=User,playerList=players,idealComp =['center','shootingGuard','pointGuard','powerForward','smallForward'])
TeamLen = int(input('How big is each team? '))
numberTeams = int(input('How many teams? '))
TodayNames = []
keepGoing = True
All = False
while keepGoing == True:
    newName = input('Name a player participating(type "done" to finish, "all" to include everyone in your list ): ')
    if newName == 'done' or newName == 'Done':
           keepGoing = False 
    elif newName == 'all' or newName == 'All':
        keepGoing = False
        All = True
    else:
        if newName in allInfo.allNames:
            TodayNames.append(newName)
        else:
            isGuest = input('is {newName} a gest or a typo(g/t)?')
            if isGuest == 'G' or isGuest == 'g':
                TodayNames.append(newName)
            elif isGuest == 't' or isGuest == 'T':
                while newName not in allInfo.allNames:
                    newName = input('Typo! No problem. Try again ...')
                    TodayNames.append(newName)

allInfo.makeTeams(nTeams = numberTeams,teamLen = TeamLen, PlayerNames = TodayNames, idealComp = True , allPlayers = All)
sleep(5)
allInfo.loadWins()
allInfo.save()

    