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
import dill
import csv
import json
class allPlayers:
    def __init__(self, user, playerList, teamLen=5, idealComp=[], lastTeams = [], allComps = [] ):
        self.user = user
        self.playersByPosition = {}
        self.teamLen = teamLen
        if idealComp:
            self.teamLen = len(idealComp)
            for position in idealComp:
                self.playersByPosition[position] = []
                for player in playerList:
                    if position in player.positions or player.positions[0] == 'wildCard':
                        self.playersByPosition[position].append(player)
        self.idealComp=idealComp
        self.playerList = playerList
        for i,player in enumerate(self.playerList):
            player.index = i
        allPlayerNames = []
        for player in self.playerList:
            allPlayerNames.append(player.name)
        self.allNames = allPlayerNames
        self.length = len(playerList)
        self.lastTeams = lastTeams
        if allComps:
            self.twoPlayer = allComps[0]
            self.threePlayer = allComps[1]
            self.fourPlayer = allComps[2]
            self.fivePlayer = allComps[3]
        else:
            self.twoPlayer = np.zeros((self.length,self.length),dtype=float)
            self.threePlayer = np.zeros((self.length,self.length,self.length),dtype=float)
            self.fourPlayer = np.zeros((self.length,self.length,self.length,self.length),dtype=float)
            self.fivePlayer = np.zeros((self.length,self.length,self.length,self.length,self.length),dtype=float)
        self.allComps = [self.twoPlayer,self.threePlayer,self.fourPlayer,self.fivePlayer]
    
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
    
    def makeTeams(self, nTeams, PlayerNames , teamLen= None, idealComp= False, reps = 10000, allPlayers = True):
        if idealComp == True:
            if teamLen != self.teamLen:
                idealComp = False
                print(f'teamLen is {teamLen} and self.teamLen is {self.teamLen}')
                print("Can't do ideal composition with different number of players than the established ideal composition.")
            else:
                idealComp = self.idealComp
        elif type(idealComp) != list:
            idealComp = None
        Players = []
        if allPlayers == True:
            Players = self.playerList
        else:
            for readyName in PlayerNames:
                if readyName in self.allNames:
                        Players.append(self.playerList[self.allNames.index(readyName)])
                elif readyName == str:
                    Players.append(player(readyName))
                elif isinstance(readyName,player):
                    self.addPlayer(readyName)
                    Players.append(readyName)
        if teamLen == None:
            teamLen = self.teamLen
        allTeamGroups = []
        allDiffScores = []
        for i in range(10):
            print(f'Patience, we\'re {i} 10ths of the way there')
            for j in range(int(reps/10)):
                teamScores = []
                teamGroup = []
                allTeamGroups.append(teamGroup)
                if idealComp:
                    groupPlayersByPosition = {}
                    for position in self.idealComp:
                        groupPlayersByPosition[position] = self.playersByPosition[position].copy()
                        for p,play in enumerate(groupPlayersByPosition[position]):
                            if play not in Players:
                                del groupPlayersByPosition[position][p]
                    positions = groupPlayersByPosition.keys()
                else:
                    positions = range(teamLen)
                groupPlayers = Players.copy()
                for i in range(nTeams):
                    teamGroup.append([])
                for team in teamGroup:
                    teamScore = 0
                    for j,pos in enumerate(positions):
                        if idealComp:
                            try:
                                randomPlayer = rd.randint(0,len(groupPlayersByPosition[pos])-1)
                                newPlayer = groupPlayersByPosition[pos].pop(randomPlayer)
                                team.append(newPlayer)
                                for pos2 in positions:
                                    for p2,play in enumerate(groupPlayersByPosition[pos2]):
                                        if newPlayer == play:
                                            del groupPlayersByPosition[pos2][p2]
                            except ValueError:
                                print(f'len(groupPlayersByPosition[{pos}])={len(groupPlayersByPosition[pos])}')
                                pass
                        else:
                            randomPlayer = rd.randint(0,len(groupPlayers)-1)
                            team.append(groupPlayers.pop(randomPlayer))
                    for player1 in team:
                        teamScore += player1.talent
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
        self.toJson()
        return bestGroup
   
    def loadWins(self):
        wins = []
        for i,team in enumerate(self.lastTeams):
            teamWins = input(f'How many wins did team {i} have?(type r for reminder,q to quit)')
            if teamWins == 'r' or teamWins=='R':
                self.remindTeams()
            elif teamWins == 'q' or teamWins == 'Q':
                return 'See you later'
            else:
                while True:
                    try:
                        teamWins = int(teamWins)
                        wins.append(teamWins)
                        break
                    except ValueError:
                        teamWins = input('please type in an integer ')
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
                        teamLosses = input('please type in an integer ')
                for player in team:
                    player.losses += teamLosses
                    player.calculateTalent()
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
        self.adjustTalent()
        self.toJson()
    
    def remindTeams(self):
        for team in range(len(self.lastTeams)):
            message = f'team {team} is: '
            for player in self.lastTeams[team]:
                message = message + str(player.name) + ' ' + str(player.index) + ' '
            print(message)
    
    def adjustTalent(self):
        bestPlayerswinMarg = self.playerList.copy()
        bestPlayerswinMarg.sort(key = op.attrgetter('winMargin'))
        for index,player in enumerate(bestPlayerswinMarg):
            if player.talent -1 < index/self.length:
                player.talent += 1
            elif player.talent + 1 > index/self.length:
                player.talent -= 1
    
    def loadPlayers(self,playersFile):
        with open(playersFile,'rb') as file:
            reader = csv.reader(file)
            playersNameList = list(reader)
        for playerName in playersNameList:
            newPlayer = player(playerName)
            self.addPlayer(newPlayer)
    
    def toJson(self):
        jsonAllComps = []
        for comp in self.allComps:
            jsonAllComps.append(json.dumps(comp.tolist()))  
        jsonPlyrs = []
        for plyr in self.playerList:
            jsonPlyrs.append(plyr.saveToJson())
        jsonLastTeams = []
        for t,team in enumerate(self.lastTeams):
            jsonLastTeams.append([])
            for plyr in team:
                jsonLastTeams[t].append(plyr.saveToJson())
        allPObj = {
            'user': self.user,
            'playerList': jsonPlyrs,
            'teamLen': self.teamLen,
            'idealComp': self.idealComp,
            'lastTeams': jsonLastTeams,
            'allComps':jsonAllComps
            }
        with open(f'{self.user}.json','w') as file:
            json.dump(allPObj,file,sort_keys = True, indent = 4)
    @staticmethod
    def loadJson(user):
        with open(f'{user}.json','r') as file:
             jsonData = json.load(file)
        plyrList = []
        for jsonPlyr in jsonData['playerList']:
            plyrList.append(player.loadFromJson(jsonPlyr))
        lstTeams = []
        for t,team in enumerate(jsonData['lastTeams']):
            lstTeams.append([])
            for jsonPlyr in team:
                lstTeams[t].append(player.loadFromJson(jsonPlyr))
        allComps = []
        for comp in jsonData['allComps']:
            allComps.append(np.array(json.loads(comp)))
        
        newAllPlayers = allPlayers(jsonData['user'],plyrList,jsonData['teamLen'],jsonData['idealComp'],\
                                   lstTeams,allComps)
        return newAllPlayers

class player:
    def __init__(self, name, talent = 50, positions=['wildCard'], wins = 0, losses = 0, index = 0):
        self.name = name
        self.talent = talent
        self.positions = positions
        self.wins = wins
        self.losses = losses
        if (self.wins + self.losses) == 0:
            self.winMargin = 0
        else:
            self.winMargin = ((self.wins -self.losses) / (self.wins + self.losses))
        self.index = index
    def calculateTalent(self):
        self.talent =  self.talent * self.winMargin
    def saveToJson(self):
        playerObject = {
            'name': self.name,
            'talent': self.talent,
            'positions': self.positions,
            'wins': self.wins,
            'losses': self.losses,
            'index': self.index,
            }
        return json.dumps(playerObject, sort_keys=True, indent = 4)
    @staticmethod
    def loadFromJson(jsonPlayerInput):
        jsonPObj = json.loads(jsonPlayerInput)
        newPlayer = player(jsonPObj['name'],jsonPObj['talent'],jsonPObj['positions'],jsonPObj['wins'],\
                           jsonPObj['losses'],jsonPObj['index'])
        return newPlayer
    
         
        
        
