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
def main():
    players = []
    User = input('Who are you? ')
    
    try:
        allInfo = allPlayers.loadJson(User)
    except FileNotFoundError:
        players,names,talents = makePlayerList('players.csv')
        allInfo = allPlayers(user=User,playerList=players,idealComp = ['center','shootingGuard','pointGuard','powerForward','smallForward'])
        #with open('players.csv','r') as input:
        #    with open(f'{User}_players.csv','w') as output:
        #        for line in input:
        #            output.write(line)
    except FileNotFoundError:
        players, names, talents = makePlayerList('{User}_players.csv')
        allInfo = allPlayers(user=User,playerList=players,idealComp =['center','shootingGuard','pointGuard','powerForward','smallForward'])
        print(allInfo.user)
    except FileNotFoundError:
        print('please load a csv file with all the players names with the name "players.csv" or {User}_players.csv')
    finally:
        pass
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
    ideal = input('Do you wish an ideal composition, with every position correctly covered(y/n)?')
    if ideal == 'y' or ideal == 'Y':
        allInfo.makeTeams(nTeams = numberTeams,teamLen = TeamLen, PlayerNames = TodayNames, idealComp = True , allPlayers = All)
    else:
        allInfo.makeTeams(nTeams = numberTeams,teamLen = TeamLen, PlayerNames = TodayNames, idealComp = False , allPlayers = All)
        
    sleep(5)
    allInfo.loadWins()
    allInfo.toJson()
if __name__ == '__main__':
    main()
    