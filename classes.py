# -*- coding: utf-8 -*-
"""
Created on Wed Sep 29 08:22:10 2021

@author: Usuario
"""

#teams is a program that helps you choose teams semi-randomly, saving you the hassle of being
#picked last. The program actually does something similar to that, but you won't actually know. 
#The program takes into account wins to evaluate a players profficiency. It also takes into account
#the role of the player/position. This is tricky, and although this will be taken into account 
# in the program, it will be very flexible with the positions, favoring wins. 
import numpy as np
import operator as op
import random as rd
class allPlayers:
    def __init__(self,playerList,teamLen,idealComp=[]):
        self.idealComp=idealComp
        self.teamLen = teamLen
        self.playerList = playerList
        for i,player in enumerate(self.playerList):
            player.index = i
        self.length = len(playerList)
        self.lastTeams = []
        self.twoPlayer = np.zeros((self.length,self.length),dtype=float)
        self.threePlayer = np.zeros((self.length,self.length,self.length),dtype=float)
        self.fourPlayer = np.zeros((self.length,self.length,self.length,self.length),dtype=float)
        self.fivePlayer = np.zeros((self.length,self.length,self.length,self.length,self.length),dtype=float)
    def addPlayer(self,player):
        self.playerList.append(player)
        self.length += 1
        newTwoPlayer = np.zeros((self.length,self.length),dtype=float)
        newTwoPlayer[0:self.length-1,0:self.length-1] = self.twoPlayer
        self.twoPlayer = newTwoPlayer
        newThreePlayer = np.zeros((self.length,self.length,self.length),dtype=float)
        newThreePlayer[0:self.length-1,0:self.length-1,0:self.length-1]=self.threePlayer
        self.threePlayer = newThreePlayer
        newFourPlayer = np.zeros((self.length,self.length,self.length,self.length),dtype=float)
        newFourPlayer[0:self.length-1,0:self.length-1,0:self.length-1,0:self.length-1] = self.fourPlayer
        self.fourPlayer = newFourPlayer
        newFivePlayer = np.zeros((self.length,self.length,self.length,self.length,self.length),dtype=float)
        newFivePlayer[0:self.length-1,0:self.length-1,0:self.length-1,0:self.length-1,0:self.length-1] = self.fivePlayer
        self.fivePlayer = newFivePlayer
    def makeTeams(self,nTeams,PlayerNames,teamLen=None,idealComp=None):
        Players = []
        for readyName in PlayerNames:
            for player in self.playerList:
                if player.name == readyName:
                    Players.append(player)
        if teamLen == None:
            teamLen = self.teamLen
        allTeamGroups = []
        allDiffScores = []
        for i in range(1000):
            teamScores = []
            teamGroup = []
            allTeamGroups.append(teamGroup)
            for i in range(nTeams):
                groupPlayers = Players.copy()
                teamGroup.append([])
            for team in teamGroup:
                teamScore = 0
                for j in range(teamLen):
                    randomPlayer = rd.randint(0,len(groupPlayers)-1)
                    team.append(groupPlayers.pop(randomPlayer))
                for player1 in team:
                    teamScore += player.talent
                    idx1 = player1.index
                    for player2 in team:
                        idx2 = player2.index
                        teamScore += self.twoPlayer[idx1,idx2]
                        if teamLen > 2:
                            for player3 in team:
                                idx3=player3.index
                                teamScore += self.threePlayer[idx1,idx2,idx3]
                                if teamLen > 3:
                                    for player4 in team:
                                        idx4=player4.index
                                        teamScore += self.fourPlayer[idx1,idx2,idx3,idx4]
                                        if teamLen > 4:
                                            for player5 in team:
                                                idx5 = player5.index
                                                teamScore += self.fivePlayer[idx1,idx2,idx3,idx4,idx5]
                teamScores.append(teamScore)
            diffScore = 0
            for score0 in teamScores:
                for score1 in teamScores:
                    diff = abs(score0 - score1)
                    diffScore += diff
            allDiffScores.append(diffScore)
        minDiffScores = min(allDiffScores)
        bestGroupIndexES = []
        for scoreDiff in allDiffScores:
            if scoreDiff == minDiffScores:
                bestGroupIndexES.append(allDiffScores.index(scoreDiff))
        bestGroupIndex = rd.choices(bestGroupIndexES)[0]
        bestGroup = allTeamGroups[bestGroupIndex]
        self.lastTeams = bestGroup
        self.remindTeams()

        return bestGroup
    def loadWins(self):
        wins = []
        for i,team in enumerate(self.lastTeams):
            teamWins = input(f'How many wins did team {i} have?(type r for reminder)')
            if teamWins == 'r' or teamWins=='R':
                self.remindTeams()
            else:
                while True:
                    try:
                        teamWins = int(teamWins)
                        wins.append(teamWins)
                        break
                    except ValueError:
                        teamWins = input('please type in an integer')
                for player in team:
                    player.wins += teamWins
                    idx1 = player.index
                    for player2 in team[1:]:
                        idx2 = player2.index
                        self.twoPlayer[idx1,idx2] += teamWins
                        if len(self.lastTeams[0]) > 2:
                            for player3 in team[2:]:
                                idx3 = player3.index
                                self.threePlayer[idx1,idx2,idx3] += teamWins
                                if len(self.lastTeams[0]) > 3:
                                    for player4 in team[3:]:
                                        idx4 = player4.index
                                        self.fourPlayer[idx1,idx2,idx3,idx4] += teamWins
                                        if len(self.lastTeams[0]) > 4:
                                            for player5 in team[4:]:
                                                idx5 =  player5.index
                                                self.fivePlayer[idx1,idx2,idx3,idx4,idx5] += teamWins
        losses = []
        for i,team in enumerate(self.lastTeams):
            teamLosses = input(f'How many losses did team {i} have?(type r for reminder)')
            if teamLosses == 'r' or teamLosses=='R':
                self.remindTeams()
            else:
                while True:
                    try:
                        teamLosses = int(teamLosses)
                        losses.append(teamLosses)
                        break
                    except:
                        teamLosses = input('please type in an integer')
                for player in team:
                    player.losses += teamLosses
                    idx1 = player.index
                    for player2 in team[1:]:
                        idx2 = player2.index
                        self.twoPlayer[idx1,idx2] -= teamLosses
                        if len(self.lastTeams[0]) > 2:
                            for player3 in team[2:]:
                                idx3 = player3.index
                                self.threePlayer[idx1,idx2,idx3] -= teamLosses
                                if len(self.lastTeams[0]) > 3:
                                    for player4 in team[3:]:
                                        idx4 = player4.index
                                        self.fourPlayer[idx1,idx2,idx3,idx4] -= teamLosses
                                        if len(self.lastTeams[0]) > 4:
                                            for player5 in team[4:]:
                                                idx5 =  player5.index
                                                self.fivePlayer[idx1,idx2,idx3,idx4,idx5] -= teamLosses
    def remindTeams(self):
        for team in range(len(self.lastTeams)):
            message = f'team {team} is: '
            for player in self.lastTeams[team]:
                message = message + str(player.name) + ' ' 
            print(message)
    
        
                    

class player:
    def __init__(self,name,profficiency = 1,position=['wildCard'],positionNot = []):
        self.name = name
        self.talent = profficiency
        self.position = position
        self.positionNot = positionNot
        self.wins = 0
        self.losses = 0
        self.index = 0
    def calculateTalent(self):
        self.talent * self.wins / self.losses

        