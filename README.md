# teams
A program to try to create teams to allow for a more competitive match. Good for any sport. 

Often when playing pick-up like games, I've found myself in situations where we want to quickly divide into teams. Although usually this isn't a problem, I've been in groups
where a few bad apples hog all the best players. One way to avoid this is to completely randomize the teams, which we can do on an excel sheet. But since we're doing that, 
why not make a program that keeps track of all the players wins/losses, thus deliberately avoiding lob-sided games? Since we're at it, let's take into account the performance 
of certain combinations of players. For example, in basketball, you might have one big strong guy that plays well as a center, and one small guy that plays well as a point-guard
who separately are OK, but together are unbeatable (thus creating lob-sided and boring results). The program will take the profficiency of all combinations of players into account. 

## Getting started 
 In order to get started, you can use the main function, but you want to get to know the methods and functions in order to make use of everything in the package. 
 To get started, you need a csv file named 'players.csv', which will have one column with the players names on them, one column with their 'talents' (initially you will 
 be required to subjectively rate them, but this rating will change as players win or loose more than their share). Talents should be regarded ideally as a percentile, so 
 a talent score of 50 means that there are approximately half of the players are better, while half are worse. On the other hand, a talent score of 100 means this player is
 better than all the other players uploaded. Try not to be too kind, at the end, around half of the players should have scores above 50, and the other half below 50 for the program 
 to work ideally. In the third column you should include a list of the players possible positions (for example: center,power_forward, or : point_guard,shooting_guard). 
 If a player can play in any position you can put the word wildCard. The last two columns are optional, as you only require the first. If there is no second or third column, the
 default is for talent: 50, and for positions: wildCard. 
 two columns are optional. If the 
 The program should save the results in a file with the name of the user {username}.pkl. 
 ## The classes
 ### Class player
 Class player has the following attributes:
 1. name
 2. talent (initially taken from the csv file, later adjusted according to wins/losses)
 3. positions (taken also from the csv file)
 4. wins 
 5. losses
 6. winMargin (which is (wins - losses)/(wins+losses))
 It also has the method: calculateTalent, which updated the talent according to wins and losses. : 
 ### Class allPlayers
 This class summarizes the data of all players in a group. In addition to the list of players in the group, it has the ideal composition.
 The default, in the main is: center, powerForward,smallForward, shootingGuard,pointGuard. This is of course, thinking about basketball, but you can make your own list, for example, for football, you can have : defense,defense,midfielder,attacker,goalkeeper. You can load any team you like. The main method inside the class is 
 makeTeams. This method take a list of names, which are the available players from the group, and gives back two teams, which are the closes in terms of strength. Actually, it can give back as many teams as you like, as long as there are enough players to form these teams (just adjsut the parameter nTeams = number of teams required). You can also load TeamLen (in basketball, it is common to play 2 on 2, 3 on 3s, 4 on 4s, as many times there aren't enough players, so you can adjust there parameter: teamLen according to the number of players available). You can also change the parameter idealComp= True means the program will stick to the ideal composition you loaded earlier, while idealComp = False will not take positions into accoutn at all. 
 Also part of the attributes of the allPlayers class is numpy arrays that indicate how well players do. The program will keep track of how well each player does in combination of up to five other players.  
  For example, let's say team1 : Catelyn, Cersei, Jon, Robert and Ned beats team2: Renly, Stannis, Robb, Arya and Sansa. 
  The score for Catelyn (and each of that team) will go up. Also, Catelyn-Cersei combination will go up, Catelyn-Cersei-Jon combination, Catelyn-Cersei-Jon-Robert and Catelyn-Cersei-Jon-Ned. Each will go up by one, and the program will take each of these numbers into account next times it's creating teams. 
  Now let's say the next game is as follows: team 1: Catelyn,Renly,Robert,Arya and Sansa, team2: Stannis,Robb,Jon, Ned and Cersei. Team 1 wins again, so now Catelyn's score has gone up by 2, as well as the Catelyn-Robert score, but all the other combinations including Catelyn stay the same. 
  #### uploadWins() method
  In the main function, this immediately asks you who won. This is of course impractical, but if you want to load wins and losses at any moment, just access the allPlayer class instance main created for you earlier, and call allPlayerInstance.uploadWins(). The questions will appear in the console: how many wins did each team have, and how many losses (this is in case there are more than two teams involved). Draws aren't counted, as they wouldn't affect anything. 
  #### save() method
  It is important to note that all the results are automatically saved in a pickle file. The main function automatically loads this pickle file, saved under the user name you gave the program, but if you need to access it yourself, you should know that this is how the program keeps track of everything. 
  #### adjustTalents() method
  This method allows for talents to be adjusted according to the nubmer of wins vs losses. Although when making the class instance of allPlayers, each player can be given a talent, the objective is to try to eliminate subjectivity as much as possible. Essentially, what this method does is assess if the player is in the correct percentile (which is what .talent attribute represents). If it isn't it will add or substract 1 from the player's talent accordingly. Why 1? Well, especially at first we don't want to be all over the place with the talents, taking into account the effect of small sample sizes. 
  
 
 
 
