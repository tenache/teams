# -*- coding: utf-8 -*-
"""
Created on Sun Oct  3 19:31:16 2021

@author: Usuario
"""
import csv
from classes import player
def makePlayerList(playersFile):
    with open(playersFile,'r') as file:
        reader = csv.reader(file,delimiter=';')                                                                   
        readerList = list(reader)
        if ',' in readerList[0][0]:
            with open(playersFile,'r') as file:
                reader = csv.reader(file,delimiter = ',')
                readerList = list(reader)
        if readerList[0][0] == 'player':
            del readerList[0]
        playersNameList = []
        playerTalents = []
        playerPositions = []
        for element in readerList:
            playersNameList.append(element[0])
            #print(element)
            if len(element) > 1:
                playerTalents.append(int(element[1]))
            else:
                playerTalents.append(5)
            if len(element) > 2:
                positions = element[2]
                positions = positions.splitlines()
                positions = csv.reader(positions)
                positions = list(positions)[0]
                playerPositions.append(positions)
            else:
                playerPositions.append('wildCard')
    playerList = []
    for Talent,playerName,playerPos in zip(playerTalents,playersNameList,playerPositions):
        newPlayer = player(name=playerName,talent=Talent,positions=playerPos)
        playerList.append(newPlayer)
    return playerList,playersNameList,playerTalents